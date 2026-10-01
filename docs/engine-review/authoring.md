# Regress authoring UI review: how config rows are really written

**Scope:** the desktop authoring side of `C:\git-projects\NGSelenium-Testing`, which is checked out at **`745e2fb` (2026-09-11, detached HEAD)**, not `af79ecd` as `framework/cta_config_assertion.md` says. Reviewed read-only, and compared with the live `CTA_CONFIG_ASSERTION` DB (read-only, 2026-09-30).
**Adds to and corrects** `qa-os/framework/cta_config_assertion.md`. It does not repeat that file.

**Path short forms:** `U/` = `Elements/src/main/java/com.centegy.selenium/ui2/tabs/utilities/`, `DBX` = `…/UI/Tab/DB/DBExecution.java`, `FT` = `…/ui2/FillTable.java`, `FC` = `…/ui2/fillCombos/FillCombos.java`, `Main` = `…/Main.java`.

## 0. Corrections to `cta_config_assertion.md`

| Topic | Map says | Actually |
|---|---|---|
| `fct_pr_ce_component_event` / `fct_pr_cmpt_component_type` | "empty" | **25 and 15 rows.** The engine event cache INNER JOINs `ce` (DBX:342, 390), so an event whose `(type, event)` pair is missing from `ce` never runs. `sef` also has an FK to `ce`, and `sf` has an FK to `cmpt`. |
| Component types | 0013 = mobile widget, 0014 = list view | **0013 and 0014 do not exist** (the FK would reject them). Real ids: 0006 AutoSelect, 0007 DropdownGrid, 0008 Multiple Selection Combobox, 0009 Grid Input Selection, 0010 Readable Elements, 0011 Auto, 0012 Dropdown with Grid, 0015 Alert Search, 0256 DDF8+Alert Search |
| Events 0000/0016–0019 | "calendar, swipe, condition, fixed combo" | 0016 Mobile Calendar Date, **0017 SearchAndRowClick**, 0018 Swipe-Left, 0019 Swipe-Right. Also: 0000/0003 Refresh, **0000/0021 File Upload**, 0015/0001 Fill Single Alert |
| Assertion sheet in `psef_fixed_value` | on assertion events (0013) | **0013 never carries a sheet** (543 `TSTMSG`, 92 `ELEVLD`, 8 `ELEVAL`, 2 NULL). The `<TYPE>,<Sheet>` form is on **0014 Group Assertion** (all 497 rows) |
| `psef_ref_serialno` | not described | Controls whether an event runs, see §2.3 |
| Test types | — | `fct_pr_tt_test_type`: 1 Regression Suite (G), **2 Smoke Suite (S)**, 3 Performance Suite (G). The flow UI lists only `S` types, so `ptt_testtypeid='2'` for flows (546/547 rows); group flows default to Regression Suite '1' |

## 1. How the UI builds each row

All saves go through `DBX.upsertDynamicRow` (DBX:572-650). It runs `SELECT COUNT(*) WHERE <checkColumns>`, then an UPDATE if a row exists and an INSERT if not. **Every value is trimmed, `''` becomes NULL, and every value is sent as a quoted string** (DBX:584). Audit values on the UI path are always: `created_by='Regress Master'` and `create_date` = a `"yyyy-MM-dd HH:mm:ss.SSS +0500"` string on insert; `modified_*` stays **NULL on insert** and is set only on edit. `master_app_id` = config `app.id` (`BaseTest.selectedApp`, BaseTest.java:52) and is **written only when that config value is non-empty**. The team's install has it empty: every row created in 2026-09 has `master_app_id` NULL.

