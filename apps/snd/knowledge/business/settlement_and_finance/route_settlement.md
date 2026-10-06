---
option: Route Settlement
area: settlement_and_finance
doc_types: [route settlement row (PJP + working date)]
screens: [ROUTE_SETTLEMENT]
framework_flows: ["00680001", "03210001", "03220001", "03250001"]
markets: [PK]
roles: [Maker]
depends_on: [goods_issue_note, cashmemo_reschedule_and_status, sales_return, goods_return_note, deposit_slips, pjp_daily_inquiry_update]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-06
---

# Route settlement: closing a DSR's day (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**. Rules: `docs/LEARNING_STANDARD.md` §3.
Last updated: 2026-10-01 (consolidated with learning session G11-1, seq 51). Source flows: 00680001 (seq 51), 03210001 (52), 03220001 (53), 03250001 (54). ~~No live replay.~~ (superseded 2026-10-01: seq 51 opened live in G11-1 and the grid was read; the settlement itself was BLOCKED by an unclosed previous day; seq 52-54 not walked.) DB has 35 settlement rows, all org 0101, none for 010104 [db, before the walk].
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md and 2026-10-06_G11-PK_session3_report.md. **The settlement was performed live by Claude for the first time** (route 02112, 2026-10-06). Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.

## 1. Purpose
Route settlement is the end-of-day reconciliation of one PJP (a DSR's route) for one working date: what was sold and delivered, what was returned, what cash and cheque was collected (previous days plus today), what stock was short, and the resulting cash shortage. It follows delivery, returns and deposit slips and precedes closing the day (PJP Daily Inquiry Update). [inferred from field and table names]
- Confirmed live: one grid row per delivery man of the date, with order counts, sale value, returns, collections (one line per deposit slip) and shortages [observed 2026-10-01 G11-1].
- Settlement is a **day-ordered** process: a route cannot be settled while any earlier working day is still open [observed 2026-10-01 G11-1].
- G11-2b: settlement is followed by the day close on PJP Daily Inquiry Update (End Of Day / Complete); on 2026-10-05 the route was settled first, then the day was closed [observed 2026-10-05 G11-2b]. Settlement is also the moment deposit slips are **posted** (see deposit_slips.md) [observed 2026-10-05 G11-2b].
- G11-3: the day's order was settlement (seq 51) -> DSR Adjustment Amount (seq 56) -> day close (seq 57) [observed 2026-10-06 G11-3]. Settlement also requires that **no order due today on the route is undelivered** (see section 8) [observed 2026-10-06 G11-3].

## 2. Actors and roles
Auto_Multi_Orga (same session) [db; observed 2026-10-01 G11-1, segment 9]. No approval step [db]. Checker behaviour not walked [unknown].
- G11-2b: the 2026-10-01 and 2026-10-05 settlements of route 02112 were done by a QA team member (not by Claude), so the settlement action itself, its screens and its message were not observed [stated 2026-10-05 QA lead; observed result only].
- G11-3: the Maker (Auto_Multi_Orga) settled route 02112 for 2026-10-06 (Edit -> row Save); no approval step followed [observed 2026-10-06 G11-3]. (superseded 2026-10-06: the settlement action is now observed, see section 5.)

## 3. Documents and master data
- `snd_tr_rsl_dsr_route_settlem` (one row per PJP code + working date): total/delivered/undelivered order counts, return picked up, sales value, return value, adjusted credit note amount, previous/today/total cash and cheque, stock shortage, stock shortage received amount, cash shortage, settlement datetime [db].
- `snd_tr_rsd_dsr_route_setl_dt`: one line per deposit-slip type (e.g. CSH "CASH"): suggested vs entered amount [db]. (superseded 2026-10-01: on screen the Collection Type list shows **one line per deposit slip**, labelled "<slip>-CASH" / "<slip>-CHEQUE", plus a "Stock Shortage" line [observed 2026-10-01 G11-1]; whether the table stores per slip or per type is [unknown].)
- Needs a PJP with delivered cash memos and collections. The row is keyed by the **delivery** PJP (02112-AutomationDSR), not the booking PJP [observed 2026-10-01 G11-1].

## 4. Inputs: screens and fields
Menu: Transaction > Receivable > Route Settlement (`ROUTE_SETTLEMENT`, /content-master/route-settlement) [db; observed 2026-10-01 G11-1].
- 006801: **Date** (date picker), **PJP Number** (autoselect), Select all (`selectAll`) then load [db].
- Header as seen [observed 2026-10-01 G11-1]: Date (default today), PJP Number (empty = all PJPs), "Select All", Route Status (default All), and read-only totals Total Payable Amount, Total Received Amount, Total Cash Shortage.
- Grid, one row per delivery man of the date [observed 2026-10-01 G11-1]: PJP Delivery Man Code, Delivery Man, Total Order, Delivered Orders (link), Undelivered Orders, Sale Value, Adjusted Credit Note Amount, Fresh Return Value, Total Cash Collected (Previous / Today / Total), Total Cheque Collect (Previous / Today / Total), Collection Type, Payable Amount, Received Amount, Cash Shortage, Edit.
- Edit on a row starts the settlement of that route [observed 2026-10-01 G11-1].
- Validation screens (read-only, compared with workbook/DB): 006802 Sale Value, Adjusted Credit Note Amount, Fresh Return Value; 006803 Previous Cash, Today Cash, Total Cash, Previous Cheque, Today Cheque, Total Cheque; 006804 Payable Amount, Received Amount, Stock Shortage Payable Amt, Stock shortage Received Amt; 006805 Cash Shortage, Total Payable Amount, Total Received Amount (row edit and save); 006806 Total Received Amount, Total Payable Amount, Total Cash Shortage [db: atlas].
- G11-2b: **Route Status filter values: All / Complete / Incomplete** [observed 2026-10-05 G11-2b]. A settled route row is shown **green and has no Edit link** (other rows keep Edit) [observed 2026-10-05 G11-2b]. Header totals (Total Payable / Received / Cash Shortage) are computed over the rows the filter shows (Incomplete filter on 10-01 -> 0 / 0 / 0) [observed 2026-10-05 G11-2b].
- G11-3 edit mode of a row [observed 2026-10-06 G11-3]: after Edit the row's Collection lines are editable per type: **CASH lines: Received editable** (prefilled = Payable); **CHEQUE lines: Received read-only**; **Stock Shortage line: Received editable** (0). The row Save sits at the right of the scrolled grid (scroll it into view first).
- G11-3: an unsettled route row with activity is shown yellow; a settled one green [observed 2026-10-06 G11-3].
- **Colour legend** [stated 2026-10-06 QA Team Lead]: per PJP row, **yellow = route not closed yet, green = route closed** (02112 was yellow before the 10-06 settlement and green after the row Save) [observed 2026-10-06 G11-3].

## 5. Process
Framework view [db]:
1. [Maker] Open Route Settlement; enter Date and PJP Number; Select all. trace 11:51:00680001
2. [Maker] Validate Sale Value, Adjusted Credit Note, Fresh Return Value. [db]
3. [Maker] Validate previous/today/total cash and cheque. [db]
4. [Maker] Validate payable vs received and stock shortage; edit a row and save to set the received amount per type. [db]
5. [Maker] Validate totals and total cash shortage; each screen asserts a toast (TSTMSG).
6. [Maker] Seq 52: Transaction Inquiry for the outlet, read **Offset Amount** (screen 032102): the part of the invoice offset by returns/credit notes [inferred]. 11:52
7. [Maker] Seq 53/54: reopen the deposit slip and read **Received Amount** after settlement; seq 54 after an order removal. 11:53, 11:54

Observed business steps (2026-10-01 G11-1) [observed]:
1. [Maker] Open Transaction > Receivable > Route Settlement (Date today, PJP Number empty, Route Status All). trace 11:51:00680001
2. [Maker] Verify the row of 02112-AutomationDSR: Total Order 4, Delivered 3, Undelivered 0, Sale Value 311,238, Adjusted Credit Note 0, Fresh Return 0. trace 11:51:00680001
3. [Maker] Verify Total Cash Collected 0 / 102,761 / 102,761 and Total Cheque Collect 0 / 121,370 / 121,370. trace 11:51:00680001
4. [Maker] Verify the Collection Type lines (one per deposit slip) with Payable = Received, and header totals Payable 224,131 = Received 224,131, Cash Shortage 0. trace 11:51:00680001
5. [Maker] Click Edit on the row -> popup "Following previous days not closed! Please close date. 2026-09-30" (Continue). **Settlement stops here.** trace 11:51:00680001
6. Seq 52-54 (03210001, 03220001, 03250001) not walked: they depend on a completed settlement [observed 2026-10-01 G11-1].

G11-2 / G11-2b (2026-10-05) [observed 2026-10-05 G11-2, G11-2b]:
1. [Maker] Open Route Settlement, Date 2026-10-05 (morning, G11-2); Verify row 02112: Total Order 13, Delivered 3, Undelivered 0, Sale Value 311,238, Adjusted Credit Note 0, Fresh Return 0, Cash 0 / 102,761 / 102,761, Cheque 1,000 (Previous) / 120,370 / 121,370; collection lines 1137-1142; header 224,131 / 224,131 / 0 (11:51:00680001).
2. [Maker] Click Edit on 02112 -> "Following previous days not closed! Please close date. 2026-10-01" (the blocker date had moved from 09-30 to 10-01). Run stopped [observed 2026-10-05 G11-2].
3. A QA team member closed the earlier days and settled the routes [stated 2026-10-05 QA lead].
4. [Maker] (G11-2b, afternoon) Open Route Settlement; Choose Route Status Complete; Verify 02112 for 2026-10-05 is Complete (green, no Edit), values unchanged from the morning; Verify 02112 for 2026-10-01 is Complete too (values as G11-1); Choose Incomplete for 2026-10-01 -> 4 zero-activity routes (8197298470 Aslam PJP DM, AutoPJGIN2, AutoPromo2, AUTO301301) still Incomplete with Edit (11:51:00680001).
5. [Maker] Read the effects in Transaction Inquiry (Offset Amount, 11:52:03210001) and Deposit Slip (Posted, Received, outstanding memos; 11:53:03220001, 11:54:03250001).

G11-3 (2026-10-06): **settlement performed by Claude** (answers the procedure part of Q-RS1) [observed 2026-10-06 G11-3 unless tagged otherwise]:
1. [Maker] Open Route Settlement, Date 2026-10-06, all PJPs; Verify row 02112: Total Order 6, Delivered 3, **Undelivered 1**, Sale Value 285,519, Cash 0 / 102,761 / 102,761, Cheque 1,000 (Previous) / 109,202 / 110,202; header 212,963 / 212,963 / 0. trace 11:51:00680001
2. [Maker] Click Edit -> modal Error **"Un-Deliver Order exists for today delivery!"**; Show details lists COL26000002012 (outlet 08, booked 2026-10-05 on PJP 02111, Net 108,202) = the 10-05 order rescheduled (Reattempt) to 10-06 and not delivered. Continue closes the modal; nothing changes.
3. Resolution [stated 2026-10-06 QA Team Lead]: a Reattempt order due today must be **allocated** in Order Stock Allocation (Order Date = its booking date, 2026-10-05), put on a **new GIN**, the GIN **approved by the Checker**, and the memo marked **Delivered** in Cashmemo Status; it may stay **unpaid**. Done live: allocation "Process completed successfully"; Edit still refused after the allocation alone; GIN 509 (only 2012 offered) saved and forwarded by the Maker, approved by Auto_Tssm; Cashmemo Status "Updated successfully" [observed].
4. [Maker] Reopen Route Settlement; Verify row 02112: Delivered **4**, Undelivered **0**, Sale Value **393,721** (+ 2012 108,202); header still 212,963 / 212,963 / 0.
5. [Maker] Click Edit on the row (no error) -> the row is in edit mode; Verify the CASH lines (1143, 1145, 1148) Received = Payable (editable), CHEQUE lines (1144, 1146, 1147) read-only, Stock Shortage 0; left as prefilled.
6. [Maker] Click the row Save -> **"Saved Successfully"** -> row turns **green**, Edit link gone = Complete; header unchanged 212,963 / 212,963 / 0. trace 11:51:00680001
7. [Maker] Verify the effects in Transaction Inquiry (Offset, 11:52:03210001) and Deposit Slip (Posted, Received, outstanding memos; 11:53:03220001, 11:54:03250001).
8. [Maker] Then DSR Adjustment Amount (seq 56) and the day close on PJP Daily Inquiry Update (seq 57).

## 6. Outputs and effects
A settlement row for PJP/date with shortage figures and lines per payment type (suggested vs entered); time-stamped (`trsl_route_settl_datetime`) [db]. Cash shortage = payable minus received [inferred].
- Pre-settlement values for 02112 on 2026-10-01 [observed 2026-10-01 G11-1]:

| Field | Value | Explained by |
|---|---|---|
| Total Order | 4 | COL26000002003-2006 = orders on GIN 506 excluding 2007 (cancelled after the GIN) |
| Delivered Orders | 3 | 2003, 2004, 2005 (Delivered/Invoiced) |
| Undelivered Orders | 0 | the rescheduled 2006 (Reattempt) counts as neither |
| Sale Value | 311,238 | 90,707 + 101,161 + 119,370 (delivered orders; 2003 at its edited Net) |
| Adjusted Credit Note Amount | 0 | approved + picked return COL26000000713 (29,077) NOT netted |
| Fresh Return Value | 0 | |
| Total Cash Collected | 0 / 102,761 / 102,761 | slips 1131 (101,161) + 1133 (600) + 1136 (1,000) |
| Total Cheque Collect | 0 / 121,370 / 121,370 | slips 1132 (119,370) + 1134 (1,000) + 1135 (1,000) |
| Collection Type (Payable = Received) | 1132-CHEQUE 119,370; 1134-CHEQUE 1,000; 1135-CHEQUE 1,000; 1131-CASH 101,161; 1133-CASH 600; 1136-CASH 1,000; Stock Shortage 0 | one line per slip, at its **allocated** amount (1133 shows 600, not its 1,000 slip amount) |
| Total Payable / Received / Cash Shortage | 224,131 / 224,131 / 0 | |

- **Sale Value vs collected**: 311,238 sold vs 224,131 collected -> 87,107 still owed, but **not shown as cash shortage** before settlement (Payable is built from the slips, not from Sale Value) [observed 2026-10-01 G11-1; how the shortfall is treated at settlement is unknown].
- Total = Previous + Today holds for cash and cheque (Previous 0 here) [observed 2026-10-01 G11-1, upgrades the [inferred] rule in section 8].
- The effect of a completed settlement (deposit-slip posting, cash memo Received/Balance, settlement row) was NOT observed [unknown; Q-DS1].

G11-2b effects of the completed settlement of 02112 for 2026-10-05 [observed 2026-10-05 G11-2b]:

| Field / effect | Value | Explained by |
|---|---|---|
| Route Status | Complete (green, Edit hidden) | settled by the QA team member |
| Total Order | 13 | not explained (10-01: 4); Q-RS3 |
| Delivered / Undelivered | 3 / 0 | 2009, 2010, 2011; rescheduled 2012 counts as neither |
| Sale Value | 311,238 | 90,707 + 101,161 + 119,370 (2009 at its edited Net) |
| Adjusted Credit Note / Fresh Return | 0 / 0 | return COL26000000714 (29,077) still NOT netted (Q-SR1) |
| Total Cash Collected | 0 / 102,761 / 102,761 | slips 1137 101,161 + 1139 600 + 1142 1,000 |
| Total Cheque Collect | **1,000 (Previous)** / 120,370 / 121,370 | today 1138 119,370 + 1141 1,000; Previous 1,000 = slip 1140 (outlet multi-cheque) applied to the 10-01 memo COL26000002003 [inferred, consistent with seq 53] |
| Collection lines (Payable = Received) | 1138 CHEQUE 119,370; 1140 CHEQUE 1,000; 1141 CHEQUE 1,000; 1137 CASH 101,161; 1139 CASH 600; 1142 CASH 1,000; Stock Shortage 0 | one line per slip at its allocated amount |
| Header Payable / Received / Cash Shortage | 224,131 / 224,131 / 0 | |
| Deposit slips 1137-1142 | Un Posted -> **Posted**; 1139 amount trimmed 1,000 -> 600 | posting at settlement (deposit_slips.md) |
| Cheques 1234501, 12444, 22337, 12222, 1234567 (x2) | Cheque Status **Clear**, dated 2026-10-05 | cheque_status.md [inferred: set by posting] |
| Cash memo Received / Offset | 2009 Received 2,600 (Balance 88,107); 2010 101,161; 2011 119,370 | transaction_inquiry.md, deposit_slips.md |
| Stock | none (ATP 309 unchanged until the SAN) | stock_inquiry_and_balances.md |

G11-3 values of the settlement of 02112 for 2026-10-06 [observed 2026-10-06 G11-3]:

| Field / effect | Before (blocked) | After 2012 delivered + settled | Explained by |
|---|---|---|---|
| Total Order | 6 | 6 | not fully explained (Q-RS3) |
| Delivered / Undelivered | 3 / **1** | **4 / 0** | 2015, 2016, 2020 (+ 2012); the undelivered one = 2012, due today |
| Sale Value | 285,519 | **393,721** | 76,156 + 101,161 + 108,202 (+ 108,202 for 2012) |
| Adjusted Credit Note / Fresh Return | 0 / 0 | 0 / 0 | return COL26000000715 (29,066) again not netted (Q-SR1) |
| Total Cash Collected | 0 / 102,761 / 102,761 | same | 1143 101,161 + 1145 600 + 1148 1,000 |
| Total Cheque Collect | **1,000 (Previous)** / 109,202 / 110,202 | same | today 1144 108,202 + 1147 1,000; Previous 1,000 = multi-cheque 1146 applied to an older outlet-04 memo by the Outstanding Outlet FIFO adjustment (oldest invoice first) [target inferred; FIFO rule stated 2026-10-06 QA Team Lead] |
| Collection lines | 1144 / 1146 / 1147 CHEQUE; 1143 / 1145 (600) / 1148 CASH; Stock Shortage 0 | same, Received = Payable | one line per slip at its allocated amount |
| Header Payable / Received / Cash Shortage | 212,963 / 212,963 / 0 | 212,963 / 212,963 / 0 | unpaid 2012 (108,202) is NOT a cash shortage; it stays open on the memo |
| Route Status | Incomplete (yellow) | **Complete** (green, no Edit) | row Save "Saved Successfully" |
| Deposit slips 1143-1148 | Un Posted | **Posted**; 1145 trimmed 1,000 -> 600 | deposit_slips.md |
| Cheques of 1144, 1146, 1147 | - | **Clear** | cheque_status.md |
| Memo balances | - | 2015 Received 2,600 / Balance 73,556; 2016 and 2020 paid (leave the outstanding list); 2012 0 / 108,202 | deposit_slips.md, transaction_inquiry.md |

- **Uncovered Sale Value is not a cash shortage**: 311,238 sold vs 224,131 collected, yet Cash Shortage 0 after settlement; the uncovered part stays open on the cash memos (2009 Balance 88,107 still in the outstanding list) [observed 2026-10-05 G11-2b]. Answers Q-RS2.
- **10-01 route Complete but its slips not posted**: 02112 for 2026-10-01 shows Complete, yet slips 1131-1136 are still Un Posted (1133 still 1,000 / 600 adjusted) [observed 2026-10-05 G11-2b]; so "Complete" does not guarantee posting; how the QA member completed 10-01 must come from the QA lead (Q-DS3).

## 7. Statuses and transitions
No document status column in the settlement tables [db]; "settled" is implied by row existence [inferred].
- The screen has a **Route Status** filter (default All) [observed 2026-10-01 G11-1]; its values were not opened [unknown].

| from | action | to | by | tag |
|---|---|---|---|---|
| route of the day, not settled | Edit while an earlier day is open | blocked ("Following previous days not closed! ...") | Maker | [observed 2026-10-01 G11-1] |
| route of the day, not settled | Edit and save (previous days closed) | settled; deposit slips Posted (presumed) | Maker | [inferred; Q-DS1] |

- G11-2b (replaces "Route Status values not opened"): Route Status has **All / Complete / Incomplete** [observed 2026-10-05 G11-2b].

| from | action | to | by | tag |
|---|---|---|---|---|
| Incomplete (Edit shown) | settle (Edit and save; done by the QA team member) | Complete: green row, Edit hidden; slips Posted (10-05) | Maker | [observed result 2026-10-05 G11-2b; action not seen] |
| Complete | Edit | not offered (no Edit link) | - | [observed 2026-10-05 G11-2b] |
| zero-activity route of a day | (nothing) | stays Incomplete; did not block settling 02112 | - | [observed 2026-10-05 G11-2b] |
| Incomplete, an order due today on the route undelivered | Edit | blocked ("Un-Deliver Order exists for today delivery!", Show details) | Maker | [observed 2026-10-06 G11-3] |
| Incomplete, nothing due today undelivered | Edit, check cash Received, row Save | Complete: "Saved Successfully", green, Edit hidden; slips Posted | Maker | [observed 2026-10-06 G11-3] (supersedes the [inferred] "Edit and save" row above) |
| Incomplete (yellow), the same PJP's previous day not closed | Edit | blocked ("Following previous days not closed! Please close date <date>"); the day cannot be finalized | Maker | [observed 2026-10-01, 2026-10-05]; per-PJP scope [stated 2026-10-06 QA Team Lead] |
| previous day's route of the PJP closed on PJP Daily Inquiry Update (End Of Day + Complete) | (next day) Edit | previous-day check passes | Maker | [stated 2026-10-06 QA Team Lead]; consistent with 10-05 close -> 10-06 settled [observed 2026-10-06 G11-3] |

## 8. Rules and validations
- Total cash/cheque = previous + today [inferred from the column triple; observed 2026-10-01 G11-1 (0 + today = total)].
- Stock shortage (payable and received) tracked separately from cash shortage [db; observed 2026-10-01 G11-1: a separate "Stock Shortage" Collection Type line, 0].
- Sale value counts delivered orders; undelivered counted separately [inferred; observed 2026-10-01 G11-1: Sale Value = sum of the 3 delivered orders].
- Total Order = orders on the route's GIN that are not cancelled; a rescheduled order (Reattempt, off the GIN) is in Total Order but in neither Delivered nor Undelivered [observed 2026-10-01 G11-1].
- **Collection = one line per deposit slip at its allocated amount**; an unallocated remainder of a slip is not collected [observed 2026-10-01 G11-1: 1133 = 600 of 1,000].
- An approved and picked sales return is not shown as Adjusted Credit Note nor Fresh Return before settlement [observed 2026-10-01 G11-1; Q-SR1].
- **Previous days must be closed**: Edit refuses with "Following previous days not closed! Please close date. 2026-09-30" when any earlier working day of the distributor/PJP is open [observed 2026-10-01 G11-1]. The closing process is [unknown] (Q-RS1).
- G11-2: the previous-day check reported the OLDEST open day: 2026-09-30 on 10-01, then 2026-10-01 on the 10-05 morning (09-30 had been closed meanwhile) [observed 2026-10-05 G11-2].
- G11-2b: zero-activity routes (4 on 10-01) stayed Incomplete and did not stop 02112 from being settled; the check presumably applies per route/PJP with activity [observed 2026-10-05 G11-2b; scope inferred, Q-RS4].
- G11-2b: a Complete route cannot be re-edited from this screen (Edit hidden) [observed 2026-10-05 G11-2b]; answers Q49 (class A) for the screen.
- G11-2b: collections against an earlier day's cash memo show under **Previous** (10-05 cheque Previous 1,000 = multi-cheque slip 1140 applied to the 10-01 memo 2003) [inferred, consistent with seq 53]. (2026-10-06: confirmed as intended: an Outstanding Outlet (multi-cheque) amount is auto-adjusted FIFO onto the outlet's oldest open invoice, so it shows as Previous when that invoice is from an earlier day [stated 2026-10-06 QA Team Lead].)
- G11-2b: settlement **posts** the route's deposit slips (Un Posted -> Posted) and trims an unallocated remainder (1139: 1,000 -> 600) [observed 2026-10-05 G11-2b].
- G11-2b: the uncovered Sale Value is not shown as Cash Shortage; it stays as open balance on the memos [observed 2026-10-05 G11-2b].
- G11-2b: an approved, picked sales return is still not shown as Adjusted Credit Note after settlement [observed 2026-10-05 G11-2b; Q-SR1].
- G11-3: **No undelivered order due today**: Edit refuses with "Un-Deliver Order exists for today delivery!" while any order whose delivery date is the settlement date is undelivered on the route; Show details lists it [observed 2026-10-06 G11-3]. On 10-05 the rescheduled order was due the NEXT day, so it did not block; on 10-06 it was due that day and blocked.
- G11-3: allocating the blocking order alone does not clear the error; it cleared only after GIN + GIN approval + Cashmemo Status Delivered [observed 2026-10-06 G11-3].
- G11-3: a delivered but unpaid memo is not a cash shortage (2012, 108,202, Offset 0) and does not block settlement [observed 2026-10-06 G11-3; leaving it unpaid stated 2026-10-06 QA Team Lead].
- G11-3: in edit mode cash Received is editable, cheque Received is fixed (read-only), Stock Shortage Received is editable [observed 2026-10-06 G11-3].
- **Save = reconcile + post + adjust** [stated 2026-10-06 QA Team Lead]: the final settlement reconciles all cash, cheques, DSR cash and stock shortage; on Save the system posts all cash and cheque deposit slips of the route, adjusts the amounts onto the invoices, and fully adjusted invoices disappear from every collection screen (2016, 2020 after 10-06) [observed 2026-10-06 G11-3]. This is why slips are not blocked before settlement (deposit_slips.md, Q-DS2).
- G11-3: preconditions of a settlement together: previous days closed (G11-1/2) and no undelivered order due today on the route [observed 2026-10-06 G11-3; stated 2026-10-06 QA Team Lead].
- **Previous-day check is per PJP** [stated 2026-10-06 QA Team Lead]: the check looks at the previous day's route of the same PJP; the day close on PJP Daily Inquiry Update (End Of Day + Complete) is what clears it. (superseded 2026-10-06: the earlier [inferred] "presumably per route with activity" and "whether the day close clears it is [inferred]" notes.)
- G11-3: return 715 (approved, picked, on GRN 248) again not netted as Adjusted Credit Note / Fresh Return [observed 2026-10-06 G11-3; Q-SR1].

