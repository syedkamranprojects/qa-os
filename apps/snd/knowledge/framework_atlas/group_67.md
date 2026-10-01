# Group 67 - Daily Cycle Only Positive Flow_Astron

Source `gtf:67`. Market guess (from name): Astron. Rows: 21 (active 6, inactive 15). User switch points: 5 (4, 5, 9, 10, 16).

Allowed apps (alg): app 13 Astron_Centegy QA -> D:/Selenium/Automation/Astron_QA// (workbook variant inferred: None)
Starts with an app login flow: True (first active flow 02440001).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 1 - Login_Astron** (`02440001`) - area: Other
   - actor: same session (runner default login)
   - consumes: `LOGIN_USERNAME` engine provided; `LOGIN_PASSWORD` engine provided
   - checks: none configured
   - screens: Login_Astron -> Distributor Selection
   - detail: flows/02440001.md ; trace prefix `67:1:02440001`
2. **seq 4 - Order Booking_Astron** (`02480001`) - area: Order Booking
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - produces: `ORDERNUMBER`
   - checks: 1 message/field assertion(s); group assertion sheet(s): `ORD_BOOK_SAVE_ASSR`; value validations 3, Q2Q 0
   - screens: Order Booking_Astron -> Order Booking Detail_Astron -> Order Booking Detail2_Astron
   - detail: flows/02480001.md ; trace prefix `67:4:02480001`
3. **seq 5 - Delivery_Order_Planning Astron** (`02980001`) - area: Other
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `ORDERNUMBER` from seq 4 (02480001)
   - checks: 1 message/field assertion(s); group assertion sheet(s): `Delivery_Order_Planning_ASSR`
   - screens: Delivery Order Planning -> Delivery Ord Plan Released Astr -> Delivery Ord Plan DO Astr -> Delivery Ord Detail Astron
   - detail: flows/02980001.md ; trace prefix `67:5:02980001`
4. **seq 9 - Good Issue Note Astron** (`02560001`) - area: GIN (Goods Issue Note)
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_GINNO` produced within same flow
   - produces: `REPO_GINNO`
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_FORWARD_ASSR`, `Goods_Issue_Note_Detail_ASSR`
   - screens: Good Issue Note Astron -> GIN_CM_Selection_Astron -> Good Issue Note Detail_Astron -> Good Issue Note Forward_Astron
   - detail: flows/02560001.md ; trace prefix `67:9:02560001`
5. **seq 10 - Good Issue Note Approval Astron** (`02650001`) - area: GIN (Goods Issue Note), Approval/Reject/Terminate
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 9 (02560001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_FORWARD_ASSR`
   - screens: GIN Approval Astron
   - detail: flows/02650001.md ; trace prefix `67:10:02650001`
6. **seq 16 - cashmemo status_Astron** (`02590001`) - area: Cashmemo
   - **SWITCH USER POINT**: log out and log in as **None** (serial None) (same user as before: re-login only)
   - consumes: `REPO_GINNO` from seq 9 (02560001)
   - checks: 0 message/field assertion(s); group assertion sheet(s): `ORD_STATUS_SAVE_ASSR`
   - screens: Cashmemo Status_Astron
   - detail: flows/02590001.md ; trace prefix `67:16:02590001`

## Inactive rows (skipped by the engine)
- seq 2 Dispatch_Advice_Astron (`02420001`) status N
- seq 3 Dispatch Advice Approval (`00740001`) status N
- seq 6 Order Editing_Astron (`02520001`) status N
- seq 7 Order Cancellation_Astron (`02540001`) status N
- seq 8 Split Manual Order_Astron (`02570001`) status N
- seq 11 Good Issue Note Approval Astron (`02650001`) status N
- seq 12 Good Issue Note Approval Astron (`02650001`) status N
- seq 13 Order Editing After GIN_Asto (`02530001`) status N
- seq 14 Cashmemo Reschedule_Astron (`02580001`) status N
- seq 15 Order Cancellation_After_GIN_Astron (`02550001`) status N
- seq 17 Goods Return Note Astron (`02640001`) status N
- seq 18 Goods Return Note App Astron (`02630001`) status N
- seq 19 PJP Daily Inquiry Update DN_Astron (`02610001`) status N
- seq 20 Trip Status Inquiry_Astron (`02600001`) status N
- seq 21 Route Settlement_Astron (`02620001`) status N
