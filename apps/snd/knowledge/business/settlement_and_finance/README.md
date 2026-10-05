# Settlement and finance (group 11 seq 39-60, 68-71)

Last updated: 2026-10-01 (consolidated with learning session G11-1, `learning_sessions/2026-10-01_G11-PK_session1_log.md`; the session stopped at seq 51).

Area summary:
1. After delivery and returns, the DSR banks collections: six deposit-slip variants (cash, cheque, multi-cheque, unposted) reduce cash-memo balances. (superseded 2026-10-01: all six walked live (slips 1131-1136); allocating a slip does NOT reduce the balance at once. Balances move only at "posting", presumably at Route Settlement. Until then the allocations show as "Un Posted Amount" on the cash memo [observed 2026-10-01 G11-1].)
2. Route Settlement reconciles one PJP and date: sales, returns, previous/today cash and cheque, stock and cash shortage. [observed 2026-10-01 G11-1: grid read for 02112. Each deposit slip is one Collection Type line at its allocated amount. Settlement BLOCKED: "Following previous days not closed! Please close date. 2026-09-30".]
3. Transaction Inquiry checks (seq 52) confirm offsets; deposit slips are re-read after settlement (53) and after an order removal (54). [not walked yet: they depend on a completed settlement]
4. Cheque Status marks banked cheques Presented/Collected/Realized/Bounced/Cancelled.
5. DSR Adjustment Amount posts a manual DSR correction (doc type AD-07); PJP Daily Inquiry Update closes the journey record.
6. OTC Stock Out is a SAN created by Maker and approved by Checker Auto_Tssm (Draft -> Pending -> Approved).
7. End-of-day validations check stock (seq 60) and amounts/tax/charges (68-71); read-only.
8. All maker work is Auto_Multi_Orga in one session except the SAN approval. [observed 2026-10-01 G11-1 for seq 39-51]
9. No flow here has a live replay and the DB holds no 010104 rows for these tables, so most statements are [db]/[inferred]. (superseded 2026-10-01: deposit slips (seq 39-46) and the Route Settlement screen (seq 51, read only up to the block) are now [observed]; the other pages are still [db]/[inferred].)
10. Many assertions are toast-only: green runs do not prove the arithmetic.
11. Key traps [observed 2026-10-01 G11-1]:
    - The Deposit Slip screen first opens with the booking PJP and bank "demo" preset; the slip needs the delivery DSR.
    - The multi-cheque popup takes dates as MM/DD/YYYY.
    - Adjusted Amount refreshes only when the screen is reloaded.
    - The bank "National Bank of Pakistan" has drifted to "...ss".
    - A duplicate cheque number is accepted, and a cash memo can apparently be allocated twice.
    - The approved sales return is not netted before settlement.
    - Route Settlement needs every earlier working day closed (a day-boundary trap for any replay).

Order of pages and walk state:

| Page | Walk state |
|---|---|
| deposit_slips.md | walked 2026-10-01 G11-1 (seq 39, 40, 41, 42, 44, 46) |
| route_settlement.md | walked 2026-10-01 G11-1 up to the block (seq 51); seq 52-54 not walked |
| cheque_status.md | not walked yet (G11-1 stopped at seq 51) |
| dsr_adjustment.md | not walked yet (G11-1 stopped at seq 51) |
| pjp_daily_inquiry_update.md | not walked yet (G11-1 stopped at seq 51) |
| otc_stock_out_and_san.md | not walked yet (G11-1 stopped at seq 51) |
| end_of_day_validations.md | not walked yet (G11-1 stopped at seq 51) |

## What this area hands to the next area
| item | to | note |
|---|---|---|
| REPO_Deposit_Slip | none consumed in group 11 | used only for slip checks |
| Deposit slips (Un Posted) | Route Settlement | one Collection Type line per slip, at its allocated amount [observed 2026-10-01 G11-1] |
| Settlement row (PJP + date) | day close / reports | Route Settlement Statement Report [db menu] |
| Cheque status (R/B) | receivable reports | Cheque For Realization |
| Approved SAN stock-out | Opening/Closing validation (seq 60) | stock keyed by calendar day |
| Verified totals | cycle end | nothing further in group 11 |

## Open questions raised in this area (2026-10-01)
- Q-DS1 (class B): what is deposit-slip posting and when does it happen? Default: at Route Settlement.
- Q-RS1 (class C): how is a working day closed, and may 2026-09-30 be closed on cnr1dev1? Default: ask the BA before closing.
- Q-SR1 (class B): when does an approved sales return reduce the receivable? Default: at Route Settlement / credit note.
- Q-DS2 (C) and Q-RS2 (B) are local to the pages (duplicate cheque / double allocation; uncovered Sale Value at settlement).

Related pages by name: inbound stock (GRN), order planning, delivery and returns (other analysts).
