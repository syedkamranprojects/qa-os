---
option: Stock Inquiry
area: inbound_stock
doc_types: []
screens: [STOCKINQUIRY]
framework_flows: ["02800001", "02810001", "02820001", "02830001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [dispatch_advice, da_loss_approval, order_booking, stock_allocation, goods_issue_note, goods_return_note]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-08
---

# Stock Inquiry and stock balances: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Confidence tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)
Last updated: 2026-10-01 (G11-1 consolidation). Source flows: 02800001 (group 11 seq 9), 02810001 (seq 24), 02820001 (seq 50), 02830001 (seq 60). G11-1 learning walk: snapshots before/after DA 1358, after orders, after GIN 506, after GRN 246.
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.
Updated 2026-10-08: merged the QA team's written answers to the 2026-10-06 review (learning_sessions/2026-10-06_G11-PK_QA_Team_Review.docx); evidence learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx). Tag [stated 2026-10-08 QA Team] = written answer of the QA team. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08: ...)".
Updated 2026-10-08 (follow-up): merged the QA team's answers to the 2026-10-08 follow-up (Q-DS4, Q-SV1, CASHMEMO_EDIT / Q-OE5); evidence learning_sessions/2026-10-08_QA_Team_followup_answers.md. Tag [stated 2026-10-08 QA Team (follow-up)]. Earlier statements are kept; replaced ones carry "(superseded 2026-10-08: ...)".

## 1. Purpose
Stock Inquiry shows, per warehouse, product, batch and stock type, how much stock the distributor holds on a chosen day: what it opened with, what came in, went out, is promised to orders (Allocated) and what remains. It is the stock controller's check that DA, GIN, GRN and adjustments did what they should (superseded 2026-10-01 G11-1: role wording; the check is done by the Maker Auto_Multi_Orga, there is no separate stock-controller role). It is read-only except for the button Generate Opening Balances [observed].
- G11-1: one screen shows the whole stock life of a day: DA approval -> In; order save -> Allocated (Closing down); order cancel before GIN -> Allocated released; GIN approval -> Allocated moves to Out (Closing unchanged); GRN approval -> In [observed 2026-10-01 G11-1].
- G11-2 (2026-10-05, second independent day): the same screen showed the whole day again, now including the end-of-day stock-out: morning 0 rows -> DA approval creates the day (Openings) -> orders Allocated -> GIN Out -> GRN In -> SAN Out [observed 2026-10-05 G11-2, G11-2b].

## 2. Actors and roles
Stock Controller = Auto_Multi_Orga [observed] (superseded 2026-10-01 G11-1: roles are only Maker and Checker; Auto_Multi_Orga reads Stock Inquiry as the **Maker**). Auto_Tssm has no Stock Inquiry menu entry (search returns nothing; 'Stock Master Inquiry', 'Stock Adjustment SAN', 'Order Stock Allocation', 'Stock' do exist for him) [observed 2026-10-01].
- Maker = Auto_Multi_Orga read every G11-1 snapshot (seq 9, 24, 50) [observed 2026-10-01 G11-1]. Checker = Auto_Tssm: no access (see above).
- G11-2/2b: the Maker Auto_Multi_Orga read every snapshot (seq 9, 24, 50, 60); Auto_Tssm still has no Stock Inquiry (confirmed on a second day) [observed 2026-10-05 G11-2].

## 3. Documents and master data
No document. Data: stock balance table snd_tr_ssb_salestock_balance, keyed by balance date, warehouse, product, batch, stock type; quantity columns in three units (qty_1 CS, qty_2 DZ, qty_3 PC are [inferred] from the screen columns) [db]. Stock types (org 010104): 01 Sound, 02 Damaged, 03 Expired, 04 Lost, 11 Variance Warehouse [db]. Warehouses e.g. Auto Main Warehouse, SAN Warehouse A, test wh 1 [observed]. In the snd-schema base DB the balance table holds only type CL rows to 2026-01-30 and none for org 010104; the live environment overlay differs [db].
- G11-1 cycle products at Auto Main Warehouse, 01 - Sound: 62740537, 20050310, 62690363, 20050308, 69997598 [observed 2026-10-01 G11-1].
- Product Name column shows "code - name - price" [observed 2026-10-01 G11-1].

## 4. Inputs: screens and fields
Menu Transaction > Stock > Stock Inquiry (layout 201069, STOCKINQUIRY) [observed].
- Period Type (default DAILY, only DAILY seen), Balance Date (yyyy-MM-dd, default today), Category (default All, 27 entries), Brand (default All); buttons Show Inquiry and Generate Opening Balances.
- Grid, 21 columns: Category, Brand, Product Name, Warehouse, Batch, Stock Type, then Opening, In, Out, Allocated, Closing, each in CS, DZ, PC. Paged, 15 rows per page; row filters rowfilter_asyd (product), rowfilter_warehousedesc, rowfilter_TXT__STOCKTYPEDESC (tick gridFilterCheckbox with a real click). No filters on numeric columns [observed].
- Drill-down checkbox-0 reloads the grid and clears the row filter [observed].
- G11-1 confirmation: filters Period Type* (DAILY), Balance Date, Category, Brand; buttons Show Inquiry, Generate Opening Balances (not clicked); 2026-10-01 grid 39 rows, 3 pages of 15 (was [observed]; now [observed 2026-10-01 G11-1]).
- After clicking a menu item the side menu stays open and covers the page buttons; click the hamburger once to close it [observed 2026-10-01 G11-1].
- G11-2/2b: grid paged 3 pages of 15 on 2026-10-05; the cycle product 62740537 sat on page 3 (filter by product instead of paging). The menu also offers **"Stock Inquiry II"** (DYL_BG1015); seq 60 was read on the normal Stock Inquiry (Period Type DAILY, Balance Date, Category All, Brand empty, Show Inquiry) [observed 2026-10-05 G11-2b]. Generate Opening Balances not clicked on either day.

## 5. Process: the business steps in order
1. [Maker] Navigate to Stock Inquiry.
2. [Maker] Choose Period Type, Balance Date, Category, Brand (defaults are fine), click Show Inquiry. No message; an empty result shows "No data" [observed]. (Actor prefix added 2026-10-01 G11-1.)
3. [Maker] Filter by Product / Warehouse / Stock Type and read In, Out, Allocated, Closing (11:9:02800001 and siblings). (Actor prefix added 2026-10-01 G11-1.)
Never click Generate Opening Balances in a validation flow: it changes data [observed, not clicked].

G11-1 walk (standard vocabulary, trace keys) [observed 2026-10-01 G11-1]:
1. [Maker] Navigate to Stock Inquiry; Choose Period DAILY, Balance Date 2026-10-01, Category All, Brand All; Click Show Inquiry; Record before snapshot of the five products (before 11:5:00740001).
2. [Maker] Show Inquiry after DA 1358 + loss 639 approval; Verify In delta = received per product (11:9:02800001).
3. [Maker] Show Inquiry after six orders booked and one cancelled; Verify Allocated up / Closing down by the open orders (after 11:16:00040001).
4. [Maker] Show Inquiry after GIN 506 approval; Verify Out = issued, Allocated down by the same, Closing unchanged (11:24:02810001).
5. [Maker] Show Inquiry after order edit and cancel after GIN; Verify no change (after 11:29:00840001, 11:31:00850001).
6. [Maker] Show Inquiry after GRN 246 approval; Verify In +19 for 62740537, Out unchanged (11:50:02820001).

G11-2 / G11-2b walk, 2026-10-05 (standard vocabulary, trace keys) [observed 2026-10-05 G11-2, G11-2b]:
1. [Maker] Navigate to Stock Inquiry; Choose Balance Date 2026-10-05; Click Show Inquiry before any DA -> "No data", 0 rows (morning baseline).
2. [Maker] Show Inquiry after DA 1359 + loss 640 approval; Verify 39 rows with Openings, In delta = received (11:9:02800001).
3. [Maker] Show Inquiry after GIN 507 approval; Verify Out = issued, Allocated down, Closing unchanged (11:24:02810001).
4. [Maker] Show Inquiry after GRN 247 approval; Verify In +19, Out unchanged (11:50:02820001).
5. [Maker] Show Inquiry after SAN 96 approval; Verify Out +50, Closing -50 (11:60:02830001).

## 6. Outputs and effects
Live-verified 2026-10-01 (Block 1, 2026-09-30, 39 rows, 3 pages of 15/15/9; Closing/Allocated/Out read for every row): **Closing = Opening + In - Out - Allocated holds on all 39 rows once the units are normalised to base PC with the pack factor from the product name (NNxSIZE)**; literal per-unit comparison holds on 37 rows and fails on 2 only because of PC-to-CS carry (the system borrows a case when allocated PC exceeds opening PC): 20050308 BLUE BAND 32X250G Auto Main (Opening 1978 CS 21 PC, Allocated 39 CS 96 PC, Closing 1936 CS 21 PC: 1978*32+21-(39*32+96) = 61,973 = 1936*32+21) and 20061858 LIFEBUOY 12X180ML IBT (310988 CS 3 PC - 203 CS 9 PC = 310784 CS 6 PC with 12 PC per CS) [observed]. **Automation must assert the identity in base PC, not per column.** Closing is available stock (net of Allocated) on every row [observed]. CS/PC never negative; DZ is 0 in every row and column [observed]. Facts of that day: warehouses Auto Main Warehouse, IBT Main warehouse, test wh 1, SAN Warehouse A; batch always 1-1; stock types 01 Sound (36 rows), 11 Variance (2), 02 Damaged (1: 20080958 SAN Warehouse A, 83 CS 4 PC); no row with any Out (GIN 505 not approved); one row with In (62740537 Auto Main: Opening 80, In 80, Allocated 63, Closing 97) [observed]. Allocated 63 CS equals the GIN 505 line for 62740537; for 20050308 Auto Main allocated 39 CS 96 PC exceeds the GIN 505 line (18 CS 16 PC), so allocation also covers other pending documents [observed].
Read only. Identity observed on 2026-09-30 for 62740537 in Auto Main Warehouse: Closing = Opening + In - Out - Allocated (80 + 80 - 0 - 63 = 97 CS) [observed]. After DA 1350: closing 80 CS equals the received quantity; on a busy day In 176 and Out 96 netted to 80 [observed].

G11-1 day trace, Auto Main Warehouse, 01 - Sound, Balance Date 2026-10-01 (CS/PC) [observed 2026-10-01 G11-1]:

Before DA 1358 approval (16:4x, 39 rows):
| Product | Opening | In | Allocated | Closing |
|---|---|---|---|---|
| 62740537 | 160/0 | 84 (DA 1356 4 + DA 1357 80) | 63/0 | 181/0 |
| 20050310 | 5751/3 | 70 | 85/0 | 5736/3 |
| 62690363 | 6200/94 | 60 | 53/32 | 6207/62 |
| 20050308 | 1978/21 | 50 | 39/96 | 1986/21 |
| 69997598 | 2560/171 | 0 | 0/96 | 2560/75 |

Movements and effects:
| Event | Effect | Evidence |
|---|---|---|
| DA 1358 approved (+ loss 639 approved) | In +80 / +64 / +55 / +50 / +40 (received, not dispatched); Closing up by the same; no Damaged/Lost rows; 39 rows | seq 9 |
| 6 orders booked (2003-2008) | Allocated up and Closing (= ATP) down at each save; 62740537 ATP 261 -> 254 -> ... -> 226 (7 CS per order) | seq 10 |
| Order 2008 cancelled before GIN | its 7 CS of 62740537 released; net Allocated 62740537 63 -> 98, Closing 261 -> 226; 20050310 Allocated 85 -> 100, Closing 5800/3 -> 5785/3; 62690363 53/32 -> 56/34; 20050308 39/96 -> 41/106; 69997598 0/96 -> 0/102 | seq 16 |
| GIN 506 approved | Out = issued (35/0, 15/0, 3/2, 2/10, 0/6); Allocated down by the same (62740537 98 -> 63); **Closing unchanged** (226, 5785/3, 6259/60, 2034/11, 2600/69) | seq 24 |
| Order 2003 edited 7 -> 4 CS after GIN | none (62740537 Out 35, Allocated 63, Closing 226) | seq 29 |
| Order 2007 cancelled after GIN | none (all five SKUs unchanged) | seq 31 |
| GRN 246 approved (19 CS 62740537) | In 164 -> 183 (+19), Out stays 35, Allocated 63, Closing 226 -> 245; other SKUs unchanged; 39 rows | seq 50 |
End of day 62740537: In 183 / Out 35 / Allocated 63 / Closing 245 [observed 2026-10-01 G11-1].
- 20050308 Allocated after the GIN read 42/0 rather than 41/106 - 2/10 = 39/96: same PC total (1418 - 74 = 1344 PC = 42 CS x 32 PC), i.e. the screen re-normalises PC into CS after a movement [observed 2026-10-01 G11-1].
- Allocated after the GIN was back to the pre-order level (62740537 63 = the old GIN 505 reservation still pending from 09-30) [observed 2026-10-01 G11-1].
- Order Booking ATP (Current Stock) = Stock Inquiry Closing; GIN Detail "Current Stock" = Stock Inquiry Closing [observed 2026-10-01 G11-1].
- Closing = Opening + In - Out - Allocated held through all G11-1 snapshots (upgraded from 2026-09-30 evidence to [observed 2026-10-01 G11-1]).

G11-2 / G11-2b day trace, Auto Main Warehouse, 01 - Sound, Balance Date 2026-10-05, product 62740537 (CS) [observed 2026-10-05 G11-2, G11-2b]:

| Event | Opening | In | Out | Allocated | Closing | Evidence |
|---|---|---|---|---|---|---|
| Morning, before any DA | (no row: "No data", 0 rows for the whole day) | | | | | baseline |
| DA 1359 approved (+ loss 640) | 308 | 80 | 0 | 63 | 325 | seq 9 |
| 6 orders booked, 1 cancelled, GIN 507 approved | 308 | 80 | 35 | 63 | 290 | seq 24 |
| GRN 247 approved (19 CS) | 308 | 99 | 35 | 63 | 309 | seq 50 |
| Route settled, slips posted, day closed (seq 51-57) | 308 | 99 | 35 | 63 | 309 (ATP 309 on the SAN line) | seq 58 |
| SAN 96 approved (-50 CS, Stock Adjustment Admin) | 308 | 99 | 85 | 63 | 259 | seq 60 |

- **The DA approval created ALL 39 rows of the day at once, with Openings** (not only the five received SKUs). **Opening = previous working day's Closing + that day's still-Allocated quantity**: 62740537 Opening 308 = 10-01 Closing 245 + 63 still allocated to the old Pending GIN 505 (09-30); 20050308 2076/11, 20050310 5870/3, 62690363 6312/92, 69997598 2600/165 are consistent with the 10-01 closings plus allocations [observed 2026-10-05 G11-2]. The old reservation is carried as Allocated 63 into the new day, so the ATP of new orders is lower than Opening + In by that amount [observed 2026-10-05 G11-2].
- DA 1359 In: 62740537 +80, 20050310 +64 (70 - 6 loss), 62690363 +55 (60 - 5), 20050308 +50, 69997598 +40; loss 640 approved: no Damaged/Lost row, row count 39 (second day) [observed 2026-10-05 G11-2].
- GIN 507: Out 35 = 5 orders x 7 CS, Closing unchanged; GRN 247: In +19, Out unchanged; identical to G11-1 (confirmed on a second day) [observed 2026-10-05 G11-2].
- **Approved SAN (Stock Adjustment Admin, -50 CS) posts as Out of Sound stock**: Out 35 -> 85, Closing 309 -> 259 [observed 2026-10-05 G11-2b].
- **Route settlement, deposit-slip posting and the day close move no stock**: the SAN line showed ATP 309-0-0 = the closing after GRN 247 [observed 2026-10-05 G11-2b].
- Other Auto Main Sound rows at seq 60 (CS/PC): 20050308 Opening 2076/11, In 50, Out 2/10, Allocated 42; 20050310 Opening 5870/3, In 64, Out 15; 62690363 Opening 6312/92, In 55, Out 3/2, Allocated 53/32, Closing 6311/58; 69997598 Opening 2600/165, In 40, Out 0/6, Allocated 0/96, Closing 2640/63 [observed 2026-10-05 G11-2b].
- Closing = Opening + In - Out - Allocated held at every 2026-10-05 snapshot (308 + 99 - 85 - 63 = 259) [observed 2026-10-05 G11-2b]; confirmed on a second day.

G11-3 day trace, Auto Main Warehouse, 01 - Sound, Balance Date 2026-10-06, product 62740537 (CS) [observed 2026-10-06 G11-3]:

| Event | Opening | In | Out | Allocated | Closing | Evidence |
|---|---|---|---|---|---|---|
| DA 1360 approved (+ loss 641) | **0** | 80 | 0 | 0 | 80 | seq 9 (only 5 rows for the day) |
| 6 orders booked (ATP 80 at booking), edits, cancels, re-allocation, GIN 508 approved | 0 | 80 | **32** | 0 | 48 | seq 24 |
| GRN 248 approved (17 CS) | 0 | **97** | 32 | 0 | **65** | seq 50 |
| 10-05 Reattempt 2012 allocated (7 CS) | 0 | 97 | 32 | (7) | 58 (ATP on the SAN line) | seq 58 [Allocated inferred from ATP] |
| GIN 509 approved (2012, 7 CS) + SAN 97 approved (-50 CS) | 0 | 97 | **89** | 0 | **8** | seq 60 |

- **Seq 9 on 2026-10-06 showed only the 5 received rows, all with Opening 0** (no carry-over, no other products, GIN 505's 63 CS not shown) [observed 2026-10-06 G11-3]. This **differs from 2026-10-05** (all 39 rows, Opening = previous Closing + still-Allocated) and **matches the 2026-10-01 morning** pattern. Hypothesis: the previous day's close (settlement Complete + End Of Day) and/or a later Generate Opening Balances changes how openings appear [inferred]; Q-OB2. Expected values for seq 9 (In = received) still matched.
- **Ruling [stated 2026-10-06 QA Team Lead] (Q-OB2 answered)**: Opening **must carry over the previous day's Closing**. If today's Opening is 0 while the previous day had closing stock, it is a **stock carry-over JOB issue in the environment**, not business behaviour; check the previous day's stock. Evidence: 62740537 closed **259** on 2026-10-05 (seq 60) but opened **0** on 2026-10-06, so the carry-over job most likely did not run on cnr1dev1 that night [inferred from the ruling + observed values]. The same applies to the 2026-10-01 morning. (superseded 2026-10-06: the hypothesis "previous day's close and/or Generate Opening Balances decides the pattern" is replaced by this ruling.)
- Other rows at seq 24 (CS/PC): 20050308 In 50, Out 2/10, Closing 47/22; 20050310 In 64, Out 10, Closing 54; 62690363 In 55, Out 3/2, Closing 51/202; 69997598 In 40, Out 0/6, Closing 39/282; Allocated 0 everywhere [observed 2026-10-06 G11-3]. Unchanged at seq 50 and 60 except 62740537 [observed 2026-10-06 G11-3].
- **GIN approval moved Allocated to Out** (Allocated 0 after GIN 508 and again after GIN 509); **GRN approval posted In** (+17); **SAN approval posted Out** (+50) [observed 2026-10-06 G11-3] (third day, same mechanics).
- Closing = Opening + In - Out - Allocated held at every 10-06 snapshot (0 + 97 - 89 - 0 = 8) [observed 2026-10-06 G11-3].

## 7. Statuses and transitions
No document status. Day states: balances exist for a day or not. 2026-09-30 had a grid (39 rows); 2026-10-01 showed "Data grid with 0 rows" (No data) before the DA approval; after DA 1356 was approved it showed 1 row (62740537, Opening 0, In 4, Closing 4) [observed 2026-10-01]. Products without a movement on the new day have no row; the day-roll is not automatic [observed] (superseded 2026-10-01 G11-1: by 16:4x the same day showed 39 rows with Opening balances for products without any movement that day, e.g. 69997598 Opening 2560/171, In 0; 62740537 Opening 160 = 09-30 closing 97 + 09-30 allocated 63, so openings appear rebuilt from the previous day with allocation released; who or what generated them during the day is unknown, someone may have clicked Generate Opening Balances: Q-OB1).
- **New-day rule (2026-10-05, supersedes "the day-roll is not automatic / previous closing is not carried")**: a new day has 0 rows until the first movement; the first movement (here the DA approval) creates the rows of the whole stock catalogue with Opening = previous Closing + still-Allocated [observed 2026-10-05 G11-2]. The 2026-10-01 morning observation (DA 1356 approval created ONE row with Opening 0, rebuilt to 160 later that day) is kept as evidence but does not fit this rule; why that day differed is open (Q-OB2).
- G11-3: the 2026-10-06 first movement (DA 1360 approval) created only the 5 received rows with Opening 0 [observed 2026-10-06 G11-3]; so the "new-day rule" of 2026-10-05 is not universal (superseded 2026-10-06 in part: the rule holds for 10-05 only; 10-01 and 10-06 opened differently; Q-OB2). (superseded again 2026-10-06: the business rule IS carry-over of the previous Closing; days with Opening 0 are an environment fault of the carry-over job [stated 2026-10-06 QA Team Lead].)

## 8. Rules and validations
- Balances are keyed by calendar day. Stock received on 09-29 was not found on 09-30: GIN approval failed with "No stock balance found for products: [20050308, 20050310, 62690363, 62740537, 69997598]" [observed]. G11-1: with stock received the same day the GIN approval succeeded (GIN 506) [observed 2026-10-01 G11-1].
- **The DA approval creates the day's balance row for a received product** (In = received, Opening 0), without Generate Opening Balances [observed 2026-10-01]. The row for 62740537 did not carry the previous day's closing (97 CS on 09-30, Opening 0 on 10-01): a day's Opening is NOT filled by the DA approval; whether Generate Opening Balances carries previous closings is [inferred, never run]. Correction: earlier text said a new day has no rows "until opening balances exist"; a movement creates the row for that product. (Superseded 2026-10-01 G11-1 in part: later the same day Opening 62740537 = 160 = previous closing 97 + previous allocated 63, i.e. opening = previous day's closing with the previous day's allocation released; the generator is unknown, Q-OB1. "The DA approval does not fill Opening" still holds.)
- Approval posts to the received date only; 09-30 stayed unchanged after the 10-01 approval [observed].
- Closing = Opening + In - Out - Allocated, asserted in base PC units (see section 6) [observed]. Contradiction with end_of_day_validations.md resolved in favour of this identity.
- Allocated stock is reserved for orders and is deducted from the closing figure [observed]; orders are auto-allocated at save [observed]. (Upgraded: each order save reserves its normalised quantity at once; Closing/ATP drops by it [observed 2026-10-01 G11-1].)
- Framework check "In CS = DA quantity, Out CS = 0" only holds on a clean day [observed]. G11-1: the seq 9 check expects In 80 while the day's In was 164 [observed 2026-10-01 G11-1].
- **Order cancellation before the GIN releases the reservation** (Allocated down, Closing up) [observed 2026-10-01 G11-1].
- **GIN approval moves Allocated to Out; Closing does not change at GIN approval** (it already went down when the orders reserved stock) [observed 2026-10-01 G11-1].
- **After the GIN, editing, cancelling or rescheduling an order does not move stock**; the undelivered quantity stays "out" until the GRN [observed 2026-10-01 G11-1].
- **GRN approval posts the returned quantity as In (Sound); it does not reduce Out** [observed 2026-10-01 G11-1].
- **DA loss approval creates no stock row** (no Damaged/Lost row) [observed 2026-10-01 G11-1].
- Received, not dispatched, quantity is what enters In [observed 2026-10-01 G11-1].
- G11-2 (supersedes the "previous closing is not carried" statements above): **previous closings ARE carried**: the first movement of a new day creates every row with Opening = previous working day's Closing + that day's still-Allocated quantity (62740537: 245 + 63 = 308) [observed 2026-10-05 G11-2]. Stock received on an earlier day is therefore available on a later day once the day's rows exist; the 09-30 GIN refusal ("No stock balance found for products") happened while the new day had no rows. Whether a GIN approval as the FIRST movement of a day also creates the rows was not tested [unknown; Q-OB2].
- Reservations of documents left Pending on an earlier day (GIN 505 of 09-30) stay Allocated on later days (63 CS on 10-01 and 10-05) [observed 2026-10-05 G11-2].
- **Approved SAN stock-out = Out** of the chosen stock type (Sound) on approval [observed 2026-10-05 G11-2b].
- Route Settlement, deposit-slip posting and the PJP day close have no stock effect [observed 2026-10-05 G11-2b].
- Rules of G11-1 (DA In = received, cancel before GIN releases, GIN Allocated -> Out with Closing unchanged, GRN In with Out unchanged, loss approval no row) all confirmed on 2026-10-05 [observed 2026-10-05 G11-2].
- G11-3: with Opening 0 the day's ATP equals only the day's receipts (62740537 ATP 80 at booking) [observed 2026-10-06 G11-3]; earlier days' closings were not usable that day.
- G11-3: an extra allocation (Reattempt order) lowers the ATP before its GIN is approved (65 -> 58) [observed ATP 2026-10-06 G11-3].
- QA team 2026-10-08 (rule 6, confirmed): GIN approval moves Allocated to Out; GRN approval posts In; SAN approval posts Out. **Stock Reconciliation**: the current day's stock is reconciled and cleared so that the correct opening stock is carried forward to the next day [stated 2026-10-08 QA Team].
- QA team 2026-10-08 (rule 7, confirmed): **Stock Carry Forward**: the closing stock of the previous working day is carried forward as the opening stock of the next working day [stated 2026-10-08 QA Team] (confirms the 2026-10-06 ruling; Opening 0 after a day with closing stock remains the environment issue E-G11-3-1).
- QA team 2026-10-08 (Q58): stock is added or deducted on the document's approval action [stated 2026-10-08 QA Team].
- QA team 2026-10-08 (Q-OE5): an edit after the GIN approval (CASHMEMO_EDIT = Y) is stated to reduce the approved GIN quantity [stated 2026-10-08 QA Team]; three walks saw no Stock Inquiry movement [observed]; open. (superseded 2026-10-08: the follow-up answer says there is NO stock movement when a cash memo is edited after the GIN is completed [stated 2026-10-08 QA Team (follow-up)]; this matches the three walks; the cut quantity comes back as In on the GRN. Q-OE5 closed, contradiction 28 resolved.)
- QA team 2026-10-08 (follow-up, Q-SV1 answered): every stock transaction must be reflected in Stock Inquiry in its own column and in the balance: **Dispatch Advice -> In; Return Document -> Out; GIN -> Out; GRN -> In; SAN -> addition or deduction** (SAN types Stock Adjustment Admin, Warehouse Transfer) [stated 2026-10-08 QA Team (follow-up)]. Which document "Return Document" is (a purchase return to the company?) is open (Q-SV2); sales returns came back as In via the GRN on three days [observed 2026-10-01, 10-05, 10-06].

## 9. Messages
No toast on Show Inquiry. Grid text "No data" when empty [observed]. G11-1: no toast on any of the six Show Inquiry clicks [observed 2026-10-01 G11-1].
- G11-2/2b: no toast on any Show Inquiry click; "No data" on the morning baseline [observed 2026-10-05 G11-2].

## 10. Dependencies
Reads results of DA (In), GIN (Out), GRN (In), SAN, order allocation (Allocated). Why keyed by day: stock is a daily snapshot per warehouse so each business day starts from an opening balance [inferred]. A cycle that creates and issues stock must run in one calendar day [observed]. Orders, GIN, returns: see the orders/delivery analyst's pages.
- G11-1 confirmation: DA In, order Allocated, GIN Out and GRN In all posted to 2026-10-01 and were read on one Balance Date (upgraded to [observed 2026-10-01 G11-1]). Route Settlement additionally requires all previous working days to be closed ("Following previous days not closed! Please close date. 2026-09-30"); how a day is closed is open (Q-RS1) and may relate to how openings are produced (Q-OB1) [observed 2026-10-01 G11-1].
- Hands Closing (= ATP) to Order Booking and GIN Detail [observed 2026-10-01 G11-1].
- G11-2: the Opening of a day depends on the previous working day's Closing and its still-Allocated reservations (old Pending GINs), so a same-day check inherits other documents' reservations [observed 2026-10-05 G11-2].
- G11-2b: hands Closing (= ATP) to the SAN line ("Current Stock (ATP)") as well [observed 2026-10-05 G11-2b].

## 11. Test design hints
- Positive: Show Inquiry for today after an approved DA; closing change equals received quantity; Opening/In/Out/Allocated/Closing identity for each row, computed in base PC units (pack factor from the product name) so carry rows do not give false failures.
- Negative: Balance Date in the future or a day with no balances (expect No data); Auto_Tssm cannot open the screen; stock type filter Damaged shows none unless losses are posted.
- Boundary: first day (Opening 0), CS vs PC conversion, rows beyond page 1.
- Traps: use before/after snapshots, not absolute In/Out; take product filter before reading row_1_*; framework screenshot assertion passes with no values checked; never include Generate Opening Balances.
- G11-1 additions [observed 2026-10-01 G11-1]:
  - Positive (business effects, one per document): DA approval -> In delta = received; order save -> Allocated delta = normalised order qty and Closing delta = minus the same; cancel before GIN -> reverse; GIN approval -> Out delta = issued, Allocated delta = minus issued, Closing delta 0; GRN approval -> In delta = returned, Out delta 0.
  - Negative (no-effect checks): loss approval -> no Damaged/Lost row; order edit or cancel after GIN -> no change; these are good regression checks because a wrong implementation would move stock.
  - Boundary: PC re-normalisation (20050308 Allocated 41/106 shown later as 42/0): compare in base PC; Opening may be 0 in the morning and non-zero later the same day.
  - Traps: **the framework's absolute In assertion fails on a busy day** (In 164 vs expected 80); Opening is not stable within a day (Q-OB1), so do not assert Opening in a same-day check; GIN approval leaves Closing unchanged, so a "Closing down after GIN" assertion is wrong; GRN posts In, not a reduction of Out, so "Out back to 0 after GRN" is wrong.
- G11-2/2b additions [observed 2026-10-05 G11-2, G11-2b]:
  - Positive (new day): before the first movement assert 0 rows; after the DA approval assert 39 rows (whole catalogue) and Opening = previous Closing + previous still-Allocated per row (in base PC).
  - Positive (SAN): after an approved Stock Adjustment Admin of -N, assert Out delta = N and Closing delta = -N, In unchanged.
  - Negative (no effect): Route Settlement, posting and the PJP day close leave In/Out/Allocated/Closing unchanged.
  - Trap: **Allocated on a new day may contain reservations of old Pending documents** (63 CS of GIN 505 from 09-30); assert deltas, never absolute Allocated.
  - Trap: the G11-1 hint "Opening is not stable within a day" came from the 10-01 anomaly; on 10-05 Opening was stable all day once created (308 from 09:5x to seq 60). Keep using deltas until Q-OB2 is answered.
  - Trap (framework drift): seq 9 expects In 80 absolute; on 10-05 In was 80 because DA 1359 was the only receipt, so the check passed by coincidence (see FRAMEWORK_DRIFT.md).
- G11-3 trap: whether the day opens with carried openings or with Opening 0 differs between days (10-05 vs 10-06); stock checks must be before/after deltas (Q-SV1), never absolute openings [observed 2026-10-06 G11-3]. (2026-10-08: Q-SV1 answered: per-transaction deltas [stated 2026-10-08 QA Team (follow-up)].)
- Pre-check (2026-10-06 ruling [stated 2026-10-06 QA Team Lead]): before a cycle, compare today's first Opening with yesterday's Closing; Opening 0 after closing stock = carry-over job not run (environment issue) -> raise it before testing; a test asserting carry-over should expect Opening = previous Closing.
- QA team 2026-10-08 (follow-up, Q-SV1 answered) [stated 2026-10-08 QA Team (follow-up)]: assert every stock transaction as its own movement, not fixed daily totals: take a before snapshot of the product row, then assert the delta in the right column and the balance (Closing): DA approval In +received; GIN approval Out +issued (Allocated -issued, Closing 0); GRN approval In +Actual; SAN approval Out +N for a deduction or In +N for an addition (Stock Adjustment Admin, Warehouse Transfer); Return Document Out +returned (which document: Q-SV2). An after-GIN cash memo edit: assert NO movement at the edit, then In on the GRN.

## 12. Open questions
Q: What exactly does Generate Opening Balances do and who may run it (it may still serve products NOT received that day and carry prior closings; unknown)? | Default: creates the selected day's opening rows from the prior day's closing | Evidence: never clicked; the DA approval created a row without it. (G11-1: openings appeared during the day = previous closing + previous allocated; see Q-OB1.)
ANSWERED 2026-10-01 (Q11): Closing is net of Allocated; identity holds on 39 of 39 rows in base PC units [observed].
Q: Other Period Types than DAILY? | Default: only DAILY | Evidence: popup read ambiguous.
Q: Do DZ columns apply to any product here? | Default: always 0 | Evidence: all seen rows 0. (G11-1: DZ is skipped in Order Booking for these SKUs; still 0 everywhere [observed 2026-10-01 G11-1].)
Q-OB1: Who or what generated the 2026-10-01 opening balances during the day (morning: none; 16:40: present, 62740537 Opening 160 = 97 + 63)? | Default: unknown; do not assert Opening in same-day checks | Class: B | Evidence: G11-1 before snapshot [observed 2026-10-01 G11-1]. **-> ANSWERED 2026-10-05**: openings are created by the first movement of the day (DA approval) = previous Closing + still-Allocated (see stock_inquiry_and_balances.md, OPEN_QUESTIONS.md).
Q-RS1: How is a working day closed (which screen/process), and may 2026-09-30 be closed on cnr1dev1? | Default: ask BA before closing | Class: C | Evidence: Route Settlement "Following previous days not closed! Please close date. 2026-09-30" [observed 2026-10-01 G11-1]. **-> PARTLY ANSWERED 2026-10-05**: day close = PJP Daily Inquiry Update, End Of Day + Complete (Current Status E); detailed procedure pending from the QA lead.
ANSWERED 2026-10-01 (Q31 part, G11-1): GIN approval = Out up / Allocated down / Closing unchanged; GRN approval = In up (Sound) / Out unchanged; order cancel before GIN releases Allocated; edit/cancel after GIN no effect [observed 2026-10-01 G11-1]. Sales-return stock effect: returned qty comes back via the GRN (see goods_return_note.md).
ANSWERED 2026-10-05 (Q-OB1, G11-2): openings are created by the first movement of the day (the DA approval), for the whole catalogue, as previous Closing + previous still-Allocated; nothing needs Generate Opening Balances [observed 2026-10-05 G11-2]. Supersedes "previous closing is not carried".
Q-OB2: Why did the first DA approval of 2026-10-01 create a single row with Opening 0 (rewritten to 160 = 97 + 63 later that day), while on 2026-10-05 it created all 39 rows with Openings at once; and does a non-DA first movement (GIN approval, SAN) create the day's rows the same way? | Default: rule of 2026-10-05 (first movement creates all rows with carried openings); treat 10-01 as an environment anomaly | Class: B | Evidence: 10-01 morning 1 row Opening 0 vs 10-05 39 rows Opening 308 [observed 2026-10-01, 2026-10-05].
Q-RS1 (day close) PARTLY ANSWERED 2026-10-05: a day is closed on PJP Daily Inquiry Update (Mark Status End Of Day + DSR Files Status Complete); it moved no stock [observed 2026-10-05 G11-2b]. See pjp_daily_inquiry_update.md.
- Q-OB2 evidence 2026-10-06: the DA 1360 approval created only 5 rows, Opening 0, no carry of 10-05's closings or GIN 505's allocation [observed 2026-10-06 G11-3]; 2 of 3 walk days (10-01, 10-06) show this pattern, so the 10-05 default is weakened. Hypothesis to ask the QA Team Lead: the previous day's settlement + End Of Day close, or a Generate Opening Balances run, decides it. Still open (needs the QA Team Lead). **-> ANSWERED 2026-10-06** [stated 2026-10-06 QA Team Lead]: Opening must carry the previous day's Closing; Opening 0 after a day with closing stock = the environment's stock carry-over job did not run (environment issue, not business behaviour). Follow-up: 10-05 Closing 259 vs 10-06 Opening 0 for 62740537 -> job likely not run on cnr1dev1; report to the environment owner.
- 2026-10-08 [stated 2026-10-08 QA Team]: carry forward and reconciliation confirmed (rules 6, 7); stock moves on approval (Q58). BA14 (Generate Opening Balances) is not addressed by the answers and stays open.
- 2026-10-08 (follow-up) [stated 2026-10-08 QA Team (follow-up)]: Q-SV1 answered (per-transaction movement in the right column + balance); Q-OE5 answered (no movement at an after-GIN cash memo edit).
Q-SV2 (new 2026-10-08): Which document is the "Return Document" that the QA team says posts Out (a purchase return of stock to the company / supplier?) | Default: a return to the company (purchase return), not the sales return, which comes back In via the GRN | Class: B | Evidence: follow-up answer [stated 2026-10-08 QA Team (follow-up)]; returns 713 / 714 / 715 came back In on GRNs 246-248 [observed]; LIVE_LEARNING_CHECKLIST L45.

## 13. Sources
framework_atlas/flows/02800001.md, 02810001.md, 02820001.md, 02830001.md; framework_flows/TC-DA-01_executed.md (TC-DA-02), DISPATCH_ADVICE.md; ui.md section "Verified in the group 11 replay"; runs/PILOT-DA-GIN/20260930-1615/exec/stock_inquiry_harvest.json, learning_block1.json, learning_block3b.json (live 2026-10-01); DB snd_tr_ssb_salestock_balance, snd_pr_stt_sku_stocktype.
- G11-1 learning walk: learning_sessions/2026-10-01_G11-PK_session1_log.md (Stock Inquiry BEFORE DA 1358, seq 9, seq 10, seq 16, seq 24, seq 29, seq 31, seq 50, seq 51) and learning_sessions/2026-10-01_G11-PK_session1_report.md (§3 rules 1-3, 6-7; §5 opening-balance contradiction; §8 Q-OB1, Q-RS1).
- G11-2 / G11-2b: learning_sessions/2026-10-05_G11-PK_session2_log.md (morning baseline, seq 9, 24, 50) and learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md (seq 58 ATP, seq 60).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 9, 24, 50, 58, 60).

- QA team written answers 2026-10-08: learning_sessions/2026-10-08_QA_Team_Review_answers.md (verbatim answers; filled docx apps/snd/knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx) (rules 6, 7; Q58).
- QA team follow-up answers 2026-10-08: learning_sessions/2026-10-08_QA_Team_followup_answers.md (Q-SV1, CASHMEMO_EDIT / Q-OE5).
