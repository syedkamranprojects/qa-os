# Group 13 - NG_Setup Flow

Source `gtf:13`. Market guess (from name): None. Rows: 22 (active 22, inactive 0). User switch points: 15 (1, 3, 4, 6, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22).

Allowed apps (alg): app 8 PK_Centegy QA 2 -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - **SWITCH USER POINT**: log out and log in as **AppUser** (serial 4)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `13:1:021400000`
2. **seq 2 - DSR Profile DT** (`00560001`) - area: DSR/PJP/Route, Master/Setup
   - actor: same session (AppUser)
   - consumes: `REPO_DSRCODE` produced within same flow
   - produces: `REPO_DSRCODE`
   - checks: 10 message/field assertion(s); group assertion sheet(s): `DSR_Profile, Device_ASSR`
   - screens: DSR Profile, Demographics -> DSR Profile, Address -> DSR ProfileAddress,Business -> DSR ProfileAddress,Residence -> DSR Profile, Documents -> DSR Profile, Qualification ...
   - detail: flows/00560001.md ; trace prefix `13:2:00560001`
3. **seq 3 - DSR Approval DT** (`00390001`) - area: DSR/PJP/Route, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_DSRCODE` from seq 2 (00560001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: DSR Approval
   - detail: flows/00390001.md ; trace prefix `13:3:00390001`
4. **seq 4 - Outlet Profile** (`00530001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **AppUser** (serial 4)
   - consumes: `REPO_OutletCode` produced within same flow
   - produces: `REPO_OutletCode`
   - checks: 12 message/field assertion(s); group assertion sheet(s): `OutletProfile_Address_ASSR`
   - screens: OutletProfile,Demographics -> OutletProfile,Operative Info -> OutletProfile-Address -> OutletProfile-Address,Business -> OutletProfile-Address,Residence -> OutletProfile,Documents ...
   - detail: flows/00530001.md ; trace prefix `13:4:00530001`
