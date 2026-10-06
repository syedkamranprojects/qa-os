---
option: Delivery Date Change
area: order_to_delivery_planning
doc_types: [CM-01]
screens: [DYL_201080]
framework_flows: ["00160001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [order_booking, stock_allocation]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-06
---
# Delivery Date Change: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)
Last updated: 2026-10-01. Source flow: 00160001 (group 11 seq 19).
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.

## 1. Purpose
Moves the promised delivery date of booked orders (cash memos) to another day, in bulk for one PJP, so the distributor can plan the delivery run (GIN) for a different day. [inferred from labels] It sits between booking/allocation and the GIN; the GIN picks orders by delivery date. [observed: GIN header needs a Delivery Date]
- Business meaning confirmed 2026-10-01: an order booked today is planned for the PJP's next delivery visit (10-07); Delivery Date Change pulls it forward to today so the GIN can issue it today. (upgraded: [observed 2026-10-01 G11-1], was [inferred])
- G11-3: **run before Order Editing** (seq 15), not only before the GIN: "change the delivery date BEFORE Order Editing" [stated 2026-10-06 QA Team Lead].

## 2. Actors and roles
Auto_Multi_Orga, same session as order booking. [observed]
- Maker = Auto_Multi_Orga. [observed 2026-10-01 G11-1]
- Checker: no role (no approval step). [observed 2026-10-01 G11-1]

## 3. Documents and master data
Order cash memos; the delivery date column `tcmm_delivery_date` and the delivery PJP (`epjp_pjpno_daily_delivery`, `epjp_sr_no_daily_delivery`) [db]. PJP master (route calendar).
- The delivery route is a separate PJP: orders booked on PJP 02111 carry **PJP Delivery No 02112** (02112-AutomationDSR, the GIN's Delivery Man PJP). [observed 2026-10-01 G11-1]
- Demand Channel of the listed orders: "01 - Back Office (BO)". [observed 2026-10-01 G11-1]

## 4. Inputs: screens and fields
Menu "Delivery Date Change", option DYL_201080, layout 201080. Fields: **Order Date** (date), **Delivery Date** (date), **PJP Number** (dropdown). Grid: Cashmemo No, Document Date, Delivery Date, Demand Channel, Outlet Name, PJP Number, PJP Delivery No, Amount FCY, Status; header checkbox selects all (`Header_0_checkbox_1`). Buttons: Process (`notrefresh`), Save changes, Discard changes. [atlas/step_labels/observed]
- Live 2026-10-01: menu Transaction > Delivery Date Change. Opens with Order Date = today, **Delivery Date = the NEW date** (default today), PJP Number = the first PJP (AUTO241602~Auto917248). Only button visible: **Process**. [observed 2026-10-01 G11-1]
- Grid (after choosing PJP 02111~AutomationOB1): checkbox, Cashmemo No, Outlet Name, Status (Confirmed), Document Date, Amount FCY, PJP Number 02111, PJP Delivery No 02112, Delivery Date (current, 2026-10-07), Demand Channel. It lists the PJP's open orders of that Order Date; the cancelled order is not listed. [observed 2026-10-01 G11-1]

## 5. Process: the business steps in order
1. [Maker] Navigate to Delivery Date Change. (`11:19:00160001`)
2. [Maker] Choose Order Date (today). **Changing Order Date resets the PJP to another one**, so choose PJP = 02111~AutomationOB1 after the date. [observed] (`11:19:00160001`)
3. [Maker] Choose Delivery Date (the new date). (`11:19:00160001`) (2026-10-01: left at the default today. [observed 2026-10-01 G11-1])
4. [Maker] Select all rows (header checkbox), Click Process, Accept the alert. -> "Delivery Date has been changed successfully, processed orders: 9". [observed] (`11:19:00160001`) Live 2026-10-01: confirm **"Are you sure you want to proceed?"** -> toast **"Delivery Date has been changed successfully, processed orders: 5"**. [observed 2026-10-01 G11-1]
5. Wait 5 s (framework). Assertion key DELIVERYDATE_CHNG_ASSR.
6. [Maker] Verify the grid Delivery Date now shows the new date (2026-10-01) and Status still Confirmed. [observed 2026-10-01 G11-1] (`11:19:00160001`)

G11-2 walk (2026-10-05) [observed 2026-10-05 G11-2]: [Maker] PJP 02111~AutomationOB1, 5 orders (2009-2013, all Confirmed, PJP Delivery No 02112, delivery 2026-10-11); new date 2026-10-05 (default); header checkbox; Process; confirm "Are you sure you want to proceed?" -> "Delivery Date has been changed successfully, processed orders: 5"; grid shows 2026-10-05 for all five (11:19:00160001).
G11-3 walk (2026-10-06, run before seq 15 on the QA Team Lead's instruction) [observed 2026-10-06 G11-3]:
1. [Maker] Delivery Date Change: PJP 02111, order date today, new delivery 2026-10-06; select all 6 orders; Process -> alert "Are you sure you want to proceed?" accept -> "Delivery Date has been changed successfully, processed orders: 6"; 2015-2020 delivery 2026-10-06, Confirmed (11:19:00160001, executed early).

## 6. Outputs and effects
Selected orders carry the new Delivery Date (and probably a new delivery PJP number) [inferred]; the count "processed orders: 9" covers 8 new + 1 older order of that PJP. [observed] The run used here did not verify the new date in Transaction Inquiry. [unknown]
- 2026-10-01: 5 orders (COL26000002003-2007) moved 2026-10-07 -> 2026-10-01; the grid showed the new date at once and Transaction Inquiry later showed Delivery Date 2026-10-01 for all five. (new date in Transaction Inquiry upgraded: [observed 2026-10-01 G11-1], was [unknown])
- The GIN of the same day then offered **exactly these 5 orders** in Cash Memo Selection (cash memos whose delivery date = the GIN delivery date). [observed 2026-10-01 G11-1]
- The cancelled order COL26000002008 (cancelled before the change) kept 2026-10-07. [observed 2026-10-01 G11-1]
- PJP Delivery No stayed 02112 (same delivery route, only the date moved). [observed 2026-10-01 G11-1]
- G11-2: confirmed on a second day: the GIN 507 Cash Memo Selection then offered exactly these 5 orders; the cancelled 2014 was not listed or moved [observed 2026-10-05 G11-2].
- G11-3: all six orders (incl. 2017, cancelled later) moved 2026-10-12 -> 2026-10-06; status stayed Confirmed [observed 2026-10-06 G11-3].

## 7. Statuses and transitions
No document status change [inferred]; only the delivery date (and PJP delivery assignment) changes. (upgraded: [observed 2026-10-01 G11-1], was [inferred]: Status stays Confirmed after the change.)
| from | action | to | by | tag |
|---|---|---|---|---|
| Confirmed, delivery 10-07 | Process | Confirmed, delivery = new date (10-01) | Maker | [observed 2026-10-01 G11-1] |

## 8. Rules and validations
- PJP resets on Order Date change. [observed]
- All grid rows for the Order Date + PJP are processed when select-all is used. [observed] (Again 5 of 5 on 2026-10-01. [observed 2026-10-01 G11-1])
- Delivery date earlier than order date / in the past: [unknown]. The workbook dates (2026-09-21) were stale vs today 2026-09-29, so the dates must be updated before a run. [observed]
- Whether allocated orders can be moved: yes (9 processed after allocation). [observed] (Again: 5 FULL-allocated orders moved. [observed 2026-10-01 G11-1])
- Live baseline 2026-10-01: the 8 orders COL26000001995-2002 now carry Delivery Date 2026-09-30 (moved from the PJP date), cancelled orders 1986 and 1993 still carry 2026-10-05; Transaction Inquiry has no Delivery-PJP column, so the effect on the delivery PJP can only be read on the GIN (Delivery Man PJP 02112) [observed]. The change itself (Q29, Q30) was not re-run. (superseded 2026-10-01: re-run live at seq 19, see sections 5-6. [observed 2026-10-01 G11-1])
- Cancelled orders are not listed and are not moved. [observed 2026-10-01 G11-1]
- **Same-day GIN needs delivery date = today**: the GIN refuses cash memos with a delivery date earlier than the PJP working date, and Cash Memo Selection only offers cash memos whose delivery date = the GIN delivery date. [observed 2026-10-01 G11-1 + earlier finding]
- The header Delivery Date is the NEW date, not a filter (the grid is chosen by Order Date + PJP). [observed 2026-10-01 G11-1]
- G11-2: PJP Delivery No stayed 02112; status stayed Confirmed (second day) [observed 2026-10-05 G11-2].

## 9. Messages
"Delivery Date has been changed successfully, processed orders: 9" (key DELIVERYDATE_CHNG_ASSR); confirmation alert (text [unknown]; accepted via browser). [observed]
- 2026-10-01: confirm **"Are you sure you want to proceed?"** (upgraded: [observed 2026-10-01 G11-1], was [unknown]); toast **"Delivery Date has been changed successfully, processed orders: 5"** (the count follows the rows selected). [observed 2026-10-01 G11-1]
- G11-2: confirm text and toast "processed orders: 5" confirmed on a second day [observed 2026-10-05 G11-2].
- G11-3: "Delivery Date has been changed successfully, processed orders: 6" [observed 2026-10-06 G11-3].

## 10. Dependencies
Reads orders from Order Booking. Hands the new Delivery Date to the GIN (Delivery Date must be typed on the GIN header; Cash Memo Selection listed 9 eligible cash memos). [observed]
- 2026-10-01: GIN 506 header Delivery Date typed 2026-10-01 -> Cash Memo Selection listed exactly the 5 moved orders; GIN 506 was then approved the same day (first successful GIN approval of the replay). [observed 2026-10-01 G11-1]
- Must run after cancellations that should not move (a cancelled order keeps its old date) and before the GIN. [observed 2026-10-01 G11-1]
- G11-2: Delivery Date Change is also the precondition for Order Editing (which lists only orders whose delivery date is today; see order_editing_cancellation.md) [observed 2026-10-05 G11-2].
- G11-3: precondition for Order Editing before the GIN (with Unallocate) [stated 2026-10-06 QA Team Lead]; group 11's order 15 -> 19 must be read as 19 -> 15 (FRAMEWORK_DRIFT.md).

## 11. Test design hints
- Positive: move one PJP's orders from 2026-10-05 to today; verify Delivery Date in Transaction Inquiry and the GIN selection.
- Negative: no row selected then Process; delivery date before order date; PJP not selected.
- Boundary: delivery date = order date; far future date; PJP with zero orders.
- Traps: the count message proves the number processed, not the date; reset of PJP on date change makes a silently empty grid.
- New 2026-10-01 [observed 2026-10-01 G11-1]:
  - Assert the count in the toast equals the number of ticked rows (5 today, 9 on 09-29): never hard-code the workbook's count.
  - Assert Status stays Confirmed and PJP Delivery No unchanged; assert the GIN Cash Memo Selection shows exactly the moved orders.
  - Trap: the confirm dialog "Are you sure you want to proceed?" must be accepted; without it nothing is processed and no toast appears. The same confirm text is used by Stock Allocation, Unallocate and Cashmemo Reschedule, so a generic "accept confirm" step works for all four.
  - Trap: the header Delivery Date is the target date; on Cashmemo Reschedule (a similar screen) changing it reloads the grid and clears the selection, so set the date FIRST, then tick rows.
  - Trap: a Delivery Date Change run after a cancellation does not list the cancelled order; a test that expects "processed orders: N" must subtract cancellations.
- G11-2: past-date refusal (Q29) still not tried; the 10-11 -> 10-05 move is a second positive data point [observed 2026-10-05 G11-2].
- G11-3 trap (framework drift): seq 19 sits after seq 15 in group 11; on cnr1dev1 it must run first [stated 2026-10-06 QA Team Lead].

## 12. Open questions (batched for the BA)
- Q: Which delivery date should orders have before the GIN (today or the PJP's date 2026-10-05)? | Default: today | Evidence: draft question 3. (ANSWERED 2026-10-01 G11-1 for the same-day cycle: today; the GIN refuses earlier dates and offers only cash memos with delivery date = the GIN delivery date. [observed])
- Q: Are past dates refused? | Default: refused | Class: B | Evidence: not tested.
- Q: Does the change also move the delivery PJP? | Default: yes if the new date maps to another visit | Evidence: column PJP Delivery No only on this screen; Transaction Inquiry has no such column (live 2026-10-01), read it on the GIN. (Update 2026-10-01 G11-1: moving 10-07 -> 10-01 kept PJP Delivery No 02112 [observed]; a move to a date of another route not tried. | Class: B)
- G11-2: no answer for the past-date or delivery-PJP questions (Q29, Q30 stay open/PARTLY).
- G11-3: fourth data point for the delivery date (10-06 booking -> 10-12); Q29, Q30 unchanged.

## 13. Sources
atlas flow 00160001, group_11.md; ui.md "Delivery Date Change"; STEP_SHEET_DRAFT_next.md row 19; step_labels "Delivery Date Change"; DB `snd_tr_cmm_cashmemo_master` columns.
- Live learning session G11-1 (2026-10-01, cnr1dev1, distributor 15108843): `learning_sessions/2026-10-01_G11-PK_session1_log.md` seq 19, 20 (GIN selection), 23, "Transaction Inquiry after GIN approval"; `learning_sessions/2026-10-01_G11-PK_session1_report.md` §3 rule 5.
- G11-2: learning_sessions/2026-10-05_G11-PK_session2_log.md (seq 19).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 15, 19).
