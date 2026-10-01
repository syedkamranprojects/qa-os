# Dispatch Advice (DA) end-to-end flow, as defined in selenium-framework-db (read-only, 2026-09-29)

Purpose: Claude replays the framework's own configuration through the browser MCP (framework tables = the script), so we learn the real business flow and find where the framework config has drifted from the live app.

## Where the chain lives
- Test-flow rows (`fct_pr_tf_test_flow`) are single steps (1 menu group each). The **end-to-end chain is a group**: `fct_pr_gtf_group_test_flow` + `fct_pr_gtfd_group_test_flow_detail` (flow order, login user `plu_serial_no`, `pgtf_testflow_login_status`, active flag).
- Groups containing DA: **11 "Daily Cycle Only Positive Flow" (Pakistan, 61 rows, ~41 active)**, 1 "Daily Cycle Negative with Positive Flow" (45), 52 (ITHD), 61 (Bangladesh, 51), 67 (Astron), 14 "For GIN Testing" (12), 12 "Order Booking Promotion Testing" (5).
- Login users (`fct_pr_lu_login_users`, **never read the password column**): app **8 "PK_Centegy QA 2" = https://dcodecnr1dev1.unilever.com/ngui** (our Pakistan env): serial 8 `Auto_Tssm` (approver), 26 `kpo_mp`, 28 `Automation`, 30 `headquarter`, 35 `Auto_Multi_Orga`. `login_status = Y` on a chain row = log in again as that row's user before the flow; blank = continue in the same session.

## Group 11 chain (active rows, in order)
1 Login Dcode (mg 7777: screens 777701 login, 777702 distributor selection) -> **2 Dispatch Advice (mg 0010)** -> 5 DA Approval (mg 0074, user 8) -> 7 DA Loss Approval (0076) -> 9 Stock Validation After DA PAK (0280, user 35) -> 10 Order Booking (0001) -> 12 Stock Allocation (0013) -> 14 Transaction Inquiry validate after OB (0296) -> 15 Order Editing (0002) -> 16 Order Cancellation (0004) -> 18 Stock Unallocation (001301) -> 19 Delivery Date Change (0016) -> 20 Goods Issue Note (0005) -> 23 GIN Approval (0078, user 8) -> 24 Stock validation after GIN (0281) -> 29 Order Editing After GIN (0084) -> 31 Order Cancellation After GIN (0085) -> 32 Cashmemo Reschedule (0104) -> 33 Cashmemo Status (0003) -> 34 Sales Return (0007) -> 36 Sales Return View (0070) -> 37 SR View Approval (0073, user 8) -> 38 SR Status Change (0071) -> 39-41 Deposit Slip flows (0323, 0324, 0326) -> 42/44/46 Deposit slip multi-cheque/cheque/cash (0014, 001404, 001405) -> 48 Goods Return Note (0009) -> 49 GRN Approval (0081, user 8) -> 50 Stock validation after GRN (0282) -> 51 Route Settlement (0068) -> 52-54 offset/deposit after RS (0321, 0322, 0325) -> 55 Cheque Status (0066) -> 56 DSR Adjustment Amount (0067) -> 57 PJP Daily Inquiry Update (0093) -> 58 OTC Stock Out R1 (0295) -> 59 SAN Approval PAK (0350, user 8) -> 60 Opening & Closing Stock Validation (0283) -> 68-71 Transaction Inquiry validations (0319, 0320, 0374, 0377).
Inactive (`N`) rows: DA Negative, DA Rejection, Loss Approval Request, GIN terminate/reject approvals, SAN Admin / W-to-W.