5. **seq 5 - Prospect Outlet** (`00380002`) - area: Master/Setup
   - actor: same session (AppUser)
   - consumes: `REPO_OutletCode` from seq 4 (00530001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`, `Prospect_Outlet_Demogra_ASSR`, `Prospect_Outlet_OperInfo_ASSR`
   - screens: Prospect Outlet Demogra -> Prospect Outlet OperInfo -> Prospect Outlet Add Other -> ProspectOutlet,Documents -> ProspectOutletProfDemo Forward
   - detail: flows/00380002.md ; trace prefix `13:5:00380002`
6. **seq 6 - Prospect Outlet Approval** (`00380001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_OutletCode` from seq 4 (00530001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `FORWARD_ASSR`
   - screens: Prospect Outlet Approval
   - detail: flows/00380001.md ; trace prefix `13:6:00380001`
7. **seq 7 - Vehicle Profile** (`00580001`) - area: Master/Setup
   - actor: same session (Auto_Tssm)
   - consumes: `REPO_Vehicle_Code` produced within same flow
   - produces: `REPO_Description`, `REPO_Vehicle_Code`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Update_assertion`
   - screens: Vehicle Profile
   - detail: flows/00580001.md ; trace prefix `13:7:00580001`
8. **seq 8 - User** (`00360001`) - area: Other
   - actor: same session (Auto_Tssm)
   - consumes: `REPO_CODE` produced within same flow
   - produces: `REPO_CODE`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Update_ASSR`
   - screens: User
   - detail: flows/00360001.md ; trace prefix `13:8:00360001`
9. **seq 9 - User Profile** (`00350001`) - area: Master/Setup
   - actor: same session (Auto_Tssm)
   - consumes: `REPO_CODE` from seq 8 (00360001); `REPO_LOCATIONCODE` unresolved in group
   - checks: none configured
   - screens: User Profile
   - detail: flows/00350001.md ; trace prefix `13:9:00350001`
10. **seq 10 - DSR Profile DT** (`00560001`) - area: DSR/PJP/Route, Master/Setup
   - actor: same session (Auto_Tssm)
   - consumes: `REPO_DSRCODE` produced within same flow
   - produces: `REPO_DSRCODE`
   - checks: 10 message/field assertion(s); group assertion sheet(s): `DSR_Profile, Device_ASSR`
   - screens: DSR Profile, Demographics -> DSR Profile, Address -> DSR ProfileAddress,Business -> DSR ProfileAddress,Residence -> DSR Profile, Documents -> DSR Profile, Qualification ...
   - detail: flows/00560001.md ; trace prefix `13:10:00560001`
11. **seq 11 - DSR Approval DT** (`00390001`) - area: DSR/PJP/Route, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8) (same user as before: re-login only)
   - consumes: `REPO_DSRCODE` from seq 10 (00560001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: DSR Approval
   - detail: flows/00390001.md ; trace prefix `13:11:00390001`
12. **seq 12 - Outlet Profile** (`00530001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **AppUser** (serial 4)
   - consumes: `REPO_OutletCode` produced within same flow
   - produces: `REPO_OutletCode`
   - checks: 12 message/field assertion(s); group assertion sheet(s): `OutletProfile_Address_ASSR`
   - screens: OutletProfile,Demographics -> OutletProfile,Operative Info -> OutletProfile-Address -> OutletProfile-Address,Business -> OutletProfile-Address,Residence -> OutletProfile,Documents ...
   - detail: flows/00530001.md ; trace prefix `13:12:00530001`
13. **seq 13 - Prospect Outlet Approval** (`00380001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_OutletCode` from seq 12 (00530001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `FORWARD_ASSR`
   - screens: Prospect Outlet Approval
   - detail: flows/00380001.md ; trace prefix `13:13:00380001`
14. **seq 14 - Selling Category** (`00940001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **AppUser** (serial 4)
   - produces: `REPO_Selling_Category_CODE`
   - checks: 2 message/field assertion(s)
   - screens: Selling Category
   - detail: flows/00940001.md ; trace prefix `13:14:00940001`
15. **seq 15 - Section** (`00590001`) - area: Master/Setup
   - actor: same session (AppUser)
   - consumes: `REPO_OutletCode` from seq 12 (00530001); `REPO_SECTION_CODE` produced within same flow
   - produces: `REPO_SECTION_CODE`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Forward_assertion`
   - screens: Section -> Section Allowable -> Section Forward
   - detail: flows/00590001.md ; trace prefix `13:15:00590001`
16. **seq 16 - Section Approval** (`00720001`) - area: Approval/Reject/Terminate, Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_SECTION_CODE` from seq 15 (00590001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: Section Approval
   - detail: flows/00720001.md ; trace prefix `13:16:00720001`
17. **seq 17 - Company Mapping** (`00950001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **ULP_GLOBAL** (serial 3)
   - checks: none configured
   - screens: Company Mapping
   - detail: flows/00950001.md ; trace prefix `13:17:00950001`
18. **seq 18 - Distributor Mapping** (`00960001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_DSRCODE` from seq 10 (00560001); `REPO_WAREHOUSE` unresolved in group; `REPO_OutletCode` from seq 12 (00530001)
   - checks: none configured
   - screens: Distributor Mapping
   - detail: flows/00960001.md ; trace prefix `13:18:00960001`
19. **seq 19 - PJP Creation** (`00610001`) - area: DSR/PJP/Route
   - **SWITCH USER POINT**: log out and log in as **AppUser** (serial 4)
   - consumes: `REPO_DSRCODE` produced within same flow; `REPO_PJP_Number` produced within same flow
   - produces: `REPO_DSRCODE`, `REPO_PJP_Number`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: PJP Creation -> PJP Configuration -> PJP Configuration Forward
   - detail: flows/00610001.md ; trace prefix `13:19:00610001`
20. **seq 20 - PJP Approval** (`00800001`) - area: DSR/PJP/Route, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_PJP_Number` from seq 19 (00610001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: PJP Approval
   - detail: flows/00800001.md ; trace prefix `13:20:00800001`
21. **seq 21 - PJP Creation** (`00610001`) - area: DSR/PJP/Route
   - **SWITCH USER POINT**: log out and log in as **AppUser** (serial 4)
   - consumes: `REPO_DSRCODE` produced within same flow; `REPO_PJP_Number` produced within same flow
   - produces: `REPO_DSRCODE`, `REPO_PJP_Number`
   - checks: 2 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: PJP Creation -> PJP Configuration -> PJP Configuration Forward
   - detail: flows/00610001.md ; trace prefix `13:21:00610001`
22. **seq 22 - PJP Approval** (`00800001`) - area: DSR/PJP/Route, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_PJP_Number` from seq 21 (00610001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Forward_ASSR`
   - screens: PJP Approval
   - detail: flows/00800001.md ; trace prefix `13:22:00800001`
