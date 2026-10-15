"""Render the ONE approval workbook (v4, decisions 8.1 / 6.3 / 13.2) and the one-page run summary from a QA OS run folder.

  python runtime/qaos_workbook.py <run_dir>

Reads requirement.json, cases.json, steps.json, paths.json, check.json (`qaos_run.py check`) and exec/ results - each
optional except cases.json; old runs without paths.json / check.json / sentences still render.
Writes <run_dir>/<KEY>_TestCases.xlsx with sheets:
  Questions - ambiguities: question, story quote, default (used until answered), evidence, answer, parked flag,
              affected cases; cases beyond the story (BA to confirm).
  Cases     - id, title (ALT- for negatives), type, traces, path, AI case (Y), readiness + reason (check.json), priority,
              pre-requisites, expected; backlog ideas listed below as one line each.
  Steps     - case, n, sentence (plain English) + grouped / collapsible event columns event, element, data column, expect
              (filled from the steps and the screen-file binding of check.json).
  Data rows - per path: one row per case with CASE_TYPE and EXPECTED_MESSAGE plus the data columns.
  Results   - actual result / status / evidence from the newest live result per case (exec/<case>/<stamp>/).
and <run_dir>/summary.md: pass/fail per path, Jira-ready defect drafts, parked questions, next action.
Edits made by the QA member are read back with runtime/qaos_import.py.
"""
import datetime as dt
import json
import os
import re
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.styles.colors import Color
from openpyxl.worksheet.datavalidation import DataValidation

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SHEETS = ('Questions', 'Cases', 'Steps', 'Data rows', 'Results')
CASES_HEAD = ['Id', 'Title', 'Type', 'Traces', 'Path', 'AI case', 'Readiness', 'Reason', 'Priority', 'Pre-requisites', 'Expected']
STEPS_HEAD = ['Case', 'N', 'Sentence', 'Event', 'Element', 'Data column', 'Expect']
QUEST_HEAD = ['Id', 'Question', 'Story quote', 'Default (used until answered)', 'Evidence', 'Answer', 'Parked', 'Affected cases']
DATA_FIXED = ['Path', 'AI case', 'Case', 'Type', 'CASE_TYPE', 'EXPECTED_MESSAGE']
RESULT_HEAD = ['Case', 'Path', 'AI case', 'Title', 'Expected Result', 'Actual Result',
               'Test Status (Passed/Failed/Blocked/Not Executed)', 'Test Case Evidence', 'Version']
DEFAULT_CASE_TYPE = 'TN'          # framework-conventions: the team uses TN; TP only enables the ELEVLD input check


def jload(run, f):
    p = os.path.join(run, f)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


# ---------------------------------------------------------------- live results
def live_results(run):
    """newest LIVE result per case (exec/<case>/<stamp>/result.json or results.json), by modification time"""
    live = {}
    ex = os.path.join(run, 'exec')
    for case_dir in (os.listdir(ex) if os.path.isdir(ex) else []):
        cdir = os.path.join(ex, case_dir)
        if not os.path.isdir(cdir):                      # stray files (e.g. exec/results.json) are not case folders
            continue
        stamps = [s for s in os.listdir(cdir) if not s.endswith('-dry') and os.path.isdir(os.path.join(cdir, s))
                  and any(os.path.exists(os.path.join(cdir, s, f)) for f in ('result.json', 'results.json'))]
        if stamps:
            p = os.path.join(cdir, max(stamps, key=lambda s: os.path.getmtime(os.path.join(cdir, s))))
            f = os.path.join(p, 'result.json') if os.path.exists(os.path.join(p, 'result.json')) else os.path.join(p, 'results.json')
            live[case_dir] = (json.load(open(f, encoding='utf-8')), os.path.relpath(p, run))
    return live


