---
option: PJP Daily Inquiry Update (day close)
area: settlement_and_finance
doc_types: []
screens: [DYL_BG1022]
framework_flows: ["00930001"]
markets: [PK]
roles: [Maker]
depends_on: [route_settlement, deposit_slips]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-08
---

# PJP Daily Inquiry Update: closing the DSR's journey (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas and the snd-schema DB. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flow: 00930001 (seq 57). No live replay. (superseded 2026-10-05: walked live in G11-2b; this is THE DAY CLOSE.)
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.
Updated 2026-10-08: merged the QA team's written answers to the 2026-10-06 review (learning_sessions/2026-10-06_G11-PK_QA_Team_Review.docx); evidence learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx). Tag [stated 2026-10-08 QA Team] = written answer of the QA team. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08: ...)".

## 1. Purpose
A PJP (permanent journey plan) is a DSR's route; each working day gets a "daily" PJP record. This screen lets a back-office user correct the daily record: journey status, DSR file status and end time, typically to close the day after settlement. [inferred]
- **G11-2b: this is the day close** [observed 2026-10-05 G11-2b]: setting Mark Status "End Of Day" and DSR Files Status "Complete" on the delivery PJP's row for the Working Date closes that route's day (Current Status becomes E). The QA team member closed the earlier un-closed days (09-30, 10-01) this way: the 10-01 row of 02112 reads Current Status E / End Of Day / Complete [observed 2026-10-05 G11-2b; stated 2026-10-05 QA lead]. It follows Route Settlement (on 10-05 the route was Complete before the close) [observed order].
- G11-3: the day close was done again for 2026-10-06 after settlement and DSR adjustment (settlement -> DSR adjustment -> day close) [observed 2026-10-06 G11-3]. The 10-05 close let 10-06 be settled without "Following previous days not closed!" [observed 2026-10-06 G11-3; causal link inferred].
- QA team 2026-10-08 (rule 21): confirmed that the day close = PJP Daily Inquiry Update (End Of Day + Complete -> Current Status E) after settlement and DSR adjustment; **this option is used for manual working from the Back Office** [stated 2026-10-08 QA Team] (in production the day is driven by the DSR's mobile sync and the settlement [inferred from rule 12]).

## 2. Actors and roles
Auto_Multi_Orga (same session) [db].
- G11-2b: Maker Auto_Multi_Orga closed 02112 for 2026-10-05 [observed 2026-10-05 G11-2b]. The QA lead allowed every button for this step ("you are allowed to click on every button now"; Bounce still avoided) [stated 2026-10-05 QA lead].
- G11-3: Maker Auto_Multi_Orga closed 02112 for 2026-10-06 (seq 57, part of the QA Team Lead's plan) [observed 2026-10-06 G11-3].

## 3. Documents and master data
`snd_en_pjp_pjphead_daily` (daily PJP head); related `snd_en_pjd_pjpdetail_daily`, `snd_en_pjv_pjpvisit_daily`, `snd_en_dfs_dsr_file_status` (DSR file status) [db: names].

## 4. Inputs: screens and fields
Menu: Distributor Setup > Journey Plan > PJP Daily Inquiry Update (`DYL_BG1022`) [db]. 009301: **Working Date**; button Refresh. 009302 grid columns: Organization Code, Type, PJP Number, Distributor Code, DSR, Serial No, Current Status, Mark Status, DSR Files Status, Working Date, Start Date, End Date, Date [db]. Editable in row edit: **DSR**, **Mark Status** (dropdown, id JourneyStatus), **DSR Files Status** (dropdown), **End Date** (date picker) [db: atlas].

Live-verified 2026-10-01 [observed + db]: layoutCode=BG1022 (Distributor Setup > Journey Plan); filter Working Date (default today); grid 8 rows, 8 columns: PJP Number, DSR, Current Status, Mark Status, DSR Files Status, Working Date, Start Date, End Date, Edit link. Mark Status and DSR Files Status are blank for all rows and become dropdowns only in Edit mode (not clicked). Db-declared page config BG1022002: Mark Status (epjp_journey_status) fixed list = E "End of Day" (single value); DSR Files Status (epjp_dsr_file_status) fixed list = P "process", C "complete" (captions are DYP.G translations). Confirm the labels live in Edit mode on a throwaway.
- G11-2b live layout [observed 2026-10-05 G11-2b]: menu search "PJP Daily" offers **PJP Daily Inquiry** (DYL_202037, read-only) and **PJP Daily Inquiry Update** (DYL_BG1022). Header Working Date (default today); grid PJP Number, DSR, Current Status, Mark Status, DSR Files Status, Working Date, Start Date, End Date, Edit (2 pages). Edit makes the row editable: DSR (text), **Mark Status** (dropdown: only "End Of Day"), **DSR Files Status** (dropdown: Process, Complete), End Date (date picker); row links Save / Cancel.

## 5. Process
1. [Maker] Open PJP Daily Inquiry Update; set Working Date; Refresh. trace 11:57:00930001
2. [Maker] Pick the PJP row (`row_1_pjp_number`), row Edit.
3. [Maker] Set DSR, Mark Status, DSR Files Status, End Date; row Save; assert toast from PJP_Inquiry_ASSR.

G11-2b walk, the day close (2026-10-05) [observed 2026-10-05 G11-2b]:
1. [Maker] Navigate to PJP Daily Inquiry Update; Choose Working Date 2026-10-01; Verify row 02112 / ITB0189: Current Status E, Mark Status End Of Day, DSR Files Status Complete, Start/End Date empty (closed by the QA team member); other PJPs (02111, 7918624876, AUTO021311, AUTO031026) blank (11:57:00930001).
2. [Maker] Choose Working Date 2026-10-05; Click Edit on row 02112; Choose Mark Status End Of Day; Choose DSR Files Status Complete; leave End Date empty; Click Save -> "Record Updated Successfully"; row shows Current Status E, End Of Day, Complete (11:57:00930001).

G11-3 walk, the day close (2026-10-06) [observed 2026-10-06 G11-3]:
1. [Maker] Navigate to PJP Daily Inquiry Update; Working Date 2026-10-06; Click Edit on row 02112 / ITB0189.
2. [Maker] Choose Mark Status End Of Day (only option; code E) and DSR Files Status Complete (Process | Complete; code C); leave End Date empty; Click Save -> **"Record Updated Successfully"**; row Current Status **E**, End Of Day, Complete (11:57:00930001).

## 6. Outputs and effects
Daily PJP row's journey status, file status and end time updated; the effect on route settlement and on mobile app sync is [unknown].
- G11-2b: the row's Current Status becomes **E**; no stock effect (ATP 309 unchanged until the SAN) [observed 2026-10-05 G11-2b]. Whether this is what clears Route Settlement's "Following previous days not closed!" for later days is [inferred] (consistent with the 10-01 close by the QA member; the QA lead's detailed note is pending, Q-RS1).

## 7. Statuses and transitions
Mark Status = E End of Day only; DSR Files Status = P process / C complete [db 2026-10-01, labels to confirm live]; transitions [unknown].
- G11-2b (replaces "Mark Status = E End of Day only [db]; transitions unknown") [observed 2026-10-05 G11-2b]:

| from | action | to | by | tag |
|---|---|---|---|---|
| blank Current / Mark / Files status | Edit, Mark Status End Of Day + DSR Files Status Complete, Save | Current Status E, End Of Day, Complete | Maker | observed 2026-10-05 G11-2b |
| (alternative) | DSR Files Status Process | not tried | - | unknown |

## 8. Rules and validations
None declared in sources [unknown]. End Date presumably must not precede Start Date [inferred].
- G11-2b: Mark Status has a single value "End Of Day"; DSR Files Status Process / Complete (db E / P / C confirmed with live labels) [observed 2026-10-05 G11-2b].
- G11-2b: End Date may stay empty on Save (as on the QA member's 10-01 row) [observed 2026-10-05 G11-2b].
- G11-2b: the close is per delivery PJP and Working Date [observed 2026-10-05 G11-2b].
- G11-3: same rule and values confirmed on a second day by Claude [observed 2026-10-06 G11-3].

## 9. Messages
Not recorded [unknown].
- G11-2b: **"Record Updated Successfully"** on row Save [observed 2026-10-05 G11-2b].
- G11-3: "Record Updated Successfully" again [observed 2026-10-06 G11-3].

## 10. Dependencies
Reads daily PJPs generated for the working date; runs after Route Settlement (seq 51) and Deposit slips. Date-keyed.
- G11-2b: runs after Route Settlement of the same route/date (observed order on 10-05); is presumably what Route Settlement's previous-day check looks for on later days [inferred; Q-RS1].
- **Role of the day close** [stated 2026-10-06 QA Team Lead]: it clears the per-PJP previous-day check of Route Settlement ("Following previous days not closed! Please close date <date>"); the route row then shows green (closed). (superseded 2026-10-06: the [inferred] "presumably what the previous-day check looks for".)
- G11-3: day order settled with the QA Team Lead: Route Settlement (51) -> DSR Adjustment Amount (56) -> day close (57) [observed 2026-10-06 G11-3]. Consistent with the previous-day check: after the 10-05 close, the 10-06 settlement got no previous-day error [observed; link inferred].

## 11. Test design hints
Positive: mark a PJP completed with end date today. Negative: end date before start; no working date; edit a PJP of another distributor. Boundary: end date = start date; midnight. A green run checks only the toast, not that the dropdowns persisted.
- G11-2b additions [observed 2026-10-05 G11-2b]:
  - Positive: close the delivery PJP's day (End Of Day + Complete) -> "Record Updated Successfully", Current Status E.
  - Positive (next day): after closing day D, Route Settlement on day D+1 must not report D as "not closed" (not yet tested; Q-RS1).
  - Trap: the day close is a shared-environment change: closing days on cnr1dev1 affects other testers; get the QA lead's go-ahead.
  - Trap: the workbook (sheet PJP Daily2: PJP 2112, DSR ITB0189, End Of Day, Complete, End Date = time) sets an End Date; the QA member's close left it empty and still worked.
- G11-3 additions: Positive (next day) is now partly evidenced: day D=10-05 closed, D+1=10-06 settled with no previous-day error [observed 2026-10-06 G11-3]. Trap: close only after settlement and the DSR adjustment of the day.
- QA team 2026-10-08: the previous-day check of Route Settlement verifies PJP working date = current date and closing date = N-1 [stated 2026-10-08 QA Team]; the close here is what makes N-1 closed.

## 12. Open questions
Q: Allowed Mark Status / DSR Files Status values? | Default: End of Day; process / complete | Evidence: db-declared 2026-10-01 (PARTLY answered, Q55); live Edit-mode read pending.
Q: Does marking complete block further collection for that day? | Default: yes | Evidence: none.
- ANSWERED 2026-10-05 (Q55): Mark Status options = End Of Day only; DSR Files Status = Process, Complete [observed 2026-10-05 G11-2b].
- Q-RS1 PARTLY ANSWERED 2026-10-05: the day is closed here (End Of Day + Complete -> Current Status E); the detailed procedure (order, permissions on cnr1dev1, whether it clears the previous-day check) is pending from the QA lead [stated 2026-10-05 QA lead] | Class: C.
- Q (does marking complete block further collection) still open (class A default: yes).
- Q-RS1 procedure part ANSWERED 2026-10-06 (see route_settlement.md): settlement -> DSR adjustment -> day close here [observed 2026-10-06 G11-3; stated 2026-10-06 QA Team Lead].
- **Q-RS1 FULLY ANSWERED 2026-10-06** [stated 2026-10-06 QA Team Lead]: the day close here (End Of Day + Complete) is what clears Route Settlement's previous-day check for that PJP; until it is done, the next day of the PJP cannot be finalized.

## 13. Sources
framework_atlas/flows/00930001; screens_db/DYL_BG1022.json; group_11.md; DB table list (snd_en_pjp_pjphead_daily).
- G11-2b: learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md (seq 56 workbook hint, seq 57).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 57).

- QA team written answers 2026-10-08: learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx) (rules 18, 21).
