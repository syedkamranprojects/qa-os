---
option: Cashmemo Reschedule and Cashmemo Status
area: delivery_and_returns
doc_types: [CM-01]
screens: [DYL_202053, CASHMEMO-STATUS]
framework_flows: ["01040001", "00030001", "00840001", "00850001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [goods_issue_note, delivery_date_change, order_editing_cancellation]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-06
---
# Cashmemo Reschedule and Cashmemo Status: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b; consolidated with learning session 1 LEARN-G11-PK/20261001-1611, seq 29/31/32/33)
Last updated: 2026-10-01. Source flows: atlas `01040001` (group 11 seq 32), `00030001` (seq 33); also seq 29 `00840001` Order Editing After GIN and seq 31 `00850001` Order Cancellation After GIN. None of these has been replayed live yet (the GIN approval blocks the chain). (superseded 2026-10-01: all four were walked live on 2026-10-01 after GIN 506 was approved: COL26000002006 rescheduled to 2026-10-02, COL26000002003/2004/2005 delivered, 2003 edited and 2007 cancelled after the GIN [observed 2026-10-01 G11-1])
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.

## 1. Purpose
A cash memo (document type `CM-01` "Sales", the confirmed order that is the delivery document) is delivered by the DSR. After the GIN, either the DSR could not deliver on the planned day (Cashmemo Reschedule moves it to another delivery date with a reason) or he reports the outcome of the day (Cashmemo Status records cash memos as delivered / not delivered). [inferred from names, execution statuses and screens; confirmed 2026-10-01: Reschedule moves the cash memo to a new delivery date with a reason and takes it off the GIN (status Reattempt); Cashmemo Status marks the ticked cash memos Delivered/Invoiced with the actual delivery time [observed 2026-10-01 G11-1]]
- G11-3: a rescheduled order becomes due on its new date and **blocks Route Settlement of that date** until it is delivered ("Un-Deliver Order exists for today delivery!") [observed 2026-10-06 G11-3]. It must be re-allocated, put on a new GIN, approved and marked Delivered here [stated 2026-10-06 QA Team Lead].

## 2. Actors and roles
Maker = Stock Controller / order user `Auto_Multi_Orga` runs all four flows, no user switch in seq 29-33 [atlas]. No approval configured [atlas]. Confirmed 2026-10-01: the Maker ran seq 29, 31, 32 and 33 in one login; neither screen has a Forward or approval step, so the Checker has no part here [observed 2026-10-01 G11-1].
- G11-2: Maker Auto_Multi_Orga ran seq 29, 31, 32, 33 in one login on 2026-10-05; no Checker step [observed 2026-10-05 G11-2].

## 3. Documents and master data
- Cash memo `snd_tr_cmm_cashmemo_master`: document status 01 Delivered, 02 Un-Delivered, 03 Cancelled, 04 Ordered, 05 Amendment, 06 Re-attempt [db: snd_pr_dos_documentstatus CM-01, org 0101]. Execution status: 02 Confirmed, 03 Planning completed, 05 Cancelled, 10 Delivered/Invoiced, 13 Ready to dispatch/Packed, 18 Partial Delivered, 19 CM Reschedule, 20 CM BLOCKED [db: glb_pr_exs_execution_status]. Date columns `tcmm_delivery_date`, `tcmm_schdelv_date`, `tcmm_actual_delivery_time` [db].
- Live-verified 2026-10-01 [db]: execution status 02 "Confirmed" is a status of its own (identifier ALC) and 03 "Planning completed" follows it (identifier GIN); orders on GIN 505 read Planning completed [observed]. Reschedule Reason (datalist REASNCMRESCH, grid filter doc type CM-01 and identifier CNL): 0017 Shop Closed, 0018 Delivery is not possible due to any reason, 0019 Customer cancels delivery, 0021 customer refused, L02L01L01L01 Credit Exceeded, L02L02L03L01 Shop Closed, L02L03L04L01 Bad Weather, L02L03L04L02 Law & order Issue [db]: the reschedule list IS the cancellation list. The reason control is a column inside the grid row, so the dropdown could not be opened without an eligible order (search order date 2026-09-29, delivery 2026-09-30, PJP 02112: 0 rows) [observed].
- **Reschedule Reason dropdown opened live 2026-10-01** (was [db] only): Bad Weather, Credit Exceeded, customer refused, Delivery is not possible due to any reason, Law & order Issue, **Law & Order Issue (5 times)**, **Shop Closed (2 times)**, **Test Reason 716** [observed 2026-10-01 G11-1]. The list holds master-data duplicates and a test entry; "Customer cancels delivery" from the DB list was not seen in the dropdown [observed 2026-10-01 G11-1]. The Order Cancellation reasons are a shorter list (Bad Weather, Credit Exceeded, Law & order Issue, Shop Closed) [observed 2026-10-01 G11-1], so the two lists are related but not identical on screen.
- Delivery PJP of the cash memo: `epjp_pjpno_daily_delivery` [db]; GIN link via `snd_tr_gnm_gingrn_refinfo` [db]. Both screens filter by the **delivery** PJP (02112~AutomationDSR), not the order booker PJP (02111) [observed 2026-10-01 G11-1].
- On screen the GIN is shown as `GN-01~506` (Cashmemo Status GIN Number) [observed 2026-10-01 G11-1].

## 4. Inputs: screens and fields
**Cashmemo Reschedule** (menu `Cashmemo Reschedule`, option DYL_202053) [atlas]: **Order Date*** (mandatory), **Delivery Date**, **PJP Number**. Grid: row filter GIN No (`REPO_GINNO`) and Outlet Code/Name, open the row (`pjp_delivery_no`), per-row dropdown **Reschedule Reason**, read **Amount FCY**, then the Process button and accept the alert [atlas].
- Observed 2026-10-01 (Transaction > Cashmemo Reschedule): header **Order Date** (default today), **Delivery Date = the NEW delivery date** (default today), **PJP Number** = the delivery PJP (default the first in the list, AutoPJGIN2~Auto GIN PJP DM; options AutoPJGIN2, AUTO301301, 02112~AutomationDSR, AutoPromo2, 8197298470). Only button: **Process** [observed 2026-10-01 G11-1].
- Grid (cash memos of the delivery PJP that are on a GIN): checkbox, Cashmemo No, Outlet Name, Status (Ready to dispatch/Packed), Document Date, Amount FCY, PJP Number (booker, 02111), PJP Delivery No (02112), Delivery Date, Demand Channel, **GIN No** (506), **Reschedule Reason** (dropdown inside the row) [observed 2026-10-01 G11-1]. On 2026-10-01 it listed 4 cash memos (2003-2006); the order cancelled after the GIN (2007) was not listed [observed 2026-10-01 G11-1].
- **Changing the header Delivery Date reloads the grid and clears every tick and reason.** The header date is not a filter (the 10-01 orders stay listed when it is set to 10-02); it is the target date. Set the new date FIRST, then the reason and the tick [observed 2026-10-01 G11-1].

**Cashmemo Status** (menu `Cashmemo Status`, option CASHMEMO-STATUS) [atlas]: **PJP Number** dropdown; grid shows **Gross Amount**, **Tax**, **Net Amount**; header checkbox selects all; **Save All** (`saveallBtn`) [atlas].
- Observed 2026-10-01 (Transaction > Cashmemo Status; the menu also offers "Cashmemo Status Change" and "Cashmemo Status Van Sale"): filters **PJP Number** (delivery PJP; default the first, AutoPJGIN2) and **GIN Number**, which fills by itself after the PJP is chosen (GN-01~506 for 02112-AutomationDSR) [observed 2026-10-01 G11-1].
- Grid: checkbox, Document No, Outlet, Document Date, GIN Number, Delivery Date, Demand Channel, Document Status (shows **"Ordered"**, read-only), Gross Amount, Tax, Net Amount [observed 2026-10-01 G11-1]. It lists only the cash memos still on the GIN: the rescheduled (2006) and cancelled (2007) orders were absent [observed 2026-10-01 G11-1].
- **There is no per-row status choice**: tick the delivered cash memos and Save [observed 2026-10-01 G11-1]. Net Amount on the grid is the line sum (2003: 90,707.06), while other screens round the header to 90,707.00 [observed 2026-10-01 G11-1].
- G11-2: Cashmemo Reschedule header: Order Date today, Delivery Date = the NEW date (set first, calendar popup: 2026-10-06; changing it clears the selection), PJP Number defaults to AutoPJGIN2 and must be changed to 02112~AutomationDSR; Reschedule Reason is an in-row dropdown (14 options incl. duplicates) [observed 2026-10-05 G11-2].
- G11-2: Cashmemo Status header: PJP defaults to AutoPJGIN2-Auto GIN PJP DM (change to 02112-AutomationDSR); the second dropdown (GIN) fills itself with GN-01~507; grid columns Document No, Outlet, Document Date, GIN Number, Delivery Date, Demand Channel, Document Status, Gross, Tax, Net; the Document Status column reads **"Ordered"** (document status) while Transaction Inquiry shows the execution text Ready to dispatch/Packed [observed 2026-10-05 G11-2].

## 5. Process: the business steps in order
1. [Maker] Navigate to Cashmemo Reschedule; Enter Order Date and Delivery Date; Choose PJP Number. (11:32:01040001)
2. [Maker] Filter the grid by GIN No = GIN1 and outlet; open the row; Choose Reschedule Reason; check Amount FCY against the workbook.
3. [Maker] Process; accept the alert. Expect: text from `Reschedule_ASSR` [unknown]. (superseded 2026-10-01: the alert is "Are you sure you want to proceed?" and the toast is `Process completed successfully` [observed 2026-10-01 G11-1])
4. [Maker] Navigate to Cashmemo Status; Choose PJP Number; select all; check Gross/Tax/Net; Save All. Expect: `Updated successfully` [atlas toast history, 83 times; observed 2026-10-01 G11-1]. (11:33:00030001)
5. Seq 29 and 31, Order Editing / Order Cancellation After GIN, reuse the seq 15/16 screens (PJP, Selling category, section, Start/End Date, Outlet Name; OrderCS/OrderPC/Reason Type; Cancellation Reason, Net Amount). Intent: show that an order already on a GIN is treated differently from one before the GIN; expected result [unknown]. (superseded 2026-10-01: both succeeded after GIN approval with no warning; see steps 6-7 [observed 2026-10-01 G11-1])

Walked live 2026-10-01 (business steps in the standard vocabulary):
6. [Maker] Navigate to Order Editing; Choose PJP Number 02111 and the outlet; Open the cash memo on the approved GIN; Enter Order CS 4 (was 7) with Reason Type "Order Change QTY"; Validate; Save. Expect: `Validation successfully`, then `Order Save successfully`; same Document No, totals recalculated; no stock movement. (11:29:00840001) [observed 2026-10-01 G11-1]
7. [Maker] Navigate to Order Cancellation; Choose the outlet; Choose Cancellation Reason "Shop Closed"; Select the cash memo; Cancel All. Expect: result window "Order Cancellation Status" with `Order Cancelled Successfully`; no stock movement. (11:31:00850001) [observed 2026-10-01 G11-1]
8. [Maker] Navigate to Cashmemo Reschedule; Enter Delivery Date = the new date (2026-10-02) FIRST; Choose PJP Number = the delivery PJP (02112); Choose Reschedule Reason "Shop Closed" on the row; Select the cash memo; Process; Accept "Are you sure you want to proceed?". Expect: `Process completed successfully`; the cash memo leaves the list. (11:32:01040001) [observed 2026-10-01 G11-1]
9. [Maker] Navigate to Cashmemo Status; Choose PJP Number = the delivery PJP; check GIN Number fills by itself; Select the delivered cash memos (header checkbox); Save. Expect: `Updated successfully`; the list empties. (11:33:00030001) [observed 2026-10-01 G11-1]
10. [Maker] Check in Transaction Inquiry: delivered cash memos Delivered/Invoiced with Actual Delivery = save time; rescheduled cash memo Reattempt with the new delivery date and no GIN [observed 2026-10-01 G11-1].

G11-2 walk (2026-10-05) [observed 2026-10-05 G11-2]:
1. [Maker] Navigate to Cashmemo Reschedule; Choose Delivery Date 2026-10-06 FIRST; Choose PJP 02112~AutomationDSR; grid lists the 4 non-cancelled cash memos of GIN 507 (2009-2012, Ready to dispatch/Packed; 2009 at its edited Net 90,707); Tick COL26000002012; Choose Reschedule Reason Shop Closed; Click Process; Accept "Are you sure you want to proceed?" -> "Process completed successfully"; the row leaves the list (11:32:01040001).
2. [Maker] Navigate to Cashmemo Status; Choose PJP 02112-AutomationDSR (GIN GN-01~507 fills); grid 2009 (Gross 96,840.34), 2010 (126,688.41 / Net 101,160.73), 2011 (126,688.41 / Tax 18,208.93 / Net 119,369.66); Select all; Click Save -> "Updated successfully"; rows leave the list (11:33:00030001).
G11-3 walk (2026-10-06) [observed 2026-10-06 G11-3]:
1. [Maker] Cashmemo Reschedule: PJP 02112; set the new Delivery Date **2026-10-07 first**, then reason Shop Closed on COL26000002018 + tick; Process -> confirm -> "Process completed successfully"; 2018 leaves the GIN 508 list (11:32:01040001).
2. [Maker] Cashmemo Status: PJP 02112 -> GIN GN-01~508 auto-filled -> 2015 (81,417.41 / 12,371.66 / 76,155.59), 2016 (126,688.41 / 0 / 101,160.73), 2020 (107,960.51 / 16,505.36 / 108,201.79), status "Ordered"; header checkbox; Save -> "Updated successfully"; list empty (11:33:00030001).
3. Extra [Maker] (after GIN 509): Cashmemo Status PJP 02112 -> GIN GN-01~509 -> COL26000002012 (2026-10-05, 107,960.51 / 16,505.36 / 108,201.79, Ordered); tick; Save -> "Updated successfully" (Delivered; left unpaid on the QA Team Lead's instruction).

## 6. Outputs and effects
- Reschedule: cash memo gets execution status 19 "CM Reschedule" and a new delivery date; it probably leaves the GIN [inferred; status 25 "adhoc removal from GIN" exists]. (superseded 2026-10-01: Transaction Inquiry shows Document Status **Reattempt** (not "CM Reschedule"), Delivery Date = the new date 2026-10-02, and **no GIN number**: rescheduling takes the cash memo off the GIN [observed 2026-10-01 G11-1])
- Status: document status Delivered (01) or Un-Delivered (02); execution 10 Delivered/Invoiced or 18 Partial Delivered [inferred]. Delivered cash memos create the cash/credit to be settled later (Deposit Slip seq 39; see the settlement pages). Confirmed 2026-10-01: the ticked cash memos show **Delivered/Invoiced**, GIN 506 kept, **Actual Delivery Date = the date and time of the Cashmemo Status save** (2026-10-01 17:54:09); Invoice Ref. No. stays empty [observed 2026-10-01 G11-1]. The delivered cash memos then appear in Sales Return (seq 34) and in the deposit slips (seq 39+) with Balance Amount = Net [observed 2026-10-01 G11-1].
- No stock movement is expected here; the GIN already took the stock out [inferred]. Confirmed 2026-10-01: edit, cancel and reschedule after the GIN did not change Out, Allocated or Closing in Stock Inquiry; the cancelled (7 CS), cut (3 CS) and rescheduled (7 CS) quantities came back only on the Goods Return Note (GRN 246, 19 CS with the 2 CS sales return) [observed 2026-10-01 G11-1].
- Order Editing after the GIN keeps the same Document No (COL26000002003) and re-applies promotions on the smaller basket (Net 90,707.00 = workbook) [observed 2026-10-01 G11-1].
- A cash memo cancelled after the GIN keeps its GIN number (506) in Transaction Inquiry; one cancelled before the GIN has none [observed 2026-10-01 G11-1].
- G11-2: 2012 -> Reattempt with delivery 2026-10-06, off GIN 507, its 7 CS returned on GRN 247; 2009-2011 -> Delivered/Invoiced with Actual Delivery Date 2026-10-05 10:37 (second day) [observed 2026-10-05 G11-2, G11-2b].
- G11-3: **a Reschedule unallocates the order** (2018 found on the Unallocated tab of Order Stock Allocation) [observed 2026-10-06 G11-3]; the order stays Reattempt with delivery date 2026-10-07 and will be due on that day.

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| Ready to dispatch (13) | Reschedule + Process | CM Reschedule (19) | Maker | [inferred] (superseded 2026-10-01: shown as **Reattempt**, off the GIN, new delivery date [observed 2026-10-01 G11-1]) |
| Ready to dispatch (13) | Cashmemo Status, Save All | Delivered/Invoiced (10) | Maker | [inferred]; confirmed (tick + Save) [observed 2026-10-01 G11-1] |
| Ordered (04) | Order Cancellation | Cancelled (03 / exec 05) | Maker | [db] |
| Ready to dispatch/Packed | Order Cancellation (after GIN) | Cancelled, GIN number kept | Maker | [observed 2026-10-01 G11-1] |
| Ready to dispatch/Packed | Order Editing (after GIN) | Ready to dispatch/Packed (same number, new totals) | Maker | [observed 2026-10-01 G11-1] |
Status chain observed 2026-10-01: Confirmed -> Ready to dispatch/Packed (GIN approved) -> Delivered/Invoiced | Reattempt | Cancelled [observed 2026-10-01 G11-1].

## 8. Rules and validations
`Please Select Any Record` when Save All has no selection [atlas, 3 occurrences]. Order Date mandatory on Reschedule [atlas]. The alert must be accepted before processing [atlas]. Amounts are compared with the workbook/DB [atlas]. Dates typed straight into the DOM may be ignored by the app; type with key events [observed on other screens, ui.md].
- The Reschedule header Delivery Date is the target date; changing it clears the selection and the reasons [observed 2026-10-01 G11-1].
- Reschedule offers only cash memos of the chosen delivery PJP that are on a GIN and not cancelled [observed 2026-10-01 G11-1].
- Cashmemo Status offers only cash memos still on the GIN (not rescheduled, not cancelled) [observed 2026-10-01 G11-1].
- Cashmemo Status marks every ticked cash memo Delivered; there is no Un-Delivered or partial choice on this screen [observed 2026-10-01 G11-1] ("Cashmemo Status Change" may offer more; not walked).
- Orders on an approved GIN can be edited and cancelled with no warning (business control question) [observed 2026-10-01 G11-1].
- G11-2: Reschedule and Status list only cash memos still on the GIN (2013 cancelled after the GIN and 2012 rescheduled were absent from Status); confirmed on a second day [observed 2026-10-05 G11-2].
- G11-3: set the new Delivery Date before ticking the row on Cashmemo Reschedule [observed 2026-10-06 G11-3].
- G11-3: Cashmemo Status picks the GIN from the PJP (latest GIN auto-filled: 508, later 509) [observed 2026-10-06 G11-3].
- G11-3: **Zero-tax rule** [stated 2026-10-06 QA Team Lead]: a zero-tax invoice of an outlet that is **NOT tax-exempt cannot be delivered** (the application stops the delivery); a zero-tax invoice of a **tax-exempt** outlet is allowed. Not exercised on 2026-10-06: the zero-tax order of non-exempt outlet 07 (COL26000002017) was cancelled at seq 16 [observed]; the exact blocking screen and message are [unknown].

## 9. Messages
`Updated successfully`; `Please Select Any Record`; reschedule success text [unknown]; one empty toast on Cashmemo Status [atlas].
- Observed 2026-10-01: Reschedule confirm `Are you sure you want to proceed?` and toast `Process completed successfully` (supersedes "reschedule success text [unknown]"); Cashmemo Status `Updated successfully` [observed 2026-10-01 G11-1].
- Order Editing After GIN: `Validation successfully`, `Order Save successfully`; Order Cancellation After GIN: result window "Order Cancellation Status", status `Successfull` (sic), message `Order Cancelled Successfully`, no toast [observed 2026-10-01 G11-1].
- G11-2: "Process completed successfully" (Reschedule, after the confirm) and "Updated successfully" (Cashmemo Status Save) confirmed on a second day [observed 2026-10-05 G11-2].
- G11-3: "Process completed successfully" (Reschedule), "Updated successfully" (Status) [observed 2026-10-06 G11-3].

## 10. Dependencies
Reads `REPO_GINNO` (Reschedule) and needs an approved GIN with cash memos. Hands over delivered cash memos to Sales Return (the same outlets) and to settlement. Cannot run live until the GIN approval works (stock day boundary). (superseded 2026-10-01: ran live after GIN 506 was approved on the same day [observed 2026-10-01 G11-1])
- Hands over: delivered cash memos to Sales Return (only delivered ones are offered there), Deposit Slip and Route Settlement; the rescheduled cash memo to the next day's planning (delivery 2026-10-02); the cancelled, cut and rescheduled quantities to the Goods Return Note (seq 48) [observed 2026-10-01 G11-1].
- Route Settlement counted the GIN's 4 non-cancelled orders as Total Order 4, Delivered 3, Undelivered 0: the rescheduled order is neither delivered nor undelivered there [observed 2026-10-01 G11-1].
- G11-3: hand-over to the next day: COL26000002018 (Reattempt, due 2026-10-07, unallocated) must be allocated (Order Date 2026-10-06), put on a GIN, approved and delivered before the 2026-10-07 settlement [observed 2026-10-06 G11-3; procedure stated 2026-10-06 QA Team Lead].

## 11. Test design hints
Positive: reschedule one cash memo of the GIN with a reason and check status 19; mark all delivered. Negative: Save All with nothing selected; reschedule without reason; to a past date; an already delivered cash memo. Boundary: partial delivery (18); a PJP with one cash memo. A green run does not prove the DB status; add a DB check of `pdos_docmstatus` / `pexs_execution_status`.
- Positive (2026-10-01): reschedule checks Reattempt, new delivery date and no GIN number in Transaction Inquiry (not "19"); delivery checks Delivered/Invoiced and Actual Delivery = save time [observed 2026-10-01 G11-1].
- **Trap, reschedule date order:** set the header Delivery Date first; changing it after ticking clears the ticks and reasons, so a run that sets the date last processes nothing or the wrong date [observed 2026-10-01 G11-1].
- **Trap, default PJP:** both screens default to the first PJP in the list (AutoPJGIN2), not the delivery PJP of the test; choose it explicitly [observed 2026-10-01 G11-1].
- **Trap, stock:** reschedule, edit and cancel after the GIN do not move stock; the quantities come back only on the GRN. Check the GRN Suggested quantity, not Stock Inquiry right after the change [observed 2026-10-01 G11-1].
- **Trap, status chain:** Confirmed -> Ready to dispatch/Packed -> Delivered/Invoiced | Reattempt | Cancelled; assert the text shown in Transaction Inquiry [observed 2026-10-01 G11-1].
- **Trap, reason list:** duplicates (Law & Order Issue x5, Shop Closed x2) and "Test Reason 716"; select by exact text and do not assert the list size [observed 2026-10-01 G11-1].
- Negative idea: Cashmemo Status has no Un-Delivered choice; test undelivered handling through Reschedule or Route Settlement instead [inferred].
- G11-2 additions [observed 2026-10-05 G11-2]:
  - Trap: both screens default to the PJP AutoPJGIN2; choose the delivery PJP explicitly.
  - Trap: Cashmemo Status shows Document Status "Ordered" for cash memos on an approved GIN (document status), not the execution text; assert the column you mean.
- G11-3 trap (replay across days): every seq 32 reschedule creates tomorrow's settlement blocker; a daily cycle must include the delivery of yesterday's Reattempt order (or not reschedule to a working day that will be settled) [observed 2026-10-06 G11-3].
- Negative (2026-10-06 ruling [stated 2026-10-06 QA Team Lead]): mark Delivered a zero-tax invoice of a non-exempt outlet -> expect the delivery to be blocked (message to be recorded); positive: zero-tax invoice of a tax-exempt outlet (e.g. 1000000005) -> Delivered.

## 12. Open questions (batched for the BA; each with a default)
Q: Does Cashmemo Status mean delivered only, or delivered/undelivered per row? | Default: Save All marks selected cash memos Delivered | Evidence: only Select All and Save All in the flow. ANSWERED 2026-10-01: delivered only; ticked rows become Delivered/Invoiced, no per-row choice [observed 2026-10-01 G11-1].
Q: What happens to GIN quantities when a cash memo is rescheduled? | Default: leaves the GIN, stock returns via Goods Return Note | Evidence: statuses 24/25 only. ANSWERED 2026-10-01: the cash memo leaves the GIN (Reattempt, no GIN number) and its 7 CS came back on GRN 246 [observed 2026-10-01 G11-1].
Q: Intent and expected result of Order Editing/Cancellation After GIN? | Default: refused once the GIN is approved | Evidence: assertions are TSTMSG without text. ANSWERED 2026-10-01 (behaviour): both are allowed with no warning and move no stock [observed 2026-10-01 G11-1]; whether this is intended stays open (next question).
Q: Should editing or cancelling an order on an approved GIN be blocked or warned? | Default: allowed (as observed); report as a business control question | Class: C | Evidence: seq 29/31 2026-10-01.
Q: Which reschedule reasons exist (workbook "Auto1")? | Default: first active reason | Evidence: list db-declared 2026-10-01 (see section 3); real dropdown not opened yet (PARTLY, Q22). ANSWERED 2026-10-01: dropdown opened, list in §3; the session used "Shop Closed" [observed 2026-10-01 G11-1].
Q: Are the duplicate reschedule reasons (Law & Order Issue x5, Shop Closed x2, Test Reason 716) a master-data clean-up item? | Default: yes, data issue; select by exact text | Class: C | Evidence: dropdown 2026-10-01.
Q: Does the rescheduled cash memo (Reattempt, delivery 2026-10-02) get picked up by the next day's GIN without a Delivery Date Change? | Default: yes, it is offered on the GIN of its new delivery date | Class: B | Evidence: not walked (needs a second day).
- G11-2: the rescheduled COL26000002012 (delivery 2026-10-06) was not followed to the next day; the next-day pickup question stays open (B).
- Q-TX1 ANSWERED 2026-10-06 [stated 2026-10-06 QA Team Lead]: outlet 06/07 tax swap = master-data modification of outlets and tax promotion; the zero-tax delivery rule above follows from it. Open detail: where exactly the block fires (GIN, Cashmemo Status) and its message [unknown], class B.

## 13. Sources
`framework_atlas/flows/01040001.md`, `00030001.md`, `00840001.md`, `00850001.md`, `group_11.md`; DB: snd_pr_dos_documentstatus, glb_pr_exs_execution_status, snd_tr_cmm_cashmemo_master, snd_tr_gnm_gingrn_refinfo.
Learning session 1 (2026-10-01): `learning_sessions/2026-10-01_G11-PK_session1_log.md` seq 29, 31, 32, 33, "Transaction Inquiry status check after seq 31-33", seq 48, seq 51; `learning_sessions/2026-10-01_G11-PK_session1_report.md` §3 rules 7 and 10, §6 items 3 and 5.
- G11-2: learning_sessions/2026-10-05_G11-PK_session2_log.md (seq 29, 31, 32, 33).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 32, 33; 2012 delivery at seq 51).
