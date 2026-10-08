# QA OS operating rules (standing preferences of the QA lead)

This file exists so a Claude session on a different account or machine, with no personal memory, behaves the same way. The assistant's original memory notes are copied verbatim into `docs/memory_export/` (index: `MEMORY.md` there); read the ones that match the task. Never put credentials in the repo.
Last updated: 2026-10-07 (release v0.5.0).

## Who and what
- QA OS: Jira story -> test cases -> steps -> live run -> `CTA_CONFIG_ASSERTION` SQL + case-data workbook (and later bulk case data) for the legacy Regress framework (`selenium-framework-db`). S&D / DCODE first, GIAS planned. The platform must stay app-agnostic and shareable (no machine-specific paths).
- There are no vendor user guides: learn from DB metadata, the live app, Jira, the framework DB and the QA team's own training (documents, verbal explanation, live walks). Business knowledge lives in `apps/snd/knowledge/business/` (start at INDEX.md).
- **Current activity: S&D training** (`docs/TRAINING_GUIDE.md`, skill `knowledge-intake`, command `/qa-os:train`). Region R1 first = **Pakistan + Bangladesh** (BD tickets are in scope). Ticket work (SDMS-2990, SDMS-12390) is parked until the QA lead says training is complete. Resume point: the latest section of `docs/STATUS.md`.

## After training: how QA OS is used (QA lead, 2026-10-07)
- **No Jira tickets as the starting point.** QA members give a **short request or one-liner** (e.g. "create one order and order detail with two products"); Claude runs the AI cycle with `/qa-os:quick` (skill `quick-script`) and generates the **Regress Master** scripts (`selenium-framework-db` / `CTA_CONFIG_ASSERTION` SQL + rollback + case-data workbook).
- **AI execution uses Claude's training and its own test steps**, not existing Selenium framework data: no case-data workbook rows, no framework event chains, no atlas flow steps drive the run. The framework DB is read only when generating the SQL (ids, conventions, reuse of an identical screen/field definition).
- **One live run per request:** the AI cycle executes a single case's data, following the test steps, only to identify screens, elements, element ids, tabs (tab ids) and messages; all requested cases are generated as case-data rows for Regress Master.
- **Phase separation:** training knowledge -> only for writing cases and test steps; execution -> only the steps + one data row (discover screens/elements/ids/tabs live, no app knowledge, no framework data); generation -> only the recording + case rows (framework DB only for table structure and free ids).
- Training walks of framework groups (`/qa-os:train`, method C) are the one exception: there the trainer explicitly asks Claude to follow a group's flows to learn the business.

## Knowledge-gap gate (QA lead, 2026-10-08)
- Before executing an AI flow or generating scripts, check the knowledge is there. If not, ask the user. **Short/ad-hoc** gap (a value, a field meaning, a message, one rule): ask, record as [stated], continue the run. **Long-term** gap (untrained screen, module or process): ask for a training session and do NOT execute the story/flow until trained. Never guess, never borrow from old framework data.
- **Promotion area (2026-10-08): partially trained, more information will follow when needed.** If an AI execution or request touches promotions / budgets and the knowledge is not there, ask the user at that moment (pending questions: `apps/snd/knowledge/business/learning_sessions/2026-10-08_Promotions_questions_for_trainer.md`); record answers as [stated]. Never assert promotion amounts or budget effects that are only [code] or [inferred].
- **Training only up to execution:** test cases, steps AND test data come from training (test data catalog per market); the app is opened only to execute the approved steps. Live state (stock, documents of the day) is checked by precondition steps during execution.

## QA-environment strict mode (QA lead, 2026-10-08)
- In the QA environment QA OS runs **strictly to the design**: never change the framework design, tools, skills or recordings during a run, never hand-edit a recording, no long investigations. A failure STOPS the run and is reported (step, message, evidence); fixes happen in development, not in the run.
- Before release, every issue in `docs/HARDENING.md` must be fixed or accepted, and the release gate there (acceptance run, verifier verdict, one engine replay) must pass.

## Run context is confirmed first (QA lead, 2026-10-08)
Before running any QA OS flow (quick request, recording or script generation), ask and confirm: market, environment, who is running it, the Maker/Checker users, and anything else the request leaves open. No silent defaults. `qaos_run.py init` checks the answers against `app.yaml`; they are stored in `run.json` and printed in the header of `framework.sql` and `framework_rollback.sql`.

