# TC-OB-01 Book an order for an outlet with 5 products: EXECUTED 2026-09-29 (framework flow 00010001, chain seq 10)

Environment cnr1dev1, distributor 15108843 (IBRAHIM TRADERS / Auto KARACHI). Actor: **Stock Controller / order user = Auto_Multi_Orga** (framework: lu 35, login status N = same session as the stock validation before it). Data: `NG_Dcode_QA_OTC (Pak).xlsx`, sheets `Order Booking` (row PK 01), `Order Booking Detail` (PK 01-01..01-05), `Order Booking Detail2` (expected summary).

| # | Step | Result | Verdict |
|---|---|---|---|
| 1 | Navigate to Order Booking | header: Order Booker/Spot Seller, PJP, Selling Category, Section, Outlet Name, Document Date, Comments, Reference Number; all 6 framework ids present | Pass |
| 2 | Choose Order Booker/Spot Seller = Order Booker; PJP = 02111-AutomationOB1; Selling Category = Selling Category 001; Section = Automation_Testing_Section; Outlet Name = 1000000001-Aautomation_Outlet_01 (the dropdowns cascade in this order); Enter Comments = "Automation Positive 01" | as entered; `Order Detail` button appears | Pass |
| 3 | Enter Reference Number = 100 (workbook), click Order Detail, add 5 lines, click Validation | **"Cashmemo with document reference number : 100 already exist."** | **Fail (data collision)** |
| 4 | New Order (dialog "Are You sure you want to cancel the order": Yes, id `continue`) and repeat step 2 **without** Reference Number | header cleared and refilled | Pass |
| 5 | Add line: 62740537, CS 5, PC 4 | gross **107,960.51** (workbook 107,960.51); ATP 80 CS | Pass |
| 6 | Add line: 20050310, CS 5, PC 0 | gross 18,727.9 (workbook 18,727.9); ATP 5,706 CS 3 PC | Pass |
| 7 | Add line: 20050308, CS 2, PC 10 | gross 6,488.44 (workbook 6,488.44); ATP 1,955 CS 5 PC | Pass |
| 8 | Add line: 62690363, CS 3, PC 2 | gross 9,855.56 (workbook 9,855.56); ATP 6,171 CS 78 PC | Pass |
| 9 | Add line: 69997598, CS 0, PC 6 | gross 76.72 (workbook 76.72); ATP 2,560 CS 123 PC | Pass |
| 10 | Validation | toast **"Validation successfully"**; a Save button appears | Pass |
| 11 | Save order | toast **"Order Save successfully"**; Document No **COL26000001995**; Order View: Delivery Date 2026-10-05, Section 101010101101-Automation_Test..., Selling Category 201-Selling Category 001 | Pass |
| 12 | Verify order summary | Gross **143,109.13**, Discount **-29,971.83**, Tax **21,861.52**, Net **134,999.00** = workbook `Order Booking Detail2` row 01 exactly | Pass |

**Result: PASS** (after removing the colliding reference number).
Cross-check: the ATP shown per product (80 / 5,706 / 6,171 / 1,955 / 2,560 CS) equals the closing balances of the Stock Inquiry validation, so the stock received by DA 1350 is what orders draw on.
The app converts the order into cases: line 1 demand 5 CS + 4 PC became order 7 CS (2 pieces per case).

## Findings for the framework owner
1. **Reference Number 100 is hard-coded in the workbook and already exists** (earlier runs used it): validation fails on any second run. The framework field `refNumberInput` is *inactive* (status N), so the engine should not fill it; the workbook column is misleading. Use a unique reference or none.
2. **Header is read-only after Order Detail**; a wrong header value needs New Order + confirm (`continue`), which discards the lines.
3. Line save (`rowEditBtn_Save_0`) shows **no toast**; framework event 6 (assertion TSTMSG, active) has nothing to assert unless EXPECTED_MESSAGE is empty.
4. Messages: validation "Validation successfully"; save "Order Save successfully" (framework assertion key ORD_BOOK_SAVE_ASSR); duplicate reference "Cashmemo with document reference number : <n> already exist.".
5. The product field is a type-ahead: real keystrokes, wait for the suggestion, click it; batch fills automatically. Quantity inputs must be set with change events and blur (the app recalculates the gross on change).
6. Selenium `clear` on the quantity inputs causes stale-element errors (the row re-renders); setting the value at page level works.
7. The `Save` button of the order has id `saveBtn`; the wrapper needs a click on its inner dx-button.

