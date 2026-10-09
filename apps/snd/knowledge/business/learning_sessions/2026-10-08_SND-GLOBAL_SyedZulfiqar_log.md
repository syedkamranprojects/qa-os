# Training session log - S&D Claims

- Date: 2026-10-08
- Trainer: Syed Zulfiqar
- App: snd (DCODE)
- Market: GLOBAL unless the trainer says a rule is market-specific (as for promotions, see the 2026-10-07 session F1/F4)
- Environment: none used so far
- Methods: to be confirmed (verbal expected)
- Users: none (no live walk)
- Previous session: `runs/TRAIN-SND-GLOBAL/20261007-SyedZulfiqar/` (Promotions and Budget) is **paused, not consolidated**; its open questions will be answered later by the trainer [stated 2026-10-08 Syed Zulfiqar].
- Known before this session (from the R2 deck "Promotions and Budgets 2026_R2.pptx", s.42-50; not yet confirmed by training):
  - Claims for promotions and damages are settled outside DCODE, based on a claims generation report.
  - A scheduled job runs on the 10th, 20th and 30th (set per distributor by "Claim Days", Operative Info tab) and sends claim data to Atlas: DIST_CD, Claim_No, Cust_CD, Doc_No (credit note / invoice), Dist_claim_amount (budget used / credit note), Promo_cd (promo or IO code).
  - Power BI Reports > Sales: claim report by Claim From / To Date with Claim Number, Type (Promotion, Incentive, Others, Damage), Description, Date, Amount, Status (Acknowledged, Approved by HQ, Cancelled, Closed Transaction, Draft, Pending for HQ Approval, Pending for HQ Final Approval, Pending for Main Dist. Approval, Rejected by HQ, Rejected by Main Dist.).
  - Off-invoice route: IO Listing (Transaction > Claim) -> Off-Invoice Credit Note upload -> Credit Note Forward -> Off-Invoice Credit Note Approval; the promotion header's I/O number traces which promotion a claim was made against.