| Table | Id rule (code) | Defaults / filled columns |
|---|---|---|
| `fct_pr_mg_menu_group` | Auto: `MAX(pmg_menugroupid) WHERE LIKE '0___'` + 1, zero-padded to 4 digits (DBX:516-529, U/NewMenuGroup.java:471-476). "Manual" is ticked by default and requires ≥4 chars (:392). The insert happens only when the id is exactly 4 chars (:442) | `pmg_navigation_type='id'` (:310). The form shows description, searchtext, navigation and navigation_type. **No required-field check** (the check is commented out, :397-402) |
| `fct_pr_sc_screens` | `<4-char menugroup><2-digit>`: `MAX(psc_screenid) LIKE '<mg>%'` + 1, same width; `<mg>01` if none (DBX:501-514, U/CopyScreen.java:287-296) | `psc_screentype` from `Save, Update, Delete, Forward, Reject` (U/NewScreen.java:41), default `Save`. Required: id, name, type (:184-195) |
| `fct_pr_mgsm_…_mapping` | `pmgsm_sequenceno` is typed or pasted (paste = grid max+1) | Rows with an empty sequence are **skipped** (U/ScreenMapping.java:333). `pmgsm_parent_screenid` is taken from the `"id-name"` dropdown and cut at `-` (:371-374); blank = top level. `pmgsm_status` has DB default `'Y'`. navigation_type/path stay NULL for top-level screens; tab children use `id` / `tab_N` (live 0612) |
| `fct_pr_sf_screen_field` | `psef_serialno` comes from the DB sequence (the key is removed when blank, U/ScreenFields.java:371-372). `psf_sequenceno` is typed or pasted | First-row defaults: `psf_sequenceno 1, prv_version '1.0', psf_locateby 'id', psf_field_status 'Y', psf_field_addition '+', psf_iteration_number 1` (:235-240). Required: component type, locateby, fieldid, sequenceno, field_db_column (:347-366). `psf_mandatory_field` ∈ {`Y`, NULL}; `psf_field_source` ∈ {EXCEL, REPO, FIXED, NULL} (NULL counts as EXCEL, LocatorMappingManager.java:77). The engine loads only `psf_field_status='Y'` fields |
| `fct_pr_sef_screen_events_flow` | `psef_serialno` is **per screen** (PK screen+serial). The user types the first one; pasted rows get grid max+1 for **both** serialno and sequenceno (FT:343-403) | First-row defaults: `psef_sequenceno 1, psef_locateby 'id', psef_status 'Y'` (U/ScreenEventsFlow.java:214-217). **`psef_desc` = the component-event description** (`Load Data`, `Click`, `Assertion`…) (:437-449). **`psef_ref_serialno` = serial of the nearest preceding `Load Data` row**; NULL on Load Data rows and on rows before any Load Data (:411-434). Required: desc, component event, sequenceno (:503-522). `psef_fixedvalue_type` ∈ {EXCEL, REPO, FIXED, ''}. Assertion `fixed_value` ∈ {TSTMSG, ELEVLD, ELEVAL} |
| `fct_pr_tf_test_flow` | `(first 4 chars of MAX(ptf_testflowid)) + 1`, padded to 4, then `'0001'` (U/TestFlow.java:177-198). **It is not derived from the menu-group id**; the two stay in step only by habit | `ptf_status 'Y'` (:273). `ptt_testtypeid` = the id of the chosen type description (S types only → '2'). `ptf_platform` NULL. Required: id, description |
| `fct_pr_tfd_test_flow_details` | `ptfd_sequenceno` is typed | The UI edits **one row per flow** (reads only the first detail, U/TestFlowDetail.java:89) and **cannot set `ptfd_filename`**: the column is not in the row map (:90-103). The 3 newest rows (0610-0612) have `ptfd_filename='NG_Dcode_QA_SDMS-10080'`, so the team sets it with SQL or another build |
| `fct_pr_gtf_group_test_flow` | `MAX(pgtf_grouptestflowid)+1`, **unpadded** (U/GroupTestFlow.java:176-191). Ids today: 1…84 | `ptgf_status='A'` always (:235); default type Regression Suite ('1', :269). Required: id, description |
| `fct_pr_gtfd_…_detail` | `pgtfd_sequenceno` is typed or pasted | New row: `pgtfd_sequenceno 1, pgtfd_status 'Y', plu_serial_no 1, pgtf_testflow_login_status 'Y'` (U/GroupTestFlowDetail.java:115-122). `pgtf_testflow_appid` is hidden, so NULL (web). The user dropdown shows `"serial-name"` and stores the serial (FT:472) |
| `fct_pr_lu_login_users` | `plu_serial_no` = max over the **visible (master-app-filtered) users** + 1 (U/LoginUser.java:132-146, filter :55-58) | Required: name, password. `plu_status` and `plu_approval_status` come from the Y/N dropdowns |
| `fct_pr_alg_app_allowable_groups` | `id` bigint sequence; PK (app, group) | Every row is re-upserted on every save, keyed on `id` (U/AllowableGroups.java:141) |
| `fct_pr_app_application` | Typed id if it exists, else max+1 (U/ApplicationUtlity.java:156-176) | `papp_master_id = app.id` config when set (:182-183) |
| `fct_pr_sq_screen_query` | **No authoring UI.** Rows are written by hand | Read by `ScreenQuery.java:29-35` (latest `prv_version`, `psv_isverification` NULL→N, `psq_validationtype` NULL→SCREEN) |

