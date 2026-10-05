---
option: DA Loss Approval
area: inbound_stock
doc_types: [DA-01]
screens: [DYL_202026]
framework_flows: ["00760001"]
markets: [PK]
roles: [Maker, Checker]
depends_on: [dispatch_advice]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-05
---

# DA Loss Approval: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Confidence tags: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Updated: 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)
Last updated: 2026-10-01 (G11-1 consolidation). Source flows: 00760001 (group 11 seq 7); inactive 00750001 (Loss Approval Request, seq 6). G11-1 learning walk: loss record **639** (DA 1358) approved.
Updated 2026-10-05: consolidated with learning sessions G11-2 (seq 1-50, 2026-10-05 morning) and G11-2b (seq 51-71, same day); evidence learning_sessions/2026-10-05_G11-PK_session2_log.md, 2026-10-05_G11-PK_session2_report.md, 2026-10-05_G11-PK_session2b_resume_log.md. Tag [stated 2026-10-05 QA lead] = ruling given in chat by the QA lead.

## 1. Purpose
Goods can arrive damaged, expired or lost on the way. When the maker records a loss on a Dispatch Advice line, the loss must be confirmed by an approver. Loss Approval is that second sign-off: a separate document and workflow ("DALossApproval") from the DA approval [db + observed]. It follows DA approval and precedes the stock check (seq 9). Live-verified 2026-10-01: the loss record is created BY THE DA APPROVAL, not by the maker's Forward [observed]. Before: dispatch_advice.md. After: stock_inquiry_and_balances.md.
- G11-1: approving the loss is a record / claim sign-off only as far as stock is concerned: it creates no stock row and changes no Stock Inquiry figure (the received quantity was already net of the loss at the DA approval) [observed 2026-10-01 G11-1].

