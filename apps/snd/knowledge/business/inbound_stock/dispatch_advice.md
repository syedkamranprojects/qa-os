---
option: Dispatch Advice
area: inbound_stock
doc_types: [DA-01]
screens: [DYL_201068]
framework_flows: ["00100001", "00740001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: []
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-08
---

# Dispatch Advice (DA): how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]** seen live, **[db]** declared by the DB or framework tables, **[inferred]** concluded by Claude, **[unknown]** not determinable yet.
Updated: 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)
Last updated: 2026-10-01 (G11-1 consolidation). Source flows: 00100001 (group 11 seq 2), 00740001 (seq 5); inactive 00100002 (negative/delete), 00740002 (reject). G11-1 learning walk: DA **1358** created, forwarded and approved.
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.
Updated 2026-10-08: merged the QA team's written answers to the 2026-10-06 review (learning_sessions/2026-10-06_G11-PK_QA_Team_Review.docx); evidence learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx). Tag [stated 2026-10-08 QA Team] = written answer of the QA team. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08: ...)".

## 1. Purpose
A Dispatch Advice is the distributor's record that a vendor (the company supply point "UPL WH") has dispatched goods to the distributor's warehouse. When it is approved, the quantities RECEIVED become stock in that warehouse, so orders can later be allocated and issued (GIN). It is the first business step of the Daily Cycle: nothing can be sold until a DA is approved [observed: before DA 1356 was approved on 2026-10-01 every product pick in Order Booking answered "Stock not available."; after approval 62740537 became orderable]. Next: DA Loss Approval, then Stock Inquiry (see da_loss_approval.md, stock_inquiry_and_balances.md).
- Confirmed in the G11-1 walk: after DA 1358 was approved, Order Booking ATP for its five products equalled the Stock Inquiry closing that included the DA's received quantities (orders see stock received today) [observed 2026-10-01 G11-1].
- G11-2: confirmed on a second day (DA 1359, 2026-10-05): identical inputs gave identical amounts (net 2,227,455.842, prices unchanged over four days) and the received stock fed Order Booking ATP the same day [observed 2026-10-05 G11-2].

## 2. Actors and roles
- Maker = Auto_Multi_Orga (creates, adds lines and losses, Forward) [observed]. Auto_Tssm cannot create a DA: "Current user is not authorized to save this record!" [observed].
- Checker = Auto_Tssm (same screen, Forward = approve; Reject is the alternative) [observed].
- The app did NOT stop KPO_mp from approving its own DA 570 [observed]; "maker and checker differ" is a QA/framework rule, not a proven app control [inferred].
- Live-verified 2026-10-01: DA 1356 was created and forwarded by Auto_Multi_Orga and approved by Auto_Tssm (Forward with comment "Auto" -> "Forwarded successfully") [observed]. Self-approval was not tried again.
- G11-1 (DA 1358): Maker Auto_Multi_Orga created and forwarded; Checker Auto_Tssm approved with Forward, comment "Automation Approval" -> "Forwarded successfully" [observed 2026-10-01 G11-1].
- **On the Pending DA the Maker still has Forward and Reject enabled (Add also)**; not clicked. On the GIN the same day the Maker's Forward/Reject were disabled on a Pending document. So the screen does not block the Maker from approving or rejecting his own DA (possible defect; Q-DA1) [observed 2026-10-01 G11-1].
- A Checker opening the screen sees a blank new-DA form with Save enabled, but cannot actually save (authorization message above) [observed 2026-10-01 G11-1]. The Checker's button set on the Pending DA is Add, Forward, Reject = the same set the Maker had [observed 2026-10-01 G11-1].
- After login Auto_Tssm landed directly on the menu (no Company / Distributor pages) [observed 2026-10-01 G11-1; cause unknown].
- G11-2 (DA 1359): Maker Auto_Multi_Orga created and forwarded; Checker Auto_Tssm approved with Forward ("Forwarded successfully"); confirmed on a second day [observed 2026-10-05 G11-2]. Q-DA1 (Maker buttons on his own Pending DA) not re-checked.
- QA team 2026-10-08 (BA2, roles and workflow) [stated 2026-10-08 QA Team]: the application roles are **0001 NG User** (Distributor User: Back Office, creates and submits transactions and setup changes; Authorized flag N in Profile), **0002 TSSM** (Authorizer: reviews and approves what 0001 submits), **0003 DSR/PJP** (Mobile User, Authorized N), **0004 Warehouse User** (mobile: Dispatch Advice, inventory management, verification, GIN, GRN, inventory audit; Authorized N) and **9999 HQ (Global)** (setup and activities without approval; bypasses the standard workflow). In R1 a **two-level approval** (submit, approve) is configured for transactions and setup screens; each setup and transaction has a predefined workflow that names the role codes of its Submit and Approve stages. So maker / checker separation is enforced **by role through the workflow**, not by comparing user names. Open detail (Q-RL1): KPO_mp approved its own DA 570 and the org 010104 GIN workflow names role 0005 for both Verify and Approve [observed / db], which does not match the 0001 / 0002 picture.

