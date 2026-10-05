# Open questions: consolidated and classified (S&D / DCODE business knowledge)

Updated: 2026-10-01 (live blocks 1-3b)

Consolidated 2026-10-01 from section 12 of the 26 area pages (73 questions as written, 60 unique after merging 13 duplicates; the Q numbers have gaps because merged questions keep the lowest id). Source ids: page code + number, e.g. DA2 = Dispatch Advice question 2 (codes at the end of this file). Live evidence: [LIVE_FINDINGS.md](LIVE_FINDINGS.md) blocks 1, 2a, 3a, 3b (2026-10-01).

Classes: **A** default is fine (no BA time; see appendix), **B** verify live (see [LIVE_LEARNING_CHECKLIST.md](LIVE_LEARNING_CHECKLIST.md)), **C** BA decision.

**Status after the live walk (2026-10-01): 10 of the 60 questions are ANSWERED (Q04, Q06, Q10 = BA1, Q11, Q23, Q28, Q35, Q36, Q37, Q57); 4 more are PARTLY answered (Q18, Q22, Q30, Q55) and stay open in a narrowed form; 2 new items came out of the walk (N1, BA14). Open now: 52 = A 14 + B 25 + C 13.**

## 1. BA decision list (class C): 13 questions open

Order follows the Daily Cycle. Each has default, why it matters, evidence. BA1 was ANSWERED by evidence (section 2); the other numbers are kept so references do not break.

**BA2. Must the app prevent the maker from approving his own document (DA, DA loss, GIN, GRN, SAN, Sales Return), or is "maker and checker differ" only a QA convention?** [Q01]
- Default: it is a QA rule; self-approval cases are reported as a deviation note, not a defect.
- Why: decides whether the negative case "same user approves" expects a block or a pass.
- Evidence: KPO_mp approved its own DA 570 [observed]; the GIN workflow of org 010104 (StockUpdateGIN v53) declares Verify and Approve for the SAME role 0005 [db 2026-10-01], so the workflow does not separate the people; the Checker's buttons (Forward/Reject/Terminate) are enabled only on Pending documents [observed]. Whether the BA wants it enforced is the open point.

**BA3. Where do approved DA losses (Damaged / Lost / Expired) appear as stock or claims?** [Q05]
- Default: not visible in Stock Inquiry the same day.
- Why: the stock check after a loss DA cannot assert Damaged/Lost rows; defines the expected outcome of the loss case.
- Evidence: after loss approval Stock Inquiry showed only Sound rows (da_loss_approval.md); live 2026-10-01: the loss record (Serial 638) is created at the DA approval and stays Pending; no 02 - Damaged row for 62740537 exists on 10-01 or 09-30; the loss approval itself was not run yet (checklist L21). A claim loss log table exists, link inferred.

**BA4. Which delivery date should a booked order carry before the GIN: the PJP's next visit date (2026-10-05 observed) or today, and are past dates refused?** [Q17]
- Default: orders carry the PJP's next visit date; Delivery Date Change moves them to today before the GIN.
- Why: the GIN needs a typed Delivery Date and eligible cash memos; wrong date gives an empty Cash Memo Selection.
- Evidence: order_booking.md, delivery_date_change.md (draft question 3); live 2026-10-01: the 8 orders on GIN 505 carry 2026-09-30 (moved), cancelled orders 1986/1993 still carry 2026-10-05.

**BA5. How is an allocated order meant to reach Order Editing / Order Cancellation (unallocate first, delivery-date range, or never)?** [Q19]
- Default: unallocate first (when it works) and use a date range covering the delivery date.
- Why: on cnr1dev1 orders are auto-allocated at save, the outlet list is empty and Unallocate fails, so edit/cancel cases cannot start.
- Evidence: outlet API returned [] (order_editing_cancellation.md, stock_allocation.md); live 2026-10-01: Order Editing / Cancellation / Reschedule grids returned 0 rows for the orders on GIN 505.

