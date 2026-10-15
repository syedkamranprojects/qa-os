"""Tests for the v4 runtime: paths.json validation, the pre-run check, the approval workbook and its re-import.

  python runtime/test_qaos_v4.py

Builds a small run (3 cases, 2 paths) and a screen file in the new contract format in a temporary folder; the check is
pointed at that folder, so the app pack's real screen files are not used. No browser, no database.
"""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qaos_run as R          # noqa: E402
import qaos_workbook as W     # noqa: E402
import qaos_import as I       # noqa: E402
from openpyxl import load_workbook   # noqa: E402

SCREEN = {
    'option_id': 'DYL_L__BusinessEntityProfile', 'title': 'Distributor Profile HQ',
    'menu': {'path': ['Company setup', 'Distributor Profile', 'Distributor Profile HQ']},
    'fields': {'Off Days': {'element': 'TXT__epp1_offdays', 'widget': 'tagbox'},
               'Invoice Print Message': {'element': 'TXT__epp1_invmsg', 'widget': 'text'}},
    'tabs': [{'label': 'Demographics', 'element': 'tab_demo'}],
    'buttons': [{'label': 'Update', 'element': 'btnUpdate'}],
    'grids': [{'label': 'Distributor List', 'element': 'gridDist'}],
}
CASES = {'key': 'T-1', 'app': 'snd', 'screen_name': 'Distributor Profile HQ', 'sections': [
    {'title': 'Core - update', 'cases': [
        {'id': 'TC01', 'title': 'Verify two Off Days are saved', 'kind': 'positive', 'traces': ['R1'], 'preconditions': [], 'expected': 'saved'},
        {'id': 'TC02', 'title': 'Verify Off Days cannot take free text', 'kind': 'negative', 'traces': ['R1'], 'preconditions': [], 'expected': 'rejected'}]},
    {'title': 'Backlog (ideas)', 'cases': [
        {'id': 'TC03', 'title': 'Verify another distributor is unchanged', 'kind': 'regression', 'traces': ['R1'], 'preconditions': [], 'expected': 'unchanged', 'note': 'needs a second distributor'}]}]}
STEPS = {'key': 'T-1', 'app': 'snd', 'defaults': {'data': {'distributor': '15108843'}}, 'cases': [
    {'case': 'TC01', 'data': {'day1': 'Monday'}, 'steps': [
        {'sentence': 'Login as Maker', 'event': 'login'},
        {'sentence': 'Open Distributor Profile HQ from the menu', 'event': 'navigate'},
        {'sentence': 'Select the distributor in the Distributor List', 'event': 'row_click', 'data_column': 'distributor'},
        {'sentence': 'Open the Demographics tab'},
        {'sentence': 'Choose Monday in Off Days', 'event': 'choose', 'element': 'TXT__epp1_offdays', 'data_column': 'day1'},
        {'sentence': 'Click Update'},
        {'sentence': 'Verify the message', 'event': 'verify_message', 'expect': {'type': 'toast', 'text': 'Updated successfully'}}]},
    {'case': 'TC02', 'steps': [
        {'do': 'navigate', 'menu': 'Company setup > Distributor Profile > Distributor Profile HQ'},
        {'do': 'enter', 'field': 'Off Days', 'value': '{{data.free_text}}'}]}]}
PATHS = [{'path': 'P1', 'label': 'update', 'record': 'TC01', 'rows': ['TC01', 'TC02']}]


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='qaos_v4_')
        self.run_dir = os.path.join(self.tmp, 'run')
        self.screens = os.path.join(self.tmp, 'screens')
        os.makedirs(self.run_dir); os.makedirs(self.screens)
        json.dump(SCREEN, open(os.path.join(self.screens, 'DYL_L__BusinessEntityProfile.json'), 'w', encoding='utf-8'))
        for n, d in (('cases', CASES), ('steps', STEPS), ('paths', PATHS)):
            json.dump(d, open(os.path.join(self.run_dir, f'{n}.json'), 'w', encoding='utf-8'))
        self._orig = R.screen_files
        R.screen_files = lambda app, folder=None: self._orig(app, self.screens)
        R._models.clear()

    def tearDown(self):
        R.screen_files = self._orig
        shutil.rmtree(self.tmp, ignore_errors=True)


