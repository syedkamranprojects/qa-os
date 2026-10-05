# Session log: LEARN-G11-PK/20261005-RS (session 2b, resume from seq 51 Route Settlement, 2026-10-05)

Env cnr1dev1, Unilever Pakistan Limited, distributor 15108843 IBRAHIM TRADERS. Maker Auto_Multi_Orga (QA lead logged in ~afternoon; Claude selected company + distributor). Business facts only.
Context (QA lead, 2026-10-05): there were many un-closed routes on earlier days; a QA team member closed them. More details on the day-close process to follow from the QA lead (Q-RS1 still to be written up from their answer).

## Seq 51 Route Settlement (Maker) - read-only check
- Transaction > Receivable > Route Settlement. Header: Date (default today), PJP Number (empty = all), Select All (ticked), **Route Status: All / Complete / Incomplete** (first time the values were read) [observed].
- **2026-10-05, route 02112 (AutomationQADSR) is now Complete**: row shown green, **no Edit link** (other routes keep Edit), listed under Route Status = Complete. Values unchanged from the morning: Total Order 13, Delivered 3, Undelivered 0, Sale Value 311,238, Adjusted Credit Note 0, Fresh Return 0, Cash 0 / 102,761 / 102,761, Cheque **1,000 (Previous)** / 120,370 / 121,370, Collection lines 1138/1140/1141 CHEQUE 119,370/1,000/1,000, 1137/1139/1142 CASH 101,161/600/1,000, Stock Shortage 0; Payable = Received per line; header totals 224,131 / 224,131 / Cash Shortage 0 [observed]. Settled by the QA team member, not by Claude (settlement action and its message not seen).
- **2026-10-01, route 02112-AutomationDSR is also Complete** (values as session 1: Total Order 4, Delivered 3, Sale 311,238, Cash 102,761, Cheque 0/121,370/121,370) [observed].
- 2026-10-01 Incomplete filter: 4 zero-activity routes (8197298470 Aslam PJP DM, AutoPJGIN2, AutoPromo2, AUTO301301) remain Incomplete with Edit; they evidently did not block 02112 from being settled [observed; inferred: the previous-day check applies per route/PJP with activity].
- Rules learned: a settled route row = Route Status Complete, green highlight, Edit hidden (cannot be re-edited from this screen) [observed]. Header totals (Payable/Received/Cash Shortage) are computed over the rows shown by the filter (Incomplete filter on 10-01 -> 0 / 0 / 0) [observed].
- Open: 02112 on 10-05 shows Total Order 13 (10-01: 4) and a Previous cheque of 1,000 - which orders/slips make up 13 and the "previous" 1,000 is not yet explained.

## Seq 52 OFFSET Amount Validate After Route Settlement (Maker) - done (read-only)
- Transaction Inquiry (DYL_102014), Document Type **Sales** (default "Demand Captured from Tele order" hides orders), Status All, dates 2026-10-05; 6 Sales documents (2 pages).
- **Offset Amount after settlement = sum of the deposit-slip allocations on the cash memo** [observed]:
  - COL26000002009 (Delivered/Invoiced, Net 90,707): Offset **2,600** = slips 1139 (600) + 1141 (1,000) + 1142 (1,000). The outlet-level multi-cheque 1,000 of slip 1140 is NOT on 2009 (see seq 53: it went to the older 2003).
  - COL26000002010 (Net 101,161): Offset **101,161** (slip 1137). COL26000002011 (Net 119,370): Offset **119,370** (slip 1138).
  - 2012 Reattempt, 2013/2014 Cancelled: Offset 0. Actual Delivery Date 2026-10-05 10:37 on the delivered ones.
- Offset before settlement on these memos was not read today (earlier sessions: Offset 0 right after booking) - whether Offset fills at allocation or only at posting is still open.