## 3. Documents and master data
- Document type DA-01 "Dispatch Advice" (also DA, DA-05 "Dispatch Advice Auto") [db snd_pr_dot_documenttype]. Header table snd_tr_stm_stock_master, lines snd_tr_stm_stock_detail [db]. Document No is a plain number (570, 1350, 1351, 1352) shown in DOCUMENTNO after save [observed]. G11-1: Document No 1358 [observed 2026-10-01 G11-1].
- Master data: Warehouse (e.g. C0000000055-Auto Main Warehouse; default offered was 0000000025-IBT Main warehouse), Vendor Code (UPL WH, default), Products (62740537, 20050310, 62690363, 20050308), stock type Sound, batch 1-1 [observed]. DA Type options: Dispatch Advice, DA Against Purchase Order, Dispatch Advice Auto [observed].
- Warehouse list has 45 warehouses (IBT Main, Auto Main C0000000055, about 41 named "Automation", SAN Warehouse A/B) [observed 2026-10-01 G11-1].
- Cycle products of DA 1358: 62740537 RAFHAN SLPC OILS CORN TIN 2X10L, 20050310 BLUEBAND MARGARINE 16X500G, 62690363 SURF EXCEL HS 204X35G, 20050308 BLUE BAND MARGARINE 32X250G, 69997598 KNORR CKN CUBE 288X18G [observed 2026-10-01 G11-1].
- **The price in the product label is not always the purchase price**: 20050310 label 31.25, Purchase Price / PC 33.79; 62690363 label has no price, purchase price 15.45; 62740537 7711.47 in both [observed 2026-10-01 G11-1]. The DA purchase price also differs from the selling trade price seen in Order Booking (e.g. 20050308 purchase 118.9316 / PC vs trade 87.6816; purchase > trade for some SKUs: price-master observation) [observed 2026-10-01 G11-1].
- Purchase price is held with 8 decimals (e.g. 7711.46500000), shown rounded to 2; amounts use the precise price [observed 2026-10-01 G11-1].
- G11-2: Document No **1359** (serial +1 vs 1358) [observed 2026-10-05 G11-2].

