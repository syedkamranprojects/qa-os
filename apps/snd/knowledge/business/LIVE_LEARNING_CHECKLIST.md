# Live learning checklist (class B questions), ordered by the Daily Cycle

Updated: 2026-10-08 (QA team follow-up answers: L42 settled (Q-OE5 answered: no stock movement at an after-GIN edit; only the optional parameter read remains); new L45 (Q-SV2); see "Status after the QA team follow-up answers"); 2026-10-08 (QA team written answers: L16, L17, L22, L31, L32, L36 settled by stated answers; new L42-L44; see section "Status after the QA team written answers"); 2026-10-06 (G11-3 consolidation: L34, L35, L39 dropped as answered by the QA Team Lead (Q-OB2, Q-OE4, Q-DJ1); Q-TI1 and Q-TX1 answered too; new check L40); 2026-10-05 (G11-2 / G11-2b consolidation, see section "Status after G11-2 / G11-2b"); 2026-10-01 (live blocks 1-3b)

Built from [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) class B (33 questions at the start; 24 still open plus 1 new after live blocks 1-3b). Environment cnr1dev1; Maker = Auto_Multi_Orga, Checker = Auto_Tssm. Logins are triggered by the QA member (Claude never types passwords); every test run starts from a fresh login. Steps use the standard vocabulary [Actor] Verb Object. Record: the exact message text, the ids/labels seen, row counts, and a Stock Inquiry before/after snapshot (same row, same filters).

## Rules for the whole walk
- **Never click Generate Opening Balances** (stock-changing, not authorised). **Do not** use Reject/Terminate/Bounce except where a step below says so.
- Mark: **RO** = read-only, can run any day; **D** = changes data but not stock; **S** = changes stock; **SD** = needs a same-day receive-and-issue cycle (DA approved, orders, GIN approved, all inside ONE calendar day, because balances are keyed by date).
- On a new day Stock Inquiry shows "No data" until a movement creates the row (observed 2026-10-01: 0 rows before the DA approval, 1 row after). **Learned: the DA approval itself creates the day's row for the received product (Opening 0, In = received), so the SD part can start with the DA** (see section "Start-of-day decision"). (2026-10-05: the first movement created ALL 39 rows with Opening = previous Closing + still-Allocated; previous closings are carried [observed 2026-10-05 G11-2].)
- Run order: RO block first (any day), then D block, then the SD block in one sitting.

## Start-of-day decision (BA1 ANSWERED 2026-10-01; remainder is BA14)
No start-of-day step is needed for a received product: the DA approval created the 2026-10-01 row of 62740537 (Opening 0, In 4, Closing 4) without Generate Opening Balances [observed, blocks 3a/3b]. Open (BA14): previous-day closings are NOT carried (62740537 closed 97 CS on 09-30, opened 0 on 10-01), so the SD cycle must use stock received the same day; whether Generate Opening Balances serves other products is unknown. Default: do not run the button; start the SD block with a DA of the day. (Superseded in part 2026-10-05: previous closings ARE carried once the first movement of the day creates the rows (Q-OB1 answered); the 10-01 single-row anomaly is Q-OB2. Starting the SD block with a DA of the day remains the rule.)

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
| L07 | DONE | G11-1 (learning_sessions/2026-10-01_G11-PK_session1_log.md) | Lists read live: Order Cancellation reasons Bad Weather / Credit Exceeded / Law & order Issue / Shop Closed; Order Editing Reason Type Order Change QTY / Wrong Order /No Order / No Scheme / Stock Already Avl.; Reschedule reasons incl. duplicates (Law & Order Issue x5, Shop Closed x2, Test Reason 716); Sales Return reasons No Cash / Wrong Order/No Order / Shop Closed / Credit Exceeded |
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
| L18 | PARTLY | G11-1 (learning_sessions/2026-10-01_G11-PK_session1_log.md) | Delivery Date Change 10-07 -> 10-01 on 5 orders: delivery PJP stays 02112 (PJP Delivery No unchanged), status stays Confirmed; past-date refusal (L17) still not tried |
| L19 | DONE | G11-1 (learning_sessions/2026-10-01_G11-PK_session1_log.md) | baseline snapshot 16:4x before DA 1358 approval (39 rows; openings present, 62740537 Opening 160) |
| L20 | DONE | G11-1 (learning_sessions/2026-10-01_G11-PK_session1_log.md) | DA 1358 (5 lines, 2 with losses) approved by the Checker: In += received qty exactly, day row already existed |
| L21 | DONE | G11-1 (learning_sessions/2026-10-01_G11-PK_session1_log.md) | loss record 639 approved: NO Damaged/Lost stock row appears (row count unchanged); loss approval has no Stock Inquiry effect |
| L22-L33 | PARTLY | G11-1 (learning_sessions/2026-10-01_G11-PK_session1_log.md) | DONE same day: orders (6), allocation/unallocation, delivery date change, GIN 506 + approval, edit/cancel after GIN, Cashmemo Reschedule + Status, Sales Return + approval + pick, deposit slips 1131-1136, GRN 246 + approval, stock snapshots after DA/GIN/GRN. NOT DONE: SAN / OTC stock out, Route Settlement (blocked: "Following previous days not closed! Please close date. 2026-09-30"), final closing snapshot |

