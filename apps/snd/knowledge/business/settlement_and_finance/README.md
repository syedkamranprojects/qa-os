# Settlement and finance (group 11 seq 39-60, 68-71)

Last updated: 2026-10-06 (consolidated with learning session G11-3, `learning_sessions/2026-10-06_G11-PK_session3_log.md`: slips 1143-1148; **Route Settlement performed by Claude** (new blocker "Un-Deliver Order exists for today delivery!" resolved by delivering the 10-05 Reattempt order on GIN 509); seq 55 checked without Bounce (Q-CS1 answered); seq 56 saved 400 (Total Shortage +400, a DSR shortage, Q-DJ1 answered); day closed (E); SAN 97; duplicate cheque numbers allowed (Q-DS2 first half); Outstanding Outlet doubled totals = display defect (Q-DS4); two collection modes: per invoice (Outstanding Cash memos) or per outlet with FIFO auto-adjustment to the oldest invoice (Outstanding Outlet), intended (Q-DS5); the day close clears the per-PJP previous-day check, route rows yellow = not closed / green = closed (Q-RS1 fully answered); slips are not blocked before settlement, Save reconciles, posts and adjusts (Q-DS2 fully answered)). Before: 2026-10-05 (consolidated with learning sessions G11-2 and G11-2b, `learning_sessions/2026-10-05_G11-PK_session2_log.md`, `learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md`: seq 39-60 and 68-71 walked; seq 55 and 56 bypassed by the QA lead). Earlier: 2026-10-01 (G11-1, stopped at seq 51).
Updated 2026-10-08 (follow-up): merged the QA team's answers to the 2026-10-08 follow-up (Q-DS4, Q-SV1, CASHMEMO_EDIT / Q-OE5); evidence learning_sessions/2026-10-08_QA_Team_followup_answers.md. Tag [stated 2026-10-08 QA Team (follow-up)]. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08: ...)".
Updated 2026-10-08 (follow-up 2): merged the QA team's answers to the 2026-10-08 second follow-up (Q-SV2 answered: "Return Document" = a purchase return of stock from the distributor to the company, posts Out; D-G11-2b-1 withdrawn: the 10-01 state of route 02112 is abnormal env data, the Q-DS3 rule stands); evidence learning_sessions/2026-10-08_QA_Team_followup2_answers.md. Tag [stated 2026-10-08 QA Team (follow-up 2)]. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08 follow-up 2: ...)".

Area summary:
1. After delivery and returns, the DSR banks collections: six deposit-slip variants (cash, cheque, multi-cheque, unposted) reduce cash-memo balances. (superseded 2026-10-01: all six walked live (slips 1131-1136); allocating a slip does NOT reduce the balance at once. Balances move only at "posting", presumably at Route Settlement. Until then the allocations show as "Un Posted Amount" on the cash memo [observed 2026-10-01 G11-1].)
2. Route Settlement reconciles one PJP and date: sales, returns, previous/today cash and cheque, stock and cash shortage. [observed 2026-10-01 G11-1: grid read for 02112. Each deposit slip is one Collection Type line at its allocated amount. Settlement BLOCKED: "Following previous days not closed! Please close date. 2026-09-30".]
3. Transaction Inquiry checks (seq 52) confirm offsets; deposit slips are re-read after settlement (53) and after an order removal (54). [not walked yet: they depend on a completed settlement] (superseded 2026-10-05: walked read-only in G11-2b after the route was settled; Offset = posted slip allocations, slips Posted, paid memos drop out [observed 2026-10-05 G11-2b])
4. Cheque Status marks banked cheques Presented/Collected/Realized/Bounced/Cancelled. (superseded 2026-10-05: on screen only Posted cheque slips are listed, cheques read "Clear" after posting and the only action is Bounce [observed 2026-10-05 G11-2b])
5. DSR Adjustment Amount posts a manual DSR correction (doc type AD-07); PJP Daily Inquiry Update closes the journey record (confirmed 2026-10-05: it is the day close [observed 2026-10-05 G11-2b]).
6. OTC Stock Out is a SAN created by Maker and approved by Checker Auto_Tssm (Draft -> Pending -> Approved).
7. End-of-day validations check stock (seq 60) and amounts/tax/charges (68-71); read-only.
8. All maker work is Auto_Multi_Orga in one session except the SAN approval. [observed 2026-10-01 G11-1 for seq 39-51]
9. (2026-10-05: every page of this area now has live evidence; see the walk-state table.) No flow here has a live replay and the DB holds no 010104 rows for these tables, so most statements are [db]/[inferred]. (superseded 2026-10-01: deposit slips (seq 39-46) and the Route Settlement screen (seq 51, read only up to the block) are now [observed]; the other pages are still [db]/[inferred].)
10. Many assertions are toast-only: green runs do not prove the arithmetic.
11. Key traps [observed 2026-10-01 G11-1]:
    - The Deposit Slip screen first opens with the booking PJP and bank "demo" preset; the slip needs the delivery DSR.
    - The multi-cheque popup takes dates as MM/DD/YYYY.
    - Adjusted Amount refreshes only when the screen is reloaded.
    - The bank "National Bank of Pakistan" has drifted to "...ss".
    - A duplicate cheque number is accepted, and a cash memo can apparently be allocated twice.
    - The approved sales return is not netted before settlement.
    - Route Settlement needs every earlier working day closed (a day-boundary trap for any replay).