## 4. Inputs: screens and fields
Menu Transaction > Primary Sale > Dispatch Advice (layout 201068, DYL_201068); tabs Header Info / Dispatch Detail [observed]. The menu search "Dispatch Advice" also offers "Dispatch Advice NUP" and "Dispatch Advice II" [observed 2026-10-01 G11-1].
- Live 2026-10-01 (cycle DA 1357, four lines 62740537 CS 80, 20050310 CS 70, 62690363 CS 60, 20050308 CS 50, no loss, net PKR 1,651,126.412): typing the quantity right after the product pick, before stock type and batch have filled, leaves the quantity empty and the line save answers "The lost quantity does not equal the sum of dispatch and received quantities" (nothing saved); a new line is always row index 0 (rowEditBtn_Save_0); the product option list sometimes detaches (re-type the product) [observed].
- Header (mandatory *): Warehouse*, Vendor Code*, **DA Type*** (options Dispatch Advice, DA Against Purchase Order, Dispatch Advice Auto; a silent Save means it is empty) [observed 2026-10-01], SO Number (optional, not unique), Shipment No, Deliver No, Invoice Due Date, Tax Invoice Number, Comments, Reference Date, Reference No, Truck No, VAT Challan Number, Invoice Number; DOCUMENTNO read-only [atlas 001001]. Dates default to today [observed]. A fresh screen defaults DA Type = Dispatch Advice and Vendor = UPL WH, but after pressing **Add** for a second DA the form resets with Warehouse, Vendor Code AND DA Type empty: pick all three before Save [observed 2026-10-01]. Extra live fields: Document Date, Tax, Discount, Net Amount, Document Status, Stock Arrival, Status, Approval Status [observed].
- Fresh-screen defaults (G11-1): Document No (read-only, generated), Document Date (read-only, today), Warehouse = 0000000025-IBT Main warehouse (not Auto Main), Vendor Code = UPL WH, DA Type = Dispatch Advice, Invoice Due Date = Reference Date = today, Stock Arrival = now (date-time), Document Status Un-Authorized, Status In-Active, Approval Status Draft; Received Date read-only and empty [observed 2026-10-01 G11-1].
- Values entered for DA 1358: Warehouse C0000000055-Auto Main Warehouse, SO Automation_01-10-2026, Shipment 123, Deliver 12312, Tax Invoice 123, Comments Positive_QA_Learning_01, Reference No 1115 [observed 2026-10-01 G11-1].
- After header Save: Add / Update / Delete / Forward enabled, Save / Reject disabled; Forward is enabled even with zero lines [observed 2026-10-01 G11-1].
- Lines (Dispatch Detail, empty until the header is saved): Product (type-ahead), Stock Type, Batch, CS; Stock Type and Batch fill by themselves AFTER the product pick and then RESET the quantity, so enter CS after the product and Tab [observed 2026-10-01]. Line Save/Edit links are anchors: scroll them into view before clicking (else "element not interactable") [observed]. Loss "+" (in the Loss cell while the row is in edit mode) opens modal "DA Loss Details": Stock, Loss Reason, CS; modal row Save; the Calculate button (CalculateBtn) is what pushes the loss to the line; closing the modal with the x DISCARDS the loss [observed 2026-10-01].
- Dispatch Detail tab (G11-1): repeats the header summary (DA No, DA Date, Reference No, Tax Invoice Number, Invoice Number); grid "DA Detail" with "+" to add a line; a new line is inserted at the TOP. Columns: Product, Stock Type, Batch, Purchase Price / PC, Dispatch CS/DZ/PC, Loss (+), Received CS/DZ/PC, Gross Amount, Discount, Tax Amount, Net Amount, Picked By [observed 2026-10-01 G11-1].
- Product type-ahead shows "code-description-price"; picking it fills Stock Type = Sound, Batch = 1-1 and Purchase Price / PC [observed 2026-10-01 G11-1].
- "DA Loss Details" window: own grid Stock / Loss Reason / CS / DZ / PC, "+" to add, row Save / Cancel (no message), **Calculate** pushes the losses to the line (upgrades the earlier observation) [observed 2026-10-01 G11-1].
- Buttons: Add, Save, Update, Delete, Forward, Reject, Terminate [step_labels]. (Superseded 2026-10-01 G11-1: no Terminate button was shown on this screen for the Checker on a Pending DA; buttons seen were Add, Save, Update, Delete, Forward, Reject.)
- Amount check screen (001010) reads Purchase Price / PC, Gross Amount, Discount, Tax Amount, Net Amount [atlas].
- Master grid: reopen a DA with Show filter row -> Document No; the grid's Warehouse column shows "Auto KARACHI" (the distributor name), not the warehouse [observed 2026-10-01 G11-1].
- G11-2: fresh-screen defaults confirmed on a second day (Warehouse 0000000025-IBT Main warehouse, Vendor UPL WH, DA Type Dispatch Advice, Document Date today). Values entered for DA 1359: Warehouse C0000000055-Auto Main Warehouse, SO Automation_05-10-2026, Shipment 123, Deliver 12312, Tax Invoice 123, Comments Positive_QA_Learning_02, Reference No 1115 [observed 2026-10-05 G11-2].

