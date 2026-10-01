# Group 70 - SAN Group Flow PAK

Source `gtf:70`. Market guess (from name): PK. Rows: 10 (active 10, inactive 0). User switch points: 10 (1, 2, 3, 4, 5, 6, 7, 8, 9, 10).

Allowed apps (alg): app 8 PK_Centegy QA 2 -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `70:1:021400000`
2. **seq 2 - SAN (Admin)** (`02840001`) - area: Stock Adjustment (SAN)
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Admin -> SAN Admin Detail -> SAN Admin Forward
   - detail: flows/02840001.md ; trace prefix `70:2:02840001`
3. **seq 3 - SAN Approval PAK** (`03500001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_DocumentNo` from seq 2 (02840001); `REPO_DocumentType` from seq 2 (02840001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN Approval PAK
   - detail: flows/03500001.md ; trace prefix `70:3:03500001`
4. **seq 4 - Stock Validation after SAN (Admin)** (`02850001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_SAN_admin -> Stock_Val_after_SAN_admin2 -> Stock_Val_after_SAN_admin3
   - detail: flows/02850001.md ; trace prefix `70:4:02850001`
5. **seq 5 - SAN (Warehouse to Warehouse)** (`00120001`) - area: Stock Adjustment (SAN), Master/Setup
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Warehouse2Warehouse -> SAN W2W Detail -> SAN W2W Forward
   - detail: flows/00120001.md ; trace prefix `70:5:00120001`
6. **seq 6 - SAN Approval PAK** (`03500001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_DocumentNo` from seq 5 (00120001); `REPO_DocumentType` from seq 5 (00120001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN Approval PAK
   - detail: flows/03500001.md ; trace prefix `70:6:03500001`
7. **seq 7 - Stock Validation After SAN (W to W)** (`02860001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_SAN_W2W -> Stock_Val_after_SAN_W2W2 -> Stock_Val_after_SAN_W2W3
   - detail: flows/02860001.md ; trace prefix `70:7:02860001`
8. **seq 8 - SAN (Entry) PK** (`03700001`) - area: Stock Adjustment (SAN)
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Entry -> SAN Entry Detail -> SAN Entry Forward
   - detail: flows/03700001.md ; trace prefix `70:8:03700001`
9. **seq 9 - SAN Approval PAK** (`03500001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_DocumentNo` from seq 8 (03700001); `REPO_DocumentType` from seq 8 (03700001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN Approval PAK
   - detail: flows/03500001.md ; trace prefix `70:9:03500001`
10. **seq 10 - Stock Validation after SAN (Entry)** (`03680001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_SAN_entry -> Stock_Val_after_SAN_entry2 -> Stock_Val_after_SAN_entry3
   - detail: flows/03680001.md ; trace prefix `70:10:03680001`
