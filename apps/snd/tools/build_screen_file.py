"""Screen file builder (design v4 W1): one machine-readable screen file per trained screen -> apps/snd/screens/<option_id>.json

  python apps/snd/tools/build_screen_file.py "Distributor Profile HQ"          # by menu title
  python apps/snd/tools/build_screen_file.py DYL_L__BusinessEntityProfile      # by option id (= sidebar li id)
  python apps/snd/tools/build_screen_file.py --all-trained                     # every trained screen + screens/_index.json
  python apps/snd/tools/build_screen_file.py --all-trained --env cnr1dev1      # live sources of one environment only
  python apps/snd/tools/build_screen_file.py --list-trained                    # print the trained set, write nothing

Merges, per screen (deterministic, files only - no network and no database calls):
  1. knowledge/screens_db/<DYL_layout>.json   config tables: structure, labels, required, data field, list source, max length  [db]
  2. knowledge/screens_observed/<id>.json     whole-app sweep (DOM ids, widgets)                                              [observed]
     knowledge/screens_observed/LIVE_*.json   read-only live harvests (labels, ids, widgets, notes -> lessons)                 [observed]
  3. runs/**/recording_*.json                 watcher logs of live runs (ids of fields, buttons, tabs, grids; toasts, alerts)  [recorded]
     runs/**/results.json                     tag-box and wrapper-id hints only
  4. tools/screen_lessons_backfill.json       screen-level lessons and stated field rules converted from run notes             [stated]
  5. the existing screen file                 lessons, messages, difference statuses and hand-written field facts are kept
Live ids win over config (recorded > live harvest > sweep > db). Every element/widget that differs from the config is written
to differences[] (status 'open' unless a person changed it). The output is validated against plugins/qa-os/schemas/screen.schema.json.
"""
import argparse, collections, copy, glob, json, os, re, sys
from urllib.parse import urlparse, parse_qs

sys.stdout.reconfigure(encoding='utf-8')
TOOLS = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(TOOLS, '..'))
QA_OS = os.path.normpath(os.path.join(APP, '..', '..'))
K = os.path.join(APP, 'knowledge')
OUT = os.path.join(APP, 'screens')
RUNS = os.path.join(QA_OS, 'runs')
SCHEMA = os.path.join(QA_OS, 'plugins', 'qa-os', 'schemas', 'screen.schema.json')
SEED = os.path.join(TOOLS, 'screen_lessons_backfill.json')
WALK_GROUPS = {'11': 'group 11 walk', '66': 'group 66 walk'}
ROW_XPATH = "//tr[contains(@class,'dx-data-row')][td[normalize-space(.)='{value}']]/td[1]"
SKIP_CLICK_IDS = {'menurollin', 'for-selenium', 'proceedbtn', 'selectbox1', 'logout'}
GENERIC_WIDGETS = {'text', 'select', 'unknown', None}
BUILDER_KEYS = {'element', 'locator', 'widget', 'provenance', 'seen_in', 'alt_elements', 'env_elements', 'tab', 'config_id', 'data_field',
                'list_source', 'regex'}
SELECTOR_IDS = {'selectbox1', 'proceedbtn', 'logout'}   # company/distributor selector and logout: the screen was left
INTERNAL = '<!--i-->'


def rel(p):
    return os.path.relpath(p, QA_OS).replace('\\', '/')


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def clean_label(s):
    return re.sub(r'\s+', ' ', str(s or '')).strip().rstrip('*').strip()


def norm(s):
    return re.sub(r'[^a-z0-9]', '', str(s or '').lower())


def id_core(s):
    """TXT__epp1_offdays / DDL__EPP1_OFFDAYS / EPP1_OFFDAYS -> epp1offdays (the control-type prefix is dropped)."""
    s = str(s or '')
    s = re.sub(r'^(TXT|DDL|DT|TT|NUM|CHK|TA|TXTA|LBL|SW)_{1,2}', '', s, flags=re.I)
    return norm(s)


def widget_of(raw, name=None, kind=None):
    w = str(raw or '').lower().strip()
    if name and re.match(r'^TT_', str(name)):
        return 'time'
    table = {'textbox': 'text', 'text': 'text', 'input': 'text', 'input:text': 'text', 'selectbox': 'select', 'select': 'select',
             'dropdown': 'select', 'div': 'select', 'datebox': 'date', 'date': 'date', 'numberbox': 'number', 'number': 'number',
             'textarea': 'textarea', 'checkbox': 'checkbox', 'switch': 'switch', 'tagbox': 'tagbox', 'lookup': 'lookup',
             'autocomplete': 'autocomplete', 'type-ahead': 'autocomplete', 'radiogroup': 'radio', 'masked text': 'masked',
             'masked': 'masked', 'allowable': 'grid_column', 'readonly': 'display', 'time': 'time'}
    if w in table:
        return table[w]
    if w.startswith('dropdown (multi'):
        return 'tagbox'
    if not w and kind == '0002':
        return 'select'
    if not w and kind == '0001':
        return 'text'
    return 'unknown' if w else None


def date_of(*vals):
    for v in vals:
        m = re.search(r'(20\d\d)-?(\d\d)-?(\d\d)', str(v or ''))
        if m:
            return f'{m.group(1)}-{m.group(2)}-{m.group(3)}'
    return None


def strip_internal(text):
    return '\n'.join(l for l in str(text).splitlines() if not l.rstrip().endswith(INTERNAL)).strip()