## DA flow 00100001 (menu group 0010)
- Navigation: menu option **`DYL_201068`** (Transaction > Primary Sale > Dispatch Advice, route `/dyl/layout?layoutCode=201068`), search text "Dispatch Advice". KPO_mp's live menu contains it.
- Screens (mgsm, in order): 001001 header (tab_1) -> 001004 grid search (tab_1) -> 001006 Detail2 (tab_2) -> 001002 Detail (tab_2) -> 001003 Loss (anchor) -> 001010 "DA Amount Val R1 PAK" (tab_2) -> 001007 detail row save (tab_2) -> 001004 -> 001005 Grid/Forward (tab_1).
- **Header fields (001001)**: Warehouse `DDL__epp1_busent_code_phs_lvl1_b` (dropdown, mandatory), Vendor Code `DDL__PVNDVENDCODE` (dropdown, mandatory), SO Number `TXT__tstm_sales_order_no`, Shipment No `TXT__tstm_shipment_no`, Deliver No `TXT__tstm_delivery_no`, Invoice Due Date `DT__tstm_invoice_due_date`, Tax Invoice Number `TXT__tstm_taxinvoice_no`, Comments `TXT__TSTMCOMMENTS`, Reference Date `DDT__origin_date`, Reference No `TXT__tstm_ref_1`, Truck No `TXT__pvch_vehicle_regno`, VAT Challan Number `TXT__tstm_vat_challan_no_1`, Invoice Number `TXT__tstm_invoice_no`, `documentNo` (type 0010 readable, repo `REPO_DOCUMENTNO`); DA Type `documentType` is inactive. Case-data sheet also has "Recieved Date" (no matching field row).
- **Detail (001002 / 001006)**: Product `prodCode_0` (0006 autoselect), Stock Type `stockType_0`, Batch `batch_0`, CS `quantity1_0` (PC/CS2 inactive); grid add button `cashMemoSelectionGrid`, row save `rowEditBtn_Save_0`, cancel `rowEditBtn_Cancel_0`.
- **Loss (001003)**: Stock `pstt_stock_type_0`, Loss Reason `reasontype_0`, CS `loss_qty1_0`; buttons `addbtn`, `rowEditBtn_Modal_Save_0`, `rowEditBtn_Modal_Cancel_0`, `CalculateBtn`.
- **Amount validation (001010)**: read-only rows `row_6_*` (purchase price/PC, gross, discount, tax, net): event 0007 "Screen Excel DB Screen Validation".
- **Events**: header save button `saveBtn` (0004/0002) then assertions 0013 `ELEVLD` and `TSTMSG`; then event 0012 **Fill Repos** stores the new document number in `REPO_DOCUMENTNO`; grid screen 001004 searches that number in `rowfilter_documentNo` (fixed value type REPO), waits 3 s, clicks `row_1_document_no`; 001005 clicks `forwardBtn`, types comment "Auto" (from Excel) into `comments`, `forwardPopUpSaveBtn`, group assertion 0014 `TSTMSG,DA_FORWARD_ASSR`.
- **Case data** (Pakistan copy `NG_Dcode_QA_OTC (Pak).xlsx`, sheets `Dispatch Advice`, `Dispatch Advice Detail2`, `Dispatch Advice Loss`, `Dispatch Advice Grid`, `*_ASSR`): warehouse "Auto Main warehouse", vendor "UPL WH", SO number "Automation_<date>", dates, comments "Positive_QA_Automation_01"; detail products 62740537 (80 CS), 20050310 (70), 62690363 (60), 20050308 (50), stock type Sound, batch 1-1; loss rows Damaged/Lost with reasons. Expected messages come from the `_ASSR` sheets (`EXPECTED_MESSAGE`); the toast and screen-query tables hold nothing for DA.
- **Approval (mg 0074, screen 007401, user 8)**: same option `DYL_201068`; **Loss approval (0076/007601)**: option `DYL_202026`.

## Component / event codes used
Types: 0001 text, 0002 dropdown, 0003 date, 0004 button, 0006 autoselect, 0007 dropdown-grid, 0010 readable element. Custom events (type 0000): 0001 load data, 0004 toast, 0006 wait, 0007 screen/DB validation, 0012 fill repos, 0013 assertion, 0014 group assertion, 0017 search-and-row-click, 0021 file upload.

