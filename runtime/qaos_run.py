"""QA OS run manifest: create a run folder, record stage states, validate stage outputs and traceability.

  python runtime/qaos_run.py init SDMS-10351 --app snd [--env cnr2dev3] [--story path/to/export.html|.md]
  python runtime/qaos_run.py init QUICK-20261008-1120 --app snd --env cnr1dev1 --request "<the one-liner>" [--screens "Order Booking"]
         --market PK --run-by "<QA member name>" --maker Auto_Multi_Orga [--checker Auto_Tssm] [--allow "save"]
         (quick run: the run context is REQUIRED - confirmed with the QA member first (quick-script Q0) - and checked
          against apps/<app>/app.yaml; it is stored in run.json "context" and printed in the generated SQL header.
          Also writes requirement.json with R1 = the request, and marks stage analyse done)
  python runtime/qaos_run.py stage <run_dir> <stage> <state> [--out file] [--note text]
  python runtime/qaos_run.py validate <run_dir>      (schemas, traces, paths.json: each core case in one path, one AI case per path)
  python runtime/qaos_run.py check <run_dir> [--app snd]
         (v4 pre-run check, no browser: binds each step's element / label to the screen file (apps/<app>/screens), checks
          the event fits the widget and the data columns have values; labels each case ready / needs-data / needs-knowledge;
          writes <run>/check.json)
  python runtime/qaos_run.py status [KEY]

Run folder: runs/<KEY>/<yyyymmdd-hhmm>/  (run.json, inputs/, requirement.json, cases.json, steps.json, <KEY>_TestCases.xlsx, exec/)
"""
import argparse, datetime as dt, glob, json, os, re, shutil, sys
from jsonschema import Draft202012Validator

sys.stdout.reconfigure(encoding='utf-8')
QA_OS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from qaos_config import installation   # dev / qa installation identity (runtime/qaos_config.py mode)
SCHEMAS = os.path.join(QA_OS, 'plugins', 'qa-os', 'schemas')
STAGES = ['analyse', 'cases', 'steps', 'data', 'execute', 'scripts', 'bulk', 'verify', 'report']
OUTPUTS = {'analyse': ('requirement.json', 'requirement'), 'cases': ('cases.json', 'cases'), 'steps': ('steps.json', 'steps')}


def now():
    return dt.datetime.now().isoformat(timespec='seconds')


def load(p):
    return json.load(open(p, encoding='utf-8'))


def save(p, d):
    json.dump(d, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)


def run_context(a):
    """Quick-run context (market, env, who runs it, users), checked against the app pack. Exits on any mismatch."""
    import yaml
    missing = [n for n in ('market', 'env', 'run_by', 'maker') if not getattr(a, n)]
    if missing:
        sys.exit('quick run needs the confirmed run context: ' + ', '.join('--' + m.replace('_', '-') for m in missing)
                 + ' (ask the QA member first, quick-script Q0)')
    app = yaml.safe_load(open(os.path.join(QA_OS, 'apps', a.app, 'app.yaml'), encoding='utf-8'))
    mk, env = (app.get('markets') or {}).get(a.market), (app.get('environments') or {}).get(a.env)
    errs = []
    if not mk:
        errs.append(f"market {a.market!r} not in app.yaml (known: {', '.join(app.get('markets') or {})})")
    if not env:
        errs.append(f"env {a.env!r} not in app.yaml (known: {', '.join(app.get('environments') or {})})")
    if errs:
        sys.exit('; '.join(errs))
    if mk.get('env') and mk['env'] != a.env:
        errs.append(f"market {a.market} runs on env {mk['env']}, not {a.env}")
    if not env.get('non_production'):
        errs.append(f'env {a.env} is not marked non_production: data-changing runs are not allowed')
    roles = mk.get('roles') or env.get('roles') or {}
    users = {}
    for role, u in (('Maker', a.maker), ('Checker', a.checker)):
        if not u:
            continue
        if u not in (env.get('users') or {}):
            errs.append(f'user {u!r} is not configured on env {a.env}')
        elif roles.get(role) and u not in roles[role]:
            errs.append(f"user {u!r} is not a {role} of market {a.market} (configured: {', '.join(roles[role])})")
        cfg = (env.get('users') or {}).get(u) or {}
        users[role] = {'user': u, 'company': cfg.get('company') or mk.get('company') or env.get('company'),
                       'distributor': cfg.get('distributor') or mk.get('distributor')}
    if errs:
        sys.exit('run context rejected: ' + '; '.join(errs))
    return {'market': a.market, 'market_name': mk.get('name'), 'org': mk.get('org'), 'env': a.env, 'url': env.get('url'),
            'framework_app_id': mk.get('framework_app_id'), 'group': mk.get('group'), 'run_by': a.run_by, 'users': users,
            'allow': [x.strip() for x in (a.allow or '').split(',') if x.strip()], 'confirmed': now()}


