# Group 11 - Daily Cycle Only Positive Flow

Source `gtf:11`. Market guess (from name): PK(none in name). Rows: 61 (active 46, inactive 15). User switch points: 10 (5, 9, 23, 24, 37, 38, 49, 50, 59, 60).

Allowed apps (alg): app 5 PK_Centegy QA -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak); app 8 PK_Centegy QA 2 -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `11:1:021400000`
2. **seq 2 - Dispatch Advice** (`00100001`) - area: Dispatch Advice
   - actor: same session (runner default login)
   - consumes: `REPO_DOCUMENTNO` produced within same flow
   - produces: `REPO_DOCUMENTNO`
   - checks: 7 message/field assertion(s); group assertion sheet(s): `DA_FORWARD_ASSR`; value validations 1, Q2Q 0
   - screens: Dispatch Advice -> Dispatch Advice -> Dispatch Advice Detail2 -> Dispatch Advice Detail -> DA Amount Val R1 PAK -> Dispatch Advice Grid ...
   - detail: flows/00100001.md ; trace prefix `11:2:00100001`
3. **seq 5 - Dispatch Advice Approval** (`00740001`) - area: Dispatch Advice, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_DOCUMENTNO` from seq 2 (00100001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DA_APPROVALFRWD_ASSR`
   - screens: Dispatch Advice Approval
   - detail: flows/00740001.md ; trace prefix `11:5:00740001`
4. **seq 7 - Dispatch Advice Loss Approval** (`00760001`) - area: Dispatch Advice, Approval/Reject/Terminate
   - actor: same session (Auto_Tssm)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DA_LOSS_APPROVALFRWD_ASSR`
   - screens: Dispatch Advice Loss Approval
   - detail: flows/00760001.md ; trace prefix `11:7:00760001`
5. **seq 9 - Stock Validation After DA PAK** (`02800001`) - area: Dispatch Advice, Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_After_DA_PAK -> Stock_Val_After_DA_PAK2 -> Stock_Val_After_DA_PAK3
   - detail: flows/02800001.md ; trace prefix `11:9:02800001`
6. **seq 10 - Order Booking** (`00010001`) - area: Order Booking
   - actor: same session (Auto_Multi_Orga)
   - consumes: `g_REPO_ORGA` unresolved in group; `g_REPO_CMDOCTYPE` unresolved in group; `ORDERNUMBER` produced within same flow; `REPO_REF_ORDER_NO` unresolved in group; `g_REPO_DISTRIBUTOR` unresolved in group
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Order Booking -> Order Booking Detail -> Order Booking Detail2
   - detail: flows/00010001.md ; trace prefix `11:10:00010001`
7. **seq 12 - Stock Allocation** (`00130001`) - area: Stock Allocation
   - actor: same session (Auto_Multi_Orga)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_Allocation_ASSR`
   - screens: Stock Allocation
   - detail: flows/00130001.md ; trace prefix `11:12:00130001`
8. **seq 14 - Transaction Inquiry Validate after OB** (`02960001`) - area: Order Booking, Transaction Inquiry
   - actor: same session (Auto_Multi_Orga)
   - checks: 4 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 4, Q2Q 0
   - screens: T Inquiry val after OB -> T Inquiry Header Amt Val -> T Inquiry Detail Amt Val -> Total Offering Amt Val -> T Inquiry Charges Amt Val
   - detail: flows/02960001.md ; trace prefix `11:14:02960001`
9. **seq 15 - Order Editing** (`00020001`) - area: Order Editing
   - actor: same session (Auto_Multi_Orga)
   - consumes: `g_REPO_ORGA` unresolved in group; `g_REPO_CMDOCTYPE` unresolved in group; `ORDERNUMBEREDIT` produced within same flow; `REPO_REF_ORDER_EDITNO` unresolved in group; `g_REPO_DISTRIBUTOR` unresolved in group; `ORDERNUMBER` from seq 10 (00010001)
   - produces: `ORDERNUMBEREDIT`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`, `screenshot_ASSR`; value validations 2, Q2Q 0
   - screens: Order Editing -> Order Editing Detail -> Order Editing Detail3
   - detail: flows/00020001.md ; trace prefix `11:15:00020001`
10. **seq 16 - Order Cancellation R2 TH** (`00040001`) - area: Order Cancellation
   - actor: same session (Auto_Multi_Orga)
   - checks: 2 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Order Cancellation -> Order Cancellation Detail -> Order Cancellation Detail_Val
   - detail: flows/00040001.md ; trace prefix `11:16:00040001`
11. **seq 18 - Stock Unallocation** (`00130002`) - area: Stock Allocation
   - actor: same session (Auto_Multi_Orga)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Unallocated_ASSR`
   - screens: Stock Unallocation
   - detail: flows/00130002.md ; trace prefix `11:18:00130002`
