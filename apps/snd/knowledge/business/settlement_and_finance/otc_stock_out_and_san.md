# OTC Stock Out (SAN) and its approval (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas and the snd-schema DB. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 02950001 (seq 58), 03500001 (seq 59). Inactive siblings: SAN (Admin) 02840001, W-to-W 00120001, approvals seq 62/65, validations 02850001/02860001. No live replay; no 010104 stock-master rows in DB.

## 1. Purpose
A Stock Adjustment Note (SAN) changes stock without an order: here an "OTC stock out" removes stock from a warehouse for a stated reason (damage, expiry, loss, over-limit and the like [inferred]). It is the finance-relevant stock write-off of the day, reviewed by an approver before it hits stock.

## 2. Actors and roles
Maker Auto_Multi_Orga creates and forwards (seq 58); checker Auto_Tssm approves (seq 59, user switch) [db]. Maker and checker must differ [known fact].

## 3. Documents and master data
Header/detail in `snd_tr_stm_stock_master` (document number "Document No", type, date, status, approval status) [db]. Document types [db, 010104]: SA "Stock Adjustment Note (ADJ Positive Minus)" inactive; SA-01 Warehouse To Warehouse Transfer; SA-02 Stock Adjustment Entry (SAE); SA-03 Stock Adjustment Admin; SFT Stock Adjustment From Transfer (Auto); SNA Stock Adjustment Note Minus inactive. Which type "OTC Stock Out R1" uses: candidate SA-03 Stock Adjustment Admin [inferred 2026-10-01 from the live dropdown and grid; workbook data still unread]. Workflow statuses: 01 Draft, 02 Pending for approval, 03 Approved, 04 Rejected, 05 Terminated [db: wkf_wf_wfs_workflow_status]. Reason Type list: glb_pr_rnt_reason_type (no rows for SA types in 010104).

## 4. Inputs: screens and fields
Live-verified 2026-10-01 [observed]: /ngui/dyl/layout?layoutCode=201045, grid "SAN Header" 164 rows; form fields Document No*, Document Date (default today), SAN Type*, From Warehouse*, To Warehouse, Comments, Status (In-Active), Approval Status (Draft); Add and Save enabled, Update/Delete/Forward/Reject disabled, SAN Detail tab disabled; nothing saved. SAN Type options (5): Warehouse To Warehouse Transfer (default), Stock Adjustment Entry, Stock Adjustment Admin, Physical Stock Reconciliation, Stock Adjustment From Transfer (Auto); db codes SA-01 W-to-W (nature SWT), SA-02 Stock Adjustment Entry (SAN_EQL), SA-03 Stock Adjustment Admin (SAN_ADJ, calc nature +), SFT Auto; Physical Stock Reconciliation has no row by that name in snd_pr_dot_documenttype. From Warehouse list 45 entries (0000000025-IBT Main warehouse, C0000000055-Auto Main Warehouse, C0000000195-SAN Warehouse A, C0000000196-SAN Warehouse B and about 41 warehouses named "Automation"); To Warehouse list the same minus IBT Main (44); defaults From = IBT Main warehouse, To = Auto Main Warehouse. **No SAN Type is labelled OTC or stock out, and the sidebar search "OTC" finds nothing (control search "Stock Adj" works): no "OTC Stock Out" menu exists.** The closest is Stock Adjustment Admin (SA-03): the 94-95 most recent grid rows are Stock Adjustment Admin from Auto Main Warehouse with no To Warehouse [observed] (candidate only, [inferred]). Auto_Tssm also has Stock Adjustment SAN [observed].
Menu: Transaction > Stock > Stock Adjustment SAN (`DYL_201045`) [db].
- Header 029501: **SAN Type***, **From Warehouse*** (list DIST2WRHS), To Warehouse (only for transfers), Comments; read-only Document No, Document Date (SAN Date), Document Type, Status (default I), Approval Status (default 01) [db].
- Detail 029502 (SAN Detail tab): **Product***, **Stock Type***, **Reason Type***, **Batch***, CS, PC; row save/cancel [db: atlas].
- Forward 029503: filter, select the document, Forward, popup Save; assert toast from SAN_FWD_ASSR [db].
- Approval 035001 (SAN Approval PAK): filter, pick the document, Forward (approve) and popup Save; toast from SAN_APP_ASSR [db]. A mandatory comment applies as for other approvals [known fact].

## 5. Process
1. [Maker] Create SAN: SAN Type, From Warehouse, Comments; Save (assert ELEVLD and TSTMSG); Document No and Type stored in REPO_DocumentNo/REPO_DocumentType. trace 11:58:02950001
2. [Maker] Add detail line: Product, Stock Type, Reason Type, Batch, CS, PC; row Save.
3. [Maker] Forward the document (Draft -> Pending for approval); assert SAN_FWD_ASSR.
4. [Checker Auto_Tssm] Log in, open SAN Approval, select the document by REPO_DocumentNo, approve with comment; assert SAN_APP_ASSR. trace 11:59:03500001
5. [Maker] Seq 60: validate stock (end_of_day_validations.md).

## 6. Outputs and effects
After approval, stock of the product/batch/stock type in the From Warehouse is reduced by CS/PC [inferred; no replay]. The document is Approved (wf 03) and status A [inferred from DA documents: tstm_status A with wf 03].

## 7. Statuses and transitions
| from | action | to | by | tag |
|---|---|---|---|---|
| (new) | Save | status I, wf 01 Draft | Maker | [db] defaults |
| 01 Draft | Forward | 02 Pending for approval | Maker | [db] |
| 02 | Approve | 03 Approved (status A) | Checker | [db] names, DA analogue observed in data |
| 02 | Reject / Terminate | 04 / 05 | Checker | [db] names |

## 8. Rules and validations
- SAN Type, From Warehouse, Product, Stock Type, Reason Type, Batch mandatory [db].
- Stock out cannot exceed available stock of that batch [inferred]; an ELEVLD element-level validation is asserted on 029501 [db].
- Maker differs from checker [known].

## 9. Messages
Atlas has assertion slots only (ELEVLD, TSTMSG, SAN_FWD_ASSR, SAN_APP_ASSR); texts unrecorded [unknown].

## 10. Dependencies
Reads stock available after GIN/GRN (opening balance for the day). Hands the approved stock-out to the Opening and Closing Stock validation (seq 60). Stock balances are keyed by calendar day.

## 11. Test design hints
Positive: damage stock-out of 1 PC; of full batch. Negative: qty above stock; zero qty; missing Reason Type; approve with same user as maker; approve without comment; forward without lines. Boundary: qty = available; available + 1 PC; CS/PC conversion (PC beyond a case). Not proved by green run: actual stock decrease (assertions are toasts only).

## 12. Open questions
ANSWERED 2026-10-01 (Q57, default updated): no type or menu is called OTC Stock Out; use Stock Adjustment Admin (SA-03, single warehouse) as the stock-out type unless the workbook says otherwise [observed dropdown + grid, inferred mapping].
Q: Does stock reduce on forward or on approval? | Default: on approval | Evidence: no replay.
Q: Is there a financial posting (write-off value, moving average price)? | Default: stock value only | Evidence: none.

## 13. Sources
framework_atlas/flows/02950001, 03500001; group_11.md; screens_db/DYL_201045.json; DB snd_pr_dot_documenttype, wkf_wf_wfs_workflow_status, snd_tr_stm_stock_master.