## Cross-flow state
Documents chain through **repos** (`REPO_DOCUMENTNO`, filled by event 0012 after a save, consumed by later screens' search fields). Stock validations (flows 0280, 0281, 0282, 0283) compare stock after each document; approvals need a second login user (8).

## Risks for replaying this through the MCP
- Login: I never type passwords; the QA user logs in as each user the chain needs (default user for creation, `Auto_Tssm` for approvals, `Auto_Multi_Orga` for stock validation).
- Every step changes real dev data (stock in, orders, GIN, returns, deposits, route settlement): the environment is cnr1dev1 (non_production) but the data is shared; run slice by slice and record document numbers.
- The framework config may have drifted from the live app (ids like `saveBtn` vs `save`, DYL layout screens changed): each mismatch is a finding for the framework owner.
- Warehouse "Auto Main warehouse", vendor "UPL WH" and the product codes must exist on cnr1dev1; not verified yet.

## Replay log (live, cnr1dev1 as KPO_mp, 2026-09-29)
- Login: done by the QA lead. Helper installed; `Q.open('Dispatch Advice')` reaches `/dyl/layout?layoutCode=201068` (framework nav `DYL_201068`: OK). Breadcrumb Home > Transaction > Primary Sale > Dispatch Advice; tabs Header Info / Dispatch Detail; grid 591 rows (distributor 50250327 MULLER & PHIPPS (KORANGI - KARACHI)).
- **Header field ids: 15 of 15 framework ids exist and are visible** (DDL__epp1_busent_code_phs_lvl1_b, DDL__PVNDVENDCODE, TXT__tstm_sales_order_no, ..._shipment_no, ..._delivery_no, DT__tstm_invoice_due_date, ..._taxinvoice_no, TXT__TSTMCOMMENTS, DDT__origin_date, TXT__tstm_ref_1, documentType, TXT__pvch_vehicle_regno, ..._vat_challan_no_1, ..._invoice_no, documentNo). `saveBtn` and `forwardBtn` (cent-button) exist; the live page also has buttons Add, Save, Update, Delete, Forward, Reject (ids add/save/update/delete/forward/reject). No header drift found. Extra live field labels not in the framework: Document Date, Tax, Discount, Net Amount, Document Status, Stock Arrival, Status, Approval Status.
- **Data drift**: workbook warehouse "Auto Main warehouse" is NOT offered to KPO_mp. Warehouses: C0000000001 M&P Main Warehouse (default), C0000000111 Ali Warehouse, C0000000126 smoke123, C0000000136 Hanzo, C0000000137 ZAIN Warehouse Sound, C0000000214 nf. Vendor "UPL WH" exists (also RYK, SITE Vender, TATA). DA Type options: Dispatch Advice, DA Against Purchase Order, Dispatch Advice Auto. The "Automation" login user (framework serial 28) probably owns the "Auto" distributor/warehouse; not verified.
- **Dispatch Detail tab is empty until a header is saved** (no add button, no row ids): detail ids (prodCode_0, stockType_0, batch_0, quantity1_0, cashMemoSelectionGrid, rowEditBtn_Save_0) and the loss tab could not be checked without creating a DA.
- Nothing has been saved yet.

## Replay log, part 2: DA created and forwarded (cnr1dev1 as KPO_mp, 2026-09-29)
User decision: the framework's `Automation` login failed (invalid), so the flow ran with **KPO_mp** and warehouse **M&P Main Warehouse** (workbook's "Auto Main warehouse" absent); quantities 2 CS instead of 50-80.
| Framework step | Result on the live app |
|---|---|
| Header fields filled (SO Number Automation_29-09-2026, Shipment 123, Deliver 12312, Tax Invoice 123, Comments Positive_QA_Automation_01, Reference No 1115; dates default to today) | OK, all ids matched |
| `saveBtn` | toast **"Saved successfully"**; **Document No 570**; Document Status Un-Authorized; grid 591 -> 592 rows. Repo `REPO_DOCUMENTNO` = 570 |
| Dispatch Detail tab: `cashMemoSelectionGrid` (+), `prodCode_0` (type-ahead: type the code, click the suggestion; stock type Sound and batch 1-1 fill by themselves), `quantity1_0`, `rowEditBtn_Save_0` | 4 lines saved, each toast **"Saved Successfully!"**: 62740537 RAFHAN SLPC OILS CORN TIN (PKR 7,452.36/pc), 20050310 BLUEBAND MARGARINE A01 (33.79), 62690363 SURF EXCEL P03 (15.45), 20050308 BLUE BAND MARGARINE 32X250G (118.93); 2 CS each; app calculates gross/net amounts (net total PKR 44,266.9984 after loss) |
| Loss (screen 001003): loss link id `Anchor` ("+" in the Loss column), modal "DA Loss Details", `addbtn`, `pstt_stock_type_0` (Damaged/Expired/SEP/Lost/Behalf 615/Variance), `reasontype_0` (Area Closed/Order Change/Customer cancels delivery/On Customer Behalf), `loss_qty1_0`, `rowEditBtn_Modal_Save_0`, `CalculateBtn` | line 2 loss Damaged / Area Closed / 1 CS: **no toast** on the modal save (framework expects TSTMSG); Calculate closes the modal and the line shows Loss 1-0-0, Received 1 CS, gross 540.58; line save `rowEditBtn_Save_1` gave "Saved Successfully!" |
| Grid search: `gridFilterCheckbox` (dx-check-box, toggles), `rowfilter_documentNo`, `row_1_document_no` | OK (filter "570" also matches other numbers containing 570: check row 1) |
| Forward: framework clicks `forwardBtn` (cent-button wrapper) | **a script click on the wrapper does nothing; click the inner `forward` dx-button** (a real mouse click at the button centre also works); popup has `comments` (textarea) and `forwardPopUpSaveBtn`; type "Auto" and **blur (Tab)** before Save, otherwise the toast is **"Please add comments"**; then toast **"Forwarded successfully"**; grid status: Status In-Active, Approval Status **Pending for approval** |