## 9. Messages
None recorded for 00680001 [unknown]. (superseded 2026-10-01:)
- **"Following previous days not closed! Please close date. 2026-09-30"**: popup (button Continue) on Edit when an earlier working day is still open [observed 2026-10-01 G11-1]. The date in the text is the oldest open day.
- Success message of a completed settlement: [unknown] (not reached).
- G11-2: "Following previous days not closed! Please close date. 2026-10-01" (Continue) on Edit, 10-05 morning [observed 2026-10-05 G11-2].
- Success message of a completed settlement: still [unknown] (settled by the QA team member).
- G11-3: **"Un-Deliver Order exists for today delivery!"** (modal Error with Show details / Continue) on Edit when an order due today on the route is undelivered [observed 2026-10-06 G11-3].
- G11-3: **"Saved Successfully"** on the row Save of a settlement [observed 2026-10-06 G11-3] (superseded 2026-10-06: success message no longer [unknown]).

## 10. Dependencies
Reads delivered cash memos (GIN seq 20), sales returns (seq 34-38), deposit slips (seq 39-46). Hands Offset Amount and Received Amount checks to seq 52-54. Keyed by PJP + working date (same-day).
- Confirmed [observed 2026-10-01 G11-1]: reads the GIN's orders (counts), Cashmemo Status (delivered), Cashmemo Reschedule (2006 excluded from both counts), Order Cancellation after GIN (2007 excluded), Order Editing after GIN (2003 at edited Net) and deposit slips (one collection line each).
- **Requires every previous working day to be closed** (day-close process, probably PJP Daily Inquiry Update or a Day Close option [inferred], Q-RS1). On cnr1dev1, 2026-09-30 is still open (stale replay day: GIN 505 Pending, orders 1995-2002) [observed 2026-10-01 G11-1].
- Seq 52-54 depend on a completed settlement [db; not walked 2026-10-01].
- G11-2b: settlement precedes the day close (PJP Daily Inquiry Update, End Of Day / Complete) [observed order 2026-10-05]. Whether the day close is what clears "Following previous days not closed!" for the next day is [inferred] (Q-RS1, detailed procedure pending from the QA lead).
- G11-2b: hands posted slips to Deposit Slip (Posted, Received) and Cheque Status (Clear cheques), Offset Amount to Transaction Inquiry [observed 2026-10-05 G11-2b].
- G11-3: depends on every order due today on the route being delivered: a rescheduled (Reattempt) order due today needs allocation (Order Date = booking date), a new GIN, the Checker's GIN approval and Cashmemo Status Delivered before settlement [stated 2026-10-06 QA Team Lead; observed]. **Order COL26000002018 (rescheduled 10-06 -> 10-07, unallocated) will block the 2026-10-07 settlement of 02112 unless handled the same way.**
- G11-3: followed by DSR Adjustment Amount (seq 56) and the day close (seq 57) [observed 2026-10-06 G11-3].

