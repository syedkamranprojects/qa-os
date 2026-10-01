"""QA OS promotion: move reusable decisions from a run into the app pack so the same question is never asked twice.

  python runtime/qaos_promote.py <run_dir>            # dry run: shows what would be added / skipped / in conflict
  python runtime/qaos_promote.py <run_dir> --apply    # writes apps/<app>/knowledge/decisions.json (+ decisions.md)
  python runtime/qaos_promote.py <run_dir> --apply --force   # also overwrite entries that conflict (rare; review first)

What is promotable (from <run_dir>/decisions.json):
  - terms written by the story author in the intake block (status "stated")
  - answers recorded with --reusable: kind term | variance | rule  (variances only from answers, never from the intake block) (status "ruled" when owner is BA, else "stated")
Entries already in the pack are skipped; an entry with the same key but a different value is reported as a conflict and left alone.
Every promoted entry carries provenance (story key, date, who). The app pack is shared by the team: review the dry run before --apply.
"""
import argparse, datetime as dt, json, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
QA_OS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def load(p, default=None):
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default


def norm(s):
    return re.sub(r'\s+', ' ', s.strip().lower())


ap = argparse.ArgumentParser()
ap.add_argument('run_dir'); ap.add_argument('--apply', action='store_true'); ap.add_argument('--force', action='store_true'); ap.add_argument('--pack', help='decisions.json to use instead of the app pack (testing)')
a = ap.parse_args()
run = os.path.abspath(a.run_dir)
d = load(os.path.join(run, 'decisions.json'))
if not d:
    sys.exit('no decisions.json in the run: run qaos_intake.py parse first')
app, key = d['app'], d['key']
packp = os.path.abspath(a.pack) if a.pack else os.path.join(QA_OS, 'apps', app, 'knowledge', 'decisions.json')
pack = load(packp, {'app': app, 'defaults': {}, 'terms': [], 'variances': [], 'rules': []})
for k in ('terms', 'variances', 'rules'):
    pack.setdefault(k, [])
today = dt.date.today().isoformat()
prov = lambda by: {'story': key, 'date': today, 'by': by}

cands = {'terms': [], 'variances': [], 'rules': []}     # (key, entry)
for t in d.get('terms', []):
    if t['source'] == 'intake' and norm(t['story']) != norm(t['app']):
        cands['terms'].append((norm(t['story']), {'story': t['story'], 'app': t['app'], 'status': 'stated', 'source': prov('story author')}))
# expected-variance lines from the intake block are NOT promoted: they describe this release/story and would hide real differences in
# later stories once the feature ships. A variance enters the pack only as a reusable BA ruling (answer --kind variance --owner BA --reusable).
for x in d.get('answers', []):
    if not x.get('reusable'):
        continue
    st = 'ruled' if (x.get('owner') or '').upper() == 'BA' else 'stated'
    by = x.get('owner') or 'QA'
    if x['kind'] == 'term':
        cands['terms'].append((norm(x['key']), {'story': x['key'], 'app': x['value'], 'status': st, 'source': prov(by)}))
    elif x['kind'] == 'variance':
        cands['variances'].append((norm(x['key']), {'key': x['key'], 'ruling': x.get('ruling'), 'note': x['value'], 'status': st, 'source': prov(by)}))
    elif x['kind'] == 'rule':
        cands['rules'].append((norm(x['key']), {'key': x['key'], 'text': x['value'], 'status': st, 'source': prov(by)}))

rank = {'observed': 0, 'stated': 1, 'ruled': 2}
for kind in cands:
    best = {}
    for k, e in cands[kind]:
        if k not in best or rank.get(e['status'], 0) >= rank.get(best[k]['status'], 0):
            best[k] = e
    cands[kind] = list(best.items())

