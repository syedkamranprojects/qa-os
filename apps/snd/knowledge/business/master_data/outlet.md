---
option: Outlet master (Outlet Profile, approval, change track, price)
area: master_data
doc_types: [outlet, outlet change request]
screens: [Outlet Profile, Outlet Approval II, Change Track Outlet Profile, Change Track Outlet Operative Info, Change Track Outlet Document, Analysis Classification - Outlet, Outlet Status, Outlet Profile View, Outlet Change Track Excel, Outlet Creation Upload, Outlet Price, Outlet Profile TM, Prospect Outlet, Prospect Outlet Approval]
framework_flows: [00530001, 00380002, 00240001, 01340001, 02200001, 01330001, 02220001]
markets: [PK]
roles: [Maker, Checker]
depends_on: [pjp]
sources: [document, sme, story-history, live-walk]
updated: 2026-10-09
---

# Outlet master: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the training session of 2026-10-08 with Syed Zulfiqar (consolidated 2026-10-09): the user guide "outlet changes.pptx" (25 slides, "Outlet Master - DMS-NG: User Guide", v1.2, Centegy; no market or date given; text read in full, screenshots and the embedded narration audio not reviewed), the trainer's rulings F1-F7 (10-08), and Jira evidence. **These screens were not walked live in this session**; the group 66 walk of 2026-10-05 used the change-track screens (seq 13-16, below). Tags: **[stated 2026-10-08 doc:outlet changes.pptx s.<n>]** = the guide; **[stated 2026-10-08 Syed Zulfiqar (F<n> 10-08)]** = verbal ruling of 2026-10-08 (the "(10-08)" suffix separates them from the 2026-10-07 session's F1-F23); **[jira <KEY>]** = Jira SDMS ticket with region and status (expectation, to be confirmed live). Rules: `docs/LEARNING_STANDARD.md` §3.
Source file: `apps/snd/knowledge/sources/20261008_outlet changes.pptx`.
Source flows: group 66 seq 13-16 (change track of outlet 1000000001, 2026-10-05) [observed 2026-10-05 G66 walk; log runs/LEARN-G66-PK/20261005/session_log.md, not shipped].
Last updated: 2026-10-09.
**2026-10-09 (group 66 live walk consolidated):** facts from group 66 (NG_Setup Flow_PK) session 1 (2026-10-05, seq 3, 4, 11, 13-16) and session 2 (2026-10-09, seq 19, 20, 36) on cnr1dev1, distributor 15108843, trainer / QA lead Syed Kamran, are added below with **[observed <date>]** and **[stated <date> Syed Kamran]**; evidence `../learning_sessions/2026-10-05_G66-PK_session1_log.md`, `../learning_sessions/2026-10-09_G66-PK_session2_log.md`.

## 1. Purpose
- The outlet (retail customer) master holds who the distributor sells to: demographics, operative / tax information, classification, documents, bank, contacts and credit limit [stated 2026-10-08 doc:outlet changes.pptx s.3-12].
- Outlets can be created by company / global users or by distributors; a distributor-created outlet needs approval by a company user to become active [stated 2026-10-08 doc:outlet changes.pptx s.3].
- Place in the business: master data before the Daily Cycle. Order Booking offers the outlets of the PJP's section (43 outlets on 02111 / Automation_Testing_Section) [observed 2026-10-08, test_data/PK.md]; the outlet's tax flags decide the order's tax (Q-TX1, below).