def init(a):
    ctx = run_context(a) if a.request else None
    run = os.path.join(QA_OS, 'runs', a.key, dt.datetime.now().strftime('%Y%m%d-%H%M'))
    os.makedirs(os.path.join(run, 'inputs'), exist_ok=True)
    if a.story:
        shutil.copy(a.story, os.path.join(run, 'inputs', os.path.basename(a.story)))
    save(os.path.join(run, 'run.json'), {
        'key': a.key, 'app': a.app, 'env': a.env, 'created': now(), 'user': os.environ.get('USERNAME'),
        'installation': {k: v for k, v in installation().items() if k in ('mode', 'version')},
        'stages': {s: {'state': 'pending'} for s in STAGES}})
    if a.request:                                         # quick run: the one-liner IS the requirement (R1)
        screens = [x.strip() for x in (a.screens or '').split(';') if x.strip()]
        save(os.path.join(run, 'requirement.json'), {
            'key': a.key, 'title': a.request[:200], 'app': a.app,
            'source': {'kind': 'pasted-text', 'ref': 'quick one-liner', 'retrieved': now()},
            'rules': [{'id': 'R1', 'text': a.request, 'quote': a.request, 'source': 'request'}],
            'acceptance_criteria': [],
            'screens': [{'story_term': x, 'status': 'in-menu-not-learned', 'note': 'set by qaos_intake.py parse'} for x in screens],
            'ambiguities': []})
        d = load(os.path.join(run, 'run.json'))
        d['quick'] = True
        d['context'] = ctx
        d['env'] = ctx['env']
        d['stages']['analyse'].update({'state': 'done', 'updated': now(), 'out': 'requirement.json', 'note': 'quick: R1 = request'})
        d['stages']['bulk'].update({'state': 'skipped', 'note': 'not part of a quick run'})
        save(os.path.join(run, 'run.json'), d)
    print(os.path.relpath(run, QA_OS))


def stage(a):
    p = os.path.join(a.run_dir, 'run.json')
    d = load(p)
    d['stages'][a.stage].update({'state': a.state, 'updated': now(), **({'out': a.out} if a.out else {}),
                                 **({'note': a.note} if a.note else {})})
    save(p, d)
    print(f'{a.stage} -> {a.state}')


