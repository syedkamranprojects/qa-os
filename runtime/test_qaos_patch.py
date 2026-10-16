"""Tests for runtime/qaos_patch.py: export on a simulated QA installation, show / apply on a simulated dev copy
(new, changed, unchanged-not-carried, conflict, internal lines, ignored design files), refusal of apply in qa mode, import-local.

  python runtime/test_qaos_patch.py

Everything happens in temporary folders; the real working copy is not touched. No browser, no database.
"""
import contextlib, datetime, io, json, os, shutil, sys, tempfile, time, unittest, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qaos_patch as P   # noqa: E402

DEV_FILES = {
    'apps/snd/knowledge/business/a.md': '# A\nrule 1\n',
    'apps/snd/knowledge/business/b.md': '# B\nrule 1\n',
    'apps/snd/knowledge/business/c.md': '# C\nrule 1\n',
    'apps/snd/knowledge/business/d.md': '# D\nrule 1\nrule from the code <!--i-->\n',
    'apps/snd/knowledge/sources/code/study.md': 'internal\n',
    'apps/snd/screens/ORDER.json': '{"title": "Order"}',
    'apps/snd/tools/t.py': 'print(1)\n',
    'feedback/design_gaps.md': '| Date |\n|---|\n',
    'docs/STATUS.md': 'status 1\n',
    'docs/OPERATING_RULES.md': 'rules\n',
    'runtime/x.py': 'x = 1\n',
    'qaos.yaml': 'version: 1\n',
    'plugins/qa-os/.claude-plugin/plugin.json': '{"version": "0.6.0"}',
}


def write(root, rel, text, mode='w'):
    p = os.path.join(root, *rel.split('/'))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, mode, encoding=None if 'b' in mode else 'utf-8', newline='' if 'b' not in mode else None) as f:
        f.write(text)
    return p


def read(root, rel):
    with open(os.path.join(root, *rel.split('/')), encoding='utf-8') as f:
        return f.read()


