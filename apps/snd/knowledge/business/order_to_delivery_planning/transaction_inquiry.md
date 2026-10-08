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
updated: 2026-10-08
---
# Transaction Inquiry (order validation): how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 02960001 (seq 14, after order booking), 03740001 (seq 70, after editing), 03190001 (seq 68, edited-order charges/tax); sales-return variants 03200001/03770001 belong to the delivery/returns analyst.
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.
Updated 2026-10-08: merged the QA team's written answers to the 2026-10-06 review (learning_sessions/2026-10-06_G11-PK_QA_Team_Review.docx); evidence learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx). Tag [stated 2026-10-08 QA Team] = written answer of the QA team. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08: ...)".
Updated 2026-10-08 (follow-up): merged the QA team's answers to the 2026-10-08 follow-up (Q-DS4, Q-SV1, CASHMEMO_EDIT / Q-OE5); evidence learning_sessions/2026-10-08_QA_Team_followup_answers.md. Tag [stated 2026-10-08 QA Team (follow-up)]. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08: ...)".

## 1. Purpose
A read-only inquiry over all transaction documents (orders, sales, returns...). In this area it is the cross-check that what Order Booking/Editing saved matches the expected Gross, Discount, Tax and Net, and shows each document's status. [observed]
- It is also where the order's **status chain**, GIN number, delivery dates, applied promotions (Total Offering) and tax components (Total Tax) are read. [observed 2026-10-01 G11-1]
- G11-2b: after Route Settlement it shows the **Offset Amount** (deposit-slip allocations on each cash memo) and, for Document Type Sales Return, the return with its Invoice Ref. No. (the sales invoice) [observed 2026-10-05 G11-2b].

## 2. Actors and roles
Auto_Multi_Orga. [observed]
- Maker = Auto_Multi_Orga reads it (seq 14 and the status checks after the GIN and after seq 31-33). [observed 2026-10-01 G11-1]
- Checker: not used on this option in group 11. [observed 2026-10-01 G11-1]
- G11-2/2b: Maker Auto_Multi_Orga read seq 14, 52, 68, 69, 70, 71 [observed 2026-10-05 G11-2, G11-2b].

## 3. Documents and master data
Reads cash memos (`snd_tr_cmm_cashmemo_master` and children detail/offering/charges [db]). Document types and statuses from `snd_pr_dot_documenttype` / `snd_pr_dos_documentstatus`.
- Promotions seen on 2026-10-01 orders (Total Offering): Automation2 / Automation2-3 (BONUS2), MARCH001 (BONUS2), MARCH002 (TRADEOFFER), May001 (BONUS2), May003 (BONUS2). [observed 2026-10-01 G11-1]
- Tax charges seen (Total Tax): **0001 - Value Added Tax** (TAX) and **9000 - 3rd Schduele** (sic, TAX). [observed 2026-10-01 G11-1]
- G11-2b: Sales Return documents (CM-02) are listed under Document Type **Sales Return**: COL26000000714, Demand Channel **"Partial Return"**, Document Status **Picked**, Invoice Ref. No. COL26000002009 [observed 2026-10-05 G11-2b].

