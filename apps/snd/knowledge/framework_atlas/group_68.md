# Group 68 - Primary Group Astron

Source `gtf:68`. Market guess (from name): Astron. Rows: 9 (active 9, inactive 0). User switch points: 4 (1, 7, 8, 9).

Allowed apps (alg): app 13 Astron_Centegy QA -> D:/Selenium/Automation/Astron_QA// (workbook variant inferred: None)
Starts with an app login flow: True (first active flow 02440001).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login_Astron** (`02440001`) - area: Other
   - **SWITCH USER POINT**: log out and log in as **Auto_Astron_QA** (serial 31)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Astron -> Distributor Selection
   - detail: flows/02440001.md ; trace prefix `68:1:02440001`
2. **seq 2 - Dispatch Advice Astron 2** (`02720001`) - area: Dispatch Advice
   - actor: same session (Auto_Astron_QA)
   - consumes: `REPO_DNNO` produced within same flow; `REPO_DocumentNo` produced within same flow
   - produces: `REPO_DNNO`, `REPO_DocumentNo`
   - checks: none configured
   - screens: Dispatch Advice Astron 2 -> DispatchAdviceDetailAstron -> DispatchAdviceUpdate
   - detail: flows/02720001.md ; trace prefix `68:2:02720001`
3. **seq 3 - Transfer_In_DA** (`02470001`) - area: Dispatch Advice
   - actor: same session (Auto_Astron_QA)
   - consumes: `REPO_DocumentNo` from seq 2 (02720001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Transfer_In_DA_ASSR`
   - screens: Transfer_In_DA -> Dispatch Detail_Transfer
   - detail: flows/02470001.md ; trace prefix `68:3:02470001`
4. **seq 4 - Dispatch_Advice_Astron** (`02420001`) - area: Dispatch Advice
   - actor: same session (Auto_Astron_QA)
   - consumes: `REPO_DOCUMENTNO` produced within same flow
   - produces: `REPO_DOCUMENTNO`
   - checks: 6 message/field assertion(s); group assertion sheet(s): `DA_FORWARD_ASSR`
   - screens: Dispatch Advice Astron -> Dispatch Advice Search _Astron -> Dispatch Advice Detail 2 Astron -> Dispatch Advice Detail Astron -> Dispatch Advice Grid Astron -> Dispatch Advice Loss_Astron ...
   - detail: flows/02420001.md ; trace prefix `68:4:02420001`
5. **seq 5 - Post Modification DA_Astron** (`02690001`) - area: Dispatch Advice
   - actor: same session (Auto_Astron_QA)
   - consumes: `REPO_DOCUMENTNO` from seq 4 (02420001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `Post Modification DA_ASSR`
   - screens: Post Modification DA Astron -> Post Modification Detail_Astron -> Post Modification Det2_Astron
   - detail: flows/02690001.md ; trace prefix `68:5:02690001`
6. **seq 6 - Stock Inquiry Astron** (`02760001`) - area: Stock Validation/Inquiry
   - actor: same session (Auto_Astron_QA)
   - checks: none configured
   - screens: Stock Inquiry Astron
   - detail: flows/02760001.md ; trace prefix `68:6:02760001`
7. **seq 7 - Order Booking_Astron** (`02480001`) - area: Order Booking
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - produces: `ORDERNUMBER`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_BOOK_SAVE_ASSR`; value validations 3, Q2Q 0
   - screens: Order Booking_Astron -> Order Booking Detail_Astron -> Order Booking Detail2_Astron
   - detail: flows/02480001.md ; trace prefix `68:7:02480001`
8. **seq 8 - Delivery_Order_Planning Astron** (`02980001`) - area: Other
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `ORDERNUMBER` from seq 7 (02480001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `Delivery_Order_Planning_ASSR`
   - screens: Delivery Order Planning -> Delivery Ord Plan Released Astr -> Delivery Ord Plan DO Astr -> Delivery Ord Detail Astron
   - detail: flows/02980001.md ; trace prefix `68:8:02980001`
9. **seq 9 - Good Issue Note Astron** (`02560001`) - area: GIN (Goods Issue Note)
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`
   - screens: Good Issue Note Astron -> GIN_CM_Selection_Astron -> Good Issue Note Detail_Astron -> Good Issue Note Forward_Astron
   - detail: flows/02560001.md ; trace prefix `68:9:02560001`