## 2. Insert order, cascades, engine coupling

1. **Order the UI forces** (each tab needs the parent in its dropdown): menu group → screen → mapping → fields → events → flow → flow detail → group → group detail (→ allowable group). FKs: `mgsm→mg,sc`; `sf→sc,cmpt,rv`; `sef→sc,ce`; `tfd→tf,mg`; `gtfd→gtf,tf,lu`; `alg→app,gtf`. `framework.sql` inserts `sc` before `mgsm`, `tf` before `tfd`, and `sf`/`sef` after `sc`, which is valid.
2. **No cascades on "new screen".** Creating a screen writes only `fct_pr_sc_screens`. Mapping is a separate tab.
3. **Copy Screen** (U/CopyScreen.java:232-249) makes three separate autocommit writes:
   - The screen row is rebuilt from a read-only TextArea of the source (`Key: value` lines, :325-352), with new id, name, `created_by='Regress Master'` and `create_date` added.
   - Fields: `SELECT *` from the source, `psc_screenid` swapped, `psef_serialno` dropped (the sequence assigns it). **Source audit, `psf_app_ids` and everything else are kept verbatim.** Live 061201's fields still say `created_by='Admin'`, 2024-05-09.
   - Events: copied verbatim, **including `psef_serialno`, `psef_ref_serialno`, `psef_status` and audit** (:267-276).
   - No mapping row is copied.
4. **How the engine consumes `psef_ref_serialno`.** Events with ref NULL/0 are top level (DBX:73-74, `getInt` turns NULL into 0). Events with ref = N run as children of event N: under a Load Data loop (Main:932), under an assertion that failed (Main:3089, 3549), or under a condition (Main:3585). **An event whose ref points at a Click never runs.** Live data: 610 of 645 active 0013 assertions have ref = the last Load Data serial.
5. **The event cache is loaded once per JVM** (static block, DBX:374-380) and refreshed only per screen by `updateScreenEventsCache`. Apply SQL **before** starting the runner. A `psef_desc` NULL on an active row throws an NPE at DBX:361 inside the loader. The static block swallows it, so **every event after that row is missing** from the cache.
6. **Top-level screens** are the `mgsm` rows with `pmgsm_parent_screenid IS NULL` and `pmgsm_status` NULL or 'Y', ordered by `pmgsm_sequenceno` (DBX:19-24).

## 3. Validation the SQL must respect (UI rules + DB constraints)

