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
updated: 2026-10-08
---

# DSR adjustment amount: manual correction of a DSR balance (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas and the snd-schema DB. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Last updated: 2026-10-01. Source flow: 00670001 (seq 56). No live replay. (superseded 2026-10-05: screen opened live in G11-2b; seq 56 BYPASSED by the QA lead, values typed and discarded, nothing saved.)
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.
Updated 2026-10-08: merged the QA team's written answers to the 2026-10-06 review (learning_sessions/2026-10-06_G11-PK_QA_Team_Review.docx); evidence learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx). Tag [stated 2026-10-08 QA Team] = written answer of the QA team. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08: ...)".
(superseded 2026-10-06: seq 56 was SAVED for the first time in G11-3, Amount 400 / AUTO, document COL26000000211.)

## 1. Purpose
Lets finance post a manual amount against a DSR/PJP (for example a shortage or a write-off) with a comment, so the DSR's account balances after route settlement. [inferred from doc type names] (superseded 2026-10-06: it records a **DSR shortage** found while the DSR collects money from the outlet (a charge to the DSR, not a write-off) [stated 2026-10-06 QA Team Lead].)
- G11-2b: the screen shows, per delivery PJP, a running **Total Shortage Amount**, **Total Adjusted Amount** and **Balance Amount** (= Shortage - Adjusted); an adjustment is entered against the selected PJP [observed 2026-10-05 G11-2b].
- G11-3: a saved adjustment **adds to the PJP's Total Shortage** (400 -> Total Shortage +400, Balance +400, Total Adjusted unchanged) [observed 2026-10-06 G11-3]; so a manual DSR adjustment looks like a charge to the DSR, not a write-off [inferred; meaning to be confirmed, Q-DJ1]. (superseded 2026-10-06: **DSR Adjustment Amount records a shortage of the DSR that arises while he collects (takes) money from the outlet**, i.e. a charge to the DSR: "yes, it is DSR shortage while taking amount from outlet" [stated 2026-10-06 QA Team Lead; Q-DJ1 answered]; it increases Total Shortage and Balance, not Total Adjusted, matching the observed +400.)
- QA team 2026-10-08 (Q-GRN1): on **GRN approval** the system automatically creates the DSR adjustment amount for a stock shortage (suggested quantity in UOM minus actual returned quantity), which is then shown on Route Settlement [stated 2026-10-08 QA Team]. So DSR shortages come from two sources: the stock shortage created by the GRN and the manual DSR Adjustment Amount [inferred combination].
- QA team 2026-10-08 (rule 20): "it couldn't be allowed to change the stock shortage" [stated 2026-10-08 QA Team]: the stock shortage cannot be changed by the user (scope of the remark not fully clear; read as: a GRN-generated stock shortage is not editable here).

## 2. Actors and roles
Auto_Multi_Orga (same session) [db]. No approver in the flow; the document status list suggests an Authorized / Un-Authorized state (below).
- G11-2b: opened by the Maker Auto_Multi_Orga; seq 56 bypassed in the group 11 walk [stated 2026-10-05 QA lead].
- G11-3: saved by the Maker Auto_Multi_Orga with the workbook values 400 / AUTO on the QA Team Lead's instruction [stated 2026-10-06 QA Team Lead]; no approval step appeared [observed 2026-10-06 G11-3].

## 3. Documents and master data
Document type AD-07 "DSR ADUSTMENT MANUAL" (abrv ADJ MANAUL, active, group RA); related AD-04 "DSR Shortage Amount" and AD-06 "Dsr Adj (SKU Wise)" are inactive [db]. Statuses of AD-07: 01 Authorized, 02 Un-Authorized, 03 Adjustment, 04 Cancelled [db]. Needs a PJP (DSR) row to adjust.
- G11-2b: the menu search "Adjustment" offers three items: Stock Adjustment SAN (DYL_201045), DSR Adjustment (DYL_201065) and **DSR Adjustment Amount** (DSR_ADJUSTMENT_AMOUNT) = the framework's option [observed 2026-10-05 G11-2b].

