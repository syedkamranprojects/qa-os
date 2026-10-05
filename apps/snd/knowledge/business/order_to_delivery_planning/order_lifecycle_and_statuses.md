---
option: Order lifecycle and statuses (cross-cutting)
area: order_to_delivery_planning
doc_types: [CM-01, CM, "2", CM-02, CM-04, GN-01, CM-06]
screens: [ORDER_BOOKING, DYL_201904, ORDER_EDITING, DYL_202022, DYL_201080, DYL_102014]
framework_flows: ["00010001", "00130001", "00020001", "00040001", "00130002", "00160001", "02960001", "00050001", "00780001", "00840001", "00850001", "01040001", "00030001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [order_booking, stock_allocation, transaction_inquiry, order_editing_cancellation, delivery_date_change]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-05
---
# Order lifecycle and statuses: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 00010001, 00130001/2, 00020001, 00040001, 00160001, 02960001 (group 11 seq 10-19); G11-1 also seq 20, 23 (GIN), 29, 31 (after GIN), 32, 33 (reschedule / status).
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.

## 1. Purpose
Explains what an "order" is in DCODE and how it moves from booking to delivery, so every other page in this folder can refer to it. The order and the sale are the same record: a **cash memo** (`snd_tr_cmm_cashmemo_master`) that starts as an Ordered cash memo and becomes Delivered after the GIN/delivery. [db][inferred]
- Confirmed live 2026-10-01: the same Document No (e.g. COL26000002003) goes from Confirmed to Delivered/Invoiced and is the "Principle Invoice" of a later sales return. (upgraded: [observed 2026-10-01 G11-1], was [inferred])

## 2. Actors and roles
Order user (Auto_Multi_Orga) books, edits, cancels, allocates, changes delivery dates; Stock Controller issues the GIN; checker Auto_Tssm approves GINs. [observed]
- Roles restated 2026-10-01 (only Maker and Checker exist): **Maker** = Auto_Multi_Orga books, allocates/unallocates, edits, cancels, changes delivery dates, creates and forwards the GIN, reschedules and sets Cashmemo Status; **Checker** = Auto_Tssm approves the GIN with one Forward. No step in the order lifecycle itself needs a Checker. ("Order user" and "Stock Controller" superseded 2026-10-01: both are the Maker. [observed 2026-10-01 G11-1])

## 3. Documents and master data
Document types for org 010104 [db]:
| code | description | note |
|---|---|---|
| CM-01 | Sales | the order/cash memo; group CM, nature identifier CM |
| CM | Cash Memo | parent type, status Ordered (04) |
| 2 | Demand Captured from Tele order | status PLACED (88); default type in Transaction Inquiry [observed] |
| CM-02 / CM-04 | Sales Return / Fresh Sales Return | statuses Authorized, Un-Authorized, Cancelled, Picked (sales return area) |
| GN-01 | Goods Issue Note | delivery area |
| CM-06 | B2B Sale | [unknown] use |
Order-level master data: PJP (daily route, order-booker and delivery PJP are separate columns `epjp_pjpno_daily` / `epjp_pjpno_daily_delivery` [db]), Section, Selling Category (shown as 201-Selling Category 001), Outlet, Demand Channel (grid column), Reference Number (`tcmm_ref_no`).
- Booking PJP 02111-AutomationOB1 and delivery PJP 02112-AutomationDSR are separate PJPs (PJP Delivery No on Delivery Date Change / Cashmemo Reschedule; Delivery Man PJP on the GIN). (upgraded: [observed 2026-10-01 G11-1], was [db])
- Order numbers COL26000002003-2008 (2026-10-01); sales return COL26000000713 has its own series (CM-02). [observed 2026-10-01 G11-1]

## 4. Inputs: screens and fields
See order_booking.md. Header grids across order screens share columns: Document No, Document Date, Delivery Date, Demand Channel, Outlet Name, Gross Amount, Discount, Tax, Net Amount, Balance Amount, Received Amount. [observed via step_labels] (Live 2026-10-01 on Order Editing and Sales Return grids. [observed 2026-10-01 G11-1])

## 5. Process: lifecycle in order
1. Order Booking: Validate + Save -> order created, auto-allocated. (seq 10)
2. Stock Allocation (manual) -> only for orders not yet allocated. (seq 12)
3. Transaction Inquiry: verify amounts, status. (seq 14)
4. Order Editing / Order Cancellation while the order is still editable. (seq 15, 16)
5. Unallocation, Delivery Date Change. (seq 18, 19)
6. GIN selects the orders for a delivery PJP, approval issues stock; then "After GIN" editing/cancellation (seq 29, 31). (delivery area)
7. Delivery -> status Delivered; sales return / settlement follow. (other areas)

Standard-vocabulary chain, as walked 2026-10-01 [observed 2026-10-01 G11-1]:
1. [Maker] Save Order (Validation, Save) -> Confirmed, Allocated FULL, delivery date = next PJP visit (10-07). (`11:10:00010001`)
2. [Maker] Verify Allocation on Order Stock Allocation (no-op when auto-allocated). (`11:12:00130001`)
3. [Maker] Verify Order in Transaction Inquiry (Confirmed, amounts, offerings, tax). (`11:14:02960001`)
4. [Maker] Edit Order before the GIN: skipped 2026-10-01 (QA/BA discussion). (`11:15:00020001`)
5. [Maker] Cancel Order before the GIN -> Cancelled, stock released. (`11:16:00040001`)
6. [Maker] Unallocate Order, then Allocate it again -> back to FULL. (`11:18:00130002`)
7. [Maker] Change Delivery Date to today -> still Confirmed, delivery 10-01. (`11:19:00160001`)
8. [Maker] Create and Forward GIN -> GIN Pending for approval. (`11:20:00050001`)
9. [Checker] Approve GIN (one Forward) -> orders Ready to dispatch/Packed, stock Out. (`11:23:00780001`)
10. [Maker] Edit Order after the GIN -> amounts change, no stock movement. (`11:29:00840001`)
11. [Maker] Cancel Order after the GIN -> Cancelled, GIN No kept, no stock movement. (`11:31:00850001`)
12. [Maker] Reschedule Cashmemo -> Reattempt, off the GIN, new delivery date. (`11:32:01040001`)
13. [Maker] Save Cashmemo Status for delivered cash memos -> Delivered/Invoiced, Actual Delivery Date set. (`11:33:00030001`)
14. Not delivered quantities (cancelled, cut, rescheduled, returned) come back on the Goods Return Note (delivery area, seq 48).

## 6. Outputs and effects
- At save: order header + lines + charges/offerings rows [db: tables `snd_tr_cmm_cashmemo_detail`, `_charges`, `_offering`, `_offritem`]; stock allocation flag `tcmm_stock_allocated_status` and `tcmm_alloc_ref_no` [db column names; semantics inferred].
- Monetary fields: Gross (list value of lines at trade price), Discount (negative, schemes/trade offers), Tax, Net = Gross + Discount + Tax. [observed arithmetic] Header Net is rounded to the whole rupee. [observed 2026-10-01 G11-1]
- Charges tab ("Additional Charges"/"Total Tax") shows Charges Amount and Tax Amount per order. [observed in atlas flows 02960001, 03190001] Live: Total Tax = 0001 Value Added Tax + 9000 3rd Schduele (sic). [observed 2026-10-01 G11-1]
- **Stock along the lifecycle** [observed 2026-10-01 G11-1, Stock Inquiry Auto Main, Sound]:

| Step | Allocated | Out | Closing | In |
|---|---|---|---|---|
| Order saved | + order qty | - | - order qty | - |
| Cancel before GIN | - order qty (released) | - | + order qty | - |
| GIN approved | - issued qty | + issued qty | unchanged | - |
| Edit / cancel / reschedule after GIN | unchanged | unchanged | unchanged | - |
| GRN approved | - | unchanged | + returned qty | + returned qty |

Closing = Opening + In - Out - Allocated. [observed 2026-10-01 G11-1]
- G11-2/2b: the whole chain reproduced on 2026-10-05 (orders 2009-2014): Confirmed -> Ready to dispatch/Packed (GIN 507) -> Delivered/Invoiced (2009-2011); Reattempt (2012, new delivery 10-06); Cancelled before (2014) and after (2013) the GIN. After settlement the delivered memos carry Offset = posted slip allocations; a partly returned memo stays Delivered/Invoiced, its return reads Picked with Demand Channel "Partial Return" [observed 2026-10-05 G11-2, G11-2b].

## 7. Statuses and transitions
Live-verified 2026-10-01 [db, read-only SQL on master data + Transaction Inquiry]: **"Confirmed" is its own EXECUTION status 02** (identifier ALC = allocated, description with a trailing space), not an alias of document status 04 Ordered. Execution status CM-01 (glb_pr_exs_execution_status, org 010104): 01 Ordered (CRT), 02 Confirmed (ALC), 03 Planning completed (DISPT, identifier GIN, follows 02), 05 Cancelled, 07 PLANNING, 08 EXECUTING, 09 PARKED, 10 Delivered/Invoiced, 11 Dispatched, 12 Sent to Locus, 13 Ready to dispatch/Packed (GINAPPRVD), 14-17 Danone Pending/Blocked/UnBlocked/Completed, 18 Partial Delivered, 20 Out for delivery; codes 04, 06 and 19 do not exist in that master (correction: 19 CM Reschedule, listed elsewhere in these pages from org 0101, is absent from the 010104 execution master; the reschedule status is to be re-read live). CM-02 execution: 01 Authorized Un-Picked, 03 Cancelled, 04 Picked, 05 Un-Authorized Un-Picked. Document status (snd_pr_dos_documentstatus) CM-01: 01 Delivered, 02 Un-Delivered (inactive), 03 Cancelled, 04 Ordered, 05 Amendment (inactive); CM-02: 01 Authorized, 02 Un-Authorized, 03 Cancelled, 04 Picked. Ordered therefore exists twice (document 04, execution 01). The Transaction Inquiry status text comes from the execution table: the 8 orders on GIN 505 show "Planning completed" (exec 03), cancelled ones "Cancelled", delivered ones "Delivered/Invoiced"; "Confirmed" and "Ordered" appear on 2026-10-01 only as filter options [observed]. Caveat: the snd-schema connector is database ng_astrone (newest cash memo 2026-01-30, no COL26000001979-2002), so per-order codes could not be cross-checked.
- Reschedule status re-read live 2026-10-01: a rescheduled cash memo shows **"Reattempt"** in Transaction Inquiry (a status in the Document Status filter list). [observed 2026-10-01 G11-1] "Confirmed" was seen on real orders right after booking (COL26000002003-2007). [observed 2026-10-01 G11-1]
Statuses of CM-01 for org 010104 [db]: 01 Delivered (nature DEL), 02 Un-Delivered (inactive), 03 Cancelled (CNL), 04 Ordered (PLD), 05 Amendment (inactive, AMD).
| from | action | to | by | tag |
|---|---|---|---|---|
| none | Order Booking save | document 04 Ordered; execution 02 Confirmed (after allocation) | Maker | [db][observed]; re-observed [observed 2026-10-01 G11-1] |
| Confirmed (exec 02) | put on a GIN (Draft/Pending) | exec 03 Planning completed | Maker (GIN) | [db + observed 2026-10-01: orders on GIN 505] |
| Ordered | Order Cancellation | Cancelled 03 | Maker | [db][inferred transition]; upgraded [observed 2026-10-01 G11-1] (was [inferred]): COL26000002008 Confirmed -> Cancelled |
| Ordered | GIN approved and delivered | Delivered 01 | delivery | [inferred]; upgraded [observed 2026-10-01 G11-1] (was [inferred]): see the two rows below |
| Ordered | Order Editing save | Ordered (new amounts); Amendment 05 inactive so not used | Maker | [inferred] (after the GIN: status unchanged, same Document No [observed 2026-10-01 G11-1]) |
| Confirmed / Planning completed | GIN approved (Checker Forward) | Ready to dispatch/Packed (exec 13), GIN No set | Checker | [observed 2026-10-01 G11-1] |
| Ready to dispatch/Packed | Cashmemo Status save | Delivered/Invoiced (exec 10), Actual Delivery Date = save time | Maker | [observed 2026-10-01 G11-1] |
| Ready to dispatch/Packed | Cashmemo Reschedule | Reattempt, new Delivery Date, GIN No cleared | Maker | [observed 2026-10-01 G11-1] |
| Ready to dispatch/Packed | Order Cancellation | Cancelled, GIN No kept | Maker | [observed 2026-10-01 G11-1] |
| Confirmed | Delivery Date Change | Confirmed (new delivery date) | Maker | [observed 2026-10-01 G11-1] |
Allocation is a separate dimension: Unallocated / Allocated (Allocation Status FULL after save). [observed]
- G11-2b: no Partial Delivered (18) status appeared on COL26000002009 after its partial return; it stayed Delivered/Invoiced [observed 2026-10-05 G11-2b].

## 8. Rules and validations
- Allocated orders are NOT listed in Order Editing / Order Cancellation outlet lists (outlet API returned []). [observed; cause unproven] (superseded 2026-10-01: allocation does not hide orders; Order Editing filters by delivery date and today's orders had delivery 10-05/10-07. Order Cancellation lists allocated orders of the order date. [observed 2026-10-01 G11-1])
- Unallocate answers "stock not found." for all orders. [observed] (superseded 2026-10-01: Unallocate of one same-day order answered "Process completed successfully". [observed 2026-10-01 G11-1])
- Stock balances are keyed by calendar day: a cycle must complete within one day. [observed] (Confirmed again: GIN 506 was approved only because stock was received and delivery dates moved to the same day. [observed 2026-10-01 G11-1])
- Order totals identical to the workbook for 8 orders. [observed] (2026-10-01: COL26000002003 = workbook order 04; the edit = workbook Detail3. [observed 2026-10-01 G11-1])
- An order stays editable and cancellable after the GIN is approved, without warning; after the GIN no stock moves until the GRN. [observed 2026-10-01 G11-1]
- The delivery date of a new order is the PJP's next visit (10-05 for 09-29 bookings, 10-07 for 10-01 bookings). [inferred, supported by observation 2026-10-01 G11-1]

## 9. Messages
"Order Save successfully", "Validation successfully", "Process completed successfully", "stock not found.", "Delivery Date has been changed successfully, processed orders: 9". [observed] Details on each page.
- 2026-10-01 additions: "Are you sure you want to proceed?" (confirm on Allocation, Unallocate, Delivery Date Change, Cashmemo Reschedule); "Delivery Date has been changed successfully, processed orders: 5"; "Order Cancelled Successfully" (result window, Status "Successfull" sic); "Updated successfully" (Cashmemo Status). "stock not found." superseded for Unallocate by "Process completed successfully". [observed 2026-10-01 G11-1]

## 10. Dependencies
Reads DA stock; hands order numbers (`ORDERNUMBER`) to editing and GIN; GIN hands `REPO_GINNO` to cashmemo reschedule/status, deposit slips, sales returns, route settlement (other analysts).
- Same-day chain: DA approved today -> orders booked -> Delivery Date Change to today -> GIN same day. The GIN refuses cash memos with a delivery date earlier than the PJP working date. [observed 2026-10-01 G11-1]

## 11. Test design hints
- Verify status text in Transaction Inquiry after each lifecycle step (Confirmed after booking). Check DB `pdos_docmstatus` of the cash memo moves 04 -> 03 after cancel.
- Negative: cancel an order already on a GIN; edit after delivery.
- Trap (resolved 2026-10-01): "Confirmed" is execution status 02, "Ordered" is document status 04 and execution 01, "Planning completed" is execution 03 once the order is on a GIN; assert the Document Status column text of Transaction Inquiry (it shows the execution status).
- New 2026-10-01 [observed 2026-10-01 G11-1]:
  - End-to-end status test: assert Confirmed -> Ready to dispatch/Packed -> Delivered/Invoiced, plus the side exits Reattempt and Cancelled (before and after the GIN, GIN No kept only after).
  - Stock along the lifecycle (table in section 6): snapshot Stock Inquiry before/after each step; a green toast never proves the stock effect.
  - Trap: Order Editing filters the delivery date while Order Cancellation filters the order date; a test that sets the same date range on both will find the order on only one of them.
  - Trap: edit/cancel after the GIN is allowed without warning and moves no stock; assert the GRN later returns the quantity, not an immediate stock change.
  - Trap: the reschedule/DDC confirm dialog "Are you sure you want to proceed?" must be accepted.
  - Trap: the order-editing grid with an SKU filter shows a negative Net (display defect); do not use that grid for amount assertions.

## 12. Open questions (batched for the BA)
- ANSWERED 2026-10-01 (Q23): "Confirmed" is execution status 02, a separate status; Ordered 04 is the document status; "Planning completed" is execution 03 [db + observed].
- Q: What is the difference between document type `2` (PLACED) and CM-01 orders? | Default: 2 = tele-order demand, CM-01 = booked order | Class: C | Evidence: names only.
- Q: What does Amendment (05, inactive) mean? | Default: unused | Class: A | Evidence: inactive. (2026-10-01: an edit after the GIN did not change the status [observed 2026-10-01 G11-1].)
- ANSWERED 2026-10-01 G11-1: why allocated orders were missing from Order Editing (empty outlet list) = the delivery-date filter, not allocation. [observed]
- Q-OE1: Is the Order Editing date range meant to be the delivery date, default today? | Default: treat as delivery date | Class: C | Evidence: report §8.
- Q-OE2: Which order should seq 15 edit when outlets 1000000001-03 are not offered? | Default: outlet 1000000004's order | Class: C | Evidence: report §8.
- Q-OB1: Who or what generated today's opening balances during the day? | Default: unknown | Class: B | Evidence: report §8. **-> ANSWERED 2026-10-05**: openings are created by the first movement of the day (DA approval) = previous Closing + still-Allocated (see stock_inquiry_and_balances.md, OPEN_QUESTIONS.md).
- Q-OE1 revised 2026-10-05 (Order Editing lists only orders whose delivery date is today; run it after Delivery Date Change?) | Class: C. New Q-OE4 (exact filter rule) | Class: B. ANSWERED 2026-10-05: Q-OB1 (openings at the first movement), Q33 (no Partial Delivered after a return) [observed 2026-10-05].

## 13. Sources
snd-schema DB tables `snd_pr_dot_documenttype`, `snd_pr_dos_documentstatus`, `snd_tr_cmm_cashmemo_master` (columns only; no order rows exist in the base DB for org 010104, orders live in the environment overlay); TC-OB-01_executed.md (TC-OB-03 section); ui.md "Verified in the group 11 replay"; atlas flows 02960001, 03190001.
- Live learning session G11-1 (2026-10-01, cnr1dev1, distributor 15108843): `learning_sessions/2026-10-01_G11-PK_session1_log.md` seq 10-33 and the two Transaction Inquiry status checks; `learning_sessions/2026-10-01_G11-PK_session1_report.md` §3 rules 3-7, 10, 11, §5, §8.
- G11-2 / G11-2b: learning_sessions/2026-10-05_G11-PK_session2_log.md, learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md.
