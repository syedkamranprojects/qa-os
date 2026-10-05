# Coverage report: S&D group 11 (PK), after learning sessions G11-1, G11-2 and G11-2b

Standard: `docs/LEARNING_STANDARD.md` §7. Date 2026-10-05. Env cnr1dev1, Unilever Pakistan Limited, distributor 15108843 IBRAHIM TRADERS. Maker Auto_Multi_Orga, Checker Auto_Tssm.
Sessions covered: G11-1 (2026-10-01, seq 1-50, consolidated 2026-10-01), **G11-2** (2026-10-05 morning, seq 1-50 again) and **G11-2b** (2026-10-05 afternoon, seq 51-71), both consolidated into the business pages on 2026-10-05.
This report gives the facts for the QA lead's G0 decision. **No area is marked `learned` here; G0 is the QA lead's sign-off.**

## 1. How the numbers were counted
- **Pages**: the L3 option pages of each area folder (READMEs excluded). Template check = the 13 numbered sections present; front-matter present.
- **Definition of done (§3.1, L3)**: (a) 13 sections; (b) no live `[unknown]` in sections 1, 2, 5, 6, 7 (an `[unknown]` that the same line or the next line marks as superseded / upgraded does not count); (c) section 9 has an observed message for every save, forward or approve action executed in the walks. Checked by a script (section presence, tag tokens per section) plus a manual read of every remaining `[unknown]` hit.
- **Share of facts by tag**: occurrences of the tag tokens `[observed` / `[stated` / `[db` (+ `[atlas`) / `[inferred` / `[unknown` in the area's L3 pages. Approximate: one fact can carry several tags, superseded text still counts, and one `[stated` per page (the provenance note of 2026-10-05) is subtracted.
- **Open questions**: from [../OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md) after the 2026-10-05 renumbering, each assigned to the area of its page.

## 2. Per area

### 2.1 Options and definition of done

| Area | Options in scope (group 11) | With an L3 page | 13 sections + front-matter | Meet L3 DoD | Pages failing DoD and why |
|---|---|---|---|---|---|
| inbound_stock | 5 (DA, DA loss, Stock Inquiry, stock validations, GRN) | 5 | 5 / 5 | **4 / 5** | da_loss_approval.md §6: where an approved loss goes outside stock (claims) is [unknown] (Q-LA1) |
| order_to_delivery_planning | 6 (lifecycle, booking, allocation, Transaction Inquiry, editing/cancellation, delivery date change) | 6 | 6 / 6 | **6 / 6** | - (seq 15 path not walkable as automated; page records it) |
| delivery_and_returns | 4 (GIN, reschedule/status, sales return, delivery lifecycle) | 4 | 4 / 4 | **1 / 4** | goods_issue_note.md §7 actor of GIN Cancel [unknown]; sales_return.md §6 CRN-02 trigger [unknown], §7 Cancel actor [unknown]; delivery_lifecycle.md §7 Planning completed between Forward and approval not checked [unknown] |
| settlement_and_finance | 7 (deposit slips, route settlement, cheque status, DSR adjustment, PJP daily update / day close, OTC stock out SAN, end-of-day validations) | 7 | 7 / 7 (front-matter added 2026-10-05 to 5 pages) | **1 / 7** | deposit_slips.md §2 approval need / Checker behaviour [unknown] (BA10); route_settlement.md §2 Checker [unknown] and the settlement action itself not observed (done by a QA team member); cheque_status.md §7 allowed transitions [unknown] (BA11); dsr_adjustment.md §6/§7 effect and status on save [unknown] (nothing saved); pjp_daily_inquiry_update.md §6 effect on mobile sync [unknown]; otc_stock_out_and_san.md §6 stock after Forward / finance posting [unknown] and §9 no message recorded for the detail-row save |
| **Total** | **22** | **22** | **22 / 22** | **12 / 22** | |

