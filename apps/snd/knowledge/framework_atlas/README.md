# Framework flow atlas (CTA_CONFIG_ASSERTION)

Machine-readable map of every group test flow, test flow, screen, field and event of the legacy Regress framework DB, so an AI can write standard
test cases and steps for any flow **without replaying it first**. Built read-only on 2026-09-30 from the `selenium-framework-db` MCP connector.
Extends (does not repeat) `qa-os/framework/cta_config_assertion.md` and `qa-os/docs/engine-review/{runtime,authoring}.md`. Rebuild with:

```
python qa-os/apps/snd/tools/build_atlas.py            # raw/*.json -> everything below (about 10 s)
python qa-os/apps/snd/tools/build_atlas.py --find "goods issue note"   # story text -> flows and groups
```

## Files

| File | Use |
|---|---|
| `raw/*.json` | Row dumps (see "Raw dump notes"). Nothing is modified; `build_atlas.py` reads only these |
| `atlas.json` | `groups` (ordered chains), `flows` (summary), `screens` (fields + events), users, apps, component/event vocab |
| `flows/<flowid>.json` / `.md` | One flow with every screen, field and event embedded / plain-language page |
| `group_<id>.md` | The whole cycle as a numbered business story with switch-user points |
| `INDEX.json` | Tags per flow (business areas, market, screens, repos, groups, files) so an orchestrator loads only matching files |
| `reverse_index.json` | Menu option, screen name, flow/menu text to flows and groups |
| `anomalies.json` | Integrity findings with `src` keys |
| `validation.json` | Group 11 chain vs live SQL |

Every object carries `src`, for example `sef:001001|serial 4`, `gtfd:11|10|00010001`, `sf:001001|DDL__PVNDVENDCODE|1.0|3|1`.
Short names: gtf, gtfd, tf, tfd, mg, mgsm, sc, sf, sef, ce, cmpt, sq, app, lu, alg, toast.

## Raw dump notes

- Large tables (`gtfd, tf, tfd, mg, mgsm, sc, sf, sef, sq, toast`) are complete and verbatim (all columns, including audit).
- Small tables (`gtf, ce, cmpt, app, lu, alg, rv, tt`) keep only the business columns (audit columns dropped).
- `fct_pr_lu_login_users.json` has **no password column** (serial, app, name, status, approval status). `fct_pr_app_application.json` drops `papp_app_db_url`
  (it embeds database credentials); only the database name is kept. No credential was read or written anywhere.
- Row counts: gtf 31, gtfd 1,029, tf 547, tfd 527, mg 586, mgsm 1,507, sc 1,477, sf 6,216, sef 9,138, ce 25, cmpt 15, sq 57, app 16, lu 32, alg 35, rv 3, tt 3, toast 1,574.
- Other tables with data: `fct_pr_alg_app_allowable_groups` (which app may list which group; group must have a row or the UI dropdown hides it),
  `fct_pr_rv_release_version` (1.0/2.0/3.0, used by `sf.prv_version`), `fct_pr_tt_test_type` (1 Regression G, 2 Smoke S, 3 Performance G),
  `fct_rp_set_screen_event_toast` (1,574 rows written by event 0004: screen, flow, message; some rows are Java exception texts, not toasts),
  `test_execution` (16,291 run log rows: date, user, type, status, totals, JSON metadata; not dumped), `pr_gg_release_info` (0 rows).

## How the tables connect (verified against the data, 100 % match unless stated)

```
gtf.pgtf_grouptestflowid = gtfd.pgtf_grouptestflowid                          1029/1029
gtfd.ptf_testflowid      = tf.ptf_testflowid                                  1029/1029
gtfd.plu_serial_no       = lu.plu_serial_no   (global, NOT app-scoped)        469/469 non-null
gtf  <-> alg <-> app:  alg.pgtf_grouptestflowid = gtf id, alg.papp_app_id = app.papp_app_id
tf.ptf_testflowid        = tfd.ptf_testflowid                                 527/527  (20 flows have no tfd)
tfd.pmg_menugroupid      = mg.pmg_menugroupid                                 527/527
mg.pmg_menugroupid       = mgsm.pmg_menugroupid                               1507/1507
mgsm.psc_screenid        = sc.psc_screenid                                    1507/1507
mgsm.pmgsm_parent_screenid = a screen of the SAME menu group                  828/832 (4 dangling)
sc.psc_screenid          = sf.psc_screenid / sef.psc_screenid / sq.psc_screenid   6216, 9138, 57 (all match)
(sef.pcmpt_componenttypeid, sef.pce_comp_event) = (ce.pcmpt_componenttypeid, ce.pce_comp_event)   9138/9138
sef.psef_ref_serialno    = sef.psef_serialno of the SAME screen               3531/3531 non-null
sf.pcmpt_componenttypeid = cmpt.pcmpt_componenttypeid                         3 rows with NULL type (screen 17)
```

