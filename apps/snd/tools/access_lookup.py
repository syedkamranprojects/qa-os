"""Query the SND access knowledge layer (apps/snd/knowledge/access/). Run by Claude, not by QA users.

  screen <text|id>            screens matching id/title: route, menu path, roles per org, user counts
  user <code> [--can <text>]  a user's org, roles, locations, screen count; --can checks named screens
  who <text> [<text> ...]     users (per org) whose roles reach EVERY named screen  -> "which user should I log in as"
  features <org> [text]       feature flags of an organization (010104 Pakistan, 010105 Bangladesh)
  diff-features <orgA> <orgB> market differences in feature flags
  validate-live <user> [<menu.json>]  DB access vs the live role-filtered menu of that user (how current is the DB?)
  plan-user <text> ... [--org <orgcode>]  rank the accounts we can log in as (env/user) for a story's screens -> Q-ENV-1/Q-ENV-2 answered from data
"""
import json, os, sys

K = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'access')
J = lambda n: json.load(open(os.path.join(K, n), encoding='utf-8'))
screens, menu, ro, users, feats, rnames = J('screens.json'), J('menu_groups.json'), J('role_options.json'), J('users.json'), J('features.json'), J('role_names.json')
ORGS = {'010104': 'Unilever Pakistan', '010105': 'Unilever Bangladesh', '99': 'GLOBAL'}
by_id = {s['id']: s for s in screens}
node = {m['id']: m for m in menu}
nodes_of = {}
for m in menu:
    if m['option_id']:
        nodes_of.setdefault(m['option_id'], []).append(m)


def path_of(opt):
    out = []
    for n in nodes_of.get(opt, [])[:2]:
        p, cur, guard = [], n, 0
        while cur and guard < 8:
            p.append(cur['title'])
            cur = node.get(cur['parent']); guard += 1
        out.append(' > '.join(reversed(p)))
    return out


def find(q):
    ql = q.lower()
    ex = [s for s in screens if s['id'].lower() == ql]
    return ex or [s for s in screens if ql in s['id'].lower() or ql in (s['title'] or '').lower()]


def opts_of_user(u):
    o = set()
    for r in u['roles']:
        o |= set(ro.get(f"{u['org']}/{r}", []))
    return o


def cmd_screen(q):
    for s in find(q)[:15]:
        print(f"{s['id']}  |  {s['title']}  |  route {s['route'] or '-'} {('?' + s['param']) if s['param'] else ''}  |  app {s['app']}  layout={s['is_layout']} admin={s['is_admin']}")
        for p in path_of(s['id']):
            print('    menu:', p)
        for org in ORGS:
            rs = sorted(k.split('/')[1] for k, v in ro.items() if k.startswith(org + '/') and s['id'] in v)
            if rs:
                n = sum(1 for u in users if u['org'] == org and set(u['roles']) & set(rs))
                print(f"    {org} {ORGS[org]}: roles {','.join(rs)}  ({n} users)")


def cmd_user(code, can=None):
    hits = [u for u in users if u['user'].lower() == code.lower()]
    if not hits:
        print('user not found (only Unilever orgs 010104/010105 are extracted)'); return
    for u in hits:
        o = opts_of_user(u)
        print(f"{u['user']}  org {u['org']} {ORGS.get(u['org'], '')}  status={u['status']} admin={u['admin']} system={u['system']} end={u['end'] or '-'}")
        print(f"  roles: {', '.join(u['roles']) or '-'}   locations: {', '.join(u['locations'][:8]) or '-'}{' ...' if len(u['locations']) > 8 else ''}   screens reachable: {len(o)}")
        for q in (can or []):
            for s in find(q)[:6]:
                print(f"  can open {s['id']} ({s['title']}): {'YES' if s['id'] in o else 'NO'}")


def cmd_who(qs):
    need = []
    for q in qs:
        m = find(q)
        if not m:
            print(f'no screen matches "{q}"'); return
        need.append((q, {s['id'] for s in m}))
    for q, ids in need:
        print(f'"{q}" -> {len(ids)} screen(s): {", ".join(sorted(ids)[:6])}')
    for org in ORGS:
        ok = [u for u in users if u['org'] == org and (u['status'] in (None, 'A', 'Y', 'ACTIVE') or True) and all(opts_of_user(u) & ids for _, ids in need)]
        if ok:
            act = [u for u in ok if not u['end'] or u['end'] >= '2026-09-29']
            print(f"{org} {ORGS[org]}: {len(ok)} users can reach all ({len(act)} not expired). e.g. " + ', '.join(u['user'] for u in act[:12]))


def cmd_features(org, text=None):
    for r in feats.get(org, []):
        if not text or text.lower() in ' '.join(r).lower():
            print(f"{r[0]:<18} {r[1]:<40} = {r[2]!s:<22} {r[3]}")


