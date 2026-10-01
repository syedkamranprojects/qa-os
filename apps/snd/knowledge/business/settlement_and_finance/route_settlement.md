# Route settlement: closing a DSR's day (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Last updated: 2026-10-01. Source flows: 00680001 (seq 51), 03210001 (52), 03220001 (53), 03250001 (54). No live replay. DB has 35 settlement rows, all org 0101, none for 010104.

## 1. Purpose
Route settlement is the end-of-day reconciliation of one PJP (a DSR's route) for one working date: what was sold and delivered, what was returned, what cash and cheque was collected (previous days plus today), what stock was short, and the resulting cash shortage. It follows delivery, returns and deposit slips and precedes closing the day (PJP Daily Inquiry Update). [inferred from field and table names]

## 2. Actors and roles
Auto_Multi_Orga (same session) [db]. No approval step [db].

## 3. Documents and master data
- `snd_tr_rsl_dsr_route_settlem` (one row per PJP code + working date): total/delivered/undelivered order counts, return picked up, sales value, return value, adjusted credit note amount, previous/today/total cash and cheque, stock shortage, stock shortage received amount, cash shortage, settlement datetime [db].
- `snd_tr_rsd_dsr_route_setl_dt`: one line per deposit-slip type (e.g. CSH "CASH"): suggested vs entered amount [db].
- Needs a PJP with delivered cash memos and collections.

## 4. Inputs: screens and fields
Menu: Transaction > Receivable > Route Settlement (`ROUTE_SETTLEMENT`, /content-master/route-settlement) [db].
- 006801: **Date** (date picker), **PJP Number** (autoselect), Select all (`selectAll`) then load [db].
- Validation screens (read-only, compared with workbook/DB): 006802 Sale Value, Adjusted Credit Note Amount, Fresh Return Value; 006803 Previous Cash, Today Cash, Total Cash, Previous Cheque, Today Cheque, Total Cheque; 006804 Payable Amount, Received Amount, Stock Shortage Payable Amt, Stock shortage Received Amt; 006805 Cash Shortage, Total Payable Amount, Total Received Amount (row edit and save); 006806 Total Received Amount, Total Payable Amount, Total Cash Shortage [db: atlas].

## 5. Process
1. [Maker] Open Route Settlement; enter Date and PJP Number; Select all. trace 11:51:00680001
2. [Maker] Validate Sale Value, Adjusted Credit Note, Fresh Return Value. [db]
3. [Maker] Validate previous/today/total cash and cheque. [db]
4. [Maker] Validate payable vs received and stock shortage; edit a row and save to set the received amount per type. [db]
5. [Maker] Validate totals and total cash shortage; each screen asserts a toast (TSTMSG).
6. [Maker] Seq 52: Transaction Inquiry for the outlet, read **Offset Amount** (screen 032102): the part of the invoice offset by returns/credit notes [inferred]. 11:52
7. [Maker] Seq 53/54: reopen the deposit slip and read **Received Amount** after settlement; seq 54 after an order removal. 11:53, 11:54

## 6. Outputs and effects
A settlement row for PJP/date with shortage figures and lines per payment type (suggested vs entered); time-stamped (`trsl_route_settl_datetime`) [db]. Cash shortage = payable minus received [inferred].

## 7. Statuses and transitions
No document status column in the settlement tables [db]; "settled" is implied by row existence [inferred].

## 8. Rules and validations
- Total cash/cheque = previous + today [inferred from the column triple].
- Stock shortage (payable and received) tracked separately from cash shortage [db].
- Sale value counts delivered orders; undelivered counted separately [inferred].

## 9. Messages
None recorded for 00680001 [unknown].

## 10. Dependencies
Reads delivered cash memos (GIN seq 20), sales returns (seq 34-38), deposit slips (seq 39-46). Hands Offset Amount and Received Amount checks to seq 52-54. Keyed by PJP + working date (same-day).

## 11. Test design hints
- Positive: PJP with full cash delivery; with returns and credit notes; with cheque collection.
- Negative: PJP with no deliveries (all-zero row exists in DB); future date; settle the same PJP twice; entered amount differing from suggested.
- Boundary: received = payable (shortage 0); received 0.01 less.
- Arithmetic cross-checks: total = previous + today; sale - return - adjusted credit note vs collections.
- A green run proves screen values against the workbook, not that the settlement row was persisted.

## 12. Open questions
Q: Payable vs Received Amount exactly? | Default: payable = system-suggested, received = entered | Evidence: rsd suggested/entered columns.
Q: Can a settled PJP/date be reopened? | Default: no | Evidence: none.
Q: How is Offset Amount derived? | Default: credit notes/returns netted against the invoice | Evidence: label only.

## 13. Sources
framework_atlas/flows/00680001, 03210001, 03220001, 03250001; group_11.md; DB snd_tr_rsl_dsr_route_settlem, snd_tr_rsd_dsr_route_setl_dt; snd_menu_outline.md.
