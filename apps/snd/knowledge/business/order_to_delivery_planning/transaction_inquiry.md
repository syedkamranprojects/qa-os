# Transaction Inquiry (order validation): how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 02960001 (seq 14, after order booking), 03740001 (seq 70, after editing), 03190001 (seq 68, edited-order charges/tax); sales-return variants 03200001/03770001 belong to the delivery/returns analyst.

## 1. Purpose
A read-only inquiry over all transaction documents (orders, sales, returns...). In this area it is the cross-check that what Order Booking/Editing saved matches the expected Gross, Discount, Tax and Net, and shows each document's status. [observed]

## 2. Actors and roles
Auto_Multi_Orga. [observed]

## 3. Documents and master data
Reads cash memos (`snd_tr_cmm_cashmemo_master` and children detail/offering/charges [db]). Document types and statuses from `snd_pr_dot_documenttype` / `snd_pr_dos_documentstatus`.

## 4. Inputs: screens and fields
Menu Transaction Inquiry, option DYL_102014. Filters: **Document Type** (default "Demand Captured from Tele order"; choose **Sales**), **Document Status** (All), **Document Date From/To**, Date Type, PJP, Product/SKU; grid filter row on Outlet Code / Document No. Grid columns include Document No, Document Status, Execution Status, Gross Amount, Discount Amount, Tax Amount, Net Amount, Outlet Code, PJP Number, GIN No, Delivery Date, Actual Delivery Date, Invoice No, DDT Ref No. Live-verified 2026-10-01 (Block 1): Document Type options (17): Demand Captured from Tele order (default), OFF INVOICE CREDIT NOTE, DSR Shortage Amount, Amount Wise, Dsr Adj (SKU Wise), Sales, Sales Return, Fresh Sales Return, B2B Sale, Sales return without reference, Customer Account Close, Credit Note, Credit Note (Sales Return), Credit Note (Fresh Return), Credit Note (Sales Return W/O Ref), Off Invocie Credit Note (sic), Return Request. Document Status filter: All, CM-01 - Ordered / Confirmed / Planning completed / Cancelled / Delivered/Invoiced / Dispatched / Sent to Locus / Ready to dispatch/Packed / Reattempt / Out for delivery. Filters PJP Number, Document Date From/To (typed with Tab), SKU. The grid has 19 columns: Document No, Outlet Code, Outlet Long Name, Order Booker/Delivery Man, PJP Number, Order Time, Document Date, Delivery Date, Actual Delivery Date, Gross Amount, Discount Amount, Tax Amount, Offset Amount, Net Amount, Document Status, Demand Channel, DDT Ref No, GIN No, Invoice Ref. No; there is NO separate Execution Status column (Document Status shows the execution status text) and NO Delivery-PJP column (PJP Number is the order booker PJP 02111; the delivery PJP 02112 is visible on the GIN only); 5 rows per page. Row buttons: Detail, Product Wise Discount, Product Wise Free Quantity, Total Offering, Total Tax, Credit Note Adjustments (Product Wise* disabled until a row with that data is chosen) [observed].
Tabs/buttons: Detail, Product Wise Discount, Product Wise Free Quantity, Total Offering, Total Tax, Additional Charges, Credit Note Adjustments. [observed/step_labels]
Framework reads: header (Gross, Discount, Tax, Net), Detail tab (per line, incl. allocated CS column), Total Offering (Discount, Tax Amount), Charges (Charges Amount). [atlas]