Unique keys observed: gtfd (group, seq) is unique in the data (PK also includes flow); sef (screen, serial) is unique; mgsm (mg, screen, seq) is unique but the
same screen may appear twice in one menu group (valid, e.g. Dispatch Advice grid screen 001004 is searched twice).
Id habits (not keys): flow id first 4 chars = menu group id in 505/527 flows; screen id first 4 chars = menu group id in 1,345/1,507 mapping rows.

Execution path the atlas follows: group chain (gtfd order by seq, status `Y`) -> flow -> its single tfd row -> menu group (search text + navigation id) ->
top-level mgsm rows by `pmgsm_sequenceno` (status NULL/`Y`) with child mgsm rows nested under their parent -> screen -> active fields -> events
(`psef_status` Y/A, ordered by `psef_sequenceno`, children by `psef_ref_serialno`).

## Data volume

31 groups (813 active / 1,029 rows), 547 flows in `tf` (444 referenced by groups, 0 referenced but missing, 20 with no tfd so they cannot run), 586 menu groups,
1,477 screens (1,331 reachable from some flow, 1,162 from group flows), 6,216 fields (5,298 active: status Y and addition `+`), 9,138 events (7,475 active),
57 screen queries, 32 users, 16 apps. Active event kinds: click 3,503, load data 1,072, fill text 744, assertion 668, group assertion 521, screen validation 407,
wait 377, fill repo 166, frame switch 146, alert click 42, flow control 39, dropdown 15, Q2Q 2.

Groups by market (name suffix; see `group_<id>.md`): Pakistan 1, 11, 12, 13(setup), 14, 66(setup), 70(SAN), 74, 77; ITHD/Thailand 51, 52, 65, 71; BD 16, 61, 69, 81, 83;
PH 15, 63, 78, 80, 84; Astron 67, 68; UP 73; VN 72, 75; KH 76; LA 79; GIS 64. Group 11 is the reference Pakistan cycle (46 active rows, 10 switch points).

## What each column means for authoring

| Where | Column | Authoring meaning |
|---|---|---|
| gtfd | `pgtfd_sequenceno`, `pgtfd_status` | Run order; only `Y` rows run. Gaps are normal |
| gtfd | `pgtf_testflow_login_status` | NULL or `N` = continue in the same session (the `plu_serial_no` is ignored); anything else (`Y`) = logout + login as `plu_serial_no`. 109 `Y` rows have no user (engine then logs in with a null name) |
| gtfd | `pgtf_testflow_appid` | Non-NULL switches driver to a mobile app; NULL everywhere in the web cycle |
| tfd | `ptfd_filename` | Case-data workbook of the flow; else `mgsm.pmgsm_screen_filename`; else app default. 396/527 flows use the default |
| mg | `pmg_searchtext`, `pmg_navigation`, `pmg_navigation_type` | Text typed in the menu search, then element(s) clicked (comma list allowed) |
| mgsm | `pmgsm_sequenceno`, `pmgsm_parent_screenid`, `pmgsm_navigation_type/_path` | Screen order; child = runs inside parent's row loop; nav path = the tab to click (`tab_1`, `tab_2`) |
| sc | `psc_screenname` | **Case-data sheet name** (<= 31 chars); `psc_screentype` Save/Update/Delete/Forward/Reject/... is informational |
| sf | `psf_field_db_column` | **Case-data column header and the on-screen caption** (the DB has no separate caption; the atlas exposes it as both `label` and `db_column`) |
| sf | `psf_fieldid`, `psf_locateby`, `pcmpt_componenttypeid` | Element id and how to drive it (0001 text, 0002 dropdown, 0003 date, 0006 autoselect, 0010 readable = never filled) |
| sf | `psf_mandatory_field` | `Y` = required field (drives REQ_FIELD checks); NULL otherwise |
| sf | `psf_repoid`, `psf_field_source` | With `REPO` source the value is read from the repo; a field with a `psf_repoid` is **written** to the repo by an active 0012 event on the same screen |
| sf | `psf_field_status`, `psf_field_addition` | Active only when `Y` and `+` |
| sef | `pcmpt_componenttypeid/pce_comp_event` | See `ce`; kind names in `atlas.json` (`click`, `load_data`, `assertion`, `group_assertion`, `fill_repo`, ...) |
| sef | `psef_ref_serialno` | Parent event. Children of a load-data event run once per case-data row (Save, assertions belong there); a ref to a click never runs |
| sef | `psef_fixed_value` | Assertion kind `TSTMSG/ELEVAL/ELEVLD`; for 0014 `<kind>,<AssertionSheet>`; wait seconds; text/value for single fills; children of assertions use `TP`/`TN` |
| sef | `psef_fixedvalue_type` | `EXCEL` column name, `REPO` repo id, `FIXED` literal for single-field fills |
| sq | `psq_query`, `psq_qryparameters`, `psq_query_target` | Q2Q data verification (event 0005) and DB validation (0007); parameters are repo keys |