12. **2026-10-05 (G11-2b) [observed]:**
    - **Posting happens at Route Settlement**: slips 1137-1142 went Un Posted -> Posted when route 02112 for 10-05 was settled (by a QA team member); posting trims an unallocated remainder (1139: 1,000 -> 600), locks the slip, updates cash memo Received/Balance, fills Transaction Inquiry Offset Amount, and sets the cheques to "Clear". Fully paid memos drop out of the outstanding list.
    - Route Status filter All / Complete / Incomplete; a settled route is green with no Edit; uncovered Sale Value stays as memo balance (Cash Shortage 0); collections against earlier days' memos show as "Previous"; the outlet-level multi-cheque goes to the outlet's oldest open memo (FIFO by design [stated 2026-10-06 QA Team Lead]).
    - **The day close is PJP Daily Inquiry Update**: Mark Status End Of Day + DSR Files Status Complete -> "Record Updated Successfully", Current Status E (the QA member closed 10-01 the same way; detailed procedure pending from the QA lead, Q-RS1).
    - SAN 96 (Stock Adjustment Admin, -50 CS) Maker save + Forward, Checker one-step approval; Out +50 on approval.
    - Cheque Status lists only Posted cheque slips, statuses "Clear", only action Bounce ("Realized" does not exist); DSR Adjustment Amount screen read (Shortage / Adjusted / Balance per PJP), nothing saved.
    - Open: 10-01 route Complete but its slips Un Posted (Q-DS3); Total Order 13 (Q-RS3); return still not netted (Q-SR1).
13. **2026-10-08 QA team written answers** [stated 2026-10-08 QA Team] (learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx)):
    - Collection process: DSR collects in the Delivery App -> end-of-day mobile sync -> system auto-creates Unposted Cash/Cheque Deposit Slips -> Route Settlement with the accountant -> slips Posted. The Back Office Deposit Slip screen is the manual path (group 11).
    - Route Settlement: final settlement of the DSR by the accountant; ignore row colours (Edit link = not settled, blank = settled); settlement amount not editable except adjustment fields (fuel / challan); Received < Payable -> DSR Cash Shortage, never below zero; cheques fixed; stock shortage = sale price x qty (UOM) + tax %; GIN qty must match GRN qty else "Stock Mismatch"; previous-day check = working date today and closing date N-1.
    - A settled route must have all its slips Posted: the 10-01 route 02112 (Complete, slips 1131-1136 Un Posted) is defect D-G11-2b-1. (superseded 2026-10-08 follow-up 2: abnormal env data, D-G11-2b-1 withdrawn; the rule stands.)
    - Cheques: Cleared/Realized immediately at posting in PK/BD ("Clear"); Bounced reverses the payment and leaves the amount outstanding at outlet level.
    - DSR adjustment has no workflow; GRN approval auto-creates the stock-shortage DSR adjustment; day close on PJP Daily Inquiry Update is for manual Back Office working.
    - Open: Q-DS4 (outlet totals) under clarification; Q-SR1 partly (returns still not netted). (superseded 2026-10-08: Q-DS4 closed by the follow-up, see item 14.)