## Seq 53 Deposit Slip After Route Settlement (Maker) - done (read-only)
- Deposit Slip (DYL_201802) header grid: **all six 10-05 slips 1137-1142 are now Posted** (were Un Posted this morning) [observed]. Posting also changed:
  - slip 1139 Deposit Amount **1,000 -> 600** (= its Adjusted Amount): posting trims an unallocated remainder [observed; inferred rule].
  - cash slips show Bank "demo" (entered without a bank) [observed].
- **10-01 slips 1131-1136 are still Un Posted** although route 02112 for 2026-10-01 shows Complete (1133 still Deposit 1,000 / Adjusted 600). 09-29 slips 1125-1130 are Posted [observed]. -> How the QA team member closed 10-01 (settlement vs another day-close action) must come from the QA lead; Complete does not always mean the day's slips were posted.
- Slip 1137 opened: header read-only after posting (Save/Update/Delete/Forward/Reject/Save All disabled; only Add) [observed]. Tabs: Outstanding Cash memos / Outstanding Outlet / Deposit Slip Detail.
- Outstanding Cash memos of PJP 02112 after settlement [observed]:
  | Memo | GIN | Net | Received | Balance | Un Posted |
  |---|---|---|---|---|---|
  | COL26000002009 | 507 | 90,707 | **2,600** | 88,107 | 0 |
  | COL26000002005 | 506 | 119,370 | 0 | 119,370 | 119,370 (10-01 slip 1132) |
  | COL26000002004 | 506 | 101,161 | 0 | 101,161 | 101,161 (10-01 slip 1131) |
  | COL26000002003 | 506 | 90,707 | **1,000** | 89,707 | 3,600 (10-01 slips 1133 600 + 1134/1135/1136 1,000 each) |
  - Fully received memos (2010, 2011) drop out of the outstanding list [observed] (this is what seq 54 asserts with its "no data" check).
  - **The outlet-level multi-cheque slip 1140 (outlet 1000000004, 1,000) was applied to the OLDEST open memo of the outlet, COL26000002003 (10-01)**, not to today's 2009 [observed]. That explains Route Settlement 10-05 "Total Cheque Collect Previous = 1,000": a collection today against a previous day's cash memo [inferred, consistent].
- Framework expected value for seq 53 (Received Amount, filter GIN 507 + outlet): 2009 -> 2,600 today.

## Seq 54 Deposit Slip Cash removal (Maker) - covered by the seq 53 read
- The flow filters the cash-memo tab by GIN 507 + outlet and asserts the grid's "no data" state for the fully settled memos; observed: 2010/2011 (fully received) are no longer listed; 2009 (partly received) still is [observed].

## Seq 55 Cheque Status (Maker) - BYPASSED by the QA lead (screen read only, no action)
- Transaction > Receivable > Cheque Status (DYL_202020). Top grid lists **only Posted deposit slips** (cheque slips): Deposit Slip, PJP-DSR (empty), Current Date, Bank, Bank Branch, Status, Amount; 37 pages of history. "Show filter row" checkbox (gridFilterCheckbox) opens a filter row; the date filter applies on Enter [observed].
- Filter 2026-10-05 -> 1138 (119,370), 1140 (1,000), 1141 (1,000), all Posted; the unposted 10-01 cheque slips 1132/1134/1135 are NOT offered [observed].
- Detail grid per slip: Cheque No, Cheque Date, Amount, **Cheque Status, Cheque Status Date**. All of today's cheques are already **"Clear"** dated 2026-10-05: 1138 -> 1234501 119,370; 1140 -> 12222 400, 1234567 100, 12444 200, 22337 300; 1141 -> 1234567 1,000 [observed]. (Duplicate cheque no. 1234567 visible on two slips.)
- **The only action on the screen is "Bounce"**; there is no Realized/Presented/Collected choice. Posting at Route Settlement sets cheques to Clear [observed: status date = settlement day; inferred: set by posting].
- QA lead asked for "Realized"; that value does not exist on this screen, and Bounce was excluded, so nothing was changed. Question for QA: does seq 55 in the framework press Bounce (event `notrefresh` after selecting the cheque row)? Page cheque_status.md listed statuses P/L/R/B/C/A from the DB; the UI shows "Clear".

