---
option: Goods Return Note
area: inbound_stock
doc_types: [GR-01]
screens: [GOODS_RETURN_NOTES]
framework_flows: ["00090001", "00810001", "02820001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [goods_issue_note, order_editing_cancellation, cashmemo_reschedule_and_status, sales_return, stock_inquiry_and_balances]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-06
---

# Goods Return Note (GRN): how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. GRN was NOT replayed live: most statements are [db]/[inferred]. (Superseded 2026-10-01 G11-1: GRN 246 was created, forwarded, approved and stock-checked live; observed facts are tagged [observed 2026-10-01 G11-1].) Confidence tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Last updated: 2026-10-01 (G11-1 consolidation). Source flows: 00090001 (group 11 seq 48), 00810001 (seq 49), 02820001 (seq 50). G11-1 learning walk: GRN **246** (19 CS, GIN 506).
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.

## 1. Purpose
After goods were issued to a delivery man (GIN) and the day's deliveries are done, goods not delivered or brought back physically return to the warehouse. The Goods Return Note records that return so the quantity goes back into warehouse stock, and an approver confirms it [inferred from names, GIN/GRN share table snd_tr_gnm_gingrn_master with a "suggested qty" and "actual qty"]. In the Daily Cycle it sits after sales returns and deposit slips and before Route Settlement; then Stock Inquiry (seq 50) checks the stock.
- Confirmed live: **everything that left on the GIN and was not delivered, or was returned, comes back on the GRN**: orders cancelled after the GIN, orders rescheduled off the GIN (Reattempt), quantities cut by an order edit after the GIN, and picked sales returns. GRN 246 suggested exactly 19 CS of 62740537 = 7 (COL26000002007 cancelled after GIN) + 7 (COL26000002006 rescheduled) + 3 (COL26000002003 cut 7 -> 4) + 2 (sales return COL26000000713) [observed 2026-10-01 G11-1] (was [inferred]).
- G11-2: confirmed on a second day: GRN **247** suggested 19 CS of 62740537 = 7 (COL26000002013 cancelled after GIN 507) + 3 (COL26000002009 cut 7 -> 4) + 7 (COL26000002012 rescheduled) + 2 (sales return COL26000000714) [observed 2026-10-05 G11-2].

## 2. Actors and roles
Maker = Auto_Multi_Orga (seq 48, same session) ; Checker = Auto_Tssm (seq 49, switch point); stock check by Auto_Multi_Orga (seq 50, switch point) [atlas].
- G11-1: Maker Auto_Multi_Orga created and forwarded GRN 246; Checker Auto_Tssm approved it; Maker Auto_Multi_Orga checked stock [observed 2026-10-01 G11-1] (was [atlas]).
- Maker on a Draft GRN: Forward ON, Reject OFF. Checker on a Pending GRN: Forward + Reject enabled [observed 2026-10-01 G11-1].
- G11-2: Maker Auto_Multi_Orga created and forwarded GRN 247, Checker Auto_Tssm approved it on the same Goods Return Notes screen [observed 2026-10-05 G11-2].

## 3. Documents and master data
Document type GR-01 "Goods Return Note" (also GR) [db snd_pr_dot_documenttype]. Stored with GINs in snd_tr_gnm_gingrn_master / _detail (columns suggested qty tgnd_sugg_qty_1..3, actual qty tgnd_qty_1..3, stock type, loss reason tgnd_loss_reason) [db]. GRN No is a number (an earlier test run recorded GRN No 225 in an error message) [atlas observed toast]. Needs a Delivery Man PJP (route/DSR) [atlas].
- G11-1: GRN No **246** (plain number, generated) [observed 2026-10-01 G11-1]. Delivery Man PJP 02112-AutomationDSR, DSR ITB0189-AutomationQADSR, Warehouse C0000000055 Auto Main, Vehicle 0040-Automation211206, GIN Number 506 [observed 2026-10-01 G11-1]. Needs a Delivery Man PJP (upgraded to [observed 2026-10-01 G11-1], was [atlas]).
- G11-2: GRN No **247**, Delivery Man PJP 02112-AutomationDSR, DSR ITB0189-AutomationQADSR, Warehouse C0000000055, Vehicle 0040-Automation211206, GIN 507 filled from the PJP, rate 7,711.47 [observed 2026-10-05 G11-2].

## 4. Inputs: screens and fields
Menu "Goods Return Notes" (GOODS_RETURN_NOTES). Screens: Goods Return Note (Delivery Man PJP*, mandatory), Detail tab (row edit: CS, PC actual quantities), validation screen reading Rate, Save All (saveAll), then Forward screen: grid filter on GRN No (field "GRN No"), Forward with Comments [atlas].
- G11-1 live labels [observed 2026-10-01 G11-1]:
  - Menu Transaction > Goods Return Notes. Tabs **GRN** / **Detail**; buttons Add, Forward, Reject.
  - Header: GRN No. (generated), GRN Date (today), Delivery Man PJP, Delivery Man DSR, Warehouse, Vehicle, Status, **Working Date** (today), **GIN Number**, Approval Status.
  - Picking Delivery Man PJP fills Delivery Man DSR, Warehouse, Vehicle and **GIN Number** (the DSR's open GIN of the working date).
  - Detail: Product, Batch, Stock Type (01-Sound), **Suggested** CS/DZ/PC, **Actual** CS/DZ/PC (editable via Edit), Rate.
  - Master grid: GRN No., GRN Date, Delivery Man PJP, Warehouse, Approval Status, Status.
  - The GRN tab resets to a blank form after Save All (like the DA and GIN); reopen the GRN from the grid.

## 5. Process: the business steps in order
1. [Maker] Navigate to Goods Return Notes; choose Delivery Man PJP (the same PJP the GIN was issued to [inferred]). (Upgraded: the delivery PJP of the GIN, 02112, whose GIN Number fills itself [observed 2026-10-01 G11-1].)
2. [Maker] On Detail, edit each row: set actual CS / PC, Save row, move to the next row (flow control event).
3. [Maker] Save All; GRN number is stored in REPO_GRNNO (11:48:00090001).
4. [Maker] Filter by GRN No, open, Forward with comment.
5. [Checker] Navigate to Good Return Note Approval, filter by GRN No, open row, Forward with comment -> "Forwarded successfully" (11:49:00810001) [atlas toast history, 14 times]. (Upgraded: [observed 2026-10-01 G11-1]; the Checker uses the same Goods Return Notes screen.)
6. [Maker] Stock Inquiry for the warehouse, compare In CS / In PC (11:50:02820001).

G11-1 walk, GRN 246 (standard vocabulary, trace keys) [observed 2026-10-01 G11-1]:
1. [Maker] Navigate to Goods Return Notes; Click Add (11:48:00090001).
2. [Maker] Choose Delivery Man PJP 02112-AutomationDSR -> DSR, Warehouse, Vehicle, GIN Number 506 fill (11:48:00090001).
3. [Maker] Open Detail; Verify Suggested 62740537 19 CS; Enter Actual 19 (11:48:00090001).
4. [Maker] Click Save All -> "Record Saved Successfully"; GRN 246 Draft / In-Active (11:48:00090001).
5. [Maker] Open GRN 246 from the grid; Click Forward; Enter Comments "Automation Approval"; Save -> "Forwarded successfully"; Pending for approval (11:48:00090001).
6. [Checker] Navigate to Goods Return Notes; Open GRN 246 (Pending for approval, GIN 506); Click Forward; Enter Comments "Automation Approval"; Save -> "Forwarded successfully"; GRN 246 leaves the grid (11:49:00810001).
7. [Maker] Navigate to Stock Inquiry; Verify 62740537 Auto Main Sound In +19, Out unchanged, Closing +19 (11:50:02820001).

G11-2 walk, GRN 247 (2026-10-05): same steps as GRN 246 (11:48:00090001, 11:49:00810001, 11:50:02820001); Save All -> "Record Saved Successfully" (Draft, In-Active); Maker Forward -> "Forwarded successfully" (Pending); Checker Forward -> "Forwarded successfully", 247 leaves the pending list; old pending GRNs 231/232 of 08-21 still listed for the Checker [observed 2026-10-05 G11-2].
- G11-3 (2026-10-06) [observed 2026-10-06 G11-3]: [Maker] Goods Return Notes; Add; Delivery Man PJP 02112 -> DSR ITB0189-AutomationQADSR, warehouse C0000000055, vehicle 0040-Automation211206, GIN 508 auto-filled; Detail 62740537 Suggested **17 CS**, Actual 17, 7,711.47; Save All -> "Record Saved Successfully", GRN **248** Draft; reopen (double-click); Forward, comment "Automation Approval" (verified), Save -> "Forwarded successfully". [Checker] open 248 (Pending, GIN 508), Forward, comment, Save -> "Forwarded successfully"; 248 leaves the pending list (11:48:00090001, 11:49:00810001).

## 6. Outputs and effects
Approved GRN: workflow GRN is bound to StockUpdateGRN and a "GRNApprovalSaga" [db], so approval updates stock: returned quantities go back In to the warehouse stock of the day [inferred]. Which stock type receives them (Sound or per detail line) is [unknown]. (Superseded 2026-10-01 G11-1: both now observed, see below.)
- **GRN approval posts the returned quantity as In (Sound) on the same day; it does not reduce Out**: 62740537 Auto Main Warehouse 01 - Sound In 164 -> 183 (+19), Out stays 35, Allocated 63, Closing 226 -> 245; other four SKUs unchanged; row count 39 [observed 2026-10-01 G11-1] (was [inferred] / [unknown]).
- Returned goods come back as **Sound** (GRN line stock type 01-Sound; the sales return was booked Sound too) [observed 2026-10-01 G11-1]. Whether a non-Sound sales return (Damaged/Expired/Lost) comes back with another stock type is open (Q-GRN2).
- Approved GRNs are not listed in the Goods Return Notes grid (like approved GINs) [observed 2026-10-01 G11-1].
- The rescheduled order's quantity (COL26000002006, Reattempt, delivery 2026-10-02) returns to stock via the GRN, and is to be issued again on its new delivery date [observed 2026-10-01 G11-1 for the return; re-issue inferred].
- The GRN reconciles exactly with the day's post-GIN changes (19 CS), so it is the point where orders edited/cancelled after the GIN finally give stock back [observed 2026-10-01 G11-1].
- G11-2: GRN 247 approval: 62740537 In 80 -> 99 (+19), Out 35 unchanged, Closing 290 -> 309 (confirmed on a second day) [observed 2026-10-05 G11-2].
- G11-3: GRN 248 = **17 CS** of 62740537 = 7 (2019 cancelled after GIN) + 7 (2018 rescheduled) + 1 (2015 cut 4 -> 3 after GIN) + 2 (return 715) [observed total 2026-10-06 G11-3; breakdown inferred]; on approval In +17, Out unchanged (seq 50) [observed 2026-10-06 G11-3]. The before-GIN edit (7 -> 4) and the before-GIN cancel (2017) are not on the GRN because they were never issued [inferred].

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| (new) | Save All | Draft | Maker | inferred (upgraded: Draft / In-Active [observed 2026-10-01 G11-1]) |
| Draft | Forward | Pending for approval | Maker | db (GRN statuses 01-05) (upgraded: [observed 2026-10-01 G11-1]) |
| Pending | Forward | Approved | Checker | db / atlas toast (upgraded: [observed 2026-10-01 G11-1]; GRN leaves the grid) |
| Pending | Reject / Terminate | Rejected / Terminated | Checker | db (G11-1: Reject enabled for the Checker on Pending; no Terminate button seen [observed 2026-10-01 G11-1]) |
A GIN/GRN cancel saga (ginGrnCancelSaga) also exists [db].

## 8. Rules and validations
- Actual quantity cannot exceed the suggested quantity: "Actual Qty cannot be greater than the suggested Qty" [atlas toast history].
- A GRN needs detail rows: "no detail found against the GRN No.:225", "incomplete data received." [atlas toast history].
- Comments needed at Forward (same popup as DA) [inferred]. "Do not use Special charters." appeared on approval comment [atlas toast history]. (Upgraded: the Forward Comments window appears for Maker and Checker [observed 2026-10-01 G11-1].)
- Suggested quantity = sum of what left on the GIN and was not delivered or was returned (cancelled after GIN, rescheduled, cut by edit, picked sales return) per SKU [observed 2026-10-01 G11-1].
- The GIN Number comes from the selected Delivery Man PJP's open GIN of the working date (not chosen separately) [observed 2026-10-01 G11-1].
- Only SKUs with a return quantity appear on the Detail (2006 and 2007 were single-line orders of 62740537, so only one row) [observed 2026-10-01 G11-1].

## 9. Messages
"Actual Qty cannot be greater than the suggested Qty"; "An Error Occurred! no detail found against the GRN No.:225"; "An Error Occurred! incomplete data received."; "Forwarded successfully"; "Do not use Special charters."; "input parameters are going to be empty. ginDetailBeans:[]" [all from past framework runs, not replayed by us].
- G11-1: Save All -> **"Record Saved Successfully"** (matches workbook GRN_DTL_SAVE_ASSR); Maker Forward and Checker Forward -> **"Forwarded successfully"** (upgraded to [observed 2026-10-01 G11-1]).
- G11-2: "Record Saved Successfully" and "Forwarded successfully" (Maker, Checker) confirmed [observed 2026-10-05 G11-2].

## 10. Dependencies
Reads the GIN issued to the delivery man (suggested quantities) and the Delivery Man PJP. Hands to: stock (In), Route Settlement and cash reconciliation (orders/delivery analyst's pages; link by name only). Day boundary: the GRN must be on the same day as the GIN/stock day or stock lookup fails [inferred from GIN failure].
- G11-1: reads the approved GIN 506 of the working date (2026-10-01), plus the post-GIN order changes (Order Editing After GIN, Order Cancellation After GIN, Cashmemo Reschedule) and the picked sales return (Sales Return Status Change "Save Sale Pick") [observed 2026-10-01 G11-1]. Hands In to Stock Inquiry the same day (seq 50) [observed 2026-10-01 G11-1].

## 11. Test design hints
- Positive: return all suggested quantities; return part; approve; stock In rises by the returned CS.
- Negative: actual > suggested; zero rows; Forward without comment; special characters in comment; checker same as maker; GRN on a PJP with no GIN.
- Boundary: actual = suggested, actual = 0, PC vs CS mix.
- Traps: seq 50 compares absolute In/Out values and is fragile on a busy day; a green approval toast does not prove stock changed; GRN not yet replayed, so ids and messages are unconfirmed. (Superseded 2026-10-01 G11-1 for "not yet replayed": messages now observed.)
- G11-1 additions [observed 2026-10-01 G11-1]:
  - Positive (reconciliation): after a day with a cancel-after-GIN, a reschedule, an edit-after-GIN cut and a picked sales return, assert Suggested per SKU = the sum of those quantities (19 = 7 + 7 + 3 + 2).
  - Positive (stock): after approval assert In delta = Actual and **Out delta = 0** (GRN posts In, not a reduction of Out); Closing delta = Actual.
  - Negative: Maker opens a Draft GRN -> Reject disabled; after approval the GRN is not in the grid (do not search for it there).
  - Boundary: Actual < Suggested (partial return) not yet tried: what happens to the difference is open (Q-GRN1).
  - Traps: the workbook GRN detail (1 CS 5 PC / 2 CS 1 PC, rates 118.93 / 33.79) belongs to its own order mix and is not valid on another day's data: derive Suggested from the day's documents; the GRN tab resets to a blank form after Save All, reopen from the grid before Forward.
- G11-2: the 19 CS reconciliation (cancel-after-GIN 7 + edit cut 3 + reschedule 7 + return 2) reproduced exactly with new documents on 2026-10-05; it is a stable, data-driven regression check [observed 2026-10-05 G11-2].
- Trap: the Checker's grid also lists stale pending GRNs (231/232 from 08-21); filter by GRN No [observed 2026-10-05 G11-2].

## 12. Open questions
Q: What business situation creates a GRN (undelivered goods, return to supplier, or both)? | Default: undelivered goods returned by the delivery man | Evidence: names and shared GIN table only.
ANSWERED 2026-10-01 (G11-1): undelivered and returned goods of the delivery man's GIN: orders cancelled after the GIN, rescheduled orders, quantities cut after the GIN, and picked sales returns [observed 2026-10-01 G11-1]. Return to supplier not seen.
Q: Which stock type and day does an approved GRN credit? | Default: Sound, same day | Evidence: not replayed.
ANSWERED 2026-10-01 (Q08, G11-1): Sound (01), same day (2026-10-01), as In; Out unchanged [observed 2026-10-01 G11-1, GRN 246].
Q: Can a GRN be created without a GIN? | Default: no | Evidence: suggested qty comes from GIN [inferred]. (G11-1: the GIN Number fills itself from the delivery PJP's open GIN [observed 2026-10-01 G11-1]; no-GIN case not tried.)
Q: Are Rate and amounts used financially? | Default: informational | Evidence: validation screen reads Rate only.
ANSWERED 2026-10-01 (Q42 part, G11-1): a picked sales return's quantity comes back to warehouse stock via the GRN (2 CS of COL26000000713 in GRN 246), not at return approval [observed 2026-10-01 G11-1].
Q-GRN1: When Actual < Suggested on a GRN, where does the difference go (loss record, shortage at Route Settlement)? | Default: shortage charged to the delivery man at Route Settlement | Class: B | Evidence: only a full return (Actual = Suggested) was walked [observed 2026-10-01 G11-1].
Q-GRN2: Does a sales return booked as Damaged/Expired/Lost come back on the GRN with that stock type? | Default: yes, per line stock type | Class: B | Evidence: only a Sound return walked; Sales Return offers Damaged, Expired, Lost, Sound [observed 2026-10-01 G11-1].
- G11-2: Q-GRN1 and Q-GRN2 still open (again only a full Sound return walked).

## 13. Sources
framework_atlas/flows/00090001.md, 00810001.md, 02820001.md, group_11.md (seq 48-50); DB snd_pr_dot_documenttype, snd_tr_gnm_gingrn_master/detail, wkf_wf_weo_wrkflw_event_orga (GRN, grnApprovalSaga), wkf_wf_wfs_workflow_status.
- G11-1 learning walk: learning_sessions/2026-10-01_G11-PK_session1_log.md (seq 29, 31, 32, 34, 38, 48, 49, 50) and learning_sessions/2026-10-01_G11-PK_session1_report.md (§1, §2, §3 rule 7).
- G11-2: learning_sessions/2026-10-05_G11-PK_session2_log.md (seq 48, 49, 50).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 48, 49, 50).
