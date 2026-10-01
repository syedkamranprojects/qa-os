# Live learning checklist (class B questions), ordered by the Daily Cycle

Updated: 2026-10-01 (live blocks 1-3b)

Built from [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) class B (33 questions at the start; 24 still open plus 1 new after live blocks 1-3b). Environment cnr1dev1; Maker = Auto_Multi_Orga, Checker = Auto_Tssm. Logins are triggered by the QA member (Claude never types passwords); every test run starts from a fresh login. Steps use the standard vocabulary [Actor] Verb Object. Record: the exact message text, the ids/labels seen, row counts, and a Stock Inquiry before/after snapshot (same row, same filters).

## Rules for the whole walk
- **Never click Generate Opening Balances** (stock-changing, not authorised). **Do not** use Reject/Terminate/Bounce except where a step below says so.
- Mark: **RO** = read-only, can run any day; **D** = changes data but not stock; **S** = changes stock; **SD** = needs a same-day receive-and-issue cycle (DA approved, orders, GIN approved, all inside ONE calendar day, because balances are keyed by date).
- On a new day Stock Inquiry shows "No data" until a movement creates the row (observed 2026-10-01: 0 rows before the DA approval, 1 row after). **Learned: the DA approval itself creates the day's row for the received product (Opening 0, In = received), so the SD part can start with the DA** (see section "Start-of-day decision").
- Run order: RO block first (any day), then D block, then the SD block in one sitting.

## Start-of-day decision (BA1 ANSWERED 2026-10-01; remainder is BA14)
No start-of-day step is needed for a received product: the DA approval created the 2026-10-01 row of 62740537 (Opening 0, In 4, Closing 4) without Generate Opening Balances [observed, blocks 3a/3b]. Open (BA14): previous-day closings are NOT carried (62740537 closed 97 CS on 09-30, opened 0 on 10-01), so the SD cycle must use stock received the same day; whether Generate Opening Balances serves other products is unknown. Default: do not run the button; start the SD block with a DA of the day.

## Status after live blocks 1-3b (2026-10-01)

DONE = answered and recorded in LIVE_FINDINGS.md and the area pages; PARTLY = part observed, remainder listed; NOT DONE = not run. Blocks: 1 = read-only walk, 2a = Maker data-changing, 3a = Checker, 3b = Maker re-read.

| Id | Status | Block | Result in one line |
|---|---|---|---|
| L01 | DONE | 1 | Stock Inquiry 09-30, 39 rows: Closing = Opening + In - Out - Allocated holds on all rows in base PC (2 rows differ per column only by PC-to-CS carry); Q11 answered |
| L02 | DONE | 1, 3b | 10-01 default date: 0 rows / No data before the DA approval; 1 row (62740537, In 4, Closing 4) after it |
| L03 | DONE | 1 | 8 orders 1995-2002 read: Document Status "Planning completed", Delivery Date 09-30, GIN 505, Total Offering = header Discount (1 paisa); no Execution Status and no Delivery-PJP column; Q23, Q28 answered, Q30 baseline |
| L04 | DONE | 1 (db) | "Confirmed" = execution status 02, Planning completed = 03, Ordered = document 04 / execution 01; Q23 answered |
| L05 | DONE | 1 (db) | org 010104 uses StockUpdateGIN v53: Verify then Approve, both role 0005 (4Level only for parent orgs); Q35 answered |
| L06 | DONE | 2a, 3a | merged into L12 |
| L07 | PARTLY | 1 | reason control is inside the grid row; no eligible order today, grids empty; lists read from the DB (CNL / ORC); open the real dropdowns on a new order |
| L08 | DONE | 1 | SAN Type options read (5); no OTC type and no OTC menu; candidate Stock Adjustment Admin SA-03; Q57 answered |
| L09 | PARTLY | 1 | PJP Daily Inquiry Update grid read (8 rows); Mark Status / DSR Files Status are dropdowns only in Edit mode (not clicked); db: E End of Day, P process / C complete |
| L10 | DONE | 1, 3a | button states for Maker and Checker on Draft 29 and Pending 505 recorded; Q36, Q37 answered; no approval log control exists |
| L11 | DONE | 2a | duplicate SO Number allowed (DA 1353, 1354), SO optional (1355); silent Save when DA Type is empty after Add; Q04 answered |
| L12 | DONE | 2a, 3a | DA 1356: no loss record after the maker's Forward; Serial 638 (Pending) after the checker's approval; Calculate required, x discards the loss; Q06 answered |
| L13 | NOT DONE | | DA Delete / Reject not run (Q02 open) |
| L14 | PARTLY | 2a, 3b | no Validation button and no header message (progressive disclosure: Order Detail only after Outlet); product pick "Stock not available." without a stock row, row fills with ATP 4/0/0 after the DA approval; Validation/Save not reached, nothing saved (Q18 partly) |
| L15 | NOT DONE | | needs a delivered cash memo |
| L16 | NOT DONE | | DSR Adjustment save not run (Q53 open) |
| L17 | NOT DONE | | past delivery date test not run (Q29 open) |
| L18 | NOT DONE | | delivery PJP before/after not run (Q30 open; read it on the GIN) |
| L19 | NOT DONE | | same-day cycle baseline snapshot to be retaken (a 10-01 snapshot after trial DA 1356 exists: 62740537 Closing 4) |
| L20 | NOT DONE | | cycle about to run: new DA with the four framework products, Checker approval. Trial DA 1356 already showed the rows appear without Generate Opening Balances (Q10 evidence) and In = received; a cycle DA 1357 was created and forwarded, approval pending |
| L21 | NOT DONE | | loss approval of Serial 638 not run (loss record is Pending; no Damaged stock row yet) |
| L22-L33 | NOT DONE | | same-day orders, allocation, delivery date, GIN, Cashmemo Status, sales return, GRN, SAN, Deposit Slip, Route Settlement, final snapshot: all remain to run |

