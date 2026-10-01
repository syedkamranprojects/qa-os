# Stock Allocation and Unallocation: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 00130001 (seq 12), 00130002 (seq 18; seq 25 duplicate inactive).

## 1. Purpose
Allocation reserves warehouse stock to booked orders so that the GIN can issue exactly the goods promised. [inferred] Unallocation releases that reservation so the stock can be given to other orders or the order can be edited. [inferred] On cnr1dev1 allocation is automatic at order save, so the manual screen mostly shows the result.

## 2. Actors and roles
Auto_Multi_Orga (same session as order booking). [observed]

## 3. Documents and master data
No new document. Acts on order cash memos (Allocation Status; `tcmm_stock_allocated_status`, `tcmm_alloc_ref_no` columns exist [db]). Allocation rules table `rpl_pr_sar_stock_alloc_rules` exists, empty for org 010104 in the base DB. [db]

## 4. Inputs: screens and fields
Menu title **Order Stock Allocation** (framework search text "Stock Allocation" only finds the group; option `DYL_201904`, layout 201904). [observed]
Fields: Order Date (date, default today), PJP Number (dropdown; PJP 02111~AutomationOB1 preselected). Tabs: **Unallocated** and **Allocated**. Buttons: Allocation, Unallocate (Allocated tab). Grid columns: Delivery Date, Demand Channel, Description, Document Date, Document No, Net Amount, Outlet Code, Outlet Name, Section; filter row `rowfilter_OUTLDESC`; select-all `checkbox-0`. [observed/atlas]
Stock Unallocation flow 00130002 uses the same layout with tab_1 (Allocated).

## 5. Process: the business steps in order
1. [Order User] Navigate to Order Stock Allocation. (`11:12:00130001`)
2. [Order User] Verify Order Date and PJP Number; open the Unallocated tab.
3. [Order User] Filter Outlet "Aautomation", select all, click Allocation, accept the browser alert "Are you sure you want to proceed?". -> "Process completed successfully". [observed]
4. Unallocation (seq 18): Allocated tab, select rows, Unallocate, accept alert. -> observed answer "stock not found." [observed] (`11:18:00130002`)

## 6. Outputs and effects
- Allocated orders move to the Allocated tab; Allocation Status FULL. [observed]
- Stock effect (reserved/allocated quantity per warehouse): the Stock Inquiry Allocated columns carry it: on 2026-09-30, 13 rows had Allocated > 0 (e.g. 62740537 Auto Main 63 CS = the GIN 505 line) and Closing is net of Allocated [observed 2026-10-01]. Allocation also covers documents other than GIN 505 (20050308 Auto Main allocated 39 CS 96 PC vs GIN line 18 CS 16 PC) [observed]. Opening/Allocated on the new day are 0 for the received product (Allocated 0 on 10-01) [observed].
- Transaction Inquiry shows an allocated CS column (`row_1_allocated_cs`) per order line. [atlas]

## 7. Statuses and transitions
| from | action | to | by | tag |
|---|---|---|---|---|
| Unallocated | Order saved | Allocated (FULL) automatically | system | [observed] |
| Unallocated | Allocation | Allocated | Order user | [observed] |
| Allocated | Unallocate | (expected Unallocated) | Order user | [inferred]; observed result "stock not found." |

## 8. Rules and validations
- Orders are auto-allocated at save (all 8 new orders already Allocated). [observed]
- Only an older order (COL26000001988, outlet 1000000002) was in Unallocated and was allocated by the manual step. [observed]
- The screen date filters by Order Date; orders booked yesterday must have the date typed (send-keys then Enter). [observed]
- Alert must be accepted through the browser; script clicks cannot. [observed]
- Unallocate failed for all 9 orders, also for the 8 new ones alone, nothing changed. [observed]
- Partial allocation when stock is short: [unknown].

## 9. Messages
"Are you sure you want to proceed?" (confirm alert); "Process completed successfully" (allocation, key Stock_Allocation_ASSR); "stock not found." (unallocation; framework key Unallocated_ASSR expects something else, [unknown] what). [observed]

## 10. Dependencies
Reads orders from Order Booking and stock from the DA; day-keyed stock balances. Hands allocated orders to Order Editing/Cancellation (hidden when allocated, see order_editing_cancellation.md) and to GIN (cash memo selection).

## 11. Test design hints
- Positive: save an order and verify Allocated tab shows it (FULL); allocate an old Unallocated order.
- Negative: order quantity beyond stock -> expect partial/Unallocated; unallocate when stock missing.
- Boundary: stock exactly equals order quantity; Order Date yesterday/tomorrow.
- Traps: "Process completed successfully" with zero Unallocated rows proves nothing; the manual step is a no-op on auto-allocation; the Unallocated_ASSR expected text may never match.

## 12. Open questions (batched for the BA)
- Q: Why does Unallocate answer "stock not found." (stock keyed by day, allocation reference missing)? | Default: stock record for the order date missing | Evidence: unexplained.
- Q: Is the framework's manual Allocation meant for a configuration without auto-allocation, and should Unallocation run in this cycle? | Default: keep the step but expect no-op | Evidence: draft step sheet questions 2.
- Q: What does Allocation do on short stock? | Default: partial allocation | Evidence: not tested.

## 13. Sources
atlas flows 00130001, 00130002, group_11.md; TC-OB-01_executed.md (TC-OB-03); ui.md "Order Stock Allocation"; STEP_SHEET_DRAFT_next.md; DB `rpl_pr_sar_stock_alloc_rules`, `snd_tr_cmm_cashmemo_master` (column names).