L1 (INDEX, glossary): every area named, every document type in the document map with creator, approver, status chain and effect (some still tagged [db]/[inferred]); roles listed (Maker / Checker with users). L2 (INDEX §1): the Daily Cycle chain now has observed evidence for every step from DA to day close and SAN, with role switches and the day rules (first movement opens the day; settlement needs every earlier day closed). L4 is the app-cartographer's job and was not assessed here.

### 2.2 Share of facts by tag (approximate token counts, see §1)

| Area | observed | stated | db / atlas | inferred | unknown | Total tokens |
|---|---|---|---|---|---|---|
| inbound_stock | 319 (81%) | 0 (0%) | 44 (11%) | 21 (5%) | 10 (3%) | 394 |
| order_to_delivery_planning | 386 (76%) | 1 (0.2%) | 46 (9%) | 48 (9%) | 27 (5%) | 508 |
| delivery_and_returns | 262 (64%) | 2 (0.5%) | 85 (21%) | 43 (10%) | 20 (5%) | 412 |
| settlement_and_finance | 203 (51%) | 10 (2.5%) | 95 (24%) | 53 (13%) | 37 (9%) | 398 |

The settlement area moved most this session (five pages had no live evidence before 2026-10-05).

### 2.3 Open questions by class, and closed this consolidation

| Area | Open A | Open B | Open C | Closed 2026-10-05 |
|---|---|---|---|---|
| inbound_stock | 8 (Q03, Q09, Q12, Q13, Q14, Q15, Q-DA2, Q-LA3) | 5 (Q-OB2, Q02, Q-GRN1, Q-GRN2, Q-LA2) | 4 (BA14, Q-DA3, Q-LA1, Q-SV1) | Q-OB1, Q08, Q31, BA7 (+ BA3 merged into Q-LA1) |
| order_to_delivery_planning | 2 (Q24, Q25) | 7 (Q16, Q18, Q26, Q27, Q-OE4, Q29, Q30) | 5 (BA4, Q-OE1, Q-OE3, Q-TI1, Q-OE2) | Q21, Q22, BA5, BA6 |
| delivery_and_returns | 0 | 3 (Q34, Q42, Q-SR1) | 2 (BA8, Q-SR2) | Q32, Q33, Q41, Q43, N1, BA9 |
| settlement_and_finance | 5 (Q47, Q54, Q56, Q60, Q61) | 7 (Q48, Q-DS3, Q-RS3, Q-RS4, Q53, Q-DJ1, Q58) | 7 (BA10, BA11, BA12, BA13, Q-DS2, Q-RS1, Q-CS1) | Q-DS1, Q45, Q46, Q-RS2, Q50, Q55, Q49 |
| cross-cutting | 0 | 0 | 1 (BA2, + Q-DA1 merged) | - |
| **Total** | **15** | **22** | **19** | **21 answered + 2 merged** (10 by G11-2/2b evidence, 11 by G11-1 evidence recorded now) |

Before this consolidation: 70 open (A 16, B 32, C 22). New this consolidation: 9 (B: Q-OB2, Q-OE4, Q-DS3, Q-RS3, Q-RS4, Q-DJ1; C: Q-TI1, Q-SR2, Q-CS1). Partly answered and still open: Q-RS1 (day close = PJP Daily Inquiry Update End Of Day / Complete; detailed procedure pending from the QA lead), BA14, Q26, Q30, Q42, Q48, Q58. BA list = 15 (the hard maximum); QA lead / framework owner list = 4.

### 2.4 Contradictions found

