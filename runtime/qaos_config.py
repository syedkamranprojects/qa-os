"""QA OS configuration loader: the one place that reads qaos.yaml and apps/<app>/app.yaml.

  python runtime/qaos_config.py show                       # global settings
  python runtime/qaos_config.py app snd                    # summary of an app pack
  python runtime/qaos_config.py role snd cnr1dev1 Checker  # role -> user (+ distributor), never a password
  python runtime/qaos_config.py market snd PK              # market -> framework group / app id / env
  python runtime/qaos_config.py validate                   # check qaos.yaml and every app pack; exit 1 on errors
  python runtime/qaos_config.py mode                       # which installation this is: dev (QA OS team) or qa (QA team release)

Import: from qaos_config import global_cfg, app_cfg, role_user, market
Values never include passwords; those are read only by qaos_player.credentials().
"""
import os
import sys

import yaml

QA_OS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def global_cfg():
    with open(os.path.join(QA_OS, 'qaos.yaml'), encoding='utf-8') as f:
        return yaml.safe_load(f)


def app_ids():
    return sorted(d for d in os.listdir(os.path.join(QA_OS, 'apps')) if os.path.exists(os.path.join(QA_OS, 'apps', d, 'app.yaml')))


def app_cfg(app_id):
    with open(os.path.join(QA_OS, 'apps', app_id, 'app.yaml'), encoding='utf-8') as f:
        return yaml.safe_load(f)


def role_users(cfg, env, role):
    """All users of a role in an environment (first = default). A role maps to one user or a list. Case-insensitive."""
    roles = (cfg.get('environments', {}).get(env) or {}).get('roles') or {}
    for name, users in roles.items():
        if name.lower() == role.lower():
            return [users] if isinstance(users, str) else list(users or [])
    return []


def role_user(cfg, env, role):
    """(user, distributor or None) for a role name in an environment: the role's default (first) user."""
    users = role_users(cfg, env, role)
    if not users:
        return None, None
    dist = ((cfg['environments'][env].get('users') or {}).get(users[0]) or {}).get('distributor')
    return users[0], dist


def role_of_user(cfg, env, user):
    roles = (cfg.get('environments', {}).get(env) or {}).get('roles') or {}
    return [r for r in roles if (user or '').lower() in [u.lower() for u in role_users(cfg, env, r)]]


def market(cfg, key):
    """The market entry (framework group, app id, env, org, ...) for a market key such as PK, BD, PH."""
    return (cfg.get('markets') or {}).get(key.upper())


def env_url(cfg, env):
    """URL of an environment; GIAS-style packs give `url_env` (an environment variable) instead of a literal URL."""
    e = cfg['environments'][env]
    return e.get('url') or os.environ.get(e.get('url_env', ''), '')


DEV_MARKER = 'qaos.dev.yaml'      # exists ONLY in the dev working copy: gitignored, never packaged (tools/build_release.py)
RELEASE_INFO = 'release.json'     # written into the QA-team release zip by tools/build_release.py


def plugin_version():
    import json
    try:
        with open(os.path.join(QA_OS, 'plugins', 'qa-os', '.claude-plugin', 'plugin.json'), encoding='utf-8') as f:
            return json.load(f).get('version')
    except OSError:
        return None


def installation():
    """Which QA OS installation this is (QA lead, 2026-10-12):
    dev = the QA OS team's working copy (qaos.dev.yaml present); qa = the QA team's release (no marker; release.json
    tells the version). No marker always means qa, so a missing or deleted file never turns a QA install into dev."""
    import json
    inst = global_cfg().get('installation') or {}
    contact = inst.get('design_contact') or ''
    dev = os.path.join(QA_OS, DEV_MARKER)
    if os.path.exists(dev):
        with open(dev, encoding='utf-8') as f:
            d = yaml.safe_load(f) or {}
        return {'mode': 'dev', 'version': plugin_version(), 'owner': d.get('owner'), 'design_contact': d.get('design_contact') or contact,
                'qaos_owner': inst.get('owner'), 'trainers': inst.get('trainers') or [], 'source': DEV_MARKER}
    rel = os.path.join(QA_OS, RELEASE_INFO)
    if os.path.exists(rel):
        with open(rel, encoding='utf-8') as f:
            r = json.load(f)
        return {'mode': 'qa', 'version': r.get('version'), 'built': r.get('built'), 'built_by': r.get('built_by'),
                'design_contact': r.get('design_contact') or contact, 'qaos_owner': r.get('qaos_owner') or inst.get('owner'),
                'trainers': r.get('trainers') or inst.get('trainers') or [], 'source': RELEASE_INFO}
    return {'mode': 'qa', 'version': plugin_version(), 'design_contact': contact, 'qaos_owner': inst.get('owner'),
            'trainers': inst.get('trainers') or [], 'source': f'no {DEV_MARKER} and no {RELEASE_INFO}: treated as a QA install'}


