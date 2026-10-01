# Group 1 - Daily Cycle Negative with Positive Flow

Source `gtf:1`. Market guess (from name): PK(none in name). Rows: 45 (active 36, inactive 9). User switch points: 8 (5, 8, 21, 23, 33, 34, 43, 44).

Allowed apps (alg): app 5 PK_Centegy QA -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak); app 8 PK_Centegy QA 2 -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak)
Starts with an app login flow: False (first active flow 00830001).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Dispatch Advice Forward Negative** (`00830001`) - area: Dispatch Advice, Negative test
   - actor: same session (runner default login)
   - consumes: `REPO_DOCUMENTNO` produced within same flow
   - produces: `REPO_DOCUMENTNO`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `DA_FORWARD_ASSR`
   - screens: Dispatch Advice -> Dispatch Advice -> Dispatch Advice Grid
   - detail: flows/00830001.md ; trace prefix `1:1:00830001`
2. **seq 3 - Dispatch Advice Negative** (`00100002`) - area: Dispatch Advice, Negative test
   - actor: same session (runner default login)
   - consumes: `REPO_DOCUMENTNO` produced within same flow
   - produces: `REPO_DOCUMENTNO`
   - checks: 6 message/field assertion(s); group assertion sheet(s): `DA_Delete_Negative_ASSR`, `DA_FORWARD_ASSR`
   - screens: Dispatch Advice -> Dispatch Advice -> Dispatch Advice Detail2 -> DA Delete Negative -> Dispatch Advice Detail -> Dispatch Advice Grid ...
   - detail: flows/00100002.md ; trace prefix `1:3:00100002`
3. **seq 5 - Dispatch Advice Approval** (`00740001`) - area: Dispatch Advice, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_DOCUMENTNO` from seq 3 (00100002)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DA_APPROVALFRWD_ASSR`
   - screens: Dispatch Advice Approval
   - detail: flows/00740001.md ; trace prefix `1:5:00740001`
4. **seq 7 - Dispatch Advice Loss Approval** (`00760001`) - area: Dispatch Advice, Approval/Reject/Terminate
   - actor: same session (Auto_Tssm)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DA_LOSS_APPROVALFRWD_ASSR`
   - screens: Dispatch Advice Loss Approval
   - detail: flows/00760001.md ; trace prefix `1:7:00760001`
5. **seq 8 - Order Booking Negative** (`00860001`) - area: Order Booking, Negative test
   - **SWITCH USER POINT**: log out and log in as **AppUser** (serial 4)
   - checks: 1 message/field assertion(s); value validations 2, Q2Q 0
   - screens: Order Booking -> Order Booking Detail
   - detail: flows/00860001.md ; trace prefix `1:8:00860001`
6. **seq 9 - Order Booking** (`00010001`) - area: Order Booking
   - actor: same session (AppUser)
   - consumes: `g_REPO_ORGA` unresolved in group; `g_REPO_CMDOCTYPE` unresolved in group; `ORDERNUMBER` produced within same flow; `REPO_REF_ORDER_NO` unresolved in group; `g_REPO_DISTRIBUTOR` unresolved in group
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Order Booking -> Order Booking Detail -> Order Booking Detail2
   - detail: flows/00010001.md ; trace prefix `1:9:00010001`
7. **seq 10 - Stock Allocation** (`00130001`) - area: Stock Allocation
   - actor: same session (AppUser)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_Allocation_ASSR`
   - screens: Stock Allocation
   - detail: flows/00130001.md ; trace prefix `1:10:00130001`
8. **seq 11 - Order Editing Negative** (`00870001`) - area: Order Editing, Negative test
   - actor: same session (AppUser)
   - consumes: `g_REPO_ORGA` unresolved in group; `g_REPO_CMDOCTYPE` unresolved in group; `ORDERNUMBEREDIT` produced within same flow; `REPO_REF_ORDER_EDITNO` unresolved in group; `g_REPO_DISTRIBUTOR` unresolved in group; `ORDERNUMBER` from seq 9 (00010001)
   - produces: `ORDERNUMBEREDIT`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`, `screenshot_ASSR`; value validations 2, Q2Q 0
   - screens: Order Editing -> Order Editing Detail -> Order Editing Detail3
   - detail: flows/00870001.md ; trace prefix `1:11:00870001`
9. **seq 12 - Order Editing** (`00020001`) - area: Order Editing
   - actor: same session (AppUser)
   - consumes: `g_REPO_ORGA` unresolved in group; `g_REPO_CMDOCTYPE` unresolved in group; `ORDERNUMBEREDIT` produced within same flow; `REPO_REF_ORDER_EDITNO` unresolved in group; `g_REPO_DISTRIBUTOR` unresolved in group; `ORDERNUMBER` from seq 9 (00010001)
   - produces: `ORDERNUMBEREDIT`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`, `screenshot_ASSR`; value validations 2, Q2Q 0
   - screens: Order Editing -> Order Editing Detail -> Order Editing Detail3
   - detail: flows/00020001.md ; trace prefix `1:12:00020001`