## Data created on cnr1dev1
Cash memo (order) **COL26000001995** for outlet 1000000001, PJP 02111-AutomationOB1, net PKR 134,999.00, delivery date 2026-10-05, stock allocated later by the Stock Allocation flow (0013).

---
# TC-OB-02 Book all 8 orders of the framework's Order Booking flow: EXECUTED 2026-09-29
The framework books one order per data row of sheet `Order Booking` (PK 01-08, outlets 1000000001-1000000008); later flows use them (order 04 for editing, order 07 for cancellation, allocation/GIN for all). Orders 02-08 were booked with an in-page routine (type-ahead driven by key events, header without Reference Number).
| PK | Outlet | Order no. | Gross | Discount | Tax | Net | vs workbook |
|---|---|---|---|---|---|---|---|
| 01 | 1000000001 | COL26000001995 | 143,109.13 | -29,971.83 | 21,861.52 | 134,999.00 | = |
| 02 | 1000000002 | COL26000001996 | 143,109.13 | -29,971.83 | 21,234.24 | 134,372.00 | = |
| 03 | 1000000003 | COL26000001997 | 143,109.13 | -29,971.83 | 21,992.03 | 135,129.00 | = |
| 04 (for editing) | 1000000004 | COL26000001998 | 143,109.13 | -29,971.83 | 21,234.24 | 134,372.00 | = |
| 05 | 1000000005 | COL26000001999 | 143,109.13 | -29,971.83 | 0 | 113,137.00 | = |
| 06 | 1000000006 | COL26000002000 | 143,109.13 | -29,971.83 | 0 | 113,137.00 | = |
| 07 (for cancellation) | 1000000007 | COL26000002001 | 143,109.13 | -29,971.83 | 21,397.32 | 134,535.00 | = |
| 08 | 1000000008 | COL26000002002 | 107,960.51 | -16,264.08 | 16,505.36 | 108,202.00 | = |
All 8 pass: validation "Validation successfully", save "Order Save successfully". Tax differs per outlet (tax-exempt / registration flags in the outlet name), as the workbook expects.
Routine notes: one order takes about 2.5 minutes at page speed; the in-page script must run in the background (tool timeout 30 s) and be polled; the "+" (add row) button is found by its label "Add a row" when `addBtn` is absent.

---
# TC-OB-03 Stock Allocation (flow 0013) and Transaction Inquiry after Order Booking (flow 0296): EXECUTED 2026-09-29
Actor: Auto_Multi_Orga (same session).
| # | Step | Result | Verdict |
|---|---|---|---|
| 1 | Navigate to **Order Stock Allocation** (menu title; the framework's search text "Stock Allocation" only finds the group; option DYL_201904, layout 201904) | tabs Unallocated / Allocated; Order Date = today and PJP 02111~AutomationOB1 preselected | Pass |
| 2 | Verify the 8 new orders are allocated | **all 8 (COL26000001995-2002) are already in the Allocated tab**: the app allocates stock when the order is saved | Finding |
| 3 | Unallocated tab: filter Outlet "Aautomation", select all (`checkbox-0`), Allocation (`notrefresh`), accept the browser alert "Are you sure you want to proceed?" | message **"Process completed successfully"** (= workbook `Stock_Allocation_ASSR`); the only order allocated was COL26000001988 (older, outlet 1000000002); Unallocated grid then 0 rows | Pass |
| 4 | Navigate to Transaction Inquiry; Document Type = Sales (default is "Demand Captured from Tele order"), Status All, dates today; Refresh | 24 Sales documents | Pass |
| 5 | Filter Document No "COL26000" and verify header amounts | outlet 1000000006 (COL26000002000): Gross 143,109.13, Discount -29,971.83, Tax 0, Net 113,137 = workbook (`T Inquiry Header Amt Val`); orders 04/05/07/08: net 134,372 / 113,137 / 134,535 / 108,202 = order booking; status **Confirmed** | Pass |
Notes: the browser alert must be accepted through the browser (script clicks cannot); Transaction Inquiry tabs (Detail, Product Wise Discount, Free Quantity, Total Offering, Total Tax, Credit Note Adjustments) are where the framework's remaining amount checks (`T Inquiry Detail Amt Val`, `Charges`, `Total Tax`) read; only the header check was run.
