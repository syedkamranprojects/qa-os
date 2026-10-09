# QA OS hardening register (before the QA-environment release)

**Rule (QA lead, 2026-10-08):** in the QA environment, QA OS runs **strictly to the design**: no changes to the framework design, the tools, the skills or the recordings during a run, and no long investigations. A failure stops the run and is reported. Therefore **every issue below must be fixed and proven here, before release.** Source: the quick runs QUICK-20261007-OB and QUICK-20261008-OB (attempts 1-3), their friction logs and two verifier reviews.

Status: **FIXED** (done and tested) · **FIXED-UNPROVEN** (code changed, not yet proven in a live run) · **OPEN**.

## A. Recording (watcher, recorder agent)
| # | Issue | Status | Fix / proof needed |
|---|---|---|---|
| A1 | Real Selenium typing/clicks were not logged; recordings were rebuilt by hand | FIXED-UNPROVEN | Passive watcher (2026-10-08). Attempt 3 needed no hand edits, but gaps A2-A5 remain |
| A2 | Grid cells under a band header are labelled with the band only ("Order"), product cell "Product Desc CS" | FIXED-UNPROVEN (mock-tested 2026-10-08: "Order CS", "Order PC", "Product Desc") | Read the column caption from the grid's column model / bottom header row; fall back to cellId (row_1_cs) |
| A3 | Cells left at their default value (0) are not logged, so a field can be missing from the spec | FIXED-UNPROVEN (mock-tested: a PC cell left at 0 is logged) | Watcher: log every editor that was focused or tabbed through; converter: build grid fields from all cells seen in any line |
| A4 | Several values for one cell (typo "20" then "2"; "1" then "12"); PC logged before CS | FIXED (converter: one field per cell, grid fields in column order; tested) | Converter: last value per cell per line wins; order fields by column index |
| A5 | Read-only results (Order Number, amounts on Order View) are not logged | FIXED-UNPROVEN (`qaos.remember` + converter -> 0000/0012 fill repo; mock-tested) | Watcher: log values read by `Remember ... as ...` steps (a `qaos.remember(label)` call) |
| A6 | Dropdown option lists were logged as popups | FIXED | Watcher + converter filter (tested) |
| A7 | Sidebar menu click not captured | FIXED-UNPROVEN | `nav_click` captured in attempt 3; converter writes `navigation` - generator must use it |
| A8 | Helper injection: pasting 18 KB; backticks/comments break it; fetch from a local server blocked | FIXED (build_helper.py -> qaos_helpers.min.js; injected as an execute_script ARGUMENT, tested; source has no backticks/NUL bytes) | Ship a minified one-line build `qaos_helpers.min.js` (no comments) and one documented injection call |
| A9 | Grid number cells: send_keys goes stale; caret after "0" gives "20" | FIXED (recipe in recording-protocol §2) | One recorder recipe in recording-protocol: click cell -> select all -> type -> Tab (and a `qaos.typeCell` helper) |
| A10 | Long dropdown lists: a click picks the wrong row; typed text is discarded if focus leaves before picking | FIXED (recipe in recording-protocol §2 + step wording) | recording-protocol + step wording: type the code, pick the single option immediately |
| A11 | Toast capture: two toasts after Save (stale "Validation successfully" first) | FIXED (converter) | Converter keeps the click's own new message; see C4 for the engine side |
| A12 | Recorder executed several cases when the brief listed several | FIXED | Rule: one case per brief; recorder executes only the first |
| A13 | Rehearsal 2026-10-08 (QUICK-20261008-1429): navigation via `qaos.open` was not logged (helper runs quiet) -> no menu navigation | FIXED-UNPROVEN (mock-tested) | `Q.open` logs its own `nav_click` (entry id, search term); converter ignores the helper's `nav` entry |
| A14 | Rehearsal: header fields / remembered order number logged BEFORE the screen entry (screen noted only on clicks) -> wrong screens, no data binding | FIXED-UNPROVEN (mock-tested) | Every log entry first logs the current screen when it changed (`rec` -> `noteScreen`) |
| A15 | Rehearsal: grid cells logged per keystroke ("10", "101", "01"); last entry not the committed value (line 5 showed CS 10) | FIXED-UNPROVEN (mock-tested) | Watcher logs a `row` snapshot (editable cells of the row, read at the row-button click); converter uses snapshots for grid fields and line values, ignores that grid's `cell` noise; binding accepts numeric equality and `<code>-<description>` pick text |
| A16 | Rehearsal: read-only computed cell (Gross Amount) logged as an input field | FIXED-UNPROVEN (mock-tested) | Read-only / disabled inputs are not logged as cells and not in snapshots |

