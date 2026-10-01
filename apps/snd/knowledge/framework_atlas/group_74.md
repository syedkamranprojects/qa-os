# Group 74 - Pak All Promotion Charges

Source `gtf:74`. Market guess (from name): PK. Rows: 44 (active 22, inactive 22). User switch points: 20 (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22).

Allowed apps (alg): app 8 PK_Centegy QA 2 -> D:/Selenium/Automation/PAK_QA// (workbook variant inferred: Pak)
Starts with an app login flow: True (first active flow 021400000).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login Dcode** (`021400000`) - area: Login/Logout
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Dcode -> Distributor selection
   - detail: flows/021400000.md ; trace prefix `74:1:021400000`
2. **seq 2 - Dispatch Advice Reject Promotin** (`03810001`) - area: Dispatch Advice, Promotion, Approval/Reject/Terminate, Negative test
   - actor: same session (runner default login)
   - consumes: `REPO_DOCUMENTNO` produced within same flow
   - produces: `REPO_DOCUMENTNO`
   - checks: 4 message/field assertion(s); group assertion sheet(s): `DA_FORWARD_ASSR`
   - screens: Dispatch Advice Reject Promo -> Dis Advice Detail2 Reject Promo -> Disp Advice Reject promotion
   - detail: flows/03810001.md ; trace prefix `74:2:03810001`
3. **seq 3 - Dispatch Advice Appro Reject Promotion** (`03820001`) - area: Dispatch Advice, Promotion, Approval/Reject/Terminate, Negative test
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_DOCUMENTNO` from seq 2 (03810001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DA_APPR_Reject_Promo_ASSR`
   - screens: Dis Advice Appro Reject Promo
   - detail: flows/03820001.md ; trace prefix `74:3:03820001`
4. **seq 4 - Dispatch Advice Pormo** (`03610001`) - area: Dispatch Advice, Promotion
   - **SWITCH USER POINT**: log out and log in as **Automation** (serial 28)
   - consumes: `REPO_DOCUMENTNO` produced within same flow
   - produces: `REPO_DOCUMENTNO`
   - checks: 3 message/field assertion(s); group assertion sheet(s): `DA_FORWARD_ASSR`, `Dpatch_Advice_Promotion_ASSR`
   - screens: Dispatch Advice Promotion -> Dispatch Advice Promotion1 -> Dispatch Advice Detail2 Promo -> Dispatc Advice Detail Promotion -> Dispatch Advice Grid promotion -> Dispatch Advice Loss Promotion ...
   - detail: flows/03610001.md ; trace prefix `74:4:03610001`
5. **seq 5 - Dispatch Advice Approval Promotion** (`05750001`) - area: Dispatch Advice, Promotion, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_DOCUMENTNO` from seq 4 (03610001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DA_APPROVALFRWD_ASSR`
   - screens: Dispatch Advice Apprv Promo
   - detail: flows/05750001.md ; trace prefix `74:5:05750001`
6. **seq 6 - Batch_Promotion** (`03480001`) - area: Promotion
   - **SWITCH USER POINT**: log out and log in as **Automation** (serial 28)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Batch_Promo_ASSR`
   - screens: Batch Multiplication Promo
   - detail: flows/03480001.md ; trace prefix `74:6:03480001`
7. **seq 7 - Order Booking Promotion** (`00910001`) - area: Order Booking, Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `g_REPO_ORGA` unresolved in group; `g_REPO_CMDOCTYPE` unresolved in group; `ORDERNUMBER` produced within same flow; `REPO_REF_ORDER_NO` unresolved in group; `g_REPO_DISTRIBUTOR` unresolved in group
   - produces: `ORDERNUMBER`
   - checks: 2 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Order Booking -> Order Booking Detail -> Order Booking Detail2
   - detail: flows/00910001.md ; trace prefix `74:7:00910001`
8. **seq 8 - Transaction InquiryVal Ater OB Promotion** (`03530001`) - area: Order Booking, Transaction Inquiry, Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 3 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Trans InquiryVal AfterOB Promo -> Trans InqVal AftOB Detail Promo -> Trans InqVal AfterOB Head Promo -> Tran InqValOB Total Offer Promo
   - detail: flows/03530001.md ; trace prefix `74:8:03530001`
9. **seq 9 - Trans_Val_AfteOB_Charges_Promotion** (`03430001`) - area: Transaction Inquiry, Promotion, Charges/Tax
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 2 message/field assertion(s); value validations 2, Q2Q 0
   - screens: Transaction Val AfterOB Charges -> Transecti After OB Charges Tax -> Trans InqVal AfterOB Header Tax
   - detail: flows/03430001.md ; trace prefix `74:9:03430001`
10. **seq 10 - Stock Allocation_Promotion Testing** (`03370001`) - area: Stock Allocation, Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Stock_Allocation_ASSR`
   - screens: Stock Allocation
   - detail: flows/03370001.md ; trace prefix `74:10:03370001`
