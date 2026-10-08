# QA OS hardening register (before the QA-environment release)

**Rule (QA lead, 2026-10-08):** in the QA environment, QA OS runs **strictly to the design**: no changes to the framework design, the tools, the skills or the recordings during a run, and no long investigations. A failure stops the run and is reported. Therefore **every issue below must be fixed and proven here, before release.** Source: the quick runs QUICK-20261007-OB and QUICK-20261008-OB (attempts 1-3), their friction logs and two verifier reviews.

Status: **FIXED** (done and tested) · **FIXED-UNPROVEN** (code changed, not yet proven in a live run) · **OPEN**.

## A. Recording (watcher, recorder agent)
| # | Issue | Status | Fix / proof needed |
|---|---|---|---|
| A1 | Real Selenium typing/clicks were not logged; recordings were rebuilt by hand | FIXED-UNPROVEN | Passive watcher (2026-10-08). Attempt 3 needed no hand edits, but gaps A2-A5 remain |
| A2 | Grid cells under a band header are labelled with the band only ("Order"), product cell "Product Desc CS" | OPEN | Read the column caption from the grid's column model / bottom header row; fall back to cellId (row_1_cs) |
| A3 | Cells left at their default value (0) are not logged, so a field can be missing from the spec | OPEN | Watcher: log every editor that was focused or tabbed through; converter: build grid fields from all cells seen in any line |
| A4 | Several values for one cell (typo "20" then "2"; "1" then "12"); PC logged before CS | OPEN | Converter: last value per cell per line wins; order fields by column index |
| A5 | Read-only results (Order Number, amounts on Order View) are not logged | OPEN | Watcher: log values read by `Remember ... as ...` steps (a `qaos.remember(label)` call) |
| A6 | Dropdown option lists were logged as popups | FIXED | Watcher + converter filter (tested) |
| A7 | Sidebar menu click not captured | FIXED-UNPROVEN | `nav_click` captured in attempt 3; converter writes `navigation` - generator must use it |
| A8 | Helper injection: pasting 18 KB; backticks/comments break it; fetch from a local server blocked | OPEN | Ship a minified one-line build `qaos_helpers.min.js` (no comments) and one documented injection call |
| A9 | Grid number cells: send_keys goes stale; caret after "0" gives "20" | OPEN | One recorder recipe in recording-protocol: click cell -> select all -> type -> Tab (and a `qaos.typeCell` helper) |
| A10 | Long dropdown lists: a click picks the wrong row; typed text is discarded if focus leaves before picking | OPEN | recording-protocol + step wording: type the code, pick the single option immediately |
| A11 | Toast capture: two toasts after Save (stale "Validation successfully" first) | FIXED (converter) | Converter keeps the click's own new message; see C4 for the engine side |
| A12 | Recorder executed several cases when the brief listed several | FIXED | Rule: one case per brief; recorder executes only the first |

## B. Steps, data and process (quick-script, data step)
| # | Issue | Status | Fix |
|---|---|---|---|
| B1 | Missing stock blocks the run ("Stock not available.") | FIXED (design) | Stock is live state: precondition steps at the top of the step sheet (Stock Inquiry check) executed in Q4; a failure stops the run; a setup Dispatch Advice only if it is in the approved plan |
| B2 | Case/execution data came from the old framework workbook | FIXED (design) | Test data comes from training only: per-market test data catalog (`knowledge/business/test_data/<market>.md`); gaps -> ask/train. No app or DB lookup before execution |
| B3 | Case expectations claimed amounts that vary with masters | FIXED | Cases assert messages and document creation only; amounts recorded, not asserted |
| B4 | Step checker label index lacks detail-screen buttons (Validation/Save) | OPEN | Add to label index |
| B5 | Late scope change after execution started | FIXED (process) | All decisions are taken at gate QG; nothing changes after the gate |
| B6 | Run bookkeeping: run.json stages stay pending; no requirement.json for quick runs | OPEN | quick-script writes requirement.json (R1 = request) and updates stages |
| B7 | Base snd-schema has no PK (010104) transactional or outlet data | OPEN (environment) | Data step must read live screens; or connect the overlay/QA DB read-only for the QA environment |
| B9 | Knowledge gaps found mid-run were handled ad hoc | FIXED (rule) | Knowledge-gap gate in quick-script / qa-orchestrator / knowledge-intake: short gap -> ask + continue; long-term gap -> training first, no execution |
| B8 | Stock carry-over job did not run on 10-06 and 10-08 | OPEN (environment owner) | Report; B1 handles it per run |

## C. Generation (framework-generator, converter, gen_framework_sql.py)
| # | Issue | Status | Fix |
|---|---|---|---|
| C1 | Detail/summary screens generated as top-level (engine would run all headers, then all lines) | OPEN | Generator: child screens via `pmgsm_parent_screenid`; documented pattern header -> lines -> save per data row |
| C2 | gen_framework_sql.py handles one screen only; agents wrote one-off scripts | IN PROGRESS | Separate task running (multi-screen support) |
| C3 | Navigation locator was a placeholder | OPEN | Use the recorded `navigation` (sidebar entry id, search text) |
| C4 | Engine reads the first toast: Save may read the stale "Validation successfully" | OPEN | Generator inserts a wait-until-the-toast-clears event before Save (or asserts with a pattern), proven in one engine replay |
| C5 | Screen without Load Data for the order-number read | OPEN | Order View screen gets Load Data + fill-repo |
| C6 | Header ids change after Order Detail and after New Order | OPEN | Recorder logs ids per screen state; generator uses the ids valid at that point |
| C7 | Product type-ahead generated as editable dropdown (0002) | OPEN | Map widget `type-ahead` to the framework's AutoSelect component |
| C8 | master_app_id, repo naming, created_by conventions | FIXED (decided) | NULL; new repo ids (e.g. QUICK_ORDERNUMBER); created_by = run tag, modified_* NULL |
| C9 | Alert text cannot be asserted by the legacy engine | OPEN (framework owner) | Listed as "not asserted"; engine change proposed |

## D. Release gate (all must be true before QA release)
1. Every row above is FIXED or explicitly accepted by the QA lead (environment items B7/B8, engine item C9).
2. **Acceptance run:** one quick request executed end to end by a clean session (as a QA member would), with **no tool/skill/design changes and no hand edits**, single-case execution, within a **time budget of about 30 minutes** from request to verified scripts (excluding logins).
3. The verifier verdict is "ready for framework-owner test-copy apply".
4. **One engine replay** of the generated flow on a test copy of CTA_CONFIG_ASSERTION passes for all N case rows (checked in the app, not only by the engine's green status).
5. Release notes, guides and the zip rebuilt; version bumped.
