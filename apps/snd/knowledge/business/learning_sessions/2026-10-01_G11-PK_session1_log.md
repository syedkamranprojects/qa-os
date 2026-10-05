# Session log: LEARN-G11-PK/20261001-1611 (learning walk, segments 1-3)

Env cnr1dev1, company Unilever Pakistan Limited, distributor 15108843 IBRAHIM TRADERS (shown "Auto KARACHI").
Business facts only; no element ids recorded as knowledge.

## Deviations
- Seg 1 planned as Automation; the QA lead logged in as **Auto_Multi_Orga** (16:20). Recorded as stated by the QA lead; Automation not exercised.
- Home page content area showed a Kaspersky "untrusted certificate" notice; ignored per QA lead; navigation via the top-left hamburger menu works.

## Segment 1: Maker (Auto_Multi_Orga)

### seq 1 Login Dcode (021400000): done 16:20
- After SSO login: **Company** page (options: Unilever Pakistan Limited, Unilever Bangladesh Limited -Bangla) -> Proceed -> **Distributor** page (options for this user: 125555555-Aqua Distlocation, 15108843-IBRAHIM TRADERS, 15178537-GNY ENTERPRISES, 18011494-Muhammad Akram Traders, 50250327-MULLER & PHIPPS (KORANGI - KARACHI), 956783323-Global user location) -> Proceed -> Home (menu). [observed]

### seq 2 Dispatch Advice (00100001): done, DA **1358** forwarded 16:3x
Navigation: hamburger -> Search "Dispatch Advice" -> Transaction > Primary Sale > Dispatch Advice (also offered: "Dispatch Advice NUP", "Dispatch Advice II").

Header (new form defaults) [observed]:
- Mandatory: Document No (ro, generated), Document Date (ro, today), Warehouse*, Vendor Code*, DA Type*.
- Defaults on a fresh screen: Warehouse = **0000000025-IBT Main warehouse** (not Auto Main), Vendor Code = UPL WH, DA Type = Dispatch Advice, Invoice Due Date = Reference Date = today, Stock Arrival = now (date-time), Document Status Un-Authorized, Status In-Active, Approval Status Draft. Received Date read-only and empty.
- Warehouse list: 45 warehouses (IBT Main, Auto Main C0000000055, ~41 named "Automation", SAN Warehouse A/B).
- Entered: Warehouse C0000000055-Auto Main Warehouse, SO Automation_01-10-2026, Shipment 123, Deliver 12312, Tax Invoice 123, Comments Positive_QA_Learning_01, Reference No 1115.
- Save -> **"Saved successfully"**, Document No 1358. Buttons after save: Add/Update/Delete/Forward enabled, Save/Reject disabled. Forward is enabled with zero lines (negative case to test later: forward a DA without lines).

Lines (Dispatch Detail tab) [observed]:
- Tab repeats header summary (DA No, DA Date, Reference No, Tax Invoice Number, Invoice Number). Grid "DA Detail" with "+" to add a line; new line is inserted at the TOP.
- Columns: Product, Stock Type, Batch, Purchase Price / PC, Dispatch CS/DZ/PC, Loss (+), Received CS/DZ/PC, Gross Amount, Discount, Tax Amount, Net Amount, Picked By.
- Product type-ahead shows "code-description-price"; picking it fills Stock Type = Sound, Batch = 1-1, Purchase Price / PC. **The price in the product label is not always the purchase price** (20050310 label 31.25, purchase price 33.79; 62690363 label has no price, purchase price 15.45; 62740537 7711.47 both).
- Purchase price is held with 8 decimals (e.g. 7711.46500000) and shown rounded to 2; amounts use the precise price.
- Gross = Received qty (in PC) x purchase price / PC; Discount 0, Tax 0, Net = Gross for every line.
- Line save -> **"Saved Successfully!"** (capital S, exclamation; differs from header "Saved successfully").
- Loss window "DA Loss Details": own grid Stock / Loss Reason / CS / DZ / PC, "+" to add, row Save/Cancel (no message), **Calculate** pushes the losses to the line.
  - Loss Stock options: Damaged, Expired, SEP, Lost, **Lost (listed twice)**, Behalf 615, Variance (duplicate "Lost" = master-data finding).
  - Loss Reason options: Area Closed, Order Change, Customer cancels delivery, On Customer Behalf.
  - Several loss rows per line are summed into one Loss figure (4 Damaged + 2 Lost = 6-0-0), Received = Dispatch - Loss, amounts recomputed on Received.

| # | Product | Disp CS | Loss | Recv CS | Net PKR |
|---|---|---|---|---|---|
| 1 | 62740537 RAFHAN SLPC OILS CORN TIN 2X10L | 80 | 0 | 80 | 1,233,834.40 |
| 2 | 20050310 BLUEBAND MARGARINE 16X500G | 70 | 6 (Damaged 4 Area Closed, Lost 2 On Customer Behalf) | 64 | 34,597.38 |
| 3 | 62690363 SURF EXCEL HS 204X35G | 60 | 5 (Damaged 5 On Customer Behalf) | 55 | 173,397.25 |
| 4 | 20050308 BLUE BAND MARGARINE 32X250G | 50 | 0 | 50 | 190,290.50 |
| 5 | 69997598 KNORR CKN CUBE 288X18G | 40 | 0 | 40 | 595,336.32 |
DA net (header/grid): **PKR 2,227,455.842**, Tax 0, Discount 0.

Forward [observed]:
- Returning to Header Info resets the form to a blank new DA; the DA must be reopened from the grid (Show filter row -> Document No).
- The grid's Warehouse column shows "Auto KARACHI" (distributor name), not the warehouse.
- Forward -> "Comments" window (mandatory text) -> Save -> **"Forwarded successfully"**. Form keeps showing Draft until reopened; reopened: Status In-Active, **Approval Status Pending for approval**, Document Status Un-Authorized, Received Date empty.
- **Finding:** on the Pending DA the Maker still has **Forward and Reject enabled** (Add also). Not clicked. On the GIN (2026-10-01) the Maker's Forward/Reject were disabled on a Pending document. Question for the BA / possible defect: can the Maker approve or reject their own DA?

### Stock Inquiry BEFORE DA 1358 approval (16:4x, Balance Date 2026-10-01, Period DAILY, Category/Brand All)
Filters: Period Type* (DAILY), Balance Date, Category, Brand; buttons Show Inquiry, Generate Opening Balances (not clicked). 39 rows, 3 pages of 15.
Columns: Category, Brand, Product Name (code - name - price), Warehouse, Batch, Stock Type, Opening/In/Out/Allocated/Closing each CS/DZ/PC.
**New fact:** today's rows now have Opening balances (this morning a new day started at Opening 0). 62740537 Auto Main: Opening 160 = 09-30 closing 97 + 09-30 allocated 63, so openings appear rebuilt from the previous day with allocation released [observed; who/what generated them unknown: someone may have clicked Generate Opening Balances during the day].

| Product @ Auto Main Warehouse, Sound | Opening CS/PC | In | Allocated CS/PC | Closing CS/PC |
|---|---|---|---|---|
| 62740537 | 160/0 | 84 (DA 1356 4 + DA 1357 80) | 63/0 | 181/0 |
| 20050310 | 5751/3 | 70 | 85/0 | 5736/3 |
| 62690363 | 6200/94 | 60 | 53/32 | 6207/62 |
| 20050308 | 1978/21 | 50 | 39/96 | 1986/21 |
| 69997598 | 2560/171 | 0 | 0/96 | 2560/75 |
Expected after approval: In +80 / +64 / +55 / +50 / +40 (received, not dispatched); no Damaged/Lost rows expected while the loss record is pending.
Menu note: after clicking a menu item the side menu stays open; click the hamburger once to close it (else it covers the page buttons).

