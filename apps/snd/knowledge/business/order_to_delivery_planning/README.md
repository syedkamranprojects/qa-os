# Area: order_to_delivery_planning (S&D / DCODE)

Updated: 2026-10-05 (G11-2/2b consolidation: orders COL26000002009-2014 on a second day, Transaction Inquiry after settlement); 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)

Status: DRAFT 2026-10-01. Tags [observed]/[db]/[inferred]/[unknown] as in _TEMPLATE.md. Roles: Maker (Auto_Multi_Orga) and Checker (Auto_Tssm) only. Evidence of the 2026-10-01 walk: `../learning_sessions/2026-10-01_G11-PK_session1_log.md`.

1. An order is a cash memo (CM-01 Sales, status Ordered 04) booked per outlet/PJP/section/selling category with product lines in cases and pieces. [db][observed]
2. Gross + Discount (negative) + Tax = Net; tax depends on the outlet. [observed] The outlet label carries its tax profile (Tax Exemption = Y -> tax 0); discount = several promotions, so its % depends on the basket; header Net is rounded to the rupee. [observed 2026-10-01 G11-1]
3. On cnr1dev1 stock is auto-allocated at save, so the manual Allocation step finds nothing new and Unallocate answers "stock not found.". [observed] (superseded 2026-10-01: Unallocate of one order answered "Process completed successfully" and re-allocation worked; booking reserves stock at once, cancellation before the GIN releases it. [observed 2026-10-01 G11-1])
4. Allocated orders disappear from Order Editing/Cancellation outlet lists; editing/cancelling are not yet executed. [observed/unknown] (superseded 2026-10-01: Order Editing dates filter the DELIVERY date, which explains the empty list; Order Cancellation filters the ORDER date. Editing and cancelling were executed, also after an approved GIN, with no warning and no stock movement. [observed 2026-10-01 G11-1])
5. Delivery Date Change moves delivery for a PJP in bulk ("processed orders: 9"); changing Order Date resets the PJP. [observed] 2026-10-01: 5 orders moved 10-07 -> 10-01 after the confirm "Are you sure you want to proceed?" ("processed orders: 5"), enabling a same-day GIN. [observed 2026-10-01 G11-1]
6. Transaction Inquiry (Document Type = Sales) proves amounts and status: Confirmed (execution 02) after booking, Planning completed (execution 03) once on a GIN. [observed 2026-10-01] Full chain seen: Confirmed -> Ready to dispatch/Packed (GIN approved) -> Delivered/Invoiced; Reattempt (rescheduled); Cancelled (GIN No kept when after the GIN). Total Offering and Total Tax sum to the header. [observed 2026-10-01 G11-1]
7. Everything depends on stock received the same calendar day. [observed] (refined 2026-10-05: previous closings are carried into a new day once its first movement creates the rows; old Pending reservations stay Allocated and lower ATP. [observed 2026-10-05 G11-2])
8. Base DB holds no order rows for org 010104 (overlay data), so statuses come from the master tables. [db]
9. Page order: order_lifecycle_and_statuses -> order_booking -> stock_allocation -> transaction_inquiry -> order_editing_cancellation -> delivery_date_change.
10. Other areas (by name): Inbound stock / Dispatch Advice; Delivery and returns (Goods Issue Note, cashmemo reschedule/status, sales return); Settlement (deposit slip, route settlement).
11. Second day 2026-10-05 (orders 2009-2014): identical amounts to the paisa, delivery date 10-11 (next visit), edit/cancel after GIN again allowed. **Order Editing listed orders only when their delivery date was today**; a range covering the future delivery date returned nothing, so seq 15 (before Delivery Date Change) cannot find its order; header PJP defaults to AUTO241602. [observed 2026-10-05 G11-2]
12. Transaction Inquiry after settlement: Offset Amount = posted deposit-slip allocations; Sales Return rows carry Invoice Ref. No. = source invoice, Demand Channel "Partial Return", status Picked; workbook drift on seq 70 header Tax and all seq 69/71 return values except Gross. [observed 2026-10-05 G11-2b]

## Pages (one line each)
| Page | What it holds (2026-10-01; 2026-10-05) |
|---|---|
| order_lifecycle_and_statuses.md | Cash memo = order; status chain and stock effect per lifecycle step, Maker/Checker chain with trace keys. |
| order_booking.md | Booking, tax profiles, basket promotions, rounding, auto-allocation at save, delivery date = next PJP visit. |
| stock_allocation.md | Allocated/Unallocated tabs; one-order unallocate + re-allocate "Process completed successfully"; framework select-all drift. |
| transaction_inquiry.md | Header amounts, Detail (Ordered vs Allocated; odd after an edit, Q-TI1), Total Offering, Total Tax, observed status chain; Offset Amount after settlement; Sales Return rows (Invoice Ref, Partial Return). |
| order_editing_cancellation.md | Editing lists only orders with delivery date = today (2026-10-05; run after Delivery Date Change) vs order-date filter (cancellation); header PJP default AUTO241602; reasons; edits/cancels before and after the GIN; SKU-filter negative-Net defect. |
| delivery_date_change.md | Bulk move to today for a same-day GIN; confirm dialog; status unchanged. |

## What this area hands to the next area
| Item | To | Detail |
|---|---|---|
| Booked, allocated orders (COL26...) | Goods Issue Note (delivery area) | Cash Memo Selection listed 9 eligible cash memos (2026-10-01 G11-1: exactly the 5 orders whose delivery date = the GIN delivery date) |
| `ORDERNUMBER` / `ORDERNUMBEREDIT` repos | Order editing, GIN | order numbers COL26000001995-2002; 2026-10-01: COL26000002003-2008 (an edit keeps the same number) |
| New Delivery Date per PJP | GIN header Delivery Date | must be typed on the GIN |
| Reserved stock (Allocated) | GIN stock issue | stock keyed by day; GIN approval moves Allocated -> Out |
| Order amounts (Gross/Net/Tax) | Cashmemo status, deposit slips, route settlement | net payable per outlet |
| Cancelled/edited orders | GIN eligibility | after-GIN rules [unknown] (superseded 2026-10-01: allowed, no stock movement; the cut/cancelled quantities return on the GRN [observed 2026-10-01 G11-1]) |

## Open questions of this area (new 2026-10-01; updated 2026-10-05)
Q-OE1 revised (run Order Editing after Delivery Date Change?), new Q-OE4 (exact date-filter rule, B), new Q-TI1 (Ordered/Allocated after an edit, C); Q-OB1 ANSWERED 2026-10-05 (openings at the first movement).
Q-OE1 (Order Editing date range = delivery date? default), Q-OE2 (which order to edit when outlets 01-03 are missing), Q-OE3 (block or warn edit/cancel after GIN?), Q-OB1 (who generated the day's opening balances). The empty-outlet-list question is ANSWERED (delivery-date filter).
