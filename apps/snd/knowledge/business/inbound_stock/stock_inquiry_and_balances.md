# Stock Inquiry and stock balances: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Confidence tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 02800001 (group 11 seq 9), 02810001 (seq 24), 02820001 (seq 50), 02830001 (seq 60).

## 1. Purpose
Stock Inquiry shows, per warehouse, product, batch and stock type, how much stock the distributor holds on a chosen day: what it opened with, what came in, went out, is promised to orders (Allocated) and what remains. It is the stock controller's check that DA, GIN, GRN and adjustments did what they should. It is read-only except for the button Generate Opening Balances [observed].

## 2. Actors and roles
Stock Controller = Auto_Multi_Orga [observed]. Auto_Tssm has no Stock Inquiry menu entry (search returns nothing; 'Stock Master Inquiry', 'Stock Adjustment SAN', 'Order Stock Allocation', 'Stock' do exist for him) [observed 2026-10-01].

## 3. Documents and master data
No document. Data: stock balance table snd_tr_ssb_salestock_balance, keyed by balance date, warehouse, product, batch, stock type; quantity columns in three units (qty_1 CS, qty_2 DZ, qty_3 PC are [inferred] from the screen columns) [db]. Stock types (org 010104): 01 Sound, 02 Damaged, 03 Expired, 04 Lost, 11 Variance Warehouse [db]. Warehouses e.g. Auto Main Warehouse, SAN Warehouse A, test wh 1 [observed]. In the snd-schema base DB the balance table holds only type CL rows to 2026-01-30 and none for org 010104; the live environment overlay differs [db].

## 4. Inputs: screens and fields
Menu Transaction > Stock > Stock Inquiry (layout 201069, STOCKINQUIRY) [observed].
- Period Type (default DAILY, only DAILY seen), Balance Date (yyyy-MM-dd, default today), Category (default All, 27 entries), Brand (default All); buttons Show Inquiry and Generate Opening Balances.
- Grid, 21 columns: Category, Brand, Product Name, Warehouse, Batch, Stock Type, then Opening, In, Out, Allocated, Closing, each in CS, DZ, PC. Paged, 15 rows per page; row filters rowfilter_asyd (product), rowfilter_warehousedesc, rowfilter_TXT__STOCKTYPEDESC (tick gridFilterCheckbox with a real click). No filters on numeric columns [observed].
- Drill-down checkbox-0 reloads the grid and clears the row filter [observed].

## 5. Process: the business steps in order
1. [Stock Controller] Navigate to Stock Inquiry.
2. Choose Period Type, Balance Date, Category, Brand (defaults are fine), click Show Inquiry. No message; an empty result shows "No data" [observed].
3. Filter by Product / Warehouse / Stock Type and read In, Out, Allocated, Closing (11:9:02800001 and siblings).
Never click Generate Opening Balances in a validation flow: it changes data [observed, not clicked].

## 6. Outputs and effects
Live-verified 2026-10-01 (Block 1, 2026-09-30, 39 rows, 3 pages of 15/15/9; Closing/Allocated/Out read for every row): **Closing = Opening + In - Out - Allocated holds on all 39 rows once the units are normalised to base PC with the pack factor from the product name (NNxSIZE)**; literal per-unit comparison holds on 37 rows and fails on 2 only because of PC-to-CS carry (the system borrows a case when allocated PC exceeds opening PC): 20050308 BLUE BAND 32X250G Auto Main (Opening 1978 CS 21 PC, Allocated 39 CS 96 PC, Closing 1936 CS 21 PC: 1978*32+21-(39*32+96) = 61,973 = 1936*32+21) and 20061858 LIFEBUOY 12X180ML IBT (310988 CS 3 PC - 203 CS 9 PC = 310784 CS 6 PC with 12 PC per CS) [observed]. **Automation must assert the identity in base PC, not per column.** Closing is available stock (net of Allocated) on every row [observed]. CS/PC never negative; DZ is 0 in every row and column [observed]. Facts of that day: warehouses Auto Main Warehouse, IBT Main warehouse, test wh 1, SAN Warehouse A; batch always 1-1; stock types 01 Sound (36 rows), 11 Variance (2), 02 Damaged (1: 20080958 SAN Warehouse A, 83 CS 4 PC); no row with any Out (GIN 505 not approved); one row with In (62740537 Auto Main: Opening 80, In 80, Allocated 63, Closing 97) [observed]. Allocated 63 CS equals the GIN 505 line for 62740537; for 20050308 Auto Main allocated 39 CS 96 PC exceeds the GIN 505 line (18 CS 16 PC), so allocation also covers other pending documents [observed].
Read only. Identity observed on 2026-09-30 for 62740537 in Auto Main Warehouse: Closing = Opening + In - Out - Allocated (80 + 80 - 0 - 63 = 97 CS) [observed]. After DA 1350: closing 80 CS equals the received quantity; on a busy day In 176 and Out 96 netted to 80 [observed].

