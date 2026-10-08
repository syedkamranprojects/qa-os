# Merge report: QA team written answers to the 2026-10-06 review (merged 2026-10-08)

- **Source:** [2026-10-08_QA_Team_Review_answers.md](2026-10-08_QA_Team_Review_answers.md). It holds the verbatim answer text from the filled review `apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx`. The review asked about 21 rules and 16 open-question items.
- **Method:** `docs/LEARNING_STANDARD.md` §3, following the conventions of the 2026-10-06 merge:
  - Every new fact is tagged **[stated 2026-10-08 QA Team]**.
  - Bullets are prefixed "QA team 2026-10-08".
  - A replaced statement keeps its text and gets "(superseded 2026-10-08: ...)".
  - Nothing was deleted.
  - Every page touched has `updated: 2026-10-08` in its front-matter and an "Updated 2026-10-08" header line.
- **Scope:** no walk, no SQL, no git. Nothing was observed live in this merge.

## 1. Result in numbers

| | Before (2026-10-06) | After (2026-10-08) |
|---|---|---|
| Open questions | 47 = A 15 + B 19 + C 13 (1a 12, 1b 1) | **36 = A 15 + B 12 + C 9 (1a 7, 1b 2)** |
| Closed by these answers | - | 14 (C 5, B 9) |
| Partly answered, still open | - | 1 (Q-SR1) |
| Not answered, follow-up sent 2026-10-08 | - | 1 (Q-SV1) |
| Reopened, answer under clarification (follow-up sent 2026-10-08) | - | 1 (Q-DS4) |
| New questions | - | 2 (Q-OE5, Q-RL1; both class B) |
| Contradictions | 27 listed: 16 resolved, 5 partly, 6 open | 32 listed: 19 resolved, 5 partly, 8 open |
| Defects | D-G11-3-1 | + **D-G11-2b-1** (D-G11-3-1 kept, under clarification) |

Arithmetic: B 19 - 9 + 2 = 12; C 13 - 5 + 1 = 9; 15 + 12 + 9 = 36. The full breakdown is in OPEN_QUESTIONS.md section 6.

## 2. Questions

**Answered and closed (OPEN_QUESTIONS.md section 2d):**

| Q | Class | Answer in one line |
|---|---|---|
| BA2 | C 1a | Approval is enforced by role through a workflow. Role 0001 NG User submits (Authorized flag N). Role 0002 TSSM approves. Roles 0003 DSR and 0004 Warehouse are mobile users (Authorized N). Role 9999 HQ bypasses the workflow. R1 uses two-level approval. |
| BA11 | C 1a | "Clear" means Cleared/Realized; PK and BD set it as soon as the slip is posted. Bounced (through the Bounced Cheque option) reverses the invoice payment, and the amount becomes outstanding at outlet level. |
| BA12 | C 1a | Cash can be reduced but never below zero; the difference is the Cash Shortage. Cheques cannot be modified. Stock shortage = expected GRN quantity (GIN - delivered + picked returns) minus the actual quantity. Not covered by the answer: what feeds Total Adjusted, and whether a negative amount is allowed. Default: do not assert or enter either. |
| Q-OE3 | C 1a | Editing after the GIN is controlled by the ORGA parameter CASHMEMO_EDIT (CM_Edit). With Y, only quantity reduction is allowed, a reason is required, and Save reduces the approved GIN quantity. With N, editing is disabled. This contradicts three walks (see contradiction 28). |
| Q-SR2 | C 1a | A partial return builds a "middle invoice" for the remaining quantity and re-prices price, scheme and tax on it. The return = original invoice - middle invoice. Fresh Return uses the same logic with the current date. |
| Q16, Q27 | B | Order quantity up to the available stock is allocated in full. Above the available stock, only the available quantity is allocated. With no stock the order stays unallocated with Cash Memo status Order. |
| Q29 | B | The delivery date cannot be earlier than the order creation date. |
| Q48 | B | The difference between Payable and Received is the DSR Cash Shortage. |
| Q-DS3 | B | A settled route with unposted slips should not be possible. It is a defect (**D-G11-2b-1**). |
| Q-GRN1 | B | The difference is a DSR Stock Shortage. GRN approval auto-creates a DSR adjustment, which shows on Route Settlement. |
| Q-GRN2 | B | Sales returns can be booked for Sound, Damaged and Expired stock (with reference to an old cash memo). |
| Q53 | B | The DSR adjustment document has no approval workflow. |
| Q58 | B | Stock changes when the document is approved. |

**Partly answered, still open:**
- **Q-SR1**: credit notes are adjusted at outlet level, against invoices whose net amount is greater than the credit note. Fresh Return is used in Bangladesh only. Not every scenario appears for every PJP. Still unexplained: returns 713, 714 and 715 were not netted on any of the three days.