### What remains
- Same-day cycle L19-L33 (new DA with four framework products, Checker approval, orders with qty = ATP and ATP + 1, Unallocate, Order Editing, Delivery Date Change, GIN with Draft Forward by the Maker and approval by the Checker, Cashmemo Status, Sales Return, GRN, Deposit Slip, Route Settlement, SAN, final snapshot). Open questions it closes: Q08, Q16, Q18 (detail messages), Q21, Q22 (real dropdowns), Q26, Q27, Q31, Q32, Q33, Q34, Q41-Q43, Q45, Q46, Q48, Q50, Q58, N1, and BA3 (loss approval L21).
- Any-day leftovers: L13 (DA delete/reject), L16 (DSR Adjustment), L17/L18 (delivery date change), L09 Edit-mode read of the PJP dropdowns.
- Learned helper notes for the cycle: enter the quantity only after stock type and batch have filled (otherwise "The lost quantity does not equal the sum of dispatch and received quantities", nothing saved); after Add pick Warehouse, Vendor and DA Type; use the calendar popup for dates on Order Cancellation; the Maker's Forward only on Drafts, the Checker's Forward only on Pending.

## Block 1: read-only, any day (RO)

| Id | Step (standard vocabulary) | User | Observe and record | Changes data? | Risk | Depends on | Questions |
|---|---|---|---|---|---|---|---|
| L01 | [Stock Controller] Navigate to Stock Inquiry; Choose Balance Date 2026-09-30; Click Show Inquiry; read all 39 rows | Auto_Multi_Orga | per row Opening, In, Out, Allocated, Closing (CS/DZ/PC); test Closing = Opening + In - Out - Allocated on every row; note any row where Allocated is not subtracted | no (RO) | low; do not click Generate Opening Balances | none | Q11 |
| L02 | [Stock Controller] Navigate to Stock Inquiry; Choose today's date; Click Show Inquiry | Auto_Multi_Orga | row count (expect "No data" on a new day), date default | no (RO) | low | none | Q10 evidence |
| L03 | [Order User] Navigate to Transaction Inquiry; Choose Document Type Sales, date range covering 2026-09-30; open orders COL26000001995-2002 | Auto_Multi_Orga | text of Document Status, Execution Status, Delivery Date, PJP Delivery No; Total Offering Discount vs header Discount; Detail line sums | no (RO) | low | orders exist from the 09-30 run | Q23, Q28, Q30 (baseline) |
| L04 | Read-only SQL (snd-schema/overlay connector): status descriptions of those order numbers and of CM-01 document and execution statuses for 010104 | no browser | whether "Confirmed" is execution 02 or an alias of 04 Ordered | no (RO) | low | connector authorised | Q23 |
| L05 | Read-only SQL: workflow definition of GIN (StockUpdateGIN4Level) levels | no browser | number of approval levels | no (RO) | low | connector | Q35 |
| L06 | (observation only) see L12 | | | | | | |
| L07 | [Order User] Navigate to Order Editing and Order Cancellation; open the Reason Type and Cancellation Reason lists; [Order User] Navigate to Cashmemo Reschedule; open the Reschedule Reason list | Auto_Multi_Orga | the full option lists (do not Save) | no (RO) | low; do not click Cancel/Process | none | Q22 |
| L08 | [Stock Controller] Navigate to Stock Adjustment SAN; open the SAN Type dropdown | Auto_Multi_Orga | which type reads as OTC stock out; record that no "OTC Stock Out" menu exists | no (RO) | low; do not Save | none | Q57 |
| L09 | [Back-office] Navigate to PJP Daily Inquiry Update; open Mark Status and DSR Files Status lists | Auto_Multi_Orga | allowed values | no (RO) | low; do not click Edit/Save | none | Q55 |
| L10 | [Stock Controller] Navigate to Goods Issue Note; open an existing Draft and a Pending GIN; note which of Forward, Reject, Terminate, De-linking are enabled for Maker; repeat as Checker | Auto_Multi_Orga, Auto_Tssm | button states per status and user | no (RO) | low; do not click any | existing GINs (505, others) | Q36, Q37 |

