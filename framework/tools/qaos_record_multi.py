"""QA OS recorder, multi-screen mode: watcher log -> flow spec in the shape gen_framework_sql.py expects (screens[]).

    python framework/tools/qaos_record_multi.py <recording.json> <flow_spec.json> --mg 0649
           [--flow-desc "..."] [--filename "NG_..."] [--names "Screen A;Screen B;..."]
           [--rows rows.json [--cases cases.json]] [--run <run folder>]

--rows: the data rows of ALL cases (a list of objects shaped like the recorded case's data.json, each with "case";
line items as a list of objects). The recorded case binds field -> data key by exact value; every case becomes one
row per screen (lines: one row per line, PK "01-01"); each assertion sheet gets one row per case.
--run: the run folder; its run.json "context" (market, env, run by, users - confirmed in quick-script Q0) and the
request (requirement.json R1) go into spec.run_info and are printed in the SQL header.

The recording is the ONLY source (FINAL_DESIGN v3 §9; QA lead rule 2026-10-08). The framework DB is used by the
caller only to choose a free menu-group id (--mg). Rules (HARDENING C1/C3/C4/C5/C6/C7):
 * one framework screen per page (URL path) the run visited, in order; the first is the root, the others are its
   CHILD screens (parent = root), so each case-data row runs header -> lines -> save -> result;
 * a page whose fields are grid cells is a "lines" page: grid-row buttons are children of its Load Data (once per
   line row); its other clicks and assertions are top level (once per order). On other pages every event is a child;
 * every screen gets a Load Data (serial 1); a remembered value becomes a 0010 field with repoid + a 0012 fill-repo;
 * a click that follows a toast (within 10 s) gets a wait 0000/0006 of 5 s first, so the engine does not read the
   stale toast;
 * fields are defined with the ids seen on THAT page (ids that change after a navigation stay correct);
 * widgets: type-ahead -> 0006 auto-select, dropdown -> 0002, date -> 0003, text -> 0001;
 * tabs: a recorded tab click starts a new framework screen on the same page (the first tab of a page becomes that
   page's screen); the screen's navigation is the tab: id -> type id, else its text -> linkText, else its xpath. The
   engine clicks it before the screen (Main.navigateOnTabs; convention of Outlet / DSR / Distributor Profile: Dem-1,
   Opr-1, tab_4 ...). Screens without a tab get the menu entry as path, type NULL (gen_framework_sql.py);
 * grid lines: when the watcher logged 'row' snapshots (the row's editable cells read at the row-button click), they are
   the authoritative fields and line values; the keystroke-level 'cell' entries of that grid are ignored;
 * menu navigation from the recorded sidebar click (navigation_type id);
 * toasts -> 0000/0014 TSTMSG,<sheet>; popups -> ELEVAL,<sheet>; browser alerts -> 0005/0002 accept/dismiss with
   the text listed as not asserted; a stale repeat of an earlier toast is not asserted.
Anything missing (no locator, no menu click) is reported as a GAP; nothing is guessed.
"""
import json, re, sys

WIDGET = {'dropdown': '0002', 'type-ahead': '0006', 'date': '0003'}
# sidebar controls used to reach the menu item: they are the menu navigation, not screen events
# (override per app with meta.nav_locators in the recording)
NAV_LOCATORS = {'#menurollin', 'input[name="filterText"]'}


def locate(entry, loc, label=None):
    l = loc.get(label or entry.get('label') or '', {})
    if l.get('id'):
        return l.get('locateby', 'id'), l['id']
    if entry.get('id'):
        return 'id', entry['id']
    lc = entry.get('locator') or ''
    if lc.startswith('#'):
        return 'id', lc[1:]
    if lc.startswith('//'):
        return 'xpath', lc
    return None, None


# DCODE tab / section ids seen in the framework's screen mappings (Outlet / DSR / Distributor Profile): a click on one of
# them is a tab even if the watcher logged it as a plain click
TAB_ID = re.compile(r'^(?:Dem|Opr|Oth|addr)-\d+$|^tab(?:_group)?_\d+$')


