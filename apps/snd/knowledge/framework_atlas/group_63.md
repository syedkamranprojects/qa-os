# Group 63 - Daily Cycle Only Positive Flow_PH

Source `gtf:63`. Market guess (from name): PK(none in name). Rows: 64 (active 55, inactive 9). User switch points: 11 (6, 7, 23, 37, 38, 50, 51, 62, 63, 72, 73).

Allowed apps (alg): app 6 PHP_CentegyQA -> D:/Selenium/Automation/PHP_QA// (workbook variant inferred: PHP)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 2 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `63:2:021400000`
2. **seq 3 - Dispatch Advice_PH** (`04220001`) - area: Dispatch Advice
   - actor: same session (runner default login)
   - consumes: `REPO_DOCUMENTNO` produced within same flow
   - produces: `REPO_DOCUMENTNO`
   - checks: 6 message/field assertion(s); group assertion sheet(s): `DA_FORWARD_ASSR`; value validations 1, Q2Q 0
   - screens: Dispatch Advice PH -> Dispatch Advice Grid PH -> Dispatch Advice Detail2 PH -> Dispatch Advice Detail PH -> Dispatch Advice Forward PH -> Dispatch Advice Loss PH ...
   - detail: flows/04220001.md ; trace prefix `63:3:04220001`
3. **seq 6 - Dispatch Advice II Approval** (`00990001`) - area: Dispatch Advice, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_DOCUMENTNO` from seq 3 (04220001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DA_APPROVALFRWD_ASSR`
   - screens: Dispatch Advice II Approval
   - detail: flows/00990001.md ; trace prefix `63:6:00990001`
4. **seq 7 - Stock Validation After DA R2 PH** (`05210001`) - area: Dispatch Advice, Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_ValafterDA3_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_DA_R2_PH -> Stock_Val_after_DA_2_R2_PH -> Stock_Val_after_DA_3_R2_PH
   - detail: flows/05210001.md ; trace prefix `63:7:05210001`
5. **seq 9 - Free SKU Stock Validation after Dispatch Advice R2 PH** (`05600001`) - area: Dispatch Advice, Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Free_SKU_Val_Aft_DA_1_PH -> Free_SKU_Val_Aft_DA_2_PH -> Free_SKU_Val_Aft_DA_3_PH
   - detail: flows/05600001.md ; trace prefix `63:9:05600001`
6. **seq 11 - Order Booking PH** (`04300001`) - area: Order Booking
   - actor: same session (Auto_PH)
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Order Booking PH -> Order Booking Detail PH -> Order Booking Detail2 PH
   - detail: flows/04300001.md ; trace prefix `63:11:04300001`
7. **seq 12 - Free SKU Stock Validation after Order Booking R2 PH** (`05330001`) - area: Order Booking, Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Free_SKU_Val_Aft_OB_1_PH -> Free_SKU_Val_Aft_OB_2_PH -> Free_SKU_Val_Aft_OB_3_PH
   - detail: flows/05330001.md ; trace prefix `63:12:05330001`
8. **seq 15 - Trans Inq Validate after OB PH** (`04310001`) - area: Order Booking, Transaction Inquiry
   - actor: same session (Auto_PH)
   - checks: 4 message/field assertion(s); value validations 4, Q2Q 0
   - screens: Trans Inquiry val after OB PH -> Trans Inquiry Detail  Val OB PH -> Trans Inq Header Val OB PH -> Total Offering Amt Val OB PH -> Transecti After OB Tax PH
   - detail: flows/04310001.md ; trace prefix `63:15:04310001`
9. **seq 16 - Stock Allocation_PH** (`04320001`) - area: Stock Allocation
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Allocation_ASSR`
   - screens: Stock Allocation PH
   - detail: flows/04320001.md ; trace prefix `63:16:04320001`
10. **seq 18 - Free SKU Stock Validation after Stock Unallocation R2 PH** (`05550001`) - area: Stock Allocation, Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Free_SKU_Val_Aft_StockUnAl_1_PH -> Free_SKU_Val_Aft_StockUnAl_2_PH -> Free_SKU_Val_Aft_StockUnAl_3_PH
   - detail: flows/05550001.md ; trace prefix `63:18:05550001`
11. **seq 19 - Order Editing PH (QTY Increase)** (`04330001`) - area: Order Editing
   - actor: same session (Auto_PH)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`, `Order_Editing_Teasting_ASSR`; value validations 2, Q2Q 0
   - screens: Order Editing QTY Increase PH -> Order Editing Detail QTY IN PH -> Order Editing Detail4 QTY IN PH
   - detail: flows/04330001.md ; trace prefix `63:19:04330001`
