---
name: quick-script
description: The main way to use QA OS after training - an ad-hoc request or one-liner, no Jira ticket (e.g. "book an order with two products", "create one order and order detail") -> Claude plans the test from its trained business knowledge, executes it ONCE live in the browser as an AI test run, and reports the result (pass/fail, messages, documents, defects). The run is always recorded silently; ONLY if the run passed and the QA member says yes, Claude generates Regress Master scripts (selenium-framework-db / CTA_CONFIG_ASSERTION SQL + rollback + case-data workbook) from that recording. Use when a QA member gives a scenario in a sentence or a few lines, types /qa-os:quick, or asks to generate scripts for an earlier quick run.
---

# Quick mode: ad-hoc request -> AI test run -> test result (-> Regress Master scripts on request)

After S&D training, QA members do **not** start from Jira tickets. They give Claude an **ad-hoc request or one-liner** to be **tested**. The purpose of quick mode is the **AI execution cycle for testing** (QA lead, 2026-10-08): Claude plans the test, executes it once live, and reports the result. **Regress Master scripts are optional**: only when the run passed and the QA member wants to keep the flow for Regress Master. Runs in the **main session**. Stops only for: the run context (Q0), one approval (gate QG), the logins, anything the training does not cover, and the scripts question after a pass.

## The phases and what each may use (QA lead, 2026-10-07/08)
| Phase | Uses | Never uses |
|---|---|---|
| Training (separate, `/qa-os:train`) | trainer's documents, explanation, live walks | - |
| **Q0-Q3 plan: the case, the steps and the data** (no app, no app DB) | **Claude's trained knowledge** incl. the test data catalog (`apps/<app>/knowledge/business/`, session logs, `[stated]` rules) to decide the actions, screens, data and expected messages, and to write the steps | old Selenium framework flows, event chains, workbooks |
| **Q4 AI test run (one execution)** | **only the approved steps + the data row**; screens, elements, element ids, tabs/tab ids and messages are DISCOVERED live and noted | training pages, session logs, UI hints from training, framework atlas/flows/ids/workbooks |
| **Q6 scripts (optional, after a pass)** | **only what Q4 recorded** + the data rows; the framework DB only for table structure, required columns, valid event pairs and free ids | copying, mirroring or reusing existing flows, screens or field definitions |

1. **No ticket, and the request IS the test case.** The request text is the requirement and the case: do not design a case list or ask for a Jira key. Only when the request itself asks for cases ("... with 5 positive test cases") are several cases written (they become extra data rows if scripts are generated).
2. **Steps are an internal plan, not a deliverable.** They must still be **complete on their own** - every action needed, in order, with real values (including choices a cascade needs) - because the executor follows only them. They are shown in the one approval (QG) and kept in the run folder for audit; the QA member does not receive a "test steps document".
3. **The main output is the test result**: pass / fail per step, the messages seen (exact text and type), the documents created, evidence, and any defect found.

**Strict mode (QA environment):** run the phases exactly as written - no changes to tools, skills, framework design or recordings during a run, no hand edits; on a failure STOP and report (step, message, evidence). Development fixes belong in `docs/HARDENING.md`, not in a run.

Never type credentials, never apply SQL, never post to Jira. Data-changing steps only on an env with `non_production: true` (`apps/<app>/app.yaml`).

## Knowledge-gap gate (QA lead rule, 2026-10-08) - before ANY AI execution or script generation
Before executing (Q4) or generating scripts (Q6), check that the knowledge needed is present (business pages with `[observed]`/`[stated]` facts for every action, screen, rule, message and data choice). If something is missing, **ask the user** and classify the gap:
| Gap | Examples | Action |
|---|---|---|
| **Short / ad-hoc** (answerable in chat in a few lines) | a value or data choice, which outlet type to use, the meaning of a field, an expected message, one business rule, which user/role | Ask with `AskUserQuestion` (or plainly); record the answer as `[stated <date> <name>]` in the run's `decisions.json` and, if reusable, in the business page (knowledge-intake method B); then **continue the run** |
| **Long-term** (needs a training session) | an untrained screen, module or business process (e.g. creating a promotion in Promotion Layout), an unknown market setup, a chain of several untrained options | Say what is missing and ask for training (`/qa-os:train <app>`: explain, documents or a walk). **Do NOT execute or generate scripts** until it is trained; the run stays paused at this gate |
Never guess to fill a gap, and never take the missing knowledge from old framework flows or workbooks. Areas marked partially trained (e.g. promotions: `promotions_and_budget/README.md`) follow that page's "ask when needed" rule.