## 5. Process: the business steps in order
1. [Order User] Navigate to Transaction Inquiry. (`11:14:02960001`)
2. Choose Document Type = Sales, Document Status All, dates today; Refresh -> 24 Sales documents. [observed]
3. Filter Document No "COL26000" (or Outlet Code "Auto"); open the order row.
4. Verify header amounts: outlet 1000000006 (COL26000002000) Gross 143,109.13, Discount -29,971.83, Tax 0, Net 113,137 = workbook; orders 04/05/07/08 net 134,372 / 113,137 / 134,535 / 108,202. [observed]
5. Verify the Document Status text. Right after booking the earlier run read "Confirmed"; on 2026-10-01 the same orders read **Planning completed** because they are on GIN 505 [observed]. Live baseline 2026-10-01 (Sales, 2026-09-29 to 09-30: 24 rows): the 8 target orders COL26000001995-2002 all have Document Date 2026-09-29, Delivery Date 2026-09-30, Actual Delivery Date empty, PJP 02111, Order Booker AutomationOB/AutomationQADSR, Demand Channel Back Office (BO), GIN No 505, Invoice Ref empty, Offset 0; amounts (Gross / Discount / Tax / Net): 1995 143,109.13 / -29,971.83 / 21,861.52 / 134,999; 1996 .../21,234.24/134,372; 1997 .../21,992.03/135,129; 1998 .../21,234.24/134,372; 1999 and 2000 tax 0 / 113,137; 2001 tax 21,397.32 / 134,535; 2002 107,960.51 / -16,264.08 / 16,505.36 / 108,202 [observed]. Other documents in the range: Cancelled 1979-1986, 1993, 1994; Delivered/Invoiced 1987, 1989-1992 (GIN 504, actual delivery 2026-09-29); 1988 also on GIN 505 (so GIN 505 holds 9 cash memos) [observed].
6. Not run live: Detail, Total Offering, Charges tab checks; after editing (seq 70, 68) the same checks on the edited order. [unknown results]

## 6. Outputs and effects
None (inquiry only).

## 7. Statuses and transitions
Shows statuses; changes none. Observed status after booking: Confirmed [observed]; DB description for CM-01 04 is Ordered. See order_lifecycle_and_statuses.md.

## 8. Rules and validations
- The default Document Type hides booked orders (they are Sales, not Demand Captured). [observed]
- Totals must equal Order Booking summary and the workbook. [observed]
- Net = Gross + Discount + Tax rounded to whole PKR (143,109.13 - 29,971.83 + 21,861.52 = 134,998.82 shown 134,999); Net is integer, Gross/Discount/Tax keep 2 decimals [observed 2026-10-01].
- **Total Offering sums equal the header Discount** (1995-2001: Automation2 BONUS2 -14,310.91, MARCH001 BONUS2 -650, MARCH002 TRADEOFFER -14,310.91, May001 BONUS2 -650, May003 BONUS2 -50 = -29,971.82 vs header -29,971.83, a 1 paisa rounding; 2002: -5,398.03, -10, -10,796.05, -10, -50 = -16,264.08 = header exactly); tax is 0 on every promo line [observed 2026-10-01].
- Tax is 0 for tax-exempt outlets. [observed]
- Date filters default to today; orders of other days need the range widened. [inferred]

## 9. Messages
None observed; assertions are value comparisons (TSTMSG with screenshot_ASSR group).

## 10. Dependencies
Reads orders (seq 10), edited orders (seq 15), later sales returns and GIN numbers. Hands nothing.

## 11. Test design hints
- Positive: for each booked order compare 4 amounts to the Order Booking summary; check status; check Detail line sums equal header; Total Offering discount equals header discount.
- Negative: wrong Document Type shows no row; status filter excludes the order.
- Boundary: order on the first/last day of the date range; 24-row list with filter on one outlet.
- Traps: header amounts are checked for the first row of the filtered grid; if filter order changes the wrong order is compared. Only the header check was run live.

## 12. Open questions (batched for the BA)
- ANSWERED 2026-10-01 (Q23): "Confirmed" is execution status 02 (separate from Ordered 04); the column shows execution status text.
- ANSWERED 2026-10-01 (Q28): Total Offering Discount sum equals the header Discount (within 1 paisa rounding) on all 8 orders.
- Surprise: orders 1993 and 1986 are Cancelled but still show Delivery Date 2026-10-05 [observed].

## 13. Sources
learning_block1.json (L03), LIVE_FINDINGS.md; atlas flows 02960001, 03740001, 03190001; TC-OB-01_executed.md (TC-OB-03); step_labels "Transaction Inquiry"; DB tables above.