| # | Topic | Resolution |
|---|---|---|
| 18 | Previous closings carried? 10-01 morning one row Opening 0 vs 10-05 all 39 rows with Opening = previous Closing + still-Allocated | resolved for the cycle (10-05 rule); 10-01 anomaly kept as Q-OB2; old text marked superseded in 6 pages and INDEX |
| 19 | Return discount "proportional" (G11-1) vs slab re-pricing on non-returned lines (G11-2b) | resolved (refined); intent Q-SR2 |
| 20 | Cheque statuses db P/L/R/B/C/A and "Realized" vs screen "Clear" + Bounce only | open (Q-CS1, BA11) |
| 21 | Route Complete + slips Posted (10-05) vs Route Complete + slips Un Posted (10-01) | open (Q-DS3) |
| 22 | Order Editing filter: "Date To must cover the delivery date" (G11-1) vs "only delivery date = today" (G11-2) | resolved in favour of G11-2; exact rule Q-OE4; session-2 report wording ("in range") reconciled with the log |
| 23 | Deposit Slip Add: blank form (G11-1) vs PJP-DSR back to 02111 (G11-2) | open (minor) |
| 24 | Why workbook return values differ: "source order edited" (G11-1) vs "workbook built 2026-09-21 for outlet 1000000003" (G11-2b) | resolved (framework drift) |
| 11, 12 | GRN feeds; order of Cashmemo Status vs return | resolved by the two walks |

Totals: 24 contradictions listed, 13 resolved, 4 partly, 7 open. Workbook / framework vs app mismatches (26 rows, 11 new this session) are in [../FRAMEWORK_DRIFT.md](../FRAMEWORK_DRIFT.md).

## 3. Flows walked and not walked (group 11 active rows, 46 flows, seq 1-71)

| Seq | Flow | G11-1 (10-01) | G11-2 / 2b (10-05) | Note |
|---|---|---|---|---|
| 1-14 | login, DA, DA approval, loss approval, stock after DA, booking, allocation, inquiry | walked | walked | identical amounts and messages |
| 15 | Order Editing (before GIN) | skipped (QA lead) | **skipped (QA lead)** | cannot find its order as automated (delivery date = next visit; list shows only delivery date = today); Q-OE1 / Q-OE2 |
| 16, 18, 19, 20, 23, 24 | cancel, unallocate/allocate, delivery date change, GIN, GIN approval, stock after GIN | walked | walked | seq 18 run as one-order round trip (QA lead) |
| 29, 31, 32, 33 | edit / cancel after GIN, reschedule, cashmemo status | walked | walked | |
| 34, 36, 37, 38 | sales return, forward, approval, pick | walked | walked | |
| 39-46 (39, 40, 41, 42, 44, 46) | deposit slips | walked | walked | |
| 48, 49, 50 | GRN, approval, stock after GRN | walked | walked | |
| 51 | Route Settlement | blocked (09-30 open) | blocked in the morning (10-01 open); afternoon read: 10-01 and 10-05 **Complete** | the settlement action was done by a QA team member, not observed |
| 52, 53, 54 | Offset after settlement, slip after settlement, cash removal | not reached | walked (read only) | seq 54 covered by the seq 53 read |
| 55 | Cheque Status | not reached | **bypassed (QA lead)**; screen read | "Realized" does not exist; only Bounce |
| 56 | DSR Adjustment Amount | not reached | **bypassed (QA lead)**; screen read, values typed and discarded | |
| 57 | PJP Daily Inquiry Update | not reached | walked: **the day close** | End Of Day / Complete -> Current Status E |
| 58, 59 | OTC Stock Out (SAN) and approval | not reached | walked (SAN 96) | detail quantity typed by the QA lead in the session |
| 60 | Opening & closing stock | not reached | walked | |
| 68, 69, 70, 71 | Transaction Inquiry validations | not reached | walked | workbook drift on 70 (header Tax) and 69/71 |

Coverage: 43 of 46 active flows walked at least once (seq 51 read only); seq 15 not walked; seq 55 and 56 bypassed by the QA lead's decision [stated 2026-10-05 QA lead].

## 4. Data left in the environment (do not reuse on another day)

