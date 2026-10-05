---
option: Cheque Status
area: settlement_and_finance
doc_types: [deposit slip cheque detail]
screens: [DYL_202020]
framework_flows: ["00660001"]
markets: [PK]
roles: [Maker]
depends_on: [deposit_slips, route_settlement]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-05
---

# Cheque status: tracking a deposited cheque (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas and the snd-schema DB. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Last updated: 2026-10-01. Source flow: 00660001 (seq 55). No live replay. (superseded 2026-10-05: screen read live in G11-2b; seq 55 itself BYPASSED by the QA lead, nothing changed.)
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.

## 1. Purpose
Once cheques are banked on a deposit slip they are not yet money: the bank may realize or bounce them. Cheque Status lets finance mark each cheque with its outcome so the outlet's receivable is restored if it bounces. [inferred]
- G11-2b: the screen lists only **Posted** cheque slips; after posting at Route Settlement the cheques already read **"Clear"**; the only action offered is **Bounce** [observed 2026-10-05 G11-2b]. So in this environment a banked cheque is cleared by posting and Cheque Status is used only to bounce it [inferred].

## 2. Actors and roles
Auto_Multi_Orga (same session) [db]. No approver [db].
- G11-2b: read by the Maker Auto_Multi_Orga; seq 55 bypassed in the group 11 walk [stated 2026-10-05 QA lead]. Bounce was not pressed (one-way action) [observed].

## 3. Documents and master data
Works on deposit slip headers/details (`snd_tr_dsl_deposit_slip`; detail `pins_instrument_status`, `tdsd_instrument_status_date`) [db]. Instrument statuses for 010104 (glb_pr_ins_instrument_status): C Cancelled, P Presented, L Collected, B Bounced, R Realized, A Amendment [db].
- G11-2b: on screen the instrument status of today's cheques reads **"Clear"**, a value not in the db list above (C Cancelled, P, L, B, R, A) [observed 2026-10-05 G11-2b]; whether "Clear" maps to R Realized or C is [unknown] (contradiction 20 in OPEN_QUESTIONS.md).

## 4. Inputs: screens and fields
Menu: Transaction > Receivable > Cheque Status (`DYL_202020`) [db]. Grid: Serial No, Currency, Organization, Cheque No, Cheque Date, Amount, Cheque Status, Cheque Status Date; button **Bounce** [db]. Flow actions: filter checkbox, select deposit slip (header and row), tick the cheque row (`checkbox-1`, `row_1_cheque_no`), "notrefresh"; assert toast from sheet Cheque_Status_ASSR [db].
- G11-2b live layout [observed 2026-10-05 G11-2b]: menu Transaction > Receivable > Cheque Status. Top grid (Posted deposit slips only): Deposit Slip, PJP-DSR (empty), Current Date, Bank, Bank Branch, Status, Amount; 37 pages of history; "Show filter row" opens a filter row, the date filter applies on Enter. Detail grid per slip: Cheque No, Cheque Date, Amount, Cheque Status, Cheque Status Date. Only button: **Bounce**.

## 5. Process
1. [Maker] Open Cheque Status; filter. trace 11:55:00660001
2. [Maker] Select the deposit slip and the cheque row.
3. [Maker] Change Cheque Status or press Bounce and save; assert toast. [inferred: atlas shows only the row selection]

G11-2b (2026-10-05, read only) [observed 2026-10-05 G11-2b]:
1. [Maker] Open Cheque Status; Show filter row; filter Current Date 2026-10-05 (Enter) -> slips 1138 (119,370), 1140 (1,000), 1141 (1,000), all Posted (11:55:00660001).
2. [Maker] Select each slip; Verify cheques: 1138 -> 1234501 119,370; 1140 -> 12222 400, 1234567 100, 12444 200, 22337 300; 1141 -> 1234567 1,000; all Cheque Status Clear, Status Date 2026-10-05.
3. The framework step (select the cheque row, then an event after the selection) was not executed: the QA lead bypassed seq 55; "Realized" was requested but does not exist on the screen, and Bounce was excluded [stated 2026-10-05 QA lead].

