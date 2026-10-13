# Session report: TRAIN-SND-PK 2026-10-13, group 66 Setup open points with the QA team (method B + live demonstration)

- Date: 2026-10-13. Trainers: Syed Kamran (QA lead), Feroz Hussain, Muhammad Fahad (QA team). Market / env: PK / cnr1dev1 (Unilever Pakistan Limited, distributor 15108843).
- Input: the parked / open Setup (group 66) points after the QA team's written answers of 2026-10-12 (`learning_sessions/2026-10-12_G66-PK_parked_questions.md`). Log: `session_log.md` (copy `learning_sessions/2026-10-13_SND-PK_QA-Team_live_log.md`).
- Users: Automation, Auto_Multi_Orga (Maker, DT user), Auto_Tssm (TSSM / Checker). Credentials typed by the QA member.
- Tags: `[stated 2026-10-13 QA team]`, `[stated 2026-10-13 Syed Kamran]` (QA lead), `[observed 2026-10-13]`. Nothing earlier was deleted; replaced wording carries `(superseded 2026-10-13: ...)`.
- **Status: PAUSED** at the end of 2026-10-13; resumes **2026-10-14 10:30** with the same trainers. Consolidated: #1 (partly), #2-#5, #6 (correction + live check). Open: #1 remainder, #6 defect confirmation, #7-#9 not started.

## 1. Outcome per item

| # | Item | Outcome | Where merged |
|---|---|---|---|
| 1 | Q-PO1 Prospect Outlet Forward | **PARTLY ANSWERED.** Stated rule "Forward enabled when In-active + Draft" did not hold live (C0154187441/442/444 Forward disabled); "Identified by" is not the condition; user switch to Auto_Multi_Orga did not help. Learned: Forward needs (a) the user's **right / role** (granted to Automation by the QA team today) and (b) a **Company address** ("Company address cannot be empty."; Address stored with Save, Update gives no message). The team's C0154187445 was forwarded -> "Forwarded successfully" -> Pending for approval on Prospect Outlet Approval; approval Forward -> "Action cannot be performed, something went wrong!" = known issue **D-TRAIN-1013-1** (reported to dev by the QA team). **Open:** what enabled Forward on 445 but not on 442 / 444 | outlet.md §1-§13; OPEN_QUESTIONS Q-PO1, 2j; FRAMEWORK_DRIFT 4c row 54; LIVE_FINDINGS; glossary |
| 2 | Q-PJ8 HQ PJP approval | **ANSWERED + proven.** Approval follows the **creating user's level**: DT user (Outlet Profile, Section Profile, PJP) -> TSSM approval; HQ user -> none. AUTO241010 (10-09) was created by Auto_Multi_Orga (DT user) on PJP Creation HQ. Live: PJP AUTO241013 (DT, Auto_Multi_Orga) In-Active -> Active after Auto_Tssm's Forward on PJP Approval. Contradiction 47 resolved. Framework decision pending: group 66 seq 35 as headquarter or add a PJP Approval step | pjp.md §2, §5 E/I, §7, §8; section_and_mappings.md §2, §12; outlet.md §2; OPEN_QUESTIONS 2j / 47; FRAMEWORK_DRIFT 4c row 63; glossary; INDEX |
| 2b | New PJP chain | **Learned.** One DSR per PJP ("DSR AUTO241134 already Exists in Other PJP(s): AUTO241009"); new DSR AUTO101013 on DSR Profile - DT (Residence address + CNIC needed for Forward: "NIC No cannot be empty"; User ID may be empty) -> DSR Approval (Auto_Tssm) -> **Distributor Mapping > DSR** (required before PJP Creation offers the DSR) -> PJP Creation DT header + configuration row + Forward -> PJP Approval -> Active | pjp.md §5 I, §8; dsr.md §1, §3-§11; section_and_mappings.md §5 D, §8; FRAMEWORK_DRIFT 4c rows 46, 51, 65; glossary |
| 3 | Q-PJ7 GPS / DDO after approval | **ANSWERED + proven.** Read-only on PJP Creation DT also on the Active PJP; changed on **PJP Change Request** (request 63: GPS Yes, Radius 1, DDO Delivery Optimization), TSSM approves on the same screen; PJP Creation TM shows the new values | pjp.md §2, §4, §5 J, §6, §8, §11; OPEN_QUESTIONS 2j; FRAMEWORK_DRIFT 4c row 47; glossary |
| 4 | Q-PJ6 PJP Daily Inquiry Process | **ANSWERED + proven.** Process creates the **daily route for the working date** (Daily Route No 1) and loads the **outlets due that day** with visit sequence (1000000001-03, seq 1-3); result only after a **full page reload** | pjp.md §5 F/K, §6, §7, §8, §11; OPEN_QUESTIONS 2j; FRAMEWORK_DRIFT 4c (seq 27); glossary (new term Daily route) |
| 5 | PJP numbering setting | **ANSWERED.** Manual vs generated codes = technical DB configuration per client / screen, not a QA subject. cnr1dev1: typed = PJP Number (max 10), DSR Code; generated = Outlet Code, section / selling category / warehouse / vehicle codes, change-request numbers | pjp.md §3, §8; outlet.md §3; OPEN_QUESTIONS 2j |
| 6 | Contradiction 49 change track on a Draft outlet | **CORRECTION + live check.** QA: the screen shows the **Active** outlet list (not "approved"). Live (read-only): In-Active outlets ARE listed (441-444 Draft, 445 / 446 Pending for approval) -> **possible defect D-TRAIN-1013-2**, QA to confirm. Contradiction 49 updated, stays open | outlet.md §4, §5 D, §8, §12; OPEN_QUESTIONS 49 / 2j; FRAMEWORK_DRIFT 4c row 56; LIVE_FINDINGS; INDEX |
| 7 | Q-DM1 / Q-DM2 Delivery Man Shuffling | NOT STARTED (2026-10-14) | - |
| 8 | Section Profile delivery days (contradiction 45) | NOT STARTED (2026-10-14) | - |
| 9 | D-G66-2-1 Company Mapping > Outlet fix date | NOT STARTED (2026-10-14) | - |