The atlas adds for each event `engine_role`: `top_level`, `per_row_child`, `assertion_branch`, `flow_control_child`, `orphan_ref_runs_top_level`, or `NEVER_RUNS_parent_is_<kind>`.

## Market and client differences (visible, not hidden)

- Groups are per market (see above); `alg` says which app (URL, base path) may run each group. The base path names the market folder (`PAK_QA`, `PHP_QA`,
  `BD_QA`, `VN_QA`, `KH_QA`, `LA_QA`, `ITHD_QA`, `Astron_QA`, `Up_Coming_QA`); `workbook_variant_inferred` maps only the four that have a sample workbook
  (Pak, PHP, Bangla, Vietnam). The framework tables do **not** say which workbook file a market uses; that comes from config `APP_EXCELCONN_RESULT` / the base path. Treat the mapping as inferred.
- Markets have their own flows and sheets: e.g. Dispatch Advice is `00100001` (sheets `Dispatch Advice*`), PH `Dispatch Advice_PH`, TH `Dispatch Advice II TH`, VN `Dispatch Advice R2 VN`.
  `flows/<id>.json` -> `workbook_coverage` shows, per sample workbook, which of the flow's sheets exist, row counts and missing columns; `best_sample_workbooks` names the fit.
- `INDEX.json` -> `families[area][market]` lists the equivalent flows across markets for one business area.

## Anomalies (full list with examples in `anomalies.json`)

- 20 flows have no `tfd` row (cannot run); 6 of them are used by a group: `02770001`, `04480001`, `04700001`, `05910001`, `05980001`, `06010001`. 5 flows are inactive in `tf`.
- 51 screens are in no `mgsm` row (orphans); 65 menu groups are used by no flow; 4 `tfd` rows point to a menu group with no screens.
- 41 active events hang under a parent that cannot run children (mostly a click or a validation): they never run. 23 fields are active but `addition != '+'`, which makes the engine remove the field.
- 109 group rows with login status `Y` and no user; 65 rows with `N` and a user (user ignored); 6 rows with NULL status and a user; 53 switch rows use a login user that belongs to an app not allowed for the group (`alg`), e.g. user `AppUser` (app 13) in group 1.
- Group 52 has no `alg` row; 6 groups do not start with an app login flow (1, 12, 14, 52, 64, 77): they assume a session or rely on the UI login.
- Repo id spellings differ (`REPO_DOCUMENTNO`/`REPO_DocumentNo`, `REPO_DISTRIBUTOR`/`g_REPO_DISTRIBUTOR`, `REPO_CODE`/`REPO_Code`); the engine keys are case-sensitive with a fuzzy `contains` fallback. The atlas compares them upper-cased without `g_`.
- 7 repos are read but no flow writes them (`REPO_ORGA`, `REPO_CMDOCTYPE`, `REPO_REF_ORDER_NO`, `REPO_REF_ORDER_EDITNO`, ... supplied by workbook `GLOBAL-REPO`/`repo_*` columns, invisible to the DB); 74 group needs are unresolved in-chain for that reason; `LOGIN_*` and `SELECTED_DIST` are engine-provided.
- 22 screen names exceed 31 chars (Excel sheet limit); 60 screen names are shared by several screens (the same sheet serves them).
- `psef_status = 'I'` (335 rows) is not in the engine filter (`Y`,`A`) and its meaning is undocumented; treated as inactive. One event (screen 005310, serial 1) has a NULL status.
- Group 11 has **46** active rows today, not 44 (the same 46 the DISPATCH_ADVICE.md session plan lists).

