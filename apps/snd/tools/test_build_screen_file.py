"""Tests for build_screen_file.py (design v4 W1 screen files).

  python apps/snd/tools/test_build_screen_file.py

Builds the Distributor Profile HQ screen file in memory (nothing is written to apps/snd/screens), validates it against
plugins/qa-os/schemas/screen.schema.json and checks the facts learned live on cnr1dev1 (SDMS-6084): live ids win over the
config, the difference is recorded, hand-added lessons survive a rebuild, and the build is deterministic.
"""
import copy, json, os, shutil, sys, tempfile, unittest

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import build_screen_file as M   # noqa: E402

KEY = 'DYL_L__BusinessEntityProfile'


class DistributorProfileHQ(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ctx = M.Context()
        cls.doc = M.build(cls.ctx, 'Distributor Profile HQ')

    def test_schema_valid(self):
        import jsonschema
        jsonschema.Draft202012Validator(M.load(M.SCHEMA)).validate(self.doc)

    def test_menu(self):
        d = self.doc
        self.assertEqual(d['option_id'], KEY)
        self.assertEqual(d['menu']['path'], ['Company setup', 'Distributor Profile', 'Distributor Profile HQ'])
        self.assertEqual(d['menu']['top_id'], 'NG02')
        self.assertEqual(d['layout_code'], 'L__BusinessEntityProfile')
        self.assertEqual(d['kind'], 'dynamic')

    def test_live_id_wins_over_config(self):
        f = self.doc['fields']['Off Days']
        self.assertEqual(f['element'], 'DDL__epp1_offdays')
        self.assertEqual(f['locator'], {'id': 'DDL__epp1_offdays'})
        self.assertEqual(f['widget'], 'tagbox')
        self.assertEqual(f['provenance']['source'], 'recorded')
        self.assertEqual(f['provenance']['env'], 'cnr1dev1')
        self.assertEqual(f['data_field'], 'EPP1_OFFDAYS')            # config facts stay
        self.assertEqual(f['env_elements']['cnr2dev3'], 'TXT__epp1_offdays')

    def test_difference_recorded(self):
        whats = {(d['what'], d['config'], d['live']) for d in self.doc['differences']}
        self.assertIn(("field 'Off Days' widget", 'text', 'tagbox'), whats)
        self.assertIn(("field 'Off Days' element", 'TXT__epp1_offdays', 'DDL__epp1_offdays'), whats)

    def test_tabs_buttons_grid(self):
        d = self.doc
        demo = next(t for t in d['tabs'] if t['label'] == 'Demographics')
        self.assertEqual(demo['element'], 'tab_2')
        self.assertEqual(d['buttons']['Update']['element'], 'update')
        self.assertIn('updateBtn', d['buttons']['Update']['alt_elements'])
        g = d['grids']['Distributor List']
        self.assertEqual(g['element'], 'dataGrid')
        self.assertEqual(g['row_id_pattern'], 'row_N_distributor')
        self.assertIn('row_by_first_cell', g)

    def test_messages_lessons_rules(self):
        d = self.doc
        self.assertIn(('toast-success', 'Updated successfully'), {(m['type'], m['text']) for m in d['messages']})
        texts = ' '.join(l['text'] for l in d['lessons'])
        for needle in ('already selected removes it', '.dx-tagbox', 'below the fold', '#tab_2'):
            self.assertIn(needle, texts)
        self.assertIn('Sub Distributor = No', d['fields']['Report To']['disable_rule'])
        self.assertNotIn('<!--i-->', json.dumps(d))

    def test_deterministic(self):
        again = M.build(M.Context(), KEY)
        self.assertEqual(json.dumps(self.doc, sort_keys=True), json.dumps(again, sort_keys=True))

    def test_hand_lesson_and_status_kept(self):
        tmp = tempfile.mkdtemp()
        old_out = M.OUT
        try:
            prev = copy.deepcopy(self.doc)
            prev['lessons'].append({'text': 'HAND-ADDED lesson kept on rebuild', 'kind': 'screen', 'field': None, 'source': 'test', 'date': '2026-10-15'})
            for d in prev['differences']:
                if d['what'] == "field 'Off Days' widget":
                    d['status'] = 'reported'
            with open(os.path.join(tmp, f'{KEY}.json'), 'w', encoding='utf-8') as f:
                json.dump(prev, f)
            M.OUT = tmp
            doc = M.build(self.ctx, KEY)
        finally:
            M.OUT = old_out
            shutil.rmtree(tmp, ignore_errors=True)
        self.assertIn('HAND-ADDED lesson kept on rebuild', [l['text'] for l in doc['lessons']])
        st = {d['what']: d['status'] for d in doc['differences']}
        self.assertEqual(st["field 'Off Days' widget"], 'reported')


if __name__ == '__main__':
    unittest.main(verbosity=2)