# ------------------------------------------------------------------ menu
class Menu:
    def __init__(self):
        flat = [m for m in load(os.path.join(K, 'snd_menu_flat.json')) if isinstance(m, dict) and m.get('option_id')]
        known = {m['group_id'] for m in flat}
        for p in sorted(glob.glob(os.path.join(K, 'env', '*', 'menu.*.json'))):     # options only in a live menu (newer than the base DB)
            for e in load(p).get('entries', []):
                if e.get('id') and e.get('app_option') and e['id'] not in known and e.get('title'):
                    known.add(e['id'])
                    flat.append({'group_id': e['id'], 'option_id': e['app_option'], 'title': e['title'], 'route': e.get('route'),
                                 'page_param': e.get('param'), 'path': ' > '.join(x for x in e.get('path') or [e['title']] if x)})
        self.by_gid, self.by_opt, self.by_title, self.by_layout, self.by_route = {}, {}, collections.defaultdict(list), {}, {}
        for m in flat:
            self.by_gid.setdefault(m['group_id'], m)
            self.by_opt.setdefault(m['option_id'], m)
            self.by_title[norm(m['title'])].append(m)
            lc = (parse_qs(m.get('page_param') or '').get('layoutCode') or [None])[0]
            if lc:
                self.by_layout.setdefault(lc, m)
            if m.get('route') and m['route'] != '/dyl/layout':
                self.by_route.setdefault(m['route'].rstrip('/'), m)
        self.top, self.live_title = {}, {}
        for p in sorted(glob.glob(os.path.join(K, 'env', '*', 'menu.*.json'))):
            for e in load(p).get('entries', []):
                if e.get('id') and e.get('top_id'):
                    self.top.setdefault(e['id'], e['top_id'])
                if e.get('id') and e.get('title') and e.get('app_option'):
                    self.live_title.setdefault(e['id'], clean_label(e['title']))
                    if e['id'] in self.by_gid and self.by_gid[e['id']] not in self.by_title[norm(e['title'])]:
                        self.by_title[norm(e['title'])].append(self.by_gid[e['id']])
        self.prefer = set()          # tie-break for duplicate titles: options used by the walks / env menus

    def layout_code(self, m):
        return (parse_qs(m.get('page_param') or '').get('layoutCode') or [None])[0]

    def resolve(self, token):
        """option id / group id / layout code / menu title / route -> menu entry (or None)."""
        t = str(token or '').strip()
        if not t:
            return None
        if t in self.by_gid:
            return self.by_gid[t]
        if t in self.by_opt:
            return self.by_opt[t]
        if 'DYL_' + t in self.by_gid:
            return self.by_gid['DYL_' + t]
        if t in self.by_layout:
            return self.by_layout[t]
        if t.startswith('/'):
            return self.resolve_url(t)
        cands = self.by_title.get(norm(t), [])
        if '>' in t and not cands:
            parts = [norm(p) for p in t.split('>')]
            for m in self.by_gid.values():
                if [norm(p) for p in m['path'].split('>')][-len(parts):] == parts:
                    return m
            cands = self.by_title.get(norm(t.split('>')[-1]), [])
        if not cands:
            return None
        cands = sorted(cands, key=lambda m: (m['group_id'] not in self.prefer, m['group_id'] not in self.top, m['group_id']))
        return cands[0]

    def resolve_url(self, url):
        u = urlparse(str(url))
        path = re.sub(r'^/ngui', '', u.path).rstrip('/')
        lc = (parse_qs(u.query).get('layoutCode') or [None])[0]
        if lc:
            return self.by_layout.get(lc)
        best = None
        for r, m in self.by_route.items():
            if path == r or path.startswith(r + '/'):
                if not best or len(r) > len(best[0]):
                    best = (r, m)
        return best[1] if best else None


# ------------------------------------------------------------------ live facts from runs
def new_live():
    return {'fields': {}, 'buttons': {}, 'tabs': {}, 'grids': {}, 'messages': [], 'refs': set(), 'dates': set(), 'stories': set()}


def run_env(path):
    d = os.path.dirname(path)
    while d.startswith(RUNS) and d != RUNS:
        rj = os.path.join(d, 'run.json')
        if os.path.exists(rj):
            try:
                return load(rj).get('env')
            except Exception:
                return None
        d = os.path.dirname(d)
    return None


def story_of(path):
    return rel(path).split('/')[1]


def recordings(menu, env_filter=None):
    """{option_id: live facts} from every watcher log under runs/ (oldest first, so newer facts overwrite older ones)."""
    out = collections.defaultdict(new_live)
    files = []
    for p in glob.glob(os.path.join(RUNS, '**', 'recording_*.json'), recursive=True):
        try:
            d = load(p)
        except Exception:
            continue
        if not isinstance(d, dict) or not isinstance(d.get('log'), list):
            continue
        meta = d.get('meta') or {}
        env = meta.get('env') or run_env(p)
        date = date_of(meta.get('recorded'), meta.get('date')) or date_of(*rel(p).split('/'))
        if env_filter and env and env != env_filter:
            continue
        files.append((date or '', rel(p), env, d['log']))
    for date, ref, env, log in sorted(files):
        cur = cur_tab = last_grid = last_click = caption = None
        prev = None
        for e in log:
            if not isinstance(e, dict):
                continue
            a = e.get('act')
            just_clicked, prev = (prev or {}).get('act') == 'click', e
            if str(e.get('id') or '').lower() in SELECTOR_IDS or (a == 'click' and not e.get('id') and clean_label(e.get('text')) == 'Change'):
                cur = cur_tab = last_grid = last_click = caption = None        # profile menu Change / selector / logout
                continue
            if a == 'nav_click':
                m = menu.resolve(e.get('id')) or menu.resolve(e.get('search'))
                cur, cur_tab, last_grid, caption = (m['group_id'] if m else None), None, None, None
                continue
            if a in ('nav', 'screen'):
                m = menu.resolve_url(e.get('url')) if e.get('url') else None
                if a == 'nav' and not m:
                    m = menu.resolve(e.get('term'))
                u = urlparse(str(e.get('url') or ''))
                if m and m['group_id'] != cur:
                    cur, cur_tab, last_grid, caption = m['group_id'], None, None, None
                elif not m and u.path and '/dyl/layout' not in u.path and a == 'screen':
                    cur = None                         # home, selector or an unknown page
                cm = re.search(r'> ([^>]+?) > Data grid with', str(e.get('crumb') or ''))
                caption = clean_label(cm.group(1)) if cm else caption
                continue
            if not cur:
                continue
            L = out[cur]
            L['refs'].add(ref)
            L['stories'].add(ref.split('/')[1])
            if date:
                L['dates'].add(date)
            prov = {'source': 'recorded', 'env': env, 'date': date or None, 'ref': ref}
            eid = (e.get('id') or '').strip()
            if a == 'tab':
                if e.get('value'):
                    cur_tab = clean_label(e['value'])
                    L['tabs'][cur_tab] = {'element': eid or None, 'provenance': prov}
                continue
            if a in ('text', 'pick', 'option', 'check', 'remember', 'cell', 'row', 'row_select'):
                grid = e.get('grid')
                if a == 'row':
                    for c in e.get('cells') or []:
                        _grid_cell(L, grid, c.get('label'), c.get('id'), c.get('widget'), None, prov, caption)
                    if e.get('button'):
                        _grid_row_button(L, grid, e['button'], prov, caption)
                    last_grid = grid or last_grid
                    continue
                if a == 'row_select':
                    g = _grid(L, grid or 'grid', prov, caption)
                    if e.get('id') and re.match(r'^row_\d+_', e['id']):
                        g['row_id_pattern'] = re.sub(r'^row_\d+_', 'row_N_', e['id'])
                    g['key_column'] = clean_label(e.get('keyColumn') or e.get('column')) or g.get('key_column')
                    if e.get('column'):
                        g['columns'].setdefault(clean_label(e['column']), None)
                    last_grid = grid or last_grid
                    continue
                if not eid:
                    continue
                if a == 'check' and eid == 'gridFilterCheckbox':
                    g = _grid(L, last_grid or 'grid', prov, caption)
                    g['filter_elements'].add(eid)
                    continue
                if grid:
                    _grid_cell(L, grid, e.get('column') or e.get('label'), eid, e.get('widget'), e.get('cellId'), prov, caption)
                    last_grid = grid
                    continue
                label = clean_label(e.get('label'))
                if not label or label.lower() == 'search here':
                    continue
                w = 'checkbox' if a == 'check' else widget_of(e.get('widget'), eid, e.get('kind'))
                f = L['fields'].setdefault(eid, {'label': label, 'element': eid})
                f.update({'label': label, 'provenance': prov})
                if w and w != 'unknown':
                    f['widget'] = w
                if cur_tab:
                    f['tab'] = cur_tab
                continue
            if a == 'click':
                if e.get('generatedId') or eid.lower() in SKIP_CLICK_IDS or eid.startswith('dx-'):
                    continue
                label = clean_label(e.get('text') or e.get('target'))
                if re.match(r'^rowEditBtn_', eid):
                    _grid_row_button(L, last_grid, eid, prov, caption)
                    continue
                if not eid or not label:
                    continue
                if re.search(r'popup|modal', eid, re.I) and '(popup)' not in label:
                    label += ' (popup)'
                L['buttons'][label] = {'element': eid, 'provenance': prov}
                last_click = label
                continue
            if a == 'toast':
                kind = str(e.get('type') or '').lower()
                typ = 'toast-' + kind if kind in ('success', 'error', 'warning', 'info') else 'toast'
                after = e.get('after') or (last_click if just_clicked else None)
                for t in e.get('messages') or []:
                    if str(t).strip():
                        L['messages'].append({'type': typ, 'text': str(t).strip(), 'when': f'after {after}' if after else None, 'provenance': prov})
                continue
            if a == 'alert' and e.get('text'):
                L['messages'].append({'type': 'confirm' if e.get('dialog') == 'confirm' else 'alert', 'text': str(e['text']).strip(),
                                      'when': f'after {last_click}' if (last_click and just_clicked) else None, 'provenance': prov})
    return out