def validate(a):
    ok, run = True, a.run_dir
    docs = {}
    for st, (fn, schema) in OUTPUTS.items():
        f = os.path.join(run, fn)
        if not os.path.exists(f):
            print(f'  -  {fn}: not present')
            continue
        docs[st] = load(f)
        errs = list(Draft202012Validator(load(os.path.join(SCHEMAS, f'{schema}.schema.json'))).iter_errors(docs[st]))
        print(f"  {'OK ' if not errs else 'ERR'} {fn}: schema" + ('' if not errs else f' — {len(errs)} error(s)'))
        for e in errs[:10]:
            print(f'       {list(e.absolute_path)}: {e.message[:200]}')
        ok &= not errs
    fd = os.path.join(run, 'decisions.json')
    if os.path.exists(fd):
        derrs = list(Draft202012Validator(load(os.path.join(SCHEMAS, 'decisions.schema.json'))).iter_errors(load(fd)))
        print(f"  {'OK ' if not derrs else 'ERR'} decisions.json: schema" + ('' if not derrs else f' — {len(derrs)} error(s)'))
        for e in derrs[:10]:
            print(f'       {list(e.absolute_path)}: {e.message[:200]}')
        ok &= not derrs
    else:
        print('  -  decisions.json: not present (run runtime/qaos_intake.py parse)')
    if 'cases' in docs:                     # v4 decision 4.1: no fixed cap on core cases; the QA member trims at approval
        core = core_ids(docs['cases'])
        if core:
            print(f'  OK  core cases: {len(core)} (no cap, v4 4.1)')
    fp = os.path.join(run, 'paths.json')
    if os.path.exists(fp):
        perrs, pwarns = check_paths(load(fp), docs.get('cases'))
        print(f"  {'OK ' if not perrs else 'ERR'} paths.json: each core case in one path, one AI case per path in its rows"
              + ('' if not perrs else f' — {len(perrs)} error(s)'))
        for e in perrs[:20]:
            print(f'       {e}')
        for w in pwarns[:20]:
            print(f'  WARN {w}')
        ok &= not perrs
    else:
        print('  -  paths.json: not present')
    req, cases, steps = docs.get('analyse'), docs.get('cases'), docs.get('steps')
    if req and cases:
        ids = {i['id'] for k in ('rules', 'acceptance_criteria', 'scope_changes', 'preconditions') for i in req.get(k, [])}
        ids |= {a['id'] for a in req.get('ambiguities', [])}
        all_cases = [c for s in cases['sections'] for c in s['cases']]
        bad = [(c['id'], t) for c in all_cases for t in c['traces'] if t not in ids]
        covered = {t for c in all_cases for t in c['traces']}
        uncovered = [x['id'] for k in ('rules', 'acceptance_criteria', 'scope_changes') for x in req.get(k, []) if x['id'] not in covered]
        dup = {c['id'] for c in all_cases if [x['id'] for x in all_cases].count(c['id']) > 1}
        print(f"  {'OK ' if not bad else 'ERR'} traces point at requirement items" + (f' — {bad[:8]}' if bad else ''))
        print(f"  {'OK ' if not uncovered else 'WARN'} every rule/AC/scope change has a case" + (f' — uncovered: {uncovered}' if uncovered else ''))
        print(f"  {'OK ' if not dup else 'ERR'} case ids unique" + (f' — {sorted(dup)}' if dup else ''))
        ok &= not bad and not dup
        if steps:
            sids = {c['case'] for c in steps['cases']}
            missing = [c['id'] for c in all_cases if c['id'] not in sids]
            extra = sorted(sids - {c['id'] for c in all_cases})
            print(f"  {'OK ' if not missing and not extra else 'ERR'} every case has steps"
                  + (f' — missing {missing}' if missing else '') + (f' — extra {extra}' if extra else ''))
            ok &= not missing and not extra
    sys.exit(0 if ok else 1)


# ---------------------------------------------------------------- v4: paths.json and the pre-run check
# Decisions 4.1 (no cap), 5.1-5.3 (one AI case per path, negatives as data rows), 7.1/7.2 (ready / needs-data /
# needs-knowledge labels; a step not matched to the screen file waits for training). The check never opens a browser.
EVENTS = ('navigate', 'tab', 'load_data', 'set', 'choose', 'remove_tag', 'click', 'grid_filter', 'row_click', 'verify_field',
          'verify_message', 'wait', 'upload', 'download', 'login', 'logout')
DO_EVENT = {'login': 'login', 'logout': 'logout', 'navigate': 'navigate', 'enter': 'set', 'set_date': 'set', 'choose': 'choose',
            'click': 'click', 'select_row': 'row_click', 'verify_ui': 'verify_field', 'capture_message': 'verify_message',
            'wait': 'wait', 'upload': 'upload', 'download': 'download', 'capture': 'verify_field'}
NO_BIND_DO = ('harvest_menu', 'harvest_i18n', 'harvest_screen', 'harvest_grid', 'screenshot', 'verify_db', 'edit_excel', 'manual')
WIDGETS = {'text': ('text', 'textbox', 'txt', 'input', 'textarea', 'number', 'numeric', 'integer', 'decimal', 'email', 'password', 'string'),
           'masked': ('masked', 'mask', 'maskedtextbox', 'masked-text'),
           'date': ('date', 'datetime', 'dt', 'datebox', 'calendar', 'time'),
           'select': ('select', 'dropdown', 'ddl', 'combobox', 'combo', 'lookup', 'selectbox', 'type-ahead', 'typeahead',
                      'autocomplete', 'radio', 'radiogroup'),
           'tagbox': ('tagbox', 'tag', 'tags', 'multiselect', 'multi-select'),
           'checkbox': ('checkbox', 'check', 'switch', 'toggle'),
           'file': ('file', 'upload', 'fileuploader')}
