"""script-generator (v1): flow spec -> CTA_CONFIG_ASSERTION SQL + rollback + case-data workbook + review sheet.

  python framework/tools/gen_framework_sql.py <spec.json> <out_dir>

Spec (JSON): story, master_app_id (default NULL), tag, source,
             menu_group{id,description,searchtext,navigation,navigation_type,evidence},
             flow{id,description,test_type,filename},
             screens[{id,name,type,url,seq,parent,
                      fields[{id,caption,type,mandatory,locateby,repoid,evidence}],
                      events[{serial,desc,type,event,locateby,field,fixed,fixedvalue_type,ref,evidence}]}],
             assertion_sheets[{sheet,kind,expected_message,...}] (optional, for the review and skeleton sheets),
             casedata{sheets[{sheet, columns[...], rows[[...]]}]}  (optional; missing sheets are written header-only),
             not_covered[], risks[], not_asserted[], gaps[]
  A one-screen spec in the old shape (top-level screen{id,name,type}, fields[], events[], casedata{sheet,columns,rows})
  is still accepted and treated as screens = [screen].

Events: `ref` = the serial of the screen's Load Data event (0000/0001) makes the event a child (runs once per case-data
row); ref NULL makes it top level (runs once after all rows). A ref to anything other than a Load Data event is rejected
(the engine never runs it). mgsm order = screen `seq` (default: position in the list).

Rules (framework/cta_config_assertion.md, skill framework-conventions):
 - prv_version '1.0' (NOT NULL); psf_field_addition '+'; psf_iteration_number 1; psef_serialno of fields comes from a sequence.
 - created_by = <tag> on every row (used by the rollback); modified_date / modified_by NULL, as the framework UI writes.
 - values are trimmed and '' is stored as NULL; psef_desc must not be empty; assertion values are TSTMSG/ELEVAL/ELEVLD
   (0013) or <kind>,<Sheet> (0014); sheet names <= 31 chars and screen sheets = psc_screenname.
 - flow file name goes in fct_pr_tfd_test_flow_details.ptfd_filename; mgsm filename stays NULL.
Never applies anything: the output is for human review.
"""
import json, os, re, sys, datetime as dt

# columns that exist in the live tables (checked 2026-09-25) — the generator refuses anything else
COLS = {
 'fct_pr_mg_menu_group': 'pmg_menugroupid pmg_description pmg_searchtext pmg_navigation create_date created_by modified_date modified_by pmg_navigation_type master_app_id',
 'fct_pr_mgsm_menu_group_screen_mapping': 'pmg_menugroupid psc_screenid pmgsm_sequenceno pmgsm_navigation_type pmgsm_navigation_path create_date created_by modified_date modified_by pmgsm_parent_screenid pmgsm_screen_filename_status pmgsm_screen_filename pmgsm_status',
 'fct_pr_sc_screens': 'psc_screenid psc_screenname psc_screentype create_date created_by modified_date modified_by psc_screen_filename_status psc_screen_filename master_app_id',
 'fct_pr_sf_screen_field': 'psc_screenid psf_fieldid prv_version psf_locateby psf_field_db_column pcmpt_componenttypeid psf_field_addition psf_fixed_value create_date created_by modified_date modified_by psf_sequenceno psef_field_waitingtime psf_subfieldid psf_field_status psf_mandatory_field psf_repoid psf_field_source psf_check_assertion psf_assertion_type psf_app_ids psef_serialno psf_iteration_number psf_extra_config',
 'fct_pr_sef_screen_events_flow': 'psc_screenid psef_serialno pcmpt_componenttypeid pce_comp_event psef_locateby psef_fieldid psef_fixed_value psef_sequenceno psef_status create_date created_by modified_date modified_by psef_ref_serialno psef_desc psef_fixedvalue_type psef_mandatory_validation psef_validationtype psef_condition_statement',
 'fct_pr_tf_test_flow': 'ptf_testflowid ptf_description ptf_status ptt_testtypeid create_date created_by modified_date modified_by ptf_platform master_app_id',
 'fct_pr_tfd_test_flow_details': 'ptf_testflowid pmg_menugroupid ptfd_sequenceno create_date created_by modified_date modified_by ptfd_filename',
}
COLS = {t: set(c.split()) for t, c in COLS.items()}
LIMITS = {('fct_pr_sc_screens', 'psc_screenname'): 50, ('fct_pr_sf_screen_field', 'psf_field_db_column'): 50,
          ('fct_pr_tf_test_flow', 'ptf_description'): 100, ('fct_pr_mg_menu_group', 'pmg_description'): 100,
          ('fct_pr_sef_screen_events_flow', 'psef_desc'): 100, ('fct_pr_sef_screen_events_flow', 'psef_fixed_value'): 200}
