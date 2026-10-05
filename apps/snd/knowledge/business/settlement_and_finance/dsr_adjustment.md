---
option: DSR Adjustment Amount
area: settlement_and_finance
doc_types: [AD-07]
screens: [DSR_ADJUSTMENT_AMOUNT]
framework_flows: ["00670001"]
markets: [PK]
roles: [Maker]
depends_on: [route_settlement]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-05
---

# DSR adjustment amount: manual correction of a DSR balance (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas and the snd-schema DB. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Last updated: 2026-10-01. Source flow: 00670001 (seq 56). No live replay. (superseded 2026-10-05: screen opened live in G11-2b; seq 56 BYPASSED by the QA lead, values typed and discarded, nothing saved.)
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.

## 1. Purpose
Lets finance post a manual amount against a DSR/PJP (for example a shortage or a write-off) with a comment, so the DSR's account balances after route settlement. [inferred from doc type names]
- G11-2b: the screen shows, per delivery PJP, a running **Total Shortage Amount**, **Total Adjusted Amount** and **Balance Amount** (= Shortage - Adjusted); an adjustment is entered against the selected PJP [observed 2026-10-05 G11-2b].

## 2. Actors and roles
Auto_Multi_Orga (same session) [db]. No approver in the flow; the document status list suggests an Authorized / Un-Authorized state (below).
- G11-2b: opened by the Maker Auto_Multi_Orga; seq 56 bypassed in the group 11 walk [stated 2026-10-05 QA lead].

## 3. Documents and master data
Document type AD-07 "DSR ADUSTMENT MANUAL" (abrv ADJ MANAUL, active, group RA); related AD-04 "DSR Shortage Amount" and AD-06 "Dsr Adj (SKU Wise)" are inactive [db]. Statuses of AD-07: 01 Authorized, 02 Un-Authorized, 03 Adjustment, 04 Cancelled [db]. Needs a PJP (DSR) row to adjust.
- G11-2b: the menu search "Adjustment" offers three items: Stock Adjustment SAN (DYL_201045), DSR Adjustment (DYL_201065) and **DSR Adjustment Amount** (DSR_ADJUSTMENT_AMOUNT) = the framework's option [observed 2026-10-05 G11-2b].

## 4. Inputs: screens and fields
Menu: Transaction > Receivable > DSR Adjustment Amount (`DSR_ADJUSTMENT_AMOUNT`, /content-master/mobility/dsr-adjustment-amount-wise) [db]. Screen 006701: grid with filter checkbox and PJP description row; popup (`SavePopUp`, `popUpSaveBtn`) with **Amount** and **Comments**. Screen 006702 (detail tab) shows Amount and the document type [db].
- G11-2b live layout [observed 2026-10-05 G11-2b]: tabs Header / Detail. Header grid "DSR Adjustment": PJP Code, PJP Description, Total Shortage Amount, Total Adjusted Amount, Balance Amount. Entry panel: **Document Date** (default today), **Amount** (pre-filled from the Balance), **Comments**, button Save. Row 02112 AutomationDSR on 2026-10-05: 2,477,571.11 / 1,649,970.43 / 827,600.68.
- Workbook (NG_Dcode_QA_OTC (Pak)): Amount 400, Comments AUTO; Detail check Amount "PKR 14,796.99" for 2026-09-21 [db: workbook].

## 5. Process
1. [Maker] Open DSR Adjustment Amount; filter and select the PJP row. trace 11:56:00670001
2. [Maker] Open the popup, enter Amount and Comments, Save; assert toast from sheet DSR_ADJ_AMOUNT_ASSR.
3. [Maker] Open the Detail tab and verify the Amount equals what was entered (value validation).

G11-2b (2026-10-05, bypassed) [observed 2026-10-05 G11-2b]:
1. [Maker] Navigate to DSR Adjustment Amount; Select row 02112 (11:56:00670001).
2. [Maker] Enter Amount 400 and Comments AUTO (workbook values); **not saved** (QA lead bypassed seq 56) [stated 2026-10-05 QA lead].

## 6. Outputs and effects
An adjustment document (AD-07) against the PJP and an amount shown on the Detail tab; its effect on route settlement payable/received is [unknown] (default: increases or decreases cash shortage).
- G11-2b: no adjustment saved, so the effect is still [unknown]. Observed context: 02112's Total Shortage 2,477,571.11 is large although its route settlements show Cash Shortage 0; what it accumulates is [unknown] (Q-DJ1) [observed 2026-10-05 G11-2b].

## 7. Statuses and transitions
| from | action | to | tag |
|---|---|---|---|
| new | Save | 02 Un-Authorized or 01 Authorized | [unknown which] |
| any | adjust / cancel | 03 / 04 | [db names, rules unknown] |

## 8. Rules and validations
Amount and Comments are mandatory [inferred from toast]; no regex declared in sources.
- G11-2b: Balance Amount = Total Shortage Amount - Total Adjusted Amount (2,477,571.11 - 1,649,970.43 = 827,600.68) [observed 2026-10-05 G11-2b].

## 9. Messages
Historic atlas toast: "Please fill all the values" (x3) on 006701 when the popup is saved incomplete [db: atlas].
- G11-2b: none (nothing saved) [observed 2026-10-05 G11-2b].

## 10. Dependencies
Reads a PJP/DSR from the daily plan. Runs after Route Settlement (seq 51) in the cycle; whether it must run before is [unknown].

## 11. Test design hints
Positive: positive amount with comment. Negative: empty Amount, empty Comments (expect "Please fill all the values"), zero, non-numeric, negative. Boundary: large amount, two decimals. A green run checks the toast and the detail amount only; not the balance effect.
- G11-2b additions [observed 2026-10-05 G11-2b]:
  - Positive (when allowed): save 400 on 02112; assert Total Adjusted +400 and Balance -400, and the Detail amount.
  - Trap (framework drift): the workbook Detail check expects "PKR 14,796.99" for document date 2026-09-21; the date and amount are stale (see FRAMEWORK_DRIFT.md).
  - Trap: three menu items contain "Adjustment"; the framework's option is DSR Adjustment Amount.

## 12. Open questions
Q: Can the amount be negative? | Default: yes (sign decides debit/credit) | Evidence: none.
Q: Is the adjustment auto-Authorized? | Default: yes, single-step | Evidence: no approval flow row.
Q: Is the Amount field maximum-limited? | Default: none | Evidence: none.
- Q-DJ1: What does a PJP's Total Shortage Amount accumulate (02112: 2,477,571.11 while its route settlements show Cash Shortage 0)? | Default: sum of all historical shortages of the PJP across environments' test runs; do not assert it absolutely | Class: B | Evidence: header grid 2026-10-05 [observed 2026-10-05 G11-2b].
- Q53 (auto-authorized) still open: nothing was saved.

## 13. Sources
framework_atlas/flows/00670001; group_11.md; DB snd_pr_dot_documenttype, snd_pr_dos_documentstatus; snd_menu_outline.md.
- G11-2b: learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md (seq 56).