**Not answered (follow-up sent 2026-10-08):**
- **Q-SV1**: the QA team described their daily smoke testing but did not answer whether the stock checks may change to before/after deltas.

**Reopened (follow-up sent 2026-10-08):**
- **Q-DS4**: the QA team answered N to rule 13 (doubled Outstanding Outlet totals are a display defect). Their comment is about the Transaction Inquiry offset and does not address the outlet totals. The 2026-10-06 display-defect ruling stays in force until clarified.

**New questions:**
- **Q-OE5** (B): is CASHMEMO_EDIT = Y on cnr1dev1, and does an edit after GIN approval reduce the approved GIN quantity? Checklist item L42.
- **Q-RL1** (B): which role codes and Authorized flags do the cnr1dev1 users hold? KPO_mp's self-approval and the 0005/0005 GIN workflow do not match the stated roles. Checklist item L43.

**Unchanged but with new evidence:** BA4, BA10, BA14, Q42, Q-RS4.

## 3. Rules (section 2 of the review)

| Rule | Agree | Merged as | Pages |
|---|---|---|---|
| 1 | Y | Order Editing lists only unallocated orders of today. | order_editing_cancellation |
| 2 | Y | The user can only reduce quantity. Save auto-allocates the available stock. | order_editing_cancellation, stock_allocation |
| 3 | **N** | Correction: editing after the GIN depends on CASHMEMO_EDIT. The 2026-10-06 statement "edit after GIN without unallocation" is superseded. Contradiction 28 / Q-OE5. | order_editing_cancellation, glossary, stock_inquiry_and_balances |
| 4 | Y | Reschedule unallocates the order (confirmed). | stock_allocation, cashmemo_reschedule_and_status |
| 5 | Y | Ordered / Allocated / Delivered confirmed. | transaction_inquiry |
| 6, 7 | Y | Stock reconciliation and carry forward (previous closing = next opening). | stock_inquiry_and_balances, glossary |
| 8 | Y | Tax is recalculated from 4 outlet attributes: Registered, Tax Filer, Advance Tax Exempted, Tax Exempted. | order_booking |
| 9 | Y | Parameter ZERO_TAX_ORDER_EXEMPTION: Y allows delivering zero-tax invoices, N blocks it. Refines the 2026-10-06 zero-tax rule. | order_booking, cashmemo_reschedule_and_status, delivery_lifecycle, glossary |
| 10 | Y | The three Deposit Slip tabs; the Back Office screen is the manual path. | deposit_slips |
| 11 | Y | Duplicate cheque numbers are allowed (confirmed). | deposit_slips |
| 12 | **N** | Correction of the process: Delivery App collection -> mobile sync -> slips auto-created Unposted -> Route Settlement with the accountant -> Posted. The purpose texts of both pages are updated. The observed non-blocking of manual slips is kept (contradiction 32, partly). | deposit_slips, route_settlement, settlement README |
| 13 | **N** (comment off-topic) | Comment recorded on Transaction Inquiry (offset fully adjusted, net unchanged). Q-DS4 reopened (contradiction 29). | transaction_inquiry, deposit_slips |
| 14 | Y | Cheque statuses Cleared/Realized and Bounced; PK/BD clear at posting. | cheque_status |
| 15 | Y | The settlement amount is not editable; only adjustment fields are (fuel / challan). Stock shortage value = sale price x quantity (UOM) + tax % from Product Configuration. | route_settlement |
| 16 | Y | Meaning of settlement: the DSR's final settlement with the accountant. | route_settlement |
| 17 | Y | Ignore colours: an Edit link means not settled, blank means settled. Supersedes the yellow/green legend. Contradiction 30, resolved. | route_settlement, glossary, FRAMEWORK_DRIFT row 38 |
| 18 | Y | Previous-day check: PJP working date = today and closing date = N-1. | route_settlement, pjp_daily_inquiry_update |
| 19 | Y | GIN quantity must match GRN quantity, otherwise **"Stock Mismatch"** (new message, not observed). | route_settlement, goods_return_note |
| 20 | Y | The stock shortage cannot be changed. The scope of this remark is unclear. | dsr_adjustment |
| 21 | Y | The day close option is used for manual Back Office work. | pjp_daily_inquiry_update |

## 4. Contradictions and defects