SCREEN_CONTROLS = ['PK', 'PK_DESC', 'CASE_TYPE', 'STPONERR']
ASSR_CONTROLS = ['PK', 'CASE_TYPE', 'EXPECTED_MESSAGE']
READABLE = '0010'   # repository-sourced / readable field: never filled, so no case-data column
NOW = object()      # marker for now()


def fail(msg):
    raise SystemExit(f'gen_framework_sql: {msg}')


def q(v):
    if v is NOW:
        return 'now()'
    if v is None:
        return 'NULL'
    if isinstance(v, int) and not isinstance(v, bool):
        return str(v)
    v = str(v).strip()
    return 'NULL' if v == '' else "'" + v.replace("'", "''") + "'"


def insert(table, row):
    bad = set(row) - COLS[table]
    if bad:
        fail(f'{table}: unknown column(s) {bad}')
    for (t, c), n in LIMITS.items():
        if t == table and row.get(c) not in (None, NOW) and len(str(row[c]).strip()) > n:
            fail(f'{table}.{c} too long ({len(str(row[c]).strip())} > {n}): {row[c]}')
    cols = list(row)
    return f"INSERT INTO {table} ({', '.join(cols)})\nVALUES ({', '.join(q(row[c]) for c in cols)});"


def normalise(spec):
    """Old one-screen shape -> screens[]; returns the screens list with seq filled."""
    if 'screens' not in spec:
        sc = dict(spec['screen'], fields=spec.get('fields', []), events=spec.get('events', []))
        spec['screens'] = [sc]
        cd = spec.get('casedata')
        if cd and 'sheet' in cd:
            spec['casedata'] = {'sheets': [cd]}
    if not isinstance(spec['screens'], list) or not all(isinstance(sc, dict) and 'fields' in sc and 'events' in sc for sc in spec['screens']):
        fail('spec.screens must be a list of {id, name, fields[], events[]} (see the docstring)')
    for i, sc in enumerate(spec['screens'], 1):
        sc.setdefault('seq', i)
    return spec['screens']


def check(spec, screens):
    """Rules the engine enforces silently; stop before writing anything."""
    ids = [sc['id'] for sc in screens]
    if len(set(ids)) != len(ids):
        fail(f'duplicate screen ids {ids}')
    if len({sc['seq'] for sc in screens}) != len(screens):
        fail('duplicate screen seq (mgsm order)')
    for sc in screens:
        name = (sc.get('name') or '').strip()
        if not name or len(name) > 31:
            fail(f"screen {sc['id']}: name must be 1-31 chars (it is the case-data sheet name): {name!r}")
        serials = [e['serial'] for e in sc['events']]
        if len(set(serials)) != len(serials):
            fail(f"screen {sc['id']}: duplicate event serials {serials}")
        loads = {e['serial'] for e in sc['events'] if (e['type'], e['event']) == ('0000', '0001')}
        for e in sc['events']:
            where = f"screen {sc['id']} event {e['serial']}"
            if not (e.get('desc') or '').strip():
                fail(f'{where}: psef_desc is empty (one NULL desc breaks every later event)')
            if e.get('ref') is not None and e['ref'] not in loads:
                fail(f"{where}: ref {e['ref']} is not a Load Data (0000/0001) event of this screen; the engine never runs it")
            fx = (e.get('fixed') or '').strip()
            if (e['type'], e['event']) == ('0000', '0013') and fx.split(',')[0] not in ('TSTMSG', 'ELEVAL', 'ELEVLD'):
                fail(f'{where}: 0000/0013 needs TSTMSG, ELEVAL or ELEVLD, got {fx!r}')
            if (e['type'], e['event']) == ('0000', '0014') and not re.fullmatch(r'(TSTMSG|ELEVAL|ELEVLD),\S.*', fx):
                fail(f'{where}: 0000/0014 needs <TSTMSG|ELEVAL|ELEVLD>,<Sheet>, got {fx!r}')
        for f in sc['fields']:
            if f.get('mandatory') not in (None, 'Y'):
                fail(f"screen {sc['id']} field {f['id']}: psf_mandatory_field must be 'Y' or NULL")