## 7. Statuses and transitions
No document status. Day states: balances exist for a day or not. 2026-09-30 had a grid (39 rows); 2026-10-01 showed "Data grid with 0 rows" (No data) before the DA approval; after DA 1356 was approved it showed 1 row (62740537, Opening 0, In 4, Closing 4) [observed 2026-10-01]. Products without a movement on the new day have no row; the day-roll is not automatic [observed].

## 8. Rules and validations
- Balances are keyed by calendar day. Stock received on 09-29 was not found on 09-30: GIN approval failed with "No stock balance found for products: [20050308, 20050310, 62690363, 62740537, 69997598]" [observed].
- **The DA approval creates the day's balance row for a received product** (In = received, Opening 0), without Generate Opening Balances [observed 2026-10-01]. The row for 62740537 did not carry the previous day's closing (97 CS on 09-30, Opening 0 on 10-01): a day's Opening is NOT filled by the DA approval; whether Generate Opening Balances carries previous closings is [inferred, never run]. Correction: earlier text said a new day has no rows "until opening balances exist"; a movement creates the row for that product.
- Approval posts to the received date only; 09-30 stayed unchanged after the 10-01 approval [observed].
- Closing = Opening + In - Out - Allocated, asserted in base PC units (see section 6) [observed]. Contradiction with end_of_day_validations.md resolved in favour of this identity.
- Allocated stock is reserved for orders and is deducted from the closing figure [observed]; orders are auto-allocated at save [observed].
- Framework check "In CS = DA quantity, Out CS = 0" only holds on a clean day [observed].

## 9. Messages
No toast on Show Inquiry. Grid text "No data" when empty [observed].

## 10. Dependencies
Reads results of DA (In), GIN (Out), GRN (In), SAN, order allocation (Allocated). Why keyed by day: stock is a daily snapshot per warehouse so each business day starts from an opening balance [inferred]. A cycle that creates and issues stock must run in one calendar day [observed]. Orders, GIN, returns: see the orders/delivery analyst's pages.

## 11. Test design hints
- Positive: Show Inquiry for today after an approved DA; closing change equals received quantity; Opening/In/Out/Allocated/Closing identity for each row, computed in base PC units (pack factor from the product name) so carry rows do not give false failures.
- Negative: Balance Date in the future or a day with no balances (expect No data); Auto_Tssm cannot open the screen; stock type filter Damaged shows none unless losses are posted.
- Boundary: first day (Opening 0), CS vs PC conversion, rows beyond page 1.
- Traps: use before/after snapshots, not absolute In/Out; take product filter before reading row_1_*; framework screenshot assertion passes with no values checked; never include Generate Opening Balances.

## 12. Open questions
Q: What exactly does Generate Opening Balances do and who may run it (it may still serve products NOT received that day and carry prior closings; unknown)? | Default: creates the selected day's opening rows from the prior day's closing | Evidence: never clicked; the DA approval created a row without it.
ANSWERED 2026-10-01 (Q11): Closing is net of Allocated; identity holds on 39 of 39 rows in base PC units [observed].
Q: Other Period Types than DAILY? | Default: only DAILY | Evidence: popup read ambiguous.
Q: Do DZ columns apply to any product here? | Default: always 0 | Evidence: all seen rows 0.

## 13. Sources
framework_atlas/flows/02800001.md, 02810001.md, 02820001.md, 02830001.md; framework_flows/TC-DA-01_executed.md (TC-DA-02), DISPATCH_ADVICE.md; ui.md section "Verified in the group 11 replay"; runs/PILOT-DA-GIN/20260930-1615/exec/stock_inquiry_harvest.json, learning_block1.json, learning_block3b.json (live 2026-10-01); DB snd_tr_ssb_salestock_balance, snd_pr_stt_sku_stocktype.
