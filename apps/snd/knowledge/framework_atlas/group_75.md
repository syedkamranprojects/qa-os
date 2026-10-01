# Group 75 - Daily Cycle Only Positive Flow_VN

Source `gtf:75`. Market guess (from name): PK(none in name). Rows: 65 (active 44, inactive 21). User switch points: 28 (3, 6, 10, 14, 18, 25, 27, 29, 31, 41, 42, 43, 44, 46, 48, 50, 51, 52, 54, 55, 56, 59, 61, 62, 63, 64, 65, 66).

Allowed apps (alg): app 16 VN_Centegy QA -> D:/Selenium/Automation/VN_QA// (workbook variant inferred: Vietnam)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 2 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `75:2:021400000`
2. **seq 3 - Dispatch Advice R2 VN** (`03950001`) - area: Dispatch Advice
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DOCUMENTNO` produced within same flow
   - produces: `REPO_DOCUMENTNO`
   - checks: 7 message/field assertion(s); group assertion sheet(s): `DA_FORWARD_ASSR`; value validations 1, Q2Q 0
   - screens: Dispatch Advice VN -> Dispatch Advice VN -> Dispatch Advice Detail2 VN -> Dispatch Advice Detail VN -> DA Amount Val R2 VN -> Dispatch Advice Grid VN ...
   - detail: flows/03950001.md ; trace prefix `75:3:03950001`
3. **seq 6 - Dispatch Advice Approval R2 VN** (`04050001`) - area: Dispatch Advice, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **AUTO_TSSM_VAT** (serial 38)
   - consumes: `REPO_DOCUMENTNO` from seq 3 (03950001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DA_APPROVALFRWD_ASSR`
   - screens: Dispatch Advice Approval VN
   - detail: flows/04050001.md ; trace prefix `75:6:04050001`
4. **seq 10 - Stock Validation After DA R2 VN** (`04190001`) - area: Dispatch Advice, Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **AUTO_VAT** (serial 37)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_DA_R2_VN -> Stock_Val_after_DA_2_R2_VN -> Stock_Val_after_DA_3_R2_VN
   - detail: flows/04190001.md ; trace prefix `75:10:04190001`
5. **seq 12 - Order Booking_R2 VN** (`03960001`) - area: Order Booking
   - actor: same session (AUTO_VAT)
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Order Booking_R2_VN -> Order Booking Detail_R2_VN -> Order Booking Detail2_R2_VN
   - detail: flows/03960001.md ; trace prefix `75:12:03960001`
6. **seq 14 - Promo, Charges Validation After OB R2** (`03280001`) - area: Order Booking, Transaction Inquiry, Promotion, Charges/Tax
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 5 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 6, Q2Q 0
   - screens: Transaction_inquiry_val_R2 -> Trans_inq_header_val_R2 -> Trans_inq_detail_val_R2 -> Trans_inq_totalOffer_val_R2_1 -> Trans_inq_totalOffer_val_R2_2 -> Trans_inq_total_tax_val_R2 ...
   - detail: flows/03280001.md ; trace prefix `75:14:03280001`
7. **seq 15 - Stock Allocation** (`00130001`) - area: Stock Allocation
   - actor: same session (AUTO_VAT)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_Allocation_ASSR`
   - screens: Stock Allocation
   - detail: flows/00130001.md ; trace prefix `75:15:00130001`
8. **seq 16 - Order Editing_R2 VN** (`03980001`) - area: Order Editing
   - actor: same session (AUTO_VAT)
   - produces: `ORDERNUMBEREDIT`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`; value validations 1, Q2Q 0
   - screens: Order Editing_R2 VN -> Order Editing Detail_R2 VN -> Order Editing Detail3_R2 VN
   - detail: flows/03980001.md ; trace prefix `75:16:03980001`
9. **seq 18 - Amounts Validation after Order Editing R2 VN** (`04360001`) - area: Order Editing, Transaction Inquiry
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 6 message/field assertion(s); value validations 6, Q2Q 0
   - screens: Amount_Val_Aft_Order_Edit_R2_VN -> Amt_Val_After_Edit_detail_R2_VN -> Amt_Val_Aft_Edit_tot_off1_R2_VN -> Amt_Val_Aft_Edit_tot_off2_R2_VN -> Amt_Val_Aft_Edit_tot_tax_R2_VN -> Amt_Val_Aft_Edit_add_chrg_R2_VN ...
   - detail: flows/04360001.md ; trace prefix `75:18:04360001`
10. **seq 19 - Order Cancellation R2 VN** (`03990001`) - area: Order Cancellation
   - actor: same session (AUTO_VAT)
   - checks: 2 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Order_Cancellation_R2_VN -> Order_Cancellation_Detail_R2_VN -> Order_Cancel_Detail_Val_R2_VN
   - detail: flows/03990001.md ; trace prefix `75:19:03990001`
