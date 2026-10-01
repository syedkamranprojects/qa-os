# Dispatch Advice (DA): how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]** seen live, **[db]** declared by the DB or framework tables, **[inferred]** concluded by Claude, **[unknown]** not determinable yet.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 00100001 (group 11 seq 2), 00740001 (seq 5); inactive 00100002 (negative/delete), 00740002 (reject).

## 1. Purpose
A Dispatch Advice is the distributor's record that a vendor (the company supply point "UPL WH") has dispatched goods to the distributor's warehouse. When it is approved, the quantities RECEIVED become stock in that warehouse, so orders can later be allocated and issued (GIN). It is the first business step of the Daily Cycle: nothing can be sold until a DA is approved [observed: before DA 1356 was approved on 2026-10-01 every product pick in Order Booking answered "Stock not available."; after approval 62740537 became orderable]. Next: DA Loss Approval, then Stock Inquiry (see da_loss_approval.md, stock_inquiry_and_balances.md).

## 2. Actors and roles
- Maker = Auto_Multi_Orga (creates, adds lines and losses, Forward) [observed]. Auto_Tssm cannot create a DA: "Current user is not authorized to save this record!" [observed].
- Checker = Auto_Tssm (same screen, Forward = approve; Reject is the alternative) [observed].
- The app did NOT stop KPO_mp from approving its own DA 570 [observed]; "maker and checker differ" is a QA/framework rule, not a proven app control [inferred].
- Live-verified 2026-10-01: DA 1356 was created and forwarded by Auto_Multi_Orga and approved by Auto_Tssm (Forward with comment "Auto" -> "Forwarded successfully") [observed]. Self-approval was not tried again.

## 3. Documents and master data
- Document type DA-01 "Dispatch Advice" (also DA, DA-05 "Dispatch Advice Auto") [db snd_pr_dot_documenttype]. Header table snd_tr_stm_stock_master, lines snd_tr_stm_stock_detail [db]. Document No is a plain number (570, 1350, 1351, 1352) shown in DOCUMENTNO after save [observed].
- Master data: Warehouse (e.g. C0000000055-Auto Main Warehouse; default offered was 0000000025-IBT Main warehouse), Vendor Code (UPL WH, default), Products (62740537, 20050310, 62690363, 20050308), stock type Sound, batch 1-1 [observed]. DA Type options: Dispatch Advice, DA Against Purchase Order, Dispatch Advice Auto [observed].

## 4. Inputs: screens and fields
Menu Transaction > Primary Sale > Dispatch Advice (layout 201068, DYL_201068); tabs Header Info / Dispatch Detail [observed].
- Live 2026-10-01 (cycle DA 1357, four lines 62740537 CS 80, 20050310 CS 70, 62690363 CS 60, 20050308 CS 50, no loss, net PKR 1,651,126.412): typing the quantity right after the product pick, before stock type and batch have filled, leaves the quantity empty and the line save answers "The lost quantity does not equal the sum of dispatch and received quantities" (nothing saved); a new line is always row index 0 (rowEditBtn_Save_0); the product option list sometimes detaches (re-type the product) [observed].
- Header (mandatory *): Warehouse*, Vendor Code*, **DA Type*** (options Dispatch Advice, DA Against Purchase Order, Dispatch Advice Auto; a silent Save means it is empty) [observed 2026-10-01], SO Number (optional, not unique), Shipment No, Deliver No, Invoice Due Date, Tax Invoice Number, Comments, Reference Date, Reference No, Truck No, VAT Challan Number, Invoice Number; DOCUMENTNO read-only [atlas 001001]. Dates default to today [observed]. A fresh screen defaults DA Type = Dispatch Advice and Vendor = UPL WH, but after pressing **Add** for a second DA the form resets with Warehouse, Vendor Code AND DA Type empty: pick all three before Save [observed 2026-10-01]. Extra live fields: Document Date, Tax, Discount, Net Amount, Document Status, Stock Arrival, Status, Approval Status [observed].
- Lines (Dispatch Detail, empty until the header is saved): Product (type-ahead), Stock Type, Batch, CS; Stock Type and Batch fill by themselves AFTER the product pick and then RESET the quantity, so enter CS after the product and Tab [observed 2026-10-01]. Line Save/Edit links are anchors: scroll them into view before clicking (else "element not interactable") [observed]. Loss "+" (in the Loss cell while the row is in edit mode) opens modal "DA Loss Details": Stock, Loss Reason, CS; modal row Save; the Calculate button (CalculateBtn) is what pushes the loss to the line; closing the modal with the x DISCARDS the loss [observed 2026-10-01].
- Buttons: Add, Save, Update, Delete, Forward, Reject, Terminate [step_labels].
- Amount check screen (001010) reads Purchase Price / PC, Gross Amount, Discount, Tax Amount, Net Amount [atlas].

