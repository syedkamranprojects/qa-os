# PJP Daily Inquiry Update: closing the DSR's journey (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas and the snd-schema DB. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flow: 00930001 (seq 57). No live replay.

## 1. Purpose
A PJP (permanent journey plan) is a DSR's route; each working day gets a "daily" PJP record. This screen lets a back-office user correct the daily record: journey status, DSR file status and end time, typically to close the day after settlement. [inferred]

## 2. Actors and roles
Auto_Multi_Orga (same session) [db].

## 3. Documents and master data
`snd_en_pjp_pjphead_daily` (daily PJP head); related `snd_en_pjd_pjpdetail_daily`, `snd_en_pjv_pjpvisit_daily`, `snd_en_dfs_dsr_file_status` (DSR file status) [db: names].

## 4. Inputs: screens and fields
Menu: Distributor Setup > Journey Plan > PJP Daily Inquiry Update (`DYL_BG1022`) [db]. 009301: **Working Date**; button Refresh. 009302 grid columns: Organization Code, Type, PJP Number, Distributor Code, DSR, Serial No, Current Status, Mark Status, DSR Files Status, Working Date, Start Date, End Date, Date [db]. Editable in row edit: **DSR**, **Mark Status** (dropdown, id JourneyStatus), **DSR Files Status** (dropdown), **End Date** (date picker) [db: atlas].

Live-verified 2026-10-01 [observed + db]: layoutCode=BG1022 (Distributor Setup > Journey Plan); filter Working Date (default today); grid 8 rows, 8 columns: PJP Number, DSR, Current Status, Mark Status, DSR Files Status, Working Date, Start Date, End Date, Edit link. Mark Status and DSR Files Status are blank for all rows and become dropdowns only in Edit mode (not clicked). Db-declared page config BG1022002: Mark Status (epjp_journey_status) fixed list = E "End of Day" (single value); DSR Files Status (epjp_dsr_file_status) fixed list = P "process", C "complete" (captions are DYP.G translations). Confirm the labels live in Edit mode on a throwaway.

## 5. Process
1. [Maker] Open PJP Daily Inquiry Update; set Working Date; Refresh. trace 11:57:00930001
2. [Maker] Pick the PJP row (`row_1_pjp_number`), row Edit.
3. [Maker] Set DSR, Mark Status, DSR Files Status, End Date; row Save; assert toast from PJP_Inquiry_ASSR.

## 6. Outputs and effects
Daily PJP row's journey status, file status and end time updated; the effect on route settlement and on mobile app sync is [unknown].

## 7. Statuses and transitions
Mark Status = E End of Day only; DSR Files Status = P process / C complete [db 2026-10-01, labels to confirm live]; transitions [unknown].

## 8. Rules and validations
None declared in sources [unknown]. End Date presumably must not precede Start Date [inferred].

## 9. Messages
Not recorded [unknown].

## 10. Dependencies
Reads daily PJPs generated for the working date; runs after Route Settlement (seq 51) and Deposit slips. Date-keyed.

## 11. Test design hints
Positive: mark a PJP completed with end date today. Negative: end date before start; no working date; edit a PJP of another distributor. Boundary: end date = start date; midnight. A green run checks only the toast, not that the dropdowns persisted.

## 12. Open questions
Q: Allowed Mark Status / DSR Files Status values? | Default: End of Day; process / complete | Evidence: db-declared 2026-10-01 (PARTLY answered, Q55); live Edit-mode read pending.
Q: Does marking complete block further collection for that day? | Default: yes | Evidence: none.

## 13. Sources
framework_atlas/flows/00930001; screens_db/DYL_BG1022.json; group_11.md; DB table list (snd_en_pjp_pjphead_daily).