12. **seq 21 - Free SKU Stock Validation after Order Editing (QTY Increase) R2 PH** (`05560001`) - area: Order Editing, Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: FreeSKU_Val_Aft_OrdEdit_IN_1_PH -> FreeSKU_Val_Aft_OrdEdit_IN_2_PH -> FreeSKU_Val_Aft_OrdEdit_IN_3_PH
   - detail: flows/05560001.md ; trace prefix `63:21:05560001`
13. **seq 22 - Stock Allocation_PH** (`04320001`) - area: Stock Allocation
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Allocation_ASSR`
   - screens: Stock Allocation PH
   - detail: flows/04320001.md ; trace prefix `63:22:04320001`
14. **seq 23 - Order Editing PH (QTY Decrease)** (`05440001`) - area: Order Editing
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `Order_Editing_Teasting_ASSR`; value validations 2, Q2Q 0
   - screens: Order Editing QTY Decrease PH -> Order Editing Detail QTY Dec PH -> Order Edit Detail4 QTY Dec PH
   - detail: flows/05440001.md ; trace prefix `63:23:05440001`
15. **seq 24 - Stock Unallocation_PH** (`03380001`) - area: Stock Allocation, Promotion
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Unallocated_ASSR`
   - screens: Stock Unallocation
   - detail: flows/03380001.md ; trace prefix `63:24:03380001`
16. **seq 25 - Free SKU Stock Validation after Order Editing (QTY Decrease) R2 PH** (`05570001`) - area: Order Editing, Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: FreeSKU_Val_AftOrdEdit_DEC_1_PH -> FreeSKU_Val_AftOrdEdit_DEC_2_PH -> FreeSKU_Val_AftOrdEdit_DEC_3_PH
   - detail: flows/05570001.md ; trace prefix `63:25:05570001`
17. **seq 27 - Trans Inq Validate after Editing PH** (`04340001`) - area: Transaction Inquiry
   - actor: same session (Auto_PH)
   - checks: 4 message/field assertion(s); value validations 4, Q2Q 0
   - screens: Trans Inq val after Editing PH -> Trans Inq Detail Val Editing PH -> Trans Inq Header Val Editing PH -> Total Offeri Amt Val Editing PH -> Transecti After Editing Tax PH
   - detail: flows/04340001.md ; trace prefix `63:27:04340001`
18. **seq 29 - Order Cancellation R2 TH** (`00040001`) - area: Order Cancellation
   - actor: same session (Auto_PH)
   - checks: 2 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Order Cancellation -> Order Cancellation Detail -> Order Cancellation Detail_Val
   - detail: flows/00040001.md ; trace prefix `63:29:00040001`
19. **seq 31 - Free SKU Stock Validation after Order Cancellation R2 PH** (`05590001`) - area: Order Cancellation, Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: FreeSKU_Val_Aft_OrdrCancel_1_PH -> FreeSKU_Val_Aft_OrdrCancel_2_PH -> FreeSKU_Val_Aft_OrdrCancel_3_PH
   - detail: flows/05590001.md ; trace prefix `63:31:05590001`
20. **seq 32 - Delivery Date Change** (`00160001`) - area: Delivery Date Change
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery Date Change
   - detail: flows/00160001.md ; trace prefix `63:32:00160001`
21. **seq 33 - Goods Issue Note_PH** (`04380001`) - area: GIN (Goods Issue Note)
   - actor: same session (Auto_PH)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue Note PH -> G Issue Note CM Select PH -> G Issue Note Detail PH -> G Issue N Val Detail PH -> G Issue Note Forward PH
   - detail: flows/04380001.md ; trace prefix `63:33:04380001`
