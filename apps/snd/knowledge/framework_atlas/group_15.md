# Group 15 - NG_Setup Flow_PH

Source `gtf:15`. Market guess (from name): None. Rows: 41 (active 41, inactive 0). User switch points: 29 (1, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 33, 34, 35, 36, 37, 38, 40).

Allowed apps (alg): app 6 PHP_CentegyQA -> D:/Selenium/Automation/PHP_QA// (workbook variant inferred: PHP)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `15:1:021400000`
2. **seq 2 - Vehicle Profile II** (`02180001`) - area: Master/Setup
   - actor: same session (Auto_PH)
   - consumes: `REPO_Vehicle_Code` produced within same flow
   - produces: `REPO_Vehicle_Code`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Vehicle Profile II
   - detail: flows/02180001.md ; trace prefix `15:2:02180001`
3. **seq 3 - Vehicle Profile Approval II** (`02160001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_Vehicle_Code` from seq 2 (02180001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Vehicle Profile Approval II
   - detail: flows/02160001.md ; trace prefix `15:3:02160001`
4. **seq 4 - Outlet Profile HQ R2** (`02430001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **ph_global** (serial 29)
   - consumes: `REPO_OutletCodeHQ` produced within same flow
   - produces: `REPO_OutletCodeHQ`
   - checks: 9 message/field assertion(s); group assertion sheet(s): `OutletProfile_Address_ASSR`, `RecSave_assertion`
   - screens: OutletProf_DemoGraphHQ_R2 -> OutletProfile,OperInfoHQ_R2 -> OutletProfile-AddressHQ_R2 -> OutletProfile-Address,BusHQ_R2 -> OutletProfileAdd_Res_HQ_R2 -> OutletProfile,Doc_HQ_R2 ...
   - detail: flows/02430001.md ; trace prefix `15:4:02430001`
5. **seq 5 - Outlet Profile_R2** (`02350001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_OutletCode` produced within same flow
   - produces: `REPO_OutletCode`
   - checks: 8 message/field assertion(s); group assertion sheet(s): `OutletProfile_Address_ASSR`, `Save_ASSR`
   - screens: OutletProfile,Demograph_R2 -> OutletProfile,Oper_Info_R2 -> OutletProfile-Address_R2 -> OutletProfile-Address,Bus_R2 -> OutletProfile-Address,OtherR2 -> OutletProfile,Documents_R2 ...
   - detail: flows/02350001.md ; trace prefix `15:5:02350001`
6. **seq 6 - Prospect Outlet_R2** (`02400001`) - area: Master/Setup
   - actor: same session (Auto_PH)
   - consumes: `REPO_OutletCode` from seq 5 (02350001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Prospect_Forward_ASSR`, `Prospect_Update_ASSR`
   - screens: Prospect-Outlet,Demograph_R2 -> Prospect-Outlet,Oper_Info_R2 -> Prospect-Outlet,DemoForward_R2
   - detail: flows/02400001.md ; trace prefix `15:6:02400001`
7. **seq 7 - Prospect_Outlet_Approval_R2** (`02410001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_OutletCode` from seq 5 (02350001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Prospect_Outlet_Approval_R2
   - detail: flows/02410001.md ; trace prefix `15:7:02410001`
8. **seq 8 - Change Track Outlet Profile** (`00240001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_OutletCode` from seq 5 (02350001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `ChangeTrack_Outlet_profile_ASSR`, `Save_assertion`
   - screens: Change Track Outlet profile
   - detail: flows/00240001.md ; trace prefix `15:8:00240001`
9. **seq 9 - Change Track Outlet Approval** (`02190001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track Out Prof Approval
   - detail: flows/02190001.md ; trace prefix `15:9:02190001`
10. **seq 10 - Change Track Outlet Document** (`01340001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_OutletCode` from seq 5 (02350001); `REPO_DocumentType` unresolved in group
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track Outlet Document
   - detail: flows/01340001.md ; trace prefix `15:10:01340001`
11. **seq 11 - Change Track Outlet Document Approval** (`02200001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Change Track Out Doc Approval
   - detail: flows/02200001.md ; trace prefix `15:11:02200001`
12. **seq 12 - Change Track Outlet Operative Info** (`01330001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_OutletCode` from seq 5 (02350001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track Outlet Oper Info
   - detail: flows/01330001.md ; trace prefix `15:12:01330001`
13. **seq 13 - Change Track Outlet Operative Info Approval** (`02220001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Change Track Out Oper Info App
   - detail: flows/02220001.md ; trace prefix `15:13:02220001`
14. **seq 14 - DSR Profile PH** (`01230001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_DSRCODE` produced within same flow
   - produces: `REPO_DSRCODE`
   - checks: 9 message/field assertion(s); group assertion sheet(s): `Device_ASSR_PH`, `Forward_ASSR`
   - screens: DSR Profile, Demographics PH -> DSR Profile, Address PH -> DSR ProfileAddress,Business PH -> DSR ProfileAddress,Other PH -> DSR Profile, Documents HQ R2 -> DSR Profile, Qualification PH ...
   - detail: flows/01230001.md ; trace prefix `15:14:01230001`
15. **seq 15 - DSR Approval DT** (`00390001`) - area: DSR/PJP/Route, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_DSRCODE` from seq 14 (01230001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: DSR Approval
   - detail: flows/00390001.md ; trace prefix `15:15:00390001`
16. **seq 16 - Change Track DSR** (`00250001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_DSRCODE` from seq 14 (01230001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track DSR
   - detail: flows/00250001.md ; trace prefix `15:16:00250001`
17. **seq 17 - Change Track DSR Profile Approval** (`02240001`) - area: DSR/PJP/Route, Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track DSR approval
   - detail: flows/02240001.md ; trace prefix `15:17:02240001`
18. **seq 18 - Change Track DSR Document** (`01320001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_DSRCODE` from seq 14 (01230001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track DSR Document
   - detail: flows/01320001.md ; trace prefix `15:18:01320001`
19. **seq 19 - Change Track DSR Document Approval** (`02250001`) - area: DSR/PJP/Route, Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track DSR Doc approval
   - detail: flows/02250001.md ; trace prefix `15:19:02250001`
20. **seq 20 - Section** (`00590001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_OutletCode` from seq 5 (02350001); `REPO_SECTION_CODE` produced within same flow
   - produces: `REPO_SECTION_CODE`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Section -> Section Allowable -> Section Forward
   - detail: flows/00590001.md ; trace prefix `15:20:00590001`
21. **seq 21 - Section Approval** (`00720001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_SECTION_CODE` from seq 20 (00590001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Section Approval
   - detail: flows/00720001.md ; trace prefix `15:21:00720001`
22. **seq 22 - BG - Section Profile R2** (`02390001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_SECTIONCODE_BG` produced within same flow
   - produces: `REPO_SECTIONCODE_BG`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`, `Update_assertion`
   - screens: BG_Section_Profile_R2 -> BG_Section_Profile_Allowable_R2 -> BG_Section_Profile_Forward_R2
   - detail: flows/02390001.md ; trace prefix `15:22:02390001`
23. **seq 23 - BG - Section Profile Approval** (`02370001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_SECTIONCODE_BG` from seq 22 (02390001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: BG-Section Profile Approve
   - detail: flows/02370001.md ; trace prefix `15:23:02370001`
24. **seq 24 - Selling Category II** (`02170001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - produces: `REPO_Selling_Category_CODE`
   - checks: 2 message/field assertion(s)
   - screens: Selling Category II
   - detail: flows/02170001.md ; trace prefix `15:24:02170001`
25. **seq 25 - Warehouse** (`00570001`) - area: Master/Setup
   - actor: same session (Auto_PH)
   - consumes: `REPO_WAREHOUSE` produced within same flow
   - produces: `REPO_WAREHOUSE`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Save_assertion`, `Update_assertion`
   - screens: Warehouse Profile
   - detail: flows/00570001.md ; trace prefix `15:25:00570001`
26. **seq 26 - Segment Setup** (`01370001`) - area: Master/Setup
   - actor: same session (Auto_PH)
   - consumes: `REPO_SegmentSetup` produced within same flow
   - produces: `REPO_SegmentSetup`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `Update_assertion`
   - screens: Segment setup
   - detail: flows/01370001.md ; trace prefix `15:26:01370001`
27. **seq 27 - User** (`00360001`) - area: Other
   - actor: same session (Auto_PH)
   - consumes: `REPO_CODE` produced within same flow
   - produces: `REPO_CODE`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Update_ASSR`
   - screens: User
   - detail: flows/00360001.md ; trace prefix `15:27:00360001`
28. **seq 28 - User Profile** (`00350001`) - area: Master/Setup
   - actor: same session (Auto_PH)
   - consumes: `REPO_CODE` from seq 27 (00360001); `REPO_LOCATIONCODE` unresolved in group
   - checks: none configured
   - screens: User Profile
   - detail: flows/00350001.md ; trace prefix `15:28:00350001`
29. **seq 29 - Role_Option** (`02300001`) - area: Master/Setup
   - actor: same session (Auto_PH)
   - checks: none configured
   - screens: Role_Option
   - detail: flows/02300001.md ; trace prefix `15:29:02300001`
30. **seq 30 - PJP Creation** (`00610001`) - area: DSR/PJP/Route
   - actor: same session (Auto_PH)
   - consumes: `REPO_DSRCODE` produced within same flow; `REPO_PJP_Number` produced within same flow
   - produces: `REPO_DSRCODE`, `REPO_PJP_Number`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: PJP Creation -> PJP Configuration -> PJP Configuration Forward
   - detail: flows/00610001.md ; trace prefix `15:30:00610001`
31. **seq 31 - Daily Visit Plan** (`01290001`) - area: DSR/PJP/Route
   - actor: same session (Auto_PH)
   - checks: 1 message/field assertion(s)
   - screens: Daily Visit Plan -> Daily Visit Plan 2
   - detail: flows/01290001.md ; trace prefix `15:31:01290001`
32. **seq 32 - PJP Change Request** (`02110001`) - area: DSR/PJP/Route
   - actor: same session (Auto_PH)
   - consumes: `REPO_PJP_Number` from seq 30 (00610001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: PJP Change Request
   - detail: flows/02110001.md ; trace prefix `15:32:02110001`
33. **seq 33 - PJP Change Request Approval** (`02320001`) - area: DSR/PJP/Route, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: PJP Change Request Approval
   - detail: flows/02320001.md ; trace prefix `15:33:02320001`
34. **seq 34 - Change Track PJP Config** (`00230001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_PJP_Number` from seq 30 (00610001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`, `Save_assertion`
   - screens: Change Track PJP Config
   - detail: flows/00230001.md ; trace prefix `15:34:00230001`
35. **seq 35 - Change Track PJP Config Approval** (`02270001`) - area: DSR/PJP/Route, Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track PJP Config App
   - detail: flows/02270001.md ; trace prefix `15:35:02270001`
36. **seq 36 - Non Unilever Products** (`02340001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - consumes: `REPO_NUP_CODE` produced within same flow
   - produces: `REPO_NUP_CODE`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `NUP_Product_Fwd_ASSR`
   - screens: NUP_Product -> NUP_Product_Analysis -> NUP_Batch -> NUP_Product_Forward
   - detail: flows/02340001.md ; trace prefix `15:36:02340001`
37. **seq 37 - NUP Approval** (`02360001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH_TSSM** (serial 20)
   - consumes: `REPO_NUP_CODE` from seq 36 (02340001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `NUP_Approval_ASSR`
   - screens: NUP_Approval
   - detail: flows/02360001.md ; trace prefix `15:37:02360001`
38. **seq 38 - Company Mapping** (`00950001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_PH** (serial 19)
   - checks: none configured
   - screens: Company Mapping
   - detail: flows/00950001.md ; trace prefix `15:38:00950001`
39. **seq 39 - Distributor Mapping TH** (`02680001`) - area: Master/Setup
   - actor: same session (Auto_PH)
   - consumes: `REPO_DSRCODE` from seq 30 (00610001); `REPO_WAREHOUSE` from seq 25 (00570001); `REPO_OutletCode` from seq 5 (02350001)
   - checks: none configured
   - screens: Distributor Mapping_TH
   - detail: flows/02680001.md ; trace prefix `15:39:02680001`
40. **seq 40 - DSR Profile HQ R2** (`02130001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **ph_global** (serial 29)
   - consumes: `REPO_DSRCODEHQ` produced within same flow
   - produces: `REPO_DSRCODEHQ`
   - checks: 9 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: DSR Profile, DemographicsHQR2 -> DSR Profile, Address HQ R2 -> DSR ProfileAddress,BusinessHQR2 -> DSR ProfileAddress,Other HQ R2 -> DSR Profile, Documents HQ R2 -> DSR Profile, Qualification HQR2 ...
   - detail: flows/02130001.md ; trace prefix `15:40:02130001`
41. **seq 41 - PJP Creation HQ** (`01280001`) - area: DSR/PJP/Route
   - actor: same session (ph_global)
   - consumes: `REPO_DSRCODEHQ` produced within same flow; `REPO_PJPNumberHQ` produced within same flow
   - produces: `REPO_DSRCODEHQ`, `REPO_PJPNumberHQ`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`, `Saved_assertion`
   - screens: PJP Creation HQ -> PJP Configuration HQ -> PJP Creation Forward HQ
   - detail: flows/01280001.md ; trace prefix `15:41:01280001`
