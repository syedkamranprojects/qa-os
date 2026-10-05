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
updated: 2026-10-01
---
# Stock Allocation and Unallocation: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 00130001 (seq 12), 00130002 (seq 18; seq 25 duplicate inactive).

## 1. Purpose
Allocation reserves warehouse stock to booked orders so that the GIN can issue exactly the goods promised. [inferred] Unallocation releases that reservation so the stock can be given to other orders or the order can be edited. [inferred] On cnr1dev1 allocation is automatic at order save, so the manual screen mostly shows the result.
- Confirmed 2026-10-01: all 6 orders booked that day were already FULL on the Allocated tab; the manual Allocation step only matters for orders that did not get stock at booking (or were unallocated). [observed 2026-10-01 G11-1] (reservation at booking upgraded from [inferred]: booking reserves stock immediately, Allocated up and Closing down; cancellation releases it; see order_booking.md and order_editing_cancellation.md.)

## 2. Actors and roles
Auto_Multi_Orga (same session as order booking). [observed]
- Maker = Auto_Multi_Orga: allocates and unallocates. [observed 2026-10-01 G11-1, seq 12 and 18]
- Checker: no role on this option (no approval step). [observed 2026-10-01 G11-1]

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

## 5. Process: the business steps in order
1. [Maker] Navigate to Order Stock Allocation. (`11:12:00130001`)
2. [Maker] Verify Order Date and PJP Number; open the Unallocated tab. (`11:12:00130001`)
3. [Maker] Filter Outlet "Aautomation", select all, click Allocation, accept the browser alert "Are you sure you want to proceed?". -> "Process completed successfully". [observed] (`11:12:00130001`) Live 2026-10-01: the Unallocated tab was empty (all 6 orders auto-allocated), so the step was a no-op. [observed 2026-10-01 G11-1]
4. Unallocation (seq 18): Allocated tab, select rows, Unallocate, accept alert. -> observed answer "stock not found." [observed] (`11:18:00130002`) (superseded 2026-10-01: the same action answered "Process completed successfully", see step 5.)
5. [Maker] Open the Allocated tab; Select order COL26000002007 (one order only); Click Unallocate; Accept "Are you sure you want to proceed?" -> toast **"Process completed successfully"**; the order leaves the Allocated tab and appears on the Unallocated tab. [observed 2026-10-01 G11-1] (`11:18:00130002`)
6. [Maker] Open the Unallocated tab; Select order COL26000002007; Click Allocation; Accept "Are you sure you want to proceed?" -> **"Process completed successfully"**; the order is back on the Allocated tab, FULL (all 5 orders 2003-2007 FULL). [observed 2026-10-01 G11-1] (`11:12:00130001` manual allocation, exercised after `11:18:00130002`)

## 6. Outputs and effects
- Allocated orders move to the Allocated tab; Allocation Status FULL. [observed]
- Stock effect (reserved/allocated quantity per warehouse): the Stock Inquiry Allocated columns carry it: on 2026-09-30, 13 rows had Allocated > 0 (e.g. 62740537 Auto Main 63 CS = the GIN 505 line) and Closing is net of Allocated [observed 2026-10-01]. Allocation also covers documents other than GIN 505 (20050308 Auto Main allocated 39 CS 96 PC vs GIN line 18 CS 16 PC) [observed]. Opening/Allocated on the new day are 0 for the received product (Allocated 0 on 10-01) [observed]. (superseded 2026-10-01 later in the day: by 16:40 the day had Opening balances and Allocated 63 CS for 62740537 at Auto Main = the pending GIN 505 reservation; who generated the openings is open, Q-OB1. [observed 2026-10-01 G11-1])
- Transaction Inquiry shows an allocated CS column (`row_1_allocated_cs`) per order line. [atlas] Confirmed: the Detail window shows **Allocated** CS/DZ/PC (normalised, e.g. 7/0/0). [observed 2026-10-01 G11-1]
- Booking allocates at save: Stock Inquiry Allocated +order quantity, Closing -order quantity (62740537 Allocated 63 -> 98 for 5 open orders x 7 CS, Closing 261 -> 226). Cancellation released 7 CS. Closing = Opening + In - Out - Allocated. [observed 2026-10-01 G11-1]
- Unallocate / re-allocate stock effect: not snapshotted; expected to be the same release/reserve mechanism as cancellation and booking. [inferred 2026-10-01 G11-1]
- At GIN approval the issued quantity leaves Allocated and appears as Out; Closing does not change (62740537 Allocated 98 -> 63). [observed 2026-10-01 G11-1; see goods_issue_note]

## 7. Statuses and transitions
| from | action | to | by | tag |
|---|---|---|---|---|
| Unallocated | Order saved | Allocated (FULL) automatically | system | [observed]; re-observed for 6 orders [observed 2026-10-01 G11-1] |
| Unallocated | Allocation | Allocated | Maker | [observed]; re-observed on COL26000002007 [observed 2026-10-01 G11-1] |
| Allocated | Unallocate | (expected Unallocated) | Maker | [inferred]; observed result "stock not found." (superseded 2026-10-01) |
| Allocated | Unallocate | Unallocated (order moves to the Unallocated tab) | Maker | [observed 2026-10-01 G11-1] (was [inferred]) |
| Allocated | GIN approved | allocation consumed (Allocated -> Out) | Checker (GIN) | [observed 2026-10-01 G11-1] |

