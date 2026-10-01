# Order Editing and Order Cancellation: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 00020001 (seq 15), 00040001 (seq 16), 00840001 Order Editing After GIN (seq 29), 00850001 Order Cancellation After GIN (seq 31); validation flows 03190001 (seq 68), 03740001 (seq 70).

## 1. Purpose
Order Editing changes quantities of a booked order (e.g. customer wants fewer cases) with a reason, recalculating gross, discount, tax and net. Order Cancellation withdraws an order entirely with a cancellation reason. Both exist before the GIN (seq 15/16) and again after the GIN (seq 29/31), where the business rule is different because stock has been issued. [inferred]

## 2. Actors and roles
Auto_Multi_Orga. [observed in group 11] Whether a checker must approve edits: [unknown] (no approval flow in the chain).

## 3. Documents and master data
Acts on the order cash memo; a successful edit produces `ORDERNUMBEREDIT` repo (an Order Number shown after edit; whether it is a new number or the same: [unknown]). Reasons come from master data: Reason Type (e.g. "Order Change QTY") and Cancellation Reason (e.g. "Shop Closed") [observed in step sheet draft; list [unknown]]. Statuses: Cancelled 03 [db].

## 4. Inputs: screens and fields
**Order Editing** (`/ngui/order-editing`, id ORDER_EDITING): PJP, Selling category, section (dropdowns), Start Date, End Date (date range), Outlet Name; result grid Document No, Document Date, Delivery Date, Outlet, Demand Channel, Gross Amount, Discount, Tax, Net Amount, Balance Amount, Received Amount; click Document No to open. [atlas/step_labels]
**Order Editing Detail**: per line OrderCS, OrderPC, Reason Type, Gross Amount; line Edit/Save/Cancel (`rowEditBtn_*`), Validation (`validateBtn`), Save (`saveBtn`), `OrderEditingBtn`. **Detail3**: Gross, Discount, Tax, Net, Order Number. [atlas]
**Order Cancellation** (option DYL_202022): PJP (mandatory), Section, Outlet Name, Date To; grid with checkbox per order (`row_1_checkbox_1`), Cancellation Reason (dropdown per row), Net Amount; buttons Refresh, Cancel All, Cancel (`cancelBtn`), Close. [atlas]

## 5. Process: the business steps in order
1. [Order User] Navigate to Order Editing; Choose PJP (category, section fill in); Choose Outlet Name; set date range to include the order. (`11:15:00020001`)
2. Open the order; edit line 1 (62740537): OrderCS = 4, OrderPC = 0, Reason Type = "Order Change QTY"; save the line; Validation; Save. Expected summary (workbook): Gross 96,840.34, Discount -20,718.07, Tax 14,584.79, Net 90,707.00. [draft step sheet; not executed]
3. [Order User] Navigate to Order Cancellation; Choose PJP; find outlet 1000000007 (order COL26000002001); select it; Cancellation Reason = "Shop Closed"; Cancel. Expected message "Order Cancelled Successfully" [unverified draft text]. (`11:16:00040001`)
4. After GIN: same screens with workbook NG_Dcode_QA_OTC_AfterGIN (seq 29, 31). Expected behaviour (allowed or refused): [unknown].
5. Validate in Transaction Inquiry after edit (seq 70, 68). See transaction_inquiry.md.

## 6. Outputs and effects
Edit: new amounts on the order, reason recorded; tax/charges recomputed (seq 68 checks Charges Amount and Tax Amount after editing). Cancellation: order status Cancelled 03 [db]; stock effect (release of allocation): [inferred], not observed. Neither step has been executed live.

## 7. Statuses and transitions
| from | action | to | by | tag |
|---|---|---|---|---|
| Ordered | Edit + Save | Ordered (amended amounts) | Order user | [inferred] |
| Ordered | Cancel | Cancelled (03) | Order user | [db] |
| Delivered / on GIN | Edit or Cancel | [unknown] | | [unknown] |

