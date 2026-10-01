"""app-cartographer v1, static harvest: S&D dynamic screens from DB metadata -> knowledge/screens_db/<option_id>.json

Chain: menu option DYL_<code> (smm_pr_opg_optiongroups + smm_pr_apo_appoption, layoutCode=<code>)
       -> layout <code> (dyp_dp_pgl_pagelayout.dpgl_layoutjson: pagePanel.appOption = DYP_<pagecode>__)
       -> page <pagecode> (dyp_dp_pgm_pagemeta: backing table)
       -> controls (dyp_dp_pgc_pageconfiguration.dpgc_configjson)

Inputs (knowledge/): snd_menu_flat.json, raw/page_layouts.json, raw/page_config_offset*.json,
                     optional env/<env>/i18n.en.json (label text; harvested live by the player), snd_tables.json.
Every fact is provenance "db-declared"; live observation (screens/<option_id>.json) takes precedence.
"""
import collections, glob, json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
K = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'knowledge')
OUT = os.path.join(K, 'screens_db')

fix = lambda s: json.loads(re.sub(r',\s*([}\]])', r'\1', s)) if s else None   # SQL-side noise stripping left trailing commas

# ---- inputs
menu = json.load(open(os.path.join(K, 'snd_menu_flat.json'), encoding='utf-8'))
layouts = {r['code']: r for r in json.load(open(os.path.join(K, 'raw', 'page_layouts.json'), encoding='utf-8'))['result']}
pages = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(K, 'raw', 'page_config_offset*.json'))):
    for r in json.load(open(f, encoding='utf-8'))['result']:
        pages[r['pc']].append(r)
i18n = {}
for f in glob.glob(os.path.join(K, 'env', '*', 'i18n.en.json')):
    def flat(o, pre=''):
        for k, v in o.items():
            if isinstance(v, dict):
                flat(v, pre + k + '.')
            else:
                i18n.setdefault(pre + k, v)
    flat(json.load(open(f, encoding='utf-8')))
tables = json.load(open(os.path.join(K, 'snd_tables.json'), encoding='utf-8'))['tables']
col_desc = {}
for t, e in tables.items():
    for c in e['columns']:
        col_desc.setdefault(c['name'].upper(), c['description'])


def caption(key):
    """Resolve an i18n key; else humanise its tail. Returns (text, source)."""
    if not key:
        return None, None
    if key in i18n:
        return i18n[key], 'i18n'
    tail = re.split(r'\.+', key)[-1]
    tail = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', tail).replace('_', ' ').strip()
    return tail[:1].upper() + tail[1:], 'key'


WIDGET = {'textBox': 'text', 'textArea': 'text', 'selectBox': 'select', 'datePicker': 'date', 'switch': 'switch',
          'hiddenField': 'hidden', 'availableAllowableCol': 'allowable'}


def page_controls(pc):
    """Fields, grid columns and buttons declared for one page."""
    fields, grids, buttons = {}, {}, []
    for r in pages.get(pc, []):
        cfg = fix(r['cfg'])
        if not isinstance(cfg, dict):
            continue

        state = {'label': None}                              # most recent label in the current form row

        def walk(o, row_label=None, grid=None):
            if isinstance(o, list):
                for x in o:
                    walk(x, None, grid)
                return None
            if not isinstance(o, dict):
                return None
            code = o.get('_code')
            if code == 'dataFormRow':
                state['label'] = None
            if code == 'label':
                state['label'] = caption(o.get('text'))[0]
                return None
            row_label, state_used = state['label'], code in WIDGET
            if state_used:
                state['label'] = None
            if code == 'dataGrid':
                title, _ = caption(o.get('title'))
                grids[title or o.get('id')] = {'columns': [], 'edit_mode': o.get('editMode'), 'selection': o.get('selectionMode')}
                walk(o.get('columns'), None, title or o.get('id'))
                return None
            if code == 'dataGridCol':
                cap, _ = caption(o.get('caption'))
                if grid is not None and o.get('visible', True) and cap:
                    grids[grid]['columns'].append(cap)
                return None
            if code == 'recordButtons':
                buttons.extend(b for k, b in (('newButton', 'New'), ('saveButton', 'Save'), ('updateButton', 'Update'),
                                               ('deleteButton', 'Delete')) if o.get(k))
                return None
            if code == 'button':
                buttons.append(caption(o.get('label'))[0] or o.get('name'))
                return None
            if code in WIDGET and o.get('dataField'):
                df = o['dataField'].split('.')[-1].upper()
                label = row_label or (caption(o.get('caption'))[0] if o.get('caption', '').startswith('DYP') else None) \
                    or col_desc.get(df) or df
                if WIDGET[code] != 'hidden':
                    fields[label] = {
                        'name': o.get('name'), 'id': o.get('id'), 'widget': WIDGET[code], 'data_field': df,
                        'db_description': col_desc.get(df),
                        'required': bool(o.get('isRequired')), 'editable': o.get('isEditable', True),
                        'readonly': bool(o.get('readOnly')), 'primary': bool(o.get('isPrimary')),
                        'max_length': o.get('maxLength'), 'type': o.get('type'),
                        'default': o.get('defaultValue'), 'data_list_id': o.get('dataListId'),
                        'validations': o.get('fieldValidations') or None, 'regex': o.get('validationRegEx') or None,
                        'page': pc}
                return None
            for k, v in o.items():
                if isinstance(v, (dict, list)):
                    walk(v, None, grid)
            return None
        walk(cfg.get('components', []))
        walk(cfg.get('footerComponents', []))
    return fields, grids, buttons