# DevExtreme generated ids (dx-<guid>) change on every page load: a click on one can never be replayed. The one seen in
# practice is the Demographics / Address drop-down toggle, which the engine opens itself (#btn_1 before Dem-1 / Opr-1).
GENERATED_ID = re.compile(r'^dx-[0-9a-f]{4,}', re.I)


def as_tab(a):
    """The log entry, with a click on a known tab id treated as a tab click."""
    return dict(a, act='tab') if a.get('act') == 'click' and TAB_ID.match(a.get('id') or '') else a


def tab_nav(a):
    """Navigation of a framework screen from a recorded tab click: (type, path) as the engine reads them."""
    if a.get('id'):
        return 'id', a['id']
    text = (a.get('value') or a.get('text') or '').strip()
    if text:
        return 'linkText', text
    lc = a.get('locator') or ''
    return ('xpath', lc) if lc.startswith('//') or lc.startswith('(') else None


def sheet_name(text):
    return re.sub(r'[^A-Z0-9]+', '_', (text or 'MSG').upper()).strip('_')[:20] + '_ASSR'


def build(log, meta, mg, flow_desc, filename, names):
    loc = meta.get('locators', {})
    pages, gaps, not_asserted, sheets, skipped = [], [], [], [], []
    cur, last_toast_t, last_click = None, None, None   # last_click: (page, serial, name, ref) across pages
    nav = next((a for a in log if a.get('act') == 'nav_click'), None)

    def page_for(url):
        nonlocal cur
        path = (url or '/').split('?')[0]
        if cur is None or cur['path'] != path:
            cur = {'path': path, 'key': path, 'url': url, 'nav': None, 'tab': None,
                   'fields': [], 'grid': False, 'seen': set(), 'last_click': None,
                   'events': [{'serial': 1, 'desc': 'Load Data', 'type': '0000', 'event': '0001', 'ref': None,
                               'evidence': 'Load Data is always serial 1'}]}
            pages.append(cur)
        return cur

    def ev(p, **e):
        e['serial'] = len(p['events']) + 1
        p['events'].append(e)
        return e['serial']

    nav_locs = set(meta.get('nav_locators') or NAV_LOCATORS)
    snap_grids = {a.get('grid') for a in log if a.get('act') == 'row'}
    for a in log:
        a = as_tab(a)
        act = a.get('act')
        if act in ('nav_click', 'nav', 'note') or a.get('locator') in nav_locs:
            continue                                     # menu navigation: goes to menu_group, not a screen
        if act == 'screen':
            page_for(a.get('url'))
            continue
        p = cur or page_for(a.get('url'))
        child = 1 if not p['grid'] else None          # event ref on this page (see rules)
        if act == 'row':
            p['grid'] = True
            for c in a.get('cells', []):
                key = (c.get('label'), a.get('grid') or '')
                if not c.get('label') or key in p['seen']:
                    continue
                p['seen'].add(key)
                by, fid = locate(c, loc, c.get('label'))
                if not fid:
                    gaps.append(f"no id/locator for grid column '{c.get('label')}'")
                    continue
                p['fields'].append({'id': fid, 'caption': c['label'], 'type': WIDGET.get(c.get('widget', ''), '0001'), 'locateby': by,
                                    'colindex': c.get('colindex'), 'grid': a.get('grid'),
                                    'evidence': f"row snapshot at {a.get('button')}: '{c.get('value')}' ({c.get('widget', '')})"})
            continue
        if a.get('grid') and a.get('grid') in snap_grids and act in ('cell', 'option'):
            continue                                     # the row snapshots carry this grid's fields and values
        if act in ('text', 'pick', 'date', 'option', 'cell'):
            label = a.get('label') or a.get('column') or ''
            if not label:
                gaps.append(f"{act} '{a.get('value', '')}' without a field label")
                continue
            if a.get('grid'):
                p['grid'] = True
            key = (label, a.get('grid') or '')
            if key in p['seen']:
                continue                                 # several values for one cell: one field
            p['seen'].add(key)
            by, fid = locate(a, loc, label)
            if not fid:
                gaps.append(f"no id/locator for field '{label}'")
                continue
            kind = WIDGET.get(a.get('widget', ''), '0002' if act in ('option', 'pick') else '0001')
            p['fields'].append({'id': fid, 'caption': label, 'type': kind, 'locateby': by, 'colindex': a.get('colindex'),
                                'grid': a.get('grid'), 'evidence': f"recorded {act} '{a.get('value', '')}' ({a.get('widget', '')})"})
        elif act == 'tab':
            tn = tab_nav(a)
            if not tn:
                gaps.append(f"tab '{a.get('value') or a.get('text')}' without id, text or xpath")
                continue
            if p['nav'] == tn:
                continue                                 # the tab already shown
            fresh = not p['fields'] and len(p['events']) == 1 and not p['nav']
            if not fresh:                                # a further tab of the same page: its own framework screen
                cur = dict(p, fields=[], grid=False, seen=set(), last_click=None,
                           events=[{'serial': 1, 'desc': 'Load Data', 'type': '0000', 'event': '0001', 'ref': None,
                                    'evidence': 'Load Data is always serial 1'}])
                pages.append(cur)
                p = cur
            p['nav'], p['tab'] = tn, (a.get('value') or a.get('text') or tn[1]).strip()
            p['key'] = p['path'] + '#' + tn[1]
            continue
        elif act in ('click', 'check'):
            if GENERATED_ID.match(a.get('id') or ''):
                skipped.append({'act': act, 'id': a.get('id'), 'text': a.get('text'),
                                'reason': 'generated id (dx-...): not replayable; tab drop-downs are opened by the engine'})
                continue
            by, fid = locate(a, loc)
            if not fid:
                gaps.append(f"no id/locator for {act} '{a.get('text') or a.get('value')}'")
                continue
            if a.get('grid') and any(e.get('field') == fid for e in p['events']):
                continue                                 # same row button for the next line: one event
            name = a.get('text') or a.get('value') or a.get('label') or fid
            ref = 1 if a.get('grid') else child
            if last_toast_t and a.get('t') and a['t'] - last_toast_t < 10000:
                ev(p, desc=f'Wait before {name}', type='0000', event='0006', fixed='5', ref=ref,
                   evidence='a toast was shown just before; let it clear (the engine reads the first toast)')
            if act == 'check':
                ev(p, desc=f'{name} Checkbox', type='0000', event='0015', locateby=by, field=fid, ref=ref,
                   evidence=f"recorded checkbox {a.get('locator') or fid}")
            else:
                s = ev(p, desc=f"{name} Button", type='0004', event='0002', locateby=by, field=fid,
                       ref=ref, evidence=f"recorded {act} on {a.get('locator') or fid}")
                p['last_click'] = (s, name, ref)
                last_click = (p, s, name, ref)
        elif act == 'toast' and a.get('messages'):
            last_toast_t = a.get('t') or last_toast_t
            msg = a['messages'][0]
            # a toast belongs to the last click, also when that click already moved the app to the next page
            if not last_click:
                gaps.append(f'toast {msg!r} without a click before it')
                continue
            cp, serial, name, ref = last_click
            mine = (cp['key'], serial)
            if any(s['click'] == mine for s in sheets):
                continue                                 # second toast of the same click: already asserted
            if any(s['expected_message'] == msg for s in sheets):
                not_asserted.append({'type': 'toast', 'text': msg, 'reason': f'repeat of an earlier message shown again after {name}'})
                continue
            sh = sheet_name(name)
            ev(cp, desc=f'Assertion {msg}', type='0000', event='0014', fixed=f'TSTMSG,{sh}', ref=ref,
               evidence=f"toast after {name}: {msg!r} ({a.get('type', '')})")
            sheets.append({'sheet': sh, 'kind': 'TSTMSG', 'expected_message': msg, 'click': mine})
        elif act == 'popup' and (a.get('title') or a.get('buttons')):
            by, fid = locate(a, loc)
            sh = sheet_name('POPUP ' + (a.get('title') or ''))
            if fid:
                ev(p, desc=f"Popup check {a.get('title') or ''}".strip(), type='0000', event='0014', fixed=f'ELEVAL,{sh}',
                   locateby=by, field=fid, ref=child, evidence=f"popup: {a.get('text')!r}")
                sheets.append({'sheet': sh, 'kind': 'ELEVAL', 'expected_message': a.get('text'), 'click': (p['key'], 'popup')})
            else:
                gaps.append(f"popup {a.get('text')!r} without a locator")
        elif act == 'alert':
            not_asserted.append({'type': 'alert', 'text': a.get('text'), 'reason': 'the engine reads but does not assert alert text'})
        elif act == 'alert_result':
            ev(p, desc=f"{(a.get('dialog') or 'alert').title()} Alert", type='0005', event='0002', locateby='id',
               field='accept' if a.get('result') else 'dismiss', ref=child, evidence=f"browser {a.get('dialog')} answered {a.get('result')}")
        elif act == 'remember':
            by, fid = locate(a, loc)
            if not fid:
                not_asserted.append({'type': 'remember', 'text': f"{a.get('name')} = {a.get('value')}",
                                     'reason': 'read from page text without a locator: recorded only'})
                continue
            p['fields'].append({'id': fid, 'caption': a.get('label') or a.get('name'), 'type': '0010', 'locateby': by,
                                'repoid': a.get('name'), 'evidence': f"remembered {a.get('value')!r} as {a.get('name')}"})
            ev(p, desc=f"Fill repository {a.get('name')}", type='0000', event='0012', ref=child, evidence=f"remember {a.get('name')}")

    pages = [p for p in pages if p['fields'] or len(p['events']) > 1]
    if not pages:
        raise SystemExit('no screens with fields or events in the recording')
    user_names = [x.strip() for x in (names or '').split(';') if x.strip()]
    screens, used = [], set()
    for i, p in enumerate(pages):
        auto = ' '.join(w.capitalize() for w in re.split(r'[-_/]+', p['path']) if w and w not in ('ngui', 'dyl', 'layout'))
        if p.get('tab'):
            auto = (auto + ' ' + p['tab']).strip()
        nm = (user_names[i] if i < len(user_names) else auto or f'Screen {i + 1}')[:31]
        while nm in used:
            nm = (nm[:27] + f' {i + 1}')[:31]
        used.add(nm)
        p['fields'].sort(key=lambda f: (1 if f.get('grid') else 0, int(f.get('colindex') or 0)))
        screens.append({'id': f'{mg}{i + 1:02d}', 'name': nm, 'type': 'Save', 'url': p['url'], 'seq': i + 1,
                        'parent': None if i == 0 else f'{mg}01',
                        'fields': [{k: v for k, v in f.items() if k not in ('colindex', 'grid')} for f in p['fields']],
                        'events': p['events'], 'page_key': p['key'],
                        **({'navigation_type': p['nav'][0], 'navigation_path': p['nav'][1]} if p.get('nav') else {})})
    if not nav or not nav.get('id'):
        gaps.append('no recorded sidebar menu click: menu navigation unknown (start the watcher before step 1 and re-record)')
    for s in sheets:
        s.pop('click', None)
    return {'story': meta.get('story'), 'tag': meta.get('tag') or f"QA-OS {meta.get('story')}", 'master_app_id': None,
            'source': 'watcher recording (qaos_record_multi.py)',
            'menu_group': {'id': mg, 'description': flow_desc[:100], 'searchtext': (nav or {}).get('search') or (nav or {}).get('value'),
                           'navigation': (nav or {}).get('id'), 'navigation_type': 'id',
                           'evidence': f"recorded sidebar click {(nav or {}).get('locator')}"},
            'flow': {'id': f'{mg}0001', 'description': flow_desc[:100], 'test_type': '2', 'filename': filename},
            'screens': screens, 'assertion_sheets': sheets, 'not_asserted': not_asserted, 'gaps': gaps,
            'skipped_clicks': skipped}


