# Group 61 - Daily Cycle Only Positive Flow_BD

Source `gtf:61`. Market guess (from name): PK(none in name). Rows: 51 (active 33, inactive 18). User switch points: 14 (5, 7, 8, 23, 24, 31, 37, 38, 46, 47, 48, 52, 53, 54).

Allowed apps (alg): app 7 BD_Centegy QA -> D:/Selenium/Automation/BD_QA// (workbook variant inferred: Bangla)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `61:1:021400000`
2. **seq 2 - Dispatch Advice II** (`00980001`) - area: Dispatch Advice
   - actor: same session (runner default login)
   - consumes: `REPO_DOCUMENTNO` produced within same flow
   - produces: `REPO_DOCUMENTNO`
   - checks: 6 message/field assertion(s); group assertion sheet(s): `DA_FORWARD_ASSR`; value validations 1, Q2Q 0
   - screens: Dispatch Advice II -> Dispatch Advice II -> Dispatch Advice II Detail2 -> Dispatch Advice II Detail -> DA Amount Val R1 BD -> Dispatch Advice II Grid ...
   - detail: flows/00980001.md ; trace prefix `61:2:00980001`
3. **seq 5 - Dispatch Advice II Approval** (`00990001`) - area: Dispatch Advice, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_DOCUMENTNO` from seq 2 (00980001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DA_APPROVALFRWD_ASSR`
   - screens: Dispatch Advice II Approval
   - detail: flows/00990001.md ; trace prefix `61:5:00990001`
4. **seq 7 - Stock Validation After DA** (`02700001`) - area: Dispatch Advice, Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_DA -> Stock_Val_after_DA2 -> Stock_Val_after_DA3
   - detail: flows/02700001.md ; trace prefix `61:7:02700001`
5. **seq 8 - Order Booking_BD** (`01050001`) - area: Order Booking
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Order Booking_BD -> Order Booking Detail_BD -> Order Booking Detail2_BD
   - detail: flows/01050001.md ; trace prefix `61:8:01050001`
6. **seq 9 - Stock Allocation_BD** (`01060001`) - area: Stock Allocation
   - actor: same session (Auto_Multi_Orga)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_Allocation_ASSR`
   - screens: Stock Allocation_BD
   - detail: flows/01060001.md ; trace prefix `61:9:01060001`
7. **seq 10 - Order Editing_BD** (`01070001`) - area: Order Editing
   - actor: same session (Auto_Multi_Orga)
   - produces: `ORDERNUMBEREDIT`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_VALD_ASSR`, `Order_Editing_Detail_BD_ASSR`; value validations 1, Q2Q 0
   - screens: Order Editing_BD -> Order Editing Detail_BD -> Order Editing Detail2_BD
   - detail: flows/01070001.md ; trace prefix `61:10:01070001`
8. **seq 11 - Order Cancellation** (`01080001`) - area: Order Cancellation
   - actor: same session (Auto_Multi_Orga)
   - checks: 1 message/field assertion(s)
   - screens: Order Cancellation_BD -> Order Cancellation Detail_BD
   - detail: flows/01080001.md ; trace prefix `61:11:01080001`
9. **seq 18 - Stock Unallocation_BD** (`01090001`) - area: Stock Allocation
   - actor: same session (Auto_Multi_Orga)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Unallocated_ASSR`
   - screens: Stock Unallocation_BD
   - detail: flows/01090001.md ; trace prefix `61:18:01090001`
10. **seq 19 - Delivery Date Change_BD** (`01100001`) - area: Delivery Date Change
   - actor: same session (Auto_Multi_Orga)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery Date Change_BD
   - detail: flows/01100001.md ; trace prefix `61:19:01100001`
11. **seq 20 - Goods Issue Note** (`00050001`) - area: GIN (Goods Issue Note)
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`, `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue Note -> Goods Issue Note CM Selection -> Goods Issue Note Detail -> Goods Issue Note Forward
   - detail: flows/00050001.md ; trace prefix `61:20:00050001`
12. **seq 23 - Goods Issue Note Approval** (`00780001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue Note Approval
   - detail: flows/00780001.md ; trace prefix `61:23:00780001`
