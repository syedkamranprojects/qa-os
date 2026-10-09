"""Regression test for gen_framework_sql.py (multi-screen specs).

  python framework/tools/test_gen_framework_sql.py

Regenerates from runs/QUICK-20261008-OB/20261008-1120/attempt2_superseded/framework/flow_spec.json (3 screens, written by the
framework-generator agent with a one-off script) and compares with that run's framework.sql, rollback and workbook:
the INSERT rows must be the same set (column -> value, ignoring statement order and comments), the pre-flight must
check the same ids and event pairs, and the workbook must have the same sheets and cells. The case-data rows are not in
the spec, so they are copied from the agent's workbook into a temporary spec. Nothing is applied to any database.
"""
import copy, json, os, re, subprocess, sys, tempfile, unittest
from collections import Counter

import openpyxl

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(TOOLS))
RUN = os.path.join(ROOT, 'runs', 'QUICK-20261008-OB', '20261008-1120', 'attempt2_superseded', 'framework')
GEN = os.path.join(TOOLS, 'gen_framework_sql.py')
BOOK = 'NG_Dcode_QA_QUICK_OrderBooking (Pak).xlsx'


def sql_values(s):
    """Split a VALUES (...) list into python values: 'x' -> str, NULL -> None, 12 -> int, now() -> 'now()'."""
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c in ' ,\n':
            i += 1
        elif c == "'":
            j, buf = i + 1, []
            while True:
                if s[j] == "'" and s[j + 1:j + 2] == "'":
                    buf.append("'"); j += 2
                elif s[j] == "'":
                    break
                else:
                    buf.append(s[j]); j += 1
            out.append(''.join(buf)); i = j + 1
        else:
            m = re.match(r"NULL|now\(\)|-?\d+", s[i:])
            assert m, f'cannot parse value at {s[i:i + 30]!r}'
            tok = m.group(0)
            out.append(None if tok == 'NULL' else tok if tok == 'now()' else int(tok)); i += len(tok)
    return out


def inserts(sql):
    """Multiset of (table, frozenset(column -> value)) for every INSERT."""
    rows = Counter()
    for t, cols, vals in re.findall(r"INSERT INTO (\w+) \(([^)]*)\)\s*VALUES \((.*?)\);\n", sql, re.S):
        cols = [c.strip() for c in cols.split(',')]
        vals = sql_values(vals)
        assert len(cols) == len(vals), (t, cols, vals)
        rows[(t, frozenset(zip(cols, vals)))] += 1
    return rows


def preflight(sql):
    block = re.search(r'DO \$\$(.*?)END \$\$;', sql, re.S).group(1)
    ids = set(re.findall(r"'(\d{4,8})'", block))
    pairs = set(re.findall(r"\('(\d{4})','(\d{4})'\)", block))
    return ids, pairs


def deletes(sql):
    return [t for t in re.findall(r'DELETE FROM (\w+)', sql)]