## 4. Inputs: screens and fields
Menu Transaction Inquiry, option DYL_102014. Filters: **Document Type** (default "Demand Captured from Tele order"; choose **Sales**), **Document Status** (All), **Document Date From/To**, Date Type, PJP, Product/SKU; grid filter row on Outlet Code / Document No. Grid columns include Document No, Document Status, Execution Status, Gross Amount, Discount Amount, Tax Amount, Net Amount, Outlet Code, PJP Number, GIN No, Delivery Date, Actual Delivery Date, Invoice No, DDT Ref No. Live-verified 2026-10-01 (Block 1): Document Type options (17): Demand Captured from Tele order (default), OFF INVOICE CREDIT NOTE, DSR Shortage Amount, Amount Wise, Dsr Adj (SKU Wise), Sales, Sales Return, Fresh Sales Return, B2B Sale, Sales return without reference, Customer Account Close, Credit Note, Credit Note (Sales Return), Credit Note (Fresh Return), Credit Note (Sales Return W/O Ref), Off Invocie Credit Note (sic), Return Request. Document Status filter: All, CM-01 - Ordered / Confirmed / Planning completed / Cancelled / Delivered/Invoiced / Dispatched / Sent to Locus / Ready to dispatch/Packed / Reattempt / Out for delivery. Filters PJP Number, Document Date From/To (typed with Tab), SKU. The grid has 19 columns: Document No, Outlet Code, Outlet Long Name, Order Booker/Delivery Man, PJP Number, Order Time, Document Date, Delivery Date, Actual Delivery Date, Gross Amount, Discount Amount, Tax Amount, Offset Amount, Net Amount, Document Status, Demand Channel, DDT Ref No, GIN No, Invoice Ref. No; there is NO separate Execution Status column (Document Status shows the execution status text) and NO Delivery-PJP column (PJP Number is the order booker PJP 02111; the delivery PJP 02112 is visible on the GIN only); 5 rows per page. Row buttons: Detail, Product Wise Discount, Product Wise Free Quantity, Total Offering, Total Tax, Credit Note Adjustments (Product Wise* disabled until a row with that data is chosen) [observed].
Tabs/buttons: Detail, Product Wise Discount, Product Wise Free Quantity, Total Offering, Total Tax, Additional Charges, Credit Note Adjustments. [observed/step_labels]
Framework reads: header (Gross, Discount, Tax, Net), Detail tab (per line, incl. allocated CS column), Total Offering (Discount, Tax Amount), Charges (Charges Amount). [atlas]
- Live 2026-10-01 seq 14: filters Document Type (chose Sales), Document Status All, PJP Number All, Document Date From/To (today), SKU All; button Refresh. 7 Sales documents that day (2 pages of 5). Product Wise Discount and Product Wise Free Quantity stayed disabled for the booked orders. [observed 2026-10-01 G11-1]
- **Detail** window columns: product label, Trade Price/Unit, **Delivered** CS/DZ/PC (empty before delivery), Gross, Discount, Tax, Net, **Allocated** CS/DZ/PC (normalised, e.g. 7/0/0), **Ordered** CS/DZ/PC (as typed, e.g. 5/0/4). The product label here carries a third price (62740537: 8135.595, about 5.5% above the trade price; retail price? [inferred]). [observed 2026-10-01 G11-1]
- **Total Offering** window: one line per promotion with its discount and Tax Amount. [observed 2026-10-01 G11-1]
- **Total Tax** window: one line per tax charge (code - name, type TAX, amount). [observed 2026-10-01 G11-1]
- G11-2b: buttons used per selected row: **Detail**, **Total Offering**, **Total Tax** (each opens a window); the grid "Show filter row" gives an Outlet Code filter [observed 2026-10-05 G11-2b].
- G11-2b Detail columns: Serial No, Product Description, Batch, Stock Type, Trade Price / Unit, Delivered CS/DZ/PC, Gross, Discount, Tax, Net, Allocated CS/DZ/PC, Ordered CS/DZ/PC [observed 2026-10-05 G11-2b].

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

