"""Export approved step drafts to an Excel record: test cases, steps, framework mapping and approvals.

  python runtime/qaos_export.py <run_dir> [--out <file.xlsx>]

Reads every <run_dir>/step_draft_*.json (written by qaos_steps.py; each has "case", "steps", optional "approval").
Sheets: Test Cases (team layout), Steps (one row per step, for validation), Framework Mapping (step -> framework flow),
Approvals & Notes. Result columns (Actual Result, Status, Evidence, Recorded message) stay empty until the flow is recorded.
"""
import argparse
import glob
import json
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

sys.stdout.reconfigure(encoding='utf-8')
HDR = PatternFill('solid', fgColor='1F4E78')
BAND = PatternFill('solid', fgColor='FFF2CC')
ONEWAY = PatternFill('solid', fgColor='FCE4D6')
CHANGE = PatternFill('solid', fgColor='FFF9E5')
thin = Side(style='thin', color='BFBFBF')
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)


def header(ws, row, cols, widths):
    for i, (c, w) in enumerate(zip(cols, widths), 1):
        x = ws.cell(row=row, column=i, value=c)
        x.font = Font(bold=True, color='FFFFFF')
        x.fill = HDR
        x.alignment = Alignment(vertical='center', wrap_text=True)
        x.border = BOX
        ws.column_dimensions[x.column_letter].width = w
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def put(ws, row, vals, wrap=True, fill=None):
    for i, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.alignment = Alignment(vertical='top', wrap_text=wrap)
        c.border = BOX
        if fill:
            c.fill = fill


def flow_of(case, n):
    for m in case.get('flow_map', []):
        if m['steps'][0] <= n <= m['steps'][1]:
            return m
    return None


