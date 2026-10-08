---
option: Delivery lifecycle (cash memo from allocation to delivered or returned)
area: delivery_and_returns
doc_types: [CM-01, GN-01, CM-02, GR-01, CRN-02]
screens: [GOOD_ISSUE_NODE, DYL_202053, CASHMEMO-STATUS, DYL_201801, SALESRETURNVIEW, SALESRETURN-STATUSCHANGE]
framework_flows: ["00130001", "00160001", "00050001", "00780001", "02810001", "01040001", "00030001", "00070001", "00700001", "00730001", "00710001", "00090001", "00810001", "02820001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [dispatch_advice, order_booking, stock_allocation, delivery_date_change]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-08
---
# Delivery lifecycle: from allocated order to delivered or returned (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b; consolidated with learning session 1 LEARN-G11-PK/20261001-1611, seq 12-50)
Last updated: 2026-10-01. Source flows: group 11 seq 12-38 (atlas `group_11.md`). Seq 12-50 walked live on 2026-10-01 in one calendar day (seq 15 skipped; seq 51 Route Settlement blocked) [observed 2026-10-01 G11-1].
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.
Updated 2026-10-08: merged the QA team's written answers to the 2026-10-06 review (learning_sessions/2026-10-06_G11-PK_QA_Team_Review.docx); evidence learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx). Tag [stated 2026-10-08 QA Team] = written answer of the QA team. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08: ...)".

## 1. Purpose
Follows one cash memo (order, `CM-01`) from allocation to the end of the delivery day, and shows where stock and documents change. It ties together Goods Issue Note, Cashmemo Reschedule/Status and Sales Return (see their pages).

## 2. Actors and roles
Stock Controller (maker) `Auto_Multi_Orga`; checker `Auto_Tssm` approves GIN (seq 23) and the sales return (37); the DSR (delivery man, PJP `02112-AutomationDSR`) physically delivers [observed/atlas].
- Only two roles act on screen: [Maker] (Auto_Multi_Orga) and [Checker] (Auto_Tssm). Checker approvals in this chain: GIN (23), Sales Return View (37), GRN (49), all with the same Forward button the Maker used to forward [observed 2026-10-01 G11-1]. The DSR has no login in this chain; he is the delivery PJP 02112 (DSR ITB0189-AutomationQADSR) [observed 2026-10-01 G11-1].

## 3. Documents and master data
`CM-01` cash memo, `GN-01` GIN, `CM-02` sales return, `GR-01` Goods Return Note, `CRN-02` credit note [db]. Link tables: GIN refinfo -> cash memo. Stock: `snd_tr_ssb_salestock_balance` by balance date [db].
- Documents of the 2026-10-01 walk: orders COL26000002003-2008, GIN 506, sales return COL26000000713 (own CM-02 series), GRN 246 [observed 2026-10-01 G11-1]. No CRN-02 credit note was seen [observed 2026-10-01 G11-1].
- Two PJPs per route: order booker PJP (02111-AutomationOB1) and delivery PJP (02112-AutomationDSR); the delivery screens all filter by the delivery PJP [observed 2026-10-01 G11-1].

## 4. Inputs: screens and fields
Order of screens: Order Stock Allocation, Delivery Date Change, Goods Issue Note, Stock Inquiry, Cashmemo Reschedule, Cashmemo Status, Sales Return, Sales Return View, Sales Return Status Change. Fields: see the individual pages.
Then (2026-10-01): Deposit Slip (seq 39-46), Goods Return Notes (48-49), Stock Inquiry (50), Route Settlement (51) [observed 2026-10-01 G11-1]. Transaction Inquiry is the screen that shows each cash memo's Document Status, GIN No, Delivery Date and Actual Delivery Date [observed 2026-10-01 G11-1].

## 5. Process: the business steps in order
| Seq | Step | Document effect | Stock effect |
|---|---|---|---|
| 12/18 | Stock Allocation / Unallocation | order Confirmed (exec 02), allocation F/P | reserves stock [db: `tcmm_stock_allocated_status`; reserved columns in stock balance, [inferred]] |
| 19 | Delivery Date Change | delivery date moved (`Delivery Date has been changed successfully, processed orders: 9`) [observed] | none |
| 20 | GIN create + forward | GIN Draft -> Pending [observed]; cash memo Planning completed (03) [inferred] | none yet |
| 23 | GIN approval | GIN Approved; cash memo Ready to dispatch/Packed (13) [inferred] | goods issued out of warehouse [inferred]; needs stock balance of the day [observed] |
| 24 | Stock check after GIN | read-only | In/Out/closing compared [atlas] |
| 29/31 | Order Editing/Cancellation After GIN | edit or cancel an order already issued | [unknown] |
| 32 | Cashmemo Reschedule | status 19 CM Reschedule | [unknown] |
| 33 | Cashmemo Status | Delivered (10) | none [inferred] |
| 34-38 | Sales Return, view, approval, status change | CM-02 created, authorised, Picked | none until GRN [inferred] |
| 48-49 | Goods Return Note (other analyst) | GR-01 | returned goods back into warehouse [inferred] |

Observed 2026-10-01 (supersedes the [inferred]/[unknown] cells above where they differ) [observed 2026-10-01 G11-1]:
| Seq | Step | Document effect | Stock effect |
|---|---|---|---|
| 10 | Order Booking | order Confirmed | **reserves at once**: Allocated up, Closing down (booking auto-allocated; seq 12 was a no-op) |
| 16 | Order Cancellation (before GIN) | Cancelled, no GIN | reservation released (Allocated down, Closing up) |
| 19 | Delivery Date Change | delivery date 10-07 -> 10-01 (`Delivery Date has been changed successfully, processed orders: 5`), still Confirmed | none |
| 20 | GIN create + forward | GIN 506 Draft -> Pending for approval | none |
| 23 | GIN approval (Checker) | cash memos **Ready to dispatch/Packed**, GIN No 506 | **Out = issued, Allocated down by the same, Closing unchanged** |
| 29 | Order Editing After GIN | same number, quantity 7 -> 4 CS, totals recalculated | none |
| 31 | Order Cancellation After GIN | Cancelled, GIN No 506 kept | none |
| 32 | Cashmemo Reschedule | **Reattempt**, new delivery date 10-02, off the GIN | none |
| 33 | Cashmemo Status | **Delivered/Invoiced**, Actual Delivery = save time | none |
| 34-38 | Sales Return, forward, approve, Save Sale Pick | CM-02 COL26000000713, `Success`, picked | none seen |
| 48-49 | Goods Return Note + approval | GRN 246 Suggested 19 CS = 7 cancelled + 7 rescheduled + 3 cut + 2 returned | **In +19 (Sound), Out unchanged, Closing +19** |

Role steps (trace keys):
1. [Maker] Book orders; Change delivery date to today; Create the GIN; Forward. (11:10:00010001, 11:19:00160001, 11:20:00050001)
2. [Checker] Approve the GIN (Forward). (11:23:00780001)
3. [Maker] Check stock after the GIN; Edit / Cancel after the GIN; Reschedule; Mark delivered; Create and forward the sales return. (11:24:02810001, 11:29:00840001, 11:31:00850001, 11:32:01040001, 11:33:00030001, 11:34:00070001, 11:36:00700001)
4. [Checker] Approve the sales return. (11:37:00730001)
5. [Maker] Save Sale Pick; Deposit slips; Create and forward the GRN. (11:38:00710001, 11:48:00090001)
6. [Checker] Approve the GRN. (11:49:00810001)
7. [Maker] Check stock after the GRN. (11:50:02820001)
- G11-3 (2026-10-06) [observed 2026-10-06 G11-3]: GIN 508 (2015, 2016, 2018, 2019, 2020) -> approval -> after-GIN edit 2015 (3 CS), cancel 2019, reschedule 2018 to 10-07 -> Cashmemo Status 2015, 2016, 2020 Delivered -> return 715 on 2015 -> slips -> GRN 248 (17 CS) -> **settlement blocked by the 10-05 Reattempt 2012 due today** -> allocate 2012, GIN 509, approve, Delivered -> settlement Complete -> DSR adjustment -> day close.

## 6. Outputs and effects
At the end of the day the load of each DSR is either delivered (receivable to settle), rescheduled (to another day) or returned (to the warehouse). Daily cycle must run inside one calendar day because stock balances are keyed by date [observed].
- **GRN reconciliation (2026-10-01):** everything that left on the GIN and was not delivered, or was returned, came back on the GRN: 62740537 Suggested **19 CS** = 7 (COL26000002007 cancelled after GIN) + 7 (COL26000002006 rescheduled, Reattempt) + 3 (COL26000002003 cut 7 -> 4 after GIN) + 2 (sales return COL26000000713). The rescheduled order's goods come back too and will be issued again on its new date. GRN approval posted In +19 (Sound): In 164 -> 183, Out stays 35, Allocated 63, Closing 226 -> 245 [observed 2026-10-01 G11-1].
- Stock identity: Closing = Opening + In - Out - Allocated holds through the day [observed 2026-10-01 G11-1].
- Receivable: delivered cash memos carry Balance Amount = Net into the deposit slips; the approved sales return was not netted (Route Settlement Adjusted Credit Note 0) [observed 2026-10-01 G11-1].
- Route Settlement for 02112 on 2026-10-01: Total Order 4 (GIN orders not cancelled), Delivered 3, Undelivered 0 (the rescheduled order is neither), Sale Value 311,238 = the three delivered Nets [observed 2026-10-01 G11-1]. Settlement itself was blocked ("Following previous days not closed! Please close date. 2026-09-30").
- G11-2/2b: the whole chain reproduced on 2026-10-05 with new documents (GIN 507, return 714, GRN 247: 19 CS again) and, for the first time, past settlement: the delivered memos were settled (slips posted, Offset filled), the day was closed on PJP Daily Inquiry Update, and the cash memo with a partial return stayed Delivered/Invoiced [observed 2026-10-05 G11-2, G11-2b].

## 7. Statuses and transitions
Live-verified 2026-10-01 [db + observed]: "Confirmed" is execution status 02 (own status, not Ordered 04); 03 Planning completed is shown for the 8 orders on GIN 505; Transaction Inquiry has one Document Status column that shows the execution status text; codes 04, 06 and 19 do not exist in the execution master of org 010104 (so '19 CM Reschedule' below comes from org 0101 and must be re-read live).
Cash memo execution status chain (CM-01): 01 Ordered -> 02 Confirmed (allocated) -> 03 Planning completed (on GIN) -> 13 Ready to dispatch/Packed (GIN approved) -> 10 Delivered/Invoiced | 18 Partial Delivered | 19 CM Reschedule | 05 Cancelled [db names; order of the chain [inferred]]. Other values: 11 Dispatched, 12 Sent to Locus, 20 CM BLOCKED, 21/22 Auto/Manual Split, 23 Partial Open [db]. Document status: 04 Ordered -> 01 Delivered / 02 Un-Delivered / 03 Cancelled / 05 Amendment / 06 Re-attempt [db]. Completion status (`pdcs`): 01 Completed, 02 DN Pending, 03 Z3 [db], meaning (delivery note to the ERP) [inferred]. In the data (org 0101, Jan 2026) most CM-01 are Delivered (01) with execution 10 or 18 [db].
**Chain observed live 2026-10-01** (Transaction Inquiry Document Status) [observed 2026-10-01 G11-1]: **Confirmed -> Ready to dispatch/Packed (GIN approved) -> Delivered/Invoiced | Reattempt | Cancelled**. "19 CM Reschedule" is shown as **Reattempt** (superseded 2026-10-01: the rescheduled cash memo reads Reattempt, consistent with document status 06 Re-attempt). Planning completed was not seen on GIN 506 between forward and approval (not checked) [unknown]. Partial Delivered was not produced (a cut order still read Delivered/Invoiced) [observed 2026-10-01 G11-1].
TI status table 2026-10-01 [observed 2026-10-01 G11-1]:
| Order | Document Status | Delivery Date | Actual Delivery | GIN |
|---|---|---|---|---|
| COL26000002003 (edited 7 -> 4), 2004, 2005 | Delivered/Invoiced | 2026-10-01 | 2026-10-01 17:54:09 | 506 |
| COL26000002006 | Reattempt (rescheduled) | 2026-10-02 | - | none |
| COL26000002007 | Cancelled (after GIN) | 2026-10-01 | - | 506 kept |
| COL26000002008 | Cancelled (before GIN) | 2026-10-07 | - | - |

- G11-2b: no Partial Delivered (18) after a partial return; the return document reads Picked, Demand Channel "Partial Return" [observed 2026-10-05 G11-2b].

## 8. Rules and validations
- Stock is needed on the day of GIN approval [observed].
- Return quantity cannot exceed ordered quantity [atlas].
- Only cash memos that are allocated and on the PJP/date can be selected into a GIN [inferred from the 9 eligible]. Confirmed: only cash memos of the delivery PJP whose delivery date = the GIN Delivery Date are offered [observed 2026-10-01 G11-1].
- Maker/checker separation on GIN and sales return [observed/atlas].
- After GIN approval, edit, cancel and reschedule do not move stock; the quantities come back only on the GRN [observed 2026-10-01 G11-1].
- Sales Return offers delivered cash memos only; Cashmemo Status offers only cash memos still on the GIN [observed 2026-10-01 G11-1].
- Route Settlement requires every earlier working day to be closed [observed 2026-10-01 G11-1].
- G11-3: **an undelivered order due today on the route blocks Route Settlement** ("Un-Deliver Order exists for today delivery!"); a Reattempt from the previous day is such an order on its new date [observed 2026-10-06 G11-3]. A delivered memo may remain unpaid (not a cash shortage) [stated 2026-10-06 QA Team Lead; observed 2026-10-06 G11-3].
- G11-3: **Zero-tax rule** [stated 2026-10-06 QA Team Lead]: a zero-tax invoice of an outlet that is **NOT tax-exempt cannot be delivered** (the application stops the delivery); a zero-tax invoice of a **tax-exempt** outlet is allowed. Not exercised on 2026-10-06: the zero-tax order of non-exempt outlet 07 (COL26000002017) was cancelled at seq 16 [observed]; the exact blocking screen and message are [unknown]. (refined 2026-10-08: controlled by ORGA parameter ZERO_TAX_ORDER_EXEMPTION, Y = zero-tax delivery allowed, N = not allowed [stated 2026-10-08 QA Team])
- QA team 2026-10-08: stock is added or deducted on document approval (GIN, GRN, SAN, ...) [stated 2026-10-08 QA Team]; editing after the GIN reduces the approved GIN quantity when CASHMEMO_EDIT = Y [stated 2026-10-08 QA Team] (not observed, Q-OE5).

## 9. Messages
See the individual pages. Chain-level: `Delivery Date has been changed successfully, processed orders: 9`; `stock not found.` on Unallocate [observed, ui.md].
- 2026-10-01: `Delivery Date has been changed successfully, processed orders: 5`; Unallocate/Allocation `Process completed successfully` (superseded 2026-10-01: "stock not found." not reproduced); Route Settlement `Following previous days not closed! Please close date. 2026-09-30` [observed 2026-10-01 G11-1].

## 10. Dependencies
Upstream: Dispatch Advice receipt (inbound stock), Order Booking, allocation (order planning). Downstream: Deposit Slip and settlement (seq 39+), Goods Return Note. Data carried: `REPO_GINNO`.
- The whole chain from DA approval to GRN approval must run on one calendar day (stock day rule); a new day means a fresh run from seq 1 [observed 2026-10-01 G11-1].

## 11. Test design hints
End-to-end positive: allocate, GIN, approve, deliver, partial return, GRN; check each status in the DB and the stock balance after each step. Negative: GIN approved on a day with no stock balance; reschedule after delivery; return more than delivered; cancel an order already on an approved GIN. A green group-11 run proves screens and messages, not that statuses and stock totals are right.
- **Reconciliation test:** GRN Suggested = cancelled after GIN + rescheduled + cut after GIN + sales returns (19 CS on 2026-10-01); assert per SKU [observed 2026-10-01 G11-1].
- **Trap, rescheduled goods:** a rescheduled cash memo's goods come back on the GRN; do not expect them to stay with the DSR [observed 2026-10-01 G11-1].
- **Trap, reschedule date first:** on Cashmemo Reschedule set the new Delivery Date before ticking; changing it clears the selection [observed 2026-10-01 G11-1].
- **Trap, receivable:** the sales return is not netted from the receivable nor in Route Settlement (Q-SR1) [observed 2026-10-01 G11-1].
- **Trap, status chain:** assert Confirmed -> Ready to dispatch/Packed -> Delivered/Invoiced | Reattempt | Cancelled as shown in Transaction Inquiry; "CM Reschedule" and "Partial Delivered" were not shown [observed 2026-10-01 G11-1].
- **Trap, stock timing:** booking reserves (Closing down), GIN approval moves Allocated to Out (Closing unchanged), GRN approval adds In (Closing up); a check of Out alone misses most of it [observed 2026-10-01 G11-1].
- Negative (2026-10-06): deliver a zero-tax invoice of a non-exempt outlet -> blocked [stated 2026-10-06 QA Team Lead]; message not yet observed.

## 12. Open questions (batched for the BA; each with a default)
Q: Exact stock effect of each step (reserve at allocation, issue at GIN approval, return at GRN)? | Default: as in the table | Evidence: only names and one error message. ANSWERED 2026-10-01: reserve at booking, Allocated -> Out at GIN approval, In at GRN approval (see §5 observed table) [observed 2026-10-01 G11-1].
Q: Is Cashmemo Status the step that makes the cash memo Delivered/Invoiced? | Default: yes | Evidence: names. ANSWERED 2026-10-01: yes [observed 2026-10-01 G11-1].
Q: Does a delivered cash memo with a return become Partial Delivered (18)? | Default: yes | Evidence: status exists. Still open 2026-10-01: the cut order (7 -> 4) read Delivered/Invoiced, not Partial Delivered; the status after its sales return was not re-read | Class: B.
Q: Is the Unallocate failure `stock not found.` a defect or by design? | Default: environment issue | Evidence: ui.md, cause unknown. PARTLY 2026-10-01: not reproduced on a same-day run ("Process completed successfully"); stale-day effect likely [observed 2026-10-01 G11-1].
Q-SR1: When does an approved sales return reduce the receivable (credit note? settlement?) | Default: at Route Settlement / credit note | Class: B | Evidence: Adjusted Credit Note 0 in Route Settlement 2026-10-01. **-> still open 2026-10-05** (not netted even after the route was settled).
Q-RS1: How is a working day closed (which screen), and may 2026-09-30 be closed on cnr1dev1? | Default: ask the BA before closing | Class: C | Evidence: Route Settlement blocked 2026-10-01. **-> PARTLY ANSWERED 2026-10-05**: day close = PJP Daily Inquiry Update, End Of Day + Complete (Current Status E); detailed procedure pending from the QA lead.
Q-DS1: What is deposit-slip "posting" and when does it happen? | Default: at Route Settlement | Class: B | Evidence: all slips Un Posted 2026-10-01. **-> ANSWERED 2026-10-05**: posting happens at Route Settlement (slips 1137-1142 Posted after route 02112 was settled; partly allocated slip trimmed) [observed 2026-10-05 G11-2b].
- ANSWERED 2026-10-05 (Q33, Partial Delivered after a return): no; COL26000002009 stayed Delivered/Invoiced after return 714 was picked [observed 2026-10-05 G11-2b].
- Q-DS1 ANSWERED 2026-10-05: posting happens at Route Settlement (slips 1137-1142 Un Posted -> Posted once route 02112 for 10-05 was settled) [observed 2026-10-05 G11-2b]. Q-RS1 PARTLY answered (day close = PJP Daily Inquiry Update End Of Day / Complete). Q-SR1 still open.
- G11-3: no new delivery-lifecycle question; the carry-over of Reattempt orders between days is now a stated procedure (see cashmemo_reschedule_and_status.md).

## 13. Sources
`framework_atlas/group_11.md`, flows `00130001`, `00160001`, `00050001`, `00780001`, `02810001`, `01040001`, `00030001`, `00070001`, `00700001`, `00730001`, `00710001`; `apps/snd/knowledge/ui.md`; `framework_flows/STEP_SHEET_DRAFT_next.md`; DB: glb_pr_exs_execution_status, snd_pr_dos_documentstatus, snd_pr_dcs_doc_cmpltn_status, snd_tr_cmm_cashmemo_master, snd_tr_gnm_gingrn_master.
Learning session 1 (2026-10-01): `learning_sessions/2026-10-01_G11-PK_session1_log.md` seq 10, 16, 18, 19, 20, 23, 24, Transaction Inquiry checks, seq 29-38, 46, 48-51; `learning_sessions/2026-10-01_G11-PK_session1_report.md` §3 rules 3-7, 10, 12, 14, §8.
- G11-2 / G11-2b: learning_sessions/2026-10-05_G11-PK_session2_log.md, learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md.
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 20-38, 48, 51).

- QA team written answers 2026-10-08: learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx) (rules 3, 9; Q58).
