# Session log: LEARN-G11-PK/20261005-0921 (session 2, fresh full run, 2026-10-05)

Env cnr1dev1, Unilever Pakistan Limited, distributor 15108843. Business facts only. Compares against session 1 (2026-10-01).

## Segment 1: Maker (Auto_Multi_Orga; QA lead logged in ~09:25)
### seq 1 Login: done (company + distributor pages shown again, same options as session 1).

### Morning baseline (answers Q-OB1): Stock Inquiry 2026-10-05 BEFORE any DA = **"No data", 0 rows**
- On a new day (first use, 10-05 ~09:30) the Stock Inquiry has NO rows, no opening balances. On 2026-10-01 the same screen showed 39 rows with openings at 16:40 and 0 rows in the morning of the same day. So openings are NOT created by the day change itself; something (a movement, the DA approval, or a start-of-day process / Generate Opening Balances by someone) creates them during the day [observed 2026-10-05]. Q-OB1 narrowed: next check after the DA approval (does the approval create openings equal to the previous day's closing?).

### seq 2 Dispatch Advice: done, DA **1359**, ~09:40
- Same header defaults as session 1 (Warehouse default 0000000025-IBT Main warehouse, Vendor UPL WH, DA Type Dispatch Advice, Document Date today). Header: Warehouse C0000000055-Auto Main Warehouse, SO Automation_05-10-2026, Shipment 123, Deliver 12312, Tax Invoice 123, Comments Positive_QA_Learning_02, Reference No 1115 -> Save -> "Saved successfully" -> 1359, Draft.
- 5 lines identical to session 1 (80 / 70 loss 6 / 60 loss 5 / 50 / 40 CS): totals per line identical (1,233,834.40 / 34,597.38 / 173,397.25 / 190,290.50 / 595,336.32), **DA net 2,227,455.842**. Line save "Saved Successfully!" each time; loss window and Calculate behave as before.
- Forward (comment "Automation Approval") -> "Forwarded successfully" -> Pending for approval.
- Reproducible: the same inputs gave the same amounts as 2026-10-01 (prices unchanged over 4 days).

## Login tooling (new, 2026-10-05 ~09:50)
- The QA lead asked whether credentials can come from environment variables. Answer: Claude/Selenium MCP cannot (MCP types literal text; Claude must not enter credentials). Built `runtime/qaos_login.py`: the QA member runs it in their own terminal; it attaches to Claude's Selenium Chrome (started with `--remote-debugging-port=9222`), logs out the current user, types user + password from the gitignored `qa-os/credentials.json` (or env SD_PASSWORD_<USER>), picks company + distributor from app.yaml. Passwords never reach Claude. **First live run (Auto_Tssm): worked.**

## Segment 2: Checker (Auto_Tssm, logged in by script)
### seq 5 DA Approval: done, DA **1359** -> Active / Approved; "Forwarded successfully" (same as session 1).
### seq 7 DA Loss Approval: done, loss record **640** (created at the DA approval, serial +1 vs 639) Pending -> Approved; Checker Forward ON / Reject OFF again; "Forwarded successfully" (reproduces session 1).

- 09:4x: `qaos_login.py --user Auto_Multi_Orga` did NOT work for the second login (error message not captured; first run for Auto_Tssm worked). TODO (QA lead: "come back to this problem" after the flow): get the error text, fix, retest; until then log in manually.

## Segment 3: Maker (Auto_Multi_Orga, logged in manually ~09:52)
### seq 9 Stock Validation After DA: done. **Answers Q-OB1.**
- Stock Inquiry 2026-10-05: before the DA = 0 rows; after the DA approval = **39 rows with Openings** (the whole stock catalogue appears at once, not only the received SKUs).
- **Opening = previous working day's Closing + that day's still-Allocated quantity**: 62740537 Auto Main Opening **308** = 10-01 closing 245 + allocated 63 (GIN 505 of 09-30 is still Pending, so its 63 CS stays allocated); 20050308 2076/11, 20050310 5870/3, 62690363 6312/92, 69997598 2600/165 consistent with 10-01 closings plus allocations [observed 2026-10-05; the rows seem to be created by the first movement of the day (the DA approval), not by the date change].
- DA 1359 In: 62740537 +80, 20050310 +64 (70 - 6 loss), 62690363 +55 (60 - 5), 20050308 +50, 69997598 +40; Out 0; Closing = Opening + In - Allocated (62740537: 308 + 80 - 63 = 325) = exactly session 1's rule. Loss 640 approved: still no Damaged/Lost rows (row count 39).
- Today's stock rows carry other people's reservations (Allocated 63 on 62740537 from the old GIN 505): ATP for orders will be lower than In by that amount.

### seq 10 Order Booking: done, **6 orders COL26000002009-2014**, Delivery Date **2026-10-11** (session 1: 10-07 -> the PJP next visit moved), "Order Save successfully" each, ~09:55
| Order | Outlet | Lines | Net (workbook-equivalent) | Tax |
|---|---|---|---|---|
| COL26000002009 | 1000000004 | 5 lines | 134,372.00 (Gross 143,109.13, Disc -29,971.83, Tax 21,234.24) | 21,234.24 |
| COL26000002010 | 1000000005 | 2 lines | 101,160.73 | 0 (tax-exempt) |
| COL26000002011 | 1000000007 | 2 lines | 119,369.65 | 18,208.93 |
| COL26000002012 | 1000000008 | 1 line | 108,201.79 | 16,505.36 |
| COL26000002013 | 1000000006 | 1 line | 91,696.43 | 0 (tax-exempt) |
| COL26000002014 | 1000000011 | 1 line | 108,201.79 | 16,505.36 |
- **Same amounts to the paisa as session 1** for the same baskets: prices, promotions and tax rules did not change in 4 days [observed 2026-10-05].
- ATP of 62740537 drops by 7 CS per saved order: 325 -> 318 -> 311 -> 304 -> 297 -> 290 (as 10-01). 325 = today's Stock Inquiry closing after the DA approval.
- Only difference: the Delivery Date field (next PJP visit 10-11 instead of 10-07).

### seq 12 Stock Allocation: done, no-op again (Unallocated empty, 6 orders FULL on the Allocated tab).
### seq 14 Transaction Inquiry after OB: done, orders 2009-2014 "Confirmed", delivery 2026-10-11, amounts as booked; identical to session 1.

### seq 15 Order Editing: **SKIPPED AGAIN by the QA lead (~10:00) - to be checked with QA**
New evidence from today's attempt (correct PJP this time, verified via the request log pjpNumber=02111):
- Filters PJP 02111~AutomationOB1 / Selling Category 201 / Section 101010101101 / Date From 2026-10-05, Date To 2026-10-11 (covers the orders' delivery date 2026-10-11) -> **grid and outlet list empty**. Then Date From = Date To = 2026-10-11 -> still **"No data to display"**.
- Requests: getOultetsForOrderEditing ...&dateFrom=2026-10-11&dateTo=2026-10-11&sellingCategory=201 returned nothing.
- On 2026-10-01 the same screen listed the orders only after the orders' delivery date had been moved to TODAY by Delivery Date Change (seq 19) [session 1 seq 29]. So **Order Editing lists orders only whose delivery date is today / the PJP working date (not a future delivery date)**, which means seq 15 (before Delivery Date Change at seq 19) can never find a freshly booked order whose delivery date is a future visit; the 09-29 empty list has the same cause. The earlier hypothesis "Date To must cover the delivery date" (session 1) is WRONG; a future date range does not help [observed 2026-10-05].
- Open for QA: Q-OE1 revised: is seq 15 meant to run AFTER Delivery Date Change, or should orders be booked with a delivery date of today? Workbook edit not done.

## Seq 16 / 18 / 19 (Maker Auto_Multi_Orga, 2026-10-05)
- Seq 16 Order Cancellation: COL26000002014 Cancelled (stock released).
- Seq 18 Stock Unallocation: COL26000002013 unallocated then re-allocated (QA lead option 1), as in session 1.
- Seq 19 Delivery Date Change: PJP 02111~AutomationOB1, 5 orders (2013, 2012, 2011, 2010, 2009), all Confirmed, PJP Delivery No 02112, delivery date 2026-10-11 -> new date 2026-10-05 (default). Header checkbox selects all, Process, confirm "Are you sure you want to proceed?", toast "Delivery Date has been changed successfully, processed orders: 5". Grid now shows delivery date 2026-10-05 for all five. [observed]

## Seq 20 Goods Issue Note (Maker Auto_Multi_Orga)
- Header list: Add -> PJP 02112-AutomationDSR (DSR ITB0189-AutomationQADSR, warehouse C0000000055 Auto Main Warehouse, vehicle 0040-Automation211206 auto-fill), Suggested Type Cashmemo List, Delivery Date 2026-10-05 (only option).
- Cash Memo Selection: 5 cash memos COL26000002009-2013 (delivery date today); header checkbox selects all. Detail tab: Save All -> "Saved successfully." GIN **507** created, status Draft.
- Reopen 507, Forward, comment "Automation Approval" -> "Forwarded successfully"; approval status Pending for approval. Old GIN 505 (09-30) still Pending for approval. [observed]
- Next: Checker Auto_Tssm approves 507 (seq 23).

## Seq 23 GIN Approval (Checker Auto_Tssm; the Maker was logged out by Claude, QA lead typed credentials)
- Goods Issue Note list shows 507 Pending for approval; open, Forward, comment "Automation Approval", Save -> "Forwarded successfully"; 507 leaves the pending list (one Checker Forward approves, as in session 1).
- Quirk: a script-fired click on the comment Save gave "Please add comments" (the Angular model had not registered the typed text); a real click worked. [observed]

## Seq 24 Stock validation after GIN (Maker; Stock Inquiry, Daily, 2026-10-05)
- 62740537 RAFHAN OILS 2X10L, Auto Main Warehouse, Sound: Opening 308, In 80, Out 35, Allocated 63, Closing 290. Out 35 = 5 orders x 7 CS (GIN 507 approval moved Allocated -> Out); the 63 still allocated belongs to old GIN 505 (09-30). Same as session 1. [observed]
- Grid is paged (3 pages of 15); the product sits on page 3. Auto_Tssm has no Stock Inquiry (needs Maker).
- Login: after the QA lead types credentials the app may still show Company then Distributor selection; Claude selects Unilever Pakistan Limited and 15108843-IBRAHIM TRADERS (Proceed button needs a real click on the button, not on the text).

## Seq 29 Order Editing After GIN (Maker)
- Order Editing: PJP default was AUTO241602~Auto917248 (not 02111~AutomationOB1; must be re-picked, which clears Section/Category); Selling Category 201-Selling Category 001 re-picked; Outlet 1000000004 (auto-filled with the SKU 69997598 filter); dates today. Grid shows COL26000002009 with the SKU-filter defect (Gross 76.72 vs whole-order discount/tax -> Net -8,660.8), as in session 1.
- Open order COL26000002009, edit line 62740537 Order 7/0/0 -> 4/0/0 (gross recomputes to 61,691.72), Reason Type "Order Change QTY" (options: Order Change QTY, Wrong Order /No Order, No Scheme, Stock Already Avl.), line Save, Validation -> "Validation successfully", Save -> "Order Save successfully".
- Totals: Gross 96,840.34, Discount -20,718.07, Tax 14,584.79, Net 90,707.00 = workbook and session 1 exactly (line 1 discount -13,198.36). [observed]

## Seq 31 Order Cancellation After GIN (Maker)
- Order Cancellation opens with PJP 02111 - AutomationOB1, dates today, outlet auto-filled (04). Outlet list holds only outlets with open orders (04, 08, 05, 07, 06). Outlet 1000000006 -> COL26000002013 (Net PKR 91,696, order date = delivery date = 2026-10-05).
- The Cancellation Reason column and checkbox sit at opposite ends of the horizontally scrolling grid (reason options: Bad Weather, Credit Exceeded, Law & order Issue, Shop Closed). Shop Closed + tick row + Cancel All -> "Order Cancellation Status": COL26000002013 | Successfull | Order Cancelled Successfully. Allowed after the approved GIN 507, no warning (Q-OE3). [observed]

## Seq 32 Cashmemo Reschedule (Maker)
- Header Order Date today, Delivery Date = NEW date (set FIRST via calendar popup: 2026-10-06; changing it clears selection), PJP Number default AutoPJGIN2 -> 02112~AutomationDSR. Grid lists the 4 cash memos on GIN 507 that are not cancelled (2009-2012; 2013 is gone), all "Ready to dispatch/Packed", amounts 90,707 / 101,161 / 119,370 / 108,202 (2009 shows the edited Net 90,707).
- COL26000002012 (outlet 08): tick row, Reschedule Reason (in-row dropdown, 14 options incl. duplicates) "Shop Closed", Process, confirm "Are you sure you want to proceed?" -> "Process completed successfully"; row leaves the list. [observed]

## Seq 33 Cashmemo Status (Maker)
- Menu Cashmemo Status: PJP default AutoPJGIN2-Auto GIN PJP DM -> 02112-AutomationDSR; second dropdown GIN auto-set to GN-01~507. Grid (Document No, Outlet, Document Date, GIN Number, Delivery Date, Demand Channel, Document Status "Ordered", Gross, Tax, Net): 2009 (Gross 96,840.34, edited), 2010 (126,688.41 / Net 101,160.73), 2011 (126,688.41 / Tax 18,208.93 / Net 119,369.66). 2012 (rescheduled) and 2013 (cancelled) absent.
- Header checkbox selects all 3, Save -> "Updated successfully"; rows leave the list. [observed]

## Seq 34 Sales Return (Maker)
- Transaction > Sales Return (first of two menu entries). PJP default AutoPJGIN2 -> 02112-AutomationDSR; the grid lists delivered/Cashmemo-Status-saved cash memos 2009 (Gross 96,840.34 / Disc 20,718.07 / Tax 14,584.79 / Net 90,707), 2010, 2011. Click the row (highlighted), Save -> "Record Saved Successfully!", return **COL26000000714** (principle invoice COL26000002009), Detail tab enabled.
- Detail: lines with Invoice Qty and Return Qty; line 1 (62740537): Return CS 0 -> 2, Reason Type "No Cash" (options: No Cash, Wrong Order/No Order, Shop Closed, Credit Exceeded), Stock Type Sound; line Save -> Gross 30,845.86. validation -> "Validation successfully"; totals Gross 30,845.86 / Discount 6,189.17 / Tax 4,419.93 / Net 29,077.00 (= session 1 and workbook). Save -> "Save successfully"; Forward button enabled. [observed]
- Quirk: typing a digit into a stale-zero grid cell gives "02"; Home + Delete fixes it.

## Seq 36 Sales Return View (Maker forward)
- Sales Return View: PJP default AutoPJGIN2 -> 02112-AutomationDSR; lists COL26000000714 (principle invoice COL26000002009, Gross 30,845.86). Tick, Forward, Comments dialog (mandatory) "Automation Approval", Save -> result window "Sales Return Status": COL26000000714 | Sales Return | Success. [observed]
- Process rule from QA lead: ALWAYS enter the comment and verify the textarea holds it before Save (first attempt today sent an empty box because the typing did not land before the dialog was ready).

## Seq 37 Sales Return View Approval (Checker Auto_Tssm)
- Login: after the QA lead typed credentials the app went straight to the home page (company and distributor already applied this time).
- Sales Return View: PJP list has all 13 PJPs for the Checker; 02112-AutomationDSR -> COL26000000714; tick, Forward, comment "Automation Approval" (textarea verified filled), Save -> "Sales Return Status": COL26000000714 | Sales Return | Success. Same screen and button as the Maker (approval = different user). [observed]

## Seq 38 Sales Return Status Change (Maker)
- Login after Checker: app showed Company then Distributor selection; Claude picked Unilever Pakistan Limited and 15108843-IBRAHIM TRADERS (Proceed = real click on the button).
- Sales Return Status Change: PJP 02112-AutomationDSR, GIN auto GN-01~507; lists the approved return COL26000000714 (principle invoice 2009). Opening it needs a real double-click on the row; Detail tab, Validation -> "Validation successfully", button "Save Sale Pick" -> "Save successfully". Return picked. [observed]

## Seq 39 Deposit Slip Full Amount Cash (Maker)
- Transaction > Receivable > Deposit Slip. Header fields: Deposit Slip No (auto), PJP-DSR (default 02111 - AutomationOB1; must be 02112 - AutomationDSR), Deposit Date (auto today), Type (Cash/Cheque), Status (Un Posted), Bank, Bank Branch, Deposit Amount. Header list shows every slip (older slips 1129-1136 from 09-29/10-01 still there; 1129/1130 Posted, 1131-1136 Un Posted).
- Cash slip 02112 / 101161 -> Save -> "Saved successfully", slip **1137** (Un Posted, Adjusted 0). Tab "Outstanding Cash memos" lists open cash memos of the PJP: today's 2009 (90,707), 2010 (101,161), 2011 (119,370) AND the old 10-01 ones (2004, 2005 with Un Posted Amount = allocated on other unposted slips).
- Deposit-Amount cell on COL26000002010 -> 101161 (click cell, type digits, Tab) -> Save All -> "Record saved successfully!". [observed]

## Seq 40 Deposit Slip Full Amount Cheque (Maker)
- Add (clears header; defaults PJP-DSR back to 02111) -> PJP-DSR 02112 - AutomationDSR, Type Cheque, Bank "Bank Al-Habib Limited" (header Bank list has ~48 entries incl. test junk; Bank Branch "DHA Branch" fills itself), Deposit Amount 119370, Save -> "Saved successfully", slip **1138**.
- Quirk: the header PJP-DSR dropdown stops opening after other fields are set; click its arrow icon (dx-dropdowneditor-icon) instead.
- Outstanding Cash memos row COL26000002011: Cheque No. 1234501, Cheque Date 2026-10-05 (typed), Bank_Name (a DIFFERENT bank list: Bank tdm, National Bank of Pakistanss, SME Bank, United Bank Limited, ...; select by typing "National Bank" then clicking the filtered option), Deposit-Amount 119370, Save All -> "Record saved successfully!". [observed]

## Seq 41 Deposit Slip Unposted Amount (Maker, learning variant)
- Slip 02112 / Cash / 1000 -> "Saved successfully", slip **1139**. Outstanding Cash memos, COL26000002009 Deposit-Amount 600 (deliberately partial of its Net 90,707), Save All -> "Record saved successfully!". Slip Adjusted = 600 of 1,000. [observed]

## Seq 42 Deposit Slip Multi Cheques (Maker)
- Slip 02112 / Cheque / Bank Al-Habib Limited / 1000 -> "Saved successfully", slip **1140** (Bank Branch DHA Branch filled itself on save). Tab "Outstanding Outlet" (outlet-level grid: Outlet Code, Desc, Net, Received, Balance, Un Posted, Deposit Amount, Action "+"; outlet 04 Net 181,414, Un Posted 4,200 = old allocations on unposted slips).
- Tick outlet 1000000004, click "+" in its Action cell (button grid-button-0) -> popup "Cheque Details" (grid Cheque No., Cheque Date, Bank, Net Amount; blue "+" adds a row; row Save / Cancel). Four rows: 12444 / 10/05/2026 / National Bank of Pakistanss / 200; 22337 / 300; 12222 / 400; 1234567 / 100 (cheque date format MM/DD/YYYY, shown back as 10/5/2026; bank typed + filtered). "Save Changes" closes popup and sets outlet Deposit Amount 1,000. Save All -> "Payment Adjusted Successfully". [observed]

## Seq 44 Deposit Slip Cheque (Maker)
- Slip 02112 / Cheque / Bank Al-Habib Limited / 1000 -> slip **1141**. Outstanding Cash memos row COL26000002009: Cheque No. 1234567 (same number as one cheque of slip 1140's multi-cheque list; accepted again = duplicate-cheque defect candidate), Cheque Date 2026-10-05, Bank_Name National Bank of Pakistanss, Deposit-Amount 1000.
- First Save All gave "Required Fields are empty!": another cash memo row (old 10-01 COL26000002005, 119,370) had been ticked by accident and has no cheque details. A row with its checkbox ticked must have Cheque No/Date/Bank when the slip is a cheque slip. Untick (the checkbox column is scrolled off-left; scroll the grid left first), Save All -> "Record saved successfully!". [observed]

## Seq 46 Deposit Slip Cash (Maker)
- Slip 02112 / Cash / 1000 -> slip **1142**; Deposit-Amount 1000 on COL26000002009 (Un Posted Amount there was 1,600 from the 600 + 1,000 on earlier slips); stray old-row tick again removed; Save All -> "Record saved successfully!".
- Deposit slips today: 1137 (cash 101,161 -> 2010), 1138 (cheque 119,370 -> 2011), 1139 (cash 1,000, 600 allocated -> 2009), 1140 (cheque 1,000, 4 cheques 200/300/400/100 on outlet 04), 1141 (cheque 1,000 -> 2009), 1142 (cash 1,000 -> 2009). All Un Posted. Learning note: 2009's Net is 90,707 but it also received 600 + 1,000 + 1,000 across slips (and the multi-cheque 1,000 at outlet level). [observed]

## Seq 48 Good Return Note (Maker)
- Transaction > Goods Return Notes: Add; Delivery Man PJP 02112-AutomationDSR -> DSR ITB0189-AutomationQADSR, warehouse C0000000055-Auto Main Warehouse, vehicle 0040-Automation211206, GIN 507 fill; Detail tab: one line 62740537 Suggested **19 CS** (= 7 cancelled 2013 + 3 cut from 2009 + 7 rescheduled 2012 + 2 returned) with Actual prefilled 19, rate 7,711.47. Save All -> "Record Saved Successfully", GRN **247** (Draft, In-Active). Reopen, Forward, comment "Automation Approval" (verified filled), Save -> "Forwarded successfully", Pending for approval. Same quantity as session 1 (19 CS). [observed]

## Seq 49 GRN Approval (Checker Auto_Tssm)
- Goods Return Notes grid lists 247 (Pending for approval, 2026-10-05) plus old pending 232/231 from 08-21. Open 247, Forward, comment "Automation Approval" (verified), Save -> "Forwarded successfully"; 247 leaves the pending list (approved). Same screen/button as the Maker. [observed]

## Seq 50 Stock validation after GRN (Maker; Stock Inquiry Daily 2026-10-05)
- New browser session (the old one expired after the Checker logout; QA lead asked to close and restart; Chrome relaunched with the debugging port).
- 62740537 Auto Main Sound: Opening 308, In **99** (was 80, +19 from GRN 247), Out 35 (unchanged), Allocated 63 (old GIN 505), Closing **309** (was 290, +19). Same as session 1: GRN approval posts the returned goods as In. [observed]

## Seq 51 Route Settlement (Maker) - STOPPED (per QA lead instruction)
- Transaction > Receivable > Route Settlement, Date 2026-10-05, all PJPs listed, totals header Total Payable PKR 224,131 / Total Received PKR 224,131 / Cash Shortage 0. Row 02112-AutomationDSR (AutomationQADSR): Total Order 13, Delivered 3, Undelivered 0, Sale Value PKR 311,238, Adjusted Credit Note Amount 0, Fresh Return Value 0 (the approved sales return still does NOT appear as an adjusted credit note), Total Cash Collected today 102,761 (= 101,161 + 600 + 1,000), cheque collected PKR 1,000?/120,370 (=119,370+1,000), collection lines 1137-1142 with suggestedAmount/enteredAmount (cheque 1138 119,370; 1140 1,000; 1141 1,000; cash 1137 101,161; 1139 600; 1142 1,000).
- Clicking Edit on the 02112 row -> modal Error: "Following previous days not closed! Please close date. **2026-10-01**" (Continue button). Previous blocker was 2026-09-30; now the oldest unclosed day is 2026-10-01 (so 09-30 was closed in the meantime or the check lists one date at a time). Day-close method still unknown (Q-RS1). Run stopped here; QA lead to decide. [observed]
