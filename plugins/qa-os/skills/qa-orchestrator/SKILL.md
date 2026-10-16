---
name: qa-orchestrator
description: QA OS life cycle for a Jira story (intake -> analyse -> cases + paths + steps -> one approval -> AI run of one case per path -> scripts per passing path). Use when a QA user pastes a story or asks to run, continue or check the QA cycle for a ticket.
---

# QA OS orchestrator (v4, design agreed 2026-10-15)

Design decisions: `qa-os/docs/DESIGN_V4_DECISIONS.md` (wins over older docs). Questions to users: `qa-os/docs/QUESTION_BANK.md`. You run in the **main session** and stay thin: keep state in `runs/<KEY>/<timestamp>/run.json`, give each stage to its agent with a short brief (input files -> output file), check the output, update `run.json`. Never load full case lists, screen catalogs or the access data into your own context; query them with the tools below.

## Principles
- **The AI intern:** trained knowledge (business pages + screen files) -> cases and plain-English steps -> the AI executes **one case per path** -> scripts -> Regress Master replays all data rows. There is no separate runner program in QA OS.
- **Login:** Claude types the user ID, the QA member types the password. Never type, read or request passwords. **One login per user role for the whole run** (not per case); a case starts by reopening its screen.
- **Ask once:** all questions go out in one batch, at the single approval. A question without an answer proceeds on its default, is marked on the affected cases and is parked for the QA lead / BA.
- **Steps are the prediction:** during execution any difference from the predicted result stops the path and is asked (no silent fixing).

**Installation (dev / qa).** At the start run `python runtime/qaos_config.py mode`. **dev** = the QA OS team's working copy (`qaos.dev.yaml`); **qa** = the QA team's release (`release.json`). In a **qa** installation the trainers may change **business knowledge**; any attempt to change the QA OS design is **refused** ("please contact the QA OS owner, Muhammad Fahad") and noted in `feedback/design_gaps.md`; a plugin hook (`plugins/qa-os/hooks/design_guard.js`) enforces this. In **dev**, gaps go to `docs/HARDENING.md` and are fixed.

**Ownership (from 2026-10-19, email of 2026-10-16):** QA OS is owned by **Muhammad Fahad**. His machine is always a **qa** installation (release zip, no git). Only **Muhammad Fahad, Feroz Hussain and Syed Zulfiqar** may train QA OS: check the trainer with `python runtime/qaos_config.py trainer "<name>"` and refuse training from anyone else. Important design or tool changes are not made on the QA machine: the owner sends a **patch** (`python runtime/qaos_patch.py export --note "<what is needed>"`) to **Syed Kamran** (design contact, limited availability), who applies it in the dev copy and sends back a new release.

## Stage 0 - intake
1. **Run context is asked every time** (QA lead 2026-10-15): market, environment, run by, Maker, Checker, distributor. Current ticket work is Pakistan only: stop a ticket of another market here. Any QA member may start a run.
2. `python runtime/qaos_run.py init <KEY> --app <app> --env <env> [--story <file>]`, then `python runtime/qaos_intake.py parse <run> [--story <file>] [--screens "A;B"]` (intake block, account check, bounded authorization: one-way actions count only if named in `allow:` and the env is `non_production`).
3. Account check when screens are known: `python apps/<app>/tools/access_lookup.py plan-user "<screen>" ... [--org <orgcode>]`.

## Stage 1 - analyse (no separate stop)
- story-analyst reads the story **plus comments, linked bugs, subtasks and attachments/images** (if the connector cannot download an attachment, name it and ask the QA member to put it in `inbox/`). Output `requirement.json` + `BA_NOTE.md`; `qaos_run.py validate`; `stage analyse done`.
- **Knowledge-gap gate:** a screen in the ticket is *trained* when it has a business page **and** a screen file (`apps/<app>/screens/<option_id>.json`, see `apps/<app>/screens/_index.json`). **Any untrained screen = long gap:** stop, say what is missing, ask for training (`/qa-os:train`), write no cases. Short gaps (a value, a rule, a message) get a default and are asked at the approval.
- Do **not** stop for the ambiguities here: they go to the approval workbook (Questions sheet) with their defaults.

