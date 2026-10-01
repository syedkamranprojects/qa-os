# DSR adjustment amount: manual correction of a DSR balance (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas and the snd-schema DB. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Last updated: 2026-10-01. Source flow: 00670001 (seq 56). No live replay.

## 1. Purpose
Lets finance post a manual amount against a DSR/PJP (for example a shortage or a write-off) with a comment, so the DSR's account balances after route settlement. [inferred from doc type names]

## 2. Actors and roles
Auto_Multi_Orga (same session) [db]. No approver in the flow; the document status list suggests an Authorized / Un-Authorized state (below).

## 3. Documents and master data
Document type AD-07 "DSR ADUSTMENT MANUAL" (abrv ADJ MANAUL, active, group RA); related AD-04 "DSR Shortage Amount" and AD-06 "Dsr Adj (SKU Wise)" are inactive [db]. Statuses of AD-07: 01 Authorized, 02 Un-Authorized, 03 Adjustment, 04 Cancelled [db]. Needs a PJP (DSR) row to adjust.

## 4. Inputs: screens and fields
Menu: Transaction > Receivable > DSR Adjustment Amount (`DSR_ADJUSTMENT_AMOUNT`, /content-master/mobility/dsr-adjustment-amount-wise) [db]. Screen 006701: grid with filter checkbox and PJP description row; popup (`SavePopUp`, `popUpSaveBtn`) with **Amount** and **Comments**. Screen 006702 (detail tab) shows Amount and the document type [db].

## 5. Process
1. [Maker] Open DSR Adjustment Amount; filter and select the PJP row. trace 11:56:00670001
2. [Maker] Open the popup, enter Amount and Comments, Save; assert toast from sheet DSR_ADJ_AMOUNT_ASSR.
3. [Maker] Open the Detail tab and verify the Amount equals what was entered (value validation).

## 6. Outputs and effects
An adjustment document (AD-07) against the PJP and an amount shown on the Detail tab; its effect on route settlement payable/received is [unknown] (default: increases or decreases cash shortage).

## 7. Statuses and transitions
| from | action | to | tag |
|---|---|---|---|
| new | Save | 02 Un-Authorized or 01 Authorized | [unknown which] |
| any | adjust / cancel | 03 / 04 | [db names, rules unknown] |

## 8. Rules and validations
Amount and Comments are mandatory [inferred from toast]; no regex declared in sources.

## 9. Messages
Historic atlas toast: "Please fill all the values" (x3) on 006701 when the popup is saved incomplete [db: atlas].

## 10. Dependencies
Reads a PJP/DSR from the daily plan. Runs after Route Settlement (seq 51) in the cycle; whether it must run before is [unknown].

## 11. Test design hints
Positive: positive amount with comment. Negative: empty Amount, empty Comments (expect "Please fill all the values"), zero, non-numeric, negative. Boundary: large amount, two decimals. A green run checks the toast and the detail amount only; not the balance effect.

## 12. Open questions
Q: Can the amount be negative? | Default: yes (sign decides debit/credit) | Evidence: none.
Q: Is the adjustment auto-Authorized? | Default: yes, single-step | Evidence: no approval flow row.
Q: Is the Amount field maximum-limited? | Default: none | Evidence: none.

## 13. Sources
framework_atlas/flows/00670001; group_11.md; DB snd_pr_dot_documenttype, snd_pr_dos_documentstatus; snd_menu_outline.md.