14. **2026-10-08 QA team follow-up answers** [stated 2026-10-08 QA Team (follow-up)] (learning_sessions/2026-10-08_QA_Team_followup_answers.md):
    - Outstanding Outlet totals are NOT a display defect: outlet 05 202,322 = 2004 (10-01) + 2016 (10-06); outlet 04 257,570 = 2015 + 2009 + 2003; the older invoices were on page 2. The outlet total = sum of ALL open invoices of the outlet across days; a genuinely duplicated amount would be a potential bug. Q-DS4 closed; D-G11-3-1 withdrawn.
    - Open in this area: Q-SR1 partly (returns still not netted).
15. **2026-10-08 QA team follow-up 2 answers** [stated 2026-10-08 QA Team (follow-up 2)] (learning_sessions/2026-10-08_QA_Team_followup2_answers.md):
    - D-G11-2b-1 withdrawn: "Irrelevant question - abnormal data". The 10-01 route 02112 state is abnormal env data, not a defect. The rule stands: a settled route must have all its slips Posted and adjusted.
    - Carry-over: the 10-01 leftovers (slips 1131-1136 Un Posted, invoices COL26000002004 / 2005 open) stay on cnr1dev1 and still inflate the outlet 04 / 05 outstanding totals; never use them as fixtures or as evidence of expected values.

Order of pages and walk state:

| Page | Walk state |
|---|---|
| deposit_slips.md | walked 2026-10-01 G11-1 and 2026-10-05 G11-2 (seq 39-46); posting observed G11-2b (seq 53/54) |
| route_settlement.md | walked 2026-10-01 G11-1 up to the block (seq 51); 2026-10-05 G11-2 blocked again (date 10-01), G11-2b read after the QA member settled 10-01 and 10-05; seq 52-54 walked (read only) |
| cheque_status.md | screen read 2026-10-05 G11-2b; seq 55 BYPASSED by the QA lead (no action) |
| dsr_adjustment.md | screen read 2026-10-05 G11-2b; seq 56 BYPASSED by the QA lead (nothing saved) |
| pjp_daily_inquiry_update.md | walked 2026-10-05 G11-2b: the day close (End Of Day / Complete) |
| otc_stock_out_and_san.md | walked 2026-10-05 G11-2b (SAN 96 created, forwarded, approved) |
| end_of_day_validations.md | walked 2026-10-05 G11-2b (seq 60, 68-71; workbook drift on 70, 69, 71) |

## What this area hands to the next area
| item | to | note |
|---|---|---|
| REPO_Deposit_Slip | none consumed in group 11 | used only for slip checks |
| Deposit slips (Un Posted) | Route Settlement | one Collection Type line per slip, at its allocated amount [observed 2026-10-01 G11-1]; posted by the settlement [observed 2026-10-05 G11-2b] |
| Settlement row (PJP + date) | day close (PJP Daily Inquiry Update End Of Day / Complete) / reports | Route Settlement Statement Report [db menu]; close observed 2026-10-05 G11-2b |
| Cheque status (R/B) | receivable reports | Cheque For Realization |
| Approved SAN stock-out | Opening/Closing validation (seq 60) | stock keyed by calendar day |
| Verified totals | cycle end | nothing further in group 11 |

## Open questions raised in this area (2026-10-01)
- Q-DS1 (class B): ANSWERED 2026-10-05: posting happens at Route Settlement [observed G11-2b].
- Q-RS1 (class C): PARTLY ANSWERED 2026-10-05: day close = PJP Daily Inquiry Update End Of Day + Complete; detailed procedure pending from the QA lead.
- Q-SR1 (class B): when does an approved sales return reduce the receivable? Default: at Route Settlement / credit note.
- Q-DS2 (C) open (duplicate cheque accepted again 10-05); Q-RS2 (B) ANSWERED 2026-10-05 (uncovered Sale Value stays as memo balance, Cash Shortage 0).
- New 2026-10-05: Q-DS3 (B, 10-01 Complete but slips Un Posted), Q-RS3 (B, Total Order 13), Q-RS4 (B, scope of the previous-day check), Q-CS1 (C, does seq 55 press Bounce), Q-DJ1 (B, what Total Shortage accumulates).

Related pages by name: inbound stock (GRN), order planning, delivery and returns (other analysts).