def text(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write_json(obj, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False)


def read_book(path):
    wb = openpyxl.load_workbook(path)
    try:
        return {ws.title: [list(r) for r in ws.iter_rows(values_only=True)] for ws in wb}
    finally:
        wb.close()


def run(spec, out):
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'spec.json')
    write_json(spec, p)
    r = subprocess.run([sys.executable, GEN, p, out], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


class QuickOrderBooking(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads(text(os.path.join(RUN, 'flow_spec.json')))
        cls.ref_sql = text(os.path.join(RUN, 'framework.sql'))
        cls.ref_rb = text(os.path.join(RUN, 'framework_rollback.sql'))
        cls.ref_book = read_book(os.path.join(RUN, BOOK))
        cls.tmp = tempfile.TemporaryDirectory()
        spec = copy.deepcopy(cls.spec)
        spec['casedata'] = {'sheets': [{'sheet': n, 'columns': rows[0], 'rows': rows[1:]} for n, rows in cls.ref_book.items()]}
        cls.out = os.path.join(cls.tmp.name, 'full')
        run(spec, cls.out)
        cls.sql = text(os.path.join(cls.out, 'framework.sql'))
        cls.rb = text(os.path.join(cls.out, 'framework_rollback.sql'))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_inserts_equal_agent_output(self):
        mine, ref = inserts(self.sql), inserts(self.ref_sql)
        self.assertEqual(sum(ref.values()), 29)
        # the 10-08 reference predates the navigation-path rule (2026-10-09): its mgsm rows have no
        # pmgsm_navigation_path; the generator now writes the menu entry id there - add it to the reference rows
        nav = self.spec['menu_group']['navigation']
        fixed = Counter()
        for (t, row), n in ref.items():
            if t == 'fct_pr_mgsm_menu_group_screen_mapping' and 'pmgsm_navigation_path' not in dict(row):
                row = frozenset(set(row) | {('pmgsm_navigation_path', nav)})
            fixed[(t, row)] += n
        ref = fixed
        self.assertEqual(mine - ref, Counter(), 'rows only in the regenerated SQL')
        self.assertEqual(ref - mine, Counter(), 'rows only in the agent SQL')

    def test_every_screen_mapping_has_a_navigation_path(self):
        """QA lead 2026-10-09: generated flows ran, but the screen-mapping rows lacked NAVIGATION PATH."""
        rows = [dict(r) for (t, r), _ in inserts(self.sql).items() if t == 'fct_pr_mgsm_menu_group_screen_mapping']
        self.assertTrue(rows)
        for r in rows:
            self.assertEqual(r.get('pmgsm_navigation_path'), self.spec['menu_group']['navigation'])
            self.assertNotIn('pmgsm_navigation_type', r)       # NULL type: the engine clicks nothing extra

    def test_audit_columns(self):
        for (t, row), _ in inserts(self.sql).items():
            row = dict(row)
            self.assertEqual(row['created_by'], 'QA-OS QUICK-20261008-OB', t)
            self.assertIsNone(row['modified_date'], t)
            self.assertIsNone(row['modified_by'], t)

    def test_single_transaction_and_preflight(self):
        self.assertEqual(self.sql.count('BEGIN;'), 1)
        self.assertEqual(self.sql.count('COMMIT;'), 1)
        self.assertLess(self.sql.index('BEGIN;'), self.sql.index('DO $$'))
        self.assertLess(self.sql.index('END $$;'), self.sql.index('INSERT INTO'))
        self.assertLess(self.sql.rindex('INSERT INTO'), self.sql.index('COMMIT;'))
        self.assertEqual(preflight(self.sql), preflight(self.ref_sql))

    def test_rollback(self):
        self.assertEqual(deletes(self.rb), deletes(self.ref_rb))   # same tables, children first
        for line in self.rb.splitlines():
            if line.startswith('DELETE'):
                self.assertIn("created_by = 'QA-OS QUICK-20261008-OB'", line)
                self.assertRegex(line, r"WHERE \w+ (=|IN) ", 'scoped by id')
        self.assertIn("psc_screenid IN ('064801', '064802', '064803')", self.rb)

    def test_workbook_equal_agent_output(self):
        self.assertEqual(read_book(os.path.join(self.out, BOOK)), self.ref_book)

    def test_skeleton_workbook_without_casedata(self):
        with tempfile.TemporaryDirectory() as d:
            msg = run(copy.deepcopy(self.spec), d)
            self.assertIn('header-only', msg)
            book = read_book(os.path.join(d, BOOK))
            self.assertEqual(list(book), list(self.ref_book))
            self.assertEqual({n: r[0] for n, r in book.items()}, {n: r[0] for n, r in self.ref_book.items()})

    def test_rejects_ref_to_a_click(self):
        spec = copy.deepcopy(self.spec)
        spec['screens'][1]['events'][3]['ref'] = 3      # assertion pointing at the Validation click
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'spec.json')
            write_json(spec, p)
            r = subprocess.run([sys.executable, GEN, p, d], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('not a Load Data', r.stderr)
            self.assertFalse(os.path.exists(os.path.join(d, 'framework.sql')))


if __name__ == '__main__':
    unittest.main(verbosity=2)
