---
name: quick-script
description: The main way to use QA OS after training - a short request or one-liner, no Jira ticket (e.g. "create one order and order detail with two products script", "... with 5 positive test cases") -> Claude writes its own test steps from its trained business knowledge, picks live data, executes the flow ONCE in the browser (to capture element ids and messages), and generates Regress Master scripts with one case-data row per requested case (selenium-framework-db / CTA_CONFIG_ASSERTION SQL + rollback + case-data workbook). Use when a QA member gives a scenario in a sentence or a few lines, or types /qa-os:quick.
---

# Quick mode: short request -> AI cycle -> Regress Master SQL

After S&D training, QA members do **not** start from Jira tickets. They give Claude a **short request or one-liner**; Claude runs the whole AI cycle and produces the SQL scripts for **Regress Master** (the legacy Selenium Regress framework, tables in `selenium-framework-db` / `CTA_CONFIG_ASSERTION`) plus the case-data workbook. Runs in the **main session**. Stops only for: one approval (gate QG), the logins, and anything the training does not cover.

## Two rules from the QA lead (2026-10-07)
1. **No ticket.** The request text is the requirement. Do not ask for a Jira key.
2. **Execute from training, not from the old framework.** The steps, order, screens, rules and expected results come from **Claude's trained knowledge** (`apps/<app>/knowledge/business/`, session logs, the trainer's `[stated]` rules) and the **test steps Claude writes itself**. Do **not** drive or copy the run from existing framework data: no case-data workbook rows from `framework/casedata-samples/`, no `fct_pr_sef_screen_events_flow` event chains, no framework atlas flow steps. The framework DB is used **only in Q5** (generation), to write the new SQL in the framework's conventions and ids.

Never type credentials, never apply SQL, never post to Jira. Data-changing steps only on an env with `non_production: true` (`apps/<app>/app.yaml`).

## Q0. Understand the request (no questions yet)
1. Defaults: app `snd`, market `PK`, env `cnr1dev1`; users = the market's Maker/Checker from `app.yaml`. A market word in the request (BD, Bangladesh...) overrides.
2. Turn the request into **business actions** and **menu options** using the business pages (start at `INDEX.md`, glossary, the option's L3 page). E.g. "order and order detail with two products" -> Order Booking (header + 2 detail lines), Maker only.
3. **Chains are allowed** when the request asks for them (e.g. "book an order, allocate it and make the GIN"): list the actions in business order, with the role per action and the switch points (Maker -> Checker). The whole chain runs on **one calendar day**; apply the carry-over checks in `docs/STATUS.md` and the run rules in `docs/OPERATING_RULES.md`.
4. **Is every option trained?** Each option needs a business page with `[observed]` or `[stated]` steps, messages and rules. If one is missing or only `[db]`/`[inferred]`, **stop** and say which, and suggest `/qa-os:train <app>` (explain it or walk it). Never improvise an untrained screen.

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
- **Data:** pick it yourself for **today**, read-only, from the app DB (`snd-schema`) and recent session evidence - never from the framework workbooks:
  - an **active outlet** on the PJP/section the Maker works, with its tax flags (respect the zero-tax rule);
  - **SKUs in stock** in the warehouse today with enough ATP for the quantities;
  - documents the chain needs (e.g. an unallocated order due today for Order Editing) - created in the same run, never reused from an earlier day.
  Write `<run>/data.json` (one row) and `<run>/step_sheet.md` (template in the `step-vocabulary` skill).

## Q3. Gate QG - one approval
One compact message: the request as understood, actions and roles, the case, the step sheet, the data row, where logins happen, and what will be generated. Ask once with `AskUserQuestion`: **Approve / Change something**. Approval phrases as in `qaos.yaml`; anything else is feedback -> fix and show again (same run). Nothing executes before QG.

## Q4. Execute once (AI execution) - ONE run, not one per case
**The AI runner executes the flow only once, with a single case's data** (QA lead, 2026-10-07, stated twice): following the test steps, the run exists to identify the **screens, elements, element ids, tabs and tab ids**, the screen sequence and every message. Brief the recorder with that ONE case only - never send it the whole case list. It is **not** a test execution of each case. When the request asks for N cases (e.g. "5 positive test cases"), pick **one representative case** to execute - the one that touches the most of the flow (e.g. most detail lines, both CS and PC) - and produce **all N cases as case-data rows** in Q5. The legacy engine (Regress Master) executes the N rows later.

Delegate to the **recorder** agent (skill `recording-protocol`) with: run folder, TC01, app, env, the approved step sheet and `data.json` - **the step sheet is the only script it follows**. Relay switch points to the QA member (who to log in as; Claude may press Login when asked; Claude selects company/distributor) and pass "logged in" back. The recorder captures the locators, messages, document numbers and amounts it meets. If a step fails for a reason the training does not explain, stop and ask the QA member; record the answer as `[stated <date> <name>]` in `friction.md` (and later in the pages, knowledge-intake rules).

## Q5. Generate the Regress Master scripts
Delegate to **framework-generator** (skill `framework-conventions`) with the passing recording **and `cases.json` + the case data of every case**: `flow_spec.json`, `framework.sql` (new test flow, its screens, fields and events in the framework's conventions), `framework_rollback.sql`, the case-data workbook with **one header row per case** (`PK` 01..N, detail lines `01-01`, `01-02`..., `PK_DESC` = case title; sheets per screen, `psf_field_db_column` headers; `EXPECTED_MESSAGE` = the messages observed in Q4 - the same fixed messages apply to every positive row; amounts only where they are certain) and `review_note.md`, all under `<run>/framework/`. Rows for cases that were not executed live are marked "not executed by AI; data checked against today's stock/masters" in the review note. Here - and only here - the generator reads `selenium-framework-db` for ids, id bands and conventions, and may **reuse an identical existing screen/field definition** instead of duplicating it (noted in `review_note.md`); it never copies old flow steps or workbook data. Then delegate to **verifier** (read-only) -> `review.md`.

## Q6. Report
One short message: what was executed (document numbers, messages), the generated files, how to apply and run them in Regress Master (the framework owner applies the SQL on a test copy first; flow/group id; workbook name and the `casedata` folder), anything unverified, friction found. Offer: "same scenario for N outlets" -> more workbook rows now, or the bulk-data-factory when available.

## Limits
- A request that needs an untrained option -> train first.
- Unknown market difference -> `access_lookup.py features` / `diff-features`, then ask.
- Generated SQL is a draft until the framework owner applies it on a test copy and Regress Master replays it.
