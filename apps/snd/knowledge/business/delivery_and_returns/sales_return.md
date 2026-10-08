---
option: Sales Return
area: delivery_and_returns
doc_types: [CM-02]
screens: [DYL_201801, SALESRETURNVIEW, SALESRETURN-STATUSCHANGE]
framework_flows: ["00070001", "00700001", "00730001", "00710001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [cashmemo_reschedule_and_status, goods_issue_note]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-08
---
# Sales Return: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (consolidated with learning session 1 LEARN-G11-PK/20261001-1611, seq 34/36/37/38)
Last updated: 2026-10-01. Source flows: atlas `00070001` (group 11 seq 34 Sales Return), `00700001` (seq 36 Sales Return View), `00730001` (seq 37 Sales Return View Approval), `00710001` (seq 38 Sales Return Status Change). Not yet replayed live. (superseded 2026-10-01: all four walked live; return **COL26000000713** against cash memo COL26000002003, 2 CS of 62740537, reason No Cash, forwarded, approved and picked [observed 2026-10-01 G11-1]) Goods Return Note (seq 48-49) is in the inbound-stock pages.
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.
Updated 2026-10-08: merged the QA team's written answers to the 2026-10-06 review (learning_sessions/2026-10-06_G11-PK_QA_Team_Review.docx); evidence learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx). Tag [stated 2026-10-08 QA Team] = written answer of the QA team. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08: ...)".

## 1. Purpose
A sales return records goods an outlet gives back after delivery (rejected, damaged, wrong, price dispute). It reverses part of a delivered cash memo: the returned quantities and amount are authorised by a checker and later picked up and received into the warehouse. [inferred from document types and names; confirmed 2026-10-01: created only from a delivered cash memo, approved by the Checker, picked by the Maker, and the returned quantity came back into warehouse stock on the Goods Return Note [observed 2026-10-01 G11-1]]
- G11-2/2b: confirmed on a second day (return **COL26000000714** against COL26000002009, 2 CS of 62740537, reason No Cash); after the pick Transaction Inquiry lists it as a Sales Return with Demand Channel "Partial Return" and status Picked [observed 2026-10-05 G11-2, G11-2b].
- QA team 2026-10-08 (Q-SR2, Q-GRN2): a **Sales Return** is generated against a **previously dated invoice** (with reference to the old cash memo); it can return **Sound, Damaged and Expired** stock; the returned quantity is valued at product sale price x returned quantity (UOM) with the applicable discount (amount-based or free-product scheme) and tax defined in the Batch Setup; one product or the complete invoice may be returned [stated 2026-10-08 QA Team].
- QA team 2026-10-08: a **Fresh Return** follows the same calculation; the only difference is that it uses the **current document date** (modification of current-order quantities) [stated 2026-10-08 QA Team]; it is used in **Bangladesh**, not in Pakistan [stated 2026-10-08 QA Team].

## 2. Actors and roles
Maker: `Auto_Multi_Orga` creates (seq 34) and views/forwards (36). Checker: `Auto_Tssm` approves (37, switch point). Back to `Auto_Multi_Orga` for the status change (38) [atlas]. Workflow `SalesReturnApproval` (event `SR`) [db: wkf_wf_weo_wrkflw_event_orga]; a separate `SRWithoutReferenceApproval` exists for returns without a cash memo [db].
- Confirmed 2026-10-01: Maker creates and forwards, Checker approves on the same Sales Return View screen with the same Forward button, Maker then saves the pick [observed 2026-10-01 G11-1]. Same maker-checker pattern as DA, GIN and GRN [observed 2026-10-01 G11-1].
- PJP visibility differs by user: on Sales Return View the Maker's PJP list shows delivery PJPs only, the **Checker sees all 13 PJPs** (booking and delivery) [observed 2026-10-01 G11-1].
- G11-2: Maker Auto_Multi_Orga saved and forwarded; Checker Auto_Tssm approved on the same Sales Return View screen with the same Forward button (approval = different user); the Checker's PJP list showed all 13 PJPs [observed 2026-10-05 G11-2].

## 3. Documents and master data
- Document type `CM-02` "Sales Return" (nature SR), stored in the cash memo tables (`snd_tr_cmm_cashmemo_master`, reference to the original cash memo `tcmm_ref_docno`) [db]. Statuses: 01 Authorized, 02 Un-Authorized, 03 Cancelled, 04 Picked [db: snd_pr_dos_documentstatus CM-02]. Related: `CM-04` Fresh Sales Return, `CM-07` Sales Return Without Reference, `CM-08` Customer Account Closed, `CRN-02` Credit Note (Sales Return) [db: snd_pr_dot_documenttype].
- **Own number series**: the return got its own number **COL26000000713** (the source cash memo is COL26000002003), shown in Sales Return View as Document No. with the source in **Principle Invoice** [observed 2026-10-01 G11-1].
- Return reasons by document type CM-02 (for example Item Out of Stock/No Substitute, Short of Cash, Area Closed, Price Difference) [db: glb_pr_rnt_reason_type]; the label Reason Type on screen [atlas]. Observed 2026-10-01: Reason Type options on the return line are **No Cash, Wrong Order/No Order, Shop Closed, Credit Exceeded** [observed 2026-10-01 G11-1] (differs from the DB examples; see §12).
- **Return Stock Type** options on the line (editable in edit mode): **Damaged, Expired, Lost, Sound** [observed 2026-10-01 G11-1]: a return can be booked as non-sound stock. The session used Sound.
- Menu neighbours (not walked): Sales Return Without Reference, Fresh Sales Return, Sales Return W/O Reference View / Pick, and a second "Sales Return" entry [observed 2026-10-01 G11-1].
- G11-2: return number **COL26000000714** (CM-02 series, +1 vs 713), Principle Invoice COL26000002009 [observed 2026-10-05 G11-2].

## 4. Inputs: screens and fields
- **Sales Return** (menu `Sales Return`, option DYL_201801) [atlas]: **PJP Number**, **Date From**, **Date To**, **Outlet Name** (dropdowns/dates); click the document-number header, pick the outlet row, Save. Detail tab (tab_9): per row Edit, **CS**, **PC**, **Reason Type**, row Save/Cancel; buttons Validation and Save. Result block read-only: **Gross Amount**, **Discount**, **Tax**, **Net Amount** [atlas].
  - Observed 2026-10-01: header Document No (generated), Document Date (today), **PJP Number** (delivery PJP; default the first, AutoPJGIN2), Date From / Date To (today), Outlet Name, SKU; tabs Header / Detail (Detail disabled until the header is saved); buttons Add, Save [observed 2026-10-01 G11-1].
  - Grid after choosing PJP 02112: **delivered cash memos only** (2003/2004/2005): Document No, Document Date, Delivery Date, Outlet Code, Gross, Discount, Tax, Net, **Received Amount** (0), **Balance Amount** (= Net), Demand Channel [observed 2026-10-01 G11-1].
  - Detail: per invoice line Product (code-name-price), Batch, Stock Type, Trade Price/Unit, **Invoice Quantity** CS/DZ/PC (shows the EDITED quantity, 4 CS), **Return Quantity** CS/DZ/PC, Gross Amount, **Reason Type**, Edit; buttons Validation, Forward [observed 2026-10-01 G11-1].
- **Sales Return View** (menu `Sales Return View`, option SALESRETURNVIEW): **PJP Number**, **Date From**, **Date To**, row filter Outlet Code; open the return; Forward button, comments, Save; shows Gross/Discount/Tax/Net and a row_1_status [atlas].
  - Observed 2026-10-01: filters PJP Number (delivery PJP; default the first), Date From/To (today); tabs Header / Detail; button Forward. Grid: checkbox, Document No. (return), **Principle Invoice** (source cash memo), Document Date, Delivery Date, Outlet Code, Gross, Discount, Tax, Net. Forward asks for **Comments** (mandatory) [observed 2026-10-01 G11-1].
- **Sales Return View Approval**: same screen layout for the checker; select document, Forward with comments, status checked [atlas]. Confirmed: same screen, same button, Checker user [observed 2026-10-01 G11-1].
- **Sales Return Status Change** (option SALESRETURN-STATUSCHANGE): **PJP Number**, **GIN Number** (REPO_GINNO), filter by Document Date, open the row; Validation then `savesalePick` [atlas].
  - Observed 2026-10-01: filters PJP Number (delivery PJP) and **Gin Number**, which fills by itself (GN-01~506). Grid: Document No. (return), Principle Invoice, Document Date, Delivery Date, Outlet Code, Gross, Discount, Tax, Net; it lists the APPROVED return. A single click does not open it; double-click opens the Detail tab: Product, Batch, Stock Type, Trade Price/Unit, **Order Quantity**, **Return Quantity** (editable again: the picked quantity can differ from the approved return), Gross, Reason Type, Edit. Button **"Save Sale Pick"** [observed 2026-10-01 G11-1].
- G11-2: Sales Return is the first of two "Sales Return" menu entries (Transaction > Sales Return); PJP defaults to AutoPJGIN2, choose 02112-AutomationDSR; the grid lists delivered cash memos (2009, 2010, 2011); click the row, Save; Detail per line: Invoice Qty, Return Qty, Reason Type (No Cash / Wrong Order/No Order / Shop Closed / Credit Exceeded), Stock Type (Sound) [observed 2026-10-05 G11-2].
- G11-2: Sales Return Status Change: PJP 02112-AutomationDSR, GIN fills GN-01~507; the approved return is opened with a double-click on the row; Detail, Validation, "Save Sale Pick" [observed 2026-10-05 G11-2].

## 5. Process: the business steps in order
1. [Maker] Navigate to Sales Return; Choose PJP Number, Date From, Date To, Outlet Name; open the outlet's cash memo. (11:34:00070001)
2. [Maker] Edit line: Enter CS/PC, Choose Reason Type; save the row. Expect: row message.
3. [Maker] Validate. Expect: `Validation successfully`. Gross/Discount/Tax/Net shown and compared with the workbook.
4. [Maker] Save. Expect: `Save successfully`. Return is Un-Authorized [inferred].
5. [Maker] Navigate to Sales Return View; open the return; Forward with comments. Expect: status Pending for approval (row_1_status) [atlas]; `Please Enter the Comments` if the comment is empty (11:36:00700001).
6. [Checker] Login; Sales Return View Approval; open; Forward with comments. Expect: status Approved/Authorized (11:37:00730001).
7. [Maker] Login; Sales Return Status Change; Choose PJP Number and GIN Number = GIN1; open the return; Validation; save pick. Expect: message from `SR_StatsChang_DTL_SAVE_ASSR` [unknown text]; return becomes Picked (04) [inferred] (11:38:00710001). (superseded 2026-10-01: message is `Save successfully` [observed 2026-10-01 G11-1])

Walked live 2026-10-01 (business steps in the standard vocabulary) [observed 2026-10-01 G11-1]:
8. [Maker] Navigate to Sales Return; Choose PJP Number = the delivery PJP (02112); Select the delivered cash memo; Save. Expect: `Record Saved Successfully!`; return number generated (COL26000000713); Detail tab enabled. (11:34:00070001)
9. [Maker] Go to tab Detail; Edit the line; Enter Return Quantity 2 CS; Choose Stock Type "Sound" and Reason Type "No Cash"; Save the line. Expect: Gross 30,845.86 (= workbook). (11:34:00070001)
10. [Maker] Validate. Expect: `Validation successfully`. Save. Expect: `Save successfully`; Forward enabled. Totals Gross 30,845.86, Discount 6,189.17, Tax 4,419.93, Net 29,077.00. (11:34:00070001)
11. [Maker] Navigate to Sales Return View; Choose PJP Number 02112; Select the return; Forward; Enter Comments; Save. Expect: result window "Sales Return Status" with Status `Success`. (11:36:00700001)
12. [Maker] Logout; [Checker] Login; Navigate to Sales Return View; Choose PJP Number 02112; Select the return; Forward; Enter Comments; Save. Expect: "Sales Return Status" `Success`; the return leaves the list (approved). (11:37:00730001)
13. [Checker] Logout; [Maker] Login; Navigate to Sales Return Status Change; Choose PJP Number 02112 (Gin Number fills by itself); Open the return (double-click); Validate; Save Sale Pick. Expect: `Validation successfully`, then `Save successfully`. (11:38:00710001)

G11-2 walk (2026-10-05) [observed 2026-10-05 G11-2]:
1. [Maker] Navigate to Sales Return; Choose PJP 02112-AutomationDSR; Select COL26000002009; Click Save -> "Record Saved Successfully!", return COL26000000714 (11:34:00070001).
2. [Maker] Open Detail; line 62740537 Return CS 0 -> 2, Reason Type No Cash, Stock Type Sound; Save line (Gross 30,845.86); Click Validation -> "Validation successfully"; Click Save -> "Save successfully" (11:34:00070001).
3. [Maker] Navigate to Sales Return View; Tick COL26000000714; Click Forward; Enter Comments "Automation Approval" (verify the box is filled); Save -> "Sales Return Status": COL26000000714 | Sales Return | Success (11:36:00700001).
4. [Checker] Navigate to Sales Return View; Choose PJP 02112-AutomationDSR; Tick COL26000000714; Forward with comment -> "Success" (11:37:00730001).
5. [Maker] Navigate to Sales Return Status Change; Open COL26000000714 (double-click); Click Validation -> "Validation successfully"; Click Save Sale Pick -> "Save successfully" (11:38:00710001).
G11-3 walk (2026-10-06, return COL26000000715) [observed 2026-10-06 G11-3]:
1. [Maker] Sales Return: PJP 02112 -> delivered memos 2015 / 2016 / 2020 -> select 2015 (outlet cell) -> Save -> "Record Saved Successfully!" -> 715; Detail: invoice qty 62740537 **3** CS (order edited twice); Edit -> Return 2 CS, Sound, No Cash; row Save (no toast); validation -> "Validation successfully"; Save -> "Save successfully" (11:34:00070001).
2. [Maker] Sales Return View: 02112 -> 715 (Principle Invoice COL26000002015) -> tick -> Forward 'Automation Approval' -> "Sales Return Status": 715 | Sales Return | Success (11:36:00700001).
3. [Checker] same screen -> 715 -> Forward -> Success (approved) (11:37:00730001).
4. [Maker] Sales Return Status Change: PJP 02112 (Gin Number auto-filled GN-01~507 = yesterday's GIN, list still shows 715) -> double-click 715 -> Detail (Order 3, Return 2, 30,845.86, No Cash) -> Validation -> "Validation successfully" -> Save Sale Pick -> "Save successfully" (11:38:00710001).

## 6. Outputs and effects
- A CM-02 document with returned quantities and reversed amounts linked to the delivered cash memo [db/inferred]. Confirmed: own number, Principle Invoice = the source cash memo [observed 2026-10-01 G11-1].
- On Picked, the goods are collected on the vehicle and handed to the Goods Return Note flow, which brings them back into the warehouse stock (inbound-stock pages) [inferred]. No stock moves at Save or at approval [inferred]. Confirmed 2026-10-01: the 2 CS returned were part of the 19 CS Suggested on GRN 246, and GRN approval posted them as In (Sound) [observed 2026-10-01 G11-1]. Stock was not snapshotted between return Save and the GRN, so "no stock move before the GRN" stays [inferred].
- A Credit Note (Sales Return) `CRN-02` may follow in finance [db: type exists; trigger [unknown]].
- **The approved and picked return did NOT reduce the receivable**: cash memo COL26000002003 still showed Balance Amount = Net in the deposit slips, and Route Settlement showed Adjusted Credit Note Amount 0 and Fresh Return Value 0 for the route [observed 2026-10-01 G11-1]. When it is netted is open (Q-SR1).
- Return amounts: Gross 30,845.86, Discount 6,189.17, Tax 4,419.93, Net 29,077.00; the workbook's Discount 6,169.17 / Tax 4,436.55 / Net 29,113.00 differ because the source order had been edited first (promotion and tax ratios of the smaller basket). Discount and tax are reversed proportionally [observed 2026-10-01 G11-1].
- G11-2: return totals Gross 30,845.86, Discount 6,189.17, Tax 4,419.93, Net 29,077.00 = 10-01 (confirmed on a second day) [observed 2026-10-05 G11-2].
- G11-2b (refines "discount and tax are reversed proportionally"): in Transaction Inquiry the return's line 1 (2 CS returned) carries Disc 6,407.54 / Tax -4,398.90 / Net -28,837.22, and **lines 2-5 (0 returned) carry small reversals** (20050310 disc -116.35 tax -20.94; 62690363 -61.23; 20050308 -40.31; 69997598 -0.48 / -0.09), netting to the header Discount 6,189.17. **Returning part of the order re-prices its slab promotions on the remaining basket**, so the credit is not a simple pro-rata of the returned line [observed values 2026-10-05 G11-2b; rule inferred; Q-SR2]. Total Offering of the return: Automation2 +3,084.59, MARCH001 +10, MARCH002 +3,084.59, May001 +10, May003 0. Total Tax: VAT -4,419.93, 3rd Schedule 0.
- G11-2b: **still not netted after settlement**: route 02112 for 10-05 is Complete with Adjusted Credit Note 0 and Fresh Return 0; COL26000002009 Balance 88,107 = 90,707 - 2,600 slip receipts (the 29,077 return is not deducted); return Offset 0 [observed 2026-10-05 G11-2b; Q-SR1 still open].
- G11-2: the returned 2 CS came back on GRN 247 (part of the 19 CS) [observed 2026-10-05 G11-2].
- G11-3 return 715 totals: Gross **30,845.86**, Discount 6,189.17, Tax **4,409.61**, Net **29,066.00** (10-05: Tax 4,419.93 / Net 29,077 with a 4 CS source order; workbook 6,169.17 / 4,436.55 / 29,113) [observed 2026-10-06 G11-3]. Gross and Discount equal 10-05; Tax/Net differ because the source order is 3 CS now.
- G11-3: the picked return came back on GRN 248 (17 CS = 2 return + the undelivered/cut/cancelled quantities) [observed 2026-10-06 G11-3]; not netted in Route Settlement (Q-SR1).
- G11-3: lines with 0 returned carry small re-priced discount reversals again (-182, -95.78, -63.06, -0.75) [observed 2026-10-06 G11-3] (Q-SR2).

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| (none) | Save | Un-Authorized (02) / Draft | Maker | [inferred] |
| Draft | Forward | Pending for approval (wf 02) | Maker | [atlas flow, status text [unknown]]; result `Success` [observed 2026-10-01 G11-1] |
| Pending | Forward (approve) | Authorized (01), wf 03 | Checker | [db]; result `Success`, return leaves the View list [observed 2026-10-01 G11-1] |
| Authorized | Status Change, save pick | Picked (04) | Maker | [inferred]; `Save successfully` on Save Sale Pick [observed 2026-10-01 G11-1]; status text "Picked" not read on screen |
| any | Cancel | Cancelled (03) | [unknown] | [db] |

- G11-2b: after Save Sale Pick the return reads **Picked** in Transaction Inquiry (Document Type Sales Return) [observed 2026-10-05 G11-2b] (upgrades the [inferred] Picked row above). The source cash memo stays Delivered/Invoiced [observed 2026-10-05 G11-2b].

## 8. Rules and validations
- `Return quantity should not greater than ordered quantity.` [atlas toast, 3 occurrences]: return cannot exceed what was ordered/delivered on the cash memo.
- Validation must pass before Save; comments are mandatory on Forward (`Please Enter the Comments`) [atlas, 9 occurrences]. Comments mandatory confirmed (the Comments popup) [observed 2026-10-01 G11-1].
- Reason Type mandatory per returned line [inferred].
- Approver differs from maker [atlas switch point].
- **Only delivered cash memos are offered** on Sales Return (rescheduled and cancelled ones are not) [observed 2026-10-01 G11-1].
- Invoice Quantity on the return = the delivered (edited) quantity, not the booked one (4 CS after the 7 -> 4 edit) [observed 2026-10-01 G11-1].
- The header must be saved before the Detail tab opens [observed 2026-10-01 G11-1].
- The Status Change pick quantity is editable and can differ from the approved return quantity [observed 2026-10-01 G11-1]; what happens if it does is [unknown].
- G11-2b: the return's Invoice Ref. No. = the source sales invoice; Demand Channel "Partial Return" for a part return [observed 2026-10-05 G11-2b].
- G11-2b: a part return re-prices slab promotions on non-returned lines (see section 6) [observed values; rule inferred].
- QA lead rule: always type the Forward comment and verify the textarea holds it before Save (an empty box was sent once on 10-05) [stated 2026-10-05 QA lead].
- G11-3: Invoice Qty = the delivered quantity after all edits (3 CS) [observed 2026-10-06 G11-3]. A "Partial / Full" choice is shown at the bottom of the Detail [observed 2026-10-06 G11-3].
- G11-3: Sales Return Status Change auto-fills the previous day's GIN (507) but still lists today's return [observed 2026-10-06 G11-3].
- QA team 2026-10-08 (Q-SR2, middle invoice): for a **partial return** the system generates a **middle invoice / cash memo** for the remaining quantity, recalculates price, discount/scheme and tax on it, and the Sales Return carries the **difference between the original invoice and the middle invoice** [stated 2026-10-08 QA Team]. This explains the reversals on non-returned lines (slab promotions re-priced on the remaining basket) [observed 2026-10-05, 2026-10-06]; supersedes the [inferred] rule wording.
- QA team 2026-10-08 (Q-SR1, partly): credit notes are adjusted at outlet level, applied where the invoice net amount > the credit note amount [stated 2026-10-08 QA Team]; still not observed for returns 713 / 714 / 715.
- Promotions training 2026-10-07 (F20, F22): a return gives the promotion amount back to the budget; a **full return** gives it back in full, a **partial return** only the part attributable to the returned allocation [stated 2026-10-07 Syed Zulfiqar]. How this fits the middle-invoice re-pricing (Q-SR2 answer, reversals on non-returned lines) is open: contradiction 33 / Q-PR10 in OPEN_QUESTIONS.md; see [promotions_and_budget.md](../promotions_and_budget/promotions_and_budget.md).
- Code study 2026-10-08 (promotion service, not observed): a return re-evaluates **only the original promotion codes** S&D passes, on whatever lines S&D sends (criteria, dates and exclusivity skipped), and books no budget on the return event; the give-back amount is **supplied by S&D** through `/promotionAllocation/adjust` or `/revert` (contradictions 33, 38; Q-PR11, L52) [code UL-R1-BD@51e7e815 PromotionExecutor.java:80-87] [code UL-R1-BD@51e7e815 PromotionBudget.java:382-410] [code UL-R1-BD@51e7e815 PromotionAllocationRevertService.java:266-327]. <!--i-->

## 9. Messages
`Validation successfully`; `Save successfully`; `Forwarded successfully` (8 times on the detail screen); `Return quantity should not greater than ordered quantity.`; `Please Enter the Comments` [atlas toast history, all recorded by the framework, none observed live yet].
- Observed 2026-10-01 [observed 2026-10-01 G11-1]: `Record Saved Successfully!` (header Save; once also while tabbing on a line), `Validation successfully`, `Save successfully` (detail Save and Save Sale Pick); Sales Return View Forward (Maker and Checker): result window "Sales Return Status" (Document No, Sales Return Status, Status, Error Message) with Status `Success` (= workbook SaleRetrunView_ASSR), no toast. `Forwarded successfully` was not shown on Sales Return View.
- G11-2: "Record Saved Successfully!" (header), "Validation successfully", "Save successfully" (detail and Save Sale Pick), result window "Sales Return Status ... Success" for Maker and Checker Forward (second day) [observed 2026-10-05 G11-2].
- G11-3: "Record Saved Successfully!", "Validation successfully", "Save successfully", "Sales Return Status" window "Success" [observed 2026-10-06 G11-3].

## 10. Dependencies
Reads a delivered cash memo of the PJP and outlet (so seq 33 or an equivalent delivery state must come first) and `REPO_GINNO` (Status Change). Hands over a Picked return to the Goods Return Note (seq 48-49), and credit/value to settlement. Confirmed 2026-10-01: Cashmemo Status (seq 33) must come first; the picked return's quantity is on the GRN Suggested; the credit value did not reach Route Settlement (Adjusted Credit Note 0) [observed 2026-10-01 G11-1].
- G11-2b: hands the return to Transaction Inquiry (seq 69/71) and the GRN; Route Settlement does not pick it up as Adjusted Credit Note even after the route is Complete [observed 2026-10-05 G11-2b].

## 11. Test design hints
Positive: return 1 CS of one line, validate, save, forward, approve, status change to Picked; amounts match the workbook (Gross, Discount, Tax, Net). Negative: quantity above ordered; CS and PC both 0; no Reason Type; Forward without comments; maker approves own return. Boundary: return = ordered quantity (full line); return of a line with discount/offer item (amounts pro-rated?, [unknown]); PC only vs CS only. A green run proves screen messages only; verify the CM-02 status in the DB and that stock did not move until the GRN.
- Positive: return with Stock Type Damaged / Expired / Lost and check which stock type the GRN posts (only Sound was walked) [observed 2026-10-01 G11-1 for Sound].
- **Trap, receivable:** the approved return is not netted from the cash memo receivable or in Route Settlement (Adjusted Credit Note 0); a test that expects the balance to fall by the return Net would fail, and a test that ignores it proves nothing about the credit (Q-SR1) [observed 2026-10-01 G11-1].
- **Trap, workbook amounts:** totals depend on the source cash memo; if the order was edited the workbook Discount/Tax/Net no longer match (Gross still did) [observed 2026-10-01 G11-1].
- **Trap, stock:** the returned quantity comes back only through the GRN (In, Sound); check the GRN Suggested and Stock Inquiry after GRN approval [observed 2026-10-01 G11-1].
- **Trap, default PJP:** screens default to the first PJP (AutoPJGIN2); choose the delivery PJP explicitly. The Checker sees all PJPs, the Maker only delivery PJPs [observed 2026-10-01 G11-1].
- **Trap, approval result:** View Forward answers in a result window ("Success"), not a toast; the approved return then leaves the View list [observed 2026-10-01 G11-1].
- G11-2 / G11-2b additions [observed 2026-10-05 G11-2, G11-2b]:
  - Positive: header totals of a 2 CS return of the outlet-04 basket after the 7 -> 4 edit: Gross 30,845.86 / Discount 6,189.17 / Tax 4,419.93 / Net 29,077 (two days identical).
  - Positive: Transaction Inquiry Detail of the return: non-returned lines carry small reversals; assert header totals and line 1, not "0 on other lines".
  - Trap (framework drift): the workbook return values (built 2026-09-21 for outlet 1000000003) differ from the app in every field except Gross (Discount 6,169.17, Tax -4,425.41 / -4,436.55, Net -29,113, VAT -4,434.18, 3rd Schedule -1.95, line 1 Disc 6,260.28 / Net -29,010.99). The G11-1 explanation "the source order was edited" is superseded: the workbook was built for another outlet and promotion state. See FRAMEWORK_DRIFT.md.
  - Trap: typing a digit into a grid cell holding 0 can give "02"; clear the cell first.
  - Trap: the return is not netted at settlement; a test expecting Adjusted Credit Note = 29,077 fails today (Q-SR1).
- G11-3 trap: return expected Tax/Net depend on the source order's delivered quantity after all edits (3 CS on 10-06 -> Tax 4,409.61 / Net 29,066); the workbook values are stale (FRAMEWORK_DRIFT.md) [observed 2026-10-06 G11-3].
- QA team 2026-10-08 additions [stated 2026-10-08 QA Team]:
  - Expected values of a partial return = original invoice - middle invoice (recompute price, scheme and tax on the remaining quantity); never pro-rata, never 0 on non-returned lines.
  - Stock types: cases for Sound, Damaged and Expired returns are valid (Lost was not named).
  - PK runs: no Fresh Return; BD runs: Fresh Return uses the current document date.

## 12. Open questions (batched for the BA; each with a default)
Q: Is the return limited to quantity ordered or quantity delivered? | Default: delivered | Evidence: message says "ordered quantity". PARTLY 2026-10-01: Invoice Quantity shown = the delivered/edited quantity (4 CS); the over-return refusal was not tried [observed 2026-10-01 G11-1].
Q: What does "Status Change" do exactly (Picked)? | Default: marks the authorised return as picked up by the DSR | Evidence: button `savesalePick`, status 04 Picked. PARTLY 2026-10-01: button "Save Sale Pick" with editable pick quantity, `Save successfully`; the status text after it was not read [observed 2026-10-01 G11-1].
Q: Does the return reverse stock at approval or only at the GRN? | Default: only at the GRN | Evidence: no stock effect in the flows. PARTLY 2026-10-01: the 2 CS came back via GRN 246 as In (Sound) [observed 2026-10-01 G11-1]; no snapshot between approval and the GRN.
Q: Are discounts/offers on returned items reversed proportionally? | Default: yes (Discount shown) | Evidence: Discount field only. ANSWERED 2026-10-01: yes, Discount 6,189.17 and Tax 4,419.93 reversed on Gross 30,845.86 at the source order's ratios [observed 2026-10-01 G11-1].
Q: Can a return be made before the cash memo is marked delivered? | Default: no | Evidence: chain order only. ANSWERED 2026-10-01: no, Sales Return lists delivered cash memos only [observed 2026-10-01 G11-1].
Q-SR1: When does an approved sales return reduce the cash memo receivable (credit note? Route Settlement?) | Default: at Route Settlement / credit note | Class: B | Evidence: after approval and pick, Balance Amount unchanged and Route Settlement Adjusted Credit Note 0 (2026-10-01); settlement itself was blocked. **-> still open 2026-10-05** (not netted even after the route was settled).
Q: Which return reasons are valid for CM-02: the DB examples (Short of Cash, Area Closed, ...) or the four on screen (No Cash, Wrong Order/No Order, Shop Closed, Credit Exceeded)? | Default: the on-screen list | Class: A | Evidence: dropdown 2026-10-01 vs glb_pr_rnt_reason_type.
Q: What happens when the picked quantity on Status Change differs from the approved return quantity? | Default: the pick quantity is what goes to the GRN | Class: B | Evidence: Return Quantity editable on Status Change 2026-10-01.
Q: Does a non-Sound return stock type (Damaged/Expired/Lost) post to the matching stock type on the GRN? | Default: yes | Class: B | Evidence: only Sound walked.
- Q-SR1 STILL OPEN 2026-10-05 (strengthened): after settlement (route Complete) Adjusted Credit Note 0, Fresh Return 0, 2009 Balance 88,107 excludes the return [observed 2026-10-05 G11-2b].
- ANSWERED 2026-10-05 (Q41, Status Change): Save Sale Pick sets the return to Picked [observed 2026-10-05 G11-2b].
- ANSWERED 2026-10-05 (Q33): the source cash memo stays Delivered/Invoiced after a partial return; the return carries Demand Channel "Partial Return" [observed 2026-10-05 G11-2b].
- Q43 (discount reversal) RE-ANSWERED 2026-10-05: not purely proportional; the slab promotions are re-priced on the remaining basket (lines 2-5 reversals) [observed values; rule inferred].
- Q-SR2: Is it intended that a part return re-prices the order's slab promotions on the non-returned lines (credit includes discount reversals on lines that were not returned)? | Default: yes, promotions are recomputed on the remaining basket | Class: C | Evidence: COL26000000714 Detail lines 2-5 [observed 2026-10-05 G11-2b].
- Q-SR1, Q-SR2 evidence 2026-10-06: return 715 not netted at settlement; re-priced reversals on 0-quantity lines [observed 2026-10-06 G11-3]. Both stay open.
- **Q-SR2 ANSWERED 2026-10-08** [stated 2026-10-08 QA Team]: yes, intended: a partial return creates a middle invoice for the remaining quantity and re-prices price, discount/scheme and tax; the return = original - middle invoice. Fresh Return uses the same logic with the current date.
- **Q-GRN2 / non-Sound return ANSWERED 2026-10-08** [stated 2026-10-08 QA Team]: Sales Returns with reference to an old cash memo can be processed for all stock types (Sound, Damaged, Expired); that the GRN then carries the same stock type is the default, not yet observed.
- Q-SR1 PARTLY ANSWERED 2026-10-08 [stated 2026-10-08 QA Team]: credit notes adjusted at outlet level where invoice net > credit note; Fresh Return BD only; not all scenarios appear for every PJP. Still open: returns 713 / 714 / 715 were never netted (three days) | Class: B.

## 13. Sources
`framework_atlas/flows/00070001.md`, `00700001.md`, `00730001.md`, `00710001.md`, `group_11.md`; DB: snd_pr_dot_documenttype, snd_pr_dos_documentstatus, glb_pr_rnt_reason_type, wkf_wf_weo_wrkflw_event_orga, snd_tr_cmm_cashmemo_master. No SR table of its own exists (CM-02 lives in the cash memo tables).
Learning session 1 (2026-10-01): `learning_sessions/2026-10-01_G11-PK_session1_log.md` seq 34, 36, 37, 38, seq 39-46 (Balance Amount), seq 48-50 (GRN), seq 51 (Route Settlement); `learning_sessions/2026-10-01_G11-PK_session1_report.md` §3 rules 12 and 15, §8 Q-SR1.
- G11-2 / G11-2b: learning_sessions/2026-10-05_G11-PK_session2_log.md (seq 34, 36, 37, 38, 48, 51); learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md (seq 51, 53, 69, 71).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 34, 36, 37, 38, 69, 71).

- QA team written answers 2026-10-08: learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx) (Q-SR1, Q-SR2, Q-GRN2).
