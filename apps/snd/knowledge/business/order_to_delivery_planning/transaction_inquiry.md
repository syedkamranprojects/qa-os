---
option: Transaction Inquiry
area: order_to_delivery_planning
doc_types: [CM-01, CM-02, "2"]
screens: [DYL_102014]
framework_flows: ["02960001", "03740001", "03190001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [order_booking, order_editing_cancellation, delivery_date_change]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-01
---
# Transaction Inquiry (order validation): how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 02960001 (seq 14, after order booking), 03740001 (seq 70, after editing), 03190001 (seq 68, edited-order charges/tax); sales-return variants 03200001/03770001 belong to the delivery/returns analyst.

## 1. Purpose
A read-only inquiry over all transaction documents (orders, sales, returns...). In this area it is the cross-check that what Order Booking/Editing saved matches the expected Gross, Discount, Tax and Net, and shows each document's status. [observed]
- It is also where the order's **status chain**, GIN number, delivery dates, applied promotions (Total Offering) and tax components (Total Tax) are read. [observed 2026-10-01 G11-1]

## 2. Actors and roles
Auto_Multi_Orga. [observed]
- Maker = Auto_Multi_Orga reads it (seq 14 and the status checks after the GIN and after seq 31-33). [observed 2026-10-01 G11-1]
- Checker: not used on this option in group 11. [observed 2026-10-01 G11-1]

## 3. Documents and master data
Reads cash memos (`snd_tr_cmm_cashmemo_master` and children detail/offering/charges [db]). Document types and statuses from `snd_pr_dot_documenttype` / `snd_pr_dos_documentstatus`.
- Promotions seen on 2026-10-01 orders (Total Offering): Automation2 / Automation2-3 (BONUS2), MARCH001 (BONUS2), MARCH002 (TRADEOFFER), May001 (BONUS2), May003 (BONUS2). [observed 2026-10-01 G11-1]
- Tax charges seen (Total Tax): **0001 - Value Added Tax** (TAX) and **9000 - 3rd Schduele** (sic, TAX). [observed 2026-10-01 G11-1]

## 4. Inputs: screens and fields
Menu Transaction Inquiry, option DYL_102014. Filters: **Document Type** (default "Demand Captured from Tele order"; choose **Sales**), **Document Status** (All), **Document Date From/To**, Date Type, PJP, Product/SKU; grid filter row on Outlet Code / Document No. Grid columns include Document No, Document Status, Execution Status, Gross Amount, Discount Amount, Tax Amount, Net Amount, Outlet Code, PJP Number, GIN No, Delivery Date, Actual Delivery Date, Invoice No, DDT Ref No. Live-verified 2026-10-01 (Block 1): Document Type options (17): Demand Captured from Tele order (default), OFF INVOICE CREDIT NOTE, DSR Shortage Amount, Amount Wise, Dsr Adj (SKU Wise), Sales, Sales Return, Fresh Sales Return, B2B Sale, Sales return without reference, Customer Account Close, Credit Note, Credit Note (Sales Return), Credit Note (Fresh Return), Credit Note (Sales Return W/O Ref), Off Invocie Credit Note (sic), Return Request. Document Status filter: All, CM-01 - Ordered / Confirmed / Planning completed / Cancelled / Delivered/Invoiced / Dispatched / Sent to Locus / Ready to dispatch/Packed / Reattempt / Out for delivery. Filters PJP Number, Document Date From/To (typed with Tab), SKU. The grid has 19 columns: Document No, Outlet Code, Outlet Long Name, Order Booker/Delivery Man, PJP Number, Order Time, Document Date, Delivery Date, Actual Delivery Date, Gross Amount, Discount Amount, Tax Amount, Offset Amount, Net Amount, Document Status, Demand Channel, DDT Ref No, GIN No, Invoice Ref. No; there is NO separate Execution Status column (Document Status shows the execution status text) and NO Delivery-PJP column (PJP Number is the order booker PJP 02111; the delivery PJP 02112 is visible on the GIN only); 5 rows per page. Row buttons: Detail, Product Wise Discount, Product Wise Free Quantity, Total Offering, Total Tax, Credit Note Adjustments (Product Wise* disabled until a row with that data is chosen) [observed].
Tabs/buttons: Detail, Product Wise Discount, Product Wise Free Quantity, Total Offering, Total Tax, Additional Charges, Credit Note Adjustments. [observed/step_labels]
Framework reads: header (Gross, Discount, Tax, Net), Detail tab (per line, incl. allocated CS column), Total Offering (Discount, Tax Amount), Charges (Charges Amount). [atlas]
- Live 2026-10-01 seq 14: filters Document Type (chose Sales), Document Status All, PJP Number All, Document Date From/To (today), SKU All; button Refresh. 7 Sales documents that day (2 pages of 5). Product Wise Discount and Product Wise Free Quantity stayed disabled for the booked orders. [observed 2026-10-01 G11-1]
- **Detail** window columns: product label, Trade Price/Unit, **Delivered** CS/DZ/PC (empty before delivery), Gross, Discount, Tax, Net, **Allocated** CS/DZ/PC (normalised, e.g. 7/0/0), **Ordered** CS/DZ/PC (as typed, e.g. 5/0/4). The product label here carries a third price (62740537: 8135.595, about 5.5% above the trade price; retail price? [inferred]). [observed 2026-10-01 G11-1]
- **Total Offering** window: one line per promotion with its discount and Tax Amount. [observed 2026-10-01 G11-1]
- **Total Tax** window: one line per tax charge (code - name, type TAX, amount). [observed 2026-10-01 G11-1]

## 5. Process: the business steps in order
1. [Maker] Navigate to Transaction Inquiry. (`11:14:02960001`)
2. [Maker] Choose Document Type = Sales, Document Status All, dates today; Click Refresh -> 24 Sales documents. [observed] (2026-10-01 with today's dates: 7 Sales documents. [observed 2026-10-01 G11-1]) (`11:14:02960001`)
3. [Maker] Filter Document No "COL26000" (or Outlet Code "Auto"); Open the order row. (`11:14:02960001`)
4. [Maker] Verify header amounts: outlet 1000000006 (COL26000002000) Gross 143,109.13, Discount -29,971.83, Tax 0, Net 113,137 = workbook; orders 04/05/07/08 net 134,372 / 113,137 / 134,535 / 108,202. [observed] (`11:14:02960001`) Live 2026-10-01 (COL26000002003, outlet 1000000004): Gross 143,109.13, Discount -29,971.83, Tax 21,234.24, Net 134,372 (rounded to the rupee). [observed 2026-10-01 G11-1]
5. [Maker] Verify the Document Status text. Right after booking the earlier run read "Confirmed"; on 2026-10-01 the same orders read **Planning completed** because they are on GIN 505 [observed]. Live baseline 2026-10-01 (Sales, 2026-09-29 to 09-30: 24 rows): the 8 target orders COL26000001995-2002 all have Document Date 2026-09-29, Delivery Date 2026-09-30, Actual Delivery Date empty, PJP 02111, Order Booker AutomationOB/AutomationQADSR, Demand Channel Back Office (BO), GIN No 505, Invoice Ref empty, Offset 0; amounts (Gross / Discount / Tax / Net): 1995 143,109.13 / -29,971.83 / 21,861.52 / 134,999; 1996 .../21,234.24/134,372; 1997 .../21,992.03/135,129; 1998 .../21,234.24/134,372; 1999 and 2000 tax 0 / 113,137; 2001 tax 21,397.32 / 134,535; 2002 107,960.51 / -16,264.08 / 16,505.36 / 108,202 [observed]. Other documents in the range: Cancelled 1979-1986, 1993, 1994; Delivered/Invoiced 1987, 1989-1992 (GIN 504, actual delivery 2026-09-29); 1988 also on GIN 505 (so GIN 505 holds 9 cash memos) [observed]. (`11:14:02960001`) Live 2026-10-01 right after booking: COL26000002003 **Confirmed**, Order Booker/Delivery Man "AutomationOB / AutomationQADSR" (the delivery man is assigned at booking), PJP 02111, Order Time filled, Delivery Date 2026-10-07, Actual Delivery Date empty, Offset 0, GIN No empty. [observed 2026-10-01 G11-1]
6. Not run live: Detail, Total Offering, Charges tab checks; after editing (seq 70, 68) the same checks on the edited order. [unknown results] (superseded 2026-10-01: Detail, Total Offering and Total Tax were run live on COL26000002003, steps 7-9; seq 68 and 70 are still not walked.)
7. [Maker] Click Detail on the order row; Verify per line Allocated (normalised) and Ordered (as typed) quantities; Delivered is empty before delivery. [observed 2026-10-01 G11-1] (`11:14:02960001`)
8. [Maker] Click Total Offering; Verify the promotion lines sum to the header Discount. [observed 2026-10-01 G11-1] (`11:14:02960001`)
9. [Maker] Click Total Tax; Verify the tax lines sum to the header Tax. [observed 2026-10-01 G11-1] (`11:14:02960001`)

## 6. Outputs and effects
None (inquiry only).
- COL26000002003 Total Offering 2026-10-01: Automation2 / Automation2-3 / BONUS2 -14,310.91; MARCH001 BONUS2 -650; MARCH002 TRADEOFFER -14,310.91; May001 BONUS2 -650; May003 BONUS2 -50; Tax Amount 0 on each. Sum -29,971.83 = header Discount. Two promotions are each exactly 10% of gross (14,310.91 = 10% x 143,109.13), plus three fixed amounts, which is why the discount % changes with the basket. [observed 2026-10-01 G11-1]
- COL26000002003 Total Tax 2026-10-01: 0001 - Value Added Tax (TAX) 18,038.93; 9000 - 3rd Schduele (sic) (TAX) 3,195.31; sum 21,234.24 = header Tax. Third-Schedule products are taxed on the retail price, which explains the higher effective tax on 62690363 / 20050308. [observed amounts; reason inferred from Pakistani tax practice, 2026-10-01 G11-1]

## 7. Statuses and transitions
Shows statuses; changes none. Observed status after booking: Confirmed [observed]; DB description for CM-01 04 is Ordered. See order_lifecycle_and_statuses.md.
- **Status chain observed 2026-10-01** (Document Status column) [observed 2026-10-01 G11-1]:

| Order | Document Status | Delivery Date | Actual Delivery | GIN | when read |
|---|---|---|---|---|---|
| COL26000002003-2007 | Confirmed | 2026-10-07 | - | - | after booking (seq 14) |
| COL26000002003-2007 | Ready to dispatch/Packed | 2026-10-01 | - | 506 | after GIN 506 approval |
| COL26000002008 | Cancelled | 2026-10-07 | - | - | cancelled before the GIN (seq 16) |
| COL26000002003/2004/2005 | Delivered/Invoiced | 2026-10-01 | 2026-10-01 17:54:09 (time of the Cashmemo Status save) | 506 | after seq 33 |
| COL26000002006 | Reattempt | 2026-10-02 | - | (none: rescheduling takes it off the GIN) | after Cashmemo Reschedule (seq 32) |
| COL26000002007 | Cancelled | 2026-10-01 | - | 506 kept | cancelled after the GIN (seq 31) |
| COL26000002008 | Cancelled | 2026-10-07 | - | - | after seq 31-33 |

- Chain: **Confirmed** (after booking) -> **Ready to dispatch/Packed** (after GIN approval) -> **Delivered/Invoiced** (Cashmemo Status save); side exits **Reattempt** (rescheduled) and **Cancelled** (before or after the GIN). "Planning completed" (seen on 09-30's GIN 505 while still Pending) = cash memo on a forwarded but unapproved GIN. [observed 2026-10-01 G11-1; Planning completed meaning inferred]

## 8. Rules and validations
- The default Document Type hides booked orders (they are Sales, not Demand Captured). [observed]
- Totals must equal Order Booking summary and the workbook. [observed]
- Net = Gross + Discount + Tax rounded to whole PKR (143,109.13 - 29,971.83 + 21,861.52 = 134,998.82 shown 134,999); Net is integer, Gross/Discount/Tax keep 2 decimals [observed 2026-10-01].
- **Total Offering sums equal the header Discount** (1995-2001: Automation2 BONUS2 -14,310.91, MARCH001 BONUS2 -650, MARCH002 TRADEOFFER -14,310.91, May001 BONUS2 -650, May003 BONUS2 -50 = -29,971.82 vs header -29,971.83, a 1 paisa rounding; 2002: -5,398.03, -10, -10,796.05, -10, -50 = -16,264.08 = header exactly); tax is 0 on every promo line [observed 2026-10-01]. Re-observed on COL26000002003: sum -29,971.83 = header exactly. [observed 2026-10-01 G11-1]
- **Total Tax lines sum to the header Tax** (VAT + 3rd Schedule). [observed 2026-10-01 G11-1]
- Tax is 0 for tax-exempt outlets. [observed]
- Date filters default to today; orders of other days need the range widened. [inferred] (upgraded: [observed 2026-10-01 G11-1], was [inferred]: Document Date From/To open on today and the 09-29 orders needed a wider range.)
- The delivery man is already shown at booking (Order Booker/Delivery Man column), before any GIN. [observed 2026-10-01 G11-1]
- A cancelled order keeps its last Delivery Date (2008 cancelled before the Delivery Date Change keeps 10-07) and, when cancelled after the GIN, keeps the GIN No (2007: 506). [observed 2026-10-01 G11-1]
- Invoice Ref. No. stays empty after delivery. [observed 2026-10-01 G11-1]
- Actual Delivery Date = the date-time the Cashmemo Status was saved. [observed 2026-10-01 G11-1]

## 9. Messages
None observed; assertions are value comparisons (TSTMSG with screenshot_ASSR group). Re-confirmed 2026-10-01: no message on Refresh, Detail, Total Offering or Total Tax. [observed 2026-10-01 G11-1]

## 10. Dependencies
Reads orders (seq 10), edited orders (seq 15), later sales returns and GIN numbers. Hands nothing.
- 2026-10-01: seq 15 (edit before the GIN) was skipped, so seq 70 (TI after Order Editing) and seq 68 (edited-order charges/tax) have no edited order from seq 15; the order edited after the GIN (COL26000002003, seq 29) is the only edited order available. [observed 2026-10-01 G11-1]

## 11. Test design hints
- Positive: for each booked order compare 4 amounts to the Order Booking summary; check status; check Detail line sums equal header; Total Offering discount equals header discount.
- Negative: wrong Document Type shows no row; status filter excludes the order.
- Boundary: order on the first/last day of the date range; 24-row list with filter on one outlet.
- Traps: header amounts are checked for the first row of the filtered grid; if filter order changes the wrong order is compared. Only the header check was run live.
- New 2026-10-01 [observed 2026-10-01 G11-1]:
  - Positive: Total Tax lines (VAT + 3rd Schedule) sum to the header Tax; Total Offering lines sum to the header Discount.
  - Positive: status after each step: Confirmed -> Ready to dispatch/Packed -> Delivered/Invoiced; Reattempt after reschedule (GIN No cleared, Delivery Date = new date); Cancelled before the GIN (no GIN No) vs after the GIN (GIN No kept).
  - Positive: Detail shows Ordered (as typed) vs Allocated (normalised) quantities; after an edit the Allocated/Ordered values should follow the edit (not yet read).
  - Trap: the status for an order on a GIN depends on the GIN's approval: Planning completed (forwarded, not approved) vs Ready to dispatch/Packed (approved). Do not assert one fixed text "after GIN".
  - Trap: the Total Tax charge name is spelt "3rd Schduele"; assert the code 9000 or the exact spelling.

## 12. Open questions (batched for the BA)
- ANSWERED 2026-10-01 (Q23): "Confirmed" is execution status 02 (separate from Ordered 04); the column shows execution status text.
- ANSWERED 2026-10-01 (Q28): Total Offering Discount sum equals the header Discount (within 1 paisa rounding) on all 8 orders.
- Surprise: orders 1993 and 1986 are Cancelled but still show Delivery Date 2026-10-05 [observed]. (Explained 2026-10-01 G11-1: a cancelled order keeps its last delivery date; 2008 cancelled before the Delivery Date Change keeps 10-07. [observed 2026-10-01 G11-1])
- Q: Which price is the third price in the Detail product label (62740537 8135.595: retail price)? | Default: retail price (basis of the 3rd Schedule tax) | Class: C | Evidence: seq 14 Detail. [observed 2026-10-01 G11-1]
- Q: When does Invoice Ref. No. get filled (empty after delivery)? | Default: not used in this cycle | Class: B | Evidence: status check after seq 33.

## 13. Sources
learning_block1.json (L03), LIVE_FINDINGS.md; atlas flows 02960001, 03740001, 03190001; TC-OB-01_executed.md (TC-OB-03); step_labels "Transaction Inquiry"; DB tables above.
- Live learning session G11-1 (2026-10-01, cnr1dev1, distributor 15108843): `learning_sessions/2026-10-01_G11-PK_session1_log.md` seq 14, "Transaction Inquiry after GIN approval (extra check)", "Transaction Inquiry status check after seq 31-33"; `learning_sessions/2026-10-01_G11-PK_session1_report.md` §3 rules 8-10.
