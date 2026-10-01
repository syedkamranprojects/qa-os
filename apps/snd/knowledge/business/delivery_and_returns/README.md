# Area: delivery and returns (group 11 seq 20-38)

1. Stock leaves the warehouse with the Goods Issue Note (GIN): maker saves and forwards, a different checker approves; approval needs a stock balance for the day.
2. Cash memos (CM-01) then get delivered, or rescheduled with a reason, via Cashmemo Status and Cashmemo Reschedule.
3. Returns come back as Sales Returns (CM-02): create with validation, forward, approve by a checker, then Status Change to Picked.
4. Most knowledge is [atlas]/[db]/[inferred]: only the GIN create/forward/approve-failure was observed live (2026-09-30); seq 29-38 are not yet replayed.
5. Biggest blocker: GIN approval fails when stock was received on an earlier calendar day.
6. Cash memo and GIN statuses are in `delivery_lifecycle.md` (execution chain 02, 03, 13, 10/18/19).
7. Sales return and GIN live in shared tables (CM-02 in the cash memo tables, GN-01/GR-01 in snd_tr_gnm_gingrn_*).
8. Order of pages: goods_issue_note.md, cashmemo_reschedule_and_status.md, sales_return.md, delivery_lifecycle.md.
9. Goods Return Note (seq 48-49), dispatch advice, order booking/allocation and settlement are other analysts' pages.
10. Open questions: 5 + 4 + 5 + 4 = 18 (see section 12 of each page).

| What this area hands to the next area | To | Carrier |
|---|---|---|
| Approved GIN number, stock issued to the DSR | Cashmemo Reschedule, Sales Return Status Change, Deposit Slip (settlement) | `REPO_GINNO` |
| Delivered cash memos (status 10/18) and their amounts | Settlement: Deposit Slip, DSR settlement | cash memo tables |
| Rescheduled cash memos (status 19, new delivery date) | next day order planning | CM-01 delivery date |
| Picked sales returns (CM-02, status 04) | Goods Return Note (inbound stock) | CM-02 document |
| Stock balance In/Out after GIN | Stock validation steps | `snd_tr_ssb_salestock_balance` |
