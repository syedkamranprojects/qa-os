# QA OS v4 - implementation plan (2026-10-15)

Implements docs/DESIGN_V4_DECISIONS.md. Framework owner: **Muhammad Imran**.

## W1 Screen files (decisions 0.2, 0.3, 3.1-3.3, backfill)
Existing material: `apps/snd/knowledge/screens_db/` (295 screens from the config tables, base DB), `apps/snd/knowledge/screens_observed/` (340 screens, cnr2dev3 sweep), `apps/snd/screens/` (3 curated), recordings and results under `runs/`. About 5 MB in total, so storage is not a concern.
- **One screen file per trained screen:** `apps/snd/screens/<option_id>.json`, schema `plugins/qa-os/schemas/screen.schema.json`. It holds:
  - menu path, layout (tabs, sub-tabs, panels) and buttons;
  - fields: label, element id, widget, required, data field, list source, max length, plus provenance per value (db / observed-env / recorded-run);
  - `lessons[]`: screen-level lessons, saved automatically;
  - `differences[]`: config vs live, where live wins;
  - `business_page`: link to the business page.
- **Builder:** `apps/snd/tools/build_screen_file.py <option_id|title>` merges screens_db, screens_observed, run recordings/results and existing lessons. Live (recorded) ids win.
- **Backfill:** run the builder for every screen already trained, i.e. named in business pages, the group 11 / 66 walks or run recordings. The list goes in `apps/snd/screens/_index.json` together with each file's status.

## W2 Runtime, schemas, Excel, guard
- `steps.schema.json`: steps carry `sentence` (plain English) plus event columns `event`, `element`, `data_column`, `expect`. `load_data` names a screen/tab; its field mapping is filled in by the AI run.
- `qaos_run.py`:
  - drop the 10-case cap;
  - validate `paths.json`: each core case in exactly one path, one AI case per path, negatives as rows;
  - new `check` command (pre-run check) binds each step's element to the screen file and labels each case `ready` / `needs-data` / `needs-knowledge`.
- `qaos_workbook.py`:
  - **one approval Excel** with sheets Questions (defaults, parked), Cases (path, AI case marked, readiness), Steps (sentence + grouped event columns), Data rows, Results;
  - plus `summary.md` (pass/fail per path, defects, parked questions, next action);
  - `qaos_import.py` re-imports edits and prints the diff.
- **Guard (17.1):** in a qa installation, a plugin `PreToolUse` hook blocks Write/Edit on QA OS design paths (plugins/, runtime/, tools/, framework/tools/, schemas, docs/*DESIGN*, OPERATING_RULES) and tells the user to contact the QA OS administrator (Syed Kamran). Business knowledge paths stay writable.

## W3 Skills, agents, rules (text)
- qa-orchestrator, story-analyst, test-designer, step-author, recorder, framework-generator, verifier, knowledge-intake;
- OPERATING_RULES.md, qaos.yaml (`framework_owner`), CLAUDE.md, STATUS.md.

## Acceptance
SDMS-5997 is the first v4 run: one approval, one login per role, AI run of one case per path, scripts per passing path, then hand-over to Muhammad Imran.