## 5. Process: the business steps in order
1. [Maker] Navigate to Dispatch Advice (11:2:00100001).
2. [Maker] Create Dispatch Advice (Warehouse, Vendor Code, refs), Save -> "Saved successfully", new Document No, grid Status In-Active / Draft [observed].
3. [Maker] Add line per product (Product + CS), save line -> "Saved Successfully!" [observed]. Switching back to Header Info blanks the header: reopen the DA from the grid by Document No before Forward [observed, friction A2-2].
4. [Maker] Optionally Add loss to a line (see da_loss_approval.md), modal row Save, **Calculate** (without it the line stays Loss 0 and Received = dispatched), then save the line [observed 2026-10-01: Dispatch 5, Loss 1, Received 4, line Save "Saved Successfully!"].
5. [Maker] Forward with comment ("Auto", then Tab) -> "Forwarded successfully"; Approval Status Pending for approval [observed].
6. [Checker] (11:5:00740001) open the same DA from the grid, Forward with comment -> "Forwarded successfully"; Status Active, Approval Status Approved, Received Date = approval day (empty until approval; set by approval) [observed 2026-10-01, DA 1356]. The net amount does not change at approval (it was already computed on the received quantity) [observed].

## 6. Outputs and effects
Approved DA: received quantities (dispatched minus loss) are added to Sound stock of the warehouse for that day (closing of 62740537 = 80 CS = DA 1350 quantity) [observed].
Live-verified 2026-10-01 (DA 1356: 62740537, dispatch 5 CS, loss 1 CS, received 4 CS): before approval Stock Inquiry for 2026-10-01 had 0 rows (No data); after approval it had exactly 1 row: 62740537 / Auto Main Warehouse / batch 1-1 / 01 - Sound, Opening 0, In 4, Out 0, Allocated 0, Closing 4 CS [observed]. So **the DA approval itself creates the day's stock row (no start-of-day step, Generate Opening Balances was not clicked)**; In = received quantity, posted to the Received Date (2026-10-01), not to the previous day (09-30 stayed unchanged: Opening 80 / In 80 / Closing 97) [observed]. The loss 1 CS created NO 02 - Damaged stock row while the loss record is Pending [observed]. Order Booking then showed ATP 4/0/0 for 62740537 = the Stock Inquiry closing [observed]. NOTE: the new row started with Opening 0 although 62740537 closed 09-30 with 97 CS: previous-day stock is not carried by the DA approval [observed; carry-over mechanism unknown]. Net amount = sum of line amounts after loss (PKR 1,632,119.522 for DA 1350) [observed]. Document number goes on via REPO_DOCUMENTNO [atlas].

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| (new) | Save | Draft, grid Status In-Active (header showed Un-Authorized right after save) | Maker | observed |
| Draft | Forward | Pending for approval | Maker | observed |
| Pending | Forward (approve) | Approved, Status Active | Checker | observed |
| Pending | Reject | Rejected | Checker | db (workflow DA: Draft, Pending for approval, Approved, Rejected, Terminated) |
| any | Terminate | Terminated | unknown | db / unknown actor |
| Draft | Delete | deleted | Maker | inferred (flow 00100002 "DA Delete Negative") |