13. **seq 24 - Stock Validation After GIN** (`02710001`) - area: GIN (Goods Issue Note), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_GIN -> Stock_Val_after_GIN2 -> Stock_Val_after_GIN3
   - detail: flows/02710001.md ; trace prefix `61:24:02710001`
14. **seq 31 - FRESH_SALES_RETURN Partial** (`01020001`) - area: Sales Return
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `FRESH_SALES_RETURN_ASSR`, `FRESH_SAL_RETVal_Partial_ASSR`, `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Valid_ASSR`; value validations 1, Q2Q 0
   - screens: FRESH_SALES_RETURN -> FRESH_SALES_RETURN DTL Partial -> FRESH_SALES_RETURN Val Partial
   - detail: flows/01020001.md ; trace prefix `61:31:01020001`
15. **seq 32 - FRESH_SALES_RETURN Full** (`01020002`) - area: Sales Return
   - actor: same session (Auto_Multi_Orga)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `FRESH_SALES_RETURN_Full_ASSR`, `FRESH_SAL_RETURN_Val_Full_ASSR`; value validations 1, Q2Q 0
   - screens: FRESH_SALES_RETURN_Full -> FRESH_SALES_RETURN DTL_Full -> FRESH_SALES_RETURN Val_Full
   - detail: flows/01020002.md ; trace prefix `61:32:01020002`
16. **seq 33 - Cashmemo Status** (`00030001`) - area: Cashmemo
   - actor: same session (Auto_Multi_Orga)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Cashmemo Status
   - detail: flows/00030001.md ; trace prefix `61:33:00030001`
17. **seq 34 - Sales Return** (`00070001`) - area: Sales Return
   - actor: same session (Auto_Multi_Orga)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Valid_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return -> Sales Return Detail -> Sales Return Validation
   - detail: flows/00070001.md ; trace prefix `61:34:00070001`
18. **seq 36 - Sales Return View** (`00700001`) - area: Sales Return
   - actor: same session (Auto_Multi_Orga)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetrunView_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View -> Sales Return View,Detail_Val
   - detail: flows/00700001.md ; trace prefix `61:36:00700001`
19. **seq 37 - Sales Return View Approval** (`00730001`) - area: Sales Return, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetrunViewApprval_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View Approval
   - detail: flows/00730001.md ; trace prefix `61:37:00730001`
20. **seq 38 - Sales Return Status Change** (`00710001`) - area: Sales Return
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SR_StatsChang_DTL_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return Status Change -> Sales Return Status Change Det -> Sales R Status Change_Valida
   - detail: flows/00710001.md ; trace prefix `61:38:00710001`
