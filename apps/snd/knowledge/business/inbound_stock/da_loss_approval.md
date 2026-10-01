# DA Loss Approval: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Confidence tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: 00760001 (group 11 seq 7); inactive 00750001 (Loss Approval Request, seq 6).

## 1. Purpose
Goods can arrive damaged, expired or lost on the way. When the maker records a loss on a Dispatch Advice line, the loss must be confirmed by an approver. Loss Approval is that second sign-off: a separate document and workflow ("DALossApproval") from the DA approval [db + observed]. It follows DA approval and precedes the stock check (seq 9). Live-verified 2026-10-01: the loss record is created BY THE DA APPROVAL, not by the maker's Forward [observed]. Before: dispatch_advice.md. After: stock_inquiry_and_balances.md.

## 2. Actors and roles
Checker = Auto_Tssm, same session as DA approval (no user switch at seq 7) [atlas, observed]. Maker records the loss on the DA. The Loss Approval screen (layout 202026) is VISIBLE to the Maker Auto_Multi_Orga (master grid readable, filter by Document No) [observed 2026-10-01].

## 3. Documents and master data
Loss record with Serial No (e.g. 637), Document No = the DA (1350), Document Type Dispatch Advice (DA-01), Status [observed]. Loss stock types for org 010104: 02 Damaged, 03 Expired, 04 Lost, 11 Variance Warehouse (05 Dummy inactive) [db snd_pr_stt_sku_stocktype]. The loss modal "Stock" list showed Damaged, Expired, SEP, Lost, Behalf 615, Variance; Loss Reasons: Area Closed, Order Change, Customer cancels delivery, On Customer Behalf [observed].

## 4. Inputs: screens and fields
Menu "Loss Approval" (layout 202026, DYL_202026). Master grid (364 rows on 2026-09-30, 365 after DA 1356; not sorted by serial, first row 372 then 1,2,3; breadcrumb can be stale; the row filter persists across reopen) with filters such as rowfilter_TXT__tstmdocno; columns Serial No, Document No, Status. Detail tab lists SKU Type with dispatched/received quantities. Tabs must be real-clicked. Forward opens a Comments popup [observed].

## 5. Process: the business steps in order
1. [Maker] on the DA: Add loss to line (Stock, Loss Reason, CS), Calculate, save line (see dispatch_advice.md).
2. [Checker] Navigate to Loss Approval; sort Serial No descending (one header click) [observed].
3. [Checker] Open the record (Serial 637, DA 1350, Pending for approval); verify detail: 20050310 type 02 Damaged 4 CS and 04 Lost 2 CS of 70 dispatched / 64 received; 62690363 type 02 Damaged 5 CS of 60 / 55 [observed].
4. [Checker] Forward with comment "Auto" -> "Forwarded successfully"; status Approved [observed] (11:7:00760001).

## 6. Outputs and effects
Live-verified 2026-10-01 (DA 1356, loss 1 CS Damaged, reason Area Closed): after the maker's Forward (DA Pending) the Loss Approval filter Document No 1356 gave 0 rows; after the checker approved the DA it gave Serial 638, Document Type DA-01 - Dispatch Advice, Distributor 15108843 Auto KARACHI, Status Pending for approval (serial +1 per DA with loss: 637 -> 638). Detail tab: 62740537, SKU Type 02 (Damaged), Dispatch CS 5, Received CS 4, Loss CS 1 [observed]. A Pending loss does not block the stock posting of the received (net of loss) quantity, and no 02 - Damaged stock row exists for 62740537 on 2026-10-01 or 09-30 [observed]; the loss approval (checklist L21) was not run yet, so the effect of APPROVING a loss remains unknown.
Loss record Approved. The stock effect is NOT confirmed: after approval Stock Inquiry still showed only Sound rows for 20050310 and 62690363, with no 02 Damaged or 04 Lost row in any warehouse [observed]. Where approved losses land (claims, later job, another screen) is [unknown]; a claim loss log table exists (snd_lg_cel_claim_exe_loss_log) [db] but its link is [inferred] only.

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| (auto, when the checker APPROVES a DA with losses) | create | Pending for approval | system | observed 2026-10-01 (correction: not at the maker's Forward) |
| Pending | Forward | Approved | Checker | observed |
| Pending | Reject / Terminate | Rejected / Terminated | Checker | db (DALossApproval statuses 01-05) |

## 8. Rules and validations
- The loss record appears automatically at the DA approval; the manual "Loss Approval Request" flow is not needed [observed]. Correction 2026-10-01: earlier text and the default said "at maker Forward"; live shows no record after Forward and a record right after the DA approval.
- Received = dispatched - loss [observed].
- In the loss modal the second row reuses ids with _0 after the first is saved; line save ids are _1, _2 by row [observed].
- Forward needs a comment [observed, same popup as DA].

## 9. Messages
"Forwarded successfully" [observed]. Loss row save shows no toast.

## 10. Dependencies
Reads the DA (document number, lines, losses). Hands to stock reporting (unclear) and possibly claims [inferred].

## 11. Test design hints
- Positive: approve one loss; two loss rows on one line; losses on several lines; detail matches entered values.
- Negative: Reject the loss; Forward without comment; try loss approval before the DA is approved; maker tries to approve.
- Boundary: loss = whole line; loss 1 CS; loss greater than dispatched quantity.
- Trap: a green "Forwarded successfully" does not prove any stock moved; stock effect is unverified.

## 12. Open questions
Q: Where do approved DA losses appear as stock (Damaged/Lost rows)? | Default: not in Stock Inquiry same day | Evidence: none after DA approval with the loss Pending (2026-10-01); loss approval itself still to run (L21).
ANSWERED 2026-10-01 (Q06): created at the DA approval, not at Forward [observed: 0 rows after Forward, Serial 638 after approval].
Q: May the maker approve losses? | Default: no | Evidence: untested.

## 13. Sources
runs/PILOT-DA-GIN/20260930-1615/exec/learning_block2a.json, learning_block3a.json, learning_block3b.json; LIVE_FINDINGS.md; framework_atlas/flows/00760001.md, 00750001.md; framework_flows/TC-DA-01_executed.md (TC-DA-03 and re-run), DISPATCH_ADVICE.md parts 7-8; DB snd_pr_stt_sku_stocktype, wkf_wf_wfs_workflow_status (DALossApproval), snd_lg_cel_claim_exe_loss_log (name only).