## 8. Rules and validations
- A DA with no product line cannot be forwarded: toast "Detail is not available", DA stays Draft [observed, DA 1351].
- Forward needs a comment, otherwise "Please add comments" [observed].
- Warehouse and Vendor Code mandatory [atlas].
- A checker user cannot create a DA (authorization) [observed].
- Received = dispatched - loss (70 sent, loss 6, received 64; live 2026-10-01: 5 - 1 = 4) [observed].
- **Duplicate SO Number is allowed**: DA 1353 and 1354 both saved with SO Number LEARN_SO_01, no warning, no refusal [observed 2026-10-01]. **SO Number is optional**: DA 1355 saved with it empty [observed].
- **A silent Save (no toast, no Document No, form unchanged, only an inline DevExtreme invalid overlay) means a mandatory field is missing, in practice DA Type empty after Add** [observed 2026-10-01].
- Closing the loss modal with the x discards the loss; Calculate is required to put it on the line [observed].
- The maker's Forward creates NO loss record; it is created when the checker approves the DA (see da_loss_approval.md) [observed].
- Correction 2026-10-01: earlier text said duplicate SO Number was untested; it is allowed.

## 9. Messages
"Saved successfully" (header); "Saved Successfully!" (line); "Forwarded successfully"; "Please add comments"; "Detail is not available"; "Current user is not authorized to save this record!". The loss-modal row save shows no toast, but picking the stock type in the modal raises "Reason Type is required" before the reason is chosen (the row still saves) [observed 2026-10-01]. Silent Save with a missing mandatory field: no message at all [observed].

## 10. Dependencies
Reads warehouse, vendor, product master. Hands to: DA Loss Approval (record created when losses exist), Stock Inquiry, and Order Booking / Allocation / GIN (need Sound stock for the same calendar day). Stock is keyed by day: see stock_inquiry_and_balances.md. Live-verified 2026-10-01: stock posts to the Received Date (day of approval). Orders and GIN are covered by the orders/delivery analyst's pages.

## 11. Test design hints
- Positive: one line; four lines; with and without loss; Forward then approve by the checker; approved Received Date = today.
- Negative: forward with no line; forward without comment; checker creates DA; save without Warehouse or Vendor; Reject path; Delete a Draft; same user approves own DA (expect a deviation note).
- Boundary: loss = whole line (received 0); loss greater than quantity; CS 0 / negative / very large.
- Positive (live-verified): two DAs with the same SO Number both save; a DA with empty SO Number saves. Negative: Save with DA Type empty is silent (assert that no Document No appears), loss modal closed with x leaves the line Loss 0.
- Stock check after approval: assert Stock Inquiry for the Received Date has a row for the product with In = received; use the before/after change.
- Traps: a green save toast does not prove stock; verify via Stock Inquiry using a before/after change, not In = quantity on a busy day. Grid filter "570" also matches other numbers; check row 1.

## 12. Open questions
Q: Is a different approver enforced by the app? | Default: no, keep as QA rule | Evidence: KPO_mp approved own DA 570; the GIN workflow declares Verify and Approve for the same role.
Q: What exactly do Terminate and Reject do and can a Draft be deleted? | Default: Reject -> Rejected; Delete allowed for Draft only | Evidence: inactive flows, not replayed (checklist L13 NOT DONE).
Q: How do DA Against Purchase Order and Dispatch Advice Auto differ? | Default: out of scope | Evidence: not replayed.
ANSWERED 2026-10-01 (Q04): duplicate SO Number does not block save; SO Number is optional [observed, DA 1353-1355].
ANSWERED 2026-10-01 (BA1 part): the DA approval creates the day's stock row; no start-of-day step is needed for received products [observed, DA 1356].

## 13. Sources
runs/PILOT-DA-GIN/20260930-1615/exec/learning_block2a.json, learning_block3a.json, learning_block3b.json (live 2026-10-01); LIVE_FINDINGS.md; framework_atlas/flows/00100001.md, 00740001.md, 00100002.md, 00740002.md; framework_flows/DISPATCH_ADVICE.md, TC-DA-01_executed.md; runs/PILOT-DA-GIN/20260930-1615/friction.md, PILOT_REPORT.md; DB snd_pr_dot_documenttype, wkf_wf_wfs_workflow_status, wkf_wf_weo_wrkflw_event_orga, snd_tr_stm_stock_master/detail (names only); step_labels.json.
