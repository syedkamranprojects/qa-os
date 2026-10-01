# Group 72 - SAN Group Flow VN

Source `gtf:72`. Market guess (from name): VN. Rows: 10 (active 10, inactive 0). User switch points: 10 (1, 2, 3, 4, 5, 6, 7, 8, 9, 10).

Allowed apps (alg): app 16 VN_Centegy QA -> D:/Selenium/Automation/VN_QA// (workbook variant inferred: Vietnam)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `72:1:021400000`
2. **seq 2 - SAN Admin R2 VN** (`04410001`) - area: Stock Adjustment (SAN)
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Admin R2 VN -> SAN Admin Detail R2 VN -> SAN Admin Forward R2 VN
   - detail: flows/04410001.md ; trace prefix `72:2:04410001`
3. **seq 3 - SAN Approval R2 VN** (`04280001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **AUTO_TSSM_VAT** (serial 38)
   - consumes: `REPO_DocumentNo` from seq 2 (04410001); `REPO_DocumentType` from seq 2 (04410001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP R2 VN
   - detail: flows/04280001.md ; trace prefix `72:3:04280001`
4. **seq 4 - Stock Validation after SAN (Admin) VN** (`04460001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **AUTO_VAT** (serial 37)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_SAN_admin_VN -> Stock_Val_after_SAN_admin2_VN -> Stock_Val_after_SAN_admin3_VN
   - detail: flows/04460001.md ; trace prefix `72:4:04460001`
5. **seq 5 - SAN (Warehouse to Warehouse) R2 VN** (`04420001`) - area: Stock Adjustment (SAN), Master/Setup
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Ware2Ware R2 VN -> SAN W2W DetailR2 VN -> SAN W2W Forward R2 VN
   - detail: flows/04420001.md ; trace prefix `72:5:04420001`
6. **seq 6 - SAN Approval R2 VN** (`04280001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **AUTO_TSSM_VAT** (serial 38)
   - consumes: `REPO_DocumentNo` from seq 5 (04420001); `REPO_DocumentType` from seq 5 (04420001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP R2 VN
   - detail: flows/04280001.md ; trace prefix `72:6:04280001`
7. **seq 7 - Stock Validation After SAN (W to W) VN** (`04470001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **AUTO_VAT** (serial 37)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `screenshot_ASSR`; value validations 1, Q2Q 0
   - screens: Stock_Val_after_SAN_W2W_VN -> Stock_Val_after_SAN_W2W2_VN -> Stock_Val_after_SAN_W2W3_VN
   - detail: flows/04470001.md ; trace prefix `72:7:04470001`
8. **seq 8 - SAN (Entry) R2 VN** (`04430001`) - area: Stock Adjustment (SAN)
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DocumentNo`, `REPO_DocumentType`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SAN_FWD_ASSR`
   - screens: SAN Entry R2 VN -> SAN Entry Detail R2 VN -> SAN Entry Forward R2 VN
   - detail: flows/04430001.md ; trace prefix `72:8:04430001`
9. **seq 9 - SAN Approval R2 VN** (`04280001`) - area: Stock Adjustment (SAN), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **AUTO_TSSM_VAT** (serial 38)
   - consumes: `REPO_DocumentNo` from seq 8 (04430001); `REPO_DocumentType` from seq 8 (04430001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SAN_APP_ASSR`
   - screens: SAN APP R2 VN
   - detail: flows/04280001.md ; trace prefix `72:9:04280001`
10. **seq 10 - Stock Validation after SAN (Entry) VN** (`04480001`) - area: Stock Adjustment (SAN), Stock Validation/Inquiry
   - **SWITCH USER POINT**: log out and log in as **AUTO_VAT** (serial 37)
   - checks: none configured
   - screens: 
   - detail: flows/04480001.md ; trace prefix `72:10:04480001`
