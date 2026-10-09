# Area: master data - PJP and outlet (S&D / DCODE)

Updated: 2026-10-09 (first consolidation: training session 2026-10-08 with Syed Zulfiqar - the PJP user guide "PJP updated R2.pptx" (P1-P13), the outlet user guide "outlet changes.pptx" (O1-O14), trainer rulings F1-F8 (10-08), and Jira evidence). Evidence: [../learning_sessions/2026-10-08_SND-GLOBAL_SyedZulfiqar_log.md](../learning_sessions/2026-10-08_SND-GLOBAL_SyedZulfiqar_log.md); report [../learning_sessions/2026-10-08_SND-GLOBAL_SyedZulfiqar_report.md](../learning_sessions/2026-10-08_SND-GLOBAL_SyedZulfiqar_report.md).
Updated 2026-10-09 (group 66 NG_Setup Flow_PK live walk, sessions 2026-10-05 seq 1-18 and 2026-10-09 seq 19-36, trainer / QA lead Syed Kamran): PJP and outlet screens walked live (facts added to pjp.md and outlet.md, tag [observed <date>] / [stated 2026-10-09 Syed Kamran]); new pages dsr.md and section_and_mappings.md; report [../learning_sessions/2026-10-09_G66-PK_session2_report.md](../learning_sessions/2026-10-09_G66-PK_session2_report.md).

Status: DRAFT. Facts are [stated] (documents and the trainer), [jira] (expectations to be confirmed live) and the group 11 / group 66 observations already in the other pages. **Neither screen has been walked as part of this training.** The 2026-10-08 rulings F1-F11 are cited as "F<n> (10-08)" so they do not clash with the 2026-10-07 promotions session's F1-F23.

1. Every Order Booker and every Delivery Man works from a **PJP** (Permanent Journey Plan) built from sections (groups of outlets), selling categories, a frequency and working days; an order PJP is linked to a delivery PJP by **Reference PJP** (group 11: 02111 -> 02112) [stated 2026-10-08 doc:PJP updated R2.pptx s.4, s.8].
2. A PJP is created by the Maker and approved by the **TM user** (Forward); on cnr1dev1 the TM user is **Auto_Tssm** [stated 2026-10-08 doc:PJP updated R2.pptx s.7, s.9] [stated 2026-10-08 Syed Zulfiqar (F7 10-08)].
3. **Outlets** created or changed by a distributor (DT) user need approval by a company / HQ user; company-user changes need none [stated 2026-10-08 Syed Zulfiqar (F1 10-08)]. Approved changes to outlet tax flags apply to **new orders only** [stated 2026-10-08 Syed Zulfiqar (F2 10-08)].
4. These are master data for the Daily Cycle (group 11) and are set up by framework group 66 (NG_Setup Flow_PK), which was walked to seq 18 on 2026-10-05.
5. Group 66 walk **completed 2026-10-09** (seq 19-36): PJP DT vs HQ, PJP Approval (separate TM menu), PJP Daily Inquiry Process, PJP Change Request / Change Track PJP Config (TM approves on the same screen, change applied at once), DSRs, sections, mappings, Delivery Man Shuffling [observed 2026-10-09]; decisions [stated 2026-10-09 Syed Kamran].

## Training status
PJP and outlet are trained from documents + rulings only (no live walk of these screens in this session). Changing PJPs, sections or outlets on cnr1dev1 alters the group 11 data (outlet tax, routes); never change them without the QA Team Lead's go-ahead. The PJP questions Q-PJ1, Q-PJ2, Q-PJ3, Q-PJ5 are **ON HOLD** (trainer will return to them).
2026-10-09: PJP, outlet change-track, DSR, section and mapping screens are now also walked live (group 66, sessions 2026-10-05 and 2026-10-09); nothing is signed off (G0 is the QA lead's decision). Defect D-G66-2-1 (Company Mapping Outlet sub-tab HTTP 500) and Q-PO1, Q-PO2, Q-PO3, Q-PJ6 are open.

## Pages (one line each)
| Page | What it holds |
|---|---|
| [pjp.md](pjp.md) | PJP Creation (header, configuration rows, Reference PJP), Maker -> TM approval, PJP Change Request, Change Track PJP Config, Selling Category, Section (+ Default delivery days), outlet-to-section mapping, Section Bulk Upload; Jira on the daily PJP job, delivery days, frequency, multi-section outlets; F7 / F8 (10-08). |
| [outlet.md](outlet.md) | Outlet Profile (demographics, Operative Info tax flags, classification, credit limit), Outlet Approval II, change-track screens, Outlet Status, Outlet Change Track Excel, Outlet Creation Upload, Outlet Price; F1-F6 (10-08); DT -> TM -> HQ workflow (SDMS-12227, "no conflict" F6); links to group 66 seq 13-16 and Q-TX1. |
| [dsr.md](dsr.md) (2026-10-09) | DSR Profile - DT (Maker) + DSR Approval (Checker) vs DSR Profile HQ (no approval needed, Report To, stricter checks); Change Track DSR Profile (name / status) and Change Track DSR Document (CNIC), approved on the same screen with one Forward; CNIC 13-digit mask; one login user per DSR; unique cell numbers [observed 2026-10-05, 2026-10-09 G66 walk]. |
| [section_and_mappings.md](section_and_mappings.md) (2026-10-09) | Section (DT, Forward + Section Approval) vs Section Creation HQ (Active at once, no Default Delivery Days field); Selling Category, Warehouse, Vehicle (generated codes); Distributor Mapping and Company Mapping tabs; mapping saves show no toast; end-state tick rule [stated 2026-10-09 Syed Kamran]; defect D-G66-2-1 (Company Mapping Outlet sub-tab) [observed 2026-10-05, 2026-10-09 G66 walk]. |

## Related pages
- [../order_to_delivery_planning/order_booking.md](../order_to_delivery_planning/order_booking.md): PJP, Section and Selling Category on the order header; outlet tax behaviour (Q-TX1).
- [../order_to_delivery_planning/delivery_date_change.md](../order_to_delivery_planning/delivery_date_change.md): delivery date of booked orders (BA4; Section Default delivery days, Q-PJ2).
- [../settlement_and_finance/pjp_daily_inquiry_update.md](../settlement_and_finance/pjp_daily_inquiry_update.md): the daily PJP row and the day close (Q-PJ1).
- [../test_data/PK.md](../test_data/PK.md): PJPs 02111 / 02112, Automation_Testing_Section, outlets on 02111.
- [../promotions_and_budget/claims.md](../promotions_and_budget/claims.md): Claim Days on the distributor profile.
- [../delivery_and_returns/delivery_man_shuffling.md](../delivery_and_returns/delivery_man_shuffling.md) (2026-10-09): moving a booked order from a source Delivery Man PJP to a destination DM PJP (group 66 seq 36).

## Open questions
Q-PJ1, Q-PJ2, Q-PJ3, Q-PJ5 (ON HOLD) and Q-PJ4 (answered by F7 (10-08)) in [../OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md) section 1c / 2h; Q-RL1 (roles) section 3; contradiction 43 (TM role code) in its section 5.
2026-10-09 (group 66 walk): new Q-PO1 (class C, 1b), Q-PO2 (class A), Q-PO3 (class B), Q-PJ6 (class B), Q-DM1 (class B); contradictions 45 (Default delivery days on the section) and 46 (PJP approval screen); defect D-G66-2-1.
