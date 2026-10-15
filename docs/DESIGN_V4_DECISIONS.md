# QA OS design v4 - decisions log (review with Syed Kamran, started 2026-10-15)

Why: the SDMS-6084 run (2026-10-14/15) took ~55 min of agent time, ~850 browser actions and 9 logins for 19 cases, because the AI recorder executed every case and worked out each click from scratch. v4 keeps the AI-intern idea (knowledge -> cases -> steps -> execution -> scripts) but makes the steps executable by a program and limits AI to understanding, case design, ONE execution per path and failures.

Key finding: DCODE screens are configuration-driven. `dyp_dp_pgl_pagelayout` (layout JSON: tabs, panels) and `dyp_dp_pgc_pageconfiguration` (control JSON: type, id e.g. TXT__epp1_offdays, caption key, mask, validation, disable expression) describe every dynamic screen. The base DB lags the environment (Off Days still a textBox there), so the environment's config tables are needed.

| Step | Decision | Date |
|---|---|---|
| 0.1 Who changes business knowledge in the QA installation | **QA members directly**, each fact tagged with name and date | 2026-10-15 |
| 0.2 Lessons found in runs | **Split by type:** screen-level lessons (ids, control behaviour) saved automatically; business rules wait for QA / Syed Kamran confirmation before they are used for prediction | 2026-10-15 |
| 0.3 Where screen-level lessons live | **Small file per used screen** (a few KB, only screens a ticket touched, beside the config read from the DB, refreshed after a release) | 2026-10-15 |
| 0.1 note | A QA edit that contradicts an existing [stated] fact keeps both and is flagged as a conflict for Syed Kamran; tool/design gaps still go to feedback/design_gaps.md | 2026-10-15 |
| 1.1 Run context | **Asked every time** (market, env, run-by, Maker, Checker, distributor), as now | 2026-10-15 |
| 1.2 Who starts a run | **Any QA member** | 2026-10-15 |
| 1.3 Jira inputs | Story **+ comments + linked bugs + subtasks + attachments/images** | 2026-10-15 |
| 1.3 note | If the Jira connector cannot download an attachment/image, the run names it and asks the QA member to place it in inbox/ | 2026-10-15 |
| 2.1 Checkpoint after analysis | **Merged with the test cases:** no separate stop; questions + defaults shown at the case approval; cases built on a default are marked and re-shaped only if the answer changes | 2026-10-15 |
| 2.2 Long knowledge gap | **Any screen in the ticket never trained** (no business page / walk-through) -> stop, ask for training, no cases | 2026-10-15 |
| 2.3 Unanswered questions | **Proceed on the default, mark affected cases, park the question** for Syed Kamran / BA; re-shape when answered | 2026-10-15 |
| 2.2 note | "Trained" = the screen has a business page AND a saved screen file (see 3.1) | 2026-10-15 |
| 3.1 Screen sheet source | **Made during training, not per ticket.** When a screen is trained (by any means: database, user guide, verbal), Claude also reads the screen (config tables where available and/or a read-only live look) and saves its screen file. A ticket run uses the saved file; a screen without one is a long gap (2.2) | 2026-10-15 |
| 3.2 Hand-coded screens | **One-time read-only AI look** during training, saved as the screen file | 2026-10-15 |
| 3.3 Config vs live differ | **Live wins**; the difference is written to the screen file and reported (deployment gap or defect) | 2026-10-15 |
| 3 action | Backfill screen files for screens already trained (group 11 / 66 walks, Distributor Profile HQ/DT, ...) from existing recordings + a read-only look | 2026-10-15 |
| 4.1 Core cases | **No fixed cap** - as many as the rules/ACs need; the QA member trims at approval (replaces the cap of 10 in qaos_run.py validate) | 2026-10-15 |
| 4.2 Backlog | **Ideas only:** one line each (title + why); steps only when the QA member promotes one to core | 2026-10-15 |
| 4.3 Case types | **All:** positive + negative, boundary / update rules, business effect, regression (linked bugs) | 2026-10-15 |
| 4.4 Missing data | **Checked at design, before approval** (read-only); case marked "needs data: X" at approval | 2026-10-15 |
| 5.1 AI case per path | **AI picks** the case covering most of the path (usually the full positive flow); shown at approval; QA member may swap | 2026-10-15 |
| 5.2 Negative cases on the same screens | **Same path, data rows** (CASE_TYPE + EXPECTED_MESSAGE, framework style); AI runs only the positive case | 2026-10-15 |
| 5.3 AI run of a path fails | **Path blocked:** its data rows wait until fixed or accepted | 2026-10-15 |
| 5.2 note | The program must assert error messages exactly (toast, inline under field, popup, alert); Regress Master cannot assert alert text (flag) | 2026-10-15 |
| 6.1 Step language | **Plain English** that both the QA member and the AI can execute (no codes in the step text) | 2026-10-15 |
| 6.2 Load data | A step may say "Load data into <screen/tab>"; **the AI decides which fields get which data-row values** while executing. Its run captures the mapping (field id <-> data column), which the program then reuses for the path's data rows and script generation | 2026-10-15 |
| 6.3 Excel view | **Sentence + event columns:** the plain-English sentence, plus grouped (hideable) columns event / element id / data column, filled in from the screen file at design and confirmed by the AI run | 2026-10-15 |
| 7.1 Approval with non-ready cases | **Yes, with labels:** ready cases run; needs-data / needs-knowledge cases wait with the reason; nothing blocks the whole ticket | 2026-10-15 |
| 7.2 Step not matched to the screen file | **Needs knowledge:** the case waits until the screen file is updated in training (no live guessing) | 2026-10-15 |
| 8.1 Approvals | **One approval:** one Excel with questions + defaults, cases, paths (AI case marked), steps, data rows, readiness | 2026-10-15 |
| 8.2 Approver | **The QA member who runs the ticket** | 2026-10-15 |
| 8.3 After Excel edits | **Import, re-run the pre-run check, show only the diff and new problems**, then execute | 2026-10-15 |
| 9.1 Missing records | **Created through the application's own screens as setup steps in the approved plan** (e.g. "Create DSR AUTO151015"); never directly in the DB | 2026-10-15 |
| 9.2 Cleanup | **Shared master data only** (distributor profile, users, settings) restored to starting values; records the test created stay, with an AUTO prefix | 2026-10-15 |
| 9.3 Starting state | **Read on screen first:** each case reads and records the fields it depends on; expected results are relative to that | 2026-10-15 |
| 10.1 Executor / password | **No separate runner program in QA OS execution: the AI executes** (browser MCP). Password as now: Claude types the user ID, the QA member types the password. Deterministic replay of data rows = Regress Master after script generation | 2026-10-15 |
| 10.2 Case start | **One login per user role for the whole run;** each case/path starts by reopening its screen from the menu; logout/login only when the actor changes (replaces "fresh login per test case") | 2026-10-15 |
| 10.3 Role order | **Batch by role:** all Maker work of all paths first, one switch to the Checker for all approvals, back only if needed | 2026-10-15 |
| 10 note | AI execution must be fast on its own: steps carry element ids from the screen file (1-2 actions per step), one login per role, screen lessons loaded as data, one recorder per role session | 2026-10-15 |
| 11.1 AI executes | **One case per path;** other cases of the path (incl. negatives) are data rows replayed only by Regress Master | 2026-10-15 |
| 11.2 Step differs from prediction | **Always stop and ask** the QA member (strict; no self-fixing). The answer is recorded (screen lesson or step fix) so the same question is not asked again | 2026-10-15 |
| 11.3 Recorder agents | **One recorder per role session:** all paths of a role in one browser session; a new recorder only at a role switch or its turn limit | 2026-10-15 |
| 11.4 Confirmed defect | **Stops only that path**; other paths continue | 2026-10-15 |
| 12 | Old step 12 (a QA OS program runs data rows) **dropped**: Regress Master replays data rows after script generation | 2026-10-15 |
| 12.1 Negative messages | **AI checks unknown ones:** a negative row whose message is not yet known (business pages / earlier runs) is run live once by the AI to capture the exact message; known messages are used as predicted | 2026-10-15 |
| 13.1 Defects | **Jira-ready draft** (title, steps, expected vs actual, exact message, evidence path); the QA member posts it | 2026-10-15 |
| 13.2 Report | **Excel (actual result / status / evidence) + one-page summary** (pass/fail per path, defects, parked questions, next action) | 2026-10-15 |
| 14.1 Script generation | **After every passing path, automatically:** SQL + rollback + case-data Excel with all its data rows | 2026-10-15 |
| 14.2 Apply + first replay | **Framework owner** (name to be given) | 2026-10-15 |
| 15.1 Verification | **Before handing over scripts:** verifier checks trace and SQL before anyone applies them | 2026-10-15 |
| 16.1 Learning loop | Covered by 0.2 (screen lessons automatic; business rules need confirmation) | 2026-10-15 |
| 17.1 QA installation | QA members may change **business knowledge**. Any attempt to change the QA OS design (skills, agents, tools, schemas, rules) is **stopped**: Claude refuses and asks them to contact the QA OS administrator (Syed Kamran); the request is noted in feedback/design_gaps.md | 2026-10-15 |

## Open items
- Name of the framework owner (14.2).
- Read access to environment config tables (helps screen files; not required - 3.1 allows any training source).
- Backfill screen files for already-trained screens (3 action).
- Implementation plan for v4 (after review of this log).
