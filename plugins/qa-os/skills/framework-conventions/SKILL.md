---
name: framework-conventions
description: How the legacy Selenium Regress framework (CTA_CONFIG_ASSERTION tables + case-data workbook) is configured and executed - table chain, id and default rules, event and field rules, workbook rules, user switching, and the engine's silent-failure traps. Use when generating, verifying or reading framework rows or workbooks.
---

# Framework conventions (CTA_CONFIG_ASSERTION)

Sources verified against the engine code (NGSelenium-Testing) and the live tables: `docs/engine-review/runtime.md`, `docs/engine-review/authoring.md`, `framework/cta_config_assertion.md`, and the atlas `apps/snd/knowledge/framework_atlas/` (README first). This skill is the working summary; when it and the atlas disagree, the data in the atlas wins. Read-only MCP: `selenium-framework-db`. **Never read a password column** (`plu_password`); never apply SQL.

## 1. The chain
`group (gtf)` -> `group detail (gtfd)`, ordered by `pgtfd_sequenceno`, only `pgtfd_status = 'Y'` -> `test flow (tf)` -> `test flow details (tfd)` (ordered menu groups + workbook file `ptfd_filename`) -> `menu group (mg)` -> `mapping (mgsm)` -> `screen (sc)` -> `fields (sf)` and `events (sef)`; queries `sq` join to the screen. Component types/events come from `cmpt` and `ce`: an event whose (type, event) pair is missing from `ce` is silently dropped.
- Group 11 = Pakistan "Daily Cycle Only Positive Flow" (46 active rows, 10 user switches). Markets have their own groups (`apps/<app>/app.yaml` -> `markets`).
- User switch: `pgtf_testflow_login_status = 'Y'` + `plu_serial_no` = logout, login as that user. `NULL` or `'N'` = same session (the serial is ignored). The first row of a group is normally the app's login flow.
- Case-data goes in `<casedata folder>\<file>.xlsx`, one sheet per **screen name** (`psc_screenname`, at most 31 chars), row 1 = headers.

## 2. Ids and defaults (what the framework's own UI writes)
- Menu group id: highest `'0___'` id + 1, 4 digits. Screen id: menu group id + 2 digits. Flow id: first 4 digits of highest flow id + 1, then `0001`. Group id: highest + 1 (not padded, status `'A'`).
- Compute ids from the **live maximum at generation time** and re-check just before review; ids in an old draft may be taken (the Van Sales draft ids 0612/061201/06120001 were taken the next day).
- New rows: `prv_version` = `'1.0'` (NOT NULL); audit `created_by` = our run tag (kept for rollback; the engine never reads it), `modified_date`/`modified_by` NULL; `master_app_id` from the spec, default NULL.
- Trim every value; empty strings are stored as NULL. Never generate login users.

## 3. Fields and events (rules the engine enforces silently)
- Field: `psf_field_status = 'Y'`, `psf_field_addition = '+'` (anything else removes the field), `psf_iteration_number = 1` (NULL is read as 0 and the field is never filled), valid `prv_version`, `psf_field_db_column` = the workbook column header.
- Component types: 0001 text, 0002 dropdown, 0003 date, 0004 button, 0006 autoselect, 0010 readable (never filled).
- Events: `psef_desc` **must not be NULL** on an active event (one NULL breaks loading of every later event). Types on system component `0000`: 0001 Load Data (always serial 1), 0005 data verification (Q2Q), 0006 wait, 0007 validation, 0012 fill repo, 0013 assertion (`psef_fixed_value` = TSTMSG | ELEVAL | ELEVLD), 0014 group assertion (`<kind>,<AssertionSheet>`).
- **Children of Load Data run once per case-data row; top-level events run once after all rows.** Save, assertions and grid-line buttons must be children of the Load Data event (`psef_ref_serialno` = its serial). An event whose ref points at a click never runs (41 such events exist today).
- Click events: leave `psef_fixedvalue_type` NULL, or its value replaces the locator. Single-field fills take `EXCEL` / `REPO` / `FIXED` in `psef_fixedvalue_type`.
- Grid line buttons: `rowEditBtn_Save_#` as a child event with one workbook row per line (the row index is not always 0). Filter checkboxes are toggles whose state persists; the engine clicks without checking, so use an `aria-checked` check event (0023) in its own screen row.
- Only statuses `Y` and `A` run; `I` is treated as inactive.

