# Order Booking: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]** seen live in a replay or recording, **[db]** declared by the application DB or the framework tables, **[inferred]** concluded by Claude from names or structure (to be confirmed), **[unknown]** not determinable yet.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 00010001 (group 11 seq 10; also groups 1, 52).

## 1. Purpose
Order Booking captures a retail outlet's demand for products (an order) on behalf of a distributor, usually entered by an Order Booker or Spot Seller [inferred from the field "Order Booker/Spot Seller"]. The order is stored as a cash memo document and is later picked, issued on a Goods Issue Note and delivered [db: order is the cash memo master `snd_tr_cmm_cashmemo_master`, status "Ordered"]. In the Daily Cycle it comes after the stock has been received (Dispatch Advice, approval, stock validation) and before Stock Allocation, Transaction Inquiry, editing/cancellation, Delivery Date Change and the GIN. [observed: group 11 chain]

## 2. Actors and roles
- Order user = **Auto_Multi_Orga** (framework login serial 35) on cnr1dev1; same session as the stock validation before it. [observed: TC-OB-01_executed.md]
- No approval step exists for an order. [observed: none in chain]

## 3. Documents and master data
- Document: cash memo (order). Number shown as **Order Number** on the summary screen, format `COL` + 2-digit year + 9 digits, e.g. COL26000001995 .. COL26000002002 (8 orders, sequential). [observed]
- Document type of the saved order: Sales `CM-01` (status Ordered 04) [db]; Transaction Inquiry lists it under type "Sales" [observed]. The demand type "Demand Captured from Tele order" (type `2`, status PLACED 88) is a different document used for tele-orders [db][inferred].
- Master data used: Order Booker/Spot Seller, PJP (e.g. 02111-AutomationOB1), Selling Category (Selling Category 001, shown later as 201-Selling Category 001), Section (Automation_Testing_Section), Outlet (1000000001-Aautomation_Outlet_01 .. 08), products by code (62740537, 20050310, 62690363, 20050308, 69997598), price list / trade price, stock (ATP). [observed]
- The 8 workbook outlets differ in tax treatment (tax exempt / registration flags are in the outlet name); tax is 0 for outlets 05 and 06. [observed: ob_orders.json; reason inferred]

## 4. Inputs: screens and fields
Menu: type "Order Booking", option `ORDER_BOOKING`; real path Transaction > Order > Order Booking. [db: mg 0001]
**Order Booking (header)**: Order Booker/Spot Seller (dropdown), PJP (dropdown), Selling Category (dropdown), Section (dropdown), Outlet Name (dropdown), Comments (text), Document Date, Reference Number (optional, framework field inactive). Dropdowns cascade in this order; category and section fill by themselves after PJP. [observed]
**Order Detail** (after the `Order Detail` button): ProductDesc (type-ahead autoselect on product code/name), OrderCS (cases), OrderPC (pieces), read-only Trade Price, Gross Amount per line, ATP shown per product; buttons Add a row (`addBtn`), line Save (`rowEditBtn_Save_0`), Validation (`validateBtn`), Save (`saveBtn`), New Order (`newOrder`, confirm `continue`). [observed]
**Order summary (Detail2)**: Gross Amount, Discount, Tax, Net Amount, Order Number (all read-only). [observed]
Mandatory fields: header fields block by **progressive disclosure, not by messages**: there is NO Validation button and no header message at all; the **Order Detail** button (id orderDetail) appears only after the Outlet is chosen; clearing Section, Selling Category or PJP (clear icon) clears every field below it and with Outlet empty there is no Order Detail button and no toast [observed 2026-10-01]. Validation (`validateBtn`) and Save appear only on the detail step after a product line exists. Default Document Date = today [inferred].
Live cascade 2026-10-01: PJP AutoPromo1-Auto Promo PJP OB -> Selling Category AutoPromoSCG -> Section Auto Promo Section -> 15 outlets (Aautomation_Outlet_21..36); PJP 02111-AutomationOB1 offers Selling Category 001 only (no label with 201) and its outlet list starts at 1000000004 (1000000001 is not offered) [observed]. Order Detail opens /ngui/order-booking/order-fillter; header locked; New Order -> "Are You sure you want to cancel the order" Yes (id continue, resets the header) / No (id reject); the detail grid starts with an insert row (product type-ahead id product, batch, CS/DZ/PC order, row Save/Cancel); after cancelling an unsaved row the grid add-row icon (.dx-icon-edit-button-addrow) is needed for a new insert row [observed].

## 5. Process: the business steps in order
1. [Order User] Navigate to Order Booking. (`11:10:00010001:000101`)
2. [Order User] Choose Order Booker/Spot Seller = Order Booker; PJP; Selling Category; Section; Outlet Name; Enter Comments. The header becomes read-only after Order Detail is clicked. [observed]
3. [Order User] Click Order Detail; per product enter code, OrderCS, OrderPC; save the line (no toast on line save). [observed] **The product pick checks stock of the current day**: a product with no stock row for today gives the toast "Stock not available." and the row stays empty (20050310 on 2026-10-01, and every product before DA 1356 was approved); a product with stock fills the row: Batch 1-1, Current Stock (ATP) = Stock Inquiry closing (62740537: 4/0/0 CS/DZ/PC), Trade Price/Unit 7711.465, order quantity inputs 0, row Save/Cancel [observed 2026-10-01, nothing saved].
4. [Order User] Click Validation -> toast "Validation successfully"; a Save button appears. [observed]
5. [Order User] Click Save -> toast "Order Save successfully"; Order Number and totals shown. [observed]
6. [Order User] New Order (confirm "Are You sure you want to cancel the order": Yes) to start another. [observed]

