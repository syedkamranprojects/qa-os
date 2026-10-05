# Learning report: LEARN-G11-PK/20261001-1611 (session 1, stopped at seq 51)

Standard: `docs/LEARNING_STANDARD.md` §7. Plan: `learning_plan.md`. Evidence: `session_log.md` (full per-flow notes, messages, numbers).
Env cnr1dev1, company Unilever Pakistan Limited, distributor 15108843 IBRAHIM TRADERS. Date 2026-10-01, 16:11-18:33 PKT.
Stopped by the QA lead at seq 51 (Route Settlement blocked by an unclosed previous day).

## 1. Flows walked (group 11, active rows only)

| Seq | Flow | Result | Key document |
|---|---|---|---|
| 1 | Login Dcode | done | Auto_Multi_Orga (QA lead logged in; plan said Automation) |
| 2 | Dispatch Advice | done | DA **1358** |
| 5 | DA Approval (Checker) | done | 1358 Approved / Authorized |
| 7 | DA Loss Approval (Checker) | done | loss **639** Approved |
| 9 | Stock Validation After DA | done | In += received qty |
| 10 | Order Booking | done (6 orders, not the workbook's 8) | **COL26000002003-2008** |
| 12 | Stock Allocation | done (no-op: auto-allocated) | - |
| 14 | Transaction Inquiry after OB | done | promotions + tax breakdown |
| 15 | Order Editing | **skipped** (QA lead: QA/BA discussion) | - |
| 16 | Order Cancellation | done | 2008 Cancelled |
| 18 | Stock Unallocation | done on ONE order, then re-allocated (QA lead option 1) | 2007 |
| 19 | Delivery Date Change | done | 5 orders 10-07 -> 10-01 |
| 20 | Goods Issue Note | done | GIN **506** |
| 23 | GIN Approval (Checker) | done | 506 approved (first successful GIN approval of the replay) |
| 24 | Stock validation after GIN | done | Out = issued |
| 29 | Order Editing After GIN | done, no error | 2003 7 -> 4 CS |
| 31 | Order Cancellation After GIN | done | 2007 Cancelled |
| 32 | Cashmemo Reschedule | done | 2006 -> 10-02 (Reattempt) |
| 33 | Cashmemo Status | done | 2003/2004/2005 Delivered/Invoiced |
| 34 | Sales Return | done | return **COL26000000713** (2 CS) |
| 36 | Sales Return View (Maker forward) | done | Success |
| 37 | Sales Return View Approval (Checker) | done | Success |
| 38 | Sales Return Status Change | done | picked ("Save Sale Pick") |
| 39 | Deposit Slip Full Amount Cash | done | slip **1131** |
| 40 | Deposit Slip Full Amount Cheque | done | slip **1132** |
| 41 | Deposit Slip Unposted Amount | done (learning variant: 600 of 1,000) | slip **1133** |
| 42 | Deposit Slip Multi Cheques | done | slip **1134** (4 cheques) |
| 44 | Deposit Slip Cheque | done | slip **1135** |
| 46 | Deposit Slip Cash | done | slip **1136** |
| 48 | Good Return Note | done | GRN **246** (19 CS) |
| 49 | GRN Approval (Checker) | done | 246 approved |
| 50 | Stock validation after GRN | done | In +19 |
| 51 | Route Settlement | **BLOCKED** | "Following previous days not closed! Please close date. 2026-09-30" |
| 52-60, 68-71 | rest of the cycle | not walked | - |

Logins used: 7 (Maker 4, Checker 3) out of 11 planned.

## 2. Documents left on cnr1dev1 (do not reuse on a later day)
DA 1358 (Approved), loss record 639 (Approved); orders COL26000002003 (edited, Delivered), 2004 and 2005 (Delivered), 2006 (Reattempt, delivery 2026-10-02, off GIN), 2007 (Cancelled after GIN), 2008 (Cancelled before GIN); GIN 506 (Approved); sales return COL26000000713 (Approved, picked); deposit slips 1131-1136 (all Un Posted); GRN 246 (Approved). Stock of 62740537 at Auto Main moved (In 183 / Out 35 / Allocated 63 / Closing 245 on 2026-10-01).
**Route 02112 for 2026-10-01 is NOT settled** and 2026-09-30 is NOT closed. The app logout did not complete before the browser was closed (server session will expire).

## 3. Business rules learned (all [observed] unless marked)
**Stock and documents**
1. DA approval adds the RECEIVED qty (dispatched - loss) as Sound In on the Received Date; the DA's own approval creates the day row. Loss lines aggregate per line (Calculate) and one loss record per DA is created at approval (SKU types 02 Damaged, 04 Lost).
2. Approving a DA loss creates NO stock row (L21 closed).
3. Saving an order reserves stock at once (Allocated up, Closing and ATP down); cancelling releases it; Closing = Opening + In - Out - Allocated.
4. Manual Stock Allocation only matters for orders not allocated at booking; unallocate/allocate answer "Process completed successfully" (confirm dialog).
5. Delivery Date Change pulls orders from the next PJP visit (10-07) to today; the GIN only offers cash memos whose delivery date = GIN delivery date.
6. GIN detail = per-SKU sum of the selected cash memos; GIN approval = ONE Checker Forward (moves Allocated -> Out, Closing unchanged).
7. After the GIN, editing/cancelling/rescheduling an order does NOT move stock; everything not delivered (cancelled, cut, rescheduled, returned) comes back on the GRN (19 CS reconciled exactly); GRN approval posts it as In (Sound).
**Orders and pricing**
8. Outlet tax profile is in the outlet label; Tax Exemption = Y -> tax 0. Tax = VAT + "3rd Schedule" (retail-price based) charges, product-dependent.
9. Discount = several promotions (two at 10% of gross + fixed amounts) -> % depends on the basket. Header Net rounded to the rupee.
10. Order statuses: Confirmed -> Ready to dispatch/Packed (GIN approved) -> Delivered/Invoiced (Cashmemo Status save); Reattempt (rescheduled, leaves the GIN); Cancelled (keeps the GIN no. when cancelled after the GIN).
11. Order Editing date filters are DELIVERY dates (explains the 09-29 empty outlet list); Order Cancellation date filters are ORDER dates.
**Returns and money**
12. Sales return: own CM-02 number, Maker forward + Checker approve on Sales Return View ("Success"), then Maker "Save Sale Pick". The approved return did NOT reduce the cash memo receivable nor appear as Adjusted Credit Note in Route Settlement [open].
13. Deposit slips: header (PJP-DSR = delivery DSR, Cash/Cheque, bank) then allocate per cash memo (or per outlet with a multi-cheque popup). Balances change only at posting; "Un Posted Amount" on a cash memo = allocations on other unposted slips. All slips stay "Un Posted" until (presumably) Route Settlement.
14. Route Settlement shows each slip as a collection line; it requires all previous working days to be closed.
**Roles**
15. Maker-checker = same screen, same Forward button, different user (DA, Loss, GIN, Sales Return, GRN). Checker sees all 13 PJPs on Sales Return View; Checker cannot create a DA.

## 4. Coverage against the standard
| Level | State after this session |
|---|---|
| L2 Daily Cycle chain | seq 1-50 confirmed live end to end on one calendar day; 51-71 not walked |
| L3 pages touched (business facts available in session_log.md, NOT yet merged into the pages) | dispatch_advice, da_loss_approval, stock_inquiry_and_balances, stock_validation_flows, order_booking, stock_allocation, transaction_inquiry, order_editing_cancellation, delivery_date_change, goods_issue_note, cashmemo_reschedule_and_status, sales_return, deposit_slips, goods_return_note, route_settlement |
| L3 not touched | cheque_status, dsr_adjustment, pjp_daily_inquiry_update, otc_stock_out_and_san, end_of_day_validations |
| Phase 3 Consolidate | **NOT DONE** - next session: merge session_log.md into the 15 pages, glossary, document_lifecycle, OPEN_QUESTIONS, LIVE_FINDINGS |
| G0 sign-off | not yet |

## 5. Contradictions / corrections to existing knowledge
- Unallocate: 09-29 page says it answered "stock not found."; today "Process completed successfully".
- Opening balance: this morning's finding "new day opens at 0" no longer held at 16:40 (Openings present; 62740537 opening 160 = 09-30 closing 97 + allocated 63) -> who generates openings is open.
- Workbook outlets 1000000001-03 not bookable; vehicle default changed (0040-Automation211206 vs "74 - Sect to Locus"); bank "National Bank of Pakistan" no longer exists (only "...ss").
- GIN Verify/Approve (two workflow tasks for role 0005) = one Checker Forward in practice.

## 6. Defect candidates / data issues (for the BA / dev)
1. Maker keeps Forward + Reject enabled on his own Pending DA (self-approval not blocked on screen).
2. Order Editing grid with the auto-filled SKU filter shows Gross of one SKU vs whole-order Discount/Tax -> negative Net (-8,660.87).
3. Orders can be edited / cancelled after the GIN is approved without any warning.
4. Duplicate cheque number accepted for the same outlet (1234567 on slips 1134 and 1135).
5. Master data: duplicate "Lost" loss type; reschedule reasons "Law & Order Issue" x5, "Shop Closed" x2, "Test Reason 716"; bank list with test/junk entries; 62740537 weight 0.67 kg for 35 cases of 2x10L; purchase price > trade price for some SKUs.
6. Locked Order Booking header shows Outlet Name blank; "Successfull" typo in the cancellation result.

## 7. Framework drift found (for the framework owner)
- Stock validation asserts absolute In (assumes a clean day).
- Unallocation selects all orders right before the GIN.
- GIN_DTL_SAVE_ASSR "Saved Succesfully." vs real "Saved successfully."; Deposit Slip,Outlet expects "Saved successfully" vs real "Payment Adjusted Successfully".
- Multi-cheque button `grid-button-0` is on the Outstanding Outlet tab (needs the tab switch); cheque date there must be MM/DD/YYYY.
- Loss Approval clicks "first row" while the default grid order is not by serial.
- Vehicle and bank values in the workbook no longer exist.

## 8. Open questions (new this session; to add to OPEN_QUESTIONS.md)
| Id | Question | Default | Class |
|---|---|---|---|
| Q-OE1 | Is the Order Editing date range meant to be the delivery date, default today? | treat as delivery date | C |
| Q-OE2 | Which order should seq 15 edit when outlets 01-03 are not offered? | outlet 04's order | C |
| Q-DA1 | May the Maker approve/reject his own Pending DA? | must not (QA convention) | C |
| Q-SR1 | When does an approved sales return reduce the receivable (credit note? settlement?) | at Route Settlement / credit note | B |
| Q-DS1 | What is deposit-slip "posting" and when does it happen? | at Route Settlement | B |
| Q-RS1 | How is a working day closed (which screen), and may 2026-09-30 be closed on cnr1dev1? | ask BA before closing | C |
| Q-OB1 | Who/what generated today's opening balances during the day? | unknown | B |

## 9. Resume plan (next session)
1. Decide Q-RS1 with the QA lead / BA (close 2026-09-30, or accept skipping settlement).
2. **A new calendar day means a fresh full run from seq 1** (stock/day rule): today's documents cannot be continued tomorrow except for read-only inspection. If the team only wants to finish learning seq 51-71, walk them on a fresh day after re-running the chain, or do read-only walks of screens 55-58.
3. Consolidate (phase 3): merge `session_log.md` facts into the L3 pages, glossary, document_lifecycle, OPEN_QUESTIONS (section 8 above) and LIVE_FINDINGS; then produce the coverage report and ask for G0 on the inbound-stock and order-to-delivery areas.
