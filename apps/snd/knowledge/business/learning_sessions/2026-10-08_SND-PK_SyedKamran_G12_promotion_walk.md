# G12 seq 8 "Order Booking Promotion" (flow 00910001) - learning walk, 2026-10-08

Env cnr1dev1, Auto_Multi_Orga (Maker), company Unilever Pakistan Limited, distributor 15108843. Training walk, not a recording. Promotion Layout list left untouched (nothing saved there). Helper not injected (own scripts used; a page-level toast observer only).

Promotion under study: Automation2 / BONUS2, Qualify = SKU group (62740537, 20050310, 62690363, 20050308, 69997598) >= 5 cases; Resultant = Range Slab Discount On Gross, 1-10 -> 5 %, 11-99999 -> 10 %.

## Navigation / screen behaviour (business)
- Sidebar search "Order Booking" -> Transaction > Order Booking. Header: Order Booker/Spot Seller, PJP, Selling Category, Section, Outlet (type-ahead, type code and pick the one option), Document Date (defaults today 2026-10-08), Comments, Reference Number. "Order Detail" button opens the detail grid (type-ahead product, batch auto-fills 1-1, columns Current Stock (ATP), Trade Price/Unit, Order CS/DZ/PC, Gross Amount). Gross per line is calculated as soon as qty is typed (CS x units per case x trade price).
- Per-row Save shows no toast; the row just joins the grid. Validation then Save.
- After "New Order" the header resets: Order Booker stays, PJP/Selling Category/Section must be picked again.
- Current Stock (ATP) falls when an order is booked (62740537: 313 -> 312 after order A took 1 CS), i.e. stock is reserved at booking.

## Order A - COL26000002029
Inputs: Order Booker; PJP 02111-AutomationOB1; Selling Category 001; Section Automation_Testing_Section; Outlet 1000000012-Aautomation_Outlet_12; Comments "G12 WALK A"; date 2026-10-08. Lines (CS/PC), batch 1-1: 62740537 1/0, 20050310 1/0, 62690363 1/0, 20050308 1/0, 69997598 1/0.

Messages (toasts): after Validation "Validation successfully"; after Save "Order Save successfully". No alerts/popups. Row Saves: no message.

Gross per line (entry grid): 62740537 15,422.93 (TP 7,711.47/unit, 2 units per CS); 20050310 3,745.58 (TP 234.1); 62690363 3,274.49 (TP 16.05); 20050308 2,805.81 (TP 87.68); 69997598 3,682.51 (TP 12.79). Sum 28,931.32.

Order View: Delivery Date 2026-10-14. Gross 28,931.32; Discount -1,446.57; Tax 5,383.88; Net 32,869.00 (calculated 32,868.63; shown rounded to whole rupee).
Per-line discount on Order View: -771.15, -187.28, -163.72, -140.29, -184.13 (each = 5.00 % of line gross). Per-line tax 2,637.32 / 782.83 / 622.37 / 571.71 / 769.65 (rates differ by SKU).

Transaction Inquiry row: Gross 28,931.32, Discount -1,446.57, Tax 5,383.88, Net 32,869, status Confirmed, channel Back Office (BO).
Total Offering: 1 line only - Automation2 | Automation2-3 | BONUS2 | Discount PKR -1,446.57 | Tax 0. Sum = header Discount (match). No gross column on this tab.

Computed: 1,446.57 / 28,931.32 = 5.000 % of Gross (without tax). Matches the 5 % slab (1 to 10 cases; total qualifying qty here 5 cs).

## Order B - COL26000002030
Inputs: same header; Outlet 1000000013-Aautomation_Outlet_13; Comments "G12 WALK B". Lines: 62740537 2/0, 20050310 2/0, 62690363 2/0, 20050308 2/0, 69997598 3/0 (total 11 cases).

Messages: "Validation successfully"; "Order Save successfully". Nothing else.

Gross per line: 30,845.86; 7,491.16; 6,548.97; 5,611.62; 11,047.54. Sum 61,545.15.
Order View: Gross 61,545.15; Discount -6,154.51; Tax 0; Net 55,391.00 (calculated 55,390.64, rounded). Per-line discounts -3,084.59, -749.12, -654.9, -561.16, -1,104.75 (each 10.00 % of line gross). Tax 0 on every line (outlet 1000000013 appears untaxed, unlike outlet 12; reason not investigated).
Transaction Inquiry row: Gross 61,545.15, Discount -6,154.51, Tax 0, Net 55,391, Confirmed.
Total Offering: 1 line - Automation2 | Automation2-3 | BONUS2 | -6,154.51 | tax 0. Sum = header Discount (match).

Computed: 6,154.51 / 61,545.15 = 10.000 % of Gross (without tax, tax is 0 anyway). Matches the 10 % slab (11+ cases).

## Findings
- Both orders match the Range Slab Discount On Gross rule exactly: slab chosen on total qualifying cases (5 -> 5 %, 11 -> 10 %), applied to each qualifying line's gross and shown as a negative Discount; header Discount = sum of lines = Total Offering amount.
- Slab applies to the whole quantity (flat 5 % / 10 % on all gross), not tiered/incremental.
- Discount is on gross before tax; tax is calculated afterwards (A: tax is on gross less discount per line, per-SKU rates 18-22 %); Net = Gross - Discount + Tax, rounded to whole rupee on Order View/inquiry.
- Only one promotion applied to each order (Automation2/BONUS2, description Automation2-3); no other promotion seen. No free goods.
- Transaction Inquiry quirk: orders are listed under Document Type "Sales" (default "Demand Captured from Tele order" and other types return 0 rows). The detail tabs are cent-tab elements; Total Offering is the 4th tab. Product Wise Discount tab did not visibly refresh in this walk (grid still showed the Total Offering content), per-line discount was taken from Order View instead.
- Other orders exist today on the same PJP (COL26000002026-2028), not ours.

## Friction (software)
- Outlet/product type-aheads: moving to another field before picking discards the typed text (Comments typed first lost the outlet once; re-done once, no data impact).
- Product option list renders 1-2 s after typing; a click made too early hits a stale element.
