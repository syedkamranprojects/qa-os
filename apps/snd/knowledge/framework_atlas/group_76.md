# Group 76 - Daily Cycle Only Positive Flow_KH

Source `gtf:76`. Market guess (from name): PK(none in name). Rows: 65 (active 41, inactive 24). User switch points: 11 (25, 27, 41, 42, 46, 48, 50, 54, 55, 61, 62).

Allowed apps (alg): app 17 KH_Centegy QA -> D:/Selenium/Automation/KH_QA// (workbook variant inferred: None)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 2 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `76:2:021400000`
2. **seq 12 - Order Booking R2 KH** (`04700001`) - area: Order Booking
   - actor: same session (runner default login)
   - checks: none configured
   - screens: 
   - detail: flows/04700001.md ; trace prefix `76:12:04700001`
3. **seq 14 - Promo, Charges Validation After OB R2** (`03280001`) - area: Order Booking, Transaction Inquiry, Promotion, Charges/Tax
   - actor: same session (runner default login)
   - checks: 5 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 6, Q2Q 0
   - screens: Transaction_inquiry_val_R2 -> Trans_inq_header_val_R2 -> Trans_inq_detail_val_R2 -> Trans_inq_totalOffer_val_R2_1 -> Trans_inq_totalOffer_val_R2_2 -> Trans_inq_total_tax_val_R2 ...
   - detail: flows/03280001.md ; trace prefix `76:14:03280001`
4. **seq 15 - Stock Allocation** (`00130001`) - area: Stock Allocation
   - actor: same session (runner default login)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_Allocation_ASSR`
   - screens: Stock Allocation
   - detail: flows/00130001.md ; trace prefix `76:15:00130001`
5. **seq 16 - Order Editing R2 KH** (`04710001`) - area: Order Editing
   - actor: same session (runner default login)
   - produces: `ORDERNUMBEREDIT`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`; value validations 1, Q2Q 0
   - screens: Order Editing_R2 KH -> Order Editing Detail_R2 KH -> Order Editing Detail3_R2 KH
   - detail: flows/04710001.md ; trace prefix `76:16:04710001`
6. **seq 18 - Amounts Validation after Order Editing R2 KH** (`04720001`) - area: Order Editing, Transaction Inquiry
   - actor: same session (runner default login)
   - checks: 6 message/field assertion(s); value validations 6, Q2Q 0
   - screens: Amount_Val_Aft_Order_Edit_R2_KH -> Amt_Val_After_Edit_detail_R2_KH -> Amt_Val_Aft_Edit_tot_off1_R2_KH -> Amt_Val_Aft_Edit_tot_off2_R2_KH -> Amt_Val_Aft_Edit_tot_tax_R2_KH -> Amt_Val_Aft_Edit_add_chrg_R2_KH ...
   - detail: flows/04720001.md ; trace prefix `76:18:04720001`
7. **seq 19 - Order Cancellation R2 KH** (`04730001`) - area: Order Cancellation
   - actor: same session (runner default login)
   - checks: 2 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Order_Cancellation_R2_KH -> Order_Cancellation_Detail_R2_KH -> Order_Cancel_Detail_Val_R2_KH
   - detail: flows/04730001.md ; trace prefix `76:19:04730001`