def _recorded_values(log, meta):
    """-> {(screen path, caption): [values in order]} and {screen path: [line dicts]} for grid fields."""
    nav_locs = set(meta.get('nav_locators') or NAV_LOCATORS)
    flat, lines, path, snapped, base = {}, {}, None, set(), None   # path = page key (URL path, '#tab' per tab screen)
    for a in log:
        a = as_tab(a)
        if a.get('act') == 'screen':
            url = (a.get('url') or '/').split('?')[0]
            if url != base:
                base = path = url
            continue
        if a.get('act') == 'tab':
            tn = tab_nav(a)
            if tn and base is not None:
                path = base + '#' + tn[1]
            continue
        if a.get('act') == 'row':
            if path not in snapped:
                snapped.add(path); lines[path] = []
            lines[path].append({c['label']: c.get('value') for c in a.get('cells', []) if c.get('label')})
            continue
        if path in snapped and a.get('grid'):
            continue
        if a.get('act') not in ('text', 'pick', 'date', 'option', 'cell') or a.get('locator') in nav_locs:
            continue
        label = a.get('label') or a.get('column')
        if not label:
            continue
        if a.get('grid'):
            if a.get('act') == 'option':
                continue                                 # the pick's display text; the typed code is the data
            L = lines.setdefault(path, [])
            # a new line starts when the line's first column is typed again (cells hold their LAST value)
            if not L or (label == next(iter(L[0])) and label in L[-1]):
                L.append({})
            L[-1][label] = a.get('value')
        else:
            flat.setdefault((path, label), []).append(a.get('value'))
    return flat, lines