- **PKs:** `mg(pmg_menugroupid)`, `sc(psc_screenid)`, `mgsm(mg, sc, seq)`, `sf(sc, fieldid, prv_version, psf_sequenceno, psf_iteration_number)`, `sef(sc, psef_serialno)`, `tf(id)`, `tfd(tf, mg, seq)`, `gtf(id)`, `gtfd(seq, tf, gtf)`, `lu(plu_serial_no)`, `alg(app, gtf)`, `sq(sc, prv_version, psn_serialno)`.
- **NOT NULL:** `sf.prv_version` (FK to `fct_pr_rv_release_version`: 1.0/2.0/3.0), `sf.psf_sequenceno`, `sf.psf_iteration_number` (default 1), `sef.psef_serialno`, `lu.plu_name`, `lu.papp_app_id`, `gtfd.pgtfd_sequenceno`.
- **Lengths:** ids varchar(10) (`master_app_id` 5); `psc_screenname` 50; `psf_field_db_column` 50; `psef_fixed_value` 200; `psef_desc` 100; `psef_locateby` 100; `psef_fixedvalue_type` 10; `psf_fieldid`/`psef_fieldid` 1000; `created_by` 50; `pmgsm_navigation_type` 10. The case-data sheet name must be **≤ 31 chars** (Excel limit) even though `psc_screenname` allows 50.
- **UI-enforced:** screen name unique per menu group, case-insensitive (Copy Screen only, U/CopyScreen.java:225-229). Screen type in the list above. Every `sef` row needs a non-empty `psef_desc` and a sequenceno. `(type, event)` must exist in `ce`. `pcmpt_componenttypeid` of a field must exist in `cmpt`. Y/N flags are upper-case.
- **Values are stored trimmed, and `''` is stored as NULL** (DBX:584): never emit empty strings.

## 4. Case-data workbook and `ExcelFileCreater`

`util/writer/ExcelFileCreater.java` is **not a template generator. It is the result log writer.** It writes one sheet per screen, renamed `<eventCount>-<testflowid>_<screen>[_error]` (:476-478), with headers `PK | Event ID | Message | Status | Screenshot` (:432-436). No code in the framework creates case-data templates (the only `createSheet` is :397). The case-data contract is therefore only what `ExcelReader`/`Main` read (already in the map, §5).

`gen_framework_sql.py` matches that contract:
- sheet = `psc_screenname` ("Van Sale Stock Request");
- field headers = `psf_field_db_column`;
- control columns `PK`, `PK_DESC`, `EXPECTED_MESSAGE`, `CASE_TYPE` (`TN`), `STPONERR` (`N`);
- `PK` written as the text `01`.

Header order is free (the header is looked up by name). Missing guards: sheet name ≤31 chars, and `CHECK_VALIDATION='Y'` when 0007/0005 events exist.

## 5. Group test flow, login users, distributor

- A group row links a user through `gtfd.plu_serial_no` → `lu.plu_serial_no`, a global integer that is not unique per app (FK `fk_plu_serial_no`).
- The runner (DBX:103-129) takes `gtfd` rows with `pgtfd_status='Y'` ordered by `pgtfd_sequenceno`. It LEFT JOINs `tfd`, so a flow with N `tfd` rows runs N times.
- If `pgtf_testflow_login_status` is **not NULL and not 'N'**, it logs out and back in as that user (Main:389-392).
- `plu_approval_status.equals("N")` NPEs when NULL (Main:401); the NPE is swallowed.
- `plu_status` is **never checked** at run time.
- `pgtf_testflow_appid` non-NULL switches the driver to that app (mobile) (Main:365-376).
- Live data: `login_status` Y 506 / N 180 / NULL 343; `plu_serial_no` NULL on 560 of 1,029 rows (no re-login).
- **Distributor.** There is no company column. Config `with.distributor=USER:DIST,…` (Symbols.WITH_DISTRIBUTOR, Main:182-190), keyed by upper-case `plu_name`. When a user matches, the runner sets repo `g_SELECTED_DIST` and runs **menu group 9999 / screen 9999** events to pick the distributor (Main:406-412, 471-478). A generated group must not reuse or alter 9999.
- A new group needs `gtf` + `gtfd` + an `alg` row for the app id, or the Group dropdown will not list it (FC:162).

## 6. `gen_framework_sql.py` / `framework.sql` compared with the UI