def norm_result(res):
    """Player result.json and recorder results.json differ in shape: map both to verdict pass / fail / needs-data and
    steps [{n, do, status, detail}]. A QA-lead revised verdict (verdict_revised) wins."""
    raw = ((res.get('verdict_revised') or {}).get('verdict') or res.get('verdict') or res.get('overall')
           or res.get('result') or '')
    low = str(raw).lower()
    if low in ('pass', 'fail', 'needs-data', 'needs-verb'):
        verdict = low
    elif low.startswith('pass'):
        verdict = 'pass'
    elif 'not runnable' in low or 'needs' in low or 'missing' in low or 'no legacy' in low or 'blocked' in low:
        verdict = 'needs-data'
    else:
        verdict = 'fail'
    steps = []
    for i, s in enumerate(res.get('steps') or [], 1):
        st = str(s.get('status') or s.get('result') or '').lower()
        steps.append({'n': s.get('n') or s.get('step') or i, 'do': s.get('do') or s.get('text') or '',
                      'status': 'pass' if st.startswith('pass') or (verdict == 'pass' and not st.startswith('fail')) else st,
                      'detail': s.get('detail') or s.get('observed') or s.get('text') or ''})
    return {'verdict': verdict, 'steps': steps, 'finished': res.get('finished') or res.get('executed') or '',
            'summary': str(raw)[:300]}


def actual(run, cid, live, step_case):
    """-> (actual result text, status, evidence)"""
    if (step_case or {}).get('readiness') == 'deferred':
        note = 'Deferred: file-upload automation is postponed; run manually or via the agreed alternative.'
        if cid in live:
            note += f" (An earlier automated run is not counted: verdict {norm_result(live[cid][0])['verdict']}.)"
        return note, 'Not Executed', None
    if cid not in live:
        return None, 'Not Executed', None
    res, rel = live[cid]
    res = norm_result(res)
    bad = [s for s in res['steps'] if s['status'] != 'pass']
    if res['verdict'] != 'pass' and not bad:
        bad = [{'n': '-', 'do': '-', 'detail': res.get('summary') or 'see the run folder'}]
    shots = [f for f in os.listdir(os.path.join(run, rel)) if f.endswith('.png')]
    if res['verdict'] == 'pass':
        text, status = f"All {len(res['steps'])} steps passed ({res['finished']}).", 'Passed'
    elif res['verdict'] in ('needs-data', 'needs-verb'):
        text, status = f"Blocked at step {bad[0]['n']}: {bad[0]['detail']}", 'Blocked'
    else:
        text, status = f"Step {bad[0]['n']} ({bad[0]['do']}) failed: {bad[0]['detail']}", 'Failed'
    return text, status, '\n'.join(os.path.join(rel, f) for f in shots) or rel


# ---------------------------------------------------------------- step rendering (v1 `do` steps -> plain English)
def val(v, data):
    def sub(m):
        expr = m.group(1).strip()
        ns, _, k = expr.partition('.')
        if ns == 'data' and data.get(k) not in (None, ''):
            return str(data[k])
        if expr.startswith('today'):
            return expr.replace(' ', '').upper().replace('TODAY', 'Today')
        return f'<{k or expr}>'
    return re.sub(r'\{\{(.+?)\}\}', sub, str(v))


def expect_text(e, data):
    if not isinstance(e, dict):
        return f'Verify {val(e, data)}'
    e = {k: (val(v, data) if isinstance(v, str) else v) for k, v in e.items()}
    if 'url_contains' in e: return f"Verify the page URL contains {e['url_contains']}"
    if 'breadcrumb' in e: return 'Verify breadcrumb shows ' + ' > '.join(e['breadcrumb'])
    if 'grid' in e and 'columns' in e: return f"Verify {e['grid']} grid shows columns: " + ', '.join(e['columns'])
    if 'grid' in e and 'row' in e: return f"Verify {e['grid']} grid {'contains' if e.get('present', True) else 'does not contain'} row {e['row']}"
    if 'fields_present' in e: return 'Verify fields are shown: ' + ', '.join(e['fields_present'])
    if 'field' in e:
        parts = [f"Verify {e['field']}"] + ([f"is {e['state']}"] if 'state' in e else []) + ([f"= \"{e['value']}\""] if 'value' in e else [])
        if 'tags' in e: parts.append('shows ' + (', '.join(e['tags']) if e['tags'] else 'no day / no tag'))
        if 'options' in e: parts.append('lists ' + ', '.join(e['options']))
        return ' '.join(parts)
    if 'button' in e: return f"Verify {e['button']} button is {e['state']}"
    if 'message_contains' in e: return f"Verify message contains \"{e['message_contains']}\""
    if 'text' in e: return f"Verify the {e.get('type', 'message')} \"{e['text']}\" is shown"
    return 'Verify ' + json.dumps(e, ensure_ascii=False)