## 6. Outputs and effects
- A cash memo with an Order Number, document status Ordered (04), execution status 02 "Confirmed" after booking and allocation, 03 "Planning completed" once it is on a GIN (the 8 orders on GIN 505 show "Planning completed" on 2026-10-01) [db + observed]. Delivery Date on the order = 2026-10-05 (copied from the PJP's next visit date, [inferred]; cancelled orders 1986 and 1993 still show 10-05, the 8 target orders show 2026-09-30 after Delivery Date Change [observed 2026-10-01]); Section 101010101101-Automation_Test..., Selling Category 201. [observed]
- Stock is **auto-allocated at save** (Allocation Status FULL); allocated orders appear in the Allocated tab of Order Stock Allocation. [observed]
- Pieces are converted into cases: 5 CS + 4 PC became 7 CS (2 PC per case for that product). [observed]
- Totals (workbook = observed): order 01 Gross 143,109.13, Discount -29,971.83, Tax 21,861.52, Net 134,999.00. Net = Gross + Discount + Tax (143,109.13 - 29,971.83 + 21,861.52 = 134,999.00). [observed]
- ATP per product equals the Stock Inquiry closing balance, so orders draw on stock received by the Dispatch Advice. [observed; live-verified 2026-10-01: ATP 4 CS for 62740537 = Closing 4 CS after DA 1356 was approved]

## 7. Statuses and transitions
| from | action | to | by | tag |
|---|---|---|---|---|
| (none) | Validation + Save | Ordered (04) / shown "Confirmed" | Order user | [db][observed] |
| Ordered | Order Cancellation | Cancelled (03) | Order user | [db] |
| Ordered | GIN approval + delivery | Delivered (01) | later areas | [db] |
Details in order_lifecycle_and_statuses.md.

## 8. Rules and validations
- Validation must succeed before Save is offered. [observed]
- Reference Number must be unique per distributor: a repeat gives the duplicate message. [observed: ref 100]
- Header is locked after Order Detail; to change it, New Order discards the lines. [observed]
- Gross is recalculated when quantities change (change event + blur). [observed]
- Tax differs by outlet tax status. [observed]
- A product without a stock row for the day cannot be picked: "Stock not available." [observed 2026-10-01]. Quantity above available stock (ATP) is allowed or blocked: [unknown, not tried].

## 9. Messages
- "Validation successfully" (validate); "Order Save successfully" (save; framework key ORD_BOOK_SAVE_ASSR). [observed]
- "Stock not available." (dx-toast-error, on product pick when the product has no stock row for the day) [observed 2026-10-01]; confirm dialog "Are You sure you want to cancel the order" (New Order) [observed].
- "Cashmemo with document reference number : 100 already exist." (duplicate Reference Number; atlas history also shows "Cashmemo Document Reference Number: 01 already exist."). [observed]

## 10. Dependencies
Reads: stock from Dispatch Advice (same calendar day; stock balances are keyed by date), repos `g_REPO_ORGA`, `g_REPO_CMDOCTYPE`, `g_REPO_DISTRIBUTOR`, `REPO_REF_ORDER_NO`. Writes repo `ORDERNUMBER` used by Order Editing (seq 15, 29), GIN selection. Hands to: Stock Allocation, Transaction Inquiry, Order Editing/Cancellation, Delivery Date Change, GIN (see delivery area, by name).

## 11. Test design hints
- Positive: book one order with 5 products; check Gross/Discount/Tax/Net equal the workbook; check Order Number format; check ATP drops after save [inferred].
- Positive: pieces beyond a case (PC > pack size) convert to cases.
- Negative: duplicate Reference Number; Save without Validation; no lines; zero quantity line; unknown product; header changed after Order Detail.
- Boundary: quantity = ATP and ATP + 1; CS 0 / PC 0 only; very large PC.
- Business effect: order is already Allocated after save; status Confirmed in Transaction Inquiry.
- Traps: line save has no toast so a TSTMSG assertion has nothing to assert; workbook Reference Number 100 collides on a second run; a green run proves the toast, not the stock effect.

## 12. Open questions (batched for the BA)
- Q: Is quantity above ATP blocked, warned, or accepted as a backorder? | Default: blocked | Evidence: never tried.
- Q: What decides the order Delivery Date (PJP next visit)? | Default: next PJP visit date | Evidence: 2026-10-05 seen, rule not shown.
- Q: Which fields are mandatory? | Default: all dropdowns except Comments and Reference Number | Evidence: header fields work by progressive disclosure (PARTLY answered 2026-10-01, Q18); the Validation messages of the detail step are still unread.
- ANSWERED 2026-10-01: which stock makes a product orderable = stock received by an approved DA for the current day; ATP = Closing today (net of allocation).

## 13. Sources
learning_block2a.json (L14), learning_block3b.json (S3), LIVE_FINDINGS.md; framework_atlas/flows/00010001.md/.json; group_11.md; framework_flows/TC-OB-01_executed.md, ob_orders.json; DB `snd_tr_cmm_cashmemo_master`, `snd_pr_dot_documenttype`, `snd_pr_dos_documentstatus` (org 010104); step_labels (qaos_steps.py labels "Order Booking").
