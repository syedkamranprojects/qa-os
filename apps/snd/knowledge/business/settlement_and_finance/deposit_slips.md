---
option: Deposit Slip
area: settlement_and_finance
doc_types: [deposit slip (serial, e.g. 1131)]
screens: [DYL_201802]
framework_flows: ["03230001", "03240001", "03260001", "00140001", "00140004", "00140005"]
markets: [PK]
roles: [Maker]
depends_on: [goods_issue_note, cashmemo_reschedule_and_status, sales_return]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-01
---

# Deposit slips: banking the cash and cheques collected (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]** seen live, **[db]** declared by the application DB or framework tables, **[inferred]** concluded by Claude, **[unknown]** not determinable yet. Rules: `docs/LEARNING_STANDARD.md` §3.
Last updated: 2026-10-01 (consolidated with learning session G11-1, seq 39-46). Source flows: 03230001 (seq 39), 03240001 (40), 03260001 (41), 00140001 (42), 00140004 (44), 00140005 (46); related 03220001 (53), 03250001 (54). ~~No live replay of any exists~~ (superseded 2026-10-01: all six walked live in G11-1 on cnr1dev1, slips 1131-1136). The DB holds no 010104 deposit-slip rows (4 rows, all org 0101) [db, before the walk].

## 1. Purpose
A deposit slip records the money a DSR (salesman, identified by his daily PJP) hands in after delivering: how much of the cash and/or cheques collected on cash memos (invoices) is being banked. It ties collected money to specific cash memos so each outlet's receivable is reduced [inferred from table links: slip detail -> snd_tr_cmm_cashmemo_master]. It follows GIN/delivery and sales return and precedes Route Settlement (seq 51), which reconciles the day's collection per PJP. [inferred; order confirmed observed 2026-10-01 G11-1: slips made after Cashmemo Status (delivered) and Sales Return pick, and each slip appears as a collection line in Route Settlement]
- The slip is a header (PJP-DSR, Cash or Cheque, bank, amount) plus allocations of that amount to the DSR's delivered cash memos, either per cash memo or per outlet (multi-cheque) [observed 2026-10-01 G11-1].
- Receivable balances do not move when a slip is saved or allocated; they move at "posting", which has not been seen yet and is presumed to happen at Route Settlement [observed 2026-10-01 G11-1 for "no movement"; posting moment inferred, Q-DS1].

## 2. Actors and roles
Maker Auto_Multi_Orga on all six flows (same session, no user switch) [db: group 11; observed 2026-10-01 G11-1, segment 7]. An approval row "Deposit Slip Approval" (00140002) exists but is inactive (seq 43/45/47) [db], so no approval step is exercised; whether slips need approval is [unknown].
- The screen shows Forward and Reject buttons next to Add/Save/Update/Delete/Save All [observed 2026-10-01 G11-1]; they were not clicked, so a maker-checker path may exist on screen even though group 11 does not use it [inferred].
- Checker behaviour on this screen not walked [unknown].

## 3. Documents and master data
- Header `snd_tr_dsl_deposit_slip`: org, entity type, distributor code, serial `tdsl_deposit_slip_srno` (auto-generated, shown as "Deposit Slip"). Holds PJP daily number, instrument type, bank, branch, amount, date, status (default `I`) [db]. Serial is a plain running number per distributor: 1128-1130 existed, today 1131-1136 [observed 2026-10-01 G11-1].
- Detail `snd_tr_dsd_deposit_slip_dtl`: one row per cash memo: document type, cash memo number (`tcmm_docno`), amount, cheque no/date, bank, instrument status and its date [db].
- Master data: payment modes for 010104: 01 Cash (default), 02 Cheque, 05 Mobile Money Transfer, 06 Credit Note active; 03 Credit Card, 04 Bank Transfer inactive [db]; banks and branches (glb_pr_bnb_bankbranch); instrument statuses (see cheque_status.md). The Type list on screen offered Cash / Cheque [observed 2026-10-01 G11-1].
- **Bank master is polluted** on cnr1dev1: real banks plus "test", "99", "32", "demo", "asd", an empty entry, "tes", "SBK", "DIST BANK", "PK BANK", "test feroz", "Test Bank 891724/951327/198290", "Bank tdm", "SAMBHA bANK", "HB Bank", "First Women Bank Limited 1", and "National Bank of Pakistanss" [observed 2026-10-01 G11-1].
- **"National Bank of Pakistan" (the workbook value) no longer exists**; only "National Bank of Pakistanss" is offered (framework value drift) [observed 2026-10-01 G11-1].
- Bank Branch fills itself when the bank has one branch (Bank Al-Habib Limited -> DHA Branch) [observed 2026-10-01 G11-1].
- Upstream: a delivered cash memo with open balance (REPO_GINNO from seq 20) [db; observed 2026-10-01 G11-1: only cash memos in status Delivered/Invoiced for the DSR were listed (2003, 2004, 2005)].