def render_step(s, data):
    """the plain-English sentence of a step: its own `sentence` (v4), else rendered from the v1 `do` step"""
    if s.get('sentence'):
        return s['sentence']
    v = s.get('do')
    if not v:
        return f"{s.get('event', '')} {s.get('element') or ''}".strip()
    t = {
        'login': lambda: 'Login' + (f" and select distributor {val(s['distributor'], data)}" if s.get('distributor') else ''),
        'logout': lambda: 'Logout',
        'navigate': lambda: f"Navigate to {s['menu']}",
        'enter': lambda: f"Enter {s['field']} = \"{val(s['value'], data)}\"",
        'choose': lambda: f"Choose {s['field']} = \"{val(s['value'], data)}\"",
        'set_date': lambda: f"Set {s['field']} = {val(s['value'], data)}",
        'click': lambda: f"Click {s['button']}",
        'select_row': lambda: f"Select {val(s['value'], data)} in {s['grid']} grid",
        'verify_ui': lambda: expect_text(s['expect'], data),
        'verify_db': lambda: f"Verify in DB ({s['recipe']}): {val(json.dumps(s['expect'], ensure_ascii=False) if not isinstance(s['expect'], str) else s['expect'], data)}",
        'capture': lambda: f"Note the {s['field']} value (as {s['as']})",
        'screenshot': lambda: 'Take screenshot',
        'wait': lambda: f"Wait {s['seconds']}s",
        'download': lambda: f"Click {s['button']} and save the file as {s['as']}",
        'upload': lambda: f"Click {s['button']} and upload {val(s['file'], data)}",
        'edit_excel': lambda: f"In {val(s['file'], data)}: " + '; '.join(
            ', '.join(f"{k} = {val(x, data)}" for k, x in r.items()) for r in s['rows']),
        'manual': lambda: f"[Manual] {s['note']}",
        'capture_message': lambda: 'Note the message shown on screen',
        'harvest_grid': lambda: f"Note the rows listed in the {s.get('grid', 'grid')} grid",
        'harvest_screen': lambda: 'Note the fields of the screen',
        'harvest_menu': lambda: '(technical) read the menu', 'harvest_i18n': lambda: '(technical) read the screen labels',
    }.get(v, lambda: v)()
    return t


def render(c, defaults):
    """numbered sentences of a case (technical harvest steps left out)"""
    data = {**defaults, **c.get('data', {})}
    out = [render_step(s, data) for s in c['steps'] if s.get('do') not in ('harvest_menu', 'harvest_i18n') or s.get('sentence')]
    return '\n'.join(f'{i}) {t}' for i, t in enumerate(out, 1))


def expect_cell(e):
    if e in (None, ''):
        return ''
    if isinstance(e, dict) and set(e) <= {'type', 'text', 'field'} and 'text' in e:
        return f"{e.get('type', 'message')}: {e['text']}"
    return e if isinstance(e, str) else json.dumps(e, ensure_ascii=False)


def step_rows(steps, check=None):
    """[(case, n, sentence, event, element, data_column, expect)] exactly as the Steps sheet shows them; also used by
    qaos_import.py to tell which cells the QA member changed."""
    defaults = ((steps or {}).get('defaults') or {}).get('data') or {}
    rows = []
    for c in (steps or {}).get('cases', []):
        bound = {x['n']: x for x in (((check or {}).get('cases') or {}).get(c['case']) or {}).get('steps', [])}
        data = {**defaults, **(c.get('data') or {})}
        for n, s in enumerate(c['steps'], 1):
            b = bound.get(n, {})
            refs = re.findall(r'\{\{\s*data\.([\w-]+)\s*\}\}', json.dumps(s, ensure_ascii=False))
            col = s.get('data_column') or (refs[0] if refs else '')
            rows.append((c['case'], n, render_step(s, data), s.get('event') or b.get('event') or '',
                         s.get('element') or b.get('element') or '', col or '', expect_cell(s.get('expect'))))
    return rows


