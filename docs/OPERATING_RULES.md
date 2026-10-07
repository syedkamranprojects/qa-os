# QA OS operating rules (standing preferences of the QA lead)

This file exists so a Claude session on a different account or machine, with no personal memory, behaves the same way. The assistant's original memory notes are copied verbatim into `docs/memory_export/` (index: `MEMORY.md` there); read the ones that match the task. Never put credentials in the repo.
Last updated: 2026-10-07 (release v0.5.0).

## Who and what
- QA OS: Jira story -> test cases -> steps -> live run -> `CTA_CONFIG_ASSERTION` SQL + case-data workbook (and later bulk case data) for the legacy Regress framework (`selenium-framework-db`). S&D / DCODE first, GIAS planned. The platform must stay app-agnostic and shareable (no machine-specific paths).
- There are no vendor user guides: learn from DB metadata, the live app, Jira, the framework DB and the QA team's own training (documents, verbal explanation, live walks). Business knowledge lives in `apps/snd/knowledge/business/` (start at INDEX.md).
- **Current activity: S&D training** (`docs/TRAINING_GUIDE.md`, skill `knowledge-intake`, command `/qa-os:train`). Region R1 first = **Pakistan + Bangladesh** (BD tickets are in scope). Ticket work (SDMS-2990, SDMS-12390) is parked until the QA lead says training is complete. Resume point: the latest section of `docs/STATUS.md`.

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