## 11. Test design hints
- Positive: PJP with full cash delivery; with returns and credit notes; with cheque collection.
- Negative: PJP with no deliveries (all-zero row exists in DB); future date; settle the same PJP twice; entered amount differing from suggested.
- Boundary: received = payable (shortage 0); received 0.01 less.
- Arithmetic cross-checks: total = previous + today; sale - return - adjusted credit note vs collections.
- A green run proves screen values against the workbook, not that the settlement row was persisted.
New from 2026-10-01 G11-1 [observed]:
- **Day-boundary trap for any replay**: settlement needs all earlier working days closed. A cycle run that leaves its day unsettled (as G11-1 did for 2026-10-01) blocks every later day's settlement for that distributor; a replay must either close the day at the end or start from an environment whose previous days are closed. Check this before seq 51 (negative case: settle with an open previous day -> expect the "Following previous days not closed!" popup).
- **Partial allocation**: a slip allocated in part is collected at its allocated amount (1133: 600); expected values must use allocations, not slip amounts.
- **Posting only at settlement**: deposit-slip Status / cash-memo Balance checks (seq 53-54) are meaningful only after a completed settlement.
- **Sale Value vs collected**: an under-collected route (87,107 owed) shows Cash Shortage 0 before settlement; test what settlement does with the shortfall.
- **Return not netted**: Adjusted Credit Note stayed 0 with an approved, picked return; a test expecting the return to reduce payable would fail at this point (Q-SR1).
- **Framework drift**: workbook values built with bank "National Bank of Pakistan" and message "Saved successfully" for multi-cheque no longer match (see deposit_slips.md); expected settlement totals depend on today's slips, not the workbook's.
- Rescheduled order case: in Total Order but neither Delivered nor Undelivered.
- G11-2 / G11-2b additions [observed 2026-10-05 G11-2, G11-2b]:
  - Positive: after settling, assert Route Status Complete (green, no Edit), slips Posted, Received/Offset on the memos = posted allocations, cheques Clear.
  - Positive: an under-collected route settles with Cash Shortage 0; assert the uncovered amount as the memo's open Balance, not as shortage.
  - Negative: a Complete route offers no Edit (cannot be settled twice from the screen).
  - Trap: a route can be Complete while its slips are still Un Posted (10-01); assert slip Status separately (Q-DS3).
  - Trap: Total Order (13 on 10-05) is not explained; do not assert it (Q-RS3).
  - Trap: "Previous" cash/cheque columns fill when money is applied to an earlier day's memo (outlet-level multi-cheque goes to the oldest open memo of the outlet), so expected Previous = 0 is wrong when old memos are open.
  - Trap (replay): the oldest open day blocks every later settlement; check Route Status Complete for all earlier days of the distributor before seq 51.
