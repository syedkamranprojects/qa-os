"""Tests for qaos_record_multi.py (watcher log -> multi-screen flow spec + case data). HARDENING C1/C3/C4/C5/C6/C7.

  python framework/tools/test_qaos_record_multi.py

Uses a small inline log shaped like a real Order Booking recording (sidebar, header, lines grid, save, summary),
then feeds the spec to gen_framework_sql.py in a temporary folder. Nothing is applied to any database.
"""
import json, os, subprocess, sys, tempfile, unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import qaos_record_multi as M   # noqa: E402

G = 'gridContainer'
LOG = [
    {'act': 'click', 'id': 'menurollin', 'locator': '#menurollin', 't': 1000},
    {'act': 'screen', 'url': '/ngui/dyl/layout?layoutCode=1', 't': 1100},
    {'act': 'text', 'label': 'Search Here', 'locator': 'input[name="filterText"]', 'value': 'Order Booking', 't': 1200},
    {'act': 'nav_click', 'id': 'ORDER_BOOKING', 'locator': '#ORDER_BOOKING', 'search': 'Order Booking', 't': 1300},
    {'act': 'screen', 'url': '/ngui/order-booking', 't': 2000},
    {'act': 'option', 'label': 'PJP', 'id': 'PJPNO', 'locator': '#PJPNO', 'widget': 'dropdown', 'value': 'PJP-1', 't': 2100},
    {'act': 'text', 'label': 'Outlet Name', 'id': 'OUTLET', 'locator': '#OUTLET', 'widget': 'type-ahead', 'value': '100', 't': 2200},
    {'act': 'option', 'label': 'Outlet Name', 'id': 'OUTLET', 'locator': '#OUTLET', 'value': '100-Outlet A', 't': 2300},
    {'act': 'click', 'id': 'orderDetail', 'locator': '#orderDetail', 'text': 'Order Detail', 't': 2400},
    {'act': 'screen', 'url': '/ngui/order-booking/lines', 't': 3000},
    {'act': 'cell', 'label': 'Product', 'grid': G, 'id': 'product', 'locator': '#product', 'widget': 'type-ahead', 'colindex': 2, 'value': 'A1', 't': 3100},
    {'act': 'option', 'label': 'Product', 'grid': G, 'id': 'product', 'locator': '#product', 'value': 'A1-Soap', 't': 3150},
    {'act': 'cell', 'label': 'Order PC', 'grid': G, 'id': 'q2', 'locator': '#q2', 'colindex': 6, 'value': '0', 't': 3200},
    {'act': 'cell', 'label': 'Order CS', 'grid': G, 'id': 'q1', 'locator': '#q1', 'colindex': 5, 'value': '20', 't': 3250},
    {'act': 'cell', 'label': 'Order CS', 'grid': G, 'id': 'q1', 'locator': '#q1', 'colindex': 5, 'value': '2', 't': 3300},
    {'act': 'click', 'id': 'rowSave', 'locator': '#rowSave', 'text': 'Save', 'grid': G, 't': 3400},
    {'act': 'cell', 'label': 'Product', 'grid': G, 'id': 'product', 'locator': '#product', 'colindex': 2, 'value': 'B2', 't': 3500},
    {'act': 'cell', 'label': 'Order CS', 'grid': G, 'id': 'q1', 'locator': '#q1', 'colindex': 5, 'value': '0', 't': 3550},
    {'act': 'cell', 'label': 'Order PC', 'grid': G, 'id': 'q2', 'locator': '#q2', 'colindex': 6, 'value': '7', 't': 3600},
    {'act': 'click', 'id': 'rowSave', 'locator': '#rowSave', 'text': 'Save', 'grid': G, 't': 3700},
    {'act': 'click', 'id': 'validateBtn', 'locator': '#validateBtn', 'text': 'Validation', 't': 4000},
    {'act': 'toast', 'messages': ['Validation successfully'], 'type': 'success', 't': 4100},
    {'act': 'click', 'id': 'saveBtn', 'locator': '#saveBtn', 'text': 'Save', 't': 6000},
    {'act': 'toast', 'messages': ['Validation successfully'], 'type': 'success', 't': 6050},
    {'act': 'toast', 'messages': ['Order Save successfully'], 'type': 'success', 't': 6100},
    {'act': 'screen', 'url': '/ngui/order-summary', 't': 7000},
    {'act': 'remember', 'name': 'QUICK_ORDERNUMBER', 'label': 'Order Number', 'id': 'orderNo', 'locator': '#orderNo', 'value': 'COL1', 't': 7100},
    {'act': 'click', 'id': 'newOrder', 'locator': '#newOrder', 'text': 'New Order', 't': 7200},
]
META = {'story': 'TEST-1', 'case': 'TC02'}
ROWS = [
    {'case': 'TC01', 'PJP': 'PJP-1', 'Outlet': '200', 'Lines': [{'code': 'C3', 'cs': 1, 'pc': 0}]},
    {'case': 'TC02', 'PJP': 'PJP-1', 'Outlet': '100', 'Lines': [{'code': 'A1', 'cs': 2, 'pc': 0}, {'code': 'B2', 'cs': 0, 'pc': 7}]},
]


