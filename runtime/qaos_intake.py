"""QA OS intake: read the story's QA-OS block, apply app-pack defaults, choose the account, write decisions.json.

  python runtime/qaos_intake.py parse <run_dir> [--story <file>] [--screens "Screen A;Screen B"]
  python runtime/qaos_intake.py answer <run_dir> --id <Q-id> --kind term|variance|rule|other --key <short key> --value <text>
                                [--ruling app-is-right|not-built|ask-ba] [--owner BA|QA] [--reusable]
  python runtime/qaos_intake.py show <run_dir>

The block (docs/QUESTION_BANK.md):
    --- QA-OS ---
    env: cnr1dev1 | user: KPO_mp | scope: browser | market: PKBD | screens: A; B | terms: X = Y | data: ... |
    allow: create, save | never: forward, approve | expected-variance: ... ; ...
    --- /QA-OS ---
Every field is optional. Missing fields come from the app pack (apps/<app>/knowledge/decisions.json) or a default and are marked assumed.
Authorization is bounded: `allow` counts only on environments with `non_production: true`; one-way actions (delete, submit, forward,
approve ...) count only when named; `never` always wins. Nothing here changes any application: it only writes decisions.json.
"""
import argparse, datetime as dt, html, json, os, re, subprocess, sys
import yaml
from jsonschema import Draft202012Validator

sys.stdout.reconfigure(encoding='utf-8')
QA_OS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SCHEMA = os.path.join(QA_OS, 'plugins', 'qa-os', 'schemas', 'decisions.schema.json')
BLOCK = re.compile(r'---\s*QA-OS\s*---(.*?)---\s*/QA-OS\s*---', re.S | re.I)
KEYS = {'env', 'user', 'scope', 'market', 'screens', 'terms', 'data', 'allow', 'never', 'expected-variance', 'key'}
SCOPES = ('browser', 'browser+manual', 'all')
ONE_WAY = {'delete', 'submit', 'forward', 'approve', 'reject', 'cancel', 'post', 'close', 'settle', 'terminate', 'authorize'}
SAFE = {'create', 'save', 'update', 'edit', 'add', 'upload', 'download'}


def now():
    return dt.datetime.now().isoformat(timespec='seconds')


def load_json(p, default=None):
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default


def save_json(p, d):
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=1, ensure_ascii=False)
        f.write('\n')


def clean(v):
    v = re.split(r'\s#', v, maxsplit=1)[0].strip()
    return '' if v.lower() in ('none', '-', 'n/a', 'na') else v


def split(v, seps=r'[;,]'):
    return [x.strip() for x in re.split(seps, v) if x.strip()]


def read_block(text):
    text = html.unescape(re.sub(r'<[^>]+>', '\n', text))
    m = BLOCK.search(text)
    if not m:
        return None, []
    fields, warn = {}, []
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or ':' not in line:
            continue
        k, v = line.split(':', 1)
        k = k.strip().lower().replace('_', '-')
        if k not in KEYS:
            warn.append(f"unknown intake field '{k}' ignored")
            continue
        v = clean(v)
        if v:
            fields[k] = (fields[k] + '; ' + v) if k in ('terms', 'data', 'expected-variance', 'screens') and k in fields else v
    return fields, warn


def plan_user(app_cfg, screens, org):
    """Run access_lookup.py plan-user; return (lines, recommended_env, recommended_user, full_cover list)."""
    look = os.path.join(QA_OS, app_cfg['access']['lookup'])
    cmd = [sys.executable, look, 'plan-user', *screens] + (['--org', org] if org else [])
    out = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', cwd=QA_OS).stdout
    accts = []
    for m in re.finditer(r'^(\S+) / (\S+)\s+\(org (.*?)\): (\d+)/(\d+) screens reachable(.*)$', out, re.M):
        accts.append({'env': m.group(1), 'user': m.group(2), 'org': m.group(3), 'got': int(m.group(4)), 'of': int(m.group(5)), 'missing': 'MISSING' in m.group(6)})
    return out, accts


