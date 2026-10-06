---
option: End-of-day validations (stock and Transaction Inquiry)
area: settlement_and_finance
doc_types: []
screens: [STOCKINQUIRY, DYL_BG1015, DYL_102014]
framework_flows: ["02830001", "03190001", "03200001", "03740001", "03770001"]
markets: [PK]
roles: [Maker]
depends_on: [otc_stock_out_and_san, order_editing_cancellation, sales_return, transaction_inquiry, stock_inquiry_and_balances]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-06
---

# End-of-day validations: stock and Transaction Inquiry checks (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas and the snd-schema DB. No user guide. Tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**. Only the finance side is covered; inbound stock, order and delivery pages belong to other analysts.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 02830001 (seq 60), 03190001 (68), 03200001 (69), 03740001 (70), 03770001 (71); finance check 03210001 (52, see route_settlement.md). No live replay. (superseded 2026-10-05: seq 60 and 68-71 walked live in G11-2b, read only.)
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.
Updated 2026-10-06: consolidated with learning session G11-3 (full seq 1-71 in one calendar day WITH the QA Team Lead); evidence learning_sessions/2026-10-06_G11-PK_session3_log.md. Tag [stated 2026-10-06 QA Team Lead] = ruling given in chat by the QA Team Lead.

## 1. Purpose
These read-only flows prove that the day's financial and stock effects are right: opening and closing stock after the SAN, and invoice amounts, discounts, tax and charges in Transaction Inquiry after order editing and sales return. They change nothing.
- G11-2b: all five checks were walked on 2026-10-05: the app values are consistent with each other (stock identity, header = sum of tax and offering lines); where they fail against the workbook the workbook is stale (framework drift) [observed 2026-10-05 G11-2b].

## 2. Actors and roles
Auto_Multi_Orga throughout; seq 60 follows the user switch back from Auto_Tssm [db].
- G11-2b: Maker Auto_Multi_Orga read seq 60 (after the switch back from Auto_Tssm) and seq 68-71 [observed 2026-10-05 G11-2b].

## 3. Documents and master data
Stock balance `snd_tr_ssb_salestock_balance` (per date, warehouse, batch, stock type: opening, in, out, allocated, closing, ATP, in-transit, moving average price, values) [db]. Transaction Inquiry shows cash memos with header, detail, offering and charges.

## 4. Inputs: screens and fields
- Seq 60: Stock Inquiry II (`DYL_BG1015`): **Period Type**, **Balance Date**, Category, Brand, Refresh; reads Opening CS, Closing CS, Opening PC, Closing PC [db]. Button "Generate Opening Balances" exists [db].
- Seq 68-71: Transaction Inquiry (`DYL_102014`): Document Type, Document Status, Document Date From/To; reads Header Gross Amount, Discount, Tax, Net Amount; Detail Gross Amount, Discount, Tax, Net Amount; Total Offering Discount and Tax Amount; Charges Amount; Tax Amount [db: atlas].
- G11-2b: seq 60 was read on the normal Stock Inquiry (Period Type DAILY, Balance Date 2026-10-05, Category All, Show Inquiry); "Stock Inquiry II" (DYL_BG1015) exists in the menu but was not opened [observed 2026-10-05 G11-2b]. Seq 68-71 on Transaction Inquiry with Document Type Sales / Sales Return and the Total Tax, Detail, Total Offering buttons [observed 2026-10-05 G11-2b].

## 5. Process
1. [Maker] Stock Inquiry II: Period Type, Balance Date, category/brand, Refresh; compare Opening/Closing CS and PC with the workbook after the SAN stock-out. trace 11:60:02830001
2. [Maker] Transaction Inquiry for the edited order: validate Charges Amount and header Tax Amount (seq 68), then header/detail/offering amounts after order editing (70). 
3. [Maker] Same for the sales return: Tax Amount, Charges Amount (69) and Gross/Discount/Tax/Net (71).
Gross - Discount + Tax (+ charges) = Net [inferred, to be confirmed against the workbook].

G11-2b results (2026-10-05) [observed 2026-10-05 G11-2b]:

| Seq | Check | Observed | Workbook | Verdict |
|---|---|---|---|---|
| 60 | Opening / Closing 62740537 Auto Main Sound | Opening 308, In 99, Out 85 (incl. SAN -50), Allocated 63, Closing 259 | absolute values from its own day | app consistent; use deltas |
| 68 | Edited order COL26000002009 charges/tax | header Tax 14,584.79 = VAT 11,389.48 + 3rd Schedule 3,195.31 | Total Tax 11,389.48 / 3,195.31, header Tax 14,584.79 | **match** |
| 70 | Edited order header / detail / offering | Gross 96,840.34, Disc -20,718.07, Tax 14,584.79, Net 90,707; detail lines 1-3 and offering rows 1-3 equal the workbook | header Tax **8,728.81** | header Tax in workbook wrong (= line 1 tax); rest matches |
| 69 | Sales return charges/tax | VAT -4,419.93, 3rd Schedule 0 | VAT -4,434.18, 3rd Schedule -1.95 | workbook stale |
| 71 | Sales return header/detail/offering | Gross -30,845.86, Disc 6,189.17, Tax -4,419.93, Net -29,077; line 1 Disc 6,407.54 / Net -28,837.22 | Gross -30,845.86 (match); Disc 6,169.17, Tax -4,425.41 / -4,436.55, Net -29,113, line 1 6,260.28 / -29,010.99 | workbook stale except Gross |
- G11-3 (2026-10-06) [observed 2026-10-06 G11-3]: seq 60 Stock Inquiry DAILY 2026-10-06: 62740537 Auto Main Sound Opening 0 / In 97 / Out **89** (32 GIN 508 + 7 GIN 509 + 50 SAN 97) / Allocated 0 / Closing **8**; other 4 rows unchanged (11:60:02830001). Seq 68-71 Transaction Inquiry values: see transaction_inquiry.md.