## 5. Process: the business steps in order
1. [Maker] Navigate to Dispatch Advice (11:2:00100001).
2. [Maker] Create Dispatch Advice (Warehouse, Vendor Code, refs), Save -> "Saved successfully", new Document No, grid Status In-Active / Draft [observed].
3. [Maker] Add line per product (Product + CS), save line -> "Saved Successfully!" [observed]. Switching back to Header Info blanks the header: reopen the DA from the grid by Document No before Forward [observed, friction A2-2]. (Upgraded: returning to Header Info resets the form to a blank new DA [observed 2026-10-01 G11-1] (was [observed, friction A2-2]).)
4. [Maker] Optionally Add loss to a line (see da_loss_approval.md), modal row Save, **Calculate** (without it the line stays Loss 0 and Received = dispatched), then save the line [observed 2026-10-01: Dispatch 5, Loss 1, Received 4, line Save "Saved Successfully!"].
5. [Maker] Forward with comment ("Auto", then Tab) -> "Forwarded successfully"; Approval Status Pending for approval [observed].
6. [Checker] (11:5:00740001) open the same DA from the grid, Forward with comment -> "Forwarded successfully"; Status Active, Approval Status Approved, Received Date = approval day (empty until approval; set by approval) [observed 2026-10-01, DA 1356]. The net amount does not change at approval (it was already computed on the received quantity) [observed].

G11-1 walk, DA 1358 (standard vocabulary, trace keys) [observed 2026-10-01 G11-1]:
1. [Maker] Navigate to Dispatch Advice (Transaction > Primary Sale > Dispatch Advice) (11:2:00100001).
2. [Maker] Choose Warehouse C0000000055-Auto Main Warehouse; Enter SO Number, Shipment No, Deliver No, Tax Invoice Number, Comments, Reference No; Click Save -> "Saved successfully", Document No 1358 (11:2:00100001).
3. [Maker] Open Dispatch Detail; Add line (Product, Dispatch CS); Save line -> "Saved Successfully!" (x5 products) (11:2:00100001).
4. [Maker] Add loss on lines 20050310 (Damaged 4 Area Closed + Lost 2 On Customer Behalf) and 62690363 (Damaged 5 On Customer Behalf); Click Calculate; Save line (11:2:00100001).
5. [Maker] Open DA 1358 from the grid (Document No filter); Click Forward; Enter Comments; Save -> "Forwarded successfully"; reopened: Approval Status Pending for approval (11:2:00100001).
6. [Checker] Navigate to Dispatch Advice; Open DA 1358 from the grid; Click Forward; Enter Comments "Automation Approval"; Save -> "Forwarded successfully" (11:5:00740001).
7. [Checker] Verify DA 1358: Received Date 2026-10-01, Status Active, Approval Status Approved, Document Status Authorized, Net 2,227,455.842 unchanged (11:5:00740001).

| # | Product | Disp CS | Loss | Recv CS | Net PKR |
|---|---|---|---|---|---|
| 1 | 62740537 | 80 | 0 | 80 | 1,233,834.40 |
| 2 | 20050310 | 70 | 6 (Damaged 4 Area Closed, Lost 2 On Customer Behalf) | 64 | 34,597.38 |
| 3 | 62690363 | 60 | 5 (Damaged 5 On Customer Behalf) | 55 | 173,397.25 |
| 4 | 20050308 | 50 | 0 | 50 | 190,290.50 |
| 5 | 69997598 | 40 | 0 | 40 | 595,336.32 |
DA 1358 net (header/grid) PKR 2,227,455.842, Tax 0, Discount 0 [observed 2026-10-01 G11-1].

