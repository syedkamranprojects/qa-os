# Session report: TRAIN-SND-PK 2026-10-12, QA team answers to the group 66 review (method B)

- Date: 2026-10-12. Trainer: the QA team (written answers); received by Syed Kamran (QA lead). Market / env: PK / cnr1dev1.
- Input: our 2026-10-09 group 66 review (`learning_sessions/2026-10-09_G66-PK_session2_report.md` / `2026-10-09_G66-PK_QA_Team_Review.docx`) returned with "Correct? Y/N" + "QA comment" for statements 1-16 and a "QA answer" for D-G66-2-1, Q-PO1, Q-G66-1..7 (`2026-10-09_G66-PK_QA_Team_Review_answered.docx`; extracted table in the log).
- Tag: `[stated 2026-10-12 QA team]`. Answers are summarised in our words; nothing earlier was deleted or rewritten; replaced wording carries `(superseded 2026-10-12: ...)`.
- QA lead rule for this merge: mismatches and unanswered points are recorded as open questions / contradictions and are **not sent now**; marked **"deferred: raise when a ticket touches this area (QA lead 2026-10-12)"**.

## 1. Outcome per item

| Item | QA answer (summary) | Outcome | Where |
|---|---|---|---|
| S1 Stock | N: an order does not deduct stock; it checks availability for delivery and temporarily allocates the quantity so other orders cannot use it | **Superseded** wording "draws / deducts / takes stock"; the PJP-warehouse observation (IBT Main vs Auto Main) is kept (not disputed); new glossary term "Stock allocation (order booking)" | pjp.md §6, order_booking.md, stock_allocation.md (+ rule line), section_and_mappings.md §1 / §10, delivery_man_shuffling.md §10, glossary, LIVE_FINDINGS (appended note), FRAMEWORK_DRIFT 4b row 53 |
| S2 Approvals | Y: change tracking has a single approval screen; setup approvals may be separate or on the same screen depending on the setup | **Confirmed** + new detail; contradiction 46 **resolved** (both set-ups valid; cnr1dev1 uses the separate PJP Approval menu) | pjp.md §2, INDEX doc map, glossary (PJP Approval), OPEN_QUESTIONS §5 |
| S3 Approvals | Y: refreshing the screen shows the latest status | **Confirmed** (in practice re-open the screen: a browser reload goes to Home) | pjp.md §7, LIVE_FINDINGS note, INDEX |
| S4 PJP | Y: PJP code generation is configurable (manual or automatic); a new PJP is saved with the current working date | **Superseded** "the app does not generate it" (environment set-up: typed on cnr1dev1 / 15108843); working date refined | pjp.md §3, §8, glossary, FRAMEWORK_DRIFT 4b row 48 |
| S5 PJP | Y: GPS / DDO interdependent; available for updating once the PJP is approved | **Confirmed** read-only at DT creation; Syed Kamran's "set elsewhere (setting or another user level)" **superseded**; new verify question Q-PJ7 (deferred) | pjp.md §8, §11 (case 9b), glossary (new term GPS / DDO), FRAMEWORK_DRIFT row 47 |
| S6 PJP | Y "That is correct" | **Confirmed** (change-request and config fields) | pjp.md §8 |
| S7 PJP | Y: Process runs through an integration job; visible after refresh | **Confirmed** + new detail; Q-PJ6 stays open (deferred) | pjp.md §6, glossary |
| S8 Section | Y: users / roles already covered in the earlier training | **Confirmed** (HQ section, no approval) | section_and_mappings.md §2 |
| S9 DSR | Y: mobile, CNIC and user validations exist because the Delivery App and Warehouse App use them | **Confirmed** + **new** reason | dsr.md §8 |
| S10 DSR | Y | **Confirmed** (HQ DSR needs no approval) | dsr.md §2 |
| S11 DSR | Y | **Confirmed** (AUTOH24109 with Auto_Multi_Orga) | dsr.md §3 |
| S12 Mapping | Y | **Confirmed** (no toast; end-state tick rule) | section_and_mappings.md §8 |
| S13 Mapping | Y: no validation prevents an outlet in several sections | **Confirmed**; **Q-PJ5 answered** | section_and_mappings.md §8, pjp.md §8 / §12 |
| S14 Outlet | Y: (comment on Company Mapping's purpose) | **Confirmed**; **Q-PO2 answered** | outlet.md §6, section_and_mappings.md §8 |
| S15 Outlet | Y: the daily PJP has not been executed, so its data is not displayed | **Confirmed** + **new** explanation of outlets 01-03, 09, 10 not offered | outlet.md §3, pjp.md §8 |
| S16 Delivery | N: known issue that requires investigation | Observed behaviour **kept**, flagged **known issue**, not a rule; new Q-DM2 + contradiction 48 (deferred) | delivery_man_shuffling.md (status line, §6, §11, §12), glossary, LIVE_FINDINGS, FRAMEWORK_DRIFT 4b row 64 |
| D-G66-2-1 | Known issue, requires investigation | **Confirmed**; defect stays **open** (deferred) | section_and_mappings.md §12, LIVE_FINDINGS, FRAMEWORK_DRIFT row 59 |
| Q-PO1 | Defines a prospect outlet (found by an Order Booker / Merchandiser on market visits, entered and submitted, then on Prospect Outlet for approval) | **New** knowledge (definition); question **kept open** (Forward not answered), deferred | outlet.md §1 / §2 / §8, glossary (Prospect Outlet) |
| Q-G66-1 | Works if the required data is on the respective screens | No user named; folded into Q-PO1 as evidence (Forward was disabled for Automation too) | outlet.md §2, OPEN_QUESTIONS Q-PO1 |
| Q-G66-2 | Change tracking applies only to approved outlets | **Q-PO3 answered**; residual: the screen accepted request 74 on the Draft outlet -> contradiction 49 (deferred) | outlet.md §5 / §8, FRAMEWORK_DRIFT row 56 |
| Q-G66-3 | Cache eviction or re-login needed for changes to take effect | Recorded; does not say what Process creates -> Q-PJ6 open (deferred) | pjp.md §6, OPEN_QUESTIONS Q-PJ6 |
| Q-G66-4 | HQ screen for specific users, no approval; Section Profile will be enhanced so delivery days are entered there | **New** (planned change, watch future tickets); contradiction 45 **partly resolved** | section_and_mappings.md §8, pjp.md §3, glossary, FRAMEWORK_DRIFT row 49 |
| Q-G66-5 | All DT-level users can update DDO / GPS; GPS keeps order taking / delivery inside geographic bounds; DDO feeds a third-party logistics route planner | **New** rule; screen still to verify: Q-PJ7 (deferred) | pjp.md §8, glossary |
| Q-G66-6 | HQ-screen changes do not require approval | **Contradiction 47** with the observation (AUTO241010 In-Active until TM approval); new Q-PJ8 (deferred); observation kept | pjp.md §5 E / §8, FRAMEWORK_DRIFT 4b row 63 |
| Q-G66-7 | OK | **Confirmed** (use 1000000014) | outlet.md §3, FRAMEWORK_DRIFT row 52 |

## 2. Facts added / confirmed / superseded per page

- **master_data/pjp.md**: status line; contradiction 46 resolved (§2); PJP code configurable + current working date (superseded §3, §8); Section delivery days planned on Section Profile (§3); stock wording superseded (§6); Process = integration job, refresh / re-login (§6); refresh shows status (§7); GPS / DDO rule and business meaning, "set elsewhere" superseded (§8); new §8 block (statement 6 confirmed, daily PJP not executed -> outlets not shown, no section-uniqueness validation, HQ no-approval claim vs observation); HQ PJP note (§5 E); case 9b (§11); Q-PJ5 answered and deferred list (§12); sources (§13).
- **master_data/outlet.md**: status line; prospect outlet definition (§1); Q-G66-1 answer under Q-PO1 (§2); daily PJP explanation + 1000000014 OK (§3); Q-PO3 answered (§5 D.4); Draft outlet confirmed (§6); change tracking only for approved outlets + contradiction 49, prospect hint (§8); §12 summary.
- **master_data/section_and_mappings.md**: status line; stock wording (§1, §10); HQ no approval confirmed (§2); planned Section Profile enhancement (§8); several sections confirmed; Draft outlet confirmed; mapping rules confirmed; D-G66-2-1 known issue, open (§12).
- **master_data/dsr.md**: status line; statements 9-11 confirmed; Delivery App / Warehouse App reason for the validations (§8); §12.
- **delivery_and_returns/delivery_man_shuffling.md**: KNOWN ISSUE status line; §6 / §11 flagged; stock wording (§10); Q-DM1 deferred, Q-DM2 new (§12).
- **order_to_delivery_planning/order_booking.md**, **stock_allocation.md**: stock wording superseded; stock_allocation gets the allocation rule line.
- **glossary.md**: 2 terms added (Stock allocation (order booking); GPS Restriction / GPS Radius / DDO Indicator), 7 rows annotated.
- **INDEX.md**: 2026-10-12 update line; change-request doc-map row annotated.
- **FRAMEWORK_DRIFT.md**: section 4b (notes on rows 47, 48, 49, 52, 53, 54, 56, 59; new rows 63, 64).
- **LIVE_FINDINGS.md**: appended block (D-G66-2-1 known issue, shuffling known issue, wording and confirmations).
- **LIVE_LEARNING_CHECKLIST.md**: L57 answered, L58 / L59 deferred notes, L60 new (Q-PJ7).
- **OPEN_QUESTIONS.md**: status header, section 1 / 1b / 1c / 3 / 4 headings, rows Q-PO1, Q-PO2, Q-PO3, Q-PJ5, Q-PJ6, Q-DM1 annotated, new rows Q-PJ7, Q-PJ8, Q-DM2, new section 2i, contradictions 45 (partly), 46 (resolved), 47-49 (new), section 6 counts, legend.
- **master_data/README.md**, **learning_sessions/README.md**: one line / one row each.

## 3. Questions answered

| Q | Class | One-line answer |
|---|---|---|
| Q-PO2 | A | Yes, only approved outlets are offered for mapping / document change track (statement 14). |
| Q-PO3 | B | Change tracking applies only to approved outlets; for those, a single approval screen (Q-G66-2, statement 2). |
| Q-PJ5 | C (1c, ON HOLD) | Currently no validation prevents an outlet in several sections (statement 13). |

## 4. Questions deferred (raise when a ticket touches the area)

| Id | One line | Area |
|---|---|---|
| Q-PO1 | What enables Forward on Prospect Outlet? (definition given; Forward not answered; Q-G66-1 "works if required data exists") | Master data / outlet (Prospect Outlet, Prospect Outlet Approval) |
| Q-PJ6 | What does PJP Daily Inquiry Process create for a PJP? (answer was about refresh / integration job / re-login) | PJP / journey plan (PJP Daily Inquiry) |
| Q-PJ7 (new) | On which screen does a DT user update GPS / DDO after the PJP is approved, and does it need TM approval? | PJP (PJP Creation DT / PJP Change Request) |
| Q-PJ8 (new) | Does a PJP made on PJP Creation HQ need TM approval? QA: HQ changes need none; observed: AUTO241010 In-Active until TM approval (contradiction 47) | PJP (PJP Creation HQ / PJP Approval) |
| Q-DM1 | After a shuffle, which DM PJP / DSR does the order show? | Delivery planning (Delivery Man Shuffling) |
| Q-DM2 (new) | Delivery Man Shuffling is a "known issue": what is the correct behaviour? (contradiction 48) | Delivery planning (Delivery Man Shuffling) |
| D-G66-2-1 | Company Mapping > Distributor > Outlet sub-tab HTTP 500: known issue, defect open; re-test when fixed | Master data / Company Mapping |
| Contradiction 49 | Change Track Outlet Profile accepted a request on a Draft outlet although change tracking applies only to approved outlets | Master data / outlet change track |
| Contradiction 45 (partly) | Default delivery days: planned Section Profile enhancement; watch future tickets (Q-PJ2 stays ON HOLD) | Master data / section |

## 5. Contradictions

- **46 RESOLVED**: guide "TM approves on the same screen" vs live separate PJP Approval menu: both are valid set-ups (S2).
- **45 PARTLY RESOLVED**: Default delivery days not on the current section screens; Section Profile will be enhanced (Q-G66-4).
- **47 NEW** (deferred): HQ-screen changes need no approval (QA) vs AUTO241010 In-Active until TM approval (observed 2026-10-09).
- **48 NEW** (deferred): Delivery Man Shuffling observed behaviour vs QA "N, known issue".
- **49 NEW** (deferred): change tracking only for approved outlets (QA) vs Change Track Outlet Profile accepting request 74 on the Draft outlet (observed 2026-10-05).
- Checked and **not** a contradiction: S5 / Q-G66-5 (read-only at DT creation, editable after approval: consistent; verify the screen, Q-PJ7); S3 (refresh vs re-open: same thing in practice); S1 (temporary allocation fits the observed Allocated / Closing at save and Out at GIN approval).

## 6. Counts

- Open questions: **before 62** = A 17 + B 22 + C 23 (1a 7, 1b 6, 1c 10); **after 62** = A 16 + B 22 + C 24 (1a 7, 1b 8, 1c 9). Closed 3 (Q-PO2, Q-PO3, Q-PJ5), new 3 (Q-PJ7, Q-PJ8, Q-DM2). Of the 62: 9 ON HOLD, 6 deferred to ticket time.
- Contradictions: 46 -> 49 listed; resolved 21 -> 22, partly 5 -> 6, open 20 -> 21.
- Defects: 1 open (D-G66-2-1, confirmed known issue).