10. **seq 13 - Order Cancellation Negative** (`00880001`) - area: Order Cancellation, Negative test
   - actor: same session (AppUser)
   - checks: none configured
   - screens: Order Cancellation -> Order Cancellation Detail
   - detail: flows/00880001.md ; trace prefix `1:13:00880001`
11. **seq 14 - Order Cancellation R2 TH** (`00040001`) - area: Order Cancellation
   - actor: same session (AppUser)
   - checks: 2 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Order Cancellation -> Order Cancellation Detail -> Order Cancellation Detail_Val
   - detail: flows/00040001.md ; trace prefix `1:14:00040001`
12. **seq 15 - Stock Unallocation** (`00130002`) - area: Stock Allocation
   - actor: same session (AppUser)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Unallocated_ASSR`
   - screens: Stock Unallocation
   - detail: flows/00130002.md ; trace prefix `1:15:00130002`
13. **seq 16 - Delivery Date Change** (`00160001`) - area: Delivery Date Change
   - actor: same session (AppUser)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery Date Change
   - detail: flows/00160001.md ; trace prefix `1:16:00160001`
14. **seq 17 - Goods Issue Note Negative** (`00890001`) - area: GIN (Goods Issue Note), Negative test
   - actor: same session (AppUser)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_DTL_SAVE_ASSR`, `screenshot_ASSR`
   - screens: Goods Issue Note -> Goods Issue Note CM Selection -> Goods Issue Note Detail
   - detail: flows/00890001.md ; trace prefix `1:17:00890001`
15. **seq 18 - Goods Issue Note** (`00050001`) - area: GIN (Goods Issue Note)
   - actor: same session (AppUser)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`, `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue Note -> Goods Issue Note CM Selection -> Goods Issue Note Detail -> Goods Issue Note Forward
   - detail: flows/00050001.md ; trace prefix `1:18:00050001`
