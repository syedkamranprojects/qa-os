# S&D (DCODE) business knowledge: index and map of the Daily Cycle

Status: consolidated 2026-10-01 from the four analysts' pages. Nothing here is new knowledge; every fact keeps the confidence tag of its source page: **[observed]** seen live, **[db]** declared by the DB/framework tables, **[inferred]** concluded from names, **[unknown]** not determined. Companion files: [glossary.md](glossary.md), [document_lifecycle.md](document_lifecycle.md), [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md), [LIVE_LEARNING_CHECKLIST.md](LIVE_LEARNING_CHECKLIST.md), page template [_TEMPLATE.md](_TEMPLATE.md).
Updated: 2026-10-01 (live blocks 1-3b); 2026-10-01 G11-1 consolidation: seq 1-50 walked live on one day (evidence [learning_sessions/2026-10-01_G11-PK_session1_log.md](learning_sessions/2026-10-01_G11-PK_session1_log.md))

## 1. The business as one story: the Daily Cycle (framework group 11)

A distributor (DT) receives goods from the company supply point, books and allocates retail-outlet orders, issues the goods to a delivery man (DSR) on a Goods Issue Note, delivers or reschedules the cash memos, takes returns back, banks the money collected, reconciles the route, and closes the day. Stock balances are keyed by calendar day, so receive-and-issue must happen inside one calendar day [observed]. **Day-boundary rule (live-verified 2026-10-01):** the DA approval creates the day's stock row of a received product (Opening 0, In = received quantity) on the Received Date, without Generate Opening Balances; products with no movement on the new day have no row, and the previous day's closing is not carried automatically (62740537 closed 97 CS on 09-30 and opened 0 on 10-01), so stock received on an earlier day cannot be issued the next day (GIN approval: "No stock balance found for products") [observed]. Makers are Auto_Multi_Orga, checkers Auto_Tssm (no Stock Inquiry menu for Auto_Tssm) [observed].

### Step 1. Inbound stock (seq 2-9, 24, 48-50, 60) - folder [inbound_stock/](inbound_stock/README.md)
| Seq | Page | One line |
|---|---|---|
| 2, 5 | [dispatch_advice.md](inbound_stock/dispatch_advice.md) | Maker records goods dispatched by the vendor (UPL WH) to the distributor warehouse; checker approves; received quantity (dispatched minus loss) becomes Sound stock of the Received Date, row created by the approval [observed 2026-10-01]; duplicate SO Number allowed, SO optional. |
| 7 | [da_loss_approval.md](inbound_stock/da_loss_approval.md) | A DA with losses creates ONE loss record AT THE DA APPROVAL (rows per product and loss type 02 Damaged / 04 Lost); the checker approves it; **approving it creates no stock row** [observed 2026-10-01 G11-1]. |
| 9, 24, 50, 60 | [stock_inquiry_and_balances.md](inbound_stock/stock_inquiry_and_balances.md) | Read-only per-day view Opening/In/Out/Allocated/Closing in CS/DZ/PC; Closing = Opening + In - Out - Allocated (assert in base PC); empty on a new day until a movement (DA approval) creates the row [observed]. |
| 9, 24, 50, 60 | [stock_validation_flows.md](inbound_stock/stock_validation_flows.md) | The four framework checkpoints that read Stock Inquiry after DA, GIN, GRN and at opening/closing [atlas]. |
| 48-50 | [goods_return_note.md](inbound_stock/goods_return_note.md) | GRN brings back everything issued but not delivered (cancelled, cut, rescheduled) plus picked returns (GRN 246: 19 CS = 7+7+3+2); approval posts it as In (Sound) [observed 2026-10-01 G11-1]. |

### Step 2. Order to delivery planning (seq 10-19) - folder [order_to_delivery_planning/](order_to_delivery_planning/README.md)
| Seq | Page | One line |
|---|---|---|
| all | [order_lifecycle_and_statuses.md](order_to_delivery_planning/order_lifecycle_and_statuses.md) | The order is a cash memo (CM-01) from Ordered to Delivered; document types and statuses [db]. |
| 10 | [order_booking.md](order_to_delivery_planning/order_booking.md) | Order user books an outlet's demand (validate then save); no approval; auto-allocated at save [observed]. |
| 12, 18 | [stock_allocation.md](order_to_delivery_planning/stock_allocation.md) | Orders reserve stock at save (auto FULL), so manual Allocation is a no-op unless an order was unallocated; Unallocate/Allocate answer "Process completed successfully" after a confirm [observed 2026-10-01 G11-1; earlier "stock not found." superseded]. |
| 14, 68-71 | [transaction_inquiry.md](order_to_delivery_planning/transaction_inquiry.md) | Read-only check of Gross/Discount/Tax/Net and the Document Status column (execution status text: Confirmed after booking, Planning completed on a GIN); Total Offering = header Discount [observed]. |
| 15, 16, 29, 31 | [order_editing_cancellation.md](order_to_delivery_planning/order_editing_cancellation.md) | Edit quantities with a reason (same document no., promotions re-applied) or cancel with a reason; allowed even after the GIN, with no stock movement until the GRN; Order Editing dates filter the DELIVERY date [observed 2026-10-01 G11-1]. |
| 19 | [delivery_date_change.md](order_to_delivery_planning/delivery_date_change.md) | Moves the delivery date of a PJP's orders in bulk ("processed orders: 9") [observed]. |

