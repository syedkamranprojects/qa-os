# Group 77 - Pak All Promotion Charges 2

Source `gtf:77`. Market guess (from name): PK. Rows: 22 (active 22, inactive 0). User switch points: 22 (23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44).

Allowed apps (alg): app 8 PK_Centegy QA 2 -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak)
Starts with an app login flow: False (first active flow 03660001).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 23 - Order Editing_Promotion After GIN** (`03660001`) - area: Order Editing, GIN (Goods Issue Note), Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `EDIT_SAVE_ASSR`, `EDIT_VALD_ASSR`, `Order_Editing_Promo_ASSR`; value validations 2, Q2Q 0
   - screens: Order Editing Promo Aft GIN -> Order Edit Detail Promo Aft GIN -> Order Edit Detail3 After GIN
   - detail: flows/03660001.md ; trace prefix `77:23:03660001`
2. **seq 24 - Trans Inq Validate after GIN Promotion order Editing** (`03710001`) - area: Order Editing, GIN (Goods Issue Note), Transaction Inquiry, Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 3 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Order Edit val after GIN Promo -> Ord Edit DetailVal Aft GIN Prom -> Ord EditHeade Val Aft GIN Promo -> Ord Edit T Offering Val GIN Pro
   - detail: flows/03710001.md ; trace prefix `77:24:03710001`
3. **seq 25 - Order Editing Aft GIN Charges Promotion** (`03720001`) - area: Order Editing, GIN (Goods Issue Note), Transaction Inquiry, Promotion, Charges/Tax
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 2 message/field assertion(s); value validations 2, Q2Q 0
   - screens: Ord Edit AftGIN Charges Promo -> Ord EditinAft GINCharg Tax Prom -> Ord Editi AftGIN Charg H Promo
   - detail: flows/03720001.md ; trace prefix `77:25:03720001`
4. **seq 26 - Cashmemo Status Promotion** (`03640001`) - area: Cashmemo, Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`
   - screens: Cashmemo Status Promotion
   - detail: flows/03640001.md ; trace prefix `77:26:03640001`
5. **seq 27 - Sale Return Promotion Reject** (`03750001`) - area: Sales Return, Promotion, Approval/Reject/Terminate, Negative test
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `Forwd_Save_ASSR`, `SReturn_PromoSave_ASSR`, `SReturn_PromoValid_ASSR`
   - screens: Sale Return Reject Terminet Pro -> S Retru Detl Rejec Terminet Pro
   - detail: flows/03750001.md ; trace prefix `77:27:03750001`
6. **seq 28 - Approval Promo Reject** (`03760001`) - area: Sales Return, Promotion, Approval/Reject/Terminate, Negative test
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `SReturn_AppvPromoSave_ASSR`, `SReturn_AppvPromoValid_ASSR`, `SReturn_AppvReject_ASSR`; value validations 3, Q2Q 0
   - screens: S Return View ApprvRej Pro -> S Return View Detl Apprv Promo -> S Return View Valid Promo Rej
   - detail: flows/03760001.md ; trace prefix `77:28:03760001`
7. **seq 29 - Sale Return Forward Detail Terminet Promotion** (`03800001`) - area: Sales Return, Promotion
   - **SWITCH USER POINT**: log out and log in as **Automation** (serial 28)
   - checks: none configured
   - screens: Sales R View Forwd Promo
   - detail: flows/03800001.md ; trace prefix `77:29:03800001`
8. **seq 30 - Sale Return Terminet Apprv Promotion** (`03780001`) - area: Sales Return, Promotion
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SReturn_AppvTerminetSave_ASSR`, `SReturn_Appvterminet_ASSR`
   - screens: Sale Return Terminet Approv Pro -> Sales Re Detl Terminet App Prom
   - detail: flows/03780001.md ; trace prefix `77:30:03780001`
9. **seq 31 - Sales Return Promotion** (`03650001`) - area: Sales Return, Promotion
   - **SWITCH USER POINT**: log out and log in as **Automation** (serial 28)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SaleRetDTL_SAVE_ASSR`, `SaleRetDTL_Vali_ASSR`, `Sales_Return_Val_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return Promotion -> Sales Return Detail Promotion -> Sales Return Validat Promotion
   - detail: flows/03650001.md ; trace prefix `77:31:03650001`