### What remains
- Same-day cycle L19-L33 (new DA with four framework products, Checker approval, orders with qty = ATP and ATP + 1, Unallocate, Order Editing, Delivery Date Change, GIN with Draft Forward by the Maker and approval by the Checker, Cashmemo Status, Sales Return, GRN, Deposit Slip, Route Settlement, SAN, final snapshot). Open questions it closes: Q08, Q16, Q18 (detail messages), Q21, Q22 (real dropdowns), Q26, Q27, Q31, Q32, Q33, Q34, Q41-Q43, Q45, Q46, Q48, Q50, Q58, N1, and BA3 (loss approval L21).
- Any-day leftovers: L13 (DA delete/reject), L16 (DSR Adjustment), L17/L18 (delivery date change), L09 Edit-mode read of the PJP dropdowns.
- Learned helper notes for the cycle: enter the quantity only after stock type and batch have filled (otherwise "The lost quantity does not equal the sum of dispatch and received quantities", nothing saved); after Add pick Warehouse, Vendor and DA Type; use the calendar popup for dates on Order Cancellation; the Maker's Forward only on Drafts, the Checker's Forward only on Pending.

## Status after G11-2 / G11-2b (2026-10-05)

Evidence: [learning_sessions/2026-10-05_G11-PK_session2_log.md](learning_sessions/2026-10-05_G11-PK_session2_log.md) (seq 1-50) and [learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md](learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md) (seq 51-71). [x] = settled, [~] = partly, [ ] = still open.