### Step 3. Delivery and returns (seq 20-38) - folder [delivery_and_returns/](delivery_and_returns/README.md)
| Seq | Page | One line |
|---|---|---|
| 12-38 | [delivery_lifecycle.md](delivery_and_returns/delivery_lifecycle.md) | One cash memo from allocation to delivered/rescheduled/returned; execution status chain [db/inferred]. |
| 20, 23 | [goods_issue_note.md](delivery_and_returns/goods_issue_note.md) | GIN takes only cash memos whose delivery date = GIN delivery date, sums them per SKU; maker saves + forwards, ONE checker Forward approves (Allocated -> Out); succeeded with same-day stock + delivery date today (GIN 506) [observed 2026-10-01 G11-1]. |
| 32, 33 | [cashmemo_reschedule_and_status.md](delivery_and_returns/cashmemo_reschedule_and_status.md) | Reschedule sets a new delivery date with a reason (status Reattempt, off the GIN); Cashmemo Status tick + Save marks Delivered/Invoiced [observed 2026-10-01 G11-1]. |
| 34-38 | [sales_return.md](delivery_and_returns/sales_return.md) | Return (CM-02, own number) against a delivered cash memo: Maker saves + forwards on Sales Return View, Checker approves ("Success"), Maker "Save Sale Pick"; the receivable is not reduced by it (open) [observed 2026-10-01 G11-1]. |

### Step 4. Settlement and finance (seq 39-60, 68-71) - folder [settlement_and_finance/](settlement_and_finance/README.md)
| Seq | Page | One line |
|---|---|---|
| 39-46, 53-54 | [deposit_slips.md](settlement_and_finance/deposit_slips.md) | DSR banks cash/cheques: slip header then allocation per cash memo or per outlet (multi-cheque popup); slips stay "Un Posted" (balances unchanged) until settlement [observed 2026-10-01 G11-1]. |
| 51-54 | [route_settlement.md](settlement_and_finance/route_settlement.md) | End-of-day reconciliation per delivery man and date: sale value vs one collection line per deposit slip; **refused while an earlier day is open** ("Following previous days not closed! Please close date. 2026-09-30") [observed 2026-10-01 G11-1]. |
| 55 | [cheque_status.md](settlement_and_finance/cheque_status.md) | Banked cheques marked Presented/Collected/Realized/Bounced/Cancelled [db]. |
| 56 | [dsr_adjustment.md](settlement_and_finance/dsr_adjustment.md) | Manual DSR amount correction (AD-07); effect unknown [db/unknown]. |
| 57 | [pjp_daily_inquiry_update.md](settlement_and_finance/pjp_daily_inquiry_update.md) | Back-office correction of the daily PJP: journey status, file status, end date [db]. |
| 58, 59 | [otc_stock_out_and_san.md](settlement_and_finance/otc_stock_out_and_san.md) | Stock Adjustment Note stock-out: maker creates, checker approves; menu "OTC Stock Out" not found live [db/observed]. |
| 52, 60, 68-71 | [end_of_day_validations.md](settlement_and_finance/end_of_day_validations.md) | Read-only closing checks of stock and amounts/tax/charges [db]. |

## 2. Document map: who creates, who approves, status chain, effect

