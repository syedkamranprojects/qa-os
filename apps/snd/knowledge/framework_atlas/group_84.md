# Group 84 - Validate Budget Capping with Free SKU Promotion PH Negative

Source `gtf:84`. Market guess (from name): PH. Rows: 17 (active 17, inactive 0). User switch points: 6 (5, 8, 9, 11, 12, 18).

Allowed apps (alg): app 6 PHP_CentegyQA -> D:/Selenium/Automation/PHP_QA// (workbook variant inferred: PHP)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `84:1:021400000`
2. **seq 2 - Order Booking SDMS-10080** (`04790001`) - area: Order Booking
   - actor: same session (runner default login)
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Order Booking SDMS -> Order Booking Detail SDMS -> Order Booking Detail2 SDMS
   - detail: flows/04790001.md ; trace prefix `84:2:04790001`
3. **seq 3 - Validate Budget Capping with Free SKU Promo Stock Unavailable PH SDMS 10080** (`06120001`) - area: Transaction Inquiry, Promotion
   - actor: same session (runner default login)
   - consumes: `ORDERNUMBER` from seq 2 (04790001)
   - checks: 5 message/field assertion(s); value validations 5, Q2Q 0
   - screens: Valid Budget Capping Free SKU -> Valid Budget Capping Free SKU2 -> Valid Budget Capping Free SKU3 -> Valid Budget Capping Free SKU4 -> Valid Budget Capping Free SKU5 -> Valid Budget Capping Free SKU6
   - detail: flows/06120001.md ; trace prefix `84:3:06120001`
4. **seq 4 - Current Promotion SDMS-10080** (`04810001`) - area: Promotion
   - actor: same session (runner default login)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status SDMS
   - detail: flows/04810001.md ; trace prefix `84:4:04810001`
5. **seq 5 - Budget Setup - Promotion Code Validation PH SDMS** (`06110001`) - area: Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Budget Setup
   - detail: flows/06110001.md ; trace prefix `84:5:06110001`
6. **seq 7 - SAN (Admin)SDMS-10080** (`04980001`) - area: Stock Adjustment (SAN)
   - actor: same session (runner default login)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Admin SDMS -> SAN Admin Detail SDMS -> SAN Admin Forward SDMS
   - detail: flows/04980001.md ; trace prefix `84:7:04980001`
7. **seq 8 - San Approval SDMS-10080** (`05010001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_DocumentNo` from seq 7 (04980001); `REPO_DocumentType` from seq 7 (04980001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP SDMS 10080
   - detail: flows/05010001.md ; trace prefix `84:8:05010001`
8. **seq 9 - Delivery Date Change SDMS-10080** (`05090001`) - area: Delivery Date Change
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery Date ChangeSDMS-10080
   - detail: flows/05090001.md ; trace prefix `84:9:05090001`
9. **seq 10 - Goods Issue Note_SDMS-10080** (`05020001`) - area: GIN (Goods Issue Note)
   - actor: same session (Auto_PH)
   - consumes: `ORDERNUMBER` from seq 2 (04790001); `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue N SDMS10080 -> G Issue N CM select SDMS-10080 -> G Issue N Detail SDMS-10080 -> G Issue N Val Dita SDMS-10080 -> G Issue N Forward SDMS-10080
   - detail: flows/05020001.md ; trace prefix `84:10:05020001`
10. **seq 11 - Goods Issue Note ApprSDMS-10080** (`05030001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_GINNO` from seq 10 (05020001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue N App SDMS-10080
   - detail: flows/05030001.md ; trace prefix `84:11:05030001`
11. **seq 12 - Promotion Remova SDMS-10080** (`05110001`) - area: Transaction Inquiry, Promotion
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `ORDERNUMBER` from seq 2 (04790001)
   - checks: value validations 1, Q2Q 0
   - screens: T Inq  Val Remove SDMS-10080 -> Trans Val offrin R SDMS-10080
   - detail: flows/05110001.md ; trace prefix `84:12:05110001`
12. **seq 13 - Promotion Remova SDMS-4605** (`05540001`) - area: Transaction Inquiry, Promotion
   - actor: same session (Auto_PH)
   - consumes: `ORDERNUMBER` from seq 2 (04790001)
   - checks: value validations 1, Q2Q 0
   - screens: T Inq  Val Remove SDMS 4605 -> Trans Val offrin R SDMS 4605
   - detail: flows/05540001.md ; trace prefix `84:13:05540001`
13. **seq 14 - Transaction Inq Validation SDMS-10080** (`04800001`) - area: Transaction Inquiry
   - actor: same session (Auto_PH)
   - consumes: `ORDERNUMBER` from seq 2 (04790001)
   - checks: 3 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Trans InquiryVal AfterOB SDMS -> Transa Valid offring OB SDMS -> Valid Budget Capping Free SKU5 -> Valid Budget Capping Free SKU6
   - detail: flows/04800001.md ; trace prefix `84:14:04800001`
14. **seq 15 - Current Promotion SDMS-10080** (`04810001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Current Promotion Status SDMS
   - detail: flows/04810001.md ; trace prefix `84:15:04810001`
15. **seq 16 - Budget Setup - Promotion Code Validation PH SDMS** (`06110001`) - area: Promotion
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Budget Setup
   - detail: flows/06110001.md ; trace prefix `84:16:06110001`
16. **seq 17 - SAN Stock Zero(SDMS-10080** (`05120001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - actor: same session (Auto_PH)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Stock Zero SDMS 10080 -> SAN Stock Zero Detail SDMS -> SAN Stock Zero Forw SDMS
   - detail: flows/05120001.md ; trace prefix `84:17:05120001`
17. **seq 18 - San Approval SDMS-10080** (`05010001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_DocumentNo` from seq 17 (05120001); `REPO_DocumentType` from seq 17 (05120001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP SDMS 10080
   - detail: flows/05010001.md ; trace prefix `84:18:05010001`
