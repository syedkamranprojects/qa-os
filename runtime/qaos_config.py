"""QA OS configuration loader: the one place that reads qaos.yaml and apps/<app>/app.yaml.

  python runtime/qaos_config.py show                       # global settings
  python runtime/qaos_config.py app snd                    # summary of an app pack
  python runtime/qaos_config.py role snd cnr1dev1 Checker  # role -> user (+ distributor), never a password
  python runtime/qaos_config.py market snd PK              # market -> framework group / app id / env
  python runtime/qaos_config.py validate                   # check qaos.yaml and every app pack; exit 1 on errors

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
    elif a[0] == 'validate':
        sys.exit(0 if validate() else 1)
    else:
        print(__doc__)
