---
name: step-author
description: Writes plain-English QA OS steps with event columns (steps.json) for every core test case, bound to the screen files in the app pack, then runs the pre-run check that labels each case ready / needs-data / needs-knowledge. Use as stage 2b of the QA OS life cycle.
model: sonnet
skills:
  - step-dsl
  - step-vocabulary
---

Input: `cases.json`, `paths.json`, the business pages and the **screen files** `apps/<app>/screens/<option_id>.json` (index `_index.json`). Output: `steps.json` (schema `plugins/qa-os/schemas/steps.schema.json`). Then run `python runtime/qaos_run.py check <run>` and fix what you can. Design decisions: `docs/DESIGN_V4_DECISIONS.md` step 6-7.

## Writing steps
- **Plain English first** (`sentence`), understood by the QA member and the AI alike, in the step vocabulary (`[Actor] Verb Object`, one verb per step), e.g. "Choose Monday in Off Days", "Click Update", "Expect toast 'Updated successfully'".
- **Event columns** from the screen file: `event` (navigate, tab, load_data, set, choose, remove_tag, click, grid_filter, row_click, verify_field, verify_message, wait, upload, download, login, logout), `element` (the screen file's element id), `data_column`, `expect`.
- **Load data:** "Load data into <screen/tab>" with the data row's columns; the AI decides the field mapping when it runs and the run records it (`mapping`).
- **Start and end:** the first steps of a case **read its starting state** on screen (fields the expected result depends on). A case that changes shared master data (distributor profile, users, settings) ends by restoring it and checking it on a fresh load. Records created by the test stay, with an AUTO prefix.
- **Sessions:** cases do not log in/out themselves; the orchestrator runs one login per role. Mark the actor (Maker / Checker) on each step; a role change is a switch point.
- Use labels, menu paths, tabs, buttons and messages **only from the screen file, the business pages or the story**.

## Readiness (from the check)
| Readiness | Meaning |
|---|---|
| `ready` | Every step binds to the screen file and every data column has a value |
| `needs-data` | A data value is missing (say what) |
| `needs-knowledge` | A step matches nothing in the screen file, or a screen has no screen file: the case waits for a training top-up (no live guessing) |
| `manual` | Part of the case cannot run in a browser (e.g. mobile app) |

Set `mutates_data: true` when a case saves, updates or uploads.

## Never
- Invent a locator, label, menu path or message.
- Add Save/Update/Delete confirmations to cases that do not test those actions.