## Segment 2: Checker (Auto_Tssm), logged in by the QA lead ~16:55
- After login Auto_Tssm landed directly on the menu: no Company / Distributor pages were shown in the browser (single org/distributor for this user, or chosen by the QA lead) [observed; cause unknown].

### seq 5 Dispatch Advice Approval (00740001): done, DA 1358 approved
- Same screen as the Maker (Transaction > Primary Sale > Dispatch Advice). A Checker opening it sees a blank new-DA form with Save enabled (a Checker cannot actually create a DA: "Current user is not authorized to save this record!", 2026-09-29).
- Reopen DA 1358 from the grid (Show filter row, Document No): Pending for approval; Checker buttons Add, Forward, Reject enabled (no Terminate button on this screen) - **same button set the Maker had on the Pending DA**.
- Forward -> Comments (mandatory) "Automation Approval" -> Save -> **"Forwarded successfully"**.
- After approval: Received Date = 2026-10-01 (set by the approval), Status **Active**, Approval Status **Approved**, Document Status **Authorized**, Net unchanged 2,227,455.842; all fields read-only; only Add enabled. [observed]

### seq 7 Dispatch Advice Loss Approval (00760001): done, loss record 639 approved
- Menu: Transaction > Loss Approval (search "Loss Approval"). Screen "Loss Approval Master": grid Serial No, Document Type, Document No, Distributor Code, Distributor Name, Status (74 pages of history; default order is not by serial: 372 first, then 1, 2, 3..., so "click first row" depends on sorting = framework drift risk: the framework clicks the Serial No header then row 1).
- Filter Document No 1358 -> **Serial 639**, DA-01 -Dispatch Advice, 15108843 Auto KARACHI, Pending for approval. ONE loss record per DA (created at the DA approval; serial +1: 638 -> 639).
- Form: Serial No, Document No, Document Type (blank form shows "NTN"), Status. Buttons: Forward ON, **Reject OFF** for the Checker on a Pending loss record (on the DA itself Reject was ON).
- Tab "Loss Approval Detail": one row per product AND loss stock type: Product, SKU Type, Dispatch CS/DZ/PC, Received CS/DZ/PC, Loss CS/DZ/PC:
  - 20050310 | 02 (Damaged) | 70 | 64 | loss 4
  - 20050310 | 04 (Lost) | 70 | 64 | loss 2
  - 62690363 | 02 (Damaged) | 60 | 55 | loss 5
  The loss reason is not shown here. SKU type codes: 02 = Damaged, 04 = Lost [observed].
- Forward -> Comments "Automation Approval" -> Save -> **"Forwarded successfully"**; grid Status **Approved** (form shows Pending until reopened); both buttons then disabled.
- Effect of the approved loss on stock: to be checked at seq 9 (before snapshot had no 02/04 rows for 20050310 or 62690363).

## Segment 3: Maker (Auto_Multi_Orga), logged in by the QA lead ~17:05 (Company + Distributor pages shown again)

### seq 9 Stock Validation After DA PAK (02800001): done
- Framework: Stock Inquiry with Period DAILY / Balance Date / Category All / Brand All, filter 62740537 + Auto Main Warehouse + 01 - Sound, assert **absolute** In CS = 80. On a day with earlier DAs this fails (today In = 164): the check assumes a clean day [observed trap].
- AFTER DA 1358 + loss 639 approval (Balance Date 2026-10-01, 39 rows, unchanged count):

| Product @ Auto Main, Sound | In before -> after | Closing before -> after | delta |
|---|---|---|---|
| 62740537 | 84 -> 164 | 181 -> 261 | +80 |
| 20050310 | 70 -> 134 | 5736/3 -> 5800/3 | +64 (= 70 dispatched - 6 loss) |
| 62690363 | 60 -> 115 | 6207/62 -> 6262/62 | +55 (= 60 - 5) |
| 20050308 | 50 -> 100 | 1986/21 -> 2036/21 | +50 |
| 69997598 | 0 -> 40 | 2560/75 -> 2600/75 | +40 |
- **The DA approval adds exactly the RECEIVED quantity to Sound stock (In and Closing), on the Received Date** [observed].
- **The approved loss creates NO stock row**: no 02 Damaged / 04 Lost rows for 20050310 or 62690363 after loss 639 was approved; row count stays 39 [observed]. Closes checklist L21: approving a DA loss has no Stock Inquiry effect (it is a record/claim only, as far as stock is concerned).