## Stage 2 - cases, paths, steps, data (test-designer, then step-author)
- **test-designer:** no fixed cap on core cases (the QA member trims); case types positive + negative, boundary/update rules, business effect, regression (one per still-relevant linked bug); backlog = one-line ideas only (title + why). **Data availability is checked now** (read-only): a case whose data does not exist is marked `needs data: <what>`; data the plan may create is created through the app's own screens as setup steps (AUTO-prefixed names), never in the DB.
- **Paths** (`<run>/paths.json`): cases with the same screen flow form one path; negatives on the same screens (ending in an error message) are **data rows** of that path with CASE_TYPE + EXPECTED_MESSAGE. The AI picks the path's **AI case** (the one covering most of the flow, usually the full positive one); the QA member may swap it.
- **step-author:** plain-English steps (`sentence`) that the QA member and the AI both understand, plus event columns (`event`, `element`, `data_column`, `expect`) bound to the screen file. "Load data into <screen/tab>" is allowed: the AI decides the field mapping when it runs and the run records it. Each case starts by **reading its starting state on screen**; cases that change shared master data (distributor profile, users, settings) end by restoring it.
- **Pre-run check:** `python runtime/qaos_run.py check <run>` binds every step to the screen file and labels each case `ready` / `needs-data` / `needs-knowledge`. A step that matches nothing in the screen file makes its case **needs-knowledge** (training top-up, no live guessing).

## Stage 3 - ONE approval (QA member who runs the ticket)
- `python runtime/qaos_workbook.py <run>` -> one workbook: Questions (defaults, parked), Cases (path, AI case, readiness + reason), Steps (sentence + collapsible event columns), Data rows, Results.
- Approval phrases: "approved", "go ahead", "yes", "LGTM", "looks good". Edits made in the Excel are imported with `runtime/qaos_import.py`, which re-runs the check and shows only the diff and new problems; approve again only if something changed.
- Approval may go ahead with some cases not ready: ready cases run, the others wait with their reason.

## Stage 4 - AI execution (agent `recorder`, skill `recording-protocol`)
- **Order by role:** all Maker work of all paths first, then **one** switch to the Checker for all approvals, back only if a later step needs it.
- **One recorder per role session:** it runs the AI case of every path of that role in one browser session (a new recorder only at a role switch or its turn limit). Brief: run folder, the approved steps of those cases, their data rows, the screen files and their lessons, the run context. It types only the user ID and returns "READY FOR PASSWORD"; relay it, pass the QA member's reply back.
- **Unknown negative messages:** a negative data row whose expected message is not yet known (business pages / earlier runs) is run once live by the AI to capture the exact message; known messages stay predicted.
- **Any difference from the prediction stops that path and is asked** (QA lead 2026-10-15). The answer is recorded (screen lesson in the screen file, or a step fix) so it is not asked again. A confirmed defect stops only its own path; a path whose AI run fails is **blocked** (its data rows wait).
- Screen-level lessons found in the run are saved to the screen file automatically; new business rules are proposed and wait for QA / QA lead confirmation.

## Stage 5 - scripts after every passing path (framework-generator, verifier)
- For **each path whose AI run passed**, framework-generator produces SQL + rollback + the case-data workbook with all the path's data rows (`framework/`). It never applies SQL.
- **verifier** (read-only) checks trace and SQL before hand-over -> `review.md`.
- Hand-over to the **framework owner, Muhammad Imran** (`qaos.yaml` > `installation.framework_owner`), who applies the SQL on a test copy and replays it first in Regress Master.

## Stage 6 - report and learning
- Results in the workbook (actual result / status / evidence) + `<run>/summary.md` (pass/fail per path, defects, parked questions, next action). Each defect gets a **Jira-ready draft** (title, steps, expected vs actual, exact message, evidence path); the QA member posts it. Never post to Jira yourself.
- `python runtime/qaos_promote.py <run>` (dry run, then `--apply` after OK) for reusable decisions.

## Tools (Claude runs these; QA users do not)
| Tool | Use |
|---|---|
| `apps/<app>/tools/access_lookup.py` | `plan-user`, `screen`, `user --can`, `features`, `diff-features` |
| `apps/<app>/tools/build_screen_file.py` | build / refresh a screen file (config + observed + recordings; live wins) |
| `plugins/qa-os/runtime/qaos_helpers.js` | page helper injected via the browser MCP |
| `framework/tools/qaos_record_multi.py`, `gen_framework_sql.py` | recording + rows -> flow spec + case data -> SQL + workbook |
| `runtime/qaos_run.py` | run folder, `validate` (schemas, paths), `check` (pre-run check), stage state |
| `runtime/qaos_intake.py` | `parse`, `answer`, `show` |
| `runtime/qaos_workbook.py` / `runtime/qaos_import.py` | approval workbook + summary / import of QA edits with diff |
| `runtime/qaos_promote.py` | dry-run / `--apply` promotion of reusable decisions |