EVENT_FITS = {'set': {'text', 'masked', 'date'}, 'choose': {'select', 'tagbox', 'checkbox'}, 'remove_tag': {'select', 'tagbox'},
              'row_click': {'grid'}, 'grid_filter': {'grid'}, 'click': {'button', 'tab'}, 'tab': {'tab'},
              'upload': {'button', 'file'}, 'download': {'button'}}
PREFER = {'set': ('field',), 'choose': ('field',), 'remove_tag': ('field',), 'click': ('button', 'tab'), 'tab': ('tab',),
          'row_click': ('grid',), 'grid_filter': ('grid',), 'upload': ('button', 'field'), 'download': ('button',)}
SENTENCE_EVENTS = [(re.compile(p, re.I), e) for p, e in (
    (r'^(log ?in|sign in)\b', 'login'), (r'^(log ?out|sign out)\b', 'logout'), (r'^load (the )?data\b', 'load_data'),
    (r'^(open|go to|switch to|click)\b.*\btab\b', 'tab'), (r'^(navigate|open|go to|reopen)\b', 'navigate'),
    (r'^(verify|check|confirm|see)\b.*\b(message|toast|popup|pop-up|alert|error)\b', 'verify_message'),
    (r'^(verify|check|confirm|see)\b', 'verify_field'),
    (r'^(select|pick|choose|click|double[- ]click)\b.*\b(row|record)\b', 'row_click'), (r'^(filter|search)\b', 'grid_filter'),
    (r'^(remove|cross out|deselect|unselect)\b', 'remove_tag'),
    (r'^(enter|type|set|fill|input|clear|change)\b', 'set'), (r'^(choose|pick|select|tick|untick)\b', 'choose'),
    (r'^(click|press|tap|hit)\b', 'click'), (r'^wait\b', 'wait'), (r'^upload\b', 'upload'), (r'^download\b', 'download'))]


def norm(s):
    return re.sub(r'\s+', ' ', str(s or '')).strip().lower()


def core_ids(cases):
    return [c['id'] for s in (cases or {}).get('sections', []) if s['title'].lower().startswith('core') for c in s['cases']]


def all_cases(cases):
    return [c for s in (cases or {}).get('sections', []) for c in s['cases']]


def path_list(doc):
    """paths.json is a list of paths, or {"paths": [...]}."""
    return (doc.get('paths') or []) if isinstance(doc, dict) else (doc or [])


def row_case(r):
    """A path row is a case id, or {"case": id, "CASE_TYPE": .., "EXPECTED_MESSAGE": .., "data": {..}}."""
    return r if isinstance(r, str) else (r or {}).get('case')


def path_of(doc):
    """case id -> (path id, is the AI case, the row entry)"""
    out = {}
    for p in path_list(doc):
        for r in (p.get('rows') or []) + (p.get('manual') or []):
            out.setdefault(row_case(r), (p.get('path'), row_case(r) == p.get('record'), r))
    return out


def check_paths(doc, cases):
    """-> (errors, warnings). Each core case in exactly one path (rows or manual); exactly one AI case (`record`) per
    path and it is one of the path's rows; negatives may be rows; every case named must exist in cases.json."""
    errs, warns, where = [], [], {}
    known = {c['id'] for c in all_cases(cases)} if cases else None
    for i, p in enumerate(path_list(doc)):
        pid = p.get('path') or f'#{i + 1}'
        rows = [row_case(r) for r in p.get('rows') or []]
        rec = p.get('record')
        if isinstance(rec, list):
            errs.append(f'path {pid}: exactly one AI case (record) per path, found {len(rec)}: {rec}')
        elif not rec:
            errs.append(f'path {pid}: no AI case (record)')
        elif rec not in rows:
            errs.append(f'path {pid}: AI case {rec} is not one of its rows {rows}')
        for cid in rows + [row_case(r) for r in p.get('manual') or []]:
            where.setdefault(cid, []).append(pid)
            if known is not None and cid not in known:
                errs.append(f'path {pid}: case {cid} is not in cases.json')
    for cid in core_ids(cases):
        n = where.get(cid, [])
        if len(n) != 1:
            errs.append(f'core case {cid} is in {len(n)} paths' + (f": {', '.join(n)}" if n else ''))
    core = set(core_ids(cases))
    for cid, n in where.items():
        if cid not in core and len(n) > 1:
            warns.append(f"case {cid} is in {len(n)} paths: {', '.join(n)}")
    return errs, warns


