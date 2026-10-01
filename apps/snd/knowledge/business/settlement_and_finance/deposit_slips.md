# Deposit slips: banking the cash and cheques collected (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]** seen live, **[db]** declared by the application DB or framework tables, **[inferred]** concluded by Claude, **[unknown]** not determinable yet.
Last updated: 2026-10-01. Source flows: 03230001 (seq 39), 03240001 (40), 03260001 (41), 00140001 (42), 00140004 (44), 00140005 (46); related 03220001 (53), 03250001 (54). No live replay of any exists; the DB holds no 010104 deposit-slip rows (4 rows, all org 0101).

## 1. Purpose
A deposit slip records the money a DSR (salesman, identified by his daily PJP) hands in after delivering: how much of the cash and/or cheques collected on cash memos (invoices) is being banked. It ties collected money to specific cash memos so each outlet's receivable is reduced [inferred from table links: slip detail -> snd_tr_cmm_cashmemo_master]. It follows GIN/delivery and sales return and precedes Route Settlement (seq 51), which reconciles the day's collection per PJP. [inferred]

## 2. Actors and roles
Maker Auto_Multi_Orga on all six flows (same session, no user switch) [db: group 11]. An approval row "Deposit Slip Approval" (00140002) exists but is inactive (seq 43/45/47) [db], so no approval step is exercised; whether slips need approval is [unknown].

## 3. Documents and master data
- Header `snd_tr_dsl_deposit_slip`: org, entity type, distributor code, serial `tdsl_deposit_slip_srno` (auto-generated, shown as "Deposit Slip"). Holds PJP daily number, instrument type, bank, branch, amount, date, status (default `I`) [db].
- Detail `snd_tr_dsd_deposit_slip_dtl`: one row per cash memo: document type, cash memo number (`tcmm_docno`), amount, cheque no/date, bank, instrument status and its date [db].
- Master data: payment modes for 010104: 01 Cash (default), 02 Cheque, 05 Mobile Money Transfer, 06 Credit Note active; 03 Credit Card, 04 Bank Transfer inactive [db]; banks and branches (glb_pr_bnb_bankbranch); instrument statuses (see cheque_status.md).
- Upstream: a delivered cash memo with open balance (REPO_GINNO from seq 20) [db].

## 4. Inputs: screens and fields
Menu: Transaction > Receivable > Deposit Slip (`DYL_201802`) [db]. Header screen plus a child tab listing cash memos.
- Header: Deposit Slip (read-only, generated), **PJP-DSR*** (list PJPDD), Date (read-only), **Type*** (list PPYM, "Instrument Type (Cash/Cheque)"), Status (default I), Bank, Bank Branch, **Deposit Amount*** (regex rejects 0 and non-numeric: `^(?!0+(\.0+)?$)\d+(\.\d+)?$`) [db].
- Cash-memo tab fields used by flows: Deposit Amount, Cheque No, Cheque Date, Bank_Name; grid columns Serial No, Document Type, Order Number, Deposit Amount, Currency, Organization, Cheque No, Cheque Date, Cheque Status, Cheque Status Date, Invoice Number, Remarks [db].
- Buttons: Refresh, New, Save, Update, Delete [db]. Picking uses a filter then a GIN row (`filter_2`, `row_1_gin`) and "save all" (`saveallBtn`) [db: atlas events].
- Variants: 03230001 Full Amount Cash; 03240001 Full Amount Cheque (adds Bank, Bank Branch, Cheque No/Date); 03260001 Unposted (then screen "Deposit slip Val Unposted" reads **Un Posted Amount**); 00140001 Multi Cheques (screen "Deposit Slip,Outlet": Cheque. No, Cheque Date, Bank, Net Amount, cash-memo selection grid, popup); 00140004 Cheque; 00140005 Cash [db].

## 5. Process
1. [Maker] Open Deposit Slip, click New (`addBtn`). trace 11:39..46
2. [Maker] Select PJP-DSR, Type (Cash/Cheque), Deposit Amount (+ Bank/Branch for cheque); Save; assert toast from sheet DEPOSIT_SAVE_ASSR. The slip number is read from the first grid row (`row_1_deposit_slip`) into REPO_Deposit_Slip. [db]
3. [Maker] In the cash-memo tab filter, pick the GIN/cash memo (REPO_GINNO), enter Deposit Amount (plus Cheque No, Date, Bank for cheque), Save all. [db]
4. [Maker] (03260001) read Un Posted Amount and compare with expected. [db]
5. After Route Settlement: 03220001 reopens the slip and reads **Received Amount**; 03250001 reopens slips after an order was removed and walks the cash and cheque tabs (flow-control only, no assertion). [db]

## 6. Outputs and effects
A slip with detail rows per cash memo; header status starts `I`; a DB sample shows status `A` with a posting date once complete [db, org 0101]. `snd_tr_cmm_cashmemo_payment` references the slip [db]. "Unposted" = slip money not yet allocated to cash memos [inferred].

## 7. Statuses and transitions
| from | action | to | by | tag |
|---|---|---|---|---|
| (new) | Save header | `I` | Maker | [db] default I |
| `I` | Save all with cash memos | `A` + posting date | Maker/process | [db] sample, trigger [unknown] |
| detail row | Cheque Status update | P/L/R/B/C/A | Maker | [db] see cheque_status.md |

## 8. Rules and validations
- PJP-DSR, Type, Deposit Amount mandatory; amount > 0 numeric [db].
- Historic toasts in the atlas (other markets): "Balance should be greater than deposit amount at Doc no. ITB000003747" (deposit above the cash memo balance [inferred]), "Required Fields are empty!", "Invalid transaction attempt", "Do not use Special charters." [db: 00140004/00140001].
- A cash memo must be delivered (GIN) before deposit [inferred].

## 9. Messages
"Saved successfully" and "Record saved successfully!" on save; others as in section 8 [db: atlas toast history, not PK-specific].

## 10. Dependencies
Reads REPO_GINNO (seq 20; 00140001 reads nothing, selects by outlet). Writes REPO_Deposit_Slip (no later row in group 11 consumes it [db]). Hands cash/cheque amounts to Route Settlement [inferred]. Slips are dated (`tdsl_deposit_slip_date`): same-day cycle [inferred].

## 11. Test design hints
- Positive: full cash, full cheque, multi-cheque across outlets, partial (unposted) then complete.
- Negative: amount 0, negative, text, special characters; empty PJP; cheque without Bank/Cheque No; amount above balance; same cash memo twice; cash memo of another PJP.
- Boundary: amount = balance; balance - 0.01; two decimals.
- A green run does not prove posted/unposted arithmetic or cash-memo balance reduction: only the save toast is asserted; seq 54 has no assertion at all.

## 12. Open questions
Q: Does a deposit slip need checker approval? | Default: no | Evidence: 00140002 inactive.
Q: What flips status I to A? | Default: Save all with full amount | Evidence: sample rows only, org 0101.
Q: Exact meaning of "Unposted Amount"? | Default: slip amount minus amount allocated to cash memos | Evidence: label only.
Q: Can a slip mix cash and cheque? | Default: no, one Type per slip | Evidence: single Type field.

## 13. Sources
framework_atlas/flows/03230001, 03240001, 03260001, 00140001, 00140004, 00140005, 03220001, 03250001 (.md/.json); framework_atlas/group_11.md; screens_db/DYL_201802.json; DB snd_tr_dsl_deposit_slip, snd_tr_dsd_deposit_slip_dtl, glb_pr_pym_paymentmode, snd_tr_cmm_cashmemo_payment.
