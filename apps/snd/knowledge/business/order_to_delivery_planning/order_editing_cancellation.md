---
option: Order Editing and Order Cancellation
area: order_to_delivery_planning
doc_types: [CM-01]
screens: [ORDER_EDITING, DYL_202022]
framework_flows: ["00020001", "00040001", "00840001", "00850001", "03190001", "03740001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [order_booking, stock_allocation, goods_issue_note]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-01
---
# Order Editing and Order Cancellation: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 00020001 (seq 15), 00040001 (seq 16), 00840001 Order Editing After GIN (seq 29), 00850001 Order Cancellation After GIN (seq 31); validation flows 03190001 (seq 68), 03740001 (seq 70).

## 1. Purpose
Order Editing changes quantities of a booked order (e.g. customer wants fewer cases) with a reason, recalculating gross, discount, tax and net. Order Cancellation withdraws an order entirely with a cancellation reason. Both exist before the GIN (seq 15/16) and again after the GIN (seq 29/31), where the business rule is different because stock has been issued. [inferred]
- Live 2026-10-01: before the GIN, cancellation releases the order's reserved stock. After an approved GIN both editing and cancellation are still allowed, with no warning, and **move no stock**: the goods are with the delivery man and come back through the Goods Return Note. [observed 2026-10-01 G11-1; GRN return observed on the GRN page]

## 2. Actors and roles
Auto_Multi_Orga. [observed in group 11] Whether a checker must approve edits: [unknown] (no approval flow in the chain).
- Maker = Auto_Multi_Orga edits (seq 29) and cancels (seq 16, 31). [observed 2026-10-01 G11-1]
- Checker: no approval step; an edit and a cancellation take effect on the Maker's Save / Cancel All. (upgraded: [observed 2026-10-01 G11-1], was [unknown])

## 3. Documents and master data
Acts on the order cash memo; a successful edit produces `ORDERNUMBEREDIT` repo (an Order Number shown after edit; whether it is a new number or the same: [unknown]). Reasons come from master data: Reason Type (e.g. "Order Change QTY") and Cancellation Reason (e.g. "Shop Closed") [observed in step sheet draft; list [unknown]]. Statuses: Cancelled 03 [db].
- **An edit keeps the same Document No** (COL26000002003 after the edit). (upgraded: [observed 2026-10-01 G11-1], was [unknown])
- **Reason Type options on the edit screen**: Order Change QTY, Wrong Order /No Order, No Scheme, Stock Already Avl. (upgraded: [observed 2026-10-01 G11-1], was [unknown])
- **Cancellation Reason options**: Bad Weather, Credit Exceeded, Law & order Issue, Shop Closed. (upgraded: [observed 2026-10-01 G11-1], was [unknown])
- Cancelled orders show "Cancelled" in Transaction Inquiry. [observed 2026-10-01 G11-1]

## 4. Inputs: screens and fields
**Order Editing** (`/ngui/order-editing`, id ORDER_EDITING): PJP, Selling category, section (dropdowns), Start Date, End Date (date range), Outlet Name; result grid Document No, Document Date, Delivery Date, Outlet, Demand Channel, Gross Amount, Discount, Tax, Net Amount, Balance Amount, Received Amount; click Document No to open. [atlas/step_labels]
- Live 2026-10-01: menu Transaction > Order Editing (search "Order Editing"; an "Order Editing HQ" option also exists). Filters: PJP (opens preselected with the FIRST PJP AUTO241602~Auto917248, with Selling Category and Section filled), Selling Category, Section, Outlet Name, **Date From / Date To (default today)**, SKU. Labels: PJP "02111~AutomationOB1", Selling Category "201-Selling Category 001", Section "101010101101-Automation_Testing_Section". Changing the PJP clears Selling Category, Section and Outlet (cascade). After the cascade Section, Outlet and **SKU** fill with their first value. [observed 2026-10-01 G11-1]
- **Date From / Date To filter the order's DELIVERY date**, not the order date. [observed 2026-10-01 G11-1]
- Order grid columns (live): Document No, Document Date, Delivery Date, Outlet, Gross, Discount, Tax, Net, **Received Amount, Balance Amount**, Demand Channel. [observed 2026-10-01 G11-1]
**Order Editing Detail**: per line OrderCS, OrderPC, Reason Type, Gross Amount; line Edit/Save/Cancel (`rowEditBtn_*`), Validation (`validateBtn`), Save (`saveBtn`), `OrderEditingBtn`. **Detail3**: Gross, Discount, Tax, Net, Order Number. [atlas]
- Live 2026-10-01: clicking the Document No opens the edit page with ALL lines of the order (the SKU filter does not limit the edit): Product Desc, Product Code, Batch, Current Stock, Price Value, **Demand** CS/DZ/PC (read-only, as booked), **Order** CS/DZ/PC (editable; DZ read-only), Gross Amount, **Reason Type**, Edit per line. After Save the summary "Order View - Header" shows the same Document No, Demand (unchanged) and Order (edited). [observed 2026-10-01 G11-1]
**Order Cancellation** (option DYL_202022): PJP (mandatory), Section, Outlet Name, Date To; grid with checkbox per order (`row_1_checkbox_1`), Cancellation Reason (dropdown per row), Net Amount; buttons Refresh, Cancel All, Cancel (`cancelBtn`), Close. [atlas]
- Live 2026-10-01: menu Transaction > Order Cancellation (layout 202022). Opens with PJP* 02111 - AutomationOB1 preselected, **Date From* / Date To* = today, filtering the ORDER (document) date**; Section preselected; Outlet Name preselected with the first outlet that has an open order. **The Outlet list holds only outlets with open (cancellable) orders.** Grid: checkbox, Document No., Document Date, Delivery Date, Net Amount, Outlet Name, Demand Channel, **Cancellation Reason** (in-grid dropdown). Buttons: **Cancel All**, Refresh. [observed 2026-10-01 G11-1]
- Result window **"Order Cancellation Status"** with columns Index No, Doc No, Status, Message. [observed 2026-10-01 G11-1]

## 5. Process: the business steps in order
1. [Maker] Navigate to Order Editing; Choose PJP (category, section fill in); Choose Outlet Name; set date range to include the order. (`11:15:00020001`) (2026-10-01: the date range must include the order's DELIVERY date. [observed 2026-10-01 G11-1])
2. Open the order; edit line 1 (62740537): OrderCS = 4, OrderPC = 0, Reason Type = "Order Change QTY"; save the line; Validation; Save. Expected summary (workbook): Gross 96,840.34, Discount -20,718.07, Tax 14,584.79, Net 90,707.00. [draft step sheet; not executed] (seq 15 skipped 2026-10-01 by the QA lead for QA/BA discussion; the same edit was executed after the GIN in seq 29 and gave these totals exactly. [observed 2026-10-01 G11-1]) (`11:15:00020001`)
3. [Maker] Navigate to Order Cancellation; Choose PJP; find outlet 1000000007 (order COL26000002001); select it; Cancellation Reason = "Shop Closed"; Cancel. Expected message "Order Cancelled Successfully" [unverified draft text]. (`11:16:00040001`) (upgraded: message [observed 2026-10-01 G11-1], see step 6.)
4. After GIN: same screens with workbook NG_Dcode_QA_OTC_AfterGIN (seq 29, 31). Expected behaviour (allowed or refused): [unknown]. (superseded 2026-10-01: both are allowed, see steps 7-8. [observed 2026-10-01 G11-1])
5. Validate in Transaction Inquiry after edit (seq 70, 68). See transaction_inquiry.md.
6. [Maker] Navigate to Order Cancellation; Verify PJP 02111 - AutomationOB1 and Date From/To = today (order date); Choose Outlet Name (QA lead chose 1000000011); Choose Cancellation Reason = Shop Closed in the order's row; Select the row checkbox; Click Cancel All -> "Order Cancellation Status": COL26000002008 | Successfull | Order Cancelled Successfully; Close the window; the order leaves the list. [observed 2026-10-01 G11-1] (`11:16:00040001`)
7. [Maker] Navigate to Order Editing; Choose PJP 02111~AutomationOB1; Choose Selling Category 201-Selling Category 001 (re-select after the cascade); Verify Date From/To cover the delivery date (today, after Delivery Date Change); Choose Outlet Name 1000000004; Open Document No COL26000002003; Edit line 62740537 Order 7/0/0 -> 4/0/0 with Reason Type = Order Change QTY; Save the line (no message); Click Validation -> "Validation successfully"; Click Save -> "Order Save successfully". [observed 2026-10-01 G11-1] (`11:29:00840001`)
8. [Maker] Navigate to Order Cancellation (after the GIN); Choose Outlet Name 1000000006; Choose Cancellation Reason = Shop Closed for COL26000002007; Select the row (scroll the checkbox cell into view); Click Cancel All -> "Order Cancellation Status": COL26000002007 | Successfull | Order Cancelled Successfully. [observed 2026-10-01 G11-1] (`11:31:00850001`)

## 6. Outputs and effects
Edit: new amounts on the order, reason recorded; tax/charges recomputed (seq 68 checks Charges Amount and Tax Amount after editing). Cancellation: order status Cancelled 03 [db]; stock effect (release of allocation): [inferred], not observed. Neither step has been executed live. (superseded 2026-10-01: both executed live, effects below. [observed 2026-10-01 G11-1])
- **Edit after the GIN (COL26000002003)**: new totals **Gross 96,840.34, Discount -20,718.07, Tax 14,584.79, Net 90,707.00 = workbook Order Editing Detail3 exactly**; promotions are re-applied on the smaller basket (line 1 discount -13,198.30); Demand stays 5/0/4, Order 4/0/0; same Document No. [observed 2026-10-01 G11-1]
- **Edit after the GIN: no stock effect**: 62740537 at Auto Main still Out 35, Allocated 63, Closing 226. The 3 CS cut are with the delivery man and come back on the GRN (seq 48 suggested 19 CS = 7 + 7 + 3 + 2, including this 3). [observed 2026-10-01 G11-1]
- The edited Net shows elsewhere: Order Cancellation lists COL26000002003 with Net 90,707; Cashmemo Status shows 90,707.06 (line sum). [observed 2026-10-01 G11-1]
- **Cancellation before the GIN (COL26000002008)**: status Cancelled; Delivery Date stays 2026-10-07; no GIN. **Reserved stock is released**: 62740537 Allocated rose only by 5 open orders x 7 CS (63 -> 98) and Closing went 261 -> 226; the cancelled order's 7 CS returned to available stock. (stock release upgraded: [observed 2026-10-01 G11-1], was [inferred])
- **Cancellation after the GIN (COL26000002007)**: status Cancelled, GIN No 506 kept, Delivery Date 2026-10-01. **No stock effect** (62740537 Out 35 / Allocated 63 / Closing 226 unchanged, same for all five SKUs); the 7 CS remain "out" with the delivery man until the GRN (seq 48 returned them). It is left off the Cashmemo Status list and the Route Settlement order count. [observed 2026-10-01 G11-1]

## 7. Statuses and transitions
| from | action | to | by | tag |
|---|---|---|---|---|
| Ordered | Edit + Save | Ordered (amended amounts) | Maker | [inferred] |
| Ordered | Cancel | Cancelled (03) | Maker | [db]; upgraded [observed 2026-10-01 G11-1] (was [db]): COL26000002008 Confirmed -> Cancelled |
| Delivered / on GIN | Edit or Cancel | [unknown] | | [unknown] (superseded 2026-10-01, rows below) |
| Ready to dispatch/Packed (on approved GIN) | Edit + Save | Ready to dispatch/Packed, amended amounts, same Document No; later Delivered/Invoiced | Maker | [observed 2026-10-01 G11-1] |
| Ready to dispatch/Packed (on approved GIN) | Cancel All | Cancelled, GIN No kept | Maker | [observed 2026-10-01 G11-1] |

## 8. Rules and validations
- Outlet Name list is EMPTY for orders that show as Allocated (outlet API `getOultetsForOrderEditing` returned [] for PJP/section/category; a wide range returned older outlets). Correlation with allocation observed, not proven; alternative suspect: date range filters on delivery date (orders had 2026-10-05). [observed/inferred] (superseded 2026-10-01: the cause is the date range, which filters the DELIVERY date; allocation does not hide orders. With the default range (today) an order booked today for delivery 2026-10-07 can never appear; after Delivery Date Change to today the same allocated orders were listed. [observed 2026-10-01 G11-1])
- Date fields must be typed with key events (DOM value ignored; request carried today). [observed] Live 2026-10-01: on Order Cancellation Refresh returned "Required parameter 'toDate' is not present." when Date To was typed (even with Tab/Enter); it worked only after picking the date from the calendar popup, so **typed dates are not always committed: use the calendar popup** [observed].
- Live 2026-10-01: the reason control exists only INSIDE a data-grid row (Order Cancellation grid column "Cancellation Reason"; Cashmemo Reschedule grid "Reschedule Reason"; Order Editing has no reason column until an order is opened). No order was eligible (all 24 orders Planning completed / Cancelled / Delivered), so the grids were empty and the dropdowns could not be opened (Order Editing PJP 02111, 2026-09-29..30: 0 rows; Order Cancellation PJP 02111, 2026-09-29..10-05: 0 rows) [observed]. (Later 2026-10-01 with same-day orders the dropdowns were opened; options in section 3. [observed 2026-10-01 G11-1])
- Reason lists [db, glb_pr_rnt_reason_type, org 010104, CM-01]: Order Editing Reason Type (identifier ORC, inferred): 0008 Order Change, 0009 Order Change QTY, 0010 Change Utlity (sic), 0020 Bogus order, 1001 testDesc, L01L01L01 and L01L01L01L01 Wrong Order/No Order, L02L04L07 and L02L04L07L01 No Scheme, L02L06L09L03 Stock Out, L0L1L1 and L0L1L1L1 Stock Already Avl. Cancellation reasons (identifier CNL; layout 202022 panel 3 is hand-coded so the use of this list is inferred): 0017 Shop Closed, 0018 Delivery is not possible due to any reason, 0019 Customer cancels delivery, 0021 customer refused, L02L01L01L01 Credit Exceeded, L02L02L03L01 Shop Closed, L02L03L04L01 Bad Weather, L02L03L04L02 Law & order Issue. Lists contain duplicates and test entries. (Live dropdowns 2026-10-01 show a subset: Reason Type 4 entries, Cancellation Reason 4 entries, no duplicates; see section 3. [observed 2026-10-01 G11-1])
- PJP is mandatory on Order Cancellation. [atlas] (Shown with * on screen. [observed 2026-10-01 G11-1])
- Cancellation needs a reason per order row. [atlas]
- Order edit must be validated before save (ORD_EDIT_VALD_ASSR then ORD_EDIT_SAVE_ASSR). [atlas] (upgraded: [observed 2026-10-01 G11-1]: Validation is followed by Save.)
- **Order Cancellation dates filter the ORDER date; Order Editing dates filter the DELIVERY date.** [observed 2026-10-01 G11-1]
- **Editing and cancelling are allowed after the GIN is approved, with no warning**, and move no stock. [observed 2026-10-01 G11-1; business control question Q-OE3]
- Orders on an approved GIN (Ready to dispatch/Packed) are still offered for cancellation. [observed 2026-10-01 G11-1]
- The SKU filter on Order Editing does not limit the edit page (all lines are shown). [observed 2026-10-01 G11-1]
- **Display defect**: with the auto-filled SKU filter (69997598) the Order Editing grid shows Gross of that SKU only (76.72) beside the whole-order Discount -29,971.83 and Tax 21,234.24, giving **Net -8,660.87**. [observed 2026-10-01 G11-1]
- The PJP dropdown selection on Order Editing is fragile: once the screen showed 02111~AutomationOB1 while the request used the next PJP (AUTO031026), after which the cascade blanked all filters. [observed 2026-10-01 G11-1]
- Demand (as booked) is read-only; only Order CS/PC are editable; DZ is read-only. [observed 2026-10-01 G11-1]

## 9. Messages
Observed: none (flows not reachable). Framework keys: ORD_EDIT_VALD_ASSR, ORD_EDIT_SAVE_ASSR, row message ELEVAL on the cancellation row, TSTMSG. Draft: "Order Cancelled Successfully" [unverified]. (superseded 2026-10-01: messages observed below.)
- Edit: line Save gives no message; **"Validation successfully"** (Validation); **"Order Save successfully"** (Save). [observed 2026-10-01 G11-1]
- Cancellation: no toast; result window **"Order Cancellation Status"** row: Doc No | Status **"Successfull"** (sic) | Message **"Order Cancelled Successfully"**. (upgraded: [observed 2026-10-01 G11-1], was [unverified])
- Order Cancellation Refresh with an uncommitted typed Date To: "Required parameter 'toDate' is not present." [observed 2026-10-01]

## 10. Dependencies
Needs an order from Order Booking (order 04 for editing, order 07 for cancellation) in an editable (probably Unallocated) state. Hands edited totals to Transaction Inquiry validation and to GIN. (superseded 2026-10-01: the order does not need to be unallocated; for Order Editing its delivery date must fall in the Date From/To range, normally after Delivery Date Change. [observed 2026-10-01 G11-1])
- After the GIN, cut and cancelled quantities are handed to the Goods Return Note (Suggested quantity). [observed 2026-10-01 G11-1]
- Workbook outlets 1000000001-03 are not offered on cnr1dev1, so the workbook's edit/cancel targets need substitutes (QA lead chose COL26000002008 for seq 16 instead of outlet 1000000007's order, and COL26000002003 for the edit). [observed 2026-10-01 G11-1]

## 11. Test design hints
- Positive: edit one line quantity down, check totals recalc and status; cancel one order with reason; verify Transaction Inquiry shows Cancelled.
- Negative: edit with no reason; quantity to zero for all lines; cancel without reason; cancel an order already on a GIN; edit after GIN.
- Boundary: quantity up by one case beyond stock; OrderPC larger than the pack size.
- Traps: green run with an empty outlet list asserts nothing; allocation state decides visibility, so state the order's allocation as precondition (unallocate first, if Unallocate worked). (superseded 2026-10-01: visibility is decided by the delivery-date range, not allocation, see below.)
- New 2026-10-01 [observed 2026-10-01 G11-1]:
  - **Delivery-date filter**: Order Editing Date From/To filter the delivery date. Positive: order booked today for delivery 10-07 appears only when Date To >= 10-07 (or after Delivery Date Change to today). Negative: default range (today) shows no outlet for a future-delivery order. Contrast Order Cancellation, which filters the order date.
  - **After-GIN control**: edit and cancel an order on an approved GIN; assert there is NO warning today (record as a business question, not a pass), the totals change, Transaction Inquiry status (still Ready to dispatch/Packed for the edit, Cancelled with GIN No kept for the cancel), and **no stock movement** (Out / Allocated / Closing unchanged); then assert the GRN Suggested quantity includes the cut and cancelled quantities.
  - **Before-GIN cancel stock effect**: Stock Inquiry Allocated -order qty and Closing +order qty after cancellation.
  - **SKU-filter defect**: on Order Editing with an SKU auto-filled, the grid Net is negative (Gross of one SKU vs whole-order Discount/Tax, -8,660.87). Assert grid Net = Order View Net; expect it to fail until fixed.
  - **Cancellation result window**: assert the Message "Order Cancelled Successfully"; the Status column reads "Successfull" (typo) and there is no toast, so a toast assertion has nothing to read.
  - Edit keeps the Document No; assert Demand unchanged and Order = new quantity; assert promotions re-applied (discount not pro rata of the old %).
  - Trap: the SKU filter auto-fills with the first SKU; it does not limit the edit page but it does change the grid totals.
  - Trap: re-select Selling Category after choosing the PJP (the cascade clears it); verify the PJP actually applied (the display can differ from what was used).

## 12. Open questions (batched for the BA)
- Q: How does an allocated order reach Order Editing / Cancellation (unallocate first? delivery-date range?) | Default: unallocate first, range covers delivery date | Evidence: outlet list empty. **ANSWERED 2026-10-01 G11-1**: by the delivery-date range; Order Editing Date From/To filter the delivery date, allocation does not hide orders (the empty list of 2026-09-29 was a default range of today vs delivery 10-05). [observed]
- Q: Are edits/cancellations after GIN allowed and what do they do to stock and the GIN? | Default: refused with a message | Evidence: unexecuted. (PARTLY ANSWERED 2026-10-01 G11-1: allowed with no warning; no stock movement; cancelled order keeps the GIN No; quantities return on the GRN [observed]. Whether this is intended is Q-OE3.)
- Q: Does an edit keep the same Order Number? | Default: same number | Evidence: ORDERNUMBEREDIT repo suggests possibly new. **ANSWERED 2026-10-01 G11-1**: same Document No (COL26000002003). [observed]
- Q: Allowed reason lists? | Default: use workbook reasons | Evidence: lists db-declared 2026-10-01 (PARTLY answered, Q22); real dropdowns not yet opened (needs an order in Ordered/Confirmed status). (ANSWERED 2026-10-01 G11-1: dropdowns opened, options in section 3 [observed].)
- Q-OE1: Is the Order Editing date range meant to be the delivery date, and should the default be the PJP's next delivery date rather than today? | Default: treat as delivery date | Class: C | Evidence: session log seq 15, report §8.
- Q-OE2: Which order should seq 15 edit when workbook outlets 1000000001-03 are not offered on cnr1dev1? | Default: outlet 1000000004's order | Class: C | Evidence: session log seq 15, report §8.
- Q-OE3: Should editing / cancelling an order on an approved GIN be blocked or warned (business control)? | Default: allowed (as observed); record as defect candidate | Class: C | Evidence: seq 29, 31; report §6 item 3.
- Q-OB1: Who or what generated the day's opening balances during 2026-10-01? It decides the stock figures the before/after checks of a cancellation start from. | Default: unknown | Class: B | Evidence: report §8.

## 13. Sources
atlas flows 00020001, 00040001, 00840001, 00850001, 03190001, 03740001; group_11.md; STEP_SHEET_DRAFT_next.md (rows 15, 16); ui.md "Order Editing / Order Cancellation"; step_labels "Order Editing", "Order Cancellation".
- Live learning session G11-1 (2026-10-01, cnr1dev1, distributor 15108843): `learning_sessions/2026-10-01_G11-PK_session1_log.md` seq 15 (skipped, filter finding), 16, 29, 31, 48 (GRN reconciliation); `learning_sessions/2026-10-01_G11-PK_session1_report.md` §3 rules 7 and 11, §6, §8.