def assertion_sheets(screens):
    """Sheet names referenced by assertion events, in event order: {sheet: (screen id, serial, kind)}."""
    out = {}
    for sc in screens:
        for e in sc['events']:
            fx = (e.get('fixed') or '').strip()
            if (e['type'], e['event']) in (('0000', '0013'), ('0000', '0014')) and ',' in fx:
                kind, sheet = (x.strip() for x in fx.split(',', 1))
                out.setdefault(sheet, (sc['id'], e['serial'], kind))
    return out


def build(spec):
    """-> (framework.sql text, rollback text, counts). Pure function of the spec."""
    screens = normalise(spec)
    check(spec, screens)
    tag, mapp = spec['tag'], spec.get('master_app_id')
    mg, fl = spec['menu_group'], spec['flow']
    audit = {'create_date': NOW, 'created_by': tag, 'modified_date': None, 'modified_by': None}
    stmts = [insert('fct_pr_mg_menu_group', {'pmg_menugroupid': mg['id'], 'pmg_description': mg['description'], 'pmg_searchtext': mg['searchtext'],
                                             'pmg_navigation': mg['navigation'], 'pmg_navigation_type': mg.get('navigation_type', 'id'),
                                             'master_app_id': mapp, **audit})]
    n_sf = n_sef = 0
    for sc in sorted(screens, key=lambda s: s['seq']):
        stmts.append(f"-- screen {sc['id']} {sc['name']}" + (f" ({sc['url']})" if sc.get('url') else ''))
        stmts.append(insert('fct_pr_sc_screens', {'psc_screenid': sc['id'], 'psc_screenname': sc['name'], 'psc_screentype': sc.get('type', 'Save'),
                                                  'master_app_id': mapp, **audit}))
        mgsm = {'pmg_menugroupid': mg['id'], 'psc_screenid': sc['id'], 'pmgsm_sequenceno': sc['seq'], 'pmgsm_status': 'Y'}
        if sc.get('parent'):
            mgsm['pmgsm_parent_screenid'] = sc['parent']
        stmts.append(insert('fct_pr_mgsm_menu_group_screen_mapping', {**mgsm, **audit}))
        for i, f in enumerate(sc['fields'], 1):
            row = {'psc_screenid': sc['id'], 'psf_fieldid': f['id'], 'prv_version': '1.0', 'psf_locateby': f.get('locateby', 'id'),
                   'psf_field_db_column': f['caption'], 'pcmpt_componenttypeid': f['type'], 'psf_field_addition': '+',
                   'psf_repoid': f.get('repoid'), 'psf_sequenceno': i, 'psf_field_status': 'Y'}
            if f.get('mandatory'):
                row['psf_mandatory_field'] = f['mandatory']
            stmts.append(insert('fct_pr_sf_screen_field', {**row, 'psf_iteration_number': 1, **audit}))
            n_sf += 1
        for e in sc['events']:
            row = {'psc_screenid': sc['id'], 'psef_serialno': e['serial'], 'pcmpt_componenttypeid': e['type'], 'pce_comp_event': e['event'],
                   'psef_locateby': e.get('locateby'), 'psef_fieldid': e.get('field'), 'psef_fixed_value': e.get('fixed'),
                   'psef_sequenceno': e.get('sequence', e['serial']), 'psef_status': 'Y', 'psef_ref_serialno': e.get('ref'), 'psef_desc': e['desc']}
            if e.get('fixedvalue_type'):
                row['psef_fixedvalue_type'] = e['fixedvalue_type']
            stmts.append(insert('fct_pr_sef_screen_events_flow', {**row, **audit}))
            n_sef += 1
    stmts.append(insert('fct_pr_tf_test_flow', {'ptf_testflowid': fl['id'], 'ptf_description': fl['description'], 'ptf_status': 'Y',
                                                'ptt_testtypeid': fl.get('test_type', '2'), 'master_app_id': mapp, **audit}))
    stmts.append(insert('fct_pr_tfd_test_flow_details', {'ptf_testflowid': fl['id'], 'pmg_menugroupid': mg['id'], 'ptfd_sequenceno': 1,
                                                         'ptfd_filename': fl.get('filename'), **audit}))

    sc_in = ', '.join(q(sc['id']) for sc in screens)
    pairs = sorted({(e['type'], e['event']) for sc in screens for e in sc['events']})
    pre = f"""DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM fct_pr_mg_menu_group WHERE pmg_menugroupid = {q(mg['id'])})
     OR EXISTS (SELECT 1 FROM fct_pr_sc_screens WHERE psc_screenid IN ({sc_in}))
     OR EXISTS (SELECT 1 FROM fct_pr_tf_test_flow WHERE ptf_testflowid = {q(fl['id'])})
     OR EXISTS (SELECT 1 FROM fct_pr_mgsm_menu_group_screen_mapping WHERE pmg_menugroupid = {q(mg['id'])} OR psc_screenid IN ({sc_in}))
     OR EXISTS (SELECT 1 FROM fct_pr_sf_screen_field WHERE psc_screenid IN ({sc_in}))
     OR EXISTS (SELECT 1 FROM fct_pr_sef_screen_events_flow WHERE psc_screenid IN ({sc_in}))
     OR EXISTS (SELECT 1 FROM fct_pr_tfd_test_flow_details WHERE pmg_menugroupid = {q(mg['id'])} OR ptf_testflowid = {q(fl['id'])}) THEN
    RAISE EXCEPTION 'QA OS: menu group {mg['id']}, screen(s) {', '.join(sc['id'] for sc in screens)} or flow {fl['id']} already in use; regenerate with fresh ids';
  END IF;"""
    if pairs:
        pre += f"""
  IF (SELECT count(*) FROM fct_pr_ce_component_event WHERE (pcmpt_componenttypeid, pce_comp_event) IN ({', '.join(f'({q(a)},{q(b)})' for a, b in pairs)})) <> {len(pairs)} THEN
    RAISE EXCEPTION 'QA OS: a (component type, event) pair used by this flow is missing in fct_pr_ce_component_event';
  END IF;"""
    pre += '\nEND $$;'
    counts = {'fct_pr_mg_menu_group': 1, 'fct_pr_sc_screens': len(screens), 'fct_pr_mgsm_menu_group_screen_mapping': len(screens),
              'fct_pr_sf_screen_field': n_sf, 'fct_pr_sef_screen_events_flow': n_sef, 'fct_pr_tf_test_flow': 1, 'fct_pr_tfd_test_flow_details': 1}
    verify = '\n'.join(f"-- {t}: expect {n} row(s)\n-- SELECT count(*) FROM {t} WHERE created_by = {q(tag)};" for t, n in counts.items())
    header = f"""-- =====================================================================================
-- {spec['story']}  {fl['description']}
-- Generated by QA OS script-generator on {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} - FOR HUMAN REVIEW. NOT APPLIED.
""" + (f"-- Source of truth: {spec['source']}. DB used for structure/ids only.\n" if spec.get('source') else '') + \
f"""-- Target: CTA_CONFIG_ASSERTION, master_app_id {mapp if mapp is not None else 'NULL'}. One transaction; every row has created_by = {q(tag)}.
-- Rollback: framework_rollback.sql. Ids: menu group {mg['id']}, screens {','.join(sc['id'] for sc in screens)}, flow {fl['id']}.
-- ====================================================================================="""
    sql = header + '\nBEGIN;\n\n-- pre-flight: stop if the ids are taken\n' + pre + '\n\n' + '\n\n'.join(stmts) + \
        '\n\nCOMMIT;\n\n-- post-check (run after COMMIT)\n' + verify + '\n'

    by = f'created_by = {q(tag)}'
    rb = [f"-- Removes everything {spec['story']} added: rows with these ids AND {by}; children first.", 'BEGIN;',
          f"DELETE FROM fct_pr_tfd_test_flow_details WHERE ptf_testflowid = {q(fl['id'])} AND pmg_menugroupid = {q(mg['id'])} AND {by};",
          f"DELETE FROM fct_pr_tf_test_flow WHERE ptf_testflowid = {q(fl['id'])} AND {by};",
          f"DELETE FROM fct_pr_sef_screen_events_flow WHERE psc_screenid IN ({sc_in}) AND {by};",
          f"DELETE FROM fct_pr_sf_screen_field WHERE psc_screenid IN ({sc_in}) AND {by};",
          f"DELETE FROM fct_pr_mgsm_menu_group_screen_mapping WHERE pmg_menugroupid = {q(mg['id'])} AND psc_screenid IN ({sc_in}) AND {by};",
          f"DELETE FROM fct_pr_sc_screens WHERE psc_screenid IN ({sc_in}) AND {by};",
          f"DELETE FROM fct_pr_mg_menu_group WHERE pmg_menugroupid = {q(mg['id'])} AND {by};",
          'COMMIT;']
    return sql, '\n'.join(rb) + '\n', counts


