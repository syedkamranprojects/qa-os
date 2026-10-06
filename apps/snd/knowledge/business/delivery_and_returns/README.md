# Area: delivery and returns (group 11 seq 20-38)

Updated: 2026-10-06 (consolidated with learning session G11-3: GIN 508 + GIN 509 for the 10-05 Reattempt order, return COL26000000715; a Reattempt order due today blocks Route Settlement until allocated, put on a GIN, approved and delivered; evidence ../learning_sessions/2026-10-06_G11-PK_session3_log.md); 2026-10-05 (consolidated with learning sessions G11-2/2b: GIN 507, return COL26000000714, second day; evidence ../learning_sessions/2026-10-05_G11-PK_session2_log.md, ..._session2b_resume_log.md); 2026-10-01 (consolidated with learning session 1 LEARN-G11-PK/20261001-1611; source `../learning_sessions/2026-10-01_G11-PK_session1_log.md`)

1. Stock leaves the warehouse with the Goods Issue Note (GIN): maker saves and forwards, a different checker approves; approval needs a stock balance for the day. Observed 2026-10-01 (GIN 506): one Checker Forward is the final approval; Allocated moves to Out, Closing unchanged.
2. Cash memos (CM-01) then get delivered, or rescheduled with a reason, via Cashmemo Status and Cashmemo Reschedule. Observed 2026-10-01: Reschedule (set the new Delivery Date first) -> Reattempt, off the GIN; Cashmemo Status tick + Save -> "Updated successfully", Delivered/Invoiced with the actual delivery time.
3. Returns come back as Sales Returns (CM-02): create with validation, forward, approve by a checker, then Status Change to Picked. Observed 2026-10-01: only delivered cash memos, own number, Sales Return View "Success" for Maker forward and Checker approval, "Save Sale Pick"; the receivable is not reduced (Q-SR1).
4. Most knowledge is [atlas]/[db]/[inferred]: only the GIN create/forward/approve-failure was observed live (2026-09-30); seq 29-38 are not yet replayed. (superseded 2026-10-01: seq 20-50 walked live in learning session 1; the pages are now largely [observed 2026-10-01 G11-1])
5. Biggest blocker: GIN approval fails when stock was received on an earlier calendar day. (2026-10-01: succeeds when DA receipt, orders, Delivery Date Change and GIN all run on the same day)
6. Cash memo and GIN statuses are in `delivery_lifecycle.md` (execution chain 02, 03, 13, 10/18/19). Observed chain: Confirmed -> Ready to dispatch/Packed -> Delivered/Invoiced | Reattempt | Cancelled.
7. Sales return and GIN live in shared tables (CM-02 in the cash memo tables, GN-01/GR-01 in snd_tr_gnm_gingrn_*).
8. Order of pages: goods_issue_note.md, cashmemo_reschedule_and_status.md, sales_return.md, delivery_lifecycle.md.
9. Goods Return Note (seq 48-49), dispatch advice, order booking/allocation and settlement are other analysts' pages. The GRN brings back cancelled, rescheduled, cut and returned quantities (19 CS reconciled exactly on 2026-10-01); see `delivery_lifecycle.md` §6.
10. Open questions: 5 + 4 + 5 + 4 = 18 (see section 12 of each page). (superseded 2026-10-01: GIN 8, Cashmemo 7, Sales Return 9, Lifecycle 7; many marked ANSWERED/PARTLY; new Q-SR1, Q-RS1, Q-DS1)
11. Second day 2026-10-05 reproduced every rule and amount (GIN 507, Cashmemo Reschedule 2012 -> 10-06, Cashmemo Status 2009-2011, return 714 Net 29,077, GRN 19 CS). New: a partly returned cash memo stays Delivered/Invoiced, the return reads Picked with Demand Channel "Partial Return" and Invoice Ref = source invoice; a part return re-prices slab promotions on the other lines (Q-SR2); the return is still not netted after the route is settled (Q-SR1) [observed 2026-10-05 G11-2, G11-2b].

Page one-liners:
- `goods_issue_note.md`: GIN create, forward, Checker approval; stock Allocated -> Out; walked live 2026-10-01 (GIN 506).
- `cashmemo_reschedule_and_status.md`: reschedule (new date first, Reattempt, off the GIN) and delivery marking (Delivered/Invoiced); edit/cancel after GIN move no stock; walked live 2026-10-01.
- `sales_return.md`: CM-02 return from a delivered cash memo, Maker forward / Checker approve ("Success"), Save Sale Pick; not netted from the receivable (Q-SR1); walked live 2026-10-01.
- `delivery_lifecycle.md`: end-to-end status and stock chain incl. the Transaction Inquiry status table and the GRN 19 CS reconciliation; walked live 2026-10-01.

| What this area hands to the next area | To | Carrier |
|---|---|---|
| Approved GIN number, stock issued to the DSR | Cashmemo Reschedule, Sales Return Status Change, Deposit Slip (settlement) | `REPO_GINNO` |
| Delivered cash memos (status 10/18) and their amounts | Settlement: Deposit Slip, DSR settlement | cash memo tables |
| Rescheduled cash memos (status 19, new delivery date) | next day order planning | CM-01 delivery date |
| Picked sales returns (CM-02, status 04) | Goods Return Note (inbound stock) | CM-02 document |
| Stock balance In/Out after GIN | Stock validation steps | `snd_tr_ssb_salestock_balance` |
| Undelivered quantities (cancelled/cut after GIN, rescheduled, returned) | Goods Return Note (Suggested), then Stock Inquiry In | GIN number on the GRN (observed 2026-10-01) |
