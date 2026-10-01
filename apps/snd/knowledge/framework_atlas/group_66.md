# Group 66 - NG_Setup Flow_PK

Source `gtf:66`. Market guess (from name): None. Rows: 36 (active 35, inactive 1). User switch points: 21 (5, 6, 7, 8, 14, 15, 16, 17, 18, 19, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 35).

Allowed apps (alg): app 8 PK_Centegy QA 2 -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `66:1:021400000`
2. **seq 2 - Distributor Profile DT** (`00970001`) - area: Master/Setup
   - actor: same session (runner default login)
   - consumes: `REPO_DISTRIBUTOR` unresolved in group
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Distributor,Other_Info1_ASSR`, `Distributor_Operati,InfoDT_ASSR`, `Distributor_ResidenceDT_ASSR`, `Update_assertion`
   - screens: Distributor,DemographicsDT -> Distributor,Operati,InfoDT -> Distributor,Other Info1 -> Distributor, Address1 -> Distributor-Address,Reside_DT -> Distributor, DocumentsDT ...
   - detail: flows/00970001.md ; trace prefix `66:2:00970001`
3. **seq 3 - Outlet Profile** (`00530001`) - area: Master/Setup
   - actor: same session (runner default login)
   - consumes: `REPO_OutletCode` produced within same flow
   - produces: `REPO_OutletCode`
   - checks: 12 message/field assertion(s); group assertion sheet(s): `OutletProfile_Address_ASSR`
   - screens: OutletProfile,Demographics -> OutletProfile,Operative Info -> OutletProfile-Address -> OutletProfile-Address,Business -> OutletProfile-Address,Residence -> OutletProfile,Documents ...
   - detail: flows/00530001.md ; trace prefix `66:3:00530001`
4. **seq 4 - Prospect Outlet** (`00380002`) - area: Master/Setup
   - actor: same session (runner default login)
   - consumes: `REPO_OutletCode` from seq 3 (00530001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`, `Prospect_Outlet_Demogra_ASSR`, `Prospect_Outlet_OperInfo_ASSR`
   - screens: Prospect Outlet Demogra -> Prospect Outlet OperInfo -> Prospect Outlet Add Other -> ProspectOutlet,Documents -> ProspectOutletProfDemo Forward
   - detail: flows/00380002.md ; trace prefix `66:4:00380002`