G11-2 walk, DA 1359 (2026-10-05): same steps as DA 1358 (11:2:00100001 save + 5 lines + losses + Forward; 11:5:00740001 Checker Forward); same five lines 80 / 70 (loss 6) / 60 (loss 5) / 50 / 40 CS; line nets 1,233,834.40 / 34,597.38 / 173,397.25 / 190,290.50 / 595,336.32; DA net 2,227,455.842 [observed 2026-10-05 G11-2].
- G11-3 (2026-10-06) [observed 2026-10-06 G11-3]: [Maker] DA **1360**: Auto Main Warehouse, Vendor UPL WH, DA Type Dispatch Advice, SO Automation_06-10-2026, Shipment 123, Deliver 12312, Tax Invoice 123, Comments Positive_QA_Learning_03, Ref 1116 -> "Saved successfully" (Draft); lines 62740537 80 CS; 20050310 70 CS with loss Damaged 4 (Area Closed) + Lost 2 (On Customer Behalf) -> received 64; 62690363 60 CS loss Damaged 5 -> 55; 20050308 50; 69997598 40 (each line "Saved Successfully!"); net **2,227,455.842** (identical to 10-01 and 10-05); reopen, Forward "Automation Approval" -> "Forwarded successfully" -> In-Active / Pending. [Checker] Forward -> "Forwarded successfully" -> Active / Approved (11:02:00100001, 11:05:00740001).

## 6. Outputs and effects
Approved DA: received quantities (dispatched minus loss) are added to Sound stock of the warehouse for that day (closing of 62740537 = 80 CS = DA 1350 quantity) [observed].
Live-verified 2026-10-01 (DA 1356: 62740537, dispatch 5 CS, loss 1 CS, received 4 CS): before approval Stock Inquiry for 2026-10-01 had 0 rows (No data); after approval it had exactly 1 row: 62740537 / Auto Main Warehouse / batch 1-1 / 01 - Sound, Opening 0, In 4, Out 0, Allocated 0, Closing 4 CS [observed]. So **the DA approval itself creates the day's stock row (no start-of-day step, Generate Opening Balances was not clicked)**; In = received quantity, posted to the Received Date (2026-10-01), not to the previous day (09-30 stayed unchanged: Opening 80 / In 80 / Closing 97) [observed]. The loss 1 CS created NO 02 - Damaged stock row while the loss record is Pending [observed]. Order Booking then showed ATP 4/0/0 for 62740537 = the Stock Inquiry closing [observed]. NOTE: the new row started with Opening 0 although 62740537 closed 09-30 with 97 CS: previous-day stock is not carried by the DA approval [observed; carry-over mechanism unknown] (superseded 2026-10-01 G11-1: by 16:4x the same day's rows had Opening balances, 62740537 Opening 160 = 09-30 closing 97 + 09-30 allocated 63; who or what generated them is open, Q-OB1; the DA approval itself still only adds In). Net amount = sum of line amounts after loss (PKR 1,632,119.522 for DA 1350) [observed]. Document number goes on via REPO_DOCUMENTNO [atlas].
- G11-1, DA 1358 approval (Stock Inquiry 2026-10-01, Auto Main Warehouse, 01 - Sound, before -> after): 62740537 In 84 -> 164 (+80), 20050310 In 70 -> 134 (+64 = 70 - 6 loss), 62690363 In 60 -> 115 (+55 = 60 - 5), 20050308 In 50 -> 100 (+50), 69997598 In 0 -> 40 (+40); Closing rose by the same amounts; row count unchanged (39). **The DA approval adds exactly the RECEIVED quantity to Sound In and Closing on the Received Date** (was [observed] on one-line DAs; now confirmed on a five-line DA with losses) [observed 2026-10-01 G11-1].
- The approval created ONE loss record (Serial 639) for the DA's three loss rows; the approved loss created no Damaged/Lost stock row (see da_loss_approval.md) [observed 2026-10-01 G11-1].
- Line amounts: Gross = Received qty (in PC) x Purchase Price / PC; Discount 0, Tax 0, Net = Gross on every line; amounts are recomputed on Received after Calculate [observed 2026-10-01 G11-1].
- After approval all fields are read-only and only Add is enabled [observed 2026-10-01 G11-1].
- G11-2 (supersedes the note above that previous-day stock is not carried): on 2026-10-05 the approval of DA 1359 was the first movement of the day and created ALL 39 stock rows with Opening = previous Closing + still-Allocated (62740537 Opening 308), then added the received quantities as In (+80 / +64 / +55 / +50 / +40) [observed 2026-10-05 G11-2]. See stock_inquiry_and_balances.md (new-day rule, Q-OB2 for the 10-01 difference).
- G11-2: the approval created loss record **640** (one per DA, serial +1) [observed 2026-10-05 G11-2].
- G11-3: DA approval posted In = received quantities and created loss record 641; on 10-06 the day's stock rows were only these 5, Opening 0 (see stock_inquiry_and_balances.md, Q-OB2) [observed 2026-10-06 G11-3].

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| (new) | Save | Draft, grid Status In-Active (header showed Un-Authorized right after save) | Maker | observed |
| Draft | Forward | Pending for approval | Maker | observed (G11-1: the form keeps showing Draft until reopened; reopened: Status In-Active, Approval Status Pending for approval, Document Status Un-Authorized, Received Date empty) [observed 2026-10-01 G11-1] |
| Pending | Forward (approve) | Approved, Status Active | Checker | observed (G11-1: also Document Status Authorized, Received Date set) [observed 2026-10-01 G11-1] |
| Pending | Reject | Rejected | Checker | db (workflow DA: Draft, Pending for approval, Approved, Rejected, Terminated) |
| Pending | Forward / Reject (buttons enabled, not clicked) | unknown | Maker | observed 2026-10-01 G11-1 (Q-DA1) |
| any | Terminate | Terminated | unknown | db / unknown actor (no Terminate button seen on the screen, G11-1) |
| Draft | Delete | deleted | Maker | inferred (flow 00100002 "DA Delete Negative") |

