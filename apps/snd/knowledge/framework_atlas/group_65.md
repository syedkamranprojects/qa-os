# Group 65 - NG_Setup Flow_TH

Source `gtf:65`. Market guess (from name): None. Rows: 45 (active 41, inactive 4). User switch points: 30 (5, 6, 7, 8, 10, 11, 12, 13, 15, 17, 18, 19, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 43).

Allowed apps (alg): app 12 ITHD_Centegy QA 2 -> D:/Selenium/Automation/ITHD_QA// (workbook variant inferred: None)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `65:1:021400000`
2. **seq 2 - User** (`00360001`) - area: Other
   - actor: same session (runner default login)
   - consumes: `REPO_CODE` produced within same flow
   - produces: `REPO_CODE`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Update_ASSR`
   - screens: User
   - detail: flows/00360001.md ; trace prefix `65:2:00360001`
3. **seq 3 - User Profile** (`00350001`) - area: Master/Setup
   - actor: same session (runner default login)
   - consumes: `REPO_CODE` from seq 2 (00360001); `REPO_LOCATIONCODE` unresolved in group
   - checks: none configured
   - screens: User Profile
   - detail: flows/00350001.md ; trace prefix `65:3:00350001`
4. **seq 4 - Warehouse Profile BG R2** (`02380001`) - area: Master/Setup
   - actor: same session (runner default login)
   - consumes: `REPO_WAREHOUSE` produced within same flow
   - produces: `REPO_WAREHOUSE`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`, `Save_ASSR`
   - screens: Warehouse Profile BG R2
   - detail: flows/02380001.md ; trace prefix `65:4:02380001`