5. **seq 5 - Prospect Outlet Approval** (`00380001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_OutletCode` from seq 3 (00530001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `FORWARD_ASSR`
   - screens: Prospect Outlet Approval
   - detail: flows/00380001.md ; trace prefix `66:5:00380001`
6. **seq 6 - Section** (`00590001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - consumes: `REPO_OutletCode` from seq 3 (00530001); `REPO_SECTION_CODE` produced within same flow
   - produces: `REPO_SECTION_CODE`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Section -> Section Allowable -> Section Forward
   - detail: flows/00590001.md ; trace prefix `66:6:00590001`
7. **seq 7 - Section Approval** (`00720001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_SECTION_CODE` from seq 6 (00590001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Section Approval
   - detail: flows/00720001.md ; trace prefix `66:7:00720001`
8. **seq 8 - Selling Category** (`00940001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - produces: `REPO_Selling_Category_CODE`
   - checks: 2 message/field assertion(s)
   - screens: Selling Category
   - detail: flows/00940001.md ; trace prefix `66:8:00940001`
9. **seq 9 - Warehouse** (`00570001`) - area: Master/Setup
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_WAREHOUSE` produced within same flow
   - produces: `REPO_WAREHOUSE`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Save_assertion`, `Update_assertion`
   - screens: Warehouse Profile
   - detail: flows/00570001.md ; trace prefix `66:9:00570001`
10. **seq 10 - Vehicle Profile** (`00580001`) - area: Master/Setup
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_Vehicle_Code` produced within same flow
   - produces: `REPO_Description`, `REPO_Vehicle_Code`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Update_assertion`
   - screens: Vehicle Profile
   - detail: flows/00580001.md ; trace prefix `66:10:00580001`
11. **seq 11 - Change Track Outlet Profile** (`00240001`) - area: Master/Setup
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_OutletCode` from seq 3 (00530001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `ChangeTrack_Outlet_profile_ASSR`, `Save_assertion`
   - screens: Change Track Outlet profile
   - detail: flows/00240001.md ; trace prefix `66:11:00240001`
12. **seq 13 - Change Track Outlet Document** (`01340001`) - area: Master/Setup
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_OutletCode` from seq 3 (00530001); `REPO_DocumentType` unresolved in group
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track Outlet Document
   - detail: flows/01340001.md ; trace prefix `66:13:01340001`
13. **seq 14 - Change Track Outlet Document Approval** (`02200001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Change Track Out Doc Approval
   - detail: flows/02200001.md ; trace prefix `66:14:02200001`
14. **seq 15 - Change Track Outlet Operative Info** (`01330001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - consumes: `REPO_OutletCode` from seq 3 (00530001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track Outlet Oper Info
   - detail: flows/01330001.md ; trace prefix `66:15:01330001`
15. **seq 16 - Change Track Outlet Operative Info Approval** (`02220001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Change Track Out Oper Info App
   - detail: flows/02220001.md ; trace prefix `66:16:02220001`
16. **seq 17 - DSR Profile DT** (`00560001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - consumes: `REPO_DSRCODE` produced within same flow
   - produces: `REPO_DSRCODE`
   - checks: 10 message/field assertion(s); group assertion sheet(s): `DSR_Profile, Device_ASSR`
   - screens: DSR Profile, Demographics -> DSR Profile, Address -> DSR ProfileAddress,Business -> DSR ProfileAddress,Residence -> DSR Profile, Documents -> DSR Profile, Qualification ...
   - detail: flows/00560001.md ; trace prefix `66:17:00560001`
17. **seq 18 - DSR Approval DT** (`00390001`) - area: DSR/PJP/Route, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_DSRCODE` from seq 17 (00560001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: DSR Approval
   - detail: flows/00390001.md ; trace prefix `66:18:00390001`
18. **seq 19 - Distributor Mapping** (`00960001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - consumes: `REPO_DSRCODE` from seq 17 (00560001); `REPO_WAREHOUSE` from seq 9 (00570001); `REPO_OutletCode` from seq 3 (00530001)
   - checks: none configured
   - screens: Distributor Mapping
   - detail: flows/00960001.md ; trace prefix `66:19:00960001`
19. **seq 20 - Company Mapping** (`00950001`) - area: Master/Setup
   - actor: same session (Auto_Multi_Orga)
   - checks: none configured
   - screens: Company Mapping
   - detail: flows/00950001.md ; trace prefix `66:20:00950001`
20. **seq 21 - Change Track DSR** (`00250001`) - area: DSR/PJP/Route, Master/Setup
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_DSRCODE` from seq 17 (00560001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track DSR
   - detail: flows/00250001.md ; trace prefix `66:21:00250001`
21. **seq 22 - Change Track DSR Profile Approval** (`02240001`) - area: DSR/PJP/Route, Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track DSR approval
   - detail: flows/02240001.md ; trace prefix `66:22:02240001`
22. **seq 23 - Change Track DSR Document** (`01320001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - consumes: `REPO_DSRCODE` from seq 17 (00560001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track DSR Document
   - detail: flows/01320001.md ; trace prefix `66:23:01320001`
23. **seq 24 - Change Track DSR Document Approval** (`02250001`) - area: DSR/PJP/Route, Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track DSR Doc approval
   - detail: flows/02250001.md ; trace prefix `66:24:02250001`
24. **seq 25 - PJP Creation DT** (`01260001`) - area: DSR/PJP/Route
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - consumes: `REPO_DSRCODE` produced within same flow; `REPO_PJP_Number` produced within same flow
   - produces: `REPO_DSRCODE`, `REPO_PJP_Number`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`, `Saved_assertion`
   - screens: PJP Creation DT -> PJP Configuration DT -> PJP Creation Forward DT
   - detail: flows/01260001.md ; trace prefix `66:25:01260001`
25. **seq 26 - PJP Approval** (`00800001`) - area: DSR/PJP/Route, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_PJP_Number` from seq 25 (01260001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: PJP Approval
   - detail: flows/00800001.md ; trace prefix `66:26:00800001`
26. **seq 27 - PJP Daily Inquiry** (`01310001`) - area: DSR/PJP/Route
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - consumes: `REPO_PJP_Number` from seq 25 (01260001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Process_ASSR`
   - screens: PJP Daily Inquiry
   - detail: flows/01310001.md ; trace prefix `66:27:01310001`
27. **seq 28 - PJP Change Request** (`02110001`) - area: DSR/PJP/Route
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_PJP_Number` from seq 25 (01260001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: PJP Change Request
   - detail: flows/02110001.md ; trace prefix `66:28:02110001`
28. **seq 29 - PJP Change Request Approval** (`02320001`) - area: DSR/PJP/Route, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: PJP Change Request Approval
   - detail: flows/02320001.md ; trace prefix `66:29:02320001`
29. **seq 30 - Change Track PJP Config** (`00230001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - consumes: `REPO_PJP_Number` from seq 25 (01260001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`, `Save_assertion`
   - screens: Change Track PJP Config
   - detail: flows/00230001.md ; trace prefix `66:30:00230001`
30. **seq 31 - Change Track PJP Config Approval** (`02270001`) - area: DSR/PJP/Route, Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track PJP Config App
   - detail: flows/02270001.md ; trace prefix `66:31:02270001`
31. **seq 32 - Section Creation HQ** (`01250001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **headquarter** (serial 30)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Save_assertion`, `Update_assertion`
   - screens: Section Creation HQ
   - detail: flows/01250001.md ; trace prefix `66:32:01250001`
32. **seq 33 - DSR Profile HQ** (`01220001`) - area: DSR/PJP/Route, Master/Setup
   - actor: same session (headquarter)
   - consumes: `REPO_DSRCODEHQ` produced within same flow
   - produces: `REPO_DSRCODEHQ`
   - checks: 8 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Saved_assertion`
   - screens: DSR Profile, Demographics HQ -> DSR Profile, Address HQ -> DSR ProfileAddress,Business HQ -> DSR ProfileAddress,Other HQ -> DSR Profile, Documents HQ -> DSR Profile, Qualification HQ ...
   - detail: flows/01220001.md ; trace prefix `66:33:01220001`
33. **seq 34 - DSR Mapping HQ** (`02460001`) - area: DSR/PJP/Route, Master/Setup
   - actor: same session (headquarter)
   - consumes: `REPO_DSRCODEHQ` from seq 33 (01220001)
   - checks: none configured
   - screens: DSR Mapping HQ
   - detail: flows/02460001.md ; trace prefix `66:34:02460001`
34. **seq 35 - PJP Creation HQ** (`01280001`) - area: DSR/PJP/Route
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 35)
   - consumes: `REPO_DSRCODEHQ` produced within same flow; `REPO_PJPNumberHQ` produced within same flow
   - produces: `REPO_DSRCODEHQ`, `REPO_PJPNumberHQ`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`, `Saved_assertion`
   - screens: PJP Creation HQ -> PJP Configuration HQ -> PJP Creation Forward HQ
   - detail: flows/01280001.md ; trace prefix `66:35:01280001`
35. **seq 36 - Delivery Man Shuffling** (`02260001`) - area: Order Booking, DSR/PJP/Route
   - actor: same session (Auto_Multi_Orga)
   - produces: `ORDERNUMBER`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DM_Shuffling_ASSR`; value validations 3, Q2Q 1
   - screens: DMS_Order_Booking -> DMS_Order_Booking_Detail -> DMS_Order_Booking_Detail2 -> Delivery Man Shuffling
   - detail: flows/02260001.md ; trace prefix `66:36:02260001`

## Inactive rows (skipped by the engine)
- seq 12 Change Track Outlet Approval (`02190001`) status N
