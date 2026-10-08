"""QA OS recorder: action log (from plugins/qa-os/runtime/qaos_helpers.js) + metadata  ->  flow_spec.json

    python framework/tools/qaos_record.py <recording.json> <flow_spec.json>

recording.json = { "meta": {...}, "log": [ {act: ...}, ... ] }
The log holds two kinds of entries:
  * helper actions (qaos.text / pick / click / clickCapture / tab / open), and
  * passive watcher entries (src: 'watch', 2026-10-08) for REAL Selenium typing and clicks:
      text | cell | option | click | tab | check | toast | popup | alert | alert_result | screen
meta carries what a browser cannot know: story key, tag, framework ids, menu-group navigation, case-data rows,
locators for controls that have no element id (label -> xpath), and evidence text.

Mapping (CTA_CONFIG_ASSERTION conventions, framework/cta_config_assertion.md and skill framework-conventions):
  text/cell (text widget) -> field 0001   option or pick or type-ahead/dropdown cell -> field 0002   date -> field 0003
  click / tab / popup button -> event 0004/0002 on the element id (or xpath)
  check (grid checkbox) -> event 0000/0015
  toast after a click  -> group assertion 0000/0014 'TSTMSG,<NAME>_ASSR' referencing the click (+ assertion sheet name)
  popup                -> assertion 0000/0014 'ELEVAL,<NAME>_ASSR' on the popup's message element
  alert                -> event 0005/0002, field 'accept' or 'dismiss' (the engine cannot assert alert text:
                          the text goes to spec['not_asserted'])
  a Load Data event 0000/0001 is always serial 1.
The recording is the ONLY source of screens, elements, ids, tabs and messages (QA lead rule 2026-10-08);
nothing is borrowed from existing flows. Nothing is applied anywhere; the output goes to gen_framework_sql.py.
"""
import json, re, sys

rec = json.load(open(sys.argv[1], encoding='utf-8'))
meta, log = rec['meta'], rec['log']
loc = meta.get('locators', {})          # label -> {"locateby": "xpath", "id": "<xpath>"} for id-less controls
ev = meta.get('evidence', {})           # label/target -> evidence text
KIND = {'text': '0001', 'pick': '0002', 'date': '0003', 'option': '0002'}
WIDGET_KIND = {'dropdown': '0002', 'type-ahead': '0002', 'date': '0003'}


def locate(entry, label=None):
    """(locateby, id) from the recorded element: id first, else xpath; css-like locators are a gap."""
    l = loc.get(label or entry.get('label') or '', {})
    if l.get('id'):
        return l.get('locateby', 'id'), l['id']
    if entry.get('id'):
        return 'id', entry['id']
    lc = entry.get('locator') or ''
    if lc.startswith('#'):
        return 'id', lc[1:]
    if lc.startswith('//'):
        return 'xpath', lc
    return None, None


def sheet_name(text):
    return re.sub(r'[^A-Z0-9]+', '_', (text or 'MSG').upper()).strip('_')[:20] + '_ASSR'


fields, events, seen = [], [{'serial': 1, 'desc': 'Load Data', 'type': '0000', 'event': '0001',
                             'evidence': 'Load Data is always serial 1'}], set()
gaps, not_asserted, assertion_sheets, screens, navs = [], [], [], [], []
last_click, last_click_text = None, ''


def add_event(**e):
    e['serial'] = len(events) + 1
    e.setdefault('ref', 1)
    events.append(e)
    return e['serial']