def _grid(L, gid, prov, caption):
    g = L['grids'].setdefault(gid, {'element': gid if gid not in ('grid',) else None, 'caption': None, 'columns': {},
                                    'cells': {}, 'row_buttons': {}, 'filter_elements': set(), 'provenance': prov})
    g['provenance'] = prov
    if caption and not g['caption']:
        g['caption'] = caption
    return g


def _grid_cell(L, gid, column, eid, widget, cell_id, prov, caption):
    g = _grid(L, gid or 'grid', prov, caption)
    col = clean_label(column)
    if not col:
        return
    g['columns'].setdefault(col, None)
    c = g['cells'].setdefault(col, {})
    if eid:
        c['element'] = eid
    w = widget_of(widget)
    if w and w != 'unknown':
        c['widget'] = w
    if cell_id and re.match(r'^row_\d+_', cell_id):
        c['cell_id_pattern'] = re.sub(r'^row_\d+_', 'row_N_', cell_id)


def _grid_row_button(L, gid, eid, prov, caption):
    m = re.match(r'^rowEditBtn_(?:Modal_)?([A-Za-z]+)_\d+$', eid or '')
    if not m:
        return
    g = _grid(L, gid or 'grid', prov, caption)
    g['row_buttons'][m.group(1)] = re.sub(r'_\d+$', '_N', eid)


def result_hints():
    """From results.json texts: element ids described as tag boxes, and inner/wrapper button ids."""
    tag, wrap = set(), {}
    for p in sorted(glob.glob(os.path.join(RUNS, '**', 'results.json'), recursive=True)):
        try:
            s = json.dumps(load(p), ensure_ascii=False)
        except Exception:
            continue
        for m in re.finditer(r'#([A-Za-z][\w-]*)\s*\(tag ?box', s, re.I):
            tag.add(m.group(1).lower())
        for m in re.finditer(r'#([A-Za-z][\w-]*)\s*\(wrapper #([A-Za-z][\w-]*)\)', s):
            wrap.setdefault(m.group(2), m.group(1))
    return tag, wrap


# ------------------------------------------------------------------ observed (sweep + live harvests)
def observed_index(menu, env_filter=None):
    """{option_id: [(rank, date, env, ref, data)]}: rank 1 = sweep, 2 = live harvest."""
    idx = collections.defaultdict(list)
    for p in sorted(glob.glob(os.path.join(K, 'screens_observed', '*.json'))):
        b = os.path.basename(p)
        if b.startswith('_'):
            continue
        try:
            d = load(p)
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        pv = d.get('provenance') or {}
        env, date = pv.get('env'), date_of(pv.get('date'))
        if env_filter and env and env != env_filter:
            continue
        live = b.startswith('LIVE_')
        m = None
        if live:
            oid = str(d.get('option_id') or '')
            m = menu.resolve_url(oid) if oid.startswith('/') else (menu.resolve(oid) if oid else None)
            if not m and d.get('url_path'):
                m = menu.resolve_url(d['url_path'])
            if not m:
                m = menu.resolve(d.get('title'))
        else:
            m = menu.resolve(b[:-5]) or menu.resolve(d.get('option_id'))
        if m:
            idx[m['group_id']].append((2 if live else 1, date or '', env, rel(p), d))
    for k in idx:
        idx[k].sort(key=lambda x: (x[0], x[1], x[3]))
    return idx


