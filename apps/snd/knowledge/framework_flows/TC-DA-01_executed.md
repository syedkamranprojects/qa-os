# TC-DA-01 Create, forward and approve a Dispatch Advice with loss: EXECUTED 2026-09-29

Environment cnr1dev1 (Unilever Pakistan, distributor 15108843 IBRAHIM TRADERS "Auto KARACHI"). Source: selenium-framework-db group 11 (flows 00100001 + 00740001), case data `NG_Dcode_QA_OTC (Pak).xlsx`. Vocabulary: `docs/STEP_VOCABULARY.md`.
Actors: **Maker = Auto_Multi_Orga**, **Checker = Auto_Tssm**.

| # | Actor | Step | Result | Verdict |
|---|---|---|---|---|
| 1 | Maker | Login as Maker (company Unilever Pakistan Limited; distributor 15108843-IBRAHIM TRADERS) | user shown: Auto_Multi_Orga | Pass |
| 2 | Maker | Navigate to Dispatch Advice | layout 201068, grid 1,303 rows | Pass |
| 3 | Maker | Create Dispatch Advice with Warehouse = "C0000000055-Auto Main Warehouse", Vendor Code = "UPL WH", SO Number = "Automation_29-09-2026", Shipment No = 123, Deliver No = 12312, Tax Invoice Number = 123, Comments = "Positive_QA_Automation_01", Reference No = 1115 | message "Saved successfully"; Document No **1350** | Pass |
| 4 | Maker | Remember Document No as DA1 | 1350 | Pass |
| 5 | Maker | Add line to DA1: Product 62740537, CS 80 | "Saved Successfully!" | Pass |
| 6 | Maker | Add line to DA1: Product 20050310, CS 70 | "Saved Successfully!" | Pass |
| 7 | Maker | Add line to DA1: Product 62690363, CS 60 | "Saved Successfully!" | Pass |
| 8 | Maker | Add line to DA1: Product 20050308, CS 50 | "Saved Successfully!" | Pass |
| 9 | Maker | Add loss to line 2: Damaged / Area Closed / CS 4; Lost / On Customer Behalf / CS 2 | line 2: Loss 6-0-0, Received 64; "Saved Successfully!" (loss modal shows no message) | Pass (message check differs from framework) |
| 10 | Maker | Add loss to line 3: Damaged / On Customer Behalf / CS 5 | Loss 5-0-0, Received 55; "Saved Successfully!" | Pass |
| 11 | Maker | Verify status of DA1 is Draft (Status In-Active) | grid: In-Active / Draft, net PKR 1,632,119.522 | Pass |
| 12 | Maker | Forward DA1 with comment "Auto" | "Forwarded successfully"; Approval Status Pending for approval | Pass |
| 13 | Maker | Logout | session ended | Pass |
| 14 | Checker | Login as Checker | user shown: Auto_Tssm | Pass |
| 15 | Checker | Navigate to Dispatch Advice | grid 1,304 rows (includes DA1) | Pass |
| 16 | Checker | Approve DA1 (Forward with comment "Auto") | "Forwarded successfully" | Pass |
| 17 | Checker | Verify status of DA1 is Active, Approval Status Approved | grid: Active / Approved, Received Date 2026-09-29 | Pass |

**Result: PASS.** Business outcome: DA 1350 is approved; stock for 4 products is received into Auto Main Warehouse (not yet verified on a stock screen: next flow "Stock Validation After DA").

## Findings for the framework owner (drift between framework config and the live app)
1. Loss-modal save shows no toast; framework event 5 (TSTMSG after modal save) would fail.
2. `rowEditBtn_Save_0` is used for every line, but a line edited after the first (loss on line 2 or 3) has id `rowEditBtn_Save_<row index>`.
3. `forwardBtn` is a wrapper; the working click target is the inner `forward` dx-button. The comment needs a blur (Tab) before Save.
4. `gridFilterCheckbox` is a toggle whose state persists across screen reopen; the engine must check `aria-checked` (or the presence of `rowfilter_documentNo`) before clicking.
5. The maker for DA creation is not defined in the framework tables (`Automation` login rejected on 2026-09-29; `Auto_Multi_Orga` works); the checker `Auto_Tssm` cannot create a DA.
6. After Company, the login shows a Distributor dropdown; the case-data sheet `Distributor selection` covers it (15108843).
7. The checker approves the same way the maker forwards (no separate Approve button); a maker (KPO_mp on M&P) was able to approve their own DA 570: no maker-checker control in the app for that user.

## Test data left on cnr1dev1
DA **1350** (Auto KARACHI, Auto Main Warehouse) Approved; DA **570** (M&P Main Warehouse, KPO_mp) Approved. Stock received for products 62740537, 20050310, 62690363, 20050308.

---
# TC-DA-02 Stock validation after Dispatch Advice: EXECUTED 2026-09-29 (framework flow 0280)
Actor: **Stock Controller = Auto_Multi_Orga** (Auto_Tssm has no Stock Inquiry screen). Read-only.

