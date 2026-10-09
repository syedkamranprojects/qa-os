# Legacy Regress engine: runtime review

Source: `C:\git-projects\NGSelenium-Testing\Elements\src\main\java\com.centegy.selenium\` (read-only). Paths below are
relative to that folder. Reviewed 2026-09-30, with facts checked against the live `CTA_CONFIG_ASSERTION` DB.
This file adds to, and corrects, `qa-os/framework/cta_config_assertion.md` (called "the schema doc" below).

## 0. Corrections to the schema doc

| Schema doc says | Code / DB says |
|---|---|
| §3: `fct_pr_cmpt_component_type` / `fct_pr_ce_component_event` are empty | **Wrong.** They hold 15 and 25 rows. The event cache query **INNER JOINs** `fct_pr_ce_component_event` on (type, event) (`UI/Tab/DB/DBExecution.java:342`). A `sef` row whose pair is not in `ce` is **silently dropped**. Valid pairs: 0000/0001-0007, 0012-0019, 0021, 0023, 0025; 0001/0001; 0002/0001; 0003/0001; 0004/0002-0003; 0005/0002; 0015/0001 |
| §3: 0007/0008/0009/0012 are "web widgets (to confirm)" | `cmpt` names: 0007 DropdownGrid, 0008 Multiple Selection Combobox, 0009 Grid Input Selection, 0010 Readable Elements, 0011 Auto, 0012 Dropdown with Grid, 0015 Alert Search, 0256 "DDF8+Alert Search". In the engine, `02xx` (xx<64) means a dropdown, then the key `Keys.values()[xx]`, then an alert (`Main.java:2182-2221`) |
| §4: `0000/0004` = toast message check | It **never asserts**. It reads the first `div.dx-toast-message`, inserts it into `fct_rp_set_screen_event_toast` and logs Success. A missing toast is swallowed (`Main.java:2881-2900`). Use `0000/0013`/`0014` with `TSTMSG` to assert |
| §4: `0000/0002` = verification | It re-finds the element up to `RETRY_COUNT` times with no delay, then logs Success **even if the text never matched** (`Main.java:2838-2878`) |
| `0000/0003` Refresh, `0000/0017`-`0020`, `0014/*` | 0003 has no engine branch: it falls to the "single fill" `else` and does nothing. 0016-0020 and 0014/0002 run only on MOBILE (`Main.java:3099,3154,3162,3180,3186,3192`) |
| §5: blank `EXPECTED_MESSAGE` = "no message expected" | At event level, blank means **not checked** (pass without looking, `assertions/ExpectedOutcome.java:64-71`). Only the field-level `<col>_EXPECTED_MESSAGE`, when blank, asserts that *no* toast is present (`ExpectedOutcome.java:144-147`) |
| §5: `PK#2` for "repeated loads" | `PK#n` is the header for the n-th `0000/0001` in the same event list. `psf_iteration_number` must equal n (see §2.3) |
| §5: `CHECK_VALIDATION` per row | It is a single **static** variable (`Main.java:102,869`). Top-level events after the row loop, and later screens, see the value from the last row loaded |

## 1. Group flow execution

**Query:** `DBExecution.getTestFlow` (`DBExecution.java:103-135`) joins gtfd, then gtf, then LEFT lu (on `plu_serial_no` only, not app-scoped), then LEFT tfd, then tf, `WHERE pgtfd_status='Y' ORDER BY pgtfd_sequenceno` (integer; gaps are fine, and the same flow may repeat). Because tfd is a LEFT JOIN, a flow with N tfd rows would run N times, and each run covers all its menus (`NavigateToClass.java:20-24`). Today all 527 flows have exactly 1 tfd row. **Keep one tfd row per flow.**

**Loop** (`Main.java:314-450`), for each row:
1. Stop if the browser is closed (318). Add `[Run #n]` to the description when the same flow ran before (337-341).
2. Resume: skip flows already passed, using `ExecutionState.csv` (343-357).
3. If `pgtf_testflow_appid` is set, quit and start a driver for that app, mobile login included (365-387).
4. If `pgtf_testflow_login_status` is **not null and not `N`**, then `logoutAndLogin(plu_name, plu_password)` (389-395, 551-572):
   - It sets the repos `LOGIN_USERNAME` and `LOGIN_PASSWORD`. The password comes from **`fct_pr_lu_login_users.plu_password`** of the gtfd row's `plu_serial_no`.
   - When the config `RUN_HARDCODED_LOGIN` is not `true` (the DCODE setup), it runs the app's logout flow and then its login flow (`fct_pr_app_application.ptf_testflowid_logout/_login`, `executeTestFlow` at 574-598). Each runs every top-level screen of the flow's menu with `pk=null` and the **default** case-data file (`resolveFilePathForExcelCaseData(null)`, which uses the config `APP_EXCELCONN_RESULT`).
   - When it is `true`: it clicks the hard-coded logout xpath, then types into `name=username`/`password` and submits (543-549, 600-603). If the config `WITH_DISTRIBUTOR` maps `user:dist`, it waits for `#selectBox1`, sets `g_SELECTED_DIST` and runs menu/screen `9999` (proceed button) (401-418).
   - Any logout or login failure is only printed (393-423). The flow still runs.
5. `navigateAndProcess()` (428). Any exception is printed and the group moves on to the next row (430-431).

A null or `N` login status keeps the current session, and `plu_serial_no` is ignored in that case.

**Starting a group:** with `RUN_HARDCODED_LOGIN != true` the engine only opens the URL (222-247). Nobody logs in, so **the first gtfd row must be the app's login flow** (group 11 seq 1 = `021400000`). That login uses the UI-entered credentials, which go into the `LOGIN_*` repos (275-278).

**DCODE login flow `021400000`** (menu `7777`, verified in the DB). Company and Distributor are handled by config:
- Screen `777701`: `a3` gets REPO `LOGIN_USERNAME`, `a4` gets REPO `LOGIN_PASSWORD`, then click `//button[@type='submit']`.
- Screen `777702`:
  - `0000/0023`: wait up to 3 s for text " Company".
  - If it is visible: fill `selectBox1` from the Excel column `Company`, click `proceedBtn`, fill `selectBox1` from `Distributor`, click `proceedBtn`.
  - If it is not visible: run the child events (ref 1), which wait for `selectBox1`, fill `Distributor` and proceed, then `break`.
- Limitation: `pk=null` means the **first row** of that sheet in the default workbook is used for **every** user. There is no per-user company or distributor.

## 2. Per-screen execution

### 2.1 Menu navigation (`Main.java:2430-2502`)
- Wait for the loader, then click `.productLogo` (home, 2 s wait, failure swallowed, 2504-2514).
- Wait for `#menurollin`, then find `input[placeholder='Search Here']`. If it is hidden, click `#menurollin`. Then click the filter `#form > form > input`, `clear()` it (hidden case only) and `sendKeys(pmg_searchtext)`.
- `pmg_navigation` may be a **comma-separated list** of locators, each clicked in turn (visibility wait, then native click), by `pmg_navigation_type` = `id|xpath|linkText|content_desc`. **Errors are swallowed** (2495-2497): a wrong id means the events run on the wrong page.
- `CustomSleep()` is a no-op (3691-3693), so the "2000/5000 ms" sleeps in this code do not happen.
- Then `navigateToSubMenu`:
  - It loads the `repo_*` columns of every screen sheet (2562-2569).
  - For each top-level `mgsm` row (`pmgsm_parent_screenid IS NULL`, status null or `Y`, ordered by `pmgsm_sequenceno`): read `GLOBAL-REPO`, click the screen's tab (`pmgsm_navigation_type/_path`, 2571-2605), load the fields, then run the events with `psef_ref_serialno = 0/NULL`.

### 2.2 Event order and nesting
- The events cache is ordered by `psef_sequenceno` (integer) (`DBExecution.java:344`). The top level is `ref_serialno = 0` (a NULL is read as 0 by `getInt`) (`DBExecution.java:70-75`).
- **Children** (`psef_ref_serialno = <parent psef_serialno>`) run only under these parents:
  - load-data `0000/0001`: once per matching Excel row (`Main.java:932-937`)
  - assertion `0013`/`0014`: filtered by `psef_fixed_value` = `TP`/`TN` or `TP;<value>` (3548-3582)
  - flow-control `0023`: runs when the element is **not** visible, then `break`s the rest of the parent list (3079-3092)
  - list view `0014` (mobile)
- **Rule:** events that must repeat for each case-data row (Save, assertion, grid line buttons) must be children of the load-data event. Top-level events after a load-data run once, after all rows are done.
- `EVENT_ID` = `x:<serial>` keeps that serial and removes the other events with the same `psef_sequenceno` (3482-3518).
- The engine calls `waitForLoader(null)` before every event except `0005/0002` and `0000/0015` (2637-2638).
- After each event: if no later `0013` exists and the last recorded assertion was TP, or TN+F, the list stops (3459-3467).
- **`psef_desc` must be non-null.** `eventDesc` concatenates it (`DBExecution.java:361`). A null throws inside the static cache load, which is swallowed (375-379), and **no events load for any screen**.

### 2.3 Load data `0000/0001`: `putvaluesFrmDB` (`Main.java:777-1018`)
- Sheet = `psc_screenname`, in the file from `ptfd_filename`, else `pmgsm_screen_filename`, else the default (2535).
- For each row: the PK comes from `PK` or `PK#n`, default `01`. Skip the row if every cell is empty. Match by prefix (`isPkFound`, 1094-1100).
- Fields: `LocatorMappingManager` (`databaseConnections/LocatorMappingManager.java:47-55`).
  - The query needs `psf_field_status='Y'`, a `prv_version` joined to `fct_pr_rv_release_version` with `prv_version_no <=` the run version, and `psf_app_ids` NULL or **`LIKE '%<appId>%'`**. Order by `psf_sequenceno`.
  - `psf_field_addition` must be `+`. Any other value **removes the previously added field** (25-31).
- Then the engine drops `0010` fields and keeps `psf_iteration_number == n` (890-892). The column is read with `getInt`, so **NULL becomes 0 and the field is never filled**. The DB has 6,209 rows with 1 and a handful with 2-11. **Always write 1** (or n for the n-th load).
- `#` in a field or event id is replaced by the 0-based **row counter** of this load-data call, and `(a+b)` is then evaluated (4175-4217). See §6.
- After the last field: send `TAB` to the last field, by `id` only (919, 3899-3907). This is the **only automatic blur**.
- Field-level assertion when `psf_check_assertion='Y'` (1046-1092).
- STPONERR is checked after the row's events. It reads the `PK` header, not `PK#n` (988).

### 2.4 Component handling (`fillFieldData`, `Main.java:1444-2226`)

**Value source.** It comes from `psf_field_source`:
- `EXCEL` (default): the column `psf_field_db_column`, with the text after the first `.` used when there is no source.
- `FIXED`: `psf_fixed_value`.
- `REPO`: `psf_repoid`, falling back to the Excel column (2334-2356).

The config `KEEP_VALUE` sentinel skips the field. A `fieldId` of the form `a,b` means double-click cell `a` (Actions), then act on `b` (grid edit, 2358-2392).

| Type | Locator | How it is driven |
|---|---|---|
| 0001 text | `id` (normal), `name`, `xpath`, `linkText` | **id:** presence, click, Ctrl+A + Delete, then `sendKeys(value)` (real keys) on the visible element (1488-1554). If `role=spinbutton`, a **JS `value=` + `change`** event instead (1535-1551). **name/xpath/linkText:** `clear()` + `sendKeys`, then wait for the value (1481-1512). A blank cell **clears** the field. No blur. Stale retry ×3 |
| 0002 dropdown | via `fieldComponents/Dropdown.java` | Click the field (native; JS scroll first unless the config `allow-scroll.<screen>.<field>=false`). Wait 2 s for `#dropdown-content`, re-clicking once if needed. **readonly input:** click the first `.dx-list-item-content` whose text equals **or contains** the value (`Main.java:2399-2420`). **editable:** Ctrl+A/Delete, `sendKeys(value)` (real keys), then click the **first** item `#dropdown-content > div > div:nth-child(1)` with no text check (`Dropdown.java:155-157,330-346`). Fallback for a grid dropdown: `<id>_rowfilter_code` and `row_1_<id>_code`. `<select>`: send the text + ENTER. **A NULL value types "Test Value"+TAB** into an empty field, or clicks the clear icon (93-101). Then `psf_extra_config` runs (below) |
| 0003 date | `id` / `name` / `xpath` / `linkText` | **id:** click, `Thread.sleep(1000)`, `clear()` if it has a value, `sendKeys(value)`, wait for the value. The text must match the widget format (`Main.java:1627-1638`) |
| 0004 button | `psef_locateby` `id` / `xpath` / `linkText` / `text` (`//*[text()='v']`) | presence, then **native** click: JS `scrollIntoView(nearest)`, wait `elementToBeClickable(locator)`, `.click()`. On any error, retry `.click()` once and then **swallow** it (3874-3897). `<a>` elements get a **JS click** (2701-2702). If `psef_fixedvalue_type` is set, the value (FIXED, EXCEL or REPO) **replaces the locator** (2663-2668) |
| 0006 autoselect | `id` / `name` / `xpath` / `linkText` | Click, then type **one character at a time** (real keys, 100 ms apart). Wait for `#dropdown-content` + 1 s. If there is 1 option click it, else click the first option whose text `startsWith(value)`. **No match is not reported** (1733-1825) |
| 0007 DropdownGrid | id | Double click. If there are more than 6 options, type the value and click the first; otherwise click the option equal to the value (1858-1939) |
| 0008 multi-select | id | Comma-separated values. Uses tag-box input or checkbox xpaths (1940-2018) |
| 0009 grid input | `a,b` | Double-click `a`, then `sendKeys` into `b` (2101-2127) |
| 0010 readable | any | **Never filled.** Read by fill-repo `0012` (if `psf_repoid` is set) and by validation `0007` (if `psf_repoid` is null), through JS `.value`, falling back to `innerText` (3635-3668, 1328-1419) |
| 0012 Dropdown with Grid | id + `psf_subfieldid` (grid checkbox) | Clicks the checkbox **blindly**: it reads `aria-checked` and ignores it (2256-2303). Types into `<id>_rowfilter_code` and clicks the hard-coded **`row_1_<id>_code`** (2060-2077) |
| 0015 alert search | id | Click the element, then `alert.sendKeys(value)` and accept (`fieldComponents/BrowserAlert.java:31-40`) |

**`psf_extra_config`** (dropdown types only, `Main.java:2228-2249`): a comma list. Each item is sent as a `Keys` name (`TAB`, `ENTER`...) to the field, or, if it is not a key name, clicked as an element id. Text fields do **not** get it.

**Single-field events** (`sef` type 0001/0002/0003/..., `Main.java:3405-3457`):
- `psef_fixedvalue_type=FIXED`: the value is `psef_fixed_value`.
- `REPO`: `psef_fixed_value` is the repo id.
- `EXCEL`: `psef_fixed_value` is the **column header**, read from the first row matching the PK.
- NULL: nothing happens, but the event is logged Success.

## 3. Custom events (component type 0000)

| Event | Behaviour | Columns used |
|---|---|---|
| 0001 load data | §2.3 | children = `psef_ref_serialno` |
| 0002 verification | Waits for element text = `psef_fixed_value`. **Never fails** (2838-2878) | locateby, fieldid, fixed_value |
| 0004 toast record | Records the toast text to the DB. Does not assert (2881-2900) | none |
| 0005 Q2Q | Only if `CHECK_VALIDATION=Y` (see §0) (2933-2947, 1122-1182) | `fct_pr_sq`: `psv_isverification='Y'`, `psq_validationType='Q2Q'`, `psq_query` + `psq_qryparameters`, `psq_query_target` + `psq_qryparameters_target`, `psq_qrydesc`. Parameters = comma list of repo keys, resolved to `<PK>_<key>`, or `g_X` to `X` (`databaseConnections/ScreenQuery.java:73-101`). A missing repo value **drops** that parameter (binding shifts). Compares column by column |
| 0006 wait | `Thread.sleep(psef_fixed_value seconds)`, default 1 (2904-2915) | fixed_value = integer seconds |
| 0007 validation | Only if `CHECK_VALIDATION=Y`. Compares **0010** fields (without `psf_repoid`) with the Excel sheet `psc_screenname` (rows whose PK starts with the PK, `#` = row counter), or with `psf_fixed_value`, or (when `psef_validationType='DB'`) with the first `psq` row whose `psv_isverification='Y'` and whose validation type is NULL/`SCREEN`. Match = exact string, numeric equality, or equality with spaces removed (1222-1419) | `psef_validationType` (`EXCEL` default / `DB`) |
| 0012 fill repo | For every field with `psf_repoid`, reads the element and stores `<PK>_<repoid>`. It stores `<repoid>` when the PK is null **or the field id** starts with `g_` (3597-3618) | psf_repoid, psf_locateby, psf_fieldid |
| 0013 assertion | `psef_fixed_value` = `TSTMSG` \| `ELEVAL` \| `ELEVLD`. Uses `EXPECTED_*`/`CASE_TYPE` of the **load-data row** (2956-2992). Then runs children whose `psef_fixed_value` = the case type (TN+F becomes TP) | fixed_value; `psef_fieldid` = element id for ELEVAL |
| 0014 group assertion | `psef_fixed_value` = `<TSTMSG\|ELEVAL\|ELEVLD>,<SheetName>` (no comma gives an error). Reads the sheet in the same workbook and checks **every row whose PK prefix-matches**. A missing sheet is a PASS (as TN) (2994-3077) | fixed_value |
| 0015 checkbox click | Native click on the id, JS click for `<a>`. No state check (2789-2836) | locateby, fieldid |
| 0021 file upload | Sends `BASE_PATH\upload\<psef_fixed_value>` to `input[type=file]` (3395-3403) | fixed_value |
| 0022 / 0024 | Close a dialog by tapping outside (mobile bounds) / `navigate().back()` | none |
| 0023 flow control | Waits `psef_fixed_value` seconds (default: the global wait) for **visibility** of the locator. If it is not visible, runs the children and **breaks the rest of the list** (3079-3098) | locateby (`text` = `//*[text()='v']`), fieldid, fixed_value |
| 0025 frame | If `psef_locateby` is non-null, `switchTo().frame(fieldid)`. Otherwise `fieldid` = `SWITCH` (frame index = fixed_value), `DEFAULT` or `PARENT` (3139-3153) | none |
| 0016-0020 | Mobile calendar, swipe, condition (`psef_condition_statement` `COL=='v'`), fix combo | none |

`psef_mandatory_validation='Y'` on a click means: after the click, check every field with `psf_mandatory_field='Y'` for `aria-required=true` AND `aria-invalid=true`. If one matches, flag an error and stop the screen (2723-2760).

## 4. Toasts and messages (`assertions/ExpectedOutcome.java`)

- **TSTMSG:** `presenceOfElementLocated(div.dx-toast-message)` with the global wait (config `WAITING_BROWSER` s, plus `SLEEP_TIME`×175 ms slept before every `until`; `Webdriver/CustomWebDriverWait.java:25-33`). It reads the **first** match's `getText()` (203-229).
  - It does not wait for a new toast. A toast still on screen from an earlier action is read immediately.
  - With no toast, the timeout is caught and the actual text is `""`, so the assertion fails with "Expected ... Actual ''".
- **Compare:** exact `equals`, case-sensitive (`AssertionComponent.java:42-47`). If the expected text contains `#`, each `#`-separated part must be a substring (93-115).
- **ELEVAL:** `presenceOfElementLocated(By.id(psef_fieldid)).getText()`. A hidden element gives `""`.
- **ELEVLD:** runs only when `CASE_TYPE` is blank or `TP`:
  - `INVALID_INPUT`: passes if **any** field of the screen has `aria-invalid=true`.
  - `REQ_FIELD`: needs mandatory fields with `aria-required` and `aria-invalid`.
  - Any other value passes (74-114).
- Blank `EXPECTED_MESSAGE` at event level passes with no check (70-71).

## 5. Repositories

- **Store:** a single static `LinkedHashMap` (`util/Repository.java:23`), shared by every flow of the group. That sharing is how a document number captured in flow A reaches flow B. Keys:
  - `<PK>_<REPOID>` from `0012` fill-repo
  - `<PK>_<REPO_COL uppercased>` from the case-data `repo_*` columns, loaded per screen **only if the key is absent** (`util/RepositoryFileHandler.java:92-121`)
  - `REPOID` from `GLOBAL-REPO` (overwrites; read once per workbook; `Main.java:3944-3975`)
  - `LOGIN_USERNAME`, `LOGIN_PASSWORD`, `g_SELECTED_DIST`
- **Read:** `REPO` fields look up `<PK>_<repoid>`, or `<repoid>` when the PK is null or the repoid starts with `g_` (`Main.java:2341-2348`). On a miss, `getRepoValue` returns the **last inserted key that contains** the id (`Repository.java:34-45`), and after that the Excel column.
- **Cross-flow reuse:** PKs are reused across flows (`01`, `01-01`), so flow B row `01` reads `01_REPO_DOCUMENTNO` written by flow A row `01`. Keep PKs aligned across the workbooks of a group.
- **Persistence:** the whole map is written to `BASE_PATH\RepoValues.csv` after each flow (when the config `dumpStatePerTestFlow=true`) and at the end. It is **loaded back at the next start before the Excel `repo_*` columns** (`Main.java:274, 443, 509`). Values from a previous run win over the workbook, and a value containing a comma is dropped (`RepositoryFileHandler.java:76-81`). `ui2/tabs/RepoValues.java:95-170` is the UI to view or clear it. The CSV also contains `LOGIN_PASSWORD` in plain text.
- **`g_` inconsistency:**
  - Fill-repo tests `fieldId.startsWith("g_")` (`Main.java:3610`), not the repo id.
  - Q2Q maps `g_X` to repo key `X` (`ScreenQuery.java:82`).
  - A REPO read keeps `g_X`.

## 6. Grids
- **Row index** is computed. `#` in `psf_fieldid` or `psef_fieldid` becomes the 0-based count of Excel rows processed by the current load-data call. `(a+b)` then adds, so `row_(#+1)_qty` gives `row_1_qty` for the first row (`Main.java:4200-4217`, counter at 838/959, applied at 895 and 936). It resets on each load-data call. It does **not** advance for rows cut short by an assertion (`continue` at 929/945).
- **Cell edit:** `psf_fieldid = "<cellId>,<inputId>"` double-clicks the cell, then types into the input (2358-2392).
- **Grid filters** (0012 or the dropdown fallback): hard-coded `<id>_rowfilter_code` and `row_1_<id>_code`, so only the first filtered row can be picked.
- **Checkbox toggles** (`0000/0015`, `checkBoxEnable/Disable`) click without reading the state.

## 7. Alerts, modals, tabs, loaders
- **Browser alert `0005/0002`:** `switchTo().alert()` right away, because the 2 s `CustomSleep` is a no-op. It accepts if `psef_fieldid='accept'` and dismisses otherwise (2767-2787). If the alert is not up yet, the result is NoAlertPresent and the event is marked an error.
- **DevExtreme modals and popups:** no special handling. They are ordinary elements: native clicks, presence waits. There is no wait for a popup to close.
- **Tabs inside a screen:**
  - Tabs are the `mgsm` rows (top-level or child) with `pmgsm_navigation_type` and `_path`, clicked by `executeClick` (a native WebElement click) (2571-2605).
  - A hard-coded `#btn_1` is clicked first when the path contains `Dem-1`, `Opr-1`, `Oth-1` or `addr-1`.
  - Child screens (`pmgsm_parent_screenid=<screen>`) run inside the parent's row loop, only for the first screen, and only if the parent row had no error (962-986).
- **Loading panel:** `waitForLoader(null)` probes `By.id("LoaderId")` 25 times with no wait. If it was ever seen, it waits for invisibility with the global wait. The 3 s `wait1` is unused (3746-3792, `util/PlatFormUtil.java:48-61`). DevExtreme load panels without id `LoaderId` are not waited for.

## 8. Errors, stop-on-error, reporting

| Level | Behaviour |
|---|---|
| Field fill | The exception is caught and only `screenErrorsMap[screen][pk]=true` is set. **No report line** (e.g. 1560-1564, 1821-1825). The load-data then logs "success" for the row (920) |
| Event | Caught per event: error map set, screenshot + Fail line, then **continue with the next event** (3469-3473). Click failures inside `executeClick` never reach this catch |
| Row | `STPONERR=Y` breaks the row loop after the failed row (988-989). Child screens are skipped for a row that has an error (963) |
| Flow / group | The flow's exception is printed and the group continues (430-431). Stop and pause come from the UI (`ExecutionController`) |

**Outputs:**
- Extent HTML: `BASE_PATH\report\group\<group desc>\SummaryReport_*.html`, plus `SummaryReport_FailedCases_*` when the config `report.generation.failedcases=Y` (`util/writer/ExcelFileCreater.java:144-180`). Each line carries testflow, screen, event desc (`<event>:<psef_desc>`), message, status and PK.
- Excel log (`writeLogInExcel`) and `ExecutionState.csv` (used for resume).
- `test_execution` row: P, then D, with pass/fail counts and the report JSON (`Main.java:283, 507`).
- `fct_rp_set_screen_event_toast` (event 0004).
- Screenshots on every step when enabled, and always on failures.

## 9. Group-11 live findings vs the engine

| # | Finding | Verdict | Evidence / how |
|---|---|---|---|
| a | `forwardBtn` is a wrapper; the inner `forward` dx-button must be clicked | **Probably handled; config-fixable if not.** The engine uses a native `WebElement.click()` at the wrapper's centre, which lands on the inner button. Our replay used a scripted click. If it misses, point `psef_fieldid` at an xpath to the inner `.dx-button` | `Main.java:2670-2715, 3874-3897` |
| b | Comment textarea needs blur (Tab) before Save | **Handled when the comment is the last field** of the load-data (TAB is sent to the last field, by id), and usually by the native click on Save (mousedown blurs). Not handled for a text field filled mid-list by a JS click. **Config fix:** give the comment the highest `psf_sequenceno` with `psf_locateby='id'`, or click a neutral element (`0004/0002`) before Save | `Main.java:919, 3899-3907` |
| c | `rowEditBtn_Save_0` used for every line | **Config-fixable.** Use `rowEditBtn_Save_#` in the child events of the load-data (`psef_ref_serialno` = load serial), with one Excel row per line (`01-01`, `01-02`...). `#` becomes 0,1,2... Use `(#+1)` for 1-based ids | `Main.java:4175-4217, 932-937` |
| d | `gridFilterCheckbox` is a toggle whose state persists | **Engine would fail:** blind clicks. **Partly config-fixable:** put a `0000/0023` on `//*[@id='gridFilterCheckbox' and @aria-checked='true']` with the click as its child. Because 0023 `break`s the remaining events, place it in its **own `mgsm` screen row** (no navigation path) before the working screen | `Main.java:2789-2836, 2256-2303, 3079-3092` |
| e | Loss-modal save shows no toast | **Config-fixable.** Leave `EXPECTED_MESSAGE` blank (event-level assertion passes without looking), or assert with `ELEVAL` on a grid/label id, or use `0023` for element visibility. Any TSTMSG with text will fail after the full wait, or read a stale toast | `ExpectedOutcome.java:63-71, 203-229` |
| f | Stock validation expects exact In/Out (clean-day) and dates are hard-coded | **Engine limitation.** `0007` does an exact or numeric-equal compare against static cells. **Dates:** config-fixable with string formulas such as `=TEXT(TODAY(),"yyyy-mm-dd")`, which `ExcelReader` evaluates; numeric formulas return **null** (`ExcelReader.java:119-121`), and in the validation reader they throw and the step passes silently. **Quantities:** switch to `0000/0005` Q2Q (compute the expected balance in SQL using repo parameters), or keep a clean-day precondition | `Main.java:1222-1326, 1396-1409` |
| g | Scripted `.click()` on DevExtreme tabs does not switch | **Handled.** Tab navigation and `0004` clicks use a native click, except on `<a>` tags, which get a JS click. If a tab is an `<a>`, give an xpath to its inner div | `Main.java:2571-2605, 2701-2702` |
| h | Product type-ahead needs real key events | **Handled** by `0006` autoselect (per-character `sendKeys`) or by an editable `0002` (`sendKeys` + first item). Caveats: 0006 picks `startsWith`, and 0002 picks the first item without checking it, so use a unique product code | `Main.java:1784-1809`, `Dropdown.java:151-161` |
| i | Distributor dropdown appears after the Company step | **Handled by config** in login flow `021400000`, screen `777702` (`0023` " Company", then Company, proceed, Distributor, proceed, with a fallback branch). Values come from row 1 of that sheet in the **default** workbook, the same for every user. A generator must fill that sheet and cannot vary it per `plu_serial_no` | DB rows `777702`; `Main.java:574-598` |

## 10. Defects that cause false passes, false failures or flakiness (ranked by impact)

| # | Defect | Where | Fix |
|---|---|---|---|
| 1 | `executeClick` swallows every exception after one retry, so a click that never happened is logged Success | `Main.java:3840-3848, 3864-3872, 3888-3896` | Rethrow after the fallback |
| 2 | Field-fill failures only set the error map; no report line, and the row is logged "success" | `Main.java:1560-1564, 1584-1588, 1727-1730, 1821-1825, 1850-1853, 920` | Log a Fail per field and propagate |
| 3 | The event loop continues after a failed event, so Save and assert run on a broken form and failures cascade | `Main.java:3469-3473` | `break` (or honour STPONERR) on error |
| 4 | Validation `0007`: `isValid` is overwritten by the last field, and exceptions return `true` | `Main.java:1256, 1291, 1321-1323` | `isValid &= ...`; return false in catch |
| 5 | Q2Q row count compared via `getFetchSize()`; `while(a.next() && b.next())` ignores extra rows | `Main.java:1143, 1164` | Count the rows of both sides |
| 6 | `0000/0002` verification never fails; the retry loop has no delay | `Main.java:2847-2874` | Poll with a wait and fail on mismatch |
| 7 | Toast check reads the first `div.dx-toast-message` present (stale toast), has no "new toast" wait, and turns no-toast into `""` | `ExpectedOutcome.java:203-229` | Wait for a visible toast created after the action, and wait for old toasts to disappear first |
| 8 | Dropdown picks the first filtered item (editable) or the first item that `contains` the text (readonly); autoselect with no match is silent | `Dropdown.java:155-161, 330-346`; `Main.java:2413, 1798-1813` | Exact text match; fail when not found |
| 9 | A NULL dropdown value types "Test Value"+TAB | `Dropdown.java:93-99` | Skip, or clear only |
| 10 | A null `psf_iteration_number` (read as 0) or a non-`+` `psf_field_addition` silently removes fields; `psf_app_ids LIKE '%1%'` also matches apps 11-18 | `LocatorMappingManager.java:25-31, 52-54, 78`; `Main.java:890-892` | Null-safe `Integer`; exact match against the app-id list |
| 11 | A null `psef_desc` kills the whole events cache silently (static block) | `DBExecution.java:361, 375-379` | Null-safe concat; do not swallow |
| 12 | Repos: `contains` fallback lookup, CSV persisted across runs and loaded before Excel, inconsistent `g_` handling, password written to CSV | `Repository.java:34-45`; `Main.java:274, 3610`; `ScreenQuery.java:82`; `RepositoryFileHandler.java:111` | Exact keys, a fresh map per run, one `g_` rule, never persist `LOGIN_*` |
| 13 | Waits: `CustomSleep` is a no-op; every `until` sleeps `SLEEP_TIME`×175 ms first; the loader check covers only `#LoaderId`; `0005` alert has no wait | `Main.java:3691-3693, 3746-3792, 2771`; `CustomWebDriverWait.java:27-28` | Condition-based waits (overlay invisibility, `alertIsPresent`) |
| 14 | `ExcelReader`: the header index counts non-blank cells (a gap shifts every later column); numeric formulas become null; the header cache is never refreshed; the validation reader throws on numeric formulas | `ExcelReader.java:66-79, 119-121`; `ExcelReaderValidation` `getCellValueValidation` | Use `cell.getColumnIndex()`; `DataFormatter` + evaluator |
| 15 | SQL built by string concatenation everywhere (IDs, toast text), and menu-navigation errors are swallowed, so a flow runs on the wrong page | `DBExecution.java:22, 50, 128, 152`; `LocatorMappingManager.java:47-55`; `Main.java:2495-2497, 2511-2513` | Prepared statements; fail the flow when navigation fails |

## 11. Rules for the QA OS generator (from the above)

1. **Event rows:** every `sef` (type, event) pair must exist in `fct_pr_ce_component_event`, and `psef_desc` must be non-null.
2. **Per-row events** (Save, assertions, grid line buttons) are children of the load-data event: `psef_ref_serialno` = its `psef_serialno`.
3. **Field rows** need all of: `psf_field_status='Y'`, `psf_field_addition='+'`, `psf_iteration_number=1`, a valid `prv_version`, and `psf_app_ids` NULL or the exact id.
4. **Click events:** leave `psef_fixedvalue_type` NULL, or the value replaces the locator.
5. **Grid lines:** use `#` or `(#+1)` in the ids plus one Excel row per line; never hard-code `_0`.
6. **Group login:** the group starts with the app login flow. Rows that switch user set `pgtf_testflow_login_status='Y'` and `plu_serial_no`.
7. **Toasts:** set `EXPECTED_MESSAGE` only when a toast is really observed, and use `#` fragments for dynamic numbers.
8. **Workbooks:**
   - no blank header cells
   - dates as text, or `TEXT()` formulas
   - no numeric formulas
   - dropdown cells never blank
9. **Repos:** keep PKs aligned across a group's workbooks. Clear `RepoValues.csv` before a run.

## Screen-mapping navigation path (checked 2026-10-09)
`fct_pr_mgsm_menu_group_screen_mapping.pmgsm_navigation_path` + `pmgsm_navigation_type` are read for top-level screens (`DBExecution.getScreensByMenu`) and child screens (`getChildScreens`). Before a top-level screen runs on web, `Main.navigateOnTabs` waits for the loader and clicks the element named by the path, located per type: `linkText`, `id` or `xpath` (anything else, incl. NULL, clicks nothing). Paths containing `Dem-1` / `Opr-1` / `Oth-1` / `addr-1` first click `#btn_1` (header). So the path is the **tab / section the screen lives on**; for single-tab screens the convention is the menu entry id with type NULL (Order Booking 0001 / 0091: `ORDER_BOOKING`). The authoring tool's Screen Mapping tab shows and saves it but does not require it. QA OS generator writes it since 2026-10-09 (HARDENING C12).
QA OS converter (2026-10-09, HARDENING C13): every recorded tab click starts a framework screen whose navigation is that tab (id -> `id`, text -> `linkText`, else `xpath`), following the Outlet / DSR / Distributor Profile mappings (first tab = root screen with its own tab id, later tabs = children).
