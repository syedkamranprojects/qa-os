# Order lifecycle and statuses: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 00010001, 00130001/2, 00020001, 00040001, 00160001, 02960001 (group 11 seq 10-19).

## 1. Purpose
Explains what an "order" is in DCODE and how it moves from booking to delivery, so every other page in this folder can refer to it. The order and the sale are the same record: a **cash memo** (`snd_tr_cmm_cashmemo_master`) that starts as an Ordered cash memo and becomes Delivered after the GIN/delivery. [db][inferred]

## 2. Actors and roles
Order user (Auto_Multi_Orga) books, edits, cancels, allocates, changes delivery dates; Stock Controller issues the GIN; checker Auto_Tssm approves GINs. [observed]

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

## 4. Inputs: screens and fields
See order_booking.md. Header grids across order screens share columns: Document No, Document Date, Delivery Date, Demand Channel, Outlet Name, Gross Amount, Discount, Tax, Net Amount, Balance Amount, Received Amount. [observed via step_labels]

## 5. Process: lifecycle in order
1. Order Booking: Validate + Save -> order created, auto-allocated. (seq 10)
2. Stock Allocation (manual) -> only for orders not yet allocated. (seq 12)
3. Transaction Inquiry: verify amounts, status. (seq 14)
4. Order Editing / Order Cancellation while the order is still editable. (seq 15, 16)
5. Unallocation, Delivery Date Change. (seq 18, 19)
6. GIN selects the orders for a delivery PJP, approval issues stock; then "After GIN" editing/cancellation (seq 29, 31). (delivery area)
7. Delivery -> status Delivered; sales return / settlement follow. (other areas)

## 6. Outputs and effects
- At save: order header + lines + charges/offerings rows [db: tables `snd_tr_cmm_cashmemo_detail`, `_charges`, `_offering`, `_offritem`]; stock allocation flag `tcmm_stock_allocated_status` and `tcmm_alloc_ref_no` [db column names; semantics inferred].
- Monetary fields: Gross (list value of lines at trade price), Discount (negative, schemes/trade offers), Tax, Net = Gross + Discount + Tax. [observed arithmetic]
- Charges tab ("Additional Charges"/"Total Tax") shows Charges Amount and Tax Amount per order. [observed in atlas flows 02960001, 03190001]

## 7. Statuses and transitions
Live-verified 2026-10-01 [db, read-only SQL on master data + Transaction Inquiry]: **"Confirmed" is its own EXECUTION status 02** (identifier ALC = allocated, description with a trailing space), not an alias of document status 04 Ordered. Execution status CM-01 (glb_pr_exs_execution_status, org 010104): 01 Ordered (CRT), 02 Confirmed (ALC), 03 Planning completed (DISPT, identifier GIN, follows 02), 05 Cancelled, 07 PLANNING, 08 EXECUTING, 09 PARKED, 10 Delivered/Invoiced, 11 Dispatched, 12 Sent to Locus, 13 Ready to dispatch/Packed (GINAPPRVD), 14-17 Danone Pending/Blocked/UnBlocked/Completed, 18 Partial Delivered, 20 Out for delivery; codes 04, 06 and 19 do not exist in that master (correction: 19 CM Reschedule, listed elsewhere in these pages from org 0101, is absent from the 010104 execution master; the reschedule status is to be re-read live). CM-02 execution: 01 Authorized Un-Picked, 03 Cancelled, 04 Picked, 05 Un-Authorized Un-Picked. Document status (snd_pr_dos_documentstatus) CM-01: 01 Delivered, 02 Un-Delivered (inactive), 03 Cancelled, 04 Ordered, 05 Amendment (inactive); CM-02: 01 Authorized, 02 Un-Authorized, 03 Cancelled, 04 Picked. Ordered therefore exists twice (document 04, execution 01). The Transaction Inquiry status text comes from the execution table: the 8 orders on GIN 505 show "Planning completed" (exec 03), cancelled ones "Cancelled", delivered ones "Delivered/Invoiced"; "Confirmed" and "Ordered" appear on 2026-10-01 only as filter options [observed]. Caveat: the snd-schema connector is database ng_astrone (newest cash memo 2026-01-30, no COL26000001979-2002), so per-order codes could not be cross-checked.
Statuses of CM-01 for org 010104 [db]: 01 Delivered (nature DEL), 02 Un-Delivered (inactive), 03 Cancelled (CNL), 04 Ordered (PLD), 05 Amendment (inactive, AMD).
| from | action | to | by | tag |
|---|---|---|---|---|
| none | Order Booking save | document 04 Ordered; execution 02 Confirmed (after allocation) | Order user | [db][observed] |
| Confirmed (exec 02) | put on a GIN (Draft/Pending) | exec 03 Planning completed | Stock Controller | [db + observed 2026-10-01: orders on GIN 505] |
| Ordered | Order Cancellation | Cancelled 03 | Order user | [db][inferred transition] |
| Ordered | GIN approved and delivered | Delivered 01 | delivery | [inferred] |
| Ordered | Order Editing save | Ordered (new amounts); Amendment 05 inactive so not used | Order user | [inferred] |
Allocation is a separate dimension: Unallocated / Allocated (Allocation Status FULL after save). [observed]

## 8. Rules and validations
- Allocated orders are NOT listed in Order Editing / Order Cancellation outlet lists (outlet API returned []). [observed; cause unproven]
- Unallocate answers "stock not found." for all orders. [observed]
- Stock balances are keyed by calendar day: a cycle must complete within one day. [observed]
- Order totals identical to the workbook for 8 orders. [observed]

## 9. Messages
"Order Save successfully", "Validation successfully", "Process completed successfully", "stock not found.", "Delivery Date has been changed successfully, processed orders: 9". [observed] Details on each page.

## 10. Dependencies
Reads DA stock; hands order numbers (`ORDERNUMBER`) to editing and GIN; GIN hands `REPO_GINNO` to cashmemo reschedule/status, deposit slips, sales returns, route settlement (other analysts).

## 11. Test design hints
- Verify status text in Transaction Inquiry after each lifecycle step (Confirmed after booking). Check DB `pdos_docmstatus` of the cash memo moves 04 -> 03 after cancel.
- Negative: cancel an order already on a GIN; edit after delivery.
- Trap (resolved 2026-10-01): "Confirmed" is execution status 02, "Ordered" is document status 04 and execution 01, "Planning completed" is execution 03 once the order is on a GIN; assert the Document Status column text of Transaction Inquiry (it shows the execution status).

## 12. Open questions (batched for the BA)
- ANSWERED 2026-10-01 (Q23): "Confirmed" is execution status 02, a separate status; Ordered 04 is the document status; "Planning completed" is execution 03 [db + observed].
- Q: What is the difference between document type `2` (PLACED) and CM-01 orders? | Default: 2 = tele-order demand, CM-01 = booked order | Evidence: names only.
- Q: What does Amendment (05, inactive) mean? | Default: unused | Evidence: inactive.

## 13. Sources
snd-schema DB tables `snd_pr_dot_documenttype`, `snd_pr_dos_documentstatus`, `snd_tr_cmm_cashmemo_master` (columns only; no order rows exist in the base DB for org 010104, orders live in the environment overlay); TC-OB-01_executed.md (TC-OB-03 section); ui.md "Verified in the group 11 replay"; atlas flows 02960001, 03190001.