## Q0. Understand the request
1. **Clarify the run context FIRST - before anything else (QA lead rule, 2026-10-08).** Ask the QA member in **one** `AskUserQuestion` call, with the options read from `apps/<app>/app.yaml` (first option = what the request says, else the usual value, marked "(Recommended)"):
   - **Market** (`markets:` - e.g. PK, BD);
   - **Environment** (`environments:` with `non_production: true`; the market's `env` first);
   - **Who is running it** (the QA member's name, for the record - free text via "Other");
   - **Users**: the Maker (and the Checker if the flow has an approval) from the market's `roles` - user ids only, never passwords;
   - and anything else the request leaves open that changes the run (e.g. which actions are allowed: save only / save + forward / approve).
   Never assume these silently, even when there is an obvious default. Company and distributor are NOT asked: they follow from the market and user in `app.yaml`. An answer that does not match `app.yaml` is rejected by `qaos_run.py init` - ask again. The confirmed context is stored in `run.json` (`context`) and, if scripts are generated, printed in the header of `framework.sql` and `framework_rollback.sql`.
2. Turn the request into **business actions** and **menu options** using the business pages (start at `INDEX.md`, glossary, the option's L3 page). E.g. "order and order detail with two products" -> Order Booking (header + 2 detail lines), Maker only.
3. **Chains are allowed** when the request asks for them (e.g. "book an order, allocate it and make the GIN"): list the actions in business order, with the role per action and the switch points (Maker -> Checker). The whole chain runs on **one calendar day**; apply the carry-over checks in `docs/STATUS.md` and the run rules in `docs/OPERATING_RULES.md`.
4. **Is every option trained?** Apply the knowledge-gap gate. Never improvise an untrained screen.

## Q1. Create the run
1. Key `QUICK-<yyyymmdd>-<hhmm>`. Write the request to a story file (scratchpad):
   ```
   <the request, verbatim>

   --- QA-OS ---
   market: <M>
   env: <env>
   user: <the market's Maker, e.g. Auto_Multi_Orga for PK, Auto_Bangla for BD>
   screens: <Menu option 1>; <Menu option 2>
   allow: save, forward, approve      (only what the scenario needs)
   --- /QA-OS ---
   ```
   `screens` = **menu options only** (e.g. `Order Booking`), never tabs/detail grids. Always name the market's Maker as `user`.
2. `python runtime/qaos_run.py init <KEY> --app <app> --env <env> --story <file> --request "<the request, verbatim>" --screens "<options>" --market <M> --run-by "<QA member>" --maker <user> [--checker <user>] [--allow "save,forward"]` (writes `run.json` context + `requirement.json` with R1 = the request; refuses a context that does not match `app.yaml`), then `python runtime/qaos_intake.py parse <run> --screens "<options>"`. Mention only warnings that need a decision.
3. `cases.json` for bookkeeping only: **one case TC01 = the request** (title = the request in test wording, trace R1, expected = the business result). Only if the request asks for N cases, write TC01..TCn (skill `case-format`, different data per case). `qaos_run.py validate <run>`; `stage <run> cases done`.

## Q2. Plan the steps and pick the data (Claude's own work, internal)
- **Steps:** write them in the standard vocabulary (`step-vocabulary`): `[Maker] Navigate to Order Booking`, `[Maker] Select PJP = ...`, `[Maker] Add line Product = ..., Order CS = 2`, `[Maker] Click Validation`, `Verify message "Validation successfully"`, `[Maker] Click Save`, `Verify message "Order Save successfully"` ... Source = the business page of each option and the session logs where it was done live. Check every label: `python runtime/qaos_steps.py check "<step>"`. Expected messages come only from what training observed or stated; anything else is marked `to be observed`. Write a `Verify message "<text>"` step after **every** action that shows a toast, alert or popup (and the button to press for an alert/popup).
- **Data: from training only** (QA lead rule, 2026-10-08). Q2 does not open the app or query the app DB. Take every value from the trained knowledge, mainly the market's **test data catalog** (`apps/<app>/knowledge/business/test_data/<market>.md`), plus the business pages' rules (e.g. an order draws stock from its PJP's warehouse; respect the zero-tax rule). Never use the old framework workbooks.
  - Catalog does not cover the request -> **knowledge gap**: short -> ask and record (also into the catalog); long-term -> ask for training and stop.
  - **Live state is checked in execution**: anything that depends on today's state (stock for the chosen SKUs, documents of the day) becomes **precondition steps at the top of the step sheet** (e.g. `Navigate to Stock Inquiry; Verify Closing of <SKU> >= <qty>`); they run before the recording starts. If a precondition fails, the run stops and reports; a setup step (e.g. Dispatch Advice + approval) is only done if it is in the approved plan or the QA member approves it then.
  - Documents the chain needs are created by earlier steps of the same run, never reused from an earlier day.
  Write `<run>/data.json` (the executed case's row; values exactly as typed or picked - codes, not display text), `<run>/rows.json` (a list with the row of every case; one entry when the request is the only case) and `<run>/step_sheet.md` (template in `step-vocabulary`).

## Q3. Gate QG - one approval
One compact message: the request as understood (= the case), actions and roles, the steps, the data, the preconditions, where logins happen, what changes in the environment (documents created), and that the result is a **test report** (scripts only if wanted after a pass). Ask once with `AskUserQuestion`: **Approve / Change something**. Anything other than approval is feedback -> fix and show again (same run). Nothing executes before QG.

## Q4. AI test run - execute ONCE, always recorded
Delegate to the **recorder** agent (skill `recording-protocol`) with **only**: run folder, the case id, app, env, the approved step sheet and the data row (`data.json`) - **the step sheet is the only script it follows**. No app knowledge in the brief (no business-page paths, no UI hints, no element ids, no framework flow ids); the recorder discovers screens, elements, ids, tabs and messages itself. Relay switch points to the QA member (who to log in as; Claude may press Login when asked; Claude selects company/distributor) and pass "logged in" back.
- **The run is always recorded silently** (helper + watcher injected before step 1): `recording_<case>.json` is written for every run that reaches its last step, whether or not scripts are wanted, so scripts can be generated later **without re-executing**.
- When the request asks for N cases, execute **one representative case only** (the one that touches the most of the flow); the others are data rows for scripts, never executed one by one.
- A failed step: stop, record step / message / evidence; if the steps were incomplete or the screen differs, ask the QA member (short gap) and record the answer as `[stated <date> <name>]`.

## Q5. Test report (always)
Write `<run>/test_report.md` and tell the QA member in one short message:
- **Result: PASS / FAIL / BLOCKED** (PASS only when every step passed with an observed message or state; nothing visibly failing is not a pass).
- Per step: result and the observed message (exact text and type: toast / alert / popup / inline).
- Documents created (numbers), amounts seen (not asserted unless trained), preconditions and setup done.
- **Defects** (expected vs actual, evidence) and anything unverified; friction found (`friction.md`).

## Q6. Regress Master scripts - only after a PASS, only on request
- After a **PASS**, ask once with `AskUserQuestion`: **"Do you want Regress Master scripts for this flow?"** - *Yes, for this case* / *Yes, with more data rows* / *No*. After a FAIL or BLOCKED run, do not ask (a failed recording never becomes scripts).
- **No** -> the run ends with the test report (`stage <run> scripts skipped`). The recording stays in the run folder; the QA member may ask later ("generate scripts for QUICK-<key>") - then resume here.
- **Yes** -> rows: default = the executed case only; with more data rows -> propose the extra rows from the test data catalog (different outlets / products / quantities, same flow), one approval, write them to `rows.json` (+ cases in `cases.json`).
- Then delegate to **framework-generator** (skill `framework-conventions`) with the passing recording and `cases.json` + `rows.json` (it runs `framework/tools/qaos_record_multi.py ... --rows rows.json --cases cases.json --run <run>`, then `gen_framework_sql.py`; the run context lands in the SQL header): `flow_spec.json`, `framework.sql`, `framework_rollback.sql`, the case-data workbook (one header row per case, `PK` 01..N, detail lines `01-01` ...; `EXPECTED_MESSAGE` = the messages observed in Q4) and `review_note.md`, all under `<run>/framework/`. Rows not executed live are marked "not executed by AI" in the review note. Screens, fields, ids, tabs, events and messages come **only from the Q4 recording**; a gap in the recording means a re-recording, not borrowing from elsewhere. Then delegate to **verifier** (read-only) -> `review.md`, and report how to apply and run them (the framework owner applies the SQL on a test copy first; flow / group; workbook and the `casedata` folder).

**Bookkeeping (every phase):** `python runtime/qaos_run.py stage <run> <stage> <running|done|failed|needs-input|skipped>` - `steps` and `data` at the end of Q2, `execute` around Q4 (`failed` with `--note` when the run stops), `report` at Q5, `scripts` and `verify` in Q6 (`skipped` when no scripts are wanted). `qaos_run.py status` must show where every quick run stopped.

## Limits
- A request that needs an untrained option -> train first.
- Unknown market difference -> `access_lookup.py features` / `diff-features`, then ask.
- Generated SQL is a draft until the framework owner applies it on a test copy and Regress Master replays it.