| Id | Tick | Result 2026-10-05 |
|---|---|---|
| L01-L05, L07, L08, L10-L12, L19-L21 | [x] | done earlier; reproduced on a second day where re-walked (DA 1359, loss 640, stock snapshots) |
| L02 (new day) | [x] | 0 rows before the DA; after DA 1359 approval 39 rows with carried Openings (Q-OB1 answered) |
| L09 | [x] | PJP Daily Inquiry Update Edit mode read and used: Mark Status End Of Day (only), DSR Files Status Process / Complete; "Record Updated Successfully", Current Status E (Q55 answered; Q-RS1 partly) |
| L13 | [ ] | DA Delete / Reject still not run (Q02) |
| L14 | [~] | unchanged (Q18) |
| L15 | [~] | slip validation messages: "Required Fields are empty!" (ticked cheque row without cheque details) observed; amount 0 / text not tried |
| L16 | [ ] | DSR Adjustment Amount screen read; save not done: seq 56 bypassed by the QA lead (Q53) |
| L17 | [ ] | past delivery date not tried (Q29) |
| L18 | [~] | second move 10-11 -> 10-05: PJP Delivery No 02112 unchanged (Q30 partly) |
| L22 | [~] | orders booked within ATP only; ATP + 1 not tried (Q16, Q27) |
| L23 | [~] | one-order Unallocate / Allocate "Process completed successfully" again (Q26 partly) |
| L24 | [x] | edit after the GIN keeps the Document No, totals = workbook (Q21 answered); edit before Delivery Date Change impossible (Q-OE1, Q-OE4) |
| L25, L26 | [x] | Delivery Date Change 5 orders; GIN 507 Maker Forward + one Checker Forward; Out +35, Closing unchanged (date variant of Q34 not tried) |
| L27 | [x] | Cashmemo Status: ticked memos Delivered/Invoiced, "Updated successfully"; partly returned memo stays Delivered/Invoiced (Q32, Q33 answered) |
| L28 | [x] | Sales return 714: Picked after Save Sale Pick (Q41); slab re-pricing on non-returned lines (Q43 re-answered, Q-SR2); no snapshot between approval and GRN (Q42 partly) |
| L29 | [x] | GRN 247: Sound, same day, In +19, Out unchanged (Q08 answered) |
| L30 | [x] | Slips 1137-1142; posting at Route Settlement, Un Posted -> Posted, remainder trimmed (Q-DS1, Q45, Q46 answered) |
| L31 | [~] | Route Settlement read before (blocked: "...Please close date. 2026-10-01") and after the QA team member settled it (Complete, Cash Shortage 0, Q-RS2 answered); Offset = posted allocations (Q50 answered); the settlement entry itself not seen (Q48 partly) |
| L32 | [~] | SAN 96 Stock Adjustment Admin -50 CS: Out +50 after approval; no snapshot after the Maker's Forward (Q58 partly) |
| L33 | [x] | Final snapshot seq 60: Opening 308 / In 99 / Out 85 / Allocated 63 / Closing 259; identity holds (Q31 answered) |

New class B checks from 2026-10-05 (add to the next walk):

| Id | Step (standard vocabulary) | User | Observe and record | Changes data? | Questions |
|---|---|---|---|---|---|
| ~~L34~~ | DROPPED 2026-10-06: Q-OB2 answered [stated 2026-10-06 QA Team Lead] (see OPEN_QUESTIONS.md section 2c); original check kept for the record: [Maker] Navigate to Stock Inquiry before the first movement of a new day; then let the first movement be something other than a DA (e.g. GIN approval of stock received earlier) and Show Inquiry again | Auto_Multi_Orga | row count, Opening per row (carried or 0) | S (only the movement itself) | Q-OB2 |
| ~~L35~~ | DROPPED 2026-10-06: Q-OE4 answered [stated 2026-10-06 QA Team Lead] (see OPEN_QUESTIONS.md section 2c); original check kept for the record: [Maker] Navigate to Order Editing; for an order with delivery date tomorrow Choose Date To = tomorrow | Auto_Multi_Orga | whether the order is listed | no (RO) | Q-OE4 |
| L36 | [Maker] Navigate to Deposit Slip; compare Status of the slips of a Complete route/date; ask the QA lead how that date was completed | Auto_Multi_Orga | Un Posted vs Posted per slip | no (RO) | Q-DS3 |
| L37 | [Maker] Navigate to Route Settlement; open Total Order / Delivered Orders links of 02112 | Auto_Multi_Orga | which orders make up Total Order | no (RO) | Q-RS3 |
| L38 | [Maker] On the day after a closed day, open Route Settlement Edit on a route while another zero-activity route of the previous day is Incomplete | Auto_Multi_Orga | blocked or not | D (only if settled) | Q-RS4 (Q-RS1 answered 2026-10-06 [stated 2026-10-06 QA Team Lead]: the day close clears the per-PJP check) |
| ~~L39~~ | DROPPED 2026-10-06: Q-DJ1 answered [stated 2026-10-06 QA Team Lead] (see OPEN_QUESTIONS.md section 2c); original check kept for the record: [Maker] Navigate to DSR Adjustment Amount; compare 02112 Total Shortage with Route Settlement history | Auto_Multi_Orga | composition of Total Shortage | no (RO) | Q-DJ1 |

