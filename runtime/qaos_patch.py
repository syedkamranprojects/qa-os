"""QA OS patch: carry local training from a QA installation to the dev copy (and back over a new release).

  python runtime/qaos_patch.py export [--note "<what I need>"] [--out feedback/patches]   # QA machine
  python runtime/qaos_patch.py show <patch.zip>                                            # dev: what would change
  python runtime/qaos_patch.py apply <patch.zip> [--yes]                                   # dev only
  python runtime/qaos_patch.py import-local <patch.zip> [--yes]                            # QA machine, after a new release

QA lead (2026-10-16): the QA installation (release zip, no git) is owned by the QA team, who train it locally (business
knowledge, screen files, runs). A patch carries that training to the dev copy; the dev copy makes the design change and
builds a new release; import-local then puts the QA machine's own latest training back on top of the new release.

What a patch holds: apps/*/knowledge/** (except sources/code/**), apps/*/screens/**, feedback/** (except
feedback/patches/), docs/STATUS.md, and of runs/<key>/<run>/ only the run record files (run.json, requirement.json,
cases.json, paths.json, steps.json, check.json, summary.md, BA_NOTE.md, friction.md, *_TestCases.xlsx, recording_*.json,
exec/**/results.json). Never: downloads, images over 2 MB, credential or local-settings files. PATCH_MANIFEST.json
records the release it is based on (files still identical to that release are left out when the release carries file
hashes), the machine user, the note and a sha256 per file (plus the file's hash in the base
release when the release carries file hashes, see tools/build_release.py).

Apply rules (apply and import-local):
  * design paths (plugins/, runtime/, tools/, framework/tools/, apps/*/tools/, schemas, docs other than STATUS.md,
    qaos.yaml, CLAUDE.md) and anything outside the patch areas are never written: listed as "ignored";
  * new -> written; same -> nothing; a file the QA side did not change since its release -> "kept" (the working copy
    is newer);
  * changed on the QA side only -> overwritten;
  * changed on BOTH sides since the base (working file differs from the base release, or - without base hashes - is
    newer than the base build date), or a dev page that holds internal lines (<!--i-->) the release never had -> the
    patch version is written beside it as <file>.from_qa and listed as a conflict; merge by hand, then delete it.
Without --yes only the plan is printed. --root <qa-os folder> is for tests.
"""
import argparse
import datetime
import fnmatch
import hashlib
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
QA_OS = os.path.normpath(os.path.join(HERE, '..'))
DEV_MARKER, RELEASE_INFO, MANIFEST = 'qaos.dev.yaml', 'release.json', 'PATCH_MANIFEST.json'
TEXT = ('.md', '.txt', '.html')
IMAGES = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.mp4', '.webm')
BIG_IMAGE = 2 * 1024 * 1024
BIG_FILE = 25 * 1024 * 1024

DESIGN = [re.compile(p, re.I) for p in (
    r'^plugins/', r'^runtime/', r'^tools/', r'^framework/tools/', r'^apps/[^/]+/tools/', r'(^|/)schemas?/',
    r'\.schema\.json$', r'^docs/(?!STATUS\.md$)', r'^qaos\.yaml$', r'^claude\.md$', r'^qaos\.dev\.yaml$', r'^release\.json$')]
RUN_FILES = ('run.json', 'requirement.json', 'cases.json', 'paths.json', 'steps.json', 'check.json', 'summary.md',
             'BA_NOTE.md', 'friction.md', '*_TestCases.xlsx', 'recording_*.json')
SECRET = re.compile(r'(^|/)(credentials\.json|settings\.local\.json|\.env|[^/]*\.env|[^/]*\.(pem|key|pfx|p12)'
                    r'|[^/]*(password|secret|token)[^/]*\.(json|ya?ml|txt|ini|cfg))$', re.I)
JUNK = re.compile(r'(^|/)(__pycache__/|~\$|\.DS_Store$|Thumbs\.db$|desktop\.ini$)|\.pyc$|\.from_qa$', re.I)


# ---------------------------------------------------------------- installation
def mode(root):
    """dev = qaos.dev.yaml present; anything else is a QA installation (same rule as qaos_config.installation())."""
    return 'dev' if os.path.exists(os.path.join(root, DEV_MARKER)) else 'qa'