22. **seq 37 - Goods Issue Note Approval** (`00780001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_GINNO` from seq 33 (04380001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue Note Approval
   - detail: flows/00780001.md ; trace prefix `63:37:00780001`
23. **seq 38 - Free SKU Stock Validation after Goods Issue Note R2 PH** (`05610001`) - area: GIN (Goods Issue Note), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Free_SKU_Val_Aft_GIN_1_PH -> Free_SKU_Val_Aft_GIN_2_PH -> Free_SKU_Val_Aft_GIN_3_PH
   - detail: flows/05610001.md ; trace prefix `63:38:05610001`
24. **seq 39 - Stock Validation After GIN R2 PH** (`05200001`) - area: GIN (Goods Issue Note), Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_ValafterGIN3_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_GIN_R2_PH -> Stock_Val_after_GIN_2_R2_PH -> Stock_Val_after_GIN_3_R2_PH
   - detail: flows/05200001.md ; trace prefix `63:39:05200001`
25. **seq 40 - Trans Inq Validate after Goods Issue Not PH** (`04400001`) - area: GIN (Goods Issue Note), Transaction Inquiry
   - actor: same session (Auto_PH)
   - checks: 4 message/field assertion(s); value validations 4, Q2Q 0
   - screens: Tran Inq val aftr Good I Not PH -> Tran Inq Detail Val G I N PH -> Trans Inq Header Val G I N PH -> Total Offer Amt Val G I N PH -> Transecti After G I N Tax PH
   - detail: flows/04400001.md ; trace prefix `63:40:04400001`
26. **seq 41 - FRESH_SALES_RETURN Partial_PH** (`04440001`) - area: Sales Return
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `FRESH_SALES_RETURN_ASSR`, `FRESH_SAL_RETVal_Partial_ASSR`, `SaleRetDTL_SAVE_ASSR`; value validations 2, Q2Q 0
   - screens: FRESH_SALES_RETURN PH -> F_SALES_RETURN DTL Partial PH -> F SALES RETURN Val Partial PH
   - detail: flows/04440001.md ; trace prefix `63:41:04440001`
27. **seq 42 - Free SKU Stock Validation after Fresh Sales Return Partial R2 PH** (`05620001`) - area: Sales Return, Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: FreeSKU_Val_Aft_FreshRet_P_1_PH -> FreeSKU_Val_Aft_FreshRet_P_2_PH -> FreeSKU_Val_Aft_FreshRet_P_3_PH
   - detail: flows/05620001.md ; trace prefix `63:42:05620001`
28. **seq 43 - FRESH_SALES_RETURN Full PH** (`04450001`) - area: Sales Return
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `FRESH_SALES_RETURN_Full_ASSR`, `FRESH_SAL_RETURN_Val_Full_ASSR`; value validations 1, Q2Q 0
   - screens: FRESH SALES RETURN Full PH -> F_SALES_RETURN DTL_Full PH -> F SALES_RETURN Val Full PH
   - detail: flows/04450001.md ; trace prefix `63:43:04450001`
29. **seq 44 - Free SKU Stock Validation after Fresh Sales Return Full R2 PH** (`05630001`) - area: Sales Return, Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: FreeSKU_Val_Aft_FreshRet_F_1_PH -> FreeSKU_Val_Aft_FreshRet_F_2_PH -> FreeSKU_Val_Aft_FreshRet_F_3_PH
   - detail: flows/05630001.md ; trace prefix `63:44:05630001`
30. **seq 45 - Transaction Inq Val After Fresh Sales R Partial Full PH** (`04490001`) - area: Transaction Inquiry
   - actor: same session (Auto_PH)
   - checks: 4 message/field assertion(s); value validations 4, Q2Q 0
   - screens: Trans InqVal Aft Partial Ful PH -> Tra InqVal Fresh S R P DetlPH -> Tran InqVal Aft Fresh  H PH -> Tran Val Fresh Parti TOffer PH -> Trans Aft Fresh Partial Tax PH
   - detail: flows/04490001.md ; trace prefix `63:45:04490001`
31. **seq 46 - Cashmemo Status_PH** (`04390001`) - area: Cashmemo
   - actor: same session (Auto_PH)
   - checks: 2 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`; value validations 2, Q2Q 0
   - screens: Cashmemo Status PH -> Cashmemo Status Val PH
   - detail: flows/04390001.md ; trace prefix `63:46:04390001`
32. **seq 47 - Sale Return PH** (`04500001`) - area: Sales Return
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Vali_ASSR`, `Sales_Return_Val_ASSR`; value validations 2, Q2Q 0
   - screens: Sales Return PH -> Sales Return Detail PH -> Sales Return Validat PH
   - detail: flows/04500001.md ; trace prefix `63:47:04500001`
33. **seq 48 - Sales Return View Forward PH** (`04520001`) - area: Sales Return, Approval/Reject/Terminate
   - actor: same session (Auto_PH)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SReturn_AppvPromoSave_ASSR`, `SReturn_AppvPromoValid_ASSR`, `SReturn_AppvReject_ASSR`; value validations 3, Q2Q 0
   - screens: S Return View Forward PH -> S Return View Detl Forward PH -> S Return View Forward Valid PH
   - detail: flows/04520001.md ; trace prefix `63:48:04520001`
34. **seq 49 - SALES_RETURN Full PH** (`04530001`) - area: Sales Return
   - actor: same session (Auto_PH)
   - checks: 2 message/field assertion(s); group assertion sheet(s): `SALES_RFull_SavePro_ASSR`, `Sales_Return_Val_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return Full PH -> SALES_Retu Detil_Full PH -> Sales Return FullVal PH -> Sales R Full Forward PH
   - detail: flows/04530001.md ; trace prefix `63:49:04530001`
35. **seq 50 - Sales Return View Approval PH** (`04510001`) - area: Sales Return, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SalesR_ViewForwdPromo_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return View Appro PH -> Sales Re View Val Approval PH
   - detail: flows/04510001.md ; trace prefix `63:50:04510001`
36. **seq 51 - Trans Inq Validate after Sales Par Full PH** (`04540001`) - area: Transaction Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - checks: 4 message/field assertion(s); value validations 4, Q2Q 0
   - screens: Tran Val Aft S R Partial Ful PH -> Tra InqVal Sales R P F DetlPH -> Tran InqVal Aft Sales R H PH -> Tran Val Sales R P F TOffer PH -> Trans Aft Sale R Partial Tax PH
   - detail: flows/04540001.md ; trace prefix `63:51:04540001`
37. **seq 52 - Sales Return Status Change PH** (`04550001`) - area: Sales Return
   - actor: same session (Auto_PH)
   - consumes: `REPO_GINNO` from seq 33 (04380001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SR_StatsChang_DTL_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Ret Status Change PH -> Sales R Status Change Detail PH -> Sales R Status Change Val PH
   - detail: flows/04550001.md ; trace prefix `63:52:04550001`
38. **seq 57 - Deposit Slip Unposted Amount Validate** (`03260001`) - area: Deposit Slip, Transaction Inquiry
   - actor: same session (Auto_PH)
   - consumes: `REPO_GINNO` from seq 33 (04380001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`; value validations 1, Q2Q 0
   - screens: Deposit Slip Unposted -> Deposit Slip,Cash memos unPost -> Deposit slip Val Unposted
   - detail: flows/03260001.md ; trace prefix `63:57:03260001`
39. **seq 58 - Deposit Slip Multi Cheques** (`00140001`) - area: Deposit Slip
   - actor: same session (Auto_PH)
   - produces: `REPO_Deposit_Slip`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`, `Deposit_Slip_Outlet_ASSR`, `screenshot_ASSR`
   - screens: Deposit Slip -> Deposit Slip,Outlet
   - detail: flows/00140001.md ; trace prefix `63:58:00140001`
40. **seq 59 - Deposit Slip Cheque PH** (`04570001`) - area: Deposit Slip
   - actor: same session (Auto_PH)
   - consumes: `REPO_GINNO` from seq 33 (04380001)
   - produces: `REPO_Deposit_Slip`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip Cheque PH -> Deposit Slip,Cash memos PH -> Deposit Slip,Cash memos
   - detail: flows/04570001.md ; trace prefix `63:59:04570001`
41. **seq 60 - Deposit Slip Cash PH** (`04560001`) - area: Deposit Slip
   - actor: same session (Auto_PH)
   - consumes: `REPO_GINNO` from seq 33 (04380001)
   - produces: `REPO_Deposit_Slip`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DEPOSIT_SAVE_ASSR`
   - screens: Deposit Slip,Cash PH -> Deposit Slip,Cash memos,Cash PH
   - detail: flows/04560001.md ; trace prefix `63:60:04560001`
42. **seq 61 - Good Return Note** (`00090001`) - area: GRN (Goods Return Note)
   - actor: same session (Auto_PH)
   - consumes: `REPO_GRN No.` unresolved in group
   - produces: `REPO_GRNNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GRN_DTL_SAVE_ASSR`, `GRN_FORWARD_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Return Note -> Good Return Note Detail -> Good Return Note Detail_Valida -> Goods Return Note Forward
   - detail: flows/00090001.md ; trace prefix `63:61:00090001`
43. **seq 62 - Good Return Note Approval** (`00810001`) - area: GRN (Goods Return Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_GRNNO` from seq 61 (00090001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GRN_APPROVAL_ASSR`
   - screens: Good Return Note Approval
   - detail: flows/00810001.md ; trace prefix `63:62:00810001`
44. **seq 63 - Stock Validation After GRN R2 PH** (`05190001`) - area: GRN (Goods Return Note), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_ValafterGRN3_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_GRN_R2_PH -> Stock_Val_after_GRN_2_R2_PH -> Stock_Val_after_GRN_3_R2_PH
   - detail: flows/05190001.md ; trace prefix `63:63:05190001`
45. **seq 64 - Free SKU Stock Validation after Goods Return Note R2 PH** (`05650001`) - area: GRN (Goods Return Note), Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Free_SKU_Val_Aft_GRN_1_PH -> Free_SKU_Val_Aft_GRN_2_PH -> Free_SKU_Val_Aft_GRN_3_PH
   - detail: flows/05650001.md ; trace prefix `63:64:05650001`
46. **seq 65 - Route Settlement PH** (`04600001`) - area: Route Settlement
   - actor: same session (Auto_PH)
   - checks: 4 message/field assertion(s); value validations 4, Q2Q 0
   - screens: Route Settlement PH -> Route Settlement Validation PH -> Route Settlement Validation1PH -> Route Settlement Validation2PH -> Route Settlement Validation3PH
   - detail: flows/04600001.md ; trace prefix `63:65:04600001`
47. **seq 66 - OFFSET Amount Validate After Route Settlem PH** (`04620001`) - area: Route Settlement, Transaction Inquiry
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: T Inquiry Search outlet PH -> Validate Offset amount PH
   - detail: flows/04620001.md ; trace prefix `63:66:04620001`
48. **seq 68 - Cheque Status** (`00660001`) - area: Cheque
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Cheque_Status_ASSR`
   - screens: Cheque Status
   - detail: flows/00660001.md ; trace prefix `63:68:00660001`
49. **seq 69 - DSR Adjustment Amount** (`00670001`) - area: DSR/PJP/Route
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DSR_ADJ_AMOUNT_ASSR`; value validations 1, Q2Q 0
   - screens: DSR Adjustment Amount -> DSR Adjustment Amount,Detail
   - detail: flows/00670001.md ; trace prefix `63:69:00670001`
50. **seq 70 - PJP Daily Inquiry Update PH** (`04640001`) - area: DSR/PJP/Route
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `PJP_Inquiry_ASSR`
   - screens: PJP Daily PH -> PJP Daily2 PH
   - detail: flows/04640001.md ; trace prefix `63:70:04640001`
51. **seq 71 - OTC Stock Out R2 PH** (`05220001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: OTC Stock Out R2 PH -> OTC Stock Out Det R2 PH -> OTC Stock Out Fwd R2 PH
   - detail: flows/05220001.md ; trace prefix `63:71:05220001`
52. **seq 72 - SAN Approval PH** (`05150001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_DocumentNo` from seq 71 (05220001); `REPO_DocumentType` from seq 71 (05220001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN Approval PH
   - detail: flows/05150001.md ; trace prefix `63:72:05150001`
53. **seq 73 - Opening & Closing Stock Validation R2 PH** (`05230001`) - area: Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Open_CloseStockVal3_ASSR`; value validations 1, Q2Q 0
   - screens: Open_Close_Stock_Val_R2_PH -> Open_Close_Stock_Val2_R2_PH -> Open_Close_Stock_Val3_R2_PH
   - detail: flows/05230001.md ; trace prefix `63:73:05230001`
54. **seq 74 - Free SKU Stock Validation after Order Booking R2 PH** (`05330001`) - area: Order Booking, Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Free_SKU_Val_Aft_OB_1_PH -> Free_SKU_Val_Aft_OB_2_PH -> Free_SKU_Val_Aft_OB_3_PH
   - detail: flows/05330001.md ; trace prefix `63:74:05330001`
55. **seq 75 - Free SKU Stock Validation after Order Booking R2 PH** (`05330001`) - area: Order Booking, Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Free_SKU_Val_Aft_OB_1_PH -> Free_SKU_Val_Aft_OB_2_PH -> Free_SKU_Val_Aft_OB_3_PH
   - detail: flows/05330001.md ; trace prefix `63:75:05330001`

## Inactive rows (skipped by the engine)
- seq 4 Dispatch Advice Negative (`00100002`) status N
- seq 5 Dispatch Advice Rejection (`00740002`) status N
- seq 10 Dispatch Advice Loss Approval (`00760001`) status N
- seq 34 Goods Issue Note Terminat Approval (`00780003`) status N
- seq 36 Goods Issue N Rejection Approval (`00780002`) status N
- seq 54 Transfer_To_Factory_Astron (`02770001`) status N
- seq 55 Deposit Slip Full Amount Cash (`03230001`) status N
- seq 56 Deposit Slip Full Amount Cheque (`03240001`) status N
- seq 67 Deposit Slip Cash removal PH (`04630001`) status N
