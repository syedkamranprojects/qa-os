# Settlement and finance (group 11 seq 39-60, 68-71)

Area summary:
1. After delivery and returns, the DSR banks collections: six deposit-slip variants (cash, cheque, multi-cheque, unposted) reduce cash-memo balances.
2. Route Settlement reconciles one PJP and date: sales, returns, previous/today cash and cheque, stock and cash shortage.
3. Transaction Inquiry checks (seq 52) confirm offsets; deposit slips are re-read after settlement (53) and after an order removal (54).
4. Cheque Status marks banked cheques Presented/Collected/Realized/Bounced/Cancelled.
5. DSR Adjustment Amount posts a manual DSR correction (doc type AD-07); PJP Daily Inquiry Update closes the journey record.
6. OTC Stock Out is a SAN created by Maker and approved by Checker Auto_Tssm (Draft -> Pending -> Approved).
7. End-of-day validations check stock (seq 60) and amounts/tax/charges (68-71); read-only.
8. All maker work is Auto_Multi_Orga in one session except the SAN approval.
9. No flow here has a live replay and the DB holds no 010104 rows for these tables, so most statements are [db]/[inferred].
10. Many assertions are toast-only: green runs do not prove the arithmetic.

Order of pages: deposit_slips.md, route_settlement.md, cheque_status.md, dsr_adjustment.md, pjp_daily_inquiry_update.md, otc_stock_out_and_san.md, end_of_day_validations.md.

## What this area hands to the next area
| item | to | note |
|---|---|---|
| REPO_Deposit_Slip | none consumed in group 11 | used only for slip checks |
| Settlement row (PJP + date) | day close / reports | Route Settlement Statement Report [db menu] |
| Cheque status (R/B) | receivable reports | Cheque For Realization |
| Approved SAN stock-out | Opening/Closing validation (seq 60) | stock keyed by calendar day |
| Verified totals | cycle end | nothing further in group 11 |

Related pages by name: inbound stock (GRN), order planning, delivery and returns (other analysts).