8. **seq 20 - Stock Unallocation** (`00130002`) - area: Stock Allocation
   - actor: same session (runner default login)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Unallocated_ASSR`
   - screens: Stock Unallocation
   - detail: flows/00130002.md ; trace prefix `76:20:00130002`
9. **seq 21 - Delivery Date Change** (`00160001`) - area: Delivery Date Change
   - actor: same session (runner default login)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery Date Change
   - detail: flows/00160001.md ; trace prefix `76:21:00160001`
10. **seq 22 - Goods Issue Note R2 KH** (`04740001`) - area: GIN (Goods Issue Note)
   - actor: same session (runner default login)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`, `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue Note R2 KH -> GIN CM Selection R2 KH -> GIN Detail R2 KH -> GIN Forward R2 KH
   - detail: flows/04740001.md ; trace prefix `76:22:04740001`
11. **seq 25 - Goods Issue Note Approval R2 KH** (`04750001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm_KH** (serial 40)
   - consumes: `REPO_GINNO` from seq 22 (04740001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue Note App R2 KH
   - detail: flows/04750001.md ; trace prefix `76:25:04750001`
12. **seq 27 - Stock Validation After GIN R2 KH** (`04760001`) - area: GIN (Goods Issue Note), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_KH1** (serial 39)
   - checks: none configured
   - screens: 
   - detail: flows/04760001.md ; trace prefix `76:27:04760001`
13. **seq 29 - Fresh Sales Return Partial R2 KH** (`04770001`) - area: Sales Return
   - actor: same session (Auto_KH1)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `FRESH_SALES_RETURN_ASSR`, `FRESH_SAL_RETVal_Partial_ASSR`, `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Valid_ASSR`; value validations 1, Q2Q 0
   - screens: Fresh_Sales_Ret_Partial_R2_KH -> Fresh_Sales_Ret_P_DTL_R2_KH -> Fresh_Sales_Ret_P_DTL_Val_R2_KH
   - detail: flows/04770001.md ; trace prefix `76:29:04770001`
14. **seq 31 - Amounts Validation after Fresh Sales Return Partial R2 KH** (`04820001`) - area: Sales Return, Transaction Inquiry
   - actor: same session (Auto_KH1)
   - checks: 6 message/field assertion(s); value validations 6, Q2Q 0
   - screens: Amt_Val_P_Fresh_return_R2_KH -> Amt_Val_P_FreshRet_detail_R2_KH -> Amt_Val_P_FreshR_TotOff_1_R2_KH -> Amt_Val_P_FreshR_TotOff_2_R2_KH -> Amt_Val_P_FreshRet_TotTax_R2_KH -> Amt_Val_P_FreshRe_AddChrg_R2_KH ...
   - detail: flows/04820001.md ; trace prefix `76:31:04820001`
15. **seq 32 - Fresh Sales Return Full R2 KH** (`04780001`) - area: Sales Return
   - actor: same session (Auto_KH1)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `FRESH_SALES_RETURN_Full_ASSR`, `FRESH_SAL_RETURN_Val_Full_ASSR`; value validations 1, Q2Q 0
   - screens: Fresh_Sales_Return_Full_R2_KH -> Fresh_Sales_Ret_F_DTL_R2_KH -> Fresh_Sales_Ret_F_DTL_Val_R2_KH
   - detail: flows/04780001.md ; trace prefix `76:32:04780001`
16. **seq 38 - Cashmemo Status R2 KH** (`04830001`) - area: Cashmemo
   - actor: same session (Auto_KH1)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Cashmemo Status R2 KH
   - detail: flows/04830001.md ; trace prefix `76:38:04830001`
17. **seq 39 - Sales Return R2 KH** (`04840001`) - area: Sales Return
   - actor: same session (Auto_KH1)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Valid_ASSR`, `Sales_Return_Val_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return R2 KH -> Sales Return Detail R2 KH -> Sales Return Validation R2 KH
   - detail: flows/04840001.md ; trace prefix `76:39:04840001`
18. **seq 40 - Sales Return View R2 KH** (`04850001`) - area: Sales Return
   - actor: same session (Auto_KH1)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetrunView_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View R2 KH -> Sales Return View Det Val R2 KH
   - detail: flows/04850001.md ; trace prefix `76:40:04850001`
19. **seq 41 - Sales Return View Approval R2 KH** (`04860001`) - area: Sales Return, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm_KH** (serial 40)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetrunViewApprval_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View App R2 KH
   - detail: flows/04860001.md ; trace prefix `76:41:04860001`
20. **seq 42 - Sales Return Status Change R2 KH** (`04870001`) - area: Sales Return
   - **SWITCH USER POINT**: log out and log in as **Auto_KH1** (serial 39)
   - consumes: `REPO_GINNO` from seq 22 (04740001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SR_StatsChang_DTL_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Ret Status Change R2 KH -> Sales Ret Status Change2 R2 KH -> Sales R Status Change Val R2 KH
   - detail: flows/04870001.md ; trace prefix `76:42:04870001`
21. **seq 43 - Amounts Validation after Sales Return R2 KH** (`04880001`) - area: Sales Return, Transaction Inquiry
   - actor: same session (Auto_KH1)
   - checks: 6 message/field assertion(s); value validations 6, Q2Q 0
   - screens: Amount_after_Sale_return_R2_KH -> Amt_after_SaleRet_detail_R2_KH -> Amt_aft_SaleRet_TotOff_1_R2_KH -> Amt_aft_SaleRet_TotOff_2_R2_KH -> Amt_aftr_SaleRet_TotalTax_R2_KH -> Amt_aft_SaleRet_AddCharge_R2_KH ...
   - detail: flows/04880001.md ; trace prefix `76:43:04880001`
22. **seq 44 - Deposit Slip Multi Cheques R2 KH** (`04890001`) - area: Deposit Slip
   - actor: same session (Auto_KH1)
   - produces: `REPO_DeSlip_M_chq`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`, `Deposit_Slip_Outlet_ASSR`, `screenshot_ASSR`
   - screens: Deposit Slip Multi Chq R2 KH -> Deposit Slip Multi Chq1 R2 KH
   - detail: flows/04890001.md ; trace prefix `76:44:04890001`
23. **seq 46 - Deposit Slip Cheque R2 KH** (`04900001`) - area: Deposit Slip
   - **SWITCH USER POINT**: log out and log in as **Auto_KH1** (serial 39) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 22 (04740001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip Chq R2 KH -> Deposit Slip Chq2 R2 KH
   - detail: flows/04900001.md ; trace prefix `76:46:04900001`
24. **seq 48 - Deposit Slip Cash R2 KH** (`04910001`) - area: Deposit Slip
   - **SWITCH USER POINT**: log out and log in as **Auto_KH1** (serial 39) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 22 (04740001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip Cash R2 KH -> Deposit Slip Cash2 R2 KH
   - detail: flows/04910001.md ; trace prefix `76:48:04910001`
25. **seq 50 - Deposit Slip Cash Full R2 KH** (`04920001`) - area: Deposit Slip
   - **SWITCH USER POINT**: log out and log in as **Auto_KH1** (serial 39) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 22 (04740001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit_Slip_Cash_Full_1_R2_KH -> Deposit_Slip_Cash_Full_2_R2_KH
   - detail: flows/04920001.md ; trace prefix `76:50:04920001`
26. **seq 51 - Deposit Slip Cheque Full R2 KH** (`04930001`) - area: Deposit Slip
   - actor: same session (Auto_KH1)
   - consumes: `REPO_GINNO` from seq 22 (04740001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit_Slip_Cheq_Full_1_R2_KH -> Deposit_Slip_Cheq_Full_2_R2_KH
   - detail: flows/04930001.md ; trace prefix `76:51:04930001`
27. **seq 52 - Deposit Slip Un Posted Amount Validation R2** (`03420001`) - area: Deposit Slip, Transaction Inquiry
   - actor: same session (Auto_KH1)
   - consumes: `REPO_GINNO` from seq 22 (04740001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Deposit_Slip_Creation_R2 -> Deposit_Slip_Cashmemo_Save_R2 -> Deposit_Slip_UnPosted_Val_R2
   - detail: flows/03420001.md ; trace prefix `76:52:03420001`
28. **seq 53 - Good Return Note R2 KH** (`04940001`) - area: GRN (Goods Return Note)
   - actor: same session (Auto_KH1)
   - consumes: `REPO_GRN No.` unresolved in group
   - produces: `REPO_GRNNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GRN_DTL_SAVE_ASSR`, `GRN_FORWARD_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Return Note R2 KH -> GRN Detail R2 KH -> GRN Detail Validation R2 KH -> GRN Forward R2 KH
   - detail: flows/04940001.md ; trace prefix `76:53:04940001`
29. **seq 54 - Good Return Note Approval R2 KH** (`04950001`) - area: GRN (Goods Return Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm_KH** (serial 40)
   - consumes: `REPO_GRNNO` from seq 53 (04940001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GRN_APPROVAL_ASSR`
   - screens: Goods Return Note App R2 KH
   - detail: flows/04950001.md ; trace prefix `76:54:04950001`
30. **seq 55 - Stock Validation After GRN R2 KH** (`04960001`) - area: GRN (Goods Return Note), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_KH1** (serial 39)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_GRN_R2_KH -> Stock_Val_after_GRN_2_R2_KH -> Stock_Val_after_GRN_3_R2_KH
   - detail: flows/04960001.md ; trace prefix `76:55:04960001`
31. **seq 56 - Route Settlement R2 KH** (`04970001`) - area: Route Settlement
   - actor: same session (Auto_KH1)
   - checks: 4 message/field assertion(s); value validations 4, Q2Q 0
   - screens: Route Settlement R2 KH -> Route Settlement Val R2 KH -> Route Settlement Val1 R2 KH -> Route Settlement Val2 R2 KH -> Route Settlement Val3 R2 KH
   - detail: flows/04970001.md ; trace prefix `76:56:04970001`
32. **seq 57 - Cheque Status R2 KH** (`04990001`) - area: Cheque
   - actor: same session (Auto_KH1)
   - consumes: `REPO_DeSlip_M_chq` from seq 44 (04890001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Cheque_Status_ASSR`
   - screens: Cheque Status R2 KH
   - detail: flows/04990001.md ; trace prefix `76:57:04990001`
33. **seq 58 - DSR Adjustment Amount R2 KH** (`05000001`) - area: DSR/PJP/Route
   - actor: same session (Auto_KH1)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DSR_ADJ_AMOUNT_ASSR`; value validations 1, Q2Q 0
   - screens: DSR Adjustment Amount R2 KH -> DSR Adjustment Amount,Det R2 KH
   - detail: flows/05000001.md ; trace prefix `76:58:05000001`
34. **seq 59 - PJP Daily Inquiry Update R2 KH** (`05040001`) - area: DSR/PJP/Route
   - actor: same session (Auto_KH1)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `PJP_Inquiry_ASSR`
   - screens: PJP Daily R2 KH -> PJP Daily2 R2 KH
   - detail: flows/05040001.md ; trace prefix `76:59:05040001`
35. **seq 60 - OTC Stock Out R2 KH** (`05050001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - actor: same session (Auto_KH1)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: OTC Stock Out R2 KH -> OTC Stock Out Det R2 KH -> OTC Stock Out Fwd R2 KH
   - detail: flows/05050001.md ; trace prefix `76:60:05050001`
36. **seq 61 - SAN Approval R2 KH** (`05060001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm_KH** (serial 40)
   - consumes: `REPO_DocumentNo` from seq 60 (05050001); `REPO_DocumentType` from seq 60 (05050001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP R2 KH
   - detail: flows/05060001.md ; trace prefix `76:61:05060001`
37. **seq 62 - Opening & Closing Stock Validation R2 KH** (`05070001`) - area: Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_KH1** (serial 39)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Open_Close_Stock_Val_R2_KH -> Open_Close_Stock_Val2_R2_KH -> Open_Close_Stock_Val3_R2_KH
   - detail: flows/05070001.md ; trace prefix `76:62:05070001`
38. **seq 63 - Received Amount Validation Transaction Inquiry R2** (`03290001`) - area: Transaction Inquiry
   - actor: same session (Auto_KH1)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: ReceivedAmt_Val_TransInq_R2_1 -> ReceivedAmt_Val_TransInq_R2_2
   - detail: flows/03290001.md ; trace prefix `76:63:03290001`
39. **seq 64 - Charges Validation Transaction Inquiry R2** (`03310001`) - area: Transaction Inquiry, Charges/Tax
   - actor: same session (Auto_KH1)
   - checks: 2 message/field assertion(s); value validations 2, Q2Q 0
   - screens: Charges_Val_Transaction_Inq_R2 -> Charges_Val_Total_Tax_R2 -> Charges_Val_Header_R2
   - detail: flows/03310001.md ; trace prefix `76:64:03310001`
40. **seq 65 - Deposit Slip Received Amount Validation R2** (`03460001`) - area: Deposit Slip, Transaction Inquiry
   - actor: same session (Auto_KH1)
   - consumes: `REPO_GINNO` from seq 22 (04740001)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: DepSlip_ReceivedAmount_Val_1_R2 -> DepSlip_ReceivedAmount_Val_2_R2
   - detail: flows/03460001.md ; trace prefix `76:65:03460001`
41. **seq 66 - Deposit Slip Zero Balance Validation R2 KH** (`05080001`) - area: Deposit Slip
   - actor: same session (Auto_KH1)
   - consumes: `REPO_GINNO` from seq 22 (04740001)
   - checks: none configured
   - screens: DepSlip_Balance0_Val_R2_KH -> Cash_DepSlip_Bal_0_Val_R2_KH -> Cheque_DepSlip_Bal_0_Val_R2_KH
   - detail: flows/05080001.md ; trace prefix `76:66:05080001`

## Inactive rows (skipped by the engine)
- seq 3 Dispatch Advice II R2 KH (`04670001`) status N
- seq 4 Dispatch Advice Negative (`00100002`) status N
- seq 5 Dispatch Advice Rejection (`00740002`) status N
- seq 6 Dispatch Advice Approval KH (`04680001`) status N
- seq 7 Dispatch Advice Loss Approval Request (`00750001`) status N
- seq 9 Dispatch Advice Loss Approval (`00760001`) status N
- seq 10 Stock Validation After DA R2 KH (`04690001`) status N
- seq 17 Stock Validation After SAN (W to W) (`02860001`) status N
- seq 23 Goods Issue Note Terminat Approval (`00780003`) status N
- seq 24 Goods Issue N Rejection Approval (`00780002`) status N
- seq 28 Stock Allocation (`00130001`) status N
- seq 33 Cashmemo Reschedule (`01040001`) status N
- seq 34 FRESH SALES RETURN Partial R2 (`03140001`) status N
- seq 36 FRESH_SALES_RETURN Full_R2 (`03130001`) status N
- seq 37 Amounts Validation after Fresh Sales Return Full R2 (`03590001`) status N
- seq 45 Deposit Slip Approval (`00140002`) status N
- seq 47 Deposit Slip Approval (`00140002`) status N
- seq 49 Deposit Slip Approval (`00140002`) status N
- seq 67 SAN (Admin) R2 (`02870001`) status N
- seq 68 SAN Approval R2 (`02890001`) status N
- seq 69 Stock Validation after SAN (Admin) (`02850001`) status N
- seq 70 SAN (Warehouse to Warehouse) R2 (`02880001`) status N
- seq 71 SAN Approval R2 (`02890001`) status N
- seq 72 Stock Validation After SAN (W to W) (`02860001`) status N
