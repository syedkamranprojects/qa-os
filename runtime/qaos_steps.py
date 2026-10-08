"""QA OS step checker and draft-sheet keeper (deterministic; no AI).

Claude rephrases a QA member's easy English into the standard wording; this tool checks that wording strictly against
vocabulary/core.yaml and against the real labels of the screen (apps/<app>/knowledge/screens_observed, apps/<app>/screens).

  python runtime/qaos_steps.py check  "<step>" --app snd [--screen "<Screen>"]        # parse + label check (JSON)
  python runtime/qaos_steps.py labels "<Screen>" --app snd                            # fields, buttons, tabs, grid columns
  python runtime/qaos_steps.py suggest --app snd [--after <verb id>] [--screen "<Screen>"]   # next-step options (JSON)
  python runtime/qaos_steps.py add    <draft.json> "<step>" --app snd [--actor Maker] [--expect "..."] [--note "..."] [--raw "<what the QA member typed>"]
  python runtime/qaos_steps.py undo   <draft.json>
  python runtime/qaos_steps.py render <draft.json> [--out sheet.md]                   # step sheet as a markdown table
  python runtime/qaos_steps.py lint   <draft.json> --app snd                          # whole-sheet checks
  python runtime/qaos_steps.py index --app snd                                        # rebuild the label index (after new screens are learned)
  python runtime/qaos_steps.py cheatsheet                                             # markdown of the predefined words

Exit code 0 = the step is valid, 1 = not valid (see `problems`). Labels are never guessed: unknown labels come back with the closest real ones.
"""
import argparse
import difflib
import glob
import json
import os
import re
import sys

import yaml

sys.stdout.reconfigure(encoding='utf-8')
QA_OS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(QA_OS, 'runtime'))


def vocab():
    with open(os.path.join(QA_OS, 'vocabulary', 'core.yaml'), encoding='utf-8') as f:
        return yaml.safe_load(f)['verbs']


def norm(s):
    return re.sub(r'\s+', ' ', (s or '').strip()).lower()


# ------------------------------------------------------------------ app knowledge (screens, roles)
def _labels_of(d):
    """fields / buttons / tabs / grid columns of one screen file. Understands the older observed files (lists of dicts) and the hand-written
    ones (dicts), and the LIVE_* harvest files (tabs are {name, fields, buttons, grids} objects; their content belongs to the screen)."""
    f, b, t, g = set(), set(), set(), set()

    def take(node):
        fl = node.get('fields')
        for x in (fl if isinstance(fl, list) else (fl or {}).keys() if isinstance(fl, dict) else []):
            f.add(x.get('label') if isinstance(x, dict) else x)
        bl = node.get('buttons')
        for x in (bl if isinstance(bl, list) else (bl or {}).keys() if isinstance(bl, dict) else []):
            b.add((x.get('text') or x.get('title')) if isinstance(x, dict) else x)
        for gr in node.get('grids') or []:
            for h in (gr.get('headers') or []) if isinstance(gr, dict) else []:
                h = ' '.join(str(y) for y in h) if isinstance(h, (list, tuple)) else h      # two-level headers: 'Group Sub'
                if h and not str(h).startswith('('):
                    g.add(h)
    take(d)
    for x in d.get('tabs') or []:
        if isinstance(x, dict):
            t.add(x.get('name') or x.get('text'))
            take(x)
        else:
            t.add(x)
    clean = lambda s: {x for x in s if x}
    return clean(f), clean(b), clean(t), clean(g)


def _button_risk(d):
    """{button text: risk}: LIVE harvest marks data-changing buttons 'ACTION - not clicked'; every other visible button is a read-only action."""
    out = {}
    nodes = [d] + [x for x in d.get('tabs') or [] if isinstance(x, dict)]
    for node in nodes:
        for x in node.get('buttons') or []:
            if isinstance(x, dict) and (x.get('text') or x.get('title')):
                out[x.get('text') or x.get('title')] = 'changes-data' if 'ACTION' in str(x.get('kind', '')) else 'read-only'
    return out


_cache = {}


def _observed(app):
    base = os.path.join(QA_OS, 'apps', app)
    out = []
    for p in glob.glob(os.path.join(base, 'knowledge', 'screens_observed', '*.json')) + glob.glob(os.path.join(base, 'screens', '*.json')):
        try:
            d = json.load(open(p, encoding='utf-8'))
        except Exception:
            continue
        if isinstance(d, dict):
            f, b, t, g = _labels_of(d)
            out.append({'title': d.get('title') or d.get('option_id'), 'fields': f, 'buttons': b, 'tabs': t, 'columns': g, 'button_risk': _button_risk(d),
                        'source': 'live' if os.path.basename(p).startswith('LIVE_') else 'observed'})
    return out