16. **seq 21 - Goods Issue Note Approval** (`00780001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_GINNO` from seq 18 (00050001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue Note Approval
   - detail: flows/00780001.md ; trace prefix `1:21:00780001`
17. **seq 23 - Order Editing After GIN** (`00840001`) - area: Order Editing, GIN (Goods Issue Note)
   - **SWITCH USER POINT**: log out and log in as **AppUser** (serial 4)
   - consumes: `g_REPO_ORGA` unresolved in group; `g_REPO_CMDOCTYPE` unresolved in group; `ORDERNUMBEREDIT` produced within same flow; `REPO_REF_ORDER_EDITNO` unresolved in group; `g_REPO_DISTRIBUTOR` unresolved in group; `ORDERNUMBER` from seq 9 (00010001)
   - produces: `ORDERNUMBEREDIT`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`, `screenshot_ASSR`; value validations 2, Q2Q 0
   - screens: Order Editing -> Order Editing Detail -> Order Editing Detail3
   - detail: flows/00840001.md ; trace prefix `1:23:00840001`
18. **seq 24 - Order Cancellation After GIN** (`00850001`) - area: Order Cancellation, GIN (Goods Issue Note)
   - actor: same session (AppUser)
   - checks: 2 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Order Cancellation -> Order Cancellation Detail -> Order Cancellation Detail_Val
   - detail: flows/00850001.md ; trace prefix `1:24:00850001`
19. **seq 25 - Cashmemo Reschedule** (`01040001`) - area: Cashmemo
   - actor: same session (AppUser)
   - consumes: `REPO_GINNO` from seq 18 (00050001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `Reschedule_ASSR`; value validations 1, Q2Q 0
   - screens: Cashmemo Reschedule -> Cashmemo Reschedule Det -> Cashmemo Reschedule Val
   - detail: flows/01040001.md ; trace prefix `1:25:01040001`
20. **seq 29 - Cashmemo Status** (`00030001`) - area: Cashmemo
   - actor: same session (AppUser)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Cashmemo Status
   - detail: flows/00030001.md ; trace prefix `1:29:00030001`
21. **seq 30 - Sales Return Negative** (`00900001`) - area: Sales Return, Negative test
   - actor: same session (AppUser)
   - checks: 2 message/field assertion(s); group assertion sheet(s): `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Valid_ASSR`
   - screens: Sales Return -> Sales Return Detail
   - detail: flows/00900001.md ; trace prefix `1:30:00900001`
22. **seq 31 - Sales Return** (`00070001`) - area: Sales Return
   - actor: same session (AppUser)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Valid_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return -> Sales Return Detail -> Sales Return Validation
   - detail: flows/00070001.md ; trace prefix `1:31:00070001`
23. **seq 32 - Sales Return View** (`00700001`) - area: Sales Return
   - actor: same session (AppUser)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetrunView_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View -> Sales Return View,Detail_Val
   - detail: flows/00700001.md ; trace prefix `1:32:00700001`
24. **seq 33 - Sales Return View Approval** (`00730001`) - area: Sales Return, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetrunViewApprval_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View Approval
   - detail: flows/00730001.md ; trace prefix `1:33:00730001`
25. **seq 34 - Sales Return Status Change** (`00710001`) - area: Sales Return
   - **SWITCH USER POINT**: log out and log in as **AppUser** (serial 4)
   - consumes: `REPO_GINNO` from seq 18 (00050001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SR_StatsChang_DTL_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return Status Change -> Sales Return Status Change Det -> Sales R Status Change_Valida
   - detail: flows/00710001.md ; trace prefix `1:34:00710001`
26. **seq 35 - Deposit Slip Negative** (`00140003`) - area: Deposit Slip, Negative test
   - actor: same session (AppUser)
   - produces: `REPO_Deposit_Slip`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`, `Deposit_Slip_Outlet_ASSR`, `screenshot_ASSR`
   - screens: Deposit Slip -> Deposit Slip,Outlet
   - detail: flows/00140003.md ; trace prefix `1:35:00140003`
27. **seq 36 - Deposit Slip Multi Cheques** (`00140001`) - area: Deposit Slip
   - actor: same session (AppUser)
   - produces: `REPO_Deposit_Slip`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`, `Deposit_Slip_Outlet_ASSR`, `screenshot_ASSR`
   - screens: Deposit Slip -> Deposit Slip,Outlet
   - detail: flows/00140001.md ; trace prefix `1:36:00140001`
28. **seq 38 - Deposit Slip Cheque** (`00140004`) - area: Deposit Slip
   - actor: same session (AppUser)
   - consumes: `REPO_GINNO` from seq 18 (00050001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip -> Deposit Slip,Cash memos
   - detail: flows/00140004.md ; trace prefix `1:38:00140004`
29. **seq 40 - Deposit Slip Cash** (`00140005`) - area: Deposit Slip
   - actor: same session (AppUser)
   - consumes: `REPO_GINNO` from seq 18 (00050001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip,Cash -> Deposit Slip,Cash memos,Cash
   - detail: flows/00140005.md ; trace prefix `1:40:00140005`
30. **seq 42 - Good Return Note** (`00090001`) - area: GRN (Goods Return Note)
   - actor: same session (AppUser)
   - consumes: `REPO_GRN No.` unresolved in group
   - produces: `REPO_GRNNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GRN_DTL_SAVE_ASSR`, `GRN_FORWARD_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Return Note -> Good Return Note Detail -> Good Return Note Detail_Valida -> Goods Return Note Forward
   - detail: flows/00090001.md ; trace prefix `1:42:00090001`
31. **seq 43 - Good Return Note Approval** (`00810001`) - area: GRN (Goods Return Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_GRNNO` from seq 42 (00090001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GRN_APPROVAL_ASSR`
   - screens: Good Return Note Approval
   - detail: flows/00810001.md ; trace prefix `1:43:00810001`
32. **seq 44 - Cheque Status** (`00660001`) - area: Cheque
   - **SWITCH USER POINT**: log out and log in as **AppUser** (serial 4)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Cheque_Status_ASSR`
   - screens: Cheque Status
   - detail: flows/00660001.md ; trace prefix `1:44:00660001`
33. **seq 45 - Route Settlement** (`00680001`) - area: Route Settlement
   - actor: same session (AppUser)
   - checks: 5 message/field assertion(s); value validations 5, Q2Q 0
   - screens: Route Settlement -> Route Settlement Validation -> Route Settlement Validation1 -> Route Settlement Validation2 -> Route Settlement Validation3 -> Route Settlement Validation4
   - detail: flows/00680001.md ; trace prefix `1:45:00680001`
34. **seq 46 - DSR Adjustment Amount** (`00670001`) - area: DSR/PJP/Route
   - actor: same session (AppUser)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DSR_ADJ_AMOUNT_ASSR`; value validations 1, Q2Q 0
   - screens: DSR Adjustment Amount -> DSR Adjustment Amount,Detail
   - detail: flows/00670001.md ; trace prefix `1:46:00670001`
35. **seq 47 - PJP Daily Inquiry Update** (`00930001`) - area: DSR/PJP/Route
   - actor: same session (AppUser)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `PJP_Inquiry_ASSR`
   - screens: PJP Daily -> PJP Daily2
   - detail: flows/00930001.md ; trace prefix `1:47:00930001`
36. **seq 48 - Analaysis 4** (`00460001`) - area: Master/Setup
   - actor: same session (AppUser)
   - consumes: `REPO_GINNO` from seq 18 (00050001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_REJECT_ASSR`
   - screens: Good Issue N Reject Appro Promo
   - detail: flows/00460001.md ; trace prefix `1:48:00460001`

## Inactive rows (skipped by the engine)
- seq 2 Dispatch Advice (`00100001`) status N
- seq 4 Dispatch Advice Rejection (`00740002`) status N
- seq 6 Dispatch Advice Loss Approval Request (`00750001`) status N
- seq 19 Goods Issue Note Terminat Approval (`00780003`) status N
- seq 20 Goods Issue N Rejection Approval (`00780002`) status N
- seq 22 Stock Allocation (`00130001`) status N
- seq 37 Deposit Slip Approval (`00140002`) status N
- seq 39 Deposit Slip Approval (`00140002`) status N
- seq 41 Deposit Slip Approval (`00140002`) status N