| # | Actor | Step | Result | Verdict |
|---|---|---|---|---|
| 1 | Checker | Logout | ended | Pass |
| 2 | Stock Controller | Login as Stock Controller (Company Unilever Pakistan Limited, distributor 15108843) | user shown Auto_Multi_Orga | Pass |
| 3 | Stock Controller | Navigate to Stock Inquiry | layout 201069, breadcrumb Transaction > Stock > Stock Inquiry | Pass |
| 4 | Stock Controller | Choose Period Type = DAILY; Balance Date = today; Category = All; Brand = All (defaults) | as workbook (workbook date 2026-09-21; today used) | Pass |
| 5 | Stock Controller | Show Inquiry | 39 rows, 21 columns (no message) | Pass |
| 6 | Stock Controller | Verify stock of 62740537 in Auto Main Warehouse (Sound) | Opening 0, **In 176, Out 96, Closing 80** | see finding 1 |
| 7 | Stock Controller | Verify stock of 20050310 / 62690363 / 20050308 in Auto Main Warehouse (Sound) | In 294 / 288 / 151 CS, Out 30 / 18 / 13 CS, Closing 5706 / 6171 / 1955 CS | Informational |

Expected values in the workbook (`Stock_Val_After_DA_PAK*`): product 62740537, warehouse Auto Main Warehouse, stock type 01 - Sound, **In CS 80, Out CS 0, In PC 0, Out PC 0**.

**Result: PARTIAL.** Closing balance of 62740537 (80 CS) equals exactly what DA 1350 received, so the stock IS received. The framework's exact In/Out check (80 / 0) fails today because of other stock movements on the same day (In 176, Out 96 net to 0).

## Findings
1. **The framework's stock validation assumes a clean day**: expected In = quantity of this DA only. Any other stock movement in the same warehouse and balance date (another DA, GRN, GIN or sales) makes the check fail. Better: validate the *change* (before/after snapshot of the closing balance) or use a document-level movement view.
2. **Loss quantities are not in Damaged/Lost stock yet**: for the products with loss (20050310, 62690363) there are no `02 - Damaged` or Lost rows in Auto Main Warehouse for today. The loss appears to need the **Loss Approval** step (framework flow 00760001, option DYL_202026) before it moves stock; that step was skipped on the QA lead's instruction ("just approve the DA").
3. The workbook's balance date (2026-09-21) and DA date are hard-coded; the check must use today's date.
4. `checkbox-0` (drill-down) reloads the grid and clears the row filter; the framework's `row_1_*` cells then refer to the first row of the unfiltered grid, not the filtered product (framework expects the filter to persist).
5. Stock Inquiry has a **Generate Opening Balances** button (changes data): must never be part of a validation flow.

---
# TC-DA-03 DA Loss Approval: EXECUTED 2026-09-29 (framework flow 00760001, chain seq 7)
Actor: **Checker = Auto_Tssm**. Precondition: DA 1350 approved with losses.

| # | Actor | Step | Result | Verdict |
|---|---|---|---|---|
| 1 | Stock Controller | Logout | ended | Pass |
| 2 | Checker | Login as Checker | user shown Auto_Tssm | Pass |
| 3 | Checker | Navigate to Loss Approval | layout 202026, master grid 364 rows (363 before DA 1350: one new record) | Pass |
| 4 | Checker | Sort by Serial No, newest first (header clicked once = descending; twice = ascending) | first row: Serial **637**, DA-01, Document **1350**, Pending for approval | Pass |
| 5 | Checker | Open Loss record 637 | Master: Serial 637, Document No 1350, Document Type Dispatch Advice, Status Pending for approval | Pass |
| 6 | Checker | Verify Loss Approval Detail lists the losses | 20050310 SKU Type 02 (Damaged) 4 CS and SKU Type 04 (Lost) 2 CS of 70 dispatched / 64 received; 62690363 SKU Type 02 (Damaged) 5 CS of 60 dispatched / 55 received | Pass (matches entered losses) |
| 7 | Checker | Approve loss record 637 (Forward with comment "Auto") | "Forwarded successfully" | Pass |
| 8 | Checker | Verify status of loss record 637 is Approved | grid: 637 / 1350 / **Approved** | Pass |

**Result: PASS.** Notes: the record appears in Loss Approval automatically when a DA with losses is forwarded/approved; the framework's flow 00750001 ("Loss Approval Request", inactive in group 11) is not needed for this path. Tabs must be clicked with a real click (scripted `.click()` on the tab element did not switch). Assertion `DA_LOSS_APPROVALFRWD_ASSR` expects the toast above.

---
# TC-DA-02 re-run after Loss Approval: EXECUTED 2026-09-29 (Auto_Multi_Orga)
Steps: Logout (Checker), Login as Stock Controller, Navigate to Stock Inquiry, Show Inquiry, filter product 20050310 / 62690363.
Result (unchanged from before the loss approval): Auto Main Warehouse, stock type 01 - Sound only. 20050310: open 5487-0-2, In 294-0-1, Out 30-0-0, Close 5706-0-3. **No 02 - Damaged and no 04 - Lost row exists for 20050310 or 62690363**, in any warehouse, although DA 1350's losses (Damaged 4 + Lost 2 CS; Damaged 5 CS) were approved (Loss record 637 Approved). Only two other non-Sound rows exist in the inquiry (LIPTON 20080958 Damaged in SAN Warehouse A; LIFEBUOY 20061858 Variance in Auto Main Warehouse).
**Correction of finding 2 above:** the Loss Approval is NOT what puts the loss quantities into the Damaged/Lost stock lines shown by Stock Inquiry. Either the movement is posted later (a scheduled job or day-end), goes to a different screen (claims / DA loss report), or the inquiry only shows Sound stock for these products. Open question for the framework owner / BA: where do approved DA losses appear as stock?
Method notes: the inquiry grid is paged (15 of 39 rows in the DOM); use the product filter (`rowfilter_asyd`, tick `gridFilterCheckbox` with a real click) instead of reading the page.
