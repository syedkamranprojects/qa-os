"""Build the SND access knowledge layer (roles, screens, users, menu tree, feature flags) from snd-schema extracts.

The extracts are produced by Claude through the read-only snd-schema connector (queries listed in
apps/snd/knowledge/access/README.md) and saved as JSON files; this script only reshapes them.
No passwords, e-mails, phone numbers or names are read or stored: users are reduced to code, status, flags, roles, locations.

    python apps/snd/tools/build_access.py <dir with the 4 extract files: screens.json users.json role_options.json menu_groups.json>
Roles and features are small and are kept in access/roles_names.json and access/features.json (written by hand from query results).
"""
import json, os, sys

src = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), '..', 'knowledge', 'access')
os.makedirs(OUT, exist_ok=True)


def load(name):
    d = json.load(open(os.path.join(src, name), encoding='utf-8'))
    r = d['result'] if isinstance(d, dict) else d
    return r[0]['json_agg']


def dump(name, obj):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
    print(f'{name}: {os.path.getsize(os.path.join(OUT, name)) // 1024} KB')


screens = load('screens.json')
dump('screens.json', screens)

menu = load('menu_groups.json')
dump('menu_groups.json', menu)

ro = load('role_options.json')
dump('role_options.json', {f"{r['org']}/{r['role_id']}": r['option_ids'].split(',') for r in ro})

users = load('users.json')
import hashlib
mask = lambda c: 'user-' + hashlib.sha1(c.lower().encode()).hexdigest()[:8] if '@' in c else c   # e-mail-like user codes are masked
dump('users.json', [{'org': u['org'], 'user': mask(u['usr']), 'status': u['status'], 'admin': u['is_admin'], 'system': u['system_user'],
                     'end': (u['end_date'] or '')[:10], 'roles': (u['roles'] or '').split(',') if u['roles'] else [],
                     'locations': (u['locations'] or '').split(',') if u['locations'] else []} for u in users])
print(len(screens), 'screens,', len(menu), 'menu nodes,', len(ro), 'role option lists,', len(users), 'users')