## Markets and users (cnr1dev1, non_production)
| Market | Company | Distributor | Maker | Checker | Daily cycle group |
|---|---|---|---|---|---|
| PK | Unilever Pakistan Limited (010104) | 15108843 IBRAHIM TRADERS | Auto_Multi_Orga (also Automation) | Auto_Tssm | 11 |
| BD | Unilever Bangladesh (010105) | 05108843 | Auto_Bangla | AutoBD_tssm | 61 |
Setup flow PK: group 66 (NG_Setup Flow_PK); its user per row comes from the group-users query (also Automation, headquarter). Users and roles are in `apps/snd/app.yaml`.

## Group run rules (daily cycle and setup walks)
- Run only ACTIVE (status Y) flows, in sequence order; the user per row from the group-users query (never select `plu_password`). For each flow follow its active `fct_pr_sef_screen_events_flow` rows and active fields; data from the market workbook in `framework/casedata-samples/`.
- The whole daily chain runs within ONE calendar day (stock is keyed by day). Learning runs record business facts only, no element ids.
- Two roles only: **Maker** and **Checker**; same screen / Forward button, different user.
- Navigation: top-left hamburger `#menurollin` -> Search Here -> click the item; ignore the Kaspersky certificate notice.
- **Order Editing (seq 15):** it lists only UNALLOCATED orders whose delivery date is TODAY. Run Delivery Date Change to today, then Unallocate in Order Stock Allocation, then edit. The save re-allocates; after GIN approval an order can be edited without unallocating.
- **Before Route Settlement (seq 51):** every Reattempt (rescheduled) order due today must be covered in a GIN: allocate (Order Date = its booking date) -> new GIN -> Checker approves -> Cashmemo Status Delivered. It may stay unpaid. A previous day of the PJP must be closed (yellow row = not closed, green = closed).
- **Settlement:** Edit on the route row -> cash Received (editable, prefilled) -> row Save ("Saved Successfully"). Save posts all slips and adjusts the invoices.
- **Seq 55 Cheque Status:** check only (cheques read "Clear"); never press Bounce. **Seq 56 DSR Adjustment:** enter the workbook amount (400), comment AUTO.
- **Day close (seq 57):** PJP Daily Inquiry Update -> End Of Day + Complete -> Current Status E.
- Check `docs/STATUS.md` "carry-over" notes before a run (leftover Reattempt orders, open receivables, environment job issues such as the stock carry-over job).
- After a full cycle, a Senior QA may run a knowledge check: Claude predicts first, executes, compares.

## Login and browser hand-off
- Claude NEVER types user ids or passwords. The trainer types them in the Selenium-controlled Chrome; Claude presses Login only when asked.
- Claude logs the current user out itself (user menu top right -> Logout) and, after login, selects Company and Distributor (per the market table) and presses Proceed (a real click).
- If the session expires, close the Selenium session and start a new browser. Close the Selenium browser after a final logout.

## Execution habits
- Every Forward / approve comment popup: type "Automation Approval", verify the textarea holds it, then a real click on Save.
- Log every flow in the run's `session_log.md` as it happens; note friction and fix it in the tooling.
- When stuck, stop and ask the QA lead/trainer; record their answer as `[stated <date> <name>]`.
- Use the plugin's sub-agents and skills for QA OS stages; the Excel the QA member finalises is the source of truth for steps.
- Minimise QA-lead intervention: only logins and decisions.
- Selenium technique notes (DevExtreme grids, stale number cells, dropdown arrows, bank lists, cheque popup, off-screen row Save links) are in STATUS.md "Gotchas" and the session logs.

## Permissions (Claude Code)
- Use the **Ask permissions** mode (not auto): auto mode has blocked typing amounts into the shared env. `.claude/settings.local.json` (gitignored) may allow `mcp__selenium` and the read-only DB connectors. Claude never edits its own permission settings.

## Open items (as of 2026-10-07)
47 open questions (`OPEN_QUESTIONS.md`; Q-RS4 and BA14 may be closed on the QA lead's confirmation). QA team review of `learning_sessions/2026-10-06_G11-PK_QA_Team_Review.docx` pending. Group 66 paused after seq 18. Bulk-data-factory approach agreed, not started (4 decisions pending). Generated framework SQL never replayed in the legacy engine.