- G11-3 additions [observed 2026-10-06 G11-3]:
  - Negative: an order due today on the route undelivered (e.g. yesterday's Reattempt) -> Edit gives "Un-Deliver Order exists for today delivery!"; allocation alone does not clear it.
  - Positive: settle = Edit -> cash Received (prefilled) -> row Save -> "Saved Successfully", green, no Edit; header Payable = Received, Cash Shortage 0.
  - Positive: a delivered but unpaid memo leaves Cash Shortage 0 (stays open on the memo).
  - Positive (Q-DS2 ruling [stated 2026-10-06 QA Team Lead]): after Save, every slip of the route is Posted and fully adjusted memos no longer appear on Deposit Slip collection tabs.
  - Boundary candidate (not tried): cash Received below Payable -> expect a Cash Shortage; cheque Received cannot be changed.
  - Trap (replay): a Cashmemo Reschedule at seq 32 creates an order due the next working day; the next day's run must allocate, GIN, approve and deliver it before seq 51.

## 12. Open questions
Q: Payable vs Received Amount exactly? | Default: payable = system-suggested, received = entered | Evidence: rsd suggested/entered columns. (2026-10-01: before settlement Payable = Received per slip line; the entry step was not reached.)
Q: Can a settled PJP/date be reopened? | Default: no | Evidence: none.
Q: How is Offset Amount derived? | Default: credit notes/returns netted against the invoice | Evidence: label only.
Q-RS1: Which process closes a working day (Day Close / PJP Daily Inquiry Update / Generate Opening Balances?), and may 2026-09-30 be closed on cnr1dev1 (it affects other testers' data)? | Default: ask the BA/QA lead before closing anything | Class: C | Evidence: Edit -> "Following previous days not closed! Please close date. 2026-09-30" (2026-10-01 G11-1). **-> PARTLY ANSWERED 2026-10-05**: day close = PJP Daily Inquiry Update, End Of Day + Complete (Current Status E); detailed procedure pending from the QA lead.
Q-DS1: What is deposit-slip "posting" and when does it happen; may a partly allocated slip be posted? | Default: at Route Settlement | Class: B | Evidence: slips 1131-1136 Un Posted; settlement not reached (2026-10-01 G11-1). **-> ANSWERED 2026-10-05**: posting happens at Route Settlement (slips 1137-1142 Posted after route 02112 was settled; partly allocated slip trimmed) [observed 2026-10-05 G11-2b].
Q-SR1: When does an approved sales return reduce the receivable (credit note? settlement?) | Default: at Route Settlement / credit note | Class: B | Evidence: Adjusted Credit Note 0 and Fresh Return 0 with return COL26000000713 (29,077) approved and picked (2026-10-01 G11-1). **-> still open 2026-10-05** (not netted even after the route was settled).
Q-RS2: What does settlement do with Sale Value not covered by collections (87,107 here): cash shortage, carried to the next day, or blocked? | Default: shown as Cash Shortage at settlement | Class: B | Evidence: Cash Shortage 0 before settlement while 87,107 is uncollected (2026-10-01 G11-1). **-> ANSWERED 2026-10-05**: not a cash shortage; the uncovered amount stays as open balance on the memos [observed 2026-10-05 G11-2b].
ANSWERED 2026-10-05 (Q-DS1): posting happens at Route Settlement; a partly allocated slip is posted with its amount trimmed to the allocation [observed 2026-10-05 G11-2b].
ANSWERED 2026-10-05 (Q-RS2): uncovered Sale Value is not a cash shortage; it stays as open balance on the cash memos (Cash Shortage 0, 2009 Balance 88,107) [observed 2026-10-05 G11-2b].
ANSWERED 2026-10-05 (Q49, can a settled PJP/date be reopened): not from this screen (Edit hidden on a Complete row) [observed 2026-10-05 G11-2b].
ANSWERED 2026-10-05 (Q50, Offset Amount): sum of posted deposit-slip allocations on the memo; returns not included [observed 2026-10-05 G11-2b].
Q-RS1 PARTLY ANSWERED 2026-10-05: a working day is closed on PJP Daily Inquiry Update (Mark Status End Of Day + DSR Files Status Complete -> Current Status E); a QA team member closed the earlier un-closed days [stated 2026-10-05 QA lead; observed on the 10-01 row and done live for 10-05]. Open part: the detailed procedure (order of settlement vs close, who may do it on cnr1dev1, whether the close is what clears the previous-day check) promised by the QA lead | Class: C.
Q-SR1 STILL OPEN 2026-10-05: return not netted even after the route is Complete | Class: B.
Q-DS3: Route 02112 for 2026-10-01 is Complete but its slips 1131-1136 are still Un Posted (1133 1,000 / 600): how was 10-01 completed, and does Complete without posting leave the 10-01 receivables open? | Default: Complete does not guarantee posting; assert slip Status separately | Class: B | Evidence: Route Status Complete 10-01 vs Deposit Slip grid [observed 2026-10-05 G11-2b].
Q-RS3: What makes up Total Order 13 for 02112 on 2026-10-05 (10-01: 4)? | Default: unknown; do not assert Total Order | Class: B | Evidence: morning and afternoon reads 2026-10-05 [observed 2026-10-05 G11-2, G11-2b].
Q-RS4: Does the "previous days not closed" check look only at routes with activity (zero-activity routes stayed Incomplete without blocking), per PJP or per distributor? | Default: per route with activity | Class: B | Evidence: 10-01 Incomplete filter 4 routes, 02112 settled anyway [observed 2026-10-05 G11-2b].
Q-RS1 ANSWERED (procedure part) 2026-10-06: settle = Edit on the route row -> check/enter Received on cash lines (cheques fixed) -> row Save ("Saved Successfully", row green, Edit gone = Complete); preconditions: earlier days closed and no undelivered order due today on the route (a Reattempt due today: allocate with Order Date = booking date, new GIN, Checker approval, Cashmemo Status Delivered); order of the day: settlement -> DSR adjustment -> day close [observed 2026-10-06 G11-3, done by Claude; stated 2026-10-06 QA Team Lead]. Still open: whether the day close is what clears "Following previous days not closed!" for the next day (consistent: 10-05 was closed and 10-06 settled without that error) [inferred]. **-> Q-RS1 FULLY ANSWERED 2026-10-06** [stated 2026-10-06 QA Team Lead]: yes, the day close (PJP Daily Inquiry Update: End Of Day + Complete) clears the previous-day check. Route Settlement checks **per PJP**: if that PJP's route of the previous day is not closed it shows "Following previous days not closed! Please close date <date>" and the current day cannot be finalized until it is closed. Grid colour per PJP row: **yellow = route not closed yet; green = route closed**.
Q-RS4 evidence 2026-10-06: the QA Team Lead states the check is per PJP [stated 2026-10-06 QA Team Lead]; consistent with zero-activity routes not blocking 02112. Kept open only for the zero-activity detail | Class: B.
Q-SR1 STILL OPEN 2026-10-06: return 715 not netted at the 10-06 settlement either | Class: B.
Q-RS3 evidence 2026-10-06: Total Order 6 on 10-06 (Delivered 4 incl. 2012 of 10-05; 2017/2019 cancelled, 2018 rescheduled); composition still not explained | Class: B.

## 13. Sources
framework_atlas/flows/00680001, 03210001, 03220001, 03250001; group_11.md; DB snd_tr_rsl_dsr_route_settlem, snd_tr_rsd_dsr_route_setl_dt; snd_menu_outline.md.
- Live walk: `learning_sessions/2026-10-01_G11-PK_session1_log.md` (seq 51) and `learning_sessions/2026-10-01_G11-PK_session1_report.md` (§1, §2, §3 rule 14, §8, §9). Env cnr1dev1, distributor 15108843, route 02112 for 2026-10-01 left unsettled; 2026-09-30 still open.
- G11-2 / G11-2b: learning_sessions/2026-10-05_G11-PK_session2_log.md (seq 51 blocked, 10-05 morning); learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md (seq 51 Complete, 52, 53, 54, 57). Route 02112 for 2026-10-01 and 2026-10-05 settled (Complete) and closed.
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 51 blocked by the undelivered Reattempt 2012, resolved with GIN 509, then settled by Claude; seq 52-57). Route 02112 for 2026-10-06 settled (Complete) and closed (E).