## 6. Outputs and effects
Instrument status and date updated on the slip detail; a bounce presumably reopens the cash memo balance [inferred].
- G11-2b: no effect produced (bypassed). Observed state: posting at settlement set today's cheques to Clear with Status Date = settlement day [observed 2026-10-05 G11-2b; set-by-posting inferred].

## 7. Statuses and transitions
| from | action | to | tag |
|---|---|---|---|
| P / L | bank clears | R Realized | [inferred] |
| P / L | Bounce button | B Bounced | [db button, target inferred] |
| any | cancel | C Cancelled | [inferred] |
Allowed transitions: [unknown].
- G11-2b: observed status after posting = **Clear**; only transition offered on screen = **Bounce** (not executed) [observed 2026-10-05 G11-2b]. Realized/Presented/Collected are not offered.

## 8. Rules and validations
None declared beyond the status master [unknown]. The slip detail table has 0 rows in this DB, so status usage is unobserved.
- G11-2b: Un Posted cheque slips are not offered (10-01 slips 1132/1134/1135 absent) [observed 2026-10-05 G11-2b].
- G11-2b: duplicate cheque number 1234567 visible on two slips (1140, 1141) [observed 2026-10-05 G11-2b; Q-DS2].

## 9. Messages
Not recorded [unknown].
- G11-2b: no message seen (no action taken) [observed 2026-10-05 G11-2b].

## 10. Dependencies
Needs a cheque deposit slip (seq 40/42/44). Nothing downstream in group 11. Reports "Cheque For Realization" (`DYL_JR1007`) and Power BI "Cheque Details" read this status [db: menu].
- G11-2b: needs the cheque slip to be Posted, i.e. Route Settlement of its route/date first [observed 2026-10-05 G11-2b].

## 11. Test design hints
Positive: mark Realized; Bounce. Negative: bounce a cash row; change status of a Realized cheque; status date in the future. Boundary: post-dated vs today cheque. A green run asserts only the toast, not the changed status or the receivable.
- G11-2b additions [observed 2026-10-05 G11-2b]:
  - Positive: after settlement, today's cheques appear with Status Clear and Status Date = settlement day.
  - Negative: an Un Posted cheque slip is not listed.
  - Trap (framework drift): the old positive hint "mark Realized" cannot be executed: there is no Realized choice, only Bounce. Seq 55 as automated must either press Bounce (one-way, changes finance) or assert only a selection; see Q-CS1 and FRAMEWORK_DRIFT.md.
  - Trap: Bounce is one-way; never press it in a learning or regression walk unless the case is about bouncing.

## 12. Open questions
Q: Effect of Bounce on the outlet balance? | Default: invoice becomes outstanding again | Evidence: none.
Q: Allowed status transitions? | Default: P/L to R or B only | Evidence: none.
- Q (allowed transitions) PARTLY ANSWERED 2026-10-05: after posting the cheque is Clear; the screen offers only Bounce [observed 2026-10-05 G11-2b]. Bounce effect stays BA11.
- Q-CS1: Does framework seq 55 press Bounce (event after selecting the cheque row), and since "Realized" does not exist on the screen, what should seq 55 assert? | Default: seq 55 stays bypassed; do not press Bounce in group 11 | Class: C (QA lead / framework owner) | Evidence: screen offers only Bounce; QA lead asked for Realized [stated 2026-10-05 QA lead; observed 2026-10-05 G11-2b].

## 13. Sources
framework_atlas/flows/00660001; screens_db/DYL_202020.json; DB glb_pr_ins_instrument_status, snd_tr_dsd_deposit_slip_dtl; snd_menu_outline.md.
- G11-2b: learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md (seq 55).