## 4. Inputs: screens and fields
Menu: Transaction > Receivable > Deposit Slip (`DYL_201802`) [db; observed 2026-10-01 G11-1, layout 201802; a direct URL redirects to the menu]. Header screen plus a child tab listing cash memos.
- Header: Deposit Slip (read-only, generated), **PJP-DSR*** (list PJPDD), Date (read-only), **Type*** (list PPYM, "Instrument Type (Cash/Cheque)"), Status (default I), Bank, Bank Branch, **Deposit Amount*** (regex rejects 0 and non-numeric: `^(?!0+(\.0+)?$)\d+(\.\d+)?$`) [db].
  - Status is shown as "Un Posted" (read-only) on screen [observed 2026-10-01 G11-1] (the DB code `I` [db] is presumably "Un Posted" [inferred]).
  - **Defaults on first opening**: the screen opens on a NEW slip with **PJP-DSR preset to the booking PJP "02111 - AutomationOB1"** and **Bank preset "demo"** [observed 2026-10-01 G11-1]. The PJP-DSR list has all 13 PJPs (booking and delivery) [observed 2026-10-01 G11-1].
  - **PJP-DSR trap**: the slip must be made for the **delivery** DSR (02112 - AutomationDSR); with the preset booking PJP the DSR's delivered cash memos are not the ones offered [observed 2026-10-01 G11-1].
  - **Add gives a BLANK form**: no PJP-DSR and no "demo" bank; those defaults appear only on first opening of the screen [observed 2026-10-01 G11-1].
- Buttons: Add, Save, Update, Delete, Forward, Reject, Save All [observed 2026-10-01 G11-1]. Earlier list: Refresh, New, Save, Update, Delete [db].
- Upper grid (slips): Deposit Slip, PJP-DSR, Deposit Date, Type, Bank, Bank Branch, Status, Deposit Amount, Adjusted Amount [observed 2026-10-01 G11-1].
- Cash-memo area (after the header is saved) has **three tabs** [observed 2026-10-01 G11-1]:
  1. **Outstanding Cash memos** (one row per delivered cash memo of the DSR): PJP, Document No, Document Type (Sales), Outlet Code, Outlet Desc, GIN, Cheque No., Cheque Date, Bank_Name, Net Amount, Received Amount, Balance, Un Posted Amount, **Deposit-Amount** (editable). Cheque Date here takes yyyy-mm-dd.
  2. **Outstanding Outlet** (one row per outlet): Outlet Code, Outlet Desc, Net, Received, Balance, Un Posted, Deposit Amount, Action "+". Tick the outlet, then "+" opens the popup **"Cheque Details"** (grid Cheque. No., Cheque Date, Bank, Net Amount; add-row icon; row Save/Cancel; "Save Changes"; close x). The "+" may need scrolling into view.
  3. **Deposit Slip Detail**.