## 2. Facts per page (summary)
- **master_data/outlet.md**: Outlet Profile mandatory Demographics fields (Outlet Code, Long Name, Channel, Geo, Lat, Long, Area Type, Sub Distributor Code) and 17 mandatory Operative Info fields; view drop-down Dem-1 Demographics / Opr-1 Operative Info / Oth-1 Address; no Forward on Outlet Profile; Prospect Outlet Forward needs right + Company address; Comments popup; Prospect Outlet Approval screen; transitions Draft -> Pending for approval; D-TRAIN-1013-1; Change Track Outlet Profile "Active" correction + D-TRAIN-1013-2; records C0154187441 / 442 / 444.
- **master_data/pjp.md**: Q-PJ8 / Q-PJ7 / Q-PJ6 answers; one DSR per PJP; DSR offered only after mapping; numbering; AUTO241013, request 63, daily route 1; new messages ("DSR ... already Exists in Other PJP(s): ..."); cases 15-19 and traps.
- **master_data/dsr.md**: DSR Forward needs Residence address + CNIC ("NIC No cannot be empty"); Qualification / Experience / Device not needed; User ID may be empty; AUTO101013 created, approved, mapped; CNIC digit-by-digit typing.
- **master_data/section_and_mappings.md**: Distributor Mapping > DSR sub-tab required for PJP Creation (no message, Save greys out); approval-by-user-level rule covers Section Profile; group 66 seq 35 framework decision pending.

## 3. Questions
- Answered: **Q-PJ6** (B), **Q-PJ7** (B), **Q-PJ8** (C 1b); contradiction **47 resolved**. Numbering answered (not a filed question).
- Partly answered, kept open (no longer deferred): **Q-PO1**, reworded: what enabled Forward on the team's C0154187445 but not on C0154187442 / 444 (created after Automation's rights change with the same workbook data)?
- Updated, open: contradiction **49** (possible defect D-TRAIN-1013-2).
- Open counts: **62 -> 59** = A 16 + B 20 + C 23 (1a 7, 1b 7, 1c 9 ON HOLD). Contradictions: 49 listed; 23 resolved, 6 partly, 20 open.

