# Learning session 3 plan: Group 11 PK full run WITH the QA Team Lead (date: TBD)

Purpose: walk the whole Daily Cycle (framework group 11 "Daily Cycle Only Positive Flow", Pakistan) from seq 1 to seq 71 in ONE calendar day, on this machine, with the QA Team Lead present, and close the knowledge gaps at the step where each comes up. After this session: consolidate, G0 sign-off of all four areas, Senior QA knowledge check, then prepare QA OS for the QA environment.

Env cnr1dev1, company Unilever Pakistan Limited, distributor 15108843 IBRAHIM TRADERS. Maker Auto_Multi_Orga (or Automation), Checker Auto_Tssm. Rules: docs/OPERATING_RULES.md. Open questions: OPEN_QUESTIONS.md (ids below).

## 0. Before the day (checklist)
| # | Check | How | Owner |
|---|---|---|---|
| P1 | Claude Code permissions: `.claude/settings.local.json` allows `mcp__selenium` (+ read-only DB servers), `defaultMode: default`; session mode selector shows **Ask permissions** (NOT auto) | settings + mode selector, restart | QA lead (user) |
| P2 | Permission smoke test: PASSED 2026-10-05 (allow list mcp__selenium in settings.local.json, Ask permissions mode): typed 400 + key presses into DSR Adjustment Amount, discarded, nothing saved. Repeat only if the mode or settings change. | Claude | Claude |
| P3 | Previous day closed for route 02112 (PJP Daily Inquiry Update: Current Status E) and Route Settlement Complete for the last cycle day; otherwise seq 51 blocks | read-only check at start | Claude + QA lead |
| P4 | Leftover reservations: old GIN 505 (2026-09-30) still Pending holds 63 CS of 62740537; decide whether to approve/terminate it first (affects ATP and Opening) | Stock Inquiry / GIN screen | QA Team Lead decides |
| P5 | Plan the whole run in one sitting (stock is keyed by calendar day); start early | - | all |
| P6 | Fresh Selenium Chrome; Claude never types credentials; Claude logs out and picks company/distributor | - | Claude |

## 1. Run sheet with the questions to ask at each step
Legend: M = Maker, C = Checker. "Ask" = question for the QA Team Lead at that step (ids in OPEN_QUESTIONS.md). "New this time" = something skipped or not observed before.

| Seq | Flow | Who | New this time / Ask |
|---|---|---|---|
| 1 | Login Dcode | M | - |
| 2 | Dispatch Advice (create, lines, loss, Forward) | M | Ask BA2 / Q-DA1 (may a Maker approve his own DA?), Q-DA3 (label price vs purchase price), Q02 (Reject/Delete of a Draft: optional demo) |
| 5 | DA Approval | C | - |
| 7 | DA Loss Approval | C | Ask Q-LA1 (where an approved loss is used), Q-LA2 (why Reject is disabled) |
| 9 | Stock Validation after DA | M | Ask Q-OB2 (first movement opens the day: always all rows?), Q-SV1 (deltas instead of absolute checks) |
| 10 | Order Booking (6 orders) | M | Ask Q16 / Q27 (quantity above ATP, allocation on short stock: optional demo) |
| 12 | Stock Allocation | M | - |
| 14 | Transaction Inquiry after OB | M | - |
| **15** | **Order Editing** | M | **New: walk it with the QA Team Lead.** Ask Q-OE1 (should it run after Delivery Date Change?), Q-OE2 (which order/outlet), Q-OE4 (exact date filter) |
| 16 | Order Cancellation | M | - |
| 18 | Stock Unallocation | M | Ask Q26 (when "stock not found." appears) |
| 19 | Delivery Date Change | M | Ask Q29 (past date refused?), Q30 (does it move the delivery PJP?) |
| 20 | Goods Issue Note | M | Ask Q34 (date used by the GIN stock check) |
| 23 | GIN Approval | C | - |
| 24 | Stock validation after GIN | M | - |
| 29 | Order Editing after GIN | M | Ask Q-OE3 (should edit/cancel after an approved GIN be blocked?), Q-TI1 (Ordered/Allocated after an edit) |
| 31 | Order Cancellation after GIN | M | - |
| 32 | Cashmemo Reschedule | M | - |
| 33 | Cashmemo Status | M | - |
| 34-38 | Sales Return, View, Approval (C at 37), Status Change | M/C | Ask Q-SR1 (when a return reduces the receivable), Q-SR2 (should a part return re-price promotions on other lines?), Q42 (stock at approval or GRN), Q-GRN2 (non-Sound returns) |
| 39-46 | Deposit Slips (cash, cheque, unposted, multi-cheque, cheque, cash) | M | Ask Q-DS2 (duplicate cheque number accepted = defect?), outlet-level multi-cheque goes to the OLDEST open memo: intended? |
| 48 | Goods Return Note | M | Ask Q-GRN1 (Actual < Suggested: where does the difference go?) |
| 49 | GRN Approval | C | - |
| 50 | Stock validation after GRN | M | - |
| **51** | **Route Settlement** | M | **New: Claude performs the settlement (Edit, entries, Save) and records message + effect.** Ask Q48 (Payable vs Received entry), Q-RS3 (what Total Order counts), Q-RS4 (scope of the previous-day check), Q-DS3 (10-01 Complete but slips Un Posted: how was it closed?), Q-RS1 detailed procedure (settle first, then day close?) |
| 52 | Offset Amount after settlement | M | (Offset before settlement: read it at seq 46 too, to settle Q50 fully) |
| 53-54 | Deposit Slip after settlement / cash removal | M | - |
| **55** | **Cheque Status** | M | **Decide with the QA Team Lead (bypassed twice).** Ask Q-CS1 (does the framework press Bounce? what should it assert, given only "Clear"/Bounce exist?) |
| **56** | **DSR Adjustment Amount** | M | **Decide with the QA Team Lead (bypassed).** Ask Q53 (auto-authorized?), Q-DJ1 (what Total Shortage Amount accumulates), amount to use (workbook 400) |
| **57** | **PJP Daily Inquiry Update = day close** | M | Confirm the order: settlement (51) -> day close (57); End Of Day + Complete; End Date empty or filled? |
| 58 | Stock Out (SAN, Stock Adjustment Admin) | M | Ask Q58 (stock moves at Forward or at approval: snapshot after Forward) |
| 59 | SAN Approval | C | - |
| 60 | Opening & Closing stock validation | M | - |
| 68-71 | Transaction Inquiry checks (edited order, sales return) | M | Show FRAMEWORK_DRIFT.md items for seq 69-71 (workbook values stale) |
| end | Logout; close browser | - | Day must be left settled + closed |

## 2. Also ask (not tied to one step)
- BA14 and the rest of the BA list (OPEN_QUESTIONS §1a), as time allows.
- Who is the framework owner who will validate the generated SQL and FRAMEWORK_DRIFT.md?
- G0 sign-off: go through the coverage report (`2026-10-05_G11-PK_coverage_report.md`) area by area at the end.

## 3. Outputs of the session
- `learning_sessions/<date>_G11-PK_session3_log.md` (per step, answers tagged `[stated <date> QA Team Lead]`), report, then consolidation into the pages and OPEN_QUESTIONS; coverage report v2; G0 per area.
- Then: prepare QA OS for the QA environment (DEPLOY.md, plugin reload, credentials per member, app.yaml env entry).