# ---------------------------------------------------------------- run model shared by the workbook, summary and import
def load_run(run):
    import qaos_run as R
    d = {f: jload(run, f + '.json') for f in ('requirement', 'cases', 'steps', 'paths', 'check', 'run')}
    d['live'] = live_results(run)
    d['by_case'] = {c['case']: c for c in (d['steps'] or {}).get('cases', [])}
    d['defaults'] = ((d['steps'] or {}).get('defaults') or {}).get('data') or {}
    d['where'] = R.path_of(d['paths']) if d['paths'] else {}
    d['R'] = R
    return d


def is_backlog(section):
    return section['title'].lower().startswith('backlog')


def readiness(d, cid):
    r = ((d['check'] or {}).get('cases') or {}).get(cid)
    if r:
        return r['readiness'], '; '.join(r['reasons'][:3]) + (f" (+{len(r['reasons']) - 3} more)" if len(r['reasons']) > 3 else '')
    sc = d['by_case'].get(cid)
    if sc:
        return sc.get('readiness', ''), '; '.join(sc.get('blocked_by', []))
    return 'no-steps', 'no steps yet'


def expected_message(d, cid, row):
    if isinstance(row, dict) and row.get('EXPECTED_MESSAGE'):
        return row['EXPECTED_MESSAGE']
    case = next((c for c in d['R'].all_cases(d['cases']) if c['id'] == cid), {})
    if case.get('expected_message'):
        return case['expected_message']
    for s in (d['by_case'].get(cid) or {}).get('steps', []):
        e = s.get('expect')
        if s.get('event') == 'verify_message' and e:
            return e.get('text') if isinstance(e, dict) else str(e)
        if isinstance(e, dict) and e.get('message_contains'):
            return e['message_contains']
    if cid in d['live']:
        msgs = d['live'][cid][0].get('messages') or []
        if msgs and isinstance(msgs[0], dict):
            return msgs[0].get('text') or ''
    return ''


def data_rows(d):
    """[(path, ai, case, kind, CASE_TYPE, EXPECTED_MESSAGE, data)] - per path, its rows (v4 5.2); without paths.json
    every case with steps under path '-'"""
    kinds = {c['id']: c['kind'] for c in d['R'].all_cases(d['cases'])}
    out = []
    paths = d['R'].path_list(d['paths']) if d['paths'] else [{'path': '-', 'record': None, 'rows': list(d['by_case'])}]
    for p in paths:
        for r in p.get('rows') or []:
            cid = d['R'].row_case(r)
            data = {**d['defaults'], **((d['by_case'].get(cid) or {}).get('data') or {}),
                    **((r.get('data') or {}) if isinstance(r, dict) else {})}
            ct = (r.get('CASE_TYPE') if isinstance(r, dict) else None) or DEFAULT_CASE_TYPE
            out.append((p.get('path'), cid == p.get('record'), cid, kinds.get(cid, ''), ct, expected_message(d, cid, r), data))
    return out


# ---------------------------------------------------------------- workbook
thin = Side(style='thin'); BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HDR = PatternFill('solid', fgColor=Color(theme=4, tint=0.5999938962981048)); SEC = PatternFill('solid', fgColor='FFFFFF00')
AI = PatternFill('solid', fgColor='FFDDEBF7')
F, FB, FT = Font(name='Calibri', size=11), Font(name='Calibri', size=11, bold=True), Font(name='Calibri', size=14, bold=True)
WC = Alignment(horizontal='center', vertical='center', wrap_text=True); TOP = Alignment(horizontal='left', vertical='top', wrap_text=True)
STATUS_FILL = {'Passed': 'FFC6EFCE', 'Failed': 'FFFFC7CE', 'Blocked': 'FFFFEB9C'}
READY_FILL = {'ready': 'FFC6EFCE', 'needs-data': 'FFFFEB9C', 'needs-knowledge': 'FFFFC7CE'}


def sheet(wb, title, head, widths):
    ws = wb.create_sheet(title)
    for i, (h, w) in enumerate(zip(head, widths), 1):
        c = ws.cell(row=1, column=i, value=h); c.font = FB; c.fill = HDR; c.border = BORDER; c.alignment = WC
        ws.column_dimensions[c.column_letter].width = w
    ws.freeze_panes = 'A2'
    return ws


def put(ws, r, vals, fill=None, font=F):
    for i, v in enumerate(vals, 1):
        c = ws.cell(row=r, column=i, value=v); c.font = font; c.alignment = TOP; c.border = BORDER
        if fill: c.fill = fill