## Sources
- `claim management manual_R2 Aug 2026.pptx` (trainer's Desktop, 12 slides, Centegy, R2, Aug 2026). Text read in full 2026-10-08; screenshots not yet viewed. To be filed as `apps/snd/knowledge/sources/20261008_claim management manual_R2 Aug 2026.pptx`.

## Document digest (tag: [stated 2026-10-08 doc:claim management manual_R2 Aug 2026.pptx s.<n>])
- D1 (s.2-3) **Claim Inquiry** lists existing claims: Document Type, Document No., Claim Number, Claim Reference Number, Credit Note Number, Claim Amount, Claim Start / End Date, Document Date, Status (Active / Inactive), Last Execution Date (last run of the claim-creation job on the Adhoc Executor), Project Code (no description).
- D2 (s.4) **Claim Detail** tab (click a claim): the promotions in the claim - Promo Code, Ref Promo Code, Description, Promo Start / End Date, Claim Amount.
- D3 (s.5) **Reference Info** tab (click a claim detail row): per outlet - Promo Code, Description, Ref Promo Code, Invoice No., Reference Document Type, Outlet Code / Description, Claim Amount.
- D4 (s.6-7) **Adhoc Job Executor**: run the claim job manually (select details, Execute -> "Message sent successfully.") or automatically (scheduled in advance). The toast does not prove a claim was created; the conditions below must hold.
- D5 (s.8) Condition 1: orders must be **Delivered** and their document date **N-1**; claims are always generated for N-1 orders, and likewise the GIN date. Check in Transaction Inquiry, Document Status.
- D6 (s.9) Condition 2: **Claim Days** must be defined on the distributor profile (Distributor Profile DT, Operative tab).
- D7 (s.10) Condition 3: Promotion Layout fields **Claim** (Yes / No) and **Claimable %**: No = the distributor cannot ask the company for reimbursement; Yes = Claim % is mandatory.
- D8 (s.10) Condition 4: resultant type must be **Bonus Type 2** (long-term scheme for wholesalers) or **Trade Offer** (short-term scheme for wholesalers); currently these give customer discounts in Pakistan. (Matches the BONUS2 / TRADEOFFER lines seen in Total Offering in group 11.)
- D9 (s.11) Claim amount = the Claim % applied to the promotion discount shown in Transaction Inquiry > Total Offering.

## PJP document (added 2026-10-08)
Source: `apps/snd/knowledge/sources/inbox/PJP updated R2.pptx` (25 slides, "PJP Master - DCODE: User Guide", v1.1, last updated 06-Aug-2024, market Pakistan, participants DT user; file name says R2). Text read in full; screenshots not viewed. Tag: [stated 2026-10-08 doc:PJP updated R2.pptx s.<n>].
- P1 (s.4) Every Order Booker and every Delivery Man has a PJP (Permanent Journey Plan), built from sections (outlets), selling category, frequency and working days. The Order Booker works only per his PJP; his PJP is downloaded to the handheld as the day's list of outlets to visit.
- P2 (s.4) Selling category = logical grouping of products (sales, delivery, marketing, promotions). Section = group of outlets assigned to a DSR for booking or delivery.
- P3 (s.5) PJP Creation (Distributor Setup > Journey Plan > PJP Creation) lists all OB and DM PJPs; naming advice: <name>_OB for order bookers, <name/ID>_DM for delivery persons.
- P4 (s.6) Header: PJP Number (unique), DSR (order booker), Working Date, Default, Status, Level Type / Level No, Enable NFC / Mandatory NFC, GPS Restriction / GPS Radius (m), DDO Indicator, Sales Route Type, PJP Description, Warehouse, Closing Date, Virtual PJP (for B2B orders placed directly by an outlet; created by the implementation team).
- P5 (s.7, s.9) Actions Add, Save, Update, Forward, Reject. Maker fills header + configuration, Forward to the **TM user**; TM opens the pending PJP on the same screen, Forward = approve / Reject. Status becomes Active on TM approval.
- P6 (s.8) Configuration tab rows: PJP Serial No (auto), Selling Category (only those allowed for the DT), Section, Frequency (Daily / Weekly / Monthly / Yearly), Repeat Days (number of days in the period, e.g. Monthly + 5 = 5 days, then the days are chosen), Start Date, **Reference PJP**.
- P7 (s.8) Reference PJP links an Order Booker PJP to a Delivery Man PJP and vice versa; every order PJP must be linked to a delivery PJP. Delivery app: the delivery PJP is mandatory. Without delivery optimisation (DT / non-Locus) a manual picklist is generated from the delivery PJP and the cash memos of the OB PJPs linked to it. (Matches group 11: OB PJP 02111 -> delivery PJP 02112.)
- P8 (s.10-11) PJP Change Request (Distributor > Journey Plan): approved PJPs only; change Description, DSR, Warehouse, Status, GPS Restriction / Radius, DDO Indicator, Sales Route Type; Save, then Forward for approval.
- P9 (s.12-13) Change Track PJP Config: pick an approved PJP, then one configuration row; change Selling Category, Section, Frequency, Repeat Day, Start Day, Reference PJP; Save + Forward; TM approves with Forward on the request (grid: Request No, Description, Distributor, Status, Request Date).
- P10 (s.14-17) Selling Category (Company Setup > General): Code, Description, Abbreviation, Entry Mode, Status, Image Path; products are mapped to it in Company Mapping (Company Setup > Setup Mapping), Selling Category tab, allowable -> mapped.
- P11 (s.18-19) Section (Setup Configuration > PJP > Section): Code, Description, Abbreviation, Status, Origin Date, **Default delivery days** (number of days used to compute the expected delivery date).
- P12 (s.20-22) Outlets are mapped to a section on the Section screen's Allowable tab, or on Distributor Mapping (Distributor Setup > Setup Mapping) Section tab (lists the distributor's active outlets).
- P13 (s.23) Section Bulk Upload (Distributor Setup > Journey Plan): pick PJP + Section, Download Excel, edit, Upload Excel; errors come back as an error file with the message in the last column; template columns Distributor Code, Section Code, Section Name, Outlet Code, Outlet Name (long name).

