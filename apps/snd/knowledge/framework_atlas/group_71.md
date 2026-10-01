# Group 71 - SAN Group Flow TH-PH

Source `gtf:71`. Market guess (from name): PH. Rows: 10 (active 10, inactive 0). User switch points: 9 (2, 3, 4, 5, 6, 7, 8, 9, 10).

Allowed apps (alg): app 12 ITHD_Centegy QA 2 -> D:/Selenium/Automation/ITHD_QA// (workbook variant inferred: None)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `71:1:021400000`
2. **seq 2 - SAN (Admin) R2** (`02870001`) - area: Stock Adjustment (SAN)
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Admin R2 -> SAN Admin Detail R2 -> SAN Admin Forward R2
   - detail: flows/02870001.md ; trace prefix `71:2:02870001`
3. **seq 3 - SAN Approval R2** (`02890001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_DocumentNo` from seq 2 (02870001); `REPO_DocumentType` from seq 2 (02870001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP R2
   - detail: flows/02890001.md ; trace prefix `71:3:02890001`
4. **seq 4 - Stock Validation after SAN (Admin)** (`02850001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_SAN_admin -> Stock_Val_after_SAN_admin2 -> Stock_Val_after_SAN_admin3
   - detail: flows/02850001.md ; trace prefix `71:4:02850001`
5. **seq 5 - SAN (Warehouse to Warehouse) R2** (`02880001`) - area: Stock Adjustment (SAN), Master/Setup
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Ware2WareR2 -> SAN W2W DetailR2 -> SAN W2W Forward R2
   - detail: flows/02880001.md ; trace prefix `71:5:02880001`
6. **seq 6 - SAN Approval R2** (`02890001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_DocumentNo` from seq 5 (02880001); `REPO_DocumentType` from seq 5 (02880001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP R2
   - detail: flows/02890001.md ; trace prefix `71:6:02890001`
7. **seq 7 - Stock Validation After SAN (W to W)** (`02860001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_SAN_W2W -> Stock_Val_after_SAN_W2W2 -> Stock_Val_after_SAN_W2W3
   - detail: flows/02860001.md ; trace prefix `71:7:02860001`
8. **seq 8 - SAN (Entry) R2** (`03670001`) - area: Stock Adjustment (SAN)
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Entry R2 -> SAN Entry Detail R2 -> SAN Entry Forward R2
   - detail: flows/03670001.md ; trace prefix `71:8:03670001`
9. **seq 9 - SAN Approval R2** (`02890001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_DocumentNo` from seq 8 (03670001); `REPO_DocumentType` from seq 8 (03670001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP R2
   - detail: flows/02890001.md ; trace prefix `71:9:02890001`
10. **seq 10 - Stock Validation after SAN (Entry)** (`03680001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_SAN_entry -> Stock_Val_after_SAN_entry2 -> Stock_Val_after_SAN_entry3
   - detail: flows/03680001.md ; trace prefix `71:10:03680001`
