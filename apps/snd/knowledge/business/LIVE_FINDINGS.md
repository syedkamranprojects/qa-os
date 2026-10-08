# Live findings (append-only)

Environment cnr1dev1 (https://dcodecnr1dev1.unilever.com/ngui), user Auto_Multi_Orga (Maker / Stock Controller), company Unilever Pakistan Limited, distributor 15108843 (org 010104). Provenance tags: observed = live UI, db-declared = snd-schema read-only SELECT, inferred = reasoning.

IMPORTANT caveat for all db-declared lines: the snd-schema connector points to database `ng_astrone`, whose newest cash-memo row is dated 2026-01-30 and which holds NO row for COL26000001979-COL26000002002. It is therefore NOT the cnr1dev1 data set (it is a metadata/base copy). Its master data (status descriptions, reason types, workflows) is used as db-declared evidence, but live data could not be cross-checked in it.

## Block 1 (2026-10-01)

### L01 Stock Inquiry, Balance Date 2026-09-30 (observed)
What I did: opened Stock Inquiry (/ngui/dyl/layout?layoutCode=201069), typed 2026-09-30 into Balance Date (real key events + Enter), Period Type = DAILY (default), Category All, Brand All, clicked Show Inquiry. Grid "39 rows, 21 columns", 3 pages of 15/15/9, read with the pager (no row clicks). Columns: Category, Brand, Product Name, Warehouse, Batch, Stock Type, then Opening/In/Out/Allocated/Closing each CS/DZ/PC.

Findings:
- Warehouses: Auto Main Warehouse, IBT Main warehouse, test wh 1, SAN Warehouse A. Batch is always 1-1.
- Stock types present: 01 - Sound (36 rows), 11 - Variance (2 rows: 20043109 in IBT Main warehouse 10000 CS, 20061858 in Auto Main Warehouse 374 CS), 02 - Damaged (1 row: 20080958 in SAN Warehouse A, 83 CS / 4 PC). No 04 or other types.
- Rows with ANY Out (CS/DZ/PC): none (0 of 39). Out is 0 everywhere because GIN 505 (Pending for approval) has not been approved.
- Rows with In: one. 62740537 / Auto Main Warehouse / 01 Sound: Opening 80 CS, In 80 CS, Allocated 63 CS, Closing 97 CS (the 80 CS In is the DA received on 2026-09-30).
- Rows with Allocated > 0 (13): 20050308 Auto Main (39 CS 96 PC), 20050308 IBT (134 CS 6 PC), 20050310 Auto Main (85 CS), 20050310 IBT (135 CS), 20061858 IBT (203 CS 9 PC), 20080958 IBT (76 CS), 62690363 IBT (77 CS 61 PC), 62690363 Auto Main (53 CS 32 PC), 62740537 Auto Main (63 CS), 62740765 IBT (7 CS 1 PC), 69993785 IBT (5 CS), 69997598 IBT (180 PC), 69997598 Auto Main (96 PC).
- Allocated for 62740537 / Auto Main (63 CS) equals the GIN 505 line (63 CS). For 20050308 Auto Main, allocated 39 CS 96 PC is larger than the GIN 505 line (18 CS 16 PC), so allocation also covers other pending documents; the others were not traced.

Identity test Closing = Opening + In - Out - Allocated, per unit column (CS, DZ, PC) taken literally:
- Holds on 37 of 39 rows in all three units literally.
- FAILS literally on 2 rows, both only because of carry between PC and CS (the system borrows a case when PC goes negative); both hold in base units:
  - Row 5: 20050308 BLUE BAND MARGARINE 32X250G, Auto Main Warehouse, 01 Sound. Opening 1978 CS/0 DZ/21 PC, Allocated 39 CS/0/96 PC, Closing shown 1936 CS/0/21 PC. Literal: 1939 CS / -75 PC. In base units with 32 PC per CS (from the product name): 1978*32+21 - (39*32+96) = 61,973 = 1936*32+21. HOLDS in base units (the 96 PC allocated = 3 CS borrowed).
  - Row 12: 20061858 LIFEBUOY HWL RED REF 12X180ML, IBT Main warehouse, 01 Sound. Opening 310988 CS/0/3 PC, Allocated 203 CS/0/9 PC, Closing shown 310784 CS/0/6 PC. Literal: 310785 CS / -6 PC. With 12 PC per CS: 310988*12+3 - (203*12+9) = 3,729,414 = 310784*12+6. HOLDS in base units (1 CS borrowed = 12 PC).
  - So the identity holds on all 39 rows once units are normalised with the pack factor taken from the product name (NNxSIZE); per-unit literal comparison fails only when allocated PC exceeds opening PC.
- Rows with PC-only subtraction that still balance literally (no borrow needed): 20050308 IBT (3814-134=3680 CS, 28-6=22 PC), 62690363 rows, 69997598 rows.
- Closing CS/PC never negative. DZ is 0 on every row and column.
- "Allocated" is subtracted from Closing on every row (Closing is available stock, not physical stock).
Answers/affects open question Q11: Closing = Opening + In - Out - Allocated is the screen's identity (Closing is net of Allocated); the two literal failures (rows 5 and 12) are PC-to-CS carry cases and hold in base units (32 and 12 PC per CS); automation must assert the identity in base PC units, not per column.

### L02 Stock Inquiry for today (observed)
Opened the same screen; Balance Date default = today 2026-10-01, Period Type DAILY, Category All, Brand All. Show Inquiry returned "Data grid with 0 rows and 21 columns" / "No data". Generate Opening Balances was NOT clicked.
Answers/affects open question Q10 evidence (a new day has no balance rows until something creates them; BA1).

### L03 Transaction Inquiry (observed)
Document Type options (17): Demand Captured from Tele order, OFF INVOICE CREDIT NOTE, DSR Shortage Amount, Amount Wise, Dsr Adj (SKU Wise), Sales, Sales Return, Fresh Sales Return, B2B Sale, Sales return without reference, Customer Account Close, Credit Note, Credit Note (Sales Return), Credit Note (Fresh Return), Credit Note (Sales Return W/O Ref), Off Invocie Credit Note (sic), Return Request. Default is "Demand Captured from Tele order".
Document Status filter options: All, CM-01 - Ordered, CM-01 - Confirmed, CM-01 - Planning completed, CM-01 - Cancelled, CM-01 - Delivered/Invoiced, CM-01 - Dispatched, CM-01 - Sent to Locus, CM-01 - Ready to dispatch/Packed, CM-01 - Reattempt, CM-01 - Out for delivery.
Other filters: PJP Number (All), Document Date From / To (typed with Tab), SKU (All). Chose Sales, 2026-09-29 to 2026-09-30, Refresh: 24 rows (5 per page, 5 pages).
Grid columns (19): Document No, Outlet Code, Outlet Long Name, Order Booker/Delivery Man, PJP Number, Order Time, Document Date, Delivery Date, Actual Delivery Date, Gross Amount, Discount Amount, Tax Amount, Offset Amount, Net Amount, Document Status, Demand Channel, DDT Ref No, GIN No, Invoice Ref. No. There is NO separate "Execution Status" column: the single "Document Status" column shows the execution-status text. Row buttons: Detail, Product Wise Discount, Product Wise Free Quantity, Total Offering, Total Tax, Credit Note Adjustments (Product Wise* disabled until a row with that data is chosen).

The eight target orders (all Document Date 2026-09-29, Delivery Date 2026-09-30, Actual Delivery Date empty, PJP 02111, Order Booker "AutomationOB / AutomationQADSR", Demand Channel Back Office (BO), GIN No 505, Invoice Ref. empty, Offset Amount 0):

| Order | Outlet | Time | Gross | Discount | Tax | Net | Document Status |
|---|---|---|---|---|---|---|---|
| COL26000001995 | 1000000001 | 17:25:00 | 143,109.13 | -29,971.83 | 21,861.52 | 134,999 | Planning completed |
| COL26000001996 | 1000000002 | 17:30:25 | 143,109.13 | -29,971.83 | 21,234.24 | 134,372 | Planning completed |
| COL26000001997 | 1000000003 | 17:31:55 | 143,109.13 | -29,971.83 | 21,992.03 | 135,129 | Planning completed |
| COL26000001998 | 1000000004 | 17:33:12 | 143,109.13 | -29,971.83 | 21,234.24 | 134,372 | Planning completed |
| COL26000001999 | 1000000005 | 17:34:32 | 143,109.13 | -29,971.83 | 0 | 113,137 | Planning completed |
| COL26000002000 | 1000000006 | 17:35:49 | 143,109.13 | -29,971.83 | 0 | 113,137 | Planning completed |
| COL26000002001 | 1000000007 | 17:37:07 | 143,109.13 | -29,971.83 | 21,397.32 | 134,535 | Planning completed |
| COL26000002002 | 1000000008 | 17:37:47 | 107,960.51 | -16,264.08 | 16,505.36 | 108,202 | Planning completed |

Total Offering panel (per order, Discount column; sum equals the header Discount Amount, tax 0 on every promo line):
- 1995-2001 (identical): Automation2 BONUS2 -14,310.91; MARCH001 BONUS2 -650; MARCH002 TRADEOFFER -14,310.91; May001 BONUS2 -650; May003 BONUS2 -50. Sum -29,971.82 vs header -29,971.83 (1 paisa rounding).
- 2002: Automation2 -5,398.03; MARCH001 -10; MARCH002 -10,796.05; May001 -10; May003 -50. Sum -16,264.08 = header exactly.
Net = Gross + Discount + Tax rounded to whole PKR (e.g. 143,109.13 - 29,971.83 + 21,861.52 = 134,998.82 shown as 134,999). Net is rounded to integers; Gross/Discount/Tax keep 2 decimals.
Other statuses in the same range: Cancelled (1979-1986, 1993, 1994), Delivered/Invoiced (1987, 1989-1992, with Actual Delivery Date 2026-09-29 15:14:4x and GIN 504) and one more in 'Planning completed' / GIN 505: COL26000001988 (outlet 1000000002). So GIN 505 holds 9 cash memos: 1988, 1995-2002.
Does the text say 'Confirmed' or 'Ordered'? NO. Only "Planning completed", "Cancelled", "Delivered/Invoiced" appear for these 24 documents. 'Confirmed' and 'Ordered' exist only as filter options.
Surprises: PJP Number column shows 02111 (the order-booker PJP); the Delivery PJP (02112) is visible only on the GIN. Orders 1993 and 1986 show a Delivery Date 2026-10-05 while Cancelled.
Answers/affects Q23 (the Document Status column is the execution status; 'Planning completed' = execution 03), Q28 and Q30 baselines (Delivery Date 2026-09-30 and no Delivery-PJP column on this screen).

### L04 Status descriptions (db-declared, snd-schema)
snd_pr_dos_documentstatus (document status), org 010104, CM-01: 01 Delivered (DEL, active), 02 Un-Delivered (UDL, INACTIVE), 03 Cancelled (CNL), 04 Ordered (abrv Order, nature PLD), 05 Amendment (AMD, inactive). CM-02: 01 Authorized (AT), 02 Un-Authorized (UA), 03 Cancelled, 04 Picked (PIC).
glb_pr_exs_execution_status (execution status), org 010104, CM-01: 01 Ordered (CRT, PLD, filter 1), 02 'Confirmed ' (ALC, identifier ALC, trailing space), 03 Planning completed (DISPT, identifier GIN, ref status 02), 05 Cancelled, 07 PLANNING, 08 EXECUTING, 09 PARKED, 10 Delivered/Invoiced (DEL), 11 Dispatched, 12 Sent to Locus, 13 Ready to dispatch/Packed (GINAPPRVD), 14 Danone Pending, 15 Danone Blocked, 16 Danone UnBlocked, 17 Danone Completed, 18 Partial Delivered, 20 Out for delivery. Codes 04, 06, 19 do not exist. CM-02 execution: 01 Authorized Un-Picked, 03 Cancelled, 04 Picked, 05 Un-Authorized Un-Picked.
Answer: 'Confirmed' is its OWN execution status 02 (identifier ALC = allocated), not an alias of document status 04 Ordered; Ordered exists twice (document status 04, execution status 01). Execution 03 'Planning completed' has pexs_ref_exection_status 02, i.e. it follows 'Confirmed'. The Transaction Inquiry status text therefore comes from the execution table. The order numbers themselves were not found in this database (see caveat), so the per-order codes could not be verified.
Answers Q23.

### L05 GIN approval workflow (db-declared, snd-schema)
Event table wkf_wf_weo_wrkflw_event_orga maps event GIN to workflow per org: org 010104 and 010105 use `StockUpdateGIN`; orgs 0101 and 0102 (parents) use `StockUpdateGIN4Level`. Event ginApprovalSaga uses GINApprovalSaga for 010104; GINMOB (API) uses GINAPIApproval; ginManualApprovalSaga uses GINManualApprovalSaga.
Camunda definitions (act_re_procdef / act_ge_bytearray):
- StockUpdateGIN latest v53 (the one org 010104 uses): 2 user tasks in sequence, "Verify" then "Approve", BOTH candidate group 0005. Role 0005 in 010104 = "Distributor Role" (srol_isauthorizer N, PBI role Distributor). Process starter group also 0005. Gateways: forwarded false loops/returns to Verify; cancelled true ends the process; the end listener is class com.centegy.snd.workflow.processes.StockUpdateProcess (this applies the stock update).
- StockUpdateGIN4Level v3 (not used by 010104): 4 user tasks: Verify (group 0005), Approve 1 (0008), Approve 2 (0005), Final Approve (0008). Role 0008 in 010104 = "Territory Manager Role" (srol_isauthorizer Y).
- GINApprovalSaga v29 service tasks (after final approval): MarkGinApprovedSaga, MarkGinApprovedReversalSaga, updateStock, DecreaseCashmemoQuantity, DeleteCMReference, revertCMReferencesByGinno, GeneratePjpHeadDailySaga.
- Field setting for GIN event: docStatus 02 to 01, status I to A (In-Active to Active at final approval).
Answer: org 010104 declares TWO approval steps (Verify, Approve) both for the Distributor role 0005, so no separation of duty is declared in the workflow; four levels exist only for the parent orgs. Whether Auto_Multi_Orga and Auto_Tssm hold role 0005 / 0008 could not be checked (neither user code appears in smm_pr_url_userroles; user TSSM has role 0008 in 010104).
Answers Q35.

### L07 Reason lists (observed screens + db-declared lists)
UI: Order Editing (/ngui/order-editing) and Order Cancellation (layoutCode=202022) and Cashmemo Reschedule (layoutCode=202053) all have the reason control only INSIDE a data-grid row (columns: Order Editing grid has no reason column until an order is opened; Order Cancellation grid has column "Cancellation Reason"; Cashmemo Reschedule grid has column "Reschedule Reason"). No order is currently eligible (all 24 orders are Planning completed / Cancelled / Delivered), so every grid was empty and the dropdowns could not be opened. Searches tried: Order Editing PJP 02111, dates 2026-09-29..30 (0 rows); Order Cancellation PJP 02111, 2026-09-29..2026-10-05 (0 rows); Cashmemo Reschedule order date 2026-09-29, delivery 2026-09-30, PJP 02112 (0 rows).
Observed quirk: Order Cancellation Refresh returned "Required parameter 'toDate' is not present." when Date To was typed (even with Tab/Enter); it worked only after picking the date from the calendar popup. Typed dates are not always committed on this screen.
Db-declared lists (glb_pr_rnt_reason_type, org 010104, doc type CM-01; identifier CNL = cancel, ORC = order change, VST = visit):
- Cashmemo Reschedule Reason: datalist REASNCMRESCH, grid filter doc type CM-01 and identifier CNL, no active filter in the datalist. Options with CNL: 0017 Shop Closed (A), 0018 Delivery is not possible due to any reason (A), 0019 Customer cancels delivery (A), 0021 customer refused (A), L02L01L01L01 Credit Exceeded (A), L02L02L03L01 Shop Closed (A), L02L03L04L01 Bad Weather (A), L02L03L04L02 Law & order Issue (A). (0901 TRE is doc type CM and inactive.)
- Order Cancellation Reason: grid page config not in DB (layout 202022 panel 3 is hand-coded); inferred to use the same CM-01/CNL list above.
- Order Editing Reason Type (ORC, CM-01, active): 0008 Order Change, 0009 Order Change QTY, 0010 Change Utlity (sic), 0020 Bogus order, 1001 testDesc, L01L01L01 Wrong Order/No Order, L01L01L01L01 Wrong Order/No Order, L02L04L07 No Scheme, L02L04L07L01 No Scheme, L02L06L09L03 Stock Out, L0L1L1 Stock Already Avl., L0L1L1L1 Stock Already Avl. (inferred that Order Editing uses the ORC identifier).
Surprises: duplicate descriptions (Shop Closed x2, Wrong Order x3, Stock Already Avl. x2, No Scheme x2), test entries (1001 testDesc), and a typo "Change Utlity". The reschedule list is the cancellation list, not a reschedule-specific list.
Not done: opening the real dropdowns (needs an order in Ordered/Confirmed status; none today). Retry after a new order is booked.
Answers/affects Q22 (partially: lists db-declared, not observed).

### L08 Stock Adjustment SAN (observed)
Opened /ngui/dyl/layout?layoutCode=201045; grid 164 rows (SAN Header). Form fields: Document No *, Document Date (default today), SAN Type * (id documentType), From Warehouse * (DDL__epp1_busent_code_phs_lvl1_b), To Warehouse (..._e), Comments, Status (In-Active), Approval Status (Draft). Buttons: Add, Save (enabled), Update/Delete/Forward/Reject disabled; SAN Detail tab disabled. Nothing saved.
SAN Type options (5): Warehouse To Warehouse Transfer (default), Stock Adjustment Entry, Stock Adjustment Admin, Physical Stock Reconciliation, Stock Adjustment From Transfer (Auto). Db-declared codes: SA-01 Warehouse To Warehouse Transfer (nature SWT), SA-02 Stock Adjustment Entry (SAN_EQL), SA-03 Stock Adjustment Admin (SAN_ADJ, calcnature +), SFT Stock Adjustment From Transfer (Auto). Physical Stock Reconciliation has no row in snd_pr_dot_documenttype by that name search (not found by description match).
From Warehouse list (45): 0000000025-IBT Main warehouse, C0000000055-Auto Main Warehouse, C0000000195-SAN Warehouse A, C0000000196-SAN Warehouse B and ~41 warehouses all named "Automation" (C0000000161-...C0000000215). To Warehouse list has the same set minus IBT Main warehouse (44). Status dropdown shows no list (read-only text). Default From = IBT Main warehouse, To = Auto Main Warehouse.
Which type reads as an OTC stock out? None is labelled OTC or "stock out". The closest is Stock Adjustment Admin (SA-03, nature SAN_ADJ; all 94-95 recent grid rows are Stock Adjustment Admin from Auto Main Warehouse with no To Warehouse), i.e. a single-warehouse adjustment. This is an inference only; BA must confirm.
Sidebar search "OTC": no results (a control search for "Stock Adj" returned exactly "Stock Adjustment SAN", so the search works). No "OTC Stock Out" menu entry exists.
Answers/affects Q57 (no OTC type or menu; candidate = Stock Adjustment Admin, inferred) and Q58 (SAN type decides stock direction).

### L09 PJP Daily Inquiry Update (observed + db-declared)
Opened layoutCode=BG1022 (Distributor Setup > Journey Plan). Filter: Working Date (default today). Grid 8 rows, 8 columns: PJP Number, DSR, Current Status, Mark Status, DSR Files Status, Working Date, Start Date, End Date, Edit link. Mark Status and DSR Files Status are blank for all rows and only become dropdowns in Edit mode (Edit not clicked), so the live lists were not observed.
Db-declared (page BG1022002 config): Mark Status (epjp_journey_status) fixed list = E "End of Day" (single value). DSR Files Status (epjp_dsr_file_status) fixed list = P "process", C "complete" (captions are DYP.G translations).
Answers Q55 (db-declared; confirm labels live in Edit mode on a throwaway).

### L10 Goods Issue Note, Maker view (observed)
Screen /ngui/good-issue-notes/GIN, 14 GINs in the grid, 3 pages (5 per page). Statuses seen: Pending for approval (505, 169, 131, 128, 113, 69, 67, 61, 27), Rejected (104, 103), Draft (29, 22, 20). Status column is In-Active on all. GIN 504 (earlier delivered orders) is not in the list (approved GINs drop out).
Header fields: GIN No, GIN Date, Delivery Man PJP, Delivery Man DSR, Warehouse, Vehicle, Suggested Type (Cashmemo List), Status, Delivery Date, Approval Status. Tabs: Header, Cash Memo Selection, Detail.
Button states for Auto_Multi_Orga (read from aria-disabled, nothing clicked):

| Record | Add | Forward | Reject | Terminate | Cash Memo Selection tab: De-linking | Detail tab: Save All | Detail tab itself |
|---|---|---|---|---|---|---|---|
| 505 Pending for approval | enabled | DISABLED | DISABLED | DISABLED | DISABLED | DISABLED | enabled (shows lines) but Detail header button on Header tab disabled before opening |
| 29 Draft | enabled | ENABLED | DISABLED | DISABLED | ENABLED | ENABLED | enabled |

Cash Memo Selection for 505: 9 cash memos (1988, 1995-2002), all Order Type 01-Back Office (BO), Order Booker PJP 02111-AutomationOB1, Delivery Man PJP 02112-AutomationDSR, Section 101010101101-Automation_Testing_Section. Detail (Gin Detail) for 505: 5 SKU lines, Current Stock 0-0-0 for every line (Suggest = Actual): 20050308 BLUE BAND 18 CS/16 PC, 20050310 40 CS, 62690363 24 CS/16 PC, 62740537 63 CS, 69997598 48 PC. For Draft 29: 6 lines (e.g. 20043109 45 CS 72 PC, 62740537 81 CS), Current Stock 0-0-0.
No "View Approval Log" or any log/history control exists on the Maker GIN screen (searched all visible text), so no approval log was read.
Not done: Checker (Auto_Tssm) button states (only the Maker session is open; no login/out allowed). Reject/Terminate are disabled for the Maker on Draft and on Pending; Forward is the only Maker action on a Draft, and it is disabled once Pending (the checker owns the next step).
Answers/affects Q36 (De-linking is enabled on a Draft GIN and disabled on a Pending one for the Maker), Q37 (Maker cannot Terminate/Reject a Draft or Pending GIN; checker side still to observe). Note: Current Stock shows 0-0-0 even though Stock Inquiry shows available stock, which suggests Current Stock is net of allocation or is not populated once allocated.

## Block 2a (2026-10-01)
Actor: Auto_Multi_Orga (Maker), cnr1dev1, distributor 15108843. Maker-only, no approvals.

### L11 Duplicate SO Number
- DA **1353**: Warehouse C0000000055-Auto Main Warehouse, Vendor UPL WH, SO Number LEARN_SO_01, Save -> toast "Saved successfully", Document No 1353 (Status In-Active, Approval Status Draft).
- DA **1354**: same SO Number LEARN_SO_01 -> "Saved successfully", Document No 1354. **Duplicate SO Number is allowed**; no warning, no refusal.
- DA **1355**: SO Number empty -> "Saved successfully", Document No 1355. **SO Number is not mandatory.**
- None forwarded (all Draft). Answers/affects open question on SO Number uniqueness (no uniqueness rule in the app on Save).
- Surprise: after pressing **Add** (for the 2nd DA) the form resets with Warehouse, Vendor Code AND **DA Type** empty (first form of a fresh screen had DA Type = Dispatch Advice and Vendor UPL WH by default). Save with DA Type empty did nothing: no toast, no Document No, the form stayed as typed (two clicks, 3 s watcher; only an inline DevExtreme invalid-message overlay). Picking DA Type (options: Dispatch Advice, DA Against Purchase Order, Dispatch Advice Auto) then Save worked. So after Add the step must pick Warehouse, Vendor and DA Type; a silent Save is the symptom of a missing mandatory field. Row filter on the grid (SO Number "LEARN_SO") showed only 1353 after the silent Save, confirming nothing was saved.

### L12 Loss record timing
- DA **1356** (SO LEARN_SO_02): Save "Saved successfully"; line Product 62740537 CS 5 -> "Saved Successfully!" (stock type Sound, batch 1-1 fill after the product pick and RESET the quantity, so enter CS after the product/tab).
- Loss modal (a "+" in the Loss cell while the row is in edit mode): add row Stock = Damaged, Reason = Area Closed, CS 1, modal row Save (rowEditBtn_Modal_Save_0). Toast "Reason Type is required" appears while picking (right after choosing the stock type, before the reason is chosen) but the row saves fine. **Closing the modal with the x discards the loss** (line stayed 0-0-0 / Received 5 after line Save). The **Calculate** button (CalculateBtn) is what pushes the loss to the line: then line shows Loss 1-0-0, Received 4, net 61,691.72; line Save -> "Saved Successfully!".
- Grid ids: line Save/Edit links are anchors that need scroll-into-view before a click (otherwise "element not interactable").
- Forward (reopened from grid, comment "Auto"): toast "Forwarded successfully"; grid: Status **In-Active**, Approval Status **Pending for approval**.
- Maker opened sidebar **Loss Approval** (/ngui/dyl/layout?layoutCode=202026, breadcrumb Transaction > Loss Approval > Loss Approval Master): the screen IS visible to the Maker, master grid 364 rows, columns Serial No, Document Type, Document No, Distributor Code, Distributor Name, Status. Filter Document No = 1356 -> **0 rows: NO loss record exists after Forward**, before any checker action (filter verified with 1350 -> serial 637 Approved). Consistent with "the loss record is created on the checker's approval of the DA", not on Forward. Answers/affects the open question on when the loss record is created (not at Forward). Not yet checked: whether it appears after the DA approval (needs the Checker).
- Note: the Loss Approval row filter persists across screen reopen like the DA grid.

### L14 Order Booking validation (no Save)
- Screen /ngui/order-booking: Order Booker/Spot Seller (default Order Booker), PJP, Selling Category, Section, Outlet Name, Document Date, Comments, Reference Number. Cascade works: PJP AutoPromo1-Auto Promo PJP OB -> Selling Category AutoPromoSCG -> Section Auto Promo Section -> Outlet list of 15 (Aautomation_Outlet_21..36).
- **There is no "Validation" button on the header and no header message at all**: the **Order Detail** button (id orderDetail) appears only after Outlet is chosen. Clearing Section, Selling Category or PJP (clear icon) clears all fields below it and (with Outlet empty) there is no Order Detail button; no toast. So header fields "block" by progressive disclosure, not by messages.
- Order Detail (/ngui/order-booking/order-fillter): header locked, button **New Order** (id newOrder) -> dialog "Are You sure you want to cancel the order" with Yes (id continue; resets the header to empty, PJP/Selling Category/Section/Outlet blank) and No (id reject). Detail grid starts with an insert row (Product type-ahead id product, batch, CS/DZ/PC order, row Save/Cancel). 
- Selecting any product (62740537, 20050310; type-ahead lists only 62740537, 62740765, 20050308, 20050310 for this distributor) gives toast **"Stock not available."** and leaves the row empty (4 attempts). No Validation and no Order Save button appeared at any point, so **the Validation button could not be reached without stock; stopped there, nothing saved**. Open: which distributor/PJP has ATP stock for Order Booking (the stock received into Auto Main Warehouse via DA does not make these products orderable for PJP AutoPromo1 / outlet 28).

## Block 3a (2026-10-01)
Actor: Checker Auto_Tssm on cnr1dev1 (company Unilever Pakistan Limited, distributor 15108843). Only DA 1356 was approved; nothing else saved/approved. Raw data: runs/PILOT-DA-GIN/20260930-1615/exec/learning_block3a.json.

### C1 Approve DA 1356
- Opened from the Dispatch Advice grid (layout 201068; gridFilterCheckbox was unchecked, so toggled on; Document No filter 1356 gave exactly one row). Before: Status In-Active, Approval Status Pending for approval, Received Date empty, Net PKR 61691.72, form Document Status "Un-Authorized", SO LEARN_SO_02, Save disabled, Forward/Reject enabled.
- Approve = Forward with comment "Auto" (dx-button#forward, comments, Tab, #forwardPopUpSaveBtn). Toast (100 ms watcher): "Forwarded successfully". No alert appeared.
- After (grid): Status Active, Approval Status Approved, Received Date 2026-10-01, Net PKR 61691.72 (unchanged), Tax 0, Discount 0.
- Line detail after (Dispatch Detail tab): 1 line, 62740537, Sound, batch 1-1, Dispatch 5-0-0, Loss 1-0-0, Received 4-0-0, Net 61,691.72, Picked By auto_multi_orga. Received = dispatched 5 - loss 1 = 4: confirmed. The net amount was already computed on the received quantity before approval.
- Surprise: the Received Date is empty until approval and is set by approval; the Net Amount does not change.
- Answers/affects: L20 (approval outcome), L21 (received qty = dispatch - loss).

### C2 Loss record at approval
- Loss Approval (layout 202026) now has 365 rows (364 after DA 1350 on 2026-09-29). Filter Document No 1356 gives Serial **638**, Document Type "DA-01 -Dispatch Advice", Distributor 15108843 Auto KARACHI, Status **Pending for approval** (a record exists now; per the checklist it did not exist before approval of the DA). Loss Approval is created at the DA approval (consistent with TC-DA-03 note), the serial increments by 1 per DA with loss (637 -> 638).
- Master tab: Serial 638, Document No 1356, Document Type Dispatch Advice, Status Pending for approval. Detail tab: 62740537 - RAFHAN SLPC OILS CORN TIN PI7 2X10L, SKU Type 02 (Damaged), Dispatch CS 5, Received CS 4, Loss CS 1 (DZ/PC empty). Not approved.
- Surprise: the breadcrumb in the Loss Approval screen was stale (showed prior tab names); the grid is not sorted by serial (first row 372, then 1,2,3...).
- Answers/affects: L10 (when the loss record is created).

### C3 Goods Issue Note as Checker (screen /ngui/good-issue-notes/GIN, 14 GIN rows)
- GIN 505 (Pending for approval, In-Active): Header tab Forward, Reject, Terminate all ENABLED; Add enabled; Detail tab enabled. Cash Memo Selection tab: De-linking disabled (aria-disabled true; probably needs selected rows). Detail tab: Save All disabled. 
- GIN 29 (Draft): Header tab Forward, Reject, Terminate all DISABLED; Detail tab button disabled until opened; De-linking disabled; Save All disabled.
- No approval log/history control seen on any tab of either record. Buttons were read only, none clicked.
- Surprise: Forward/Reject/Terminate are enabled only for Pending for approval records for the Checker: Drafts cannot be forwarded by this user (Maker's action).

### C4 Screens of Auto_Tssm
- 'Stock Inquiry' does NOT exist for Auto_Tssm (search returns nothing); 'Stock Master Inquiry', 'Stock Adjustment SAN', 'Order Stock Allocation', 'Stock' exist. Loss Approval and Goods Issue Note exist.
- Top-level sidebar sections: Approval, Company setup, Configuration, Distributor Setup, Reports, Target, Transaction, Master Data, Integrator, Setup/Configuration, RCOA.
- Helper note: Q.open leaves the sidebar expanded and sometimes inside the last submenu (Distributor Setup); the hamburger toggles it, and it overlays grid controls (clicks on gridFilterCheckbox were intercepted).

### Session end
Logged out via user menu > li#logout; browser left open on the login page.

## Block 3b (2026-10-01)
Actor: Maker Auto_Multi_Orga (distributor 15108843) on cnr1dev1, after the Checker approved DA 1356. Strictly read-only; nothing saved. Raw data: runs/PILOT-DA-GIN/20260930-1615/exec/learning_block3b.json.

### S1 Stock Inquiry for 2026-10-01 (Period DAILY, Category All, Brand All)
- Show Inquiry: "Data grid with **1 rows** and 21 columns" (earlier today, before the approval: 0 rows / No data).
- The single row: 62740537 - RAFHAN SLPC OILS CORN TIN PI7 2X10L, Auto Main Warehouse, batch 1-1, **01 - Sound**: Opening 0/0/0, **In 4/0/0 CS/DZ/PC**, Out 0, Allocated 0, **Closing 4/0/0**. No 02 - Damaged row for 62740537. No other product has any row today (all other products, e.g. test wh 1 stock, are absent).
- Interpretation: the DA approval created today's stock row directly (not via Generate Opening Balances, which was not clicked): In = received qty 4 (dispatch 5 - loss 1), Opening 0. The loss 1 CS did not create a Damaged stock row (Loss Approval 638 is still Pending). Products without a movement today have no row, so Stock Inquiry for a new day only lists products with a movement unless opening balances are generated (the 09-30 list was 39 rows). Answers/affects: stock effect of DA approval, BA question 1 (when stock posts and in which stock type), Q on Opening Balance generation (the day-roll does not appear to be automatic).

### S2 Stock Inquiry for 2026-09-30 (re-read)
- 39 rows (3 pages: 15/15/9), unchanged. 62740537 Auto Main Warehouse 01 - Sound: Opening 80, In 80, Out 0, Allocated 63, Closing 97 (CS; DZ/PC 0): identical, no leakage from today's approval. Same product in "test wh 1": Opening 1000, Closing 1000. No 02 - Damaged row for 62740537 on 09-30; the only Damaged row on the date is 20080958 (SAN Warehouse A, 83 CS / 4 PC). Only one row on that date has any In/Out (the 62740537 one).
- Interpretation: approval posts only to the received date (2026-10-01), not to the document date of the previous day.

### S3 Order Booking product pick retest (nothing saved)
- Cascade deviations: PJP 02111-AutomationOB1 picked; Selling Category dropdown offered only "Selling Category 001" (no label with 201, picked it); Section Automation_Testing_Section; Outlet 1000000001 is NOT in the list for this PJP (list starts at 1000000004), so 1000000004-Aautomation_Outlet_04 was picked. Order Detail then opened (/ngui/order-booking/order-fillter).
- Product 62740537 (type-ahead real keys, list item "62740537-RAFHAN SLPC OILS CORN TIN PI7 2X10L"): **NO toast; "Stock not available." did NOT appear.** The row is populated: Batch 1-1, **Current Stock (ATP) 4 / 0 / 0 (CS/DZ/PC)**, Trade Price/Unit 7711.465, Order quantity inputs (quantity1_0 CS, quantity3_0 PC) = 0, Gross Amount 0, row Save/Cancel visible (not clicked). I cancelled the row with Cancel (rowEditBtn_Cancel_0).
- Product 20050310 (BLUEBAND MARGARINE A01 CP+GIFT 16X500G): toast **"Stock not available."** (dx-toast-error), row stays empty (product and batch blank). Unchanged vs the morning.
- Left via New Order -> Yes (id continue); nothing saved. An unsaved row cancel needed the grid add-row icon (.dx-icon-edit-button-addrow) to get a new insert row afterwards.
- Interpretation: the approval made 62740537 orderable and the ATP equals the Stock Inquiry closing for today (4 CS) in the Auto Main Warehouse; the product pick checks stock for the current day only (it said no stock before the approval). Product with no stock rows (20050310) still blocked. Answers the open question "which stock makes a product orderable": received DA stock, ATP = Closing today minus allocations. Affects BA question 1.

### S4 Maker view
- Dispatch Advice grid (layout 201068, filter Document No 1356, 1 row): Document Date 2026-10-01, Distributor 15108843 - Auto KARACHI, SO LEARN_SO_02, Received Date **2026-10-01**, Tax 0, Discount 0, Net PKR 61691.72, Status **Active**, Approval Status **Approved**.
- Loss Approval (layout 202026, filter Document No 1356): Serial **638**, DA-01 - Dispatch Advice, Distributor 15108843 Auto KARACHI, Status **Pending for approval** (Maker sees it; grid total 365 rows).
- Interpretation: Loss approval pending does not block the stock posting of the received (net of loss) quantity.

## Cycle step 1 (2026-10-01)
Maker Auto_Multi_Orga (cnr1dev1, distributor 15108843) created, lined and forwarded one Dispatch Advice following the TC01 attempt 2 sequence.
- Document: DA_CYCLE = **1357** (warehouse C0000000055-Auto Main Warehouse, vendor UPL WH, SO Number CYCLE_1001; DA Type not required). Toast "Saved successfully".
- Lines (each "Saved Successfully!"): 62740537 CS 80 (PKR 1,233,834.4); 20050310 CS 70 (37,840.88); 62690363 CS 60 (189,160.63); 20050308 CS 50 (190,290.5). No losses.
- Header Info tab reset the form as before; DA reopened from the grid (document filter, first row exactly 1357); Forward comment "Auto" gave "Forwarded successfully".
- Grid after: Status In-Active, Approval Status Pending for approval, net amount PKR 1651126.412.
- Surprises: (1) typing the quantity right after picking the product (before the row had finished loading) left quantity empty, and the row save answered "The lost quantity does not equal the sum of dispatch and received quantities" (nothing saved); wait for stock type/batch to fill, then type the quantity. (2) A new row is always index 0 (rowEditBtn_Save_0) even with earlier lines present. (3) The product option list sometimes detaches; re-type the product to get it back. (4) Document numbers 1353-1356 were already used, so the new DA is 1357.
- Browser left open, logged in as Auto_Multi_Orga.

## Cycle step 2 (2026-10-01)
Checker Auto_Tssm (Unilever Pakistan Limited, distributor 15108843), cnr1dev1. Helper injected with comments stripped of backticks (code unchanged) because String.raw cannot hold backticks.
- **DA 1357** (Auto KARACHI, Auto Main Warehouse, SO CYCLE_1001, PKR 1,651,126.412): before In-Active / Pending for approval; Forward with comment "Auto" -> toast **"Forwarded successfully"**; grid after: **Active / Approved, Received Date 2026-10-01**. The approval works the same way as on 09-29.
- **GIN 505** (GIN Date 2026-09-30, Delivery Date 2026-09-30, Auto Main Warehouse, DSR 02112-AutomationDSR, vehicle 0040-Automation211206, In-Active / Pending for approval; 9 cash memos dated 2026-09-29). Detail (Current Stock now; Suggest CS-DZ-PC): 20050308 50 / 18-0-16; 20050310 70 / 40-0-0; 62690363 60 / 24-0-16; 62740537 84 / 63-0-0; 69997598 0 / 0-0-48. Actual 0 on all lines.
- One approval attempt (comment "Automation Approval") -> toast **"cashmemo(s) found with delivery date earlier than the pjp working date, order no: [COL26000001998, COL26000001999, COL26000002000, COL26000002001, COL26000002002, COL26000001988, COL26000001995, COL26000001996, COL26000001997]"**. GIN stays In-Active / Pending for approval. No retry.
- Surprise: the "No stock balance found for products" error is gone (stock balances now exist for 2026-10-01 or the check no longer fires first); a different validation now blocks: the GIN's Delivery Date (2026-09-30) and its cash memos (dated 2026-09-29) are earlier than the PJP working date (today). A GIN made on one day cannot be approved on a later day; the whole cycle (orders, cash memos, GIN, approval) must run on the same calendar day, and the cash memo dates must not be earlier than the PJP working date.
- UI traps: the GIN Detail tab (tab_3) is disabled for a few seconds after opening a GIN; switching back to the Header tab blanks the header (ginNum empty), so Forward must be done on a freshly reopened GIN without tab switching; the Forward button is not present on the Detail tab.

## Learning session G11-PK 1 (2026-10-01 16:11-18:33): seq 1-50 walked on one calendar day
Full per-flow evidence: [learning_sessions/2026-10-01_G11-PK_session1_log.md](learning_sessions/2026-10-01_G11-PK_session1_log.md); summary, defects, drift and resume plan: [learning_sessions/2026-10-01_G11-PK_session1_report.md](learning_sessions/2026-10-01_G11-PK_session1_report.md). Maker Auto_Multi_Orga, Checker Auto_Tssm, distributor 15108843.
Chain: DA 1358 -> loss 639 -> orders COL26000002003-2008 -> delivery date change -> GIN 506 (**first successful GIN approval**: same-day stock + delivery date = today) -> edit/cancel/reschedule after GIN -> delivered 2003-2005 -> sales return COL26000000713 -> deposit slips 1131-1136 -> GRN 246 (19 CS back = 7 cancelled + 7 rescheduled + 3 cut + 2 returned) -> **blocked at Route Settlement ("Following previous days not closed! Please close date. 2026-09-30")**.
Headline rules (observed): DA approval adds received qty; loss approval has no stock effect (closes L21); order save reserves stock, cancel releases it; GIN approval = one Checker Forward, Allocated -> Out; after the GIN nothing moves stock until the GRN, which posts In; Tax Exemption Y -> tax 0; tax = VAT + 3rd Schedule; discount = several promotions (basket-dependent); Order Editing dates = delivery dates (explains the empty outlet list of 09-29); deposit slips stay Un Posted until settlement; approved sales return not netted from the receivable.

## Learning sessions G11-PK 2 and 2b (2026-10-05): seq 1-50 again (morning), seq 51-71 (afternoon)
Full per-flow evidence: [learning_sessions/2026-10-05_G11-PK_session2_log.md](learning_sessions/2026-10-05_G11-PK_session2_log.md), [learning_sessions/2026-10-05_G11-PK_session2_report.md](learning_sessions/2026-10-05_G11-PK_session2_report.md), [learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md](learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md); coverage: [learning_sessions/2026-10-05_G11-PK_coverage_report.md](learning_sessions/2026-10-05_G11-PK_coverage_report.md); drift: [FRAMEWORK_DRIFT.md](FRAMEWORK_DRIFT.md).
Chain: DA 1359 -> loss 640 -> orders COL26000002009-2014 -> delivery date change -> GIN 507 -> edit 2009 / cancel 2013 after GIN, reschedule 2012 -> delivered 2009-2011 -> return COL26000000714 -> slips 1137-1142 -> GRN 247 (19 CS) -> [QA team member closes earlier days, settles 02112 for 10-01 and 10-05] -> slips Posted -> day close 10-05 -> SAN 96 (-50 CS) -> closing snapshot and Transaction Inquiry checks.
Headline rules (observed 2026-10-05): every session-1 amount and message reproduced; a new day opens at its first movement with Opening = previous Closing + still-Allocated (previous closings ARE carried; supersedes the 10-01 note); posting happens at Route Settlement (remainder trimmed, slip locked, cheques Clear, Offset filled); the day close is PJP Daily Inquiry Update End Of Day + Complete (Current Status E); SAN approval = Out; settlement/posting/day close move no stock; Order Editing lists only orders whose delivery date is today; a part return re-prices slab promotions on the other lines and is still not netted after settlement.

## Learning session G11-PK 3 (2026-10-06): full seq 1-71 in one calendar day WITH the QA Team Lead
Full per-flow evidence: [learning_sessions/2026-10-06_G11-PK_session3_log.md](learning_sessions/2026-10-06_G11-PK_session3_log.md); report: [learning_sessions/2026-10-06_G11-PK_session3_report.md](learning_sessions/2026-10-06_G11-PK_session3_report.md). Maker Auto_Multi_Orga, Checker Auto_Tssm, env cnr1dev1, distributor 15108843.
Chain: DA 1360 -> loss 641 -> orders COL26000002015-2020 -> Delivery Date Change (before seq 15) -> unallocate -> **first before-GIN edit (2015 7 -> 4 CS)** -> cancel 2017 -> unallocate/allocate -> GIN 508 -> edit 2015 to 3 CS, cancel 2019, reschedule 2018 to 10-07 -> delivered 2015, 2016, 2020 -> return COL26000000715 -> slips 1143-1148 -> GRN 248 (17 CS) -> settlement blocked by the 10-05 Reattempt 2012 -> allocate 2012, GIN 509, approve, deliver (unpaid) -> **route 02112 settled by Claude** -> cheque check -> DSR adjustment 400 (COL26000000211) -> day close (E) -> SAN 97 (-50 CS) -> stock and Transaction Inquiry checks.
Headline findings (observed 2026-10-06 unless tagged):
- **Route Settlement procedure**: Edit -> cash Received editable (prefilled), cheque Received read-only, Stock Shortage editable -> row Save -> "Saved Successfully" -> row green, Edit gone. Header 212,963 / 212,963 / 0.
- **New settlement blocker**: "Un-Deliver Order exists for today delivery!" (Show details: COL26000002012, the 10-05 Reattempt order due today). Allocation alone did not clear it; resolution [stated 2026-10-06 QA Team Lead]: allocate (Order Date = booking date), new GIN, Checker approval, Cashmemo Status Delivered; may stay unpaid (not a cash shortage).
- **Reschedule unallocates** the order (2018 on the Unallocated tab); **Order Editing save re-allocates** the edited order.
- **Order Editing rule** [stated 2026-10-06 QA Team Lead; observed]: only UNALLOCATED orders whose delivery date is today are listed; after GIN approval no unallocation is needed.
- **DSR Adjustment** 400 / AUTO: confirm modal, "Record Saved Successfully", COL26000000211; Total Shortage +400, Balance +400, Total Adjusted unchanged; meaning [stated 2026-10-06 QA Team Lead]: a DSR shortage while taking money from the outlet.
- **Seq 55 Cheque Status** is a check only (cheques Clear; no Bounce) [stated 2026-10-06 QA Team Lead].
- **Duplicate cheque numbers** (1234567 on 1146 and 1147) are allowed: no cheque inventory is kept [stated 2026-10-06 QA Team Lead].
- **Opening balances**: the DA approval created only the 5 received rows with Opening 0 (as on 10-01, unlike 10-05); Q-OB2.
- **Tax**: outlets 06 and 07 swapped tax behaviour vs 10-05 (2017 outlet 07 Tax 0, 2019 outlet 06 Tax 16,505.36); Q-TX1.
- Stock mechanics confirmed a third day: GIN approval Allocated -> Out; GRN approval In +; SAN approval Out +. 62740537 end of day: Opening 0 / In 97 / Out 89 / Allocated 0 / Closing 8.

### D-G11-3-1 DEFECT (display): doubled totals on the Deposit Slip "Outstanding Outlet" tab
- Observed 2026-10-06 (seq 42): outlet 1000000005 Net / Balance / Un Posted **202,322** although its only open memo (COL26000002016) is 101,161; outlet 1000000004 Net **257,570** vs its open memos 2015 76,156 + 2009 90,707 = 166,863 (difference 90,707 = 2009 counted twice); outlets 07 and 11 correct.
- Ruling [stated 2026-10-06 QA Team Lead]: a **display defect** (Q-DS4 answered). Do not assert outlet-level totals; use the Outstanding Cash memos tab or Transaction Inquiry for amounts. The multi-cheque allocation itself saved correctly ("Payment Adjusted Successfully", outlet Deposit Amount 1,000).

### E-G11-3-1 ENVIRONMENT ISSUE: stock carry-over job did not run on cnr1dev1 (2026-10-05 -> 2026-10-06)
- Observed: 62740537 at Auto Main Warehouse closed **259 CS** on 2026-10-05 (seq 60, after SAN 96) but the first movement of 2026-10-06 (DA 1360 approval) created only the 5 received rows with **Opening 0** (seq 9); the 63 CS old allocation of GIN 505 was not shown either. Same pattern on the 2026-10-01 morning.
- Ruling [stated 2026-10-06 QA Team Lead] (Q-OB2 answered): Opening must carry over the previous day's Closing; Opening 0 while the previous day had closing stock is a **stock carry-over JOB issue in the environment**, not business behaviour. Conclusion [inferred]: the carry-over job most likely did not run on cnr1dev1 for 2026-10-06. Action: report to the environment owner; before each cycle compare today's Opening with yesterday's Closing.

### QA Team Lead rulings added after the run (2026-10-06)
- Q-TI1: Transaction Inquiry Detail Ordered = original order quantity; Allocated = allocated from available stock (lower when stock is short); 5 CS 4 PC / 4 / 3 delivered is expected.
- Q-TX1: outlet 06/07 tax swap came from master-data modification of the outlets and the tax promotion (not a defect). Rule: a zero-tax invoice of a non-exempt outlet cannot be delivered; tax-exempt outlets' zero-tax invoices are allowed (not exercised: 2017 was cancelled).

## QA team written answers to the 2026-10-06 review (received 2026-10-08)
Source: learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx). No new walk; this block records the findings the answers create. Tag [stated 2026-10-08 QA Team].

### D-G11-2b-1 DEFECT: route 02112 for 2026-10-01 is Complete but its deposit slips were never posted
- Observed 2026-10-05 (G11-2b): Route Settlement, Route Status Complete, shows 02112 for 2026-10-01 as Complete (values as G11-1: Sale Value 311,238, Payable = Received 224,131, Cash Shortage 0); the Deposit Slip grid still shows that day's slips **1131-1136 Un Posted** (1133 still Deposit 1,000 / Adjusted 600). The 09-29 slips (1125-1130) are Posted.
- Observed 2026-10-06 (G11-3): after the 10-06 settlement the Outstanding Cash memos tab still shows COL26000002004 / COL26000002005 with Un Posted 101,161 / 119,370 (their 10-01 slips 1131 / 1132): the 10-01 receivables were never adjusted.
- Contrast: the settlements of 2026-10-05 and 2026-10-06 posted all their slips (1137-1142, 1143-1148) [observed].
- Ruling [stated 2026-10-08 QA Team] (Q-DS3): "This should not be possible. Once the route is settled, all associated deposit slips must be posted, and their amounts must be adjusted against the respective invoices/cash memos. If this does not happen, it should be considered a defect."
- Unknown: how the 10-01 route was completed (done by a QA team member on 10-05, action not seen). Action: report to the QA team / development with this evidence; ask whether the 10-01 route was completed through a path other than the row Save. Regression check: after every settlement assert that every slip of the route/date is Posted.

### Q-OE5 CONTRADICTION: edit after GIN approval vs stock (stated GIN reduction, observed none)
- Stated [stated 2026-10-08 QA Team] (rule 3, Q-OE3): with ORGA parameter CASHMEMO_EDIT (CM_Edit) = Y an approved cash memo may be edited (quantity reduction, reason required) and on Save the system reduces the corresponding quantity in the approved GIN.
- Observed on three walks: COL26000002003 (10-01, 7 -> 4 CS), COL26000002009 (10-05, 7 -> 4 CS), COL26000002015 (10-06, 4 -> 3 CS) edited after GIN approval: Stock Inquiry Out / Allocated / Closing unchanged and the cut quantity came back on the GRN Suggested quantity (19 / 19 / 17 CS).
- Open (Q-OE5, class B): read CASHMEMO_EDIT on cnr1dev1 and re-observe the GIN detail and stock after an after-GIN edit (LIVE_LEARNING_CHECKLIST L42).

### Q-DS4 UNDER CLARIFICATION: Outstanding Outlet doubled totals (D-G11-3-1)
- The QA team answered N to "doubled totals = display defect" but the comment talks about Transaction Inquiry (offset fully adjusted, net not impacted, current logic correct) [stated 2026-10-08 QA Team]. Follow-up sent 2026-10-08. D-G11-3-1 and the rule "never assert outlet-level totals" stay until clarified.

### New stated messages and rules (not yet observed)
- "Stock Mismatch" at Route Settlement when today's GIN quantity does not match the GRN quantity [stated 2026-10-08 QA Team].
- Route Settlement: Edit link = not settled, blank = settled; ignore colours [stated 2026-10-08 QA Team].
- ZERO_TAX_ORDER_EXEMPTION (Y: zero-tax invoices deliverable, N: not) [stated 2026-10-08 QA Team]; CASHMEMO_EDIT (see above).
- Previous-day check: PJP working date = current date and closing date = N-1 [stated 2026-10-08 QA Team].