## B. Steps, data and process (quick-script, data step)
| # | Issue | Status | Fix |
|---|---|---|---|
| B1 | Missing stock blocks the run ("Stock not available.") | FIXED (design) | Stock is live state: precondition steps at the top of the step sheet (Stock Inquiry check) executed in Q4; a failure stops the run; a setup Dispatch Advice only if it is in the approved plan |
| B2 | Case/execution data came from the old framework workbook | FIXED (design) | Test data comes from training only: per-market test data catalog (`knowledge/business/test_data/<market>.md`); gaps -> ask/train. No app or DB lookup before execution |
| B3 | Case expectations claimed amounts that vary with masters | FIXED | Cases assert messages and document creation only; amounts recorded, not asserted |
| B4 | Step checker label index lacks detail-screen buttons (Validation/Save) | FIXED | `label_extras.json` Order Booking: Validation, Save, New Order + grid columns (seen live 10-08), index rebuilt; `qaos_steps.py check` now accepts the sheet's `[Role]` prefix (was rejected as an unknown verb) and `add` takes the actor from it |
| B5 | Late scope change after execution started | FIXED (process) | All decisions are taken at gate QG; nothing changes after the gate |
| B6 | Run bookkeeping: run.json stages stay pending; no requirement.json for quick runs | FIXED | `qaos_run.py init ... --request "<one-liner>" [--screens]` writes requirement.json (R1 = request, schema-valid), marks analyse done and bulk skipped; quick-script calls `stage` in every phase |
| B7 | Base snd-schema has no PK (010104) transactional or outlet data | OPEN (environment) | Data step must read live screens; or connect the overlay/QA DB read-only for the QA environment |
| B9 | Knowledge gaps found mid-run were handled ad hoc | FIXED (rule) | Knowledge-gap gate in quick-script / qa-orchestrator / knowledge-intake: short gap -> ask + continue; long-term gap -> training first, no execution |
| B8 | Stock carry-over job did not run on 10-06 and 10-08 | OPEN (environment owner) | Report; B1 handles it per run |