def screen_files(app, folder=None):
    """{normalised name -> screen file}: option_id, title, file name, last menu item and full menu path of
    apps/<app>/screens/*.json; apps/<app>/screens/_index.json entries (option_id, title, path, aliases, file) come first."""
    d = folder or os.path.join(QA_OS, 'apps', app, 'screens')
    out = {}
    idx = os.path.join(d, '_index.json')
    entries = []
    if os.path.exists(idx):
        try:
            x = load(idx)
        except (ValueError, OSError):
            x = []
        entries = x.get('screens', x) if isinstance(x, dict) else x
        if isinstance(entries, dict):
            entries = [{'option_id': k, **(v if isinstance(v, dict) else {})} for k, v in entries.items()]
    for e in entries if isinstance(entries, list) else []:
        if not isinstance(e, dict):
            continue
        f = e.get('file') or (f"{e['option_id']}.json" if e.get('option_id') else None)
        fp = f and os.path.join(d, os.path.basename(f))
        if fp and os.path.exists(fp):
            mp = e.get('path') if isinstance(e.get('path'), str) else ' > '.join(e.get('path') or [])
            for k in [e.get('option_id'), e.get('title'), mp] + list(e.get('aliases') or []):
                if k:
                    out.setdefault(norm(k), fp)
    for fp in sorted(glob.glob(os.path.join(d, '*.json'))):
        if os.path.basename(fp).startswith('_'):
            continue
        try:
            sc = load(fp)
        except (ValueError, OSError):                 # half-written or just replaced by the screen-file builder
            continue
        keys = [sc.get('option_id'), sc.get('title'), os.path.splitext(os.path.basename(fp))[0]]
        mp = (sc.get('menu') or {}).get('path') if isinstance(sc.get('menu'), dict) else None
        if isinstance(mp, list) and mp:
            keys += [mp[-1], ' > '.join(mp)]
        elif isinstance(mp, str) and mp:
            keys += [mp, mp.split('>')[-1]]
        for k in keys:
            if k:
                out.setdefault(norm(k), fp)
    return out


def find_screen(sfiles, name):
    if not name:
        return None
    n = norm(name)
    return sfiles.get(n) or sfiles.get(norm(re.sub(r'\s*>\s*', ' > ', n))) or sfiles.get(norm(n.split('>')[-1]))


def widget_kind(kind, w):
    if kind != 'field':
        return kind
    w = norm(w)
    for k, al in WIDGETS.items():
        if w in al:
            return k
    return w or None


def _items(x):
    """{label: {...}} or [{label, ...}] -> [(label, dict)]"""
    if isinstance(x, dict):
        return [(k, v if isinstance(v, dict) else {}) for k, v in x.items()]
    if isinstance(x, list):
        return [(i.get('label') or i.get('title') or i.get('name') or i.get('element'), i) for i in x if isinstance(i, dict)]
    return []


def _elem(v):
    loc = v.get('locator') if isinstance(v.get('locator'), dict) else {}
    return v.get('element') or v.get('id') or loc.get('id') or loc.get('xpath') or loc.get('css')


_models = {}


