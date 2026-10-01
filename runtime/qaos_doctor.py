"""QA OS setup check for a QA member's machine.

  python runtime/qaos_doctor.py            # check only
  python runtime/qaos_doctor.py --fix      # also pip-install missing packages from requirements.txt

Checks: Python version, required packages, Chrome, credentials for each app pack (presence only; values never printed).
"""
import importlib.util, json, os, shutil, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')
QA_OS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ok = True


def report(good, msg, hint=''):
    global ok
    ok &= good
    print(f"  {'OK ' if good else 'NO '} {msg}" + (f'   → {hint}' if hint and not good else ''))


print('QA OS doctor')
report(sys.version_info >= (3, 10), f'Python {sys.version.split()[0]} (need 3.10+)', 'install Python 3.10 or newer from python.org')

pkgs = {'selenium': 'selenium', 'yaml': 'pyyaml', 'jsonschema': 'jsonschema', 'openpyxl': 'openpyxl'}
missing = [pip for mod, pip in pkgs.items() if importlib.util.find_spec(mod) is None]
if missing and '--fix' in sys.argv:
    subprocess.call([sys.executable, '-m', 'pip', 'install', '-r', os.path.join(QA_OS, 'requirements.txt')])
    missing = [pip for mod, pip in pkgs.items() if importlib.util.find_spec(mod) is None]
report(not missing, 'Python packages: ' + ('all present' if not missing else 'missing ' + ', '.join(missing)),
       f'python -m pip install -r "{os.path.join(QA_OS, "requirements.txt")}"  (or rerun with --fix)')

chrome = shutil.which('chrome') or shutil.which('google-chrome') or next(
    (p for p in [os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe'),
                 os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe'),
                 os.path.expandvars(r'%LocalAppData%\Google\Chrome\Application\chrome.exe')] if os.path.exists(p)), None)
report(bool(chrome), 'Google Chrome ' + ('found' if chrome else 'not found'), 'install Chrome; Selenium downloads the matching driver on first run')

try:
    sys.path.insert(0, os.path.join(QA_OS, 'runtime'))
    import yaml
    from qaos_player import credentials, AppPack  # noqa: E402
    for app_id in sorted(os.listdir(os.path.join(QA_OS, 'apps'))):
        if os.path.exists(os.path.join(QA_OS, 'apps', app_id, 'app.yaml')):
            app = AppPack(app_id)
            u, p = credentials(app)
            c = app.cfg['credentials']
            report(bool(u and p), f"credentials for app '{app_id}' ({c['user_env']} / {c['password_env']}) " + ('set' if u and p else 'not set'),
                   'add them to your own .claude/settings.local.json "env" block, or set them as environment variables')
except Exception as e:  # packages missing: already reported above
    report(False, f'credential check skipped ({type(e).__name__})')

print('READY' if ok else 'NOT READY — fix the items marked NO')
sys.exit(0 if ok else 1)