def questions(d):
    """[(id, question, quote, default, evidence, answer, parked, affected)]"""
    out = []
    allc = d['R'].all_cases(d['cases'])
    for a in (d['requirement'] or {}).get('ambiguities', []):
        aff = [c['id'] for c in allc if a['id'] in c.get('traces', []) or any(str(x).startswith(a['id'] + ':') for x in c.get('assumptions', []))]
        parked = a.get('parked') if a.get('parked') is not None else not a.get('answer')
        out.append((a['id'], a.get('question', ''), a.get('quote', ''), a.get('default', ''), a.get('evidence', ''),
                    a.get('answer') or '', 'Y' if parked else '', ', '.join(aff)))
    return out


def build_workbook(run, d):
    cases, key = d['cases'], d['cases']['key']
    wb = Workbook(); wb.remove(wb.active)
    # Questions
    ws = sheet(wb, 'Questions', QUEST_HEAD, [8, 60, 40, 50, 45, 40, 8, 20])
    r = 2
    for q in questions(d):
        put(ws, r, q); r += 1
    beyond = [c for c in d['R'].all_cases(cases) if c.get('beyond_story')]
    if beyond:
        r += 1
        put(ws, r, ['Cases testing behaviour the story does not state - BA to confirm or delete'], font=FB); r += 1
        for c in beyond:
            put(ws, r, [c['id'], c['title'], '', 'kept as a case unless the BA says otherwise', '', '', '', ', '.join(c['traces'])]); r += 1
    # Cases
    ws = sheet(wb, 'Cases', CASES_HEAD, [8, 60, 14, 22, 7, 8, 16, 60, 8, 50, 60])
    r = 2
    backlog = []
    for sec in cases['sections']:
        if is_backlog(sec):
            backlog += sec['cases']
            continue
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=len(CASES_HEAD))
        put(ws, r, [sec['title']], SEC, FB); r += 1
        for c in sec['cases']:
            pid, ai, _ = d['where'].get(c['id'], (None, False, None))
            rd, why = readiness(d, c['id'])
            put(ws, r, [c['id'], ('ALT-' if c['kind'] == 'negative' else '') + c['title'], c['kind'], ', '.join(c['traces']),
                        pid or '', 'Y' if ai else '', rd, why, c.get('priority', ''),
                        '\n'.join(f'{i}) {p}' for i, p in enumerate(c.get('preconditions', []), 1)), c.get('expected', '')],
                AI if ai else None)
            if rd in READY_FILL:
                ws.cell(row=r, column=7).fill = PatternFill('solid', fgColor=READY_FILL[rd])
            r += 1
    if backlog:
        r += 1
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=len(CASES_HEAD))
        put(ws, r, ['Backlog ideas (one line each; to promote one, move it to a core section and give it a path)'], SEC, FB); r += 1
        for c in backlog:
            pid, ai, _ = d['where'].get(c['id'], (None, False, None))
            why = c.get('why') or c.get('note') or ''
            put(ws, r, [c['id'], ('ALT-' if c['kind'] == 'negative' else '') + c['title'] + (f' - {why}' if why else ''), c['kind'], ', '.join(c['traces']), pid or '', 'Y' if ai else '']); r += 1
    dv = DataValidation(type='list', formula1='"Y"', allow_blank=True); ws.add_data_validation(dv); dv.add(f'F2:F{max(r, 2)}')
    # Steps
    ws = sheet(wb, 'Steps', STEPS_HEAD, [8, 5, 80, 14, 34, 18, 40])
    for i, row in enumerate(step_rows(d['steps'], d['check']), 2):
        put(ws, i, list(row))
    ws.column_dimensions.group('D', 'G', outline_level=1, hidden=False)     # event columns: collapsible
    ev = DataValidation(type='list', formula1='"' + ','.join(d['R'].EVENTS) + '"', allow_blank=True)
    ws.add_data_validation(ev); ev.add('D2:D2000')
    # Data rows
    rows = data_rows(d)
    cols = list(dict.fromkeys(k for x in rows for k in x[6]))
    ws = sheet(wb, 'Data rows', DATA_FIXED + cols, [7, 8, 8, 14, 11, 50] + [18] * len(cols))
    for i, (pid, ai, cid, kind, ct, msg, data) in enumerate(rows, 2):
        put(ws, i, [pid, 'Y' if ai else '', cid, kind, ct, msg] + [data.get(k) for k in cols], AI if ai else None)
    # Results
    ws = sheet(wb, 'Results', RESULT_HEAD, [8, 7, 8, 50, 50, 50, 18, 34, 12])
    dv = DataValidation(type='list', formula1='"Passed,Failed,Blocked,Not Executed"', allow_blank=True); ws.add_data_validation(dv)
    for i, c in enumerate(d['R'].all_cases(cases), 2):
        pid, ai, _ = d['where'].get(c['id'], (None, False, None))
        act, status, evid = actual(run, c['id'], d['live'], d['by_case'].get(c['id']))
        put(ws, i, [c['id'], pid or '', 'Y' if ai else '', c['title'], c.get('expected', ''), act, status, evid, key])
        if status in STATUS_FILL:
            ws.cell(row=i, column=7).fill = PatternFill('solid', fgColor=STATUS_FILL[status])
        dv.add(f'G{i}')
    out = os.path.join(run, f'{key}_TestCases.xlsx')
    wb.save(out)
    return out