def observed_facts(entries):
    """Normalise sweep / live-harvest files into the same shape as the recorded facts."""
    L = new_live()
    notes = []
    for rank, date, env, ref, d in entries:
        prov = {'source': 'observed', 'env': env, 'date': date or None, 'ref': ref}
        L['refs'].add(ref)
        if date:
            L['dates'].add(date)
        nodes = [(d, None)] + [(t, clean_label(t.get('name') or t.get('text'))) for t in d.get('tabs') or [] if isinstance(t, dict)]
        labels = collections.Counter(clean_label(f.get('label')) for n, _ in nodes for f in n.get('fields') or [] if isinstance(f, dict))
        for node, tab in nodes:
            if tab:
                L['tabs'].setdefault(tab, {'element': None, 'provenance': prov})
            for f in node.get('fields') or []:
                if not isinstance(f, dict) or not f.get('id'):
                    continue
                lab = clean_label(f.get('label'))
                reliable = rank == 2 or (lab and labels[lab] == 1)          # sweep labels are often shifted to the neighbour
                fx = L['fields'].setdefault(f['id'], {'element': f['id']})
                fx.update({'label': lab if reliable else None, 'provenance': prov, 'rank': rank,
                           'widget': widget_of(f.get('widget') or f.get('type'), f['id']) or fx.get('widget'),
                           'required': f.get('required'), 'readonly': f.get('readonly')})
                if tab:
                    fx['tab'] = tab
                if rank == 2 and f.get('default') not in (None, ''):
                    fx['default'] = f['default']
            for bt in node.get('buttons') or []:
                if not isinstance(bt, dict):
                    continue
                lab, bid = clean_label(bt.get('text') or bt.get('title')), (bt.get('id') or '').strip()
                if not lab or not bid or bid.lower() in SKIP_CLICK_IDS or '..' in bid or ' ' in bid:
                    continue
                if re.match(r'^rowEditBtn_', bid):
                    continue
                L['buttons'][lab] = {'element': bid, 'provenance': prov,
                                     'risk': 'changes-data' if 'ACTION' in str(bt.get('kind', '')) else None}
            for i, g in enumerate(node.get('grids') or []):
                if not isinstance(g, dict):
                    continue
                cols = [clean_label(' '.join(h) if isinstance(h, list) else h) for h in g.get('headers') or []]
                cols = [c for c in cols if c and not c.startswith('(')]
                gid = g.get('id') or f'{ref}#{i}'
                gg = L['grids'].setdefault(gid, {'element': g.get('id'), 'caption': None, 'columns': {}, 'cells': {}, 'row_buttons': {},
                                                 'filter_elements': set(), 'provenance': prov})
                for c in cols:
                    gg['columns'].setdefault(c, None)
                fi = g.get('filter_inputs')
                if isinstance(fi, dict):
                    gg['filter_elements'] |= {v for v in fi.values() if isinstance(v, str)}
                if g.get('pager_ids'):
                    gg['pager'] = str(g['pager_ids'])
        if rank == 2:
            for msg in d.get('messages') or []:
                txt = strip_internal(msg)
                if txt:
                    notes.append({'text': txt, 'kind': 'screen', 'field': None, 'source': ref, 'date': date or None})
    return L, notes


# ------------------------------------------------------------------ trained set and business pages
def frontmatter_screens(path):
    with open(path, encoding='utf-8') as f:
        txt = f.read()
    m = re.match(r'^---\s*\n(.*?)\n---', txt, re.S)
    if not m:
        return [], None
    fm = m.group(1)
    sm = re.search(r'^screens:\s*\[(.*?)\]\s*$', fm, re.M)
    um = re.search(r'^updated:\s*(\S+)', fm, re.M)
    items = [x.strip().strip('"\'') for x in sm.group(1).split(',')] if sm else []
    return [x for x in items if x], (date_of(um.group(1)) if um else None)


def business_pages(menu):
    """{option_id: [(n_screens_on_page, relpath, updated)]} from the 'screens:' front matter of the business pages."""
    pages, unresolved = collections.defaultdict(list), []
    for p in sorted(glob.glob(os.path.join(K, 'business', '**', '*.md'), recursive=True)):
        if 'learning_sessions' in p.replace('\\', '/'):
            continue
        items, upd = frontmatter_screens(p)
        for it in items:
            m = menu.resolve(it)
            if m:
                pages[m['group_id']].append((len(items), os.path.relpath(p, APP).replace('\\', '/'), upd))
            else:
                unresolved.append((os.path.relpath(p, APP).replace('\\', '/'), it))
    return pages, unresolved


def walk_dates():
    out = {}
    for gid in WALK_GROUPS:
        ds = [date_of(os.path.basename(p)) for p in glob.glob(os.path.join(K, 'business', 'learning_sessions', f'*G{gid}-*'))]
        out[gid] = max([d for d in ds if d] or [None], key=lambda x: x or '')
    return out


def walk_screens(menu):
    ap = os.path.join(K, 'framework_atlas', 'atlas.json')
    res = collections.defaultdict(set)
    if not os.path.exists(ap):
        return res
    a = load(ap)
    for gid in WALK_GROUPS:
        for r in (a.get('groups', {}).get(gid) or {}).get('chain', []):
            if not r.get('active'):
                continue
            f = a.get('flows', {}).get(r.get('flow_id')) or {}
            for mm in f.get('menus') or []:
                m = menu.resolve(mm.get('navigation')) or menu.resolve(mm.get('search_text'))
                if m:
                    res[m['group_id']].add(gid)
    return res


class Context:
    def __init__(self, env=None):
        self.env = env
        self.menu = Menu()
        self.walks = walk_screens(self.menu)
        self.menu.prefer = set(self.walks)
        self.pages, self.unresolved_pages = business_pages(self.menu)
        self.walk_dates = walk_dates()
        self.rec = recordings(self.menu, env)
        self.obs = observed_index(self.menu, env)
        self.tag_hint, self.wrap_hint = result_hints()
        self.seed = load(SEED) if os.path.exists(SEED) else {}
        self.curated = {}
        for p in glob.glob(os.path.join(OUT, '*.json')):
            if not os.path.basename(p).startswith('_'):
                try:
                    self.curated[load(p)['option_id']] = p
                except Exception:
                    pass

    def trained(self):
        keys = set(self.pages) | set(self.walks) | {k for k, v in self.rec.items() if v['fields'] or v['buttons'] or v['grids'] or v['tabs']}
        keys |= {k for k in self.curated if self.menu.resolve(k)}
        keys |= {s.get('screen') for s in self.seed.get('lessons', []) if self.menu.resolve(s.get('screen'))}
        return sorted(k for k in keys if k)