def layout_panels(code):
    lay = layouts.get(code)
    if not lay or not lay.get('lj'):
        return []
    out = []

    def walk(o, tab=None):
        if isinstance(o, list):
            for x in o:
                walk(x, tab)
        elif isinstance(o, dict):
            if o.get('_code') == 'tab':
                tab = caption(o.get('title'))[0]
            if o.get('_code') == 'pagePanel' and o.get('appOption'):
                m = re.match(r'DYP_(.+?)_*$', o['appOption'])
                out.append({'page': m.group(1) if m else o['appOption'], 'tab': tab, 'is_child': o.get('isChild'),
                            'parent': (re.match(r'DYP_(.+?)_*$', o.get('parentAppOption') or '') or [None, None])[1],
                            'partial': (re.match(r'DYP_(.+?)_*$', o.get('partialAppOption') or '') or [None, None])[1]})
            for v in o.values():
                if isinstance(v, (dict, list)):
                    walk(v, tab)
    walk(fix(lay['lj']))
    return out


# ---- build
os.makedirs(OUT, exist_ok=True)
page_meta = {}
for pc, rs in pages.items():
    r = rs[0]
    tbl = (r.get('tbl') or '').split()
    page_meta[pc] = {'desc': r.get('pdesc'), 'table': tbl[0] if tbl else None, 'type': r.get('pt')}

index, stats = [], collections.Counter()
for m in menu:
    opt = m.get('option_id') or ''
    code = None
    if m.get('page_param') and 'layoutCode=' in m['page_param']:
        code = m['page_param'].split('layoutCode=')[1].split('&')[0]
    elif opt.startswith('DYL_'):
        code = opt[4:]
    if not code:
        continue
    stats['dyl_options'] += 1
    panels = layout_panels(code)
    if not panels:
        stats['no_layout'] += 1
    screen = {'option_id': opt, 'title': m['title'], 'menu': {'path': m['path'].split(' > '), 'group_id': m['group_id']},
              'route': m.get('route'), 'layout_code': code, 'kind': 'dynamic',
              'provenance': {'source': 'db-declared', 'db': 'snd-schema (ng_astrone)'},
              'panels': [], 'fields': {}, 'grids': {}, 'buttons': []}
    for p in panels:
        f, g, b = page_controls(p['page'])
        meta = page_meta.get(p['page'], {})
        screen['panels'].append({**p, 'desc': meta.get('desc'), 'table': meta.get('table'), 'n_fields': len(f), 'grids': list(g)})
        for k, v in f.items():
            prev = screen['fields'].get(k)
            if prev and prev['name'] != v['name']:           # same label on another panel: keep both
                k = f"{k} [{p['tab'] or meta.get('desc') or p['page']}]"
            screen['fields'].setdefault(k, v)
        screen['grids'].update(g)
        screen['buttons'] += [x for x in b if x not in screen['buttons']]
    stats['fields'] += len(screen['fields'])
    json.dump(screen, open(os.path.join(OUT, f'{opt}.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    index.append({'option_id': opt, 'title': m['title'], 'path': m['path'], 'layout': code, 'panels': len(panels),
                  'fields': len(screen['fields']), 'required': sum(1 for v in screen['fields'].values() if v['required']),
                  'grids': len(screen['grids']), 'tables': sorted({p.get('table') for p in screen['panels'] if p.get('table')})})
json.dump(index, open(os.path.join(OUT, '_index.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(f"dynamic options: {stats['dyl_options']}  without layout: {stats['no_layout']}  fields: {stats['fields']}  "
      f"i18n keys loaded: {len(i18n)}  -> {os.path.relpath(OUT)}")