- Cash-memo tab fields used by flows: Deposit Amount, Cheque No, Cheque Date, Bank_Name; grid columns Serial No, Document Type, Order Number, Deposit Amount, Currency, Organization, Cheque No, Cheque Date, Cheque Status, Cheque Status Date, Invoice Number, Remarks [db].
- **Date-format trap**: in the "Cheque Details" popup the Cheque Date must be typed **MM/DD/YYYY** ("10/01/2026"); typing 2026-10-01 shows the text but leaves the value empty, and row Save answers "Fill all the values!". The Outstanding Cash memos grid accepts yyyy-mm-dd [observed 2026-10-01 G11-1].
- Picking uses a filter then a GIN row (`filter_2`, `row_1_gin`) and "save all" (`saveallBtn`) [db: atlas events].
- Variants: 03230001 Full Amount Cash; 03240001 Full Amount Cheque (adds Bank, Bank Branch, Cheque No/Date); 03260001 Unposted (then screen "Deposit slip Val Unposted" reads **Un Posted Amount**); 00140001 Multi Cheques (screen "Deposit Slip,Outlet": Cheque. No, Cheque Date, Bank, Net Amount, cash-memo selection grid, popup); 00140004 Cheque; 00140005 Cash [db; all six walked 2026-10-01 G11-1, see section 5].

## 5. Process
Framework view [db]:
1. [Maker] Open Deposit Slip, click New (`addBtn`). trace 11:39..46
2. [Maker] Select PJP-DSR, Type (Cash/Cheque), Deposit Amount (+ Bank/Branch for cheque); Save; assert toast from sheet DEPOSIT_SAVE_ASSR. The slip number is read from the first grid row (`row_1_deposit_slip`) into REPO_Deposit_Slip. [db]
3. [Maker] In the cash-memo tab filter, pick the GIN/cash memo (REPO_GINNO), enter Deposit Amount (plus Cheque No, Date, Bank for cheque), Save all. [db]
4. [Maker] (03260001) read Un Posted Amount and compare with expected. [db]
5. After Route Settlement: 03220001 reopens the slip and reads **Received Amount**; 03250001 reopens slips after an order was removed and walks the cash and cheque tabs (flow-control only, no assertion). [db]

Observed business steps (2026-10-01 G11-1) [observed]:
1. [Maker] Open Transaction > Receivable > Deposit Slip. trace 11:39:03230001
2. [Maker] Change PJP-DSR to the delivery DSR "02112 - AutomationDSR", select Type "Cash", enter Deposit Amount 101161, Save -> "Saved successfully" (slip 1131, Un Posted). trace 11:39:03230001
3. [Maker] On Outstanding Cash memos enter Deposit-Amount 101161 on COL26000002004, Save All -> "Record saved successfully!". trace 11:39:03230001
4. [Maker] Add a slip with PJP-DSR 02112, Type "Cheque", Bank "Bank Al-Habib Limited" (Bank Branch "DHA Branch" fills itself), Deposit Amount 119370, Save -> "Saved successfully" (slip 1132). trace 11:40:03240001
5. [Maker] On Outstanding Cash memos enter Cheque No. 1234501, Cheque Date 2026-10-01, Bank_Name "National Bank of Pakistanss", Deposit-Amount 119370 on COL26000002005, Save All -> "Record saved successfully!". trace 11:40:03240001
6. [Maker] Add a slip 02112 / Cash / 1000, Save -> "Saved successfully" (slip 1133); verify Un Posted Amount on the other cash memos; enter Deposit-Amount 600 on COL26000002003 (deliberately partial), Save All -> "Record saved successfully!". trace 11:41:03260001
7. [Maker] Add a slip 02112 / Cheque / Bank Al-Habib Limited / 1000, Save -> "Saved successfully" (slip 1134). trace 11:42:00140001
8. [Maker] Open the Outstanding Outlet tab, tick outlet 1000000004, click "+", add four rows in "Cheque Details" (12444 / 200, 22337 / 300, 12222 / 400, 1234567 / 100, date 10/01/2026, bank National Bank of Pakistanss), Save Changes, Save All -> "Payment Adjusted Successfully". trace 11:42:00140001
9. [Maker] Add a slip 02112 / Cheque / Bank Al-Habib Limited / 1000 (slip 1135); on Outstanding Cash memos enter Cheque No. 1234567, Cheque Date 2026-10-01, Bank_Name National Bank of Pakistanss, Deposit-Amount 1000 on COL26000002003, Save All -> "Record saved successfully!". trace 11:44:00140004
10. [Maker] Add a slip 02112 / Cash / 1000, Save -> "Saved successfully" (slip 1136); enter Deposit-Amount 1000 on COL26000002003, Save All -> "Record saved successfully!". trace 11:46:00140005
11. [Maker] Reload the screen and verify Adjusted Amount per slip (Adjusted refreshes only on reload). trace 11:46:00140005

