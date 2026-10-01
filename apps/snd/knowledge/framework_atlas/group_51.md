# Group 51 - Daily Cycle Only Positive Flow_ITHD

Source `gtf:51`. Market guess (from name): TH. Rows: 65 (active 44, inactive 21). User switch points: 17 (3, 6, 10, 14, 18, 25, 27, 33, 34, 37, 41, 42, 43, 54, 55, 61, 62).

Allowed apps (alg): app 12 ITHD_Centegy QA 2 -> D:/Selenium/Automation/ITHD_QA// (workbook variant inferred: None); app 14 Up_Coming_Centegy QA -> D:/Selenium/Automation/Up_Coming_QA// (workbook variant inferred: None)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 2 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `51:2:021400000`
2. **seq 3 - Dispatch Advice II TH** (`01210001`) - area: Dispatch Advice
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DOCUMENTNO` produced within same flow
   - produces: `ORDERNUMBER`, `REPO_DOCUMENTNO`
   - checks: 7 message/field assertion(s); group assertion sheet(s): `DA_FORWARD_ASSR`
   - screens: Dispatch Advice II_THI -> Dispatch Advice II__THI -> Dispatch Advice II Detail2_THI -> Dispatch Advice II Detail_THI -> Dispatch Advice II Detail3_THI -> Dispatch Advice II Grid_THI ...
   - detail: flows/01210001.md ; trace prefix `51:3:01210001`
3. **seq 6 - Dispatch Advice II Approval** (`00990001`) - area: Dispatch Advice, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_DOCUMENTNO` from seq 3 (01210001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DA_APPROVALFRWD_ASSR`
   - screens: Dispatch Advice II Approval
   - detail: flows/00990001.md ; trace prefix `51:6:00990001`
4. **seq 10 - Stock Validation After DA** (`02700001`) - area: Dispatch Advice, Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_DA -> Stock_Val_after_DA2 -> Stock_Val_after_DA3
   - detail: flows/02700001.md ; trace prefix `51:10:02700001`
5. **seq 12 - Order Booking R2** (`03110001`) - area: Order Booking
   - actor: same session (Auto_Th)
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Order Booking_R2 -> Order Booking Detail_R2 -> Order Booking Detail2_R2
   - detail: flows/03110001.md ; trace prefix `51:12:03110001`
6. **seq 14 - Promo, Charges Validation After OB R2** (`03280001`) - area: Order Booking, Transaction Inquiry, Promotion, Charges/Tax
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 5 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 6, Q2Q 0
   - screens: Transaction_inquiry_val_R2 -> Trans_inq_header_val_R2 -> Trans_inq_detail_val_R2 -> Trans_inq_totalOffer_val_R2_1 -> Trans_inq_totalOffer_val_R2_2 -> Trans_inq_total_tax_val_R2 ...
   - detail: flows/03280001.md ; trace prefix `51:14:03280001`
7. **seq 15 - Stock Allocation** (`00130001`) - area: Stock Allocation
   - actor: same session (Auto_Th)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_Allocation_ASSR`
   - screens: Stock Allocation
   - detail: flows/00130001.md ; trace prefix `51:15:00130001`
8. **seq 16 - Order Editing R2 TH** (`03120001`) - area: Order Editing
   - actor: same session (Auto_Th)
   - produces: `ORDERNUMBEREDIT`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`; value validations 1, Q2Q 0
   - screens: Order Editing_R2 -> Order Editing Detail_R2 -> Order Editing Detail3_R2
   - detail: flows/03120001.md ; trace prefix `51:16:03120001`
9. **seq 18 - Amounts Validation after Order Editing R2** (`03330001`) - area: Order Editing, Transaction Inquiry
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 5 message/field assertion(s); value validations 5, Q2Q 0
   - screens: Amount_Val_After_Order_Edit_R2 -> Amt_Val_After_Edit_header_R2 -> Amt_Val_After_Edit_detail_R2 -> Amt_Val_After_Edit_tot_offer_R2 -> Amt_Val_After_Edit_tot_tax_R2 -> Amt_Val_After_Edit_add_charg_R2
   - detail: flows/03330001.md ; trace prefix `51:18:03330001`
10. **seq 19 - Order Cancellation R2 TH** (`00040001`) - area: Order Cancellation
   - actor: same session (Auto_Th)
   - checks: 2 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Order Cancellation -> Order Cancellation Detail -> Order Cancellation Detail_Val
   - detail: flows/00040001.md ; trace prefix `51:19:00040001`
11. **seq 20 - Stock Unallocation** (`00130002`) - area: Stock Allocation
   - actor: same session (Auto_Th)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Unallocated_ASSR`
   - screens: Stock Unallocation
   - detail: flows/00130002.md ; trace prefix `51:20:00130002`
12. **seq 21 - Delivery Date Change R2 TH** (`04650001`) - area: Delivery Date Change
   - actor: same session (Auto_Th)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery Date Change
   - detail: flows/04650001.md ; trace prefix `51:21:04650001`
13. **seq 22 - Goods Issue Note R2 TH** (`04660001`) - area: GIN (Goods Issue Note)
   - actor: same session (Auto_Th)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`, `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue Note -> Goods Issue Note CM Selection -> Goods Issue Note Detail -> Goods Issue Note Forward
   - detail: flows/04660001.md ; trace prefix `51:22:04660001`
14. **seq 25 - Goods Issue Note Approval** (`00780001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_GINNO` from seq 22 (04660001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue Note Approval
   - detail: flows/00780001.md ; trace prefix `51:25:00780001`
15. **seq 27 - Stock Validation After GIN R2 TH** (`05260001`) - area: GIN (Goods Issue Note), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_val_after_GIN_1 -> Stock_Val_after_GIN_2 -> Stock_Val_after_GIN_3
   - detail: flows/05260001.md ; trace prefix `51:27:05260001`
16. **seq 33 - FRESH SALES RETURN Partial R2** (`03140001`) - area: Sales Return
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12) (same user as before: re-login only)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `FRESH_SALES_RETURN_ASSR`, `FRESH_SAL_RETVal_Partial_ASSR`, `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Valid_ASSR`; value validations 1, Q2Q 0
   - screens: FRESH_SALES_RET_Partial_R2 -> FRESH_SALES_RET_DTL Partial_R2 -> FRESH_SALES_RETURN Val Partial
   - detail: flows/03140001.md ; trace prefix `51:33:03140001`
17. **seq 34 - Amounts Validation after Fresh Sales Return Partial R2** (`03600001`) - area: Sales Return, Transaction Inquiry
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 6 message/field assertion(s); value validations 6, Q2Q 0
   - screens: Amt_Val_Partial_Fresh_return_R2 -> Amt_Val_P_FreshRet_detail_R2 -> Amt_Val_P_FreshRe_TotalOff_1_R2 -> Amt_Val_P_FreshRe_TotalOff_2_R2 -> Amt_Val_P_FreshRet_TotalTax_R2 -> Amt_Val_P_FreshRe_AddCharges_R2 ...
   - detail: flows/03600001.md ; trace prefix `51:34:03600001`
18. **seq 36 - FRESH_SALES_RETURN Full_R2** (`03130001`) - area: Sales Return
   - actor: same session (Auto_Th)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `FRESH_SALES_RETURN_Full_ASSR`, `FRESH_SAL_RETURN_Val_Full_ASSR`; value validations 1, Q2Q 0
   - screens: FRESH_SALES_RET_Full_R2 -> FRESH_SALES_RET_DTL_Full_R2 -> FRESH_SALES_RETURN Val_Full
   - detail: flows/03130001.md ; trace prefix `51:36:03130001`
19. **seq 37 - Amounts Validation after Fresh Sales Return Full R2** (`03590001`) - area: Sales Return, Transaction Inquiry
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DOCUMENTNO` from seq 3 (01210001)
   - checks: 5 message/field assertion(s); value validations 5, Q2Q 0
   - screens: Amt_Val_Full_Fresh_return_R2 -> Amt_Val_F_FreshRe_TotalOff_1_R2 -> Amt_Val_F_FreshRe_TotalOff_2_R2 -> Amt_Val_F_FreshRet_TotalTax_R2 -> Amt_Val_F_FreshRe_AddCharges_R2 -> Amt_Val_F_FreshRet_Header_R2 ...
   - detail: flows/03590001.md ; trace prefix `51:37:03590001`
20. **seq 38 - Cashmemo Status** (`00030001`) - area: Cashmemo
   - actor: same session (Auto_Th)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Cashmemo Status
   - detail: flows/00030001.md ; trace prefix `51:38:00030001`
21. **seq 39 - Sales Return_R2** (`03150001`) - area: Sales Return
   - actor: same session (Auto_Th)
   - checks: 2 message/field assertion(s); group assertion sheet(s): `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Valid_ASSR`, `Sales_Return_Val_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return_R2 -> Sales Return Detail_R2 -> Sales Return Validation_R2
   - detail: flows/03150001.md ; trace prefix `51:39:03150001`
22. **seq 40 - Sales Return View_R2** (`03160001`) - area: Sales Return
   - actor: same session (Auto_Th)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetrunView_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View_R2 -> Sales Return View,Detail_Val_R2
   - detail: flows/03160001.md ; trace prefix `51:40:03160001`
23. **seq 41 - Sales Return View Approval_R2** (`03170001`) - area: Sales Return, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetrunViewApprval_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View Approval_R2
   - detail: flows/03170001.md ; trace prefix `51:41:03170001`
24. **seq 42 - Sales Return Status Change_R2** (`03180001`) - area: Sales Return
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - consumes: `REPO_GINNO` from seq 22 (04660001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SR_StatsChang_DTL_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return Status Change_R2 -> Sales Ret Status Change2_R2 -> Sales R Status Change_Valid_R2
   - detail: flows/03180001.md ; trace prefix `51:42:03180001`
25. **seq 43 - Amounts Validation after Sales Return R2** (`03360001`) - area: Sales Return, Transaction Inquiry
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 6 message/field assertion(s); value validations 6, Q2Q 0
   - screens: Amount_after_Sale_return_R2 -> Amt_after_SaleRet_detail_R2 -> Amt_after_SaleRet_TotalOff_1_R2 -> Amt_after_SaleRet_TotalOff_2_R2 -> Amt_after_SaleRet_TotalTax_R2 -> Amt_after_SaleRet_AddCharges_R2 ...
   - detail: flows/03360001.md ; trace prefix `51:43:03360001`
26. **seq 44 - Deposit Slip Multi Cheques** (`00140001`) - area: Deposit Slip
   - actor: same session (Auto_Th)
   - produces: `REPO_Deposit_Slip`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`, `Deposit_Slip_Outlet_ASSR`, `screenshot_ASSR`
   - screens: Deposit Slip -> Deposit Slip,Outlet
   - detail: flows/00140001.md ; trace prefix `51:44:00140001`
27. **seq 46 - Deposit Slip Cheque** (`00140004`) - area: Deposit Slip
   - actor: same session (Auto_Th)
   - consumes: `REPO_GINNO` from seq 22 (04660001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip -> Deposit Slip,Cash memos
   - detail: flows/00140004.md ; trace prefix `51:46:00140004`
28. **seq 48 - Deposit Slip Cash** (`00140005`) - area: Deposit Slip
   - actor: same session (Auto_Th)
   - consumes: `REPO_GINNO` from seq 22 (04660001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip,Cash -> Deposit Slip,Cash memos,Cash
   - detail: flows/00140005.md ; trace prefix `51:48:00140005`
29. **seq 50 - Deposit Slip Cash Full R2** (`03400001`) - area: Deposit Slip
   - actor: same session (Auto_Th)
   - consumes: `REPO_GINNO` from seq 22 (04660001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit_Slip_Cash_Full_1_R2 -> Deposit_Slip_Cash_Full_2_R2
   - detail: flows/03400001.md ; trace prefix `51:50:03400001`
30. **seq 51 - Deposit Slip Cheque Full R2** (`03410001`) - area: Deposit Slip
   - actor: same session (Auto_Th)
   - consumes: `REPO_GINNO` from seq 22 (04660001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit_Slip_Cheque_Full_1_R2 -> Deposit_Slip_Cheque_Full_2_R2
   - detail: flows/03410001.md ; trace prefix `51:51:03410001`
31. **seq 52 - Deposit Slip Un Posted Amount Validation R2** (`03420001`) - area: Deposit Slip, Transaction Inquiry
   - actor: same session (Auto_Th)
   - consumes: `REPO_GINNO` from seq 22 (04660001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Deposit_Slip_Creation_R2 -> Deposit_Slip_Cashmemo_Save_R2 -> Deposit_Slip_UnPosted_Val_R2
   - detail: flows/03420001.md ; trace prefix `51:52:03420001`
32. **seq 53 - Good Return Note** (`00090001`) - area: GRN (Goods Return Note)
   - actor: same session (Auto_Th)
   - consumes: `REPO_GRN No.` unresolved in group
   - produces: `REPO_GRNNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GRN_DTL_SAVE_ASSR`, `GRN_FORWARD_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Return Note -> Good Return Note Detail -> Good Return Note Detail_Valida -> Goods Return Note Forward
   - detail: flows/00090001.md ; trace prefix `51:53:00090001`
33. **seq 54 - Good Return Note Approval** (`00810001`) - area: GRN (Goods Return Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_GRNNO` from seq 53 (00090001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GRN_APPROVAL_ASSR`
   - screens: Good Return Note Approval
   - detail: flows/00810001.md ; trace prefix `51:54:00810001`
34. **seq 55 - Stock Validation After GRN** (`02730001`) - area: GRN (Goods Return Note), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_GRN -> Stock_Val_after_GRN2 -> Stock_Val_after_GRN3
   - detail: flows/02730001.md ; trace prefix `51:55:02730001`
35. **seq 56 - Route Settlement** (`00680001`) - area: Route Settlement
   - actor: same session (Auto_Th)
   - checks: 5 message/field assertion(s); value validations 5, Q2Q 0
   - screens: Route Settlement -> Route Settlement Validation -> Route Settlement Validation1 -> Route Settlement Validation2 -> Route Settlement Validation3 -> Route Settlement Validation4
   - detail: flows/00680001.md ; trace prefix `51:56:00680001`
36. **seq 57 - Cheque Status R2** (`03520001`) - area: Cheque
   - actor: same session (Auto_Th)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Cheque_Status_ASSR`
   - screens: Cheque Status R2
   - detail: flows/03520001.md ; trace prefix `51:57:03520001`
37. **seq 58 - DSR Adjustment Amount** (`00670001`) - area: DSR/PJP/Route
   - actor: same session (Auto_Th)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DSR_ADJ_AMOUNT_ASSR`; value validations 1, Q2Q 0
   - screens: DSR Adjustment Amount -> DSR Adjustment Amount,Detail
   - detail: flows/00670001.md ; trace prefix `51:58:00670001`
38. **seq 59 - PJP Daily Inquiry Update** (`00930001`) - area: DSR/PJP/Route
   - actor: same session (Auto_Th)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `PJP_Inquiry_ASSR`
   - screens: PJP Daily -> PJP Daily2
   - detail: flows/00930001.md ; trace prefix `51:59:00930001`
39. **seq 60 - OTC Stock Out R2** (`02910001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - actor: same session (Auto_Th)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: OTC Stock Out R2 -> OTC Stock Out Det R2 -> OTC Stock Out Fwd R2
   - detail: flows/02910001.md ; trace prefix `51:60:02910001`
40. **seq 61 - SAN Approval R2** (`02890001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_DocumentNo` from seq 60 (02910001); `REPO_DocumentType` from seq 60 (02910001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP R2
   - detail: flows/02890001.md ; trace prefix `51:61:02890001`
41. **seq 62 - Opening & Closing Stock Validation** (`02830001`) - area: Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Open_Close_Stock_Val -> Open_Close_Stock_Val2 -> Open_Close_Stock_Val3
   - detail: flows/02830001.md ; trace prefix `51:62:02830001`
42. **seq 63 - Received Amount Validation Transaction Inquiry R2** (`03290001`) - area: Transaction Inquiry
   - actor: same session (Auto_Th)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: ReceivedAmt_Val_TransInq_R2_1 -> ReceivedAmt_Val_TransInq_R2_2
   - detail: flows/03290001.md ; trace prefix `51:63:03290001`
43. **seq 64 - Charges Validation Transaction Inquiry R2** (`03310001`) - area: Transaction Inquiry, Charges/Tax
   - actor: same session (Auto_Th)
   - checks: 2 message/field assertion(s); value validations 2, Q2Q 0
   - screens: Charges_Val_Transaction_Inq_R2 -> Charges_Val_Total_Tax_R2 -> Charges_Val_Header_R2
   - detail: flows/03310001.md ; trace prefix `51:64:03310001`
44. **seq 65 - Deposit Slip Received Amount Validation R2** (`03460001`) - area: Deposit Slip, Transaction Inquiry
   - actor: same session (Auto_Th)
   - consumes: `REPO_GINNO` from seq 22 (04660001)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: DepSlip_ReceivedAmount_Val_1_R2 -> DepSlip_ReceivedAmount_Val_2_R2
   - detail: flows/03460001.md ; trace prefix `51:65:03460001`

## Inactive rows (skipped by the engine)
- seq 4 Dispatch Advice Negative (`00100002`) status N
- seq 5 Dispatch Advice Rejection (`00740002`) status N
- seq 7 Dispatch Advice Loss Approval Request (`00750001`) status N
- seq 9 Dispatch Advice Loss Approval (`00760001`) status N
- seq 17 Stock Validation After SAN (W to W) (`02860001`) status N
- seq 23 Goods Issue Note Terminat Approval (`00780003`) status N
- seq 24 Goods Issue N Rejection Approval (`00780002`) status N
- seq 28 Stock Allocation (`00130001`) status N
- seq 29 Order Editing After GIN (`00840001`) status N
- seq 31 Order Cancellation After GIN (`00850001`) status N
- seq 32 Cashmemo Reschedule (`01040001`) status N
- seq 45 Deposit Slip Approval (`00140002`) status N
- seq 47 Deposit Slip Approval (`00140002`) status N
- seq 49 Deposit Slip Approval (`00140002`) status N
- seq 66 Deposit Slip Zero Balance Validation R2 (`03490001`) status N
- seq 67 SAN (Admin) R2 (`02870001`) status N
- seq 68 SAN Approval R2 (`02890001`) status N
- seq 69 Stock Validation after SAN (Admin) (`02850001`) status N
- seq 70 SAN (Warehouse to Warehouse) R2 (`02880001`) status N
- seq 71 SAN Approval R2 (`02890001`) status N
- seq 72 Stock Validation After SAN (W to W) (`02860001`) status N