## Outlet document (added 2026-10-08)
Source: `apps/snd/knowledge/sources/inbox/outlet changes.pptx` (25 slides, "Outlet Master - DMS-NG: User Guide", v1.2, Centegy; no market or date given). Text read in full; screenshots and the embedded narration audio not reviewed. Tag: [stated 2026-10-08 doc:outlet changes.pptx s.<n>].
- O1 (s.3) Outlets can be created by company / global users or by distributors; **a distributor-created outlet needs approval by a company user** to become active.
- O2 (s.3-4) Screens: Outlet Profile (creation), Outlet Approval II, Change Track Outlet Profile, Change Track Outlet Operative Info, Change Track Outlet Document, Analysis Classification - Outlet, Outlet Status, Outlet Profile View, Outlet Change Track Excel, Outlet Creation Upload, Outlet Price.
- O3 (s.6-7) Demographics: Outlet Code auto-generated; Long / Short Name; Previous Outlet Code; **Channel Hierarchy** mandatory (last level, e.g. Bakery, Restaurant); **Outlet Type** mandatory (Local Modern Trade, Modern Trade, General Trade...); Currency; Geographical Hierarchy; Outlet / Company Rank (user-defined); latitude / longitude; Area Type; Identified By / On; Status (auto, Active / Inactive); Ship To Code; Bill To Code (head-office outlet that is billed); Analysis 1-3; Is B2B; Activation Date (mandatory); Sub Distributor + Code (code mandatory); Manual Order Creation; Completion Date; Requested Section; Approval Status; Prospect ID.
- O4 (s.8) Operative Info: tax fields **Tax Registration, Tax Exemption, Tax Registered (mandatory), Tax Payer, Auto Tax Invoice, WHT flag**; also Perfect Store (+ date), SMS Notification, Post-dated Cheque, B2B phone / email, Barcode + Barcode Scanning, preferred order / delivery times, Auto Cheque Realization, Restrict Un-Mapped Bank. (Links to the group 11 outlet tax profile and Q-TX1.)
- O5 (s.9) Classification attributes (Tiers, Perfect Village, Channel TTS, Perfect Store Compliance, Point of Consumption, Loyalty Programs, Chain Outlets, Customer Attribute 12, Outlet Programs) + GPS Restriction / Radius; their values come from **Analysis Classification - Outlet** (prerequisite).
- O6 (s.10-12) Other Info (Shopper Type; Company Turnover and Overall Total Turnover mandatory; stock selling / holding capacity); Documents (number, issue / expiry date, status, reference); Bank (bank, branch, details); Contact Person; **Credit Limit** (Credit Amount Limit + Amount Action, Day Limit + Day Action).
- O7 (s.13) Outlet Approval II (company user): new outlets listed with status **PROSPECT** (= inactive); select, Approve or Reject; a "similar outlets" pop-up shows outlets with similar attributes (duplicate check).
- O8 (s.14-17) Changes to approved outlets go through change-track screens: Profile (long name, ranks, area type, status, B2B mobile, manual order creation, prospect ID), Operative Info, Document; each = select outlet, edit, **Forward for Approval**; the request appears in the grid above for review and approval. (Group 66 seq 13-16 changed outlet 1000000001's NTN and tax flags this way, 2026-10-05.)
- O9 (s.18) Analysis Classification Outlet: pick analysis type, Edit a classification, Save -> success pop-up.
- O10 (s.19) Outlet Status: lists active outlets; select, Process -> "Are you sure you want to proceed?" Yes -> "Process completed successfully." -> outlet becomes **inactive** (check on Outlet Profile).
- O11 (s.20) Outlet Profile View: read-only.
- O12 (s.21) Outlet Change Track Excel: filter by Distributor, PJP Number, Section, Geo Hierarchy Code, Outlet Channel; Download Excel, edit, Upload Excel; updates show on Outlet Profile.
- O13 (s.22) Outlet Creation Upload: Download Template, fill, Upload Excel; new outlets show on Outlet Profile.
- O14 (s.23) Outlet Price: pick an outlet and set / review product prices for it.
- Doc issue: s.17 (document change) says to search "Change Track Outlet Operative Info"; probably means Change Track Outlet Document.

## Jira evidence for the PJP questions (read 2026-10-08, centegy.atlassian.net, project SDMS; tag [jira <key>], to be confirmed by the trainer)
- J1 daily PJP: a **PJP creation job** generates the **PJP Daily** (daily route) records; it runs on cnr1dev1 (SDMS-9885, PK/BD, env cnr1dev1). It should skip distributor holidays (SDMS-9801, PK prod bug, Assigned to QA; SDMS-10441 B2B PJPs on DT holidays). The **Order Booker PJP Working Date** should follow the daily route generation date (SDMS-11041, R2 story, QA Verified). After Route Settlement with no orders, the **Delivery Man PJP Working Date** should move to the next scheduled PJP date (SDMS-11166, R2, QA Verified). GIN approval checks that the PJP configuration covers today; otherwise "PJP not created" (SDMS-9297, PK/BD R1, QA In Progress; friendlier message requested). The DM daily / DSR file is generated separately (DSR File Generation, SDMS-6732/6852).
- J2 delivery date: Section **Default delivery days** takes precedence over the **distributor's default delivery days** (SDMS-10310, R2 hot fix, QA Verified); section value must not exceed the DT profile's **Maximum Delivery Days** (SDMS-11316 VN R2 bug, New; SDMS-12248 Section Creation HQ validation bug, New).
- J3 frequency: in R2 TH a frequency model F1 / F2 / F4 (visits per month over 24 working days) exists at outlet level via "PJP Creation HQ - Outlet level" / PJP Configuration Bulk Upload II (SDMS-10114, TH R2); configurations have a start date and the previous configuration's end date is set to start date - 1. GIN example config: Start Date + week days Fri/Sun (SDMS-9297). Not yet clear for the PK screen's Daily / Weekly / Monthly + Repeat Days.
- J5 / inactive: same DSR on 2 PJPs (one inactive) gives "PJP head does not exist" at Start of Day (SDMS-11331/11332, PH, open); inactive PJP + DSR removal hides the PJP (SDMS-10939 BD, SDMS-11255 invalid).
- Other: PJP Configuration "Duplicate Record Found" from number generation (SDMS-12418, PK R1 prod, New); BG PJP code auto-generated with the DT prefix (SDMS-11391); section forward / reject error when outlets mapped (SDMS-12115, TH).
- Second SDMS search (2026-10-08):
  - J3: PK/BD R1 configuration row = Selling Category, Section, **Frequency, Repeat Days, Week Day First, Start Date, Expiry Date, Reference PJP** (SDMS-9087 PKBD R1, SDMS-6631 Merge PKBD). Weekly / Monthly / Yearly without the day(s) is refused with "PJP cannot be scheduled for the weekend marked days." (SDMS-6631, closed as Invalid Bug = treated as expected). Fortnightly (F2) story for PKBD: first visit on the first selected weekday from the start date, then every 14 days until the expiry date; "changes will be made in the ad hoc executor" (SDMS-4040, Assigned to QA).
  - J1 (support): the PJP schedule is executed through the **Adhoc Executor** job (SDMS-4040 note), consistent with the "PJP creation job" (SDMS-9885, cnr1dev1).
  - J2 (support): BD route table in SDMS-4040 pairs each order day with the next day as delivery day (e.g. order Thursday, delivery Friday).
  - J5: an outlet **can** be mapped to more than one section: the grid shows an outlet already mapped to another section in green (SDMS-4060 / 4062 CR track, 4061 / 4083 TH/PH); a prompt "Outlet already mapped with: <sections>" was requested (SDMS-744); a **"unique section" setting** is meant to stop multiple mapping (SDMS-1896 BD, New: did not stop it); removing an outlet from its only section is refused "...must be associated with another section" (SDMS-1550); an outlet listed twice in a section stopped order processing (SDMS-6535 BD).
  - J4: no ticket found on who the TM approver is.
## Jira evidence for promotion, budget, claims, outlet (SDMS search 2026-10-08, trainer authorised; to be confirmed)
- Promotion / budget:
  - Order edit gives budget back: "Utilized budget is not getting reverted for the order edited through Order Editing" was a bug, Verified and Closed (SDMS-5481, R2) -> edit re-prices and re-books the budget. Cancellation should reverse it too: PK prod bug "promo amount of a cancelled invoice was not reversed into its budget" (SDMS-11596, PK R1, New).
  - **Free goods DO use budget (quantity)**, but only for free SKUs actually given: PK/BD bug - free SKU added back to budget on partial return although never given because stock was 0 (SDMS-10626, PKBD R1, env CNR1DEV1, QA Verified); VN - budget must not be utilised when the free SKU qty is not allocated (SDMS-10863, R2). Budget can be quantity-based at ORGA level (SDMS-10146 PK/BD).
  - Fresh return used budget although no promotion applied = bug (SDMS-10625 / porting SDMS-10663).
  - Promotions can be **constrained (check budget = Y) or unconstrained** (no budget check) (SDMS-11953).
  - **Bulk Promo Allocation** = the budget allocation upload of Budget Setup (SDMS-9438 "(PK) PROD - Budget Setup (Bulk Promo Allocation)"; "Adjust Promo Allocation" SDMS-11264, 10146); duplicate distributor rows in the upload give a server error (SDMS-10610 PK prod, 11264).
  - Purchase limit per cash memo (SDMS-3027 BD, invalid) and per slab unit (SDMS-11686): purchase limit applies per invoice; Discount Cap vs Discount Limit: no ticket distinguishes them.
  - Current Promotion Approver issues are TH/PH (end date edits, SDMS-4237, 4752, 7902); integrator schedule: no ticket found.
- Claims (PK/BD = R1 unless noted):
  - Two claim families: **Jupiter** and **Non-Jupiter** (on-invoice promotion) claims, each generated by its own job (SDMS-12373, 12134, 12147, 11880, 11427).
  - Schedule (BD CR, SDMS-7051, QA Verified): was weekly on Saturday night if all DM routes settled, else Sunday; changed to an **organisation claim calendar** (backend "Organization Claim Period", SDMS-7263 / 7265) with weekly + month-end dates; on each date the job takes **all delivered orders from the last executed claim's From Date to the current date (To Date), using the actual delivery time**; the route-settlement check was removed for Non-Jupiter.
  - Jupiter claim generated for an **unsettled** open working date = defect (SDMS-12408 BD, Open) -> Jupiter claims expect the route settled.
  - TH R2 model (SDMS-11924): Claim Period Setup per distributor; claims per **IO number** for orders delivered and **returns picked** in the period; later returns can produce **negative claims** in later cycles; no duplication of transactions; claims shown in Claim Inquiry Doc Wise and sent by a scheduled integration job (PEGA in TH).
- Outlet (PKBD R1, SDMS-12227, Assigned to QA, Sept 2026): role-based workflow **DT (role 0005) creates -> Draft; TM (role 0008, screen Outlet Profile TM) reviews / edits and Forwards; HQ (role 0001, Outlet Approval) approves -> Active / Approved, or rejects -> In-Active / Rejected (editable again)**. After activation a DT user may edit only 4 fields (phone, contact person, credit limit amount, credit limit days); TM view only. Completion Date = first activation date-time; Activation Date = first creation date-time. Credit limit: only one row allowed (SDMS-12365, New).
  - **Possible contradiction** with F1 (outlet approval only for DT users; company users need none) and the deck (company user approves on Outlet Approval II): SDMS-12227 adds a TM forward step. Likely a newer R1 change; ask the trainer which applies on cnr1dev1.
  - Same story gives the TM role code **0008** -> J4: the "TM user" who approves PJPs is a TM-role user (0008); whether Auto_Tssm holds it is still to confirm.
- Note: SDMS-10310's description contains a plain-text login for a UAT environment (not copied here).

## Open questions - ON HOLD (trainer will answer later; do not re-ask until he returns to the topic) [stated 2026-10-08 Syed Zulfiqar]
- C1 Claim Days and N-1: with Claim Days 10/20/30 and a run on the 20th, does the claim cover only the 19th or every delivered order since the last claim? What do Claim Start / End Date hold?
- C2 Return or cancellation after the claim is created: is the claim reduced, or adjusted in the next period?
- C3 Grouping: one claim per distributor per run, with promotions as detail lines?
- C4 After creation: does the claim go to Atlas, and where do the approval statuses (Pending for HQ Approval, Approved by HQ, ...) come in?
- C5 Name of the claim job in Adhoc Job Executor and the fields selected.
- C6 Can a claim job be tried on cnr1dev1 (R1) for one day of group 11 orders, or is it R2 only?
- PJP questions on hold [stated 2026-10-08 Syed Zulfiqar]:
  - J1 How is the daily PJP record (used by Route Settlement / day close) created from the permanent PJP: job or first use of the day?
  - J2 Planned delivery date of an order: from the section's Default delivery days or from the delivery PJP's visit days?
  - J3 Frequency / Repeat Days: Weekly + 2 = pick two weekdays? What does Start Date / Start Day do for Weekly?
  - J4 TM approver on cnr1dev1: the Checker (Auto_Tssm) or another user?
  - J5 Can one outlet be in several sections / PJPs (e.g. per selling category)?
- Promotion / budget questions on hold: see `runs/TRAIN-SND-GLOBAL/20261007-SyedZulfiqar/session_log.md` (Open) and the QA-team doc's "Open questions" (order edit give-back, Discount Limit vs Cap, integrator schedule, free goods vs budget, R1 gaps, Bulk Promo Allocation / Cash Memo Promotion Viewer, test data on cnr1dev1).

## Facts

| # | Fact | Tag | Affects |
|---|---|---|---|
| F1 | Outlet approval is required **only when a DT (distributor) user** creates or changes the outlet; an outlet created / changed by a company user needs no approval. | [stated 2026-10-08 Syed Zulfiqar] | outlet page; O1, O7, O8 |
| F2 | An approved change to an outlet's tax flags (Operative Info) applies to **new orders only**; orders already booked keep their tax. (Fits Q-TX1 / the zero-tax rule: a booked zero-tax invoice of an outlet that is no longer exempt cannot be delivered.) | [stated 2026-10-08 Syed Zulfiqar] | outlet page, order_booking.md, delivery rule |
| F3 | Credit limit actions are configured per outlet: **Block** blocks order booking when the amount / day limit is exceeded; **Warn** shows a warning at order booking. The check is made at order booking. | [stated 2026-10-08 Syed Zulfiqar] | outlet page, order_booking.md (negative cases) |
| F4 | **Outlet Price overrides the normal price list** for that outlet's products. | [stated 2026-10-08 Syed Zulfiqar] | outlet page, order_booking.md (pricing) |
| F6 | Ruling on the outlet "conflict": there is **no conflict**. An outlet created by a DT user is approved by a company / HQ user (F1 and the deck agree). SDMS-12227's TM forward step (DT 0005 -> TM 0008 -> HQ 0001) is a step before the HQ approval, not a different approver; recorded as Jira detail, not a contradiction. | [stated 2026-10-08 Syed Zulfiqar] | outlet page; supersedes the "possible contradiction" note in the Jira evidence section |
| F7 | **Auto_Tssm is the TM user** on cnr1dev1 (our Checker): it approves PJPs (Forward on PJP Creation / Change Track PJP Config) and is the TM in the outlet DT -> TM -> HQ flow. Answers J4. | [stated 2026-10-08 Syed Zulfiqar] | PJP page, outlet page, app.yaml roles note |
| F8 | Scheduled jobs each have their own schedule: the **PJP (daily route) job runs daily**; the **claim job is planned weekly or daily** (per configuration; cf. the BD claim calendar SDMS-7051); the **target achievement job runs daily**. The schedule of the job that brings Excel-approved promotions into DCODE was not stated separately. | [stated 2026-10-08 Syed Zulfiqar] | PJP page (J1), claims page (C1/C5), promotions page (F15), test design (wait for the job run) |
| F9 | The claim job's name **differs per market** (answers C5 in general; the PK name is to be read from Adhoc Job Executor on cnr1dev1 during a live walk; PK/BD Jira uses "Jupiter" and "Non-Jupiter" claim jobs, SDMS-7110, 12373). | [stated 2026-10-08 Syed Zulfiqar] | claims page, app.yaml markets (per-market job names) |
| F10 | The integrator job that brings **Excel-approved promotions** (Current Promotion Approver) into DCODE **runs daily**; an approved Excel promotion reaches orders after the next daily run. | [stated 2026-10-08 Syed Zulfiqar] | promotions page (F15 of 2026-10-07), test design |
| F11 | Discount Limit vs Discount Cap: **not clear to the trainer either**; parked. Raise it again only when a live run or ticket shows a difference (keep both as separate fields until then; do not assert either). | [stated 2026-10-08 Syed Zulfiqar] | promotions page (open question, class B: settle live) |
| F5 | Operative Info holds only the outlet's operational information (not its documents). So the deck's s.17 instruction to search "Change Track Outlet Operative Info" for document changes is a doc error; documents are changed on Change Track Outlet Document (reading restated to the trainer). | [stated 2026-10-08 Syed Zulfiqar] | outlet page; doc issue noted under O14 |
