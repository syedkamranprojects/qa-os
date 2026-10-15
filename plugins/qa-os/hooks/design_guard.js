#!/usr/bin/env node
/*
 * QA OS design guard (decision 17.1, docs/DESIGN_V4_DECISIONS.md) - a PreToolUse hook (hooks/hooks.json).
 *
 * In a QA installation (no qaos.dev.yaml in the qa-os folder; release.json tells the version - the same rule as
 * runtime/qaos_config.py installation()), QA members may change business knowledge, runs, inbox and feedback, but
 * not the QA OS design. A Write / Edit / NotebookEdit, or a shell command that writes a file, whose target is a design
 * path is blocked (exit code 2, the reason goes back to Claude) and noted in feedback/design_gaps.md.
 * In the dev installation (qaos.dev.yaml present) and outside a qa-os folder the hook does nothing.
 *
 * Design paths (relative to the qa-os folder): plugins/**, runtime/**, tools/**, framework/tools/**, apps/<app>/tools/**,
 * docs/*DESIGN*, docs/OPERATING_RULES.md, docs/V4_*, qaos.yaml, CLAUDE.md.
 * Input (stdin): {tool_name, tool_input: {file_path | notebook_path | command}, cwd}.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const DEV_MARKER = 'qaos.dev.yaml';
const RELEASE_INFO = 'release.json';
const DESIGN = [
  /^plugins\//i, /^runtime\//i, /^tools\//i, /^framework\/tools\//i, /^apps\/[^/]+\/tools\//i,
  /^docs\/[^/]*design[^/]*$/i, /^docs\/operating_rules\.md$/i, /^docs\/v4_[^/]*$/i, /^qaos\.yaml$/i, /^claude\.md$/i,
];
const WRITE_CMDS = /^(cp|mv|install|rm|rmdir|touch|mkdir|truncate|tee|ln|rsync|dd|unzip|tar|set-content|add-content|out-file|new-item|remove-item|copy-item|move-item|rename-item|clear-content|del|erase|copy|move|ren|rename|md|ni|ri|rm|cpi|mi|sc|ac)$/i;
// inline code that writes files (python -c, node -e, heredocs); redirections and file commands are parsed exactly
// above, so running a runtime tool with its output redirected into runs/ is never mistaken for a design change
const WRITE_HINT = /(\bopen\([^)]*,\s*['"][wax]|write_text|write_bytes|\.write\(|shutil\.(copy|move|rmtree)|os\.(remove|unlink|rename|replace)|writeFileSync|appendFileSync|\[IO\.File\]::Write)/i;

function winPath(p) {
  // Git-bash style /c/dir -> C:/dir (Windows only)
  if (process.platform === 'win32') {
    const m = /^\/([a-zA-Z])(\/.*)?$/.exec(p);
    if (m) return `${m[1].toUpperCase()}:${m[2] || '/'}`;
  }
  return p;
}

function unquote(t) {
  return t.replace(/^(['"])(.*)\1$/s, '$2');
}

function findRoot(abs) {
  let dir = abs;
  for (let i = 0; i < 40; i++) {
    if (fs.existsSync(path.join(dir, 'qaos.yaml')) && fs.existsSync(path.join(dir, 'plugins', 'qa-os'))) return dir;
    const up = path.dirname(dir);
    if (up === dir) return null;
    dir = up;
  }
  return null;
}

function mode(root) {
  return fs.existsSync(path.join(root, DEV_MARKER)) ? 'dev' : 'qa';
}

function isDesign(rel) {
  return DESIGN.some((rx) => rx.test(rel));
}

function words(segment) {
  return (segment.match(/"[^"]*"|'[^']*'|[^\s]+/g) || []).map(unquote);
}

/* write targets of a shell command (bash or PowerShell): redirections, file-writing commands, and - when the command
   clearly writes (python -c open(..,'w'), Set-Content, sed -i, ...) - every path-like word in it */
