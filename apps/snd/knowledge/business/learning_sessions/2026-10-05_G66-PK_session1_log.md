# Session log: LEARN-G66-PK/20261005 (framework group 66 "NG_Setup Flow_PK", learning walk)

Decided by the QA lead 2026-10-05: learning walk (business facts only), all 35 active flows, follow the workbook NG_Dcode_QA_Setup.xlsx as is (even where it touches group 11's distributor/PJPs/delivery men). Env cnr1dev1, company Unilever Pakistan Limited, distributor 15108843 (REPO_DISTRIBUTOR). Users: Maker Auto_Multi_Orga (serial 35, runner default), Checker Auto_Tssm (8), HeadOffice headquarter (30). Run sheet: run_sheet.md (atlas + workbook; positive rows PK ..-01 used).

## seq 1 Login (Auto_Multi_Orga, QA lead typed credentials; Claude picked company + distributor) - done

## seq 2 Distributor Profile DT (00970001) - done
- Menu search "Distributor Profile" offers 6 options: Distributor Profile, Distributor Profile HQ, Distributor Profile View, **Distributor Profile DT**, Distributor Profile TM, RCOA Distributor Profile [observed].
- DT screen: grid of the login distributor only (15108843 Auto KARACHI, Geo FS Karachi-TTY, Location Karachi West, Appointment 2024-12-26). Selecting the row fills the profile; tabs Demographics (with a drop-down: Demographics / Operative Info / Other Info / Address), Document, Bank, Contact Person Details; single Update button [observed].
- **The DT user can edit very little**: on Demographics only Off Days, GIN Initiation Time and **Invoice Print Message** are editable; everything else (code, name, MIS type HPC, geo, location, currency USD, registration, coordinates, prefix COL, auto inventory allocation Yes, manual order Yes, ...) is read-only [observed]. Operative Info is fully read-only (POP inactive days 1, limit 3, default delivery days 6, max order delivery days 6, scheme apply date Order Date, Auto GIN Yes, delivery optimization Yes, tax on date Order Date, margin 4, ref company code 1111, distributor type AutomationQA, sales org TEST, GPS restriction Yes, radius 2) [observed]. Other Info: Capital Investment 1, Credit Limit/Bank Guarantee 2 (editable).
- Workbook values differ from the live profile in many read-only fields (e.g. workbook Distributor 2411342 / name Automation KARACHI QA / currency PKR / MIS HPC; live 15108843 Auto KARACHI / USD); the framework only fills Invoice Print Message and Fax, so this does not matter [observed: drift note].
- Demographics: Invoice Print Message 4CHAIN44444 (already that value) -> Update -> **"Updated successfully"**; Operative Info -> Update -> "Updated successfully"; Other Info -> Update (no field changed; workbook 2/2 not entered by the framework) -> "Updated successfully"; Address has sub-tabs **Company / Business / Residence**; Residence: Fax 1234 -> Update -> "Updated successfully" [observed]. (Workbook Update_assertion = "Updated successfully": match.)
- Address Company tab: Premises 501, Darya Lal Street, Jodia Bazar, City Larkana, Region East (read-only), Locality Jodia Bazar - 1, mobile 03432026770; Residence: test values (21312, asd@asd.com) [observed].

## Method note (QA lead, 2026-10-05): follow each test flow's event flow
- Per screen, execute the active rows of fct_pr_sef_screen_events_flow in psef_sequenceno order; event 0000/0001 "Load Data" (EXCEL) = fill the screen's ACTIVE fields (fct_pr_sf_screen_field, psf_field_status Y) from the workbook row; screens with no active events are not executed. Positive workbook rows (PK ..-01, CASE_TYPE TN) are used.

## seq 3 Outlet Profile (00530001) - done: new outlet C0154187435 (Draft)
- Menu "Outlet Profile" (DYL_202009001); also Outlet Profile HQ / View / TM / Change Track Outlet Profile exist. Grid of outlets (Outlet Code, Name, Outlet Status, Approval Status; 287 pages) + form already in new mode (Save enabled, Add disabled) [observed].
- Demographics defaults on a new outlet: MIS Type Local Modern Trade, Currency PKR, Channel C00020 - FOH TOURISM, Geo f008, Outlet Rank A, Company Rank A, Area Type Urban, Identified by today (ro), Status In-Active (ro), Analysis A/B/C 0101, B2B enroll No (ro), Requested Section asf15124, WF status Draft [observed].
- Event flow 005301: Add -> Load Data (10 active fields: Short Name Automation, Long Name Automation QA TEST, Channel FOH TOURISM, Geo FS Karachi-TTY - 001004002001001001MHC001 (only 3 geo options), Company Rank A, Lat 1333, Long 22, Area Urban, Sub Distributor No) -> Save -> **"Saved successfully"**, Outlet Code generated **C0154187435**, WF Draft; tabs Documents/Bank/Contact/Credit Limit/Gallery become enabled [observed].
- 005302 Operative Info (via the Demographics drop-down: Demographics / Operative Info / Address): 18 active fields (B2B phone/email, Tax Exemption No, Tax Registered Registered, Tax Payer No, Advance Tax Exemption Yes, Tiers CA2T1, Perfect Village CA302, Channel TTS CA402, Perfect Store CA501, PS Compliance CA705, Point of Consumption ICTB001, Loyalty CA1102, Chain CA1302, Customer Attr 12 CA803, Classification CA904 - A, Outlet range 1221 - adug1; Outlet Programs left empty, no workbook value) -> Save -> "Saved successfully" [observed].
- 005304 Address (sub-tabs Company / Business / Residence; framework fills the Company tab only, Business/Residence screens have no active events): 19 fields (Automation, Saddar, Saddar1, ref 11, City Karachi -> Region East -> Locality (DHA) SADDAR, phones, mobiles (masked inputs), fax 1313, emails, ZIP 12121, postal 1111, opening 7:00, closing 8:00, estimate delivery 2024-12-13) -> Save -> "Saved successfully" [observed].
- 005305 Documents: Add a row -> NTN / 1111112222333330000 / 2024-12-13 / 2036-06-23 / Active / 1212 -> row Save -> **"Record Saved Successfully!"** [observed].
- 005306 Bank: Add a row -> Bank Al-Habib Limited / DHA Branch / Automation -> "Record Saved Successfully!" (Sr No 1) [observed].
- 005307 Contact Person: Add a row -> Automation / CNIC-test-update / 121212 / Manager / Intermediate / 60624113402 x2 / Automation@gmail.com -> "Record Saved Successfully!" [observed]. Drift: framework clicks `standardEditableGrid`, live add button is `standardEditableGrid1` (ids are for the recorder; noted only).
- 005308 Credit Limit: 10000 / Allowed / 6 / Allowed -> "Record Saved Successfully!" (Sr # 4309) [observed].
- 005310 Gallery, 005303 Other Info, 005309 Demographics Forward: no active events -> not executed; **the outlet is NOT forwarded by this flow (stays Draft / In-Active)** [db: sef; observed state].

## seq 4 Prospect Outlet (00380002) - PARTLY done, Forward blocked
- Menu "Prospect Outlet" (DYL_102003081) + "Prospect Outlet Approval" (DYL_102003100). Grid: Distributor Code/Name, Outlet Code, Outlet Name, Identified On, Identified by, Approval Status, Cancelled Status; it lists outlets of OTHER distributors too (50250327 MULLER & PHIPPS) [observed].
- Filter C0154187435 -> 15108843 Auto KARACHI / Automation QA TEST / 2026-10-05 / Identified by empty / **Draft** [observed]. Tabs Demographics (drop-down Demographics / Operative Info / Address), Document, Bank, Contact Person Name, Credit Limit, Gallery, Comment Log; buttons Update, Translation, Forward, Reject, Similar Outlets.
- Demographics: Outlet Type (MIS) "Local Modern Trade" -> **Modern Trade** -> Update -> "Updated successfully"; Operative Info -> Update -> "Updated successfully" (the Update button sat under a label until scrolled into view) [observed]. Workbook expects "Updated successfully": match.
- **Forward stays DISABLED** for this Draft outlet as Auto_Multi_Orga (also after a fresh reopen; also disabled on another Draft-less outlet of distributor 50250327 that was only selected, nothing changed). Outlets that reached Draft/Pending in the list have "Identified by" filled (e.g. IC11OI), ours is empty [observed]. Open: which user is the framework's "runner default login" for seq 1-4 (login flow 021400000 takes LOGIN_USERNAME from a repo value that is not in NG_Dcode_QA_Setup's GLOBAL-REPO), and what enables Forward on Prospect Outlet.
- Security note: framework table fct_pr_lu_login_users stores login passwords in plain text and the read-only connector returns them (seen by accident with SELECT *; not used, not recorded).

## Correction: users per row (QA lead's group query, run without the password column)
- Query (QA lead): fct_pr_gtfd_group_test_flow_detail d JOIN fct_pr_gtf_group_test_flow f LEFT JOIN fct_pr_lu_login_users u ON d.plu_serial_no=u.plu_serial_no LEFT JOIN fct_pr_tfd_test_flow_details tfd JOIN fct_pr_tf_test_flow tf, WHERE group='66' AND status='Y' ORDER BY sequence.
- Result: **seq 1-4 run as Automation (serial 28, login status N = the session's starting login)**; approvals (5, 7, 14, 16, 18, 22, 24, 26, 29, 31) Auto_Tssm (8); makers Auto_Multi_Orga (35); seq 32-34 headquarter (30); seq 35-36 Auto_Multi_Orga.
- The atlas showed seq 1-4 as "runner default login" (it treats login status N as "same session") - wrong for seq 1; to fix in build_atlas.py. **Deviation: seq 2-3 (and the seq 4 updates) above were executed as Auto_Multi_Orga instead of Automation.**
- Re-check as **Automation** (QA lead logged in; Automation lands directly on the menu, no company/distributor page): Prospect Outlet lists ~16 older "Automation QA TEST" outlets of 15108843 from earlier framework runs (C0124183421/22 of 2025-05-21, C0124186565-578 of 2025-10-24/27), **all still Draft** with "Identified by" = 2024-12-13 [observed] -> the framework's own seq 4 Forward evidently did not move them either.
- C0154187435 as Automation: **Forward still disabled** (Reject disabled too). Gallery tab is empty (Image Gallery + Upload) [observed]. Hypothesis (unconfirmed): Forward needs an outlet image in Gallery, or prospects must come from the mobile app. Waiting for the QA lead.
- QA lead: skip the Gallery image upload. -> seq 4 Forward NOT done; **seq 5 Prospect Outlet Approval skipped** (nothing pending to approve). Open question Q-PO1 for the QA Team Lead: what enables Forward on Prospect Outlet (image? mobile-identified prospects only? a role?); framework drift: seq 4/5 cannot pass as configured (16 earlier framework outlets stuck in Draft).

## seq 6 Section (00590001) - done (Allowable step not possible)
- Menu "Section" offers: Section Approval, Section Creation HQ, BG - Section Profile, **Section** (DYL_102003015), Section Bulk Upload, Section Setup [observed].
- New section form: Code read-only (generated), Description, Abbreviation, Status In-Active (ro), Origin Date today (ro); tabs Detail / Allowable; buttons Add, Save, Update, Translation, Forward, Reject [observed].
- Description Automation, Abbreviation "Automation section" -> Save -> **"Saved successfully"**, code **SEC000000067** (the workbook Code Auto24113402 is not enterable: the app generates SECnnnnnnnnn) [observed; drift].
- Allowable tab = outlets assigned to the section: available list (129 outlets, Code / Description / Sub Element / Start / Expiry, Select All, Batch Save / Revert). Filter on C0154187435 -> **0 rows: the Draft outlet is not offered**, so it could not be attached (in the framework the outlet would be approved at seq 4-5 first) [observed].
- Forward (Detail tab) -> comment "Automation Approval" -> Save -> **"Forwarded successfully"**; section stays In-Active until approved. Earlier framework sections of the same name exist (SEC000000053/65/66) [observed].

## seq 7 Section Approval (00720001, Auto_Tssm) - done
- Auto_Tssm lands directly on the menu (no company/distributor page). Menu "Section Approval" (DYL_BG1002): grid of pending sections only; SEC000000067 / Automation / Automation section / Auto KARACHI / In-Active. Selected -> tabs Detail / Allowable, buttons Forward + Reject only [observed].
- Forward -> comment "Automation Approval" -> Save -> **"Forwarded successfully"** -> the pending list is empty (one Checker step approves) [observed]. Workbook Forward_ASSR: match.
- QA lead decision on seq 6 Allowable: option B = after approval, tick ONE active outlet in Section Allowable and Batch Save (not Select All), to learn the mechanics; done next as Auto_Multi_Orga.
- Option B done (Auto_Multi_Orga): Section SEC000000067 is now **Active** after the approval. Allowable tab: "Show filter row" (filter_2), available Code filter 1000000001 + Enter -> row checkbox ticked -> Batch Save -> message **"Outlet already mapped with 124-Auto Section, 929292929222-section Testing, Auto03100043-Automation, ... SEC000000065-Automation, Sectin122025-HB_SECtion"** (about 50 sections, most from earlier framework runs) and the outlet appears in the section's assigned grid (Code / Description / Start Date / Expiry Date) [observed]. Rule: an outlet may belong to many sections; Batch Save saves and informs which other sections already hold the outlet (not an error) [observed; inferred: informational].

## seq 8 Selling Category (00940001) - done
- Menu "Selling Category" (DYL_102005); related: Selling category-Product hierarchy mapping, Selling Category Product Mapping, Selling Category Bulk Upload [observed].
- New form: Code read-only (generated), Description, Abbreviation, Entry Mode (default SKU), Status (empty), image path; Detail tab; Add/Save/Update [observed].
- Automation / Auto / SKU / Active -> Save -> **"Saved successfully"**, code **SEC000000035** (workbook Code Auto26243402 not enterable; selling categories also get SEC-prefixed codes) [observed].

## seq 9 Warehouse Profile (00570001) - done
- Menu "Warehouse Profile" (DYL_102003003); also Warehouse Profile Approval, Warehouse Profile -BG [observed].
- New form defaults: Code (ro, generated), Warehouse Type Sound Stock, Level No 1 (ro), Level Type D (ro), Status Active, Default empty [observed].
- Description Automation, Sound Stock, Active, Default No -> Save -> **"Saved successfully"**, code **C0000000216**; grid filter -> row (Code / Description / Warehouse Type / Status / Default) -> Update -> **"Updated successfully"** [observed]. No approval step for warehouses in this flow (a Warehouse Profile Approval option exists) [observed/db].

## seq 10 Vehicle Profile (00580001) - done
- Menu "Vehicle Profile" (DYL_1032); also Vehicle Profile View, Vehicle Profile Approval II, Vehicle Profile II, Vehicle Profile (NG0407) [observed].
- New form (Code ro, generated) with defaults: Status Active, Model Name Shezor Pakistan, Colour Navy Blue, Model Description 1ton, Fuel Petrol, Unloading Side Rear, Average Rate/Mileage/Min/Max Volume 1, Vehicle Type BIKE, Multi Trip No, Deep Freezer No, Cold Chain No, User Count 1, Unit Meters / Cubic + KG, weights 1/10, GSV/NIV/TIV 10/10 [observed].
- Workbook values entered (Description Automation241134, Auto Test, No, Active, Toyota, Blue, 1ton, 121-212, model 1212, chassis 1234, engine 22222, 1985, owner Automation, Petrol, DLY, 323.4,139.5,165, Top, rate 2, mileage 10, vol 1/10, Truck, multi-trip No, Captive, No, No, users 1, Meters / Cubic, KG, weight 200/1200, GSV 10/100000000, NIV 10/100000000, TIV 10/100000000). Limit Multi Trip is disabled while Allow Multiple Trips = No. **Owner CNIC is a 13-digit mask (#####-#######-#); the workbook value 42101121231231231 has 17 digits** -> first 13 digits entered (42101-1212312-3) [observed; drift].
- Save -> **"Saved successfully"**, code **999713523**; filter Code -> row -> Update -> **"Updated successfully"** [observed]. No approval in this flow.

## seq 11 Change Track Outlet Profile (00240001) - done: request 74 forwarded
- Menu "Change Track Outlet" offers Change Track Outlet Document / Operative Info / Profile; Profile opens /change-management/outlet-profile-management [observed].
- Screen: request grid (Request No, Description, Distributor, Status, Request Date; ~50 pages) + "List of Outlets" (Outlet Code/Name/Status/Approval Status, show-filter checkbox) + "Outlet Modification attribute" pairs (current value | New Value): Outlet Short Name, Long Name, Channel Hierarchy, Geographical Hierarchy, Outlet Rank, Company Rank, Latitude, Longitude, Area Type, Status, B2B Mobile Number, Manual Order Creation, Prospect ID; buttons Add, Save, Update, Forward, Reject, Cancel [observed]. **A Draft outlet (C0154187435) can be change-tracked.**
- New values (workbook): Aautomation_Outlet x2, channel **C10002 - Others** (workbook says "C10002 - OTHER", the option text is "Others"; 161 channel options), Outlet Rank A, Company Rank B, 5.8844 / 25.7291, Rural, Active, Yes, Yes, 1212 (geo left unchanged) -> Save -> **"Saved successfully"**, request **74** (status In-Active, 2026-10-05) -> select request -> Forward -> "Automation Approval" -> **"Forwarded successfully"** [observed]. (Workbook EXPECTED_MESSAGE "Saved Successfully" with capital S vs app "Saved successfully" - case drift.) No approval row for this request type in group 66.

## seq 13 Change Track Outlet Document (01340001) - BLOCKED (outlet not offered)
- Screen /change-management/outlet-document: request grid + outlet list (Outlet Code / Description / Status) [observed].
- C0154187435 is **not listed** (0 rows); neighbouring outlets are (C0154187407 TestOutl28_1 Active, C0154187434 nfTestOutl In-Active, ...) [observed]. Likely cause: our outlet is still a Draft (never approved, seq 4-5) and/or locked by the pending change request 74 [inferred]. Waiting for the QA lead (use another active test outlet, or skip seq 13-16).
- QA lead (2026-10-05): "try to approve 1000000001 outlet, use Automation user" -> REPO_OutletCode switched to **1000000001** (Aautomation_Outlet_01, group 11's outlet 01) for the outlet-dependent steps: retry seq 4 Prospect Outlet Forward as Automation, then seq 5 approval (Auto_Tssm), then seq 13-16. Caution recorded: approved document/operative changes on outlet 01 can change group 11 order tax.
- As Automation, Prospect Outlet filter 1000000001 (and partial 10000000) -> **0 rows**: the screen lists only outlets created as prospects (back-office Outlet Profile drafts / mobile prospects), not regular approved outlets. 1000000001 is already Active/Approved, so there is nothing to forward or approve for it [observed]. Plan: use 1000000001 directly for seq 13-16 (change track document / operative info + approvals); seq 4 Forward / seq 5 remain not done.

## seq 13 Change Track Outlet Document (01340001) on outlet 1000000001 - done: request 47 forwarded
- Outlet 1000000001 documents: (1) NTN 8798 **UN-Authorized**, (2) Tax Exemption 76878 Active [observed].
- Document grid filter Document Type NTN -> select row -> attribute pair "NTN | New Value", "8798 | New Value1"; buttons Add, Save, Update, Forward, Reject [observed].
- New Value NTN, New Value1 1111112222333330001 (workbook) -> Save -> **"Saved successfully"**, request **47** (description = old number 8798, In-Active, 2026-10-05) -> select request -> Forward -> "Automation Approval" -> **"Forwarded successfully"** [observed]. Earlier framework requests 43-46 (description 1111112222333330000, Active) exist from previous runs.

## seq 14 Change Track Outlet Document Approval (02200001, Auto_Tssm) - done
- Same menu option (CHANGETRACK_OUTL_DOC) for the Checker. Request list + outlet list; the first click on request 47 only selects it, the **second click opens it** (the framework also clicks row_1_request_no twice) -> shows NTN | NTN, 8798 | 1111112222333330001; buttons Forward + Reject enabled [observed].
- Forward -> comment "Automation approval" -> Save -> **"Forwarded successfully"**; the request row still shows In-Active right after (grid not refreshed, or further approval level - to check) [observed].
- Check after seq 14 (Auto_Multi_Orga): request 47 now **Active**; outlet 1000000001 documents = NTN **1111112222333330001** (status still UN-Authorized) + Tax Exemption 76878 Active -> approving a document change request replaces the document number at once (one Checker step) [observed].

## seq 15 Change Track Outlet Operative Info (01330001) on 1000000001 - done: request 50 forwarded
- Menu CHANGETRACK_OUTL_OPINFO -> /change-management; request list (66 rows) + outlet list + "Outlet Modification attribute" pairs [observed].
- Current operative values of outlet 01: Tax Exemption No, Tax Registered **Unregistered**, Tax Payer **Yes**, Tiers CA2T3, Perfect Village CA308 PV-2020, Channel TTS CA404 Supermarket, Perfect Store CA505 PS 8 Shelf, PS Compliance CA70 VAN, Point of Consumption NA, Loyalty CA1103 Others, Chain CA1201 ABC, Customer Attr 12 CA803 Others, Outlet Programs OP004 Charity Fair Sponsorship [observed].
- New values (workbook): No, **Registered**, **No**, CA2T1 Tier 1, CA302 Perfect City, CA402 Cosmetic TTS, CA505 PS 8 Shelf, CA70 VAN, CA1001 POC, CA1103 Others, CA1202 DOCY, CA801 WEW -> Save -> **"Saved successfully"**, request **50** -> Forward "Automation Approval" -> **"Forwarded successfully"** [observed]. NOT yet approved (seq 16 needs the QA lead's OK: approval would turn outlet 01 into a Registered / non-tax-payer outlet and change group 11 order tax).
- QA lead (2026-10-05): option 1 = approve request 50 as the workbook says (accepting the tax change on outlet 01).

## seq 16 Change Track Outlet Operative Info Approval (02220001, Auto_Tssm) - done
- Request 50 opened (second click opens it), new values shown; Forward -> "Automation approval" -> **"Forwarded successfully"** [observed]. **Outlet 1000000001 is now Registered / Tax Payer No (+ new tiers/attributes)** per the QA lead's decision; group 11 order tax for outlet 01 may differ from earlier sessions from now on.

## seq 17 DSR Profile DT (00560001) - done: DSR AUTO241134 forwarded
- Menu "DSR Profile" offers: DSR Profile (x2), Change Track DSR Profile, **DSR Profile - DT** (DYL_DT1002), DSR Profile Bulk Upload, DSR Profile - TM, DSR Profile Approval Bulk Upload, DSR Profile HQ, DSR Profile Bangladesh [observed].
- New DSR defaults: DSR Type 0001 - Order Booker, Sales Hierarchy NSM, Appointment today, Status In-Active (ro), Vehicle "28 - Vehicle 001", User ID Auto_Tssm, Designation Supervisor; tabs Demographics (drop-down Demographics / Address), Documents, Qualification, Previous Experience, Device [observed].
- DSR Code is typed by the user (needs a real click before typing): Auto241134 -> stored **AUTO241134** (upper-cased); name AutomationQ, Order Booker, Employee 1111, Sales Hierarchy DSR, appointment 2024-11-12, Counter Sales Yes, Working Nature Local, Vehicle **999713312 - Automation151825** (workbook vehicle from an earlier run; today's vehicle 999713523 was not used), Route Starting Distributor, Designation Manager, Incentive No -> Save -> **"Saved successfully"** [observed]. Workbook code was free (no duplicate message).
- Address -> Residence (Company / Business / Residence sub-tabs; framework fills Residence only): Automation QA, Saddar, Saddar 1, 1234, Karachi / South, landlines 31221234568, cells 60624113402, fax 1234, emails, ZIP 111, postal 1234 -> Save -> "Saved successfully" [observed].
- Documents: CNIC with workbook number 12026224113402222 -> **"Document Number-Value is Not According to the Format"**; the CNIC field is a mask **#####-#######-#** (13 digits; QA lead: format like 85420-0524526-5) -> 12026-2241134-0, 2024-12-04 / 2036-06-23 / Active / 1234 -> "Record Saved Successfully!" [observed; workbook drift].
- Qualification Intermediate / Intermediate / 2012 / Automation -> "Record Saved Successfully!"; Previous Experience Automation / Saddar / 32436111 / 60624113402 / 2022-05-16..2026-06-14 -> "Record Saved Successfully!"; Device Andriod (sic) / Automation / Samsung / Auto / 1234 / 123456 / 2024-11-12..2024-12-12 -> "Record Saved Successfully!" [observed].
- Forward (Demographics) -> "Automation Approval" -> **"Forwarded successfully"** [observed].
- QA lead: after the seq 18 approval, stop for today; continue tomorrow after the session with the QA Team Lead.

## seq 18 DSR Approval DT (00390001, Auto_Tssm) - done
- Menu "DSR Approval" (DYL_102003061): pending DSR grid (Distributor Code, Distributor, DSR Type, DSR Code, DSR Name, Employee No, Status) -> AUTO241134 / AutomationQ / Order Booker / 1111 / In-Active; open (second click) -> tabs Demographics, Documents, Qualification, Previous Experience, Device; Forward + Reject [observed].
- Forward -> "Automation Approval" -> **"Forwarded successfully"** -> pending list empty (one Checker step) [observed].
- Session paused here by the QA lead (2026-10-05); logout + browser closed.

## Status at pause (resume at seq 19 Distributor Mapping, Auto_Multi_Orga)
| Seq | Flow | Result |
|---|---|---|
| 1 | Login | ok (should be Automation; seq 2-3 ran as Auto_Multi_Orga = deviation) |
| 2 | Distributor Profile DT | done (4 x Updated successfully) |
| 3 | Outlet Profile | done: outlet C0154187435 (Draft) |
| 4 | Prospect Outlet | updates done; **Forward disabled** (Q-PO1) |
| 5 | Prospect Outlet Approval | skipped (nothing pending) |
| 6 | Section | done: SEC000000067 (+ outlet 1000000001 attached, option B) |
| 7 | Section Approval | done |
| 8 | Selling Category | done: SEC000000035 |
| 9 | Warehouse | done: C0000000216 |
| 10 | Vehicle Profile | done: 999713523 |
| 11 | Change Track Outlet Profile | done: request 74 (on C0154187435), forwarded, no approval row |
| 13/14 | Change Track Outlet Document + approval | done on 1000000001: request 47, NTN -> 1111112222333330001 |
| 15/16 | Change Track Outlet Operative Info + approval | done on 1000000001: request 50, outlet 01 now Registered / Tax Payer No |
| 17/18 | DSR Profile DT + approval | done: DSR AUTO241134 AutomationQ (CNIC 12026-2241134-0) |
| 19-36 | Distributor Mapping ... Delivery Man Shuffling | not started |
Records left on cnr1dev1 today: outlet C0154187435, section SEC000000067, selling category SEC000000035, warehouse C0000000216, vehicle 999713523, change requests 74/47/50, DSR AUTO241134.
Drift found (for FRAMEWORK_DRIFT.md): generated codes (section/selling category) vs fixed workbook codes; CNIC workbook values 17 digits vs 13-digit mask (owner CNIC, DSR CNIC); channel "C10002 - OTHER" vs "C10002 - Others"; "Saved Successfully" case; standardEditableGrid vs standardEditableGrid1; seq 4/5 cannot pass (16 earlier framework outlets stuck in Draft); atlas labels seq 1-4 user wrongly.
Questions for the QA Team Lead: Q-PO1 (what enables Prospect Outlet Forward), whether seq 1-4 must run as Automation for Forward, Outlet Allowable for a Draft outlet, request 74 has no approval row.
