"""Import the QA member's edited Excel (Test Cases sheet, Test Steps column) as the step draft that drives execution.

  python runtime/qaos_import.py <file.xlsx> --run <run_dir> [--app snd] [--apply] [--approved-by "<who>"]

Reads the sheet "Test Cases": one row per case (TestCase#, Test Screen, Test Scenario, Description, Pre-Requisite, Test Steps,
Test Data, Expected Result, Priority). Each line of Test Steps is "<n>. [<Actor>] <step in the standard wording>".
Every step is checked with runtime/qaos_steps.py (verb, roles, screens, field/button labels against the real screen).
Without --apply nothing is written: it prints the problems (case, step number, reason, closest labels) and the differences to the current draft.
With --apply (only when there are no problems) it replaces <run>/step_draft_<TC>.json (the old one goes to <run>/history/) and marks the
approval as "imported from Excel"; pass --approved-by only when the QA member has said in chat that the steps are final.
Exit code 0 = no problems.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys

from openpyxl import load_workbook

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qaos_steps as Q  # noqa: E402

LINE = re.compile(r'^\s*(\d+)\s*[.)]\s*(?:\[(?P<actor>[^\]]+)\]\s*)?(?P<step>.+?)\s*$')


def cell_lines(v):
    return [x for x in (str(v).splitlines() if v not in (None, '') else []) if x.strip()]


def read_cases(path):
    wb = load_workbook(path, data_only=True)
    if 'Test Cases' not in wb.sheetnames:
        sys.exit('sheet "Test Cases" not found (sheets: ' + ', '.join(wb.sheetnames) + ')')
    ws = wb['Test Cases']
    head = {str(c.value).strip(): i for i, c in enumerate(ws[1]) if c.value}
    need = ['TestCase#', 'Test Steps']
    for n in need:
        if n not in head:
            sys.exit(f'column "{n}" not found in the Test Cases sheet (columns: {", ".join(head)})')
    cases = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        g = lambda k: r[head[k]] if k in head and head[k] < len(r) else None
        if not g('TestCase#'):
            continue
        cases.append({'id': str(g('TestCase#')).strip(), 'screen': g('Test Screen'), 'scenario': g('Test Scenario'), 'title': g('Description'),
                      'preconditions': [x.lstrip('- ').strip() for x in cell_lines(g('Pre-Requisite'))], 'steps_text': cell_lines(g('Test Steps')),
                      'data': dict((k.strip(), v.strip()) for k, _, v in (x.partition(' = ') for x in cell_lines(g('Test Data'))) if v),
                      'expected': g('Expected Result'), 'priority': g('Priority')})
    return cases


def build(case, app):
    """-> (steps, problems). Steps use the same entry shape as qaos_steps.add()."""
    steps, problems, ctx, prev_actor = [], [], None, None
    for raw in case['steps_text']:
        m = LINE.match(raw)
        if not m:
            problems.append({'line': raw.strip(), 'reason': 'not in the form "<n>. [<Actor>] <step>"'})
            continue
        actor = (m.group('actor') or prev_actor or '').strip()
        text = m.group('step').strip()
        r = Q.check(text, app, ctx)
        if not r['ok']:
            problems.append({'n': int(m.group(1)), 'step': text, 'reason': '; '.join(r['problems']), 'try': r.get('try')})
            continue
        if r['verb'] in ('login', 'switch_user'):
            actor = r['slots']['role']
        ctx = r['screen'] or ctx
        prev_actor = actor
        steps.append({'n': len(steps) + 1, 'actor': actor, 'step': text, 'verb': r['verb'], 'slots': r['slots'], 'risk': r['risk'], 'screen': r['screen'] or ctx,
                      'expect': None, 'note': None, 'raw': raw.strip(), 'state': 'clear' if not r['warnings'] else 'unverified', 'warnings': r['warnings']})
    return steps, problems


def diff(old, new):
    o, n = [s['step'] for s in old], [s['step'] for s in new]
    out = []
    for i in range(max(len(o), len(n))):
        a = o[i] if i < len(o) else None
        b = n[i] if i < len(n) else None
        if a != b:
            out.append(f"step {i + 1}: {'(none)' if a is None else a}  ->  {'(none)' if b is None else b}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('xlsx')
    ap.add_argument('--run', required=True)
    ap.add_argument('--app', default='snd')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--approved-by')
    a = ap.parse_args()
    bad = 0
    for case in read_cases(a.xlsx):
        steps, problems = build(case, a.app)
        p = os.path.join(a.run, f"step_draft_{case['id']}.json")
        old = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {'steps': [], 'case': {}}
        ch = diff(old['steps'], steps) if not problems else []      # step numbers shift when a line is invalid: no diff until fixed
        print(f"\n== {case['id']}: {len(case['steps_text'])} line(s) read, {len(steps)} valid step(s), {len(problems)} problem(s)"
              + ('' if problems else f", {len(ch)} change(s) vs the current draft"))
        for x in problems:
            print('  PROBLEM', (f"step {x['n']}: " if 'n' in x else '') + (x.get('step') or x['line']) + '\n          -> ' + x['reason'] + (f"  (try: {x['try']})" if x.get('try') else ''))
        if problems:
            print('  (the list of changes is shown once the problems are fixed)')
        for c in ch[:25]:
            print('  CHANGED', c)
        for st in steps:
            for w in st['warnings']:
                print(f"  CHECK  step {st['n']}: {w}")
        if problems:
            bad += 1
            continue
        lint_path = os.path.join(a.run, f".import_{case['id']}.json")
        json.dump({'steps': steps}, open(lint_path, 'w', encoding='utf-8'))
        lint = Q.lint(lint_path, a.app)
        os.remove(lint_path)
        for w in lint['warnings']:
            print('  warning', w)
        if lint['problems']:
            bad += 1
            for x in lint['problems']:
                print('  PROBLEM', x)
            continue
        if not a.apply:
            print('  (dry run: nothing written; add --apply to replace the draft)')
            continue
        os.makedirs(os.path.join(a.run, 'history'), exist_ok=True)
        if os.path.exists(p):
            shutil.copy(p, os.path.join(a.run, 'history', f"step_draft_{case['id']}_{datetime.datetime.now():%Y%m%d-%H%M%S}.json"))
        oc = old.get('case', {})
        new_case = {**oc, 'id': case['id'], 'screen': case['screen'] or oc.get('screen'), 'scenario': case['scenario'] or oc.get('scenario'),
                    'title': case['title'] or oc.get('title'), 'preconditions': case['preconditions'] or oc.get('preconditions', []),
                    'expected': case['expected'] or oc.get('expected'), 'priority': case['priority'] or oc.get('priority'), 'data': case['data'] or oc.get('data', {})}
        if ch and len(steps) != len(old['steps']):
            new_case['flow_map_stale'] = True          # the step ranges of the framework mapping no longer match
        approval = ({'gate': 'G3', 'status': 'approved (Excel import)', 'by': a.approved_by, 'date': datetime.date.today().isoformat(),
                     'note': 'the QA member edited the Test Steps column and confirmed the steps are final'} if a.approved_by else
                    {'gate': 'G3', 'status': 'imported from Excel, not yet confirmed as final', 'by': '', 'date': datetime.date.today().isoformat()})
        json.dump({'case': new_case, 'steps': steps, 'approval': approval}, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
        print(f"  written {p}  |  approval: {approval['status']}" + ('  |  framework mapping is now STALE (step count changed)' if new_case.get('flow_map_stale') else ''))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
