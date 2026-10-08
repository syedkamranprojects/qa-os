"""Build the QA-team release package of QA OS (a zip of the qa-os folder), with internal material removed.

    python tools/build_release.py <version> [--out dist]

QA lead rule (2026-10-08): never mention to the QA team / trainers that knowledge was learned by reading application
source code. The working copy keeps everything; ONLY the package is cleaned:
  * left out: apps/*/knowledge/sources/code/ (code studies), learning-session reports of code studies, runs/, dist/,
    inbox/, .git/, credential and local-settings files, caches;
  * written documents (.md/.txt/.html): every line ending with the internal marker <!--i--> (code-derived facts, see
    knowledge-intake method E) is dropped; as a safety net, remaining [code ...] clauses are removed, known phrases get
    neutral wording, and the "source code" training method and the [code] tag row are removed;
  * program and data files (.py, .js, .json, .yaml, .csv) are copied unchanged;
  * the build FAILS if a [code tag in the working copy has no <!--i--> marker, or if any blocked term (repository,
    branches, .java paths, "source code", "code study"...) is still present in a shared document.
Nothing in the working copy is changed.
"""
import os, re, shutil, sys, tempfile, zipfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# written documents only. Program files (.py, .js: e.g. WIDGET[code] is Python, not a tag) and data files (.json, .yaml,
# .csv: DB / framework extracts where "Code:" is real data) are copied unchanged; code-study content only lives in Markdown.
TEXT = ('.md', '.txt', '.html')

SKIP_DIRS = {'.git', 'runs', 'dist', 'inbox', '__pycache__', '.pytest_cache', 'node_modules'}
SKIP_PATH = [re.compile(p) for p in (
    r'^apps/[^/]+/knowledge/sources/code(/|$)',
    r'learning_sessions/[^/]*code[^/]*_report\.md$',
    r'^docs/memory_export/reference_ms_promotion_repo\.md$',
    r'^tools/build_release\.py$',          # the packaging tool itself stays internal
    r'(^|/)\.claude/settings\.local\.json$',
    r'(^|/)credentials\.json$',
)]

# ordered replacements applied to every shared text file (internal references are rewritten INSIDE the line;
# whole lines are dropped only when a blocked term still remains afterwards)
REPLACE = [
    (r'\[code [^\]]*\]', '[internal, to be confirmed live]'),
    (r'(?:\.\./)*(?:\.\./|apps/[^/\s]+/knowledge/)?sources/code/MS_Promotion/?(?:[\w.-]+\.md)?(?: \([^)]*\))?', 'internal notes'),
    (r'\bR1_(?:engine|budget_api|vs_R2)\.md\b', 'internal notes'),
    (r'learning_sessions/2026-10-08_SND-GLOBAL_code_MS_Promotion_report\.md|2026-10-08_SND-GLOBAL_code_MS_Promotion_report\.md', 'internal notes'),
    (r',? ?\(?method [A-E][,:]? ?source[ -]code\)?', ''),
    (r'\bMS_Promotion\b(?: source code)?,? ?(?:branch )?', ''),
    (r'\b(?:origin/)?UL-R[12]-[A-Z]+(?:-HOTFIX)? ?@ ?[0-9a-f]{7,8}\b,?', ''),
    (r'\b(?:origin/)?(?:UL-R1-BD|UL-R2-COUNTRY|NonUL-SDMS)\b,?', ''),
    (r'\b[\w/.-]*\w\.java(?::\d+(?:-\d+)?)?', ''),
    (r'\bsource-code\b', 'internal'),
    (r'\bsource code\b', 'internal review'),
    (r'\b[Cc]ode stud(?:y|ies)\b', 'internal review'),
    (r'\[code\]', '[internal]'),
    (r'\b(?:by )?the caller\b', 'by another part of the application'),
    (r'\bcaller\b', 'other part of the application'),
    (r'\b(?:promotion )?microservice\b', 'promotion module'),
    (r'\(code\)', '(internal)'),
    (r'\bcode evidence\b', 'internal evidence'),
    (r'[Aa]nswered by code', 'answered internally'),
    (r'\bCode diff list\b', 'Internal list'),
    (r'\bCode:', 'Internal review:'),
    (r'\bcodebase\b', 'internal review'),
    (r'\( ?,? ?\)', ''),
]
# sections removed from specific files: (path, start regex, end regex = next heading of same or higher level)
DROP_SECTIONS = [
    ('plugins/qa-os/skills/knowledge-intake/SKILL.md', r'^### E\. Source code', r'^#{2,3} '),
]
DROP_LINES = [
    ('docs/LEARNING_STANDARD.md', r'^\| `\[code\]` '),
]
# case-sensitive on purpose: DB columns such as PPMS_PROMOTION_CODE and the "Source code legend" of question ids are fine
TRIGGER = re.compile(r'\[code|[Cc]ode stud|\(code\)|[Aa]nswered by code|\bcode evidence\b|Code diff list|\bCode:|\bcaller\b|microservice')
BLOCKED = re.compile(r'PromotionBuilder|read on branch|\bmicroservice\b|[Cc]ode stud|\[code\]|\bMS_Promotion\b|sources/code|\bsource[ -]code\b|UL-R1-BD|UL-R2-COUNTRY|NonUL-SDMS|\w\.java\b|\bcodebase\b|R1_engine|R1_budget_api|R1_vs_R2|\[code ')