G11-2 / G11-2b walk (2026-10-05) [observed 2026-10-05 G11-2, G11-2b]:
1. [Maker] Verify orders 2009-2014 "Confirmed", delivery 2026-10-11, amounts as booked (11:14:02960001) - identical to 10-01.
2. [Maker] After Route Settlement: Choose Document Type Sales, dates 2026-10-05; Verify Offset Amount per cash memo (11:52:03210001).
3. [Maker] Filter Outlet Code 1000000004; Select COL26000002009; Verify header Gross 96,840.34 / Discount -20,718.07 / Tax 14,584.79 / Offset 2,600 / Net 90,707; Click Total Tax -> 0001 VAT 11,389.48 + 9000 3rd Schduele 3,195.31 (11:68:03190001).
4. [Maker] Click Detail and Total Offering on COL26000002009; Verify lines (11:70:03740001).
5. [Maker] Choose Document Type Sales Return; Verify COL26000000714 header, Total Tax, Detail, Total Offering (11:69:03200001, 11:71:03770001).
G11-3 reads (2026-10-06) [observed 2026-10-06 G11-3]:
1. Seq 14: Document Type Sales, today: 6 orders Confirmed, delivery 2026-10-12 (values in order_booking.md; 2017/2019 tax differs, Q-TX1) (11:14:02960001).
2. Seq 52 (after the settlement by Claude): 2015 Delivered/Invoiced Offset **2,600** (1145 600 + 1147 1,000 + 1148 1,000); 2016 Offset 101,161; 2020 Offset 108,202; 2017 / 2019 Cancelled 0; 2018 Reattempt (delivery 10-07) 0; 2012 (10-05) Delivered/Invoiced, GIN 509, Offset 0 (unpaid) (11:52:03210001).
3. Seq 68: COL26000002015 (edited 7 -> 4 -> 3 CS): header 81,417.41 / -17,633.48 / **12,371.66** / Offset 2,600 / Net 76,156, Delivered/Invoiced, GIN 508; Total Tax VAT **9,176.35** + 3rd Schedule **3,195.31** = 12,371.66 (11:68:03190001).
4. Seq 70: Detail line 62740537 Delivered **3 CS**, 46,268.79 / -10,020.95 / 6,524.61 / 42,772.45, **Allocated 4 CS, Ordered 5 CS 4 PC**; 20050310 5 CS 18,727.90 / -4,056.11 / 2,640.92 / 17,312.71; 62690363 3/0/2 9,855.56 / -2,134.53 / 1,873.23 / 9,594.26; 20050308 2/0/10 6,488.44 / -1,405.27 / 1,322.08 / 6,405.25; 69997598 6 PC 76.72 / -16.62 / 10.82 / 70.92. Total Offering: Automation2 -8,141.74, MARCH001 -650, MARCH002 -8,141.74, May001 -650, May003 -50 (sum -17,633.48 = header) (11:70:03740001).
5. Seq 69 + 71: Document Type Sales Return: **COL26000000715**, outlet 04, -30,845.86 / 6,189.17 / **-4,409.61** / Offset 0 / **-29,066**, **Picked**, Demand Channel "Partial Return", Invoice Ref COL26000002015; Total Tax VAT -4,409.61, 3rd Schedule 0; Detail line 1 2 CS -30,845.86 / 6,530.75 / -4,376.72 / -28,691.83, lines 2-5 qty 0 with small re-priced discounts (-182, -95.78, -63.06, -0.75); Offering Automation2 +3,084.59, MARCH001 +10, MARCH002 +3,084.59, May001 +10, May003 0 (11:69:03200001, 11:71:03770001).

## 6. Outputs and effects
None (inquiry only).
- COL26000002003 Total Offering 2026-10-01: Automation2 / Automation2-3 / BONUS2 -14,310.91; MARCH001 BONUS2 -650; MARCH002 TRADEOFFER -14,310.91; May001 BONUS2 -650; May003 BONUS2 -50; Tax Amount 0 on each. Sum -29,971.83 = header Discount. Two promotions are each exactly 10% of gross (14,310.91 = 10% x 143,109.13), plus three fixed amounts, which is why the discount % changes with the basket. [observed 2026-10-01 G11-1]
- COL26000002003 Total Tax 2026-10-01: 0001 - Value Added Tax (TAX) 18,038.93; 9000 - 3rd Schduele (sic) (TAX) 3,195.31; sum 21,234.24 = header Tax. Third-Schedule products are taxed on the retail price, which explains the higher effective tax on 62690363 / 20050308. [observed amounts; reason inferred from Pakistani tax practice, 2026-10-01 G11-1]