## 4. Defects
| Id | Status | Summary |
|---|---|---|
| D-TRAIN-1013-1 | **known issue, reported to dev by the QA team (2026-10-13)** | Prospect Outlet Approval > Forward of C0154187445 as Automation -> "Action cannot be performed, something went wrong!"; stays Pending for approval |
| D-TRAIN-1013-2 | **possible, QA team to confirm** | Change Track Outlet Profile lists In-Active (Draft / Pending for approval) outlets although change tracking applies to Active outlets |
| D-G66-2-1 | known issue, open (fix date = #9 tomorrow) | Company Mapping > Distributor > Outlet sub-tab HTTP 500 |
Open defects: 3 (2 known issues + 1 possible).

## 5. Still open for 2026-10-14 10:30
1. #1 Q-PO1 remainder: how C0154187445 was created / what the team changed (Forward enabled) vs C0154187442 / 444.
2. #6 confirm D-TRAIN-1013-2 (Change Track Outlet Profile lists In-Active outlets).
3. #7 Q-DM1 / Q-DM2 Delivery Man Shuffling (correct behaviour; which DM PJP / DSR the order shows after a shuffle).
4. #8 Section Profile delivery days (contradiction 45, planned change).
5. #9 D-G66-2-1 fix date.
6. Framework owner: group 66 seq 35 run as headquarter or add a PJP Approval step; Q-PJ8 wording confirmation by the team.

## 6. Records left on cnr1dev1 (15108843)
- Outlets **C0154187441, C0154187442, C0154187444** (Automation QA TEST; In-Active / Draft).
- Outlet **C0154187445** 'auto99' (created by the QA team; Company address added by us; forwarded; **Pending for approval**, approval failed D-TRAIN-1013-1). (C0154187443 'TestAuto11' and C0154187446 'new13/10' are the QA team's / others'.)
- DSR **AUTO101013** Auto_DSR_PJP (Active; mapped to 15108843; CNIC 12026-1010131-3; cells 60624101301 / 60624101302; User ID empty).
- PJP **AUTO241013** Auto_test (Active; DSR AUTO101013; Auto Main; configuration Full Range SKU / SEC000000067 / Weekly MON-SAT / 2026-10-13 - 2099-12-23 / Ref 8197298470; GPS Yes / Radius 1 / DDO Delivery Optimization via **PJP Change Request 63**; **daily route 1** for 2026-10-13 with outlets 1000000001-03).
- Rights change for user Automation (done by the QA team).
- Nothing else changed (#6 check was read-only; no change-track request created).

## 7. Friction (for HARDENING; not business)
Gateway "Access Denied" twice after heavy activity (and once on the SSO page); session 401 after the rights change; masked CNIC needs key-by-key typing; Process button is the outer button; Process result needs a full page reload; drop-down lists close on page scroll; loading overlay intercepts clicks; filter-row toggles differ per grid; Comments textarea typeable only once the popup has fully opened.

## 8. Files changed (knowledge)
master_data/outlet.md, master_data/pjp.md, master_data/dsr.md, master_data/section_and_mappings.md, OPEN_QUESTIONS.md (status, 1b, Q-PO1, 2i note, new 2j, class B, contradictions 47 / 49, counts, legend), learning_sessions/2026-10-12_G66-PK_parked_questions.md, glossary.md (4 entries updated, 4 new), INDEX.md, FRAMEWORK_DRIFT.md (new 4c), LIVE_FINDINGS.md (new block), LIVE_LEARNING_CHECKLIST.md (L58, L60 done), master_data/README.md, learning_sessions/README.md; copies learning_sessions/2026-10-13_SND-PK_QA-Team_live_log.md and _live_report.md.