NL, DROP = chr(10), '<<DROP>>'
SEG = re.compile(r'(?<=[.;])\s+(?=\S)')


def strip_code_facts(line):
    """Remove every sentence / clause carrying a [code ...] tag; table cells keep their other facts.
    A line whose content becomes empty is dropped (marker)."""
    if '[code ' not in line:
        return line
    def keep(part):
        segs = [x for x in SEG.split(part) if '[code ' not in x]
        return ' '.join(segs).strip()
    if line.lstrip().startswith('|'):
        cells = line.split('|')
        new = [keep(c) if '[code ' in c else c.strip() for c in cells]
        inner = [c for c in new[1:-1]]
        if sum(1 for c in inner if c) <= 1:          # only an id / label left: the row was a code row
            return DROP
        # a row that carried code evidence is shared only if another source (stated / observed / db) still backs it
        if not re.search(r'\[(?:stated|observed|db)\b', ' '.join(inner)):
            return DROP
        return '| ' + ' | '.join(inner) + ' |'
    prefix = re.match(r'^\s*(?:[-*]|\d+\.)?\s*', line).group(0)
    rest = keep(line[len(prefix):])
    return prefix + rest if rest and re.search(r'\w{3}', rest) else DROP


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, '/')


def skipped(r):
    return any(x.search(r) for x in SKIP_PATH)


INTERNAL = re.compile(r'<!--i-->\s*$')        # end-of-line marker of a code-derived (internal) line


def clean(r, text):
    # 1) lines marked internal are never shared (the main mechanism; see knowledge-intake method E)
    text = NL.join(l for l in text.split(NL) if not INTERNAL.search(l))
    for path, start, end in DROP_SECTIONS:
        if r == path:
            lines, out, drop = text.split('\n'), [], False
            for l in lines:
                if re.match(start, l):
                    drop = True
                    continue
                if drop and re.match(end, l):
                    drop = False
                if not drop:
                    out.append(l)
            text = '\n'.join(out)
    for path, pat in DROP_LINES:
        if r == path:
            text = '\n'.join(l for l in text.split('\n') if not re.match(pat, l))
    # gate: after the marked lines and the removed sections, no [code fact may be left (it lacks the marker)
    unmarked = [l.strip() for l in text.split(NL) if '[code ' in l]
    if '[code ' in text:                                # facts learned from the code stay internal: remove them
        text = NL.join(l for l in (strip_code_facts(l) for l in text.split(NL)) if l != DROP)
    if TRIGGER.search(text) or BLOCKED.search(text):      # only files that mention internal sources are rewritten
        for pat, new in REPLACE:
            text = re.sub(pat, new, text)
    # a line still naming the repository / branches / source files is internal: drop it
    dropped = [l for l in text.split('\n') if BLOCKED.search(l)]
    text = '\n'.join(l for l in text.split('\n') if not BLOCKED.search(l))
    return text, dropped, unmarked


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    version = sys.argv[1]
    out_dir = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else os.path.join(ROOT, 'dist')
    stage = tempfile.mkdtemp(prefix='qaos_release_')
    report = {'skipped': 0, 'cleaned': 0, 'dropped': [], 'unmarked': []}
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            src = os.path.join(dp, fn)
            r = rel(src)
            if skipped(r):
                report['skipped'] += 1
                continue
            dst = os.path.join(stage, 'qa-os', r)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if fn.lower().endswith(TEXT) and r != 'tools/build_release.py':
                text = open(src, encoding='utf-8', errors='surrogateescape').read()
                new, dropped, unmarked = clean(r, text)
                report['unmarked'] += [f'{r}: {u[:90]}' for u in unmarked]
                if new != text:
                    report['cleaned'] += 1
                report['dropped'] += [(r, l.strip()[:120]) for l in dropped]
                open(dst, 'w', encoding='utf-8', errors='surrogateescape', newline='').write(new)
            else:
                shutil.copy2(src, dst)
    # final gate: nothing internal left in any shared text file
    left = []
    for dp, _, fns in os.walk(stage):
        for fn in fns:
            if fn.lower().endswith(TEXT) and fn != 'build_release.py':
                p = os.path.join(dp, fn)
                for i, l in enumerate(open(p, encoding='utf-8', errors='ignore'), 1):
                    if BLOCKED.search(l):
                        left.append(f'{os.path.relpath(p, stage)}:{i}: {l.strip()[:100]}')
    if report['unmarked']:
        shutil.rmtree(stage, ignore_errors=True)
        sys.exit('REFUSED: [code] facts without the internal marker <!--i--> (mark them, knowledge-intake method E):\n  '
                 + '\n  '.join(report['unmarked'][:40]))
    if left:
        shutil.rmtree(stage, ignore_errors=True)
        sys.exit('REFUSED: internal references remain:\n' + '\n'.join(left[:40]))
    os.makedirs(out_dir, exist_ok=True)
    zp = os.path.join(out_dir, f'qa-os-v{version}.zip')
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for dp, _, fns in os.walk(stage):
            for fn in fns:
                p = os.path.join(dp, fn)
                z.write(p, os.path.relpath(p, stage))
    shutil.rmtree(stage, ignore_errors=True)
    print(f"{zp}\n  left out {report['skipped']} internal file(s); cleaned {report['cleaned']} text file(s); "
          f"dropped {len(report['dropped'])} line(s) that still named internal sources")
    for r, l in report['dropped'][:60]:
        print(f'    - {r}: {l}')


if __name__ == '__main__':
    main()