def parse(a):
    run = os.path.abspath(a.run_dir)
    rj = load_json(os.path.join(run, 'run.json')) or {}
    key, app = rj.get('key', os.path.basename(os.path.dirname(run))), rj.get('app', 'snd')
    cfg = yaml.safe_load(open(os.path.join(QA_OS, 'apps', app, 'app.yaml'), encoding='utf-8'))
    pack = load_json(os.path.join(QA_OS, 'apps', app, 'knowledge', 'decisions.json'), {})
    story = a.story or next((os.path.join(run, 'inputs', f) for f in sorted(os.listdir(os.path.join(run, 'inputs'))) if os.path.isfile(os.path.join(run, 'inputs', f))), None) if os.path.isdir(os.path.join(run, 'inputs')) else a.story
    text = open(story, encoding='utf-8', errors='replace').read() if story and os.path.exists(story) else ''
    fields, warn = read_block(text)
    found = fields is not None
    fields = fields or {}
    assumed = []
    d = {'key': key, 'app': app, 'created': now(), 'intake': {'found': found, 'source': os.path.relpath(story, run) if story else None}}
    if not found:
        warn.append('no QA-OS intake block in the story: all values are assumed from the app pack / defaults')

    # scope
    sc = fields.get('scope') or pack.get('defaults', {}).get('scope')
    src = 'intake' if fields.get('scope') else 'app-pack' if sc else 'default'
    sc = sc or 'browser+manual'
    if sc not in SCOPES:
        warn.append(f"scope '{sc}' is not one of {SCOPES}; using browser+manual"); sc, src = 'browser+manual', 'default'
    d['scope'] = {'value': sc, 'source': src, 'assumed': src != 'intake'}
    if src != 'intake': assumed.append('scope')

    # screens, market
    screens = split(fields.get('screens', ''), ';') if fields.get('screens') else (split(a.screens, ';') if a.screens else [])
    d['screens'] = screens
    mk_map = cfg.get('access', {}).get('market_of_story', {})
    market, msrc = fields.get('market'), 'intake'
    if not market:
        toks = sorted(mk_map, key=len, reverse=True)
        market = next((t for t in toks if re.search(r'(?<![A-Za-z])' + re.escape(t) + r'(?![A-Za-z])', text)), None)
        msrc = 'story-text' if market else 'pending'
    org = mk_map.get(market) if market else None
    d['market'] = {'value': market, 'source': msrc, 'assumed': msrc != 'intake', 'note': f'org {org}' if org else 'no market found: account chosen without an org preference'}
    if msrc != 'intake': assumed.append('market')

    # env + user
    envs = cfg.get('environments', {})
    want_env, want_user = fields.get('env'), fields.get('user')
    if want_env and want_env not in envs:
        warn.append(f"env '{want_env}' is not in app.yaml environments {list(envs)}; ignored"); want_env = None
    if want_env and want_user:
        real = next((u for u in envs[want_env].get('users', {}) if u.lower() == want_user.lower()), None)
        if not real:
            warn.append(f"user '{want_user}' is not a known account of {want_env}; ignored"); want_user = None
        else:
            want_user = real
    env_c = user_c = None
    plan_text = ''
    if screens and cfg.get('access'):
        plan_text, accts = plan_user(cfg, screens, org)
        full = [x for x in accts if not x['missing']]
        pick = lambda pool: pool[0] if pool else None
        chosen = None
        if want_env and want_user:
            mine = next((x for x in accts if x['env'] == want_env and x['user'].lower() == want_user.lower()), None)
            if mine and not mine['missing']:
                chosen = mine
            else:
                alt = pick([x for x in full if x['env'] == want_env]) or pick(full)
                warn.append(f"{want_env}/{want_user} does not reach every screen" + (f"; using {alt['env']}/{alt['user']}" if alt else '; no account reaches all of them: split the story or ask Q-ENV-1'))
                chosen = alt
                if alt: d['_override'] = f'{want_env}/{want_user}'
        else:
            pool = [x for x in full if (not want_env or x['env'] == want_env)]
            chosen = pick(pool) or pick(full)
            if not chosen: warn.append('no account reaches every screen: split the story by environment or ask Q-ENV-1')
        if chosen:
            env_c, user_c = chosen['env'], chosen['user']
            if not (want_env and want_user and (env_c, user_c.lower()) == (want_env, want_user.lower())):
                assumed += [x for x in ('env', 'user') if x not in assumed]
    if not env_c:
        env_c, user_c = want_env, want_user
    ov = d.pop('_override', None)
    isrc = 'intake' if (want_env and want_user and (env_c, (user_c or '').lower()) == (want_env, want_user.lower())) else 'plan-user' if screens and env_c else 'pending' if not env_c else 'intake'
    note = 'no screens known yet: run again with --screens after analysis to verify/choose the account' if not screens else ''
    d['env'] = {'value': env_c, 'source': isrc, 'assumed': isrc != 'intake', 'note': note, 'overridden_from': ov}
    d['user'] = {'value': user_c, 'source': isrc, 'assumed': isrc != 'intake', 'note': note, 'overridden_from': ov}
    d['distributor'] = (envs.get(env_c, {}).get('users', {}).get(user_c, {}) or {}).get('distributor') if env_c and user_c else None

    # terms, data hints, variances (+ app-pack knowledge as context)
    terms = []
    for t in split(fields.get('terms', ''), ';'):
        if '=' in t:
            s, p = [x.strip() for x in t.split('=', 1)]
            terms.append({'story': s, 'app': p, 'source': 'intake'})
        else:
            warn.append(f"term '{t}' ignored (use 'story term = app term')")
    have = {t['story'].lower() for t in terms}
    for t in pack.get('terms', []):
        if t['story'].lower() not in have:
            terms.append({'story': t['story'], 'app': t['app'], 'source': 'app-pack'})
    d['terms'] = terms
    d['data_hints'] = split(fields.get('data', ''), ';')
    d['expected_variances'] = [{'text': v, 'source': 'intake'} for v in split(fields.get('expected-variance', ''), ';')]
    d['known'] = {k: pack.get(k, []) for k in ('terms', 'variances', 'rules')}

    # authorization
    allow, never = [x.lower() for x in split(fields.get('allow', ''))], [x.lower() for x in split(fields.get('never', ''))]
    np_ = envs.get(env_c, {}).get('non_production') if env_c else None
    unknown = [x for x in allow + never if x not in ONE_WAY | SAFE]
    if unknown:
        warn.append(f"unknown action word(s) {sorted(set(unknown))}: treated like one-way actions (must be named to count)")
    allowed = [x for x in allow if x not in never] if np_ else []
    if allow and not np_:
        warn.append(f"'allow' ignored: environment {env_c or '?'} is not marked non_production in app.yaml")
    d['authorization'] = {'env_non_production': np_, 'allowed': allowed, 'never': never, 'one_way_allowed': [x for x in allowed if x not in SAFE],
                          'policy': 'as listed; anything else that changes data or stock is skipped and marked unverified' if allowed else
                                    'unspecified: ask at C2 (Q-RISK) before any data-changing step; read-only steps need no approval'}
    d['answers'] = (load_json(os.path.join(run, 'decisions.json'), {}) or {}).get('answers', [])
    d['assumed'], d['warnings'] = assumed, warn
    errs = [e.message for e in Draft202012Validator(json.load(open(SCHEMA, encoding='utf-8'))).iter_errors(d)]
    if errs:
        sys.exit('decisions.json failed schema: ' + '; '.join(errs))
    save_json(os.path.join(run, 'decisions.json'), d)
    if plan_text:
        open(os.path.join(run, 'plan_user.txt'), 'w', encoding='utf-8').write(plan_text)
    show(d)


