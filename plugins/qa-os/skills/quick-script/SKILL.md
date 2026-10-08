---
name: quick-script
description: The main way to use QA OS after training - a short request or one-liner, no Jira ticket (e.g. "create one order and order detail with two products script", "... with 5 positive test cases") -> Claude writes its own test steps from its trained business knowledge, picks live data, executes the flow ONCE in the browser (to capture element ids and messages), and generates Regress Master scripts with one case-data row per requested case (selenium-framework-db / CTA_CONFIG_ASSERTION SQL + rollback + case-data workbook). Use when a QA member gives a scenario in a sentence or a few lines, or types /qa-os:quick.
---

# Quick mode: short request -> AI cycle -> Regress Master SQL

After S&D training, QA members do **not** start from Jira tickets. They give Claude a **short request or one-liner**; Claude runs the whole AI cycle and produces the SQL scripts for **Regress Master** (the legacy Selenium Regress framework, tables in `selenium-framework-db` / `CTA_CONFIG_ASSERTION`) plus the case-data workbook. Runs in the **main session**. Stops only for: one approval (gate QG), the logins, and anything the training does not cover.

## The four phases and what each may use (QA lead, 2026-10-07/08)
| Phase | Uses | Never uses |
|---|---|---|
| Training (separate, `/qa-os:train`) | trainer's documents, explanation, live walks | - |
| **Q0-Q3 cases, test steps and test data** (no app, no app DB) | **Claude's trained knowledge** incl. the test data catalog (`apps/<app>/knowledge/business/`, session logs, `[stated]` rules) to decide the actions, screens, data and expected messages, and to write the steps | old Selenium framework flows, event chains, workbooks |
| **Q4 execution (one case)** | **only the approved test steps + that case's data row**; screens, elements, element ids, tabs/tab ids and messages are DISCOVERED live and noted | training pages, session logs, UI hints from training, framework atlas/flows/ids/workbooks |
| **Q5 generation** | **only what Q4 noted** + the cases' data rows; the framework DB only for table structure, required columns, valid event pairs and free ids | copying, mirroring or reusing existing flows, screens or field definitions |

1. **No ticket.** The request text is the requirement. Do not ask for a Jira key.
2. The steps must therefore be **complete on their own**: every action needed to perform the flow, in order, with real values (including choices a cascade needs, e.g. a dropdown that does not fill itself). The executor will know nothing else.

**Strict mode (QA environment):** run the phases exactly as written - no changes to tools, skills, framework design or recordings during a run, no hand edits; on a failure STOP and report (step, message, evidence). Development fixes belong in `docs/HARDENING.md`, not in a run.

Never type credentials, never apply SQL, never post to Jira. Data-changing steps only on an env with `non_production: true` (`apps/<app>/app.yaml`).

## Knowledge-gap gate (QA lead rule, 2026-10-08) - before ANY AI execution or script generation
Before executing an AI flow (recording) or generating scripts, check that the knowledge needed is present (business pages with `[observed]`/`[stated]` facts for every action, screen, rule, message and data choice). If something is missing, **ask the user** and classify the gap:
| Gap | Examples | Action |
|---|---|---|
| **Short / ad-hoc** (answerable in chat in a few lines) | a value or data choice, which outlet type to use, the meaning of a field, an expected message, one business rule, which user/role | Ask with `AskUserQuestion` (or plainly); record the answer as `[stated <date> <name>]` in the run's `decisions.json` and, if reusable, in the business page (knowledge-intake method B); then **continue the run** |
| **Long-term** (needs a training session) | an untrained screen, module or business process (e.g. incentive -> credit note chain), an unknown market setup, a chain of several untrained options | Say what is missing and ask for training (`/qa-os:train <app>`: explain, documents or a walk). **Do NOT execute the story/flow or generate scripts** until it is trained; the run stays paused at this gate |
Never guess to fill a gap, and never take the missing knowledge from old framework flows or workbooks.

