# Area: order_to_delivery_planning (S&D / DCODE)

Updated: 2026-10-01 (live blocks 1-3b)

Status: DRAFT 2026-10-01. Tags [observed]/[db]/[inferred]/[unknown] as in _TEMPLATE.md.

1. An order is a cash memo (CM-01 Sales, status Ordered 04) booked per outlet/PJP/section/selling category with product lines in cases and pieces. [db][observed]
2. Gross + Discount (negative) + Tax = Net; tax depends on the outlet. [observed]
3. On cnr1dev1 stock is auto-allocated at save, so the manual Allocation step finds nothing new and Unallocate answers "stock not found.". [observed]
4. Allocated orders disappear from Order Editing/Cancellation outlet lists; editing/cancelling are not yet executed. [observed/unknown]
5. Delivery Date Change moves delivery for a PJP in bulk ("processed orders: 9"); changing Order Date resets the PJP. [observed]
6. Transaction Inquiry (Document Type = Sales) proves amounts and status: Confirmed (execution 02) after booking, Planning completed (execution 03) once on a GIN. [observed 2026-10-01]
7. Everything depends on stock received the same calendar day. [observed]
8. Base DB holds no order rows for org 010104 (overlay data), so statuses come from the master tables. [db]
9. Page order: order_lifecycle_and_statuses -> order_booking -> stock_allocation -> transaction_inquiry -> order_editing_cancellation -> delivery_date_change.
10. Other areas (by name): Inbound stock / Dispatch Advice; Delivery and returns (Goods Issue Note, cashmemo reschedule/status, sales return); Settlement (deposit slip, route settlement).

## What this area hands to the next area
| Item | To | Detail |
|---|---|---|
| Booked, allocated orders (COL26...) | Goods Issue Note (delivery area) | Cash Memo Selection listed 9 eligible cash memos |
| `ORDERNUMBER` / `ORDERNUMBEREDIT` repos | Order editing, GIN | order numbers COL26000001995-2002 |
| New Delivery Date per PJP | GIN header Delivery Date | must be typed on the GIN |
| Reserved stock (Allocated) | GIN stock issue | stock keyed by day |
| Order amounts (Gross/Net/Tax) | Cashmemo status, deposit slips, route settlement | net payable per outlet |
| Cancelled/edited orders | GIN eligibility | after-GIN rules [unknown] |
