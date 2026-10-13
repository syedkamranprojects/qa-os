# Parked questions after the QA team's answers (group 66 Setup review) - 2026-10-12

The QA team answered our 2026-10-09 Setup flow review on 2026-10-12. The answers are merged into the business pages (`learning_sessions/2026-10-12_SND-PK_QA-Team_answers_report.md`).

**Rule (QA lead, 2026-10-12):** the points below are **not sent now**. When a ticket or test case touches one of these areas, the question is raised with the QA team during that ticket's run, before its test case is executed (knowledge-gap gate). Once answered, record it in `OPEN_QUESTIONS.md` and the page, and remove it here.

**Update 2026-10-13:** the QA lead raised this list in a live training session with the QA team (`2026-10-13_SND-PK_QA-Team_live_report.md`). **Q-PJ6, Q-PJ7 and Q-PJ8 were answered 2026-10-13 in the live session** (OPEN_QUESTIONS.md section 2j) and are removed from this list. Q-PO1 is partly answered, C-49 is updated. The session resumes 2026-10-14 10:30 with the remaining rows.

| Id | Area (screens) | Question | What we know so far |
|---|---|---|---|
| Q-PO1 | Outlet: Prospect Outlet, Prospect Outlet Approval | (reworded 2026-10-13) What enabled **Forward** on the QA team's prospect outlet C0154187445 but not on our C0154187442 / C0154187444, created after Automation's rights change with the same workbook data? | 2026-10-13: Forward needs the user's right / role (granted to Automation by the QA team) and the Forward Save needs a Company address ("Company address cannot be empty."). Status In-Active + Draft and "Identified by" are not enough. Approval Forward fails: known issue D-TRAIN-1013-1 (reported to dev). On the 2026-10-14 list (#1). |
| Q-DM1 | Delivery: Delivery Man Shuffling | After a shuffle, which DM PJP / DSR does the order show? | - (on the 2026-10-14 list, #7) |
| Q-DM2 | Delivery: Delivery Man Shuffling | QA calls the shuffling behaviour a **known issue**: what is the correct behaviour? | Observed behaviour kept, marked as a known issue (contradiction 48). On the 2026-10-14 list (#7). |
| D-G66-2-1 | Company Mapping > Distributor > Outlet | Known issue (HTTP 500). Re-test when fixed. | QA confirmed it is a known issue. Fix date on the 2026-10-14 list (#9). |
| C-49 | Outlet: Change Track Outlet Profile | (updated 2026-10-13) QA correction: the screen lists **Active** outlets. Live 2026-10-13 it lists In-Active (Draft, Pending for approval) outlets too: is that a defect? | Possible defect **D-TRAIN-1013-2**, QA team to confirm. Request 74 on Draft C0154187435 (2026-10-05) fits the same behaviour. |
| C-45 | Section: Section Profile / Section Creation HQ | **Planned change:** delivery days will be entered on the Section Profile screen. Check whether it has been delivered when a section ticket comes. | QA, 2026-10-12. On the 2026-10-14 list (#8). |

Removed 2026-10-13 (answered in the live session, OPEN_QUESTIONS.md 2j): Q-PJ6 (Process creates the daily route + outlets due that day), Q-PJ7 (GPS / DDO via PJP Change Request, TSSM approval on the same screen), Q-PJ8 (approval follows the creating user's level).

## Separate: current ticket SDMS-6084 (not parked)
SDMS-6084 (Off Days on Distributor Profile HQ) was on hold until these answers arrived. Its own question is still open and belongs to that ticket's run:
- On Distributor Profile HQ, **Update** is refused with "Required" on **Report To \*** for distributor 15108843 (Sub Distributor = No). Is Report To meant to be mandatory here (possible defect), or should the test use a Report To value or another distributor?