def trainer_allowed(name):
    """Only the named trainers may train QA OS (QA lead, 2026-10-16). Case- and space-insensitive name match."""
    norm = lambda s: ' '.join(str(s or '').lower().split())
    allowed = installation().get('trainers') or []
    return (not allowed) or norm(name) in {norm(x) for x in allowed}


def validate():
    errs, warns = [], []
    g = global_cfg()
    ids = app_ids()
    for a in g['apps']['active'] + g['apps']['available']:
        if a not in ids:
            errs.append(f"qaos.yaml lists app '{a}' but apps/{a}/app.yaml does not exist")
    for a in ids:
        c = app_cfg(a)
        if c.get('id') != a:
            errs.append(f"apps/{a}/app.yaml: id '{c.get('id')}' must equal the folder name")
        envs = c.get('environments') or {}
        if not envs:
            errs.append(f'{a}: no environments')
        if c.get('default_env') not in envs:
            errs.append(f"{a}: default_env '{c.get('default_env')}' is not in environments")
        for en, e in envs.items():
            if not (e.get('url') or e.get('url_env')):
                errs.append(f'{a}/{en}: needs url or url_env')
            if 'non_production' not in e:
                warns.append(f'{a}/{en}: non_production not stated (defaults to false: no data-changing steps)')
            users = e.get('users') or {}
            for role in (e.get('roles') or {}):
                ru = role_users(c, en, role)
                if not ru:
                    errs.append(f"{a}/{en}: role '{role}' has no users")
                for user in ru:
                    if user not in users:
                        errs.append(f"{a}/{en}: role '{role}' maps to user '{user}' which is not listed under users")
            host = (e.get('url') or '').split('/')[2] if e.get('url') else None
            if host and host not in (c.get('allowed_hosts') or []):
                warns.append(f'{a}/{en}: host {host} is not in allowed_hosts')
        for mk, m in (c.get('markets') or {}).items():
            if m.get('env') and m['env'] not in envs:
                warns.append(f"{a}: market {mk} points at environment '{m['env']}' which is not in this pack")
        cr = c.get('credentials') or {}
        if not (cr.get('user_env') and cr.get('password_env')):
            errs.append(f'{a}: credentials.user_env / password_env missing')
    for e in errs:
        print('ERR ', e)
    for w in warns:
        print('warn', w)
    print('OK' if not errs else f'{len(errs)} error(s)')
    return not errs


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    a = sys.argv[1:]
    if not a or a[0] == 'show':
        print(yaml.safe_dump(global_cfg(), sort_keys=False, allow_unicode=True))
    elif a[0] == 'app':
        c = app_cfg(a[1])
        print(f"{c['id']}: {c['name']} | default_env {c['default_env']}")
        for en, e in c['environments'].items():
            print(f"  {en}: {e.get('url') or '$' + e.get('url_env', '?')} | non_production={e.get('non_production')} | users {list((e.get('users') or {}))} | roles {e.get('roles') or {}}")
        print('  markets:', {k: {x: v for x, v in m.items() if x in ('group', 'framework_app_id', 'env')} for k, m in (c.get('markets') or {}).items()})
    elif a[0] == 'role':
        c = app_cfg(a[1])
        print(role_user(c, a[2], a[3]), 'all users:', role_users(c, a[2], a[3]))
    elif a[0] == 'market':
        print(yaml.safe_dump(market(app_cfg(a[1]), a[2]), sort_keys=False, allow_unicode=True))
    elif a[0] == 'mode':
        i = installation()
        print(f"QA OS installation: {i['mode'].upper()}  (version {i.get('version')}; from {i['source']})")
        print(f"  QA OS owner: {i.get('qaos_owner')}; trainers: {', '.join(i.get('trainers') or []) or '(anyone)'}")
        if i['mode'] == 'qa':
            print(f"  design / tool gaps are noted in feedback/design_gaps.md, not fixed; important changes go as a patch "
                  f"(python runtime/qaos_patch.py export --note \"...\") to {i.get('design_contact')}")
    elif a[0] == 'trainer':                       # python runtime/qaos_config.py trainer "<name>"  -> exit 0 allowed / 1 refused
        ok = trainer_allowed(' '.join(a[1:]))
        print('allowed' if ok else f"NOT a QA OS trainer. Only these people may train QA OS: {', '.join(installation().get('trainers') or [])}")
        sys.exit(0 if ok else 1)
    elif a[0] == 'validate':
        sys.exit(0 if validate() else 1)
    else:
        print(__doc__)
