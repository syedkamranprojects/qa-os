# Group 83 - Positive SDMS-10080 BD (R1, independent ids)

Source `gtf:83`. Market guess (from name): BD. Rows: 36 (active 30, inactive 6). User switch points: 12 (5, 6, 20, 21, 22, 23, 31, 32, 35, 36, 37, 38).

Allowed apps (alg): app 7 BD_Centegy QA -> D:/Selenium/Automation/BD_QA// (workbook variant inferred: Bangla)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 3 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `83:3:021400000`
2. **seq 4 - SAN (Admin)SDMS-1008** (`05790001`) - area: Stock Adjustment (SAN)
   - actor: same session (runner default login)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Admin SDMS -> SAN Admin Detail SDMS -> SAN Admin Forward SDMS
   - detail: flows/05790001.md ; trace prefix `83:4:05790001`
3. **seq 5 - San Approval SDMS-1008** (`05800001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_DocumentNo` from seq 4 (05790001); `REPO_DocumentType` from seq 4 (05790001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP SDMS 1008
   - detail: flows/05800001.md ; trace prefix `83:5:05800001`
4. **seq 6 - Order Booking Positiv SDMS-1008** (`05810001`) - area: Order Booking
   - **SWITCH USER POINT**: log out and log in as **Auto_Bangla** (serial 10)
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: O Booking positive SDMS-1008 -> O Booking Det Positi SDMS-1008 -> O Booking Det2 Posit SDMS-1008
   - detail: flows/05810001.md ; trace prefix `83:6:05810001`
5. **seq 7 - Trans Section Validate Promotion apply SDMS CL** (`05820001`) - area: Transaction Inquiry, Promotion, Master/Setup
   - actor: same session (Auto_Bangla)
   - consumes: `ORDERNUMBER` from seq 6 (05810001)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: T Section Promotion SDMS 10080 -> T S Promotion Offer SDMS 10080
   - detail: flows/05820001.md ; trace prefix `83:7:05820001`
6. **seq 9 - Current Promotion Positive SDMS-1008** (`05840001`) - area: Promotion
   - actor: same session (Auto_Bangla)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status2 SDMS -> C Promotion Val Status2 SDMS
   - detail: flows/05840001.md ; trace prefix `83:9:05840001`
7. **seq 11 - Order Cancellation SDMS-10080 CL** (`05860001`) - area: Order Cancellation
   - actor: same session (Auto_Bangla)
   - checks: 2 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Order Cancellation SDMS Positiv -> Order Cancell Det SDMS Positive -> Ord Cancel Deta_Val SDMS Posit
   - detail: flows/05860001.md ; trace prefix `83:11:05860001`
8. **seq 12 - Current Promotion Positive (3)SDMS-1008** (`05870001`) - area: Promotion
   - actor: same session (Auto_Bangla)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status3 SDMS
   - detail: flows/05870001.md ; trace prefix `83:12:05870001`
9. **seq 13 - Stock Allocation_Positive CL** (`05880001`) - area: Stock Allocation
   - actor: same session (Auto_Bangla)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Allocation_ASSR`
   - screens: Stock Allocation Positive CL
   - detail: flows/05880001.md ; trace prefix `83:13:05880001`
10. **seq 14 - Order Editing BD CL_SDMS** (`05890001`) - area: Order Editing
   - actor: same session (Auto_Bangla)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`, `Order_Editing_Teasting_ASSR`; value validations 2, Q2Q 0
   - screens: Order Editing Positive SDMS -> O Editing Detail Positive SDMS -> O Editing Detail3 positive SDMS
   - detail: flows/05890001.md ; trace prefix `83:14:05890001`
11. **seq 15 - Current Promotion Positive (4) CL SDMS** (`05900001`) - area: Promotion
   - actor: same session (Auto_Bangla)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status4 SDMS
   - detail: flows/05900001.md ; trace prefix `83:15:05900001`
12. **seq 17 - Stock Unallocation BD CL Positive _SDMS** (`05920001`) - area: Stock Allocation, Promotion
   - actor: same session (Auto_Bangla)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Unallocated_ASSR`
   - screens: Stock Unallocation BD
   - detail: flows/05920001.md ; trace prefix `83:17:05920001`
13. **seq 18 - Delivery Date Change BD CL SDMS** (`05930001`) - area: Delivery Date Change
   - actor: same session (Auto_Bangla)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery D Change Positive SDMS
   - detail: flows/05930001.md ; trace prefix `83:18:05930001`
14. **seq 19 - Goods Issue Note BD Positive CL _SDMS** (`05940001`) - area: GIN (Goods Issue Note)
   - actor: same session (Auto_Bangla)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue N 2 SDMS -> G Issue N CM selec 2 SDMS -> G Issue N Detail 2 SDMS -> G Issue N Val Dita 2 SDMS -> G Issue N Forward 2 SDMS
   - detail: flows/05940001.md ; trace prefix `83:19:05940001`
15. **seq 20 - Goods Issue Note Appr BD CL SDMS** (`05950001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_GINNO` from seq 19 (05940001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue N App BD CL SDMS
   - detail: flows/05950001.md ; trace prefix `83:20:05950001`
16. **seq 21 - Goods Issue Note Positive(3) BD CL_SDMS** (`05960001`) - area: GIN (Goods Issue Note)
   - **SWITCH USER POINT**: log out and log in as **Auto_Bangla** (serial 10)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue N 3 SDMS -> G Issue N CM selec 3 SDMS -> G Issue N Detail 3 SDMS -> G Issue N Val Dita 3 SDMS -> G Issue N Forward 3 SDMS
   - detail: flows/05960001.md ; trace prefix `83:21:05960001`
17. **seq 22 - Goods Issue Note Appr BD CL SDMS** (`05950001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_GINNO` from seq 21 (05960001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue N App BD CL SDMS
   - detail: flows/05950001.md ; trace prefix `83:22:05950001`
18. **seq 23 - Current Promotion Positive BD CL (5) SDMS** (`05970001`) - area: Promotion
   - **SWITCH USER POINT**: log out and log in as **Auto_Bangla** (serial 10)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status 5 SDMS
   - detail: flows/05970001.md ; trace prefix `83:23:05970001`
19. **seq 25 - Fresh Return partial BD CL SDMS** (`05990001`) - area: Sales Return
   - actor: same session (Auto_Bangla)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `FRESH_SALES_RETURN_ASSR`, `FRESH_SAL_RETVal_Partial_ASSR`, `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Valid_ASSR`; value validations 1, Q2Q 0
   - screens: Fresh_Sale_Partial_SDMS -> Fresh SDetil Partial SDMS -> Fresh S Val Partial SDMS
   - detail: flows/05990001.md ; trace prefix `83:25:05990001`
20. **seq 26 - Current Promotion Positive BD CL (6)SDMS** (`06000001`) - area: Promotion
   - actor: same session (Auto_Bangla)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status 6 SDMS
   - detail: flows/06000001.md ; trace prefix `83:26:06000001`
21. **seq 28 - Cashmemo Status BD CL SDMS** (`06020001`) - area: Cashmemo
   - actor: same session (Auto_Bangla)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`
   - screens: Cashmemo Status SDMS
   - detail: flows/06020001.md ; trace prefix `83:28:06020001`
22. **seq 29 - Cashmemo Status BD CL SDMS** (`06020001`) - area: Cashmemo
   - actor: same session (Auto_Bangla)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`
   - screens: Cashmemo Status SDMS
   - detail: flows/06020001.md ; trace prefix `83:29:06020001`
23. **seq 30 - Sale Return BD CL SDMS** (`06030001`) - area: Sales Return
   - actor: same session (Auto_Bangla)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Vali_ASSR`, `Sales_Return_Val_ASSR`; value validations 2, Q2Q 0
   - screens: Sales Return SDMS -> Sales Return Detail SDMS -> Sales Return Validat SDMS
   - detail: flows/06030001.md ; trace prefix `83:30:06030001`
24. **seq 31 - Sales Return View Approval SDMS** (`06040001`) - area: Sales Return, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SalesR_ViewForwdPromo_ASSR`
   - screens: Sales Return V Appro SDMS
   - detail: flows/06040001.md ; trace prefix `83:31:06040001`
25. **seq 32 - Current Promotion Positive BD CL (7) SDMS** (`06050001`) - area: Promotion
   - **SWITCH USER POINT**: log out and log in as **Auto_Bangla** (serial 10)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status 7 SDMS
   - detail: flows/06050001.md ; trace prefix `83:32:06050001`
26. **seq 34 - Good Return Note BD CL SDMS** (`06070001`) - area: GRN (Goods Return Note)
   - actor: same session (Auto_Bangla)
   - consumes: `REPO_GRN No.` unresolved in group
   - produces: `REPO_GRNNO`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GRN_DTL_SAVE_ASSR`, `GRN_FORWARD_ASSR`
   - screens: Goods Return Note SDMS -> GRN Detail SDMS -> GRN Forward SDMS -> GRN Detail Validat SDMS
   - detail: flows/06070001.md ; trace prefix `83:34:06070001`
27. **seq 35 - Good Return Note Approval BD CL SDMS** (`06080001`) - area: GRN (Goods Return Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_GRNNO` from seq 34 (06070001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GRN_APPROVAL_ASSR`
   - screens: Good Return Note Approval SDMS
   - detail: flows/06080001.md ; trace prefix `83:35:06080001`
28. **seq 36 - SAN (Out the Stock)BD CL SDMS** (`06090001`) - area: Stock Adjustment (SAN)
   - **SWITCH USER POINT**: log out and log in as **Auto_Bangla** (serial 10)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Out The Stock SDMS -> SAN Out The Stock Detail SDMS -> SAN Out The Stock Forwa SDMS
   - detail: flows/06090001.md ; trace prefix `83:36:06090001`
29. **seq 37 - San Approval SDMS-1008** (`05800001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_DocumentNo` from seq 36 (06090001); `REPO_DocumentType` from seq 36 (06090001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP SDMS 1008
   - detail: flows/05800001.md ; trace prefix `83:37:05800001`
30. **seq 38 - Stock Inq Validation BD CL SDMS** (`06100001`) - area: Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Bangla** (serial 10)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_ValafterGIN3_ASSR`; value validations 1, Q2Q 0
   - screens: Stock Inq SDMS -> Stock Inq Val 2 SDMS -> Stock Inq Val 3 SDMS
   - detail: flows/06100001.md ; trace prefix `83:38:06100001`

## Inactive rows (skipped by the engine)
- seq 8 Trans Section Validate Promotion apply SDMS-4605 CL (`05830001`) status N
- seq 10 Current Promotion Positive (24) SDMS-460 (`05850001`) status N
- seq 16 Current Promotion Positive (4)SDMS-460 (`05910001`) status N
- seq 24 Current Promotion Positive (5)SDMS-460 (`05980001`) status N
- seq 27 Current Promotion Positive (6)SDMS-460 (`06010001`) status N
- seq 33 Current Promotion Positive (7) SDMS-460 (`06060001`) status N