def release_info(root):
    try:
        with open(os.path.join(root, RELEASE_INFO), encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def plugin_version(root):
    try:
        with open(os.path.join(root, 'plugins', 'qa-os', '.claude-plugin', 'plugin.json'), encoding='utf-8') as f:
            return json.load(f).get('version')
    except (OSError, ValueError):
        return None


def user():
    return os.environ.get('USERNAME') or os.environ.get('USER') or 'unknown'


# ---------------------------------------------------------------- paths
def area(rel):
    p = rel.split('/')
    if len(p) >= 3 and p[0] == 'apps' and p[2] in ('knowledge', 'screens'):
        return p[2]
    if p[0] in ('feedback', 'runs'):
        return p[0]
    if rel == 'docs/STATUS.md':
        return 'docs'
    return None


def is_design(rel):
    return any(x.search(rel) for x in DESIGN)


def excluded(rel, size=0):
    """Reason a file is never part of a patch, or None."""
    low = rel.lower()
    if SECRET.search(rel) or '/.claude/' in '/' + low:
        return 'credential / local settings'
    if JUNK.search(rel):
        return 'cache / temp'
    if '/downloads/' in '/' + low + '/' or low.startswith('downloads/'):
        return 'download'
    if low.endswith(IMAGES) and size > BIG_IMAGE:
        return 'image over 2 MB'
    if size > BIG_FILE:
        return 'file over 25 MB'
    return None


def wanted(rel):
    """Is this path (relative, forward slashes) part of the patch areas?"""
    a = area(rel)
    if a is None or is_design(rel):
        return False
    p = rel.split('/')
    if a == 'knowledge':
        return not (len(p) > 3 and p[3] == 'sources' and len(p) > 4 and p[4] == 'code')
    if a == 'feedback':
        return not (len(p) > 1 and p[1] == 'patches')
    if a == 'runs':
        if len(p) < 4:
            return False
        inner = p[3:]
        name = inner[-1]
        if inner[0] == 'exec':
            return name == 'results.json'
        if name.startswith('recording_') and name.endswith('.json'):
            return True
        return len(inner) == 1 and any(fnmatch.fnmatchcase(name, pat) for pat in RUN_FILES)
    return True


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    with open(path, 'rb') as f:
        return f.read()


def walk(root):
    for top in ('apps', 'feedback', 'runs', 'docs'):
        base = os.path.join(root, top)
        for dp, dns, fns in os.walk(base):
            dns[:] = [d for d in dns if d not in ('__pycache__', '.git', 'node_modules')]
            for fn in fns:
                full = os.path.join(dp, fn)
                yield os.path.relpath(full, root).replace(os.sep, '/'), full


def human(n):
    for u in ('B', 'KB', 'MB'):
        if n < 1024:
            return f'{n:.0f} {u}' if u == 'B' else f'{n:.1f} {u}'
        n /= 1024
    return f'{n:.1f} GB'


# ---------------------------------------------------------------- export
def export(root, note='', out=None, now=None):
    now = now or datetime.datetime.now()
    rel_info, m = release_info(root), mode(root)
    base_files = rel_info.get('files') or {}
    files, skipped = [], {}
    for rel, full in sorted(walk(root)):
        if not wanted(rel):
            continue
        why = excluded(rel, os.path.getsize(full))
        if why:
            skipped[why] = skipped.get(why, 0) + 1
            continue
        data = read(full)
        h = sha(data)
        b = base_files.get(rel)
        state = 'unknown' if not base_files else ('new' if b is None else ('release' if b == h else 'changed'))
        if state == 'release':                 # identical to what the release shipped: nothing to carry (lossless)
            skipped['unchanged since the release'] = skipped.get('unchanged since the release', 0) + 1
            continue
        files.append({'path': rel, 'area': area(rel), 'size': len(data), 'sha256': h, 'base_sha256': b, 'qa_state': state,
                      'mtime': datetime.datetime.fromtimestamp(os.path.getmtime(full)).isoformat(timespec='seconds')})
    out = out or os.path.join(root, 'feedback', 'patches')
    out = out if os.path.isabs(out) else os.path.join(root, out)
    sent = earlier_versions(root, out)
    for f in files:
        f['sent_sha256'] = sorted(sent.get(f['path'], set()) - {f['sha256']})
    who = user()
    manifest = {'kind': 'qaos-patch', 'format': 1,
                'version': rel_info.get('version') or plugin_version(root), 'mode': m, 'user': who,
                'machine': os.environ.get('COMPUTERNAME') or '', 'date': now.isoformat(timespec='seconds'), 'note': note or '',
                'base': {'release_version': rel_info.get('version'), 'built': rel_info.get('built'),
                         'has_file_hashes': bool(base_files)},
                'skipped': skipped, 'files': files}
    os.makedirs(out, exist_ok=True)
    safe = re.sub(r'[^\w.-]+', '_', who)
    zp = os.path.join(out, f"qaos_patch_{now.strftime('%Y%m%d-%H%M')}_{safe}.zip")
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(os.path.join(root, f['path']), f['path'])
        z.writestr(MANIFEST, json.dumps(manifest, indent=1, ensure_ascii=False))
    return zp, manifest


def earlier_versions(root, *dirs):
    """{path: {sha256}} of every file version this machine already sent in an earlier patch (its exports in
    feedback/patches). A working copy holding one of them has not changed since (e.g. the dev copy applied that patch
    into the next release), so a later patch may overwrite it."""
    seen, out = set(), {}
    for d in (os.path.join(root, 'feedback', 'patches'),) + dirs:
        if not os.path.isdir(d) or os.path.normcase(os.path.abspath(d)) in seen:
            continue
        seen.add(os.path.normcase(os.path.abspath(d)))
        for fn in os.listdir(d):
            if not (fn.startswith('qaos_patch_') and fn.endswith('.zip')):
                continue
            try:
                with zipfile.ZipFile(os.path.join(d, fn)) as z:
                    man = json.loads(z.read(MANIFEST).decode('utf-8'))
            except Exception:
                continue
            for f in man.get('files', []):
                out.setdefault(f['path'], set()).add(f['sha256'])
    return out


def print_export(zp, man):
    per = {}
    for f in man['files']:
        a = per.setdefault(f['area'], [0, 0, 0])
        a[0] += 1
        a[1] += f['size']
        a[2] += f['qa_state'] in ('new', 'changed')
    print(f"QA OS patch written: {zp}  ({human(os.path.getsize(zp))})")
    print(f"  based on release {man['base']['release_version'] or man['version']} built {man['base']['built'] or '?'}; "
          f"installation {man['mode']}; user {man['user']}")
    for a in ('knowledge', 'screens', 'feedback', 'runs', 'docs'):
        if a in per:
            n, s, ch = per[a]
            extra = f', {ch} new/changed since the release' if man['base']['has_file_hashes'] else ''
            print(f'  {a:<10} {n:>5} file(s)  {human(s):>9}{extra}')
    if man['skipped']:
        print('  left out: ' + ', '.join(f'{v} {k}' for k, v in sorted(man['skipped'].items())))
    if man['note']:
        print(f"  note: {man['note']}")
    print('\nSend this file to Syed Kamran (email / share) with:')
    print(f'  "Hi Syed, attached is my QA OS patch {os.path.basename(zp)} ({len(man["files"])} files, based on release '
          f'{man["base"]["release_version"] or man["version"]}). {("I need: " + man["note"] + ". ") if man["note"] else ""}'
          f'Please apply it with: python runtime/qaos_patch.py apply {os.path.basename(zp)}"')
    print('Keep the file: after installing the next release, run  python runtime/qaos_patch.py import-local <this zip>  '
          'with your LATEST export to keep the training you made after sending it.')


# ---------------------------------------------------------------- compare / plan
def _cleaner():
    """The release cleaner (drops <!--i--> internal lines) - only in the dev copy, where tools/build_release.py exists."""
    try:
        sys.path.insert(0, os.path.join(QA_OS, 'tools'))
        import build_release
        return build_release.clean
    except Exception:
        return None
    finally:
        sys.path.pop(0)


def released_view(rel, data, cleaner):
    """What the release would ship for this working-copy file (text pages lose their internal lines)."""
    if cleaner is None or not rel.lower().endswith(TEXT):
        return data
    try:
        text = data.decode('utf-8', errors='surrogateescape')
        return cleaner(rel, text)[0].encode('utf-8', errors='surrogateescape')
    except Exception:
        return data


def load_patch(zp):
    z = zipfile.ZipFile(zp)
    try:
        man = json.loads(z.read(MANIFEST).decode('utf-8'))
    except KeyError:
        z.close()
        raise SystemExit(f'{zp}: not a QA OS patch (no {MANIFEST})')
    return z, man


def _parse(dt):
    try:
        return datetime.datetime.fromisoformat(dt) if dt else None
    except ValueError:
        return None


def plan(root, z, man, allowed=('knowledge', 'screens', 'feedback', 'runs', 'docs'), cleaner=None):
    """One entry per patch file: (status, rel, reason). Status: new / changed / same / kept / conflict / ignored."""
    base_dt = _parse(man.get('base', {}).get('built'))
    meta = {f['path']: f for f in man.get('files', [])}
    out = []
    for name in z.namelist():
        if name == MANIFEST or name.endswith('/'):
            continue
        rel = name.replace('\\', '/')
        if rel.startswith('/') or '..' in rel.split('/') or re.match(r'^[A-Za-z]:', rel):
            out.append(('ignored', rel, 'unsafe path'))
            continue
        if is_design(rel):
            out.append(('ignored', rel, 'design path'))
            continue
        if not wanted(rel) or area(rel) not in allowed:
            out.append(('ignored', rel, 'outside the patch areas' if area(rel) in allowed or area(rel) is None
                        else f'{area(rel)} is not re-applied here'))
            continue
        if excluded(rel, z.getinfo(name).file_size):
            out.append(('ignored', rel, excluded(rel, z.getinfo(name).file_size)))
            continue
        pdata = z.read(name)
        target = os.path.join(root, *rel.split('/'))
        if not os.path.exists(target):
            out.append(('new', rel, ''))
            continue
        raw = read(target)
        view = released_view(rel, raw, cleaner)
        if pdata == raw:
            out.append(('same', rel, ''))
            continue
        internal = view != raw
        if pdata == view:                       # equals what the release shipped from this dev page
            out.append(('same', rel, 'same apart from internal lines'))
            continue
        m = meta.get(rel, {})
        qa_changed = m.get('qa_state') not in ('release',)
        if not qa_changed:
            out.append(('kept', rel, 'not changed on the QA side since its release; working copy is newer'))
            continue
        b = m.get('base_sha256')
        if sha(view) in set(m.get('sent_sha256') or []):
            here_changed = False                   # still the version QA sent earlier (applied here / in this release)
        elif b is not None or (m.get('qa_state') == 'new' and man.get('base', {}).get('has_file_hashes')):
            here_changed = sha(view) != b          # new on QA + exists here -> b is None -> changed here too
        elif base_dt:
            here_changed = datetime.datetime.fromtimestamp(os.path.getmtime(target)) > base_dt
        else:
            here_changed = True                    # no base known: never overwrite blindly
        if internal:
            out.append(('conflict', rel, 'working page holds internal lines (<!--i-->); merge the QA edit by hand'))
        elif here_changed:
            out.append(('conflict', rel, 'changed on both sides since the base'))
        else:
            out.append(('changed', rel, ''))
    return out


ORDER = ('new', 'changed', 'conflict', 'kept', 'same', 'ignored')


def print_plan(rows, verbose_same=False):
    for st in ORDER:
        sel = [r for r in rows if r[0] == st]
        if not sel:
            continue
        print(f'\n{st.upper()} ({len(sel)})')
        if st == 'same' and not verbose_same:
            by = {}
            for _, rel, _ in sel:
                by[area(rel) or '-'] = by.get(area(rel) or '-', 0) + 1
            print('  ' + ', '.join(f'{k}: {v}' for k, v in sorted(by.items())))
            continue
        cur = None
        for _, rel, why in sorted(sel, key=lambda r: (area(r[1]) or '~', r[1])):
            a = area(rel) or 'other'
            if a != cur:
                print(f'  [{a}]')
                cur = a
            print(f'    {rel}' + (f'   - {why}' if why else ''))


def print_manifest(man, zp):
    b = man.get('base', {})
    print(f"Patch {os.path.basename(zp)}: from {man.get('user')} ({man.get('mode')} installation{', ' + man['machine'] if man.get('machine') else ''}) "
          f"on {man.get('date')}")
    print(f"  version {man.get('version')}; base release {b.get('release_version')} built {b.get('built')}"
          f"{'' if b.get('has_file_hashes') else ' (no file hashes: both-sides check by date)'}; {len(man.get('files', []))} file(s)")
    if man.get('note'):
        print(f"  note: {man['note']}")


def execute(root, z, rows, log_name=None):
    written = {'new': 0, 'changed': 0, 'conflict': 0}
    for st, rel, _ in rows:
        if st not in written:
            continue
        target = os.path.join(root, *rel.split('/'))
        if st == 'conflict':
            target += '.from_qa'
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, 'wb') as f:
            f.write(z.read(rel))
        written[st] += 1
    if log_name:
        d = os.path.join(root, 'feedback', 'patches')
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, log_name), 'w', encoding='utf-8') as f:
            json.dump({'applied': datetime.datetime.now().isoformat(timespec='seconds'), 'by': user(),
                       'rows': [{'status': s, 'path': p, 'reason': w} for s, p, w in rows]}, f, indent=1, ensure_ascii=False)
    return written