## 6. Outputs and effects
A slip with detail rows per cash memo; header status starts `I`; a DB sample shows status `A` with a posting date once complete [db, org 0101]. `snd_tr_cmm_cashmemo_payment` references the slip [db].
- ~~"Unposted" = slip money not yet allocated to cash memos [inferred]~~ (superseded 2026-10-01: on a **cash memo**, "Un Posted Amount" = the amount already allocated to it on OTHER slips that are not yet posted; the open slip's own allocation is not counted [observed 2026-10-01 G11-1]. E.g. 2003 Un Posted went 600 -> 1,600 -> 2,600 as slips 1133, 1134, 1135 allocated to it.)
- **Allocation does not change Received or Balance** on the cash memo: after slip 1131 allocated 101,161 to COL26000002004, the grid still showed Received 0 / Balance 101,161 [observed 2026-10-01 G11-1]. Balances change only at posting [inferred; Q-DS1].
- **The approved and picked sales return (29,077) did NOT reduce COL26000002003's receivable**: Net/Balance stayed 90,707 [observed 2026-10-01 G11-1; Q-SR1].
- **All six slips stayed "Un Posted"** after allocation; older slips 1128-1130 show "Posted" [observed 2026-10-01 G11-1]. Posting presumably happens at Route Settlement [inferred; not reached, seq 51 blocked].
- **Adjusted Amount** on the slip = amount allocated from it. Partial allocations do fill it (1133: Adjusted 600 of 1,000) [observed 2026-10-01 G11-1]. (superseded 2026-10-01, same session: the seq-41 note "Adjusted stays 0 for a partly allocated slip, filled only when fully allocated" was a stale grid; Adjusted refreshes only when the screen is reloaded.)
- Slips of the day [observed 2026-10-01 G11-1]:

| Slip | Type | Amount | Adjusted | Cash memo |
|---|---|---|---|---|
| 1131 | Cash | 101,161 | 101,161 | 2004 |
| 1132 | Cheque (Al-Habib/DHA, chq 1234501) | 119,370 | 119,370 | 2005 |
| 1133 | Cash | 1,000 | 600 | 2003 |
| 1134 | Cheque x4 (12444/200, 22337/300, 12222/400, 1234567/100) | 1,000 | 1,000 | outlet 04 (2003) |
| 1135 | Cheque (chq 1234567) | 1,000 | 1,000 | 2003 |
| 1136 | Cash | 1,000 | 1,000 after reload | 2003 |

- How to check: reopen the screen (reload), read Status and Adjusted Amount per slip in the upper grid; read Net / Received / Balance / Un Posted per cash memo in the Outstanding Cash memos tab; at Route Settlement each slip appears as one Collection Type line (see route_settlement.md) [observed 2026-10-01 G11-1].

## 7. Statuses and transitions
| from | action | to | by | tag |
|---|---|---|---|---|
| (new) | Save header | `I` | Maker | [db] default I |
| (new) | Save header | "Un Posted" (screen label) | Maker | [observed 2026-10-01 G11-1] |
| `I` | Save all with cash memos | `A` + posting date | Maker/process | [db] sample, trigger [unknown] (superseded 2026-10-01: Save All with full allocation left slips 1131/1132 "Un Posted"; Save All does not post) |
| "Un Posted" | Save All (any allocation, full or partial) | "Un Posted" (Adjusted Amount filled) | Maker | [observed 2026-10-01 G11-1] |
| "Un Posted" | Route Settlement (presumed) | "Posted" | Maker/process | [inferred; older slips 1128-1130 are Posted; Q-DS1] |
| detail row | Cheque Status update | P/L/R/B/C/A | Maker | [db] see cheque_status.md |

## 8. Rules and validations
- PJP-DSR, Type, Deposit Amount mandatory; amount > 0 numeric [db].
- Historic toasts in the atlas (other markets): "Balance should be greater than deposit amount at Doc no. ITB000003747" (deposit above the cash memo balance [inferred]), "Required Fields are empty!", "Invalid transaction attempt", "Do not use Special charters." [db: 00140004/00140001].
- A cash memo must be delivered (GIN) before deposit [inferred; observed 2026-10-01 G11-1: only Delivered/Invoiced cash memos of the DSR were offered].
- A slip may be allocated **partially** (1,000 slip, 600 allocated) and saved without warning [observed 2026-10-01 G11-1]. Whether a partly allocated slip may be posted is [unknown] (Q-DS1).
- **Duplicate cheque number accepted**: cheque 1234567 used on slip 1134 (multi-cheque) and on slip 1135 (single) for the same outlet, no duplicate check [observed 2026-10-01 G11-1; the workbook also uses it twice]. Defect candidate.
- **Double-allocation risk**: because Balance only changes at posting, a cash memo already fully allocated on one slip (2004 on 1131) is still offered with its full Balance on the next slip; a second slip can apparently allocate it again. The system only shows the other allocations in "Un Posted Amount" [observed 2026-10-01 G11-1 for the display; the second allocation itself was not tried].
- In the "Cheque Details" popup every column is required; an empty value (including a date typed in the wrong format) gives "Fill all the values!" [observed 2026-10-01 G11-1].
- Can one slip mix cash and cheque? One Type per header; the multi-cheque popup holds several cheques under one Cheque slip [observed 2026-10-01 G11-1]; mixing not tried.

## 9. Messages
"Saved successfully" and "Record saved successfully!" on save; others as in section 8 [db: atlas toast history, not PK-specific]. Confirmed and refined [observed 2026-10-01 G11-1]:
- **"Saved successfully"**: header Save of a new slip.
- **"Record saved successfully!"**: Save All after allocating on the Outstanding Cash memos tab.
- **"Payment Adjusted Successfully"**: Save All after a multi-cheque allocation on the Outstanding Outlet tab (framework sheet "Deposit Slip,Outlet" expects "Saved successfully": message drift).
- **"Fill all the values!"**: row Save in the "Cheque Details" popup with an empty column (e.g. Cheque Date typed yyyy-mm-dd).

## 10. Dependencies
Reads REPO_GINNO (seq 20; 00140001 reads nothing, selects by outlet). Writes REPO_Deposit_Slip (no later row in group 11 consumes it [db]). Hands cash/cheque amounts to Route Settlement [inferred; observed 2026-10-01 G11-1: Route Settlement lists each slip as one Collection Type line with its allocated amount]. Slips are dated (`tdsl_deposit_slip_date`): same-day cycle [inferred].
- Needs cash memos in status Delivered/Invoiced for the delivery DSR (Cashmemo Status, seq 33) [observed 2026-10-01 G11-1].
- Slip-by-slip `Un Posted Amount` depends on the earlier slips of the same day (order of seq 39 -> 46 matters for expected values) [observed 2026-10-01 G11-1].
- Posting (and therefore Received/Balance change) depends on Route Settlement, which needs every previous working day closed [observed 2026-10-01 G11-1: settlement blocked; see route_settlement.md].

## 11. Test design hints
- Positive: full cash, full cheque, multi-cheque across outlets, partial (unposted) then complete.
- Negative: amount 0, negative, text, special characters; empty PJP; cheque without Bank/Cheque No; amount above balance; same cash memo twice; cash memo of another PJP.
- Boundary: amount = balance; balance - 0.01; two decimals.
- A green run does not prove posted/unposted arithmetic or cash-memo balance reduction: only the save toast is asserted; seq 54 has no assertion at all.
New from 2026-10-01 G11-1 [observed]:
- **Partial allocation**: slip 1,000, allocate 600; expect Adjusted 600 after reload, the remaining 400 unallocated, slip still Un Posted. Then check how Route Settlement counts it (it showed 600, not 1,000).
- **Posting happens only at settlement**: right after Save All, expect Status "Un Posted" and Received/Balance unchanged; asserting a reduced Balance at seq 39-46 would fail. Assert "Un Posted Amount" on the next slip instead.
- **Adjusted refreshes only on reload**: read Adjusted after reopening the screen, or a correct partial allocation looks like 0.
- **PJP-DSR default trap**: the first opening presets the booking PJP 02111 and bank "demo"; a replay that does not set PJP-DSR explicitly works on the wrong PJP. Add gives a blank form (no defaults), so behaviour differs between the first slip and later ones.
- **Date-format trap**: Cheque Date MM/DD/YYYY in the multi-cheque popup, yyyy-mm-dd on the cash-memo grid.
- **Double allocation** (negative): allocate the same cash memo in full on two slips; expected a rejection (e.g. "Balance should be greater than deposit amount..."); current behaviour suggests it may be accepted.
- **Duplicate cheque number** (negative): same cheque no for the same outlet on two slips is accepted today; raise with the BA before asserting either way.
- **Framework drift**: bank "National Bank of Pakistan" no longer exists (use "National Bank of Pakistanss" or a clean bank); multi-cheque message is "Payment Adjusted Successfully", not "Saved successfully"; the multi-cheque "+" is on the Outstanding Outlet tab (needs a tab switch).
- Day boundary: Un Posted figures depend on all slips made earlier the same day for the DSR; a re-run on the same day sees the previous run's slips.

## 12. Open questions
Q: Does a deposit slip need checker approval? | Default: no | Evidence: 00140002 inactive. (2026-10-01: Forward/Reject buttons are on the screen but unused in group 11.)
Q: What flips status I to A? | Default: ~~Save all with full amount~~ Route Settlement (superseded 2026-10-01: Save All with full amount left 1131/1132 "Un Posted") | Evidence: sample rows only, org 0101; G11-1 slips all Un Posted. See Q-DS1.
Q: Exact meaning of "Unposted Amount"? | ANSWERED 2026-10-01 [observed G11-1]: on a cash memo, the amount allocated to it on other not-yet-posted slips (old default "slip amount minus amount allocated to cash memos" superseded).
Q: Can a slip mix cash and cheque? | Default: no, one Type per slip | Evidence: single Type field; not tried 2026-10-01.
Q-DS1: What is deposit-slip "posting" (who, when: Route Settlement? Forward?), and may a partly allocated slip be posted? | Default: posting happens at Route Settlement | Class: B | Evidence: slips 1131-1136 all Un Posted after Save All; older 1128-1130 Posted; settlement blocked at seq 51 (2026-10-01 G11-1).
Q-RS1: How is a working day closed, and may 2026-09-30 be closed on cnr1dev1? | Default: ask BA before closing | Class: C | Evidence: Route Settlement blocked, so posting could not be observed (see route_settlement.md).
Q-SR1: When does an approved sales return reduce the receivable (credit note? settlement?) | Default: at Route Settlement / credit note | Class: B | Evidence: COL26000002003 Balance stayed 90,707 after return COL26000000713 (29,077) was approved and picked (2026-10-01 G11-1).
Q-DS2: Is a duplicate cheque number for the same outlet allowed, and should a cash memo already fully allocated on an unposted slip be blocked on another slip? | Default: both should be blocked (treat current acceptance as a defect candidate) | Class: C | Evidence: cheque 1234567 on 1134 and 1135 accepted; 2004 still offered with full Balance after slip 1131 (2026-10-01 G11-1).

## 13. Sources
framework_atlas/flows/03230001, 03240001, 03260001, 00140001, 00140004, 00140005, 03220001, 03250001 (.md/.json); framework_atlas/group_11.md; screens_db/DYL_201802.json; DB snd_tr_dsl_deposit_slip, snd_tr_dsd_deposit_slip_dtl, glb_pr_pym_paymentmode, snd_tr_cmm_cashmemo_payment.
- Live walk: `learning_sessions/2026-10-01_G11-PK_session1_log.md` (seq 39, 40, 41, 42, 44, 46 and the "Deposit slips today" table) and `learning_sessions/2026-10-01_G11-PK_session1_report.md` (§3 rule 13, §6, §7, §8). Env cnr1dev1, distributor 15108843, slips 1131-1136 left Un Posted.
