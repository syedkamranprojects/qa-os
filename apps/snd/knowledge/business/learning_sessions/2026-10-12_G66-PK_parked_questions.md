# Parked questions after the QA team's answers (group 66 Setup review) - 2026-10-12

The QA team answered our 2026-10-09 Setup flow review on 2026-10-12. The answers are merged into the business pages (`learning_sessions/2026-10-12_SND-PK_QA-Team_answers_report.md`).

**Rule (QA lead, 2026-10-12):** the points below are **not sent now**. When a ticket or test case touches one of these areas, the question is raised with the QA team during that ticket's run, before its test case is executed (knowledge-gap gate). Once answered, record it in `OPEN_QUESTIONS.md` and the page, and remove it here.

**Update 2026-10-13:** the QA lead raised this list in a live training session with the QA team (`2026-10-13_SND-PK_QA-Team_live_report.md`). **Q-PJ6, Q-PJ7 and Q-PJ8 were answered 2026-10-13 in the live session** (OPEN_QUESTIONS.md section 2j) and are removed from this list. Q-PO1 is partly answered, C-49 is updated. The session resumes 2026-10-14 10:30 with the remaining rows.

| Id | Area (screens) | Question | What we know so far |
|---|---|---|---|

**Update 2026-10-14:** the live session continued and completed the list. Removed 2026-10-14 (answered or closed, OPEN_QUESTIONS.md section 2k; log `2026-10-14_SND-PK_QA-Team_live_log.md`, report `2026-10-14_SND-PK_QA-Team_live_report.md`): **Q-PO1** (Forward needs a user whose role is in the prospect-outlet workflow diagram; C0154187445 was made by such a user; plus Company address) [stated 2026-10-14 QA team], **Q-DM1** (the order belongs to the destination DM PJP / delivery man) and **Q-DM2** (behaviour correct; only the on-load 'PJP not found' / "Required parameter 'pjpNo' is not present." message is a known issue) [stated 2026-10-14 QA team], **D-G66-2-1** (fixed: Company Mapping > Outlet sub-tab loads, re-tested live) [observed 2026-10-14]. Kept: **C-45** (waiting for the QA team's update on the section delivery-days enhancement) and the SDMS-6084 section below.

Removed 2026-10-14: C-45 (section delivery-days field is not part of R1; skip it in R1 scenarios [stated 2026-10-14 QA team]).

Removed 2026-10-14: C-49 (Draft outlets are listed on Change Track Outlet Profile by design; D-TRAIN-1013-2 withdrawn) [stated 2026-10-14 QA team].

Removed 2026-10-13 (answered in the live session, OPEN_QUESTIONS.md 2j): Q-PJ6 (Process creates the daily route + outlets due that day), Q-PJ7 (GPS / DDO via PJP Change Request, TSSM approval on the same screen), Q-PJ8 (approval follows the creating user's level).

## Separate: current ticket SDMS-6084 (not parked) - ANSWERED 2026-10-14
Report To is not needed when Sub Distributor = N [stated 2026-10-14 Syed Kamran]; the "Required" on Report To for 15108843 is defect D-6084-1 (LIVE_FINDINGS.md, OPEN_QUESTIONS.md 2l). Nothing left in this list.
