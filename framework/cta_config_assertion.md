# CTA_CONFIG_ASSERTION: schema map for script-generator and bulk-data-factory

**Target of generated scripts:** the legacy Regress engine = `C:\git-projects\NGSelenium-Testing`, branch
`appium_development` (commit `af79ecd`, 2026-06-10), the version the QA team runs.

**Access:** MCP connector `selenium-framework-db`, PostgreSQL `CTA_CONFIG_ASSERTION`, 21 tables. Read-only;
writes happen only through reviewed `framework.sql` applied by a Framework admin.

Everything here was verified on 2026-09-25 from the live DB and the engine source (`Main.java`,
`UI/Tab/DB/DBExecution.java`, `util/reader/ExcelReader.java`, `assertions/ExpectedOutcome.java`).

## 1. Table relationships

```
fct_pr_app_application (papp_app_id, papp_base_path, ptf_testflowid_login/_logout)
  └─ fct_pr_lu_login_users (papp_app_id, plu_serial_no, plu_name, plu_password, …)

fct_pr_gtf_group_test_flow (pgtf_grouptestflowid, ptt_testtypeid)          ← a suite
  ├─ fct_pr_gtfd_group_test_flow_detail (pgtfd_sequenceno → ptf_testflowid, plu_serial_no, pgtf_testflow_appid)
  └─ fct_pr_alg_app_allowable_groups (papp_app_id ↔ pgtf_grouptestflowid)

fct_pr_tf_test_flow (ptf_testflowid, ptf_description, ptf_status, master_app_id)   ← one flow
  └─ fct_pr_tfd_test_flow_details (ptfd_sequenceno → pmg_menugroupid, ptfd_filename = case-data workbook)
        └─ fct_pr_mg_menu_group (pmg_menugroupid, pmg_searchtext, pmg_navigation, pmg_navigation_type)
              └─ fct_pr_mgsm_menu_group_screen_mapping (pmgsm_sequenceno → psc_screenid, pmgsm_parent_screenid,
                                                        pmgsm_screen_filename, pmgsm_status)
                    └─ fct_pr_sc_screens (psc_screenid, psc_screenname = case-data SHEET name)
                          ├─ fct_pr_sf_screen_field (psf_fieldid, psf_locateby, psf_field_db_column = case-data COLUMN,
                          │                          pcmpt_componenttypeid, psf_mandatory_field, psf_assertion_type, …)
                          ├─ fct_pr_sef_screen_events_flow (psef_serialno, psef_sequenceno, pcmpt_componenttypeid,
                          │                                 pce_comp_event, psef_locateby, psef_fieldid, psef_fixed_value,
                          │                                 psef_status — only 'Y' runs, psef_ref_serialno, psef_condition_statement)
                          └─ fct_pr_sq_screen_query (psq_query, psq_qryparameters, psq_query_target, psv_isverification)
Results: test_execution (16k rows), fct_rp_set_screen_event_toast
```

## 2. Navigation (matches QA OS `navigate`)

| Column | Meaning | Example |
|---|---|---|
| `pmg_searchtext` | Text typed in the menu search | `Order Booking` |
| `pmg_navigation` | The `li` id to click = S&D `optionGroupId` | `ORDER_BOOKING`, `DYL_102014` |
| `pmg_navigation_type` | Locator type | `id` |

A QA OS step `navigate "Transaction > SKU Substitution Policy"` maps to `pmg_searchtext='SKU Substitution Policy'`,
`pmg_navigation='SKU_SUBSTITUTION_POLICY'`, `pmg_navigation_type='id'`.

## 3. Component types (`pcmpt_componenttypeid`)

The `fct_pr_cmpt_component_type` / `fct_pr_ce_component_event` tables are empty; meanings come from the engine source.

| Id | Widget | Id | Widget |
|---|---|---|---|
| `0000` | system / non-UI event | `0006` | auto-select |
| `0001` | text box | `0010` | repository-sourced field |
| `0002` | dropdown | `0013` | mobile widget |
| `0003` | date picker | `0014` | list view |
| `0004` | button / clickable | `0015` | alert (click) |
| `0005` | alert (accept) | `0007`, `0008`, `0009`, `0012` | web widgets (exact kinds to confirm in P3) |

## 4. Event codes (`pce_comp_event`) and live usage