## 8. Rules and validations
- A DA with no product line cannot be forwarded: toast "Detail is not available", DA stays Draft [observed, DA 1351]. Note: the Forward button itself is enabled with zero lines; the refusal comes at Forward [observed 2026-10-01 G11-1].
- Forward needs a comment, otherwise "Please add comments" [observed]. The Forward "Comments" window has a mandatory text [observed 2026-10-01 G11-1].
- Warehouse and Vendor Code mandatory [atlas]. (Upgraded: Warehouse*, Vendor Code*, DA Type* marked mandatory on screen [observed 2026-10-01 G11-1] (was [atlas]).)
- A checker user cannot create a DA (authorization) [observed].
- Received = dispatched - loss (70 sent, loss 6, received 64; live 2026-10-01: 5 - 1 = 4) [observed]. G11-1: 70 - 6 = 64, 60 - 5 = 55 [observed 2026-10-01 G11-1].
- Several loss rows on one line are summed into one Loss figure (4 Damaged + 2 Lost = 6-0-0) [observed 2026-10-01 G11-1].
- Gross = Received qty in PC x Purchase Price / PC (8-decimal price); Discount and Tax 0 on a DA [observed 2026-10-01 G11-1].
- **Duplicate SO Number is allowed**: DA 1353 and 1354 both saved with SO Number LEARN_SO_01, no warning, no refusal [observed 2026-10-01]. **SO Number is optional**: DA 1355 saved with it empty [observed].
- **A silent Save (no toast, no Document No, form unchanged, only an inline DevExtreme invalid overlay) means a mandatory field is missing, in practice DA Type empty after Add** [observed 2026-10-01].
- Closing the loss modal with the x discards the loss; Calculate is required to put it on the line [observed].
- The maker's Forward creates NO loss record; it is created when the checker approves the DA (see da_loss_approval.md) [observed]. G11-1: one loss record per DA, created at approval (Serial 638 -> 639) [observed 2026-10-01 G11-1].
- Correction 2026-10-01: earlier text said duplicate SO Number was untested; it is allowed.
- The app does not stop the Maker from acting on his own Pending DA (Forward / Reject enabled for him) [observed 2026-10-01 G11-1; Q-DA1].
- G11-2: amounts are reproducible: the same lines on 2026-10-01 and 2026-10-05 gave the same line and DA totals [observed 2026-10-05 G11-2].
- G11-3 gotchas: quantity cells need focus and single key presses; the line Save link is off-screen to the right (scroll it into view); the loss Stock list has two "Lost" entries (use the first, Q-LA3) [observed 2026-10-06 G11-3].

