/*
 * Test of design_guard.js: a simulated qa-os folder in a temp dir, first as a QA installation (release.json, no
 * qaos.dev.yaml), then as the dev installation. Run: node plugins/qa-os/hooks/test_design_guard.js
 */
'use strict';
const assert = require('assert');
const cp = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const GUARD = path.join(__dirname, 'design_guard.js');
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'qaos_guard_'));
for (const d of ['plugins/qa-os/skills', 'runtime', 'tools', 'framework/tools', 'apps/snd/tools', 'apps/snd/knowledge/business', 'docs', 'runs/K/1', 'inbox', 'feedback']) {
  fs.mkdirSync(path.join(root, d), { recursive: true });
}
fs.writeFileSync(path.join(root, 'qaos.yaml'), 'version: 1\n');
fs.writeFileSync(path.join(root, 'release.json'), JSON.stringify({ mode: 'qa', version: '0.6.0', design_contact: 'Syed Kamran' }));
fs.writeFileSync(path.join(root, 'feedback', 'design_gaps.md'), '| Date | QA member |\n|---|---|\n');
const gaps = () => fs.readFileSync(path.join(root, 'feedback', 'design_gaps.md'), 'utf8');

function hook(tool, toolInput, cwd = root) {
  const r = cp.spawnSync(process.execPath, [GUARD], { input: JSON.stringify({ tool_name: tool, tool_input: toolInput, cwd }), encoding: 'utf8' });
  return { code: r.status, err: r.stderr };
}
const P = (...x) => path.join(root, ...x);
let n = 0;
function expect(code, tool, input, label) {
  const r = hook(tool, input);
  assert.strictEqual(r.code, code, `${label}: expected exit ${code}, got ${r.code} ${r.err}`);
  n++;
  return r;
}

// ---- QA installation: design paths blocked
let r = expect(2, 'Write', { file_path: P('runtime', 'qaos_run.py') }, 'runtime');
assert.ok(r.err.startsWith('QA OS design changes are not allowed in the QA installation. Please contact the QA OS administrator (Syed Kamran). The request is noted in feedback/design_gaps.md.'));
assert.ok(/design guard \(Write\) \| Blocked a change to QA OS design: runtime\/qaos_run\.py/.test(gaps()), 'noted in design_gaps.md');
expect(2, 'Edit', { file_path: P('plugins', 'qa-os', 'skills', 'x.md') }, 'plugins');
expect(2, 'Edit', { file_path: P('tools', 'build_release.py') }, 'tools');
expect(2, 'Edit', { file_path: P('framework', 'tools', 'gen.py') }, 'framework/tools');
expect(2, 'Write', { file_path: P('apps', 'snd', 'tools', 'b.py') }, 'apps/*/tools');
expect(2, 'Edit', { file_path: P('docs', 'DESIGN_V4_DECISIONS.md') }, 'docs DESIGN');
expect(2, 'Edit', { file_path: P('docs', 'FINAL_DESIGN.md') }, 'docs *DESIGN*');
expect(2, 'Edit', { file_path: P('docs', 'OPERATING_RULES.md') }, 'operating rules');
expect(2, 'Edit', { file_path: P('docs', 'V4_IMPLEMENTATION_PLAN.md') }, 'docs V4_');
expect(2, 'Edit', { file_path: P('qaos.yaml') }, 'qaos.yaml');
expect(2, 'Edit', { file_path: P('CLAUDE.md') }, 'CLAUDE.md');
expect(2, 'NotebookEdit', { notebook_path: P('tools', 'n.ipynb') }, 'notebook');
expect(2, 'Bash', { command: 'echo x > runtime/new.py' }, 'bash redirect');
expect(2, 'Bash', { command: 'cp /tmp/a.py tools/a.py' }, 'bash cp');
expect(2, 'Bash', { command: "sed -i 's/a/b/' plugins/qa-os/skills/x.md" }, 'sed -i');
expect(2, 'Bash', { command: `python -c "open('runtime/z.py','w').write('x')"` }, 'python -c write');
expect(2, 'PowerShell', { command: 'Set-Content -Path runtime\\a.py -Value x' }, 'Set-Content');
// ---- QA installation: business knowledge, runs, inbox, feedback stay writable; reading is never blocked
expect(0, 'Write', { file_path: P('apps', 'snd', 'knowledge', 'business', 'orders.md') }, 'business knowledge');
expect(0, 'Write', { file_path: P('runs', 'K', '1', 'steps.json') }, 'runs');
expect(0, 'Write', { file_path: P('inbox', 'SDMS-1.md') }, 'inbox');
expect(0, 'Edit', { file_path: P('feedback', 'design_gaps.md') }, 'feedback');
expect(0, 'Edit', { file_path: P('docs', 'STATUS.md') }, 'other docs');
expect(0, 'Bash', { command: 'python runtime/qaos_run.py check runs/K/1 > runs/K/1/check.txt 2>&1' }, 'running a tool');
expect(0, 'Bash', { command: 'cat runtime/qaos_run.py | head -5' }, 'reading');
expect(0, 'Write', { file_path: path.join(os.tmpdir(), 'elsewhere.txt') }, 'outside qa-os');
const lines = gaps().split('\n').filter((l) => l.includes('design guard')).length;
assert.strictEqual(lines, 17, `one design_gaps line per blocked call (got ${lines})`);

// ---- dev installation: nothing is blocked
fs.writeFileSync(path.join(root, 'qaos.dev.yaml'), 'mode: dev\n');
expect(0, 'Write', { file_path: P('runtime', 'qaos_run.py') }, 'dev runtime');
expect(0, 'Bash', { command: 'echo x > tools/a.py' }, 'dev bash');

fs.rmSync(root, { recursive: true, force: true });
console.log(`design_guard: ${n} checks OK`);
