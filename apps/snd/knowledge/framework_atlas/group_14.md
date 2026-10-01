# Group 14 - For GIN Testing

Source `gtf:14`. Market guess (from name): None. Rows: 12 (active 8, inactive 4). User switch points: 2 (5, 21).

Allowed apps (alg): app 5 PK_Centegy QA -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak); app 8 PK_Centegy QA 2 -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak)
Starts with an app login flow: False (first active flow 00100003).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 2 - Dispatch Advice Without Loss** (`00100003`) - area: Dispatch Advice
   - actor: same session (runner default login)
   - consumes: `REPO_DOCUMENTNO` produced within same flow
   - produces: `REPO_DOCUMENTNO`
   - checks: 4 message/field assertion(s); group assertion sheet(s): `DA_FORWARD_ASSR`
   - screens: Dispatch Advice -> Dispatch Advice -> Dispatch Advice Detail2 -> Dispatch Advice Grid
   - detail: flows/00100003.md ; trace prefix `14:2:00100003`
2. **seq 5 - Dispatch Advice Approval** (`00740001`) - area: Dispatch Advice, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_DOCUMENTNO` from seq 2 (00100003)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DA_APPROVALFRWD_ASSR`
   - screens: Dispatch Advice Approval
   - detail: flows/00740001.md ; trace prefix `14:5:00740001`
3. **seq 7 - Dispatch Advice Loss Approval** (`00760001`) - area: Dispatch Advice, Approval/Reject/Terminate
   - actor: same session (Auto_Tssm)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DA_LOSS_APPROVALFRWD_ASSR`
   - screens: Dispatch Advice Loss Approval
   - detail: flows/00760001.md ; trace prefix `14:7:00760001`
4. **seq 10 - Stock Allocation** (`00130001`) - area: Stock Allocation
   - actor: same session (Auto_Tssm)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_Allocation_ASSR`
   - screens: Stock Allocation
   - detail: flows/00130001.md ; trace prefix `14:10:00130001`
5. **seq 16 - Delivery Date Change** (`00160001`) - area: Delivery Date Change
   - actor: same session (Auto_Tssm)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery Date Change
   - detail: flows/00160001.md ; trace prefix `14:16:00160001`
6. **seq 17 - Goods Issue Note Negative** (`00890001`) - area: GIN (Goods Issue Note), Negative test
   - actor: same session (Auto_Tssm)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_DTL_SAVE_ASSR`, `screenshot_ASSR`
   - screens: Goods Issue Note -> Goods Issue Note CM Selection -> Goods Issue Note Detail
   - detail: flows/00890001.md ; trace prefix `14:17:00890001`
7. **seq 18 - Goods Issue Note** (`00050001`) - area: GIN (Goods Issue Note)
   - actor: same session (Auto_Tssm)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`, `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue Note -> Goods Issue Note CM Selection -> Goods Issue Note Detail -> Goods Issue Note Forward
   - detail: flows/00050001.md ; trace prefix `14:18:00050001`
8. **seq 21 - Goods Issue Note Approval** (`00780001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 18 (00050001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue Note Approval
   - detail: flows/00780001.md ; trace prefix `14:21:00780001`

## Inactive rows (skipped by the engine)
- seq 3 Dispatch Advice Negative (`00100002`) status N
- seq 6 Dispatch Advice Loss Approval Request (`00750001`) status N
- seq 19 Goods Issue Note Terminat Approval (`00780003`) status N
- seq 20 Goods Issue N Rejection Approval (`00780002`) status N
