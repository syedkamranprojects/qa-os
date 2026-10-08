"""QA OS run manifest: create a run folder, record stage states, validate stage outputs and traceability.

  python runtime/qaos_run.py init SDMS-10351 --app snd [--env cnr2dev3] [--story path/to/export.html|.md]
  python runtime/qaos_run.py init QUICK-20261008-1120 --app snd --env cnr1dev1 --request "<the one-liner>" [--screens "Order Booking"]
         --market PK --run-by "<QA member name>" --maker Auto_Multi_Orga [--checker Auto_Tssm] [--allow "save"]
         (quick run: the run context is REQUIRED - confirmed with the QA member first (quick-script Q0) - and checked
          against apps/<app>/app.yaml; it is stored in run.json "context" and printed in the generated SQL header.
          Also writes requirement.json with R1 = the request, and marks stage analyse done)
  python runtime/qaos_run.py stage <run_dir> <stage> <state> [--out file] [--note text]
  python runtime/qaos_run.py validate <run_dir>
  python runtime/qaos_run.py status [KEY]

Run folder: runs/<KEY>/<yyyymmdd-hhmm>/  (run.json, inputs/, requirement.json, cases.json, steps.json, <KEY>_TestCases.xlsx, exec/)
"""
import argparse, datetime as dt, glob, json, os, shutil, sys
from jsonschema import Draft202012Validator

sys.stdout.reconfigure(encoding='utf-8')
QA_OS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
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
    if 'cases' in docs:
        core = [c for s in docs['cases']['sections'] if s['title'].lower().startswith('core') for c in s['cases']]
        if core:
            print(f"  {'OK ' if len(core) <= 10 else 'ERR'} core cases: {len(core)} (cap 10)")
            ok &= len(core) <= 10
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


def status(a):
    for p in sorted(glob.glob(os.path.join(QA_OS, 'runs', a.key or '*', '*', 'run.json'))):
        d = load(p)
        st = ' '.join(f"{k}:{v['state']}" for k, v in d['stages'].items() if v['state'] != 'pending')
        print(f"{d['key']:<12} {os.path.basename(os.path.dirname(p))}  {st or '(nothing run)'}")


ap = argparse.ArgumentParser()
sp = ap.add_subparsers(dest='cmd', required=True)
p = sp.add_parser('init'); p.add_argument('key'); p.add_argument('--app', required=True); p.add_argument('--env'); p.add_argument('--story')
p.add_argument('--request'); p.add_argument('--screens')
for n in ('--market', '--run-by', '--maker', '--checker', '--allow'):
    p.add_argument(n)
p = sp.add_parser('stage'); p.add_argument('run_dir'); p.add_argument('stage', choices=STAGES)
p.add_argument('state', choices=['pending', 'running', 'done', 'needs-input', 'failed', 'skipped']); p.add_argument('--out'); p.add_argument('--note')
p = sp.add_parser('validate'); p.add_argument('run_dir')
p = sp.add_parser('status'); p.add_argument('key', nargs='?')
a = ap.parse_args()
{'init': init, 'stage': stage, 'validate': validate, 'status': status}[a.cmd](a)