function shellTargets(cmd) {
  const out = new Set();
  const redir = /(^|[^0-9&<>=-])>{1,2}\s*("[^"]+"|'[^']+'|[^\s;&|<>()]+)/g;
  let m;
  while ((m = redir.exec(cmd))) {
    const t = unquote(m[2]);
    if (!/^(\/dev\/null|nul|\$null|&\d)$/i.test(t)) out.add(t);
  }
  for (const seg of cmd.split(/&&|\|\||[;|\n]/)) {
    const w = words(seg.trim()).filter((x) => !/^\w+=/.test(x));
    if (!w.length) continue;
    let i = 0;
    while (i < w.length && /^(sudo|command|builtin|env|nohup|time)$/.test(w[i])) i++;
    const c = (w[i] || '').replace(/^.*[\\/]/, '');
    const args = w.slice(i + 1).filter((x) => !/^-/.test(x));
    if (WRITE_CMDS.test(c)) args.forEach((a) => out.add(a));
    else if (c === 'sed' && w.slice(i + 1).some((x) => /^-i/.test(x) || x === '--in-place')) args.slice(1).forEach((a) => out.add(a));
    else if (c === 'git' && /^(checkout|restore|apply|mv|rm|am|reset|stash|clean)$/.test(args[0] || '')) args.slice(1).forEach((a) => out.add(a));
  }
  if (WRITE_HINT.test(cmd)) {
    for (const t of cmd.match(/[\w.:~\\/-]*[\\/][\w.\\/-]+|\b(?:qaos\.yaml|CLAUDE\.md)\b/g) || []) out.add(t.replace(/^['"(]+|['",)]+$/g, ''));
  }
  return [...out].filter((t) => t && !/^https?:/i.test(t));
}

function targets(input) {
  const ti = input.tool_input || {};
  const name = input.tool_name || '';
  if (/^(Write|Edit|MultiEdit)$/.test(name)) return [ti.file_path].filter(Boolean);
  if (name === 'NotebookEdit') return [ti.notebook_path || ti.file_path].filter(Boolean);
  if (/^(Bash|PowerShell)$/.test(name) && ti.command) return shellTargets(String(ti.command));
  return [];
}

function note(root, tool, rels, input) {
  const p = path.join(root, 'feedback', 'design_gaps.md');
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  const stamp = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
  const who = process.env.USERNAME || process.env.USER || '';
  const esc = (s) => String(s).replace(/\|/g, '\\|').replace(/\s+/g, ' ').slice(0, 200);
  const line = `| ${stamp} | ${esc(who)} | ${esc(input.session_id ? `session ${input.session_id}` : '-')} | design guard (${esc(tool)}) | `
    + `Blocked a change to QA OS design: ${esc(rels.join(', '))} | Contact the QA OS administrator | open |\n`;
  try {
    fs.mkdirSync(path.dirname(p), { recursive: true });
    let pre = '';
    if (fs.existsSync(p)) {
      const cur = fs.readFileSync(p, 'utf8');
      if (cur && !cur.endsWith('\n')) pre = '\n';
    }
    fs.appendFileSync(p, pre + line, 'utf8');
  } catch (e) { /* the block itself still happens */ }
}

function contact(root) {
  try {
    return JSON.parse(fs.readFileSync(path.join(root, RELEASE_INFO), 'utf8')).design_contact || 'Syed Kamran';
  } catch (e) {
    return 'Syed Kamran';
  }
}

function decide(input) {
  const cwd = winPath(input.cwd || process.cwd());
  const blocked = {};
  for (const t of targets(input)) {
    const abs = path.resolve(cwd, winPath(t));
    const root = findRoot(path.dirname(abs)) || (fs.existsSync(abs) && fs.statSync(abs).isDirectory() ? findRoot(abs) : null);
    if (!root || mode(root) !== 'qa') continue;
    const rel = path.relative(root, abs).split(path.sep).join('/');
    if (!rel || rel.startsWith('..')) continue;
    if (isDesign(rel)) (blocked[root] = blocked[root] || []).push(rel);
  }
  const roots = Object.keys(blocked);
  if (!roots.length) return null;
  for (const r of roots) note(r, input.tool_name, [...new Set(blocked[r])], input);
  return `QA OS design changes are not allowed in the QA installation. Please contact the QA OS administrator (${contact(roots[0])}). `
    + 'The request is noted in feedback/design_gaps.md.'
    + ` (blocked: ${[...new Set(roots.flatMap((r) => blocked[r]))].join(', ')})`;
}

function main() {
  let raw = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (c) => { raw += c; });
  process.stdin.on('end', () => {
    let input;
    try {
      input = JSON.parse(raw || '{}');
    } catch (e) {
      process.exit(0);           // not a hook payload: never block on a parse problem
    }
    let msg = null;
    try {
      msg = decide(input);
    } catch (e) {
      process.exit(0);
    }
    if (msg) {
      process.stderr.write(msg + '\n');
      process.exit(2);
    }
    process.exit(0);
  });
}

if (require.main === module) main();
module.exports = { decide, shellTargets, isDesign, findRoot, mode };
