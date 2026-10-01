# Group 80 - Positive SDMS-10080 PH

Source `gtf:80`. Market guess (from name): PH. Rows: 36 (active 36, inactive 0). User switch points: 12 (3, 4, 18, 19, 20, 21, 29, 30, 33, 34, 35, 36).

Allowed apps (alg): app 6 PHP_CentegyQA -> D:/Selenium/Automation/PHP_QA// (workbook variant inferred: PHP)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `80:1:021400000`
2. **seq 2 - SAN (Admin)SDMS-10080** (`04980001`) - area: Stock Adjustment (SAN)
   - actor: same session (runner default login)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Admin SDMS -> SAN Admin Detail SDMS -> SAN Admin Forward SDMS
   - detail: flows/04980001.md ; trace prefix `80:2:04980001`
3. **seq 3 - San Approval SDMS-10080** (`05010001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_DocumentNo` from seq 2 (04980001); `REPO_DocumentType` from seq 2 (04980001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP SDMS 10080
   - detail: flows/05010001.md ; trace prefix `80:3:05010001`
4. **seq 4 - Order Booking Positiv SDMS-10080** (`05130001`) - area: Order Booking
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: O Booking positive SDMS-10080 -> O Booking Det Positi SDMS-10080 -> O Booking Det2 Posit SDMS-10080
   - detail: flows/05130001.md ; trace prefix `80:4:05130001`
5. **seq 5 - Trans Section Validate Promotion apply SDMS** (`05160001`) - area: Transaction Inquiry, Promotion, Master/Setup
   - actor: same session (Auto_PH)
   - consumes: `ORDERNUMBER` from seq 4 (05130001)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: T Section Promotion SDMS 10080 -> T S Promotion Offer SDMS 10080
   - detail: flows/05160001.md ; trace prefix `80:5:05160001`
6. **seq 6 - Trans Section Validate Promotion apply SDMS-4605** (`05520001`) - area: Transaction Inquiry, Promotion, Master/Setup
   - actor: same session (Auto_PH)
   - consumes: `ORDERNUMBER` from seq 4 (05130001)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: T Section Promotion SDMS 4605 -> T S Promotion Offer SDMS 4605
   - detail: flows/05520001.md ; trace prefix `80:6:05520001`
7. **seq 7 - Current Promotion Positive SDMS-10080** (`05240001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status2 SDMS -> C Promotion Val Status2 SDMS
   - detail: flows/05240001.md ; trace prefix `80:7:05240001`
8. **seq 8 - Current Promotion Positive (8) SDMS-4605** (`05430001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion S 2 SDMS 4605
   - detail: flows/05430001.md ; trace prefix `80:8:05430001`
9. **seq 9 - Order Cancellation SDMS-10080** (`05250001`) - area: Order Cancellation
   - actor: same session (Auto_PH)
   - checks: 2 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Order Cancellation SDMS 10080 -> Order Cancellat Deti SDMS 10080 -> Ord Cancel Deta_Val SDMS 10080
   - detail: flows/05250001.md ; trace prefix `80:9:05250001`
10. **seq 10 - Current Promotion Positive (3)SDMS-10080** (`05270001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status3 SDMS
   - detail: flows/05270001.md ; trace prefix `80:10:05270001`
11. **seq 11 - Stock Allocation_PH** (`04320001`) - area: Stock Allocation
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Allocation_ASSR`
   - screens: Stock Allocation PH
   - detail: flows/04320001.md ; trace prefix `80:11:04320001`
12. **seq 12 - Order Editing_SDMS-10080** (`05280001`) - area: Order Editing
   - actor: same session (Auto_PH)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`, `Order_Editing_Teasting_ASSR`; value validations 2, Q2Q 0
   - screens: Order Editing SDMS-10080 -> Order Editing Detail SDMS-10080 -> Order Editing Detail3 PH
   - detail: flows/05280001.md ; trace prefix `80:12:05280001`
13. **seq 13 - Current Promotion Positive (4)SDMS-10080** (`05290001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status4 SDMS
   - detail: flows/05290001.md ; trace prefix `80:13:05290001`
14. **seq 14 - Current Promotion Positive (4)SDMS-4605** (`05470001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion S 4 SDMS 4605
   - detail: flows/05470001.md ; trace prefix `80:14:05470001`
15. **seq 15 - Stock Unallocation_PH** (`03380001`) - area: Stock Allocation, Promotion
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Unallocated_ASSR`
   - screens: Stock Unallocation
   - detail: flows/03380001.md ; trace prefix `80:15:03380001`
16. **seq 16 - Delivery Date Change SDMS-10080** (`05090001`) - area: Delivery Date Change
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery Date ChangeSDMS-10080
   - detail: flows/05090001.md ; trace prefix `80:16:05090001`
17. **seq 17 - Goods Issue Note Positive_SDMS-10080** (`05300001`) - area: GIN (Goods Issue Note)
   - actor: same session (Auto_PH)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue N 2 SDMS10080 -> G Issue N CM selec 2 SDMS-10080 -> G Issue N Detail 2 SDMS-10080 -> G Issue N Val Dita 2 SDMS-10080 -> G Issue N Forward 2 SDMS-10080
   - detail: flows/05300001.md ; trace prefix `80:17:05300001`
18. **seq 18 - Goods Issue Note ApprSDMS-10080** (`05030001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_GINNO` from seq 17 (05300001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue N App SDMS-10080
   - detail: flows/05030001.md ; trace prefix `80:18:05030001`
19. **seq 19 - Goods Issue Note Positive(3)_SDMS-10080** (`05310001`) - area: GIN (Goods Issue Note)
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue N 3 SDMS10080 -> G Issue N CM selec 3 SDMS-10080 -> G Issue N Detail 3 SDMS-10080 -> G Issue N Val Dita 3 SDMS-10080 -> G Issue N Forward 3 SDMS-10080
   - detail: flows/05310001.md ; trace prefix `80:19:05310001`
20. **seq 20 - Goods Issue Note ApprSDMS-10080** (`05030001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_GINNO` from seq 19 (05310001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue N App SDMS-10080
   - detail: flows/05030001.md ; trace prefix `80:20:05030001`
21. **seq 21 - Current Promotion Positive (5)SDMS-10080** (`05320001`) - area: Promotion
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status 5 SDMS
   - detail: flows/05320001.md ; trace prefix `80:21:05320001`
22. **seq 22 - Current Promotion Positive (5)SDMS-4605** (`05480001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion S 5 SDMS 4605
   - detail: flows/05480001.md ; trace prefix `80:22:05480001`
23. **seq 23 - Fresh Return partial SDMS-10080** (`05340001`) - area: Sales Return
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `FRESH_SALES_RETURN_ASSR`, `FRESH_SAL_RETVal_Partial_ASSR`, `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Valid_ASSR`; value validations 1, Q2Q 0
   - screens: Fresh_Sale_Partial_SDMS-10080 -> Fresh SDetil Partial SDMS 10080 -> Fresh S Val Partial SDMS 10080
   - detail: flows/05340001.md ; trace prefix `80:23:05340001`
24. **seq 24 - Current Promotion Positive (6)SDMS-10080** (`05350001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status 6 SDMS
   - detail: flows/05350001.md ; trace prefix `80:24:05350001`
25. **seq 25 - Current Promotion Positive (6)SDMS-4605** (`05490001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion S 6 SDMS 4605
   - detail: flows/05490001.md ; trace prefix `80:25:05490001`
26. **seq 26 - Cashmemo Status SDMS-10080** (`05360001`) - area: Cashmemo
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`
   - screens: Cashmemo Status SDMS 10080
   - detail: flows/05360001.md ; trace prefix `80:26:05360001`
27. **seq 27 - Cashmemo Status SDMS-10080** (`05360001`) - area: Cashmemo
   - actor: same session (Auto_PH)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`
   - screens: Cashmemo Status SDMS 10080
   - detail: flows/05360001.md ; trace prefix `80:27:05360001`
28. **seq 28 - Sale Return SDMS** (`05370001`) - area: Sales Return
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Vali_ASSR`, `Sales_Return_Val_ASSR`; value validations 2, Q2Q 0
   - screens: Sales Return SDMS -> Sales Return Detail SDMS -> Sales Return Validat SDMS
   - detail: flows/05370001.md ; trace prefix `80:28:05370001`
29. **seq 29 - Sales Return View Approval SDMS** (`05380001`) - area: Sales Return, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SalesR_ViewForwdPromo_ASSR`
   - screens: Sales Return V Appro SDMS
   - detail: flows/05380001.md ; trace prefix `80:29:05380001`
30. **seq 30 - Current Promotion Positive (7) SDMS-10080** (`05400001`) - area: Promotion
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status 7 SDMS
   - detail: flows/05400001.md ; trace prefix `80:30:05400001`
31. **seq 31 - Current Promotion Positive (7) SDMS-4605** (`05510001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion S 7 SDMS 4605
   - detail: flows/05510001.md ; trace prefix `80:31:05510001`
32. **seq 32 - Good Return Note SDMS** (`05390001`) - area: GRN (Goods Return Note)
   - actor: same session (Auto_PH)
   - consumes: `REPO_GRN No.` unresolved in group
   - produces: `REPO_GRNNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GRN_DTL_SAVE_ASSR`, `GRN_FORWARD_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Return Note SDMS -> GRN Detail SDMS -> GRN Detail Validat SDMS -> GRN Forward SDMS
   - detail: flows/05390001.md ; trace prefix `80:32:05390001`
33. **seq 33 - Good Return Note Approval** (`00810001`) - area: GRN (Goods Return Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_GRNNO` from seq 32 (05390001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GRN_APPROVAL_ASSR`
   - screens: Good Return Note Approval
   - detail: flows/00810001.md ; trace prefix `80:33:00810001`
34. **seq 34 - SAN (Out the Stock)SDMS** (`05410001`) - area: Stock Adjustment (SAN)
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Out The Stock SDMS -> SAN Out The Stock Detail SDMS -> SAN Out The Stock Forwa SDMS
   - detail: flows/05410001.md ; trace prefix `80:34:05410001`
35. **seq 35 - San Approval SDMS-10080** (`05010001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_DocumentNo` from seq 34 (05410001); `REPO_DocumentType` from seq 34 (05410001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP SDMS 10080
   - detail: flows/05010001.md ; trace prefix `80:35:05010001`
36. **seq 36 - Stock Inq Validation SDMS** (`05420001`) - area: Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_ValafterGIN3_ASSR`; value validations 1, Q2Q 0
   - screens: Stock Inq SDMS -> Stock Inq Val 2 SDMS -> Stock Inq Val 3 SDMS
   - detail: flows/05420001.md ; trace prefix `80:36:05420001`
