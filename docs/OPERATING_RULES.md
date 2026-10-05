# QA OS operating rules (standing preferences of the QA lead)

This file exists so a Claude session on a different account or machine, with no personal memory, behaves the same way. The assistant's original memory notes are copied verbatim into `docs/memory_export/` (index: `MEMORY.md` there); read the ones that match the task. Never put credentials in the repo.

## Who and what
- The QA lead builds QA OS: Jira story -> test cases -> steps -> live run -> `CTA_CONFIG_ASSERTION` SQL + case-data workbook for the legacy Regress framework (`snd-selenium` framework DB). S&D / DCODE first (Pakistan, env cnr1dev1, non_production), GIAS planned. The platform must stay app-agnostic and shareable (no machine-specific paths).
- There are no vendor user guides: learn from DB metadata, the live app, Jira, the framework DB. Business knowledge lives in `apps/snd/knowledge/business/` (start at INDEX.md).
- Current activity: learning phase (`docs/LEARNING_STANDARD.md`) by replaying framework group 11 "Daily Cycle Only Positive Flow". Resume point: the latest section of `docs/STATUS.md`.

## Group 11 run rules
- Run only ACTIVE (status Y) flows, in sequence order; the whole chain within ONE calendar day (stock is keyed by day). Learning runs record business facts only, no element ids (the recorder agent captures ids later).
- Two roles only: **Maker** (Automation, Auto_Multi_Orga) and **Checker** (Auto_Tssm); same screen/Forward button, different user. Company Unilever Pakistan Limited, distributor 15108843 IBRAHIM TRADERS.
- Navigation: top-left hamburger `#menurollin` -> Search Here -> click the item; ignore the Kaspersky certificate notice.
- Seq 15 Order Editing is skipped until QA/BA answer Q-OE1/Q-OE2. At seq 51 Route Settlement, if "previous days not closed" appears, stop and show the QA lead (do not close days without QA/BA agreement, Q-RS1).
- After the cycle reaches seq 71 (Transaction Inquiry Validate After Sales Return), a Senior QA runs a knowledge check: predict first, execute, compare.

## Login and browser hand-off
- Claude NEVER types user ids or passwords. The QA lead types them in the Selenium-controlled Chrome (start it with `--remote-debugging-port=9222`).
- Claude logs the current user out itself (user menu top right -> Logout) and, once the QA lead has submitted credentials, Claude selects Company (Unilever Pakistan Limited) and Distributor (15108843-IBRAHIM TRADERS) and presses Proceed (a real click on the button).
- If the session expires, close the Selenium session and start a new browser. Close the Selenium browser after a final logout.

## Execution habits
- Every Forward / approve comment popup: type "Automation Approval", verify the textarea holds it, then a real click on Save.
- Log every flow in the run's `session_log.md` as it happens; note friction (what needed manual help) and fix it in the tooling.
- Use the plugin's sub-agents and skills for QA OS stages, not inline work; the Excel the QA member finalises is the source of truth for steps.
- Minimise QA-lead intervention: only logins and decisions.
- Selenium technique notes (DevExtreme grids, stale number cells, dropdown arrows, bank lists, cheque popup) are in STATUS.md "Gotchas" and the session logs.

## Open items (as of 2026-10-05)
Q-RS1 day close for 2026-10-01; Q-OE1/Q-OE2 Order Editing; `qaos_login.py` fails for Auto_Multi_Orga; plugin 0.4.1 not reloaded; qa-os changes uncommitted; session 2 findings not yet consolidated into the knowledge pages.
