# Learning report: LEARN-G11-PK/20261006 (session 3, full group 11 run WITH the QA Team Lead)

Evidence: [2026-10-06_G11-PK_session3_log.md](2026-10-06_G11-PK_session3_log.md) (verbatim copy of `runs/LEARN-G11-PK/20261006/session_log.md`). Plan: [G11-PK_session3_plan_with_QA_lead.md](G11-PK_session3_plan_with_QA_lead.md).
Env cnr1dev1, Unilever Pakistan Limited, distributor 15108843. Date 2026-10-06, one calendar day. Maker Auto_Multi_Orga, Checker Auto_Tssm (10 user switches). Logins typed by the QA member; Claude picked company and distributor.
**Consolidated 2026-10-06** into the area pages, glossary, document_lifecycle, INDEX, LIVE_FINDINGS, FRAMEWORK_DRIFT and OPEN_QUESTIONS.

## 1. What was walked
All 46 active rows of group 11, seq 1-71, in order, with the QA Team Lead's rulings where the automated flow does not fit cnr1dev1:
- seq 1-14 as planned. Seq 19 Delivery Date Change was run **before** seq 15, and the order was unallocated, on the QA Team Lead's instruction.
- **Seq 15 Order Editing before the GIN was executed for the first time.** The workbook values matched exactly.
- Seq 16-38 were run with substitute orders agreed with the QA Team Lead, because workbook outlets 01-03 are not offered.
- Seq 39-50 as planned.
- **Seq 51 Route Settlement was performed by Claude for the first time.** It was first blocked by a new error, which was resolved with an extra allocation, GIN 509 and a delivery.
- Seq 52-54 were read. **Seq 55 was run as a check only**, with no Bounce. **Seq 56 was saved (400)** and seq 57 closed the day.
- Seq 58-60 created and approved SAN 97, then checked stock. Seq 68-71 were read in Transaction Inquiry.