def build(log=LOG, rows=ROWS):
    spec = M.build(log, META, '0999', 'Test flow', 'NG_TEST', 'Header;Lines;Summary')
    M.casedata(spec, log, META, rows, {'TC01': 'one line', 'TC02': 'two lines'})
    return spec


class Converter(unittest.TestCase):
    def setUp(self):
        self.spec = build()
        self.sc = {s['name']: s for s in self.spec['screens']}

    def ev(self, screen, kind):
        return [e for e in self.sc[screen]['events'] if (e['type'], e['event']) == kind]

    def test_screens_and_children(self):            # C1, sidebar is navigation not a screen
        self.assertEqual([s['name'] for s in self.spec['screens']], ['Header', 'Lines', 'Summary'])
        self.assertEqual([s['parent'] for s in self.spec['screens']], [None, '099901', '099901'])
        self.assertEqual(self.spec['gaps'], [])

    def test_navigation(self):                       # C3
        mg = self.spec['menu_group']
        self.assertEqual((mg['navigation'], mg['navigation_type'], mg['searchtext']), ('ORDER_BOOKING', 'id', 'Order Booking'))

    def test_wait_after_toast(self):                 # C4: wait before the Save that follows the validation toast
        ev = self.sc['Lines']['events']
        i = next(i for i, e in enumerate(ev) if e.get('field') == 'saveBtn')
        self.assertEqual((ev[i - 1]['event'], ev[i - 1]['fixed']), ('0006', '5'))
        self.assertEqual([e['fixed'] for e in self.ev('Lines', ('0000', '0014'))], ['TSTMSG,VALIDATION_ASSR', 'TSTMSG,SAVE_ASSR'])
        self.assertEqual([n['text'] for n in self.spec['not_asserted']], ['Validation successfully'])

    def test_load_data_and_repo(self):               # C5
        for s in self.spec['screens']:
            self.assertEqual((s['events'][0]['event'], s['events'][0]['serial']), ('0001', 1))
        repo = [f for f in self.sc['Summary']['fields'] if f['type'] == '0010']
        self.assertEqual((repo[0]['id'], repo[0]['repoid']), ('orderNo', 'QUICK_ORDERNUMBER'))
        self.assertEqual(len(self.ev('Summary', ('0000', '0012'))), 1)

    def test_widgets_and_grid(self):                 # C7, grid columns in colindex order, one row-button event
        f = {x['caption']: x for x in self.sc['Lines']['fields']}
        self.assertEqual([x['caption'] for x in self.sc['Lines']['fields']], ['Product', 'Order CS', 'Order PC'])
        self.assertEqual(f['Product']['type'], '0006')
        self.assertEqual({x['caption']: x['type'] for x in self.sc['Header']['fields']}, {'PJP': '0002', 'Outlet Name': '0006'})
        rows = [e for e in self.sc['Lines']['events'] if e.get('field') == 'rowSave']
        self.assertEqual([e['ref'] for e in rows], [1])
        self.assertIsNone(next(e for e in self.sc['Lines']['events'] if e.get('field') == 'saveBtn')['ref'])

    def test_casedata_rows(self):
        cd = {s['sheet']: s for s in self.spec['casedata']['sheets']}
        self.assertEqual([r[4:] for r in cd['Header']['rows']], [['PJP-1', '200'], ['PJP-1', '100']])
        self.assertEqual([r[0] for r in cd['Lines']['rows']], ['01-01', '02-01', '02-02'])
        self.assertEqual([r[4:] for r in cd['Lines']['rows']], [['C3', '1', '0'], ['A1', '2', '0'], ['B2', '0', '7']])
        self.assertEqual(cd['SAVE_ASSR']['rows'], [['01', 'TN', 'Order Save successfully'], ['02', 'TN', 'Order Save successfully']])

    def test_no_guess_when_value_does_not_match(self):
        rows = [dict(ROWS[1], Lines=[{'code': 'A1', 'cs': 9, 'pc': 0}, {'code': 'B2', 'cs': 0, 'pc': 7}])]
        spec = build(rows=rows)
        self.assertNotIn('Lines', [s['sheet'] for s in spec['casedata']['sheets']])
        self.assertTrue(any('Order CS' in g for g in spec['gaps']))

    def test_row_snapshots_win_over_noisy_cells(self):
        """Watcher 'row' entries (row cells read at the row-Save click) are authoritative; keystroke noise is ignored.
        Also: the helper's own 'nav' entry is navigation, pick text '<code>-<desc>' and '01' bind to data '1'."""
        snap = lambda p, cs, pc: {'act': 'row', 'grid': G, 'button': 'rowSave', 'cells': [
            {'label': 'Product', 'value': p, 'id': 'product', 'locator': '#product', 'widget': 'type-ahead', 'colindex': '2'},
            {'label': 'Order CS', 'value': cs, 'id': 'q1', 'locator': '#q1', 'colindex': '5'},
            {'label': 'Order PC', 'value': pc, 'id': 'q2', 'locator': '#q2', 'colindex': '6'}]}
        log = []
        for a in LOG:
            if a.get('act') == 'click' and a.get('id') == 'rowSave':
                log.append(snap('A1-Soap', '02', '0') if not any(x.get('act') == 'row' for x in log) else snap('B2-Tea', '0', '7'))
            if a.get('act') == 'cell':
                a = dict(a, value='101')                 # keystroke noise must not matter
            log.append(a)
        log.insert(4, {'act': 'nav', 'term': 'Order Booking', 'url': '/ngui/dyl/layout'})
        spec = build(log=log)
        self.assertEqual(spec['gaps'], [])
        cd = {s['sheet']: s for s in spec['casedata']['sheets']}
        self.assertEqual([r[4:] for r in cd['Lines']['rows']], [['C3', '1', '0'], ['A1', '2', '0'], ['B2', '0', '7']])
        self.assertEqual(['Header', 'Lines', 'Summary'], [s['name'] for s in spec['screens']])
        self.assertTrue(M.same('01', 1) and M.same('62740537-RAFHAN', '62740537') and not M.same('6274', '62740537'))

    def test_tabs_become_screens_with_navigation(self):
        """A recorded tab click starts a framework screen whose navigation is the tab (convention of DSR / Outlet Profile:
        first tab Dem-1 is the root, later tabs are children with their own ids; a tab without id -> linkText)."""
        url = '/ngui/dsr-profile'
        log = [
            {'act': 'nav_click', 'id': 'DSR_PROFILE', 'locator': '#DSR_PROFILE', 'search': 'DSR Profile', 't': 1},
            {'act': 'screen', 'url': url, 't': 2},
            {'act': 'tab', 'id': 'Dem-1', 'value': 'Demographics', 'locator': '#Dem-1', 't': 3},
            {'act': 'text', 'label': 'DSR Code', 'id': 'dsrCode', 'locator': '#dsrCode', 'value': 'AUTO1', 't': 4},
            {'act': 'click', 'id': 'saveBtn', 'locator': '#saveBtn', 'text': 'Save', 't': 5},
            {'act': 'toast', 'messages': ['Saved successfully'], 't': 6},
            {'act': 'click', 'id': 'dx-34ec4a40-7c17-1e45', 'text': '', 'locator': '#dx-34ec4a40-7c17-1e45', 't': 19999},  # drop-down toggle
            {'act': 'click', 'id': 'Opr-1', 'text': 'Address', 'locator': '#Opr-1', 't': 20000},   # logged as a plain click
            {'act': 'screen', 'url': url, 't': 20001},              # same page: no new screen from this entry
            {'act': 'text', 'label': 'Street/Road', 'id': 'street', 'locator': '#street', 'value': 'Saddar', 't': 20002},
            {'act': 'click', 'id': 'saveAddr', 'locator': '#saveAddr', 'text': 'Save', 't': 20003},
            {'act': 'toast', 'messages': ['Address saved'], 't': 20004},
            {'act': 'tab', 'id': '', 'value': 'Qualification', 'locator': '//a[normalize-space(.)="Qualification"]', 't': 40000},
            {'act': 'text', 'label': 'Year Passed', 'id': 'year', 'locator': '#year', 'value': '2012', 't': 40001},
        ]
        rows = [{'case': 'TC01', 'Code': 'AUTO1', 'Street': 'Saddar', 'Year': '2012'},
                {'case': 'TC02', 'Code': 'AUTO2', 'Street': 'Clifton', 'Year': '2015'}]
        meta = {'story': 'TEST-2', 'case': 'TC01'}
        spec = M.build(log, meta, '0998', 'Tabs', 'NG_TABS', 'Demographics;Address;Qualification')
        M.casedata(spec, log, meta, rows, {})
        self.assertEqual(spec['gaps'], [])
        sc = spec['screens']
        self.assertEqual([s['name'] for s in sc], ['Demographics', 'Address', 'Qualification'])
        self.assertEqual([(s.get('navigation_type'), s.get('navigation_path')) for s in sc],
                         [('id', 'Dem-1'), ('id', 'Opr-1'), ('linkText', 'Qualification')])
        self.assertEqual([s['parent'] for s in sc], [None, '099801', '099801'])
        self.assertEqual([[f['caption'] for f in s['fields']] for s in sc], [['DSR Code'], ['Street/Road'], ['Year Passed']])
        self.assertFalse(any('Tab' in e['desc'] for s in sc for e in s['events']))   # tab clicks are navigation, not events
        self.assertEqual([x['id'] for x in spec['skipped_clicks']], ['dx-34ec4a40-7c17-1e45'])   # generated id dropped
        self.assertFalse(any((e.get('field') or '').startswith('dx-') for s in sc for e in s['events']))
        self.assertEqual([x['expected_message'] for x in spec['assertion_sheets']], ['Saved successfully', 'Address saved'])
        cd = {x['sheet']: x['rows'] for x in spec['casedata']['sheets']}
        self.assertEqual([r[4:] for r in cd['Address']], [['Saddar'], ['Clifton']])
        self.assertEqual([r[4:] for r in cd['Qualification']], [['2012'], ['2015']])
        sys.path.insert(0, TOOLS)
        import gen_framework_sql as G
        sql, _, _ = G.build(spec)
        self.assertIn("'Opr-1'", sql)
        self.assertIn("'linkText'", sql)

    def test_run_info_in_sql_header(self):
        sys.path.insert(0, TOOLS)
        import gen_framework_sql as G
        ri = {'key': 'QUICK-1', 'request': 'Create an order\nwith 2 lines', 'market': 'PK', 'market_name': 'Unilever Pakistan',
              'org': '010104', 'framework_app_id': '8', 'group': '11', 'env': 'cnr1dev1', 'run_by': 'QA Member',
              'users': {'Maker': {'user': 'Auto_Multi_Orga', 'company': 'C', 'distributor': '15108843'}},
              'executed_case': 'TC02', 'recording': 'recording_TC02.json', 'cases': 2}
        spec = dict(self.spec, run_info=ri)
        sql, rb, _ = G.build(spec)
        head = sql.split('BEGIN;')[0]
        for text in ('-- Run by:            QA Member', 'Create an order with 2 lines', 'Market:            PK - Unilever Pakistan',
                     'Maker Auto_Multi_Orga', 'case TC02 only'):
            self.assertIn(text, head)
        self.assertIn('-- Run by:', rb.split('BEGIN;')[0])
        self.assertTrue(all(l.startswith('--') for l in head.strip().splitlines()))   # comments only, no SQL injected

    def test_generator_accepts_spec(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'spec.json')
            with open(p, 'w', encoding='utf-8') as fh:
                json.dump(self.spec, fh)
            r = subprocess.run([sys.executable, os.path.join(TOOLS, 'gen_framework_sql.py'), p, os.path.join(d, 'out')],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertNotIn('header-only', r.stdout + r.stderr)
            with open(os.path.join(d, 'out', 'framework.sql'), encoding='utf-8') as fh:
                sql = fh.read()
            self.assertIn("'099902'", sql)
            self.assertIn('ORDER_BOOKING', sql)


if __name__ == '__main__':
    unittest.main(verbosity=1)
