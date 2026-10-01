# End-of-day validations: stock and Transaction Inquiry checks (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas and the snd-schema DB. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**. Only the finance side is covered; inbound stock, order and delivery pages belong to other analysts.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 02830001 (seq 60), 03190001 (68), 03200001 (69), 03740001 (70), 03770001 (71); finance check 03210001 (52, see route_settlement.md). No live replay.

## 1. Purpose
These read-only flows prove that the day's financial and stock effects are right: opening and closing stock after the SAN, and invoice amounts, discounts, tax and charges in Transaction Inquiry after order editing and sales return. They change nothing.

## 2. Actors and roles
Auto_Multi_Orga throughout; seq 60 follows the user switch back from Auto_Tssm [db].

## 3. Documents and master data
Stock balance `snd_tr_ssb_salestock_balance` (per date, warehouse, batch, stock type: opening, in, out, allocated, closing, ATP, in-transit, moving average price, values) [db]. Transaction Inquiry shows cash memos with header, detail, offering and charges.

## 4. Inputs: screens and fields
- Seq 60: Stock Inquiry II (`DYL_BG1015`): **Period Type**, **Balance Date**, Category, Brand, Refresh; reads Opening CS, Closing CS, Opening PC, Closing PC [db]. Button "Generate Opening Balances" exists [db].
- Seq 68-71: Transaction Inquiry (`DYL_102014`): Document Type, Document Status, Document Date From/To; reads Header Gross Amount, Discount, Tax, Net Amount; Detail Gross Amount, Discount, Tax, Net Amount; Total Offering Discount and Tax Amount; Charges Amount; Tax Amount [db: atlas].

## 5. Process
1. [Maker] Stock Inquiry II: Period Type, Balance Date, category/brand, Refresh; compare Opening/Closing CS and PC with the workbook after the SAN stock-out. trace 11:60:02830001
2. [Maker] Transaction Inquiry for the edited order: validate Charges Amount and header Tax Amount (seq 68), then header/detail/offering amounts after order editing (70). 
3. [Maker] Same for the sales return: Tax Amount, Charges Amount (69) and Gross/Discount/Tax/Net (71).
Gross - Discount + Tax (+ charges) = Net [inferred, to be confirmed against the workbook].

## 6. Outputs and effects
None; assertions only.

## 7. Statuses and transitions
None.

## 8. Rules and validations
- **Corrected 2026-10-01: Closing = Opening + In - Out - Allocated** (Closing is net of Allocated, i.e. available stock; ATP = Closing) [observed on 39 of 39 rows of Stock Inquiry 2026-09-30, in base PC units; two rows differ literally only by PC-to-CS carry]. The earlier inferred text (allocated tracked separately) was wrong.
- Stock balances are keyed by calendar day: the check must use the same Balance Date the cycle ran on [known fact].

## 9. Messages
Assertion slots only (TSTMSG, screenshot_ASSR); texts unrecorded [unknown].

## 10. Dependencies
Consumes everything earlier: SAN approval (seq 59) for stock, order editing/sales return for amounts. Hands nothing on.

## 11. Test design hints
Positive: closing stock equals opening minus SAN qty (and plus receipts, less issues); header totals equal sum of detail. Negative: wrong Balance Date (previous day) must show different opening; cycle across midnight splits balances. Boundary: PC-to-CS conversion (assert the stock identity in base PC with the pack factor from the product name). Green run proves values equal the workbook, which may itself be stale; use DB recompute for the finance totals.

## 12. Open questions
Q: Rounding rule of tax/charges? | Default: document-type rounding (pdot_rounding_decimal) | Evidence: field exists, values unread.
Q: Is the closing stock check restricted to SAN products? | Default: filtered by Category/Brand of the SAN product | Evidence: none.

## 13. Sources
framework_atlas/flows/02830001, 03190001, 03200001, 03740001, 03770001, 03210001; group_11.md; screens_db/DYL_BG1015.json; DB snd_tr_ssb_salestock_balance, snd_pr_dot_documenttype.
