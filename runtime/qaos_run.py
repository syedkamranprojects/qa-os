"""QA OS run manifest: create a run folder, record stage states, validate stage outputs and traceability.

  python runtime/qaos_run.py init SDMS-10351 --app snd [--env cnr2dev3] [--story path/to/export.html|.md]
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


def init(a):
    run = os.path.join(QA_OS, 'runs', a.key, dt.datetime.now().strftime('%Y%m%d-%H%M'))
    os.makedirs(os.path.join(run, 'inputs'), exist_ok=True)
    if a.story:
        shutil.copy(a.story, os.path.join(run, 'inputs', os.path.basename(a.story)))
    save(os.path.join(run, 'run.json'), {
        'key': a.key, 'app': a.app, 'env': a.env, 'created': now(), 'user': os.environ.get('USERNAME'),
        'stages': {s: {'state': 'pending'} for s in STAGES}})
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
p = sp.add_parser('stage'); p.add_argument('run_dir'); p.add_argument('stage', choices=STAGES)
p.add_argument('state', choices=['pending', 'running', 'done', 'needs-input', 'failed']); p.add_argument('--out'); p.add_argument('--note')
p = sp.add_parser('validate'); p.add_argument('run_dir')
p = sp.add_parser('status'); p.add_argument('key', nargs='?')
a = ap.parse_args()
{'init': init, 'stage': stage, 'validate': validate, 'status': status}[a.cmd](a)
