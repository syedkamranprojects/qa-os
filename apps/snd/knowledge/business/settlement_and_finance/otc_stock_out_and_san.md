---
option: OTC Stock Out (Stock Adjustment SAN, type Stock Adjustment Admin)
area: settlement_and_finance
doc_types: [SA-03]
screens: [DYL_201045]
framework_flows: ["02950001", "03500001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [goods_return_note, stock_inquiry_and_balances]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-06
---

# OTC Stock Out (SAN) and its approval (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas and the snd-schema DB. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 02950001 (seq 58), 03500001 (seq 59). Inactive siblings: SAN (Admin) 02840001, W-to-W 00120001, approvals seq 62/65, validations 02850001/02860001. No live replay; no 010104 stock-master rows in DB. (superseded 2026-10-05: walked live in G11-2b, SAN **96** created, forwarded, approved and stock-checked.)
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.

## 1. Purpose
A Stock Adjustment Note (SAN) changes stock without an order: here an "OTC stock out" removes stock from a warehouse for a stated reason (damage, expiry, loss, over-limit and the like [inferred]). It is the finance-relevant stock write-off of the day, reviewed by an approver before it hits stock.
- G11-2b: walked live: the framework's "OTC Stock Out R1" was performed as a Stock Adjustment SAN of type **Stock Adjustment Admin** from Auto Main Warehouse with a negative quantity (-50 CS of 62740537); on approval the quantity left Sound stock as **Out** [observed 2026-10-05 G11-2b].
- G11-3: walked again: **SAN 97**, Stock Adjustment Admin, -50 CS of 62740537 from Auto Main Warehouse; approval posted Out +50 [observed 2026-10-06 G11-3].

## 2. Actors and roles
Maker Auto_Multi_Orga creates and forwards (seq 58); checker Auto_Tssm approves (seq 59, user switch) [db]. Maker and checker must differ [known fact].
- G11-2b: Maker Auto_Multi_Orga saved and forwarded SAN 96 (the detail quantity was typed by the QA lead in Claude's session); Checker Auto_Tssm approved it on the same Stock Adjustment SAN option. For the Checker on the Pending SAN: Forward and **Reject** enabled, Save/Update/Delete disabled [observed 2026-10-05 G11-2b].
- G11-3: Maker Auto_Multi_Orga created SAN 97 and typed the quantity himself (no permission block); Checker Auto_Tssm approved it [observed 2026-10-06 G11-3].

## 3. Documents and master data
Header/detail in `snd_tr_stm_stock_master` (document number "Document No", type, date, status, approval status) [db]. Document types [db, 010104]: SA "Stock Adjustment Note (ADJ Positive Minus)" inactive; SA-01 Warehouse To Warehouse Transfer; SA-02 Stock Adjustment Entry (SAE); SA-03 Stock Adjustment Admin; SFT Stock Adjustment From Transfer (Auto); SNA Stock Adjustment Note Minus inactive. Which type "OTC Stock Out R1" uses: candidate SA-03 Stock Adjustment Admin [inferred 2026-10-01 from the live dropdown and grid; workbook data still unread]. Workflow statuses: 01 Draft, 02 Pending for approval, 03 Approved, 04 Rejected, 05 Terminated [db: wkf_wf_wfs_workflow_status]. Reason Type list: glb_pr_rnt_reason_type (no rows for SA types in 010104).
- G11-2b: SAN Document No **96** (previous SANs 93-95 on 09-22/28/29, same type, all Approved) [observed 2026-10-05 G11-2b].
- G11-3: SAN Document No **97** on 2026-10-06 [observed 2026-10-06 G11-3].
- G11-2b: Reason Type options on the line: test, HHB, MICE BITTEN, Just Cause; Stock Type 01-Sound / 02-Damaged / 03-Expired / 04-Lost; Batch 1-1 (only option) [observed 2026-10-05 G11-2b].

## 4. Inputs: screens and fields
Live-verified 2026-10-01 [observed]: /ngui/dyl/layout?layoutCode=201045, grid "SAN Header" 164 rows; form fields Document No*, Document Date (default today), SAN Type*, From Warehouse*, To Warehouse, Comments, Status (In-Active), Approval Status (Draft); Add and Save enabled, Update/Delete/Forward/Reject disabled, SAN Detail tab disabled; nothing saved. SAN Type options (5): Warehouse To Warehouse Transfer (default), Stock Adjustment Entry, Stock Adjustment Admin, Physical Stock Reconciliation, Stock Adjustment From Transfer (Auto); db codes SA-01 W-to-W (nature SWT), SA-02 Stock Adjustment Entry (SAN_EQL), SA-03 Stock Adjustment Admin (SAN_ADJ, calc nature +), SFT Auto; Physical Stock Reconciliation has no row by that name in snd_pr_dot_documenttype. From Warehouse list 45 entries (0000000025-IBT Main warehouse, C0000000055-Auto Main Warehouse, C0000000195-SAN Warehouse A, C0000000196-SAN Warehouse B and about 41 warehouses named "Automation"); To Warehouse list the same minus IBT Main (44); defaults From = IBT Main warehouse, To = Auto Main Warehouse. **No SAN Type is labelled OTC or stock out, and the sidebar search "OTC" finds nothing (control search "Stock Adj" works): no "OTC Stock Out" menu exists.** The closest is Stock Adjustment Admin (SA-03): the 94-95 most recent grid rows are Stock Adjustment Admin from Auto Main Warehouse with no To Warehouse [observed] (candidate only, [inferred]). Auto_Tssm also has Stock Adjustment SAN [observed].
Menu: Transaction > Stock > Stock Adjustment SAN (`DYL_201045`) [db].
- Header 029501: **SAN Type***, **From Warehouse*** (list DIST2WRHS), To Warehouse (only for transfers), Comments; read-only Document No, Document Date (SAN Date), Document Type, Status (default I), Approval Status (default 01) [db].
- Detail 029502 (SAN Detail tab): **Product***, **Stock Type***, **Reason Type***, **Batch***, CS, PC; row save/cancel [db: atlas].
- Forward 029503: filter, select the document, Forward, popup Save; assert toast from SAN_FWD_ASSR [db].
- Approval 035001 (SAN Approval PAK): filter, pick the document, Forward (approve) and popup Save; toast from SAN_APP_ASSR [db]. A mandatory comment applies as for other approvals [known fact].
- G11-2b live [observed 2026-10-05 G11-2b]: header defaults SAN Type Warehouse To Warehouse Transfer, From IBT Main warehouse, To Auto Main Warehouse, Status In-Active, Approval Status Draft; only Save enabled; SAN Detail tab disabled until the header is saved. Choosing **Stock Adjustment Admin clears To Warehouse** (not used by this type).
- G11-2b SAN Detail: "Add a row"; columns Product, Stock Type, Reason Type, Batch, **Current Stock (ATP)** (CS-DZ-PC), **Adjustment Quantity**, **Price**, Gross Amount, Tax Amount, CS, DZ, PC; row links Edit / Delete. Product type-ahead label "62740537-RAFHAN SLPC OILS CORN TIN PI7 2X10L-7711.47". After a detail save the header tab resets to a blank new document; re-select SAN 96 in the grid to Forward.

## 5. Process
1. [Maker] Create SAN: SAN Type, From Warehouse, Comments; Save (assert ELEVLD and TSTMSG); Document No and Type stored in REPO_DocumentNo/REPO_DocumentType. trace 11:58:02950001
2. [Maker] Add detail line: Product, Stock Type, Reason Type, Batch, CS, PC; row Save.
3. [Maker] Forward the document (Draft -> Pending for approval); assert SAN_FWD_ASSR.
4. [Checker Auto_Tssm] Log in, open SAN Approval, select the document by REPO_DocumentNo, approve with comment; assert SAN_APP_ASSR. trace 11:59:03500001
5. [Maker] Seq 60: validate stock (end_of_day_validations.md).

G11-2b walk, SAN 96 (2026-10-05) [observed 2026-10-05 G11-2b]:
1. [Maker] Navigate to Stock Adjustment SAN; Choose SAN Type Stock Adjustment Admin; Choose From Warehouse C0000000055-Auto Main Warehouse; Enter Comments "Automation"; Click Save -> "Saved successfully"; SAN 96, In-Active / Draft; Update, Delete, Forward, Add and SAN Detail enabled (11:58:02950001).
2. [Maker] Open SAN Detail; Add a row: Product 62740537, Stock Type 01-Sound, Reason Type test, Batch 1-1 -> Current Stock (ATP) 309-0-0, Price 7,711.47; CS -50; row Save -> Adjustment Quantity -50, Gross -771,146.50, Tax 0 (11:58:02950001).
3. [Maker] Re-select SAN 96; Click Forward; Enter Comments "Automation Approval" (verified); Save -> "Forwarded successfully"; In-Active / Pending for approval (11:58:02950001).
4. [Checker] Navigate to Stock Adjustment SAN; Open SAN 96 (Pending); Click Forward; Enter Comments; Save -> "Forwarded successfully"; SAN 96 Active / Approved in one Checker step (11:59:03500001).
5. [Maker] Stock Inquiry 2026-10-05: 62740537 Out 35 -> 85, Closing 309 -> 259 (11:60:02830001).

G11-3 walk, SAN 97 (2026-10-06) [observed 2026-10-06 G11-3]:
1. [Maker] Stock Adjustment SAN: SAN Type Stock Adjustment Admin, From C0000000055-Auto Main Warehouse, Comments "Automation"; Save -> "Saved successfully"; SAN 97 Draft (11:58:02950001).
2. [Maker] SAN Detail; Add a row: 62740537 / 01-Sound / test / 1-1 -> Current Stock (ATP) **58-0-0** (= Closing 65 - 7 CS allocated to 2012 for GIN 509); CS -50 -> Gross -771,146.5; row Save -> "Record Saved Successfully!".
3. [Maker] Tab SAN Header; select SAN 97; Forward; comment "Automation Approval" (verified); Save -> "Forwarded successfully"; Pending for approval.
4. [Checker] Stock Adjustment SAN; SAN 97 (Pending); Forward; comment "Automation Approval"; Save -> "Forwarded successfully"; **Active / Approved** (11:59:03500001).
5. [Maker] Stock Inquiry 2026-10-06: 62740537 Out 39 -> **89** (32 GIN 508 + 7 GIN 509 + 50 SAN 97), Closing **8** (11:60:02830001).

## 6. Outputs and effects
After approval, stock of the product/batch/stock type in the From Warehouse is reduced by CS/PC [inferred; no replay]. The document is Approved (wf 03) and status A [inferred from DA documents: tstm_status A with wf 03].
- G11-2b (upgrades "stock reduced on approval [inferred]"): **after approval Sound stock of 62740537 at Auto Main Warehouse: Out +50, Closing -50** (309 -> 259); In unchanged [observed 2026-10-05 G11-2b]. Stock after the Maker's Forward alone was not read [unknown; Q58 PARTLY].
- G11-2b: line value Gross -771,146.50 = 100 PC x 7,711.47: the SAN **Price is per PC** (1 CS = 2 PC for this 2X10L pack); Tax 0 [observed 2026-10-05 G11-2b]. A finance posting of this value was not looked for [unknown; BA13].
- G11-2b: the approved SAN reads Status Active, Approval Status Approved [observed 2026-10-05 G11-2b].
- G11-3: SAN approval again posted as **Out +50** (no change at the Maker's Forward was read); Gross -771,146.5 again (price per PC) [observed 2026-10-06 G11-3].

## 7. Statuses and transitions
| from | action | to | by | tag |
|---|---|---|---|---|
| (new) | Save | status I, wf 01 Draft | Maker | [db] defaults |
| 01 Draft | Forward | 02 Pending for approval | Maker | [db] |
| 02 | Approve | 03 Approved (status A) | Checker | [db] names, DA analogue observed in data |
| 02 | Reject / Terminate | 04 / 05 | Checker | [db] names |

- G11-2b confirmation [observed 2026-10-05 G11-2b]:

| from | action | to | by | tag |
|---|---|---|---|---|
| (new) | Save header | In-Active / Draft | Maker | observed 2026-10-05 G11-2b |
| Draft | Forward + comment | In-Active / Pending for approval | Maker | observed 2026-10-05 G11-2b |
| Pending | Forward + comment | Active / Approved (one step) | Checker | observed 2026-10-05 G11-2b |
| Pending | Reject | (enabled for the Checker, not clicked) | Checker | observed button state 2026-10-05 G11-2b |

## 8. Rules and validations
- SAN Type, From Warehouse, Product, Stock Type, Reason Type, Batch mandatory [db].
- Stock out cannot exceed available stock of that batch [inferred]; an ELEVLD element-level validation is asserted on 029501 [db].
- Maker differs from checker [known].
- G11-2b: a stock-out is entered as a **negative Adjustment Quantity** on a Stock Adjustment Admin line [observed 2026-10-05 G11-2b].
- G11-2b: the line shows the product's ATP (= Stock Inquiry Closing) before the quantity is entered [observed 2026-10-05 G11-2b]. Whether a quantity above ATP is refused was not tried [unknown].
- G11-2b: Forward needs a comment (Comments popup) for Maker and Checker [observed 2026-10-05 G11-2b].
- G11-3: the line ATP reflects allocations not yet issued (58 = Closing 65 - 7 allocated for the later GIN 509) [observed 2026-10-06 G11-3].

## 9. Messages
Atlas has assertion slots only (ELEVLD, TSTMSG, SAN_FWD_ASSR, SAN_APP_ASSR); texts unrecorded [unknown].
- G11-2b: "Saved successfully" (header Save), "Forwarded successfully" (Maker Forward and Checker approval; = workbook SAN Approval PAK EXPECTED_MESSAGE) [observed 2026-10-05 G11-2b]. Detail row save message not recorded.
- G11-3: detail row save **"Record Saved Successfully!"**; "Saved successfully" (header); "Forwarded successfully" (Maker and Checker) [observed 2026-10-06 G11-3].

## 10. Dependencies
Reads stock available after GIN/GRN (opening balance for the day). Hands the approved stock-out to the Opening and Closing Stock validation (seq 60). Stock balances are keyed by calendar day.
- G11-2b: read the closing after GRN 247 as ATP (309); hands Out +50 to seq 60 [observed 2026-10-05 G11-2b].
- G11-3: ATP 58 after GRN 248 and the extra allocation for GIN 509; hands Out +50 to seq 60 [observed 2026-10-06 G11-3].

## 11. Test design hints
Positive: damage stock-out of 1 PC; of full batch. Negative: qty above stock; zero qty; missing Reason Type; approve with same user as maker; approve without comment; forward without lines. Boundary: qty = available; available + 1 PC; CS/PC conversion (PC beyond a case). Not proved by green run: actual stock decrease (assertions are toasts only).
- G11-2b additions [observed 2026-10-05 G11-2b]:
  - Positive: Stock Adjustment Admin -50 CS, approve, assert Out +50 / Closing -50 and Gross = qty in PC x price per PC.
  - Negative: the Checker has Reject on a Pending SAN (not walked); quantity above ATP (not walked).
  - Trap: after the detail row save the header resets to a blank document; re-select the SAN before Forward.
  - Trap: the CS cell re-renders on focus; enter the number key by key.
  - Trap: Gross uses price per PC; a CS-based expectation is off by the pack factor.
  - G11-3 trap: the expected ATP on the SAN line depends on everything allocated/issued that day (an extra GIN for a Reattempt order changed it 65 -> 58) [observed 2026-10-06 G11-3].

## 12. Open questions
ANSWERED 2026-10-01 (Q57, default updated): no type or menu is called OTC Stock Out; use Stock Adjustment Admin (SA-03, single warehouse) as the stock-out type unless the workbook says otherwise [observed dropdown + grid, inferred mapping].
Q: Does stock reduce on forward or on approval? | Default: on approval | Evidence: no replay.
Q: Is there a financial posting (write-off value, moving average price)? | Default: stock value only | Evidence: none.
- PARTLY ANSWERED 2026-10-05 (Q58): stock reduces at the latest on approval (Out +50); not read between Forward and approval [observed 2026-10-05 G11-2b].
- Q57 mapping confirmed by the walk: OTC Stock Out R1 = Stock Adjustment SAN, type Stock Adjustment Admin (the run matched the workbook approval message) [observed 2026-10-05 G11-2b; workbook SAN Type value not re-read].
- BA13 (financial posting of a SAN) still open; line Gross -771,146.50 observed.
- Q58 evidence 2026-10-06: Out +50 after approval again (SAN 97); stock after the Forward alone still not read [observed 2026-10-06 G11-3].

## 13. Sources
framework_atlas/flows/02950001, 03500001; group_11.md; screens_db/DYL_201045.json; DB snd_pr_dot_documenttype, wkf_wf_wfs_workflow_status, snd_tr_stm_stock_master.
- G11-2b: learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md (seq 58, 59, 60).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 58, 59, 60; SAN 97).