def same(recorded, data):
    """Recorded value vs data value: equal text, equal numbers ('01' == 1), or the app's pick text '<code>-<description>'."""
    r, d = str(recorded if recorded is not None else '').strip(), str(data if data is not None else '').strip()
    if r == d:
        return True
    try:
        return float(r) == float(d)
    except ValueError:
        return bool(d) and r.startswith(d + '-')


def casedata(spec, log, meta, rows, titles):
    """Case-data sheets for N cases from ONE recording: each recorded field is bound to the data key whose value in
    the recorded case equals what was typed/picked (exact match only); the binding is then applied to every case.
    A field that binds to no key (or to several) is a gap and its sheet is left header-only."""
    flat, lines = _recorded_values(log, meta)
    case_id = meta.get('case') or meta.get('test_case')
    rec = next((r for r in rows if r.get('case') == case_id), rows[0] if len(rows) == 1 else None)
    if rec is None:
        spec['gaps'].append(f'case data: the recorded case {case_id!r} is not in the rows file; cannot bind fields')
        return
    path_of = {s['id']: s.get('page_key') or (s.get('url') or '/').split('?')[0] for s in spec['screens']}
    line_key = next((k for k, v in rec.items() if isinstance(v, list) and v and isinstance(v[0], dict)), None)
    out = []
    for sc in spec['screens']:
        caps = [f['caption'] for f in sc['fields'] if f['type'] != '0010']
        path, binding, bad = path_of[sc['id']], {}, []
        grid_lines = lines.get(path) or []
        for c in caps:
            if grid_lines and any(c in l for l in grid_lines):
                rl = rec.get(line_key) or []
                got = [l.get(c) for l in grid_lines]
                keys = [k for k in (rl[0].keys() if rl else []) if len(rl) == len(got) and
                        all(same(g, x.get(k)) for x, g in zip(rl, got))]
            else:
                vals = [str(v) for v in flat.get((path, c), [])]
                keys = [k for k, v in rec.items() if not isinstance(v, (list, dict)) and any(same(x, v) for x in vals) and k != 'case']
            if len(keys) == 1:
                binding[c] = keys[0]
            else:
                bad.append(f"{c} ({'no' if not keys else 'several'} data key(s) match the recorded value{'' if not keys else ': ' + ', '.join(keys)})")
        if bad:
            spec['gaps'].append(f"case data sheet {sc['name']!r} left header-only: " + '; '.join(bad))
            continue
        cols, data = SCREEN_COLS + caps, []
        is_lines = bool(grid_lines) and caps
        for i, r in enumerate(rows, 1):
            title = f"{r.get('case')} {titles.get(r.get('case'), '')}".strip()
            if is_lines:
                for j, ln in enumerate(r.get(line_key) or [], 1):
                    data.append([f'{i:02d}-{j:02d}', f'{r.get("case")} line {j}', 'TN', 'N'] + [str(ln.get(binding[c], '')) for c in caps])
            else:
                data.append([f'{i:02d}', title, 'TN', 'N'] + [str(r.get(binding[c], '')) for c in caps])
        out.append({'sheet': sc['name'], 'columns': cols, 'rows': data})
    for s in spec['assertion_sheets']:
        out.append({'sheet': s['sheet'], 'columns': ['PK', 'CASE_TYPE', 'EXPECTED_MESSAGE'],
                    'rows': [[f'{i:02d}', 'TN', s['expected_message']] for i in range(1, len(rows) + 1)]})
    spec['casedata'] = {'sheets': out, 'binding_source': f'recorded case {rec.get("case")}: exact value match'}