11. **seq 11 - Order Editing_Promotion Testing** (`03390001`) - area: Order Editing, Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 3 message/field assertion(s); group assertion sheet(s): `ORD_EDIT_SAVE_ASSR`, `ORD_EDIT_VALD_ASSR`, `Order_Editing_Teasting_ASSR`; value validations 2, Q2Q 0
   - screens: Order Editing Teasting -> Order Editing Detail Teasting -> Order Editing Detail4 Teasting
   - detail: flows/03390001.md ; trace prefix `74:11:03390001`
12. **seq 12 - Transaction_InquiryVal_Ater_Editing_Promo** (`03510001`) - area: Transaction Inquiry, Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 3 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Transa InqVal Aft Editing Promo -> Trans InqVal AftEdit Det Promo -> Trans Inq Edit Val After Header -> Tran InqEditVal TotalOfer Promo
   - detail: flows/03510001.md ; trace prefix `74:12:03510001`
13. **seq 13 - Editing After_Charges_Promotion** (`03440001`) - area: Order Editing, Transaction Inquiry, Promotion, Charges/Tax
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 2 message/field assertion(s); value validations 2, Q2Q 0
   - screens: Order Editing Aft Charges Promo -> Order EditinAft Charg Tax Promo -> Ord Editi Aft Charg Head Promo
   - detail: flows/03440001.md ; trace prefix `74:13:03440001`
14. **seq 14 - Delivery Date Change_Promotion** (`03450001`) - area: Delivery Date Change, Promotion
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `DELIVERYDATE_CHNG_ASSR`
   - screens: Delivery Date Change Promotion
   - detail: flows/03450001.md ; trace prefix `74:14:03450001`
