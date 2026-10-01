# Cheque status: tracking a deposited cheque (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas and the snd-schema DB. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Last updated: 2026-10-01. Source flow: 00660001 (seq 55). No live replay.

## 1. Purpose
Once cheques are banked on a deposit slip they are not yet money: the bank may realize or bounce them. Cheque Status lets finance mark each cheque with its outcome so the outlet's receivable is restored if it bounces. [inferred]

## 2. Actors and roles
Auto_Multi_Orga (same session) [db]. No approver [db].

## 3. Documents and master data
Works on deposit slip headers/details (`snd_tr_dsl_deposit_slip`; detail `pins_instrument_status`, `tdsd_instrument_status_date`) [db]. Instrument statuses for 010104 (glb_pr_ins_instrument_status): C Cancelled, P Presented, L Collected, B Bounced, R Realized, A Amendment [db].

## 4. Inputs: screens and fields
Menu: Transaction > Receivable > Cheque Status (`DYL_202020`) [db]. Grid: Serial No, Currency, Organization, Cheque No, Cheque Date, Amount, Cheque Status, Cheque Status Date; button **Bounce** [db]. Flow actions: filter checkbox, select deposit slip (header and row), tick the cheque row (`checkbox-1`, `row_1_cheque_no`), "notrefresh"; assert toast from sheet Cheque_Status_ASSR [db].

## 5. Process
1. [Maker] Open Cheque Status; filter. trace 11:55:00660001
2. [Maker] Select the deposit slip and the cheque row.
3. [Maker] Change Cheque Status or press Bounce and save; assert toast. [inferred: atlas shows only the row selection]

## 6. Outputs and effects
Instrument status and date updated on the slip detail; a bounce presumably reopens the cash memo balance [inferred].

## 7. Statuses and transitions
| from | action | to | tag |
|---|---|---|---|
| P / L | bank clears | R Realized | [inferred] |
| P / L | Bounce button | B Bounced | [db button, target inferred] |
| any | cancel | C Cancelled | [inferred] |
Allowed transitions: [unknown].

## 8. Rules and validations
None declared beyond the status master [unknown]. The slip detail table has 0 rows in this DB, so status usage is unobserved.

## 9. Messages
Not recorded [unknown].

## 10. Dependencies
Needs a cheque deposit slip (seq 40/42/44). Nothing downstream in group 11. Reports "Cheque For Realization" (`DYL_JR1007`) and Power BI "Cheque Details" read this status [db: menu].

## 11. Test design hints
Positive: mark Realized; Bounce. Negative: bounce a cash row; change status of a Realized cheque; status date in the future. Boundary: post-dated vs today cheque. A green run asserts only the toast, not the changed status or the receivable.

## 12. Open questions
Q: Effect of Bounce on the outlet balance? | Default: invoice becomes outstanding again | Evidence: none.
Q: Allowed status transitions? | Default: P/L to R or B only | Evidence: none.

## 13. Sources
framework_atlas/flows/00660001; screens_db/DYL_202020.json; DB glb_pr_ins_instrument_status, snd_tr_dsd_deposit_slip_dtl; snd_menu_outline.md.
