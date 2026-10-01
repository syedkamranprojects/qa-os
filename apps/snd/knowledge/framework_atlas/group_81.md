# Group 81 - SDMS-10080 BD

Source `gtf:81`. Market guess (from name): BD. Rows: 13 (active 13, inactive 0). User switch points: 5 (6, 7, 9, 10, 13).

Allowed apps (alg): app 7 BD_Centegy QA -> D:/Selenium/Automation/BD_QA// (workbook variant inferred: Bangla)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `81:1:021400000`
2. **seq 2 - Order Booking BD SDMS-10080** (`05660001`) - area: Order Booking
   - actor: same session (runner default login)
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Order Booking BD SDMS -> Order Booking BD Detail SDMS -> Order Booking BD Detail2 SDMS
   - detail: flows/05660001.md ; trace prefix `81:2:05660001`
3. **seq 3 - Transaction Inq Validation BD SDMS-10080** (`05670001`) - area: Transaction Inquiry
   - actor: same session (runner default login)
   - consumes: `ORDERNUMBER` from seq 2 (05660001)
   - checks: 3 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Trans Inq BD Val After OB SDMS -> Transa Val BD offring OB SDMS -> Transa Val BD offring 3 OB SDMS -> Transa Val BD offring 4 OB SDMS
   - detail: flows/05670001.md ; trace prefix `81:3:05670001`
4. **seq 4 - Current Promotion BD SDMS-10080** (`05680001`) - area: Promotion
   - actor: same session (runner default login)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Curent Promotion BD Status SDMS
   - detail: flows/05680001.md ; trace prefix `81:4:05680001`
5. **seq 5 - SAN (Admin) BD SDMS-10080** (`05690001`) - area: Stock Adjustment (SAN)
   - actor: same session (runner default login)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Admin BD SDMS -> SAN Admin BD Detail SDMS -> SAN Admin BD Forward SDMS
   - detail: flows/05690001.md ; trace prefix `81:5:05690001`
6. **seq 6 - San Approval BD SDMS-10080** (`05700001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_DocumentNo` from seq 5 (05690001); `REPO_DocumentType` from seq 5 (05690001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP BD SDMS 10080
   - detail: flows/05700001.md ; trace prefix `81:6:05700001`
7. **seq 7 - Delivery Date Change BD SDMS-10080** (`05710001`) - area: Delivery Date Change
   - **SWITCH USER POINT**: log out and log in as **Auto_Bangla** (serial 10)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery D Change BD SDMS-10080
   - detail: flows/05710001.md ; trace prefix `81:7:05710001`
8. **seq 8 - Goods Issue Note_ BD SDMS-10080** (`05720001`) - area: GIN (Goods Issue Note)
   - actor: same session (Auto_Bangla)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue N BD SDMS10080 -> G Issue N CM sele BD SDMS10080 -> G Issue N Detail BD SDMS-10080 -> G Issue N Val Dit BD SDMS-10080 -> G Issue N Forwa BD SDMS-10080
   - detail: flows/05720001.md ; trace prefix `81:8:05720001`
9. **seq 9 - Goods Issue Note ApprSDMS-10080** (`05030001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_GINNO` from seq 8 (05720001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_SAVE_ASSR`
   - screens: Goods Issue N App SDMS-10080
   - detail: flows/05030001.md ; trace prefix `81:9:05030001`
10. **seq 10 - Promotion Remova BD SDMS-10080** (`05730001`) - area: Transaction Inquiry, Promotion
   - **SWITCH USER POINT**: log out and log in as **Auto_Bangla** (serial 10)
   - consumes: `ORDERNUMBER` from seq 2 (05660001)
   - checks: value validations 1, Q2Q 0
   - screens: T Inq  Val Remove BD SDMS-10080 -> Tran Val offrin R BD SDMS-10080
   - detail: flows/05730001.md ; trace prefix `81:10:05730001`
11. **seq 11 - Current Promotion BD SDMS-10080** (`05680001`) - area: Promotion
   - actor: same session (Auto_Bangla)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Curent Promotion BD Status SDMS
   - detail: flows/05680001.md ; trace prefix `81:11:05680001`
12. **seq 12 - SAN Stock Zero BD (SDMS-10080** (`05740001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - actor: same session (Auto_Bangla)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Stock Zero BD SDMS 10080 -> SAN Stock BD Zero Detail SDMS -> SAN Stock Zero BD Forw SDMS
   - detail: flows/05740001.md ; trace prefix `81:12:05740001`
13. **seq 13 - San Approval BD SDMS-10080** (`05700001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_DocumentNo` from seq 12 (05740001); `REPO_DocumentType` from seq 12 (05740001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP BD SDMS 10080
   - detail: flows/05700001.md ; trace prefix `81:13:05700001`