**BA6. Are Order Editing and Order Cancellation allowed after the GIN is approved, and what happens to the GIN and stock?** [Q20]
- Default: refused with a message once the GIN is approved.
- Why: defines expected result of the "After GIN" flows (seq 29, 31), whose assertions have no text.
- Evidence: only toast-without-text assertions in the atlas (order_editing_cancellation.md, cashmemo_reschedule_and_status.md).

**BA7. What business situation creates a Goods Return Note (undelivered goods from the DSR, returned sales returns, or both), and can one exist without a GIN?** [Q07]
- Default: undelivered goods returned by the delivery man; not possible without a GIN.
- Why: decides preconditions and the link with Picked sales returns.
- Evidence: shared GIN/GRN tables with suggested quantities; sales return page hands Picked returns to the GRN (goods_return_note.md, sales_return.md).

**BA8. Is a sales return limited to the quantity ordered or the quantity delivered, and may it be made before the cash memo is delivered?** [Q40]
- Default: limited to delivered quantity; only after delivery.
- Why: boundary values of the return quantity and the order of the chain.
- Evidence: message says "ordered quantity" (sales_return.md).

**BA9. When a cash memo is rescheduled, what happens to its quantities on the GIN and to the stock (leave the GIN, return through a GRN)?** [Q38]
- Default: it leaves the GIN and the stock returns via a Goods Return Note.
- Why: stock arithmetic after reschedule; cannot be derived from the UI.
- Evidence: only execution statuses 19, 24, 25 (cashmemo_reschedule_and_status.md); live 2026-10-01: status 19 is absent from the 010104 execution master (see contradiction 17).

**BA10. Does a Deposit Slip need checker approval?** [Q44]
- Default: no, single maker step.
- Why: the approval row 00140002 is inactive; defines whether an approval case exists.
- Evidence: deposit_slips.md.

**BA11. What does a bounced cheque do to the outlet receivable, and which cheque status transitions are allowed?** [Q51]
- Default: the invoice becomes outstanding again; only P/L to R or B.
- Why: negative and transition cases of Cheque Status.
- Evidence: cheque_status.md (no rows, no flow beyond selection).

**BA12. What is the effect of a DSR Adjustment (sign, debit/credit, link to cash shortage) in Route Settlement?** [Q52]
- Default: the sign decides debit or credit and it changes the cash shortage.
- Why: its assertion is toast plus detail amount only; the finance effect cannot be tested without the rule.
- Evidence: dsr_adjustment.md.

**BA13. Does a stock write-off through a SAN produce a financial posting (value, moving average price) in addition to the stock change?** [Q59]
- Default: stock value only, no other posting.
- Why: end-of-day finance checks.
- Evidence: otc_stock_out_and_san.md.