SCREEN_COLS = ['PK', 'PK_DESC', 'CASE_TYPE', 'STPONERR']


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    def arg(n, d=None):
        return sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
    rec = json.load(open(sys.argv[1], encoding='utf-8'))
    meta = rec.get('meta', {})
    spec = build(rec['log'], meta, arg('--mg', '9999'), arg('--flow-desc', f"QA OS {meta.get('story', 'flow')}"),
                 arg('--filename', f"NG_QAOS_{meta.get('story', 'FLOW')}"), arg('--names'))
    if arg('--rows'):
        rows = json.load(open(arg('--rows'), encoding='utf-8'))
        rows = rows if isinstance(rows, list) else rows.get('rows', [rows])
        titles = {}
        if arg('--cases'):
            cj = json.load(open(arg('--cases'), encoding='utf-8'))
            titles = {c['id']: c.get('title', '') for s in cj.get('sections', []) for c in s.get('cases', [])}
        casedata(spec, rec['log'], meta, rows, titles)
    if arg('--run'):
        import os
        rd = arg('--run')
        rj = json.load(open(os.path.join(rd, 'run.json'), encoding='utf-8'))
        if not rj.get('context'):
            spec['gaps'].append('run.json has no confirmed run context (market/env/run by/users): run quick-script Q0')
        if meta.get('story') and rj.get('key') != meta.get('story'):
            spec['gaps'].append(f"recording belongs to {meta.get('story')!r}, run folder is {rj.get('key')!r}")
        req = os.path.join(rd, 'requirement.json')
        rq = json.load(open(req, encoding='utf-8')) if os.path.exists(req) else {}
        spec['run_info'] = dict(rj.get('context') or {}, key=rj.get('key'), app=rj.get('app'),
                                request=next((r['text'] for r in rq.get('rules', []) if r.get('id') == 'R1'), None),
                                executed_case=meta.get('case'), recording=os.path.basename(sys.argv[1]),
                                cases=len(json.load(open(arg('--rows'), encoding='utf-8'))) if arg('--rows') else None)
    json.dump(spec, open(sys.argv[2], 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    print(f"{len(spec['screens'])} screens: " + '; '.join(
        f"{s['id']} {s['name']} [{len(s['fields'])} fields, {len(s['events'])} events, parent {s['parent']}]" for s in spec['screens'])
        + f" | {len(spec['assertion_sheets'])} assertion sheets | {len(spec['gaps'])} gaps")
    for g in spec['gaps']:
        print('  GAP:', g)
