# Goods Return Note (GRN): how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. GRN was NOT replayed live: most statements are [db]/[inferred]. Confidence tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Last updated: 2026-10-01. Source flows: 00090001 (group 11 seq 48), 00810001 (seq 49), 02820001 (seq 50).

## 1. Purpose
After goods were issued to a delivery man (GIN) and the day's deliveries are done, goods not delivered or brought back physically return to the warehouse. The Goods Return Note records that return so the quantity goes back into warehouse stock, and an approver confirms it [inferred from names, GIN/GRN share table snd_tr_gnm_gingrn_master with a "suggested qty" and "actual qty"]. In the Daily Cycle it sits after sales returns and deposit slips and before Route Settlement; then Stock Inquiry (seq 50) checks the stock.

## 2. Actors and roles
Maker = Auto_Multi_Orga (seq 48, same session) ; Checker = Auto_Tssm (seq 49, switch point); stock check by Auto_Multi_Orga (seq 50, switch point) [atlas].

## 3. Documents and master data
Document type GR-01 "Goods Return Note" (also GR) [db snd_pr_dot_documenttype]. Stored with GINs in snd_tr_gnm_gingrn_master / _detail (columns suggested qty tgnd_sugg_qty_1..3, actual qty tgnd_qty_1..3, stock type, loss reason tgnd_loss_reason) [db]. GRN No is a number (an earlier test run recorded GRN No 225 in an error message) [atlas observed toast]. Needs a Delivery Man PJP (route/DSR) [atlas].

## 4. Inputs: screens and fields
Menu "Goods Return Notes" (GOODS_RETURN_NOTES). Screens: Goods Return Note (Delivery Man PJP*, mandatory), Detail tab (row edit: CS, PC actual quantities), validation screen reading Rate, Save All (saveAll), then Forward screen: grid filter on GRN No (field "GRN No"), Forward with Comments [atlas].

## 5. Process: the business steps in order
1. [Maker] Navigate to Goods Return Notes; choose Delivery Man PJP (the same PJP the GIN was issued to [inferred]).
2. [Maker] On Detail, edit each row: set actual CS / PC, Save row, move to the next row (flow control event).
3. [Maker] Save All; GRN number is stored in REPO_GRNNO (11:48:00090001).
4. [Maker] Filter by GRN No, open, Forward with comment.
5. [Checker] Navigate to Good Return Note Approval, filter by GRN No, open row, Forward with comment -> "Forwarded successfully" (11:49:00810001) [atlas toast history, 14 times].
6. [Stock Controller] Stock Inquiry for the warehouse, compare In CS / In PC (11:50:02820001).

## 6. Outputs and effects
Approved GRN: workflow GRN is bound to StockUpdateGRN and a "GRNApprovalSaga" [db], so approval updates stock: returned quantities go back In to the warehouse stock of the day [inferred]. Which stock type receives them (Sound or per detail line) is [unknown].

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| (new) | Save All | Draft | Maker | inferred |
| Draft | Forward | Pending for approval | Maker | db (GRN statuses 01-05) |
| Pending | Forward | Approved | Checker | db / atlas toast |
| Pending | Reject / Terminate | Rejected / Terminated | Checker | db |
A GIN/GRN cancel saga (ginGrnCancelSaga) also exists [db].

## 8. Rules and validations
- Actual quantity cannot exceed the suggested quantity: "Actual Qty cannot be greater than the suggested Qty" [atlas toast history].
- A GRN needs detail rows: "no detail found against the GRN No.:225", "incomplete data received." [atlas toast history].
- Comments needed at Forward (same popup as DA) [inferred]. "Do not use Special charters." appeared on approval comment [atlas toast history].

## 9. Messages
"Actual Qty cannot be greater than the suggested Qty"; "An Error Occurred! no detail found against the GRN No.:225"; "An Error Occurred! incomplete data received."; "Forwarded successfully"; "Do not use Special charters."; "input parameters are going to be empty. ginDetailBeans:[]" [all from past framework runs, not replayed by us].

## 10. Dependencies
Reads the GIN issued to the delivery man (suggested quantities) and the Delivery Man PJP. Hands to: stock (In), Route Settlement and cash reconciliation (orders/delivery analyst's pages; link by name only). Day boundary: the GRN must be on the same day as the GIN/stock day or stock lookup fails [inferred from GIN failure].

## 11. Test design hints
- Positive: return all suggested quantities; return part; approve; stock In rises by the returned CS.
- Negative: actual > suggested; zero rows; Forward without comment; special characters in comment; checker same as maker; GRN on a PJP with no GIN.
- Boundary: actual = suggested, actual = 0, PC vs CS mix.
- Traps: seq 50 compares absolute In/Out values and is fragile on a busy day; a green approval toast does not prove stock changed; GRN not yet replayed, so ids and messages are unconfirmed.

## 12. Open questions
Q: What business situation creates a GRN (undelivered goods, return to supplier, or both)? | Default: undelivered goods returned by the delivery man | Evidence: names and shared GIN table only.
Q: Which stock type and day does an approved GRN credit? | Default: Sound, same day | Evidence: not replayed.
Q: Can a GRN be created without a GIN? | Default: no | Evidence: suggested qty comes from GIN [inferred].
Q: Are Rate and amounts used financially? | Default: informational | Evidence: validation screen reads Rate only.

## 13. Sources
framework_atlas/flows/00090001.md, 00810001.md, 02820001.md, group_11.md (seq 48-50); DB snd_pr_dot_documenttype, snd_tr_gnm_gingrn_master/detail, wkf_wf_weo_wrkflw_event_orga (GRN, grnApprovalSaga), wkf_wf_wfs_workflow_status.