5. **seq 5 - Warehouse Profile Appr-BG** (`02230001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_WAREHOUSE` from seq 4 (02380001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Warehouse Profile App-BG
   - detail: flows/02230001.md ; trace prefix `65:5:02230001`
6. **seq 6 - Vehicle Profile II** (`02180001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - consumes: `REPO_Vehicle_Code` produced within same flow
   - produces: `REPO_Vehicle_Code`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Vehicle Profile II
   - detail: flows/02180001.md ; trace prefix `65:6:02180001`
7. **seq 7 - Vehicle Profile Approval II** (`02160001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_Vehicle_Code` from seq 6 (02180001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Vehicle Profile Approval II
   - detail: flows/02160001.md ; trace prefix `65:7:02160001`
8. **seq 8 - Selling Category II** (`02170001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - produces: `REPO_Selling_Category_CODE`
   - checks: 2 message/field assertion(s)
   - screens: Selling Category II
   - detail: flows/02170001.md ; trace prefix `65:8:02170001`
9. **seq 9 - Section** (`00590001`) - area: Master/Setup
   - actor: same session (Auto_Th)
   - consumes: `REPO_OutletCode` unresolved in group; `REPO_SECTION_CODE` produced within same flow
   - produces: `REPO_SECTION_CODE`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Section -> Section Allowable -> Section Forward
   - detail: flows/00590001.md ; trace prefix `65:9:00590001`
10. **seq 10 - Section Approval** (`00720001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_SECTION_CODE` from seq 9 (00590001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Section Approval
   - detail: flows/00720001.md ; trace prefix `65:10:00720001`
11. **seq 11 - BG - Section Profile R2** (`02390001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - consumes: `REPO_SECTIONCODE_BG` produced within same flow
   - produces: `REPO_SECTIONCODE_BG`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`, `Update_assertion`
   - screens: BG_Section_Profile_R2 -> BG_Section_Profile_Allowable_R2 -> BG_Section_Profile_Forward_R2
   - detail: flows/02390001.md ; trace prefix `65:11:02390001`
12. **seq 12 - BG - Section Profile Approval** (`02370001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_SECTIONCODE_BG` from seq 11 (02390001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: BG-Section Profile Approve
   - detail: flows/02370001.md ; trace prefix `65:12:02370001`
13. **seq 13 - Outlet Profile_R2** (`02350001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - consumes: `REPO_OutletCode` produced within same flow
   - produces: `REPO_OutletCode`
   - checks: 8 message/field assertion(s); group assertion sheet(s): `OutletProfile_Address_ASSR`, `Save_ASSR`
   - screens: OutletProfile,Demograph_R2 -> OutletProfile,Oper_Info_R2 -> OutletProfile-Address_R2 -> OutletProfile-Address,Bus_R2 -> OutletProfile-Address,OtherR2 -> OutletProfile,Documents_R2 ...
   - detail: flows/02350001.md ; trace prefix `65:13:02350001`
14. **seq 14 - Prospect Outlet_R2** (`02400001`) - area: Master/Setup
   - actor: same session (Auto_Th)
   - consumes: `REPO_OutletCode` from seq 13 (02350001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Prospect_Forward_ASSR`, `Prospect_Update_ASSR`
   - screens: Prospect-Outlet,Demograph_R2 -> Prospect-Outlet,Oper_Info_R2 -> Prospect-Outlet,DemoForward_R2
   - detail: flows/02400001.md ; trace prefix `65:14:02400001`
15. **seq 15 - Prospect_Outlet_Approval_R2** (`02410001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_OutletCode` from seq 13 (02350001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Prospect_Outlet_Approval_R2
   - detail: flows/02410001.md ; trace prefix `65:15:02410001`
16. **seq 17 - DSR Profile HQ R2** (`02130001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **headquarter** (serial 27)
   - consumes: `REPO_DSRCODEHQ` produced within same flow
   - produces: `REPO_DSRCODEHQ`
   - checks: 9 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: DSR Profile, DemographicsHQR2 -> DSR Profile, Address HQ R2 -> DSR ProfileAddress,BusinessHQR2 -> DSR ProfileAddress,Other HQ R2 -> DSR Profile, Documents HQ R2 -> DSR Profile, Qualification HQR2 ...
   - detail: flows/02130001.md ; trace prefix `65:17:02130001`
17. **seq 18 - DSR Profile PH** (`01230001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - consumes: `REPO_DSRCODE` produced within same flow
   - produces: `REPO_DSRCODE`
   - checks: 9 message/field assertion(s); group assertion sheet(s): `Device_ASSR_PH`, `Forward_ASSR`
   - screens: DSR Profile, Demographics PH -> DSR Profile, Address PH -> DSR ProfileAddress,Business PH -> DSR ProfileAddress,Other PH -> DSR Profile, Documents HQ R2 -> DSR Profile, Qualification PH ...
   - detail: flows/01230001.md ; trace prefix `65:18:01230001`
18. **seq 19 - DSR Approval DT** (`00390001`) - area: DSR/PJP/Route, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_DSRCODE` from seq 18 (01230001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: DSR Approval
   - detail: flows/00390001.md ; trace prefix `65:19:00390001`
19. **seq 20 - Company Mapping** (`00950001`) - area: Master/Setup
   - actor: same session (auto_thai_tssm)
   - checks: none configured
   - screens: Company Mapping
   - detail: flows/00950001.md ; trace prefix `65:20:00950001`
20. **seq 21 - Distributor Mapping TH** (`02680001`) - area: Master/Setup
   - actor: same session (auto_thai_tssm)
   - consumes: `REPO_DSRCODE` from seq 18 (01230001); `REPO_WAREHOUSE` from seq 4 (02380001); `REPO_OutletCode` from seq 13 (02350001)
   - checks: none configured
   - screens: Distributor Mapping_TH
   - detail: flows/02680001.md ; trace prefix `65:21:02680001`
21. **seq 22 - Daily Visit Plan** (`01290001`) - area: DSR/PJP/Route
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - checks: 1 message/field assertion(s)
   - screens: Daily Visit Plan -> Daily Visit Plan 2
   - detail: flows/01290001.md ; trace prefix `65:22:01290001`
22. **seq 23 - Change Track Outlet Profile** (`00240001`) - area: Master/Setup
   - actor: same session (Auto_Th)
   - consumes: `REPO_OutletCode` from seq 13 (02350001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `ChangeTrack_Outlet_profile_ASSR`, `Save_assertion`
   - screens: Change Track Outlet profile
   - detail: flows/00240001.md ; trace prefix `65:23:00240001`
23. **seq 24 - Change Track Outlet Approval** (`02190001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track Out Prof Approval
   - detail: flows/02190001.md ; trace prefix `65:24:02190001`
24. **seq 25 - Change Track Outlet Document** (`01340001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - consumes: `REPO_OutletCode` from seq 13 (02350001); `REPO_DocumentType` unresolved in group
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track Outlet Document
   - detail: flows/01340001.md ; trace prefix `65:25:01340001`
25. **seq 26 - Change Track Outlet Document Approval** (`02200001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Change Track Out Doc Approval
   - detail: flows/02200001.md ; trace prefix `65:26:02200001`
26. **seq 27 - Change Track Outlet Operative Info** (`01330001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - consumes: `REPO_OutletCode` from seq 13 (02350001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track Outlet Oper Info
   - detail: flows/01330001.md ; trace prefix `65:27:01330001`
27. **seq 28 - Change Track Outlet Operative Info Approval** (`02220001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Change Track Out Oper Info App
   - detail: flows/02220001.md ; trace prefix `65:28:02220001`
28. **seq 29 - Change Track DSR** (`00250001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - consumes: `REPO_DSRCODE` from seq 18 (01230001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track DSR
   - detail: flows/00250001.md ; trace prefix `65:29:00250001`
29. **seq 30 - Change Track DSR Profile Approval** (`02240001`) - area: DSR/PJP/Route, Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track DSR approval
   - detail: flows/02240001.md ; trace prefix `65:30:02240001`
30. **seq 31 - Change Track DSR Document** (`01320001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - consumes: `REPO_DSRCODE` from seq 18 (01230001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track DSR Document
   - detail: flows/01320001.md ; trace prefix `65:31:01320001`
31. **seq 32 - Change Track DSR Document Approval** (`02250001`) - area: DSR/PJP/Route, Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track DSR Doc approval
   - detail: flows/02250001.md ; trace prefix `65:32:02250001`
32. **seq 33 - PJP Creation HQ** (`01280001`) - area: DSR/PJP/Route
   - **SWITCH USER POINT**: log out and log in as **headquarter** (serial 27)
   - consumes: `REPO_DSRCODEHQ` produced within same flow; `REPO_PJPNumberHQ` produced within same flow
   - produces: `REPO_DSRCODEHQ`, `REPO_PJPNumberHQ`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`, `Saved_assertion`
   - screens: PJP Creation HQ -> PJP Configuration HQ -> PJP Creation Forward HQ
   - detail: flows/01280001.md ; trace prefix `65:33:01280001`
33. **seq 34 - PJP Creation** (`00610001`) - area: DSR/PJP/Route
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - consumes: `REPO_DSRCODE` produced within same flow; `REPO_PJP_Number` produced within same flow
   - produces: `REPO_DSRCODE`, `REPO_PJP_Number`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: PJP Creation -> PJP Configuration -> PJP Configuration Forward
   - detail: flows/00610001.md ; trace prefix `65:34:00610001`
34. **seq 36 - Change Track PJP Config** (`00230001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12) (same user as before: re-login only)
   - consumes: `REPO_PJP_Number` from seq 34 (00610001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`, `Save_assertion`
   - screens: Change Track PJP Config
   - detail: flows/00230001.md ; trace prefix `65:36:00230001`
35. **seq 37 - Change Track PJP Config Approval** (`02270001`) - area: DSR/PJP/Route, Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track PJP Config App
   - detail: flows/02270001.md ; trace prefix `65:37:02270001`
36. **seq 38 - PJP Change Request** (`02110001`) - area: DSR/PJP/Route
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - consumes: `REPO_PJP_Number` from seq 34 (00610001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: PJP Change Request
   - detail: flows/02110001.md ; trace prefix `65:38:02110001`
37. **seq 39 - PJP Change Request Approval** (`02320001`) - area: DSR/PJP/Route, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: PJP Change Request Approval
   - detail: flows/02320001.md ; trace prefix `65:39:02320001`
38. **seq 40 - Segment Setup** (`01370001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Th** (serial 12)
   - consumes: `REPO_SegmentSetup` produced within same flow
   - produces: `REPO_SegmentSetup`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `Update_assertion`
   - screens: Segment setup
   - detail: flows/01370001.md ; trace prefix `65:40:01370001`
39. **seq 41 - Role_Option** (`02300001`) - area: Master/Setup
   - actor: same session (Auto_Th)
   - checks: none configured
   - screens: Role_Option
   - detail: flows/02300001.md ; trace prefix `65:41:02300001`
40. **seq 42 - Non Unilever Products** (`02340001`) - area: Master/Setup
   - actor: same session (Auto_Th)
   - consumes: `REPO_NUP_CODE` produced within same flow
   - produces: `REPO_NUP_CODE`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `NUP_Product_Fwd_ASSR`
   - screens: NUP_Product -> NUP_Product_Analysis -> NUP_Batch -> NUP_Product_Forward
   - detail: flows/02340001.md ; trace prefix `65:42:02340001`
41. **seq 43 - NUP Approval** (`02360001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **auto_thai_tssm** (serial 13)
   - consumes: `REPO_NUP_CODE` from seq 42 (02340001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `NUP_Approval_ASSR`
   - screens: NUP_Approval
   - detail: flows/02360001.md ; trace prefix `65:43:02360001`

## Inactive rows (skipped by the engine)
- seq 16 Outlet Profile HQ (`01300001`) status N
- seq 35 PJP Approval (`00800001`) status N
- seq 44 Distributor Mapping TH (`02680001`) status N
- seq 45 Company Mapping (`00950001`) status N