# ------------------------------------------------------------------ build one screen
def build(ctx, option_id):
    menu = ctx.menu
    m = menu.resolve(option_id)
    if not m:
        raise SystemExit(f'screen not found in the menu: {option_id}')
    key = m['group_id']
    out_path = os.path.join(OUT, f'{key}.json')
    existing = load(out_path) if os.path.exists(out_path) else {}
    lc = menu.layout_code(m)
    dbp = os.path.join(K, 'screens_db', f'DYL_{lc}.json') if lc else None
    if not (dbp and os.path.exists(dbp)):
        dbp = os.path.join(K, 'screens_db', f'{key}.json')
    db = load(dbp) if os.path.exists(dbp) else None
    if db is not None and not isinstance(db, dict):
        db = None
    path = [p.strip() for p in m['path'].split('>')]
    title = menu.live_title.get(key) or clean_label(m['title'])          # the live menu title wins over the base DB title
    path[-1] = title
    doc = {
        '$schema': '../../../plugins/qa-os/schemas/screen.schema.json',
        'option_id': key, 'title': title,
        'menu': {'path': path, 'option_id': key, 'search_text': title, 'top_id': menu.top.get(key),
                 'app_option': m['option_id'] if m['option_id'] != key else None},
        'route': m.get('route'), 'page_param': m.get('page_param'), 'layout_code': lc,
        'kind': 'dynamic' if (m.get('route') == '/dyl/layout' or lc) else 'static',
        'tabs': [], 'panels': [], 'fields': {}, 'buttons': {}, 'grids': {}, 'messages': [], 'lessons': [], 'differences': [],
    }
    seen = collections.defaultdict(list)            # label -> ['db', 'observed:cnr2dev3:2026-09-25', ...]
    config = {}                                     # label -> {element, widget} as configured
    dates = set()

    # 1. db config
    tabs, tab_pages = [], collections.OrderedDict()
    if db:
        page_tab = {}
        for pnl in db.get('panels') or []:
            doc['panels'].append({k: pnl.get(k) for k in ('page', 'tab', 'desc', 'table', 'is_child', 'grids', 'n_fields')})
            page_tab[pnl.get('page')] = pnl.get('tab')
            if pnl.get('tab'):
                tab_pages.setdefault(clean_label(pnl['tab']), []).append(str(pnl.get('page')))
        dprov = {'source': 'db', 'env': None, 'date': None, 'ref': rel(dbp)}
        for raw_label, f in (db.get('fields') or {}).items():
            lab = clean_label(raw_label)
            if not lab or lab in doc['fields']:
                continue
            w = widget_of(f.get('widget'), f.get('name')) or 'unknown'
            if w == 'text' and str(f.get('id') or '').startswith('textarea'):
                w = 'textarea'
            elif w == 'text' and f.get('type') == 'N':
                w = 'number'
            doc['fields'][lab] = {
                'element': f.get('name'), 'widget': w, 'tab': clean_label(page_tab.get(f.get('page'))) or None,
                'required': f.get('required'), 'readonly': f.get('readonly'), 'data_field': f.get('data_field'),
                'list_source': f.get('data_list_id'), 'max_length': f.get('max_length'), 'default': f.get('default'),
                'regex': f.get('regex'), 'config_id': f.get('id'), 'provenance': dict(dprov)}
            config[lab] = {'element': f.get('name'), 'widget': w}
            seen[lab].append('db')
        for b in db.get('buttons') or []:
            lab = clean_label(b)
            if lab:
                doc['buttons'][lab] = {'element': None, 'provenance': dict(dprov), 'seen_in': ['db']}
        for gname, g in (db.get('grids') or {}).items():
            doc['grids'][clean_label(gname)] = {'element': None, 'caption': None, 'columns': list(dict.fromkeys(clean_label(c) for c in g.get('columns') or [] if clean_label(c))),
                                                'edit_mode': g.get('edit_mode'), 'selection': g.get('selection'), 'provenance': dict(dprov)}
    for t, pages in tab_pages.items():
        variants = sorted({p.rsplit('_', 1)[-1] for p in pages if '_' in p}) if len(pages) > 1 else []
        tabs.append({'label': t, 'element': None, 'sub_tabs': variants, 'pages': pages,
                     'provenance': {'source': 'db', 'env': None, 'date': None, 'ref': rel(dbp)}})

    # field matching helpers
    def find_field(element, label, label_ok):
        el = str(element or '')
        for lab, f in doc['fields'].items():
            if f.get('element') and f['element'].lower() == el.lower():
                return lab, 'id'
        core = id_core(el)
        if core:
            for lab, f in doc['fields'].items():
                if id_core(f.get('element')) == core or (f.get('data_field') and norm(f['data_field']) == core):
                    return lab, 'id'
        if label_ok and label:
            for lab in doc['fields']:
                if norm(lab) == norm(label):
                    return lab, 'label'
        return None, None

    def apply_live(fact, src_tag):
        lab_live = fact.get('label')
        lab, how = find_field(fact['element'], lab_live, label_ok=bool(lab_live))
        if how == 'label' and (config.get(lab) or {}).get('element'):
            # same caption, unrelated configured control (e.g. a popup 'Comments' box): keep the configured element, note the other
            f = doc['fields'][lab]
            f['alt_elements'] = sorted(set(f.get('alt_elements', [])) | {fact['element']})
            label_only.append((lab, fact))
            seen[lab].append(src_tag)
            return
        if not lab:
            if not lab_live:
                return
            lab = lab_live
            doc['fields'][lab] = {'element': fact['element'], 'widget': fact.get('widget') or 'unknown', 'provenance': fact['provenance']}
        f = doc['fields'][lab]
        prev_el = f.get('element')
        if prev_el and prev_el != fact['element'] and f.get('locator'):
            f.setdefault('env_elements', {})[f['provenance'].get('env') or '?'] = prev_el
        f['element'] = fact['element']
        f['locator'] = {'id': fact['element']}
        nw, ow = fact.get('widget'), f.get('widget')
        live_before = f.get('provenance', {}).get('source') in ('observed', 'recorded')
        if nw and nw != 'unknown' and not (live_before and nw in GENERIC_WIDGETS and ow not in GENERIC_WIDGETS):
            f['widget'] = nw                                  # a generic recorded widget never hides a more specific live one
        f['provenance'] = dict(fact['provenance'])
        if fact.get('tab') and not f.get('tab'):
            f['tab'] = fact['tab']
        if fact.get('default') is not None and f.get('default') in (None, ''):
            f['default'] = fact['default']
        if 'env_elements' in f:
            f['env_elements'][fact['provenance'].get('env') or '?'] = fact['element']
            if len(set(f['env_elements'].values())) < 2:
                f.pop('env_elements')
        seen[lab].append(src_tag)

    def tag(prov):
        return ':'.join(x for x in (prov['source'], prov.get('env') or '', prov.get('date') or '') if x is not None).rstrip(':')

    sources = {'db': rel(dbp) if db else None, 'observed': [], 'recorded': [], 'stated': []}
    label_only = []

    # 2. observed (sweep, then live harvests), 3. recorded
    obs_L, obs_notes = observed_facts(ctx.obs.get(key, []))
    rec_L = ctx.rec.get(key) or new_live()
    for L, kind in ((obs_L, 'observed'), (rec_L, 'recorded')):
        sources[kind] = sorted(L['refs'])
        dates |= L['dates']
        facts = sorted(L['fields'].values(), key=lambda f: (f.get('rank', 3), f['provenance'].get('date') or '', f['provenance'].get('ref') or ''))
        for fact in facts:
            apply_live(fact, tag(fact['provenance']))
        for lab, t in L['tabs'].items():
            ex = next((x for x in tabs if norm(x['label']) == norm(lab)), None)
            if not ex:
                ex = {'label': lab, 'element': None, 'provenance': t['provenance']}
                tabs.append(ex)
            if t.get('element'):
                ex['element'] = t['element']
                ex['provenance'] = t['provenance']
        tab_labels = {norm(t['label']) for t in tabs}
        for lab, b in L['buttons'].items():
            if norm(lab) in tab_labels and kind == 'observed':
                continue
            ex = doc['buttons'].get(lab) or next((v for k, v in doc['buttons'].items() if v.get('element') == b['element']), None)
            if ex is None:
                ex = doc['buttons'].setdefault(lab, {'element': None})
            ex['element'] = b['element']
            ex['locator'] = {'id': b['element']}
            ex['provenance'] = dict(b['provenance'])
            if b.get('risk'):
                ex['risk'] = b['risk']
            ex.setdefault('seen_in', []).append(tag(b['provenance']))
        for gid, g in L['grids'].items():
            cols = list(g['columns'])
            target = None
            best = 0
            for name, dg in doc['grids'].items():
                if g.get('element') and dg.get('element') == g['element']:
                    target = name
                    break
                ov = len({norm(c) for c in cols} & {norm(c) for c in dg['columns']})
                if ov > best and (ov >= 2 or ov == len(cols)):
                    best, target = ov, name
            if not target:
                target = g.get('caption') or g.get('element') or (m['title'] if not doc['grids'] else f"{m['title']} grid {len(doc['grids']) + 1}")
                doc['grids'][target] = {'element': None, 'caption': None, 'columns': [], 'provenance': g['provenance']}
            dg = doc['grids'][target]
            for c in cols:
                if norm(c) not in {norm(x) for x in dg['columns']}:
                    dg['columns'].append(c)
            if g.get('element'):
                dg['element'] = g['element']
            if g.get('caption'):
                dg['caption'] = g['caption']
            for k in ('row_id_pattern', 'key_column', 'pager'):
                if g.get(k):
                    dg[k] = g[k]
            if g['cells']:
                dg.setdefault('cells', {}).update({k: v for k, v in g['cells'].items() if v})
            if g['row_buttons']:
                dg.setdefault('row_buttons', {}).update(g['row_buttons'])
            if g['filter_elements']:
                dg['filter_elements'] = sorted(set(dg.get('filter_elements', [])) | g['filter_elements'])
            dg['provenance'] = dict(g['provenance'])
            dg.setdefault('row_by_first_cell', ROW_XPATH)
        for msg in L['messages']:
            doc['messages'].append(msg)
    # grids keyed by the on-screen caption when it is known (what step authors write)
    for name in list(doc['grids']):
        cap = doc['grids'][name].get('caption')
        if cap and cap != name and cap not in doc['grids']:
            doc['grids'][cap] = doc['grids'].pop(name)

    # results.json hints: tag boxes and wrapper ids
    for lab, f in doc['fields'].items():
        if f.get('locator') and str(f.get('element')).lower() in ctx.tag_hint:
            f['widget'] = 'tagbox'
    for lab, b in doc['buttons'].items():
        if b.get('element') in ctx.wrap_hint:
            alt = ctx.wrap_hint[b['element']]
            b['alt_elements'] = sorted(set(b.get('alt_elements', [])) | {alt})
            b.setdefault('note', f'#{b["element"]} is the wrapper; the clickable inner element is #{alt}')

    # 4. stated seed facts
    seed_fields = (ctx.seed.get('fields') or {}).get(key) or {}
    for lab, facts in seed_fields.items():
        f = doc['fields'].get(lab)
        if f is None:
            continue
        for k, v in facts.items():
            if k in ('provenance', 'source', 'date'):
                continue
            f[k] = v
        sources['stated'].append(facts.get('source') or 'stated')
        dates.add(date_of(facts.get('date')) or '')

    # 5. existing file (hand-written facts, legacy curated format)
    legacy_prov = existing.get('provenance') if isinstance(existing.get('provenance'), dict) else None
    lp = {'source': 'observed', 'env': (legacy_prov or {}).get('env'), 'date': date_of((legacy_prov or {}).get('date')),
          'ref': rel(out_path)}
    for lab, ef in (existing.get('fields') or {}).items():
        ef = copy.deepcopy(ef)
        if 'locator' in ef and 'element' not in ef:                 # legacy curated: {"locator": {"id": ...}}
            loc = ef['locator']
            ef['element'] = loc.get('id')
            ef.setdefault('provenance', dict(lp))
            ef['widget'] = widget_of(ef.get('widget')) or 'unknown'
            for k in ('notes', 'options_note'):
                if k in ef:
                    ef['note'] = (ef.get('note', '') + ' ' + str(ef.pop(k))).strip()
            if 'options' in ef:
                ef['options_seen'] = ef.pop('options')
            if 'validation' in ef and 'max_length' in ef['validation']:
                ef.setdefault('max_length', ef['validation']['max_length'])
        f = doc['fields'].get(lab)
        if f is None:
            doc['fields'][lab] = ef
            seen[lab].append(tag(ef['provenance']) if isinstance(ef.get('provenance'), dict) else 'existing')
            continue
        epv = ef.get('provenance') if isinstance(ef.get('provenance'), dict) else {}
        hand = epv.get('source') == 'stated' or epv.get('ref') == rel(out_path)     # written by a person / curated live look
        if hand and not f.get('locator') and ef.get('locator'):
            for k in ('element', 'locator', 'widget', 'provenance'):
                if ef.get(k) is not None:
                    f[k] = ef[k]
        for k, v in ef.items():
            if k in BUILDER_KEYS and not hand:
                continue                                                  # recomputed on every build
            if k not in f or f[k] in (None, '', []):
                f[k] = v
    for lab, eb in (existing.get('buttons') or {}).items():
        eb = copy.deepcopy(eb)
        if 'locator' in eb and 'element' not in eb:
            eb['element'] = eb['locator'].get('id')
            eb.setdefault('provenance', dict(lp))
        b = doc['buttons'].get(lab)
        if b is None:
            doc['buttons'][lab] = eb
        else:
            if not b.get('locator') and eb.get('locator'):
                b.update({k: eb[k] for k in ('element', 'locator', 'provenance') if eb.get(k) is not None})
            for k, v in eb.items():
                if k not in b or b[k] in (None, '', []):
                    b[k] = v
    for name, eg in (existing.get('grids') or {}).items():
        eg = copy.deepcopy(eg)
        eg.setdefault('provenance', dict(lp))
        g = doc['grids'].get(name)
        if g is None:
            doc['grids'][name] = eg
        else:
            if eg.get('row_by_first_cell') and eg['row_by_first_cell'] != ROW_XPATH:
                g['row_by_first_cell'] = eg['row_by_first_cell']             # a curated row locator beats the generic one
            for k, v in eg.items():
                if k not in g or g[k] in (None, '', []):
                    g[k] = v
    for t in existing.get('tabs') or []:
        if isinstance(t, dict) and t.get('label') and not any(norm(x['label']) == norm(t['label']) for x in tabs):
            tabs.append(t)
    for k in ('breadcrumb', 'stage', 'modes', 'flow'):
        if k in existing:
            doc[k] = existing[k]
    if existing.get('kind') == 'hand-coded':
        doc['kind'] = 'static'
    if existing.get('route') and not doc['route']:
        doc['route'] = existing['route']

    # messages: existing (legacy dict or list) + recorded, deduplicated
    msgs = []
    em = existing.get('messages') or []
    if isinstance(em, dict):                                          # legacy curated {"save_success": {"text", "provenance"}}
        em = [{'type': 'message', 'text': v.get('text'), 'when': k.replace('_', ' '),
               'provenance': {'source': 'observed', 'env': lp['env'], 'date': date_of(v.get('provenance')) or lp['date'],
                              'ref': str(v.get('provenance') or rel(out_path))}} for k, v in em.items() if isinstance(v, dict) and v.get('text')]
    for sm in ctx.seed.get('messages') or []:
        mm = menu.resolve(sm.get('screen'))
        if mm and mm['group_id'] == key:
            em = list(em) + [{'type': sm.get('type', 'message'), 'text': sm['text'], 'when': sm.get('when'),
                              'provenance': {'source': sm.get('provenance', 'observed'), 'env': sm.get('env'), 'date': sm.get('date'), 'ref': sm.get('source')}}]
    for msg in list(em) + doc['messages']:                           # one entry per text (+ when); a known 'when' beats none
        msg = {kk: msg[kk] for kk in ('type', 'text', 'when', 'provenance') if kk in msg}
        same = [x for x in msgs if x['text'] == msg['text'] and (x.get('when') == msg.get('when') or not x.get('when') or not msg.get('when'))]
        if not same:
            msgs.append(msg)
            continue
        x = same[0]
        if not x.get('when') and msg.get('when'):
            x['when'] = msg['when']
        if x.get('type') in ('message', 'toast') and msg.get('type') not in ('message', 'toast', None):
            x['type'] = msg['type']
    doc['messages'] = msgs

    # lessons: existing + legacy observations + live-harvest notes + seed (never dropped, deduplicated by text)
    lessons = list(existing.get('lessons') or [])
    for o in existing.get('observations') or []:
        lessons.append({'text': strip_internal(o), 'kind': 'screen', 'field': None, 'source': rel(out_path) + ' (curated observations)', 'date': lp['date']})
    if legacy_prov:
        for k in ('note', 'also_observed'):
            if legacy_prov.get(k):
                lessons.append({'text': strip_internal(legacy_prov[k]), 'kind': 'screen', 'field': None, 'source': rel(out_path), 'date': lp['date']})
    lessons += obs_notes
    for s in ctx.seed.get('lessons') or []:
        if menu.resolve(s.get('screen')) and menu.resolve(s.get('screen'))['group_id'] == key:
            sources['stated'].append(rel(SEED))
            lessons.append({'text': s['text'], 'kind': 'screen', 'field': s.get('field'), 'source': s.get('source'), 'date': s.get('date')})
    seen_txt, doc['lessons'] = set(), []
    for l in lessons:
        t = strip_internal(l.get('text', ''))
        if t and norm(t) not in seen_txt:
            seen_txt.add(norm(t))
            doc['lessons'].append({'text': t, 'kind': 'screen', 'field': l.get('field'), 'source': l.get('source'), 'date': l.get('date')})

    # differences: config vs live (live wins), existing statuses kept
    diffs = []
    for lab, f in doc['fields'].items():
        c = config.get(lab)
        if not c or not f.get('locator') or f['provenance'].get('source') == 'db':
            continue
        pv = f['provenance']
        for what in ('element', 'widget'):
            cv, lv = c.get(what), f.get(what)
            if what == 'widget' and lv in GENERIC_WIDGETS | {'display'}:
                continue                                       # a generic or read-only rendering says nothing about the control type
            if cv and lv and cv != lv and not (what == 'widget' and 'unknown' in (cv, lv)):
                diffs.append({'what': f"field '{lab}' {what}", 'config': cv, 'live': lv, 'env': pv.get('env'), 'date': pv.get('date'),
                              'ref': pv.get('ref'), 'status': 'open'})
    for lab, fact in label_only:
        pv = fact['provenance']
        diffs.append({'what': f"field '{lab}' element (same label, other control)", 'config': config[lab]['element'], 'live': fact['element'],
                      'env': pv.get('env'), 'date': pv.get('date'), 'ref': pv.get('ref'), 'status': 'open',
                      'note': 'Matched by label only: a popup/grid control with the same caption, or a renamed id. The configured element is kept; the live id is in alt_elements.'})
    if clean_label(m['title']) != title:
        diffs.append({'what': 'menu title', 'config': clean_label(m['title']), 'live': title, 'env': None, 'date': None,
                      'ref': 'knowledge/env/*/menu.*.json', 'status': 'open'})
    old = {(d.get('what'), d.get('env')): d for d in existing.get('differences') or []}
    for d in diffs:
        o = old.pop((d['what'], d['env']), None)
        if o:
            d['status'] = o.get('status', 'open')
            if o.get('note'):
                d['note'] = o['note']
    diffs += [d for d in old.values() if d.get('status') != 'open' or d.get('note')]      # hand-written entries stay
    doc['differences'] = sorted(diffs, key=lambda d: (d['what'], d.get('env') or ''))

    # finish fields: seen_in, drop empties
    for lab, f in doc['fields'].items():
        s = sorted(set(seen.get(lab) or []))
        if s:
            f['seen_in'] = s
        for k in [k for k, v in f.items() if v is None and k not in ('element', 'required', 'readonly')]:
            f.pop(k)
        if f.get('widget') is None:
            f['widget'] = 'unknown'
    for b in doc['buttons'].values():
        if 'seen_in' in b:
            b['seen_in'] = sorted(set(b['seen_in']))
        for k in [k for k, v in b.items() if v is None and k != 'element']:
            b.pop(k)
    for g in doc['grids'].values():
        for k in [k for k, v in g.items() if v is None]:
            g.pop(k)
    doc['tabs'] = tabs
    if not doc['panels']:
        doc.pop('panels')

    # business page, trained
    pg = sorted(ctx.pages.get(key, []), key=lambda x: (x[0], x[1]))
    doc['business_page'] = pg[0][1] if pg else None
    if len(pg) > 1:
        doc['business_pages_also'] = sorted({p[1] for p in pg[1:]} - {pg[0][1]})
    how, tdates = [], []
    if pg:
        how.append('business page')
        tdates += [p[2] for p in pg if p[2]]
    for gid in sorted(ctx.walks.get(key, [])):
        how.append(WALK_GROUPS[gid])
        tdates.append(ctx.walk_dates.get(gid))
    for st in sorted(rec_L['stories']):
        how.append(f'run {st}')
    tdates += list(rec_L['dates'])
    if any(r.endswith('.json') and '/LIVE_' in r for r in obs_L['refs']):
        how.append('live read-only look')
    prev_trained = existing.get('trained') if isinstance(existing.get('trained'), dict) else {}
    if existing.get('observations') or legacy_prov or 'curated live look' in (prev_trained.get('how') or []):
        how.append('curated live look')
        tdates += [lp['date'] or prev_trained.get('date')]
    tdates = [d for d in tdates if d]
    doc['trained'] = {'status': bool(how), 'date': max(tdates) if tdates else None, 'how': how}
    sources['stated'] = sorted({s for s in sources['stated'] if s})
    doc['sources'] = sources
    all_dates = [d for d in list(dates) + tdates + [l.get('date') for l in doc['lessons']] + [x.get('date') for x in doc['differences']] if d]
    doc['updated'] = max(all_dates) if all_dates else None
    validate(doc)
    return doc


