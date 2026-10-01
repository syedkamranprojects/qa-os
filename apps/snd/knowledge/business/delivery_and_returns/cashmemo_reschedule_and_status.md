# Cashmemo Reschedule and Cashmemo Status: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: atlas `01040001` (group 11 seq 32), `00030001` (seq 33); also seq 29 `00840001` Order Editing After GIN and seq 31 `00850001` Order Cancellation After GIN. None of these has been replayed live yet (the GIN approval blocks the chain).

## 1. Purpose
A cash memo (document type `CM-01` "Sales", the confirmed order that is the delivery document) is delivered by the DSR. After the GIN, either the DSR could not deliver on the planned day (Cashmemo Reschedule moves it to another delivery date with a reason) or he reports the outcome of the day (Cashmemo Status records cash memos as delivered / not delivered). [inferred from names, execution statuses and screens]

## 2. Actors and roles
Maker = Stock Controller / order user `Auto_Multi_Orga` runs all four flows, no user switch in seq 29-33 [atlas]. No approval configured [atlas].

## 3. Documents and master data
- Cash memo `snd_tr_cmm_cashmemo_master`: document status 01 Delivered, 02 Un-Delivered, 03 Cancelled, 04 Ordered, 05 Amendment, 06 Re-attempt [db: snd_pr_dos_documentstatus CM-01, org 0101]. Execution status: 02 Confirmed, 03 Planning completed, 05 Cancelled, 10 Delivered/Invoiced, 13 Ready to dispatch/Packed, 18 Partial Delivered, 19 CM Reschedule, 20 CM BLOCKED [db: glb_pr_exs_execution_status]. Date columns `tcmm_delivery_date`, `tcmm_schdelv_date`, `tcmm_actual_delivery_time` [db].
- Live-verified 2026-10-01 [db]: execution status 02 "Confirmed" is a status of its own (identifier ALC) and 03 "Planning completed" follows it (identifier GIN); orders on GIN 505 read Planning completed [observed]. Reschedule Reason (datalist REASNCMRESCH, grid filter doc type CM-01 and identifier CNL): 0017 Shop Closed, 0018 Delivery is not possible due to any reason, 0019 Customer cancels delivery, 0021 customer refused, L02L01L01L01 Credit Exceeded, L02L02L03L01 Shop Closed, L02L03L04L01 Bad Weather, L02L03L04L02 Law & order Issue [db]: the reschedule list IS the cancellation list. The reason control is a column inside the grid row, so the dropdown could not be opened without an eligible order (search order date 2026-09-29, delivery 2026-09-30, PJP 02112: 0 rows) [observed].
- Delivery PJP of the cash memo: `epjp_pjpno_daily_delivery` [db]; GIN link via `snd_tr_gnm_gingrn_refinfo` [db].

## 4. Inputs: screens and fields
**Cashmemo Reschedule** (menu `Cashmemo Reschedule`, option DYL_202053) [atlas]: **Order Date*** (mandatory), **Delivery Date**, **PJP Number**. Grid: row filter GIN No (`REPO_GINNO`) and Outlet Code/Name, open the row (`pjp_delivery_no`), per-row dropdown **Reschedule Reason**, read **Amount FCY**, then the Process button and accept the alert [atlas].
**Cashmemo Status** (menu `Cashmemo Status`, option CASHMEMO-STATUS) [atlas]: **PJP Number** dropdown; grid shows **Gross Amount**, **Tax**, **Net Amount**; header checkbox selects all; **Save All** (`saveallBtn`) [atlas].

## 5. Process: the business steps in order
1. [Maker] Navigate to Cashmemo Reschedule; Enter Order Date and Delivery Date; Choose PJP Number. (11:32:01040001)
2. [Maker] Filter the grid by GIN No = GIN1 and outlet; open the row; Choose Reschedule Reason; check Amount FCY against the workbook.
3. [Maker] Process; accept the alert. Expect: text from `Reschedule_ASSR` [unknown].
4. [Maker] Navigate to Cashmemo Status; Choose PJP Number; select all; check Gross/Tax/Net; Save All. Expect: `Updated successfully` [atlas toast history, 83 times]. (11:33:00030001)
5. Seq 29 and 31, Order Editing / Order Cancellation After GIN, reuse the seq 15/16 screens (PJP, Selling category, section, Start/End Date, Outlet Name; OrderCS/OrderPC/Reason Type; Cancellation Reason, Net Amount). Intent: show that an order already on a GIN is treated differently from one before the GIN; expected result [unknown].

## 6. Outputs and effects
- Reschedule: cash memo gets execution status 19 "CM Reschedule" and a new delivery date; it probably leaves the GIN [inferred; status 25 "adhoc removal from GIN" exists].
- Status: document status Delivered (01) or Un-Delivered (02); execution 10 Delivered/Invoiced or 18 Partial Delivered [inferred]. Delivered cash memos create the cash/credit to be settled later (Deposit Slip seq 39; see the settlement pages).
- No stock movement is expected here; the GIN already took the stock out [inferred].

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| Ready to dispatch (13) | Reschedule + Process | CM Reschedule (19) | Maker | [inferred] |
| Ready to dispatch (13) | Cashmemo Status, Save All | Delivered/Invoiced (10) | Maker | [inferred] |
| Ordered (04) | Order Cancellation | Cancelled (03 / exec 05) | Maker | [db] |

## 8. Rules and validations
`Please Select Any Record` when Save All has no selection [atlas, 3 occurrences]. Order Date mandatory on Reschedule [atlas]. The alert must be accepted before processing [atlas]. Amounts are compared with the workbook/DB [atlas]. Dates typed straight into the DOM may be ignored by the app; type with key events [observed on other screens, ui.md].

## 9. Messages
`Updated successfully`; `Please Select Any Record`; reschedule success text [unknown]; one empty toast on Cashmemo Status [atlas].

## 10. Dependencies
Reads `REPO_GINNO` (Reschedule) and needs an approved GIN with cash memos. Hands over delivered cash memos to Sales Return (the same outlets) and to settlement. Cannot run live until the GIN approval works (stock day boundary).

## 11. Test design hints
Positive: reschedule one cash memo of the GIN with a reason and check status 19; mark all delivered. Negative: Save All with nothing selected; reschedule without reason; to a past date; an already delivered cash memo. Boundary: partial delivery (18); a PJP with one cash memo. A green run does not prove the DB status; add a DB check of `pdos_docmstatus` / `pexs_execution_status`.

## 12. Open questions (batched for the BA; each with a default)
Q: Does Cashmemo Status mean delivered only, or delivered/undelivered per row? | Default: Save All marks selected cash memos Delivered | Evidence: only Select All and Save All in the flow.
Q: What happens to GIN quantities when a cash memo is rescheduled? | Default: leaves the GIN, stock returns via Goods Return Note | Evidence: statuses 24/25 only.
Q: Intent and expected result of Order Editing/Cancellation After GIN? | Default: refused once the GIN is approved | Evidence: assertions are TSTMSG without text.
Q: Which reschedule reasons exist (workbook "Auto1")? | Default: first active reason | Evidence: list db-declared 2026-10-01 (see section 3); real dropdown not opened yet (PARTLY, Q22).

## 13. Sources
`framework_atlas/flows/01040001.md`, `00030001.md`, `00840001.md`, `00850001.md`, `group_11.md`; DB: snd_pr_dos_documentstatus, glb_pr_exs_execution_status, snd_tr_cmm_cashmemo_master, snd_tr_gnm_gingrn_refinfo.