def build_index(app):
    """Small label index (apps/<app>/knowledge/step_labels.json): observed screens + framework atlas fields + live menu titles."""
    base = os.path.join(QA_OS, 'apps', app, 'knowledge')
    scr = _observed(app)
    ap = os.path.join(base, 'framework_atlas', 'atlas.json')
    if os.path.exists(ap):                                   # the framework's own field captions = what testers see on screen
        for sid, sc in (json.load(open(ap, encoding='utf-8')).get('screens') or {}).items():
            labels = {f['label'] for f in sc.get('fields', []) if f.get('label') and f.get('active')}
            if sc.get('name') and labels:
                scr.append({'title': sc['name'], 'fields': labels, 'buttons': set(), 'tabs': set(), 'columns': set(), 'source': 'framework-atlas'})
    titles = set()
    for mp in glob.glob(os.path.join(base, 'env', '*', 'menu.*.json')):           # live menus per environment and user
        for e in json.load(open(mp, encoding='utf-8')).get('entries', []):
            if e.get('title') and (e.get('route') or e.get('app_option')):
                titles.add(e['title'])
    fp = os.path.join(base, 'snd_menu_flat.json')
    if os.path.exists(fp):
        titles |= {m['title'] for m in json.load(open(fp, encoding='utf-8')) if isinstance(m, dict) and m.get('option_id') and m.get('title')}
    xp = os.path.join(base, 'label_extras.json')                 # labels seen live / in the framework but not yet in screens_observed
    if os.path.exists(xp):
        for title, e in json.load(open(xp, encoding='utf-8')).items():
            if title.startswith('_'):
                continue
            scr.append({'title': title, 'fields': set(), 'buttons': set(e.get('buttons', [])), 'tabs': set(e.get('tabs', [])),
                        'columns': set(e.get('columns', [])), 'button_risk': e.get('button_risk', {}), 'source': 'extras'})
    merged = {}
    for x in scr:
        if not x['title']:
            continue
        m = merged.setdefault(norm(x['title']), {'title': x['title'], 'fields': set(), 'buttons': set(), 'tabs': set(), 'columns': set(), 'sources': set(), 'button_risk': {}})
        m['button_risk'].update(x.get('button_risk', {}))
        for k in ('fields', 'buttons', 'tabs', 'columns'):
            m[k] |= x[k]
        m['sources'].add(x['source'])
    out = {'app': app, 'menu_titles': sorted(titles),
           'screens': [{k: (sorted(v) if isinstance(v, set) else v) for k, v in m.items()} for m in merged.values()]}
    json.dump(out, open(os.path.join(base, 'step_labels.json'), 'w', encoding='utf-8'), indent=0, ensure_ascii=False)
    return out


def screens(app):
    if app in _cache:
        return _cache[app]
    ip = os.path.join(QA_OS, 'apps', app, 'knowledge', 'step_labels.json')
    d = json.load(open(ip, encoding='utf-8')) if os.path.exists(ip) else build_index(app)
    obs = [{**x, **{k: set(x[k]) for k in ('fields', 'buttons', 'tabs', 'columns')}} for x in d['screens']]
    _cache[app] = (obs, d['menu_titles'])
    return _cache[app]


def find_screen(app, name):
    obs, _ = screens(app)
    hits = [s for s in obs if norm(s['title']) == norm(name)]
    if not hits:
        return None
    merged = {'title': hits[0]['title'], 'fields': set(), 'buttons': set(), 'tabs': set(), 'columns': set(), 'button_risk': {}}
    for s in hits:
        merged['button_risk'].update(s.get('button_risk', {}))                       # several files can describe one screen (per environment)
        for k in ('fields', 'buttons', 'tabs', 'columns'):
            merged[k] |= s[k]
    return merged


def screen_names(app):
    obs, menu = screens(app)
    return sorted(set(menu) | {s['title'] for s in obs if s['title']})


def roles(app):
    import qaos_config
    cfg = qaos_config.app_cfg(app)
    r = set()
    for e in (cfg.get('environments') or {}).values():
        r |= set((e.get('roles') or {}).keys())
    return sorted(r)