### seq 10 Order Booking (00010001): order 1 = **COL26000002003** (outlet 1000000004), 17:2x
Header [observed]: Order Booker/Spot Seller (default "Order Booker"), PJP, Selling Category, Section, Outlet Name, Document Date (ro, today), Comments, Reference Number.
- PJP list (8): AUTO241602-Auto917248, AutoPromo1-Auto Promo PJP OB, 7918624876-Aslam PJP OB, AutoPJGIN1-Auto GIN PJP OB, AUTO021311-Auto917248, AUTO061238-Auto917248, **02111-AutomationOB1**, AUTO031026-Auto_test.
- 02111-AutomationOB1 -> Selling Category list has only "Selling Category 001" (did NOT auto-fill this time) -> Section only "Automation_Testing_Section" -> Outlet list 43 entries. **Workbook outlets 1000000001-03 are not offered** (list starts at 1000000004; same as 09-29) -> workbook orders 01-03 cannot be booked as written [observed; reason unknown: not on today's route? blocked?].
- **Outlet labels carry the outlet's tax profile**, e.g. "1000000004-...Outlet_04 Tax Exemption_N/Tax Registered_Reg/Tax Payer_Y/Advance Tax Exempti_N"; 05 = Exemp_Y/Reg/Payer_Y/AdvExempt_Y; 06 = Exemp_Y/Reg/Payer_Y/AdvExempt_N; 07 = Reg, Payer No, Exemp No; 08 = Exemp_N/UnReg/Payer No. This explains the workbook's different Tax per order (orders 05/06 Tax 0).
- The Order Detail button appears only when the Outlet is chosen; clicking it locks the header (locked header shows Outlet Name blank on screen though the value is kept) and opens /order-booking/order-fillter with an insert row.
Detail [observed]: columns Product Desc, Product Code, Batch, Current Stock (ATP) CS/DZ/PC, Trade Price / Unit, Order CS/DZ/PC, Gross Amount.
- ATP = Stock Inquiry closing (62740537 261, 20050310 5800/3, 62690363 6262/62, 20050308 2036/21, 69997598 2600/75): orders see stock received today.
- **Selling trade price differs from the DA purchase price**: 62740537 7711.465 both; 20050310 trade 234.09875/PC vs purchase 33.7865/PC; 62690363 16.0514 vs 15.4543; 20050308 87.6816 vs 118.9316; 69997598 12.7865 vs 51.6785 (price-master observation, purchase > trade for some SKUs).
- DZ is skipped when tabbing (no dozen unit for these SKUs). PC above the case size is accepted at entry (62740537: 4 PC with 2 PC/CS).
- Line Save: no message; a new insert row opens by itself. Validation (appears after the first line) -> **"Validation successfully"** -> Validation is replaced by **Save** -> **"Order Save successfully"**; no totals are shown before saving.
- Saved view "Order View - Header": Document No COL26000002003, Outlet, Document Date 2026-10-01, **Delivery Date 2026-10-07** (ro; orders booked 09-29 got 10-05: delivery date = next PJP visit [inferred]), PJP, Section 101010101101-Automation_Test..., Selling Category 201-Selling Category 001. Grid "Cash Memo Details": Serial, Product, Batch, Stock Type, Trade Price/Unit, **Demand** CS/DZ/PC (as entered), **Order** CS/DZ/PC (normalised: 5 CS 4 PC -> 7 CS 0 PC), Gross, Discount, Tax, Net.

| Line | Product | Demand | Order | Gross | Discount | Tax | Net | tax % of (gross+disc) |
|---|---|---|---|---|---|---|---|---|
| 1 | 62740537 | 5/0/4 | 7/0/0 | 107,960.51 | -22,610.53 | 15,363.00 | 100,712.97 | 18.0% |
| 2 | 20050310 | 5/0/0 | 5/0/0 | 18,727.90 | -3,922.25 | 2,665.02 | 17,470.67 | 18.0% |
| 3 | 62690363 | 3/0/2 | 3/0/2 | 9,855.56 | -2,064.08 | 1,873.23 | 9,664.70 | 24.0% |
| 4 | 20050308 | 2/0/10 | 2/0/10 | 6,488.44 | -1,358.90 | 1,322.08 | 6,451.63 | 25.8% |
| 5 | 69997598 | 0/0/6 | 0/0/6 | 76.72 | -16.07 | 10.92 | 71.57 | 18.0% |
Header: **Gross 143,109.13, Discount -29,971.83, Tax 21,234.24, Net 134,372.00 = workbook order 04 exactly** [observed].
- Discount = the same 20.94% on every line (order-level promotion spread pro rata). Tax is computed after discount at a product-dependent rate (18% / ~24% / ~25.8%).
- **Header Net is rounded to the whole rupee** (line nets sum 134,371.54 -> 134,372.00).

#### Orders booked (all PJP 02111-AutomationOB1, Selling Category 001, Automation_Testing_Section, Delivery Date 2026-10-07, "Order Save successfully")
| Order | Outlet (tax profile) | Lines | Gross | Discount | Tax | Net (line sum) |
|---|---|---|---|---|---|---|
| COL26000002003 | 1000000004 (Exempt N / Reg / Payer Y / AdvExempt N) | 5 (workbook 04) | 143,109.13 | -29,971.83 (20.94%) | 21,234.24 | 134,372.00 |
| COL26000002004 | 1000000005 (Exempt Y / Reg / Payer Y / AdvExempt Y) | 62740537 5/4, 20050310 5/0 | 126,688.41 | -25,527.68 (20.15%) | **0** | 101,160.73 |
| COL26000002005 | 1000000007 (Reg / Payer No / Exempt No) | same 2 lines | 126,688.41 | -25,527.68 (20.15%) | 18,208.93 (18%) | 119,369.65 |
| COL26000002006 | 1000000008 (Exempt N / UnReg / Payer No) | 62740537 5/4 (= workbook 08) | 107,960.51 | -16,264.08 (15.06%) | 16,505.36 (18%) | 108,201.79 |
| COL26000002007 | 1000000006 (Exempt Y / Reg / Payer Y / AdvExempt N) | 62740537 5/4 | 107,960.51 | -16,264.08 | **0** | 91,696.43 |
| COL26000002008 | 1000000011 (no profile in label) | 62740537 5/4 | 107,960.51 | -16,264.08 | 16,505.36 (18%) | 108,201.79 |
Rules learned [observed]:
- **Tax Exemption = Y -> Tax 0** (Advance Tax Exempt flag makes no difference). Registered/unregistered and tax payer Y/N gave the same 18% on 62740537 in these orders (no extra tax for unregistered seen).
- **Discount depends on order composition**: 62740537 alone 15.06%; + 20050310 20.15%; all 5 SKUs 20.94% (multi-SKU / basket promotion) [observed; promotion definition not read].
- **ATP drops by the ordered (normalised) quantity at each save**: 62740537 ATP 261 -> 254 -> 247 -> 240 -> 233 -> 226 (7 CS per order) = automatic allocation at save.
- Workbook orders 01-03 (outlets 1000000001-03) are not bookable on cnr1dev1 (outlets not offered).
- New Order after a saved order resets the header without a confirmation.

### seq 12 Stock Allocation (00130001): done, no-op
- Menu "Order Stock Allocation" (search "Stock Allocation"); Order Date (today) and PJP Number (02111~AutomationOB1) preselected; tabs Unallocated / Allocated; Allocation button on Unallocated, Unallocate on Allocated.
- **Unallocated tab empty**: all 6 orders already FULL (auto-allocated at save). Allocated grid: Description (distributor), Document No, Outlet Code, Outlet Name, Document Date, Delivery Date, Net Amount (rounded), Section, Demand Channel "Back Office (BO)", Allocation Status FULL. The manual allocation step only matters for orders that did not get stock at booking [inferred].

### seq 14 Transaction Inquiry Validate after OB (02960001): done (COL26000002003)
- Filters: Document Type (default "Demand Captured from Tele order"; chose Sales), Document Status All, PJP Number All, Document Date From/To (today), SKU All; Refresh. 7 Sales docs today (2 pages of 5).
- Right after booking: Document Status **Confirmed**, Order Booker/Delivery Man "AutomationOB / AutomationQADSR" (delivery man assigned at booking), PJP 02111, Order Time, Delivery Date 2026-10-07, Actual Delivery Date empty, Offset 0, GIN No empty, Net rounded to the rupee.
- Row buttons: Detail, Product Wise Discount (disabled), Product Wise Free Quantity (disabled), Total Offering, Total Tax, Credit Note Adjustments.
- **Detail**: per line Trade Price/Unit, **Delivered** CS/DZ/PC (empty before delivery), Gross, Discount, Tax, Net, **Allocated** CS/DZ/PC (normalised, e.g. 7/0/0) and **Ordered** CS/DZ/PC (as typed, 5/0/4). The product label here carries a third price (62740537 8135.595, ~5.5% above trade price; retail price? [inferred]).
- **Total Offering** (promotions applied to the order): Automation2 / Automation2-3 / BONUS2 -14,310.91; MARCH001 BONUS2 -650; MARCH002 TRADEOFFER -14,310.91; May001 BONUS2 -650; May003 BONUS2 -50; Tax Amount 0 each. Sum = -29,971.83 = header discount. Two promotions are each exactly 10% of gross (14,310.91 = 10% x 143,109.13) plus three fixed amounts [observed]; that is why the discount % changes with the basket.
- **Total Tax** (charges): 0001 - Value Added Tax (TAX) 18,038.93; **9000 - 3rd Schduele (sic)** (TAX) 3,195.31; sum 21,234.24 = header tax. Third-Schedule products are taxed on retail price, explaining the higher effective tax on 62690363 / 20050308 [inferred from Pakistani tax practice + observed amounts].

### seq 15 Order Editing (00020001): **SKIPPED by the QA lead (17:4x) - to be discussed with the QA/BA team**
What was learned before the skip [observed]:
- Menu Transaction > Order Editing (search "Order Editing"; also "Order Editing HQ" exists). Hand-coded page /ngui/order-editing.
- Filters: PJP (opens preselected with the FIRST PJP AUTO241602~Auto917248, with Selling Category and Section filled), Selling Category, Section, Outlet Name, **Date From / Date To (default today)**, SKU.
- Changing the PJP clears Selling Category, Section and Outlet (cascade). Labels differ from Order Booking: PJP "02111~AutomationOB1", Selling Category "201-Selling Category 001", Section "101010101101-Automation_Testing_Section".
- **Date From/To filter the DELIVERY date**, not the order date (API calls use strDlvDateFrom/strDlvDateTo and dateFrom/dateTo): with the default (today) an order booked today for delivery 2026-10-07 can never appear -> **explains the empty Outlet list of 2026-09-29** ("No data to display"). Date To must cover the order's delivery date (10-07).
- Order list API: order-service cashmemo/getOultetsForOrderEditing (outlets), cashMemoDetail/getSKUForOrderEditing, cashmemo/gridDataCMEditing.
- The PJP dropdown selection is fragile: the display showed 02111~AutomationOB1 while the request used AUTO031026 (the next item); after that the cascade blanked all filters.
Not done: the edit itself (workbook: outlet 1000000004 = COL26000002003, line 62740537 -> 4 CS 0 PC, reason "Order Change QTY"; expected Gross 96,840.34, Discount -20,718.07, Tax 14,584.79, Net 90,707.00; messages "Validation successfully", "Order Save successfully").
Downstream impact: seq 70 (TI after Order Editing) and seq 68 (edited-order charges/tax) have no edited order from seq 15; seq 29 (Order Editing After GIN) uses the same screen and the same date rule.
Questions for the QA/BA team:
- Q-OE1: Is the Order Editing date range meant to be the delivery date? Should the default be the PJP's next delivery date rather than today?
- Q-OE2: Which order should the cycle edit when workbook outlets 1000000001-03 are not offered on cnr1dev1?

### seq 16 Order Cancellation R2 TH (00040001): done, **COL26000002008 cancelled** (QA lead chose the order), ~17:55
- Menu Transaction > Order Cancellation (layout 202022, studio page). Opens with PJP* 02111 - AutomationOB1 preselected, **Date From* / Date To* = today, and here they filter the ORDER (document) date** (today's orders listed; contrast Order Editing, where the dates filter the delivery date). Section preselected; Outlet Name preselected with the first outlet that has an open order (1000000004).
- Outlet list = only outlets with open (cancellable) orders: 04, 11, 08, 05, 07, 06.
- Grid: checkbox, Document No., Document Date, Delivery Date, Net Amount, Outlet Name, Demand Channel, **Cancellation Reason** (in-grid dropdown). Buttons: **Cancel All**, Refresh.
- Cancellation Reason options: Bad Weather, Credit Exceeded, Law & order Issue, Shop Closed. Chose Shop Closed (workbook).
- Tick the row checkbox -> Cancel All -> result window **"Order Cancellation Status"** (Index No, Doc No, Status, Message): COL26000002008 | **Successfull** (sic) | **Order Cancelled Successfully**. No toast. closeBtn closes it; the order disappears from the list.
- Workbook expects outlet 1000000007 / Net 134,535 (workbook order 07) - not used (QA lead chose 2008).
- **Effect on stock** [observed, Stock Inquiry 2026-10-01 Auto Main, after 6 orders booked and 1 cancelled]: Allocated 62740537 63 -> 98 (= 63 + 5 orders x 7 CS; the cancelled order's 7 CS released), Closing 261 -> 226; 20050310 Allocated 85 -> 100 (+3 x 5 CS), Closing 5800/3 -> 5785/3; 62690363 53/32 -> 56/34 (+3/2); 20050308 39/96 -> 41/106 (+2/10); 69997598 0/96 -> 0/102 (+6 PC). **Booking reserves stock immediately (Allocated up, Closing down); cancellation releases it.** Closing = Opening + In - Out - Allocated holds.

### seq 18 Stock Unallocation (00130002): done on ONE order (QA lead option 1), then re-allocated, ~18:0x
- Order Stock Allocation > Allocated tab: 5 orders FULL. Ticked only COL26000002007 (the row checkbox is not clickable itself; click its cell) -> Unallocate -> browser confirm **"Are you sure you want to proceed?"** (accepted) -> toast **"Process completed successfully"** (on 2026-09-29 the same action answered "stock not found." - not reproduced today). 2007 left the Allocated tab and appeared on the Unallocated tab (columns: Description, Document No, Outlet Code, Outlet Name, Document Date, Delivery Date, Net Amount, Section, Demand Channel; no Allocation Status column).
- Framework drift: the framework selects ALL rows (filter "Aautomation", select-all) and unallocates everything right before the GIN; done as written it would leave the GIN with no allocated cash memos [QA lead chose one order].
- Re-allocation (exercises seq 12 manual Allocation): Unallocated tab -> tick 2007 -> **Allocation** -> same confirm -> **"Process completed successfully"** -> 2007 back on Allocated, FULL. All 5 orders (2003-2007) FULL.
- Stock effect of unallocate/re-allocate not snapshotted (same mechanism as the cancellation, which released 7 CS) [inferred].

### seq 19 Delivery Date Change (00160001): done, 5 orders moved 2026-10-07 -> 2026-10-01
- Menu Transaction > Delivery Date Change (layout 201080). Opens with Order Date = today, Delivery Date (the NEW date) = today, PJP Number = first PJP (AUTO241602~Auto917248). Only button: Process.
- PJP 02111~AutomationOB1 -> grid lists the PJP's open orders of that order date: checkbox, Cashmemo No, Outlet Name, Status (Confirmed), Document Date, Amount FCY, PJP Number 02111, **PJP Delivery No 02112** (the delivery route is a separate PJP), Delivery Date 2026-10-07, Demand Channel "01 - Back Office (BO)". The cancelled order is not listed.
- Header checkbox selects all -> Process -> confirm "Are you sure you want to proceed?" -> toast **"Delivery Date has been changed successfully, processed orders: 5"**; grid Delivery Date now 2026-10-01, status still Confirmed.
- Business meaning: an order booked today is planned for the PJP's next delivery visit (10-07); Delivery Date Change pulls it forward to today so the GIN can issue it today (GIN refuses cash memos with a delivery date earlier than the PJP working date; same-day issue needs delivery date = today) [observed + earlier finding].

### seq 20 Goods Issue Note (00050001): done, **GIN 506** created and forwarded (Pending for approval)
- Menu Transaction > Goods Issue Note (/ngui/good-issue-notes/GIN). Tabs Header / Cash Memo Selection / Detail; buttons Add, Forward, Reject, Terminate. Master grid: GIN No., GIN Date, Warehouse, Delivery Man, Vehicle, Approval Status, Status, SR Document No., Suggested Type (505 of 09-30 still Pending for approval).
- Add -> Header: GIN No. (generated), GIN Date (today), Delivery Man PJP, Delivery Man DSR, Warehouse, Vehicle, Suggested Type (default Cashmemo List), Status, Delivery Date, Approval Status. Cash Memo Selection and Detail tabs are disabled until Delivery Man PJP + Delivery Date are set.
- Delivery Man PJP options (6): AutoPJGIN2-Auto GIN PJP DM, AUTO301301-Auto_test, **02112-AutomationDSR**, AUTO301258-Auto_test, AutoPromo2-Auto Promo PJP DM, 8197298470-Aslam PJP DM. Picking 02112 fills DSR ITB0189-AutomationQADSR, Warehouse C0000000055-Auto Main Warehouse, Vehicle **0040-Automation211206** (workbook expects "74 - Sect to Locus": vehicle default changed). Delivery Date typed 2026-10-01.
- Cash Memo Selection: grid Doc. Date, Doc No, Outlet Name, DSR Name (= order booker ITB0190-AutomationOB), Order Type 01-Back Office (BO), Order Booker PJP 02111-AutomationOB1, Delivery Man PJP 02112-AutomationDSR, Section. **Exactly the 5 orders whose delivery date = the GIN delivery date** (2003-2007; cancelled 2008 absent). Header checkbox selects all -> Detail tab enabled.
- Detail = **aggregated per SKU over the selected cash memos**: SKU Nature (Sales), SKU Description, Stock Type, SKU Code, Batch, Current Stock (= Stock Inquiry closing), Suggest CS/DZ/PC (= sum of order quantities), Actual CS/DZ/PC (defaults to Suggest, editable), Gross Amount, Weight (Kg), Loss Reason (for Actual < Suggest).
  | SKU | Current | Suggest = Actual | Gross | Weight kg |
  |---|---|---|---|---|
  | 20050308 | 2034-0-11 | 2/0/10 | 6,488.44 | 19.46 |
  | 20050310 | 5785-0-3 | 15/0/0 | 56,183.70 | 125.28 |
  | 62690363 | 6259-0-60 | 3/0/2 | 9,855.56 | 22.48 |
  | 62740537 | 226-0-0 | 35/0/0 | 539,802.55 | **0.67** (35 cases of 2x10L oil: weight master-data error?) |
  | 69997598 | 2600-0-69 | 0/0/6 | 76.72 | 0.12 |
- Issued in full (workbook reduces some Actuals with Loss Reason "Stock Out"; not done). **Save All -> "Saved successfully."**; GIN 506 Draft / In-Active; Cash Memo Selection and Save All lock. Framework sheet GIN_DTL_SAVE_ASSR expects "Saved Succesfully." (typo + capital S) = assertion drift vs the real text (the Detail sheet has the right text).
- Header tab resets to a blank form after save (like the DA); reopen 506 from the grid: Maker on Draft -> Forward ON, Reject/Terminate OFF. Forward -> Comments "Automation Approval" -> Save -> **"Forwarded successfully"**; grid: **Pending for approval / In-Active**.

## Trial end (segments 1-3, seq 1-20): documents created today on cnr1dev1
DA **1358** (Approved), loss record **639** (Approved), orders **COL26000002003-2007** (Confirmed, delivery 2026-10-01, on GIN 506), **COL26000002008** (Cancelled, Shop Closed), GIN **506** (Pending for approval; approval = seq 23 by the Checker). Seq 15 Order Editing skipped (QA/BA discussion).

## Segment 4: Checker (Auto_Tssm) - continued the same day at the QA lead's request (~17:45)
- The QA lead's first Auto_Tssm login landed in a different browser window (the Selenium window was still Auto_Multi_Orga); Claude logged that window out and the QA lead logged in there. Hand-off note: always log in in the Selenium-controlled window ("Chrome is being controlled by automated test software").

### seq 23 Goods Issue Note Approval (00780001): done, **GIN 506 approved**
- Checker opens GIN 506 (Pending for approval): Forward, Reject, Terminate, Add enabled (Detail tab disabled).
- Forward -> Comments "Automation Approval" -> Save -> **"Forwarded successfully"**. GIN 506 disappears from the GIN grid (approved GINs are not listed; 505 of 09-30 still Pending).
- **First successful GIN approval in the replay**: preconditions met = stock received the SAME day (DA 1358 approved today) + cash memos' delivery date = today (Delivery Date Change). The two earlier failures ("No stock balance found for products", "cashmemo(s) found with delivery date earlier than the pjp working date") came from stale-day data.
- Open: the workflow declares Verify + Approve (both role 0005); one Checker Forward removed the GIN from the list -> verify at seq 24 that stock went out (Out CS) = final approval [to confirm].

## Segment 5: Maker (Auto_Multi_Orga), ~17:45

### seq 24 Stock validation after GIN PAK (02810001): done
Stock Inquiry 2026-10-01, Auto Main Warehouse, 01 - Sound, after GIN 506 approval (39 rows):
| Product | Out | Allocated before -> after | Closing before -> after |
|---|---|---|---|
| 62740537 | 35/0 | 98 -> 63 | 226 -> 226 |
| 20050310 | 15/0 | 100/0 -> 85/0 | 5785/3 -> 5785/3 |
| 62690363 | 3/2 | 56/34 -> 53/32 | 6259/60 -> 6259/60 |
| 20050308 | 2/10 | 41/106 -> 42/0 (same PC total, normalised: 1418-74 = 1344 PC = 42 CS x 32) | 2034/11 -> 2034/11 |
| 69997598 | 0/6 | 0/102 -> 0/96 | 2600/69 -> 2600/69 |
- **The single Checker Forward is the FINAL GIN approval**: the issued quantities appear as **Out** exactly, and the same quantities leave **Allocated**; **Closing does not change at GIN approval** (it already went down when the orders reserved the stock) [observed]. Settles the Verify/Approve question for org 010104: one Forward by Auto_Tssm completes it.
- Allocated after the GIN is back to the pre-order levels (e.g. 62740537 63 = the old GIN 505 reservation still pending from 09-30).

### Transaction Inquiry after GIN approval (extra check)
- COL26000002003-2007: Document Status **"Ready to dispatch/Packed"**, GIN No **506**, Delivery Date 2026-10-01, Actual Delivery Date empty. Status chain observed today: **Confirmed** (after booking) -> **Ready to dispatch/Packed** (after GIN approval). ("Planning completed" was seen on 09-30's GIN 505 while still Pending: = cash memo on a forwarded but unapproved GIN [inferred].)
- COL26000002008: **Cancelled**, delivery date stays 2026-10-07 (cancelled before the Delivery Date Change), no GIN.

### seq 29 Order Editing After GIN (00840001): done, **COL26000002003 edited after GIN 506 approval** (QA lead: try it, go on to 31 if it errors) - NO error
- Same Order Editing screen as seq 15. With the orders' delivery date = today the default Date From/To (today) now finds them (confirms the delivery-date filter). PJP 02111 selected correctly this time (verified via the request: pjpNumber=02111); Selling Category "201-..." re-selected after the cascade; Section, Outlet (1000000004) and **SKU (69997598)** auto-filled with their first value.
- **Display defect**: with the auto-filled SKU filter the order grid shows Gross 76.72 (only that SKU) beside the whole-order Discount -29,971.83 and Tax 21,234.24 -> **Net -8,660.87**. Grid columns: Document No, Document Date, Delivery Date, Outlet, Gross, Discount, Tax, Net, **Received Amount, Balance Amount**, Demand Channel.
- Clicking the Document No opens /order-editing/order-edit-new with ALL 5 lines (the SKU filter does not limit the edit): Product Desc, Product Code, Batch, Current Stock, Price Value, Demand CS/DZ/PC (read-only, as booked), Order CS/DZ/PC (editable; DZ read-only), Gross Amount, **Reason Type**, Edit per line.
- Reason Type options: **Order Change QTY, Wrong Order /No Order, No Scheme, Stock Already Avl.**
- Line 62740537 Order 7/0/0 -> **4/0/0**, reason Order Change QTY -> line Save (no message) -> **Validation** -> "Validation successfully" -> **Save** -> **"Order Save successfully"** -> /order-edit-summary "Order View - Header": **same Document No COL26000002003** (an edit does not create a new number here), Demand stays 5/0/4, Order 4/0/0.
- New totals: **Gross 96,840.34, Discount -20,718.07, Tax 14,584.79, Net 90,707.00 = workbook Order Editing Detail3 exactly**; promotions re-applied on the smaller basket (line 1 discount -13,198.30).
- **Stock effect: none** - 62740537 Auto Main still Out 35, Allocated 63, Closing 226 after the edit. The 3 CS cut after the GIN are with the delivery man; they are expected to come back through the Goods Return Note (seq 48) [inferred].
- Open for QA/BA: seq 15 (edit BEFORE the GIN) was skipped; editing after an approved GIN is allowed with no warning (business control question).

### seq 31 Order Cancellation After GIN (00850001): done, **COL26000002007 cancelled** after GIN 506 approval
- Same Order Cancellation screen (layout 202022). Orders on the approved GIN (Ready to dispatch/Packed) are still offered for cancellation (outlets 04, 08, 05, 07, 06); COL26000002003 shows its edited Net 90,707.
- Outlet 1000000006 -> COL26000002007 (Net 91,696) -> Cancellation Reason Shop Closed -> tick (scroll the checkbox cell into view first) -> Cancel All -> "Order Cancellation Status": COL26000002007 | Successfull | **Order Cancelled Successfully**.
- **Stock effect: none** (62740537 Out 35 / Allocated 63 / Closing 226 unchanged; same for all five SKUs). After the GIN, a cancelled or reduced order does not return stock by itself: 7 CS (2007) + 3 CS (2003 edit) of 62740537, plus 2007's other lines, remain "out" with the delivery man until the Goods Return Note (seq 48) [observed + inferred].

### seq 32 Cashmemo Reschedule (01040001): done, **COL26000002006 rescheduled to 2026-10-02** (reason Shop Closed)
- Menu Transaction > Cashmemo Reschedule (layout 202053). Header: Order Date (today), **Delivery Date = the NEW date** (default today), PJP Number = the **delivery** PJP (default first: AutoPJGIN2~Auto GIN PJP DM; options AutoPJGIN2, AUTO301301, 02112~AutomationDSR, AutoPromo2, 8197298470). Button: Process.
- PJP 02112 -> grid of the PJP's cash memos on a GIN: checkbox, Cashmemo No, Outlet Name, Status (Ready to dispatch/Packed), Document Date, Amount FCY, PJP Number 02111, PJP Delivery No 02112, Delivery Date, Demand Channel, **GIN No 506**, **Reschedule Reason** (in-grid dropdown). 4 rows (2003-2006; cancelled 2007 absent).
- **Changing the header Delivery Date reloads the grid and clears the selection and reasons** (it is not a filter: the 10-01 orders stay listed; request DOCMDT=2026-10-01&PJPNODLY=02112&DELIVERYDATE=2026-10-02) -> set the new date FIRST, then reason + tick.
- Reschedule Reason options (master-data duplicates): Bad Weather, Credit Exceeded, customer refused, Delivery is not possible due to any reason, Law & order Issue, **Law & Order Issue x5**, **Shop Closed x2**, **Test Reason 716**.
- Tick 2006 + reason Shop Closed -> Process -> confirm "Are you sure you want to proceed?" -> toast **"Process completed successfully"**; 2006 leaves the list (2003/2004/2005 remain, Ready to dispatch/Packed, GIN 506).

### seq 33 Cashmemo Status (00030001): done, **COL26000002003, 2004, 2005 delivered**
- Menu Transaction > Cashmemo Status (/order-booking/cashmemo-status; also offered: "Cashmemo Status Change" DYL_202019, "Cashmemo Status Van Sale"). Filters: PJP Number (delivery PJP; default first AutoPJGIN2) and **GIN Number** (fills by itself: GN-01~506 after choosing 02112-AutomationDSR).
- Grid: checkbox, Document No, Outlet, Document Date, GIN Number, Delivery Date, Demand Channel, Document Status (**"Ordered"** = document status, read-only), Gross Amount, Tax, Net Amount. Only the 3 cash memos still on GIN 506 (2006 rescheduled off the GIN; 2007 cancelled). 2003 shows Net 90,707.06 (= line sum; the header elsewhere rounds to 90,707.00).
- No per-row status choice: **tick the delivered cash memos + Save -> "Updated successfully"**; the list empties. (Framework: header checkbox + saveallBtn, expected "Updated successfully".)

### Transaction Inquiry status check after seq 31-33 [observed]
| Order | Document Status | Delivery Date | Actual Delivery | GIN |
|---|---|---|---|---|
| COL26000002003/2004/2005 | **Delivered/Invoiced** | 2026-10-01 | 2026-10-01 17:54:09 (time of Cashmemo Status save) | 506 |
| COL26000002006 | **Reattempt** (after Cashmemo Reschedule) | **2026-10-02** | - | (none: rescheduling takes it off the GIN) |
| COL26000002007 | **Cancelled** (after GIN) | 2026-10-01 | - | 506 kept |
| COL26000002008 | **Cancelled** (before GIN) | 2026-10-07 | - | - |
Invoice Ref. No. stays empty after delivery.

### seq 34 Sales Return (00070001): done, **return COL26000000713 against COL26000002003** (2 CS of 62740537, reason No Cash)
- Menu Transaction > Sales Return (DYL_201801, /content-master/mobility/sales-return; the menu also has Sales Return Status Change, Sales Return View, Sales Return Without Reference, Fresh Sales Return, Sales Return W/O Reference View / Pick, and a 2nd "Sales Return" NG0906).
- Header filters: Document No (generated), Document Date (today), PJP Number (delivery PJP; default first AutoPJGIN2), Date From/To (today), Outlet Name, SKU. Tabs Header / Detail (Detail disabled until saved); buttons Add, Save.
- PJP 02112 -> grid of **delivered** cash memos only (2003/2004/2005): Document No, Document Date, Delivery Date, Outlet Code, Gross, Discount, Tax, Net, **Received Amount 0, Balance Amount = Net**, Demand Channel.
- Select the cash memo (click its Outlet Code cell) -> Save -> **"Record Saved Successfully!"** -> return document **COL26000000713** (own number series, CM-02); Save disabled, Detail enabled.
- Detail: per invoice line Product (code-name-price), Batch, Stock Type, Trade Price/Unit, **Invoice Quantity** CS/DZ/PC (62740537 shows the EDITED 4 CS), **Return Quantity** CS/DZ/PC, Gross Amount, **Reason Type**, Edit. Buttons validation, Forward.
- In edit mode Stock Type is editable: **Damaged, Expired, Lost, Sound** (return can be booked as non-sound stock). Return reasons: **No Cash, Wrong Order/No Order, Shop Closed, Credit Exceeded**.
- 62740537 Return 2/0/0, Sound, No Cash -> line Save (no toast; a "Record Saved Successfully!" toast appeared once while tabbing) -> Gross **30,845.86 = workbook** -> validation -> **"Validation successfully"** -> Save -> **"Save successfully"** -> Forward enabled.
- Return totals: Gross 30,845.86, Discount 6,189.17, Tax 4,419.93, **Net 29,077.00** (workbook 6,169.17 / 4,436.55 / 29,113.00: differs because the source order was edited first, so its promotion/tax ratios differ) [observed].

### seq 36 Sales Return View (00700001): done, return COL26000000713 forwarded by the Maker
- Menu Transaction > Sales Return View (SALESRETURNVIEW, /sales-return-statusChange/view). Filters: PJP Number (delivery PJP; default first), Date From/To (today). Tabs Header / Detail; button Forward.
- Grid: checkbox, Document No. (return), **Principle Invoice** (the source cash memo), Document Date, Delivery Date, Outlet Code, Gross, Discount, Tax, Net. PJP 02112 -> COL26000000713 | COL26000002003 | 30,845.86 | 6,189.17 | 4,419.93 | 29,077.
- Tick -> Forward -> "Comments" (mandatory) "Automation Approval" -> Save -> result window **"Sales Return Status"** (Document No, Sales Return Status, Status, Error Message): COL26000000713 | Sales Return | **Success** (= workbook SaleRetrunView_ASSR "Success"). No toast.
- Next: seq 37 Sales Return View Approval by the Checker (Auto_Tssm).

## Segment 6: Checker (Auto_Tssm)
### seq 37 Sales Return View Approval (00730001): done, return COL26000000713 approved
- Same Sales Return View screen. The Checker's PJP list has ALL 13 PJPs (booking + delivery), the Maker's showed delivery PJPs only.
- 02112 -> COL26000000713 (Principle Invoice COL26000002003) -> tick -> Forward -> Comments "Automation Approval" -> Save -> "Sales Return Status": COL26000000713 | Sales Return | **Success** (= workbook). The return then disappears from the list (approved). Same screen, same button, different user = approval (maker-checker pattern as DA/GIN).

## Segment 7: Maker (Auto_Multi_Orga), ~18:04
### seq 38 Sales Return Status Change (00710001): done, return COL26000000713 marked picked
- Menu Transaction > Sales Return Status Change (/sales-return-statusChange). Filters: PJP Number (delivery PJP; default first) and Gin Number (fills itself: GN-01~506). Grid: Document No. (return), Principle Invoice, Document Date, Delivery Date, Outlet Code, Gross, Discount, Tax, Net. Lists the APPROVED return COL26000000713.
- A single click does not open it; double-click (framework clicks the document no) -> Detail tab: Product, Batch, Stock Type, Trade Price/Unit, **Order Quantity**, **Return Quantity** (editable again: picked quantity can differ from the approved return), Gross, Reason Type, Edit.
- Validation -> "Validation successfully" + totals (Gross 30,845.86, Discount 6,189.17, Tax 4,419.93, Net 29,077) -> button **"Save Sale Pick"** -> **"Save successfully"** (= workbook SR_StatsChang_DTL_SAVE_ASSR).
- Stock effect not checked here; returned goods are expected back in warehouse stock with the GRN (seq 48) [inferred].

### seq 39 Deposit Slip Full Amount Cash (03230001): done, **slip 1131** = 101,161 cash for COL26000002004 (outlet 05)
- Menu Transaction > Receivable > Deposit Slip (layout 201802; direct URL redirects to the menu). The screen opens on a NEW slip: Deposit Slip* (generated), **PJP-DSR* preset to the booking PJP "02111 - AutomationOB1"** (must be changed to the delivery DSR 02112 - AutomationDSR; list has all 13 PJPs), Date (ro), Type* (Cash / Cheque), Status "Un Posted" (ro), **Bank preset "demo"**, Bank Branch, Deposit Amount*. Buttons Add, Save, Update, Delete, Forward, Reject, Save All.
- Upper grid (slips): Deposit Slip, PJP-DSR, Deposit Date, Type, Bank, Bank Branch, Status, Deposit Amount, Adjusted Amount. Lower grid (after save): the DSR's delivered cash memos: PJP, Document No, Document Type (Sales), Outlet Code, Outlet Desc, GIN, Cheque No., Cheque Date, Bank_Name, Net Amount, Received Amount, Balance, Un Posted Amount, **Deposit-Amount** (editable).
- Header 02112 / Cash / 101161 -> Save -> **"Saved successfully"** -> slip **1131**, Un Posted, Adjusted 0.
- Cash memos before allocation: 2005 Net/Balance 119,370; 2004 101,161; **2003 90,707 (the approved + picked sales return 29,077 has NOT reduced the receivable)** [observed; credit note / settlement step expected to net it, unknown].
- Deposit-Amount 101161 on COL26000002004 -> Save All -> **"Record saved successfully!"**. After re-opening the screen: slip 1131 **Adjusted 101,161, Status still Un Posted** (older slips 1128-1130 show Posted: posting probably happens at Route Settlement [inferred; check at seq 51]).

### seq 40 Deposit Slip Full Amount Cheque (03240001): done, **slip 1132** = cheque 119,370 for COL26000002005 (outlet 07)
- Header: 02112 / **Cheque** / Bank **Bank Al-Habib Limited** / Bank Branch **DHA Branch** (fills itself: the bank's only branch) / 119370 -> Save -> "Saved successfully" -> slip 1132.
- **Bank master data is polluted**: list contains real banks plus "test", "99", "32", "demo", "asd", "", "tes", "SBK", "DIST BANK", "PK BANK", "test feroz", "Test Bank 891724/951327/198290", "Bank tdm", "SAMBHA bANK", "HB Bank", "First Women Bank Limited 1", and **"National Bank of Pakistanss"** (the workbook's "National Bank of Pakistan" no longer exists -> framework value drift; used "...ss").
- Cash-memo row 2005: Cheque No. 1234501, Cheque Date 2026-10-01, Bank_Name National Bank of Pakistanss, Deposit-Amount 119370 -> Save All -> **"Record saved successfully!"**.
- **Risk observed**: after slip 1131 allocated 101,161 to COL26000002004, the lower grid still showed 2004 with Received 0 / Balance 101,161 when creating slip 1132 -> balances update only at posting, so the same cash memo can apparently be allocated again by another slip in the meantime (double-allocation risk; not tried).

### seq 41 Deposit Slip Unposted Amount Validate (03260001): done (learning variant), **slip 1133** = cash 1,000, 600 allocated to COL26000002003
- Add -> the new form is BLANK (no PJP-DSR, no "demo" bank: those defaults appear only on first opening). 02112 / Cash / 1000 -> Save -> "Saved successfully" -> slip 1133.
- Cash-memo grid after saving 1133: 2005 Un Posted 119,370 and 2004 Un Posted 101,161 (= the allocations on slips 1132 / 1131, not yet posted), Balance still full -> **"Un Posted Amount" on a cash memo = amount already allocated on OTHER unposted slips**; Balance/Received change only at posting [observed].
- Deposit-Amount 600 on 2003 (deliberately partial; workbook allocates the full 1,000 and expects Un Posted 0) -> Save All -> "Record saved successfully!".
- After reopening: slip 1133 shows Dep 600 on 2003 (saved) but the slip's **Adjusted Amount stays 0** (slips 1131/1132, fully allocated, show Adjusted = amount) -> Adjusted seems to be filled only when the slip is fully allocated [observed; to confirm]. 2003's Un Posted shows 0 while slip 1133 is open (its own allocation is not counted).
- Q-DS1 (BA): what is "posting" (who/when: Route Settlement? Forward?), and is a partly allocated slip allowed to be posted?

### seq 42 Deposit Slip Multi Cheques (00140001): done, **slip 1134** = cheque 1,000 split into 4 cheques for outlet 1000000004
- Header 02112 / Cheque / Bank Al-Habib Limited (branch DHA fills itself) / 1000 -> "Saved successfully" -> slip 1134.
- The cash-memo area has 3 tabs: **Outstanding Cash memos** (per cash memo), **Outstanding Outlet** (per outlet: Outlet Code, Outlet Desc, Net, Received, Balance, Un Posted, Deposit Amount, Action "+"), **Deposit Slip Detail**. Multi-cheque entry is on Outstanding Outlet: tick the outlet -> "+" (scroll it into view) -> popup **"Cheque Details"** (grid Cheque. No., Cheque Date, Bank, Net Amount; add-row icon; row Save/Cancel; "Save Changes"; x).
- **Cheque Date must be typed MM/DD/YYYY here** ("10/01/2026"); typing 2026-10-01 shows the text but leaves the value empty -> row Save answers **"Fill all the values!"** (other screens take yyyy-mm-dd).
- 4 cheques (workbook): 12444 / 200, 22337 / 300, 12222 / 400, 1234567 / 100, all dated 10/1/2026, bank National Bank of Pakistanss -> Save Changes -> outlet 04 Deposit Amount 1,000 -> Save All -> **"Payment Adjusted Successfully"** (workbook Deposit Slip,Outlet expects "Saved successfully": message drift).
- Outlet 04 at that point: Net 90,707, Received 0, Balance 90,707, Un Posted 600 (slip 1133).

### seq 44 Deposit Slip Cheque (00140004): done, **slip 1135** = cheque 1,000 (Bank Al-Habib / DHA) for COL26000002003
- Outstanding Cash memos tab: 2003 row Cheque No. 1234567, Cheque Date 2026-10-01 (yyyy-mm-dd accepted on THIS grid), Bank_Name National Bank of Pakistanss, Deposit-Amount 1000 -> Save All -> "Record saved successfully!". 2003 Un Posted before: 1,600 (= 600 slip 1133 + 1,000 slip 1134).

### seq 46 Deposit Slip Cash (00140005): done, **slip 1136** = cash 1,000 for COL26000002003
- 02112 / Cash / 1000 -> "Saved successfully" -> 1136; 2003 Un Posted 2,600 -> Deposit-Amount 1000 -> Save All -> "Record saved successfully!".

### Deposit slips today (all **Un Posted**; correction to seq 41: slip 1133 later shows Adjusted 600, so partial allocations DO fill Adjusted - the earlier 0 was a stale grid; Adjusted refreshes only when the screen is reloaded)
| Slip | Type | Amount | Adjusted | Cash memo |
|---|---|---|---|---|
| 1131 | Cash | 101,161 | 101,161 | 2004 |
| 1132 | Cheque (Al-Habib/DHA, chq 1234501) | 119,370 | 119,370 | 2005 |
| 1133 | Cash | 1,000 | 600 | 2003 |
| 1134 | Cheque x4 (12444/200, 22337/300, 12222/400, 1234567/100) | 1,000 | 1,000 | outlet 04 (2003) |
| 1135 | Cheque (chq 1234567) | 1,000 | 1,000 | 2003 |
| 1136 | Cash | 1,000 | (1,000 after refresh) | 2003 |
- Same cheque number 1234567 used on slip 1134 (multi) and 1135 (single) for the same outlet: accepted, no duplicate-cheque check [observed; workbook uses it twice too].

### seq 48 Good Return Note (00090001): done, **GRN 246** created and forwarded (Pending for approval)
- Menu Transaction > Goods Return Notes (/goods-return-notes/GRN). Tabs GRN / Detail; buttons Add, Forward, Reject. Header: GRN No. (generated), GRN Date (today), Delivery Man PJP, Delivery Man DSR, Warehouse, Vehicle, Status, **Working Date** (today), **GIN Number**, Approval Status. Master grid: GRN No., GRN Date, Delivery Man PJP, Warehouse, Approval Status, Status.
- Add -> Delivery Man PJP 02112-AutomationDSR -> fills DSR ITB0189-AutomationQADSR, Warehouse C0000000055 Auto Main, Vehicle 0040-Automation211206, **GIN Number 506** (the DSR's open GIN of the working date).
- Detail: Product, Batch, Stock Type (01-Sound), **Suggested** CS/DZ/PC, **Actual** CS/DZ/PC (editable via Edit), Rate.
  - Suggested = **62740537 19 CS** only = 7 (COL26000002007 cancelled after GIN) + 7 (COL26000002006 rescheduled / Reattempt) + 3 (COL26000002003 cut 7->4 after GIN) + 2 (sales return COL26000000713). **Every quantity that left on the GIN and was not delivered or was returned comes back on the GRN, including the rescheduled order** (it will be issued again for 10-02) [observed: exact reconciliation]. 2006/2007 were single-line orders, hence only one SKU.
- Actual = 19 (full) -> Save All -> **"Record Saved Successfully"** (workbook GRN_DTL_SAVE_ASSR: "Record Saved Successfully" = match) -> GRN **246** Draft / In-Active.
- GRN tab resets to a blank form after save; reopen 246 from the grid (Draft, Forward ON, Reject OFF for the Maker) -> Forward -> Comments "Automation Approval" -> Save -> **"Forwarded successfully"** -> Pending for approval.
- Workbook GRN detail (1 CS 5 PC / 2 CS 1 PC, rates 118.93 / 33.79) belongs to its own order mix; not applicable to today's data.

## Segment 8: Checker (Auto_Tssm)
### seq 49 Good Return Note Approval (00810001): done, **GRN 246 approved**
- Goods Return Notes grid -> 246 (Pending for approval, GIN 506) -> Checker buttons Forward + Reject enabled -> Forward -> Comments "Automation Approval" -> Save -> **"Forwarded successfully"**; 246 disappears from the grid (approved GRNs are not listed, like approved GINs).

## Segment 9: Maker (Auto_Multi_Orga), ~18:30
### seq 50 Stock validation after GRN PAK (02820001): done
- Stock Inquiry 2026-10-01 Auto Main, 01 - Sound: **62740537 In 164 -> 183 (+19 = GRN 246), Out stays 35, Allocated 63, Closing 226 -> 245**. Other four SKUs unchanged (no return lines for them). Row count 39.
- **A GRN posts the returned quantity as In (Sound) on approval; it does not reduce Out** [observed]. Returned goods come back as Sound stock (GRN line stock type 01-Sound; the sales return was booked Sound too).

### seq 51 Route Settlement (00680001): **BLOCKED** - "Following previous days not closed! Please close date. 2026-09-30"
- Menu Transaction > Receivable > Route Settlement (/content-master/route-settlement). Header: Date (today), PJP Number (empty = all), "Select All", Route Status (All), Total Payable Amount, Total Received Amount, Total Cash Shortage (read-only totals).
- Grid: one row per delivery man of the date: PJP Delivery Man Code, Delivery Man, Total Order, Delivered Orders (link), Undelivered Orders, Sale Value, Adjusted Credit Note Amount, Fresh Return Value, Total Cash Collected (Previous/Today/Total), Total Cheque Collect (Previous/Today/Total), Collection Type, Payable Amount, Received Amount, Cash Shortage, Edit.
- 02112-AutomationDSR / AutomationQADSR [observed]: Total Order **4** (2003-2006 = orders on GIN 506 excluding the cancelled 2007), Delivered **3**, Undelivered **0** (the rescheduled 2006 is neither), **Sale Value 311,238** (= 90,707 + 101,161 + 119,370, delivered orders), Adjusted Credit Note **0** and Fresh Return 0 (the approved+picked sales return 29,077 is NOT netted here), Cash 0 / 102,761 / 102,761, Cheque 0 / 121,370 / 121,370.
- **Collection Type = one line per deposit slip** with Payable = Received: 1132-CHEQUE 119,370; 1134-CHEQUE 1,000; 1135-CHEQUE 1,000; 1131-CASH 101,161; 1133-CASH **600** (its allocated part, not the 1,000 slip amount); 1136-CASH 1,000; Stock Shortage 0. Header totals Payable 224,131 = Received 224,131, Cash Shortage 0. Note: Sale Value 311,238 vs collected 224,131 -> 87,107 still owed (not shown as shortage before settlement).
- **Edit (start settlement) -> error popup "Following previous days not closed! Please close date. 2026-09-30"** (Continue). Route Settlement requires every earlier working day of the distributor/PJP to be closed. 2026-09-30 is still open (stale replay day: GIN 505 Pending, orders 1995-2002).
- Not done: settlement itself, deposit-slip posting check, seq 52-54 (depend on settlement).
- Q-RS1 (BA/QA): which process closes a day (Day Close / PJP Daily Inquiry Update / Generate Opening Balances?), and is it acceptable to close 2026-09-30 on cnr1dev1 (affects other testers' data)?
