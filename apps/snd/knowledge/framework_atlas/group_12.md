# Group 12 - Order Booking Promotion Testing Only Positive Flow

Source `gtf:12`. Market guess (from name): None. Rows: 5 (active 1, inactive 4). User switch points: 1 (8).

Allowed apps (alg): app 5 PK_Centegy QA -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak); app 8 PK_Centegy QA 2 -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak)
Starts with an app login flow: False (first active flow 00910001).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 8 - Order Booking Promotion** (`00910001`) - area: Order Booking, Promotion
   - **SWITCH USER POINT**: log out and log in as **AppUser** (serial 4)
   - consumes: `g_REPO_ORGA` unresolved in group; `g_REPO_CMDOCTYPE` unresolved in group; `ORDERNUMBER` produced within same flow; `REPO_REF_ORDER_NO` unresolved in group; `g_REPO_DISTRIBUTOR` unresolved in group
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Order Booking -> Order Booking Detail -> Order Booking Detail2
   - detail: flows/00910001.md ; trace prefix `12:8:00910001`

## Inactive rows (skipped by the engine)
- seq 2 Dispatch Advice Bulk Testing (`00920001`) status N
- seq 4 Dispatch Advice Approval (`00740001`) status N
- seq 5 Dispatch Advice Loss Approval Request (`00750001`) status N
- seq 6 Dispatch Advice Loss Approval (`00760001`) status N