## 2. Actors and roles
- **Approval only for DT users:** outlet approval is required only when a **DT (distributor) user** creates or changes the outlet; an outlet created / changed by a company user needs no approval [stated 2026-10-08 Syed Zulfiqar (F1 10-08)].
- **Company user approves** DT-created outlets on Outlet Approval II [stated 2026-10-08 doc:outlet changes.pptx s.13].
- **R1 workflow (Jira):** DT (role 0005) creates -> Draft; TM (role 0008, screen **Outlet Profile TM**) reviews / edits and Forwards; HQ (role 0001, Outlet Approval) approves -> Active / Approved, or rejects -> In-Active / Rejected (editable again) [jira SDMS-12227] (PKBD R1, Assigned to QA, Sept 2026).
- **Ruling "no conflict":** an outlet created by a DT user is approved by a company / HQ user (F1 and the deck agree); the TM forward step of SDMS-12227 (DT 0005 -> TM 0008 -> HQ 0001) is a step **before** the HQ approval, not a different approver; recorded as Jira detail, not a contradiction [stated 2026-10-08 Syed Zulfiqar (F6 10-08)].
- **TM user on cnr1dev1 = Auto_Tssm** (our Checker), also the TM in the outlet DT -> TM -> HQ flow [stated 2026-10-08 Syed Zulfiqar (F7 10-08)]. Role-code question (0008 in SDMS-12227 vs 0002 TSSM in the QA team's table): contradiction 43, Q-RL1.
- Note on role codes: SDMS-12227 numbers the roles differently from the QA team's table (there 0001 = NG User / DT back office, 9999 = HQ) [stated 2026-10-08 QA Team]; role codes may be configured per org [inferred] (contradiction 43).
- Group 66 (2026-10-05): the change-track requests seq 13-16 were made by the Maker and approved with Auto_Tssm [observed 2026-10-05 G66 walk; stated 2026-10-05 QA lead].
- Change-track approvals: the Checker (Auto_Tssm) opens the **same menu option** as the Maker (e.g. Change Track Outlet Document) and approves with one Forward [observed 2026-10-05].
- Prospect Outlet: as Auto_Multi_Orga and as Automation (the framework's seq 1-4 user) **Forward and Reject stayed disabled** on the Draft outlet C0154187435; what enables Forward is open (Q-PO1) [observed 2026-10-05].

## 3. Documents and master data
- **Outlet**: Outlet Code (auto-generated), Long / Short Name, Channel Hierarchy, Outlet Type, Geographical Hierarchy, tax flags, classification, credit limit (section 4) [stated 2026-10-08 doc:outlet changes.pptx s.6-12]. PK test outlets on 02111: 1000000004 - 1000000011 used in group 11, 1000000001 - 1000000003 not offered on that PJP [observed, test_data/PK.md].
- **Outlet change request** (change track: Profile, Operative Info, Document): Forward for Approval, appears in the grid above for review and approval [stated 2026-10-08 doc:outlet changes.pptx s.14-17].
- **Outlet Price**: product prices set per outlet [stated 2026-10-08 doc:outlet changes.pptx s.23]; it **overrides the normal price list** for that outlet's products [stated 2026-10-08 Syed Zulfiqar (F4 10-08)].
- **Analysis Classification - Outlet**: the value lists of the classification attributes (prerequisite) [stated 2026-10-08 doc:outlet changes.pptx s.9, s.18].
- Dates (R1 Jira): Completion Date = first activation date-time; Activation Date = first creation date-time [jira SDMS-12227] (PKBD R1, Assigned to QA). (The guide lists Activation Date as mandatory on Demographics [stated 2026-10-08 doc:outlet changes.pptx s.6-7].)
- Live (group 66): a new back-office outlet gets a generated **Outlet Code C0154187435** (prefix C015...) and workflow status **Draft**, outlet Status In-Active [observed 2026-10-05]. Change request numbers observed: Change Track Outlet Profile **74** (on C0154187435), Change Track Outlet Document **47** and Change Track Outlet Operative Info **50** (both on 1000000001) [observed 2026-10-05].
- **Outlet 1000000001 (Aautomation_Outlet_01) was changed on 2026-10-05** by group 66: NTN document 8798 -> **1111112222333330001** (request 47; document status still UN-Authorized), and Operative Info Tax Registered Unregistered -> **Registered**, Tax Payer Yes -> **No**, plus new tiers / attributes (CA2T1, CA302, CA402, CA1001, CA1202, CA801) (request 50) [observed 2026-10-05]; approved as the workbook says, accepting the tax change on outlet 01 [stated 2026-10-05 Syed Kamran]. Group 11 tax expectations for outlet 01 may differ from earlier sessions.
- **Outlets offered for booking:** on Aslam PJP OB 7918624876 / Automation_Testing_Section the Order Booking outlet list offered 1000000004-08, 1000000011-20 and some C01... outlets, but **not 1000000001, 02, 03, 09, 10** [observed 2026-10-09]; group 11 found 01-03 not offered on 02111 [observed 2026-10-01 G11-1, test_data/PK.md]. Outlet 1000000014 was used instead [stated 2026-10-09 Syed Kamran].

## 4. Inputs: screens and fields
| Screen / tab | Fields | Tag |
|---|---|---|
| Outlet Profile > Demographics | Outlet Code (auto); Long / Short Name; Previous Outlet Code; **Channel Hierarchy** (mandatory, last level e.g. Bakery, Restaurant); **Outlet Type** (mandatory: Local Modern Trade, Modern Trade, General Trade ...); Currency; Geographical Hierarchy; Outlet / Company Rank (user-defined); latitude / longitude; Area Type; Identified By / On; Status (auto, Active / Inactive); Ship To Code; Bill To Code (head-office outlet that is billed); Analysis 1-3; Is B2B; Activation Date (mandatory); Sub Distributor + Code (code mandatory); Manual Order Creation; Completion Date; Requested Section; Approval Status; Prospect ID | [stated 2026-10-08 doc:outlet changes.pptx s.6-7] |
| Outlet Profile > **Operative Info** | Tax: **Tax Registration, Tax Exemption, Tax Registered (mandatory), Tax Payer, Auto Tax Invoice, WHT flag**; also Perfect Store (+ date), SMS Notification, Post-dated Cheque, B2B phone / email, Barcode + Barcode Scanning, preferred order / delivery times, Auto Cheque Realization, Restrict Un-Mapped Bank. Operative Info holds only operational information, not documents [stated 2026-10-08 Syed Zulfiqar (F5 10-08)] | [stated 2026-10-08 doc:outlet changes.pptx s.8] |
| Outlet Profile > Classification | Tiers, Perfect Village, Channel TTS, Perfect Store Compliance, Point of Consumption, Loyalty Programs, Chain Outlets, Customer Attribute 12, Outlet Programs; GPS Restriction / Radius; values from Analysis Classification - Outlet | [stated 2026-10-08 doc:outlet changes.pptx s.9] |
| Outlet Profile > Other Info | Shopper Type; **Company Turnover** and **Overall Total Turnover** (mandatory); stock selling / holding capacity | [stated 2026-10-08 doc:outlet changes.pptx s.10] |
| Outlet Profile > Documents / Bank / Contact Person | Documents: number, issue / expiry date, status, reference; Bank: bank, branch, details; Contact Person | [stated 2026-10-08 doc:outlet changes.pptx s.10-12] |
| Outlet Profile > **Credit Limit** | Credit Amount Limit + Amount Action; Day Limit + Day Action (actions Block / Warn, F3 (10-08)); only one credit-limit row allowed [jira SDMS-12365] (New) | [stated 2026-10-08 doc:outlet changes.pptx s.12] |
| Outlet Approval II | New outlets with status **PROSPECT** (= inactive); select, Approve or Reject; a "similar outlets" pop-up shows outlets with similar attributes (duplicate check) | [stated 2026-10-08 doc:outlet changes.pptx s.13] |
| Change Track Outlet Profile | Long name, ranks, area type, status, B2B mobile, manual order creation, prospect ID; select outlet, edit, Forward for Approval | [stated 2026-10-08 doc:outlet changes.pptx s.14-15] |
| Change Track Outlet Operative Info | Operative Info fields (tax flags ...); select, edit, Forward for Approval | [stated 2026-10-08 doc:outlet changes.pptx s.16] |
| Change Track Outlet Document | Documents; select, edit, Forward for Approval. (The guide's s.17 says to search "Change Track Outlet Operative Info" for document changes: a doc error; documents are changed on Change Track Outlet Document) | [stated 2026-10-08 doc:outlet changes.pptx s.17]; correction [stated 2026-10-08 Syed Zulfiqar (F5 10-08)] |
| Analysis Classification - Outlet | Pick analysis type, Edit a classification, Save -> success pop-up | [stated 2026-10-08 doc:outlet changes.pptx s.18] |
| Outlet Status | Lists active outlets; select, Process | [stated 2026-10-08 doc:outlet changes.pptx s.19] |
| Outlet Profile View | Read-only | [stated 2026-10-08 doc:outlet changes.pptx s.20] |
| Outlet Change Track Excel | Filter by Distributor, PJP Number, Section, Geo Hierarchy Code, Outlet Channel; Download Excel, edit, Upload Excel | [stated 2026-10-08 doc:outlet changes.pptx s.21] |
| Outlet Creation Upload | Download Template, fill, Upload Excel | [stated 2026-10-08 doc:outlet changes.pptx s.22] |
| Outlet Price | Pick an outlet; set / review product prices for it | [stated 2026-10-08 doc:outlet changes.pptx s.23] |
| Outlet Profile TM (R1) | TM review / edit of a DT-created outlet, Forward | [jira SDMS-12227] |

Menu paths: not given in the text (screenshots not viewed) [unknown].

Live screens (group 66) [observed 2026-10-05 unless marked]:
| Screen | Menu / path | Fields / actions | Tag |
|---|---|---|---|
| Outlet Profile | menu "Outlet Profile" (also Outlet Profile HQ / View / TM, Change Track Outlet Profile) | Grid (Outlet Code, Name, Outlet Status, Approval Status; 287 pages) + form already in new mode. New-outlet defaults: MIS Type Local Modern Trade, Currency PKR, Channel C00020 - FOH TOURISM, Geo f008, Outlet / Company Rank A, Area Urban, Identified by today (ro), Status In-Active (ro), Analysis A/B/C 0101, B2B enroll No (ro), Requested Section asf15124, WF status Draft. Demographics drop-down Demographics / Operative Info / Address; tabs Documents, Bank, Contact, Credit Limit, Gallery enable after the first Save | [observed 2026-10-05] |
| Outlet Profile > Address | (drop-down) | sub-tabs Company / Business / Residence; City -> Region -> Locality cascade; masked phone / mobile inputs; opening / closing time, estimate delivery date | [observed 2026-10-05] |
| Prospect Outlet | menu "Prospect Outlet" (+ "Prospect Outlet Approval") | Grid Distributor Code / Name, Outlet Code, Outlet Name, Identified On, Identified by, Approval Status, Cancelled Status (also other distributors' prospects); tabs Demographics (drop-down Demographics / Operative Info / Address), Document, Bank, Contact Person Name, Credit Limit, Gallery (Image Gallery + Upload), Comment Log; buttons Update, Translation, Forward, Reject, Similar Outlets. **Lists only prospect outlets** (back-office drafts / mobile prospects): approved outlet 1000000001 is not listed | [observed 2026-10-05] |
| Change Track Outlet Profile | /change-management/outlet-profile-management | Request grid (Request No, Description, Distributor, Status, Request Date), "List of Outlets" (Code, Name, Status, Approval Status), "Outlet Modification attribute" pairs (current \| New Value): Short Name, Long Name, Channel Hierarchy, Geographical Hierarchy, Outlet Rank, Company Rank, Latitude, Longitude, Area Type, Status, B2B Mobile Number, Manual Order Creation, Prospect ID; buttons Add, Save, Update, Forward, Reject, Cancel. A Draft outlet can be change-tracked here | [observed 2026-10-05] |
| Change Track Outlet Document | /change-management/outlet-document | Request grid + outlet list (Code / Description / Status) + document grid; pairs Document Type \| New Value, Document No \| New Value1; Add, Save, Update, Forward, Reject. A Draft outlet is **not listed** | [observed 2026-10-05] |
| Change Track Outlet Operative Info | /change-management | Request list + outlet list + attribute pairs for the Operative Info fields (Tax Exemption, Tax Registered, Tax Payer, Tiers, Perfect Village, Channel TTS, Perfect Store, PS Compliance, Point of Consumption, Loyalty, Chain, Customer Attr 12, Outlet Programs) | [observed 2026-10-05] |

## 5. Process: the business steps in order
A. DT user creates an outlet [stated 2026-10-08 doc:outlet changes.pptx s.3, s.6-13]
1. [Maker] (DT user) Navigate to Outlet Profile; fill Demographics, Operative Info, Classification, Other Info, Documents, Bank, Contact Person, Credit Limit; Click Save. Status PROSPECT (inactive).
2. (R1, Jira) [Checker] (TM, Auto_Tssm) Review on Outlet Profile TM; Click Forward [jira SDMS-12227] [stated 2026-10-08 Syed Zulfiqar (F6 10-08, F7 10-08)].
3. [Company / HQ user] Navigate to Outlet Approval II; select the outlet (check the "similar outlets" pop-up); Click Approve (or Reject) -> Active.
   - A company user creating an outlet skips the approval [stated 2026-10-08 Syed Zulfiqar (F1 10-08)].

B. Change an approved outlet [stated 2026-10-08 doc:outlet changes.pptx s.14-17]
1. [Maker] Navigate to Change Track Outlet Profile / Operative Info / Document; select the outlet; edit; Click Forward for Approval.
2. [Checker] Review the request in the grid; approve. (Approval needed only for DT-user changes, F1 (10-08).)
   - Group 66 seq 13-16 (2026-10-05) did this for outlet **1000000001**: NTN changed; it is now Registered / Tax Payer No (affects group 11 tax) [observed 2026-10-05 G66 walk; stated 2026-10-05 QA lead]. Earlier, outlets 06 / 07 swapped tax behaviour between 10-05 and 10-06 by master-data modification (Q-TX1 answered) [stated 2026-10-06 QA Team Lead].

C. Other options [stated 2026-10-08 doc:outlet changes.pptx s.18-23]
1. Deactivate: Outlet Status -> select -> Process -> "Are you sure you want to proceed?" Yes -> "Process completed successfully." -> outlet inactive (check on Outlet Profile).
2. Bulk change: Outlet Change Track Excel (filter, Download, edit, Upload) -> updates on Outlet Profile.
3. Bulk create: Outlet Creation Upload (Download Template, fill, Upload) -> new outlets on Outlet Profile.
4. Outlet Price: pick the outlet, set product prices.

D. Live, group 66 (back-office outlet, prospect, change tracks)
1. [Maker] Navigate to Outlet Profile (already in new mode); fill Demographics; Click Save -> "Saved successfully", Outlet Code generated (C0154187435), WF **Draft** [observed 2026-10-05] (66:3:00530001).
2. [Maker] Operative Info, Address (Company tab) -> Save -> "Saved successfully"; Documents, Bank, Contact Person, Credit Limit rows -> row Save -> "Record Saved Successfully!" [observed 2026-10-05]. The flow has no Forward event: the outlet **stays Draft / In-Active** [db: event flow; observed 2026-10-05].
3. [Maker] Navigate to Prospect Outlet; filter the outlet; change Outlet Type (Local Modern Trade -> Modern Trade); Click Update -> "Updated successfully"; Operative Info Update -> "Updated successfully"; **Forward is disabled** (also as Automation) -> seq 4 Forward and seq 5 Prospect Outlet Approval not done (Q-PO1) [observed 2026-10-05; skip stated 2026-10-05 Syed Kamran] (66:4:00380002).
4. [Maker] Change Track Outlet Profile: pick the outlet; enter New Values; Click Save -> "Saved successfully", request 74; select it; Forward; comment; Save -> "Forwarded successfully" [observed 2026-10-05] (66:11:00240001). Group 66 has no approval row for this request (Q-PO3).
5. [Maker] Change Track Outlet Document on 1000000001: filter Document Type NTN; select the row; New Value NTN / new number; Save -> "Saved successfully", request 47; Forward -> "Forwarded successfully" [observed 2026-10-05] (66:13:01340001).
6. [Checker] Same menu option; first click on the request selects it, the second opens it; Forward; comment; Save -> "Forwarded successfully"; afterwards request Active and the document number replaced (one Checker step) [observed 2026-10-05] (66:14:02200001).
7. [Maker] Change Track Outlet Operative Info on 1000000001: New Values; Save -> "Saved successfully", request 50; Forward -> "Forwarded successfully" [observed 2026-10-05] (66:15:01330001).
8. [Checker] Open request 50 (second click); Forward -> "Forwarded successfully"; outlet 01 is now Registered / Tax Payer No [observed 2026-10-05] (66:16:02220001).

## 6. Outputs and effects
- Approved outlet: Active, offered for order booking on its section's PJP [stated 2026-10-08 doc:outlet changes.pptx s.13] [inferred link to booking].
- **An approved change to the outlet's tax flags (Operative Info) applies to new orders only; orders already booked keep their tax** [stated 2026-10-08 Syed Zulfiqar (F2 10-08)]. Fits the zero-tax delivery rule: a booked zero-tax invoice of an outlet that is no longer exempt cannot be delivered (Q-TX1 answer, ZERO_TAX_ORDER_EXEMPTION = N) [stated 2026-10-06 QA Team Lead; stated 2026-10-08 QA Team].
- **Outlet Price overrides the normal price list** for that outlet's products [stated 2026-10-08 Syed Zulfiqar (F4 10-08)].
- Outlet Status Process -> outlet inactive [stated 2026-10-08 doc:outlet changes.pptx s.19].
- After activation (R1 Jira): a DT user may edit only 4 fields (phone, contact person, credit limit amount, credit limit days); TM view only [jira SDMS-12227] (PKBD R1, Assigned to QA).
- Live: an approved Change Track Outlet Document request replaces the document number at once (request 47 Active; NTN 1111112222333330001, document status still UN-Authorized) [observed 2026-10-05]; an approved Operative Info request changes the tax flags at once (outlet 01 Registered / Tax Payer No) [observed 2026-10-05].
- Live: a **Draft outlet is not usable downstream**: not offered on Section Allowable, Distributor Mapping > Outlet, Change Track Outlet Document [observed 2026-10-05, 2026-10-09] (Q-PO2); the earlier framework runs left about 16 "Automation QA TEST" outlets of 15108843 in Draft [observed 2026-10-05].

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| (new, DT user) | Save | **PROSPECT** (inactive) | DT user | [stated 2026-10-08 doc:outlet changes.pptx s.13] |
| (new, DT user, R1) | Save | Draft | DT (0005) | [jira SDMS-12227] |
| Draft | Forward | to HQ approval | TM (0008; Auto_Tssm on cnr1dev1) | [jira SDMS-12227]; user [stated 2026-10-08 Syed Zulfiqar (F7 10-08)] |
| PROSPECT / pending | Approve | Active / Approved | company / HQ user | [stated 2026-10-08 doc:outlet changes.pptx s.13] [jira SDMS-12227] |
| PROSPECT / pending | Reject | In-Active / Rejected (editable again) | company / HQ user | [stated 2026-10-08 doc:outlet changes.pptx s.13] [jira SDMS-12227] |
| (new, company user) | Save | Active, no approval | company user | [stated 2026-10-08 Syed Zulfiqar (F1 10-08)] |
| Active | Outlet Status Process | inactive | user | [stated 2026-10-08 doc:outlet changes.pptx s.19] |
| Active | change-track Forward for Approval, then approval | change applied | Maker, Checker | [stated 2026-10-08 doc:outlet changes.pptx s.14-17] |
| (new, back-office Outlet Profile, Maker) | Save | WF **Draft**, Status In-Active | Auto_Multi_Orga | [observed 2026-10-05] |
| Draft (Prospect Outlet) | Forward | not possible: Forward disabled (Q-PO1) | Auto_Multi_Orga, Automation | [observed 2026-10-05] |
| change request (new) | Save | request In-Active | Maker | [observed 2026-10-05] |
| request In-Active | Maker Forward, then Checker Forward (same menu) | request Active, change applied | Maker, Auto_Tssm | [observed 2026-10-05] |

## 8. Rules and validations
- Approval only for DT-user creations / changes [stated 2026-10-08 Syed Zulfiqar (F1 10-08)].
- Mandatory: Channel Hierarchy, Outlet Type, Activation Date, Sub Distributor Code, Tax Registered, Company Turnover, Overall Total Turnover [stated 2026-10-08 doc:outlet changes.pptx s.6-10].
- Classification values come from Analysis Classification - Outlet (set up first) [stated 2026-10-08 doc:outlet changes.pptx s.9].
- **Credit limit actions** are configured per outlet: **Block** blocks order booking when the amount / day limit is exceeded; **Warn** shows a warning at order booking; the check is made **at order booking** [stated 2026-10-08 Syed Zulfiqar (F3 10-08)]. Only one credit-limit row allowed [jira SDMS-12365] (New: requested, not current behaviour).
- Tax flag changes apply to new orders only [stated 2026-10-08 Syed Zulfiqar (F2 10-08)]; never assert tax from the outlet label, re-check the outlet per run (Q-TX1, test_data/PK.md).
- Duplicate check: Outlet Approval II shows a "similar outlets" pop-up [stated 2026-10-08 doc:outlet changes.pptx s.13].
- After activation a DT user may edit only phone, contact person, credit limit amount and days [jira SDMS-12227].
- Live rules (group 66):
  - A Draft outlet can be change-tracked on Change Track Outlet Profile, but is not listed on Change Track Outlet Document [observed 2026-10-05].
  - Prospect Outlet lists only prospects (back-office drafts / mobile prospects), not regular approved outlets [observed 2026-10-05].
  - Prospect Outlet Forward is disabled for a back-office Draft outlet whose "Identified by" is empty (outlets that reached Draft / Pending have it filled); cause unknown (image in Gallery? mobile prospects only? role?) [observed 2026-10-05; hypotheses inferred] (Q-PO1).
  - On change-track approval screens the first click on a request selects it, the second opens it [observed 2026-10-05].
  - Channel option text is "C10002 - Others" (161 channel options) [observed 2026-10-05].

## 9. Messages
| Type | Text | Trigger | Tag |
|---|---|---|---|
| confirm (type not seen) | "Are you sure you want to proceed?" (Yes) | Outlet Status, Process | [stated 2026-10-08 doc:outlet changes.pptx s.19] |
| success (type not seen) | "Process completed successfully." | after Yes | [stated 2026-10-08 doc:outlet changes.pptx s.19] |
| success pop-up (text not given) | - | Analysis Classification - Outlet, Save | [stated 2026-10-08 doc:outlet changes.pptx s.18] |
| pop-up | "similar outlets" list | Outlet Approval II, select | [stated 2026-10-08 doc:outlet changes.pptx s.13] |
| booking block / warning (texts unknown) | - | Order Booking over the credit limit (Block / Warn) | [stated 2026-10-08 Syed Zulfiqar (F3 10-08)] |

None observed live in this session.

Observed live (group 66):
| Type | Text | Trigger | Tag |
|---|---|---|---|
| toast success | "Saved successfully" | Outlet Profile Save (Demographics, Operative Info, Address); change-track request Save | [observed 2026-10-05] |
| toast success | "Record Saved Successfully!" | row Save on Documents, Bank, Contact Person, Credit Limit | [observed 2026-10-05] |
| toast success | "Updated successfully" | Prospect Outlet Update (Demographics, Operative Info) | [observed 2026-10-05] |
| toast success | "Forwarded successfully" | change-track Forward (Maker) and approval Forward (Checker) | [observed 2026-10-05] |

## 10. Dependencies
- Before: channel and geographical hierarchies, Analysis Classification - Outlet values, sub-distributor, sections (pjp.md) for the outlet to be bookable.
- After: Order Booking (outlet offered via section / PJP; tax from Operative Info, F2 (10-08); price from Outlet Price, F4 (10-08); credit limit check, F3 (10-08)), delivery (zero-tax rule, Q-TX1), deposit slips (outlet-level collection).
- Group 66 (NG_Setup Flow_PK) seq 13-16 changed outlet 1000000001 (NTN, tax flags) on 2026-10-05; group 11 tax expectations depend on that state [observed 2026-10-05 G66 walk].

## 11. Test design hints
Candidate cases (expectations to be confirmed live; outlet changes alter group 11 data, QA Team Lead's go-ahead only):
| # | Case | Expected | Tag |
|---|---|---|---|
| 1 | DT user creates an outlet | PROSPECT / Draft; not bookable until approved | [stated 2026-10-08 doc:outlet changes.pptx s.13] [jira SDMS-12227] |
| 2 | Company user creates an outlet | Active without approval | [stated 2026-10-08 Syed Zulfiqar (F1 10-08)] |
| 3 | Approved tax-flag change, then book a new order and look at an older one | new order taxed per the new flags; older order keeps its tax | [stated 2026-10-08 Syed Zulfiqar (F2 10-08)] |
| 4 | Credit limit Block, order over the limit | booking blocked | [stated 2026-10-08 Syed Zulfiqar (F3 10-08)] |
| 5 | Credit limit Warn, order over the limit | warning, booking continues | [stated 2026-10-08 Syed Zulfiqar (F3 10-08)] |
| 6 | Outlet Price set for a product, book an order | the line uses the outlet price, not the price list | [stated 2026-10-08 Syed Zulfiqar (F4 10-08)] |
| 7 | Outlet Status Process | "Process completed successfully."; outlet inactive | [stated 2026-10-08 doc:outlet changes.pptx s.19] |
| 8 | After activation, DT user edits a field other than the 4 allowed | not editable | [jira SDMS-12227] |

Traps: outlets 1000000001 - 1000000011 are shared group 11 fixtures whose tax flags are changed by setup walks (group 66 seq 13-16) and by other testers (Q-TX1); read the outlet's current flags before asserting tax.

## 12. Open questions
No new question filed for the outlet page. Related: Q-RL1 (role codes, F7 (10-08) evidence) and contradiction 43 (TM role 0008 vs 0002) in OPEN_QUESTIONS.md; Q-TX1 (answered 2026-10-06). Still to observe live (no question needed): the menu paths, the credit-limit Block / Warn message texts, and whether Outlet Profile TM exists on cnr1dev1.
2026-10-09 (group 66 walk), new in OPEN_QUESTIONS.md: **Q-PO1** (class C, 1b): what enables Forward on Prospect Outlet (image in Gallery, mobile-identified prospects only, a role, the seq 1-4 user Automation)? | Default: seq 4 Forward / seq 5 approval are not executable for a back-office Draft outlet; skip them. **Q-PO2** (class A): a Draft outlet is not offered for mapping / document change track | Default: only approved outlets are offered. **Q-PO3** (class B): who approves a Change Track Outlet Profile request (request 74, group 66 has no approval row)? | Default: the Checker on the same screen, as for the other change tracks.

## 13. Sources
- Session log: `../learning_sessions/2026-10-08_SND-GLOBAL_SyedZulfiqar_log.md` (Outlet document O1-O14, Jira "Outlet", F1-F7 (10-08)); report `../learning_sessions/2026-10-08_SND-GLOBAL_SyedZulfiqar_report.md`.
- Guide: `apps/snd/knowledge/sources/20261008_outlet changes.pptx` (25 slides, v1.2).
- Jira (centegy.atlassian.net, project SDMS, read 2026-10-08): SDMS-12227, SDMS-12365.
- Group 66 walk 2026-10-05 (seq 13-16): `runs/LEARN-G66-PK/20261005/session_log.md` (not shipped); Q-TX1 in `../OPEN_QUESTIONS.md` section 2c; `../order_to_delivery_planning/order_booking.md` (outlet tax table); `../test_data/PK.md` (outlets).
- Shipped copies of the group 66 logs: `../learning_sessions/2026-10-05_G66-PK_session1_log.md` (seq 3, 4, 11, 13-16), `../learning_sessions/2026-10-09_G66-PK_session2_log.md` (seq 19, 20, 36); report `../learning_sessions/2026-10-09_G66-PK_session2_report.md`.