| Type / event | Meaning (engine comment) | Rows in DB |
|---|---|---|
| `0004/0002` (`0003` = long click) | Click | 4,244 |
| `0000/0001` | Load data (fill fields from the case-data row) | 1,153 |
| `0001/0001` | Fill text field | 892 |
| `0000/0013` | Assertion (uses `CASE_TYPE` / `EXPECTED_*`) | 740 |
| `0000/0014` | Group assertion | 560 |
| `0000/0007` | Validation (runs only if `CHECK_VALIDATION = Y`) | 445 |
| `0000/0006` | Wait | 414 |
| `0000/0012` | Fill repository values | 171 |
| `0000/0025` | Frame switch (web) | 144 |
| `0005/0002` | Accept alert | 64 |
| `0000/0023` | Flow-control assertion | 49 |
| `0000/0004` | Toast message check | 46 |
| `0002/0001` | Fill dropdown | 30 |
| `0000/0005` | Data verification, query-to-query (`fct_pr_sq_screen_query`; only if `CHECK_VALIDATION = Y`) | 30 |
| `0000/0015` | Checkbox click | 4 |
| `0000/0002` | Verification | — |
| `0000/0016`–`0019` | Mobile: calendar, swipe, condition, fixed combo | — |

Only `psef_status = 'Y'` rows run; the engine filters `IN ('Y','A')`, and `A` is unused.

## 5. Case-data workbook (bulk data), read by `util/reader/ExcelReader.java`