def screen_model(fp):
    """Elements of a screen file (contract: plugins/qa-os/schemas/screen.schema.json): fields{label: {element, widget}},
    tabs[{label, element}] (sub-tabs and per-tab fields/buttons/grids allowed), buttons, grids - dict or list form;
    older curated files keep the id under locator.id."""
    if fp in _models:
        return _models[fp]
    try:
        sc = load(fp)
    except (ValueError, OSError):
        sc = {}
    els = []

    def add(kind, label, v, tab=None):
        els.append({'kind': kind, 'label': label, 'element': _elem(v), 'tab': tab or v.get('tab'),
                    'widget': widget_kind(kind, v.get('widget') or v.get('type'))})

    def walk(tabs, parent=None):
        for label, t in _items(tabs):
            add('tab', label, t, parent)
            for k, kind in (('fields', 'field'), ('buttons', 'button'), ('grids', 'grid')):
                for lb, v in _items(t.get(k)):
                    add(kind, lb, v, label)
            walk(t.get('tabs') or t.get('sub_tabs'), label)

    for k, kind in (('fields', 'field'), ('buttons', 'button'), ('grids', 'grid')):
        for lb, v in _items(sc.get(k)):
            add(kind, lb, v)
    walk(sc.get('tabs'))
    if isinstance(sc.get('layout'), dict):
        walk(sc['layout'].get('tabs'))
    _models[fp] = {'file': os.path.relpath(fp, QA_OS).replace(os.sep, '/'), 'option_id': sc.get('option_id'),
                   'title': sc.get('title'), 'elements': [e for e in els if e['label'] or e['element']]}
    return _models[fp]


def sentence_event(text):
    t = re.sub(r'^\s*(\d+\s*[.)]\s*)?(\[[^\]]*\]\s*)?', '', str(text or ''))
    for rx, ev in SENTENCE_EVENTS:
        if rx.search(t):
            return ev
    return None


def dsl_label(s):
    """the field / button / grid label named by a v1 (`do`) step"""
    d = s.get('do')
    if d in ('enter', 'choose', 'set_date', 'capture'):
        return s.get('field')
    if d in ('click', 'download', 'upload'):
        return s.get('button')
    if d == 'select_row':
        return s.get('grid')
    if d == 'verify_ui':
        e = s.get('expect') if isinstance(s.get('expect'), dict) else {}
        return e.get('field') or e.get('button') or e.get('grid')
    return s.get('field') or s.get('button') or s.get('grid') or s.get('label')


def _words(x):
    return ' ' + re.sub(r'[^\w/%-]+', ' ', norm(x)).strip() + ' '


def bind(model, ev, element=None, label=None, sentence=None):
    els = model['elements']
    if element:
        hit = [e for e in els if e['element'] == element] or [e for e in els if norm(e['label']) == norm(element)]
        return hit[0] if hit else None
    if label:
        hit = [e for e in els if norm(e['label']) == norm(label)]
        hit.sort(key=lambda e: e['kind'] not in PREFER.get(ev, ()))
        return hit[0] if hit else None
    if sentence:                                    # the longest screen label named in the sentence, preferring the event's kind
        t = _words(sentence)
        hit = [e for e in els if e['label'] and _words(e['label']) in t]
        hit.sort(key=lambda e: (e['kind'] not in PREFER.get(ev, ()), -len(e['label'])))
        return hit[0] if hit else None
    return None