class Paths(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(R.check_paths(PATHS, CASES), ([], []))

    def test_core_missing_and_two_ai(self):
        errs, _ = R.check_paths([{'path': 'P1', 'record': ['TC01', 'TC02'], 'rows': ['TC01']}], CASES)
        self.assertTrue(any('exactly one AI case' in e for e in errs))
        self.assertTrue(any('TC02 is in 0 paths' in e for e in errs))

    def test_ai_not_in_rows_and_core_twice(self):
        errs, _ = R.check_paths([{'path': 'P1', 'record': 'TC02', 'rows': ['TC01']},
                                 {'path': 'P2', 'record': 'TC01', 'rows': ['TC01', 'TC02']}], CASES)
        self.assertTrue(any('AI case TC02 is not one of its rows' in e for e in errs))
        self.assertTrue(any('TC01 is in 2 paths' in e for e in errs))

    def test_no_cap(self):
        many = {'key': 'K', 'app': 'snd', 'sections': [{'title': 'Core', 'cases': [
            {'id': f'TC{i:02d}', 'title': 'Verify x', 'kind': 'positive', 'traces': ['R1'], 'preconditions': [], 'expected': 'x'} for i in range(1, 15)]}]}
        self.assertEqual(len(R.core_ids(many)), 14)


class Check(Base):
    def test_labels(self):
        res = R.run_check(self.run_dir, 'snd')
        tc1, tc2, tc3 = (res['cases'][c] for c in ('TC01', 'TC02', 'TC03'))
        self.assertEqual(tc1['readiness'], 'ready', tc1['reasons'])
        bound = {s['n']: s for s in tc1['steps']}
        self.assertEqual(bound[3]['element'], 'gridDist')            # row_click on the grid named in the sentence
        self.assertEqual(bound[4]['event'], 'tab')                   # event read from the sentence
        self.assertEqual(bound[6]['element'], 'btnUpdate')
        self.assertTrue(tc1['ai_case'])
        self.assertEqual(tc2['readiness'], 'needs-knowledge')        # enter (set) on a tagbox does not fit
        self.assertTrue(any('does not fit' in x for x in tc2['reasons']))
        self.assertTrue(any("'free_text'" in x for x in tc2['reasons']))   # and its data column is empty
        self.assertEqual(tc3['readiness'], 'no-steps')

    def test_missing_screen_and_data(self):
        steps = json.loads(json.dumps(STEPS))
        steps['cases'][0]['data'] = {'day1': ''}
        steps['cases'][1]['steps'][0]['menu'] = 'Company setup > Distributor Profile > Distributor Profile DT'
        res = R.run_check(self.run_dir, 'snd', steps=steps)
        self.assertEqual(res['cases']['TC01']['readiness'], 'needs-data')
        self.assertTrue(any('no screen file' in x for x in res['cases']['TC02']['reasons']))

    def test_unknown_label(self):
        steps = json.loads(json.dumps(STEPS))
        steps['cases'][0]['steps'][5] = {'sentence': 'Click Approve'}
        res = R.run_check(self.run_dir, 'snd', steps=steps)
        self.assertEqual(res['cases']['TC01']['readiness'], 'needs-knowledge')


class WorkbookImport(Base):
    def render(self):
        R.save(os.path.join(self.run_dir, 'check.json'), R.run_check(self.run_dir, 'snd'))
        d = W.load_run(self.run_dir)
        out = W.build_workbook(self.run_dir, d)
        W.write_summary(self.run_dir, d, out)
        return out

    def test_sheets_and_summary(self):
        out = self.render()
        wb = load_workbook(out)
        self.assertEqual(wb.sheetnames, list(W.SHEETS))
        cases = [r for r in wb['Cases'].iter_rows(min_row=2, values_only=True) if r[0]]
        tc1 = next(r for r in cases if r[0] == 'TC01')
        self.assertEqual((tc1[4], tc1[5], tc1[6]), ('P1', 'Y', 'ready'))
        self.assertTrue(any(r[0] == 'TC03' and 'needs a second distributor' in r[1] for r in cases))   # backlog one-liner
        self.assertEqual(wb['Steps'].column_dimensions['D'].outline_level, 1)
        data = list(wb['Data rows'].iter_rows(min_row=1, values_only=True))
        self.assertEqual(data[0][:6], tuple(W.DATA_FIXED))
        self.assertEqual(data[1][5], 'Updated successfully')
        self.assertIn('## Next action', open(os.path.join(self.run_dir, 'summary.md'), encoding='utf-8').read())

    def test_round_trip_no_change(self):
        out = self.render()
        self.assertEqual(I.import_approval(out, self.run_dir, 'snd', apply=False), 0)

    def test_edits(self):
        out = self.render()
        wb = load_workbook(out)
        ws = wb['Steps']
        for row in ws.iter_rows(min_row=2):
            if row[0].value == 'TC02' and row[1].value == 2:
                row[2].value = 'Choose Monday in Off Days'; row[3].value = 'choose'; row[4].value = 'TXT__epp1_offdays'
                row[5].value = None
        ws.insert_rows(9)                                               # a new step after TC01 step 7
        for i, v in enumerate(['TC01', 8, 'Verify Off Days shows Monday', 'verify_field', 'TXT__epp1_offdays', None, 'Monday'], 1):
            ws.cell(row=9, column=i, value=v)
        dr = wb['Data rows']
        head = [c.value for c in dr[1]]
        for row in dr.iter_rows(min_row=2):
            if row[2].value == 'TC02':
                row[head.index('EXPECTED_MESSAGE')].value = 'Invalid day'
        wb.save(out)
        rc = I.import_approval(out, self.run_dir, 'snd', apply=True)
        self.assertEqual(rc, 0)
        steps = json.load(open(os.path.join(self.run_dir, 'steps.json'), encoding='utf-8'))
        tc1, tc2 = steps['cases']
        self.assertEqual(len(tc1['steps']), 8)
        self.assertEqual(tc1['steps'][7]['event'], 'verify_field')
        self.assertNotIn('do', tc2['steps'][1])                         # rewritten sentence replaces the v1 step
        self.assertEqual(tc2['steps'][1]['element'], 'TXT__epp1_offdays')
        paths = json.load(open(os.path.join(self.run_dir, 'paths.json'), encoding='utf-8'))
        self.assertEqual(paths[0]['rows'][1], {'case': 'TC02', 'EXPECTED_MESSAGE': 'Invalid day'})
        chk = json.load(open(os.path.join(self.run_dir, 'check.json'), encoding='utf-8'))
        self.assertEqual(chk['cases']['TC02']['readiness'], 'ready')

    def test_two_ai_cases_refused(self):
        out = self.render()
        wb = load_workbook(out)
        for row in wb['Cases'].iter_rows(min_row=2):
            if row[0].value == 'TC02':
                row[5].value = 'Y'
        wb.save(out)
        self.assertEqual(I.import_approval(out, self.run_dir, 'snd', apply=True), 1)
        self.assertEqual(json.load(open(os.path.join(self.run_dir, 'paths.json'), encoding='utf-8')), PATHS)   # nothing written


class Schema(unittest.TestCase):
    def test_validate_cli_on_v4_run(self):
        tmp = tempfile.mkdtemp(prefix='qaos_v4s_')
        try:
            for n, d in (('cases', CASES), ('steps', STEPS), ('paths', PATHS)):
                json.dump(d, open(os.path.join(tmp, f'{n}.json'), 'w', encoding='utf-8'))
            r = subprocess.run([sys.executable, os.path.join(HERE, 'qaos_run.py'), 'validate', tmp], capture_output=True, text=True,
                               encoding='utf-8')
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn('OK  paths.json', r.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    unittest.main(verbosity=1)