| # | Item | Generator / sample | UI / live practice | Fix in `gen_framework_sql.py` |
|---|---|---|---|---|
| 1 | **Ids already taken** | mg `0612`, sc `061201`, tf `06120001` (generated 09-28) | A tester created 0612 / 061201-061206 / 06120001 on **2026-09-29** | The pre-flight guard will abort, so regenerate. Compute ids from live max at generation time with the UI rules (mg = max `'0___'`+1; sc = `<mg>`+`01`; tf = `lpad(left(max tf,4)::int+1,4,'0')`+`'0001'`, not `<mg>0001`). Keep the guard. Better: lock and assign inside the DO block (`LOCK TABLE … IN EXCLUSIVE MODE`, then compute max+1) |
| 2 | **Assertion `psef_ref_serialno`** | event 4 (0000/0013) ref = **3** (a Click) | ref = the last preceding Load Data serial (**1**); 610/645 live | Derive ref automatically: every non-Load-Data event gets the serial of the latest preceding `0000/0001`, or NULL. With ref=3 the assertion **never runs** (§2.4) |
| 3 | `modified_date` / `modified_by` | `now()` / tag on insert | NULL on insert | Drop them from `audit` on INSERT |
| 4 | `created_by` | `QAOS-<story>` | `'Regress Master'` | Keep the tag (the engine never reads audit columns and the rollback relies on it), but record this as a deliberate deviation. `create_date` = `now()` is fine (timestamptz) |
| 5 | `master_app_id` | `'1'` on mg/sc/tf | NULL in the team's install (`app.id` unset); `'1'` only where a tester had `app.id=1` | Take it from the spec with default NULL. A value hides the rows from UI users whose `app.id` differs (FC:218, 287, 445) |
| 6 | Empty strings, whitespace | `q()` keeps `''` and spaces | trimmed; `''` → NULL | In `q()`: `v = str(v).strip(); return 'NULL' if v == '' else …` |
| 7 | `psef_desc` NULL guard | not enforced | required; NULL breaks the engine cache (§2.5) | Assert non-empty. Default to the `ce.pce_description` of the event (UI behaviour) |
| 8 | `(type, event)` / field type validity | not checked | FK to `ce` / `cmpt` | Hard-code the 25 `ce` pairs and 15 `cmpt` ids, and reject others (e.g. 0013/0014 as field types) |
| 9 | `psef_fixedvalue_type` | never set | `EXCEL` / `REPO` / `FIXED` on single-field fills (0001/0001, 0002/0001; 704/731 set) | Set it when an event fills a single field. The sample needs none (fields are filled by Load Data) |
| 10 | Assertion `fixed_value` | `'TSTMSG'` | fine for 0013; 0014 needs `TSTMSG,<Sheet>` | Validate: 0013 ∈ {TSTMSG, ELEVLD, ELEVAL}; 0014 must match `^(TSTMSG\|ELEVAL\|ELEVLD),.+` |
| 11 | Group run support | no `gtf`/`gtfd`/`alg` rows | a group needs `gtf` (status 'A', type '1') + `gtfd` (seq, status 'Y', `plu_serial_no`, login_status 'Y' on the first flow) + `alg(app, gtf)` | Add optional `group{id, description, user_serial, app_id}` to the spec. Never write `lu` (passwords are entered by the QA member) |
| 12 | Case-data sheet name | no length check | ≤31 chars | Assert `len(sheet) <= 31` and `sheet == screen.name` |
| 13 | Menu-group navigation / screen type | `'id'`, `'Save'` | same defaults | OK. Also validate screen type ∈ {Save, Update, Delete, Forward, Reject} |
| 14 | `mgsm` / `tfd` filename | mgsm NULL, tfd set | same as live 0610-0612 | OK |
| 15 | `sf` columns | `prv_version '1.0'`, `'+'`, status Y, iteration 1, serial omitted | same | OK. `psf_mandatory_field` must be `'Y'` or NULL, never `'N'` |

## 7. Defects in the authoring code (ranked)