**Contradictions:**
- **28 (open), CASHMEMO_EDIT vs observation.** Stated: an edit after GIN approval reduces the approved GIN quantity. Observed on 10-01 (2003), 10-05 (2009) and 10-06 (2015): Stock Inquiry did not move, and the cut quantity came back on the GRN. Next step: check the CASHMEMO_EDIT value on cnr1dev1 and re-observe (Q-OE5, L42).
- **29 (open), Q-DS4.** The display-defect ruling (2026-10-06) meets the N answer with an unrelated comment. Under clarification.
- **30 (resolved), colour vs Edit link.** The Edit link is used from now on.
- **31 (open), stated roles vs observation.** Stated roles (0001 submits, 0002 approves) do not match KPO_mp approving his own DA 570, or the 0005/0005 GIN workflow (Q-RL1, L43).
- **32 (partly), rule 12.** The process correction is merged. The non-blocking of manual slips is kept as observed.
- **20 resolved**: cheque "Clear" = Cleared/Realized.
- **21 resolved**: Complete implies all slips Posted; the 10-01 case is a defect.
- **2 annotated**: BA2 answered.

**Defects:**
- **D-G11-2b-1 (new)**: route 02112 for 2026-10-01 shows Complete while its slips 1131-1136 are still Un Posted, and memos 2004 and 2005 never adjusted. Evidence: G11-2b on 10-05 and G11-3 on 10-06. The QA team ruled it a defect (LIVE_FINDINGS.md).
- **D-G11-3-1 (kept)**: doubled Outstanding Outlet totals. Under clarification (Q-DS4).

## 5. Files changed

**Area pages** (front-matter `updated: 2026-10-08` plus a header line):
- `settlement_and_finance/`:
  - `route_settlement.md`
  - `deposit_slips.md`
  - `cheque_status.md`
  - `dsr_adjustment.md`
  - `pjp_daily_inquiry_update.md`
  - `otc_stock_out_and_san.md`
  - `README.md` (summary item 13)
- `order_to_delivery_planning/`:
  - `order_editing_cancellation.md`
  - `stock_allocation.md`
  - `order_booking.md`
  - `delivery_date_change.md`
  - `transaction_inquiry.md`
  - `README.md`
- `delivery_and_returns/`:
  - `sales_return.md`
  - `cashmemo_reschedule_and_status.md`
  - `delivery_lifecycle.md`
  - `goods_issue_note.md`
- `inbound_stock/`:
  - `goods_return_note.md`
  - `stock_inquiry_and_balances.md`
  - `stock_validation_flows.md`
  - `dispatch_advice.md`

**Shared files:**
- `OPEN_QUESTIONS.md`: section 2d, recounts, rows Q-OE5 and Q-RL1, Q-DS4 reopened, contradictions 28-32, section 6 arithmetic.
- `glossary.md`: 16 terms added, including the configuration parameters CASHMEMO_EDIT and ZERO_TAX_ORDER_EXEMPTION and the role codes; 8 rows annotated.
- `INDEX.md`: application roles paragraph; 5 document-map rows annotated.
- `document_lifecycle.md`: new section 0d.
- `LIVE_FINDINGS.md`: new block covering D-G11-2b-1, the Q-OE5 contradiction, Q-DS4 and the stated messages.
- `LIVE_LEARNING_CHECKLIST.md`: status table for 2026-10-08; new items L42 (Q-OE5), L43 (Q-RL1) and L44 ("Stock Mismatch", optional).
- `FRAMEWORK_DRIFT.md`: section 2d, rows 38-43:
  - 38: seq 51, assert the Edit link instead of the colour.
  - 39: GRN Actual < Suggested gives a DSR stock-shortage adjustment.
  - 40: "Stock Mismatch" precondition.
  - 41: after-GIN edit stock effect, pending Q-OE5.
  - 42: cheque "Clear".
  - 43: all slips Posted after settlement.

**This report**, plus a resume paragraph in `docs/STATUS.md`.

## 6. Follow-ups

1. **QA team (sent 2026-10-08):**
   - Q-DS4: was the rule-13 comment meant for the doubled Outstanding Outlet totals?
   - Q-SV1: may seq 9, 24, 50 and 60 become before/after deltas?
2. **QA team / development:** report D-G11-2b-1 with the evidence in LIVE_FINDINGS, and ask how the 10-01 route was completed.
3. **Next walk:**
   - L42 (CASHMEMO_EDIT and GIN quantity after an edit).
   - L43 (role codes on the Profile screen).
   - L41 (record ZERO_TAX_ORDER_EXEMPTION first).
   - Optional, with the QA Team Lead's go-ahead: L44 ("Stock Mismatch").
   - When a case reduces cash Received, observe the Cash Shortage (Q48 stated, not yet seen).
4. **Q-SR1:** why approved and picked returns are not netted at settlement in PK (credit-note path). The QA team plans to add these scenarios to the Regress Master flow.