New checks from 2026-10-06 (G11-3):

| Id | Step (standard vocabulary) | User | Observe and record | Changes data? | Questions |
|---|---|---|---|---|---|
| L40 | [Maker] Navigate to Stock Inquiry; Choose yesterday's date; read Closing of the cycle products; Choose today's date before the first movement / after it; compare Opening with yesterday's Closing | Auto_Multi_Orga | Opening = previous Closing (carry-over job ran) or 0 (environment issue, report it) | no (RO) | pre-check from the Q-OB2 ruling |
| L41 | [Maker] Book (or find) a zero-tax order of a NON-exempt outlet; put it on a GIN and try Cashmemo Status Delivered | Auto_Multi_Orga / Auto_Tssm | where the delivery is blocked and the exact message | D | Q-TX1 rule (stated, not yet observed) |
## Status after the QA team written answers (2026-10-08)

Source: [learning_sessions/2026-10-08_QA_Team_Review_answers.md](learning_sessions/2026-10-08_QA_Team_Review_answers.md). A stated answer closes the question; the walk item stays optional only to capture the exact message or value. [x] = settled, [~] = partly, [ ] = still open.

| Id | Tick | Result 2026-10-08 [stated 2026-10-08 QA Team] |
|---|---|---|
| L16 | [x] | Q53 answered: no workflow on the DSR adjustment (observed direct save 10-06 agrees) |
| L17 | [x] | Q29 answered: delivery date cannot be earlier than the order date; optional: capture the message |
| L22 | [x] | Q16 / Q27 answered: > available -> only the available qty allocated; none -> unallocated, status Order; optional: capture Allocation Status of a partial order |
| L31 | [x] | Q48 answered: Payable - Received = DSR Cash Shortage; optional: observe it when a case reduces cash Received |
| L32 | [x] | Q58 answered: stock moves on approval |
| L36 | [x] | Q-DS3 answered: a Complete route with Un Posted slips is a defect (LIVE_FINDINGS D-G11-2b-1); no walk needed |
| L28 (Q42) | [~] | Q58 (stock moves on approval) and the GRN evidence suggest the return moves stock only via the GRN; snapshot between return approval and GRN still not taken |
| L38 | [~] | Q-RS4: check = working date today and closing date N-1 per PJP; zero-activity detail open |
| L41 | [~] | rule refined: record ZERO_TAX_ORDER_EXEMPTION first (N blocks, Y allows) |

New checks from the 2026-10-08 answers:

| Id | Step (standard vocabulary) | User | Observe and record | Changes data? | Questions |
|---|---|---|---|---|---|
| L42 | Ask the QA team (or read the ORGA parameter screen) for CASHMEMO_EDIT of org 010104; then [Maker] edit an order on an approved GIN (reduce 1 CS, reason); read the GIN detail Actual quantity and Stock Inquiry Out / Allocated / Closing before and after; later read the GRN Suggested | Auto_Multi_Orga | whether the approved GIN quantity and Out drop at the edit save, or the cut returns on the GRN (as on 3 walks) | S | Q-OE5 (contradiction 28) (settled 2026-10-08 follow-up: no stock movement at the edit; only the optional parameter read remains) |
| L43 | [Maker] Navigate to the Profile / user setup screen (read-only); read the role code and Authorized flag of Auto_Multi_Orga, Auto_Tssm and KPO_mp; [Maker] open a Pending DA he forwarded and read whether Forward (approve) is enabled | Auto_Multi_Orga | role codes vs 0001 / 0002; why self-approval of DA 570 was possible | no (RO) | Q-RL1 (contradiction 31) |
| L44 | Optional, only with the QA Team Lead's go-ahead: before the GRN of the day is approved, [Maker] Navigate to Route Settlement; Click Edit on the route | Auto_Multi_Orga | whether "Stock Mismatch" appears (exact text) | no (blocked) | rule 19 (stated) |

