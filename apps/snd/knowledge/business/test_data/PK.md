# Test data catalog - Pakistan (PK, region R1), env cnr1dev1

Sources: G11 learning sessions 1-3 (2026-10-01/05/06), quick runs 2026-10-07/08. Tags as in docs/LEARNING_STANDARD.md §3.4.

## Organisation and users
| Item | Value | Source |
|---|---|---|
| Company | Unilever Pakistan Limited (org 010104) | [observed 2026-10-01 G11-1] |
| Distributor | 15108843 - IBRAHIM TRADERS ("Auto KARACHI") | [observed 2026-10-01 G11-1] |
| Maker | Auto_Multi_Orga (also Automation) | [stated 2026-10-01 QA lead] |
| Checker | Auto_Tssm | [stated 2026-10-01 QA lead] |
| Head office | headquarter (setup flows only) | [stated 2026-10-05 QA lead] |

## Order booking route
| Item | Value | Source |
|---|---|---|
| Order Booker/Spot Seller | Order Booker (also Spot Seller, Van Sales) | [observed 2026-10-08 quick run] |
| Booking PJP | 02111-AutomationOB1 | [observed 2026-10-01 G11-1] |
| Delivery PJP / DSR | 02112-AutomationDSR / ITB0189-AutomationQADSR | [observed 2026-10-05 G11-2] |
| Selling Category | Selling Category 001 (must be chosen; does not auto-fill) | [observed 2026-10-01 G11-1] |
| Section | Automation_Testing_Section (101010101101) | [observed 2026-10-01 G11-1] |
| Other booking PJPs offered | AUTO241602, AutoPromo1, 7918624876, AutoPJGIN1, AUTO021311, AUTO061238, AUTO031026 (not trained) | [observed 2026-10-01 G11-1] |

## Outlets on PJP 02111 / Selling Category 001 / Automation_Testing_Section (43 offered)
| Outlet | Tax behaviour seen | Used in | Source |
|---|---|---|---|
| 1000000004 | taxed (18% on 62740537) | G11 orders, quick runs | [observed 2026-10-01..08] |
| 1000000005 | label "Exempt Y"; Tax 0 on 10-01/05/06, **taxed on 10-07** (master data changes) | G11, quick 10-07 | [observed] |
| 1000000006 | label "Exempt Y"; Tax 0 until 10-05, taxed 10-06 | G11 | [observed] |
| 1000000007 | taxed until 10-05, Tax 0 on 10-06 | G11 | [observed] |
| 1000000008 | taxed 10-01/05/06, Tax 0 on 10-07 | G11, quick 10-07 | [observed] |
| 1000000011 | taxed | G11 | [observed] |
| 1000000012 - 1000000020 | not yet used | - | [observed 2026-10-08 outlet list] |
| 1000000016 | booked OK (COL26000002026) | quick 10-08 | [observed 2026-10-08] |
| C0124183423/26/33/39, C0124186615/22, C0154186884..C0154186971 (several), C0154187365 | not used; "Automation QA TEST" / "Aautomation_Outlet" | - | [observed 2026-10-08 outlet list] |
| 1000000001 - 1000000003 | **not offered** on this PJP | - | [observed 2026-10-01 G11-1] |
Rule: outlet tax behaviour follows outlet master data and changes between days; never assert tax from the outlet label (Q-TX1). A zero-tax invoice of a non-exempt outlet cannot be delivered when ZERO_TAX_ORDER_EXEMPTION = N [stated 2026-10-08 QA Team].

## Products (warehouse C0000000055-Auto Main Warehouse, stock type 01-Sound, batch 1-1)
| SKU | Description | Pack (PC per CS) | Source |
|---|---|---|---|
| 62740537 | RAFHAN SLPC OILS CORN TIN PI7 2X10L | 2 (5 CS 4 PC -> 7 CS) | [observed 2026-10-01 G11-1] |
| 20050310 | BLUEBAND MARGARINE A01 CP+GIFT 16X500G | 16 [inferred from description] | [observed] |
| 62690363 | SURF EXCEL HS STD PWD CARE P03 204X35G | 204 [inferred from description] | [observed] |
| 20050308 | BLUE BAND MARGARINE 32X250G | 32 [inferred from description] | [observed] |
| 69997598 | KNORR CKN CUBE IRON 288X18G | 288 [inferred from description] | [observed] |
Stock for these comes from a same-day Dispatch Advice (vendor UPL WH); openings carry over only when the environment job runs. Check stock with a precondition step during execution.

## Gaps (ask the trainer)
- Other SKUs / product groups usable for orders (only the 5 above are trained).
- Which other PJPs, outlets and sections may be used (only 02111 + Automation_Testing_Section trained).
- Banks/branches and cheque data for deposit slips beyond Bank Al-Habib Limited / DHA Branch and National Bank of Pakistanss.
