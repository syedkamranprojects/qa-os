---
name: snd-test-automation-project
description: "QA OS (agentic QA automation for S&D, then GIAS) - current state, where everything is, and the plan; read qa-os/docs/STATUS.md first when resuming."
metadata:
  node_type: memory
  type: project
  originSessionId: eb4a66f7-6654-4151-a641-fe8df7bda0d6
  modified: 2026-09-28T07:01:36.112Z
---

**Resume here:** `C:\MyWork\gias-qa-workspace\qa-os\docs\STATUS.md` (bottom section "Update: Monday 2026-09-28" is the latest). Design: `qa-os/docs/ARCHITECTURE.md`.

**What it is:** a QA user gives Claude a Jira story; Claude makes cases + steps, records each flow **once** through the Selenium MCP (one data row), and generates `CTA_CONFIG_ASSERTION` SQL + a case-data workbook for the legacy Regress framework (NGSelenium-Testing @ appium_development). A person reviews/applies the SQL; the legacy engine runs all cases and data variations. Started 2026-09-24. S&D (DCODE) is not GIAS; GIAS is the next app pack.

**Working rules (from the user):** Claude never types passwords (QA user logs in); **max 10 core cases per story, rest is backlog**; MCP run = one-time recording per flow, not regression; **minimise user intervention** (see [[minimise-user-intervention]]); no user guides, learn from DB metadata + live app + stories; SQL never auto-applied; platform shared across QA members ([[qaos-shareable]], [[no-docs-learn-from-metadata]]).

**State 2026-09-28:** pilot SDMS-10351 done earlier (SQL draft in runs/SDMS-10351/.../framework, unvalidated). Second story **Van Sales end-to-end** (VAN-SALES-E2E, run 20260928-1012, env cnr1dev1 as KPO_mp): requirement (39 rules, 13 ambiguities), 42 cases, recorded flows, SQL draft for the create-request flow (13 INSERTs, ids 0612/061201/06120001) + workbook; not applied. Helper (`plugins/qa-os/runtime/qaos_helpers.js`) and recorder (`framework/tools/qaos_record.py`) built. Test data left: Van Sale Stock Requests 20260000000570/571 (Drafts). Many story-vs-app variances listed in STATUS.md for the BA.

**Environments:** cnr1dev1 https://dcodecnr1dev1.unilever.com/ngui as KPO_mp is the Unilever env (use for Van Sales; navigate via sidebar search box, pushState does not work there). cnr2dev3 as KPO_slv (dist 50000451) has the SKU screens. Passwords only in gitignored `.claude/settings.local.json`; never echo (KPO_mp password was pasted in chat once). Windows Python: `C:\Users\syed.kamran\AppData\Local\Python\bin\python.exe`.

**Next:** framework owner validates both SQL drafts on a test copy; cut cases.json to 10 core + backlog; record the small missing flows; fixture discovery + variance registry; stock-changing flows only with explicit OK; snd-schema query for status codes.

See [[snd-table-catalog]], [[regress-casedata-contract]].

**Correction 2026-09-29 (snd-schema inspection):** cnr1dev1 / KPO_mp belongs to org **010104 = Unilever Pakistan Limited** (not "Thai/PH-flavoured"). Orgs: 0101/0102 Danone Indonesia, 010104 Unilever Pakistan, 010105 Unilever Bangladesh, 99 GLOBAL. snd-schema has roles/users/options and per-org feature flags but NO Van Sales tables/doc types (older than the app), empty role->action and deny tables (authorization is screen-level), no status-transition table. Details: `qa-os/apps/snd/knowledge/db_inspection_2026-09-29.md`.

**State 2026-09-29 (end of day):** built the access knowledge layer (`qa-os/apps/snd/knowledge/access/`, lookup `apps/snd/tools/access_lookup.py` incl. `plan-user`), orchestrator v0.3 Stage 0 (intake block -> `decisions.json` via `runtime/qaos_intake.py`; account chosen from live menus + DB; authorization only on `non_production` envs), promotion step `runtime/qaos_promote.py` (dry run default; variances only from reusable BA rulings), question bank `docs/QUESTION_BANK.md`, `cases.json` cut to 10 core + backlog. Van Sales intake block written and parsed; term "Van Seller = Van Sales" promoted (stated). Nothing applied to any framework DB. **Top blocker: no framework owner has validated the SQL drafts in the legacy engine.** Full list in STATUS.md ("What is needed from the user next").

**2026-09-29 late:** Dispatch Advice replay from selenium-framework-db (group 11 chain) started; DA 570 exists on cnr1dev1 (M&P, KPO_mp; approved by same user). Automation data is under distributor 15108843; `Auto_Tssm` approves only; maker login (Auto_Multi_Orga/Automation) still needed. QA lead's rules: standard step vocabulary (`qa-os/docs/STEP_VOCABULARY.md`, `apps/snd/steps/library.yaml`), maker-checker with explicit switch points, approval = same DA option by a different user. Never read the framework `plu_password` column.

**2026-09-29 end of day (RESUME):** replayed the framework's Pakistan daily cycle (group 11) on cnr1dev1 up to Order Booking (8 orders COL26000001995-2002) + Stock Allocation + Transaction Inquiry; blocked at seq 15 Order Editing (empty Outlet list). Full state, findings and next steps: `qa-os/docs/STATUS.md` (last section) and `qa-os/apps/snd/knowledge/framework_flows/` (DISPATCH_ADVICE.md, TC-DA-01_executed.md, TC-OB-01_executed.md, STEP_SHEET_DRAFT_next.md). Users on cnr1dev1: Maker/Stock Controller Auto_Multi_Orga, Checker Auto_Tssm (approve-only); Claude never types credentials; QA lead logs in at switch points. QA lead wants QA-provided/approved step sheets to avoid back-and-forth.

**2026-10-01 (PAUSE — resume here):** v0.4.0 released (git-tagged, zipped, DEPLOY.md + RELEASE_NOTES.md written; see [[qaos-shareable]]). Learning mode ran: 4 business-area digests + live screen harvest + 3 rounds of live walk-throughs (apps/snd/knowledge/business/). Confirmed live: stock/orders are keyed by calendar day — a DA approved "yesterday" does not carry stock into "today", and GIN approval is refused if cash-memo delivery date is before the PJP working date ("cashmemo(s) found with delivery date earlier than the pjp working date"). This is now the hard constraint for any Daily Cycle run: the whole receive→order→issue chain must happen same-day.

**User's plan (2026-10-01):** pausing agentic work. The user will personally learn the application (as Maker, Checker, and themselves) using what QA OS has already written — there is still no vendor user guide, so apps/snd/knowledge/business/INDEX.md, document_lifecycle.md, glossary.md and OPEN_QUESTIONS.md are the closest thing to one. Once the user has that understanding, they want to **restart Daily Cycle Only Positive Flow end-to-end, starting with one market: Pakistan**, presumably with fresh same-day data and the user driving/checking the flow more directly rather than Claude exploring alone.

**Next session should NOT auto-resume learning-mode agents.** Wait for the user to say they're ready, then re-run the Pakistan Daily Cycle (group 11, env cnr1dev1) from the top with a fresh same-day Dispatch Advice, honoring the day-boundary finding. Credentials are never typed by Claude (see [[excel-source-of-truth]] mechanism and ~/.qa-os/credentials.json); the user logs in as Maker (Auto_Multi_Orga) / Checker (Auto_Tssm) each time asked.