same = {'terms': lambda e, n: norm(e['app']) == norm(n['app']),
        'variances': lambda e, n: (e.get('ruling'), norm(e.get('note') or '')) == (n.get('ruling'), norm(n.get('note') or '')) or n.get('ruling') is None and e.get('ruling') is not None,
        'rules': lambda e, n: norm(e['text']) == norm(n['text'])}
keyof = {'terms': lambda e: norm(e['story']), 'variances': lambda e: norm(e['key']), 'rules': lambda e: norm(e['key'])}
add, dup, conf = [], [], []
for kind, items in cands.items():
    idx = {keyof[kind](e): e for e in pack[kind]}
    for k, new in items:
        old = idx.get(k)
        if old is None:
            add.append((kind, new)); idx[k] = new
        elif same[kind](old, new) and rank.get(new['status'], 0) <= rank.get(old.get('status'), 0):
            dup.append((kind, k))
        elif rank.get(new['status'], 0) > rank.get(old.get('status'), 0) or a.force:
            conf.append((kind, k, old, new, 'upgrade' if rank.get(new['status'], 0) > rank.get(old.get('status'), 0) else 'forced'))
        else:
            conf.append((kind, k, old, new, 'conflict'))

print(f"promotion from {key} into {os.path.relpath(packp, QA_OS)}")
for kind, e in add:
    print(f"  + {kind[:-1]:<8} {e.get('story') or e.get('key')}  ->  {e.get('app') or e.get('text') or e.get('ruling') or e.get('note')}  [{e['status']}]")
for kind, k in dup:
    print(f"  = {kind[:-1]:<8} {k} (already in the pack)")
for kind, k, old, new, why in conf:
    tag = {'upgrade': '^ upgrade (stronger source)', 'forced': '! overwrite (--force)', 'conflict': '? CONFLICT (kept existing; review)'}[why]
    print(f"  {tag} {kind[:-1]} {k}\n      existing: {json.dumps({x: old[x] for x in old if x != 'source'}, ensure_ascii=False)}\n      new     : {json.dumps({x: new[x] for x in new if x != 'source'}, ensure_ascii=False)}")

if not a.apply:
    print(f"\ndry run: {len(add)} to add, {len(dup)} already present, {len(conf)} to review. Use --apply to write.")
    sys.exit(0)

for kind, e in add:
    pack[kind].append(e)
for kind, k, old, new, why in conf:
    if why in ('upgrade', 'forced'):
        pack[kind] = [new if keyof[kind](e) == k else e for e in pack[kind]]
pack['updated'] = today
with open(packp, 'w', encoding='utf-8') as f:
    json.dump(pack, f, indent=1, ensure_ascii=False); f.write('\n')

md = [f'# {app} decisions (generated from decisions.json; edit through qaos_intake/qaos_promote, not by hand)', '', f'Updated {today}. Status: observed (seen in the app) < stated (story author / QA) < ruled (BA).', '',
      '## Terms (story term = app term)', '| Story term | App term | Status | Source |', '|---|---|---|---|']
md += [f"| {t['story']} | {t['app']} | {t['status']} | {t['source']['story']} {t['source']['date']} ({t['source']['by']}) |" for t in pack['terms']]
md += ['', '## Variances (story vs app)', '| Variance | Ruling | Note | Status | Source |', '|---|---|---|---|---|']
md += [f"| {v['key']} | {v.get('ruling') or '-'} | {v.get('note') or ''} | {v['status']} | {v['source']['story']} {v['source']['date']} ({v['source']['by']}) |" for v in pack['variances']]
md += ['', '## Rules', '| Rule | Text | Status | Source |', '|---|---|---|---|']
md += [f"| {r['key']} | {r['text']} | {r['status']} | {r['source']['story']} {r['source']['date']} ({r['source']['by']}) |" for r in pack['rules']]
open(os.path.join(os.path.dirname(packp), 'decisions.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
print(f"\napplied: {len(add)} added, {sum(1 for c in conf if c[4] != 'conflict')} updated, {sum(1 for c in conf if c[4] == 'conflict')} left for review. decisions.md regenerated.")