G11-2b values (2026-10-05) [observed 2026-10-05 G11-2b]:
- **Offset Amount after settlement = sum of the posted deposit-slip allocations on the cash memo**: COL26000002009 Offset 2,600 (slips 1139 600 + 1141 1,000 + 1142 1,000; the outlet-level multi-cheque of slip 1140 went to the older COL26000002003, not to 2009); COL26000002010 101,161 (slip 1137); COL26000002011 119,370 (slip 1138); 2012 Reattempt, 2013/2014 Cancelled: 0. The sales return is NOT in the Offset (return Offset 0; 2009 Offset excludes its 29,077 return). Actual Delivery Date of the delivered memos 2026-10-05 10:37.
- **Edited order COL26000002009** (seq 68/70): header Gross 96,840.34, Discount -20,718.07, Tax 14,584.79, Offset 2,600, Net 90,707, Delivered/Invoiced, GIN 507. Total Tax: 0001 Value Added Tax 11,389.48 + 9000 3rd Schduele 3,195.31 = 14,584.79.
- Detail (seq 70): 1. 62740537 TP 7,711.47, Delivered 4 CS, Gross 61,691.72, Disc -13,198.36, Tax 8,728.81, Net 57,222.17, **Allocated 7 CS, Ordered 5 CS 4 PC**; 2. 20050310 5 CS 18,727.90 / -4,006.66 / 2,649.82 / 17,371.07; 3. 62690363 3 CS 2 PC 9,855.56 / -2,108.50 / 1,873.23 / 9,620.28; 4. 20050308 2 CS 10 PC 6,488.44 / -1,388.14 / 1,322.08 / 6,422.38; 5. 69997598 6 PC 76.72 / -16.41 / 10.86 / 71.16.
- Total Offering (2009): Automation2 BONUS2 -9,684.03; MARCH001 BONUS2 -650; MARCH002 TRADEOFFER -9,684.03; May001 BONUS2 -650; May003 BONUS2 -50; Tax 0 each; sum -20,718.06 vs header -20,718.07 (1 paisa).
- **Sales return COL26000000714** (seq 69/71): outlet 1000000004, Document/Delivery Date 2026-10-05, Actual Delivery 2026-10-05 10:44:25, Gross -30,845.86, Discount 6,189.17, Tax -4,419.93, Offset 0, Net -29,077, Picked, Demand Channel Partial Return, Invoice Ref. No. COL26000002009. Total Tax: VAT -4,419.93, 3rd Schduele 0. Detail: line 1 62740537 2 CS, Gross -30,845.86, Disc 6,407.54, Tax -4,398.90, Net -28,837.22; lines 2-5 return 0 quantity but carry small reversals (20050310 disc -116.35 tax -20.94; 62690363 -61.23; 20050308 -40.31; 69997598 -0.48 / -0.09). Total Offering: Automation2 +3,084.59; MARCH001 +10; MARCH002 +3,084.59; May001 +10; May003 0 (sum 6,189.18 = header Discount).
- G11-3: Offset = posted slip allocations again (2015: 2,600); the multi-cheque 1146 is not on 2015; a delivered unpaid memo shows Offset 0 [observed 2026-10-06 G11-3].
- G11-3: tax of the twice-edited order: VAT 9,176.35 + 3rd Schedule 3,195.31; the 3rd Schedule part did not change between 4 CS and 3 CS (3,195.31 on both) [observed 2026-10-05 and 2026-10-06; rule inferred].
- G11-3: return 715 Tax -4,409.61 / Net -29,066 (10-05: -4,419.93 / -29,077, source order 4 CS); Gross -30,845.86 and Discount 6,189.17 unchanged [observed 2026-10-06 G11-3].

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
- G11-2b: the sales return CM-02 reads **Picked** after Save Sale Pick; the source cash memo COL26000002009 stays **Delivered/Invoiced** after its partial return (no Partial Delivered status shown) [observed 2026-10-05 G11-2b].
- G11-2: chain Confirmed -> Ready to dispatch/Packed -> Delivered/Invoiced / Reattempt / Cancelled confirmed on a second day [observed 2026-10-05 G11-2].
- G11-3: chain Confirmed -> Ready to dispatch/Packed -> Delivered/Invoiced / Reattempt / Cancelled seen a third day; return Picked, Demand Channel Partial Return; source memo stays Delivered/Invoiced [observed 2026-10-06 G11-3].

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
- G11-2b: **Offset Amount = posted deposit-slip allocations on the memo** (after settlement); returns are not netted into it [observed 2026-10-05 G11-2b]. Whether Offset fills at allocation or only at posting: not read before settlement on 10-05 (10-01 orders showed Offset 0 right after booking) [unknown].
- G11-2b: **Invoice Ref. No. of a sales return = its sales invoice** (COL26000002009); it stays empty on the sales cash memo [observed 2026-10-05 G11-2b].
- G11-2b: Total Tax lines sum to header Tax and Total Offering lines to header Discount also for the edited order and for the return (1 paisa rounding) [observed 2026-10-05 G11-2b].
- G11-2b: **after an edit the Detail keeps Allocated = original 7 CS and shows Ordered "5 CS 4 PC" for the edited line, while Delivered = 4 CS and the amounts follow the edit**; meaning unclear (Q-TI1) [observed 2026-10-05 G11-2b].
- G11-2b: the return re-prices the order's slab promotions: lines with 0 returned quantity carry small discount/tax reversals [observed 2026-10-05 G11-2b; rule inferred; see sales_return.md].
- G11-3: after two edits (7 -> 4 -> 3 CS) the Detail shows **Allocated 4 CS** (the allocation made by the first edit's save, not the booked 7) and **Ordered 5 CS 4 PC** (as on 10-05), Delivered 3 CS; amounts follow the last edit [observed 2026-10-06 G11-3]. (Refines the G11-2b note "Allocated = original 7 CS": Allocated = the order's last allocation before the GIN [inferred].) Meaning of Ordered stays Q-TI1. (superseded 2026-10-06: **Ordered = the outlet's original order quantity; Allocated = what was allocated from available stock (less when stock was short)**; Ordered 5 CS 4 PC / Allocated 4 / Delivered 3 is expected [stated 2026-10-06 QA Team Lead]; Q-TI1 answered.)
- G11-3: Total Offering sums to header Discount and Total Tax to header Tax again (edited order and return) [observed 2026-10-06 G11-3].
- QA team 2026-10-08 (rule 5, confirmed): Ordered = the outlet's original quantity, Allocated = what stock availability allowed; "based on stock availability the stock and delivered qty will be modified on delivery" [stated 2026-10-08 QA Team].
- QA team 2026-10-08 (comment given under rule 13): Transaction Inquiry shows invoice details incl. gross amount, discount, tax, **received / offset amount** and net amount; in the case reviewed "the offset amount has been fully adjusted, but it does not impact the net amount", which the QA team considers correct under the current logic [stated 2026-10-08 QA Team]. So the Net column is the invoice net and is NOT reduced by collections; Offset/Received carry the collections (consistent with Q50 [observed 2026-10-05]). The comment was given as an answer to the Outstanding Outlet doubled-totals rule; whether it was meant for that rule is under clarification (Q-DS4, follow-up sent 2026-10-08). (2026-10-08 follow-up: Q-DS4 closed: the outlet totals were correct sums of all open invoices of the outlet, not a defect [stated 2026-10-08 QA Team (follow-up)]; the rule-13 comment stands as a statement about Transaction Inquiry only.)
- Promotions training 2026-10-07: **Total Offering** (one line per promotion) is the order-side reading of promotion use; the budget side is read on Current Promotion (allocated / utilised), so a budget case compares Utilized before / after plus Total Offering [stated 2026-10-07 Syed Zulfiqar]; see [promotions_and_budget.md](../promotions_and_budget/promotions_and_budget.md) section 6.

## 9. Messages
None observed; assertions are value comparisons (TSTMSG with screenshot_ASSR group). Re-confirmed 2026-10-01: no message on Refresh, Detail, Total Offering or Total Tax. [observed 2026-10-01 G11-1]
- G11-2/2b: no message on Refresh, Detail, Total Offering or Total Tax [observed 2026-10-05 G11-2b].

## 10. Dependencies
Reads orders (seq 10), edited orders (seq 15), later sales returns and GIN numbers. Hands nothing.
- 2026-10-01: seq 15 (edit before the GIN) was skipped, so seq 70 (TI after Order Editing) and seq 68 (edited-order charges/tax) have no edited order from seq 15; the order edited after the GIN (COL26000002003, seq 29) is the only edited order available. [observed 2026-10-01 G11-1]
- G11-2b: seq 52 needs a completed Route Settlement (posting); seq 68/70 read the order edited after the GIN at seq 29 (seq 15 skipped again); seq 69/71 need the picked return (seq 38) [observed 2026-10-05 G11-2b].
- G11-3: seq 68/70 read the order edited at seq 15 AND seq 29 (both executed on 10-06), so the workbook values (one edit to 4 CS) do not apply; seq 69/71 read return 715 on that order [observed 2026-10-06 G11-3].

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
- G11-2/2b additions [observed 2026-10-05 G11-2b]:
  - Positive: Offset Amount after settlement = sum of the memo's posted slip allocations (2009: 600 + 1,000 + 1,000 = 2,600); a memo allocated only at outlet level may show 0 because the money went to the outlet's oldest open memo.
  - Positive: sales return row: Invoice Ref. No. = source invoice, Demand Channel "Partial Return", Document Status Picked, negative Gross/Tax/Net, positive Discount.
  - Positive: Total Tax = VAT + 3rd Schedule = header Tax (edited order 11,389.48 + 3,195.31 = 14,584.79).
  - Trap (framework drift): workbook "T Inquiry Header Amt Val OE" expects header **Tax 8,728.81** (= line 1's tax); the real header Tax is 14,584.79, so the engine would fail seq 70 although the app is right.
  - Trap (framework drift): all seq 69/71 return values in the workbook (built 2026-09-21 for outlet 1000000003) differ from the app except Gross -30,845.86 (Discount 6,169.17 vs 6,189.17; Tax -4,425.41 / -4,436.55 vs -4,419.93; Net -29,113 vs -29,077; VAT -4,434.18 + 3rd Schedule -1.95 vs -4,419.93 + 0; line 1 Disc 6,260.28 / Net -29,010.99 vs 6,407.54 / -28,837.22). See FRAMEWORK_DRIFT.md.
  - Trap: after an edit, Detail Allocated/Ordered keep pre-edit values (7 CS / 5 CS 4 PC); assert Delivered and amounts, not Allocated/Ordered, until Q-TI1 is answered.
  - Trap: the default Document Type hides both orders and returns; choose Sales or Sales Return explicitly (confirmed 10-05).
- G11-3 additions [observed 2026-10-06 G11-3]:
  - Trap (framework drift): when seq 15 and seq 29 both edit the same order, the seq 68/70 expected values (workbook 11,389.48 / 3,195.31 / 14,584.79) and the seq 69/71 return values change (3 CS: VAT 9,176.35; return Tax -4,409.61 / Net -29,066). Compute expected values from the day's edits.
  - Trap: Allocated in the Detail reflects the last allocation (re-allocation by the edit save), not the booked quantity.
  - Rule for assertions [stated 2026-10-06 QA Team Lead]: Ordered = original order quantity, Allocated = allocated from available stock, Delivered = delivered; all three may differ and that is correct.
  - Positive: a Reattempt order delivered on a later GIN shows Delivered/Invoiced with the new GIN No and actual delivery time of that day.

## 12. Open questions (batched for the BA)
- ANSWERED 2026-10-01 (Q23): "Confirmed" is execution status 02 (separate from Ordered 04); the column shows execution status text.
- ANSWERED 2026-10-01 (Q28): Total Offering Discount sum equals the header Discount (within 1 paisa rounding) on all 8 orders.
- Surprise: orders 1993 and 1986 are Cancelled but still show Delivery Date 2026-10-05 [observed]. (Explained 2026-10-01 G11-1: a cancelled order keeps its last delivery date; 2008 cancelled before the Delivery Date Change keeps 10-07. [observed 2026-10-01 G11-1])
- Q: Which price is the third price in the Detail product label (62740537 8135.595: retail price)? | Default: retail price (basis of the 3rd Schedule tax) | Class: C | Evidence: seq 14 Detail. [observed 2026-10-01 G11-1]
- Q: When does Invoice Ref. No. get filled (empty after delivery)? | Default: not used in this cycle | Class: B | Evidence: status check after seq 33.
- PARTLY ANSWERED 2026-10-05 (Invoice Ref. No.): filled on a sales return with the source sales invoice; still empty on sales cash memos [observed 2026-10-05 G11-2b].
- ANSWERED 2026-10-05 (Q50, Offset Amount): sum of posted deposit-slip allocations on the memo; returns not included [observed 2026-10-05 G11-2b].
- Q-TI1: After an order edit, why does Transaction Inquiry Detail show Allocated = original 7 CS and Ordered = "5 CS 4 PC" for the edited line (Delivered 4 CS)? What should Ordered/Allocated mean after an edit? | Default: they keep the as-booked values; assert Delivered and amounts only | Class: C | Evidence: COL26000002009 Detail line 1 [observed 2026-10-05 G11-2b].
- Q-TI1 evidence 2026-10-06: after 7 -> 4 -> 3 CS the Detail shows Allocated 4 CS (not 7 as on 10-05 after one edit made after the GIN), Ordered 5 CS 4 PC, Delivered 3 CS [observed 2026-10-06 G11-3]. Still open: what Ordered / Allocated should mean after an edit. **-> ANSWERED 2026-10-06** [stated 2026-10-06 QA Team Lead]: Ordered = the outlet's original order quantity; Allocated = quantity allocated from available stock (lower when stock was short); Delivered = what was delivered. Ordered 5 CS 4 PC / Allocated 4 / Delivered 3 is expected behaviour.
- Q-DS4 cross-reference 2026-10-08: see deposit_slips.md; the QA team's rule-13 comment (offset fully adjusted, net unchanged = correct) is recorded above; Q-DS4 is under clarification. (superseded 2026-10-08: Q-DS4 closed by the follow-up, not a defect [stated 2026-10-08 QA Team (follow-up)]; Transaction Inquiry remains a valid source for per-invoice amounts when an outlet total is computed.)

## 13. Sources
learning_block1.json (L03), LIVE_FINDINGS.md; atlas flows 02960001, 03740001, 03190001; TC-OB-01_executed.md (TC-OB-03); step_labels "Transaction Inquiry"; DB tables above.
- Live learning session G11-1 (2026-10-01, cnr1dev1, distributor 15108843): `learning_sessions/2026-10-01_G11-PK_session1_log.md` seq 14, "Transaction Inquiry after GIN approval (extra check)", "Transaction Inquiry status check after seq 31-33"; `learning_sessions/2026-10-01_G11-PK_session1_report.md` §3 rules 8-10.
- G11-2 / G11-2b: learning_sessions/2026-10-05_G11-PK_session2_log.md (seq 14); learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md (seq 52, 68, 69, 70, 71).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 14, 52, 68, 69, 70, 71).

- QA team written answers 2026-10-08: learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx) (rules 5, 13).
- QA team follow-up answers 2026-10-08: learning_sessions/2026-10-08_QA_Team_followup_answers.md (Q-DS4 closed).
