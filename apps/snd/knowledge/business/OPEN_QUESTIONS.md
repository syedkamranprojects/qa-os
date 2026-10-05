# Open questions: consolidated and classified (S&D / DCODE business knowledge)

Updated: 2026-10-05 (consolidation of learning sessions G11-2 and G11-2b; earlier: 2026-10-01 live blocks 1-3b and G11-1)

Consolidated 2026-10-01 from section 12 of the 26 area pages (73 questions as written, 60 unique after merging 13 duplicates; the Q numbers have gaps because merged questions keep the lowest id). Source ids: page code + number, e.g. DA2 = Dispatch Advice question 2 (codes at the end of this file). Questions raised by the learning sessions keep their page ids (Q-OE1, Q-DS1, ...) so references in the pages do not break; since 2026-10-05 they are filed in the class sections below (the former unnumbered section 8 "New from learning session G11-PK 1" is merged in). Live evidence: [LIVE_FINDINGS.md](LIVE_FINDINGS.md) blocks 1, 2a, 3a, 3b (2026-10-01); [learning_sessions/](learning_sessions/README.md) G11-1 (2026-10-01), G11-2 and G11-2b (2026-10-05).

Classes: **A** default is fine (no BA time; see appendix), **B** verify live (see [LIVE_LEARNING_CHECKLIST.md](LIVE_LEARNING_CHECKLIST.md)), **C** decision by the BA (section 1a) or by the QA lead / framework owner (section 1b).

**Status after the 2026-10-05 consolidation: open 56 = A 15 + B 22 + C 19** (before: 70 = A 16 + B 32 + C 22, counting the 18 items of the former section 8). Closed in this consolidation: 21 answered (10 by G11-2/2b evidence, 11 by G11-1 evidence that had been written into the pages but not into this file) and 2 merged as duplicates; 9 new questions (B 6, C 3). Exact arithmetic in section 6.

## 1. Class C: decisions (19 open)

### 1a. BA decision list (15 open; hard maximum 15)

Order follows the Daily Cycle. Each has default, why it matters, evidence. BA1, BA5, BA6, BA7, BA9 were answered by evidence (section 2); BA3 is merged into Q-LA1; the numbers are kept so references do not break.

**BA2. Must the app prevent the maker from approving his own document (DA, DA loss, GIN, GRN, SAN, Sales Return), or is "maker and checker differ" only a QA convention?** [Q01; merged 2026-10-05 with Q-DA1 "May the Maker approve or reject his own Pending Dispatch Advice (buttons stay enabled for him)?"]
- Default: it is a QA rule; self-approval cases are reported as a deviation note, not a defect.
- Why: decides whether the negative case "same user approves" expects a block or a pass.
- Evidence: KPO_mp approved its own DA 570 [observed]; the GIN workflow of org 010104 (StockUpdateGIN v53) declares Verify and Approve for the SAME role 0005 [db 2026-10-01], so the workflow does not separate the people; the Checker's buttons (Forward/Reject/Terminate) are enabled only on Pending documents [observed]. Whether the BA wants it enforced is the open point.
- 2026-10-05: on the Pending DA 1358 the Maker still had Forward/Reject enabled while on the Pending GIN 506 they were disabled [observed 2026-10-01 G11-1]; the Checker has Reject on Pending SAN 96 and Pending GRNs [observed 2026-10-05 G11-2b].

**BA4. Which delivery date should a booked order carry before the GIN: the PJP's next visit date (2026-10-05 observed) or today, and are past dates refused?** [Q17]
- Default: orders carry the PJP's next visit date; Delivery Date Change moves them to today before the GIN.
- Why: the GIN needs a typed Delivery Date and eligible cash memos; wrong date gives an empty Cash Memo Selection.
- Evidence: order_booking.md, delivery_date_change.md (draft question 3); live 2026-10-01: the 8 orders on GIN 505 carry 2026-09-30 (moved), cancelled orders 1986/1993 still carry 2026-10-05.
- 2026-10-05: third data point: bookings of 09-29 -> 10-05, 10-01 -> 10-07, 10-05 -> 10-11 [observed]; Delivery Date Change needed before the GIN on both walk days; Order Editing lists only orders whose delivery date is today (Q-OE1). The "next visit" rule stays [inferred] (PJP calendar not read).

**BA8. Is a sales return limited to the quantity ordered or the quantity delivered, and may it be made before the cash memo is delivered?** [Q40]
- Default: limited to delivered quantity; only after delivery.
- Why: boundary values of the return quantity and the order of the chain.
- Evidence: message says "ordered quantity" (sales_return.md).
- 2026-10-05: Invoice Qty on the return = the delivered (edited) 4 CS; only delivered memos are offered (both days) [observed]; over-return not tried.

**BA10. Does a Deposit Slip need checker approval?** [Q44]
- Default: no, single maker step.
- Why: the approval row 00140002 is inactive; defines whether an approval case exists.
- Evidence: deposit_slips.md.
- 2026-10-05: slips were posted by Route Settlement without any approval step [observed 2026-10-05 G11-2b]; Forward/Reject buttons remain unused.

**BA11. What does a bounced cheque do to the outlet receivable, and which cheque status transitions are allowed?** [Q51]
- Default: the invoice becomes outstanding again; only P/L to R or B.
- Why: negative and transition cases of Cheque Status.
- Evidence: cheque_status.md (no rows, no flow beyond selection).
- 2026-10-05 (narrows the transition part of the default): after posting the cheques read "Clear" and the screen offers only Bounce (no Realized / Presented / Collected) [observed 2026-10-05 G11-2b]; Bounce not pressed (one-way). Open: the effect of Bounce on the receivable.