## 9. Messages
"Saved successfully" (header); "Saved Successfully!" (line); "Forwarded successfully"; "Please add comments"; "Detail is not available"; "Current user is not authorized to save this record!". The loss-modal row save shows no toast, but picking the stock type in the modal raises "Reason Type is required" before the reason is chosen (the row still saves) [observed 2026-10-01]. Silent Save with a missing mandatory field: no message at all [observed].
- G11-1 confirmations: header Save -> "Saved successfully"; line Save -> "Saved Successfully!" (capital S, exclamation; differs from the header text); Maker Forward and Checker Forward -> "Forwarded successfully"; loss-window row Save/Cancel -> no message [observed 2026-10-01 G11-1].
- G11-2: "Saved successfully" (header), "Saved Successfully!" (each line), "Forwarded successfully" (Maker and Checker) confirmed on a second day [observed 2026-10-05 G11-2].

## 10. Dependencies
Reads warehouse, vendor, product master. Hands to: DA Loss Approval (record created when losses exist), Stock Inquiry, and Order Booking / Allocation / GIN (need Sound stock for the same calendar day). Stock is keyed by day: see stock_inquiry_and_balances.md. Live-verified 2026-10-01: stock posts to the Received Date (day of approval). Orders and GIN are covered by the orders/delivery analyst's pages.
- G11-1: the first successful GIN approval of the replay (GIN 506) was possible because DA 1358 was approved the SAME day; the received stock fed Order Booking ATP and the GIN [observed 2026-10-01 G11-1].
- G11-2: the DA approval is also the step that opens the stock day (creates all rows with carried Openings) when it is the first movement of the day [observed 2026-10-05 G11-2].

## 11. Test design hints
- Positive: one line; four lines; with and without loss; Forward then approve by the checker; approved Received Date = today.
- Negative: forward with no line; forward without comment; checker creates DA; save without Warehouse or Vendor; Reject path; Delete a Draft; same user approves own DA (expect a deviation note).
- Boundary: loss = whole line (received 0); loss greater than quantity; CS 0 / negative / very large.
- Positive (live-verified): two DAs with the same SO Number both save; a DA with empty SO Number saves. Negative: Save with DA Type empty is silent (assert that no Document No appears), loss modal closed with x leaves the line Loss 0.
- Stock check after approval: assert Stock Inquiry for the Received Date has a row for the product with In = received; use the before/after change.
- Traps: a green save toast does not prove stock; verify via Stock Inquiry using a before/after change, not In = quantity on a busy day. Grid filter "570" also matches other numbers; check row 1.
- G11-1 additions [observed 2026-10-01 G11-1]:
  - Positive: five-line DA with two loss types on one line; assert In delta per product = Dispatch - Loss (80/64/55/50/40), not the dispatched quantity.
  - Positive: line Net = Received PC x Purchase Price / PC using the 8-decimal price; do not compute from the price in the product label (it can differ or be missing).
  - Negative: Maker opens his own Pending DA: Forward/Reject should be disabled (today they are enabled -> expect a defect/deviation, Q-DA1). Checker clicks Save on the blank form -> "Current user is not authorized to save this record!".
  - Negative: Forward with zero lines -> "Detail is not available" although the button is enabled.
  - Boundary: the warehouse default is IBT Main warehouse, not Auto Main; a test that does not pick the warehouse posts stock to the wrong warehouse.
  - Traps: the grid's Warehouse column shows the distributor name (Auto KARACHI), so do not assert the warehouse from the grid; after Forward the open form still shows Draft until reopened; message texts differ in case and punctuation between header ("Saved successfully") and line ("Saved Successfully!").