1. **Id collisions become silent overwrites.**
   - Every id is read-max-then-write with no lock or sequence, and the save is an **upsert**, so a colliding id UPDATEs the existing row instead of failing.
   - Lexical `MAX` on varchar ids will break: the group id after `'99'` stays `'100'` for ever (U/GroupTestFlow.java:176-191, DBX:712-726); menu groups past `0999` are invisible to `LIKE '0___'` (DBX:519).
   - The login-user serial is max+1 over **only the current master-app's users** (U/LoginUser.java:55-58, 132-146) and is upserted on `plu_serial_no` (:156, :167), so it can **overwrite another app's user and password**.
2. **Upsert key ≠ table PK, or a wrong status key.**
   - The `tfd` upsert keys on (flow, seq) without the menu group (U/TestFlowDetail.java:181).
   - The `mgsm` upsert keys on (mg, seq) without the screen (U/ScreenMapping.java:348), so remapping a sequence overwrites a different screen's row.
   - GroupTestFlow checks the row status with key `ptf_testflowid`, which does not exist in that grid (U/GroupTestFlow.java:203). Every row counts as "new", so `created_by`/`create_date` are rewritten on every save.
3. **Paste renumbers real ids.** Pasted rows get grid max+1 in every column whose name contains `serial`, `seq` or `testflowid` (FT:343-351, 399-404). That includes `ptf_testflowid` in the Group Test Flow Detail grid (a pasted flow reference becomes a different flow) and `sf.psef_serialno` (bypasses the DB sequence, so later `nextval` duplicates serials).
4. **No transactions.** Multi-table and multi-row saves are separate autocommit statements (no `setAutoCommit`/`commit` anywhere). Copy Screen can leave a screen without fields or events (U/CopyScreen.java:235-239).
5. **Swallowed failures reported as success.**
   - `upsertDynamicRow` returns false after `printStackTrace` (DBX:646-649), and the events and fields tabs ignore that return, then show "Changes Saved" (U/ScreenEventsFlow.java:526, U/ScreenFields.java:374).
   - The copy helpers swallow errors (U/CopyScreen.java:280-284, 390-394).
   - TestFlowDetail saves only the first row and shows "Changes Saved" before checking the result (U/TestFlowDetail.java:182-184).
6. **SQL built by string concatenation throughout.**
   - `deleteRow` does not escape key values (DBX:949-966).
   - The selects are unescaped, e.g. `getMaxScreenId` (DBX:504), `getEventIdsByDesc`, `FC.getUserPassword` (FC:203, by user name).
   - Table and column names are raw in `upsertDynamicRow`.
   - A quote in a locator or description breaks deletes and lookups. Any grid value is an injection vector.
   - Related: `plu_password` is selected (FC:495) and **shown in plain text** in the Login Users grid (not in hiddenColumns, U/LoginUser.java:33).
7. **Over-broad delete.** Mapping delete keys on (screen, seq) with no menu group (U/ScreenMapping.java:283), so it deletes that screen's mapping in every menu group. All deletes are hard deletes with no FK pre-check (FT:906-944).
8. **Stale, hard-coded timestamps.** `NewMenuGroup.formattedDate` is static, computed once at class load (U/NewMenuGroup.java:238-239), and reused by Copy Screen (U/CopyScreen.java:22, 320). Every other tab freezes its time when the tab is built. The offset is always +05 (e.g. :36-37). Live proof: mg 0612 and screens 061201-061206 all have `13:15:14.086`.
9. **Test Flow Detail handles only a single row.**
   - It reads only the first detail (U/TestFlowDetail.java:89).
   - The new-row default puts `"1"` into result column 12 (`pmg_menugroupid`) (:102).
   - `ptfd_filename` cannot be set.
   - The save returns after the first row (:184).
10. **Empty-table sentinel rows.** `getAllByScreenIdAndTableName` returns one all-NULL row when a table is empty (DBX:296-305). Copy Screen then tries to insert it (it fails on NOT NULL, and the error is swallowed). The UI also depends on `isRowEmpty` sentinels to seed new grids, which makes it easy to save half-filled rows.