def summary_line(rows):
    c = {s: sum(1 for r in rows if r[0] == s) for s in ORDER}
    return ', '.join(f'{c[s]} {s}' for s in ORDER)


# ---------------------------------------------------------------- commands
def cmd_show(root, zp):
    z, man = load_patch(zp)
    with z:
        print_manifest(man, zp)
        rows = plan(root, z, man, cleaner=_cleaner() if mode(root) == 'dev' else None)
    print_plan(rows)
    print(f'\n{summary_line(rows)}')
    return rows


def cmd_apply(root, zp, yes, local=False):
    m = mode(root)
    if not local and m != 'dev':
        print('REFUSED: apply runs only in the dev copy (qaos.dev.yaml). In a QA installation use '
              '"python runtime/qaos_patch.py import-local <your own patch>" after installing a new release.')
        return 2
    z, man = load_patch(zp)
    with z:
        print_manifest(man, zp)
        if local and man.get('user') and man['user'].lower() != user().lower():
            print(f"  warning: this patch was exported by {man['user']}, not by you ({user()})")
        allowed = ('knowledge', 'screens', 'feedback', 'runs') if local else ('knowledge', 'screens', 'feedback', 'runs', 'docs')
        rows = plan(root, z, man, allowed, cleaner=_cleaner() if m == 'dev' else None)
        print_plan(rows)
        print(f'\n{summary_line(rows)}')
        if not yes:
            print('\nNothing written (dry run). Add --yes to apply.')
            return 0
        base = os.path.splitext(os.path.basename(zp))[0]
        w = execute(root, z, rows, log_name=f"{'imported' if local else 'applied'}_{base}.json")
    print(f"\nWritten: {w['new']} new, {w['changed']} changed, {w['conflict']} conflict(s) as <file>.from_qa"
          f" (log: feedback/patches/{'imported' if local else 'applied'}_{base}.json)")
    if w['conflict']:
        print('Merge each <file>.from_qa into its file by hand, then delete the .from_qa file.')
    return 0


def main(argv=None):
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description='QA OS patch (export / show / apply / import-local)')
    ap.add_argument('--root', default=QA_OS, help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest='cmd')
    e = sub.add_parser('export')
    e.add_argument('--note', default='')
    e.add_argument('--out', default=None)
    s = sub.add_parser('show')
    s.add_argument('patch')
    for name in ('apply', 'import-local'):
        a = sub.add_parser(name)
        a.add_argument('patch')
        a.add_argument('--yes', action='store_true')
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    if a.cmd == 'export':
        zp, man = export(root, a.note, a.out)
        print_export(zp, man)
        return 0
    if a.cmd == 'show':
        cmd_show(root, a.patch)
        return 0
    if a.cmd in ('apply', 'import-local'):
        return cmd_apply(root, a.patch, a.yes, local=a.cmd == 'import-local')
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
