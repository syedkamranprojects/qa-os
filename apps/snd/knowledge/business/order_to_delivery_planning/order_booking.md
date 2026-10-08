---
option: Order Booking
area: order_to_delivery_planning
doc_types: [CM-01]
screens: [ORDER_BOOKING]
framework_flows: ["00010001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [dispatch_advice, stock_validation_flows, stock_inquiry_and_balances]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-08
---
# Order Booking: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]** seen live in a replay or recording, **[db]** declared by the application DB or the framework tables, **[inferred]** concluded by Claude from names or structure (to be confirmed), **[unknown]** not determinable yet.
Updated: 2026-10-01 (G11-1 consolidation)
Last updated: 2026-10-01. Source flows: 00010001 (group 11 seq 10; also groups 1, 52).
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.
Updated 2026-10-08: merged the QA team's written answers to the 2026-10-06 review (learning_sessions/2026-10-06_G11-PK_QA_Team_Review.docx); evidence learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx). Tag [stated 2026-10-08 QA Team] = written answer of the QA team. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08: ...)".

## 1. Purpose
Order Booking captures a retail outlet's demand for products (an order) on behalf of a distributor, usually entered by an Order Booker or Spot Seller [inferred from the field "Order Booker/Spot Seller"]. The order is stored as a cash memo document and is later picked, issued on a Goods Issue Note and delivered [db: order is the cash memo master `snd_tr_cmm_cashmemo_master`, status "Ordered"]. In the Daily Cycle it comes after the stock has been received (Dispatch Advice, approval, stock validation) and before Stock Allocation, Transaction Inquiry, editing/cancellation, Delivery Date Change and the GIN. [observed: group 11 chain]
- Saving an order also reserves its stock at once (automatic allocation), so booking is the step that commits stock to the outlet. [observed 2026-10-01 G11-1]
- G11-2: confirmed on a second day (2026-10-05): six orders saved by the Maker, each reserving its stock at save [observed 2026-10-05 G11-2].
- G11-3: third day (2026-10-06): six orders COL26000002015-2020 saved by the Maker, each reserving stock at save [observed 2026-10-06 G11-3].

## 2. Actors and roles
- Maker (formerly written "Order user") = **Auto_Multi_Orga** (framework login serial 35) on cnr1dev1; same session as the stock validation before it. [observed: TC-OB-01_executed.md; again observed 2026-10-01 G11-1, seq 10]
- No approval step exists for an order. [observed: none in chain; confirmed 2026-10-01 G11-1: six orders saved by the Maker, none needed a Checker]
- Checker: no role on this option. [observed 2026-10-01 G11-1]
- G11-2: Maker Auto_Multi_Orga booked all six orders of 2026-10-05; no Checker step [observed 2026-10-05 G11-2].
- G11-3: Maker Auto_Multi_Orga booked all six orders; no Checker step [observed 2026-10-06 G11-3].

## 3. Documents and master data
- Document: cash memo (order). Number shown as **Order Number** on the summary screen, format `COL` + 2-digit year + 9 digits, e.g. COL26000001995 .. COL26000002002 (8 orders, sequential). [observed] Live 2026-10-01: COL26000002003 .. COL26000002008 (6 orders, sequential, shown as Document No on "Order View - Header"). [observed 2026-10-01 G11-1]
- Document type of the saved order: Sales `CM-01` (status Ordered 04) [db]; Transaction Inquiry lists it under type "Sales" [observed]. The demand type "Demand Captured from Tele order" (type `2`, status PLACED 88) is a different document used for tele-orders [db][inferred].
- Master data used: Order Booker/Spot Seller, PJP (e.g. 02111-AutomationOB1), Selling Category (Selling Category 001, shown later as 201-Selling Category 001), Section (Automation_Testing_Section), Outlet (1000000001-Aautomation_Outlet_01 .. 08), products by code (62740537, 20050310, 62690363, 20050308, 69997598), price list / trade price, stock (ATP). [observed]
- The 8 workbook outlets differ in tax treatment (tax exempt / registration flags are in the outlet name); tax is 0 for outlets 05 and 06. [observed: ob_orders.json; reason inferred] (reason upgraded 2026-10-01: now [observed 2026-10-01 G11-1], was [inferred]: the outlet label carries the tax profile and Tax Exemption = Y gives tax 0, see section 8.)
- **Outlet tax profile is part of the Outlet Name label** [observed 2026-10-01 G11-1], e.g. "1000000004-...Outlet_04 Tax Exemption_N/Tax Registered_Reg/Tax Payer_Y/Advance Tax Exempti_N". Profiles seen: 04 = Exempt N / Reg / Payer Y / AdvExempt N; 05 = Exempt Y / Reg / Payer Y / AdvExempt Y; 06 = Exempt Y / Reg / Payer Y / AdvExempt N; 07 = Reg / Payer No / Exempt No; 08 = Exempt N / UnReg / Payer No; 11 = no profile in the label.
- PJP master: 8 booking PJPs offered to the Maker: AUTO241602-Auto917248, AutoPromo1-Auto Promo PJP OB, 7918624876-Aslam PJP OB, AutoPJGIN1-Auto GIN PJP OB, AUTO021311-Auto917248, AUTO061238-Auto917248, 02111-AutomationOB1, AUTO031026-Auto_test. [observed 2026-10-01 G11-1]
- Price master: the selling **Trade Price / Unit** differs from the Dispatch Advice purchase price for most SKUs (62740537 7711.465 both; 20050310 trade 234.09875/PC vs purchase 33.7865/PC; 62690363 16.0514 vs 15.4543; 20050308 87.6816 vs 118.9316; 69997598 12.7865 vs 51.6785; purchase > trade for some SKUs = data finding). [observed 2026-10-01 G11-1]
- Promotions (master data, definitions not read): Automation2 / Automation2-3, MARCH001, MARCH002, May001, May003 are applied to these orders; see transaction_inquiry.md (Total Offering). [observed 2026-10-01 G11-1]
- G11-2: orders **COL26000002009-2014** (sequential) on 2026-10-05 [observed 2026-10-05 G11-2].
- G11-3: orders **COL26000002015-2020** on 2026-10-06; PJP 02111 offered 43 outlets starting at 1000000004 (workbook outlets 01-03 still not offered) [observed 2026-10-06 G11-3].

## 4. Inputs: screens and fields
Menu: type "Order Booking", option `ORDER_BOOKING`; real path Transaction > Order > Order Booking. [db: mg 0001]
**Order Booking (header)**: Order Booker/Spot Seller (dropdown), PJP (dropdown), Selling Category (dropdown), Section (dropdown), Outlet Name (dropdown), Comments (text), Document Date, Reference Number (optional, framework field inactive). Dropdowns cascade in this order; category and section fill by themselves after PJP. [observed] (superseded 2026-10-01: with PJP 02111-AutomationOB1 the Selling Category did NOT fill by itself; its list had only "Selling Category 001" and had to be chosen, then Section offered only "Automation_Testing_Section" [observed 2026-10-01 G11-1].)
- Header defaults live 2026-10-01: Order Booker/Spot Seller default "Order Booker"; Document Date read-only = today (upgrades "Default Document Date = today [inferred]" below to [observed 2026-10-01 G11-1]). [observed 2026-10-01 G11-1]
- Outlet list for PJP 02111 / Selling Category 001 / Automation_Testing_Section: 43 entries, starting at 1000000004; workbook outlets 1000000001-03 are not offered (same as 2026-09-29). [observed 2026-10-01 G11-1; reason unknown]
**Order Detail** (after the `Order Detail` button): ProductDesc (type-ahead autoselect on product code/name), OrderCS (cases), OrderPC (pieces), read-only Trade Price, Gross Amount per line, ATP shown per product; buttons Add a row (`addBtn`), line Save (`rowEditBtn_Save_0`), Validation (`validateBtn`), Save (`saveBtn`), New Order (`newOrder`, confirm `continue`). [observed]
- Detail grid columns live 2026-10-01: Product Desc, Product Code, Batch, Current Stock (ATP) CS/DZ/PC, Trade Price / Unit, Order CS/DZ/PC, Gross Amount. DZ is skipped when tabbing (no dozen unit for these SKUs). Validation appears only after the first line; no totals are shown before saving. [observed 2026-10-01 G11-1]
**Order summary (Detail2)**: Gross Amount, Discount, Tax, Net Amount, Order Number (all read-only). [observed]
- Saved view live 2026-10-01 = **"Order View - Header"**: Document No, Outlet, Document Date, **Delivery Date** (read-only), PJP, Section (101010101101-Automation_Test...), Selling Category (201-Selling Category 001); header Gross, Discount, Tax, Net. Grid **"Cash Memo Details"**: Serial, Product, Batch, Stock Type, Trade Price/Unit, **Demand** CS/DZ/PC (as entered), **Order** CS/DZ/PC (normalised to cases), Gross, Discount, Tax, Net. [observed 2026-10-01 G11-1]
Mandatory fields: header fields block by **progressive disclosure, not by messages**: there is NO Validation button and no header message at all; the **Order Detail** button (id orderDetail) appears only after the Outlet is chosen; clearing Section, Selling Category or PJP (clear icon) clears every field below it and with Outlet empty there is no Order Detail button and no toast [observed 2026-10-01]. Validation (`validateBtn`) and Save appear only on the detail step after a product line exists. Default Document Date = today [inferred] (upgraded: [observed 2026-10-01 G11-1], was [inferred]).
Live cascade 2026-10-01: PJP AutoPromo1-Auto Promo PJP OB -> Selling Category AutoPromoSCG -> Section Auto Promo Section -> 15 outlets (Aautomation_Outlet_21..36); PJP 02111-AutomationOB1 offers Selling Category 001 only (no label with 201) and its outlet list starts at 1000000004 (1000000001 is not offered) [observed]. Order Detail opens /ngui/order-booking/order-fillter; header locked; New Order -> "Are You sure you want to cancel the order" Yes (id continue, resets the header) / No (id reject); the detail grid starts with an insert row (product type-ahead id product, batch, CS/DZ/PC order, row Save/Cancel); after cancelling an unsaved row the grid add-row icon (.dx-icon-edit-button-addrow) is needed for a new insert row [observed].
- The locked header shows Outlet Name blank on screen although the value is kept (display finding). [observed 2026-10-01 G11-1]

## 5. Process: the business steps in order
1. [Maker] Navigate to Order Booking. (`11:10:00010001:000101`)
2. [Maker] Choose Order Booker/Spot Seller = Order Booker; PJP; Selling Category; Section; Outlet Name; Enter Comments. The header becomes read-only after Order Detail is clicked. [observed] (`11:10:00010001`) Live 2026-10-01: PJP 02111-AutomationOB1, Selling Category 001 (chosen, not auto-filled), Automation_Testing_Section, outlet 1000000004 for workbook order 04. [observed 2026-10-01 G11-1]
3. [Maker] Click Order Detail; per product enter code, OrderCS, OrderPC; save the line (no toast on line save). [observed] **The product pick checks stock of the current day**: a product with no stock row for today gives the toast "Stock not available." and the row stays empty (20050310 on 2026-10-01, and every product before DA 1356 was approved); a product with stock fills the row: Batch 1-1, Current Stock (ATP) = Stock Inquiry closing (62740537: 4/0/0 CS/DZ/PC), Trade Price/Unit 7711.465, order quantity inputs 0, row Save/Cancel [observed 2026-10-01, nothing saved]. After a line Save a new insert row opens by itself. [observed 2026-10-01 G11-1] (`11:10:00010001`)
4. [Maker] Click Validation -> toast "Validation successfully"; a Save button appears. [observed] (Validation is replaced by Save. [observed 2026-10-01 G11-1]) (`11:10:00010001`)
5. [Maker] Click Save -> toast "Order Save successfully"; Order Number and totals shown. [observed] (Shown on "Order View - Header" with the Delivery Date. [observed 2026-10-01 G11-1]) (`11:10:00010001`)
6. [Maker] Click New Order (confirm "Are You sure you want to cancel the order": Yes) to start another. [observed] After a SAVED order New Order resets the header without a confirmation. [observed 2026-10-01 G11-1] (`11:10:00010001`)

## 6. Outputs and effects
- A cash memo with an Order Number, document status Ordered (04), execution status 02 "Confirmed" after booking and allocation, 03 "Planning completed" once it is on a GIN (the 8 orders on GIN 505 show "Planning completed" on 2026-10-01) [db + observed]. Delivery Date on the order = 2026-10-05 (copied from the PJP's next visit date, [inferred]; cancelled orders 1986 and 1993 still show 10-05, the 8 target orders show 2026-09-30 after Delivery Date Change [observed 2026-10-01]); Section 101010101101-Automation_Test..., Selling Category 201. [observed]
- (superseded 2026-10-01: orders booked on 2026-10-01 got **Delivery Date 2026-10-07**, not 10-05; 10-05 was the date for orders booked 2026-09-29. The delivery date is the PJP's NEXT visit after the booking day [inferred], it is not a fixed date.) [observed 2026-10-01 G11-1]
- Stock is **auto-allocated at save** (Allocation Status FULL); allocated orders appear in the Allocated tab of Order Stock Allocation. [observed] Confirmed again for all 6 orders of 2026-10-01. [observed 2026-10-01 G11-1]
- **Stock effect at save**: ATP drops by the ordered (normalised) quantity at each save: 62740537 ATP 261 -> 254 -> 247 -> 240 -> 233 -> 226 (7 CS per order). In Stock Inquiry: Allocated up and Closing down by the order quantity. [observed 2026-10-01 G11-1] (upgrades the earlier test hint "check ATP drops after save [inferred]".)
- Pieces are converted into cases: 5 CS + 4 PC became 7 CS (2 PC per case for that product). [observed] Live 2026-10-01: the view keeps **Demand** 5/0/4 (as typed) and shows **Order** 7/0/0 (normalised). [observed 2026-10-01 G11-1]
- Totals (workbook = observed): order 01 Gross 143,109.13, Discount -29,971.83, Tax 21,861.52, Net 134,999.00. Net = Gross + Discount + Tax (143,109.13 - 29,971.83 + 21,861.52 = 134,999.00). [observed]
- ATP per product equals the Stock Inquiry closing balance, so orders draw on stock received by the Dispatch Advice. [observed; live-verified 2026-10-01: ATP 4 CS for 62740537 = Closing 4 CS after DA 1356 was approved] Again 2026-10-01 after DA 1358: ATP 62740537 261, 20050310 5800/3, 62690363 6262/62, 20050308 2036/21, 69997598 2600/75 = Stock Inquiry closing; orders see stock received the same day. [observed 2026-10-01 G11-1]
- **Order 1 of 2026-10-01 (COL26000002003, outlet 1000000004, = workbook order 04 exactly)** [observed 2026-10-01 G11-1]:

| Line | Product | Demand | Order | Gross | Discount | Tax | Net | tax % of (gross+disc) |
|---|---|---|---|---|---|---|---|---|
| 1 | 62740537 | 5/0/4 | 7/0/0 | 107,960.51 | -22,610.53 | 15,363.00 | 100,712.97 | 18.0% |
| 2 | 20050310 | 5/0/0 | 5/0/0 | 18,727.90 | -3,922.25 | 2,665.02 | 17,470.67 | 18.0% |
| 3 | 62690363 | 3/0/2 | 3/0/2 | 9,855.56 | -2,064.08 | 1,873.23 | 9,664.70 | 24.0% |
| 4 | 20050308 | 2/0/10 | 2/0/10 | 6,488.44 | -1,358.90 | 1,322.08 | 6,451.63 | 25.8% |
| 5 | 69997598 | 0/0/6 | 0/0/6 | 76.72 | -16.07 | 10.92 | 71.57 | 18.0% |

Header: Gross 143,109.13, Discount -29,971.83, Tax 21,234.24, **Net 134,372.00** (line nets sum 134,371.54).

- **The 6 orders booked 2026-10-01** (all PJP 02111-AutomationOB1, Selling Category 001, Automation_Testing_Section, Delivery Date 2026-10-07, "Order Save successfully") [observed 2026-10-01 G11-1]:

| Order | Outlet (tax profile) | Lines | Gross | Discount | Tax | Net (line sum) |
|---|---|---|---|---|---|---|
| COL26000002003 | 1000000004 (Exempt N / Reg / Payer Y / AdvExempt N) | 5 (workbook 04) | 143,109.13 | -29,971.83 (20.94%) | 21,234.24 | 134,372.00 |
| COL26000002004 | 1000000005 (Exempt Y / Reg / Payer Y / AdvExempt Y) | 62740537 5/4, 20050310 5/0 | 126,688.41 | -25,527.68 (20.15%) | 0 | 101,160.73 |
| COL26000002005 | 1000000007 (Reg / Payer No / Exempt No) | same 2 lines | 126,688.41 | -25,527.68 (20.15%) | 18,208.93 (18%) | 119,369.65 |
| COL26000002006 | 1000000008 (Exempt N / UnReg / Payer No) | 62740537 5/4 (= workbook 08) | 107,960.51 | -16,264.08 (15.06%) | 16,505.36 (18%) | 108,201.79 |
| COL26000002007 | 1000000006 (Exempt Y / Reg / Payer Y / AdvExempt N) | 62740537 5/4 | 107,960.51 | -16,264.08 | 0 | 91,696.43 |
| COL26000002008 | 1000000011 (no profile in label) | 62740537 5/4 | 107,960.51 | -16,264.08 | 16,505.36 (18%) | 108,201.79 |

Later fate (other pages): 2003 edited after GIN, delivered; 2004/2005 delivered; 2006 rescheduled (Reattempt); 2007 cancelled after GIN; 2008 cancelled before GIN. [observed 2026-10-01 G11-1]

- **The 6 orders booked 2026-10-05** (same baskets and outlets as 10-01; "Order Save successfully" each; Delivery Date **2026-10-11**) [observed 2026-10-05 G11-2]:

| Order | Outlet | Lines | Net | Tax |
|---|---|---|---|---|
| COL26000002009 | 1000000004 | 5 | 134,372.00 (Gross 143,109.13, Discount -29,971.83, Tax 21,234.24) | 21,234.24 |
| COL26000002010 | 1000000005 | 2 | 101,160.73 | 0 (tax-exempt) |
| COL26000002011 | 1000000007 | 2 | 119,369.65 | 18,208.93 |
| COL26000002012 | 1000000008 | 1 | 108,201.79 | 16,505.36 |
| COL26000002013 | 1000000006 | 1 | 91,696.43 | 0 (tax-exempt) |
| COL26000002014 | 1000000011 | 1 | 108,201.79 | 16,505.36 |

- **Same amounts to the paisa as 2026-10-01** for the same baskets: prices, promotions and tax rules unchanged over four days (confirmed on a second day) [observed 2026-10-05 G11-2].
- ATP of 62740537 dropped by 7 CS per saved order: 325 -> 318 -> 311 -> 304 -> 297 -> 290; 325 = the Stock Inquiry Closing after the DA approval (Opening 308 + In 80 - Allocated 63 of the old GIN 505) [observed 2026-10-05 G11-2].
- The only difference to 10-01: Delivery Date 2026-10-11 instead of 10-07 (the PJP's next visit moved) [observed 2026-10-05 G11-2; "next visit" rule still inferred].
- Later fate: 2009 edited after the GIN (7 -> 4 CS), delivered, partly returned; 2010, 2011 delivered; 2012 rescheduled to 10-06 (Reattempt); 2013 cancelled after the GIN; 2014 cancelled before the GIN [observed 2026-10-05 G11-2].
- G11-3 order values [observed 2026-10-06 G11-3]:

| Order | Outlet | Gross / Discount / Tax / Net | vs sessions 1-2 |
|---|---|---|---|
| COL26000002015 | 1000000004 (5 lines) | 143,109.13 / -29,971.83 / 21,234.24 / 134,372 | same |
| COL26000002016 | 1000000005 (Exempt Y) | 126,688.41 / -25,527.68 / 0 / 101,161 | same |
| COL26000002017 | 1000000007 (Reg / Payer No / Exempt No) | 126,688.41 / -25,527.68 / **0** / 101,161 | **changed**: was Tax 18,208.93, Net 119,369.65 (Q-TX1) |
| COL26000002018 | 1000000008 (Exempt N / UnReg / Payer No) | 107,960.51 / -16,264.08 / 16,505.36 / 108,202 | same |
| COL26000002019 | 1000000006 (Exempt Y / Reg / Payer Y / AdvExempt N) | 107,960.51 / -16,264.08 / **16,505.36** / 108,202 | **changed**: was Tax 0, Net 91,696.43 (Q-TX1) |
| COL26000002020 | 1000000011 | 107,960.51 / -16,264.08 / 16,505.36 / 108,202 | same |

- G11-3: **outlets 06 and 07 have swapped tax behaviour** since 2026-10-05 (07 now untaxed, 06 now taxed) while the outlet labels still show the old profiles; the saved order views confirm the outlets [observed 2026-10-06 G11-3]. Cause unknown (outlet flag change or tax-rule change), Q-TX1. (superseded 2026-10-06: caused by **master-data modification of the outlets and of the tax promotion**, not a defect [stated 2026-10-06 QA Team Lead]; Q-TX1 answered.) Outlet 01's tax profile was changed during the group 66 walk (NTN, Registered / Tax Payer No) [stated 2026-10-06 session log pre-check], but outlet 01 is not offered on PJP 02111, so it did not affect this run.
- G11-3: delivery date of a 10-06 booking = **2026-10-12** [observed 2026-10-06 G11-3].
- G11-3: ATP of 62740537 at booking = 80 = today's DA quantity only (no carry-over; see Q-OB2) [observed 2026-10-06 G11-3].

## 7. Statuses and transitions
| from | action | to | by | tag |
|---|---|---|---|---|
| (none) | Validation + Save | Ordered (04) / shown "Confirmed" | Maker | [db][observed]; Confirmed right after booking re-observed [observed 2026-10-01 G11-1] |
| Ordered | Order Cancellation | Cancelled (03) | Maker | [db]; upgraded [observed 2026-10-01 G11-1] (was [db]): COL26000002008 shows Cancelled |
| Ordered | GIN approval + delivery | Delivered (01) | later areas | [db]; upgraded [observed 2026-10-01 G11-1] (was [db]): 2003-2005 show Delivered/Invoiced |
Details in order_lifecycle_and_statuses.md.

## 8. Rules and validations
- Validation must succeed before Save is offered. [observed]
- Reference Number must be unique per distributor: a repeat gives the duplicate message. [observed: ref 100]
- Header is locked after Order Detail; to change it, New Order discards the lines. [observed]
- Gross is recalculated when quantities change (change event + blur). [observed]
- Tax differs by outlet tax status. [observed]
- **Tax Exemption = Y -> Tax 0** (outlets 05 and 06; the Advance Tax Exempt flag makes no difference). Registered/unregistered and Tax Payer Y/N gave the same 18% on 62740537 in these orders (no extra tax for unregistered seen). [observed 2026-10-01 G11-1]
- **Tax is computed after discount** at a product-dependent rate: 18% (62740537, 20050310, 69997598), ~24% (62690363), ~25.8% (20050308). Tax = VAT + "3rd Schedule" charges; see transaction_inquiry.md (Total Tax). [observed 2026-10-01 G11-1]
- **Discount depends on the order composition** (basket promotions): 62740537 alone 15.06%; + 20050310 20.15%; all 5 SKUs 20.94%. Within one order the same % is spread pro rata over every line. [observed 2026-10-01 G11-1; promotion definitions not read]
- **Header Net is rounded to the whole rupee** (line nets 134,371.54 -> header 134,372.00); Gross, Discount and Tax keep 2 decimals. [observed 2026-10-01 G11-1]
- **PC above the case size is accepted at entry** and normalised on save (62740537: 4 PC with 2 PC/CS -> 5 CS 4 PC becomes 7 CS 0 PC). [observed 2026-10-01 G11-1]
- A product without a stock row for the day cannot be picked: "Stock not available." [observed 2026-10-01]. Quantity above available stock (ATP) is allowed or blocked: [unknown, not tried].
- Each saved order reserves (allocates) its stock immediately: ATP drops by the normalised quantity. [observed 2026-10-01 G11-1]
- Workbook orders 01-03 (outlets 1000000001-03) are not bookable on cnr1dev1 because the outlets are not offered. [observed 2026-10-01 G11-1; reason unknown]
- G11-2: confirmed on a second day: tax-exempt outlets 05/06 give Tax 0; header Net rounded to the rupee; basket-dependent discount; reservation at save [observed 2026-10-05 G11-2].
- G11-2: ATP can include reservations of old Pending documents carried into the day (Allocated 63 of GIN 505), so ATP < Opening + In [observed 2026-10-05 G11-2].
- G11-3: tax-exempt outlet 05 Tax 0 again; outlets 06/07 swapped (Q-TX1) [observed 2026-10-06 G11-3]. Do not assert tax for 06/07 from the outlet label alone.
- QA team 2026-10-08 (rule 8): the system **recalculates the invoice tax from the outlet's tax attributes**: Registered / Non-Registered, Tax Filer, Advance Tax Exempted, Tax Exempted [stated 2026-10-08 QA Team]. (Explains the outlet 06 / 07 swap after their master data changed, Q-TX1.)
- QA team 2026-10-08 (rule 9): ORGA parameter **ZERO_TAX_ORDER_EXEMPTION** decides whether zero-tax orders / invoices can be **delivered**: **Y** = allowed, **N** = delivery not allowed [stated 2026-10-08 QA Team]. (Refines the 2026-10-06 rule "a non-exempt outlet's zero-tax invoice cannot be delivered": the block applies when the parameter is N; how it interacts with the outlet's Tax Exempted flag was not stated.)
- QA team 2026-10-08 (Q16): an order quantity above the available stock is **accepted**; allocation takes only the available quantity; with no stock the order stays unallocated with Cash Memo status Order [stated 2026-10-08 QA Team].
- Promotions training 2026-10-07 (F16): a fixed-value or percentage promotion takes its budget at **order save** (the budget's Utilized goes up) [stated 2026-10-07 Syed Zulfiqar]; see [promotions_and_budget.md](../promotions_and_budget/promotions_and_budget.md) section 6. Not yet observed.
- Promotions training 2026-10-07 (F17-F19): for a **free-goods** promotion the free SKU's stock is checked and the promotion applies only once the order is Confirmed; if the free SKU is out of stock the order is still saved, without the free goods [stated 2026-10-07 Syed Zulfiqar]; meaning of "Confirmed" here: Q-PR9.
- Promotions training 2026-10-07 (F21): if the promotion's remaining budget is less than the discount, the promotion is **not applied at all** (no partial discount) [stated 2026-10-07 Syed Zulfiqar]; boundary cases in [promotions_and_budget.md](../promotions_and_budget/promotions_and_budget.md) section 11.
- Code study 2026-10-08 (promotion service, not observed): the budget is booked only when the order request carries `cashmemoEvent = S` (which order action sends it is S&D's choice, Q-PR11); a short balance is applied partially when org flag ALLOW_PARTIAL_BUDGET = Y (contradiction 36, Q-PR12); QTY1 / QTY2 are counted rounded down from pieces (30 pieces at 24 / case = 1 QTY1) [code UL-R1-BD@51e7e815 AllocationResolver.java:57-83] [code UL-R1-BD@51e7e815 PromotionAllocationService.java:141-179] [code UL-R1-BD@51e7e815 SnDRepositoryFiller.java:158-172]. <!--i-->

## 9. Messages
- "Validation successfully" (validate); "Order Save successfully" (save; framework key ORD_BOOK_SAVE_ASSR). [observed] Both re-observed on 6 orders. [observed 2026-10-01 G11-1]
- "Stock not available." (dx-toast-error, on product pick when the product has no stock row for the day) [observed 2026-10-01]; confirm dialog "Are You sure you want to cancel the order" (New Order) [observed].
- "Cashmemo with document reference number : 100 already exist." (duplicate Reference Number; atlas history also shows "Cashmemo Document Reference Number: 01 already exist."). [observed]
- Line Save: no message. New Order after a saved order: no confirmation. [observed 2026-10-01 G11-1]
- G11-2: "Order Save successfully" on each of the six orders [observed 2026-10-05 G11-2].
- G11-3: "Validation successfully", "Order Save successfully" on each order [observed 2026-10-06 G11-3].

## 10. Dependencies
Reads: stock from Dispatch Advice (same calendar day; stock balances are keyed by date), repos `g_REPO_ORGA`, `g_REPO_CMDOCTYPE`, `g_REPO_DISTRIBUTOR`, `REPO_REF_ORDER_NO`. Writes repo `ORDERNUMBER` used by Order Editing (seq 15, 29), GIN selection. Hands to: Stock Allocation, Transaction Inquiry, Order Editing/Cancellation, Delivery Date Change, GIN (see delivery area, by name).
- Date rule: the order's Delivery Date (next PJP visit, 2026-10-07 for a 10-01 booking) is later than today, so Delivery Date Change (seq 19) is needed before a same-day GIN. [observed 2026-10-01 G11-1]
- Stock received the same day (DA 1358 approved 10-01) is visible as ATP immediately. [observed 2026-10-01 G11-1]
- G11-2: Delivery Date of a 10-05 booking = 2026-10-11, so Delivery Date Change (seq 19) was again needed before the GIN [observed 2026-10-05 G11-2].
- G11-3: delivery date 2026-10-12 -> Delivery Date Change needed again, this time BEFORE seq 15 Order Editing (QA Team Lead) [observed 2026-10-06 G11-3].

## 11. Test design hints
- Positive: book one order with 5 products; check Gross/Discount/Tax/Net equal the workbook; check Order Number format; check ATP drops after save [inferred] (upgraded: [observed 2026-10-01 G11-1], ATP -7 CS per order of 62740537).
- Positive: pieces beyond a case (PC > pack size) convert to cases. (Confirmed: PC above the case size is accepted at entry; assert Demand 5/0/4 and Order 7/0/0. [observed 2026-10-01 G11-1])
- Negative: duplicate Reference Number; Save without Validation; no lines; zero quantity line; unknown product; header changed after Order Detail.
- Boundary: quantity = ATP and ATP + 1; CS 0 / PC 0 only; very large PC.
- Business effect: order is already Allocated after save; status Confirmed in Transaction Inquiry.
- Traps: line save has no toast so a TSTMSG assertion has nothing to assert; workbook Reference Number 100 collides on a second run; a green run proves the toast, not the stock effect.
- New case ideas 2026-10-01 [observed 2026-10-01 G11-1]:
  - Tax-exempt outlet (label Tax Exemption_Y, outlets 05/06) gives Tax 0 with the same lines that give 18% on a non-exempt outlet (compare 2004 vs 2005).
  - Basket-dependent discount: book the same SKU alone (15.06%), with a second SKU (20.15%) and with all 5 (20.94%); assert the discount changes and Total Offering sums to it.
  - Header Net rounding: assert header Net = round(sum of line nets) to the rupee (134,371.54 -> 134,372.00), not the raw sum.
  - Delivery Date assertion must not be a fixed date: it is the PJP's next visit (10-05 for a 09-29 booking, 10-07 for a 10-01 booking).
  - Stock effect: Stock Inquiry Allocated +order qty and Closing -order qty after save.
- Traps 2026-10-01: Selling Category may or may not auto-fill (it did not for 02111 today), so a flow that waits for it to fill breaks; workbook orders 01-03 use outlets that are not offered on cnr1dev1; the locked header shows Outlet Name blank (do not assert it there); discount % from the workbook only holds for the same basket. [observed 2026-10-01 G11-1]
- G11-2 additions [observed 2026-10-05 G11-2]:
  - Positive (regression): the six workbook-equivalent baskets give identical Gross/Discount/Tax/Net on any day while the price/promotion masters are unchanged (10-01 = 10-05).
  - Trap: the Delivery Date differs per booking day (10-05 for 09-29, 10-07 for 10-01, 10-11 for 10-05); never assert a fixed date.
  - Trap: ATP starts below Opening + In when an old Pending document still holds stock (325 = 308 + 80 - 63); derive expected ATP from Stock Inquiry Closing, not from the DA quantity.
- G11-3 (2026-10-06 ruling [stated 2026-10-06 QA Team Lead]): a booked zero-tax order of a NON-exempt outlet (like 2017, outlet 07) will be refused at delivery; book with the outlet's correct tax master data, or expect the block. 2017 was cancelled at seq 16, so the block was not seen.
- G11-3 trap: outlet tax behaviour can change between runs (06/07 swapped on 10-06); expected tax per order must come from the outlet's current tax profile, re-checked each run [observed 2026-10-06 G11-3].
- QA team 2026-10-08 additions [stated 2026-10-08 QA Team]:
  - Tax: derive the expected tax from the outlet's four tax attributes (Registered, Tax Filer, Advance Tax Exempted, Tax Exempted) as they are on the run day, not from the outlet label.
  - Zero-tax delivery: record ZERO_TAX_ORDER_EXEMPTION of the environment first; N -> a zero-tax invoice cannot be delivered; Y -> it can.
  - Boundary (Q16): qty = available -> FULL; available + 1 -> saved, partially allocated.

## 12. Open questions (batched for the BA)
- Q: Is quantity above ATP blocked, warned, or accepted as a backorder? | Default: blocked | Evidence: never tried.
- Q: What decides the order Delivery Date (PJP next visit)? | Default: next PJP visit date | Evidence: 2026-10-05 seen, rule not shown. (Update 2026-10-01 G11-1: 10-01 bookings got 2026-10-07, 09-29 bookings got 10-05, which supports "next PJP visit"; still [inferred], the PJP calendar was not read.)
- Q: Which fields are mandatory? | Default: all dropdowns except Comments and Reference Number | Evidence: header fields work by progressive disclosure (PARTLY answered 2026-10-01, Q18); the Validation messages of the detail step are still unread.
- ANSWERED 2026-10-01: which stock makes a product orderable = stock received by an approved DA for the current day; ATP = Closing today (net of allocation).
- Q: Why are outlets 1000000001-03 not offered for PJP 02111 (not on today's route? blocked?), and which order should the cycle use instead? | Default: use the next offered outlet (1000000004) | Class: C | Evidence: list starts at 1000000004 on 09-29 and 10-01 (related to Q-OE2). [observed 2026-10-01 G11-1]
- Q-OB1: Who or what generated the day's opening balances during 2026-10-01 (they were 0 in the morning, rebuilt from the previous day by 16:40)? This decides the ATP an order sees. | Default: unknown (someone may have clicked Generate Opening Balances) | Class: B | Evidence: session report §8; stock_inquiry_and_balances. **-> ANSWERED 2026-10-05**: openings are created by the first movement of the day (DA approval) = previous Closing + still-Allocated (see stock_inquiry_and_balances.md, OPEN_QUESTIONS.md).
- G11-2: Q (delivery date rule) gets a third data point (10-05 booking -> 10-11); still [inferred]. ANSWERED 2026-10-05 (Q-OB1): the day's openings come from the first movement (DA approval) = previous Closing + still-Allocated; ATP = Closing (see stock_inquiry_and_balances.md).
- Q-TX1 (new 2026-10-06): Why did outlets 1000000006 and 1000000007 swap tax behaviour between 2026-10-05 and 2026-10-06 (07 now Tax 0, 06 now 16,505.36), while their labels still show the old profiles: outlet flags changed (change-track approval?) or a tax-rule change? | Default: treat the current behaviour as the expectation; re-check per run | Class: C (QA lead) | Evidence: orders 2017 and 2019, seq 10 and seq 14 [observed 2026-10-06 G11-3]. **-> ANSWERED 2026-10-06** [stated 2026-10-06 QA Team Lead]: master-data modification of the outlets and the tax promotion (not a defect). Related rule: a zero-tax invoice of an outlet that is NOT tax-exempt cannot be delivered; a tax-exempt outlet's zero-tax invoice is allowed (see cashmemo_reschedule_and_status.md). Delivery date rule: fourth data point (10-06 -> 10-12) [observed].
- **Q16 ANSWERED 2026-10-08** [stated 2026-10-08 QA Team]: quantity above available stock is accepted; only the available quantity is allocated; none available -> unallocated, status Order.

## 13. Sources
learning_block2a.json (L14), learning_block3b.json (S3), LIVE_FINDINGS.md; framework_atlas/flows/00010001.md/.json; group_11.md; framework_flows/TC-OB-01_executed.md, ob_orders.json; DB `snd_tr_cmm_cashmemo_master`, `snd_pr_dot_documenttype`, `snd_pr_dos_documentstatus` (org 010104); step_labels (qaos_steps.py labels "Order Booking").
- Live learning session G11-1 (2026-10-01, cnr1dev1, distributor 15108843): `learning_sessions/2026-10-01_G11-PK_session1_log.md` seq 10 (also seq 16, 29, 31, 33 for the later fate of the orders); `learning_sessions/2026-10-01_G11-PK_session1_report.md` §3 rules 3, 8, 9 and §8.
- G11-2: learning_sessions/2026-10-05_G11-PK_session2_log.md (seq 10).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 10, 14).

- QA team written answers 2026-10-08: learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx) (rules 8, 9; Q16).