def show(d):
    v = lambda c: f"{c['value']} [{c['source']}{', assumed' if c.get('assumed') else ''}]" + (f" (was {c['overridden_from']})" if c.get('overridden_from') else '')
    print(f"decisions for {d['key']} ({d['app']}), intake block: {'found' if d['intake']['found'] else 'NOT found'}")
    print(f"  env    : {v(d['env'])}\n  user   : {v(d['user'])}" + (f"  distributor {d['distributor']}" if d.get('distributor') else ''))
    print(f"  scope  : {v(d['scope'])}\n  market : {v(d['market'])}")
    au = d['authorization']
    print(f"  allow  : {', '.join(au['allowed']) or '-'}  |  never: {', '.join(au['never']) or '-'}  |  one-way allowed: {', '.join(au['one_way_allowed']) or '-'}  |  env non_production: {au['env_non_production']}")
    print(f"  policy : {au['policy']}")
    print(f"  terms  : {len(d['terms'])} ({sum(1 for t in d['terms'] if t['source'] == 'app-pack')} from app pack) | variances: {len(d['expected_variances'])} | data hints: {len(d['data_hints'])} | answers: {len(d['answers'])}")
    for w in d['warnings']:
        print('  WARN   :', w)
    if d['assumed']:
        print('  assumed:', ', '.join(d['assumed']))


def answer(a):
    p = os.path.join(os.path.abspath(a.run_dir), 'decisions.json')
    d = load_json(p)
    if not d:
        sys.exit('no decisions.json yet: run "parse" first')
    d['answers'] = [x for x in d.get('answers', []) if x['id'] != a.id] + [{'id': a.id, 'kind': a.kind, 'key': a.key, 'value': a.value, 'ruling': a.ruling,
                                                                            'owner': a.owner, 'reusable': bool(a.reusable), 'at': now()}]
    save_json(p, d)
    print(f"answer {a.id} saved ({a.kind}: {a.key}); reusable={bool(a.reusable)}")


ap = argparse.ArgumentParser()
sp = ap.add_subparsers(dest='cmd', required=True)
p = sp.add_parser('parse'); p.add_argument('run_dir'); p.add_argument('--story'); p.add_argument('--screens')
p = sp.add_parser('answer'); p.add_argument('run_dir'); p.add_argument('--id', required=True); p.add_argument('--kind', required=True, choices=['term', 'variance', 'rule', 'other'])
p.add_argument('--key', required=True); p.add_argument('--value', required=True); p.add_argument('--ruling', choices=['app-is-right', 'not-built', 'ask-ba']); p.add_argument('--owner'); p.add_argument('--reusable', action='store_true')
p = sp.add_parser('show'); p.add_argument('run_dir')
a = ap.parse_args()
if a.cmd == 'parse': parse(a)
elif a.cmd == 'answer': answer(a)
else: show(load_json(os.path.join(os.path.abspath(a.run_dir), 'decisions.json')))
