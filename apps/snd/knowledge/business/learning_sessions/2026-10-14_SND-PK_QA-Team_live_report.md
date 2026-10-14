# Session report: TRAIN-SND-PK 2026-10-14, group 66 Setup open points with the QA team (continuation, method B + live demonstration)

- Date: 2026-10-14 (from 10:30). Trainers: Syed Kamran (QA lead), Feroz Hussain, Muhammad Fahad (QA team). Market / env: PK / cnr1dev1 (Unilever Pakistan Limited, distributor 15108843).
- Input: the open list left by the 2026-10-13 session (#1 Q-PO1 remainder, #6 D-TRAIN-1013-2, #7 Q-DM1 / Q-DM2, #8 section delivery days / contradiction 45, #9 D-G66-2-1, framework decision on group 66 step 35). Log: `session_log.md` (copy `learning_sessions/2026-10-14_SND-PK_QA-Team_live_log.md`). Previous: `learning_sessions/2026-10-13_SND-PK_QA-Team_live_report.md`.
- Users: Auto_Multi_Orga (read-only checks). Credentials typed by the QA member. Nothing was created or changed on cnr1dev1 today (re-test and checks were read-only).
- Tags: `[stated 2026-10-14 QA team]`, `[stated 2026-10-14 Syed Kamran]` (QA lead decision), `[observed 2026-10-14]`. Nothing earlier was deleted; replaced wording carries `(superseded 2026-10-14: ...)`.
- **Status: COMPLETE** for the group 66 open list. Consolidated 2026-10-14 (#6 had already been applied during the session; verified, gaps fixed in INDEX / glossary / counts).

## 1. Outcome per item

| # | Item | Outcome | Where merged |
|---|---|---|---|
| 1 | Roles and workflow | **STATED.** R1 role codes: **0001 / 0005 = DT user (submit only)**, **0002 / 0008 = approval user (approves setup and transaction records)**, **0014 = HQ user (HQ screens only, no approval)**. Refines the 2026-10-08 list (0001 NG User, 0002 TSSM, 9999 HQ Global; 0003 / 0004 / 9999 kept as earlier stated). Predefined roles follow the SOP; extra roles may be created (e.g. for checking) and placed in workflow diagrams. **Key rule: a user can act on a document only when a role is assigned to the user AND the same role is defined in that document's workflow diagram** (Submit / Approve step). Explains the GIN diagram naming 0005 for both steps (configured diagram) and, likely, role 0006 on PK menus [inferred]. Test design: run users must match each document's workflow diagram; a disabled Forward / Approve is first checked as "is the user's role in this workflow" | document_lifecycle.md §0e (new); glossary (3 new terms, 5 rows annotated); INDEX §2; outlet.md §2; pjp.md §2; section_and_mappings.md §2; goods_issue_note.md §2, §8; OPEN_QUESTIONS Q-RL1, contradictions 31 / 43; FRAMEWORK_DRIFT 4d |
| 1 | Q-PO1 Prospect Outlet Forward | **ANSWERED.** Forward was disabled because Automation's role was not in the prospect-outlet workflow diagram (Submit role); C0154187445 was created by a user whose role matched (Claude's summary confirmed: 'Yes you are right'). Plus the Company address rule (2026-10-13). The exact user / role behind 445 was not named | outlet.md §1 header, §2, §7, §8, §11, §12; OPEN_QUESTIONS 1b / 2k; FRAMEWORK_DRIFT 4d row 54; parked list (row removed) |
| 6 | Change Track Outlet Profile lists Draft outlets | **EXPECTED** (applied during the session): an outlet is available as soon as it is created in Draft; D-TRAIN-1013-2 withdrawn; contradiction 49 resolved. Verified; gaps fixed (OPEN_QUESTIONS 2j note, counts, LIVE_FINDINGS status line, INDEX, glossary) | outlet.md, OPEN_QUESTIONS, FRAMEWORK_DRIFT, LIVE_FINDINGS, parked list |
| 7 | Q-DM1 / Q-DM2 Delivery Man Shuffling | **ANSWERED** ('yes it is correct'). Source PJP + Outlet (multi-select) + destination DM PJP -> Save "Saved Successfully" -> the order leaves the source list and belongs to the destination delivery-man PJP / its DSR (e.g. COL26000002031 8197298470 -> AUTO301258). The **only** defect is the on-load 'PJP not found' / "Required parameter 'pjpNo' is not present." message (known issue, never asserted). Contradiction 48 resolved | delivery_man_shuffling.md (header, §1, §2, §6-§12); OPEN_QUESTIONS 1b / 3 / 2k / 48; FRAMEWORK_DRIFT 4d row 64; glossary; INDEX |
| 8 | Section delivery days (contradiction 45) | **STATED + read-only check.** Not an HQ feature; the business manages a section's delivery days on the Section Profile screen; seq 32 must drop Default Delivery Days. Live: no delivery-days field on Section (DT, DYL_102003015) nor Section Setup (/ngui/sectionsetup). The QA team will update later -> **C-45 / Q-PJ2 stay parked, waiting for the enhancement** | section_and_mappings.md §4, §8, §11, §12; OPEN_QUESTIONS 45 / 2k; FRAMEWORK_DRIFT 4d row 49; parked list C-45 |
| 9 | D-G66-2-1 Company Mapping > Outlet | **FIXED / CLOSED** [observed 2026-10-14]: Company Mapping (DYL_102013003) > Distributor > 15108843 Auto KARACHI > Outlet: no error toast; available 555,906 rows, mapped 131 | section_and_mappings.md §5, §9, §11, §12; LIVE_FINDINGS (new block, old heading marked); OPEN_QUESTIONS 2k / counts; FRAMEWORK_DRIFT 4d row 59 (seq 20 unblocked); parked list (row removed) |
| - | Framework decision step 35 | **DECIDED** [stated 2026-10-14 Syed Kamran]: group 66 step 35 PJP Creation HQ runs as **headquarter (HQ role 0014)** -> Active at once, no approval step | FRAMEWORK_DRIFT 4d row 63; pjp.md §1 header, §5, §7, §12; section_and_mappings.md §12; glossary |

## 2. Questions
- Answered: **Q-PO1** (C 1b), **Q-DM1** (B), **Q-DM2** (C 1b) -> OPEN_QUESTIONS section 2k. Their 2026-10-12 deferral and parked-list rows removed.
- Evidence added, kept open: **Q-RL1** (B): role codes and the workflow-diagram rule stated; only the read of the cnr1dev1 users' role codes (Auto_Multi_Orga, Auto_Tssm, Automation, KPO_mp) remains (L43).
- Contradictions: **43 resolved** (0002 / 0008 both approval codes), **48 resolved**, **49 resolved** (applied during the session); **31 partly resolved** (GIN diagram configured with 0005 on both steps); **45** answered for HQ, stays partly (Section Profile field parked).
- Open counts: **59 -> 56** = A 16 + B 19 + C 21 (1a 7, 1b 5, 1c 9 ON HOLD). Contradictions: 49 listed; 26 resolved, 7 partly, 16 open. No new questions.

## 3. Defects
| Id | Status | Summary |
|---|---|---|
| D-TRAIN-1013-1 | **open** - known issue, reported to dev by the QA team (2026-10-13) | Prospect Outlet Approval > Forward of C0154187445 -> "Action cannot be performed, something went wrong!"; stays Pending for approval |
| D-TRAIN-1013-2 | **withdrawn 2026-10-14** (not a defect) | Draft outlets on Change Track Outlet Profile are by design |
| D-G66-2-1 | **closed 2026-10-14** (fixed, re-tested live) | Company Mapping > Distributor > Outlet sub-tab no longer fails |
| (no id) | known issue | Delivery Man Shuffling on-load 'PJP not found' / "Required parameter 'pjpNo' is not present."; never asserted |
Open defects: 1 (D-TRAIN-1013-1).

## 4. Still parked / open
- **C-45** (section delivery days on Section Profile): waiting for the QA team's update on the enhancement; which menu item "Section Profile" is (the Section menu also offers "BG - Section Profile") is not confirmed. With **Q-PJ2** (ON HOLD).
- **SDMS-6084** ticket question (Report To mandatory on Distributor Profile HQ) stays in the parked file's separate section.
- **Q-RL1**: read the users' role codes on the Profile screen (L43) when convenient.
- Framework owner (FRAMEWORK_DRIFT 4d): seq 35 user -> headquarter; seq 32 drop Default Delivery Days; seq 4 / 5 users must match the prospect-outlet workflow diagram (seq 5 still blocked by D-TRAIN-1013-1); seq 36 part 2 never assert the on-load message; general rule: run users must match each document's workflow diagram.

## 5. Records left on cnr1dev1 (15108843)
- None new on 2026-10-14 (all checks read-only). Records of 2026-10-13 unchanged (see that report §6).

## 6. Files changed (knowledge)
document_lifecycle.md (new §0e, header), glossary.md (header, 3 new terms, 5 rows annotated), INDEX.md (header, roles paragraph, outlet / section / Delivery Man Shuffling rows), master_data/outlet.md, master_data/pjp.md, master_data/section_and_mappings.md, delivery_and_returns/delivery_man_shuffling.md, delivery_and_returns/goods_issue_note.md, OPEN_QUESTIONS.md (header, status, 1 / 1b / 3 headers, Q-PO1, Q-DM1, Q-DM2, Q-RL1, 2i / 2j notes, new 2k, contradictions 31 / 43 / 45 / 48, counts), FRAMEWORK_DRIFT.md (header, new 4d), LIVE_FINDINGS.md (new block; D-G66-2-1 heading and D-TRAIN-1013-2 status marked), learning_sessions/2026-10-12_G66-PK_parked_questions.md (Q-PO1, Q-DM1, Q-DM2, D-G66-2-1 removed with a dated note; C-45 updated), learning_sessions/README.md (row), learning_sessions/2026-10-14_SND-PK_QA-Team_live_log.md and _live_report.md (copies).
