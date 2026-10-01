# Group 16 - NG_Setup Flow_BG

Source `gtf:16`. Market guess (from name): None. Rows: 32 (active 32, inactive 0). User switch points: 23 (4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 23, 24, 25, 26, 29, 30, 31, 32).

Allowed apps (alg): app 7 BD_Centegy QA -> D:/Selenium/Automation/BD_QA// (workbook variant inferred: Bangla)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `16:1:021400000`
2. **seq 2 - Selling Category** (`00940001`) - area: Master/Setup
   - actor: same session (runner default login)
   - produces: `REPO_Selling_Category_CODE`
   - checks: 2 message/field assertion(s)
   - screens: Selling Category
   - detail: flows/00940001.md ; trace prefix `16:2:00940001`
3. **seq 3 - BG - Section Profile** (`02280001`) - area: Master/Setup
   - actor: same session (runner default login)
   - consumes: `REPO_SECTIONCODE_BG` produced within same flow
   - produces: `REPO_SECTIONCODE_BG`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`, `Update_assertion`
   - screens: BG-Section Profile -> BG-Section Profile Allowable -> BG-Section Profile Forward
   - detail: flows/02280001.md ; trace prefix `16:3:02280001`
4. **seq 4 - BG - Section Profile Approval** (`02370001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_SECTIONCODE_BG` from seq 3 (02280001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: BG-Section Profile Approve
   - detail: flows/02370001.md ; trace prefix `16:4:02370001`
5. **seq 5 - Warehouse Profile – BG** (`02210001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - consumes: `REPO_WAREHOUSE` produced within same flow
   - produces: `REPO_WAREHOUSE`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`, `Save_ASSR`
   - screens: Warehouse Profile – BG
   - detail: flows/02210001.md ; trace prefix `16:5:02210001`
6. **seq 6 - Warehouse Profile Appr-BG** (`02230001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_WAREHOUSE` from seq 5 (02210001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Warehouse Profile App-BG
   - detail: flows/02230001.md ; trace prefix `16:6:02230001`
7. **seq 7 - Warehouse Profile Appr-BG** (`02230001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11) (same user as before: re-login only)
   - consumes: `REPO_WAREHOUSE` from seq 5 (02210001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Warehouse Profile App-BG
   - detail: flows/02230001.md ; trace prefix `16:7:02230001`
8. **seq 8 - Vehicle Profile II** (`02180001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - consumes: `REPO_Vehicle_Code` produced within same flow
   - produces: `REPO_Vehicle_Code`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Vehicle Profile II
   - detail: flows/02180001.md ; trace prefix `16:8:02180001`
9. **seq 9 - Vehicle Profile Approval II** (`02160001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_Vehicle_Code` from seq 8 (02180001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Vehicle Profile Approval II
   - detail: flows/02160001.md ; trace prefix `16:9:02160001`
10. **seq 10 - Outlet Profile** (`00530001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - consumes: `REPO_OutletCode` produced within same flow
   - produces: `REPO_OutletCode`
   - checks: 12 message/field assertion(s); group assertion sheet(s): `OutletProfile_Address_ASSR`
   - screens: OutletProfile,Demographics -> OutletProfile,Operative Info -> OutletProfile-Address -> OutletProfile-Address,Business -> OutletProfile-Address,Residence -> OutletProfile,Documents ...
   - detail: flows/00530001.md ; trace prefix `16:10:00530001`
11. **seq 11 - Prospect Outlet** (`00380002`) - area: Master/Setup
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_OutletCode` from seq 10 (00530001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`, `Prospect_Outlet_Demogra_ASSR`, `Prospect_Outlet_OperInfo_ASSR`
   - screens: Prospect Outlet Demogra -> Prospect Outlet OperInfo -> Prospect Outlet Add Other -> ProspectOutlet,Documents -> ProspectOutletProfDemo Forward
   - detail: flows/00380002.md ; trace prefix `16:11:00380002`
12. **seq 12 - Prospect Outlet Approval** (`00380001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - consumes: `REPO_OutletCode` from seq 10 (00530001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `FORWARD_ASSR`
   - screens: Prospect Outlet Approval
   - detail: flows/00380001.md ; trace prefix `16:12:00380001`
13. **seq 13 - Change Track Outlet Profile** (`00240001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - consumes: `REPO_OutletCode` from seq 10 (00530001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `ChangeTrack_Outlet_profile_ASSR`, `Save_assertion`
   - screens: Change Track Outlet profile
   - detail: flows/00240001.md ; trace prefix `16:13:00240001`
14. **seq 14 - Change Track Outlet Approval** (`02190001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track Out Prof Approval
   - detail: flows/02190001.md ; trace prefix `16:14:02190001`
15. **seq 15 - Change Track Outlet Document** (`01340001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - consumes: `REPO_OutletCode` from seq 10 (00530001); `REPO_DocumentType` unresolved in group
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track Outlet Document
   - detail: flows/01340001.md ; trace prefix `16:15:01340001`
16. **seq 16 - Change Track Outlet Document Approval** (`02200001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Change Track Out Doc Approval
   - detail: flows/02200001.md ; trace prefix `16:16:02200001`
17. **seq 17 - Change Track Outlet Operative Info** (`01330001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - consumes: `REPO_OutletCode` from seq 10 (00530001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track Outlet Oper Info
   - detail: flows/01330001.md ; trace prefix `16:17:01330001`
18. **seq 18 - Change Track Outlet Operative Info Approval** (`02220001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Change Track Out Oper Info App
   - detail: flows/02220001.md ; trace prefix `16:18:02220001`
19. **seq 19 - DSR Profile Bangladesh** (`01030001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - consumes: `REPO_Vehicle_Code` produced within same flow; `REPO_DSRCODE` produced within same flow
   - produces: `REPO_DSRCODE`, `REPO_Vehicle_Code`
   - checks: 10 message/field assertion(s); group assertion sheet(s): `Update_assertion`
   - screens: DSR Profile Demographics BD -> DSR ProfileAddress Comp BD -> DSR ProfileAddress Busi BD -> DSR ProfileAddress Resi BD -> DSR Profile Document BD -> DSR Profile Qualification BD ...
   - detail: flows/01030001.md ; trace prefix `16:19:01030001`
20. **seq 20 - Distributor Mapping** (`00960001`) - area: Master/Setup
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_DSRCODE` from seq 19 (01030001); `REPO_WAREHOUSE` from seq 5 (02210001); `REPO_OutletCode` from seq 10 (00530001)
   - checks: none configured
   - screens: Distributor Mapping
   - detail: flows/00960001.md ; trace prefix `16:20:00960001`
21. **seq 21 - Company Mapping** (`00950001`) - area: Master/Setup
   - actor: same session (Auto_Multi_Orga)
   - checks: none configured
   - screens: Company Mapping
   - detail: flows/00950001.md ; trace prefix `16:21:00950001`
22. **seq 22 - Change Track DSR** (`00250001`) - area: DSR/PJP/Route, Master/Setup
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_DSRCODE` from seq 19 (01030001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track DSR
   - detail: flows/00250001.md ; trace prefix `16:22:00250001`
23. **seq 23 - Change Track DSR Profile Approval** (`02240001`) - area: DSR/PJP/Route, Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track DSR approval
   - detail: flows/02240001.md ; trace prefix `16:23:02240001`
24. **seq 24 - Change Track DSR Document** (`01320001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - consumes: `REPO_DSRCODE` from seq 19 (01030001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: Change Track DSR Document
   - detail: flows/01320001.md ; trace prefix `16:24:01320001`
25. **seq 25 - Change Track DSR Document Approval** (`02250001`) - area: DSR/PJP/Route, Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track DSR Doc approval
   - detail: flows/02250001.md ; trace prefix `16:25:02250001`
26. **seq 26 - PJP Creation BG** (`01270001`) - area: DSR/PJP/Route
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - consumes: `REPO_DSRCODE` produced within same flow; `REPO_PJP_Number` produced within same flow
   - produces: `REPO_DSRCODE`, `REPO_PJP_Number`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`, `Saved_assertion`
   - screens: PJP Creation BG -> PJP Configuration BD -> PJP Creation Forward BD
   - detail: flows/01270001.md ; trace prefix `16:26:01270001`
27. **seq 27 - PJP Daily Inquiry** (`01310001`) - area: DSR/PJP/Route
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_PJP_Number` from seq 26 (01270001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Process_ASSR`
   - screens: PJP Daily Inquiry
   - detail: flows/01310001.md ; trace prefix `16:27:01310001`
28. **seq 28 - PJP Change Request** (`02110001`) - area: DSR/PJP/Route
   - actor: same session (Auto_Multi_Orga)
   - consumes: `REPO_PJP_Number` from seq 26 (01270001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_assertion`, `Save_assertion`
   - screens: PJP Change Request
   - detail: flows/02110001.md ; trace prefix `16:28:02110001`
29. **seq 29 - PJP Change Request Approval** (`02320001`) - area: DSR/PJP/Route, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: PJP Change Request Approval
   - detail: flows/02320001.md ; trace prefix `16:29:02320001`
30. **seq 30 - Change Track PJP Config** (`00230001`) - area: DSR/PJP/Route, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - consumes: `REPO_PJP_Number` from seq 26 (01270001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`, `Save_assertion`
   - screens: Change Track PJP Config
   - detail: flows/00230001.md ; trace prefix `16:30:00230001`
31. **seq 31 - Change Track PJP Config Approval** (`02270001`) - area: DSR/PJP/Route, Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **autoBD_Tssm** (serial 11)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Change Track PJP Config App
   - detail: flows/02270001.md ; trace prefix `16:31:02270001`
32. **seq 32 - Delivery Man Shuffling** (`02260001`) - area: Order Booking, DSR/PJP/Route
   - **SWITCH USER POINT**: log out and log in as **Auto_Multi_Orga** (serial 36)
   - produces: `ORDERNUMBER`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `DM_Shuffling_ASSR`; value validations 3, Q2Q 1
   - screens: DMS_Order_Booking -> DMS_Order_Booking_Detail -> DMS_Order_Booking_Detail2 -> Delivery Man Shuffling
   - detail: flows/02260001.md ; trace prefix `16:32:02260001`