21. **seq 39 - Deposit Slip Multi Cheques** (`00140001`) - area: Deposit Slip
   - actor: same session (Auto_Multi_Orga)
   - produces: `REPO_Deposit_Slip`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`, `Deposit_Slip_Outlet_ASSR`, `screenshot_ASSR`
   - screens: Deposit Slip -> Deposit Slip,Outlet
   - detail: flows/00140001.md ; trace prefix `61:39:00140001`
22. **seq 41 - Deposit Slip Cheque** (`00140004`) - area: Deposit Slip
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip -> Deposit Slip,Cash memos
   - detail: flows/00140004.md ; trace prefix `61:41:00140004`
23. **seq 43 - Deposit Slip Cash** (`00140005`) - area: Deposit Slip
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip,Cash -> Deposit Slip,Cash memos,Cash
   - detail: flows/00140005.md ; trace prefix `61:43:00140005`
24. **seq 45 - Good Return Note** (`00090001`) - area: GRN (Goods Return Note)
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GRN No.` unresolved in group
   - produces: `REPO_GRNNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GRN_DTL_SAVE_ASSR`, `GRN_FORWARD_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Return Note -> Good Return Note Detail -> Good Return Note Detail_Valida -> Goods Return Note Forward
   - detail: flows/00090001.md ; trace prefix `61:45:00090001`
25. **seq 46 - Good Return Note Approval** (`00810001`) - area: GRN (Goods Return Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_GRNNO` from seq 45 (00090001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GRN_APPROVAL_ASSR`
   - screens: Good Return Note Approval
   - detail: flows/00810001.md ; trace prefix `61:46:00810001`
26. **seq 47 - Stock Validation After GRN** (`02730001`) - area: GRN (Goods Return Note), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_GRN -> Stock_Val_after_GRN2 -> Stock_Val_after_GRN3
   - detail: flows/02730001.md ; trace prefix `61:47:02730001`
27. **seq 48 - Route Settlement** (`00680001`) - area: Route Settlement
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 5 message/field assertion(s); value validations 5, Q2Q 0
   - screens: Route Settlement -> Route Settlement Validation -> Route Settlement Validation1 -> Route Settlement Validation2 -> Route Settlement Validation3 -> Route Settlement Validation4
   - detail: flows/00680001.md ; trace prefix `61:48:00680001`
28. **seq 49 - Cheque Status** (`00660001`) - area: Cheque
   - actor: same session (Auto_Multi_Orga)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Cheque_Status_ASSR`
   - screens: Cheque Status
   - detail: flows/00660001.md ; trace prefix `61:49:00660001`
29. **seq 50 - DSR Adjustment Amount** (`00670001`) - area: DSR/PJP/Route
   - actor: same session (Auto_Multi_Orga)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DSR_ADJ_AMOUNT_ASSR`; value validations 1, Q2Q 0
   - screens: DSR Adjustment Amount -> DSR Adjustment Amount,Detail
   - detail: flows/00670001.md ; trace prefix `61:50:00670001`
30. **seq 51 - PJP Daily Inquiry Update** (`00930001`) - area: DSR/PJP/Route
   - actor: same session (Auto_Multi_Orga)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `PJP_Inquiry_ASSR`
   - screens: PJP Daily -> PJP Daily2
   - detail: flows/00930001.md ; trace prefix `61:51:00930001`
31. **seq 52 - OTC Stock Out R1** (`02950001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: OTC Stock Out R1 -> OTC Stock Out Det R1 -> OTC Stock Out Fwd R1
   - detail: flows/02950001.md ; trace prefix `61:52:02950001`
32. **seq 53 - SAN Approval BD** (`02940001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_DocumentNo` from seq 52 (02950001); `REPO_DocumentType` from seq 52 (02950001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP BD
   - detail: flows/02940001.md ; trace prefix `61:53:02940001`
33. **seq 54 - Opening & Closing Stock Validation** (`02830001`) - area: Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Open_Close_Stock_Val -> Open_Close_Stock_Val2 -> Open_Close_Stock_Val3
   - detail: flows/02830001.md ; trace prefix `61:54:02830001`

## Inactive rows (skipped by the engine)
- seq 3 Dispatch Advice Negative (`00100002`) status N
- seq 4 Dispatch Advice Rejection (`00740002`) status N
- seq 6 Dispatch Advice Loss App_BD (`00770001`) status N
- seq 21 Goods Issue Note Terminat Approval (`00780003`) status N
- seq 22 Goods Issue N Rejection Approval (`00780002`) status N
- seq 25 Stock Allocation (`00130001`) status N
- seq 27 Order Editing After GIN (`00840001`) status N
- seq 28 Order Cancellation After GIN (`00850001`) status N
- seq 29 Cashmemo Reschedule (`01040001`) status N
- seq 40 Deposit Slip Approval (`00140002`) status N
- seq 42 Deposit Slip Approval (`00140002`) status N
- seq 44 Deposit Slip Approval (`00140002`) status N
- seq 55 SAN (Admin) BD (`02930001`) status N
- seq 56 SAN Approval BD (`02940001`) status N
- seq 57 Stock Validation after SAN (Admin) (`02850001`) status N
- seq 58 SAN (Warehouse to Warehouse) (`00120001`) status N
- seq 59 SAN Approval BD (`02940001`) status N
- seq 60 Stock Validation After SAN (W to W) (`02860001`) status N