## C. Generation (framework-generator, converter, gen_framework_sql.py)
| # | Issue | Status | Fix |
|---|---|---|---|
| C1 | Detail/summary screens generated as top-level (engine would run all headers, then all lines) | FIXED-UNPROVEN | `framework/tools/qaos_record_multi.py`: one screen per page visited, first = root, others `parent` = root (child screens); grid-row buttons ref the lines Load Data, once-per-order clicks/assertions NULL. Tests: `test_qaos_record_multi.py`. Proof: engine replay |
| C2 | gen_framework_sql.py handles one screen only; agents wrote one-off scripts | FIXED | Multi-screen spec (screens[] with own fields/events), pre-flight + rollback + workbook per screen; 7 tests pass (framework/tools/test_gen_framework_sql.py; fixture now under attempt2_superseded/), matches the 10-08 SQL row for row |
| C3 | Navigation locator was a placeholder | FIXED | Converter takes `menu_group.navigation` from the recorded sidebar `nav_click` (id, search text, navigation_type id); sidebar clicks/typing are no longer screen events; no nav_click = GAP |
| C4 | Engine reads the first toast: Save may read the stale "Validation successfully" | FIXED-UNPROVEN | Converter inserts wait 0000/0006 (5 s) before any click within 10 s of a toast; a repeated earlier toast is listed as not asserted. Proof: engine replay |
| C5 | Screen without Load Data for the order-number read | FIXED | Every screen gets Load Data serial 1; `qaos.remember` -> 0010 field with repoid + 0012 fill-repo on that screen |
| C6 | Header ids change after Order Detail and after New Order | FIXED-UNPROVEN | Each screen's fields use the ids logged on that page; proof = acceptance run with the current watcher |
| C7 | Product type-ahead generated as editable dropdown (0002) | FIXED | Widget `type-ahead` -> 0006 AutoSelect, dropdown -> 0002, date -> 0003 |
| C8 | master_app_id, repo naming, created_by conventions | FIXED (decided) | NULL; new repo ids (e.g. QUICK_ORDERNUMBER); created_by = run tag, modified_* NULL |
| C10 | Case-data rows for N cases were hand-written by the agent | FIXED | `framework/tools/qaos_record_multi.py --rows rows.json --cases cases.json`: fields bound to data keys by exact match with the recorded case, then one row per case (lines `01-01`), assertion sheets one row per case; a field that does not match = GAP, sheet left header-only (never guessed). quick-script writes `rows.json` in Q2 |
| C11 | Quick run 2026-10-09 (QUICK-20261009-1305): scripts for a flow that already exists as a QA OS flow (06490001 = same as 06480001 from 10-08) create a duplicate flow | OPEN | Before generating, compare the recording's screens with earlier QA OS flows (same menu group navigation + screens); if equal, offer "add a case-data row to the existing flow" instead of a new flow |
| A17 | Quick run 2026-10-09: the recorder wrote recording_TC01.json by transcribing the dump (no direct file write from the browser); verifier: evidence rests on one transcription | OPEN | Write the log to disk without transcription: e.g. the recorder saves `qaos.dump()` via a small runtime tool that reads the MCP result, or the helper downloads the log as a file to the run folder |
| C12 | Generated screen-mapping rows had no pmgsm_navigation_path (flow 06490001 ran, path reported missing by the QA lead 2026-10-09) | FIXED | gen_framework_sql.py writes the menu entry id (e.g. ORDER_BOOKING) on every mgsm row, type NULL, as in flows 0001/0091; a screen's own tab locator + type (linkText / id / xpath) when the spec has one - the engine clicks it before the screen (Main.navigateOnTabs). Test: test_every_screen_mapping_has_a_navigation_path. 0648 fix script: runs/QUICK-20261008-1429/20261008-1429/framework/fix_navigation_path.sql (not applied) |
| C13 | Multi-tab screens (Outlet / DSR / Distributor Profile pattern) were one framework screen per URL; the tab a screen lives on was not in the scripts | FIXED-UNPROVEN | qaos_record_multi.py: a recorded tab click (or a click on a known tab id Dem-1 / Opr-1 / Oth-1 / addr-1 / tab_N / tab_group_N) starts a framework screen; navigation from the tab (id -> type id, text -> linkText, else xpath) -> gen_framework_sql.py writes pmgsm_navigation_type / _path; case data and assertions keyed per tab. Test: test_tabs_become_screens_with_navigation. Proof: one live recording of a multi-tab screen (e.g. DSR Profile) + engine replay |
| A18 | DSR Profile tabs are dx-buttons without id; the tab id (tab_4..tab_7, tab_group_N, Dem-1/Opr-1) sits on the parent element; the watcher logs a plain click with a generic locator, so the converter cannot make tab screens (blocks C13 proof) | OPEN | Watcher: on a click inside an element whose ancestor id matches a tab pattern (or role=tab / dx-tab / dx-button inside a tab container), log act 'tab' with the ancestor id + text; converter TAB_ID already accepts those ids |
| A19 | Quick run 2026-10-09 (DSR Profile): executor saved the address on the default Address sub-tab instead of Residence -> Forward refused "Residence Address cannot be empty" | OPEN | Step sheets name every sub-tab as its own step (Click tab Residence); recorder verifies the active sub-tab before filling |
| C9 | Alert text cannot be asserted by the legacy engine | OPEN (framework owner) | Listed as "not asserted"; engine change proposed |

## D. Release gate (all must be true before QA release)
1. Every row above is FIXED or explicitly accepted by the QA lead (environment items B7/B8, engine item C9).
2. **Acceptance run:** one quick request executed end to end by a clean session (as a QA member would), with **no tool/skill/design changes and no hand edits**, single-case execution, within a **time budget of about 30 minutes** from request to verified scripts (excluding logins).
3. The verifier verdict is "ready for framework-owner test-copy apply".
4. **One engine replay** of the generated flow on a test copy of CTA_CONFIG_ASSERTION passes for all N case rows (checked in the app, not only by the engine's green status).
5. Release notes, guides and the zip rebuilt; version bumped.