### Framework drift / engine notes found
1. `rowEditBtn_Save_0` / `rowEditBtn_Cancel_0` assume the edited row is index 0; the loss save on row 2 uses `_1`.
2. Loss modal save shows no toast; the framework's TSTMSG assertion there (event 5) would fail.
3. Forward needs a blur before Save (DevExtreme commit on change): the engine's typing may already blur, unverified.
4. `gridFilterCheckbox` is a toggle: clicking it when already on hides the filter row.
5. The "Auto Main warehouse" data (workbook) is not available to KPO_mp; the `Automation` credentials in the framework did not work (invalid user or password).
6. Header form retains stale values (Approval Status Draft) after Forward until the screen is reloaded.

## Replay log, part 3: DA approval (cnr1dev1, 2026-09-29)
- Framework approval flow 00740001 (screen 007401, user 8 Auto_Tssm): filter by REPO_DOCUMENTNO + SO number "Automation", open row, click `forwardBtn`, comment "Auto", `forwardPopUpSaveBtn`, group assertion `TSTMSG,DA_APPROVALFRWD_ASSR`. On the live app the approval is the **same Forward action** (Reject is the alternative), done from the same DA screen.
- **KPO_mp itself forwarded DA 570 a second time: toast "Forwarded successfully"; grid shows Status Active, Approval Status Approved, Received Date 2026-09-29.** So the app does not enforce a different approver here (no maker-checker) for this document.
- The QA lead asked for the approval to be done with a different login user (the framework does it as user 8); the window was logged out at this point so the loss approval can be done by that user. Not yet done: Loss Approval (flow 00760001, screen 007601, option DYL_202026, 108 rows in the master grid, filter ids `rowfilter_TXT__tstmdocno` etc.; framework clicks `Header_0_serial_no`, `row_1_document_no`, tabs `tab_2`/`tab_1`, `forwardBtn`, comment, save, assertion `DA_LOSS_APPROVALFRWD_ASSR`).
- User menu (top right) shows organization "010104-Unilever Pakistan Limited" and distributor "50250327-MULLER & PHIPPS (KORANGI - KARACHI)"; Logout is the item inside that menu (click the user name, then Logout).