## 2. Documents created (do not reuse on another day)
| Document | Number(s) | State at end of day |
|---|---|---|
| Dispatch Advice / loss | DA 1360 / loss 641 | Approved / Approved |
| Orders | COL26000002015-2020 | 2015 edited twice (7 -> 4 -> 3 CS), Delivered, partly returned, Balance 73,556; 2016, 2020 Delivered and paid; 2017 cancelled before GIN; 2019 cancelled after GIN; **2018 Reattempt, delivery 2026-10-07, unallocated** |
| Goods Issue Notes | GIN 508 (day's orders), GIN 509 (10-05 Reattempt COL26000002012) | Approved |
| Sales return | COL26000000715 (on 2015, 2 CS) | Approved, Picked |
| Deposit slips | 1143-1148 | Posted (1145 trimmed to 600) |
| Goods Return Note | GRN 248 (17 CS) | Approved |
| Route settlement | 02112, 2026-10-06 | Complete (by Claude); day closed (E) |
| DSR adjustment | COL26000000211 (400, AUTO) | Saved |
| SAN | 97 (-50 CS 62740537, Stock Adjustment Admin) | Approved |
| Open receivables | 2012 (108,202, unpaid by the QA Team Lead's choice), 2015 (73,556) | Open |

## 3. Rules learned
The rule's source is tagged [stated 2026-10-06 QA Team Lead] or [observed 2026-10-06 G11-3].
1. **Order Editing lists only UNALLOCATED orders whose delivery date is today.** Run Delivery Date Change first, then unallocate the order, then edit [stated]. Saving the edit **re-allocates** the order [observed]. After GIN approval an order can be edited without unallocation [stated + observed].
2. **Route Settlement procedure** [observed]:
   1. Click Edit on the route row.
   2. Cash lines' Received is editable (prefilled). Cheque Received is read-only. Stock Shortage Received is editable.
   3. Click the row Save. "Saved Successfully" appears, the row turns green, Edit disappears and the route is Complete.
   4. Order of the day: settlement -> DSR adjustment -> day close.
3. **New settlement blocker: "Un-Deliver Order exists for today delivery!"** It appears when an order due today on the route is undelivered. Here that order was yesterday's Reattempt [observed]. Allocating the order alone does not clear it [observed]. Resolution [stated]:
   1. Allocate the order in Order Stock Allocation, using Order Date = its booking date.
   2. Put it on a new GIN.
   3. The Checker approves the GIN.
   4. Mark it Delivered in Cashmemo Status.

   The order may stay unpaid. An unpaid delivered memo is not a cash shortage [observed].
4. **A Cashmemo Reschedule unallocates the order** [observed].
5. **Deposit slips**:
   - They are posted at settlement, and a partly allocated slip is trimmed to its allocation (1145: 1,000 -> 600) [observed, third day].
   - The outlet multi-cheque 1146 was counted as a "Previous" cheque, so it went to an older outlet-04 memo [inferred target]. This is intended: the Outstanding Outlet mode auto-adjusts FIFO, oldest invoice first; the Outstanding Cash memos mode collects per invoice [stated, Q-DS5].
   - **Duplicate cheque numbers are allowed because no cheque inventory is kept** [stated].
   - **Slips are not blocked before settlement** (a memo fully allocated on an unposted slip is still offered); Route Settlement Save reconciles, posts all slips, adjusts the invoices, and fully adjusted invoices leave the collection screens [stated; 2016/2020 observed].
   - **Outstanding Outlet doubled totals are a display defect** [stated, Q-DS4].
6. **Cheque Status (seq 55) is a check only; never Bounce** [stated]. Cheques read Clear after settlement [observed].
7. **DSR Adjustment Amount** [observed]:
   - Saving shows a confirm modal, then "Record Saved Successfully".
   - The save adds the amount to the PJP's **Total Shortage and Balance**; Total Adjusted is unchanged (+400 / +400 / 0).
   - Its meaning is a DSR shortage that arises while he takes money from the outlet [stated, Q-DJ1].
8. **Stock** [observed, third day]:
   - GIN approval moves Allocated to Out. GRN approval posts In. SAN approval posts Out.
   - 62740537 ended at Opening 0 / In 97 / Out 89 / Closing 8.
   - **Seq 9 opened the day with only the 5 received rows and Opening 0.** This matches 10-01 and differs from 10-05. Ruling (Q-OB2): carry-over of the previous Closing is the business rule; 10-05 Closing 259 vs 10-06 Opening 0 means the environment's carry-over job most likely did not run.
9. **Tax**: outlets 06 and 07 swapped tax behaviour compared with 10-05 [observed]; cause = master-data modification of the outlets and the tax promotion [stated, Q-TX1]. Rule [stated]: a zero-tax invoice of a non-exempt outlet cannot be delivered; a tax-exempt outlet's zero-tax invoice is allowed (not exercised: 2017 cancelled). Outlet 01's profile was changed in the group 66 walk, but outlet 01 is not offered.
10. **Transaction Inquiry**:
    - Offset = posted slip allocations (2015: 2,600).
    - On the order edited twice, the Detail shows Allocated 4 CS, Ordered 5 CS 4 PC and Delivered 3 CS; expected [stated, Q-TI1]: Ordered = original order quantity, Allocated = allocated from available stock.
    - Return 715: Tax -4,409.61, Net -29,066.

## 4. Questions
- **Answered (closed)**: Q-OE1, Q-OE2, Q-OE4 (Order Editing), Q-CS1 (seq 55 check only), Q-DJ1 (DSR shortage), Q-DS4 (display defect; raised and answered today), **Q-TI1** (Ordered = original order qty, Allocated = allocated from available stock; expected), **Q-OB2** (Opening must carry the previous Closing; Opening 0 = the environment's carry-over job did not run, see LIVE_FINDINGS E-G11-3-1), **Q-TX1** (outlet 06/07 tax swap = master-data modification of outlets and tax promotion; rule: a zero-tax invoice of a non-exempt outlet cannot be delivered, not exercised today), **Q-DS5** (Outstanding Outlet amounts are auto-adjusted FIFO to the outlet's oldest invoice; intended), **Q-RS1** (fully: the day close clears the per-PJP previous-day check; route rows yellow = not closed, green = closed), **Q-DS2** (fully: duplicate cheques allowed, no cheque inventory; slips are not blocked before settlement, whose Save reconciles, posts and adjusts the invoices).
- **Partly answered, still open**: BA12 (negative amounts / link to Route Settlement).
- **New**: Q-TX1 and Q-DS5, both answered the same day; no new open question remains.
- **Still waiting for the QA Team Lead**: nothing from today (Q-RS4 zero-activity detail left open by the user's choice). For the BA: Q-SR1 (return not netted at settlement), Q-OE3, BA11 (Bounce effect).
- Counts: open 47 = A 15 + B 19 + C 13 (1a 12, 1b 1; was 56).

## 5. Framework drift found (FRAMEWORK_DRIFT.md section 2b and new rows 27-36)
- Seq 15 needs Delivery Date Change and an Unallocate before it.
- Seq 29 uses the same data as seq 15, so after seq 15 runs it is a no-op. Expectations for seq 34 and 68-71 depend on what seq 29 does: on 10-06 the order was edited to 3 CS. The seq 68 Total Tax was 9,176.35 / 3,195.31 / 12,371.66 (workbook 11,389.48 / 3,195.31 / 14,584.79). The seq 69/71 return values were Tax -4,409.61 / Net -29,066.
- Seq 16 expected Net 134,535 is stale (actual 101,161). Seq 40 amount 119,370 belongs to the order that seq 16 cancels.
- Seq 51 needs a second precondition: deliver any Reattempt order due today. Seq 51's success message is "Saved Successfully".
- Seq 55: assert Clear only, never Bounce.
- Seq 56: assert Total Shortage +Amount and Balance +Amount. This corrects the earlier suggestion in row 7.
- Seq 24 Out 32 and seq 48 GRN 17 CS follow the day's edits. Seq 19 count is 6.
- Outlet tax for 06/07 has changed.

## 6. Readiness for G0 sign-off per area (facts for the QA lead; not a sign-off)
| Area | Verdict | Remaining gaps |
|---|---|---|
| inbound_stock | **Ready for G0 review** (three days observed; Q-OB2 answered) | Environment: the carry-over job did not run for 10-06 (LIVE_FINDINGS E-G11-3-1); pre-check Opening vs previous Closing. Also Q02, Q-GRN1/2, Q-LA1/2. |
| order_to_delivery_planning | **Ready for G0 review** (seq 15 now walked; Q-OE1/2/4, Q-TI1, Q-TX1 answered) | Q16/Q27 (above ATP / short stock), Q29 (past delivery date), Q-OE3 (BA); zero-tax delivery block stated but not yet observed (checklist L41). |
| delivery_and_returns | **Ready for G0 review, with one material gap** | Q-SR1: the return is still not netted at settlement (three days). The Reattempt carry-over to the next day is now a stated procedure. |
| settlement_and_finance | **Close to ready; G0 review possible after the remaining clarifications** (settlement, cheque check and DSR adjustment now observed and explained; multi-cheque FIFO stated) | Q-DS3 (10-01 slips never posted), Q48 (Received < Payable not tried), BA11 (Bounce effect), Q53 (adjustment status). DoD recount needed: run the coverage check again. |

## 7. Hand-over to the next day
- **COL26000002018** (Reattempt, delivery 2026-10-07, unallocated) will block the 2026-10-07 settlement of route 02112 ("Un-Deliver Order exists for today delivery!") unless it is handled. Either allocate it (Order Date 2026-10-06), put it on a GIN, approve it and mark it Delivered before seq 51, or have the QA team handle it.
- 2012 (108,202) and 2015 (73,556) remain open receivables on 02112.
- Group 66 (NG_Setup Flow_PK) is still paused after seq 18.
