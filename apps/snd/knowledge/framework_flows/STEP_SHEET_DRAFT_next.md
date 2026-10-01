# DRAFT step sheet: rest of the group-11 cycle (for QA review before execution)

Status 2026-09-29 end of day. Written from the framework tables (`fct_pr_*`) and the Pakistan workbook, in the standard vocabulary (`docs/STEP_VOCABULARY.md`). Each step is **clear** (the tables and a live check agree) or **NEEDS INPUT** (the framework config and the live app disagree, or something is unknown). **Nothing below has been executed except where marked "done".** QA: please answer the NEEDS INPUT items; then Claude runs the sheet without further questions except logins.

Session now: browser logged in as **Auto_Multi_Orga** (Stock Controller), distributor 15108843 IBRAHIM TRADERS. Roles: Maker/Stock Controller = Auto_Multi_Orga; Checker = Auto_Tssm.

## Already done today (do not repeat)
| Chain seq | Flow | Result |
|---|---|---|
| 2 | Dispatch Advice | DA **1350** created, 4 lines, losses, forwarded |
| 5 | DA Approval (Auto_Tssm) | 1350 Active / Approved |
| 7 | DA Loss Approval (Auto_Tssm) | loss record 637 Approved |
| 9 | Stock validation after DA | Sound closing = received; framework's exact In/Out check fails on a busy day |
| 10 | Order Booking | 8 orders COL26000001995-2002, totals = workbook |
| 12 | Stock Allocation | orders are auto-allocated at save; "Process completed successfully" for the one older order 1988 |
| 14 | Transaction Inquiry after OB | outlet 1000000006 header amounts = workbook; all orders Confirmed |

## Next (in chain order)
| Seq | Step | State | Notes / question for QA |
|---|---|---|---|
| 15 | `[Order User] Navigate to Order Editing` | clear | menu Transaction > Order > Order Editing (`/ngui/order-editing`) |
| 15 | `[Order User] Choose PJP = 02111~AutomationOB1` (category 201 and section fill in by themselves) | clear | |
| 15 | `[Order User] Choose Outlet Name = 1000000004` | **NEEDS INPUT** | The Outlet list says "No data to display" (date range today to today). Suspected: the range filters on **delivery date** (orders have 2026-10-05), or allocated orders are hidden. What is the correct way to make outlet 1000000004's order 04 (COL26000001998) show up? |
| 15 | `[Order User] Open the order, edit line 1 (62740537): OrderCS = 4, OrderPC = 0, Reason Type = "Order Change QTY", save the line, Validate, Save order` | clear once the order opens | expected summary (workbook `Order Editing Detail2`): Gross 96,840.34, Discount -20,718.07, Tax 14,584.79, Net 90,707.00; assertions ORD_EDIT_VALD_ASSR, ORD_EDIT_SAVE_ASSR |
| 16 | `[Order User] Navigate to Order Cancellation` (option DYL_202022) | clear | |
| 16 | `[Order User] Find outlet 1000000007 (order 07, COL26000002001), Cancellation Reason = "Shop Closed", Cancel` | **NEEDS INPUT** | same date-range question as Order Editing; expected message "Order Cancelled Successfully" |
| 18 | `[Order User] Navigate to Order Stock Allocation (menu title), Allocated / Unallocated tab, Unallocate` | **NEEDS INPUT** | Orders are already allocated automatically. Which orders should be unallocated (framework filter "Aautomation", select all)? That would unallocate all remaining orders and change the GIN step. Confirm intent. |
| 19 | `[Order User] Navigate to Delivery Date Change: Order Date = today, Delivery Date = today, PJP = 02111~AutomationOB1, select all, Process (accept the alert)` | **NEEDS INPUT** | workbook dates are 2026-09-21; today = 2026-09-29. Expected message key DELIVERYDATE_CHNG_ASSR. Should delivery be moved to today? |
| 20 | `[Order User] Navigate to Goods Issue Note: Delivery Man PJP = 02112-AutomationDSR, DSR = AutomationQADSR, Selling Category 001, Warehouse C0000000055 Auto Main, Section 101020304050, Vehicle "74 - Sect to Locus", Suggested Type = Cashmemo List, Delivery Date = ?` | **NEEDS INPUT** | workbook delivery date 2026-09-21; needs the date the orders are delivered on (see 19). Then select orders by DSR name "Auto", Save all, Forward with comment "Automation Approval" -> GIN number |
| 21 | **SWITCH -> Checker Auto_Tssm** | clear | logout, QA lead logs in |
| 23 | `[Checker] Approve Goods Issue Note <GIN>` (same screen) | clear | comment "Automation Approval"; assertion GIN_FORWARD_ASSR / approval |
| 24 | **SWITCH -> Auto_Multi_Orga**; stock validation after GIN | clear | expect a clean-day problem like seq 9 |
| 29+ | Order Editing After GIN, Order Cancellation After GIN, Cashmemo Reschedule and Status, Sales Return chain ... | not read yet | read from the tables when reached |

## Questions for QA (answer once, in any order)
1. How do you make an order appear in **Order Editing / Order Cancellation** (date range? unallocate first?)
2. Stock is **auto-allocated** when an order is saved. Is the framework's manual Stock Allocation step meant for another configuration, and should Unallocation be run at all in this cycle?
3. Which **delivery date** should the orders have before the GIN (today, or the PJP's 2026-10-05)?
4. Who is the Maker default user (the framework tables don't say); is `Auto_Multi_Orga` the right one?
