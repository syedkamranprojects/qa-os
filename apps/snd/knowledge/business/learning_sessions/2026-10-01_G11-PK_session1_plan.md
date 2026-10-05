# Learning plan: S&D Daily Cycle, group 11, Pakistan (phase 0, Scope)

Run id: `LEARN-G11-PK/20261001-1611`. Standard: `docs/LEARNING_STANDARD.md` (v1). Written 2026-10-01 16:11 PKT.
Type: **learning session**, business knowledge only, **no element ids / locators** (the recorder captures those later).

## 1. Scope

| Item | Value |
|---|---|
| App / market | S&D (DCODE) / Pakistan (org 010104) |
| Framework group | **11 Daily Cycle Only Positive Flow** (framework app 8, PK_Centegy QA 2) |
| Rows in scope | **46 active rows (status Y)**, in `pgtfd_sequenceno` order. The 15 inactive rows (status N) are not run. |
| Environment | cnr1dev1, https://dcodecnr1dev1.unilever.com/ngui (`non_production: true`) |
| Company / distributor | Unilever Pakistan Limited / 15108843 - IBRAHIM TRADERS (shown as "Auto KARACHI") |
| Roles | **Maker** = Automation (session start, seq 1-2, QA lead 2026-10-01) and Auto_Multi_Orga (rows that name it: seq 9 onwards). **Checker** = Auto_Tssm |
| Levels targeted | L2 (Daily Cycle chain, confirmed live), L3 (19 option pages), cross-cutting (glossary, lifecycle, open questions) |
| Authorization | QA lead, 2026-10-01: run the active flows of group 11 live, data-changing steps included, on cnr1dev1 |

## 2. Sources (trust order for this session)

1. `legacy-framework-replay`: `selenium-framework-db` group 11 rows, per-flow screens/fields/events/queries (atlas `apps/snd/knowledge/framework_atlas/group_11.md` + `flows/<id>.md`), case data `framework/casedata-samples/NG_Dcode_QA_OTC (Pak).xlsx` (183 sheets). Facts tagged `[db]`.
2. `app-db`: `snd-schema` (document types, status codes, workflows). Facts tagged `[db]`.
3. `live-walk`: cnr1dev1 via the Selenium MCP. Facts tagged `[observed]`.
4. `sme`: QA lead rulings during the session (`[stated]`); BA questions batched at the end.

## 3. Login segments and flows

Logins are typed by the QA member. Claude logs out, names the user, and continues after the login (company and distributor selection are done by Claude).
A row with no user runs as the current session user. 11 logins in total.