12. **seq 19 - Delivery Date Change** (`00160001`) - area: Delivery Date Change
   - actor: same session (Auto_Multi_Orga)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery Date Change
   - detail: flows/00160001.md ; trace prefix `11:19:00160001`
13. **seq 20 - Goods Issue Note** (`00050001`) - area: GIN (Goods Issue Note)
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`, `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue Note -> Goods Issue Note CM Selection -> Goods Issue Note Detail -> Goods Issue Note Forward
   - detail: flows/00050001.md ; trace prefix `11:20:00050001`
14. **seq 23 - Goods Issue Note Approval** (`00780001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue Note Approval
   - detail: flows/00780001.md ; trace prefix `11:23:00780001`
15. **seq 24 - Stock validation after GIN PAK** (`02810001`) - area: GIN (Goods Issue Note), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_val_after_GIN_PAK1 -> Stock_Val_after_GIN_PAK2 -> Stock_Val_after_GIN_PAK3
   - detail: flows/02810001.md ; trace prefix `11:24:02810001`
16. **seq 29 - Order Editing After GIN** (`00840001`) - area: Order Editing, GIN (Goods Issue Note)
   - actor: same session (Auto_Multi_Orga)
   - consumes: `g_REPO_ORGA` unresolved in group; `g_REPO_CMDOCTYPE` unresolved in group; `ORDERNUMBEREDIT` produced within same flow; `REPO_REF_ORDER_EDITNO` unresolved in group; `g_REPO_DISTRIBUTOR` unresolved in group; `ORDERNUMBER` from seq 10 (00010001)
   - produces: `ORDERNUMBEREDIT`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`, `screenshot_ASSR`; value validations 2, Q2Q 0
   - screens: Order Editing -> Order Editing Detail -> Order Editing Detail3
   - detail: flows/00840001.md ; trace prefix `11:29:00840001`
17. **seq 31 - Order Cancellation After GIN** (`00850001`) - area: Order Cancellation, GIN (Goods Issue Note)
   - actor: same session (Auto_Multi_Orga)
   - checks: 2 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Order Cancellation -> Order Cancellation Detail -> Order Cancellation Detail_Val
   - detail: flows/00850001.md ; trace prefix `11:31:00850001`
18. **seq 32 - Cashmemo Reschedule** (`01040001`) - area: Cashmemo
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `Reschedule_ASSR`; value validations 1, Q2Q 0
   - screens: Cashmemo Reschedule -> Cashmemo Reschedule Det -> Cashmemo Reschedule Val
   - detail: flows/01040001.md ; trace prefix `11:32:01040001`
19. **seq 33 - Cashmemo Status** (`00030001`) - area: Cashmemo
   - actor: same session (Auto_Multi_Orga)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Cashmemo Status
   - detail: flows/00030001.md ; trace prefix `11:33:00030001`
20. **seq 34 - Sales Return** (`00070001`) - area: Sales Return
   - actor: same session (Auto_Multi_Orga)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Valid_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return -> Sales Return Detail -> Sales Return Validation
   - detail: flows/00070001.md ; trace prefix `11:34:00070001`
21. **seq 36 - Sales Return View** (`00700001`) - area: Sales Return
   - actor: same session (Auto_Multi_Orga)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetrunView_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View -> Sales Return View,Detail_Val
   - detail: flows/00700001.md ; trace prefix `11:36:00700001`
22. **seq 37 - Sales Return View Approval** (`00730001`) - area: Sales Return, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetrunViewApprval_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View Approval
   - detail: flows/00730001.md ; trace prefix `11:37:00730001`
23. **seq 38 - Sales Return Status Change** (`00710001`) - area: Sales Return
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SR_StatsChang_DTL_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return Status Change -> Sales Return Status Change Det -> Sales R Status Change_Valida
   - detail: flows/00710001.md ; trace prefix `11:38:00710001`
24. **seq 39 - Deposit Slip Full Amount Cash** (`03230001`) - area: Deposit Slip
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip Full Cash -> Deposit Slip,Cmemos Full Cash
   - detail: flows/03230001.md ; trace prefix `11:39:03230001`
25. **seq 40 - Deposit Slip Full Amount Cheque** (`03240001`) - area: Deposit Slip
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip FullAmount Cheque -> Depo Slip,Cash m F Amount Che
   - detail: flows/03240001.md ; trace prefix `11:40:03240001`
26. **seq 41 - Deposit Slip Unposted Amount Validate** (`03260001`) - area: Deposit Slip, Transaction Inquiry
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Deposit Slip Unposted -> Deposit Slip,Cash memos unPost -> Deposit slip Val Unposted
   - detail: flows/03260001.md ; trace prefix `11:41:03260001`
27. **seq 42 - Deposit Slip Multi Cheques** (`00140001`) - area: Deposit Slip
   - actor: same session (Auto_Multi_Orga)
   - produces: `REPO_Deposit_Slip`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`, `Deposit_Slip_Outlet_ASSR`, `screenshot_ASSR`
   - screens: Deposit Slip -> Deposit Slip,Outlet
   - detail: flows/00140001.md ; trace prefix `11:42:00140001`
28. **seq 44 - Deposit Slip Cheque** (`00140004`) - area: Deposit Slip
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip -> Deposit Slip,Cash memos
   - detail: flows/00140004.md ; trace prefix `11:44:00140004`
29. **seq 46 - Deposit Slip Cash** (`00140005`) - area: Deposit Slip
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip,Cash -> Deposit Slip,Cash memos,Cash
   - detail: flows/00140005.md ; trace prefix `11:46:00140005`
30. **seq 48 - Good Return Note** (`00090001`) - area: GRN (Goods Return Note)
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GRN No.` unresolved in group
   - produces: `REPO_GRNNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GRN_DTL_SAVE_ASSR`, `GRN_FORWARD_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Return Note -> Good Return Note Detail -> Good Return Note Detail_Valida -> Goods Return Note Forward
   - detail: flows/00090001.md ; trace prefix `11:48:00090001`
31. **seq 49 - Good Return Note Approval** (`00810001`) - area: GRN (Goods Return Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_GRNNO` from seq 48 (00090001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GRN_APPROVAL_ASSR`
   - screens: Good Return Note Approval
   - detail: flows/00810001.md ; trace prefix `11:49:00810001`
32. **seq 50 - Stock validation after GRN PAK** (`02820001`) - area: GRN (Goods Return Note), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_GRN_PAK1 -> Stock_Val_after_GRN_PAK2 -> Stock_Val_after_GRN_PAK3
   - detail: flows/02820001.md ; trace prefix `11:50:02820001`
33. **seq 51 - Route Settlement** (`00680001`) - area: Route Settlement
   - actor: same session (Auto_Multi_Orga)
   - checks: 5 message/field assertion(s); value validations 5, Q2Q 0
   - screens: Route Settlement -> Route Settlement Validation -> Route Settlement Validation1 -> Route Settlement Validation2 -> Route Settlement Validation3 -> Route Settlement Validation4
   - detail: flows/00680001.md ; trace prefix `11:51:00680001`
34. **seq 52 - OFFSET Amount Validate After Route Settlement** (`03210001`) - area: Route Settlement, Transaction Inquiry
   - actor: same session (Auto_Multi_Orga)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: T Inquiry Search outlet -> Validate Offset amount
   - detail: flows/03210001.md ; trace prefix `11:52:03210001`
35. **seq 53 - Deposit Slip After Route Settlement** (`03220001`) - area: Deposit Slip, Route Settlement
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Deposit S After R Settlement -> D Slip,Cash m After R Settle
   - detail: flows/03220001.md ; trace prefix `11:53:03220001`
36. **seq 54 - Deposit Slip Cash removal** (`03250001`) - area: Deposit Slip
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_GINNO` from seq 20 (00050001)
   - checks: none configured
   - screens: Deposit slip after order removal -> Dslip cash after order removal -> Dslip chequ after order removal
   - detail: flows/03250001.md ; trace prefix `11:54:03250001`
37. **seq 55 - Cheque Status** (`00660001`) - area: Cheque
   - actor: same session (Auto_Multi_Orga)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Cheque_Status_ASSR`
   - screens: Cheque Status
   - detail: flows/00660001.md ; trace prefix `11:55:00660001`
38. **seq 56 - DSR Adjustment Amount** (`00670001`) - area: DSR/PJP/Route
   - actor: same session (Auto_Multi_Orga)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DSR_ADJ_AMOUNT_ASSR`; value validations 1, Q2Q 0
   - screens: DSR Adjustment Amount -> DSR Adjustment Amount,Detail
   - detail: flows/00670001.md ; trace prefix `11:56:00670001`
39. **seq 57 - PJP Daily Inquiry Update** (`00930001`) - area: DSR/PJP/Route
   - actor: same session (Auto_Multi_Orga)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `PJP_Inquiry_ASSR`
   - screens: PJP Daily -> PJP Daily2
   - detail: flows/00930001.md ; trace prefix `11:57:00930001`
40. **seq 58 - OTC Stock Out R1** (`02950001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: OTC Stock Out R1 -> OTC Stock Out Det R1 -> OTC Stock Out Fwd R1
   - detail: flows/02950001.md ; trace prefix `11:58:02950001`
41. **seq 59 - SAN Approval PAK** (`03500001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_DocumentNo` from seq 58 (02950001); `REPO_DocumentType` from seq 58 (02950001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN Approval PAK
   - detail: flows/03500001.md ; trace prefix `11:59:03500001`
42. **seq 60 - Opening & Closing Stock Validation** (`02830001`) - area: Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Open_Close_Stock_Val -> Open_Close_Stock_Val2 -> Open_Close_Stock_Val3
   - detail: flows/02830001.md ; trace prefix `11:60:02830001`
43. **seq 68 - Validate Edited Order Charges Tax In Transaction Inquiry** (`03190001`) - area: Transaction Inquiry, Charges/Tax
   - actor: same session (Auto_Multi_Orga)
   - checks: 2 message/field assertion(s); value validations 2, Q2Q 0
   - screens: Order Editing After Charges -> T Inquiry Total Tax Amt Val2 -> T Inquiry Header Tax Amt Val2
   - detail: flows/03190001.md ; trace prefix `11:68:03190001`
44. **seq 69 - Validate Charges Tax After Sales Return In Transaction Inquiry** (`03200001`) - area: Sales Return, Transaction Inquiry, Charges/Tax
   - actor: same session (Auto_Multi_Orga)
   - checks: 2 message/field assertion(s); value validations 2, Q2Q 0
   - screens: Sales Return Charges -> Sales Return Header Tax -> Sales Return Total Tax
   - detail: flows/03200001.md ; trace prefix `11:69:03200001`
45. **seq 70 - Transaction Inquiry Validations After Order Editing** (`03740001`) - area: Order Editing, Transaction Inquiry
   - actor: same session (Auto_Multi_Orga)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 3, Q2Q 0
   - screens: T Inquiry val after OE -> T Inquiry Header Amt Val OE -> T Inquiry Detail Amt Val OE -> Total Offering Amt Val OE
   - detail: flows/03740001.md ; trace prefix `11:70:03740001`
46. **seq 71 - Transaction Inquiry Validate After Sales Return** (`03770001`) - area: Sales Return, Transaction Inquiry
   - actor: same session (Auto_Multi_Orga)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 3, Q2Q 0
   - screens: T Inquiry val after SR -> T Inquiry Header Amt Val SR -> T Inquiry Detail Amt Val SR -> Total Offering Amt Val SR
   - detail: flows/03770001.md ; trace prefix `11:71:03770001`

## Inactive rows (skipped by the engine)
- seq 3 Dispatch Advice Negative (`00100002`) status N
- seq 4 Dispatch Advice Rejection (`00740002`) status N
- seq 6 Dispatch Advice Loss Approval Request (`00750001`) status N
- seq 21 Goods Issue Note Terminat Approval (`00780003`) status N
- seq 22 Goods Issue N Rejection Approval (`00780002`) status N
- seq 25 Stock Allocation (`00130001`) status N
- seq 43 Deposit Slip Approval (`00140002`) status N
- seq 45 Deposit Slip Approval (`00140002`) status N
- seq 47 Deposit Slip Approval (`00140002`) status N
- seq 61 SAN (Admin) (`02840001`) status N
- seq 62 SAN Approval PAK (`03500001`) status N
- seq 63 Stock Validation after SAN (Admin) (`02850001`) status N
- seq 64 SAN (Warehouse to Warehouse) (`00120001`) status N
- seq 65 SAN Approval PAK (`03500001`) status N
- seq 66 Stock Validation After SAN (W to W) (`02860001`) status N