11. **seq 20 - Stock Unallocation** (`00130002`) - area: Stock Allocation
   - actor: same session (AUTO_VAT)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Unallocated_ASSR`
   - screens: Stock Unallocation
   - detail: flows/00130002.md ; trace prefix `75:20:00130002`
12. **seq 21 - Delivery Date Change** (`00160001`) - area: Delivery Date Change
   - actor: same session (AUTO_VAT)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery Date Change
   - detail: flows/00160001.md ; trace prefix `75:21:00160001`
13. **seq 22 - Goods Issue Note R2 VN** (`04000001`) - area: GIN (Goods Issue Note)
   - actor: same session (AUTO_VAT)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`, `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue Note R2 VN -> GIN CM Selection R2 VN -> GIN Detail R2 VN -> GIN Forward R2 VN
   - detail: flows/04000001.md ; trace prefix `75:22:04000001`
14. **seq 25 - Goods Issue Note Approval R2 VN** (`04010001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **AUTO_TSSM_VAT** (serial 38)
   - consumes: `REPO_GINNO` from seq 22 (04000001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue Note App R2 VN
   - detail: flows/04010001.md ; trace prefix `75:25:04010001`
15. **seq 27 - Stock Validation After GIN R2 VN** (`04200001`) - area: GIN (Goods Issue Note), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **AUTO_VAT** (serial 37)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_GIN_R2_VN -> Stock_Val_after_GIN_2_R2_VN -> Stock_Val_after_GIN_3_R2_VN
   - detail: flows/04200001.md ; trace prefix `75:27:04200001`
16. **seq 29 - Order Editing After GIN R2 VN** (`04020001`) - area: Order Editing, GIN (Goods Issue Note)
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - produces: `ORDERNUMBEREDIT`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`, `screenshot_ASSR`; value validations 2, Q2Q 0
   - screens: Order Editing After GIN R2 VN -> Order Editing Det Aft GIN R2 VN -> Order Editing Det2 AftGIN R2 VN
   - detail: flows/04020001.md ; trace prefix `75:29:04020001`
17. **seq 31 - Amounts Validation after GIN Order Edit R2 VN** (`04040001`) - area: Order Editing, GIN (Goods Issue Note), Transaction Inquiry
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 5 message/field assertion(s); value validations 5, Q2Q 0
   - screens: Amt_Val_AfterGIN_Odr_Edit_R2_VN -> Amt_Val_AftGIN_Edit_detail_R2VN -> Amt_Val_Aft_GIN_Edt_tot_offR2VN -> Amt_Val_AftGIN_Edt_tot_tax_R2VN -> Amt_Val_AftGIN_Edt_addchargR2VN -> Amt_Val_AfTGIN_Edit_header_R2VN
   - detail: flows/04040001.md ; trace prefix `75:31:04040001`
18. **seq 32 - Order Cancellation After GIN R2 VN** (`04030001`) - area: Order Cancellation, GIN (Goods Issue Note)
   - actor: same session (AUTO_VAT)
   - checks: 2 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Order Cancel after GIN R2 VN -> Odr Cancel after GIN det R2 VN -> Odr_Can_afterGINDetail_Val_R2VN
   - detail: flows/04030001.md ; trace prefix `75:32:04030001`
19. **seq 38 - Cashmemo Status R2 VN** (`04070001`) - area: Cashmemo
   - actor: same session (AUTO_VAT)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Cashmemo Status R2 VN
   - detail: flows/04070001.md ; trace prefix `75:38:04070001`
20. **seq 39 - Sales Return R2 VN** (`04080001`) - area: Sales Return
   - actor: same session (AUTO_VAT)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Valid_ASSR`, `Sales_Return_Val_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return R2 VN -> Sales Return Detail R2 VN -> Sales Return Validation R2 VN
   - detail: flows/04080001.md ; trace prefix `75:39:04080001`
21. **seq 40 - Sales Return View R2 VN** (`04090001`) - area: Sales Return
   - actor: same session (AUTO_VAT)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetrunView_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View R2 VN -> Sales Return View Det Val R2 VN
   - detail: flows/04090001.md ; trace prefix `75:40:04090001`
22. **seq 41 - Sales Return View Approval R2 VN** (`04100001`) - area: Sales Return, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **AUTO_TSSM_VAT** (serial 38)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetrunViewApprval_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View App R2 VN
   - detail: flows/04100001.md ; trace prefix `75:41:04100001`
23. **seq 42 - Sales Return Status Change R2 VN** (`04110001`) - area: Sales Return
   - **SWITCH USER POINT**: log out and log in as **AUTO_VAT** (serial 37)
   - consumes: `REPO_GINNO` from seq 22 (04000001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SR_StatsChang_DTL_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Ret Status Change R2 VN -> Sales Ret Status Change2 R2 VN -> Sales R Status Change Val R2 VN
   - detail: flows/04110001.md ; trace prefix `75:42:04110001`
24. **seq 43 - Amounts Validation after Sales Return R2 VN** (`04370001`) - area: Sales Return, Transaction Inquiry
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 6 message/field assertion(s); value validations 6, Q2Q 0
   - screens: Amount_after_Sale_return_R2_VN -> Amt_after_SaleRet_detail_R2_VN -> Amt_aft_SaleRet_TotOff_1_R2_VN -> Amt_aft_SaleRet_TotOff_2_R2_VN -> Amt_aftr_SaleRet_TotalTax_R2_VN -> Amt_aft_SaleRet_AddCharge_R2_VN ...
   - detail: flows/04370001.md ; trace prefix `75:43:04370001`
25. **seq 44 - Deposit Slip Multi Cheque R2 VN** (`04120001`) - area: Deposit Slip
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - produces: `REPO_DeSlip_M_chq`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`, `Deposit_Slip_Outlet_ASSR`, `screenshot_ASSR`
   - screens: Deposit Slip Multi Chq R2 VN -> Deposit Slip Multi Chq1 R2 VN
   - detail: flows/04120001.md ; trace prefix `75:44:04120001`
26. **seq 46 - Deposit Slip Cheque R2 VN** (`04130001`) - area: Deposit Slip
   - **SWITCH USER POINT**: log out and log in as **AUTO_VAT** (serial 37) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 22 (04000001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip Chq R2 VN -> Deposit Slip Chq2 R2 VN
   - detail: flows/04130001.md ; trace prefix `75:46:04130001`
27. **seq 48 - Deposit Slip Cash R2 VN** (`04140001`) - area: Deposit Slip
   - **SWITCH USER POINT**: log out and log in as **AUTO_VAT** (serial 37) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 22 (04000001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip Cash R2 VN -> Deposit Slip Cash2 R2 VN
   - detail: flows/04140001.md ; trace prefix `75:48:04140001`
28. **seq 50 - Deposit Slip Cash Full R2 VN** (`04150001`) - area: Deposit Slip
   - **SWITCH USER POINT**: log out and log in as **AUTO_VAT** (serial 37) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 22 (04000001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit_Slip_Cash_Full_1_R2_VN -> Deposit_Slip_Cash_Full_2_R2_VN
   - detail: flows/04150001.md ; trace prefix `75:50:04150001`
29. **seq 51 - Deposit Slip Cheque Full R2 VN** (`04160001`) - area: Deposit Slip
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 22 (04000001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit_Slip_Cheq_Full_1_R2_VN -> Deposit_Slip_Cheq_Full_2_R2_VN
   - detail: flows/04160001.md ; trace prefix `75:51:04160001`
30. **seq 52 - Deposit Slip Un Posted Amount Validation R2** (`03420001`) - area: Deposit Slip, Transaction Inquiry
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 22 (04000001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Deposit_Slip_Creation_R2 -> Deposit_Slip_Cashmemo_Save_R2 -> Deposit_Slip_UnPosted_Val_R2
   - detail: flows/03420001.md ; trace prefix `75:52:03420001`
31. **seq 53 - Good Return Note R2 VN** (`04170001`) - area: GRN (Goods Return Note)
   - actor: same session (AUTO_VAT)
   - consumes: `REPO_GRN No.` unresolved in group
   - produces: `REPO_GRNNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GRN_DTL_SAVE_ASSR`, `GRN_FORWARD_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Return Note R2 VN -> GRN Detail R2 VN -> GRN Detail Validation R2 VN -> GRN Forward R2 VN
   - detail: flows/04170001.md ; trace prefix `75:53:04170001`
32. **seq 54 - Good Return Note Approval R2 VN** (`04180001`) - area: GRN (Goods Return Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **AUTO_TSSM_VAT** (serial 38)
   - consumes: `REPO_GRNNO` from seq 53 (04170001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GRN_APPROVAL_ASSR`
   - screens: Goods Return Note App R2 VN
   - detail: flows/04180001.md ; trace prefix `75:54:04180001`
33. **seq 55 - Stock Validation After GRN R2 VN** (`04210001`) - area: GRN (Goods Return Note), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **AUTO_VAT** (serial 37)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_GRN_R2_VN -> Stock_Val_after_GRN_2_R2_VN -> Stock_Val_after_GRN_3_R2_VN
   - detail: flows/04210001.md ; trace prefix `75:55:04210001`
34. **seq 56 - Route Settlement R2 VN** (`04230001`) - area: Route Settlement
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 4 message/field assertion(s); value validations 4, Q2Q 0
   - screens: Route Settlement R2 VN -> Route Settlement Val R2 VN -> Route Settlement Val1 R2 VN -> Route Settlement Val2 R2 VN -> Route Settlement Val3 R2 VN
   - detail: flows/04230001.md ; trace prefix `75:56:04230001`
35. **seq 57 - Cheque Status R2 VN** (`04240001`) - area: Cheque
   - actor: same session (AUTO_VAT)
   - consumes: `REPO_DeSlip_M_chq` from seq 44 (04120001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Cheque_Status_ASSR`
   - screens: Cheque Status R2 VN
   - detail: flows/04240001.md ; trace prefix `75:57:04240001`
36. **seq 58 - DSR Adjustment Amount R2 VN** (`04250001`) - area: DSR/PJP/Route
   - actor: same session (AUTO_VAT)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DSR_ADJ_AMOUNT_ASSR`; value validations 1, Q2Q 0
   - screens: DSR Adjustment Amount R2 VN -> DSR Adjustment Amount,Det R2 VN
   - detail: flows/04250001.md ; trace prefix `75:58:04250001`
37. **seq 59 - PJP Daily Inquiry Update R2 VN** (`04260001`) - area: DSR/PJP/Route
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `PJP_Inquiry_ASSR`
   - screens: PJP Daily R2 VN -> PJP Daily2 R2 VN
   - detail: flows/04260001.md ; trace prefix `75:59:04260001`
38. **seq 60 - OTC Stock Out R2 VN** (`04270001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - actor: same session (AUTO_VAT)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: OTC Stock Out R2 VN -> OTC Stock Out Det R2 VN -> OTC Stock Out Fwd R2 VN
   - detail: flows/04270001.md ; trace prefix `75:60:04270001`
39. **seq 61 - SAN Approval R2 VN** (`04280001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **AUTO_TSSM_VAT** (serial 38)
   - consumes: `REPO_DocumentNo` from seq 60 (04270001); `REPO_DocumentType` from seq 60 (04270001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP R2 VN
   - detail: flows/04280001.md ; trace prefix `75:61:04280001`
40. **seq 62 - Opening & Closing Stock Validation R2 VN** (`04290001`) - area: Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **AUTO_VAT** (serial 37)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Open_Close_Stock_Val_R2_VN -> Open_Close_Stock_Val2_R2_VN -> Open_Close_Stock_Val3_R2_VN
   - detail: flows/04290001.md ; trace prefix `75:62:04290001`
41. **seq 63 - Received Amount Validation Transaction Inquiry R2** (`03290001`) - area: Transaction Inquiry
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: ReceivedAmt_Val_TransInq_R2_1 -> ReceivedAmt_Val_TransInq_R2_2
   - detail: flows/03290001.md ; trace prefix `75:63:03290001`
42. **seq 64 - Charges Validation Transaction Inquiry R2** (`03310001`) - area: Transaction Inquiry, Charges/Tax
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 2 message/field assertion(s); value validations 2, Q2Q 0
   - screens: Charges_Val_Transaction_Inq_R2 -> Charges_Val_Total_Tax_R2 -> Charges_Val_Header_R2
   - detail: flows/03310001.md ; trace prefix `75:64:03310001`
43. **seq 65 - Deposit Slip Received Amount Validation R2** (`03460001`) - area: Deposit Slip, Transaction Inquiry
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 22 (04000001)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: DepSlip_ReceivedAmount_Val_1_R2 -> DepSlip_ReceivedAmount_Val_2_R2
   - detail: flows/03460001.md ; trace prefix `75:65:03460001`
44. **seq 66 - Deposit Slip Zero Balance Validation R2 VN** (`04350001`) - area: Deposit Slip
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 22 (04000001)
   - checks: none configured
   - screens: DepSlip_Balance0_Val_R2_VN -> Cash_DepSlip_Bal_0_Val_R2_VN -> Cheque_DepSlip_Bal_0_Val_R2_VN
   - detail: flows/04350001.md ; trace prefix `75:66:04350001`

## Inactive rows (skipped by the engine)
- seq 4 Dispatch Advice Negative (`00100002`) status N
- seq 5 Dispatch Advice Rejection (`00740002`) status N
- seq 7 Dispatch Advice Loss Approval Request (`00750001`) status N
- seq 9 Dispatch Advice Loss Approval R2 VN (`04060001`) status N
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