## Seq 56 DSR Adjustment Amount (Maker) - BYPASSED by the QA lead (typed values discarded, nothing saved)
- Menu search "Adjustment" offers three items: Stock Adjustment SAN (DYL_201045), DSR Adjustment (DYL_201065) and **DSR Adjustment Amount** (DSR_ADJUSTMENT_AMOUNT, /content-master/mobility/dsr-adjustment-amount-wise) = the framework's option [observed].
- Screen: tabs Header / Detail. Header grid "DSR Adjustment": PJP Code, PJP Description, Total Shortage Amount, Total Adjusted Amount, Balance Amount; one row **02112 AutomationDSR: 2,477,571.11 / 1,649,970.43 / 827,600.68** (Balance = Shortage - Adjusted) [observed]. Entry panel: Document Date (2026-10-05, default today), Amount (`balanceAmt`), Comments, button Save (`SavePopUp`) [observed].
- Workbook (NG_Dcode_QA_OTC (Pak)): Amount 400, Comments AUTO; Detail check Amount "PKR 14,796.99" for 2026-09-21 (stale date).
- Row 02112 selected, Amount 400 + Comments AUTO typed, **not saved**: Claude's permission system blocked further data-changing actions on the shared environment (auto-mode classifier, "Modify Shared Resources"). Waiting for the QA lead.
- Workbook hint for seq 57 (PJP Daily Inquiry Update, sheet PJP Daily2): PJP 2112, DSR ITB0189, **Mark Status "End Of Day", DSR Files Status "Complete"**, End Date = time -> this is likely the day-close action that Route Settlement's "previous days not closed" refers to [inferred; to confirm with the QA lead's information].