for a in log:
    act = a.get('act')
    if act == 'nav_click':
        spec_nav = {'text': a.get('value'), 'id': a.get('id'), 'locator': a.get('locator'), 'search': a.get('search')}
        navs.append(spec_nav)
        continue
    if act == 'screen':
        screens.append({k: a.get(k) for k in ('url', 'title', 'crumb')})
        continue
    if act in ('text', 'pick', 'date', 'option', 'cell'):
        label = a.get('label') or a.get('column') or ''
        key = (label, a.get('grid') or '')
        if not label:
            gaps.append(f"{act} '{a.get('value', '')}' has no label/owner field: add meta.locators or re-record")
            continue
        if key in seen:
            continue
        seen.add(key)
        kind = KIND.get(act) or WIDGET_KIND.get(a.get('widget', ''), '0001')
        if act in ('text', 'cell') and a.get('widget') in WIDGET_KIND:
            kind = WIDGET_KIND[a['widget']]
        by, fid = locate(a, label)
        if not fid:
            gaps.append(f"no id or locator for field '{label}': add it to meta.locators or re-record")
            continue
        f = {'id': fid, 'caption': label, 'type': kind, 'mandatory': meta.get('mandatory', {}).get(label),
             'locateby': by, 'evidence': ev.get(label, f"recorded: {act} '{a.get('value', '')}' ({a.get('widget', '')})")}
        if a.get('grid'):
            f.update({'grid': a['grid'], 'column': a.get('column'), 'rowindex': a.get('rowindex')})
        fields.append(f)
    elif act in ('click', 'tab'):
        by, fid = locate(a)
        if not fid:
            gaps.append(f"no id or locator for {act} '{a.get('text') or a.get('value')}'")
            continue
        name = a.get('text') or a.get('value') or a.get('target') or fid
        if a.get('grid') and any(e.get('field') == fid and e.get('grid') == a['grid'] for e in events):
            last_click, last_click_text = next(e['serial'] for e in events if e.get('field') == fid), name
            continue   # same row button for the next line: one event, repeated per case-data row
        last_click = add_event(grid=a.get('grid'), desc=(f"{name} Tab" if act == 'tab' else f"{name} Button"), type='0004', event='0002',
                               locateby=by, field=fid,
                               evidence=ev.get(name, f"recorded {act} on {a.get('locator') or fid}" + (f" (controls {a['controls']})" if a.get('controls') else '')))
        last_click_text = name
    elif act == 'check':
        by, fid = locate(a)
        if fid:
            add_event(desc=f"{a.get('label') or 'Row'} Checkbox", type='0000', event='0015', locateby=by, field=fid,
                      evidence=f"recorded checkbox click (grid {a.get('grid')}, row {a.get('rowindex')})")
        else:
            gaps.append('checkbox without id/locator')
    elif act == 'toast' and a.get('messages'):
        msg = a['messages'][0]
        if any(x['expected_message'] == msg and x.get('click') != last_click for x in assertion_sheets):
            not_asserted.append({'type': 'toast', 'text': msg, 'reason': f'repeat of an earlier message shown again after {last_click_text}'})
            continue
        if not last_click:
            gaps.append(f"toast {a['messages'][0]!r} without a preceding click")
            continue
        sh = sheet_name(last_click_text)
        add_event(desc=f"Assertion {a['messages'][0]}", type='0000', event='0014', fixed=f'TSTMSG,{sh}',
                  evidence=f"toast after {last_click_text}: {a['messages'][0]!r} ({a.get('type', '')})")
        assertion_sheets.append({'sheet': sh, 'kind': 'TSTMSG', 'expected_message': a['messages'][0], 'click': last_click})
    elif act == 'popup':
        if not a.get('title') and not a.get('buttons'):
            continue   # a dropdown option list or picker overlay, not a message (no title, no buttons)
        by, fid = locate(a)
        sh = sheet_name('POPUP ' + (a.get('title') or ''))
        if fid:
            add_event(desc=f"Popup check {a.get('title') or ''}".strip(), type='0000', event='0014', fixed=f'ELEVAL,{sh}',
                      locateby=by, field=fid, evidence=f"popup: {a.get('text')!r}")
            assertion_sheets.append({'sheet': sh, 'kind': 'ELEVAL', 'expected_message': a.get('text')})
        else:
            gaps.append(f"popup {a.get('text')!r} has no locator for its message element")
    elif act == 'alert':
        not_asserted.append({'type': 'alert', 'dialog': a.get('dialog'), 'text': a.get('text'),
                             'reason': 'the engine (Main.java Click Alert) reads but does not assert alert text'})
    elif act == 'alert_result':
        add_event(desc=f"{a.get('dialog', 'alert').title()} Alert", type='0005', event='0002', locateby='id',
                  field='accept' if a.get('result') else 'dismiss', evidence=f"browser {a.get('dialog')} answered {a.get('result')}")

spec = {k: meta[k] for k in ('story', 'master_app_id', 'tag', 'menu_group', 'screen', 'flow', 'casedata', 'not_covered', 'risks') if k in meta}
spec['fields'], spec['events'] = fields, events
spec['assertion_sheets'] = assertion_sheets
spec['screens_seen'] = screens
spec['navigation'] = navs   # sidebar entries clicked (menu navigation of the flow)
spec['not_asserted'] = not_asserted
spec['gaps'] = gaps
json.dump(spec, open(sys.argv[2], 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print(f'{len(fields)} fields, {len(events)} events, {len(assertion_sheets)} assertion sheets, '
      f'{len(screens)} screens, {len(gaps)} gaps -> {sys.argv[2]}')
if gaps:
    print('GAPS (re-record or add meta.locators):'); [print('  -', g) for g in gaps]
