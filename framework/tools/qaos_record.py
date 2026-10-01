"""QA OS recorder: action log (from plugins/qa-os/runtime/qaos_helpers.js) + metadata  ->  flow_spec.json

    python framework/tools/qaos_record.py <recording.json> <flow_spec.json>

recording.json = { "meta": {...}, "log": [ {act: text|pick|click|toast|nav|tab, ...}, ... ] }
meta carries what a browser cannot know: story key, tag, framework ids, menu-group navigation, case-data rows,
locators for controls that have no element id (label -> xpath), and evidence text.

Mapping (matches the legacy CTA_CONFIG_ASSERTION conventions in framework/cta_config_assertion.md):
  text  -> field, component 0001     pick -> field, component 0002     date -> field, 0003
  click -> event 0004/0002 (button click) on the button id
  toast after a click -> event 0000/0013 assertion TSTMSG referencing that click
  a Load Data event 0000/0001 is always serial 1.
Nothing is applied anywhere; the output goes to framework/tools/gen_framework_sql.py for review.
"""
import json, sys

rec = json.load(open(sys.argv[1], encoding='utf-8'))
meta, log = rec['meta'], rec['log']
loc = meta.get('locators', {})          # label -> {"locateby": "xpath", "id": "<xpath>"} for id-less controls
ev = meta.get('evidence', {})           # label/target -> evidence text
KIND = {'text': '0001', 'pick': '0002', 'date': '0003'}

fields, events, seen = [], [{'serial': 1, 'desc': 'Load Data', 'type': '0000', 'event': '0001',
                             'evidence': 'same as every DYL flow (Vehicle Color 004901)'}], set()
last_click = None
for a in log:
    act = a.get('act')
    if act in KIND and a.get('label') not in seen:
        seen.add(a['label'])
        l = loc.get(a['label'], {})
        fid = l.get('id') or a.get('id')
        if not fid:
            raise SystemExit(f"no id or locator for field '{a['label']}': add it to meta.locators")
        fields.append({'id': fid, 'caption': a['label'], 'type': KIND[act], 'mandatory': meta.get('mandatory', {}).get(a['label']),
                       'locateby': l.get('locateby', 'id'),
                       'evidence': ev.get(a['label'], f"recorded: {act} '{a.get('value', '')}' ({a.get('widget', '')})")})
    elif act == 'click':
        n = len(events) + 1
        events.append({'serial': n, 'desc': (a.get('text') or a.get('target')) + ' Button', 'type': '0004', 'event': '0002', 'locateby': 'id',
                       'field': a.get('id') or a['target'], 'ref': 1, 'evidence': ev.get(a['target'], f"recorded click on #{a.get('id') or a['target']}")})
        last_click = n
    elif act == 'toast' and a.get('messages') and last_click:
        n = len(events) + 1
        events.append({'serial': n, 'desc': 'Assertion', 'type': '0000', 'event': '0013', 'fixed': 'TSTMSG', 'ref': last_click,
                       'evidence': f"toast after {a['after']}: {a['messages'][0]!r}"})

spec = {k: meta[k] for k in ('story', 'master_app_id', 'tag', 'menu_group', 'screen', 'flow', 'casedata', 'not_covered', 'risks') if k in meta}
spec['fields'], spec['events'] = fields, events
json.dump(spec, open(sys.argv[2], 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print(f'{len(fields)} fields, {len(events)} events -> {sys.argv[2]}')
