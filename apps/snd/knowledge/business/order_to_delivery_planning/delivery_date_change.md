# Delivery Date Change: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flow: 00160001 (group 11 seq 19).

## 1. Purpose
Moves the promised delivery date of booked orders (cash memos) to another day, in bulk for one PJP, so the distributor can plan the delivery run (GIN) for a different day. [inferred from labels] It sits between booking/allocation and the GIN; the GIN picks orders by delivery date. [observed: GIN header needs a Delivery Date]

## 2. Actors and roles
Auto_Multi_Orga, same session as order booking. [observed]

## 3. Documents and master data
Order cash memos; the delivery date column `tcmm_delivery_date` and the delivery PJP (`epjp_pjpno_daily_delivery`, `epjp_sr_no_daily_delivery`) [db]. PJP master (route calendar).

## 4. Inputs: screens and fields
Menu "Delivery Date Change", option DYL_201080, layout 201080. Fields: **Order Date** (date), **Delivery Date** (date), **PJP Number** (dropdown). Grid: Cashmemo No, Document Date, Delivery Date, Demand Channel, Outlet Name, PJP Number, PJP Delivery No, Amount FCY, Status; header checkbox selects all (`Header_0_checkbox_1`). Buttons: Process (`notrefresh`), Save changes, Discard changes. [atlas/step_labels/observed]

## 5. Process: the business steps in order
1. [Order User] Navigate to Delivery Date Change. (`11:19:00160001`)
2. Choose Order Date (today). **Changing Order Date resets the PJP to another one**, so choose PJP = 02111~AutomationOB1 after the date. [observed]
3. Choose Delivery Date (the new date).
4. Select all rows (header checkbox), click Process, accept the alert. -> "Delivery Date has been changed successfully, processed orders: 9". [observed]
5. Wait 5 s (framework). Assertion key DELIVERYDATE_CHNG_ASSR.

## 6. Outputs and effects
Selected orders carry the new Delivery Date (and probably a new delivery PJP number) [inferred]; the count "processed orders: 9" covers 8 new + 1 older order of that PJP. [observed] The run used here did not verify the new date in Transaction Inquiry. [unknown]

## 7. Statuses and transitions
No document status change [inferred]; only the delivery date (and PJP delivery assignment) changes.

## 8. Rules and validations
- PJP resets on Order Date change. [observed]
- All grid rows for the Order Date + PJP are processed when select-all is used. [observed]
- Delivery date earlier than order date / in the past: [unknown]. The workbook dates (2026-09-21) were stale vs today 2026-09-29, so the dates must be updated before a run. [observed]
- Whether allocated orders can be moved: yes (9 processed after allocation). [observed]
- Live baseline 2026-10-01: the 8 orders COL26000001995-2002 now carry Delivery Date 2026-09-30 (moved from the PJP date), cancelled orders 1986 and 1993 still carry 2026-10-05; Transaction Inquiry has no Delivery-PJP column, so the effect on the delivery PJP can only be read on the GIN (Delivery Man PJP 02112) [observed]. The change itself (Q29, Q30) was not re-run.

## 9. Messages
"Delivery Date has been changed successfully, processed orders: 9" (key DELIVERYDATE_CHNG_ASSR); confirmation alert (text [unknown]; accepted via browser). [observed]

## 10. Dependencies
Reads orders from Order Booking. Hands the new Delivery Date to the GIN (Delivery Date must be typed on the GIN header; Cash Memo Selection listed 9 eligible cash memos). [observed]

## 11. Test design hints
- Positive: move one PJP's orders from 2026-10-05 to today; verify Delivery Date in Transaction Inquiry and the GIN selection.
- Negative: no row selected then Process; delivery date before order date; PJP not selected.
- Boundary: delivery date = order date; far future date; PJP with zero orders.
- Traps: the count message proves the number processed, not the date; reset of PJP on date change makes a silently empty grid.

## 12. Open questions (batched for the BA)
- Q: Which delivery date should orders have before the GIN (today or the PJP's date 2026-10-05)? | Default: today | Evidence: draft question 3.
- Q: Are past dates refused? | Default: refused | Evidence: not tested.
- Q: Does the change also move the delivery PJP? | Default: yes if the new date maps to another visit | Evidence: column PJP Delivery No only on this screen; Transaction Inquiry has no such column (live 2026-10-01), read it on the GIN.

## 13. Sources
atlas flow 00160001, group_11.md; ui.md "Delivery Date Change"; STEP_SHEET_DRAFT_next.md row 19; step_labels "Delivery Date Change"; DB `snd_tr_cmm_cashmemo_master` columns.
