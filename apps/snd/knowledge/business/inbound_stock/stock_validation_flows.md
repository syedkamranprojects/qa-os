# Stock validation flows: how they work (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Confidence tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 02800001 (seq 9, after DA), 02810001 (seq 24, after GIN), 02820001 (seq 50, after GRN), 02830001 (seq 60, opening and closing). Inactive: 02840001, 02850001, 02860001 (after SAN), 02950001 / 03500001 (OTC stock out and SAN approval).

## 1. Purpose
These flows are checkpoints in the Daily Cycle: after a stock-moving document is approved, the stock controller opens Stock Inquiry and checks that the stock figures moved as expected. They are tests of stock, not business operations (read-only). See stock_inquiry_and_balances.md for the screen and the meaning of columns.

## 2. Actors and roles
Auto_Multi_Orga (serial 35) with a user switch before each (seq 9, 24, 50, 60) because the preceding approval is done by Auto_Tssm [atlas].

## 3. Documents and master data
None created. Reads case-data sheets per flow: Stock_Val_After_DA_PAK1/2/3, Stock_val_after_GIN_PAK1/2/3, Stock_Val_after_GRN_PAK1/2/3, Open_Close_Stock_Val/2/3 and screenshot_ASSR [atlas]. Expected values in the workbook were product 62740537, Auto Main Warehouse, 01 - Sound, In CS 80, Out CS 0, In PC 0, Out PC 0 [observed].

## 4. Inputs: screens and fields
Three screens each: (1) criteria: Period Type, Balance Date, Category, Brand, click Show Inquiry; (2) grid row filters Auto (product), Auto1 (warehouse), Auto2 (stock type), click first row checkbox; (3) read cells: In CS, Out CS, In PC, Out PC (flows 9, 24, 50) or Opening CS, Closing CS, Opening PC, Closing PC (flow 60), click row_1_closing_pc to expand, compare to workbook (event 0007) [atlas]. The GIN flow waits 2 s around the expand click [atlas].

## 5. Process: the business steps in order
1. [Stock Controller] Login as Stock Controller (switch point).
2. Navigate to Stock Inquiry; Show Inquiry for the chosen date.
3. Filter product / warehouse / stock type; open the row.
4. Verify values against expected. After DA: In = received; after GIN: Out/Allocated reflect the issue; after GRN: In rises by the return; flow 60: Opening and Closing for the day.
Trace keys 11:9:02800001, 11:24:02810001, 11:50:02820001, 11:60:02830001.

## 6. Outputs and effects
None (read only). They produce a pass/fail on stock correctness and screenshots.

## 7. Statuses and transitions
Not applicable.

## 8. Rules and validations
- Expected In/Out are absolute values from the workbook: valid only on a clean day [observed: In 176, Out 96 netted to closing 80].
- Date in workbook is hard-coded (2026-09-21): must be today [observed].
- Live-verified 2026-10-01: for a product received today, the day's row is created by the DA approval with Opening 0, so In = received and Closing = received hold on a day without other movements; assert the identity Closing = Opening + In - Out - Allocated in base PC units [observed].
- Drill-down checkbox-0 clears the row filter, so row_1_* then points at the first unfiltered row [observed].
- Screenshot assertion group (screenshot_ASSR) checks no message text [atlas].

## 9. Messages
None on Show Inquiry; "No data" for an empty day [observed].

## 10. Dependencies
Needs the preceding document approved the same calendar day (balances keyed by date). A new day shows No data until a movement creates the row (the DA approval does, observed 2026-10-01) or opening balances are generated; GIN approval on a new day for stock received the day before failed with "No stock balance found for products" [observed]; previous-day closings are not carried automatically [observed].

## 11. Test design hints
- Positive: after each DA / GIN / GRN, closing changes by exactly the document quantity (before/after snapshot).
- Negative: wrong product filter, date with no balances, user without the screen (Auto_Tssm).
- Boundary: busy day with several movements; PC vs CS; Damaged and Lost rows after loss approval (currently absent).
- Traps: framework run can be green while only screenshots are compared; absolute In/Out checks fail on busy days; never run Generate Opening Balances in these flows.

## 12. Open questions
Q: Should validation compare absolute values or the change from a pre-snapshot? | Default: change from a snapshot | Evidence: busy-day failure.
Q: What should flow 60 Opening/Closing expect after a new day starts? | Default: Opening = 0 for a product first moved today, prior Closing only after Generate Opening Balances | Evidence: 62740537 closed 97 CS on 09-30 and opened 0 on 10-01 after the DA approval.
Q: Are the SAN stock validations (02850001, 02860001) part of the cycle? | Default: no, inactive | Evidence: status N.

## 13. Sources
framework_atlas/flows/02800001.md, 02810001.md, 02820001.md, 02830001.md, group_11.md; framework_flows/TC-DA-01_executed.md, DISPATCH_ADVICE.md; ui.md (Verified in the group 11 replay).