def quiet(fn, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = fn(*a, **k)
    return r, buf.getvalue()


def make_release(src, dst, version='0.6.0', built=None, hashes=True):
    """Simulate tools/build_release.py: copy src without internal lines / code studies / dev marker, + release.json."""
    clean = P._cleaner()
    files = {}
    for rel, full in P.walk(src):
        if '/sources/code/' in rel or rel.startswith('runs/') or rel.endswith('.from_qa') or rel.startswith('feedback/patches/'):
            continue
        data = P.read(full)
        data = P.released_view(rel, data, clean)
        write(dst, rel, data, 'wb')
        if P.wanted(rel):
            files[rel] = P.sha(data)
    for rel in ('qaos.yaml', 'runtime/x.py', 'plugins/qa-os/.claude-plugin/plugin.json'):
        shutil.copy2(os.path.join(src, *rel.split('/')), write(dst, rel, ''))
    info = {'mode': 'qa', 'version': version, 'built': (built or datetime.datetime.now()).isoformat(timespec='seconds')}
    if hashes:
        info['files'] = files
    write(dst, 'release.json', json.dumps(info))


class Patch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='qaos_patch_')
        self.dev = os.path.join(self.tmp, 'dev')
        self.qa = os.path.join(self.tmp, 'qa')
        for rel, text in DEV_FILES.items():
            write(self.dev, rel, text)
        write(self.dev, 'qaos.dev.yaml', 'mode: dev\n')
        make_release(self.dev, self.qa, built=datetime.datetime.now() - datetime.timedelta(days=1))
        # local training on the QA machine after the release
        write(self.qa, 'apps/snd/knowledge/business/a.md', '# A\nrule 1\nrule 2 (Fahad)\n')
        write(self.qa, 'apps/snd/knowledge/business/c.md', '# C\nrule 1\nrule 3 (Fahad)\n')
        write(self.qa, 'apps/snd/knowledge/business/d.md', '# D\nrule 1\nrule 4 (Fahad)\n')
        write(self.qa, 'apps/snd/knowledge/business/new.md', '# New page\n')
        write(self.qa, 'apps/snd/screens/PJP.json', '{"title": "PJP"}')
        write(self.qa, 'feedback/design_gaps.md', '| Date |\n|---|\n| 2026-10-19 | Fahad | need X |\n')
        write(self.qa, 'feedback/patches/old.zip', 'old', 'w')
        write(self.qa, 'docs/STATUS.md', 'status 1\nQA note\n')
        write(self.qa, 'runs/T-1/20261019-1000/run.json', '{"key": "T-1"}')
        write(self.qa, 'runs/T-1/20261019-1000/cases.json', '{}')
        write(self.qa, 'runs/T-1/20261019-1000/T-1_TestCases.xlsx', 'xlsx', 'w')
        write(self.qa, 'runs/T-1/20261019-1000/recording_P1.json', '{}')
        write(self.qa, 'runs/T-1/20261019-1000/exec/P1/results.json', '{}')
        write(self.qa, 'runs/T-1/20261019-1000/exec/P1/shot.png', 'png', 'w')
        write(self.qa, 'runs/T-1/20261019-1000/downloads/report.xlsx', 'x', 'w')
        write(self.qa, 'runs/T-1/20261019-1000/log.txt', 'log', 'w')
        write(self.qa, 'apps/snd/knowledge/business/big.png', b'\0' * (P.BIG_IMAGE + 1), 'wb')
        write(self.qa, 'apps/snd/knowledge/credentials.json', '{"password": "x"}')
        write(self.qa, '.claude/settings.local.json', '{}')
        write(self.qa, 'runtime/x.py', 'x = 2  # QA hack\n')
        # dev work since the release
        write(self.dev, 'apps/snd/knowledge/business/a.md', '# A\nrule 1\nrule 9 (Syed)\n')
        write(self.dev, 'apps/snd/knowledge/business/b.md', '# B\nrule 1\nrule 8 (Syed)\n')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def export(self, root=None, note='need a new event'):
        (zp, man), out = quiet(P.export, root or self.qa, note)
        return zp, man, out

    def test_export_contents(self):
        zp, man, out = self.export()
        self.assertTrue(os.path.basename(zp).startswith('qaos_patch_'))
        self.assertEqual(os.path.dirname(zp), os.path.join(self.qa, 'feedback', 'patches'))
        names = set(zipfile.ZipFile(zp).namelist())
        for rel in ('apps/snd/knowledge/business/a.md', 'apps/snd/knowledge/business/new.md', 'apps/snd/screens/PJP.json',
                    'feedback/design_gaps.md', 'docs/STATUS.md', 'runs/T-1/20261019-1000/run.json',
                    'runs/T-1/20261019-1000/T-1_TestCases.xlsx', 'runs/T-1/20261019-1000/recording_P1.json',
                    'runs/T-1/20261019-1000/exec/P1/results.json', P.MANIFEST):
            self.assertIn(rel, names)
        for rel in ('feedback/patches/old.zip', 'runtime/x.py', 'qaos.yaml', 'release.json', '.claude/settings.local.json',
                    'apps/snd/knowledge/credentials.json', 'apps/snd/knowledge/business/big.png', 'apps/snd/tools/t.py',
                    'runs/T-1/20261019-1000/log.txt', 'runs/T-1/20261019-1000/downloads/report.xlsx',
                    'runs/T-1/20261019-1000/exec/P1/shot.png', 'docs/OPERATING_RULES.md'):
            self.assertNotIn(rel, names)
        self.assertEqual(man['mode'], 'qa')
        self.assertEqual(man['version'], '0.6.0')
        self.assertEqual(man['note'], 'need a new event')
        self.assertTrue(man['base']['has_file_hashes'])
        st = {f['path']: f['qa_state'] for f in man['files']}
        self.assertEqual(st['apps/snd/knowledge/business/a.md'], 'changed')
        self.assertNotIn('apps/snd/knowledge/business/b.md', st)          # unchanged since the release: not carried
        self.assertEqual(man['skipped']['unchanged since the release'], 2)  # b.md, screens/ORDER.json
        self.assertEqual(st['apps/snd/knowledge/business/new.md'], 'new')
        self.assertTrue(all(len(f['sha256']) == 64 for f in man['files']))

    def test_show_and_apply_dev(self):
        zp, _, _ = self.export()
        with zipfile.ZipFile(zp, 'a') as z:            # a hand-made entry: design files are never applied
            z.writestr('runtime/qaos_run.py', 'evil')
            z.writestr('plugins/qa-os/skills/x/SKILL.md', 'evil')
            z.writestr('docs/OPERATING_RULES.md', 'evil')
            z.writestr('../outside.txt', 'evil')
        rows, out = quiet(P.cmd_show, self.dev, zp)
        st = {rel: s for s, rel, _ in rows}
        self.assertEqual(st['apps/snd/knowledge/business/a.md'], 'conflict')      # both sides
        self.assertNotIn('apps/snd/knowledge/business/b.md', st)                # dev only: not in the patch
        self.assertEqual(st['apps/snd/knowledge/business/c.md'], 'changed')       # QA only
        self.assertEqual(st['apps/snd/knowledge/business/d.md'], 'conflict')      # dev page has internal lines
        self.assertEqual(st['apps/snd/knowledge/business/new.md'], 'new')
        self.assertEqual(st['apps/snd/screens/PJP.json'], 'new')
        self.assertEqual(st['runs/T-1/20261019-1000/run.json'], 'new')
        for rel in ('runtime/qaos_run.py', 'plugins/qa-os/skills/x/SKILL.md', 'docs/OPERATING_RULES.md', '../outside.txt'):
            self.assertEqual(st[rel], 'ignored', rel)
        self.assertIn('CONFLICT', out)
        # dry run writes nothing
        quiet(P.cmd_apply, self.dev, zp, False)
        self.assertFalse(os.path.exists(os.path.join(self.dev, 'apps', 'snd', 'knowledge', 'business', 'new.md')))
        rc, out = quiet(P.cmd_apply, self.dev, zp, True)
        self.assertEqual(rc, 0)
        self.assertEqual(read(self.dev, 'apps/snd/knowledge/business/a.md'), '# A\nrule 1\nrule 9 (Syed)\n')
        self.assertEqual(read(self.dev, 'apps/snd/knowledge/business/a.md.from_qa'), '# A\nrule 1\nrule 2 (Fahad)\n')
        self.assertEqual(read(self.dev, 'apps/snd/knowledge/business/b.md'), '# B\nrule 1\nrule 8 (Syed)\n')
        self.assertEqual(read(self.dev, 'apps/snd/knowledge/business/c.md'), '# C\nrule 1\nrule 3 (Fahad)\n')
        self.assertIn('<!--i-->', read(self.dev, 'apps/snd/knowledge/business/d.md'))
        self.assertTrue(os.path.exists(os.path.join(self.dev, 'apps', 'snd', 'knowledge', 'business', 'd.md.from_qa')))
        self.assertEqual(read(self.dev, 'apps/snd/knowledge/business/new.md'), '# New page\n')
        self.assertEqual(read(self.dev, 'docs/STATUS.md'), 'status 1\nQA note\n')
        self.assertEqual(read(self.dev, 'runtime/x.py'), 'x = 1\n')
        self.assertEqual(read(self.dev, 'docs/OPERATING_RULES.md'), 'rules\n')
        self.assertFalse(os.path.exists(os.path.join(self.dev, 'runtime', 'qaos_run.py')))
        self.assertFalse(os.path.exists(os.path.join(self.tmp, 'outside.txt')))
        self.assertTrue(any(f.startswith('applied_') for f in os.listdir(os.path.join(self.dev, 'feedback', 'patches'))))

    def test_date_fallback_without_hashes(self):
        os.remove(os.path.join(self.qa, 'release.json'))
        write(self.qa, 'release.json', json.dumps({'mode': 'qa', 'version': '0.5.0',
                                                    'built': (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(timespec='seconds')}))
        zp, man, _ = self.export()
        self.assertFalse(man['base']['has_file_hashes'])
        old = time.time() - 3 * 86400                  # c.md in dev untouched since before the base build
        os.utime(os.path.join(self.dev, 'apps', 'snd', 'knowledge', 'business', 'c.md'), (old, old))
        rows, _ = quiet(P.cmd_show, self.dev, zp)
        st = {rel: s for s, rel, _ in rows}
        self.assertEqual(st['apps/snd/knowledge/business/a.md'], 'conflict')      # dev file newer than the base
        self.assertEqual(st['apps/snd/knowledge/business/c.md'], 'changed')

    def test_apply_refused_in_qa(self):
        zp, _, _ = self.export()
        before = read(self.qa, 'apps/snd/knowledge/business/a.md')
        rc, out = quiet(P.cmd_apply, self.qa, zp, True)
        self.assertEqual(rc, 2)
        self.assertIn('REFUSED', out)
        self.assertEqual(read(self.qa, 'apps/snd/knowledge/business/a.md'), before)

    def test_import_local_over_new_release(self):
        zp, _, _ = self.export()
        # dev applied the patch, merged a.md by hand, and builds a new release; QA installs it in a fresh folder
        quiet(P.cmd_apply, self.dev, zp, True)
        write(self.dev, 'apps/snd/knowledge/business/a.md', '# A\nrule 1\nrule 2 (Fahad)\nrule 9 (Syed)\n')
        write(self.dev, 'apps/snd/knowledge/business/b.md', '# B\nrule 1\nrule 8 (Syed) v2\n')
        new = os.path.join(self.tmp, 'qa2')
        make_release(self.dev, new, version='0.7.0')
        # training the QA machine made AFTER sending the patch is in a later export of the old installation
        write(self.qa, 'apps/snd/knowledge/business/c.md', '# C\nrule 1\nrule 3 (Fahad)\nrule 5 (Fahad, later)\n')
        time.sleep(0.01)
        (zp2, man2), _ = quiet(P.export, self.qa, 'before upgrade', os.path.join(self.tmp, 'out'))
        c = [f for f in man2['files'] if f['path'] == 'apps/snd/knowledge/business/c.md'][0]
        self.assertEqual(len(c['sent_sha256']), 1)        # the version sent in the first patch
        rc, out = quiet(P.cmd_apply, new, zp2, False, local=True)
        rows_out = out
        self.assertEqual(rc, 0)
        self.assertIn('NEW', rows_out)
        rc, out = quiet(P.cmd_apply, new, zp2, True, local=True)
        self.assertEqual(rc, 0)
        self.assertEqual(read(new, 'apps/snd/knowledge/business/c.md'), '# C\nrule 1\nrule 3 (Fahad)\nrule 5 (Fahad, later)\n')
        # a.md: the new release changed it AND the QA side had changed it since the old release -> conflict, release kept
        self.assertEqual(read(new, 'apps/snd/knowledge/business/a.md'), '# A\nrule 1\nrule 2 (Fahad)\nrule 9 (Syed)\n')
        self.assertTrue(os.path.exists(os.path.join(new, 'apps', 'snd', 'knowledge', 'business', 'a.md.from_qa')))
        # b.md: unchanged on the QA side -> the new release's version stays
        self.assertEqual(read(new, 'apps/snd/knowledge/business/b.md'), '# B\nrule 1\nrule 8 (Syed) v2\n')
        # runs come back; docs/STATUS.md is not re-applied by import-local
        self.assertTrue(os.path.exists(os.path.join(new, 'runs', 'T-1', '20261019-1000', 'run.json')))
        self.assertEqual(read(new, 'docs/STATUS.md'), 'status 1\nQA note\n')   # from the release (dev applied it)
        self.assertNotIn('qaos.dev.yaml', os.listdir(new))

    def test_cli(self):
        zp, _, _ = self.export()
        import subprocess
        r = subprocess.run([sys.executable, os.path.join(HERE, 'qaos_patch.py'), '--root', self.qa, 'apply', zp],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        r = subprocess.run([sys.executable, os.path.join(HERE, 'qaos_patch.py'), '--root', self.dev, 'show', zp],
                           capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('CONFLICT', r.stdout)
        r = subprocess.run([sys.executable, os.path.join(HERE, 'qaos_patch.py'), '--root', self.qa, 'export', '--note', 'x',
                            '--out', os.path.join(self.tmp, 'o2')], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('Send this file to Syed Kamran', r.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=1)