def norm_step(t):
    """The recorder may shorten the wording (drop quotes, brackets, 'Dispatch Advice' before DA1); the step number and the leading verb must still agree."""
    w = ''.join(ch if ch.isalnum() else ' ' for ch in (t or '')).lower().split()
    return w[0] if w else ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('run')
    ap.add_argument('--out')
    ap.add_argument('--results', help='exec/results*.json from the recorder: fills Recorded result, Observed, Evidence, Actual Result and Status')
    ap.add_argument('--history', action='append', default=[], help='a line for the attempt history in Approvals & Notes (repeatable)')
    a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(a.run, 'step_draft_*.json')))
    if not files:
        sys.exit('no step_draft_*.json in ' + a.run)
    drafts = [json.load(open(f, encoding='utf-8')) for f in files]
    key = os.path.basename(os.path.dirname(os.path.abspath(a.run)))
    out = a.out or os.path.join(a.run, f'{key}_TestCases_Steps.xlsx')

    wb = Workbook()
    # ---- Test Cases (team layout)
    ws = wb.active
    ws.title = 'Test Cases'
    header(ws, 1, ['Test Screen', 'Test Scenario', 'TestCase#', 'Description', 'Pre-Requisite', 'Test Steps', 'Test Data', 'Expected Result',
                   'Actual Result', 'Status', 'Evidence', 'Priority', 'Approval'],
           [20, 22, 10, 44, 44, 70, 36, 44, 30, 14, 24, 9, 28])
    r = 2
    for d in drafts:
        c = d.get('case', {})
        steps = '\n'.join(f"{s['n']}. [{s['actor']}] {s['step']}" for s in d['steps'])
        data = '\n'.join(f'{k} = {v}' for k, v in (c.get('data') or {}).items())
        appr = d.get('approval') or {}
        put(ws, r, [c.get('screen'), c.get('scenario'), c.get('id'), c.get('title'), '\n'.join('- ' + x for x in c.get('preconditions', [])), steps, data,
                    c.get('expected'), 'Not executed (recording pending)', 'Not Executed', None, c.get('priority'),
                    f"{appr.get('status', 'not approved')} at {appr.get('gate', 'G3')} on {appr.get('date', '')}" if appr else 'not approved'])
        ws.row_dimensions[r].height = min(409, 15 * (len(d['steps']) + 2))
        r += 1
    dv = DataValidation(type='list', formula1='"Not Executed,Pass,Fail,Blocked,Unverified"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f'J2:J{max(r, 3)}')

    # ---- Steps (one row per step)
    ws2 = wb.create_sheet('Steps')
    header(ws2, 1, ['TestCase#', '#', 'Actor', 'Step (standard wording)', 'QA member\'s wording', 'Verb', 'Risk', 'Screen', 'Label check', 'Expected / note',
                    'Framework flow', 'Trace (group:seq:flow)', 'Recorded result', 'Observed message / status', 'Evidence'],
           [10, 5, 12, 62, 34, 16, 13, 18, 14, 30, 12, 20, 14, 30, 22])
    r = 2
    for d in drafts:
        c = d.get('case', {})
        for s in d['steps']:
            m = flow_of(c, s['n'])
            trace = (f"{m['group']}:{m['group_seq']}:{m['flow']}" if m and m.get('group') else 'NOT COVERED by the framework') if m else ''
            fill = ONEWAY if s['risk'] == 'one-way' else CHANGE if s['risk'] == 'changes-data' else None
            put(ws2, r, [c.get('id'), s['n'], s['actor'], s['step'], s.get('raw'), s['verb'], s['risk'], s.get('screen'),
                         s.get('state') + (' (labels unverified)' if s.get('warnings') else ''), s.get('expect') or s.get('note'),
                         m['flow'] if m else '', trace, 'Not recorded', None, None], fill=fill)
            r += 1
    ws2.auto_filter.ref = f'A1:O{r - 1}'

    # ---- Framework mapping
    ws3 = wb.create_sheet('Framework Mapping')
    header(ws3, 1, ['TestCase#', 'Steps', 'Framework flow', 'What it is', 'New group / seq (group 11 seq)', 'User (role)', 'Case-data sheets (per atlas)', 'Note'],
           [10, 10, 14, 40, 12, 26, 60, 50])
    r = 2
    sheets = {'021400000': 'Login / Distributor selection sheets', '00100001': 'Dispatch Advice, Dispatch Advice Detail2, Dispatch Advice Detail, Dispatch Advice Grid, DA_FORWARD_ASSR, GLOBAL-REPO',
              '00740001': 'Dispatch Advice Approval, DA_APPROVALFRWD_ASSR, GLOBAL-REPO', 'switch': '(login user serial 8)', 'none': '-'}
    for d in drafts:
        c = d.get('case', {})
        for m in c.get('flow_map', []):
            put(ws3, r, [c.get('id'), f"{m['steps'][0]}-{m['steps'][1]}", m['flow'], m['name'], (f"{m['group']} / {m['group_seq']} ({m['g11_seq']})" if m.get('group') else '-'), m['user'], sheets.get(m['flow'], ''),
                         'Existing framework flow; not duplicated. Logout/login is the group detail row with login status Y.' if m['flow'] == 'switch' else ('A green engine run proves nothing for this step: add a check in the framework or verify it in the live recording.' if m['flow'] == 'none' else 'Existing framework flow (also group 11).')], fill=BAND if m['flow'] in ('switch', 'none') else None)
            r += 1

    # ---- Approvals & notes
    RECORDING_STATUS = ('RECORDED manually through the Selenium MCP: see the Steps sheet (Recorded result, Observed message / status) and the attempt history below. The framework replay has NOT been run.' if a.results else
                        'NOT RECORDED. The steps are authored and approved, not yet executed live. Record on a fresh calendar day (one-day rule); Actual Result / Status stay empty until then.')
    ws4 = wb.create_sheet('Approvals & Notes')
    header(ws4, 1, ['Item', 'Detail'], [26, 110])
    r = 2
    for d in drafts:
        c, ap_ = d.get('case', {}), d.get('approval') or {}
        rows = [('Test case', f"{c.get('id')} - {c.get('title')}"), ('Gate G3 (step sheet)', f"{ap_.get('status', 'not approved')} by {ap_.get('by', '-')} on {ap_.get('date', '-')}"),
                ('Approval note', ap_.get('note', '')), ('Known risks', '\n'.join('- ' + x for x in c.get('known_risks', []))),
                ('Recording status', RECORDING_STATUS),
                ('How to validate', '1) Compare the Steps sheet with the live screens. 2) The recorded results are filled from exec/results*.json (python runtime/qaos_export.py <run> --results <file>); a result is attached by step number and leading verb. 3) Compare the Framework Mapping with the group rows in the atlas (apps/snd/knowledge/framework_atlas/group_11.md). 4) Edit the Test Steps column and re-import with runtime/qaos_import.py to change the steps.')]
        for k, v in rows:
            put(ws4, r, [k, v])
            r += 1
    if a.history:
        r = ws4.max_row + 1
        for h in a.history:
            put(ws4, r, ['Attempt history', h])
            r += 1
    if a.results:
        rj = json.load(open(a.results, encoding='utf-8'))
        res_case = rj.get('case')                                  # results belong to one case only
        res = {x['n']: x for x in rj['results']}
        stat = {}
        for row in ws2.iter_rows(min_row=2):
            n = row[1].value
            x = res.get(n) if (res_case is None or row[0].value == res_case) else None
            if not x:
                continue
            if norm_step(x['step']) != norm_step(str(row[3].value)):
                row[12].value = 'MISMATCH: result was recorded for "' + x['step'] + '"'
                stat[row[0].value] = 'Unverified'
                continue
            obs = x.get('observed') or {}
            row[12].value = x['result']
            row[13].value = '; '.join(f'{k}: {v}' for k, v in obs.items())
            row[14].value = x.get('evidence')
            row[12].fill = PatternFill('solid', fgColor={'pass': 'E2EFDA', 'fail': 'F8CBAD', 'blocked': 'F8CBAD'}.get(x['result'], 'EDEDED'))
            stat.setdefault(row[0].value, []).append(x['result']) if not isinstance(stat.get(row[0].value), str) else None
        for row in ws.iter_rows(min_row=2):
            cid = row[2].value
            rs = stat.get(cid)
            if isinstance(rs, str):
                row[9].value = rs
            elif rs and cid == (res_case or cid):
                allp = all(v == 'pass' for v in rs) and len(rs) == len(drafts[0]['steps'])
                row[9].value = 'Pass' if allp else ('Fail' if 'fail' in rs else 'Unverified')
                row[8].value = f"{rs.count('pass')} of {len(rs)} recorded steps passed" + ('' if allp else f"; {len(drafts[0]['steps']) - len(rs)} not recorded")
                row[10].value = os.path.relpath(a.results, a.run)
    wb.save(out)
    print('written', out, '|', sum(len(d['steps']) for d in drafts), 'steps in', len(drafts), 'case(s)')


if __name__ == '__main__':
    main()
