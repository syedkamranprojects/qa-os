# Delivery lifecycle: from allocated order to delivered or returned (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: group 11 seq 12-38 (atlas `group_11.md`).

## 1. Purpose
Follows one cash memo (order, `CM-01`) from allocation to the end of the delivery day, and shows where stock and documents change. It ties together Goods Issue Note, Cashmemo Reschedule/Status and Sales Return (see their pages).

## 2. Actors and roles
Stock Controller (maker) `Auto_Multi_Orga`; checker `Auto_Tssm` approves GIN (seq 23) and the sales return (37); the DSR (delivery man, PJP `02112-AutomationDSR`) physically delivers [observed/atlas].

## 3. Documents and master data
`CM-01` cash memo, `GN-01` GIN, `CM-02` sales return, `GR-01` Goods Return Note, `CRN-02` credit note [db]. Link tables: GIN refinfo -> cash memo. Stock: `snd_tr_ssb_salestock_balance` by balance date [db].

## 4. Inputs: screens and fields
Order of screens: Order Stock Allocation, Delivery Date Change, Goods Issue Note, Stock Inquiry, Cashmemo Reschedule, Cashmemo Status, Sales Return, Sales Return View, Sales Return Status Change. Fields: see the individual pages.

## 5. Process: the business steps in order
| Seq | Step | Document effect | Stock effect |
|---|---|---|---|
| 12/18 | Stock Allocation / Unallocation | order Confirmed (exec 02), allocation F/P | reserves stock [db: `tcmm_stock_allocated_status`; reserved columns in stock balance, [inferred]] |
| 19 | Delivery Date Change | delivery date moved (`Delivery Date has been changed successfully, processed orders: 9`) [observed] | none |
| 20 | GIN create + forward | GIN Draft -> Pending [observed]; cash memo Planning completed (03) [inferred] | none yet |
| 23 | GIN approval | GIN Approved; cash memo Ready to dispatch/Packed (13) [inferred] | goods issued out of warehouse [inferred]; needs stock balance of the day [observed] |
| 24 | Stock check after GIN | read-only | In/Out/closing compared [atlas] |
| 29/31 | Order Editing/Cancellation After GIN | edit or cancel an order already issued | [unknown] |
| 32 | Cashmemo Reschedule | status 19 CM Reschedule | [unknown] |
| 33 | Cashmemo Status | Delivered (10) | none [inferred] |
| 34-38 | Sales Return, view, approval, status change | CM-02 created, authorised, Picked | none until GRN [inferred] |
| 48-49 | Goods Return Note (other analyst) | GR-01 | returned goods back into warehouse [inferred] |

## 6. Outputs and effects
At the end of the day the load of each DSR is either delivered (receivable to settle), rescheduled (to another day) or returned (to the warehouse). Daily cycle must run inside one calendar day because stock balances are keyed by date [observed].

## 7. Statuses and transitions
Live-verified 2026-10-01 [db + observed]: "Confirmed" is execution status 02 (own status, not Ordered 04); 03 Planning completed is shown for the 8 orders on GIN 505; Transaction Inquiry has one Document Status column that shows the execution status text; codes 04, 06 and 19 do not exist in the execution master of org 010104 (so '19 CM Reschedule' below comes from org 0101 and must be re-read live).
Cash memo execution status chain (CM-01): 01 Ordered -> 02 Confirmed (allocated) -> 03 Planning completed (on GIN) -> 13 Ready to dispatch/Packed (GIN approved) -> 10 Delivered/Invoiced | 18 Partial Delivered | 19 CM Reschedule | 05 Cancelled [db names; order of the chain [inferred]]. Other values: 11 Dispatched, 12 Sent to Locus, 20 CM BLOCKED, 21/22 Auto/Manual Split, 23 Partial Open [db]. Document status: 04 Ordered -> 01 Delivered / 02 Un-Delivered / 03 Cancelled / 05 Amendment / 06 Re-attempt [db]. Completion status (`pdcs`): 01 Completed, 02 DN Pending, 03 Z3 [db], meaning (delivery note to the ERP) [inferred]. In the data (org 0101, Jan 2026) most CM-01 are Delivered (01) with execution 10 or 18 [db].

## 8. Rules and validations
- Stock is needed on the day of GIN approval [observed].
- Return quantity cannot exceed ordered quantity [atlas].
- Only cash memos that are allocated and on the PJP/date can be selected into a GIN [inferred from the 9 eligible].
- Maker/checker separation on GIN and sales return [observed/atlas].

## 9. Messages
See the individual pages. Chain-level: `Delivery Date has been changed successfully, processed orders: 9`; `stock not found.` on Unallocate [observed, ui.md].

## 10. Dependencies
Upstream: Dispatch Advice receipt (inbound stock), Order Booking, allocation (order planning). Downstream: Deposit Slip and settlement (seq 39+), Goods Return Note. Data carried: `REPO_GINNO`.

## 11. Test design hints
End-to-end positive: allocate, GIN, approve, deliver, partial return, GRN; check each status in the DB and the stock balance after each step. Negative: GIN approved on a day with no stock balance; reschedule after delivery; return more than delivered; cancel an order already on an approved GIN. A green group-11 run proves screens and messages, not that statuses and stock totals are right.

## 12. Open questions (batched for the BA; each with a default)
Q: Exact stock effect of each step (reserve at allocation, issue at GIN approval, return at GRN)? | Default: as in the table | Evidence: only names and one error message.
Q: Is Cashmemo Status the step that makes the cash memo Delivered/Invoiced? | Default: yes | Evidence: names.
Q: Does a delivered cash memo with a return become Partial Delivered (18)? | Default: yes | Evidence: status exists.
Q: Is the Unallocate failure `stock not found.` a defect or by design? | Default: environment issue | Evidence: ui.md, cause unknown.

## 13. Sources
`framework_atlas/group_11.md`, flows `00130001`, `00160001`, `00050001`, `00780001`, `02810001`, `01040001`, `00030001`, `00070001`, `00700001`, `00730001`, `00710001`; `apps/snd/knowledge/ui.md`; `framework_flows/STEP_SHEET_DRAFT_next.md`; DB: glb_pr_exs_execution_status, snd_pr_dos_documentstatus, snd_pr_dcs_doc_cmpltn_status, snd_tr_cmm_cashmemo_master, snd_tr_gnm_gingrn_master.