**BA14 (new 2026-10-01). Is Generate Opening Balances still part of the day (does it carry the previous day's closing for products that are not received that day), who runs it, and is carrying the previous day's stock meant to be automatic?** [new, follows from Q10]
- Default: not part of the QA cycle; the cycle starts with a DA of the day (the DA approval creates the row of a received product); stock received on an earlier day is not usable the next day without it, and the cycle never relies on earlier stock.
- Why: 62740537 closed 97 CS on 2026-09-30 but opened 0 on 2026-10-01 after the DA approval, and GIN 505 approval on 09-30 was refused for stock received 09-29: previous closings are not carried automatically. Any case that issues stock not received that day depends on the answer.
- Evidence: Stock Inquiry 09-30 vs 10-01 (LIVE_FINDINGS L01, S1, S2); button never clicked (not authorised).

## 2. ANSWERED by the live walk (2026-10-01): 10 questions

Each answer carries the new default or rule. Evidence ids refer to LIVE_FINDINGS.md.

| Q | Question | ANSWER (new default / rule) | Evidence |
|---|---|---|---|
| Q04 | Duplicate SO Number blocks save (DA4) | NO. Duplicates are allowed (DA 1353 and 1354 both saved with LEARN_SO_01, "Saved successfully") and SO Number is optional (DA 1355 saved empty). Rule: no uniqueness check on Save; do not write a negative case for it. | L11 [observed] |
| Q06 | Loss record created at DA Forward or approval (DAL2) | AT THE DA APPROVAL. After the maker's Forward the Loss Approval filter Document No 1356 gave 0 rows; after Auto_Tssm approved the DA it gave Serial 638, Pending for approval. A Draft's Forward belongs to the Maker; the loss record is a side effect of the checker's approval. Loss Approval is visible to the Maker. | L12, C2, S4 [observed] |
| Q10 (BA1) | Is a start-of-day step needed before receiving and issuing? | NO for a received product: the DA approval creates the day's stock row (Opening 0, In = received 4 CS, Closing 4 CS) without Generate Opening Balances; In posts to the Received Date. Rule: the cycle starts with the DA; no start-of-day step. Caveat kept as BA14: Generate Opening Balances may still serve products not received that day and carry previous closings (unknown). | L02, C1, S1, S2 [observed] |
| Q11 | Is Allocated deducted from Closing (SI2) | YES. Closing = Opening + In - Out - Allocated holds on 39 of 39 rows of 2026-09-30 in base PC units; two rows fail literally only because of PC-to-CS carry (20050308 Auto Main, 32 PC per CS; 20061858 IBT, 12 PC per CS). Rule: assert the identity in base PC with the pack factor from the product name; Closing is available stock (ATP). | L01 [observed] |
| Q23 | "Confirmed" vs Ordered 04 (OL1, TI1) | "Confirmed" is its OWN execution status 02 (identifier ALC); "Planning completed" is execution 03 (identifier GIN, follows 02); Ordered is document status 04 and execution status 01. The Transaction Inquiry column Document Status shows the execution status text: the 8 orders on GIN 505 read "Planning completed". Rule: assert the Document Status column text, expect Confirmed after booking and Planning completed once on a GIN. | L03, L04 [observed + db] |
| Q28 | Total Offering Discount equals header Discount (TI2) | YES. Sum of the five offering lines equals the header Discount on all 8 orders (-29,971.82 vs -29,971.83 = 1 paisa rounding for 1995-2001; -16,264.08 exactly for 2002); tax is 0 on every promo line; Net is rounded to whole PKR. Rule: allow 0.01 tolerance. | L03 [observed] |
| Q35 | GIN approval levels (GIN3) | TWO steps in org 010104: workflow StockUpdateGIN v53, user tasks Verify then Approve, both candidate group 0005 (Distributor Role, not an authorizer role). Four levels (StockUpdateGIN4Level v3: 0005, 0008, 0005, 0008) exist only for the parent orgs 0101/0102. Separation of duty is NOT declared. Rule: expect the checker flow to be Forward on a Pending GIN; whether Verify then Approve needs two Forward clicks is not observed (GIN 505 approval never completed). | L05 [db] |
| Q36 | Add/remove cash memo on an approved GIN (GIN4) | De-linking is ENABLED for the Maker on a Draft GIN (29) and DISABLED on a Pending GIN (505); approved GINs are not listed on the screen. Rule: cash memos are removed only while the GIN is Draft; for an approved GIN only the adhoc add/remove statuses 24/25 exist. | L10, C3 [observed] |
| Q37 | Who may cancel a GIN (GIN5) | Only the Checker, and only on a Pending GIN: Auto_Tssm has Forward, Reject, Terminate enabled on Pending 505 and all disabled on Draft 29; the Maker has Reject and Terminate disabled on both. Rule: the Maker cannot cancel; Terminate effect on stock/cash memos still unknown (default: cash memos return to the selection pool). | L10, C3 [observed] |
| Q57 | Which SAN Type is "OTC Stock Out" (OT1) | NONE is labelled so and the sidebar search "OTC" finds nothing. SAN Type options: Warehouse To Warehouse Transfer, Stock Adjustment Entry, Stock Adjustment Admin, Physical Stock Reconciliation, Stock Adjustment From Transfer (Auto). Default updated to Stock Adjustment Admin (SA-03, single warehouse; all recent grid rows are of that type, no To Warehouse) [inferred mapping]; Q58 (stock direction at Forward vs approval) stays B. | L08 [observed + inferred] |

PARTLY answered (stay open in section 3): Q18 (Order Booking has no header messages and no Validation button before the detail step: fields work by progressive disclosure, detail-step messages unread), Q22 (reason lists db-declared, dropdowns not opened because no order was eligible), Q30 (Transaction Inquiry has no Delivery-PJP column; delivery PJP is visible on the GIN; the date change was not re-run), Q55 (Mark Status = E End of Day; DSR Files Status = P process / C complete, db-declared; labels still to read in Edit mode). Also new evidence on Q31 (DA approval stock effect now known) and Q16/Q27 (product pick answers "Stock not available." when the product has no stock row for the day; ATP 4 CS = Closing; quantity above ATP not tried).

## 3. Class B: verify live (25 open: 24 original + 1 new)

Each is run in [LIVE_LEARNING_CHECKLIST.md](LIVE_LEARNING_CHECKLIST.md) (step ids L01-L33, each citing its Q numbers). Ordered by Daily Cycle; "needs same day" means a same-day receive-and-issue cycle. Status: OPEN, or PARTLY with what is already known.

| Q | Question (merged ids) | Status / live check, area/step, user | Needs same day cycle |
|---|---|---|---|
| Q02 | DA Reject / Terminate / Delete of a Draft (DA2) | OPEN. Inbound > DA: create Draft DA, Delete; second DA forward then Reject; record statuses. Maker, then Checker (L13 not done) | no (no stock moves unless approved) |
| Q08 | Stock type and day credited by approved GRN (GRN2) | OPEN. GRN approval then Stock Inquiry rows by stock type. Maker/Checker/Stock Controller | yes |
| Q16 | Quantity above ATP blocked / warned / accepted (OB1) | OPEN (known: pick without stock row gives "Stock not available."; ATP shown 4/0/0). Order Booking: line qty = ATP, ATP + 1. Maker | yes (stock for the day) |
| Q18 | Mandatory fields of Order Booking (OB3) | PARTLY. Header: progressive disclosure, no messages, no Validation button until the detail step. Remaining: messages of the detail step (Validation / Save with a missing quantity). Maker | yes (needs stock to reach the detail step) |
| Q21 | Edit keeps the same Order Number (OE3) | OPEN. Order Editing after reaching an editable order. Maker | yes |
| Q22 | Reason lists for edit, cancel, reschedule (OE4, CR4) | PARTLY. Lists db-declared (CNL list for cancel/reschedule, ORC list for edit); real dropdowns not opened (no eligible order on 2026-10-01). Remaining: open the three dropdowns on a new order | yes (needs an order in Ordered/Confirmed) |
| Q26 | Why Unallocate answers "stock not found." (SA1, DL4) | OPEN. Allocation > Unallocate on a same-day order after stock exists | yes |
| Q27 | Allocation on short stock (SA3) | OPEN. book an order above stock, read Allocation Status | yes |
| Q29 | Past delivery date refused (DD2) | OPEN. Delivery Date Change with a past date, check message | no (needs orders) |
| Q30 | Date change also moves the delivery PJP (DD3) | PARTLY. Baseline: Transaction Inquiry has no Delivery-PJP column; read the Delivery Man PJP on the GIN header after the change | no (needs orders) |
| Q31 | Stock effect of allocation, GIN approval, GRN, sales return (DL1, GIN1) | PARTLY. DA approval effect known (In = received, Allocated 0, row created); allocation shows in Allocated and is subtracted from Closing. Remaining: GIN approval, GRN, sales return snapshots | yes |
| Q32 | Cashmemo Status meaning (CR1, DL2) | OPEN. open Cashmemo Status grid for a PJP with a GIN | yes |
| Q33 | Partial Delivered (18) after a return (DL3) | OPEN. DB/UI status of a partly returned cash memo | yes |
| Q34 | Date used by GIN approval stock check (GIN2) | OPEN (known: refused for stock received the day before). GIN approval with Delivery Date today vs future | yes |
| Q41 | What Status Change (Picked) does (SR2) | OPEN. Sales Return Status Change on an authorised return | yes |
| Q42 | Stock reversal at approval or at GRN for a return (SR3) | OPEN. Stock Inquiry snapshots around return approval, Picked, GRN | yes |
| Q43 | Discounts reversed proportionally (SR4) | OPEN. return one line with a discount, read Discount | yes |
| Q45 | What flips slip status I to A (DS2) | OPEN. Deposit Slip: full-amount save, read status | yes (needs delivered cash memo) |
| Q46 | Meaning of Unposted Amount (DS3) | OPEN. Unposted variant | yes |
| Q48 | Payable vs Received (RS1) | OPEN. Route Settlement screens | yes |
| Q50 | How Offset Amount is derived (RS3) | OPEN (baseline: Offset 0 on all 8 orders before delivery). Transaction Inquiry after settlement | yes |
| Q53 | DSR Adjustment auto-authorized (DJ2) | OPEN. save one adjustment, read status | no |
| Q55 | Allowed Mark Status / DSR Files Status values (PJ1) | PARTLY. Db-declared: Mark Status E End of Day; DSR Files Status P process, C complete. Remaining: read the dropdowns in Edit mode on a throwaway | no |
| Q58 | Stock reduces on forward or approval (OT2) | OPEN. SAN type Stock Adjustment Admin: Stock Inquiry snapshot after Forward and after approval | yes |
| N1 (new) | Why GIN Detail shows Current Stock 0-0-0 for every line although Stock Inquiry has stock; which stock the GIN approval check reads | OPEN. Compare GIN Detail Current Stock before and after allocation on a same-day GIN (GIN 505 and Draft 29 both show 0-0-0). Maker | yes |

## 4. Class A: default is fine (appendix): 14 questions

| Q | Question | Default we assume | Source |
|---|---|---|---|
| Q03 | How DA Against Purchase Order and Dispatch Advice Auto differ | out of scope; only type "Dispatch Advice" is tested | DA3 |
| Q09 | Rate and amounts in a GRN used financially | informational only | GRN4 |
| Q12 | Other Period Types than DAILY | only DAILY | SI3 |
| Q13 | DZ columns | always 0 (live 2026-10-01: 0 in all 39 rows) | SI4 |
| Q14 | Absolute values vs change from a snapshot in stock validations | change from a before/after snapshot | SV1 |
| Q15 | SAN stock validations (02850001, 02860001) in the cycle | no, inactive | SV3 |
| Q24 | Difference between document type 2 (PLACED) and CM-01 | 2 = tele-order demand, CM-01 = booked order | OL2 |
| Q25 | Meaning of Amendment 05 | unused, inactive | OL3 |
| Q47 | Can a slip mix cash and cheque | no, one Type per slip | DS4 |
| Q49 | Can a settled PJP/date be reopened | no | RS2 |
| Q54 | Maximum limit of the adjustment amount | none | DJ3 |
| Q56 | Does marking a PJP complete block collection | yes | PJ2 |
| Q60 | Rounding rule of tax/charges | document-type rounding (pdot_rounding_decimal); live: Net rounded to whole PKR, Gross/Discount/Tax keep 2 decimals | EO1 |
| Q61 | Is the closing stock check restricted to SAN products | filtered by Category/Brand of the SAN product | EO2 |

## 5. Contradictions between sources

Status column updated 2026-10-01 after the live walk. RESOLVED rows keep the old sources for the record.

| # | Topic | Source A says | Source B says | Pages | Status |
|---|---|---|---|---|---|
| 1 | Is Allocated inside Closing? | Closing = Opening + In - Out - Allocated (80+80-0-63 = 97 CS) [observed] | Closing = Opening + In - Out; ATP = Closing - Allocated [inferred] | stock_inquiry_and_balances.md vs end_of_day_validations.md | **RESOLVED**: Source A holds on 39 of 39 rows of 2026-09-30 in base PC units (two rows differ per column only by PC-to-CS carry: 20050308 Auto Main, 20061858 IBT). Assert Closing = Opening + In - Out - Allocated in base PC; Closing is available stock (= ATP). end_of_day_validations.md corrected |
| 2 | Maker must differ from checker | "Maker and checker must differ [observed]" (GIN switch point; SAN, Sales Return, GRN) | App did not stop KPO_mp approving own DA 570 | goods_issue_note.md, dispatch_advice.md | **RESOLVED as a convention**: GIN workflow of org 010104 is StockUpdateGIN v53, Verify then Approve both role 0005, so separation of duty is NOT declared; "must differ" is a QA convention (tag changed from observed). Whether the BA wants it enforced stays BA2 |
| 3 | Status vocabulary: Confirmed vs Ordered | UI shows "Confirmed" after booking | DB doc status 04 "Ordered"; execution chain "01 Ordered -> 02 Confirmed" | transaction_inquiry.md, order_lifecycle_and_statuses.md, delivery_lifecycle.md | **RESOLVED**: "Confirmed" is execution status 02 (own status), "Planning completed" is 03, "Ordered" is document 04 and execution 01; Transaction Inquiry's Document Status column shows the execution text (orders on GIN 505 read Planning completed) |
| 4 | Status vocabularies per document | Workflow Draft/Pending/Approved; DA grid In-Active/Active; DA header Un-Authorized | doc status Authorized/Un-Authorized/Cancelled/Picked; letters I/A, P/L/R/B/C/A for slips and cheques | document_lifecycle.md sec 3 | OPEN (explained: several status columns per document; assert one column and name it). DA 1356 confirms: grid Active, Approval Status Approved, header Un-Authorized before approval |
| 5 | Cancelled | document status 03 Cancelled | execution status 05 Cancelled | order_lifecycle_and_statuses.md, delivery_lifecycle.md | **RESOLVED**: both exist, they are two columns (document 03, execution 05), Transaction Inquiry shows the execution one |
| 6 | Document type codes | DA-01 "Dispatch Advice", also DA and DA-05 "Auto"; GR-01 and GR | CM "Cash Memo" parent vs CM-01 "Sales"; type `2` "Demand Captured from Tele order"; AD-07 active vs AD-04/06 inactive; CM-06 B2B use unknown | dispatch_advice.md, goods_return_note.md, order_lifecycle_and_statuses.md, dsr_adjustment.md | OPEN (live: Transaction Inquiry Document Type has 17 options incl. Sales, Sales Return, B2B Sale) |
| 7 | Org 0101 vs 010104 data | statuses, document types and counts come from org 0101 | live app is org 010104 (overlay); the snd-schema connector is database ng_astrone (newest cash memo 2026-01-30, no COL26000001979-2002) | goods_issue_note.md sec 13, deposit_slips.md, route_settlement.md, order planning README | OPEN (master data is usable as db-declared evidence; live transactions cannot be cross-checked in it) |
| 8 | Framework filters vs live | Framework Transaction Inquiry reads Document Type per workbook and filters Document No "COL26000" / Outlet Code "Auto"; framework DA validation expects In CS = DA quantity, Out CS = 0 with workbook date 2026-09-21 | Live default Document Type is "Demand Captured from Tele order" (hides orders) and grids show 15-39 rows of mixed days; absolute In/Out failed on a busy day | transaction_inquiry.md sec 8, stock_validation_flows.md sec 8 | OPEN. Note: SO Number is optional and NOT unique (live), so it cannot serve as a unique DA filter key; use the Document No |
| 9 | Delivery date of an order | Delivery Date 2026-10-05 copied from the PJP next visit [inferred] | GIN needs Delivery Date typed; draft question suggests today | order_booking.md vs delivery_date_change.md | PARTLY: orders on GIN 505 carry 2026-09-30 after Delivery Date Change, cancelled orders still 10-05; the booking rule stays BA4 |
| 10 | Screens in the framework but not in the live menu | Flows for "OTC Stock Out", "Opening/Closing Stock", "Dispatch Advice Approval" | live harvest found no such menu entries; DSR Adjustment is a top-level 201065 | screen_harvest_log.md vs otc_stock_out_and_san.md, dsr_adjustment.md | PARTLY RESOLVED: sidebar search "OTC" finds nothing (live 2026-10-01); the stock-out maps to Stock Adjustment SAN, type Stock Adjustment Admin (candidate) |
| 11 | What feeds the GRN | GRN suggested quantity comes from the GIN (Delivery Man PJP) | Sales return page says Picked CM-02 returns are handed to the GRN | goods_return_note.md vs sales_return.md | OPEN (BA7) |
| 12 | Order of Cashmemo Status vs sales return | delivery_lifecycle puts Status (seq 33, Delivered) before Sales Return (34-38) | Cashmemo Status GIN Number list was empty for DM PJPs on 2026-10-01; whether a return needs Delivered status is open (Q40) | delivery_lifecycle.md, screen_harvest_log.md | OPEN |
| 13 | Stock Inquiry screens | Stock Inquiry layout 201069 (seq 9, 24, 50) | seq 60 reads "Stock Inquiry II" DYL_BG1015 | stock_inquiry_and_balances.md vs end_of_day_validations.md | OPEN (Auto_Tssm has no Stock Inquiry; he has Stock Master Inquiry) |
| 14 | When does the DA loss record exist | "created when the DA is forwarded" (da_loss_approval.md, default of DAL2) | no record after the maker's Forward, Serial 638 after the checker's approval (live) | da_loss_approval.md, dispatch_advice.md | **RESOLVED 2026-10-01**: created at the DA approval; pages corrected |
| 15 | Is a start-of-day step needed (BA1) | "a new day has no rows until Generate Opening Balances"; GIN approval refused for earlier-day stock | the DA approval creates the day's row for the received product without the button (Opening 0, In 4, Closing 4) | stock_inquiry_and_balances.md, goods_issue_note.md | **RESOLVED for received products**; the remaining question (carry of previous closings, products not received that day) is BA14 |
| 16 | GIN workflow name | `StockUpdateGIN4Level` (goods_issue_note.md, glossary) | org 010104 uses `StockUpdateGIN` v53 (4Level only for parent orgs 0101/0102) | goods_issue_note.md | **RESOLVED 2026-10-01**: pages corrected |
| 17 | Execution status 19 "CM Reschedule" | listed in the delivery pages (from org 0101, Jan 2026 data) | glb_pr_exs_execution_status of org 010104 has no codes 04, 06, 19 | cashmemo_reschedule_and_status.md, delivery_lifecycle.md | OPEN: re-read the reschedule status live after a reschedule |

## 6. Counts

- Questions as written in the 26 pages: **73**. Unique after merging duplicates (13 merged: DAL3 into Q01, GRN3 into Q07, SV2 into Q10, DD1 into Q17, SA2 into Q19, CR3 into Q20, TI1 into Q23, DL4 into Q26, GIN1 into Q31, CR1 into Q32, SR5 into Q40, CS2 into Q51, CR4 into Q22): **60**.
- Before the live walk: A = 14, B = 33, C = 13 (14 + 33 + 13 = 60).
- **ANSWERED live 2026-10-01: 10** (Q04, Q06, Q10 = BA1, Q11, Q23, Q28, Q35, Q36, Q37, Q57; of the 33 B questions 9 were answered, of the 13 C questions 1).
- Still open from the original 60: **50** = **A 14**, **B 24** (33 - 9; 4 of them PARTLY answered: Q18, Q22, Q30, Q55, plus partial evidence on Q31), **C 12** (BA2-BA13).
- New items from the walk: **N1** (class B) and **BA14** (class C).
- **Open now: 52 = A 14 + B 25 + C 13.** The BA list has 13 questions (hard maximum 15).
- Contradictions: 17 listed; 7 resolved (1, 2, 3, 5, 14, 15, 16), 2 partly (9, 10), 8 open (4, 6, 7, 8, 11, 12, 13, 17).

## 7. Source code legend
DA = dispatch_advice, DAL = da_loss_approval, GRN = goods_return_note, SI = stock_inquiry_and_balances, SV = stock_validation_flows, OB = order_booking, OE = order_editing_cancellation, OL = order_lifecycle_and_statuses, SA = stock_allocation, TI = transaction_inquiry, DD = delivery_date_change, DL = delivery_lifecycle, GIN = goods_issue_note, CR = cashmemo_reschedule_and_status, SR = sales_return, DS = deposit_slips, RS = route_settlement, CS = cheque_status, DJ = dsr_adjustment, PJ = pjp_daily_inquiry_update, OT = otc_stock_out_and_san, EO = end_of_day_validations. Number = position in section 12 of that page.

## 8. New from learning session G11-PK 1 (2026-10-01 evening; not yet renumbered into the sections above)
Evidence: [learning_sessions/2026-10-01_G11-PK_session1_report.md](learning_sessions/2026-10-01_G11-PK_session1_report.md) §8.
| Id | Question | Default | Class |
|---|---|---|---|
| Q-OE1 | Is the Order Editing date range meant to be the delivery date, defaulting to today (orders booked today for a later delivery are invisible)? | treat as delivery date | C |
| Q-OE2 | Which order should group 11 seq 15 edit when workbook outlets 1000000001-03 are not offered on cnr1dev1? | the outlet-04 order | C |
| Q-OE3 | Should editing / cancelling an order on an approved GIN be blocked or warned (business control)? | allowed (as observed); record as defect candidate | C |
| Q-DA1 | May the Maker approve or reject his own Pending Dispatch Advice (buttons stay enabled for him)? | must not (QA convention); possible defect | C |
| Q-SR1 | When does an approved and picked sales return reduce the cash memo receivable (credit note? Route Settlement)? | at Route Settlement / credit note | B |
| Q-DS1 | What is deposit-slip "posting" (who/when), and may a partly allocated slip be posted? | at Route Settlement | B |
| Q-RS1 | How is a working day closed (which screen/process), and may 2026-09-30 be closed on cnr1dev1? | ask BA before closing | C |
| Q-OB1 | Who or what generated the 2026-10-01 opening balances during the day (morning: none; 16:40: present)? | unknown | B |
| Q-DS2 | Is a duplicate cheque number for the same outlet allowed, and should a cash memo already fully allocated on an unposted slip be blocked on another slip? | both should be blocked (current acceptance = defect candidate) | C |
| Q-RS2 | What does Route Settlement do with Sale Value not covered by collections (87,107 on 2026-10-01): cash shortage, carried to the next day, or blocked? | shown as Cash Shortage at settlement | B |
| Q-DA2 | What are "Dispatch Advice NUP" and "Dispatch Advice II" in the menu, and are they in scope? (page inbound_stock\dispatch_advice.md) | out of scope; only "Dispatch Advice" is tested | A |
| Q-DA3 | Why does the product label price differ from the Purchase Price / PC (and purchase exceed trade price for some SKUs)? (page inbound_stock\dispatch_advice.md) | label shows another price list; assert amounts on Purchase Price / PC only | C |
| Q-GRN1 | When Actual < Suggested on a GRN, where does the difference go (loss record, shortage at Route Settlement)? (page inbound_stock\goods_return_note.md) | shortage charged to the delivery man at Route Settlement | B |
| Q-GRN2 | Does a sales return booked as Damaged/Expired/Lost come back on the GRN with that stock type? (page inbound_stock\goods_return_note.md) | yes, per line stock type | B |
| Q-LA1 | Is an approved loss used anywhere else (claim to the supplier, finance, a claim loss log)? (page inbound_stock\da_loss_approval.md) | claim record only, no stock effect | C |
| Q-LA2 | Why is Reject disabled for the Checker on a Pending loss record while the workflow declares Rejected? (page inbound_stock\da_loss_approval.md) | losses cannot be rejected on this screen; do not design a Reject case | B |
| Q-LA3 | Is the duplicate "Lost" entry in the loss Stock list two different stock types? (page inbound_stock\da_loss_approval.md) | master-data duplicate; use the first | A |
| Q-SV1 | May the framework stock checks (seq 9, 24, 50) be changed to before/after deltas (needs a pre-snapshot step)? (page inbound_stock\stock_validation_flows.md) | yes, deltas | C |
Answered this session: L21 / loss-stock effect (approving a DA loss creates no stock row); GIN Verify+Approve = one Checker Forward in org 010104; why Order Editing showed no outlets (delivery-date filter).