## 4. Case-data workbook rules
- Sheet per screen; headers = `psf_field_db_column` plus controls `PK`, `PK_DESC`, `STPONERR`, `CASE_TYPE`, `EXPECTED_INPUT`, `EXPECTED_MESSAGE`, `CHECK_VALIDATION`, `EVENT_ID`, `SWIPE`, and `repo_*` columns.
- **Formula cells need a cached value.** openpyxl saves `=TEXT(NOW(),"YYYY-MM-DD")` with an empty cached result; the engine's row check (`ExcelReader.isRowValid`) reads the cached value, POI throws, the exception is only printed and the screen is silently skipped. After EVERY workbook write run `python framework/tools/cache_formulas.py <workbook.xlsx>` (it writes the cached text; the formula stays live), then re-read with `openpyxl data_only=True` to confirm. An openpyxl save drops the cached values again.
- No blank header cells. Dates as text `yyyy-mm-dd` (or `TEXT(TODAY(),...)`), no numeric formulas. **Never leave a dropdown cell blank**: the engine types "Test Value".
- `PK` is hierarchical (`01`, `01-01`), matched by prefix; keep PKs aligned across the group's sheets. `CASE_TYPE`: the team uses `TN`; `TP` only enables the ELEVLD input check. `STPONERR` = `N`.
- `EXPECTED_MESSAGE` is compared with the toast; a `#` means pattern match; **blank means not checked**. Fill it only with text observed live.
- **Every observed message becomes an assertion** (QA lead, 2026-10-07). Map by type (`observed.messages` in the recording):

  | Message type | Framework events | Workbook |
  |---|---|---|
  | `toast` | assertion `0000/0013` with `psef_fixed_value = TSTMSG,<NAME>_ASSR` right after the click that raises it (child of Load Data) | `<NAME>_ASSR` sheet row: `PK`, `EXPECTED_MESSAGE` = exact text |
  | `popup` (in-page modal) | assertion `0000/0013` `ELEVAL,<NAME>_ASSR` on the modal's message element (field locator = the observed `locator`), then a click `0004/0002` on the button used (e.g. Continue, Save changes) | `<NAME>_ASSR` row with the modal text in `EXPECTED_MESSAGE` |
  | `alert` (browser dialog) | `0005/0002` with field id `accept` or `dismiss` | none: **the engine reads the alert text but does not assert it** (`Main.java`, "Click Alert" only prints it). Put the observed text in `review_note.md` under "Not asserted by the engine" and propose the engine change to the framework owner |
  | `inline` validation | `0000/0013` `ELEVLD,<NAME>_ASSR`; row `CASE_TYPE = TP`, `EXPECTED_INPUT = REQ_FIELD` or `INVALID_INPUT` | as named |
  A message that appears but is not asserted is listed in `review_note.md` with the reason.
- Repos (`REPO_DOCUMENTNO`, `ORDERNUMBER`, `REPO_GINNO` ...) are keyed by PK and shared across the group; they persist in `RepoValues.csv` between runs, so clear it before each run. Repo id spellings differ in the data (`REPO_DOCUMENTNO` / `REPO_DocumentNo`); use the spelling the writing flow uses.

## 5. The engine's silent-failure traps (why a green run is not proof)
1. Failed clicks are swallowed and reported as passed.
2. A failed field fill produces no report line; the row is logged as success.
3. After a failed event the next event still runs, so Save and assertions run on a broken form.
4. A validation event keeps only the last field's result; an exception counts as a pass.
5. The toast check reads the first toast on screen (possibly an old one); a missing toast becomes empty text.
6. Query-to-query checks never compare row counts.
Consequence: every generated flow needs an observed live recording behind it, assertions on **specific** messages, and result evidence, not only the engine's status.

## 6. Framework limits to design around
- Exact quantity assertions assume a clean day (expected In = this document only): prefer a query-to-query check (0005) or assert the change, not the total.
- Workbook dates are hard-coded examples: generate with `TEXT(TODAY())` or resolved dates.
- Company and Distributor come from row 1 of one sheet, so they are the same for every user in a group.
- Stock is auto-allocated at order save on this environment; the framework's manual Stock Allocation / Unallocation flows can disagree with that (see `apps/snd/knowledge/ui.md`).

## 7. Using the atlas (reading existing flows only - NOT for generating new ones)
**When generating from a QA OS recording, do not use the atlas or existing flows for names, ids or events** (QA lead rule, 2026-10-08): the recording is the only source; the live DB is read only for table structure, required columns, valid event pairs and free ids. The atlas is for understanding or reviewing existing legacy flows (e.g. FRAMEWORK_DRIFT analysis, training walks the trainer asked for).
Find a flow with `python apps/snd/tools/build_atlas.py --find "<text>"`; read `flows/<id>.md`, then the JSON for exact ids. Attach the trace key `<group>:<seq>:<flow>:<screen>:e<event serial>` to every executed step. A screen or field missing from the atlas is an **authoring gap** to report, not something to invent.