# ------------------------------------------------------------------ parsing
def parse_pairs(text):
    """'A = 1, B = "x, y", C = z'  ->  [('A','1'), ('B','x, y'), ('C','z')]"""
    parts, cur, q = [], '', False
    for ch in text:
        if ch == '"':
            q = not q
        if ch == ',' and not q:
            parts.append(cur)
            cur = ''
        else:
            cur += ch
    parts.append(cur)
    pairs, bad = [], []
    for p in parts:
        if '=' not in p:
            bad.append(p.strip())
            continue
        k, v = p.split('=', 1)
        pairs.append((k.strip(), v.strip().strip('"')))
    return pairs, bad


def closest(label, options):
    return difflib.get_close_matches(label, sorted(options), n=3, cutoff=0.55) if options else []


_ALIASES = {}


def aliases(app):
    """apps/<app>/knowledge/label_aliases.json: {"<Screen>": {"<caption users see>": "<label in the knowledge>"}} (also "*" for every screen)."""
    if app not in _ALIASES:
        p = os.path.join(QA_OS, 'apps', app, 'knowledge', 'label_aliases.json')
        _ALIASES[app] = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    return _ALIASES[app]


def alias_of(app, screen_title, label):
    al = aliases(app)
    for scope in (screen_title, '*'):
        for k, v in (al.get(scope) or {}).items():
            if norm(k) == norm(label):
                return v
    return None


def check_label(kind, label, scr, problems, warnings, app=None):
    """kind: fields | buttons | tabs | columns. Exact (case-insensitive) match wins; unknown labels get the closest real ones."""
    if scr is None:
        warnings.append(f'label "{label}" not verified: no screen knowledge (say which screen with --screen)')
        return
    pool = scr[kind] | (scr['columns'] if kind == 'fields' else set())
    if not pool:
        warnings.append(f'label "{label}" not verified: no {kind} recorded for screen "{scr["title"]}"')
        return
    if any(norm(x) == norm(label) for x in pool):
        return
    al = alias_of(app, scr['title'], label) if app else None
    if al and any(norm(x) == norm(al) for x in pool):
        return
    al_keys = set()
    if app:
        for scope in (scr['title'], '*'):
            al_keys |= {k for k in (aliases(app).get(scope) or {}) if not k.startswith('_')}
    sug = closest(label, pool | al_keys)
    problems.append(f'unknown {kind[:-1]} label "{label}" on "{scr["title"]}"' + (f'; closest: {", ".join(sug)}' if sug else ''))