Status after the QA team follow-up answers (2026-10-08) [stated 2026-10-08 QA Team (follow-up)], source [learning_sessions/2026-10-08_QA_Team_followup_answers.md](learning_sessions/2026-10-08_QA_Team_followup_answers.md):

| Id | Tick | Result |
|---|---|---|
| L42 | [x] | Q-OE5 answered: no stock movement when a cash memo is edited after the GIN (matches 3 walks; contradiction 28 resolved). Optional only: record the CASHMEMO_EDIT value of org 010104; no stock observation needed |

New check from the follow-up:

| Id | Step (standard vocabulary) | User | Observe and record | Changes data? | Questions |
|---|---|---|---|---|---|
| L45 | Ask the QA team which document "Return Document" is; then [Maker] Navigate to the menu search and look for a purchase return / return to company option (read-only); if one exists and the QA Team Lead agrees, take a Stock Inquiry snapshot before and after its approval | Auto_Multi_Orga | the option name, document type, and whether its approval posts Out (not In) for the returned quantity | no (RO) unless the QA Team Lead approves a document (then S) | Q-SV2 |

## Block 1: read-only, any day (RO)

| Id | Step (standard vocabulary) | User | Observe and record | Changes data? | Risk | Depends on | Questions |
|---|---|---|---|---|---|---|---|
| L01 | [Maker] Navigate to Stock Inquiry; Choose Balance Date 2026-09-30; Click Show Inquiry; read all 39 rows | Auto_Multi_Orga | per row Opening, In, Out, Allocated, Closing (CS/DZ/PC); test Closing = Opening + In - Out - Allocated on every row; note any row where Allocated is not subtracted | no (RO) | low; do not click Generate Opening Balances | none | Q11 |
| L02 | [Maker] Navigate to Stock Inquiry; Choose today's date; Click Show Inquiry | Auto_Multi_Orga | row count (expect "No data" on a new day), date default | no (RO) | low | none | Q10 evidence |
| L03 | [Maker] Navigate to Transaction Inquiry; Choose Document Type Sales, date range covering 2026-09-30; open orders COL26000001995-2002 | Auto_Multi_Orga | text of Document Status, Execution Status, Delivery Date, PJP Delivery No; Total Offering Discount vs header Discount; Detail line sums | no (RO) | low | orders exist from the 09-30 run | Q23, Q28, Q30 (baseline) |
| L04 | Read-only SQL (snd-schema/overlay connector): status descriptions of those order numbers and of CM-01 document and execution statuses for 010104 | no browser | whether "Confirmed" is execution 02 or an alias of 04 Ordered | no (RO) | low | connector authorised | Q23 |
| L05 | Read-only SQL: workflow definition of GIN (StockUpdateGIN4Level) levels | no browser | number of approval levels | no (RO) | low | connector | Q35 |
| L06 | (observation only) see L12 | | | | | | |
| L07 | [Maker] Navigate to Order Editing and Order Cancellation; open the Reason Type and Cancellation Reason lists; [Maker] Navigate to Cashmemo Reschedule; open the Reschedule Reason list | Auto_Multi_Orga | the full option lists (do not Save) | no (RO) | low; do not click Cancel/Process | none | Q22 |
| L08 | [Maker] Navigate to Stock Adjustment SAN; open the SAN Type dropdown | Auto_Multi_Orga | which type reads as OTC stock out; record that no "OTC Stock Out" menu exists | no (RO) | low; do not Save | none | Q57 |
| L09 | [Back-office] Navigate to PJP Daily Inquiry Update; open Mark Status and DSR Files Status lists | Auto_Multi_Orga | allowed values | no (RO) | low; do not click Edit/Save | none | Q55 |
| L10 | [Maker] Navigate to Goods Issue Note; open an existing Draft and a Pending GIN; note which of Forward, Reject, Terminate, De-linking are enabled for Maker; repeat as Checker | Auto_Multi_Orga, Auto_Tssm | button states per status and user | no (RO) | low; do not click any | existing GINs (505, others) | Q36, Q37 |

