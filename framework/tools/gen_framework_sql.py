"""script-generator (v0): flow spec -> CTA_CONFIG_ASSERTION SQL + rollback + case-data workbook + review sheet.

  python framework/tools/gen_framework_sql.py <spec.json> <out_dir>

Spec (JSON): story, master_app_id, tag, menu_group{id,description,searchtext,navigation,navigation_type},
             screen{id,name,type}, fields[{id,caption,type,mandatory,locateby,evidence}],
             events[{serial,desc,type,event,locateby,field,fixed,ref,evidence}], flow{id,description,test_type,filename},
             casedata{sheet, columns[...], rows[[...]]}

Rules learned from the live schema (see framework/cta_config_assertion.md):
 - prv_version is NOT NULL ('1.0'); psf_field_addition '+'; psef_serialno of fields comes from a sequence, so it is omitted.
 - flow file name goes in fct_pr_tfd_test_flow_details.ptfd_filename (story-specific workbooks); mgsm filename stays NULL.
 - every generated row carries created_by = <tag>, so the rollback script and audits can find exactly what was added.
Never applies anything: the output is for human review.
"""
import json, os, sys, datetime as dt

spec = json.load(open(sys.argv[1], encoding='utf-8'))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)

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
TAG, MAPP = spec['tag'], spec['master_app_id']


def q(v):
    if v is None:
        return 'NULL'
    if isinstance(v, int) and not isinstance(v, bool):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"


def insert(table, row):
    bad = set(row) - COLS[table]
    assert not bad, f'{table}: unknown column(s) {bad}'
    for (t, c), n in LIMITS.items():
        if t == table and c in row and row[c] and len(str(row[c])) > n:
            raise SystemExit(f'{table}.{c} too long ({len(str(row[c]))} > {n}): {row[c]}')
    cols = list(row)
    return f"INSERT INTO {table} ({', '.join(cols)})\nVALUES ({', '.join(q(row[c]) if not str(row[c]).startswith('@') else row[c][1:] for c in cols)});"


now = '@now()'
audit = {'create_date': now, 'created_by': TAG, 'modified_date': now, 'modified_by': TAG}
mg, sc, fl = spec['menu_group'], spec['screen'], spec['flow']
stmts = []
stmts.append(insert('fct_pr_mg_menu_group', {'pmg_menugroupid': mg['id'], 'pmg_description': mg['description'], 'pmg_searchtext': mg['searchtext'],
                                              'pmg_navigation': mg['navigation'], 'pmg_navigation_type': mg.get('navigation_type', 'id'), 'master_app_id': MAPP, **audit}))
stmts.append(insert('fct_pr_sc_screens', {'psc_screenid': sc['id'], 'psc_screenname': sc['name'], 'psc_screentype': sc.get('type', 'Save'), 'master_app_id': MAPP, **audit}))
stmts.append(insert('fct_pr_mgsm_menu_group_screen_mapping', {'pmg_menugroupid': mg['id'], 'psc_screenid': sc['id'], 'pmgsm_sequenceno': 1, 'pmgsm_status': 'Y', **audit}))
for i, f in enumerate(spec['fields'], 1):
    stmts.append(insert('fct_pr_sf_screen_field', {'psc_screenid': sc['id'], 'psf_fieldid': f['id'], 'prv_version': '1.0', 'psf_locateby': f.get('locateby', 'id'),
                                                    'psf_field_db_column': f['caption'], 'pcmpt_componenttypeid': f['type'], 'psf_field_addition': '+',
                                                    'psf_sequenceno': i, 'psf_field_status': 'Y', 'psf_mandatory_field': f.get('mandatory'), 'psf_iteration_number': 1, **audit}))
for e in spec['events']:
    stmts.append(insert('fct_pr_sef_screen_events_flow', {'psc_screenid': sc['id'], 'psef_serialno': e['serial'], 'pcmpt_componenttypeid': e['type'], 'pce_comp_event': e['event'],
                                                          'psef_locateby': e.get('locateby'), 'psef_fieldid': e.get('field'), 'psef_fixed_value': e.get('fixed'),
                                                          'psef_sequenceno': e['serial'], 'psef_status': 'Y', 'psef_ref_serialno': e.get('ref'), 'psef_desc': e['desc'], **audit}))
stmts.append(insert('fct_pr_tf_test_flow', {'ptf_testflowid': fl['id'], 'ptf_description': fl['description'], 'ptf_status': 'Y', 'ptt_testtypeid': fl.get('test_type', '2'), 'master_app_id': MAPP, **audit}))
stmts.append(insert('fct_pr_tfd_test_flow_details', {'ptf_testflowid': fl['id'], 'pmg_menugroupid': mg['id'], 'ptfd_sequenceno': 1, 'ptfd_filename': fl.get('filename'), **audit}))