def check_case(c, defaults, sfiles, row=None, default_screen=None):
    """-> {readiness, reasons, warnings, steps}. knowledge = unmatched step / missing screen file; data = empty data column."""
    data = {**(defaults or {}), **(c.get('data') or {}), **(((row or {}).get('data') or {}) if isinstance(row, dict) else {})}
    know, need, warn, out = [], [], [], []
    cur = c.get('screen') or default_screen

    def knowledge(msg, rec):
        if msg not in know:
            know.append(msg)
        rec['status'] = 'needs-knowledge'

    for n, s in enumerate(c.get('steps') or [], 1):
        text = s.get('sentence') or ''
        ev = s.get('event') or DO_EVENT.get(s.get('do')) or sentence_event(text)
        rec = {'n': n, 'event': ev, 'status': 'ok'}
        if text:
            rec['sentence'] = text
        cols = ([s['data_column']] if s.get('data_column') else []) + re.findall(r'\{\{\s*data\.([\w-]+)\s*\}\}', json.dumps(s, ensure_ascii=False))
        for col in dict.fromkeys(cols):
            if data.get(col) in (None, ''):
                need.append(f'step {n}: data column {col!r} has no value in the data row')
                rec['status'] = 'needs-data'
        if s.get('do') in NO_BIND_DO and not s.get('event'):
            rec['status'] = 'no-binding'
            if s['do'] == 'manual':
                warn.append(f"step {n}: manual step, executed by the AI from its note: {s.get('note', '')[:80]}")
            out.append(rec)
            continue
        if not ev:
            knowledge(f'step {n}: action not recognised in "{(text or json.dumps(s, ensure_ascii=False))[:90]}"', rec)
            out.append(rec)
            continue
        if ev in ('login', 'logout', 'wait'):
            out.append(rec)
            continue
        if ev == 'verify_message':
            if not s.get('expect') and not s.get('as'):
                warn.append(f'step {n}: expected message not known yet - the AI captures it live once (12.1)')
            out.append(rec)
            continue
        if ev == 'navigate':
            target = s.get('menu') or s.get('screen') or s.get('element')
            if not target and text:
                t = _words(text)
                keys = sorted((k for k in sfiles if len(k) > 3 and _words(k) in t), key=len, reverse=True)
                target = keys[0] if keys else None
            if not target:
                knowledge(f'step {n}: navigate names no screen that has a screen file: "{text[:90]}"', rec)
                cur = None
            else:
                cur = rec['screen'] = target
                if not find_screen(sfiles, target):
                    knowledge(f'no screen file for {target!r} (train the screen first, decision 2.2)', rec)
            out.append(rec)
            continue
        scr = s.get('screen') or cur
        if not scr:
            knowledge(f'step {n}: no screen is open before this step (add a navigate step or the case screen)', rec)
            out.append(rec)
            continue
        fp = find_screen(sfiles, scr)
        rec['screen'] = scr
        if not fp:
            knowledge(f'no screen file for {scr!r} (train the screen first, decision 2.2)', rec)
            out.append(rec)
            continue
        model = screen_model(fp)
        if ev == 'load_data':
            if s.get('tab') and not bind(model, 'tab', label=s['tab']):
                knowledge(f"step {n}: tab {s['tab']!r} is not in the screen file of {model['title']}", rec)
            for el, col in (s.get('mapping') or {}).items():
                if not bind(model, 'set', element=el):
                    knowledge(f"step {n}: mapped element {el!r} is not in the screen file of {model['title']}", rec)
                if data.get(col) in (None, ''):
                    need.append(f'step {n}: data column {col!r} (load_data mapping) has no value in the data row')
            if not s.get('mapping'):
                rec['note'] = 'field mapping is filled by the AI run'
            out.append(rec)
            continue
        label = None if s.get('element') else dsl_label(s)
        if ev == 'verify_field' and not s.get('element') and not label and (s.get('do') or not text):
            out.append(rec)                          # page-level check (URL, breadcrumb): nothing to bind
            continue
        e = bind(model, ev, element=s.get('element'), label=label, sentence=None if (s.get('element') or label) else text)
        what = s.get('element') or label or text
        if not e:
            knowledge(f"step {n}: {what[:90]!r} is not on screen {model['title']} ({model['file']})", rec)
            out.append(rec)
            continue
        rec.update({'element': e['element'], 'label': e['label'], 'kind': e['kind'], 'widget': e['widget']})
        fits = EVENT_FITS.get(ev)
        if fits and e['widget'] and e['widget'] not in fits:
            knowledge(f"step {n}: {ev} does not fit {e['label']!r} ({e['widget']}; expected {'/'.join(sorted(fits))})", rec)
        elif fits and not e['widget']:
            warn.append(f"step {n}: widget of {e['label']!r} is not in the screen file; {ev} not checked")
        if not e['element']:
            warn.append(f"step {n}: {e['label']!r} has no element id in the screen file")
        out.append(rec)
    readiness = 'needs-knowledge' if know else 'needs-data' if need else 'ready'
    return {'readiness': readiness, 'reasons': know + need, 'warnings': warn, 'steps': out}