def workbook_sheets(spec):
    """-> ([(sheet, columns, rows)], warnings): one sheet per screen (mgsm order) + one per referenced _ASSR sheet."""
    screens = normalise(spec)
    given = {s['sheet']: s for s in (spec.get('casedata') or {}).get('sheets', [])}
    assr = assertion_sheets(screens)
    checks = any((e['type'], e['event']) in (('0000', '0007'), ('0000', '0005')) for sc in screens for e in sc['events'])
    out, warn = [], []
    wanted = [(sc['name'], sc) for sc in sorted(screens, key=lambda s: s['seq'])] + [(name, None) for name in assr]
    for name, sc in wanted:
        if len(name) > 31:
            fail(f'sheet name longer than 31 chars: {name!r}')
        if sc is not None:
            needed = [f['caption'] for f in sc['fields'] if f['type'] != READABLE]
            skeleton = SCREEN_CONTROLS + (['CHECK_VALIDATION'] if checks else []) + needed
        else:
            needed, skeleton = ['PK', 'EXPECTED_MESSAGE'], ASSR_CONTROLS
        s = given.pop(name, None)
        if s is None:
            warn.append(f'sheet {name!r}: no case-data rows in the spec, written header-only')
            out.append((name, skeleton, []))
            continue
        cols = s['columns']
        if any(c is None or not str(c).strip() for c in cols):
            fail(f'sheet {name!r}: blank header cell')
        missing = [c for c in needed + ['PK'] if c not in cols]
        if missing:
            fail(f'sheet {name!r}: missing column(s) {missing}')
        for r in s['rows']:
            if len(r) != len(cols):
                fail(f'sheet {name!r}: row {r!r} has {len(r)} cells for {len(cols)} columns')
        out.append((name, cols, s['rows']))
    if given:
        fail(f'case-data sheet(s) {sorted(given)} match no screen and no assertion event')
    return out, warn