## Q0. Understand the request
1. Defaults: app `snd`, market `PK`, env `cnr1dev1`; users = the market's Maker/Checker from `app.yaml`. A market word in the request (BD, Bangladesh...) overrides.
2. Turn the request into **business actions** and **menu options** using the business pages (start at `INDEX.md`, glossary, the option's L3 page). E.g. "order and order detail with two products" -> Order Booking (header + 2 detail lines), Maker only.
3. **Chains are allowed** when the request asks for them (e.g. "book an order, allocate it and make the GIN"): list the actions in business order, with the role per action and the switch points (Maker -> Checker). The whole chain runs on **one calendar day**; apply the carry-over checks in `docs/STATUS.md` and the run rules in `docs/OPERATING_RULES.md`.
4. **Is every option trained?** Apply the knowledge-gap gate above: each option needs a business page with `[observed]` or `[stated]` steps, messages and rules. A short gap -> ask and continue; a long-term gap (untrained option/process) -> ask for training and do not execute. Never improvise an untrained screen.

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
   `screens` = **menu options only** (e.g. `Order Booking`), never tabs/detail grids. Always name the market's Maker as `user` (otherwise the account selector may pick a head-office account).
2. `python runtime/qaos_run.py init <KEY> --app <app> --env <env> --story <file>`, then `python runtime/qaos_intake.py parse <run> --screens "<options>"`. Mention only warnings that need a decision.
3. `cases.json` (skill `case-format`): as many cases as the request asks (default one), all traced to the request as rule `R1` (e.g. "5 positive test cases" -> TC01..TC05 with different data: outlets, tax profiles, product mixes, CS/PC). Each case is a **data row** for the legacy engine; only one of them is executed live in Q4. `qaos_run.py validate <run>`; `stage <run> cases done`.

## Q2. Write the steps and pick the data (Claude's own work)
- **Steps:** write them yourself in the standard vocabulary (`step-vocabulary`): `[Maker] Navigate to Order Booking`, `[Maker] Select PJP = ...`, `[Maker] Add line Product = ..., Order CS = 2`, `[Maker] Click Validation`, `Expect: "Validation successfully"`, `[Maker] Click Save`, `Expect: "Order Save successfully"` ... Source = the business page of each option and the session logs where it was done live. Check every label: `python runtime/qaos_steps.py check "<step>"`; keep the draft in `<run>/step_draft_TC01.json` (`qaos_steps.py add`). Expected messages come only from what training observed or stated; anything else is marked `to be observed`. Write a `Verify message "<text>"` step after **every** action that shows a toast, alert or popup (and the button to press for an alert/popup) - all of them become assertions in Q5 (`framework-conventions`, message mapping).
- **Data: from training only** (QA lead rule, 2026-10-08). Phase Q2 does not open the app or query the app DB. Take every data value from the trained knowledge, mainly the market's **test data catalog** (`apps/<app>/knowledge/business/test_data/<market>.md`: users, company/distributor, PJPs, sections, outlets with tax profile, SKUs with pack size, warehouses), plus the business pages' rules (e.g. respect the zero-tax rule, quantities within normal stock, PC above pack size normalises). Never use the old framework workbooks.
  - If the catalog does not cover what the request needs (an outlet type, a product group, a market), that is a **knowledge gap**: short -> ask the user and record the answer (also into the catalog); long-term -> ask for training and stop.
  - **Live state is checked in execution, not here**: anything that depends on today's state (stock for the chosen SKUs, documents of the day) becomes **precondition steps at the top of the step sheet** (e.g. `Navigate to Stock Inquiry; Verify Closing of <SKU> >= <qty>`). If a precondition fails during Q4, the run stops and reports; a setup step (e.g. Dispatch Advice + approval) is only done if it is in the approved plan.
  - Documents the chain needs (e.g. an unallocated order due today for Order Editing) are created by earlier steps of the same run, never reused from an earlier day.
  Write `<run>/data.json` (the executed case's row) and `<run>/step_sheet.md` (template in the `step-vocabulary` skill).

## Q3. Gate QG - one approval
One compact message: the request as understood, actions and roles, the case, the step sheet, the data row, where logins happen, and what will be generated. Ask once with `AskUserQuestion`: **Approve / Change something**. Approval phrases as in `qaos.yaml`; anything else is feedback -> fix and show again (same run). Nothing executes before QG.

## Q4. Execute once (AI execution) - ONE run, not one per case
**The AI runner executes the flow only once, with a single case's data** (QA lead, 2026-10-07, stated twice): following the test steps, the run exists to identify the **screens, elements, element ids, tabs and tab ids**, the screen sequence and every message. Brief the recorder with that ONE case only - never send it the whole case list. It is **not** a test execution of each case. When the request asks for N cases (e.g. "5 positive test cases"), pick **one representative case** to execute - the one that touches the most of the flow (e.g. most detail lines, both CS and PC) - and produce **all N cases as case-data rows** in Q5. The legacy engine (Regress Master) executes the N rows later.

Delegate to the **recorder** agent (skill `recording-protocol`) with **only**: run folder, the ONE case id, app, env, the approved step sheet and that case's data row (`data.json`) - **the step sheet is the only script it follows**. Do **not** put app knowledge in the brief (no business-page paths, no UI hints from training, no element ids, no framework flow ids); the recorder discovers and notes screens, elements, ids, tabs and messages itself. Relay switch points to the QA member (who to log in as; Claude may press Login when asked; Claude selects company/distributor) and pass "logged in" back. The recorder captures the locators, messages, document numbers and amounts it meets. If a step fails (the steps were incomplete or the screen differs), stop and ask the QA member; record the answer as `[stated <date> <name>]` in `friction.md` (and later in the pages, knowledge-intake rules).

## Q5. Generate the Regress Master scripts
Delegate to **framework-generator** (skill `framework-conventions`) with the passing recording **and `cases.json` + the case data of every case**: `flow_spec.json`, `framework.sql` (new test flow, its screens, fields and events in the framework's conventions), `framework_rollback.sql`, the case-data workbook with **one header row per case** (`PK` 01..N, detail lines `01-01`, `01-02`..., `PK_DESC` = case title; sheets per screen, `psf_field_db_column` headers; `EXPECTED_MESSAGE` = the messages observed in Q4 - the same fixed messages apply to every positive row; amounts only where they are certain) and `review_note.md`, all under `<run>/framework/`. Rows for cases that were not executed live are marked "not executed by AI; data checked against today's stock/masters" in the review note. Screens, fields, element ids, tabs, events and messages come **only from the Q4 recording**; the generator reads `selenium-framework-db` only for table structure, required columns, valid event pairs and free ids, and never copies, mirrors or reuses existing flows, screens or field definitions. A gap in the recording means a re-recording, not borrowing from elsewhere. Then delegate to **verifier** (read-only) -> `review.md`.

## Q6. Report
One short message: what was executed (document numbers, messages), the generated files, how to apply and run them in Regress Master (the framework owner applies the SQL on a test copy first; flow/group id; workbook name and the `casedata` folder), anything unverified, friction found. Offer: "same scenario for N outlets" -> more workbook rows now, or the bulk-data-factory when available.

## Limits
- A request that needs an untrained option -> train first.
- Unknown market difference -> `access_lookup.py features` / `diff-features`, then ask.
- Generated SQL is a draft until the framework owner applies it on a test copy and Regress Master replays it.
