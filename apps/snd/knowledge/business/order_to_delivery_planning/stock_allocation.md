---
option: Order Stock Allocation (Stock Allocation and Unallocation)
area: order_to_delivery_planning
doc_types: [CM-01]
screens: [DYL_201904]
framework_flows: ["00130001", "00130002"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [order_booking, stock_inquiry_and_balances]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-08
---
# Stock Allocation and Unallocation: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 00130001 (seq 12), 00130002 (seq 18; seq 25 duplicate inactive).
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.
Updated 2026-10-08: merged the QA team's written answers to the 2026-10-06 review (learning_sessions/2026-10-06_G11-PK_QA_Team_Review.docx); evidence learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx). Tag [stated 2026-10-08 QA Team] = written answer of the QA team. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08: ...)".

## 1. Purpose
Allocation reserves warehouse stock to booked orders so that the GIN can issue exactly the goods promised. [inferred] Unallocation releases that reservation so the stock can be given to other orders or the order can be edited. [inferred] On cnr1dev1 allocation is automatic at order save, so the manual screen mostly shows the result.
- Confirmed 2026-10-01: all 6 orders booked that day were already FULL on the Allocated tab; the manual Allocation step only matters for orders that did not get stock at booking (or were unallocated). [observed 2026-10-01 G11-1] (reservation at booking upgraded from [inferred]: booking reserves stock immediately, Allocated up and Closing down; cancellation releases it; see order_booking.md and order_editing_cancellation.md.)
- G11-3: allocation also gates Order Editing: an order must be **unallocated** before Order Editing lists it (before the GIN) [stated 2026-10-06 QA Team Lead]; and a Reattempt order due today must be **allocated** again before it can go on a GIN [stated 2026-10-06 QA Team Lead; observed 2026-10-06 G11-3].
- QA team 2026-10-08 (Q16 / Q27): in Region 1 both countries allocate stock automatically when an Order / Cash Memo / Invoice is created [stated 2026-10-08 QA Team].

## 2. Actors and roles
Auto_Multi_Orga (same session as order booking). [observed]
- Maker = Auto_Multi_Orga: allocates and unallocates. [observed 2026-10-01 G11-1, seq 12 and 18]
- Checker: no role on this option (no approval step). [observed 2026-10-01 G11-1]
- G11-3: Maker Auto_Multi_Orga (seq 12, 18 and the extra allocation of the Reattempt order 2012) [observed 2026-10-06 G11-3].

## 3. Documents and master data
No new document. Acts on order cash memos (Allocation Status; `tcmm_stock_allocated_status`, `tcmm_alloc_ref_no` columns exist [db]). Allocation rules table `rpl_pr_sar_stock_alloc_rules` exists, empty for org 010104 in the base DB. [db]
- Demand Channel of the listed orders: "Back Office (BO)". [observed 2026-10-01 G11-1]

## 4. Inputs: screens and fields
Menu title **Order Stock Allocation** (framework search text "Stock Allocation" only finds the group; option `DYL_201904`, layout 201904). [observed]
Fields: Order Date (date, default today), PJP Number (dropdown; PJP 02111~AutomationOB1 preselected). Tabs: **Unallocated** and **Allocated**. Buttons: Allocation, Unallocate (Allocated tab). Grid columns: Delivery Date, Demand Channel, Description, Document Date, Document No, Net Amount, Outlet Code, Outlet Name, Section; filter row `rowfilter_OUTLDESC`; select-all `checkbox-0`. [observed/atlas]
Stock Unallocation flow 00130002 uses the same layout with tab_1 (Allocated).
- Live 2026-10-01: Order Date (today) and PJP Number (02111~AutomationOB1) preselected; Allocation button on the Unallocated tab, Unallocate on the Allocated tab. [observed 2026-10-01 G11-1]
- **Allocated** grid columns: Description (the distributor), Document No, Outlet Code, Outlet Name, Document Date, Delivery Date, Net Amount (rounded), Section, Demand Channel, **Allocation Status** (FULL). [observed 2026-10-01 G11-1]
- **Unallocated** grid columns: Description, Document No, Outlet Code, Outlet Name, Document Date, Delivery Date, Net Amount, Section, Demand Channel; **no Allocation Status column**. [observed 2026-10-01 G11-1]
- Selecting one order: the row checkbox itself does not react, click its cell. [observed 2026-10-01 G11-1]
- G11-3: Order Stock Allocation (DYL_201904) filters by **Order Date** (the booking date), not the delivery date: the Reattempt order 2012 (booked 10-05, delivery 10-06) appeared only with Order Date 2026-10-05 [observed 2026-10-06 G11-3]. Tabs Allocated / Unallocated; tick a row by clicking the checkbox CELL; the header checkbox selects all rows of the tab [observed 2026-10-06 G11-3].

## 5. Process: the business steps in order
1. [Maker] Navigate to Order Stock Allocation. (`11:12:00130001`)
2. [Maker] Verify Order Date and PJP Number; open the Unallocated tab. (`11:12:00130001`)
3. [Maker] Filter Outlet "Aautomation", select all, click Allocation, accept the browser alert "Are you sure you want to proceed?". -> "Process completed successfully". [observed] (`11:12:00130001`) Live 2026-10-01: the Unallocated tab was empty (all 6 orders auto-allocated), so the step was a no-op. [observed 2026-10-01 G11-1]
4. Unallocation (seq 18): Allocated tab, select rows, Unallocate, accept alert. -> observed answer "stock not found." [observed] (`11:18:00130002`) (superseded 2026-10-01: the same action answered "Process completed successfully", see step 5.)
5. [Maker] Open the Allocated tab; Select order COL26000002007 (one order only); Click Unallocate; Accept "Are you sure you want to proceed?" -> toast **"Process completed successfully"**; the order leaves the Allocated tab and appears on the Unallocated tab. [observed 2026-10-01 G11-1] (`11:18:00130002`)
6. [Maker] Open the Unallocated tab; Select order COL26000002007; Click Allocation; Accept "Are you sure you want to proceed?" -> **"Process completed successfully"**; the order is back on the Allocated tab, FULL (all 5 orders 2003-2007 FULL). [observed 2026-10-01 G11-1] (`11:12:00130001` manual allocation, exercised after `11:18:00130002`)

G11-2 (2026-10-05) [observed 2026-10-05 G11-2]: seq 12 no-op again (Unallocated tab empty, orders 2009-2014 FULL on the Allocated tab); seq 18 unallocate ONE order (COL26000002013) and allocate it again (QA lead option 1), as on 10-01.
G11-3 walk (2026-10-06) [observed 2026-10-06 G11-3]:
1. Seq 12 (no-op): Order Date today, PJP 02111 -> Unallocated tab empty; Allocated tab lists the 6 orders 2015-2020 (allocated at save) (11:12:00130001).
2. Before seq 15 (QA team, during the QA Team Lead's check): 2015 and 2016 unallocated so that Order Editing lists them [stated 2026-10-06 QA Team Lead].
3. Seq 18: Allocated = 2015 (re-allocated FULL by the edit save), 2018, 2019, 2020; Unallocated = 2016. Tick 2020 -> Unallocate -> "Are you sure you want to proceed?" -> "Process completed successfully"; Unallocated tab: header checkbox (2016 + 2020) -> Allocation -> confirm -> "Process completed successfully"; Unallocated empty (11:18:00130002).
4. Extra (for the Route Settlement blocker): Order Date **2026-10-05**, PJP 02111 -> Unallocated tab = COL26000002012 (Reattempt, delivery 10-06, 108,202) -> tick -> Allocation -> confirm -> "Process completed successfully" [stated 2026-10-06 QA Team Lead: "Order status reattempt should be allocated in order allocation option for scheduled GIN"].
5. Order Date 2026-10-06 Unallocated tab then showed 2018 (rescheduled at seq 32 to 10-07): **a Cashmemo Reschedule unallocates the order**.

## 6. Outputs and effects
- Allocated orders move to the Allocated tab; Allocation Status FULL. [observed]
- Stock effect (reserved/allocated quantity per warehouse): the Stock Inquiry Allocated columns carry it: on 2026-09-30, 13 rows had Allocated > 0 (e.g. 62740537 Auto Main 63 CS = the GIN 505 line) and Closing is net of Allocated [observed 2026-10-01]. Allocation also covers documents other than GIN 505 (20050308 Auto Main allocated 39 CS 96 PC vs GIN line 18 CS 16 PC) [observed]. Opening/Allocated on the new day are 0 for the received product (Allocated 0 on 10-01) [observed]. (superseded 2026-10-01 later in the day: by 16:40 the day had Opening balances and Allocated 63 CS for 62740537 at Auto Main = the pending GIN 505 reservation; who generated the openings is open, Q-OB1. [observed 2026-10-01 G11-1])
- Transaction Inquiry shows an allocated CS column (`row_1_allocated_cs`) per order line. [atlas] Confirmed: the Detail window shows **Allocated** CS/DZ/PC (normalised, e.g. 7/0/0). [observed 2026-10-01 G11-1]
- Booking allocates at save: Stock Inquiry Allocated +order quantity, Closing -order quantity (62740537 Allocated 63 -> 98 for 5 open orders x 7 CS, Closing 261 -> 226). Cancellation released 7 CS. Closing = Opening + In - Out - Allocated. [observed 2026-10-01 G11-1]
- Unallocate / re-allocate stock effect: not snapshotted; expected to be the same release/reserve mechanism as cancellation and booking. [inferred 2026-10-01 G11-1]
- At GIN approval the issued quantity leaves Allocated and appears as Out; Closing does not change (62740537 Allocated 98 -> 63). [observed 2026-10-01 G11-1; see goods_issue_note]
- G11-2: a new day's Allocated already holds reservations of old Pending documents (62740537: 63 CS of GIN 505 from 09-30, carried on 10-01 and 10-05) [observed 2026-10-05 G11-2].
- G11-3: **Order Editing save re-allocates the edited order** (2015 FULL on the Allocated tab after the edit) [observed 2026-10-06 G11-3].
- G11-3: **Cashmemo Reschedule unallocates the order** (2018 on the Unallocated tab after seq 32) [observed 2026-10-06 G11-3]; to deliver it on its new date it must be allocated again (Order Date = booking date) and put on a new GIN [stated 2026-10-06 QA Team Lead; observed for 2012].
- G11-3: allocation alone of a Reattempt order due today does not clear Route Settlement's "Un-Deliver Order exists for today delivery!" [observed 2026-10-06 G11-3].
- G11-3: GIN approval moved Allocated to Out (Allocated 0 everywhere at seq 24) [observed 2026-10-06 G11-3]; the 63 CS of the old Pending GIN 505 did not appear on 10-06 (no carry-over rows, Q-OB2).

## 7. Statuses and transitions
| from | action | to | by | tag |
|---|---|---|---|---|
| Unallocated | Order saved | Allocated (FULL) automatically | system | [observed]; re-observed for 6 orders [observed 2026-10-01 G11-1] |
| Unallocated | Allocation | Allocated | Maker | [observed]; re-observed on COL26000002007 [observed 2026-10-01 G11-1] |
| Allocated | Unallocate | (expected Unallocated) | Maker | [inferred]; observed result "stock not found." (superseded 2026-10-01) |
| Allocated | Unallocate | Unallocated (order moves to the Unallocated tab) | Maker | [observed 2026-10-01 G11-1] (was [inferred]) |
| Allocated | GIN approved | allocation consumed (Allocated -> Out) | Checker (GIN) | [observed 2026-10-01 G11-1] |
| Allocated (FULL) | Unallocate | Unallocated (order becomes editable in Order Editing if delivery today) | Maker | [observed 2026-10-06 G11-3] |
| Unallocated (edited in Order Editing) | Order Editing Save | Allocated FULL | Maker | [observed 2026-10-06 G11-3] |
| Allocated / on GIN | Cashmemo Reschedule | Unallocated (Reattempt, new delivery date) | Maker | [observed 2026-10-06 G11-3] |
| Unallocated Reattempt (Order Date = booking date) | Allocation | Allocated; offered on a GIN for its delivery date | Maker | [observed 2026-10-06 G11-3] |

## 8. Rules and validations
- Orders are auto-allocated at save (all 8 new orders already Allocated). [observed] Again all 6 orders of 2026-10-01. [observed 2026-10-01 G11-1]
- Only an older order (COL26000001988, outlet 1000000002) was in Unallocated and was allocated by the manual step. [observed]
- The screen date filters by Order Date; orders booked yesterday must have the date typed (send-keys then Enter). [observed]
- Alert must be accepted through the browser; script clicks cannot. [observed]
- Unallocate failed for all 9 orders, also for the 8 new ones alone, nothing changed. [observed] (superseded 2026-10-01: Unallocate of one order succeeded with "Process completed successfully" and moved it to the Unallocated tab; the 09-29 failure was not reproduced [observed 2026-10-01 G11-1].)
- Unallocate and Allocation both ask for confirmation "Are you sure you want to proceed?". [observed 2026-10-01 G11-1]
- An unallocated order can be allocated again with the manual Allocation button (FULL). [observed 2026-10-01 G11-1]
- Partial allocation when stock is short: [unknown]. (superseded 2026-10-08: order qty <= available -> the required qty is allocated; order qty > available -> **only the available qty** is allocated; no stock -> the order stays **unallocated** and the Cash Memo status is **Order** [stated 2026-10-08 QA Team])
- G11-2: auto-allocation at save and the one-order Unallocate/Allocate round trip confirmed on a second day [observed 2026-10-05 G11-2].
- G11-3: the Unallocate / Allocation round trip worked again ("Process completed successfully", both directions) [observed 2026-10-06 G11-3]; "stock not found." not seen (Q26).
- G11-3: the screen's Order Date is the booking date; a rescheduled order is found under its original booking date [observed 2026-10-06 G11-3].
- QA team 2026-10-08 (Q16 / Q27, allocation logic) [stated 2026-10-08 QA Team]: the system checks the booked quantity against the available stock: <= available -> allocated in full; > available -> the available quantity only (partial); none available -> unallocated, Cash Memo status **Order**.
- QA team 2026-10-08 (rule 2): after an Order Editing save the system automatically allocates the available stock against the modified order [stated 2026-10-08 QA Team].
- QA team 2026-10-08 (rule 4, confirmed): a Cashmemo Reschedule unallocates the order [stated 2026-10-08 QA Team].
- Promotions training 2026-10-07 (F17, F19): a **free-goods** promotion checks the free SKU's stock; when it is out of stock the order is saved but the **free goods are not allocated** [stated 2026-10-07 Syed Zulfiqar]; see [promotions_and_budget.md](../promotions_and_budget/promotions_and_budget.md) (Q-PR9). Not yet observed.
- Code study 2026-10-08 (promotion service, not observed): the promotion service has **no stock check** and never reads the order status; free goods (and their quantity budget) are calculated on the same save event as discounts, so the free-SKU stock rule, if it holds, is enforced by the S&D order / allocation side (contradiction 37) [code UL-R1-BD@51e7e815 SnDRepositoryFiller.java:408] [code UL-R1-BD@51e7e815 BusinessResolver.java:40-60]. <!--i-->
- Group 66 walk 2026-10-09: **an order draws stock from its PJP's warehouse**: on Aslam PJP OB 7918624876 (warehouse 0000000025-IBT Main warehouse) product 20061858 gave "Stock not available." while its only stock (DA 1362) was in C0000000055-Auto Main Warehouse, and was booked normally (ATP 10 CS, order COL26000002031) once DA 1363 had put stock into IBT Main [observed 2026-10-09]; group 11's PJP 02111 books from Auto Main, where the group 11 DAs receive stock [observed G11 walks; the PJP 02111 warehouse field itself not read]. Receive stock into the warehouse of the booking PJP.

## 9. Messages
"Are you sure you want to proceed?" (confirm alert); "Process completed successfully" (allocation, key Stock_Allocation_ASSR); "stock not found." (unallocation; framework key Unallocated_ASSR expects something else, [unknown] what). [observed]
- 2026-10-01: Unallocate answered **"Process completed successfully"** (toast) after the confirm; Allocation of the same order answered the same text. [observed 2026-10-01 G11-1] ("stock not found." superseded 2026-10-01 for this data; kept as the 09-29 observation.)
- G11-3: alert "Are you sure you want to proceed?" then "Process completed successfully" (Unallocate and Allocation) [observed 2026-10-06 G11-3].

## 10. Dependencies
Reads orders from Order Booking and stock from the DA; day-keyed stock balances. Hands allocated orders to Order Editing/Cancellation (hidden when allocated, see order_editing_cancellation.md) and to GIN (cash memo selection).
- (superseded 2026-10-01: allocated orders are NOT hidden from Order Editing/Cancellation; the empty outlet list was caused by the Order Editing date filter working on the delivery date. See order_editing_cancellation.md. [observed 2026-10-01 G11-1])
- The GIN issues allocated cash memos only; an unallocate of all orders right before the GIN would leave nothing to issue. [inferred 2026-10-01 G11-1]
- G11-3: Order Editing (before GIN) depends on Unallocate here; the GIN (seq 20) needs the orders allocated again (seq 18); a Reattempt order needs Allocation here before its GIN [stated 2026-10-06 QA Team Lead; observed 2026-10-06 G11-3].

## 11. Test design hints
- Positive: save an order and verify Allocated tab shows it (FULL); allocate an old Unallocated order.
- Negative: order quantity beyond stock -> expect partial/Unallocated; unallocate when stock missing.
- Boundary: stock exactly equals order quantity; Order Date yesterday/tomorrow.
- Traps: "Process completed successfully" with zero Unallocated rows proves nothing; the manual step is a no-op on auto-allocation; the Unallocated_ASSR expected text may never match.
- New 2026-10-01 [observed 2026-10-01 G11-1]:
  - Positive round trip: unallocate ONE order (assert it moves to Unallocated, no Allocation Status column), allocate it again (assert FULL), then snapshot Stock Inquiry Allocated before/after to prove the stock effect (not yet measured).
  - Trap (framework drift): flow 00130002 selects ALL rows (filter "Aautomation", select-all) and unallocates everything right before the GIN; run as written it leaves the GIN with no allocated cash memos. Unallocate one order, or re-allocate before the GIN.
  - Trap: the confirm dialog must be accepted, otherwise nothing happens and no toast appears.
- G11-2: the framework's select-all Unallocate (flow 00130002) was again replaced by a one-order round trip; drift entry in FRAMEWORK_DRIFT.md.
- G11-3 additions [observed 2026-10-06 G11-3]:
  - Positive: Unallocate an order with delivery today -> it appears in Order Editing; save the edit -> it is Allocated again.
  - Positive: reschedule an order -> it is on the Unallocated tab under its booking date; allocate it -> it is offered on the GIN of its new delivery date.
  - Trap: search a rescheduled order under its ORDER (booking) date, not today's.
- QA team 2026-10-08 additions [stated 2026-10-08 QA Team]:
  - Boundary: book qty = available -> allocated FULL; available + 1 -> only the available qty allocated (partial); product with 0 available -> unallocated, status Order.
  - Assert Transaction Inquiry Allocated = min(Ordered, available) (consistent with Q-TI1).

## 12. Open questions (batched for the BA)
- Q: Why does Unallocate answer "stock not found." (stock keyed by day, allocation reference missing)? | Default: stock record for the order date missing | Evidence: unexplained. (Update 2026-10-01 G11-1: not reproduced; Unallocate succeeded on a same-day order with stock received that day. Likely stale-day data on 09-29 [inferred]. | Class: B)
- Q: Is the framework's manual Allocation meant for a configuration without auto-allocation, and should Unallocation run in this cycle? | Default: keep the step but expect no-op | Evidence: draft step sheet questions 2. (Update 2026-10-01 G11-1: QA lead chose to unallocate one order and re-allocate it, so the GIN still has all orders. | Class: C)
- Q: What does Allocation do on short stock? | Default: partial allocation | Class: B | Evidence: not tested.
- Q-OB1: Who or what generated the day's opening balances during 2026-10-01 (0 in the morning, rebuilt from the previous day with allocation released by 16:40)? This decides the Allocated and Closing a check starts from. | Default: unknown | Class: B | Evidence: session report §8. **-> ANSWERED 2026-10-05**: openings are created by the first movement of the day (DA approval) = previous Closing + still-Allocated (see stock_inquiry_and_balances.md, OPEN_QUESTIONS.md).
- G11-2: Q (Unallocate "stock not found.") not reproduced on a second same-day run (10-05); stays PARTLY (cause [inferred] stale-day data). ANSWERED 2026-10-05 (Q-OB1): see stock_inquiry_and_balances.md.
- Q26 evidence 2026-10-06: not reproduced on a third day; close if confirmed once more [observed 2026-10-06 G11-3].
- **Allocation on short stock (Q27) ANSWERED 2026-10-08** [stated 2026-10-08 QA Team]: partial allocation of the available quantity; nothing available -> unallocated, status Order.

## 13. Sources
atlas flows 00130001, 00130002, group_11.md; TC-OB-01_executed.md (TC-OB-03); ui.md "Order Stock Allocation"; STEP_SHEET_DRAFT_next.md; DB `rpl_pr_sar_stock_alloc_rules`, `snd_tr_cmm_cashmemo_master` (column names).
- Live learning session G11-1 (2026-10-01, cnr1dev1, distributor 15108843): `learning_sessions/2026-10-01_G11-PK_session1_log.md` seq 12, 16 (stock effect), 18, 24; `learning_sessions/2026-10-01_G11-PK_session1_report.md` §3 rule 4, §5, §7, §8.
- G11-2: learning_sessions/2026-10-05_G11-PK_session2_log.md (seq 12, 18).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 12, 15 preparation, 18, seq 51 resolution).

- QA team written answers 2026-10-08: learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx) (rules 2, 4; Q16 / Q27).