| Aspect | Rule |
|---|---|
| **Path** | `<BASE_PATH>\casedata\<fileName>.xlsx`. `BASE_PATH` = config `BASEPATH_<appId>`, else `fct_pr_app_application.papp_base_path` (e.g. `D:\Selenium\Automation\PHP_QA\`) |
| **File name** | `fct_pr_tfd_test_flow_details.ptfd_filename`, else `pmgsm_screen_filename`, else the app default. Existing: `NG_Dcode_QA_OTC`, `NG_Dcode_QA_Setup`, `NG_Dcode_QA_OTC_Negative`, `NG_Dcode_QA_OTC_AfterGIN`, `NG_Dcode_QA_Promotion`, `NG_Dcode_QA_SDMS-10080` |
| **Sheets** | One per screen, named `psc_screenname` |
| **Header** | Row 1, case-insensitive. Field columns = `psf_field_db_column`, plus control columns |

**Control columns:**

| Column | Meaning |
|---|---|
| `PK` (`PK#2`… for repeated loads) | Row id, default `01`; links parent and child screen sheets |
| `PK_DESC` | Row label, cached as "PK - desc" |
| `STPONERR` | `Y` = stop at the first error |
| `CASE_TYPE` | `TP`/`TN`. It only controls the `ELEVLD` input-validation check; see §5.1: the team uses `TN` almost everywhere. A blank counts as `TN` in event assertions but as `TP` in `ELEVLD`, so always fill it |
| `EXPECTED_MESSAGE` | Toast (`TSTMSG`) or element text (`ELEVAL`); `#` in the value = pattern match; blank = no message expected |
| `EXPECTED_INPUT` | `INVALID_INPUT` (fields flagged `aria-invalid`) or `REQ_FIELD` (mandatory fields flagged `aria-required` + `aria-invalid`) |
| `<db_column>_CASE_TYPE`, `<db_column>_EXPECTED_MESSAGE`, `<db_column>_EXPECTED_INPUT` | The same checks for one field |
| `CHECK_VALIDATION` | `Y` enables events `0000/0007` and `0000/0005` for the row |
| `EVENT_ID` | `<x>:<serial>`; picks the conditional event to run |
| `SWIPE` | Mobile only |
| `repo_*` | Repository-sourced values |

### 5.1 Verified against real workbooks (2026-09-25)

**Samples:** `casedata-samples/NG_Dcode_QA_OTC*.xlsx` (default, Bangla, PHP, Pak, Vietnam), 924 sheets and 1,457 data rows in total.
**Tools:** profile with `tools/analyse_casedata.py`; full per-sheet profile in `casedata_profile.json`, report in `casedata_profile.md`.

| Topic | What the team actually does |
|---|---|
| **Sheet names** | **Two sources:** (1) `psc_screenname` for screen data. (2) **Assertion sheets** named in the assertion event's `psef_fixed_value` as `<TSTMSG\|ELEVAL\|ELEVLD>,<SheetName>` (559 events). By convention these end in `_ASSR` (e.g. `ORD_BOOK_SAVE_ASSR`, `DA_FORWARD_ASSR`). Sheets like `Order Booking_BD (2)` are referenced by nothing and look like leftover copies |
| **`GLOBAL-REPO` sheet** | Columns `REPOID`, `REPOVALUE`. Global repository values, read from the app's default case-data file at start-up (`Main.ReadGlobalRepo`) |
| **`PK`** | Hierarchical: header rows `01`, `02`…; detail/child rows `01-01`, `01-02`… Matching is **prefix-based in both directions** (`isPkFound`: row PK startsWith pk or pk startsWith row PK), so one header row drives all its `01-nn` detail lines. `01` is used in 566 rows, `01-01` in 268 |
| **`PK_DESC`** | Free text naming the case, e.g. `OB Positive 01-01`, `DA Positive Case 01` |
| **`CASE_TYPE`** | **Almost always `TN`** (765 rows, vs 4 `TP`), including for positive "save succeeds" rows. **Correction to §5:** `CASE_TYPE` does *not* mean positive vs negative. `TP` (or blank) turns on the `ELEVLD` input-validation check driven by `EXPECTED_INPUT`; `TN` skips it. Message assertions (`TSTMSG`/`ELEVAL`) run either way. **Generate `TN` by default; use `TP` only for rows that assert field validation.** |
| **`EXPECTED_MESSAGE`** | Exact toast text, e.g. `Saved successfully` ×65, `Forwarded successfully` ×61, `Order Save successfully` ×42, `Record Saved Successfully!` ×40, `Process completed successfully` ×19. Wording differs per screen, so it has to be observed, never guessed |
| **`STPONERR`** | Always `N` in the samples |
| **`CHECK_VALIDATION`** | `Y` in 592 rows: validation and query-to-query data verification are widely used |
| **`EXPECTED_INPUT`** | Header present in 44 sheets, never filled in |
| **`EVENT_ID`, `SWIPE`, per-field `<col>_*` columns** | Not used in the samples |
| **Field headers** | Exactly the `psf_field_db_column` text: mostly **captions** (`Outlet Name`, `Stock Type`, `Bank Branch`, `Deposit Amount`); some DB column names (`epp2_reference_1`, `DDL__pccy_ctrycty_code`) |
| **Dates** | Text `yyyy-mm-dd` (257 cells), sometimes `dd-mm-yyyy` (74). Match the widget; S&D DevExtreme date boxes use `yyyy-mm-dd` |
| **Dropdowns** | Often the display text `code - description` (e.g. `0001 - Value Added Tax`), as shown in the dropdown |
| **Region variants** | One workbook per region with the same file stem (`NG_Dcode_QA_OTC (PHP).xlsx`, `(Pak)`, `(Bangla)`, `(Vietnam)`). Copied to the runner's `casedata\` under the name the flow expects |

**Rules for bulk-data-factory:**
- Write one sheet per screen (`psc_screenname`), plus the `_ASSR` sheets that the flow's assertion events name.
- Use hierarchical `PK`s (`01`, then `01-01`…).
- Set `CASE_TYPE` to `TN` unless the row asserts input validation.
- Fill `EXPECTED_MESSAGE` only with text observed in the live one-row run.
- Set `STPONERR=N`, and `CHECK_VALIDATION=Y` when the flow has `0000/0007` or `0000/0005` events.
- Use field headers exactly as `psf_field_db_column`, dates as `yyyy-mm-dd`, and dropdown values as displayed.
- Create or refresh `GLOBAL-REPO` only when the flow uses repository fields.

## 6. Apps and bases (`fct_pr_app_application`)

16 app rows. Examples:

| App id | Name | Base path |
|---|---|---|
| 1 | PK_Centegy | (no base path; 183 flows) |
| 3 | GIS CLASSIC | `D:\Selenium\Automation\GIS_QA\` |
| 6 | PHP_CentegyQA | `D:\Selenium\Automation\PHP_QA\` (likely the PH region) |
| 7 | BD_Centegy QA | |
| 16 | VN_Centegy QA | |
| 17 | KH_Centegy QA | |
| 18 | LA_Centegy QA | |

Which app id S&D PH flows should use is **to be confirmed** before P3.