## Maker / checker switch protocol (rule from the QA lead, 2026-09-29)
Whenever the framework chain needs a different login user (`login_status = Y` on a chain row), or the app requires a second person, the run gets an explicit **checker step** with a **SWITCH point**:
1. I finish the maker's part, record document numbers and statuses, and state the plan: "SWITCH: log out; the checker is <user> (framework serial <n>)".
2. I log the window out (I click the profile menu, then Logout). I never type credentials.
3. The QA lead logs in as the named user in the same window and says so.
4. I **verify the user name shown top-right** equals the expected user, reinstall the page helper (a new login clears it), and only then do the checker step: open the document (filter by the stored document number), act (Forward / Approve / Reject), read the toast and the new status.
5. If the checker cannot act (for example "Current user is not authorized to save this record!"), I stop, record it, and ask; I do not retry with a different account on my own.
6. When a step could be done by the maker (the app did not block it), I still schedule it with the checker to keep the maker-checker separation. DA 570 (KPO_mp) was forwarded and approved by the same user: recorded as a deviation.

### Users in this chain (cnr1dev1, framework app 8; names only)
| Role | Framework user | Serial | Notes |
|---|---|---|---|
| Maker (creates DA, orders, GIN ...) | not named in the tables (runner default login); candidates `Automation` (28), `Auto_Multi_Orga` (35); `AppUser` (4) is inactive | ? | `Automation` login was rejected (invalid) on 2026-09-29 |
| Checker / approver | `Auto_Tssm` | 8 | **cannot create a DA**: "Current user is not authorized to save this record!" (verified live, distributor 15108843 Auto KARACHI) |
| Stock validation | `Auto_Multi_Orga` | 35 | |
Distributor selected by the framework's login flow: **15108843 (Auto KARACHI)**, company Unilever Pakistan Limited (case-data sheet `Distributor selection`). Warehouse `C0000000055-Auto Main Warehouse`; Auto_Tssm's DA grid holds 1,303 earlier automation DAs (SO numbers "Automation_<date>").

### Planned DA slice with switch points
| # | Step | Who | Switch before? |
|---|---|---|---|
| 1 | Create DA header (workbook data, Auto Main Warehouse, vendor UPL WH), save | maker | yes: maker login |
| 2 | Add 4 detail lines (62740537 80 CS, 20050310 70, 62690363 60, 20050308 50), stock Sound, batch 1-1 | maker | |
| 3 | Loss rows (line 2: Damaged/Area Closed 4, Lost/On Customer Behalf 2; line 3: Damaged/On Customer Behalf 5), Calculate, save lines | maker | |
| 4 | Forward with comment "Auto" | maker | |
| 5 | **SWITCH -> checker Auto_Tssm**: DA approval (Forward with comment "Auto"; assertion DA_APPROVALFRWD_ASSR) | checker | yes |
| 6 | Loss approval (screen 007601): find the record, tabs, Forward | checker (framework: same session) | no |
| 7 | Stock validation after DA (flow 0280) | Auto_Multi_Orga | yes |