## Block 2: data-changing, no stock movement (D), any day

| Id | Step | User | Observe and record | Data/stock | Risk | Depends on | Questions |
|---|---|---|---|---|---|---|---|
| L11 | [Maker] Navigate to Dispatch Advice; Create DA with a SO Number; Save; Create a second DA with the same SO Number; Save | Auto_Multi_Orga | message on the duplicate, new Document Nos | D (Draft DAs, no stock) | low; leaves Draft DAs | none | Q04 |
| L12 | [Maker] Create a DA with one line and a loss row; Forward with comment; [Maker] Navigate to Loss Approval and look for the record BEFORE any checker action | Auto_Multi_Orga | whether a loss record exists at maker Forward (Pending for approval) and its Serial No | D (record only) | low; DA stays Pending (do not approve unless in Block 3) | none | Q06 |
| L13 | [Maker] Create a DA with one line; Delete it. Create another DA, Forward; [Checker] Navigate to the DA; Click Reject with comment | Auto_Multi_Orga, Auto_Tssm | messages and final statuses (Draft delete, Rejected); whether a Rejected DA creates stock (it must not) | D (no stock if Rejected) | medium: Reject is data-changing; confirm the DA is a throwaway | none | Q02 |
| L14 | [Maker] Navigate to Order Booking; Click Validation with each header field empty in turn (no Save) | Auto_Multi_Orga | which fields block, exact messages | no data saved if blocked | low; do not click Save | none | Q18 |
| L15 | [Back-office] Navigate to Deposit Slip, click the Cash variants and the save with amount 0, text, special characters on a throwaway | Auto_Multi_Orga | messages (not in checklist class B unless listed; run only if a delivered cash memo exists) | D | medium | delivered cash memo | Q45 prerequisite |
| L16 | [Back-office] Navigate to DSR Adjustment; add one small adjustment with Comments to a test PJP; read status on Detail tab | Auto_Multi_Orga | status after save (Authorized / Un-Authorized), displayed amount | D (AD-07 row) | medium: finance row cannot be deleted by us | PJP row | Q53 |
| L17 | [Maker] Navigate to Delivery Date Change; Choose Order Date and a PJP that has orders; Choose a past Delivery Date; Click Process | Auto_Multi_Orga | whether refused and the message | D if accepted (changes dates) | medium: moves delivery dates of real test orders; run before the SD block and restore the date | orders of that PJP | Q29 |
| L18 | After L17 and a valid change: [Maker] Navigate to Transaction Inquiry; compare Delivery Date and PJP Delivery No before/after | Auto_Multi_Orga | whether the delivery PJP changes | D | medium | L03 baseline | Q30 |

(L06 is merged into L12; ids kept to avoid renumbering.)

## Block 3: same-day receive-and-issue cycle (SD), in Daily Cycle order, one calendar day