Only facts stated in the pages. "Maker" = Auto_Multi_Orga, "Checker" = Auto_Tssm on cnr1dev1.
**Group 11 user roles (R1 / Pakistan, stated by the QA lead 2026-10-01) [stated]:** company Unilever Pakistan Limited, distributor 15108843 - IBRAHIM TRADERS; there are **only two roles, Maker and Checker**, and each can have several users. Maker = **Auto_Multi_Orga** (default, framework serial 35) or **Automation** (serial 28, the framework's SAN Admin rows seq 61/63/66); Checker = **Auto_Tssm** (serial 8), who approves for every maker. There is no separate Stock Controller or Order User: the Maker runs stock checks, orders and allocation. Source of truth: `apps/snd/app.yaml` environments.cnr1dev1.roles.

| Document | Creates | Approves | Status chain (as the page states it) | Stock / finance effect |
|---|---|---|---|---|
| Dispatch Advice (DA-01) | Maker [observed] | Checker, same screen, Forward [observed] | Draft (grid In-Active) -> Pending for approval -> Approved (Active, Received Date set) [observed]; Rejected/Terminated [db] | Received qty (dispatched - loss) added to Sound stock of the Received Date, day row created by the approval [observed 2026-10-01]; net amount e.g. PKR 1,632,119.522 / 61,691.72 [observed] |
| DA Loss record (DALossApproval) | Created automatically AT THE DA APPROVAL when the DA has losses (not at Forward) [observed 2026-10-01] | Checker [observed] | Pending for approval -> Approved [observed]; Rejected/Terminated [db] | Stock effect NOT confirmed: no Damaged/Lost row appeared, also not while the loss is Pending [observed] |
| Order / cash memo (CM-01 Sales) | Order user (Maker) [observed] | none [observed] | document 04 Ordered; execution 02 Confirmed -> 03 Planning completed (on a GIN) [db][observed 2026-10-01] -> Cancelled 03 [db] / Delivered 01 [inferred] | Auto-allocated at save, reserved stock shown in Allocated [observed]; Gross + Discount(-) + Tax = Net [observed] |
| Stock allocation | Order user | none | Unallocated -> Allocated (FULL) [observed] | Reserves stock [inferred]; effect on stock screens unknown |
| Goods Issue Note (GN-01) | Maker [observed] | Checker, ONE Forward on the Pending GIN = final approval [observed 2026-10-01 G11-1, GIN 506]; workflow declares Verify then Approve, both role 0005 [db] | Draft/In-Active -> Pending for approval [observed] -> Approved (doc 01 Authorized, wf 03) [db]; Rejected 04, Terminated 05 [db] | Stock out to the DSR on approval [inferred]; approval needs a same-day stock balance [observed]; cash memos move to **Ready to dispatch/Packed** at approval [observed 2026-10-01 G11-1] (Planning completed seen on a pending GIN) |
| Cashmemo Reschedule | Maker | none [observed] | Ready to dispatch/Packed -> **Reattempt** [observed 2026-10-01 G11-1] | New delivery date; leaves the GIN; goods return on the GRN [observed 2026-10-01 G11-1] |
| Cashmemo Status | Maker | none [observed] | -> **Delivered/Invoiced**, Actual Delivery Date = save time [observed 2026-10-01 G11-1] | None expected [inferred]; creates receivable to settle [inferred] |
| Sales Return (CM-02) | Maker | Checker (SalesReturnApproval) [atlas/db] | Un-Authorized -> Pending -> Authorized -> Picked (04) [inferred/db]; Cancelled 03 [db] | No stock until GRN [inferred]; credit note CRN-02 may follow, trigger unknown [db] |
| Goods Return Note (GR-01) | Maker [atlas] | Checker [atlas] | Draft -> Pending for approval -> Approved [db/inferred]; Rejected/Terminated [db] | Returned qty back In to warehouse stock on approval [inferred]; stock type unknown |
| Deposit Slip | Maker | none (approval row inactive) [db] | I -> A with posting date [db sample, trigger unknown] | Reduces cash memo balances [inferred]; Unposted = not yet allocated [inferred] |
| Route Settlement | Maker | none [db] | No status; row existence [db] | Cash shortage = payable - received [inferred] |
| Cheque Status | Maker | none [db] | P/L -> R or B; C; A [db names, transitions unknown] | Bounce presumably restores receivable [inferred] |
| DSR Adjustment (AD-07) | Maker | none in flow [db] | Authorized / Un-Authorized / Adjustment / Cancelled; which on save unknown [db] | Effect on settlement unknown [unknown] |
| SAN stock out | Maker [db] | Checker [db] | Draft -> Pending for approval -> Approved (status A) [db]; Rejected/Terminated [db]; no "OTC Stock Out" type or menu, candidate type Stock Adjustment Admin SA-03 [observed/inferred] | Stock of product/batch/type in From Warehouse reduced on approval [inferred] |
| PJP Daily Inquiry Update | Maker | none | Mark Status values unknown [unknown] | Updates the daily PJP row [db] |

## 3. How to use this knowledge when generating test cases and steps

1. Read the page for the screen under test in this order: section 4 (inputs: real labels, mandatory fields, defaults) -> section 5 (process in standard vocabulary, with trace keys group:seq:flow) -> section 8 (rules and validations) -> section 9 (exact messages for assertions) -> section 11 (test design hints and traps).
2. Treat the confidence tag as a gate: an [observed] message or id may be asserted; [db]/[inferred] behaviour must be written as an expectation with a note "to be confirmed live"; [unknown] must not be asserted, put it in the live checklist instead.
3. Respect the day rule: any case that receives stock and later issues it (DA -> GIN) must run inside one calendar day (the DA approval creates the day's row for the received product; earlier-day stock is not carried), and any run starts from login [see glossary: Balance Date, and LIVE_LEARNING_CHECKLIST.md].
4. Stock assertions use before/after snapshots of the same row (not absolute In/Out), and a green toast never proves a stock or finance effect.
5. Open points are in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md): class B items are settled by running [LIVE_LEARNING_CHECKLIST.md](LIVE_LEARNING_CHECKLIST.md); class C waits for the BA; class A uses the stated default.
6. Never click Generate Opening Balances, Reject/Terminate or Bounce in a validation flow unless a case explicitly targets it (stock- or data-changing).