10. **seq 32 - Sales Return Forward Appr Promotion** (`03860001`) - area: Sales Return, Promotion, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SalesR_ViewForwdPromo_ASSR`
   - screens: Sales Return View Forwd Promo
   - detail: flows/03860001.md ; trace prefix `77:32:03860001`
11. **seq 33 - Sales Return Forward Appr Promotion** (`03860001`) - area: Sales Return, Promotion, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `SalesR_ViewForwdPromo_ASSR`
   - screens: Sales Return View Forwd Promo
   - detail: flows/03860001.md ; trace prefix `77:33:03860001`
12. **seq 34 - SALES_RETURN Full promotion** (`03690001`) - area: Sales Return, Promotion
   - **SWITCH USER POINT**: log out and log in as **Automation** (serial 28)
   - checks: 2 message/field assertion(s); group assertion sheet(s): `SALES_RFull_SavePro_ASSR`, `Sales_Return_Val_ASSR`; value validations 1, Q2Q 0
   - screens: Sales Return Full Promotion -> SALES_Retu Detil_Full Promo -> Sales Return FullVal Promotion -> Sales R Full Forward Promo
   - detail: flows/03690001.md ; trace prefix `77:34:03690001`
13. **seq 35 - Sale Return Approval Promotion** (`03790001`) - area: Sales Return, Promotion, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `SReturn_Approval_ASSR`
   - screens: Sale Return Approval Promo
   - detail: flows/03790001.md ; trace prefix `77:35:03790001`
14. **seq 36 - Transaction Inq Val After Sales R Partial Promo** (`03870001`) - area: Transaction Inquiry, Promotion
   - **SWITCH USER POINT**: log out and log in as **Automation** (serial 28)
   - checks: 3 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Trans InqVal Aft Sale R Promo -> Tra InqVal Aft SaleR Detl Promo -> Trans InqVal Aft Sale R H Promo -> Tran InqValSale R T Offer Promo
   - detail: flows/03870001.md ; trace prefix `77:36:03870001`
15. **seq 37 - Transaction Inq Val After Sales R Partial Full Charges Promo** (`03880001`) - area: Transaction Inquiry, Promotion, Charges/Tax
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 2 message/field assertion(s); value validations 2, Q2Q 0
   - screens: Trans Val Aft Sale R Charg prom -> Tran Aft Sale R Charg Tax Promo -> T InqVal Aftsales R H Tax Promo
   - detail: flows/03880001.md ; trace prefix `77:37:03880001`
16. **seq 38 - Sales Return Status Change Promo** (`03890001`) - area: Sales Return, Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 2 message/field assertion(s); group assertion sheet(s): `StatsChang_DTL_SAVE_ASSR`; value validations 2, Q2Q 0
   - screens: Sales Retur Status Change Promo -> Sales Re Statu Change Det Promo -> Sales R Status Change_Val Promo
   - detail: flows/03890001.md ; trace prefix `77:38:03890001`
17. **seq 39 - Transaction Inq Val After Pick Promo** (`03900001`) - area: Transaction Inquiry, Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 3 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Trans InqVal Aft Pick Promo -> Tra InqVal Aft Pick Detl Promo -> Trans InqVal Aft Pick H Promo -> Tran InqVal Pick T Offer Promo
   - detail: flows/03900001.md ; trace prefix `77:39:03900001`
18. **seq 40 - Sales Return Status Change All Pick Promo** (`03910001`) - area: Sales Return, Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `StatsChang_DTL_SAVE_ASSR`
   - screens: S R Status Change AllPick Promo -> S R Statu Change AllPic D Promo
   - detail: flows/03910001.md ; trace prefix `77:40:03910001`
19. **seq 41 - Transaction Inq Val Sales Return Status Change Charges Promo** (`03920001`) - area: Sales Return, Transaction Inquiry, Promotion, Charges/Tax
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 2 message/field assertion(s); value validations 2, Q2Q 0
   - screens: TransInq ValAft SRSG Charge Pro -> Transec Aft SRSG ChargeTax Pro -> Trans InqVal Aft S R S G H Tax
   - detail: flows/03920001.md ; trace prefix `77:41:03920001`
20. **seq 42 - Good Return Note Promotion** (`03930001`) - area: GRN (Goods Return Note), Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_GRN No.` unresolved in group
   - produces: `REPO_GRNNO`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GRN_FORWARD_ASSR`
   - screens: Goods Return Note Promo -> Good Return Note Detail Promo -> Goods Return N Forward Promo
   - detail: flows/03930001.md ; trace prefix `77:42:03930001`
21. **seq 43 - Good Return Note Approval** (`00810001`) - area: GRN (Goods Return Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_GRNNO` from seq 42 (03930001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GRN_APPROVAL_ASSR`
   - screens: Good Return Note Approval
   - detail: flows/00810001.md ; trace prefix `77:43:00810001`
22. **seq 44 - Route Settlement Promotion** (`03940001`) - area: Route Settlement, Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 1 message/field assertion(s); value validations 1, Q2Q 0
   - screens: Route Settlement Promotion -> Route Settlement Save Promo
   - detail: flows/03940001.md ; trace prefix `77:44:03940001`