## 4. Inputs: screens and fields
Menu: Transaction > Receivable > DSR Adjustment Amount (`DSR_ADJUSTMENT_AMOUNT`, /content-master/mobility/dsr-adjustment-amount-wise) [db]. Screen 006701: grid with filter checkbox and PJP description row; popup (`SavePopUp`, `popUpSaveBtn`) with **Amount** and **Comments**. Screen 006702 (detail tab) shows Amount and the document type [db].
- G11-2b live layout [observed 2026-10-05 G11-2b]: tabs Header / Detail. Header grid "DSR Adjustment": PJP Code, PJP Description, Total Shortage Amount, Total Adjusted Amount, Balance Amount. Entry panel: **Document Date** (default today), **Amount** (pre-filled from the Balance), **Comments**, button Save. Row 02112 AutomationDSR on 2026-10-05: 2,477,571.11 / 1,649,970.43 / 827,600.68.
- G11-3: row 02112 on 2026-10-06 before saving: 2,477,571.11 / 1,649,970.43 / 827,600.68 (unchanged since 10-05; the 10-06 settlement with Cash Shortage 0 did not change it). Click the row -> Amount prefilled 827600.68 (= Balance) [observed 2026-10-06 G11-3]. Save opens a confirm modal **"Are you sure you want to save transaction?"** (button Save changes) [observed 2026-10-06 G11-3]. Detail tab columns: Document No, date, PJP, Comments, Amount, Document Type (blank) [observed 2026-10-06 G11-3].
- Workbook (NG_Dcode_QA_OTC (Pak)): Amount 400, Comments AUTO; Detail check Amount "PKR 14,796.99" for 2026-09-21 [db: workbook].

## 5. Process
1. [Maker] Open DSR Adjustment Amount; filter and select the PJP row. trace 11:56:00670001
2. [Maker] Open the popup, enter Amount and Comments, Save; assert toast from sheet DSR_ADJ_AMOUNT_ASSR.
3. [Maker] Open the Detail tab and verify the Amount equals what was entered (value validation).

G11-2b (2026-10-05, bypassed) [observed 2026-10-05 G11-2b]:
1. [Maker] Navigate to DSR Adjustment Amount; Select row 02112 (11:56:00670001).
2. [Maker] Enter Amount 400 and Comments AUTO (workbook values); **not saved** (QA lead bypassed seq 56) [stated 2026-10-05 QA lead].

G11-3 (2026-10-06, saved) [observed 2026-10-06 G11-3]:
1. [Maker] Navigate to DSR Adjustment Amount; Verify row 02112 2,477,571.11 / 1,649,970.43 / 827,600.68; Select the row (11:56:00670001).
2. [Maker] Replace Amount 827600.68 with **400**; Enter Comments **AUTO**; Document Date 2026-10-06.
3. [Maker] Click Save -> confirm "Are you sure you want to save transaction?" -> Save changes -> **"Record Saved Successfully"**.
4. [Maker] Verify header row 02112: Total Shortage **2,477,971.11** (+400), Total Adjusted 1,649,970.43 (unchanged), Balance **828,000.68** (+400).
5. [Maker] Open the Detail tab; Verify one row Document No **COL26000000211**, 2026-10-06, 02112, Comments AUTO, Amount 400 (Document Type blank).

