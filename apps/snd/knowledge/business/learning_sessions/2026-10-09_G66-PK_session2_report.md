# Report: group 66 (NG_Setup Flow_PK) learning walk, PK, sessions 1-2 (2026-10-05, 2026-10-09)

- Trainer / run by: Syed Kamran (QA lead). Env cnr1dev1, company Unilever Pakistan Limited, distributor 15108843 (Auto KARACHI / IBRAHIM TRADERS). Users: Maker Auto_Multi_Orga, Checker / TM Auto_Tssm, HQ headquarter; seq 1-4 per the framework = Automation.
- Method: C (live execution of a framework group, learning only: business facts, no ids), with QA-lead decisions during the walk (method B).
- Logs: [2026-10-05_G66-PK_session1_log.md](2026-10-05_G66-PK_session1_log.md) (seq 1-18), [2026-10-09_G66-PK_session2_log.md](2026-10-09_G66-PK_session2_log.md) (seq 19-36 + decisions). Originals in `runs/LEARN-G66-PK/20261005/` and `runs/LEARN-G66-PK/20261009/`.
- Tags used in the pages: [observed 2026-10-05], [observed 2026-10-09], [stated 2026-10-05 Syed Kamran], [stated 2026-10-09 Syed Kamran]. Consolidated 2026-10-09.

## 1. Coverage
All 35 active flows of group 66 walked (seq 1-36). Not done: seq 4 Prospect Outlet Forward and seq 5 Prospect Outlet Approval (Forward disabled, Q-PO1; skipped by the QA lead); Distributor Mapping Outlet tab and Company Mapping Outlet sub-tab for the Draft outlet (not offered / defect D-G66-2-1). Deviations agreed with the QA lead: seq 2-3 ran as Auto_Multi_Orga instead of Automation; outlet 1000000001 used for seq 13-16; extra Section Allowable step (option B); outlet 1000000014 and setup DAs 1362 / 1363 for seq 36; extra TM approval of the HQ PJP AUTO241010.

| Seq | Flow | Result |
|---|---|---|
| 1-3 | Login, Distributor Profile DT, Outlet Profile | done; outlet C0154187435 (Draft) |
| 4-5 | Prospect Outlet + approval | updates done; Forward disabled (Q-PO1); 5 skipped |
| 6-7 | Section + Section Approval | SEC000000067 Active; outlet 1000000001 attached |
| 8-10 | Selling Category, Warehouse, Vehicle | SEC000000035, C0000000216, 999713523 |
| 11 | Change Track Outlet Profile | request 74 forwarded (no approval row, Q-PO3) |
| 13-16 | Change Track Outlet Document / Operative Info + approvals | on 1000000001: requests 47, 50; outlet 01 now Registered / Tax Payer No |
| 17-18 | DSR Profile DT + approval | DSR AUTO241134 Active |
| 19-20 | Distributor Mapping, Company Mapping | done except the outlet mappings (Draft outlet; D-G66-2-1) |
| 21-24 | Change Track DSR + document, approvals | requests 48 (name -> Auto_Test241134), 40 (CNIC -> 12026-2241134-1) |
| 25-26 | PJP Creation DT + PJP Approval | AUTO241009 Active |
| 27 | PJP Daily Inquiry | Process: "Process completed successfully", no visible change (Q-PJ6) |
| 28-31 | PJP Change Request, Change Track PJP Config + approvals | requests 62 (description -> Auto917248), 39 (Weekly -> Daily) |
| 32-35 | Section Creation HQ, DSR Profile HQ, DSR Mapping HQ, PJP Creation HQ | SEC000000068, AUTOH24109, AUTO241010 (Active after TM approval) |
| 36 | Delivery Man Shuffling | order COL26000002031 shuffled 8197298470 -> AUTO301258 |