_validator = None


def validate(doc):
    global _validator
    try:
        import jsonschema
    except ImportError:                                                       # minimal check without the library
        for k in load(SCHEMA)['required']:
            if k not in doc:
                raise SystemExit(f"{doc.get('option_id')}: missing {k}")
        return
    if _validator is None:
        _validator = jsonschema.Draft202012Validator(load(SCHEMA))
    errs = sorted(_validator.iter_errors(doc), key=lambda e: list(e.path))
    if errs:
        raise SystemExit(f"{doc['option_id']}: schema errors:\n" + '\n'.join(f"  {'/'.join(map(str, e.path))}: {e.message}" for e in errs[:20]))


def write(doc):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, f"{doc['option_id']}.json")
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(doc, f, indent=1, ensure_ascii=False)
        f.write('\n')
    return p


def index_entry(ctx, doc):
    fields = doc['fields'].values()
    live = [f for f in fields if f.get('locator')]
    gaps = []
    if not doc.get('business_page'):
        gaps.append('no business page')
    if not live and not any(b.get('locator') for b in doc['buttons'].values()):
        gaps.append('no live ids yet')
    elif len(live) < len(doc['fields']):
        gaps.append(f'{len(doc["fields"]) - len(live)} of {len(doc["fields"])} fields without a live id')
    if not doc['fields']:
        gaps.append('no fields known')
    if not doc['sources'].get('db') and doc['kind'] == 'dynamic':
        gaps.append('no config in screens_db')
    if not doc['menu'].get('top_id'):
        gaps.append('menu top_id unknown (not in a harvested live menu)')
    open_d = [d for d in doc['differences'] if d['status'] == 'open']
    if open_d:
        gaps.append(f'{len(open_d)} open config-vs-live difference(s)')
    used = [k for k in ('db', 'observed', 'recorded', 'stated') if doc['sources'].get(k)]
    return {'option_id': doc['option_id'], 'title': doc['title'], 'path': ' > '.join(doc['menu']['path']), 'kind': doc['kind'],
            'business_page': doc.get('business_page'), 'trained': doc['trained']['status'], 'trained_how': doc['trained']['how'],
            'file': f"{doc['option_id']}.json", 'n_fields': len(doc['fields']), 'n_live_fields': len(live),
            'n_buttons': len(doc['buttons']), 'n_grids': len(doc['grids']), 'n_lessons': len(doc['lessons']),
            'n_differences': len(doc['differences']), 'sources': used, 'gaps': gaps, 'updated': doc.get('updated')}