def run_check(run, app=None, cases=None, steps=None, paths=None):
    """Pre-run check of a run folder. cases / steps / paths may be passed in to check edits before they are written."""
    f = lambda n: load(os.path.join(run, n)) if os.path.exists(os.path.join(run, n)) else None
    cases = cases if cases is not None else f('cases.json')
    steps = steps if steps is not None else f('steps.json')
    paths = paths if paths is not None else f('paths.json')
    app = app or (steps or {}).get('app') or (cases or {}).get('app') or (f('run.json') or {}).get('app') or 'snd'
    sfiles = screen_files(app)
    defaults = ((steps or {}).get('defaults') or {}).get('data') or {}
    where = path_of(paths) if paths else {}
    res = {'run': os.path.relpath(os.path.abspath(run), QA_OS).replace(os.sep, '/'), 'app': app, 'checked': now(),
           'screen_files': len(set(sfiles.values())), 'cases': {}}
    if paths:
        res['paths_errors'], res['paths_warnings'] = check_paths(paths, cases)
    by_steps = {c['case']: c for c in (steps or {}).get('cases', [])}
    core = set(core_ids(cases))
    ids = [c['id'] for c in all_cases(cases)]
    for cid in ids + [k for k in by_steps if k not in ids]:
        pid, ai, row = where.get(cid, (None, False, None))
        meta = {'path': pid, 'ai_case': ai, 'core': (cid in core) if cases else None}
        if cid not in by_steps:
            res['cases'][cid] = {**meta, 'readiness': 'no-steps', 'reasons': ['no steps yet (backlog idea or not written)'],
                                 'warnings': [], 'steps': []}
            continue
        res['cases'][cid] = {**meta, **check_case(by_steps[cid], defaults, sfiles, row, (cases or {}).get('screen_name'))}
    cnt = {}
    for r in res['cases'].values():
        cnt[r['readiness']] = cnt.get(r['readiness'], 0) + 1
    res['summary'] = cnt
    return res


def print_check(res, only=None):
    print(f"pre-run check {res['run']}  (app {res['app']}, {res['screen_files']} screen file(s))")
    for e in res.get('paths_errors') or []:
        print(f'  PATHS ERR  {e}')
    for w in res.get('paths_warnings') or []:
        print(f'  PATHS WARN {w}')
    for cid, r in res['cases'].items():
        if only is not None and cid not in only:
            continue
        tag = f"{r['path'] or '-'}{' AI' if r['ai_case'] else ''}"
        print(f"  {cid:<6} {r['readiness']:<16} {tag:<7} {r['reasons'][0] if r['reasons'] else ''}")
        for x in r['reasons'][1:4]:
            print(f"  {'':<31}{x}")
        if len(r['reasons']) > 4:
            print(f"  {'':<31}... {len(r['reasons']) - 4} more (check.json)")
    print('  ' + ', '.join(f'{k} {v}' for k, v in sorted(res['summary'].items())))


def check_cmd(a):
    res = run_check(a.run_dir, a.app)
    save(os.path.join(a.run_dir, 'check.json'), res)
    print_check(res)
    print(f"  -> {os.path.join(a.run_dir, 'check.json')}")


def status(a):
    for p in sorted(glob.glob(os.path.join(QA_OS, 'runs', a.key or '*', '*', 'run.json'))):
        d = load(p)
        st = ' '.join(f"{k}:{v['state']}" for k, v in d['stages'].items() if v['state'] != 'pending')
        print(f"{d['key']:<12} {os.path.basename(os.path.dirname(p))}  {st or '(nothing run)'}")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('init'); p.add_argument('key'); p.add_argument('--app', required=True); p.add_argument('--env'); p.add_argument('--story')
    p.add_argument('--request'); p.add_argument('--screens')
    for n in ('--market', '--run-by', '--maker', '--checker', '--allow'):
        p.add_argument(n)
    p = sp.add_parser('stage'); p.add_argument('run_dir'); p.add_argument('stage', choices=STAGES)
    p.add_argument('state', choices=['pending', 'running', 'done', 'needs-input', 'failed', 'skipped']); p.add_argument('--out'); p.add_argument('--note')
    p = sp.add_parser('validate'); p.add_argument('run_dir')
    p = sp.add_parser('check'); p.add_argument('run_dir'); p.add_argument('--app')
    p = sp.add_parser('status'); p.add_argument('key', nargs='?')
    a = ap.parse_args()
    {'init': init, 'stage': stage, 'validate': validate, 'check': check_cmd, 'status': status}[a.cmd](a)


if __name__ == '__main__':
    main()