## 2. Facts placed (pages)
- **master_data/pjp.md** (added, nothing removed): live screens PJP Creation DT / HQ / TM, PJP Approval (separate TM menu), PJP Daily Inquiry, PJP Change Request, Change Track PJP Config; process sections E-H with traces 66:25-31, 35; 10-character PJP number; GPS / DDO read-only on DT (expected, stated) vs editable on HQ; HQ warehouse from the DSR; TM approval -> Active, change requests applied at once; statuses only after re-opening; observed messages; test cases 8-14; Q-PJ4 confirmed, Q-PJ5 evidence, Q-PJ6, contradictions 45 / 46.
- **master_data/outlet.md**: back-office Outlet Profile -> Draft (C0154187435), Prospect Outlet (lists prospects only; Forward disabled, Q-PO1), change-track outlet profile / document / operative info screens and approvals (same menu, one Forward), outlet 1000000001 NTN / tax change of 2026-10-05, outlets 01-03 / 09 / 10 not offered on Aslam PJP OB / group 11 PJPs; Draft outlet not usable downstream (Q-PO2); Q-PO3.
- **master_data/dsr.md** (new): DSR Profile - DT + DSR Approval vs DSR Profile HQ (no approval needed); Change Track DSR Profile / Document; CNIC mask; one login user per DSR; unique cell numbers; messages.
- **master_data/section_and_mappings.md** (new): Section DT + approval vs Section Creation HQ; Selling Category, Warehouse, Vehicle; Distributor Mapping and Company Mapping tabs; mapping saves show no toast; end-state tick rule; defect D-G66-2-1.
- **delivery_and_returns/delivery_man_shuffling.md** (new) + README item 12 and one-liner.
- **order_to_delivery_planning/order_booking.md** and **stock_allocation.md**: one line each: an order draws stock from its PJP's warehouse (Aslam PJP 7918624876 = IBT Main 0000000025; group 11 PJP 02111 = Auto Main).
- **master_data/README.md**, **INDEX.md** (rows for the new pages, document-map rows DSR / Section / master-data change requests), **glossary.md** (10 terms), **LIVE_FINDINGS.md** (group 66 block, D-G66-2-1), **LIVE_LEARNING_CHECKLIST.md** (L57-L59), **FRAMEWORK_DRIFT.md** (section 4, rows 44-62).
- Not consolidated into a page: Distributor Profile DT (seq 2: the DT user can edit only Off Days, GIN Initiation Time, Invoice Print Message and a few Other Info / Address fields; 4 x "Updated successfully") - no target page; kept in the session 1 log and drift row 61.

## 3. Questions, contradictions, defects
- New questions: **Q-PO1** (C, 1b: what enables Prospect Outlet Forward), **Q-PO2** (A: Draft outlet not offered for mapping / document change track), **Q-PO3** (B: who approves a Change Track Outlet Profile request), **Q-PJ6** (B: what PJP Daily Inquiry Process creates), **Q-DM1** (B: the order's DM PJP after shuffling).
- Answered during the walk by the QA lead (not filed): GPS / DDO read-only on DT is expected; PJP number AUTO241009; HQ DSR needs no approval; AUTOH24109 with Auto_Multi_Orga acceptable; SEC000000067 on outlets 01-03 acceptable; mapping tick rule (end state); outlet 1000000014 for seq 36; approve request 50 despite the tax change on outlet 01; skip the Gallery image. Observed answer: an approved PJP change request applies at once (read after re-opening).
- Evidence only: Q-PJ4 (confirmed live), Q-PJ5 (kept ON HOLD).
- New contradictions: 45 (Default delivery days on the section: guide vs no field on Section Creation HQ / DT form), 46 (PJP approval: guide "same screen" vs separate PJP Approval menu).
- New defect: **D-G66-2-1** (Company Mapping > Distributor > Outlet sub-tab: HTTP 500, "Action cannot be performed, something went wrong!").
- Counts (OPEN_QUESTIONS.md section 6): open 57 -> **62 = A 17 + B 22 + C 23** (1a 7, 1b 6, 1c 10 ON HOLD); contradictions 46 listed, 20 open.

## 4. Records left on cnr1dev1
Outlet C0154187435 (Draft); sections SEC000000067, SEC000000068; selling category SEC000000035; warehouse C0000000216; vehicle 999713523; DSRs AUTO241134 (Auto_Test241134), AUTOH24109; PJPs AUTO241009 (Auto917248, Daily), AUTO241010; change requests 74, 47, 50, 48, 40, 62, 39; DAs 1362 (Auto Main) and 1363 (IBT Main), 10 CS 20061858 each; order COL26000002031 (shuffled to AUTO301258). Outlet 1000000001 is Registered / Tax Payer No since 2026-10-05 (group 11 tax).

## 5. Still needs a walk
L57 (Q-PO3), L58 (Q-PJ6), L59 (Q-DM1); Prospect Outlet Forward once Q-PO1 is answered; a re-test of Company Mapping Outlet after D-G66-2-1 is fixed. Nothing is signed off (G0 is the QA lead's decision).