## Block 2: data-changing, no stock movement (D), any day

| Id | Step | User | Observe and record | Data/stock | Risk | Depends on | Questions |
|---|---|---|---|---|---|---|---|
| L11 | [Maker] Navigate to Dispatch Advice; Create DA with a SO Number; Save; Create a second DA with the same SO Number; Save | Auto_Multi_Orga | message on the duplicate, new Document Nos | D (Draft DAs, no stock) | low; leaves Draft DAs | none | Q04 |
| L12 | [Maker] Create a DA with one line and a loss row; Forward with comment; [Maker] Navigate to Loss Approval and look for the record BEFORE any checker action | Auto_Multi_Orga | whether a loss record exists at maker Forward (Pending for approval) and its Serial No | D (record only) | low; DA stays Pending (do not approve unless in Block 3) | none | Q06 |
| L13 | [Maker] Create a DA with one line; Delete it. Create another DA, Forward; [Checker] Navigate to the DA; Click Reject with comment | Auto_Multi_Orga, Auto_Tssm | messages and final statuses (Draft delete, Rejected); whether a Rejected DA creates stock (it must not) | D (no stock if Rejected) | medium: Reject is data-changing; confirm the DA is a throwaway | none | Q02 |
| L14 | [Order User] Navigate to Order Booking; Click Validation with each header field empty in turn (no Save) | Auto_Multi_Orga | which fields block, exact messages | no data saved if blocked | low; do not click Save | none | Q18 |
| L15 | [Back-office] Navigate to Deposit Slip, click the Cash variants and the save with amount 0, text, special characters on a throwaway | Auto_Multi_Orga | messages (not in checklist class B unless listed; run only if a delivered cash memo exists) | D | medium | delivered cash memo | Q45 prerequisite |
| L16 | [Back-office] Navigate to DSR Adjustment; add one small adjustment with Comments to a test PJP; read status on Detail tab | Auto_Multi_Orga | status after save (Authorized / Un-Authorized), displayed amount | D (AD-07 row) | medium: finance row cannot be deleted by us | PJP row | Q53 |
| L17 | [Order User] Navigate to Delivery Date Change; Choose Order Date and a PJP that has orders; Choose a past Delivery Date; Click Process | Auto_Multi_Orga | whether refused and the message | D if accepted (changes dates) | medium: moves delivery dates of real test orders; run before the SD block and restore the date | orders of that PJP | Q29 |
| L18 | After L17 and a valid change: [Order User] Navigate to Transaction Inquiry; compare Delivery Date and PJP Delivery No before/after | Auto_Multi_Orga | whether the delivery PJP changes | D | medium | L03 baseline | Q30 |

(L06 is merged into L12; ids kept to avoid renumbering.)

## Block 3: same-day receive-and-issue cycle (SD), in Daily Cycle order, one calendar day