## 6. Outputs and effects
An adjustment document (AD-07) against the PJP and an amount shown on the Detail tab; its effect on route settlement payable/received is [unknown] (default: increases or decreases cash shortage). (superseded 2026-10-06: it adds to the PJP's Total Shortage and Balance on this screen [observed 2026-10-06 G11-3; meaning stated 2026-10-06 QA Team Lead]; no effect on the already Complete Route Settlement row was seen.)
- G11-2b: no adjustment saved, so the effect is still [unknown]. Observed context: 02112's Total Shortage 2,477,571.11 is large although its route settlements show Cash Shortage 0; what it accumulates is [unknown] (Q-DJ1) [observed 2026-10-05 G11-2b]. (superseded 2026-10-06: Total Shortage accumulates the manual DSR shortages entered here (every replay adds 400) [stated 2026-10-06 QA Team Lead; observed +400]; the large amount = many earlier runs [inferred].)
- G11-3: saving 400 created adjustment document **COL26000000211** (number in the COL260000... series, like returns) and moved the header: **Total Shortage +400 -> 2,477,971.11; Total Adjusted unchanged 1,649,970.43; Balance +400 -> 828,000.68** [observed 2026-10-06 G11-3]. (superseded 2026-10-06: the G11-2b hint "assert Total Adjusted +400 and Balance -400" was wrong for this screen.) Whether this is the intended meaning (charge to the DSR vs adjustment of the shortage) is open (Q-DJ1, BA12). (superseded 2026-10-06: intended; it is a DSR shortage arising while taking the amount from the outlet [stated 2026-10-06 QA Team Lead; Q-DJ1 answered].)
- G11-3: no effect on Route Settlement of the same day (the route was already Complete) [observed 2026-10-06 G11-3].

## 7. Statuses and transitions
| from | action | to | tag |
|---|---|---|---|
| new | Save | 02 Un-Authorized or 01 Authorized | [unknown which] |
| any | adjust / cancel | 03 / 04 | [db names, rules unknown] |
| new | Save (confirm modal) | saved directly, listed on the Detail tab; no approval step seen (status column not shown) | [observed 2026-10-06 G11-3]; Authorized vs Un-Authorized still [unknown] (Q53) |
- QA team 2026-10-08 (Q53): **there is no workflow on the DSR adjustment document** [stated 2026-10-08 QA Team]: it is final at Save (no approval); answers Q53, consistent with the observed direct save [observed 2026-10-06 G11-3]. (superseded 2026-10-08: "02 Un-Authorized or 01 Authorized [unknown which]" - no approval step exists; the stored status code itself is still not read.)

## 8. Rules and validations
Amount and Comments are mandatory [inferred from toast]; no regex declared in sources.
- G11-2b: Balance Amount = Total Shortage Amount - Total Adjusted Amount (2,477,571.11 - 1,649,970.43 = 827,600.68) [observed 2026-10-05 G11-2b].
- G11-3: Balance = Shortage - Adjusted still holds after the save (2,477,971.11 - 1,649,970.43 = 828,000.68) [observed 2026-10-06 G11-3].
- G11-3: an adjustment amount is added to Total Shortage, not to Total Adjusted [observed 2026-10-06 G11-3].
- G11-3: the Amount field is prefilled with the Balance; it must be replaced (select all, then type) [observed 2026-10-06 G11-3].
- QA team 2026-10-08 (BA12, settlement adjustment types) [stated 2026-10-08 QA Team]: **Cash**: the receivable can be reduced but cannot become negative; the difference shows in the Cash Shortage column. **Cheque**: the cheque amount cannot be modified. **Stock shortage**: generated when the DSR returns the remaining stock to the warehouse; expected GRN qty = GIN qty - delivered order qty + picked sales return qty; the warehouse in-charge enters the actual received qty; the difference is the Stock Shortage.
- QA team 2026-10-08 (rule 20): the stock shortage cannot be changed [stated 2026-10-08 QA Team].

## 9. Messages
Historic atlas toast: "Please fill all the values" (x3) on 006701 when the popup is saved incomplete [db: atlas].
- G11-2b: none (nothing saved) [observed 2026-10-05 G11-2b].
- G11-3: **"Are you sure you want to save transaction?"** (confirm modal, button Save changes) and **"Record Saved Successfully"** after confirming [observed 2026-10-06 G11-3].

## 10. Dependencies
Reads a PJP/DSR from the daily plan. Runs after Route Settlement (seq 51) in the cycle; whether it must run before is [unknown].
- G11-3: run after the route was settled and before the day close (settlement -> DSR adjustment -> day close), as planned with the QA Team Lead [observed 2026-10-06 G11-3]; whether it is allowed after the day close is [unknown].

## 11. Test design hints
Positive: positive amount with comment. Negative: empty Amount, empty Comments (expect "Please fill all the values"), zero, non-numeric, negative. Boundary: large amount, two decimals. A green run checks the toast and the detail amount only; not the balance effect.
- G11-2b additions [observed 2026-10-05 G11-2b]:
  - Positive (when allowed): save 400 on 02112; assert Total Adjusted +400 and Balance -400, and the Detail amount.
  - Trap (framework drift): the workbook Detail check expects "PKR 14,796.99" for document date 2026-09-21; the date and amount are stale (see FRAMEWORK_DRIFT.md).
  - Trap: three menu items contain "Adjustment"; the framework's option is DSR Adjustment Amount.
- G11-3 additions [observed 2026-10-06 G11-3]:
  - Positive: save 400 / AUTO on 02112 -> confirm modal -> "Record Saved Successfully"; assert **Total Shortage +400, Balance +400, Total Adjusted unchanged** (supersedes the G11-2b hint above) and the Detail row (Amount 400, Comments AUTO, today).
  - Trap: the Amount field is prefilled with the Balance (827,600.68); a replay that appends instead of replacing saves a huge amount.
  - Trap: every replay adds 400 to 02112's Total Shortage; assert deltas, never absolute values.
- QA team 2026-10-08 additions [stated 2026-10-08 QA Team]:
  - Positive: approve a GRN with Actual < expected -> a DSR adjustment for the stock shortage is created automatically (value = sale price x qty + tax %) and shows on Route Settlement; assert the PJP's Total Shortage delta [inferred link].
  - Negative: try to change a GRN-generated stock shortage -> not allowed.
  - No approval case exists for a DSR adjustment (no workflow).

## 12. Open questions
Q: Can the amount be negative? | Default: yes (sign decides debit/credit) | Evidence: none.
Q: Is the adjustment auto-Authorized? | Default: yes, single-step | Evidence: no approval flow row.
Q: Is the Amount field maximum-limited? | Default: none | Evidence: none.
- Q-DJ1: What does a PJP's Total Shortage Amount accumulate (02112: 2,477,571.11 while its route settlements show Cash Shortage 0)? | Default: sum of all historical shortages of the PJP across environments' test runs; do not assert it absolutely | Class: B | Evidence: header grid 2026-10-05 [observed 2026-10-05 G11-2b].
- Q53 (auto-authorized) still open: nothing was saved.
- Q-DJ1 evidence 2026-10-06: saving 400 increased Total Shortage and Balance by 400, Total Adjusted unchanged [observed 2026-10-06 G11-3]. **-> ANSWERED 2026-10-06**: "yes, it is DSR shortage while taking amount from outlet": the option records a shortage of the DSR arising when he collects money from the outlet (a charge to the DSR), so it increases Total Shortage and Balance, not Total Adjusted [stated 2026-10-06 QA Team Lead]. BA12 (sign / debit-credit) is answered for a positive amount; a negative amount was not tried.
- Q53 evidence 2026-10-06: the save went through without any approval step and the row is listed at once on the Detail tab (status column not shown) [observed 2026-10-06 G11-3]; Authorized vs Un-Authorized not visible, still open.
- **Q53 ANSWERED 2026-10-08** [stated 2026-10-08 QA Team]: no workflow on the DSR adjustment document (no approval; final at Save).
- **BA12 ANSWERED 2026-10-08** [stated 2026-10-08 QA Team]: the adjustment types are cash (reducible, never negative, difference = Cash Shortage), cheque (not modifiable) and stock shortage (expected GRN qty = GIN - delivered + picked returns; difference to the warehouse's actual = Stock Shortage; GRN approval auto-creates the DSR adjustment). Residual not covered by the answer: what feeds **Total Adjusted** and whether a negative DSR Adjustment Amount is accepted; default: never assert Total Adjusted, never enter a negative amount (ask only if a case needs it).

## 13. Sources
framework_atlas/flows/00670001; group_11.md; DB snd_pr_dot_documenttype, snd_pr_dos_documentstatus; snd_menu_outline.md.
- G11-2b: learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md (seq 56).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 56, saved: COL26000000211, 400).

- QA team written answers 2026-10-08: learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx) (rule 20; BA12, Q53, Q-GRN1).