**BA12. What is the effect of a DSR Adjustment (sign, debit/credit, link to cash shortage) in Route Settlement?** [Q52]
- Default: the sign decides debit or credit and it changes the cash shortage.
- Why: its assertion is toast plus detail amount only; the finance effect cannot be tested without the rule.
- Evidence: dsr_adjustment.md.
- 2026-10-05: screen read: per PJP Total Shortage / Total Adjusted / Balance = Shortage - Adjusted (02112: 2,477,571.11 / 1,649,970.43 / 827,600.68); nothing saved (seq 56 bypassed by the QA lead) [observed 2026-10-05 G11-2b]. See also Q-DJ1.

**BA13. Does a stock write-off through a SAN produce a financial posting (value, moving average price) in addition to the stock change?** [Q59]
- Default: stock value only, no other posting.
- Why: end-of-day finance checks.
- Evidence: otc_stock_out_and_san.md.
- 2026-10-05: SAN 96 line Gross -771,146.50 (100 PC x 7,711.47, price per PC), Tax 0; stock Out +50 on approval [observed 2026-10-05 G11-2b]; no finance screen read.

**BA14 (new 2026-10-01). Is Generate Opening Balances still part of the day (does it carry the previous day's closing for products that are not received that day), who runs it, and is carrying the previous day's stock meant to be automatic?** [new, follows from Q10] **PARTLY ANSWERED 2026-10-05**
- Default: not part of the QA cycle; the cycle starts with a DA of the day (the DA approval creates the row of a received product); stock received on an earlier day is not usable the next day without it, and the cycle never relies on earlier stock.
- Why: 62740537 closed 97 CS on 2026-09-30 but opened 0 on 2026-10-01 after the DA approval, and GIN 505 approval on 09-30 was refused for stock received 09-29: previous closings are not carried automatically. Any case that issues stock not received that day depends on the answer.
- Evidence: Stock Inquiry 09-30 vs 10-01 (LIVE_FINDINGS L01, S1, S2); button never clicked (not authorised).
- 2026-10-05 (answers the carry part, supersedes "previous closings are not carried automatically" in Why): the first movement of a new day (DA 1359 approval) created all 39 rows with Opening = previous Closing + still-Allocated (62740537: 245 + 63 = 308) without the button [observed 2026-10-05 G11-2]. Still open: what the button does, who may run it. New default: never needed in the QA cycle; never click it.

**Q-OE1 (revised 2026-10-05). Order Editing listed only orders whose delivery date is today: is the edit before the GIN (seq 15) meant to run AFTER Delivery Date Change, or should orders be booked with a delivery date of today?**
- Default: run Order Editing after Delivery Date Change.
- Why: as automated, seq 15 can never find a freshly booked order (delivery date = next visit).
- Evidence: 2026-10-05: ranges 10-05..10-11 and 10-11..10-11 empty for orders delivered 10-11; after Delivery Date Change the orders were listed (seq 29) [observed 2026-10-01, 2026-10-05]. The G11-1 hypothesis "Date To must cover the delivery date" is superseded.

**Q-OE3. Should editing / cancelling an order on an approved GIN be blocked or warned (business control)?** [absorbs the intent part of BA6]
- Default: allowed (as observed); record as defect candidate.
- Evidence: allowed with no warning and no stock movement on 2026-10-01 (2003, 2007) and 2026-10-05 (2009, 2013) [observed].

**Q-DS2. Is a duplicate cheque number for the same outlet allowed, and should a cash memo already fully allocated on an unposted slip be blocked on another slip?**
- Default: both should be blocked (current acceptance = defect candidate).
- Evidence: cheque 1234567 accepted twice on 10-01 (1134, 1135) and again on 10-05 (1140, 1141); both visible on Cheque Status [observed].

**Q-DA3. Why does the product label price differ from the Purchase Price / PC (and purchase exceed trade price for some SKUs)?** (page inbound_stock/dispatch_advice.md)
- Default: label shows another price list; assert amounts on Purchase Price / PC only.

**Q-LA1. Is an approved DA loss used anywhere else (claim to the supplier, finance, a claim loss log)?** (page inbound_stock/da_loss_approval.md) [merged 2026-10-05 with BA3 "Where do approved DA losses appear as stock or claims?"; the stock part is answered: no stock row on approval, two days]
- Default: claim record only, no stock effect.

**Q-TI1 (new 2026-10-05). After an order edit, why does Transaction Inquiry Detail show Allocated = original 7 CS and Ordered = "5 CS 4 PC" for the edited line (Delivered 4 CS, amounts follow the edit)? What should Ordered / Allocated mean after an edit?**
- Default: they keep the as-booked values; assert Delivered and amounts only.
- Evidence: COL26000002009 Detail line 1 [observed 2026-10-05 G11-2b].

**Q-SR2 (new 2026-10-05). Is it intended that a part return re-prices the order's slab promotions, so the credit includes discount/tax reversals on lines that were not returned?**
- Default: yes, promotions are recomputed on the remaining basket.
- Evidence: return COL26000000714 lines 2-5 (0 returned) carry -116.35 / -61.23 / -40.31 / -0.48 discount reversals [observed 2026-10-05 G11-2b].

### 1b. QA lead / framework owner decisions (4 open)

| Id | Question | Default | Evidence |
|---|---|---|---|
| Q-RS1 | How is a working day closed, in what order with settlement, and may it be done on cnr1dev1? **PARTLY ANSWERED 2026-10-05**: a day is closed on PJP Daily Inquiry Update (Mark Status End Of Day + DSR Files Status Complete -> Current Status E, "Record Updated Successfully"); a QA team member closed the earlier un-closed days this way (10-01 row reads E / End Of Day / Complete); on 10-05 the route was settled first, then the day closed. Open: the detailed procedure promised by the QA lead (order, permissions, whether the close is what clears "Following previous days not closed!") | ask the QA lead before closing days on the shared env | [stated 2026-10-05 QA lead]; [observed 2026-10-05 G11-2b] |
| Q-OE2 | Which order should group 11 seq 15 edit when workbook outlets 1000000001-03 are not offered on cnr1dev1? | the outlet-04 order | seq 15 skipped by the QA lead on 10-01 and 10-05 |
| Q-SV1 | May the framework stock checks (seq 9, 24, 50, 60) be changed to before/after deltas (needs a pre-snapshot step)? | yes, deltas | FRAMEWORK_DRIFT.md rows 9-12 |
| Q-CS1 (new 2026-10-05) | Does framework seq 55 press Bounce (event after selecting the cheque row), and since "Realized" does not exist on the screen, what should seq 55 assert? | keep seq 55 bypassed; never Bounce in group 11 | screen offers only Bounce; cheques already "Clear" [observed 2026-10-05 G11-2b]; QA lead asked for Realized and bypassed seq 55 [stated 2026-10-05] |

## 2. ANSWERED

### 2a. By the live walk 2026-10-01 (10 questions)

Each answer carries the new default or rule. Evidence ids refer to LIVE_FINDINGS.md.

| Q | Question | ANSWER (new default / rule) | Evidence |
|---|---|---|---|
| Q04 | Duplicate SO Number blocks save (DA4) | NO. Duplicates are allowed (DA 1353 and 1354 both saved with LEARN_SO_01, "Saved successfully") and SO Number is optional (DA 1355 saved empty). Rule: no uniqueness check on Save; do not write a negative case for it. | L11 [observed] |
| Q06 | Loss record created at DA Forward or approval (DAL2) | AT THE DA APPROVAL. After the maker's Forward the Loss Approval filter Document No 1356 gave 0 rows; after Auto_Tssm approved the DA it gave Serial 638, Pending for approval. A Draft's Forward belongs to the Maker; the loss record is a side effect of the checker's approval. Loss Approval is visible to the Maker. (2026-10-05: re-observed, serials 639 on 10-01 and 640 on 10-05.) | L12, C2, S4 [observed] |
| Q10 (BA1) | Is a start-of-day step needed before receiving and issuing? | NO for a received product: the DA approval creates the day's stock row (Opening 0, In = received 4 CS, Closing 4 CS) without Generate Opening Balances; In posts to the Received Date. Rule: the cycle starts with the DA; no start-of-day step. Caveat kept as BA14: Generate Opening Balances may still serve products not received that day and carry previous closings (unknown). (2026-10-05: on a new day the DA approval created ALL 39 rows with Opening = previous Closing + still-Allocated, so previous closings are carried; see Q-OB1 in 2b; BA14 narrowed.) | L02, C1, S1, S2 [observed] |
| Q11 | Is Allocated deducted from Closing (SI2) | YES. Closing = Opening + In - Out - Allocated holds on 39 of 39 rows of 2026-09-30 in base PC units; two rows fail literally only because of PC-to-CS carry (20050308 Auto Main, 32 PC per CS; 20061858 IBT, 12 PC per CS). Rule: assert the identity in base PC with the pack factor from the product name; Closing is available stock (ATP). (2026-10-05: identity held at every snapshot of 10-01 and 10-05.) | L01 [observed] |
| Q23 | "Confirmed" vs Ordered 04 (OL1, TI1) | "Confirmed" is its OWN execution status 02 (identifier ALC); "Planning completed" is execution 03 (identifier GIN, follows 02); Ordered is document status 04 and execution status 01. The Transaction Inquiry column Document Status shows the execution status text: the 8 orders on GIN 505 read "Planning completed". Rule: assert the Document Status column text, expect Confirmed after booking and Planning completed once on a GIN. | L03, L04 [observed + db] |
| Q28 | Total Offering Discount equals header Discount (TI2) | YES. Sum of the five offering lines equals the header Discount on all 8 orders (-29,971.82 vs -29,971.83 = 1 paisa rounding for 1995-2001; -16,264.08 exactly for 2002); tax is 0 on every promo line; Net is rounded to whole PKR. Rule: allow 0.01 tolerance. (2026-10-05: also for the edited order and the sales return.) | L03 [observed] |
| Q35 | GIN approval levels (GIN3) | TWO steps in org 010104: workflow StockUpdateGIN v53, user tasks Verify then Approve, both candidate group 0005 (Distributor Role, not an authorizer role). Four levels (StockUpdateGIN4Level v3: 0005, 0008, 0005, 0008) exist only for the parent orgs 0101/0102. Separation of duty is NOT declared. Rule: expect the checker flow to be Forward on a Pending GIN; whether Verify then Approve needs two Forward clicks is not observed (GIN 505 approval never completed). (2026-10-05: one Checker Forward approved GIN 506 and GIN 507.) | L05 [db] |
| Q36 | Add/remove cash memo on an approved GIN (GIN4) | De-linking is ENABLED for the Maker on a Draft GIN (29) and DISABLED on a Pending GIN (505); approved GINs are not listed on the screen. Rule: cash memos are removed only while the GIN is Draft; for an approved GIN only the adhoc add/remove statuses 24/25 exist. | L10, C3 [observed] |
| Q37 | Who may cancel a GIN (GIN5) | Only the Checker, and only on a Pending GIN: Auto_Tssm has Forward, Reject, Terminate enabled on Pending 505 and all disabled on Draft 29; the Maker has Reject and Terminate disabled on both. Rule: the Maker cannot cancel; Terminate effect on stock/cash memos still unknown (default: cash memos return to the selection pool). | L10, C3 [observed] |
| Q57 | Which SAN Type is "OTC Stock Out" (OT1) | NONE is labelled so and the sidebar search "OTC" finds nothing. SAN Type options: Warehouse To Warehouse Transfer, Stock Adjustment Entry, Stock Adjustment Admin, Physical Stock Reconciliation, Stock Adjustment From Transfer (Auto). Default updated to Stock Adjustment Admin (SA-03, single warehouse; all recent grid rows are of that type, no To Warehouse) [inferred mapping]; Q58 (stock direction at Forward vs approval) stays B. (2026-10-05: confirmed by the walk: SAN 96 of type Stock Adjustment Admin, approved with the workbook message.) | L08 [observed + inferred] |

PARTLY answered (stay open in section 3): Q18 (Order Booking has no header messages and no Validation button before the detail step: fields work by progressive disclosure, detail-step messages unread), Q22 (reason lists db-declared, dropdowns not opened because no order was eligible), Q30 (Transaction Inquiry has no Delivery-PJP column; delivery PJP is visible on the GIN; the date change was not re-run), Q55 (Mark Status = E End of Day; DSR Files Status = P process / C complete, db-declared; labels still to read in Edit mode). Also new evidence on Q31 (DA approval stock effect now known) and Q16/Q27 (product pick answers "Stock not available." when the product has no stock row for the day; ATP 4 CS = Closing; quantity above ATP not tried). (2026-10-05 status: Q22 and Q55 answered, see 2b; Q18 and Q30 still PARTLY; Q31 answered; Q16/Q27 unchanged.)

### 2b. Closed in the 2026-10-05 consolidation (21 answered + 2 merged)

"By" = which evidence closed it: G11-2 / G11-2b (new this consolidation) or G11-1 (evidence of 2026-10-01 already in the pages, now recorded here).

| Q | Class | Question | ANSWER (rule) | By | Evidence |
|---|---|---|---|---|---|
| Q-OB1 | B | Who or what generated the 2026-10-01 opening balances during the day? | The first movement of a new day (the DA approval) creates the rows of the whole catalogue with Opening = previous Closing + still-Allocated (62740537: 245 + 63 = 308); before it the day has 0 rows. Supersedes "previous closing is not carried". The 10-01 morning anomaly is Q-OB2. | G11-2 | stock_inquiry_and_balances.md [observed 2026-10-05] |
| Q-DS1 + Q45 | B | What is deposit-slip posting, when does it happen (what flips I to A); may a partly allocated slip be posted? | Posting happens at Route Settlement: slips 1137-1142 Un Posted -> Posted; Received/Balance and Offset updated; header locked; a partly allocated slip is posted with its amount trimmed to the allocation (1139: 1,000 -> 600). | G11-2b | deposit_slips.md [observed 2026-10-05] |
| Q-RS2 | B | What does settlement do with Sale Value not covered by collections? | Not a cash shortage (Cash Shortage 0); the uncovered amount stays open on the cash memos (2009 Balance 88,107). | G11-2b | route_settlement.md [observed 2026-10-05] |
| Q50 | B | How is Offset Amount derived (RS3)? | Sum of the posted deposit-slip allocations on the memo (2009: 600 + 1,000 + 1,000 = 2,600); returns are not included. Whether it fills before posting: not read. | G11-2b | transaction_inquiry.md [observed 2026-10-05] |
| Q55 | B | Allowed Mark Status / DSR Files Status values (PJ1)? | Mark Status: End Of Day only; DSR Files Status: Process, Complete; End Of Day + Complete = day close (Current Status E). | G11-2b | pjp_daily_inquiry_update.md [observed 2026-10-05] |
| Q33 | B | Partial Delivered (18) after a return (DL3)? | No: the partly returned memo stays Delivered/Invoiced; the return reads Picked with Demand Channel "Partial Return". | G11-2b | transaction_inquiry.md, sales_return.md [observed 2026-10-05] |
| Q41 | B | What Status Change (Picked) does (SR2)? | Save Sale Pick sets the return to Picked; its quantity goes to the GRN. | G11-2b (+G11-1) | sales_return.md [observed] |
| Q43 | B | Discounts reversed proportionally (SR4)? | Re-answered: NOT a simple pro-rata; returning part of the order re-prices its slab promotions, so non-returned lines carry small reversals (G11-1's "proportional" superseded). Intent: Q-SR2. | G11-2b | sales_return.md [observed values; rule inferred] |
| Q49 | A | Can a settled PJP/date be reopened (RS2)? | Not from the Route Settlement screen: a Complete row has no Edit. | G11-2b | route_settlement.md [observed 2026-10-05] |
| Q31 | B | Stock effect of allocation, GIN approval, GRN, sales return (DL1, GIN1) | Booking reserves (Allocated +, Closing -); cancel before GIN releases; GIN approval Allocated -> Out, Closing unchanged; edit/cancel after GIN none; GRN approval In +, Out unchanged; sales return via the GRN. Same on both days. | G11-1, confirmed G11-2 | stock_inquiry_and_balances.md |
| Q08 | B | Stock type and day credited by approved GRN (GRN2) | Sound, same day, as In; Out unchanged (GRN 246, 247). | G11-1, confirmed G11-2 | goods_return_note.md |
| Q21 | B | Edit keeps the same Order Number (OE3) | Yes (COL26000002003, 2009). | G11-1, confirmed G11-2 | order_editing_cancellation.md |
| Q22 | B | Reason lists for edit, cancel, reschedule (OE4, CR4) | Read live: edit Order Change QTY / Wrong Order /No Order / No Scheme / Stock Already Avl.; cancel Bad Weather / Credit Exceeded / Law & order Issue / Shop Closed; reschedule 14 options with duplicates; return No Cash / Wrong Order/No Order / Shop Closed / Credit Exceeded. | G11-1, confirmed G11-2 | checklist L07 |
| Q32 | B | Cashmemo Status meaning (CR1, DL2) | Ticked rows become Delivered/Invoiced ("Updated successfully"); no per-row undelivered choice. | G11-1, confirmed G11-2 | cashmemo_reschedule_and_status.md |
| Q46 | B | Meaning of Unposted Amount (DS3) | On a cash memo: amount allocated to it on OTHER not-yet-posted slips. | G11-1, confirmed G11-2 | deposit_slips.md |
| N1 | B | Why GIN Detail showed Current Stock 0-0-0 | Stale-day data: with same-day stock the GIN Detail Current Stock = Stock Inquiry Closing. | G11-1 | stock_inquiry_and_balances.md §6 |
| BA5 | C | How does an allocated order reach Order Editing / Cancellation (Q19)? | Allocation does not hide orders; Order Editing lists orders whose delivery date is today (after Delivery Date Change); Order Cancellation filters the order date. Remaining intent in Q-OE1. | G11-1, refined G11-2 | order_editing_cancellation.md |
| BA6 | C | Are edit/cancel allowed after the GIN is approved and what happens (Q20)? | Allowed, no warning, no stock movement; cancelled order keeps its GIN No; quantities return on the GRN (both days). Whether intended: Q-OE3. | G11-1, confirmed G11-2 | order_editing_cancellation.md |
| BA7 | C | What creates a GRN (Q07)? | Everything issued on the DSR's GIN and not delivered (cancelled / cut / rescheduled after the GIN) plus picked sales returns (19 CS on both days); the GIN Number fills from the delivery PJP. | G11-1, confirmed G11-2 | goods_return_note.md |
| BA9 | C | What happens to GIN quantities when a cash memo is rescheduled (Q38)? | The memo leaves the GIN (Reattempt, new delivery date) and its quantity returns on the GRN. | G11-1, confirmed G11-2 | cashmemo_reschedule_and_status.md |
| (merged) BA3 -> Q-LA1 | C | Where do approved DA losses appear | stock part answered (no Damaged/Lost row on approval, 10-01 and 10-05); claims part stays as Q-LA1 | G11-1, G11-2 | da_loss_approval.md |
| (merged) Q-DA1 -> BA2 | C | Maker may approve/reject own Pending DA | same decision as BA2 (self-approval) | - | dispatch_advice.md |

## 3. Class B: verify live (22 open)

Each is run in [LIVE_LEARNING_CHECKLIST.md](LIVE_LEARNING_CHECKLIST.md). Ordered by Daily Cycle. Status: OPEN, or PARTLY with what is already known.

| Q | Question (merged ids) | Status / live check, area/step, user | Needs same day cycle |
|---|---|---|---|
| Q-OB2 (new 2026-10-05) | Why did the first DA approval of 10-01 create ONE row with Opening 0 (rewritten to 160 later), while on 10-05 it created all 39 rows with Openings; does a non-DA first movement (GIN, SAN) open the day the same way? (page stock_inquiry_and_balances.md) | OPEN. Default: the 10-05 rule; 10-01 = environment anomaly. Check: morning snapshot, then first movement of another type. Maker | yes |
| Q02 | DA Reject / Terminate / Delete of a Draft (DA2) | OPEN. Inbound > DA: create Draft DA, Delete; second DA forward then Reject; record statuses. Maker, then Checker (L13 not done) **2026-10-05:** no change 2026-10-05. | no (no stock moves unless approved) |
| Q16 | Quantity above ATP blocked / warned / accepted (OB1) | OPEN (known: pick without stock row gives "Stock not available."; ATP shown 4/0/0). Order Booking: line qty = ATP, ATP + 1. Maker **2026-10-05:** no change 2026-10-05 (ATP again = Closing, 325 -> 290 by 7 per order). | yes (stock for the day) |
| Q18 | Mandatory fields of Order Booking (OB3) | PARTLY. Header: progressive disclosure, no messages, no Validation button until the detail step. Remaining: messages of the detail step (Validation / Save with a missing quantity). Maker **2026-10-05:** no change 2026-10-05. | yes (needs stock to reach the detail step) |
| Q26 | Why Unallocate answers "stock not found." (SA1, DL4) | OPEN. Allocation > Unallocate on a same-day order after stock exists **2026-10-05: PARTLY:** not reproduced on 10-01 or 10-05 ("Process completed successfully" both days); cause [inferred] stale-day data; close if a third run agrees. | yes |
| Q27 | Allocation on short stock (SA3) | OPEN. book an order above stock, read Allocation Status **2026-10-05:** no change 2026-10-05. | yes |
| Q-OE4 (new 2026-10-05) | Exact Order Editing date filter: only delivery date = working date, or a range capped at today? (page order_editing_cancellation.md) | OPEN. Default: only delivery date = today is listed. Check: an order with delivery date tomorrow with Date To = tomorrow. Maker | no (needs orders) |
| Q29 | Past delivery date refused (DD2) | OPEN. Delivery Date Change with a past date, check message **2026-10-05:** no change 2026-10-05. | no (needs orders) |
| Q30 | Date change also moves the delivery PJP (DD3) | PARTLY. Baseline: Transaction Inquiry has no Delivery-PJP column; read the Delivery Man PJP on the GIN header after the change **2026-10-05:** PJP Delivery No stayed 02112 on the 10-01 and 10-05 moves; a move to another route date not tried. | no (needs orders) |
| Q34 | Date used by GIN approval stock check (GIN2) | OPEN (known: refused for stock received the day before). GIN approval with Delivery Date today vs future **2026-10-05:** GIN Date = Delivery Date = stock date again on 10-05 (GIN 507), still not separable. | yes |
| Q42 | Stock reversal at approval or at GRN for a return (SR3) | OPEN. Stock Inquiry snapshots around return approval, Picked, GRN **2026-10-05: PARTLY:** returned quantity came back via the GRN on both days; no snapshot between approval and GRN. | yes |
| Q-SR1 | When does an approved and picked sales return reduce the cash memo receivable (credit note? Route Settlement?) | OPEN, strengthened 2026-10-05: even after the route was settled (Complete) Adjusted Credit Note 0, Fresh Return 0, 2009 Balance 88,107 excludes the 29,077 return | yes |
| Q-GRN1 | When Actual < Suggested on a GRN, where does the difference go? (page goods_return_note.md) | OPEN (only full returns on both days). Default: shortage charged to the delivery man at Route Settlement | yes |
| Q-GRN2 | Does a sales return booked as Damaged/Expired/Lost come back on the GRN with that stock type? | OPEN. Default: yes | yes |
| Q-LA2 | Why is Reject disabled for the Checker on a Pending loss record? | OPEN (Reject OFF again on 640). Default: losses cannot be rejected on this screen | no |
| Q48 | Payable vs Received (RS1) | OPEN. Route Settlement screens **2026-10-05: PARTLY:** Payable = Received per slip line before and after settlement; the settlement entry was done by a QA team member (not seen). | yes |
| Q-DS3 (new 2026-10-05) | Route 02112 for 2026-10-01 is Complete but its slips 1131-1136 are still Un Posted: how was 10-01 completed, and are its receivables left open? (page deposit_slips.md) | OPEN. Default: Complete does not guarantee posting; assert slip Status separately. Ask the QA lead how 10-01 was closed | no (read only) |
| Q-RS3 (new 2026-10-05) | What makes up Total Order 13 for 02112 on 2026-10-05 (10-01: 4)? (page route_settlement.md) | OPEN. Default: do not assert Total Order | no (read only) |
| Q-RS4 (new 2026-10-05) | Does the "previous days not closed" check look only at routes with activity, per PJP or per distributor? (page route_settlement.md) | OPEN. Default: per route with activity (4 zero-activity routes of 10-01 stayed Incomplete and did not block 02112) | next day |
| Q53 | DSR Adjustment auto-authorized (DJ2) | OPEN. save one adjustment, read status **2026-10-05:** seq 56 bypassed by the QA lead, nothing saved. | no |
| Q-DJ1 (new 2026-10-05) | What does a PJP's Total Shortage Amount accumulate (02112: 2,477,571.11 while route settlements show Cash Shortage 0)? (page dsr_adjustment.md) | OPEN. Default: historical shortages of all runs; never assert absolutely | no |
| Q58 | Stock reduces on forward or approval (OT2) | OPEN. SAN type Stock Adjustment Admin: Stock Inquiry snapshot after Forward and after approval **2026-10-05:** PARTLY: after approval Out +50 / Closing -50 (SAN 96); stock after the Maker's Forward alone not read. | yes |

## 4. Class A: default is fine (appendix): 15 questions

| Q | Question | Default we assume | Source |
|---|---|---|---|
| Q03 | How DA Against Purchase Order and Dispatch Advice Auto differ | out of scope; only type "Dispatch Advice" is tested | DA3 |
| Q09 | Rate and amounts in a GRN used financially | informational only | GRN4 |
| Q12 | Other Period Types than DAILY | only DAILY | SI3 |
| Q13 | DZ columns | always 0 (0 in all rows on 10-01 and 10-05) | SI4 |
| Q14 | Absolute values vs change from a snapshot in stock validations | change from a before/after snapshot | SV1 |
| Q15 | SAN stock validations (02850001, 02860001) in the cycle | no, inactive | SV3 |
| Q24 | Difference between document type 2 (PLACED) and CM-01 | 2 = tele-order demand, CM-01 = booked order | OL2 |
| Q25 | Meaning of Amendment 05 | unused, inactive | OL3 |
| Q47 | Can a slip mix cash and cheque | no, one Type per slip | DS4 |
| Q54 | Maximum limit of the adjustment amount | none | DJ3 |
| Q56 | Does marking a PJP complete (day close) block collection | yes | PJ2 |
| Q60 | Rounding rule of tax/charges | Net rounded to whole PKR, Gross/Discount/Tax 2 decimals, line sums within 1 paisa (observed again 10-05) | EO1 |
| Q61 | Is the closing stock check restricted to SAN products | filtered by the SAN product | EO2 |
| Q-DA2 | What are "Dispatch Advice NUP" and "Dispatch Advice II", in scope? (page dispatch_advice.md) | out of scope; only "Dispatch Advice" is tested | G11-1 |
| Q-LA3 | Is the duplicate "Lost" entry in the loss Stock list two stock types? (page da_loss_approval.md) | master-data duplicate; use the first | G11-1 |

(Q49 moved to section 2b: answered 2026-10-05.)

## 5. Contradictions between sources

Status column updated 2026-10-05. RESOLVED rows keep the old sources for the record.

| # | Topic | Source A says | Source B says | Pages | Status |
|---|---|---|---|---|---|
| 1 | Is Allocated inside Closing? | Closing = Opening + In - Out - Allocated (80+80-0-63 = 97 CS) [observed] | Closing = Opening + In - Out; ATP = Closing - Allocated [inferred] | stock_inquiry_and_balances.md vs end_of_day_validations.md | **RESOLVED**: Source A holds on 39 of 39 rows of 2026-09-30 in base PC units (two rows differ per column only by PC-to-CS carry: 20050308 Auto Main, 20061858 IBT). Assert Closing = Opening + In - Out - Allocated in base PC; Closing is available stock (= ATP). end_of_day_validations.md corrected |
| 2 | Maker must differ from checker | "Maker and checker must differ [observed]" (GIN switch point; SAN, Sales Return, GRN) | App did not stop KPO_mp approving own DA 570 | goods_issue_note.md, dispatch_advice.md | **RESOLVED as a convention**: GIN workflow of org 010104 is StockUpdateGIN v53, Verify then Approve both role 0005, so separation of duty is NOT declared; "must differ" is a QA convention (tag changed from observed). Whether the BA wants it enforced stays BA2 |
| 3 | Status vocabulary: Confirmed vs Ordered | UI shows "Confirmed" after booking | DB doc status 04 "Ordered"; execution chain "01 Ordered -> 02 Confirmed" | transaction_inquiry.md, order_lifecycle_and_statuses.md, delivery_lifecycle.md | **RESOLVED**: "Confirmed" is execution status 02 (own status), "Planning completed" is 03, "Ordered" is document 04 and execution 01; Transaction Inquiry's Document Status column shows the execution text (orders on GIN 505 read Planning completed) |
| 4 | Status vocabularies per document | Workflow Draft/Pending/Approved; DA grid In-Active/Active; DA header Un-Authorized | doc status Authorized/Un-Authorized/Cancelled/Picked; letters I/A, P/L/R/B/C/A for slips and cheques | document_lifecycle.md sec 3 | OPEN (explained: several status columns per document; assert one column and name it). DA 1356 confirms: grid Active, Approval Status Approved, header Un-Authorized before approval 2026-10-05 adds: slip "Un Posted / Posted", cheque "Clear", Cashmemo Status grid "Ordered" vs Transaction Inquiry "Ready to dispatch/Packed". |
| 5 | Cancelled | document status 03 Cancelled | execution status 05 Cancelled | order_lifecycle_and_statuses.md, delivery_lifecycle.md | **RESOLVED**: both exist, they are two columns (document 03, execution 05), Transaction Inquiry shows the execution one |
| 6 | Document type codes | DA-01 "Dispatch Advice", also DA and DA-05 "Auto"; GR-01 and GR | CM "Cash Memo" parent vs CM-01 "Sales"; type `2` "Demand Captured from Tele order"; AD-07 active vs AD-04/06 inactive; CM-06 B2B use unknown | dispatch_advice.md, goods_return_note.md, order_lifecycle_and_statuses.md, dsr_adjustment.md | OPEN (live: Transaction Inquiry Document Type has 17 options incl. Sales, Sales Return, B2B Sale) |
| 7 | Org 0101 vs 010104 data | statuses, document types and counts come from org 0101 | live app is org 010104 (overlay); the snd-schema connector is database ng_astrone (newest cash memo 2026-01-30, no COL26000001979-2002) | goods_issue_note.md sec 13, deposit_slips.md, route_settlement.md, order planning README | OPEN (master data is usable as db-declared evidence; live transactions cannot be cross-checked in it) |
| 8 | Framework filters vs live | Framework Transaction Inquiry reads Document Type per workbook and filters Document No "COL26000" / Outlet Code "Auto"; framework DA validation expects In CS = DA quantity, Out CS = 0 with workbook date 2026-09-21 | Live default Document Type is "Demand Captured from Tele order" (hides orders) and grids show 15-39 rows of mixed days; absolute In/Out failed on a busy day | transaction_inquiry.md sec 8, stock_validation_flows.md sec 8 | OPEN. Note: SO Number is optional and NOT unique (live), so it cannot serve as a unique DA filter key; use the Document No 2026-10-05: full list of drift items in FRAMEWORK_DRIFT.md. |
| 9 | Delivery date of an order | Delivery Date 2026-10-05 copied from the PJP next visit [inferred] | GIN needs Delivery Date typed; draft question suggests today | order_booking.md vs delivery_date_change.md | PARTLY: orders on GIN 505 carry 2026-09-30 after Delivery Date Change, cancelled orders still 10-05; the booking rule stays BA4 2026-10-05: third data point (10-05 booking -> 10-11); Delivery Date Change needed again; rule stays BA4. |
| 10 | Screens in the framework but not in the live menu | Flows for "OTC Stock Out", "Opening/Closing Stock", "Dispatch Advice Approval" | live harvest found no such menu entries; DSR Adjustment is a top-level 201065 | screen_harvest_log.md vs otc_stock_out_and_san.md, dsr_adjustment.md | PARTLY RESOLVED: sidebar search "OTC" finds nothing (live 2026-10-01); the stock-out maps to Stock Adjustment SAN, type Stock Adjustment Admin (candidate) 2026-10-05: OTC Stock Out walked as Stock Adjustment SAN / Stock Adjustment Admin (SAN 96); DSR Adjustment Amount found by menu search "Adjustment". |
| 11 | What feeds the GRN | GRN suggested quantity comes from the GIN (Delivery Man PJP) | Sales return page says Picked CM-02 returns are handed to the GRN | goods_return_note.md vs sales_return.md | OPEN (BA7) **RESOLVED 2026-10-05** (G11-1 + G11-2): both; the GRN brings back the undelivered quantities of the DSR's GIN and the picked returns (19 CS on both days). |
| 12 | Order of Cashmemo Status vs sales return | delivery_lifecycle puts Status (seq 33, Delivered) before Sales Return (34-38) | Cashmemo Status GIN Number list was empty for DM PJPs on 2026-10-01; whether a return needs Delivered status is open (Q40) | delivery_lifecycle.md, screen_harvest_log.md | OPEN **RESOLVED 2026-10-05**: Sales Return lists only delivered (Cashmemo Status saved) memos on both days, so Status comes first. |
| 13 | Stock Inquiry screens | Stock Inquiry layout 201069 (seq 9, 24, 50) | seq 60 reads "Stock Inquiry II" DYL_BG1015 | stock_inquiry_and_balances.md vs end_of_day_validations.md | OPEN (Auto_Tssm has no Stock Inquiry; he has Stock Master Inquiry) 2026-10-05: PARTLY: both screens exist in the menu; seq 60 was read on Stock Inquiry (Stock Inquiry II not opened). |
| 14 | When does the DA loss record exist | "created when the DA is forwarded" (da_loss_approval.md, default of DAL2) | no record after the maker's Forward, Serial 638 after the checker's approval (live) | da_loss_approval.md, dispatch_advice.md | **RESOLVED 2026-10-01**: created at the DA approval; pages corrected |
| 15 | Is a start-of-day step needed (BA1) | "a new day has no rows until Generate Opening Balances"; GIN approval refused for earlier-day stock | the DA approval creates the day's row for the received product without the button (Opening 0, In 4, Closing 4) | stock_inquiry_and_balances.md, goods_issue_note.md | **RESOLVED for received products**; the remaining question (carry of previous closings, products not received that day) is BA14 |
| 16 | GIN workflow name | `StockUpdateGIN4Level` (goods_issue_note.md, glossary) | org 010104 uses `StockUpdateGIN` v53 (4Level only for parent orgs 0101/0102) | goods_issue_note.md | **RESOLVED 2026-10-01**: pages corrected |
| 17 | Execution status 19 "CM Reschedule" | listed in the delivery pages (from org 0101, Jan 2026 data) | glb_pr_exs_execution_status of org 010104 has no codes 04, 06, 19 | cashmemo_reschedule_and_status.md, delivery_lifecycle.md | OPEN: re-read the reschedule status live after a reschedule 2026-10-05: PARTLY: screens show "Reattempt" after a reschedule on both days; the code behind it not read. |
| 18 (new) | Are previous closings carried into a new day? | 10-01 morning: DA approval created ONE row with Opening 0 ("not carried") [observed 2026-10-01] | 10-05: first movement created all 39 rows with Opening = previous Closing + still-Allocated [observed 2026-10-05] | stock_inquiry_and_balances.md, dispatch_advice.md | **RESOLVED for the cycle in favour of B** (the 10-01 row itself was rewritten to 160 later that day); the anomaly is Q-OB2 |
| 19 (new) | Return discount reversal | "reversed proportionally" [observed 2026-10-01] | non-returned lines also carry reversals (slab re-pricing) [observed 2026-10-05] | sales_return.md | **RESOLVED** (refined to B); intent Q-SR2 |
| 20 (new) | Cheque statuses | db P/L/R/B/C/A; framework/QA lead "Realized" | screen "Clear", only action Bounce | cheque_status.md | OPEN (Q-CS1, BA11) |
| 21 (new) | Does "Complete" mean posted? | 10-05: route Complete and slips Posted | 10-01: route Complete, slips still Un Posted | route_settlement.md, deposit_slips.md | OPEN (Q-DS3) |
| 22 (new) | Order Editing date filter | G11-1: "Date To must cover the delivery date" | G11-2: a range covering the future delivery date lists nothing; only delivery date = today | order_editing_cancellation.md | **RESOLVED** in favour of B (G11-1 hypothesis superseded); exact rule Q-OE4 |
| 23 (new) | Deposit Slip Add | G11-1: Add gives a blank form (no PJP-DSR) | G11-2: Add brought PJP-DSR back to 02111 | deposit_slips.md | OPEN (minor; always set PJP-DSR) |
| 24 (new) | Why the workbook return values differ | G11-1: because the source order was edited | G11-2b: the workbook was built 2026-09-21 for outlet 1000000003 (stale) | sales_return.md | **RESOLVED** in favour of B (framework drift) |

## 6. Counts

- Questions as written in the 26 pages: **73**; unique after merging duplicates: **60** (see the 2026-10-01 version: DAL3 into Q01, GRN3 into Q07, SV2 into Q10, DD1 into Q17, SA2 into Q19, CR3 into Q20, TI1 into Q23, DL4 into Q26, GIN1 into Q31, CR1 into Q32, SR5 into Q40, CS2 into Q51, CR4 into Q22).
- After the 2026-10-01 live walk: answered 10 (section 2a); open 52 = A 14 + B 25 + C 13; G11-1 then added 18 page questions (A 2: Q-DA2, Q-LA3; B 7: Q-SR1, Q-DS1, Q-OB1, Q-RS2, Q-GRN1, Q-GRN2, Q-LA2; C 9: Q-OE1, Q-OE2, Q-OE3, Q-DA1, Q-RS1, Q-DS2, Q-DA3, Q-LA1, Q-SV1).
- **Before this consolidation: 70 open = A 16 + B 32 + C 22.**
- Closed 2026-10-05 (section 2b): A 1 (Q49); B 16 (Q-OB1, Q-DS1 with Q45, Q-RS2, Q50, Q55, Q33, Q41, Q43, Q31, Q08, Q21, Q22, Q32, Q46, N1 = 15 ids + Q45 = 16); C 4 answered (BA5, BA6, BA7, BA9) + 2 merged (BA3 into Q-LA1, Q-DA1 into BA2).
  - Of these, closed by the new G11-2/2b evidence: Q-OB1, Q-DS1, Q45, Q-RS2, Q50, Q55, Q33, Q41, Q43, Q49 (10). Closed by G11-1 evidence now recorded: Q31, Q08, Q21, Q22, Q32, Q46, N1, BA5, BA6, BA7, BA9 (11).
  - PARTLY answered and still open: Q-RS1, BA14, Q26, Q30, Q42, Q48, Q58.
- New 2026-10-05: B 6 (Q-OB2, Q-OE4, Q-DS3, Q-RS3, Q-RS4, Q-DJ1); C 3 (Q-TI1, Q-SR2, Q-CS1).
- **Open now: 56 = A 15 (16 - 1) + B 22 (32 - 16 + 6) + C 19 (22 - 4 - 2 + 3).** BA list (1a) 15 = the hard maximum; QA lead / framework owner list (1b) 4.
- Contradictions: 24 listed; 13 resolved (1, 2, 3, 5, 11, 12, 14, 15, 16, 18, 19, 22, 24), 4 partly (9, 10, 13, 17), 7 open (4, 6, 7, 8, 20, 21, 23).

## 7. Source code legend
DA = dispatch_advice, DAL = da_loss_approval, GRN = goods_return_note, SI = stock_inquiry_and_balances, SV = stock_validation_flows, OB = order_booking, OE = order_editing_cancellation, OL = order_lifecycle_and_statuses, SA = stock_allocation, TI = transaction_inquiry, DD = delivery_date_change, DL = delivery_lifecycle, GIN = goods_issue_note, CR = cashmemo_reschedule_and_status, SR = sales_return, DS = deposit_slips, RS = route_settlement, CS = cheque_status, DJ = dsr_adjustment, PJ = pjp_daily_inquiry_update, OT = otc_stock_out_and_san, EO = end_of_day_validations. Number = position in section 12 of that page. Session ids (Q-xx#) use the same page codes, except Q-OB1/Q-OB2 = opening balances and Q-LA = loss approval.
