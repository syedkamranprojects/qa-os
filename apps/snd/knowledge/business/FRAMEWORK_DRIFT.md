# Framework drift: group 11 (PK) workbook / framework vs the live app

For the framework owner. Created 2026-10-05 from the learning walks G11-1 (2026-10-01, seq 1-50) and G11-2 / G11-2b (2026-10-05, seq 1-71) on cnr1dev1, distributor 15108843. Every row is a place where the legacy framework rows (CTA_CONFIG_ASSERTION) or the case-data workbook (NG_Dcode_QA_OTC (Pak) and sheets named below) no longer match what the app does. In most rows the app is consistent and the expected value is stale; a run would fail (or pass by coincidence) for the wrong reason.

Evidence files: [learning_sessions/2026-10-01_G11-PK_session1_report.md](learning_sessions/2026-10-01_G11-PK_session1_report.md) §7, [learning_sessions/2026-10-05_G11-PK_session2_log.md](learning_sessions/2026-10-05_G11-PK_session2_log.md), [learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md](learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md). The pages named in the last column hold the business detail (section 11 traps).

Tags: [observed] seen live; [db] read from the framework tables or workbook. Nothing here has been changed in the framework; this is a to-do list.

## 1. Value and message drift

| # | Seq | Flow id | Sheet / field | Workbook / framework value | Observed value | Evidence | Suggested fix | Page |
|---|---|---|---|---|---|---|---|---|
| 1 | 70 | 03740001 | T Inquiry Header Amt Val OE / header Tax | 8,728.81 | 14,584.79 (8,728.81 is line 1's tax) | G11-2b seq 70 [observed 2026-10-05] | Set header Tax 14,584.79 (Gross 96,840.34, Discount -20,718.07, Net 90,707 already match) | transaction_inquiry.md, end_of_day_validations.md |
| 2 | 69 | 03200001 | Return Total Tax / VAT, 3rd Schedule | VAT -4,434.18; 3rd Schedule -1.95 | VAT -4,419.93; 3rd Schedule 0 | G11-2b seq 69 [observed 2026-10-05] | Rebuild from today's return (workbook built 2026-09-21 for outlet 1000000003) | sales_return.md, end_of_day_validations.md |
| 3 | 69/71 | 03200001, 03770001 | Return header Tax | -4,425.41 / -4,436.55 | -4,419.93 | G11-2b [observed 2026-10-05] | as row 2 | sales_return.md |
| 4 | 71 | 03770001 | Return header Discount / Net | 6,169.17 / -29,113 | 6,189.17 / -29,077 (Gross -30,845.86 matches) | G11-2b seq 71 [observed 2026-10-05]; same Net in G11-1 and G11-2 | as row 2; or compute expected values from the source order | sales_return.md, transaction_inquiry.md |
| 5 | 71 | 03770001 | Return detail line 1 Discount / Net | 6,260.28 / -29,010.99 | 6,407.54 / -28,837.22; lines 2-5 carry small reversals (slab promotions re-priced) | G11-2b seq 71 [observed 2026-10-05] | as row 2; do not assert 0 on non-returned lines | sales_return.md |
| 6 | 34 | 00070001 | Sales return summary Discount / Tax / Net | 6,169.17 / 4,436.55 / 29,113.00 | 6,189.17 / 4,419.93 / 29,077.00 (Gross 30,845.86 matches) | G11-1 and G11-2 seq 34 [observed 2026-10-01, 2026-10-05] | as row 2 | sales_return.md |
| 7 | 56 | 00670001 | DSR Adjustment Detail check / Amount and date | "PKR 14,796.99" for document date 2026-09-21 | not saved (seq bypassed); Document Date defaults to today; PJP 02112 Balance 827,600.68 | G11-2b seq 56 [observed 2026-10-05] | Use today's date and assert the delta (Total Adjusted +Amount, Balance -Amount) | dsr_adjustment.md |
| 8 | 55 | 00660001 | Cheque Status action | QA lead asked for "Realized"; framework selects the cheque row then fires an event (Bounce?) | no Realized / Presented / Collected choice; cheques already "Clear" after posting; only action Bounce | G11-2b seq 55 [observed 2026-10-05; stated 2026-10-05 QA lead] | Decide (Q-CS1): keep bypassed, or assert Status "Clear" read-only; never Bounce in the cycle | cheque_status.md |
| 9 | 9 | 02800001 | Stock_Val_After_DA_PAK1-3 / In CS | absolute 80 | 10-01: day In 164 (fail); 10-05: 80 (pass by coincidence, only receipt of the day) | G11-1, G11-2 seq 9 [observed] | Before/after delta per product (Q-SV1) | stock_validation_flows.md |
| 10 | 24, 50 | 02810001, 02820001 | stock after GIN / GRN / In-Out CS | absolute In/Out (Out 0) | GIN: Out = issued, Closing unchanged; GRN: In + returned, Out unchanged; old reservations (63 CS of GIN 505) carried | G11-1, G11-2 [observed] | Deltas: GIN Out +issued, Allocated -issued; GRN In +returned, Out 0 | stock_validation_flows.md |
| 11 | 60 | 02830001 | Open_Close_Stock_Val / Opening, Closing | absolute values of the workbook day (Opening 0 assumption) | Opening = previous Closing + still-Allocated (308), Closing 259 after SAN -50 | G11-2b seq 60 [observed 2026-10-05] | Opening = previous day's Closing + Allocated; Closing delta = -SAN quantity | stock_validation_flows.md, end_of_day_validations.md |
| 12 | 9-60 | all stock flows | Balance Date | hard-coded 2026-09-21 | must be the run day | G11-1 [observed] | Use today | stock_validation_flows.md |
| 13 | 20 | 00050001 | GIN_DTL_SAVE_ASSR | "Saved Succesfully." | "Saved successfully." | G11-1, G11-2 [observed] | Correct the text | goods_issue_note.md |
| 14 | 42 | 00140001 | Deposit Slip,Outlet / save message | "Saved successfully" | "Payment Adjusted Successfully" | G11-1, G11-2 [observed] | Correct the text | deposit_slips.md |
| 15 | 40, 42, 44 | 03240001, 00140001, 00140004 | bank value | "National Bank of Pakistan" | not in the list; only "National Bank of Pakistanss" (grid Bank_Name list differs from the header Bank list) | G11-1, G11-2 [observed] | Use an existing clean bank, or fix the bank master | deposit_slips.md |
| 16 | (G11-1 report §7) | GIN / GRN rows | vehicle value | workbook vehicle | no longer exists (the PJP fills 0040-Automation211206) | G11-1 [observed] | Let the PJP fill the vehicle | goods_issue_note.md |
| 17 | 48 | 00090001 | GRN detail (1 CS 5 PC / 2 CS 1 PC, rates 118.93 / 33.79) | fixed lines | Suggested follows the day's documents (19 CS of 62740537 on both days) | G11-1, G11-2 [observed] | Derive Suggested from the day's cancel/cut/reschedule/return quantities | goods_return_note.md |
| 18 | 10 | 00010001 | Order Booking outlets 1000000001-03, Reference Number 100 | outlets 01-03; ref 100 | outlets 01-03 not offered on cnr1dev1; ref 100 collides on a second run ("Cashmemo with document reference number : 100 already exist.") | G11-1 [observed] | Use offered outlets (04-08, 11); unique reference per run | order_booking.md |
| 19 | 19 | 00160001 | DELIVERYDATE_CHNG_ASSR count | "processed orders: 9" | "processed orders: 5" (count = rows ticked) | G11-1, G11-2 [observed] | Assert the count of ticked rows | delivery_date_change.md |

## 2. Flow-order and step drift

| # | Seq | Flow id | Item | Framework does | Observed | Evidence | Suggested fix | Page |
|---|---|---|---|---|---|---|---|---|
| 20 | 15 | 00020001 | Order Editing before Delivery Date Change | edits the new order at seq 15 with a date range | Order Editing lists only orders whose delivery date is today; booked orders carry the next visit (10-07, 10-11), so seq 15 finds nothing even with a range covering the delivery date; skipped by the QA lead on both days | G11-1, G11-2 seq 15 [observed; stated QA lead] | Move the edit after seq 19, or book for today (Q-OE1) | order_editing_cancellation.md |
| 21 | 15, 29 | 00020001, 00840001 | Order Editing header PJP | expects the booking PJP | defaults to AUTO241602~Auto917248; re-picking 02111 clears Section / Selling Category | G11-2 seq 29 [observed] | Pick PJP, then Selling Category and Section explicitly | order_editing_cancellation.md |
| 22 | 18 | 00130002 | Unallocation | selects ALL orders right before the GIN | leaves the GIN nothing to issue; QA lead replaced it by one-order unallocate + re-allocate (both days) | G11-1, G11-2 [observed; stated QA lead] | Unallocate one order and re-allocate it | stock_allocation.md |
| 23 | 7 | 00760001 | Loss Approval row pick | clicks Serial No header then the first row | default order not by serial (372 first); can open the wrong record | G11-1 [observed] | Filter by Document No (REPO_DOCUMENTNO) | da_loss_approval.md |
| 24 | 42 | 00140001 | Multi-cheque popup | button on the cash-memo tab; date yyyy-mm-dd | button on the Outstanding Outlet tab; Cheque Date MM/DD/YYYY | G11-1, G11-2 [observed] | Switch tab first; type MM/DD/YYYY | deposit_slips.md |
| 25 | 51 | 00680001 | Route Settlement precondition | assumes the day can be settled | refused while any earlier day is open ("Following previous days not closed! Please close date. <date>") | G11-1, G11-2 [observed] | Add a precondition check (all earlier days Complete / closed on PJP Daily Inquiry Update) before seq 51 | route_settlement.md |
| 26 | 52-54 | 03210001, 03220001, 03250001 | expected Offset / Received | (values from the workbook day) | Offset = posted slip allocations (2009: 2,600); outlet-level multi-cheque goes to the outlet's oldest open memo, so expected values depend on earlier days' open memos | G11-2b [observed 2026-10-05] | Compute from the day's slips and the outlet's open memos | deposit_slips.md, transaction_inquiry.md |

## 3. Notes
- Rows 1-8, 11, 21 and 26 are new from G11-2 / G11-2b (2026-10-05); the others were found in G11-1 and re-observed where marked.
- Framework flows for seq 55 and 56 were not executed (bypassed by the QA lead); rows 7-8 describe the screens and workbook, not an engine run.
- Decision items for the QA lead / framework owner: Q-SV1 (deltas), Q-OE1 / Q-OE2 (seq 15), Q-CS1 (seq 55) in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).