## Validation (group 11)

`validation.json`: the atlas chain for group 11 equals the live SQL capture `select * from fct_pr_gtfd_group_test_flow_detail where pgtf_grouptestflowid='11' and pgtfd_status='Y' order by pgtfd_sequenceno`
(46 rows: sequence, flow, user, login status, app compared as one ordered string; capture in `raw/_validation_group11_sql.json`), and the switch points equal `5, 9, 23, 24, 37, 38, 49, 50, 59, 60`. Result: no mismatch.

## How an AI should use the atlas

### (a) Write standard test steps for a flow
1. Find the flow: `--find "<story words>"`, or `INDEX.json` -> `areas[...]` / `families[area][market]`, then read `flows/<id>.md` (one page) and, when you need exact ids, `flows/<id>.json`.
2. Steps come from the screens in `screens_exec` order: `navigate` = menu search text + navigation id; per screen: one `fill` step per active field with its `label` (case-data column) and component type,
   then the events in order (click ids, waits, `fill_repo`, assertions). Children of a load-data event repeat per case-data row.
3. Data: one workbook sheet per screen name plus the `_ASSR` sheets named by 0014 events (`sheets` in the flow file); keep PKs aligned across a group (`01`, `01-01`); dates `yyyy-mm-dd`; use `TN` unless asserting validation.
   `EXPECTED_MESSAGE` text must be observed live (see `observed_toasts_event0004` and the flow's live notes), never guessed.
4. Repos: `repos.writes` tell which step captures a document number; `repos.reads` and the group's `needs` say which earlier flow must have produced it.
5. Users: honour `login_action` of the chain row (SWITCH vs same session). Passwords are never in the atlas; the QA member logs in.

### (b) Remember what was executed (trace key)
Attach to every executed step: `<group>:<seq>:<flow>:<screen>:e<event serial>`, e.g. `11:10:00010001:000101:e3` (group 11, chain seq 10, Order Booking, screen 000101, event 3).
Field steps use `<group>:<seq>:<flow>:<screen>:f<field seq>`. `trace_prefix` on every chain row gives the first three parts; `trace_key` on every event gives `<screen>:e<serial>`.
A trace key resolves to exactly one row: split it, look up `groups[group].chain[seq]`, `screens[screen].events[serial]` and read the `src`. Record the observed value (document number, toast, status) next to the key.

### (c) Refer back when authoring a new story
1. `--find` the business words (menu option, screen name or flow text) to get candidate flows and the groups/seq numbers that already use them.
2. Pick the market family in `INDEX.json`, copy the group's ordering and switch points from `group_<id>.md` (maker/checker pattern: creation flows keep the current user, approval flows switch to the `tssm` approver user).
3. Reuse a flow's `repos` to chain new steps to existing documents; if the story needs a screen or field absent from the atlas, mark it as an authoring gap (framework config change) instead of inventing ids.
4. Known drift between framework config and the live app is in the flows' "Known live quirks" section (verbatim lines from `framework_flows/*.md`, only where a replay log exists: DA, OB).

## Columns / tables whose meaning is not determined

- `psef_status = 'I'` (335 events).
- `psf_iteration_number` values 2-11 (7 fields) and `psf_app_ids` (always NULL) : semantics are in engine code only.
- `pmgsm_screen_filename_status` (Y/N/NULL) : whether `N` disables the filename is not shown in the engine review.
- `ptf_platform` (always NULL), `psef_mandatory_validation` (only `N`/blank), `psef_validationtype` `EXCEL`/`DB`/`Q2Q` per event are used as documented in runtime.md; `psef_condition_statement` is NULL in all rows.
- `test_execution.execution_metadata` (JSON run report) was not opened.