# ---------------------------------------------------------------- one-page summary
def path_verdicts(run, d):
    """[(path, label, ai case, rows, verdict, note)]"""
    out = []
    for p in (d['R'].path_list(d['paths']) if d['paths'] else []):
        ids = [d['R'].row_case(x) for x in (p.get('rows') or []) + (p.get('manual') or [])]
        res = {cid: actual(run, cid, d['live'], d['by_case'].get(cid))[1] for cid in ids}
        failed = [c for c, s in res.items() if s == 'Failed']
        if failed:
            v = 'FAIL'
        elif res.get(p.get('record')) == 'Passed':
            v = 'PASS'
        elif res.get(p.get('record')) == 'Blocked':
            v = 'BLOCKED'
        elif str(p.get('status', '')).upper().startswith(('PASS', 'SKIP', 'FAIL', 'BLOCK')):
            v = str(p['status']).split()[0].upper()
        else:
            v = 'NOT RUN'
        note = str(p.get('status') or '') or ', '.join(f'{c} {s}' for c, s in res.items())
        out.append((p.get('path'), p.get('label', ''), p.get('record'), ids, v, note, failed))
    return out


def defect_drafts(run, d):
    """Jira-ready drafts (decision 13.1) from failed live results and from `defects` written by the recorder"""
    key, drafts = d['cases']['key'], []
    cases = {c['id']: c for c in d['R'].all_cases(d['cases'])}
    for cid, (res, rel) in sorted(d['live'].items()):
        c = cases.get(cid, {})
        for x in res.get('defects') or []:
            if isinstance(x, dict):
                drafts.append({'title': x.get('title') or f"{key} {cid}: {c.get('title', '')}", 'case': cid,
                               'steps': x.get('steps') or (render(d['by_case'][cid], d['defaults']) if cid in d['by_case'] else ''),
                               'expected': x.get('expected') or c.get('expected', ''), 'actual': x.get('actual', ''),
                               'message': x.get('message', ''), 'evidence': x.get('evidence') or rel})
        n = norm_result(res)
        if n['verdict'] != 'fail' or any(dd['case'] == cid for dd in drafts):
            continue
        bad = [s for s in n['steps'] if s['status'] != 'pass'] or [{'n': '-', 'do': '-', 'detail': n['summary']}]
        msgs = [m.get('text') if isinstance(m, dict) else str(m) for m in res.get('messages') or []]
        drafts.append({'title': f"{key} {cid}: {c.get('title', '').removeprefix('Verify ')} - fails at step {bad[0]['n']}",
                       'case': cid, 'steps': render(d['by_case'][cid], d['defaults']) if cid in d['by_case'] else '',
                       'expected': c.get('expected', ''), 'actual': f"step {bad[0]['n']} ({bad[0]['do']}): {bad[0]['detail']}",
                       'message': '; '.join(f'"{m}"' for m in msgs if m), 'evidence': rel})
    return drafts