def cmd_diff(a, b):
    A = {(r[0], r[1]): r for r in feats[a]}; B = {(r[0], r[1]): r for r in feats[b]}
    for k in sorted(set(A) | set(B)):
        va, vb = A.get(k), B.get(k)
        if va is None or vb is None:
            print(f"only in {b if va is None else a}: {k[0]}/{k[1]} = {(vb or va)[2]!r}  ({(vb or va)[3]})")
        elif va[2] != vb[2]:
            print(f"differs: {k[0]}/{k[1]}: {a}={va[2]!r}  {b}={vb[2]!r}  ({va[3]})")


def cmd_validate(code, live=None):
    hits = [u for u in users if u['user'].lower() == code.lower()]
    if not hits:
        print('user not found'); return
    db = opts_of_user(hits[0])
    live = live or os.path.join(K, '..', 'env', 'cnr1dev1', f'menu.{code.upper()}.json')
    lv = {e['app_option'] for e in json.load(open(live, encoding='utf-8'))['entries'] if e.get('app_option')}
    only_live, only_db = sorted(lv - db), sorted(db - lv)
    print(f"{code}: DB screens {len(db)} | live menu screens {len(lv)} | both {len(lv & db)}")
    print(f"live-only (DB is older / screen not in DB): {len(only_live)}  e.g. {only_live[:12]}")
    print(f"DB-only (in role but not in live menu): {len(only_db)}  e.g. {only_db[:8]}")


def cmd_plan(qs, prefer_org=None):
    """Rank the accounts we can log in as (those with a harvested live menu) for a story's screens.
    Live menu is the truth; the DB is only consulted when a user has no live-menu match for a screen."""
    envdir = os.path.join(K, '..', 'env')
    cands = []
    for env in sorted(os.listdir(envdir)):
        d = os.path.join(envdir, env)
        for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
            if f.startswith('menu.') and f.endswith('.json'):
                cands.append((env, f[5:-5]))
    notes = json.load(open(os.path.join(K, 'account_notes.json'), encoding='utf-8'))
    rows = []
    for env, usr in cands:
        entries = json.load(open(os.path.join(envdir, env, f'menu.{usr}.json'), encoding='utf-8'))['entries']
        dbu = next((u for u in users if u['user'].lower() == usr.lower()), None)
        dbo = opts_of_user(dbu) if dbu else set()
        got, miss = [], []
        for q in qs:
            ql = q.lower()
            live = [e for e in entries if e.get('app_option') and (ql in (e['title'] or '').lower() or ql == e['app_option'].lower())]
            if live:
                got.append((q, 'live menu', live[0]['app_option'], ' > '.join(live[0]['path'])))
                continue
            dbm = [s for s in find(q) if s['id'] in dbo]
            if dbm:
                got.append((q, 'DB only (not in live menu: verify)', dbm[0]['id'], ''))
            else:
                miss.append(q)
        nt = notes.get(f'{env}/{usr}', {})
        rows.append((len(got), env, usr, dbu['org'] if dbu else nt.get('org', 'not in DB'), got, miss, nt))
    rows.sort(key=lambda r: (-r[0], r[3] != prefer_org, r[6].get('rank', 99), r[1], r[2]))
    for n, env, usr, org, got, miss, nt in rows:
        print(f"{env} / {usr}  (org {org}): {n}/{len(qs)} screens reachable" + (f"  MISSING: {', '.join(miss)}" if miss else '  <- all'))
        if nt.get('notes'):
            print(f"    note: {nt['notes']}")
        for q, how, oid, p in got:
            print(f"    {q!r}: {oid} [{how}] {p}")
    best = [r for r in rows if not r[5]]
    if prefer_org and best and best[0][3] != prefer_org:
        print(f'note: no fully-covering account is in org {prefer_org}; market may differ from the story')
    print('\nRECOMMENDED: ' + (f"{best[0][1]} / {best[0][2]}" + (f" (also fully covers: {', '.join(f'{r[1]}/{r[2]}' for r in best[1:])})" if len(best) > 1 else '') if best else 'none covers every screen: split the story by environment or ask (Q-ENV-1)'))


a = sys.argv[1:]
if not a:
    print(__doc__)
elif a[0] == 'screen':
    cmd_screen(' '.join(a[1:]))
elif a[0] == 'user':
    can = a[a.index('--can') + 1:] if '--can' in a else None
    cmd_user(a[1], [' '.join(can)] if can else None)
elif a[0] == 'who':
    cmd_who(a[1:])
elif a[0] == 'features':
    cmd_features(a[1], a[2] if len(a) > 2 else None)
elif a[0] == 'diff-features':
    cmd_diff(a[1], a[2])
elif a[0] == 'validate-live':
    cmd_validate(a[1], a[2] if len(a) > 2 else None)
elif a[0] == 'plan-user':
    org = a[a.index('--org') + 1] if '--org' in a else None
    cmd_plan([x for i, x in enumerate(a[1:], 1) if x != '--org' and (i < 2 or a[i - 1] != '--org')], org)
else:
    print(__doc__)