def write_index(ctx, docs):
    entries = sorted((index_entry(ctx, d) for d in docs), key=lambda e: e['option_id'])
    idx = {'app': 'snd', 'schema': 'plugins/qa-os/schemas/screen.schema.json',
           'note': 'One screen file per trained screen (business page, group 11/66 walk, or a run recording). Built by tools/build_screen_file.py --all-trained.',
           'env_filter': ctx.env, 'updated': max([e['updated'] for e in entries if e['updated']] or [None]),
           'count': len(entries), 'screens': entries,
           'unresolved_business_page_screens': [{'page': p, 'name': n} for p, n in ctx.unresolved_pages]}
    with open(os.path.join(OUT, '_index.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(idx, f, indent=1, ensure_ascii=False)
        f.write('\n')
    return idx


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('screen', nargs='*', help='option id or menu title')
    ap.add_argument('--all-trained', action='store_true')
    ap.add_argument('--list-trained', action='store_true')
    ap.add_argument('--env', help='use live sources of this environment only')
    ap.add_argument('--stdout', action='store_true', help='print instead of writing the file')
    a = ap.parse_args(argv)
    ctx = Context(a.env)
    if a.list_trained:
        for k in ctx.trained():
            print(k, '|', ctx.menu.by_gid[k]['title'])
        return 0
    targets = ctx.trained() if a.all_trained else a.screen
    if not targets:
        ap.error('give a screen or --all-trained')
    docs = []
    for t in targets:
        d = build(ctx, t)
        docs.append(d)
        if a.stdout:
            print(json.dumps(d, indent=1, ensure_ascii=False))
        else:
            write(d)
            print(f"{d['option_id']}: {len(d['fields'])} fields ({sum(1 for f in d['fields'].values() if f.get('locator'))} live), "
                  f"{len(d['buttons'])} buttons, {len(d['grids'])} grids, {len(d['lessons'])} lessons, {len(d['differences'])} differences")
    if a.all_trained and not a.stdout:
        idx = write_index(ctx, docs)
        print(f"_index.json: {idx['count']} screens")
    return 0


if __name__ == '__main__':
    sys.exit(main())