def main(spec_path, out):
    spec = json.load(open(spec_path, encoding='utf-8'))
    os.makedirs(out, exist_ok=True)
    sql, rollback, counts = build(spec)
    sheets, warn = workbook_sheets(spec)
    screens, mg, fl = spec['screens'], spec['menu_group'], spec['flow']
    open(os.path.join(out, 'framework.sql'), 'w', encoding='utf-8').write(sql)
    open(os.path.join(out, 'framework_rollback.sql'), 'w', encoding='utf-8').write(rollback)

    # ---- case data workbook (engine format: sheet = screen name, headers = psf_field_db_column + control columns)
    import openpyxl
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name, cols, rows in sheets:
        ws = wb.create_sheet(name)
        ws.append(cols)
        for r in rows:
            ws.append(r)
    wb.save(os.path.join(out, fl['filename'] + '.xlsx'))
    formulas = any(isinstance(c, str) and c.startswith('=') for _, _, rows in sheets for r in rows for c in r)

    # ---- review sheet: every generated row traced to evidence
    assr = {a['sheet']: a for a in spec.get('assertion_sheets', [])}
    L = [f"# Framework script review — {spec['story']}", '',
         f"Flow **{fl['id']}** `{fl['description']}` · menu group **{mg['id']}** · screens **{', '.join(s['id'] for s in screens)}** · master_app_id {spec.get('master_app_id')}",
         f"Files: `framework.sql` (apply), `framework_rollback.sql`, `{fl['filename']}.xlsx` (case data → `<BASE_PATH>\\casedata\\`).", '',
         '## Row counts', ', '.join(f'{t} {n}' for t, n in counts.items()), '',
         '## Navigation', f"- searchtext `{mg['searchtext']}` → `{mg['navigation']}` (type `{mg.get('navigation_type', 'id')}`). Evidence: {mg.get('evidence', '')}"]
    for sc in sorted(screens, key=lambda s: s['seq']):
        L += ['', f"## Screen {sc['seq']}: {sc['id']} {sc['name']}" + (f" (`{sc['url']}`)" if sc.get('url') else ''), '',
              '| # | Caption (case-data column) | Locator | Type | Mandatory | Repo | Evidence |', '|---|---|---|---|---|---|---|']
        for i, f in enumerate(sc['fields'], 1):
            L.append(f"| {i} | {f['caption']} | {f.get('locateby', 'id')}=`{f['id']}` | {f['type']} | {f.get('mandatory') or ''} | {f.get('repoid') or ''} | {f.get('evidence', '')} |")
        L += ['', '| # | Description | Type/Event | Target | Runs | Evidence |', '|---|---|---|---|---|---|']
        for e in sc['events']:
            runs = 'per row (child of Load Data)' if e.get('ref') is not None else 'once (top level)'
            L.append(f"| {e['serial']} | {e['desc']} | {e['type']}/{e['event']} | {e.get('field') or e.get('fixed') or ''} | {runs} | {e.get('evidence', '')} |")
    L += ['', '## Workbook sheets'] + [f"- `{n}`: {len(r)} row(s)" + (f" — expected `{assr[n]['expected_message']}`" if n in assr else '') for n, _, r in sheets]
    L += [f'- WARNING: {w}' for w in warn]
    if formulas:
        L.append('- Formula cells present: run `python framework/tools/cache_formulas.py` on the workbook as the last write.')
    L += ['', '## Not asserted'] + [f"- {x.get('type', '')}: {x.get('text', '')} — {x.get('reason', '')}" for x in spec.get('not_asserted', [])]
    L += ['', '## Gaps'] + [f"- {x.get('item', x) if isinstance(x, dict) else x}: {x.get('note', '') if isinstance(x, dict) else ''}" for x in spec.get('gaps', [])]
    L += ['', '## Not covered by this flow (and why)'] + [f'- {x}' for x in spec.get('not_covered', [])]
    L += ['', '## Risks to check on first apply'] + [f'- {x}' for x in spec.get('risks', [])]
    open(os.path.join(out, 'framework_review.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    n_ins = sql.count('INSERT INTO')
    print(f"wrote {n_ins} INSERTs ({len(screens)} screen(s)), rollback, {fl['filename']}.xlsx "
          f"({len(sheets)} sheet(s), {sum(len(r) for _, _, r in sheets)} data rows), review -> {out}")
    for w in warn:
        print('WARNING:', w)
    if formulas:
        print('NOTE: formula cells present - run framework/tools/cache_formulas.py on the workbook as the last write')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