| Seg | Log in as | Seq | Test flow id | Flow | L3 page (`apps/snd/knowledge/business/`) |
|---|---|---|---|---|---|
| 1 | Maker (Automation) | 1 | 021400000 | Login Dcode | (login recipe, `app.yaml`) |
| | | 2 | 00100001 | Dispatch Advice (create, lines, loss, forward) | inbound_stock/dispatch_advice.md |
| 2 | Checker (Auto_Tssm) | 5 | 00740001 | Dispatch Advice Approval | inbound_stock/dispatch_advice.md |
| | | 7 | 00760001 | Dispatch Advice Loss Approval | inbound_stock/da_loss_approval.md |
| 3 | Maker (Auto_Multi_Orga) | 9 | 02800001 | Stock Validation After DA PAK | inbound_stock/stock_validation_flows.md, stock_inquiry_and_balances.md |
| | | 10 | 00010001 | Order Booking | order_to_delivery_planning/order_booking.md |
| | | 12 | 00130001 | Stock Allocation | order_to_delivery_planning/stock_allocation.md |
| | | 14 | 02960001 | Transaction Inquiry Validate after OB | order_to_delivery_planning/transaction_inquiry.md |
| | | 15 | 00020001 | Order Editing | order_to_delivery_planning/order_editing_cancellation.md |
| | | 16 | 00040001 | Order Cancellation R2 TH | order_to_delivery_planning/order_editing_cancellation.md |
| | | 18 | 00130002 | Stock Unallocation | order_to_delivery_planning/stock_allocation.md |
| | | 19 | 00160001 | Delivery Date Change | order_to_delivery_planning/delivery_date_change.md |
| | | 20 | 00050001 | Goods Issue Note (create, select cash memos, forward) | delivery_and_returns/goods_issue_note.md |
| 4 | Checker | 23 | 00780001 | Goods Issue Note Approval | delivery_and_returns/goods_issue_note.md |
| 5 | Maker | 24 | 02810001 | Stock validation after GIN PAK | inbound_stock/stock_validation_flows.md |
| | | 29 | 00840001 | Order Editing After GIN | order_to_delivery_planning/order_editing_cancellation.md |
| | | 31 | 00850001 | Order Cancellation After GIN | order_to_delivery_planning/order_editing_cancellation.md |
| | | 32 | 01040001 | Cashmemo Reschedule | delivery_and_returns/cashmemo_reschedule_and_status.md |
| | | 33 | 00030001 | Cashmemo Status | delivery_and_returns/cashmemo_reschedule_and_status.md |
| | | 34 | 00070001 | Sales Return | delivery_and_returns/sales_return.md |
| | | 36 | 00700001 | Sales Return View | delivery_and_returns/sales_return.md |
| 6 | Checker | 37 | 00730001 | Sales Return View Approval | delivery_and_returns/sales_return.md |
| 7 | Maker | 38 | 00710001 | Sales Return Status Change | delivery_and_returns/sales_return.md |
| | | 39 | 03230001 | Deposit Slip Full Amount Cash | settlement_and_finance/deposit_slips.md |
| | | 40 | 03240001 | Deposit Slip Full Amount Cheque | settlement_and_finance/deposit_slips.md |
| | | 41 | 03260001 | Deposit Slip Unposted Amount Validate | settlement_and_finance/deposit_slips.md |
| | | 42 | 00140001 | Deposit Slip Multi Cheques | settlement_and_finance/deposit_slips.md |
| | | 44 | 00140004 | Deposit Slip Cheque | settlement_and_finance/deposit_slips.md |
| | | 46 | 00140005 | Deposit Slip Cash | settlement_and_finance/deposit_slips.md |
| | | 48 | 00090001 | Good Return Note (create, forward) | inbound_stock/goods_return_note.md |
| 8 | Checker | 49 | 00810001 | Good Return Note Approval | inbound_stock/goods_return_note.md |
| 9 | Maker | 50 | 02820001 | Stock validation after GRN PAK | inbound_stock/stock_validation_flows.md |
| | | 51 | 00680001 | Route Settlement | settlement_and_finance/route_settlement.md |
| | | 52 | 03210001 | OFFSET Amount Validate After Route Settlement | settlement_and_finance/route_settlement.md |
| | | 53 | 03220001 | Deposit Slip After Route Settlement | settlement_and_finance/deposit_slips.md |
| | | 54 | 03250001 | Deposit Slip Cash removal | settlement_and_finance/deposit_slips.md |
| | | 55 | 00660001 | Cheque Status | settlement_and_finance/cheque_status.md |
| | | 56 | 00670001 | DSR Adjustment Amount | settlement_and_finance/dsr_adjustment.md |
| | | 57 | 00930001 | PJP Daily Inquiry Update | settlement_and_finance/pjp_daily_inquiry_update.md |
| | | 58 | 02950001 | OTC Stock Out R1 | settlement_and_finance/otc_stock_out_and_san.md |
| 10 | Checker | 59 | 03500001 | SAN Approval PAK | settlement_and_finance/otc_stock_out_and_san.md |
| 11 | Maker | 60 | 02830001 | Opening & Closing Stock Validation | settlement_and_finance/end_of_day_validations.md |
| | | 68 | 03190001 | Validate Edited Order Charges Tax In Transaction Inquiry | settlement_and_finance/end_of_day_validations.md |
| | | 69 | 03200001 | Validate Charges Tax After Sales Return In Transaction Inquiry | settlement_and_finance/end_of_day_validations.md |
| | | 70 | 03740001 | Transaction Inquiry Validations After Order Editing | settlement_and_finance/end_of_day_validations.md |
| | | 71 | 03770001 | Transaction Inquiry Validate After Sales Return | settlement_and_finance/end_of_day_validations.md |

## 4. Document chain (what each flow hands to the next)

Framework repository values (`REPO_*`) show the business hand-offs:

- **Dispatch Advice** (seq 2) produces `REPO_DOCUMENTNO`, which seq 5 consumes (DA approval). The approval creates the day's stock row and the loss record (seq 7).
- **Order Booking** (seq 10) produces `ORDERNUMBER`, which seq 15 consumes (Order Editing → `ORDERNUMBEREDIT`). Allocation, cancellation, unallocation and delivery date change work on the same day's orders.
- **Goods Issue Note** (seq 20) produces `REPO_GINNO`, which seq 23 approves. After the GIN: order editing and cancellation (29, 31), reschedule (32), delivery status (33).
- **Sales Return** (34) is viewed (36), approved (37) and status-changed (38). Then **deposit slips** (39–46) produce `REPO_Deposit_Slip`.
- **Good Return Note** (48) produces `REPO_GRNNO`, approved at 49. Then route settlement (51) and the dependent deposit slip flows (52–54), cheque status (55), DSR adjustment (56), PJP daily update (57).
- **OTC Stock Out** (58) produces `REPO_DocumentNo/Type`, approved as SAN at 59. Then closing checks (60, 68–71).