def next_action(d, paths, drafts):
    chk = d['check'] or {}
    if chk.get('paths_errors'):
        return 'Fix paths.json (' + '; '.join(chk['paths_errors'][:3]) + '), then re-run `qaos_run.py check`.'
    if drafts:
        return 'Post the defect drafts in Jira (QA member); their paths stay blocked until fixed or accepted (5.3). Other paths continue.'
    passed = [p[0] for p in paths if p[4] == 'PASS']
    open_ = [p[0] for p in paths if p[4] == 'NOT RUN']
    know = sorted({re.sub(r'^.*no screen file for ', '', x) for r in (chk.get('cases') or {}).values()
                   for x in r['reasons'] if 'no screen file' in x})
    if not chk and not paths:
        return 'Write steps and paths.json, then run `qaos_run.py check` and render this workbook again.'
    if open_ and know:
        return 'Train the missing screens first (' + ', '.join(know[:4]) + '); then re-run the check and approve the workbook.'
    if open_:
        return f"Approve the workbook; then the AI runs the AI case of paths {', '.join(open_)} (one login per role)."
    if passed:
        return f"Generate Regress Master scripts for the passing paths {', '.join(passed)} (14.1), verify, hand over to the framework owner."
    return 'Review the results with the QA member.'


def write_summary(run, d, xlsx):
    key = d['cases']['key']
    paths = path_verdicts(run, d)
    drafts = defect_drafts(run, d)
    rel = os.path.relpath(os.path.abspath(run), d['R'].QA_OS)
    rel = os.path.abspath(run) if rel.startswith('..') else rel
    L = [f'# {key} - run summary', '',
         f"Run `{rel.replace(os.sep, '/')}` - {dt.date.today().isoformat()} - "
         f"approval workbook `{os.path.basename(xlsx)}`", '', '## Paths', '']
    if paths:
        L += ['| Path | What | AI case | Cases | Result |', '|---|---|---|---|---|']
        for pid, label, rec, ids, v, note, failed in paths:
            L.append(f"| {pid} | {label[:80]} | {rec or '-'} | {', '.join(ids)} | **{v}**{' - failed: ' + ', '.join(failed) if failed else ''} |")
        cnt = {}
        for p in paths:
            cnt[p[4]] = cnt.get(p[4], 0) + 1
        L += ['', 'Totals: ' + ', '.join(f'{k} {v}' for k, v in sorted(cnt.items()))]
    else:
        L.append('No paths.json yet.')
    chk = (d['check'] or {}).get('summary')
    if chk:
        L += ['', 'Pre-run check: ' + ', '.join(f'{k} {v}' for k, v in sorted(chk.items())) + ' (details in the Cases sheet / check.json).']
    L += ['', '## Defects', '']
    if not drafts:
        L.append('None found in the execution results.')
    for i, x in enumerate(drafts, 1):
        L += [f"### D{i}: {x['title']}", '', f"- **Case:** {x['case']}", '- **Steps to reproduce:**', '',
              *[f'  {s}' for s in str(x['steps']).splitlines()], '', f"- **Expected:** {x['expected']}",
              f"- **Actual:** {x['actual']}", f"- **Exact message:** {x['message'] or '(none shown)'}",
              f"- **Evidence:** `{str(x['evidence']).replace(os.sep, '/')}`", '']
    L += ['', '## Parked questions', '']
    parked = [q for q in questions(d) if q[6] == 'Y']
    L += [f'- **{q[0]}** {q[1]} - default used: {q[3]}' + (f' (cases {q[7]})' if q[7] else '') for q in parked] or ['None.']
    L += ['', '## Next action', '', next_action(d, paths, drafts), '']
    p = os.path.join(run, 'summary.md')
    open(p, 'w', encoding='utf-8').write('\n'.join(L))
    return p, len(drafts)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    run = sys.argv[1]
    d = load_run(run)
    if not d['cases']:
        sys.exit(f'cases.json not found in {run}')
    out = build_workbook(run, d)
    sp, nd = write_summary(run, d, out)
    n = len(d['R'].all_cases(d['cases']))
    print(f"{n} cases, {len(d['by_case'])} with steps, {len(d['R'].path_list(d['paths'])) if d['paths'] else 0} path(s)"
          f"{'' if d['check'] else ' (no check.json: run qaos_run.py check for readiness)'} -> {out}")
    print(f'summary ({nd} defect draft(s)) -> {sp}')


if __name__ == '__main__':
    main()
