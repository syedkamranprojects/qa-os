---
name: regress-casedata-contract
description: "How the legacy Regress engine (NGSelenium-Testing + CTA_CONFIG_ASSERTION) reads bulk case data - file path, sheet and header rules - which bulk-data-factory must produce."
metadata:
  node_type: memory
  type: reference
  originSessionId: eb4a66f7-6654-4151-a641-fe8df7bda0d6
  modified: 2026-09-25T07:37:27.351Z
---

Verified 2026-09-25 from engine source `C:\git-projects\NGSelenium-Testing\Elements\src\main\java\com.centegy.selenium\Main.java`
(`resolveFilePathForExcelCaseData`, around line 3992; file-name resolution around line 1025) and `util\reader\ExcelReader.java`,
plus the `CTA_CONFIG_ASSERTION` DB (reached via the `selenium-framework-db` MCP):

- **File:** `<BASE_PATH>\casedata\<fileName>.xlsx`. BASE_PATH = config `BASEPATH_<appId>`, else `fct_pr_app_application.papp_base_path`
  (e.g. `D:\Selenium\Automation\PHP_QA\`).
- **fileName:** `fct_pr_tfd_test_flow_details.ptfd_filename`, else `fct_pr_mgsm_menu_group_screen_mapping.pmgsm_screen_filename`, else the app default.
  Existing names: NG_Dcode_QA_OTC, NG_Dcode_QA_Setup, NG_Dcode_QA_OTC_Negative, NG_Dcode_QA_Promotion, NG_Dcode_QA_SDMS-10080.
- **Sheets:** one per screen, named `fct_pr_sc_screens.psc_screenname`.
- **Header row:** row 0, case-insensitive. Field columns = `fct_pr_sf_screen_field.psf_field_db_column`. Control columns: PK (PK#2… for repeated loads),
  PK_DESC, STPONERR, CASE_TYPE, EXPECTED_INPUT, EXPECTED_MESSAGE, CHECK_VALIDATION, EVENT_ID, SWIPE, repo_*.
- **Rows:** one row = one case iteration; empty rows are skipped; PK links parent and child screen sheets.

This is the data contract for QA OS bulk-data-factory (design §13A). The user's QA team wants bulk data generated per story or test case; it is used only
by the legacy engine after scripts are generated, never during AI execution (one row per case there).
Control-column semantics, read from `Main.java` and `assertions\ExpectedOutcome.java` on 2026-09-25:
- **PK:** default "01". PK#n is used for repeated loads. PK_DESC is cached as "PK - desc".
- **STPONERR:** Y = stop at the first error.
- **CASE_TYPE:** TP = expect success, TN = expect rejection. A blank value is treated as TN in the event checks but as TP in the ELEVLD check, so always fill it.
- **EXPECTED_MESSAGE:** compared with toast (TSTMSG) or element text (ELEVAL); a `#` in the value means a pattern match; blank = no message expected.
- **EXPECTED_INPUT:** INVALID_INPUT checks aria-invalid; REQ_FIELD checks aria-required plus aria-invalid on mandatory fields.
- **Per-field variants:** `<db_column>_CASE_TYPE`, `<db_column>_EXPECTED_MESSAGE`, `<db_column>_EXPECTED_INPUT`.
- **CHECK_VALIDATION:** Y enables validation on component events 0005/0007.
- **EVENT_ID:** format `<x>:<serial>`; picks the conditional event. **SWIPE:** mobile only.

Resolved from `Main.java` (around lines 2916–2946): the component events are on the system component type `0000`.
- `0000/0007` = **Validation**: `dataValidation(...)` using `psef_validationtype`.
- `0000/0005` = **Data Verification**: `dataVerificationNewEvent(..., "Q2Q")`, a query-to-query DB check (see `fct_pr_sq_screen_query`).

Both run only when the row has CHECK_VALIDATION=Y. Component types seen in code: 0001 text, 0002 dropdown, 0003 datepicker, 0006 autoSelect,
0010 repo field, 0007/0008/0009/0012 web widgets, 0013 mobile.

**Verified with real samples (2026-09-25):** `qa-os/framework/casedata-samples/NG_Dcode_QA_OTC*.xlsx` (default/Bangla/PHP/Pak/Vietnam), profiled by
`qa-os/framework/tools/analyse_casedata.py`. The full contract is in `qa-os/framework/cta_config_assertion.md` §5.1. Key corrections and additions:
- **CASE_TYPE:** it is NOT positive vs negative. The team uses TN almost always (765 vs 4). TP only enables the ELEVLD input check. Default to TN.
- **PK:** hierarchical (01 → 01-01, 01-02), matched by prefix both ways.
- **Assertion sheets** are named in `psef_fixed_value` as "TSTMSG|ELEVAL|ELEVLD,<Sheet>", conventionally ending `_ASSR`.
- **GLOBAL-REPO sheet:** REPOID/REPOVALUE.
- **Headers** are mostly captions.
- **Dates:** yyyy-mm-dd text. **Dropdowns:** "code - description".
- **Usage:** EXPECTED_MESSAGE is exact toast text (varies per screen); STPONERR always N; CHECK_VALIDATION Y is common; EVENT_ID/SWIPE are unused.
See [[snd-test-automation-project]], [[no-docs-learn-from-metadata]].