def check(step, app, screen=None):
    step = step.strip()
    m = re.match(r'^\[([^\]]+)\]\s*', step)          # step sheets write the actor first: "[Maker] Click Save"
    actor = m.group(1).strip() if m else None
    step = step[m.end():] if m else step
    res = {'step': step, 'ok': False, 'verb': None, 'slots': {}, 'risk': None, 'expect_needed': False, 'problems': [], 'warnings': [], 'screen': screen}
    if actor:
        res['actor'] = actor
    v = vocab()
    for vid, spec in v.items():
        m = re.match(spec['pattern'], step)
        if not m:
            continue
        res.update(verb=vid, slots={k: x for k, x in m.groupdict().items() if x is not None}, risk=spec.get('risk'), expect_needed=bool(spec.get('expect')))
        break
    if not res['verb']:
        first = step.split(' ')[0].lower()
        res['problems'].append('not in the vocabulary: ' + (f'"{first}" is not a predefined verb; ' if first else '') + 'rephrase with one of the predefined forms or start with "Do:" (treated as manual)')
        res['try'] = [spec['form'] for spec in v.values() if any(first == s.split(' ')[0] for s in spec.get('says', []))][:3]
        return res
    spec, slots = v[res['verb']], res['slots']
    scr = find_screen(app, screen) if screen else None
    if screen and scr is None and res['verb'] != 'navigate':
        res['warnings'].append(f'screen "{screen}" has no observed knowledge: labels cannot be verified yet')
    if res['verb'] in ('add_line', 'add_loss') and scr:      # line fields live on the tab's own screens ("<Screen> Detail", "<Screen> Detail2", "<Screen> Loss")
        obs, _ = screens(app)
        pre = norm(scr['title'])
        merged = {k: set(scr[k]) for k in ('fields', 'buttons', 'tabs', 'columns')}
        merged['title'] = scr['title'] + ' (+ detail screens)'
        for x in obs:
            t = norm(x['title'] or '')
            if t.startswith(pre + ' detail') or t.startswith(pre + ' loss') or t.startswith(pre + ' line'):
                for k in ('fields', 'buttons', 'tabs', 'columns'):
                    merged[k] |= x[k]
        scr = merged
    types = spec.get('slots') or {}
    for slot, kind in types.items():
        val = slots.get(slot)
        if kind == 'Role':
            known = roles(app)
            if val and known and norm(val) not in [norm(r) for r in known]:
                res['problems'].append(f'unknown role "{val}"; roles: {", ".join(known)}')
        elif kind == 'Screen' and val:
            names = screen_names(app)
            if not any(norm(n) == norm(val) for n in names):
                sug = closest(val, names)
                res['problems'].append(f'unknown screen "{val}"' + (f'; closest: {", ".join(sug)}' if sug else ''))
            else:
                scr = find_screen(app, val)
                res['screen'] = val
                if scr is None:
                    res['warnings'].append(f'screen "{val}" exists in the menu but has no observed field knowledge yet')
        elif kind == 'Tab' and val:
            if scr and scr['tabs']:
                check_label('tabs', val, scr, res['problems'], res['warnings'], app)
        elif kind == 'Field':
            if slot == 'pairs':
                pairs, bad = parse_pairs(val)
                for b in bad:
                    res['problems'].append(f'"{b}" is not "Field = value"')
                slots['pairs'] = pairs
                for k, _ in pairs:
                    check_label('fields', k, scr, res['problems'], res['warnings'], app)
            elif val:
                check_label('fields', val, scr, res['problems'], res['warnings'], app)
        elif kind == 'Column' and val:
            check_label('columns', val, scr, res['problems'], res['warnings'], app)
        elif kind == 'Button' and val:
            check_label('buttons', val, scr, res['problems'], res['warnings'], app)
    doc = slots.get('doc')
    if doc and res['verb'] != 'verify_listed':
        names = screen_names(app)
        nd = norm(doc)
        known = any(nd == norm(t) or nd.startswith(norm(t) + ' ') for t in names)
        single = ' ' not in doc.strip()                               # a remembered name such as DA1
        if not known and not single:
            base = re.sub(r'\s+[A-Za-z]*\d+[A-Za-z0-9_]*$', '', doc.strip())   # drop a trailing remembered name / number
            if not any(norm(base) == norm(t) for t in names):
                sug = closest(base, names)
                res['warnings'].append(f'document name "{doc}" is not a known screen/document name' + (f'; closest: {", ".join(sug)}' if sug else ''))
    if res['verb'] == 'click' and scr and slots.get('button'):
        br = {k.lower(): v for k, v in (scr.get('button_risk') or {}).items()}
        if slots['button'].lower() in br:
            res['risk'] = br[slots['button'].lower()]
            res['expect_needed'] = res['risk'] != 'read-only'
    if res['verb'] == 'remember' and slots.get('name') and slots['name'] != slots['name'].upper() and not re.match(r'^[A-Z][A-Za-z0-9_]*$', slots['name']):
        res['warnings'].append('name should start with a capital letter (e.g. DA1)')
    res['ok'] = not res['problems']
    res['form'] = spec['form']
    return res


# ------------------------------------------------------------------ suggestions
def suggest(app, after=None, screen=None):
    v = vocab()
    opts = []
    for vid in (v[after].get('next') if after in v else ['login', 'navigate']) or []:
        s = v[vid]
        opts.append({'verb': vid, 'form': s['form'], 'says': s.get('says', [])[:3]})
    scr = find_screen(app, screen) if screen else None
    if scr:
        useful = [b for b in sorted(scr['buttons']) if b and not re.match(r'^(\d+|menurollin|for-selenium)$', b)]
        for b in useful[:4]:
            opts.append({'verb': 'click', 'form': f'Click {b}', 'from': 'screen button'})
        if scr['tabs']:
            opts.append({'verb': 'go_to_tab', 'form': 'Go to tab ' + sorted(scr['tabs'])[0], 'from': 'screen tab', 'all_tabs': sorted(scr['tabs'])})
    return opts


# ------------------------------------------------------------------ draft sheet
def load(p):
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'steps': []}


def save(p, d):
    os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
    json.dump(d, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)


def add(p, step, app, actor=None, expect=None, note=None, raw=None):
    d = load(p)
    steps = d['steps']
    ctx = next((s['screen'] for s in reversed(steps) if s.get('screen')), None)
    r = check(step, app, ctx)
    if not r['ok']:
        return r
    if r['verb'] in ('login', 'switch_user'):
        actor = r['slots']['role']
    actor = actor or r.get('actor') or (steps[-1]['actor'] if steps else None)
    steps.append({'n': len(steps) + 1, 'actor': actor, 'step': r['step'], 'verb': r['verb'], 'slots': r['slots'], 'risk': r['risk'],
                  'screen': r['screen'] or ctx, 'expect': expect, 'note': note, 'raw': raw,
                  'state': 'clear' if not r['warnings'] else 'unverified', 'warnings': r['warnings']})
    save(p, d)
    r['n'] = len(steps)
    return r


