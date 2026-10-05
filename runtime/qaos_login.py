#!/usr/bin/env python
"""QA OS login helper: signs a user in to the app in a browser that is ALREADY open, so the QA member does not type passwords.

Run it YOURSELF in your own terminal (Claude never runs this and never sees the password):

    python runtime/qaos_login.py --user Auto_Tssm

How it works
- Claude starts its Selenium Chrome with `--remote-debugging-port=9222`. This script attaches to that Chrome,
  logs out the current user if one is signed in, then types the user name and password and picks company + distributor
  from apps/<app>/app.yaml (login recipe, environment users).
- Passwords are read from (first found): --creds FILE, env QAOS_CREDENTIALS, qa-os/credentials.json, ~/.qa-os/credentials.json,
  then env SD_PASSWORD_<USER>. The file is gitignored. Nothing secret is printed or logged.
- Only runs against an environment marked `non_production: true` in app.yaml.
"""
import argparse, json, os, re, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qaos_config  # noqa: E402


def find_password(app_id, user, creds_arg):
    candidates = [creds_arg, os.environ.get('QAOS_CREDENTIALS'),
                  os.path.join(HERE, '..', 'credentials.json'),
                  os.path.join(os.path.expanduser('~'), '.qa-os', 'credentials.json')]
    for f in candidates:
        if f and os.path.exists(f):
            try:
                entry = ((json.load(open(f, encoding='utf-8')).get(app_id) or {}).get('users') or {}).get(user) or {}
            except Exception as e:                       # never echo file content
                print(f'cannot read credentials file {f}: {type(e).__name__}')
                continue
            if entry.get('password'):
                return entry['password']
    return os.environ.get('SD_PASSWORD_' + re.sub(r'\W', '_', user.upper()))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--app', default='snd')
    ap.add_argument('--env', help='environment name in app.yaml (default: the app default_env)')
    ap.add_argument('--user', required=True, help='user name as listed in app.yaml (e.g. Auto_Multi_Orga, Auto_Tssm)')
    ap.add_argument('--port', type=int, default=9222, help='remote debugging port of the open Chrome')
    ap.add_argument('--creds', help='credentials JSON file (default: see the docstring)')
    ap.add_argument('--no-logout', action='store_true', help='do not log out a signed-in user first')
    a = ap.parse_args()

    cfg = qaos_config.app_cfg(a.app)
    env_name = a.env or cfg['default_env']
    env = cfg['environments'][env_name]
    if not env.get('non_production'):
        sys.exit(f'refusing: {env_name} is not marked non_production in app.yaml')
    users = env.get('users') or {}
    if a.user not in users:
        sys.exit(f'unknown user {a.user}; app.yaml lists: {", ".join(users)}')
    pwd = find_password(a.app, a.user, a.creds)
    if not pwd:
        sys.exit(f'no password found for {a.user} (credentials.json / SD_PASSWORD_{re.sub(chr(92) + "W", "_", a.user.upper())})')

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    opts = webdriver.ChromeOptions()
    opts.debugger_address = f'127.0.0.1:{a.port}'
    try:
        d = webdriver.Chrome(options=opts)
    except Exception as e:
        sys.exit(f'cannot attach to Chrome on port {a.port} ({type(e).__name__}). Ask Claude to restart its browser with the debugging port.')
    d.switch_to.window(d.window_handles[0])
    W = lambda t=40: WebDriverWait(d, t)
    lg = cfg['login']

    def click_css(css, t=40):
        W(t).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css))).click()

    def click_xp(xp, t=40):
        W(t).until(EC.element_to_be_clickable((By.XPATH, xp))).click()

    # 1. log out a signed-in user (the app shows the user name top right; Logout is in that menu)
    if not a.no_logout and 'sso-dev' not in d.current_url:
        try:
            who = d.execute_script("const e=[...document.querySelectorAll('*')].find(e=>e.offsetParent!==null&&e.children.length<=2&&e.getBoundingClientRect().top<60&&e.getBoundingClientRect().left>1100&&/^[A-Za-z_]+$/.test(e.textContent.trim())); if(e){e.click(); return e.textContent.trim();}")
            time.sleep(0.8)
            d.execute_script("document.querySelector('li#logout').click()")
            print(f'logged out {who}')
            W(30).until(lambda x: 'sso-dev' in x.current_url or x.find_elements(By.CSS_SELECTOR, lg['username']['css']))
        except Exception:
            d.get(env['url'])
    if not d.find_elements(By.CSS_SELECTOR, lg['username']['css']):
        d.get(env['url'])

    # 2. credentials
    W(40).until(EC.presence_of_element_located((By.CSS_SELECTOR, lg['username']['css']))).clear()
    d.find_element(By.CSS_SELECTOR, lg['username']['css']).send_keys(a.user)
    d.find_element(By.CSS_SELECTOR, lg['password']['css']).send_keys(pwd)      # never printed
    click_css(lg['submit']['css'])

    # 3. company, then distributor
    company = env.get('company')
    if company:
        click_css(lg['company']['button']['css'], 60)
        click_xp(lg['company']['option']['xpath'].replace('{company}', company))
        click_css(lg['company']['proceed']['css'])
    dist = (users[a.user] or {}).get('distributor')
    if dist:
        dl = lg['distributor']
        click_xp(dl['button']['xpath'], 60)
        click_xp(dl['option']['xpath'].replace('{code}', dist))
        click_xp(dl['proceed']['xpath'])
    W(90).until(lambda x: lg['landed_url_contains'] in x.current_url)
    print(f'logged in as {a.user}' + (f', company {company}' if company else '') + (f', distributor {dist}' if dist else ''))
    # leave the browser open for Claude; only drop this driver connection
    try:
        d.service.stop()
    except Exception:
        pass


if __name__ == '__main__':
    main()