15. **seq 15 - Goods Issue N_Promotion Reject** (`03540001`) - area: GIN (Goods Issue Note), Promotion, Approval/Reject/Terminate, Negative test
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `Delinkking_ASSR`, `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`, `SCreenhot_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue N Promo Reject -> G Issue N CM Selec Pormo Reject -> G Issue N Detail Promo Reject -> G Issue Note Grid promotion -> G Issue N CM Select Pormo D Link -> G Issue N Forwa promo Reject
   - detail: flows/03540001.md ; trace prefix `74:15:03540001`
16. **seq 16 - Goods Issue N Rejection promotion Approval** (`03560001`) - area: GIN (Goods Issue Note), Promotion, Approval/Reject/Terminate, Negative test
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_GINNO` from seq 15 (03540001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_REJECT_ASSR`
   - screens: Good Issue N Reject Appro Promo
   - detail: flows/03560001.md ; trace prefix `74:16:03560001`
17. **seq 17 - Good issue Note Forwd Terminet Promo** (`03850001`) - area: GIN (Goods Issue Note), Promotion
   - **SWITCH USER POINT**: log out and log in as **Automation** (serial 28)
   - consumes: `REPO_GINNO` from seq 15 (03540001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Save_Btn_ASSR`
   - screens: G Issue N Forwd Terminet promo
   - detail: flows/03850001.md ; trace prefix `74:17:03850001`
18. **seq 18 - Goods Issue Note Terminat promotion Approval** (`03570001`) - area: GIN (Goods Issue Note), Promotion, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_GINNO` from seq 15 (03540001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_TERMINATE_SAVE_ASSR`
   - screens: Goods Issue N Terminat Approval
   - detail: flows/03570001.md ; trace prefix `74:18:03570001`
19. **seq 19 - Goods Issue Note_Promotion** (`03470001`) - area: GIN (Goods Issue Note), Promotion
   - **SWITCH USER POINT**: log out and log in as **Automation** (serial 28)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`; value validations 1, Q2Q 0
   - screens: Goods Issue Note Promotion -> G Issue Note CM Select Pormotion -> G Issue Note Detail Promotion -> G Issue N Val Detail Promotion -> G Issue Note Forward promotion
   - detail: flows/03470001.md ; trace prefix `74:19:03470001`
20. **seq 20 - Goods Issue Note Approval Promotion** (`03550001`) - area: GIN (Goods Issue Note), Promotion, Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **Auto_Tssm** (serial 8)
   - consumes: `REPO_GINNO` from seq 19 (03470001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_REJECT_ASSR`
   - screens: Good Issue N Reject Appro Promo
   - detail: flows/03550001.md ; trace prefix `74:20:03550001`
21. **seq 21 - Trans Inq Validate after GIN Promotion** (`03620001`) - area: GIN (Goods Issue Note), Transaction Inquiry, Promotion
   - **SWITCH USER POINT**: log out and log in as **Automation** (serial 28)
   - checks: 3 message/field assertion(s); value validations 3, Q2Q 0
   - screens: Trans Inquiry val after GIN -> Trans Inquiry Detail  Val GIN -> Trans Inq Header Val GIN -> Total Offering Amt Val GIN
   - detail: flows/03620001.md ; trace prefix `74:21:03620001`
22. **seq 22 - Transaction Inquiry Afte GIN_Charges_Promotion** (`03630001`) - area: Transaction Inquiry, Promotion, Charges/Tax
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - checks: 2 message/field assertion(s); value validations 2, Q2Q 0
   - screens: Transaction Val Aft GIN Charges -> Transecti After GIN Charges Tax -> Trans InqVal Aft GIN Header Tax
   - detail: flows/03630001.md ; trace prefix `74:22:03630001`

## Inactive rows (skipped by the engine)
- seq 23 Order Editing_Promotion After GIN (`03660001`) status N
- seq 24 Trans Inq Validate after GIN Promotion order Editing (`03710001`) status N
- seq 25 Order Editing Aft GIN Charges Promotion (`03720001`) status N
- seq 26 Cashmemo Status Promotion (`03640001`) status N
- seq 27 Sale Return Promotion Reject (`03750001`) status N
- seq 28 Approval Promo Reject (`03760001`) status N
- seq 29 Sale Return Forward Detail Terminet Promotion (`03800001`) status N
- seq 30 Sale Return Terminet Apprv Promotion (`03780001`) status N
- seq 31 Sales Return Promotion (`03650001`) status N
- seq 32 Sales Return Forward Appr Promotion (`03860001`) status N
- seq 33 Sales Return Forward Appr Promotion (`03860001`) status N
- seq 34 SALES_RETURN Full promotion (`03690001`) status N
- seq 35 Sale Return Approval Promotion (`03790001`) status N
- seq 36 Transaction Inq Val After Sales R Partial Promo (`03870001`) status N
- seq 37 Transaction Inq Val After Sales R Partial Full Charges Promo (`03880001`) status N
- seq 38 Sales Return Status Change Promo (`03890001`) status N
- seq 39 Transaction Inq Val After Pick Promo (`03900001`) status N
- seq 40 Sales Return Status Change All Pick Promo (`03910001`) status N
- seq 41 Transaction Inq Val Sales Return Status Change Charges Promo (`03920001`) status N
- seq 42 Good Return Note Promotion (`03930001`) status N
- seq 43 Good Return Note Approval (`00810001`) status N
- seq 44 Route Settlement Promotion (`03940001`) status N