| Id | Step | User | Observe and record | Data/stock | Risk | Depends on | Questions |
|---|---|---|---|---|---|---|---|
| L19 | [Maker] Take a before snapshot of Stock Inquiry for product 62740537 in Auto Main Warehouse (all stock types) | Auto_Multi_Orga | all 5 column groups | RO | low | none | baseline |
| L20 | [Maker] Create DA (one line, one loss row), Forward; [Checker] approve; | Auto_Multi_Orga, Auto_Tssm | messages, Received Date; exact stock delta; **do rows appear for today without Generate Opening Balances?** | S (Sound In rises by received qty) | medium: stock-changing, part of the authorised cycle | L12 outcome | Q10 evidence, Q31 |
| L21 | [Checker] Navigate to Loss Approval; Forward; then [Maker] re-read Stock Inquiry for stock types 02, 04 | Auto_Tssm, Auto_Multi_Orga | whether Damaged/Lost rows appear (feeds BA3) | S/unknown | medium | L20 | evidence for Q05 |
| L22 | [Maker] Book an order with quantity = ATP and one with ATP + 1 (Validation, Save) | Auto_Multi_Orga | blocked / warned / accepted, Allocation Status | S (Allocated) | medium | L20 stock | Q16, Q27 |
| L23 | [Maker] Navigate to Order Stock Allocation; Click Unallocate on a same-day order (accept alert) | Auto_Multi_Orga | message (was "stock not found."), whether it now works | S (allocation) | medium | L22 | Q26 |
| L24 | [Maker] Navigate to Order Editing; open an order; change a quantity; Validation; Save | Auto_Multi_Orga | whether the order is reachable, Order Number same or new, totals | D/S | medium | L23 outcome | Q21 |
| L25 | [Maker] Navigate to Delivery Date Change; Choose valid date; Process | Auto_Multi_Orga | processed count | D | low | orders | feeds L26 |
| L26 | [Maker] Create GIN (Cash Memo Selection, Save All), Forward; [Checker] approve with Delivery Date today and again variant with a future Delivery Date | Auto_Multi_Orga, Auto_Tssm | which date the stock check uses, messages; Stock Inquiry Out and Allocated delta, execution status of the cash memos | S (stock out) | **high**: stock-changing; two GINs needed for the date variants | L20, L25 | Q31, Q34 |
| L27 | [Maker] Navigate to Cashmemo Status; Choose PJP; read grid; Save All on one cash memo | Auto_Multi_Orga | grid columns, message ("Updated successfully"), document and execution status in DB | D | medium | L26 | Q32, Q33 |
| L28 | [Maker] Sales Return: return one line with a discount; Validate, Save, Forward; [Checker] approve; [Maker] Status Change | Auto_Multi_Orga, Auto_Tssm | Discount reversal, Return quantity vs ordered/delivered, stock snapshot after each step | S (none expected until GRN) | medium | L27 | Q41, Q42, Q43, Q40 evidence |
| L29 | [Maker] Goods Return Note: Delivery Man PJP, edit rows, Save All, Forward; [Checker] approve; [Maker] snapshot | Auto_Multi_Orga, Auto_Tssm | stock type and day credited, messages | S (stock In) | high: stock-changing | L26 | Q08 |
| L30 | [Maker] Deposit Slip full-amount cash on the delivered cash memo; read status, Unposted variant | Auto_Multi_Orga | status I -> A trigger, Unposted Amount meaning | D | medium | L27 | Q45, Q46 |
| L31 | [Maker] Route Settlement for the PJP/date; read payable, received, shortage screens; then Transaction Inquiry Offset Amount | Auto_Multi_Orga | payable vs received, Offset Amount | D (settlement row) | medium | L30 | Q48, Q50 |
| L32 | [Maker] SAN stock out of 1 PC, Forward; snapshot; [Checker] approve; snapshot | Auto_Multi_Orga, Auto_Tssm | whether stock reduces at Forward or approval | S | high | L20 | Q58 |
| L33 | [Maker] Final Stock Inquiry snapshot; compare with L19 step by step and the identity Opening + In - Out - Allocated | Auto_Multi_Orga | total effect of the cycle per step | RO | low | all | Q31 |

## Summary
- RO any-day items: L01-L05, L07-L10, L33 baseline reads; D any-day: L11-L18; SD (same-day receive and issue required): L19-L32.
- Items that change stock: L20, L21 (maybe), L22 (allocation), L23, L26, L29, L32. These need the BA/environment owner's go-ahead for the day plan; the Generate Opening Balances button is excluded in all steps.
- Class C questions that this checklist can only inform, not close: BA3 (losses), BA6, BA7, BA9, BA14 (BA1 was answered by the DA approval evidence).
