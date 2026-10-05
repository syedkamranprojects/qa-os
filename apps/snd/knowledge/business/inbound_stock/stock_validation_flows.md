---
option: Stock validation flows (after DA, GIN, GRN; opening/closing)
area: inbound_stock
doc_types: []
screens: [STOCKINQUIRY]
framework_flows: ["02800001", "02810001", "02820001", "02830001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [stock_inquiry_and_balances, dispatch_advice, da_loss_approval, goods_issue_note, goods_return_note]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-01
---

# Stock validation flows: how they work (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Confidence tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)
Last updated: 2026-10-01 (G11-1 consolidation). Source flows: 02800001 (seq 9, after DA), 02810001 (seq 24, after GIN), 02820001 (seq 50, after GRN), 02830001 (seq 60, opening and closing). Inactive: 02840001, 02850001, 02860001 (after SAN), 02950001 / 03500001 (OTC stock out and SAN approval). G11-1 learning walk: seq 9, 24 and 50 walked; seq 60 not walked.

## 1. Purpose
These flows are checkpoints in the Daily Cycle: after a stock-moving document is approved, the stock controller opens Stock Inquiry and checks that the stock figures moved as expected (superseded 2026-10-01 G11-1: role wording; the Maker Auto_Multi_Orga opens Stock Inquiry, there is no stock-controller role). They are tests of stock, not business operations (read-only). See stock_inquiry_and_balances.md for the screen and the meaning of columns.

## 2. Actors and roles
Auto_Multi_Orga (serial 35) with a user switch before each (seq 9, 24, 50, 60) because the preceding approval is done by Auto_Tssm [atlas].
- G11-1: Maker = Auto_Multi_Orga ran seq 9, 24 and 50, each after a user switch from the Checker Auto_Tssm (DA/loss approval, GIN approval, GRN approval) [observed 2026-10-01 G11-1] (was [atlas]). The Checker has no Stock Inquiry menu entry [observed 2026-10-01].

## 3. Documents and master data
None created. Reads case-data sheets per flow: Stock_Val_After_DA_PAK1/2/3, Stock_val_after_GIN_PAK1/2/3, Stock_Val_after_GRN_PAK1/2/3, Open_Close_Stock_Val/2/3 and screenshot_ASSR [atlas]. Expected values in the workbook were product 62740537, Auto Main Warehouse, 01 - Sound, In CS 80, Out CS 0, In PC 0, Out PC 0 [observed].
- G11-1: the seq 9 framework criteria are Period DAILY / Balance Date / Category All / Brand All, row filter 62740537 + Auto Main Warehouse + 01 - Sound, assertion **absolute** In CS = 80 [observed 2026-10-01 G11-1].

## 4. Inputs: screens and fields
Three screens each: (1) criteria: Period Type, Balance Date, Category, Brand, click Show Inquiry; (2) grid row filters Auto (product), Auto1 (warehouse), Auto2 (stock type), click first row checkbox; (3) read cells: In CS, Out CS, In PC, Out PC (flows 9, 24, 50) or Opening CS, Closing CS, Opening PC, Closing PC (flow 60), click row_1_closing_pc to expand, compare to workbook (event 0007) [atlas]. The GIN flow waits 2 s around the expand click [atlas].
- G11-1 confirmation of screen (1) labels: Period Type*, Balance Date, Category, Brand, Show Inquiry [observed 2026-10-01 G11-1] (was [atlas]).

## 5. Process: the business steps in order
1. [Maker] Login as Stock Controller (switch point). (Superseded 2026-10-01 G11-1: the role is Maker; read as "[Maker] Login as Auto_Multi_Orga (switch point)".)
2. [Maker] Navigate to Stock Inquiry; Show Inquiry for the chosen date. (Actor prefix added 2026-10-01 G11-1.)
3. [Maker] Filter product / warehouse / stock type; open the row. (Actor prefix added 2026-10-01 G11-1.)
4. [Maker] Verify values against expected. After DA: In = received; after GIN: Out/Allocated reflect the issue; after GRN: In rises by the return; flow 60: Opening and Closing for the day. (Actor prefix added 2026-10-01 G11-1.)
Trace keys 11:9:02800001, 11:24:02810001, 11:50:02820001, 11:60:02830001.

G11-1 walk (standard vocabulary, trace keys) [observed 2026-10-01 G11-1]:
1. [Maker] Login (switch from Checker after DA 1358 + loss 639 approval) (11:9:02800001).
2. [Maker] Navigate to Stock Inquiry; Choose Balance Date 2026-10-01; Click Show Inquiry; Filter 62740537 / Auto Main Warehouse / 01 - Sound; Verify In 84 -> 164 (+80 = DA 1358 received) (11:9:02800001).
3. [Maker] Login (switch from Checker after GIN 506 approval); Navigate to Stock Inquiry; Verify Out 35/0, Allocated 98 -> 63, Closing 226 unchanged for 62740537 (and Out = issued for the other four SKUs) (11:24:02810001).
4. [Maker] Login (switch from Checker after GRN 246 approval); Navigate to Stock Inquiry; Verify 62740537 In 164 -> 183 (+19), Out 35 unchanged, Closing 226 -> 245 (11:50:02820001).

## 6. Outputs and effects
None (read only). They produce a pass/fail on stock correctness and screenshots.
- G11-1 results [observed 2026-10-01 G11-1]:
  | Seq | Check | Observed | Framework assertion would |
  |---|---|---|---|
  | 9 | after DA | In delta +80 / +64 / +55 / +50 / +40 = received; no Damaged/Lost rows; 39 rows | FAIL: expects absolute In 80, day In 164 |
  | 24 | after GIN | Out = 35/0, 15/0, 3/2, 2/10, 0/6 (= GIN issued); Allocated down by the same; Closing unchanged | pass for Out only if no earlier GIN was approved that day |
  | 50 | after GRN | 62740537 In +19, Out unchanged 35, Closing +19 | FAIL if it expects absolute In / Out = 0 |

## 7. Statuses and transitions
Not applicable.

## 8. Rules and validations
- Expected In/Out are absolute values from the workbook: valid only on a clean day [observed: In 176, Out 96 netted to closing 80]. G11-1: reconfirmed, expected In 80 vs day In 164 [observed 2026-10-01 G11-1].
- Date in workbook is hard-coded (2026-09-21): must be today [observed].
- Live-verified 2026-10-01: for a product received today, the day's row is created by the DA approval with Opening 0, so In = received and Closing = received hold on a day without other movements; assert the identity Closing = Opening + In - Out - Allocated in base PC units [observed]. (Superseded 2026-10-01 G11-1 in part: later the same day the rows carried Opening balances (62740537 Opening 160), so "Closing = received" does not hold even for the first DA once openings exist; the identity still holds.)
- Drill-down checkbox-0 clears the row filter, so row_1_* then points at the first unfiltered row [observed].
- Screenshot assertion group (screenshot_ASSR) checks no message text [atlas].
- After GIN approval the correct expectation is Out = issued and Closing unchanged [observed 2026-10-01 G11-1].
- After GRN approval the correct expectation is In up by the GRN quantity and Out unchanged [observed 2026-10-01 G11-1].
- Approved DA losses add no Damaged/Lost row, so no check for them belongs in seq 9 [observed 2026-10-01 G11-1].

## 9. Messages
None on Show Inquiry; "No data" for an empty day [observed]. G11-1: no message on seq 9, 24, 50 [observed 2026-10-01 G11-1].

## 10. Dependencies
Needs the preceding document approved the same calendar day (balances keyed by date). A new day shows No data until a movement creates the row (the DA approval does, observed 2026-10-01) or opening balances are generated; GIN approval on a new day for stock received the day before failed with "No stock balance found for products" [observed]; previous-day closings are not carried automatically [observed] (superseded 2026-10-01 G11-1: by 16:4x opening balances = previous closing + previous allocated were present for all 39 rows; whether this is automatic or someone ran Generate Opening Balances is open, Q-OB1).
- G11-1: seq 9 needs seq 5 and 7 (DA + loss approval); seq 24 needs seq 23 (GIN approval); seq 50 needs seq 49 (GRN approval); all done the same day [observed 2026-10-01 G11-1].

## 11. Test design hints
- Positive: after each DA / GIN / GRN, closing changes by exactly the document quantity (before/after snapshot).
- Negative: wrong product filter, date with no balances, user without the screen (Auto_Tssm).
- Boundary: busy day with several movements; PC vs CS; Damaged and Lost rows after loss approval (currently absent).
- Traps: framework run can be green while only screenshots are compared; absolute In/Out checks fail on busy days; never run Generate Opening Balances in these flows.
- G11-1 additions [observed 2026-10-01 G11-1]:
  - Correction to the first positive hint: "closing changes by exactly the document quantity" is right for DA and GRN, but **after GIN approval Closing does not change** (Allocated -> Out); assert Out delta = issued and Allocated delta = minus issued instead.
  - Positive: take a before snapshot of In/Out/Allocated/Closing right before each approval and assert deltas: DA In + received; GIN Out + issued, Allocated - issued, Closing 0; GRN In + returned, Out 0.
  - Negative: loss approval -> no Damaged/Lost row (assert absence); order edit/cancel after GIN -> no delta.
  - Boundary: Damaged and Lost rows after loss approval are absent by design (not a defect); PC re-normalisation (20050308 Allocated 41/106 then 42/0) means compare in base PC.
  - Traps: **the framework's absolute-In assertion fails on a busy day** (seq 9 expected 80, actual 164); **GRN posts In, not a reduction of Out**, so an "Out back to 0" expectation is wrong; Opening is not stable within a day (Q-OB1), so flow 60 cannot assert Opening = 0.

## 12. Open questions
Q: Should validation compare absolute values or the change from a pre-snapshot? | Default: change from a snapshot | Evidence: busy-day failure. (G11-1: second busy-day failure, In 164 vs 80 [observed 2026-10-01 G11-1]; kept for the framework owner as drift, report §7.)
Q: What should flow 60 Opening/Closing expect after a new day starts? | Default: Opening = 0 for a product first moved today, prior Closing only after Generate Opening Balances | Evidence: 62740537 closed 97 CS on 09-30 and opened 0 on 10-01 after the DA approval. (G11-1: the same row showed Opening 160 = 97 + 63 later that day; default changed to "Opening = previous Closing + previous Allocated once openings exist; do not assert Opening until Q-OB1 is answered".)
Q: Are the SAN stock validations (02850001, 02860001) part of the cycle? | Default: no, inactive | Evidence: status N.
Q-OB1: Who or what generated the 2026-10-01 opening balances during the day (morning: none; 16:40: present)? | Default: unknown; do not assert Opening | Class: B | Evidence: G11-1 before snapshot [observed 2026-10-01 G11-1].
Q-SV1: May the framework stock checks (seq 9, 24, 50) be changed to before/after deltas (needs a pre-snapshot step)? | Default: yes, deltas | Class: C | Evidence: report §7 framework drift "Stock validation asserts absolute In" [observed 2026-10-01 G11-1].

## 13. Sources
framework_atlas/flows/02800001.md, 02810001.md, 02820001.md, 02830001.md, group_11.md; framework_flows/TC-DA-01_executed.md, DISPATCH_ADVICE.md; ui.md (Verified in the group 11 replay).
- G11-1 learning walk: learning_sessions/2026-10-01_G11-PK_session1_log.md (Stock Inquiry before DA 1358, seq 9, seq 24, seq 50) and learning_sessions/2026-10-01_G11-PK_session1_report.md (§3 rules 1, 6, 7; §5; §7 drift "Stock validation asserts absolute In"; §8 Q-OB1).