| Document | Numbers | State at end of 2026-10-05 |
|---|---|---|
| Dispatch Advice | 1358 (10-01), 1359 (10-05) | Approved |
| DA loss records | 639, 640 | Approved |
| Orders / cash memos | COL26000002003-2008 (10-01) | 2003 edited + delivered (partly received 1,000 from slip 1140; 3,600 on unposted 10-01 slips); 2004, 2005 delivered (open, on unposted 10-01 slips); 2006 Reattempt (delivery 10-02); 2007, 2008 Cancelled |
| | COL26000002009-2014 (10-05) | 2009 edited + delivered, Received 2,600, Balance 88,107; 2010, 2011 delivered and fully received; **2012 Reattempt with delivery 2026-10-06 (will be offered on a future GIN)**; 2013 Cancelled after the GIN; 2014 Cancelled |
| Goods Issue Notes | 506 (10-01), 507 (10-05) | Approved; old GIN 505 (09-30) still Pending, holding 63 CS of 62740537 Allocated on every day |
| Sales returns | COL26000000713, COL26000000714 | Approved and Picked; not netted from the receivable |
| Deposit slips | 1131-1136 (10-01) | still **Un Posted** although route 02112 for 10-01 is Complete (Q-DS3) |
| | 1137-1142 (10-05) | **Posted** (1139 trimmed to 600) |
| Goods Return Notes | 246, 247 | Approved |
| Stock Adjustment SAN | 96 | Approved (-50 CS 62740537, Auto Main, Sound) |
| Routes / days | 02112 for 2026-10-01 and 2026-10-05 | settled (Complete) and closed (PJP Daily Inquiry Update Current Status E) |
| Stock (62740537, Auto Main, Sound, 10-05) | | Opening 308 / In 99 / Out 85 / Allocated 63 / Closing 259 |

## 5. G0 readiness verdict per area (for the QA lead; not a sign-off)

| Area | Verdict | What is missing |
|---|---|---|
| inbound_stock | **Ready for G0 review** | Positive cycle observed on two days, new-day rule settled. Gaps the QA lead may accept as known: DA Reject/Delete (Q02), GRN partial return and non-Sound returns (Q-GRN1, Q-GRN2), loss Reject disabled (Q-LA2), loss claims (Q-LA1, also the one DoD failure), 10-01 opening anomaly (Q-OB2). |
| order_to_delivery_planning | **Ready for G0 review** | All 6 pages meet the DoD. Decision needed on seq 15 (Q-OE1 / Q-OE2); not yet walked: quantity above ATP / short-stock allocation (Q16, Q27), past delivery date (Q29); meaning of Ordered/Allocated after an edit (Q-TI1). |
| delivery_and_returns | **Ready for G0 review, with one material gap** | Positive path observed on two days. Material gap: an approved and picked sales return is not netted from the receivable even after settlement (Q-SR1) - the QA lead should decide whether cases may be written around it. Smaller: 3 pages fail the DoD on minor [unknown]s (GIN/return cancel actor, CRN-02 trigger, Planning completed timing); date used by the GIN stock check (Q34); slab re-pricing intent (Q-SR2). |
| settlement_and_finance | **Not ready** | Only 1 of 7 pages meets the DoD. The settlement action itself was performed by a QA team member (screens, entry step and success message not observed; Q48); seq 55 and 56 bypassed (cheque bounce effect BA11, DSR adjustment effect and status BA12 / Q53 unknown); day-close procedure pending from the QA lead (Q-RS1); 10-01 route Complete while its slips are Un Posted (Q-DS3); Total Order 13 unexplained (Q-RS3); SAN stock after Forward and finance posting (Q58, BA13). Needed: QA lead's day-close note, one observed settlement by the Maker on a fresh day, a decision on seq 55/56 (Q-CS1), then a re-check of the DoD. |

Next steps: QA lead reviews this report and the pages for G0; framework owner reviews [../FRAMEWORK_DRIFT.md](../FRAMEWORK_DRIFT.md); BA receives section 1a of [../OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md); the Senior QA knowledge check (predict, execute, compare) can use the observed facts of all four areas.