- G11-2 additions [observed 2026-10-05 G11-2]:
  - Positive (regression): the same five-line DA must give the same amounts on any day while prices are unchanged (2,227,455.842 on 10-01 and 10-05); a difference signals a price-master change.
  - Positive (new day): if the DA approval is the first movement of the day, assert the day's rows appear with carried Openings, then In delta = received.
  - Trap: on 10-05 the framework's absolute check (seq 9 In 80) passed only because DA 1359 was the day's only receipt.

## 12. Open questions
Q: Is a different approver enforced by the app? | Default: no, keep as QA rule | Evidence: KPO_mp approved own DA 570; the GIN workflow declares Verify and Approve for the same role. (G11-1 adds: the Maker keeps Forward/Reject enabled on his own Pending DA 1358; see Q-DA1.)
Q: What exactly do Terminate and Reject do and can a Draft be deleted? | Default: Reject -> Rejected; Delete allowed for Draft only | Evidence: inactive flows, not replayed (checklist L13 NOT DONE).
Q: How do DA Against Purchase Order and Dispatch Advice Auto differ? | Default: out of scope | Evidence: not replayed.
ANSWERED 2026-10-01 (Q04): duplicate SO Number does not block save; SO Number is optional [observed, DA 1353-1355].
ANSWERED 2026-10-01 (BA1 part): the DA approval creates the day's stock row; no start-of-day step is needed for received products [observed, DA 1356].
Q-DA1: May the Maker approve or reject his own Pending Dispatch Advice (Forward/Reject stay enabled for him)? | Default: must not (QA convention); possible defect | Class: C | Evidence: DA 1358 Pending, Maker buttons Forward/Reject/Add enabled; on GIN 506 the Maker's Forward/Reject were disabled [observed 2026-10-01 G11-1].
Q-DA2: What are "Dispatch Advice NUP" and "Dispatch Advice II" in the menu, and are they in scope? | Default: out of scope; only "Dispatch Advice" is tested | Class: A | Evidence: menu search results only [observed 2026-10-01 G11-1].
Q-DA3: Why does the product label price differ from the Purchase Price / PC (and purchase exceed trade price for some SKUs)? | Default: label shows another price list; assert amounts on Purchase Price / PC only | Class: C | Evidence: 20050310 label 31.25 vs purchase 33.79; 20050308 purchase 118.93 vs trade 87.68 [observed 2026-10-01 G11-1].
- G11-2 (2026-10-05): no change to Q-DA1/Q-DA2/Q-DA3; Q-DA1 is merged into BA2 in OPEN_QUESTIONS.md (self-approval).
- **BA2 ANSWERED 2026-10-08** [stated 2026-10-08 QA Team]: separation of duty is by role and workflow (0001 NG User submits, Authorized N; 0002 TSSM approves; two-level approval in R1; 9999 HQ bypasses the workflow). New Q-RL1 (class B): which role codes the cnr1dev1 users hold and why KPO_mp could approve his own DA 570.

## 13. Sources
runs/PILOT-DA-GIN/20260930-1615/exec/learning_block2a.json, learning_block3a.json, learning_block3b.json (live 2026-10-01); LIVE_FINDINGS.md; framework_atlas/flows/00100001.md, 00740001.md, 00100002.md, 00740002.md; framework_flows/DISPATCH_ADVICE.md, TC-DA-01_executed.md; runs/PILOT-DA-GIN/20260930-1615/friction.md, PILOT_REPORT.md; DB snd_pr_dot_documenttype, wkf_wf_wfs_workflow_status, wkf_wf_weo_wrkflw_event_orga, snd_tr_stm_stock_master/detail (names only); step_labels.json.
- G11-1 learning walk: learning_sessions/2026-10-01_G11-PK_session1_log.md (seq 2, seq 5, Stock Inquiry before/after, seq 9) and learning_sessions/2026-10-01_G11-PK_session1_report.md (§3 rule 1, §6 defect 1, §8 Q-DA1).
- G11-2: learning_sessions/2026-10-05_G11-PK_session2_log.md (seq 2, 5, 9).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 2, 5).

- QA team written answers 2026-10-08: learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx) (BA2).
