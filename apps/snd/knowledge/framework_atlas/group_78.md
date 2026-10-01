# Group 78 - SDMS-10080PH

Source `gtf:78`. Market guess (from name): None. Rows: 19 (active 17, inactive 2). User switch points: 6 (9, 10, 11, 12, 13, 19).

Allowed apps (alg): app 6 PHP_CentegyQA -> D:/Selenium/Automation/PHP_QA// (workbook variant inferred: PHP)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `78:1:021400000`
2. **seq 2 - Order Booking SDMS-10080** (`04790001`) - area: Order Booking
   - actor: same session (runner default login)
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Order Booking SDMS -> Order Booking Detail SDMS -> Order Booking Detail2 SDMS
   - detail: flows/04790001.md ; trace prefix `78:2:04790001`
3. **seq 3 - Transaction Inq Validation SDMS-10080** (`04800001`) - area: Transaction Inquiry
   - actor: same session (runner default login)
   - consumes: `ORDERNUMBER` from seq 2 (04790001)
   - checks: 3 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Trans InquiryVal AfterOB SDMS -> Transa Valid offring OB SDMS -> Valid Budget Capping Free SKU5 -> Valid Budget Capping Free SKU6
   - detail: flows/04800001.md ; trace prefix `78:3:04800001`
4. **seq 4 - Transaction Inq Validation SDMS-4605** (`05530001`) - area: Transaction Inquiry
   - actor: same session (runner default login)
   - consumes: `ORDERNUMBER` from seq 2 (04790001)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Trans Inq Val Af OB SDMS 4605 -> Transa Val offring OB SDMS 4605
   - detail: flows/05530001.md ; trace prefix `78:4:05530001`
5. **seq 5 - Current Promotion SDMS-10080** (`04810001`) - area: Promotion
   - actor: same session (runner default login)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status SDMS
   - detail: flows/04810001.md ; trace prefix `78:5:04810001`
6. **seq 7 - Budget Setup - Promotion Code Validation PH SDMS** (`06110001`) - area: Promotion
   - actor: same session (runner default login)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Budget Setup
   - detail: flows/06110001.md ; trace prefix `78:7:06110001`
7. **seq 8 - SAN (Admin)SDMS-10080** (`04980001`) - area: Stock Adjustment (SAN)
   - actor: same session (runner default login)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Admin SDMS -> SAN Admin Detail SDMS -> SAN Admin Forward SDMS
   - detail: flows/04980001.md ; trace prefix `78:8:04980001`
8. **seq 9 - San Approval SDMS-10080** (`05010001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_DocumentNo` from seq 8 (04980001); `REPO_DocumentType` from seq 8 (04980001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP SDMS 10080
   - detail: flows/05010001.md ; trace prefix `78:9:05010001`
9. **seq 10 - Delivery Date Change SDMS-10080** (`05090001`) - area: Delivery Date Change
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery Date ChangeSDMS-10080
   - detail: flows/05090001.md ; trace prefix `78:10:05090001`
10. **seq 11 - Goods Issue Note_SDMS-10080** (`05020001`) - area: GIN (Goods Issue Note)
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19) (same user as before: re-login only)
   - consumes: `ORDERNUMBER` from seq 2 (04790001); `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue N SDMS10080 -> G Issue N CM select SDMS-10080 -> G Issue N Detail SDMS-10080 -> G Issue N Val Dita SDMS-10080 -> G Issue N Forward SDMS-10080
   - detail: flows/05020001.md ; trace prefix `78:11:05020001`
11. **seq 12 - Goods Issue Note ApprSDMS-10080** (`05030001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_GINNO` from seq 11 (05020001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue N App SDMS-10080
   - detail: flows/05030001.md ; trace prefix `78:12:05030001`
12. **seq 13 - Promotion Remova SDMS-10080** (`05110001`) - area: Transaction Inquiry, Promotion
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `ORDERNUMBER` from seq 2 (04790001)
   - checks: value validations 1, Q2Q 0
   - screens: T Inq  Val Remove SDMS-10080 -> Trans Val offrin R SDMS-10080
   - detail: flows/05110001.md ; trace prefix `78:13:05110001`
13. **seq 14 - Promotion Remova SDMS-4605** (`05540001`) - area: Transaction Inquiry, Promotion
   - actor: same session (Auto_PH)
   - consumes: `ORDERNUMBER` from seq 2 (04790001)
   - checks: value validations 1, Q2Q 0
   - screens: T Inq  Val Remove SDMS 4605 -> Trans Val offrin R SDMS 4605
   - detail: flows/05540001.md ; trace prefix `78:14:05540001`
14. **seq 15 - Current Promotion SDMS-10080** (`04810001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status SDMS
   - detail: flows/04810001.md ; trace prefix `78:15:04810001`
15. **seq 16 - Current Promotion Positive (7) SDMS-4605** (`05510001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion S 7 SDMS 4605
   - detail: flows/05510001.md ; trace prefix `78:16:05510001`
16. **seq 18 - SAN Stock Zero(SDMS-10080** (`05120001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Stock Zero SDMS 10080 -> SAN Stock Zero Detail SDMS -> SAN Stock Zero Forw SDMS
   - detail: flows/05120001.md ; trace prefix `78:18:05120001`
17. **seq 19 - San Approval SDMS-10080** (`05010001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_DocumentNo` from seq 18 (05120001); `REPO_DocumentType` from seq 18 (05120001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP SDMS 10080
   - detail: flows/05010001.md ; trace prefix `78:19:05010001`

## Inactive rows (skipped by the engine)
- seq 6 Current Promotion Positive (7) SDMS-4605 (`05510001`) status N
- seq 17 Budget Setup - Promotion Code Validation PH SDMS (`06110001`) status N