## 6. Outputs and effects
None; assertions only.
- G11-2b: none (read only) [observed 2026-10-05 G11-2b].
- G11-3: SAN approval posts as Out; the extra GIN 509 (Reattempt order) also contributes to the day's Out [observed 2026-10-06 G11-3].

## 7. Statuses and transitions
None.

## 8. Rules and validations
- **Corrected 2026-10-01: Closing = Opening + In - Out - Allocated** (Closing is net of Allocated, i.e. available stock; ATP = Closing) [observed on 39 of 39 rows of Stock Inquiry 2026-09-30, in base PC units; two rows differ literally only by PC-to-CS carry]. The earlier inferred text (allocated tracked separately) was wrong.
- Stock balances are keyed by calendar day: the check must use the same Balance Date the cycle ran on [known fact].
- G11-2b: Net = Gross + Discount + Tax with Discount negative on sales and positive on returns (return: -30,845.86 + 6,189.17 - 4,419.93 = -29,076.62 shown -29,077) [observed 2026-10-05 G11-2b]; the earlier "Gross - Discount + Tax" wording means the same with Discount as a positive number.
- G11-2b: header Tax = sum of Total Tax lines; header Discount = sum of Total Offering lines (1 paisa rounding) for sales and returns [observed 2026-10-05 G11-2b].
- G11-2b: stock identity Closing = Opening + In - Out - Allocated holds at seq 60 [observed 2026-10-05 G11-2b].

## 9. Messages
Assertion slots only (TSTMSG, screenshot_ASSR); texts unrecorded [unknown].
- G11-2b: no message on any of these reads [observed 2026-10-05 G11-2b].

## 10. Dependencies
Consumes everything earlier: SAN approval (seq 59) for stock, order editing/sales return for amounts. Hands nothing on.
- G11-2b: seq 60 depends on the SAN approval (seq 59); seq 68/70 on the order edited after the GIN (seq 29; seq 15 skipped); seq 69/71 on the picked return (seq 38) [observed 2026-10-05 G11-2b].

## 11. Test design hints
Positive: closing stock equals opening minus SAN qty (and plus receipts, less issues); header totals equal sum of detail. Negative: wrong Balance Date (previous day) must show different opening; cycle across midnight splits balances. Boundary: PC-to-CS conversion (assert the stock identity in base PC with the pack factor from the product name). Green run proves values equal the workbook, which may itself be stale; use DB recompute for the finance totals.
- G11-2b framework drift (also in FRAMEWORK_DRIFT.md) [observed 2026-10-05 G11-2b]:
  - Seq 70: workbook header Tax 8,728.81 is line 1's tax; real header Tax 14,584.79 -> the engine would fail a correct app.
  - Seq 69/71: workbook return values built 2026-09-21 for outlet 1000000003 are stale in every field except Gross.
  - Seq 60: absolute Opening/Closing from the workbook day cannot match; Opening is the carried balance (308 on 10-05).
  - Recommendation: compute expected values from the day's documents (header = sum of lines; stock deltas) instead of fixed workbook numbers.
- G11-3 trap: the day's Out at seq 60 includes any extra GIN made to deliver a previous day's Reattempt order (+7 on 10-06); compute expected values from the day's documents [observed 2026-10-06 G11-3].

## 12. Open questions
Q: Rounding rule of tax/charges? | Default: document-type rounding (pdot_rounding_decimal) | Evidence: field exists, values unread.
Q: Is the closing stock check restricted to SAN products? | Default: filtered by Category/Brand of the SAN product | Evidence: none.
- G11-2b: Q60 (rounding) observed again: Net to whole PKR, Gross/Discount/Tax 2 decimals, totals within 1 paisa. Q61 (closing check restricted to SAN products) not decided: the walk filtered by the SAN product.

## 13. Sources
framework_atlas/flows/02830001, 03190001, 03200001, 03740001, 03770001, 03210001; group_11.md; screens_db/DYL_BG1015.json; DB snd_tr_ssb_salestock_balance, snd_pr_dot_documenttype.
- G11-2b: learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md (seq 60, 68, 69, 70, 71).
- G11-3: learning_sessions/2026-10-06_G11-PK_session3_log.md (seq 60, 68-71).