## 8. Rules and validations
- Outlet Name list is EMPTY for orders that show as Allocated (outlet API `getOultetsForOrderEditing` returned [] for PJP/section/category; a wide range returned older outlets). Correlation with allocation observed, not proven; alternative suspect: date range filters on delivery date (orders had 2026-10-05). [observed/inferred]
- Date fields must be typed with key events (DOM value ignored; request carried today). [observed] Live 2026-10-01: on Order Cancellation Refresh returned "Required parameter 'toDate' is not present." when Date To was typed (even with Tab/Enter); it worked only after picking the date from the calendar popup, so **typed dates are not always committed: use the calendar popup** [observed].
- Live 2026-10-01: the reason control exists only INSIDE a data-grid row (Order Cancellation grid column "Cancellation Reason"; Cashmemo Reschedule grid "Reschedule Reason"; Order Editing has no reason column until an order is opened). No order was eligible (all 24 orders Planning completed / Cancelled / Delivered), so the grids were empty and the dropdowns could not be opened (Order Editing PJP 02111, 2026-09-29..30: 0 rows; Order Cancellation PJP 02111, 2026-09-29..10-05: 0 rows) [observed].
- Reason lists [db, glb_pr_rnt_reason_type, org 010104, CM-01]: Order Editing Reason Type (identifier ORC, inferred): 0008 Order Change, 0009 Order Change QTY, 0010 Change Utlity (sic), 0020 Bogus order, 1001 testDesc, L01L01L01 and L01L01L01L01 Wrong Order/No Order, L02L04L07 and L02L04L07L01 No Scheme, L02L06L09L03 Stock Out, L0L1L1 and L0L1L1L1 Stock Already Avl. Cancellation reasons (identifier CNL; layout 202022 panel 3 is hand-coded so the use of this list is inferred): 0017 Shop Closed, 0018 Delivery is not possible due to any reason, 0019 Customer cancels delivery, 0021 customer refused, L02L01L01L01 Credit Exceeded, L02L02L03L01 Shop Closed, L02L03L04L01 Bad Weather, L02L03L04L02 Law & order Issue. Lists contain duplicates and test entries.
- PJP is mandatory on Order Cancellation. [atlas]
- Cancellation needs a reason per order row. [atlas]
- Order edit must be validated before save (ORD_EDIT_VALD_ASSR then ORD_EDIT_SAVE_ASSR). [atlas]

## 9. Messages
Observed: none (flows not reachable). Framework keys: ORD_EDIT_VALD_ASSR, ORD_EDIT_SAVE_ASSR, row message ELEVAL on the cancellation row, TSTMSG. Draft: "Order Cancelled Successfully" [unverified].

## 10. Dependencies
Needs an order from Order Booking (order 04 for editing, order 07 for cancellation) in an editable (probably Unallocated) state. Hands edited totals to Transaction Inquiry validation and to GIN.

## 11. Test design hints
- Positive: edit one line quantity down, check totals recalc and status; cancel one order with reason; verify Transaction Inquiry shows Cancelled.
- Negative: edit with no reason; quantity to zero for all lines; cancel without reason; cancel an order already on a GIN; edit after GIN.
- Boundary: quantity up by one case beyond stock; OrderPC larger than the pack size.
- Traps: green run with an empty outlet list asserts nothing; allocation state decides visibility, so state the order's allocation as precondition (unallocate first, if Unallocate worked).

## 12. Open questions (batched for the BA)
- Q: How does an allocated order reach Order Editing / Cancellation (unallocate first? delivery-date range?) | Default: unallocate first, range covers delivery date | Evidence: outlet list empty.
- Q: Are edits/cancellations after GIN allowed and what do they do to stock and the GIN? | Default: refused with a message | Evidence: unexecuted.
- Q: Does an edit keep the same Order Number? | Default: same number | Evidence: ORDERNUMBEREDIT repo suggests possibly new.
- Q: Allowed reason lists? | Default: use workbook reasons | Evidence: lists db-declared 2026-10-01 (PARTLY answered, Q22); real dropdowns not yet opened (needs an order in Ordered/Confirmed status).

## 13. Sources
atlas flows 00020001, 00040001, 00840001, 00850001, 03190001, 03740001; group_11.md; STEP_SHEET_DRAFT_next.md (rows 15, 16); ui.md "Order Editing / Order Cancellation"; step_labels "Order Editing", "Order Cancellation".