## Seq 57 PJP Daily Inquiry Update (Maker) - done = THE DAY CLOSE
- QA lead (chat, 2026-10-05): "you are allowed to click on every button now" (Bounce still avoided).
- Menu: "PJP Daily" offers PJP Daily Inquiry (DYL_202037, read-only) and **PJP Daily Inquiry Update (DYL_BG1022)**. Header: Working Date (default today). Grid: PJP Number, DSR, Current Status, Mark Status, DSR Files Status, Working Date, Start Date, End Date, Edit (2 pages) [observed].
- Evidence of how the QA team member closed 2026-10-01: row 02112 / ITB0189 on Working Date 2026-10-01 = **Current Status E, Mark Status End Of Day, DSR Files Status Complete**, Start/End Date empty; the other PJPs (02111, 7918624876, AUTO021311, AUTO031026) blank [observed]. Matches the framework workbook (sheet PJP Daily2: Mark Status End Of Day, DSR Files Status Complete).
- Today: Working Date 2026-10-05, row 02112 -> Edit (row becomes editable: DSR ITB0189 text, Mark Status dropdown, DSR Files Status dropdown, End Date picker; Save / Cancel links). **Mark Status options: only "End Of Day"**; **DSR Files Status options: Process, Complete**. Chose End Of Day + Complete, End Date left empty (as the QA member's 10-01 row) -> Save -> toast **"Record Updated Successfully"** -> row shows **Current Status E**, End Of Day, Complete [observed].
- Rule: closing a working day for a route = PJP Daily Inquiry Update, Mark Status "End Of Day" + DSR Files Status "Complete" on the delivery PJP for that Working Date; Current Status becomes "E" [observed; to be confirmed by the QA lead's detailed note: whether this is what clears "Following previous days not closed!"].
- Order observed today: Route Settlement for 10-05 was Complete BEFORE the day close (settled by the QA member), then the day was closed here.

## Seq 58 OTC Stock Out R1 = Stock Adjustment SAN (Maker) - header saved, detail line NOT saved
- Menu Stock Adjustment SAN (DYL_201045). Header defaults: SAN Type "Warehouse To Warehouse Transfer", From IBT Main warehouse, To Auto Main Warehouse, Status In-Active, Approval Status Draft; buttons Save only (Add/Update/Delete/Forward/Reject disabled), SAN Detail tab disabled until save [observed].
- Choosing SAN Type **Stock Adjustment Admin** clears To Warehouse (not used by this type) [observed].
- Header: Stock Adjustment Admin, From C0000000055-Auto Main Warehouse, Comments "Automation" -> Save -> **"Saved successfully"** -> **SAN Document No 96**, In-Active / Draft; Update, Delete, Forward and Add enabled, SAN Detail tab enabled [observed]. (Previous SANs 93-95 on 09-22/28/29, same type, all Approved.)
- SAN Detail: button "Add a row" (`cashMemoSelectionGrid0`); grid columns Product, Stock Type, Reason Type, Batch, **Current Stock (ATP)**, Adjustment Quantity, Price, Gross Amount, Tax Amount, CS, DZ, PC [observed]. Product type-ahead "62740537" -> "62740537-RAFHAN SLPC OILS CORN TIN PI7 2X10L-7711.47"; Stock Type options 01-Sound / 02-Damaged / 03-Expired / 04-Lost; Reason Type test / HHB / MICE BITTEN / Just Cause; Batch 1-1 (only option) [observed].
- After product + batch: **Current Stock (ATP) "309-0-0"** (CS-DZ-PC) = the closing 309 CS read at seq 50 after GRN 247, so nothing moved this product's stock since then (settlement/day close have no stock effect) [observed]; Price 7,711.47.
- CS -50 could not be entered: Claude's permission system blocked the keystroke again ("Modify Shared Resources") although the QA lead allowed all buttons in chat. **SAN 96 remains a Draft header with no saved line** (CS empty, Gross shows NaN in the unsaved row). Waiting for the QA lead.
- (after Claude restart, new browser, QA lead re-logged in) SAN 96 reopened: still Draft, detail empty. Line re-filled (62740537 / 01-Sound / test / 1-1, ATP 309-0-0); typing CS -50 was blocked again by the permission system ("Modify Shared Resources"); CS stays 0, line NOT saved. A restart does not lift this block; it needs a permission change by the QA lead.
- Gotcha: the CS number cell re-renders on focus (send_keys -> stale element); it needs focus + key presses one at a time.
- Detail line entered + row-saved by the QA lead (CS -50): line 62740537 / 01-Sound / test / 1-1 / ATP 309-0-0 / Adjustment Quantity **-50** / Price 7,711.47 / **Gross -771,146.50** (= 100 PC x 7,711.47: price is per PC, 1 CS = 2 PC for this 2X10L pack) / Tax 0; row links Edit / Delete [observed].
- After a detail save the header tab resets to a blank new document; re-select SAN 96 in the grid to get Forward [observed].
- Forward (button id `forward`) -> popup Comments (textarea `comments`) + Save/Cancel; Claude typed "Automation Approval", verified, clicked Save -> **"Forwarded successfully"**; grid row 96 = In-Active / **Pending for approval** [observed].

## Seq 59 SAN Approval PAK (Checker Auto_Tssm) - done
- QA lead switched the Claude session out of auto mode (blocks gone); Claude logged Auto_Multi_Orga out, QA lead logged in as Auto_Tssm (landed directly on the menu; no company/distributor page this time).
- Stock Adjustment SAN (same option as the Maker, DYL_201045): SAN 96 Pending for approval; for the Checker Forward and **Reject** are enabled (Save/Update/Delete disabled) [observed].
- Forward -> Comments "Automation Approval" (verified) -> Save -> **"Forwarded successfully"** -> SAN 96 **Active / Approved** in one Checker step [observed]. Matches workbook SAN Approval PAK (EXPECTED_MESSAGE "Forwarded successfully").

## Seq 60 Opening & Closing Stock Validation (Maker Auto_Multi_Orga) - done (read-only)
- Logout Checker -> QA lead logged in as Auto_Multi_Orga -> Claude picked company + distributor (the distributor Proceed needed a second try).
- Stock Inquiry (STOCKINQUIRY; also "Stock Inquiry II" DYL_BG1015 exists): Period Type DAILY, Balance Date 2026-10-05, Category All, Brand empty -> Show Inquiry (`showInquiryRefresh`). Button "Generate Opening Balances" NOT clicked. 3 pages [observed].
- **62740537 RAFHAN CORN TIN 2X10L, Auto Main Warehouse, Sound: Opening 308 / In 99 / Out 85 / Allocated 63 / Closing 259** (CS) [observed].
  - vs seq 50 (after GRN 247): Out 35 -> **85 (+50)**, Closing 309 -> **259 (-50)**: the approved SAN 96 (Stock Adjustment Admin, -50 CS) posts as **Out** of Sound stock on approval [observed]. Closing = Opening + In - Out - Allocated (308 + 99 - 85 - 63 = 259) holds again.
  - Settlement, posting and the day close (seq 51-57) moved no stock [observed: ATP stayed 309 until the SAN].
- Other Auto Main Sound rows today (CS / PC): 20050308 Opening 2076/11, In 50, Out 2/10, Alloc 42; 20050310 5870/3, In 64, Out 15, ...; 62690363 6312/92, In 55, Out 3/2, Alloc 53/32, Closing 6311/58; 69997598 2600/165, In 40, Out 0/6, Alloc 0/96, Closing 2640/63 [observed].

## Summary of this resume session (seq 51-60)
- 51 Route Settlement: already Complete (QA member) for 10-01 and 10-05; 52-54 read after settlement (posting, offsets, outstanding memos); 55 Cheque Status and 56 DSR Adjustment BYPASSED by the QA lead; **57 day close done (End Of Day / Complete -> Current Status E)**; 58 SAN 96 created + forwarded (CS -50 typed by the QA lead while Claude was blocked); 59 SAN 96 approved by Auto_Tssm; 60 stock confirms -50 Out.
- Documents of today added: SAN 96 (Approved). Route 02112 2026-10-05 settled + day closed.
- Remaining active rows of group 11: seq 68-71 (Transaction Inquiry validations; read-only), then consolidation into the knowledge pages.
- Tooling note: Claude Code "auto mode" blocked typing amounts/quantities on the shared env ("Modify Shared Resources") even with allow rules; the QA lead switched the session to Ask permissions and the blocks stopped.

## Seq 68 Validate Edited Order Charges Tax In Transaction Inquiry (Maker) - done, MATCHES workbook
- Transaction Inquiry, Document Type Sales, 2026-10-05, Show filter row -> Outlet Code 1000000004 -> COL26000002009 (edited 7 -> 4 CS on line 1 at seq 29): header Gross 96,840.34 / Discount -20,718.07 / **Tax 14,584.79** / Offset 2,600 / Net 90,707, Delivered/Invoiced, GIN 507 [observed].
- Row selected -> button **Total Tax**: 0001 Value Added Tax TAX **11,389.48**; 9000 3rd Schduele (sic) TAX **3,195.31** (sum 14,584.79 = header Tax) [observed]. Workbook T Inquiry Total Tax Amt Val2 = 11,389.48 / 3,195.31 and Header Tax Amt Val2 = 14,584.79: exact match.

## Seq 70 Transaction Inquiry Validations After Order Editing (Maker) - done; detail + offering MATCH, header Tax in workbook is wrong
- **Detail** (same memo 2009): columns Serial No, Product Description, Batch, Stock Type, Trade Price / Unit, Delivered CS/DZ/PC, Gross, Discount, Tax, Net, Allocated CS/DZ/PC, Ordered CS/DZ/PC [observed]:
  1. 62740537 corn tin, TP 7,711.47, Delivered 4 CS, Gross 61,691.72, Disc -13,198.36, Tax 8,728.81, Net 57,222.17, Allocated 7 CS, Ordered 5 CS 4 PC (!)
  2. 20050310, 5 CS, 18,727.90 / -4,006.66 / 2,649.82 / 17,371.07
  3. 62690363, 3 CS 2 PC, 9,855.56 / -2,108.50 / 1,873.23 / 9,620.28
  4. 20050308, 2 CS 10 PC, 6,488.44 / -1,388.14 / 1,322.08 / 6,422.38
  5. 69997598, 6 PC, 76.72 / -16.41 / 10.86 / 71.16
  -> lines 1-3 equal the workbook "T Inquiry Detail Amt Val OE" rows exactly. After the edit, Allocated still shows the original 7 CS and Ordered shows "5 CS 4 PC" for line 1 (unexpected; open question for QA: what Ordered/Allocated mean after an edit) [observed].
- **Total Offering**: Automation2 (BONUS2) -9,684.03; MARCH001 (BONUS2) -650; MARCH002 (TRADEOFFER) -9,684.03; May001 (BONUS2) -650; May003 (BONUS2) -50; Tax 0 each; sum -20,718.06 (= header Discount -20,718.07, rounding) [observed]. Workbook rows 1-3 (-9,684.03 / -650 / -9,684.03) match.
- Workbook "T Inquiry Header Amt Val OE" expects Gross 96,840.34, Discount -20,718.07, Net 90,707 (match) but **Tax 8,728.81** - that is line 1's tax, not the header's 14,584.79 -> framework/workbook drift (would fail in the engine).

## Seq 69 Validate Charges Tax After Sales Return + Seq 71 Transaction Inquiry Validate After Sales Return (Maker) - done; app consistent, workbook values STALE
- Document Type **Sales Return**, 2026-10-05: one document **COL26000000714**, outlet 1000000004, Document Date / Delivery 2026-10-05, Actual Delivery 2026-10-05 10:44:25, Gross **-30,845.86**, Discount **6,189.17**, Tax **-4,419.93**, Offset 0, Net **-29,077**, Document Status **Picked**, Demand Channel **"Partial Return"**, Invoice Ref. No. **COL26000002009** (the return points to its sales invoice) [observed].
- Total Tax: 0001 VAT **-4,419.93**; 9000 3rd Schduele **0** [observed].
- Detail: line 1 62740537 Delivered (returned) 2 CS, Gross -30,845.86, Disc 6,407.54, Tax -4,398.90, Net -28,837.22; **lines 2-5 return 0 quantity but carry small negative discounts/taxes** (20050310 disc -116.35 tax -20.94; 62690363 -61.23; 20050308 -40.31; 69997598 -0.48/-0.09): returning 2 CS of the corn tin re-prices the order's slab promotions, so the return also reverses part of the discount on the other lines [observed; rule inferred].
- Total Offering (return): Automation2 +3,084.59; MARCH001 +10; MARCH002 +3,084.59; May001 +10; May003 0 (sum 6,189.18 = header Discount) [observed].
- Workbook (built 2026-09-21 for outlet 1000000003) expects Discount 6,169.17, Tax -4,425.41 / -4,436.55, Net -29,113, VAT -4,434.18 + 3rd Schedule -1.95, line 1 Disc 6,260.28 / Net -29,010.99 -> **all differ** from today's values while Gross -30,845.86 matches; the app gave the same Net -29,077 in sessions 1 and 2, so the workbook values are stale for the current promotions/outlet (framework drift) [observed].

## Group 11 cycle status
- Seq 1-71 (active rows) now walked across session 2 (seq 1-50, 2026-10-05 morning) and this resume (seq 51-71, same calendar day), with seq 15 skipped and seq 55/56 bypassed by the QA lead. Next: consolidate into the knowledge pages; Senior QA knowledge check.