## Replay log, part 4: DA 1350 as designed (maker Auto_Multi_Orga, 2026-09-29)
- Login: after the company step, the app shows a **Distributor** dropdown (multi-organization page). `Auto_Multi_Orga`: Company "Unilever Pakistan Limited" -> Proceed -> Distributor list: 125555555-Aqua Distlocation, **15108843-IBRAHIM TRADERS** (chosen, the framework's distributor), 15178537-GNY ENTERPRISES, 18011494-Muhammad Akram Traders, 50250327-MULLER & PHIPPS (KORANGI - KARACHI), 956783323-Global user location -> Proceed -> home.
- **Auto_Multi_Orga can create a DA** (maker confirmed). Warehouse list includes `C0000000055-Auto Main Warehouse` (the workbook's warehouse); default was 0000000025-IBT Main warehouse.
- DA header (workbook values) saved: **Document No 1350**, "Saved successfully", grid 1303 -> 1304.
- Lines (workbook quantities): 62740537 RAFHAN SLPC OILS CORN TIN 80 CS @ PKR 7,711.47 (line 1,233,834.4), 20050310 BLUEBAND MARGARINE A01 70 CS @ 33.79 (37,840.88), 62690363 SURF EXCEL HS STD PWD CARE P03 60 CS @ 15.45 (189,160.63), 20050308 BLUE BAND MARGARINE 32X250G 50 CS @ 118.93 (190,290.5); each toast "Saved Successfully!".
- Loss (workbook): line 2 = Damaged/Area Closed 4 CS + Lost/On Customer Behalf 2 CS (Loss 6-0-0, Received 64, net 34,597.38); line 3 = Damaged/On Customer Behalf 5 CS (Loss 5-0-0, Received 55, net 173,397.25). In the loss modal the second row uses the same ids (`_0`) after the first is saved. Line save ids: `rowEditBtn_Save_1` (line 2), `_2` (line 3).
- Grid after: Status In-Active, Approval Status Draft, net PKR 1,632,119.522. Forward (comment "Auto"): **"Forwarded successfully"**.
- Gotcha: `gridFilterCheckbox` state is unreliable from scripts; use a real click and verify `aria-checked="true"` and that `rowfilter_documentNo` exists.
- NEXT: SWITCH POINT: logout; checker `Auto_Tssm` approves document 1350 from the same Dispatch Advice option.

## Replay log, part 5: checker approval (Auto_Tssm, 2026-09-29)
- After the SWITCH point the checker `Auto_Tssm` logged in (identity verified from the profile name) and opened the same Dispatch Advice option: DA **1350** was visible as In-Active / **Pending for approval**; Forward and Reject were enabled; Forward with comment "Auto" gave "Forwarded successfully"; after reloading, the grid shows **Active / Approved**, Received Date 2026-09-29.
- Full step table with results: `TC-DA-01_executed.md` (17 steps, all pass; 7 drift findings).
- Next in the framework chain: flow 0280 Stock Validation After DA (user Auto_Multi_Orga), then 0001 Order Booking, 0013 Stock Allocation, ... (see chain above).

## Stock Validation After DA (flow 0280, menu group 0280) from the framework tables (2026-09-29)
- Navigation: search text "Stock Inquiry", option **STOCKINQUIRY**; screens 028001 (criteria), 028002 (grid filter), 028003 (values). Framework user: **Auto_Multi_Orga** (serial 35, login Y).
- 028001 fields: Period Type `DDL__pptp_period_type`, Balance Date `DDT__tssb_balance_date`, Category `categoryFilter`, Brand `brandFilter`; event: load data (Excel), click `showInquiryRefresh` ("Show Inquiry"), group assertion `TSTMSG,screenshot_ASSR`.
- 028002: row filters `rowfilter_asyd` (product), `rowfilter_warehousedesc` (warehouse), `rowfilter_TXT__STOCKTYPEDESC` (stock type); click `checkbox-0` (first row), load data, screenshot assertion.
- 028003: readable cells `row_1_in_cs`, `row_1_out_cs`, `row_1_in_pc`, `row_1_out_pc`; event 0007 data validation against the case-data values; click `row_1_closing_pc` ("slide" to expand).
- **Auto_Tssm cannot open Stock Inquiry**: the sidebar search finds no entry (verified live). The stock validation therefore needs the switch back to Auto_Multi_Orga.

## Replay log, part 6: stock validation (Auto_Multi_Orga, 2026-09-29)
- Stock Inquiry = layout 201069 (Transaction > Stock > Stock Inquiry). Result table and findings: `TC-DA-01_executed.md` (TC-DA-02). Closing balance of 62740537 in Auto Main Warehouse = 80 CS = DA 1350's quantity; the framework's expected In 80 / Out 0 fails on a busy day (In 176, Out 96). Loss quantities not yet in Damaged/Lost stock (needs Loss Approval, skipped).
- Next in chain (same user Auto_Multi_Orga, no switch): flow 0001 Order Booking, 0013 Stock Allocation, 0296 Transaction Inquiry validation, ...

## Group 11 session plan (from `fct_pr_gtfd_group_test_flow_detail`, pgtf_grouptestflowid = '11', pgtfd_status = 'Y', ordered by pgtfd_sequenceno) — confirmed with the QA lead 2026-09-29
Semantics: `plu_serial_no` = the user to be logged in; `pgtf_testflow_login_status = 'Y'` = the legacy engine **logs out and logs in as that user before the flow**; blank / `N` = continue in the current session (`N` rows repeat the current user). Query used: `select * from fct_pr_gtfd_group_test_flow_detail where pgtf_grouptestflowid = '11' and pgtfd_status = 'Y' order by 3`.
| Segment | User | Starts at seq | Flows (seq: flow) |
|---|---|---|---|
| A | Maker: default login, not named in the tables (Auto_Multi_Orga works) | 1 | 1 Login Dcode, 2 Dispatch Advice |
| B | Auto_Tssm | 5 (Y) | 5 DA Approval, **7 DA Loss Approval** |
| C | Auto_Multi_Orga | 9 (Y) | 9 Stock Validation After DA, 10 Order Booking (N), 12 Stock Allocation, 14 Transaction Inquiry after OB, 15 Order Editing, 16 Order Cancellation, 18 Stock Unallocation, 19 Delivery Date Change (N), 20 Goods Issue Note |
| D | Auto_Tssm | 23 (Y) | 23 GIN Approval |
| E | Auto_Multi_Orga | 24 (Y) | 24 Stock validation after GIN, 29 Order Editing After GIN (N), 31 Order Cancellation After GIN, 32 Cashmemo Reschedule, 33 Cashmemo Status, 34 Sales Return, 36 Sales Return View |
| F | Auto_Tssm | 37 (Y) | 37 Sales Return View Approval |
| G | Auto_Multi_Orga | 38 (Y) | 38 Sales Return Status Change, 39 Deposit Slip Full Amount Cash, 40 Full Amount Cheque, 41 Unposted Amount Validate, 42 Multi Cheques, 44 Cheque, 46 Cash, 48 Good Return Note |
| H | Auto_Tssm | 49 (Y) | 49 Good Return Note Approval |
| I | Auto_Multi_Orga | 50 (Y) | 50 Stock validation after GRN, 51 Route Settlement (N), 52 Offset Amount Validate, 53 Deposit Slip After RS, 54 Deposit Slip Cash removal, 55 Cheque Status, 56 DSR Adjustment Amount, 57 PJP Daily Inquiry Update, 58 OTC Stock Out R1 |
| J | Auto_Tssm | 59 (Y) | 59 SAN Approval PAK |
| K | Auto_Multi_Orga | 60 (Y) | 60 Opening & Closing Stock Validation, 68 Edited Order Charges Tax, 69 Charges Tax After Sales Return, 70 Transaction Inquiry After Order Editing, 71 Transaction Inquiry After Sales Return |
**10 switch points** in the whole cycle. Deviation so far: **seq 7 (DA Loss Approval) not yet run** for DA 1350; seq 9 (stock validation) was run before it.

## Replay log, part 7: DA Loss Approval (Auto_Tssm, 2026-09-29)
- Loss record **637** (DA-01, DA 1350) was Pending for approval; the detail tab listed exactly the three entered losses; Forward with "Auto": "Forwarded successfully"; status **Approved**. Details: TC-DA-03 in `TC-DA-01_executed.md`.
- NEXT: SWITCH to Auto_Multi_Orga and re-run the stock validation (TC-DA-02) to see whether the Damaged (02) and Lost (04) quantities now appear in Auto Main Warehouse.

## Replay log, part 8: stock re-check (2026-09-29)
- After the Loss Approval, Stock Inquiry (Auto_Multi_Orga) still shows only Sound rows for 20050310 and 62690363 in Auto Main Warehouse; the earlier hypothesis that Loss Approval creates the Damaged/Lost lines is not confirmed. Open question recorded in TC-DA-01_executed.md.
- DA slice status: created, forwarded, approved, loss approved, stock (Sound) validated. Next in chain as Auto_Multi_Orga: 0001 Order Booking, 0013 Stock Allocation, 0296 Transaction Inquiry after OB.

## Replay log, part 9: Order Booking (Auto_Multi_Orga, 2026-09-29)
- Flow 00010001 executed: order **COL26000001995**, gross 143,109.13 / net 134,999.00 = workbook. Details, drift and findings: `TC-OB-01_executed.md`. Reference Number 100 collision fixed by leaving the field empty.
- NEXT in chain (same user): 0013 Stock Allocation (seq 12), 0296 Transaction Inquiry validate after OB (seq 14), 0002 Order Editing (15), 0004 Order Cancellation (16), 001301 Stock Unallocation (18), 0016 Delivery Date Change (19), 0005 GIN (20).