pre = f"""DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM fct_pr_mg_menu_group WHERE pmg_menugroupid = {q(mg['id'])})
     OR EXISTS (SELECT 1 FROM fct_pr_sc_screens WHERE psc_screenid = {q(sc['id'])})
     OR EXISTS (SELECT 1 FROM fct_pr_tf_test_flow WHERE ptf_testflowid = {q(fl['id'])}) THEN
    RAISE EXCEPTION 'QA OS: menu group {mg['id']}, screen {sc['id']} or flow {fl['id']} already exists; regenerate with fresh ids';
  END IF;
END $$;"""
counts = {'fct_pr_mg_menu_group': 1, 'fct_pr_sc_screens': 1, 'fct_pr_mgsm_menu_group_screen_mapping': 1, 'fct_pr_sf_screen_field': len(spec['fields']),
          'fct_pr_sef_screen_events_flow': len(spec['events']), 'fct_pr_tf_test_flow': 1, 'fct_pr_tfd_test_flow_details': 1}
verify = '\n'.join(f"-- {t}: expect {n} row(s)\n-- SELECT count(*) FROM {t} WHERE created_by = {q(TAG)};" for t, n in counts.items())
header = f"""-- =====================================================================================
-- {spec['story']}  {fl['description']}
-- Generated by QA OS script-generator on {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} — FOR HUMAN REVIEW. NOT APPLIED.
-- Target: CTA_CONFIG_ASSERTION (master_app_id {MAPP}). Apply in one transaction; every row is tagged created_by = {TAG}.
-- Roll back with {os.path.basename(out)}/framework_rollback.sql. Traceability: framework_review.md.
-- ====================================================================================="""
open(os.path.join(out, 'framework.sql'), 'w', encoding='utf-8').write(
    header + '\nBEGIN;\n\n-- pre-flight: stop if the ids are taken\n' + pre + '\n\n' + '\n\n'.join(stmts) + '\n\nCOMMIT;\n\n-- post-check (run after COMMIT)\n' + verify + '\n')
rb = [f"-- Removes everything {spec['story']} added ({TAG}). Order matters (children first).", 'BEGIN;']
for t in ['fct_pr_tfd_test_flow_details', 'fct_pr_tf_test_flow', 'fct_pr_sef_screen_events_flow', 'fct_pr_sf_screen_field',
          'fct_pr_mgsm_menu_group_screen_mapping', 'fct_pr_sc_screens', 'fct_pr_mg_menu_group']:
    rb.append(f"DELETE FROM {t} WHERE created_by = {q(TAG)};")
rb.append('COMMIT;')
open(os.path.join(out, 'framework_rollback.sql'), 'w', encoding='utf-8').write('\n'.join(rb) + '\n')

# ---- case data workbook (engine format: sheet = screen name, headers = psf_field_db_column + control columns)
import openpyxl
cd = spec['casedata']
wb = openpyxl.Workbook()
ws = wb.active
ws.title = cd['sheet']
ws.append(cd['columns'])
for r in cd['rows']:
    ws.append(r)
wb.save(os.path.join(out, fl['filename'] + '.xlsx'))

# ---- review sheet: every generated row traced to evidence
L = [f"# Framework script review — {spec['story']}", '', f"Flow **{fl['id']}** `{fl['description']}` · menu group **{mg['id']}** · screen **{sc['id']}** · master_app_id {MAPP}",
     f"Files: `framework.sql` (apply), `framework_rollback.sql`, `{fl['filename']}.xlsx` (case data → `<BASE_PATH>\\casedata\\`).", '',
     '## Navigation', f"- searchtext `{mg['searchtext']}` → click `li#{mg['navigation']}` (type `{mg.get('navigation_type', 'id')}`). Evidence: {mg.get('evidence', '')}", '',
     '## Fields (fct_pr_sf_screen_field)', '| # | Caption (case-data column) | Locator | Type | Mandatory | Evidence |', '|---|---|---|---|---|---|']
for i, f in enumerate(spec['fields'], 1):
    L.append(f"| {i} | {f['caption']} | {f.get('locateby', 'id')}=`{f['id']}` | {f['type']} | {f.get('mandatory') or ''} | {f.get('evidence', '')} |")
L += ['', '## Events (fct_pr_sef_screen_events_flow)', '| # | Description | Type/Event | Target | Evidence |', '|---|---|---|---|---|']
for e in spec['events']:
    L.append(f"| {e['serial']} | {e['desc']} | {e['type']}/{e['event']} | {e.get('field') or e.get('fixed') or ''} | {e.get('evidence', '')} |")
L += ['', '## Not covered by this flow (and why)'] + [f'- {x}' for x in spec.get('not_covered', [])]
L += ['', '## Risks to check on first apply'] + [f'- {x}' for x in spec.get('risks', [])]
open(os.path.join(out, 'framework_review.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(f"wrote {len(stmts)} INSERTs, rollback, {fl['filename']}.xlsx ({len(cd['rows'])} data rows), review -> {out}")