## 2. Actors and roles
Checker = Auto_Tssm, same session as DA approval (no user switch at seq 7) [atlas, observed]. Maker records the loss on the DA. The Loss Approval screen (layout 202026) is VISIBLE to the Maker Auto_Multi_Orga (master grid readable, filter by Document No) [observed 2026-10-01].
- G11-1: Checker Auto_Tssm approved loss 639 in the same session right after DA 1358 (no user switch) (upgraded from [atlas, observed] to [observed 2026-10-01 G11-1]).
- For the Checker on a Pending loss record: **Forward ON, Reject OFF** (on the DA itself the Checker's Reject was ON) [observed 2026-10-01 G11-1]. After approval both buttons are disabled [observed 2026-10-01 G11-1].
- G11-2: Checker Auto_Tssm approved loss **640** right after DA 1359 (no user switch); Forward ON / Reject OFF again (confirmed on a second day) [observed 2026-10-05 G11-2].

## 3. Documents and master data
Loss record with Serial No (e.g. 637), Document No = the DA (1350), Document Type Dispatch Advice (DA-01), Status [observed]. Loss stock types for org 010104: 02 Damaged, 03 Expired, 04 Lost, 11 Variance Warehouse (05 Dummy inactive) [db snd_pr_stt_sku_stocktype]. The loss modal "Stock" list showed Damaged, Expired, SEP, Lost, Behalf 615, Variance; Loss Reasons: Area Closed, Order Change, Customer cancels delivery, On Customer Behalf [observed].
- G11-1: the loss Stock list shows **"Lost" twice** (Damaged, Expired, SEP, Lost, Lost, Behalf 615, Variance): duplicate master-data entry [observed 2026-10-01 G11-1]. Loss Reason options confirmed: Area Closed, Order Change, Customer cancels delivery, On Customer Behalf [observed 2026-10-01 G11-1] (was [observed]).
- SKU type codes shown on the loss detail: 02 = Damaged, 04 = Lost (upgrades the [db] codes to [observed 2026-10-01 G11-1]).
- G11-1 record: Serial **639**, Document No 1358, Document Type DA-01 -Dispatch Advice, Distributor 15108843 Auto KARACHI [observed 2026-10-01 G11-1].
- **One loss record per DA**, whatever the number of loss rows (serial +1 per DA with loss: 638 -> 639) [observed 2026-10-01 G11-1].
- G11-2: Serial **640** for DA 1359 (+1 vs 639): one record per DA confirmed on a second day [observed 2026-10-05 G11-2].

## 4. Inputs: screens and fields
Menu "Loss Approval" (layout 202026, DYL_202026). Master grid (364 rows on 2026-09-30, 365 after DA 1356; not sorted by serial, first row 372 then 1,2,3; breadcrumb can be stale; the row filter persists across reopen) with filters such as rowfilter_TXT__tstmdocno; columns Serial No, Document No, Status. Detail tab lists SKU Type with dispatched/received quantities. Tabs must be real-clicked. Forward opens a Comments popup [observed].
- G11-1: menu path Transaction > Loss Approval (search "Loss Approval"); screen title "Loss Approval Master"; grid columns Serial No, Document Type, Document No, Distributor Code, Distributor Name, Status; 74 pages of history; default order not by serial (372 first, then 1, 2, 3 ...) [observed 2026-10-01 G11-1] (confirms the earlier order observation).
- Form: Serial No, Document No, Document Type (a blank form shows "NTN"), Status [observed 2026-10-01 G11-1].
- Tab "Loss Approval Detail": one row per product AND loss stock type: Product, SKU Type, Dispatch CS/DZ/PC, Received CS/DZ/PC, Loss CS/DZ/PC. **The loss reason is not shown here** [observed 2026-10-01 G11-1].

## 5. Process: the business steps in order
1. [Maker] on the DA: Add loss to line (Stock, Loss Reason, CS), Calculate, save line (see dispatch_advice.md).
2. [Checker] Navigate to Loss Approval; sort Serial No descending (one header click) [observed].
3. [Checker] Open the record (Serial 637, DA 1350, Pending for approval); verify detail: 20050310 type 02 Damaged 4 CS and 04 Lost 2 CS of 70 dispatched / 64 received; 62690363 type 02 Damaged 5 CS of 60 / 55 [observed].
4. [Checker] Forward with comment "Auto" -> "Forwarded successfully"; status Approved [observed] (11:7:00760001).

G11-1 walk, loss 639 (standard vocabulary, trace keys) [observed 2026-10-01 G11-1]:
1. [Maker] Add loss to DA 1358 lines; Click Calculate; Save line (11:2:00100001).
2. [Checker] Approve DA 1358 (creates loss record 639, Pending for approval) (11:5:00740001).
3. [Checker] Navigate to Loss Approval; Filter Document No 1358 -> Serial 639, Pending for approval (11:7:00760001).
4. [Checker] Open Loss Approval Detail; Verify rows 20050310 | 02 | 70 | 64 | 4, 20050310 | 04 | 70 | 64 | 2, 62690363 | 02 | 60 | 55 | 5 (11:7:00760001).
5. [Checker] Click Forward; Enter Comments "Automation Approval"; Save -> "Forwarded successfully"; grid Status Approved (11:7:00760001).
6. [Maker] Verify Stock Inquiry: no 02 Damaged / 04 Lost row created (11:9:02800001).

## 6. Outputs and effects
Live-verified 2026-10-01 (DA 1356, loss 1 CS Damaged, reason Area Closed): after the maker's Forward (DA Pending) the Loss Approval filter Document No 1356 gave 0 rows; after the checker approved the DA it gave Serial 638, Document Type DA-01 - Dispatch Advice, Distributor 15108843 Auto KARACHI, Status Pending for approval (serial +1 per DA with loss: 637 -> 638). Detail tab: 62740537, SKU Type 02 (Damaged), Dispatch CS 5, Received CS 4, Loss CS 1 [observed]. A Pending loss does not block the stock posting of the received (net of loss) quantity, and no 02 - Damaged stock row exists for 62740537 on 2026-10-01 or 09-30 [observed]; the loss approval (checklist L21) was not run yet, so the effect of APPROVING a loss remains unknown (superseded 2026-10-01 G11-1: L21 run on loss 639; approving creates no stock row, see below).
Loss record Approved. The stock effect is NOT confirmed: after approval Stock Inquiry still showed only Sound rows for 20050310 and 62690363, with no 02 Damaged or 04 Lost row in any warehouse [observed]. Where approved losses land (claims, later job, another screen) is [unknown]; a claim loss log table exists (snd_lg_cel_claim_exe_loss_log) [db] but its link is [inferred] only. (Superseded 2026-10-01 G11-1: the stock effect IS now confirmed as none in Stock Inquiry; where the loss goes outside stock, e.g. claims, stays [unknown].)
- **G11-1: approving loss 639 created NO stock row**: no 02 Damaged / 04 Lost rows for 20050310 or 62690363 on 2026-10-01 after approval; Stock Inquiry row count stayed 39; Sound In/Closing moved only by the received quantity of the DA (+64, +55) [observed 2026-10-01 G11-1]. Closes checklist L21.
- After Forward the grid shows Status **Approved** while the open form still shows Pending until reopened [observed 2026-10-01 G11-1].
- G11-2: approving loss 640 again created no Damaged/Lost row (Stock Inquiry row count 39) [observed 2026-10-05 G11-2].

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| (auto, when the checker APPROVES a DA with losses) | create | Pending for approval | system | observed 2026-10-01 (correction: not at the maker's Forward); confirmed G11-1 (Serial 639) [observed 2026-10-01 G11-1] |
| Pending | Forward | Approved | Checker | observed; confirmed G11-1 [observed 2026-10-01 G11-1] |
| Pending | Reject / Terminate | Rejected / Terminated | Checker | db (DALossApproval statuses 01-05); G11-1: Reject is DISABLED for the Checker on a Pending record [observed 2026-10-01 G11-1], so this path is not reachable on screen today |
| Approved | (any) | - | - | Forward and Reject disabled [observed 2026-10-01 G11-1] |

## 8. Rules and validations
- The loss record appears automatically at the DA approval; the manual "Loss Approval Request" flow is not needed [observed]. Correction 2026-10-01: earlier text and the default said "at maker Forward"; live shows no record after Forward and a record right after the DA approval.
- Received = dispatched - loss [observed].
- In the loss modal the second row reuses ids with _0 after the first is saved; line save ids are _1, _2 by row [observed].
- Forward needs a comment [observed, same popup as DA]. G11-1: Comments window mandatory [observed 2026-10-01 G11-1].
- One loss record per DA; one detail row per product and loss stock type (two loss rows of the same type on one line would aggregate; Damaged and Lost on one line give two rows) [observed 2026-10-01 G11-1].
- Approving a loss has no stock effect in Stock Inquiry [observed 2026-10-01 G11-1].

## 9. Messages
"Forwarded successfully" [observed]. Loss row save shows no toast.
- G11-1: Checker Forward with comment "Automation Approval" -> "Forwarded successfully" [observed 2026-10-01 G11-1]. Loss-window row Save / Cancel show no message [observed 2026-10-01 G11-1].
- G11-2: "Forwarded successfully" on the Checker Forward (second day) [observed 2026-10-05 G11-2].

## 10. Dependencies
Reads the DA (document number, lines, losses). Hands to stock reporting (unclear) and possibly claims [inferred]. (Superseded 2026-10-01 G11-1 for stock: hands nothing to Stock Inquiry; a hand-off to claims remains [inferred].)
- Needs the DA approved first (the record does not exist before) [observed 2026-10-01 G11-1].

## 11. Test design hints
- Positive: approve one loss; two loss rows on one line; losses on several lines; detail matches entered values.
- Negative: Reject the loss; Forward without comment; try loss approval before the DA is approved; maker tries to approve.
- Boundary: loss = whole line; loss 1 CS; loss greater than dispatched quantity.
- Trap: a green "Forwarded successfully" does not prove any stock moved; stock effect is unverified. (Superseded 2026-10-01 G11-1: the stock effect is verified as none; see the trap below.)
- G11-1 additions [observed 2026-10-01 G11-1]:
  - Positive: one DA with Damaged + Lost on one line and Damaged on another -> ONE record with three detail rows (02/04/02), Dispatch/Received/Loss per row.
  - Positive (business effect): after approval assert NO new Damaged/Lost row in Stock Inquiry and unchanged row count; do not expect a stock posting.
  - Negative: Checker Reject on a Pending record is disabled (assert the button state, not a Rejected status).
  - Negative: filter Loss Approval by a DA that is still Pending -> no record.
  - Traps: **loss approval has no stock effect**, so a test asserting Damaged stock after approval would fail; the master grid default order is not by serial (372 first), so the framework's "click Serial No header then row 1" can open the wrong record: filter by Document No instead; the loss reason is not shown on the approval detail, so it cannot be verified here; the form shows Pending after Forward until reopened.
- G11-2: the no-stock-effect rule and the Reject-disabled button state reproduced on 2026-10-05; both are stable regression checks [observed 2026-10-05 G11-2].

## 12. Open questions
Q: Where do approved DA losses appear as stock (Damaged/Lost rows)? | Default: not in Stock Inquiry same day | Evidence: none after DA approval with the loss Pending (2026-10-01); loss approval itself still to run (L21).
ANSWERED 2026-10-01 (L21 / loss stock effect, G11-1): approving a DA loss creates NO stock row and changes no Stock Inquiry figure (loss 639: no 02/04 rows for 20050310, 62690363; 39 rows unchanged) [observed 2026-10-01 G11-1]. Where the loss is used outside stock (claims) stays open as Q-LA1.
ANSWERED 2026-10-01 (Q06): created at the DA approval, not at Forward [observed: 0 rows after Forward, Serial 638 after approval].
Q: May the maker approve losses? | Default: no | Evidence: untested.
Q-LA1: Is an approved loss used anywhere else (claim to the supplier, finance, a claim loss log)? | Default: claim record only, no stock effect | Class: C | Evidence: no stock row after approval; table snd_lg_cel_claim_exe_loss_log exists [db, name only].
Q-LA2: Why is Reject disabled for the Checker on a Pending loss record while the workflow declares Rejected? | Default: losses cannot be rejected on this screen; do not design a Reject case | Class: B | Evidence: Serial 639 Pending, Forward ON / Reject OFF [observed 2026-10-01 G11-1].
Q-LA3: Is the duplicate "Lost" entry in the loss Stock list two different stock types? | Default: master-data duplicate; use the first | Class: A | Evidence: list shows Lost twice [observed 2026-10-01 G11-1].
- G11-2: BA3 (where losses appear) is merged into Q-LA1 in OPEN_QUESTIONS.md: the stock part is answered (none, two days), claims stay open.

## 13. Sources
runs/PILOT-DA-GIN/20260930-1615/exec/learning_block2a.json, learning_block3a.json, learning_block3b.json; LIVE_FINDINGS.md; framework_atlas/flows/00760001.md, 00750001.md; framework_flows/TC-DA-01_executed.md (TC-DA-03 and re-run), DISPATCH_ADVICE.md parts 7-8; DB snd_pr_stt_sku_stocktype, wkf_wf_wfs_workflow_status (DALossApproval), snd_lg_cel_claim_exe_loss_log (name only).
- G11-1 learning walk: learning_sessions/2026-10-01_G11-PK_session1_log.md (seq 2 loss window, seq 7, seq 9) and learning_sessions/2026-10-01_G11-PK_session1_report.md (§3 rules 1-2, §6 defect 5, §7 Loss Approval "first row" drift).
- G11-2: learning_sessions/2026-10-05_G11-PK_session2_log.md (seq 7, seq 9).