## 5. Data needed

| What | Value / source | Status |
|---|---|---|
| Warehouse | C0000000055 Auto Main Warehouse (receives the DA) | known |
| PJP / DSR | 02112-AutomationDSR (automation PJP) | known; working date must equal today |
| Products and quantities | workbook sheets `Dispatch Advice Detail*`, `Order Booking Detail*`, `Goods Issue Note*`, `Sales Return Detail` … (Pak) | to read per flow in phase 1 |
| Outlets for orders | workbook `Order Booking` sheet | to read; must be on today's PJP |
| Payment data (cash/cheque, bank, cheque no) | workbook `Deposit Slip*`, `Cheque Status` | to read |
| Stock before / after | Stock Inquiry snapshot (same rows, same filters) at seq 9, 24, 50, 60 | taken live |

**Do not reuse** (earlier days, stale stock): DA 570, 1350, 1353–1357; loss records 637, 638; GIN 504, 505; orders COL26000001988, COL26000001995–2002. Every document in this session is created fresh today.

## 6. What is recorded per flow (business facts only)

Purpose and place in the cycle · actor and what the other role can or cannot do · inputs (real labels, mandatory, defaults, value origin) · steps in the standard vocabulary · rules and validations · exact messages · status before/after · stock and amount effects (before/after) · dependencies and date rules · test-design hints · contradictions with the framework rows (drift).
Not recorded: element ids, locators, xpaths.

## 7. Outputs

- L3 pages updated in place (facts tagged `[observed]` / `[db]` / `[stated]`), `INDEX.md` L2 chain confirmed, `glossary.md`, `document_lifecycle.md`.
- `LIVE_FINDINGS.md` (raw evidence log, new section per segment), `OPEN_QUESTIONS.md` (closed/new), `LIVE_LEARNING_CHECKLIST.md` (items settled).
- This folder: `session_log.md` (per flow: done / blocked / skipped, documents created), `learning_report.md` (standard §7 report), BA note if class C questions arise.

## 8. Stop rules

- **Stop and ask the QA lead** when: a flow's precondition is missing (e.g. empty outlet list), a message contradicts the framework's expected result, an action would be one-way and isn't the flow's purpose, or the session drifts towards the day boundary.
- **Never click:** Generate Opening Balances, Reject, Terminate, Bounce (no active row needs them), or any delete outside a flow.
- **On a failure:** record the exact message and state, don't retry with different data unless the QA lead agrees, and continue only with flows that don't depend on the failed one.

## 9. Timing and the one-calendar-day rule (decision needed)

The receive → order → issue → return → settle chain must finish **inside one calendar day**: stock and PJP working dates are keyed by date, and earlier-day stock cannot be issued (observed 2026-09-30 and 2026-10-01).

- **Time now:** 16:11 on 2026-10-01.
- **Expected duration:** 46 flows with 11 logins. Earlier sessions needed most of a day for seq 1–14 alone, so a realistic estimate is 6–10 hours.
- **Risk:** a walk started now would almost certainly cross midnight and break the chain from the GIN onwards.

**Decision (QA lead, 16:15):** walk **segments 1–3 today as a trial** (seq 1–20: DA → approval → loss approval → stock validation → orders → allocation → editing/cancellation → delivery date → GIN). The full run restarts from seq 1 on a later day with fresh data; today's documents are not reused.

~~Proposal: do phase 1 (Harvest, no browser) today~~ (superseded). Read the 46 flows' framework rows and workbook data, and draft the per-flow expectations and step sheets. Then start **phase 2 (Walk) tomorrow morning** with a fresh login and run it in one sitting. The QA lead decides.

## 10. Risks and open points

| # | Risk / question | Default / mitigation |
|---|---|---|
| R1 | Seq 15 Order Editing: Outlet Name list was empty on 2026-09-29 (suspected delivery-date range) | Check the order's delivery date and PJP date first; stop and ask if empty |
| R2 | First login user for seq 1–2 is the engine's run-time default, not stored in the group row | **Decided:** Automation (QA lead). Its login was rejected on 2026-09-29: if it fails again, stop and ask |
| R3 | Sessions expire after a long idle gap | Answer login hand-offs promptly; on expiry, re-login as the same user and continue |
| R4 | Allocation is automatic at order save; the manual Stock Allocation step was a no-op before | Record what the screen shows; no forced data |
| R5 | Loss approval stock effect unknown (L21) | Before/after Stock Inquiry snapshot around seq 7 |
| R6 | Framework drift (row-0 grid assumptions, wrapper buttons, blur commits) | Note as drift; the walk follows the business intent, not the engine's quirks |
| R7 | GRN at seq 48 needs undelivered / returned goods from the same day | Confirm the source documents at seq 32–38 before seq 48 |