def lint(p, app):
    d = load(p)
    steps, probs, warns = d['steps'], [], []
    ctx = None
    for i, s in enumerate(steps):
        r = check(s['step'], app, ctx)
        ctx = r['screen'] or ctx
        if not r['ok']:
            probs.append(f"step {s['n']}: " + '; '.join(r['problems']))
        if r['expect_needed'] and not any(x['verb'].startswith('verify') for x in steps[i + 1:i + 3]) and not s.get('expect'):
            warns.append(f"step {s['n']} ({s['verb']}): no expected result; add a Verify message / Verify status step or an Expect text")
        if r['verb'] == 'approve' and i > 0:
            makers = {x['actor'] for x in steps[:i] if x['verb'] in ('create_doc', 'add_line', 'forward')}
            if s['actor'] in makers:
                warns.append(f"step {s['n']}: approval by the same actor ({s['actor']}) that created the document; use a different user")
    for i in range(1, len(steps)):
        a, b = steps[i - 1], steps[i]
        if a['actor'] != b['actor'] and not (b['verb'] in ('login', 'switch_user') or a['verb'] in ('logout',)):
            warns.append(f"step {b['n']}: actor changes from {a['actor']} to {b['actor']} without Logout / Login as <role>")
    return {'steps': len(steps), 'problems': probs, 'warnings': warns, 'ok': not probs}


def render(p):
    d = load(p)
    out = ['| # | Actor | Step | Risk | State | Expect |', '|---|---|---|---|---|---|']
    for s in d['steps']:
        out.append(f"| {s['n']} | {s['actor'] or ''} | {s['step']} | {s['risk']} | {s.get('state', '')} | {s.get('expect') or ''} |")
    return '\n'.join(out)


def cheatsheet():
    v = vocab()
    out = ['# QA OS predefined step words', '',
           'Write each step in one of these forms. Use the label exactly as it appears on the screen. If a step does not fit, start it with `Do:` and it will be treated as manual.', '',
           '| Step form | You can say it like | Risk |', '|---|---|---|']
    for s in v.values():
        out.append(f"| `{s['form']}` | {', '.join(s.get('says', [])[:4])} | {s.get('risk', '')} |")
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['check', 'labels', 'suggest', 'add', 'undo', 'render', 'lint', 'cheatsheet', 'index'])
    ap.add_argument('arg', nargs='*')
    ap.add_argument('--app', default='snd')
    ap.add_argument('--screen')
    ap.add_argument('--after')
    ap.add_argument('--actor')
    ap.add_argument('--expect')
    ap.add_argument('--note')
    ap.add_argument('--raw', help="the QA member's original wording, kept for learning")
    ap.add_argument('--out')
    a = ap.parse_args()
    if a.cmd == 'check':
        r = check(a.arg[0], a.app, a.screen)
        print(json.dumps(r, indent=1, ensure_ascii=False))
        sys.exit(0 if r['ok'] else 1)
    if a.cmd == 'labels':
        s = find_screen(a.app, a.arg[0])
        print(json.dumps({k: sorted(v) if isinstance(v, set) else v for k, v in s.items()} if s else {'error': 'no observed knowledge for this screen', 'similar': closest(a.arg[0], screen_names(a.app))}, indent=1, ensure_ascii=False))
    elif a.cmd == 'index':
        d = build_index(a.app)
        print(f"step_labels.json: {len(d['screens'])} screens with labels, {len(d['menu_titles'])} menu titles")
    elif a.cmd == 'suggest':
        print(json.dumps(suggest(a.app, a.after, a.screen), indent=1, ensure_ascii=False))
    elif a.cmd == 'add':
        r = add(a.arg[0], a.arg[1], a.app, a.actor, a.expect, a.note, a.raw)
        print(json.dumps(r, indent=1, ensure_ascii=False))
        sys.exit(0 if r['ok'] else 1)
    elif a.cmd == 'undo':
        d = load(a.arg[0])
        if d['steps']:
            print('removed:', d['steps'].pop()['step'])
        save(a.arg[0], d)
    elif a.cmd == 'render':
        t = render(a.arg[0])
        if a.out:
            open(a.out, 'w', encoding='utf-8').write(t)
        print(t)
    elif a.cmd == 'lint':
        r = lint(a.arg[0], a.app)
        print(json.dumps(r, indent=1, ensure_ascii=False))
        sys.exit(0 if r['ok'] else 1)
    else:
        print(cheatsheet())


if __name__ == '__main__':
    main()