| Id | Step | User | Observe and record | Data/stock | Risk | Depends on | Questions |
|---|---|---|---|---|---|---|---|
| L19 | [Stock Controller] Take a before snapshot of Stock Inquiry for product 62740537 in Auto Main Warehouse (all stock types) | Auto_Multi_Orga | all 5 column groups | RO | low | none | baseline |
| L20 | [Maker] Create DA (one line, one loss row), Forward; [Checker] approve; | Auto_Multi_Orga, Auto_Tssm | messages, Received Date; exact stock delta; **do rows appear for today without Generate Opening Balances?** | S (Sound In rises by received qty) | medium: stock-changing, part of the authorised cycle | L12 outcome | Q10 evidence, Q31 |
| L21 | [Checker] Navigate to Loss Approval; Forward; then [Stock Controller] re-read Stock Inquiry for stock types 02, 04 | Auto_Tssm, Auto_Multi_Orga | whether Damaged/Lost rows appear (feeds BA3) | S/unknown | medium | L20 | evidence for Q05 |
| L22 | [Order User] Book an order with quantity = ATP and one with ATP + 1 (Validation, Save) | Auto_Multi_Orga | blocked / warned / accepted, Allocation Status | S (Allocated) | medium | L20 stock | Q16, Q27 |
| L23 | [Order User] Navigate to Order Stock Allocation; Click Unallocate on a same-day order (accept alert) | Auto_Multi_Orga | message (was "stock not found."), whether it now works | S (allocation) | medium | L22 | Q26 |
| L24 | [Order User] Navigate to Order Editing; open an order; change a quantity; Validation; Save | Auto_Multi_Orga | whether the order is reachable, Order Number same or new, totals | D/S | medium | L23 outcome | Q21 |
| L25 | [Order User] Navigate to Delivery Date Change; Choose valid date; Process | Auto_Multi_Orga | processed count | D | low | orders | feeds L26 |
| L26 | [Stock Controller] Create GIN (Cash Memo Selection, Save All), Forward; [Checker] approve with Delivery Date today and again variant with a future Delivery Date | Auto_Multi_Orga, Auto_Tssm | which date the stock check uses, messages; Stock Inquiry Out and Allocated delta, execution status of the cash memos | S (stock out) | **high**: stock-changing; two GINs needed for the date variants | L20, L25 | Q31, Q34 |
| L27 | [Stock Controller] Navigate to Cashmemo Status; Choose PJP; read grid; Save All on one cash memo | Auto_Multi_Orga | grid columns, message ("Updated successfully"), document and execution status in DB | D | medium | L26 | Q32, Q33 |
| L28 | [Maker] Sales Return: return one line with a discount; Validate, Save, Forward; [Checker] approve; [Maker] Status Change | Auto_Multi_Orga, Auto_Tssm | Discount reversal, Return quantity vs ordered/delivered, stock snapshot after each step | S (none expected until GRN) | medium | L27 | Q41, Q42, Q43, Q40 evidence |
| L29 | [Maker] Goods Return Note: Delivery Man PJP, edit rows, Save All, Forward; [Checker] approve; [Stock Controller] snapshot | Auto_Multi_Orga, Auto_Tssm | stock type and day credited, messages | S (stock In) | high: stock-changing | L26 | Q08 |
| L30 | [Maker] Deposit Slip full-amount cash on the delivered cash memo; read status, Unposted variant | Auto_Multi_Orga | status I -> A trigger, Unposted Amount meaning | D | medium | L27 | Q45, Q46 |
| L31 | [Maker] Route Settlement for the PJP/date; read payable, received, shortage screens; then Transaction Inquiry Offset Amount | Auto_Multi_Orga | payable vs received, Offset Amount | D (settlement row) | medium | L30 | Q48, Q50 |
| L32 | [Maker] SAN stock out of 1 PC, Forward; snapshot; [Checker] approve; snapshot | Auto_Multi_Orga, Auto_Tssm | whether stock reduces at Forward or approval | S | high | L20 | Q58 |
| L33 | [Stock Controller] Final Stock Inquiry snapshot; compare with L19 step by step and the identity Opening + In - Out - Allocated | Auto_Multi_Orga | total effect of the cycle per step | RO | low | all | Q31 |

## Summary
- RO any-day items: L01-L05, L07-L10, L33 baseline reads; D any-day: L11-L18; SD (same-day receive and issue required): L19-L32.
- Items that change stock: L20, L21 (maybe), L22 (allocation), L23, L26, L29, L32. These need the BA/environment owner's go-ahead for the day plan; the Generate Opening Balances button is excluded in all steps.
- Class C questions that this checklist can only inform, not close: BA3 (losses), BA6, BA7, BA9, BA14 (BA1 was answered by the DA approval evidence).