## 8. Rules and validations
- Orders are auto-allocated at save (all 8 new orders already Allocated). [observed] Again all 6 orders of 2026-10-01. [observed 2026-10-01 G11-1]
- Only an older order (COL26000001988, outlet 1000000002) was in Unallocated and was allocated by the manual step. [observed]
- The screen date filters by Order Date; orders booked yesterday must have the date typed (send-keys then Enter). [observed]
- Alert must be accepted through the browser; script clicks cannot. [observed]
- Unallocate failed for all 9 orders, also for the 8 new ones alone, nothing changed. [observed] (superseded 2026-10-01: Unallocate of one order succeeded with "Process completed successfully" and moved it to the Unallocated tab; the 09-29 failure was not reproduced [observed 2026-10-01 G11-1].)
- Unallocate and Allocation both ask for confirmation "Are you sure you want to proceed?". [observed 2026-10-01 G11-1]
- An unallocated order can be allocated again with the manual Allocation button (FULL). [observed 2026-10-01 G11-1]
- Partial allocation when stock is short: [unknown].

## 9. Messages
"Are you sure you want to proceed?" (confirm alert); "Process completed successfully" (allocation, key Stock_Allocation_ASSR); "stock not found." (unallocation; framework key Unallocated_ASSR expects something else, [unknown] what). [observed]
- 2026-10-01: Unallocate answered **"Process completed successfully"** (toast) after the confirm; Allocation of the same order answered the same text. [observed 2026-10-01 G11-1] ("stock not found." superseded 2026-10-01 for this data; kept as the 09-29 observation.)

## 10. Dependencies
Reads orders from Order Booking and stock from the DA; day-keyed stock balances. Hands allocated orders to Order Editing/Cancellation (hidden when allocated, see order_editing_cancellation.md) and to GIN (cash memo selection).
- (superseded 2026-10-01: allocated orders are NOT hidden from Order Editing/Cancellation; the empty outlet list was caused by the Order Editing date filter working on the delivery date. See order_editing_cancellation.md. [observed 2026-10-01 G11-1])
- The GIN issues allocated cash memos only; an unallocate of all orders right before the GIN would leave nothing to issue. [inferred 2026-10-01 G11-1]

## 11. Test design hints
- Positive: save an order and verify Allocated tab shows it (FULL); allocate an old Unallocated order.
- Negative: order quantity beyond stock -> expect partial/Unallocated; unallocate when stock missing.
- Boundary: stock exactly equals order quantity; Order Date yesterday/tomorrow.
- Traps: "Process completed successfully" with zero Unallocated rows proves nothing; the manual step is a no-op on auto-allocation; the Unallocated_ASSR expected text may never match.
- New 2026-10-01 [observed 2026-10-01 G11-1]:
  - Positive round trip: unallocate ONE order (assert it moves to Unallocated, no Allocation Status column), allocate it again (assert FULL), then snapshot Stock Inquiry Allocated before/after to prove the stock effect (not yet measured).
  - Trap (framework drift): flow 00130002 selects ALL rows (filter "Aautomation", select-all) and unallocates everything right before the GIN; run as written it leaves the GIN with no allocated cash memos. Unallocate one order, or re-allocate before the GIN.
  - Trap: the confirm dialog must be accepted, otherwise nothing happens and no toast appears.

## 12. Open questions (batched for the BA)
- Q: Why does Unallocate answer "stock not found." (stock keyed by day, allocation reference missing)? | Default: stock record for the order date missing | Evidence: unexplained. (Update 2026-10-01 G11-1: not reproduced; Unallocate succeeded on a same-day order with stock received that day. Likely stale-day data on 09-29 [inferred]. | Class: B)
- Q: Is the framework's manual Allocation meant for a configuration without auto-allocation, and should Unallocation run in this cycle? | Default: keep the step but expect no-op | Evidence: draft step sheet questions 2. (Update 2026-10-01 G11-1: QA lead chose to unallocate one order and re-allocate it, so the GIN still has all orders. | Class: C)
- Q: What does Allocation do on short stock? | Default: partial allocation | Class: B | Evidence: not tested.
- Q-OB1: Who or what generated the day's opening balances during 2026-10-01 (0 in the morning, rebuilt from the previous day with allocation released by 16:40)? This decides the Allocated and Closing a check starts from. | Default: unknown | Class: B | Evidence: session report §8.

## 13. Sources
atlas flows 00130001, 00130002, group_11.md; TC-OB-01_executed.md (TC-OB-03); ui.md "Order Stock Allocation"; STEP_SHEET_DRAFT_next.md; DB `rpl_pr_sar_stock_alloc_rules`, `snd_tr_cmm_cashmemo_master` (column names).
- Live learning session G11-1 (2026-10-01, cnr1dev1, distributor 15108843): `learning_sessions/2026-10-01_G11-PK_session1_log.md` seq 12, 16 (stock effect), 18, 24; `learning_sessions/2026-10-01_G11-PK_session1_report.md` §3 rule 4, §5, §7, §8.
