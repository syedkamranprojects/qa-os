# Parked questions after the QA team's answers (group 66 Setup review) - 2026-10-12

The QA team answered our 2026-10-09 Setup flow review on 2026-10-12. The answers are merged into the business pages (`learning_sessions/2026-10-12_SND-PK_QA-Team_answers_report.md`).

**Rule (QA lead, 2026-10-12):** the points below are **not sent now**. When a ticket or test case touches one of these areas, the question is raised with the QA team during that ticket's run, before its test case is executed (knowledge-gap gate). Once answered, record it in `OPEN_QUESTIONS.md` and the page, and remove it here.

| Id | Area (screens) | Question | What we know so far |
|---|---|---|---|
| Q-PO1 | Outlet: Prospect Outlet, Prospect Outlet Approval | What enables **Forward** on Prospect Outlet? It stays disabled, so a new outlet never reaches approval. | QA explained what a prospect outlet is, and that it works "if the required data is on the respective screens". Which data or user enables Forward is not known. |
| Q-PJ6 | PJP: PJP Daily Inquiry | What does **Process** create or change for a PJP? | Runs through an integration job; the result shows after refresh, cache eviction or re-login. |
| Q-PJ7 | PJP: PJP Creation DT, PJP Change Request | On which screen does a DT user update **GPS / DDO** after approval, and does that change need TM approval? | Read-only at creation on DT; editable for all DT users once the PJP is approved (QA). |
| Q-PJ8 | PJP: PJP Creation HQ, PJP Approval | Does a PJP created on **PJP Creation HQ** need TM approval? | QA: HQ changes need no approval. Observed 2026-10-09: AUTO241010 stayed In-Active until the TM approved it (contradiction 47). |
| Q-DM1 | Delivery: Delivery Man Shuffling | After a shuffle, which DM PJP / DSR does the order show? | - |
| Q-DM2 | Delivery: Delivery Man Shuffling | QA calls the shuffling behaviour a **known issue**: what is the correct behaviour? | Observed behaviour kept, marked as a known issue (contradiction 48). |
| D-G66-2-1 | Company Mapping > Distributor > Outlet | Known issue (HTTP 500). Re-test when fixed. | QA confirmed it is a known issue. |
| C-49 | Outlet: Change Track Outlet Profile | The screen accepted change request 74 on a **Draft** outlet, but change tracking applies only to approved outlets. Should it block Draft outlets? | QA: change tracking applies to approved outlets only. |
| C-45 | Section: Section Profile / Section Creation HQ | **Planned change:** delivery days will be entered on the Section Profile screen. Check whether it has been delivered when a section ticket comes. | QA, 2026-10-12. |

## Separate: current ticket SDMS-6084 (not parked)
SDMS-6084 (Off Days on Distributor Profile HQ) was on hold until these answers arrived. Its own question is still open and belongs to that ticket's run:
- On Distributor Profile HQ, **Update** is refused with "Required" on **Report To \*** for distributor 15108843 (Sub Distributor = No). Is Report To meant to be mandatory here (possible defect), or should the test use a Report To value or another distributor?
