# Sales Return: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]**, **[db]**, **[inferred]**, **[unknown]**.
Last updated: 2026-10-01. Source flows: atlas `00070001` (group 11 seq 34 Sales Return), `00700001` (seq 36 Sales Return View), `00730001` (seq 37 Sales Return View Approval), `00710001` (seq 38 Sales Return Status Change). Not yet replayed live. Goods Return Note (seq 48-49) is in the inbound-stock pages.

## 1. Purpose
A sales return records goods an outlet gives back after delivery (rejected, damaged, wrong, price dispute). It reverses part of a delivered cash memo: the returned quantities and amount are authorised by a checker and later picked up and received into the warehouse. [inferred from document types and names]

## 2. Actors and roles
Maker: `Auto_Multi_Orga` creates (seq 34) and views/forwards (36). Checker: `Auto_Tssm` approves (37, switch point). Back to `Auto_Multi_Orga` for the status change (38) [atlas]. Workflow `SalesReturnApproval` (event `SR`) [db: wkf_wf_weo_wrkflw_event_orga]; a separate `SRWithoutReferenceApproval` exists for returns without a cash memo [db].

## 3. Documents and master data
- Document type `CM-02` "Sales Return" (nature SR), stored in the cash memo tables (`snd_tr_cmm_cashmemo_master`, reference to the original cash memo `tcmm_ref_docno`) [db]. Statuses: 01 Authorized, 02 Un-Authorized, 03 Cancelled, 04 Picked [db: snd_pr_dos_documentstatus CM-02]. Related: `CM-04` Fresh Sales Return, `CM-07` Sales Return Without Reference, `CM-08` Customer Account Closed, `CRN-02` Credit Note (Sales Return) [db: snd_pr_dot_documenttype].
- Return reasons by document type CM-02 (for example Item Out of Stock/No Substitute, Short of Cash, Area Closed, Price Difference) [db: glb_pr_rnt_reason_type]; the label Reason Type on screen [atlas].

## 4. Inputs: screens and fields
- **Sales Return** (menu `Sales Return`, option DYL_201801) [atlas]: **PJP Number**, **Date From**, **Date To**, **Outlet Name** (dropdowns/dates); click the document-number header, pick the outlet row, Save. Detail tab (tab_9): per row Edit, **CS**, **PC**, **Reason Type**, row Save/Cancel; buttons Validation and Save. Result block read-only: **Gross Amount**, **Discount**, **Tax**, **Net Amount** [atlas].
- **Sales Return View** (menu `Sales Return View`, option SALESRETURNVIEW): **PJP Number**, **Date From**, **Date To**, row filter Outlet Code; open the return; Forward button, comments, Save; shows Gross/Discount/Tax/Net and a row_1_status [atlas].
- **Sales Return View Approval**: same screen layout for the checker; select document, Forward with comments, status checked [atlas].
- **Sales Return Status Change** (option SALESRETURN-STATUSCHANGE): **PJP Number**, **GIN Number** (REPO_GINNO), filter by Document Date, open the row; Validation then `savesalePick` [atlas].

## 5. Process: the business steps in order
1. [Maker] Navigate to Sales Return; Choose PJP Number, Date From, Date To, Outlet Name; open the outlet's cash memo. (11:34:00070001)
2. [Maker] Edit line: Enter CS/PC, Choose Reason Type; save the row. Expect: row message.
3. [Maker] Validate. Expect: `Validation successfully`. Gross/Discount/Tax/Net shown and compared with the workbook.
4. [Maker] Save. Expect: `Save successfully`. Return is Un-Authorized [inferred].
5. [Maker] Navigate to Sales Return View; open the return; Forward with comments. Expect: status Pending for approval (row_1_status) [atlas]; `Please Enter the Comments` if the comment is empty (11:36:00700001).
6. [Checker] Login; Sales Return View Approval; open; Forward with comments. Expect: status Approved/Authorized (11:37:00730001).
7. [Maker] Login; Sales Return Status Change; Choose PJP Number and GIN Number = GIN1; open the return; Validation; save pick. Expect: message from `SR_StatsChang_DTL_SAVE_ASSR` [unknown text]; return becomes Picked (04) [inferred] (11:38:00710001).

## 6. Outputs and effects
- A CM-02 document with returned quantities and reversed amounts linked to the delivered cash memo [db/inferred].
- On Picked, the goods are collected on the vehicle and handed to the Goods Return Note flow, which brings them back into the warehouse stock (inbound-stock pages) [inferred]. No stock moves at Save or at approval [inferred].
- A Credit Note (Sales Return) `CRN-02` may follow in finance [db: type exists; trigger [unknown]].

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| (none) | Save | Un-Authorized (02) / Draft | Maker | [inferred] |
| Draft | Forward | Pending for approval (wf 02) | Maker | [atlas flow, status text [unknown]] |
| Pending | Forward (approve) | Authorized (01), wf 03 | Checker | [db] |
| Authorized | Status Change, save pick | Picked (04) | Maker | [inferred] |
| any | Cancel | Cancelled (03) | [unknown] | [db] |

## 8. Rules and validations
- `Return quantity should not greater than ordered quantity.` [atlas toast, 3 occurrences]: return cannot exceed what was ordered/delivered on the cash memo.
- Validation must pass before Save; comments are mandatory on Forward (`Please Enter the Comments`) [atlas, 9 occurrences].
- Reason Type mandatory per returned line [inferred].
- Approver differs from maker [atlas switch point].

## 9. Messages
`Validation successfully`; `Save successfully`; `Forwarded successfully` (8 times on the detail screen); `Return quantity should not greater than ordered quantity.`; `Please Enter the Comments` [atlas toast history, all recorded by the framework, none observed live yet].

## 10. Dependencies
Reads a delivered cash memo of the PJP and outlet (so seq 33 or an equivalent delivery state must come first) and `REPO_GINNO` (Status Change). Hands over a Picked return to the Goods Return Note (seq 48-49), and credit/value to settlement.

## 11. Test design hints
Positive: return 1 CS of one line, validate, save, forward, approve, status change to Picked; amounts match the workbook (Gross, Discount, Tax, Net). Negative: quantity above ordered; CS and PC both 0; no Reason Type; Forward without comments; maker approves own return. Boundary: return = ordered quantity (full line); return of a line with discount/offer item (amounts pro-rated?, [unknown]); PC only vs CS only. A green run proves screen messages only; verify the CM-02 status in the DB and that stock did not move until the GRN.

## 12. Open questions (batched for the BA; each with a default)
Q: Is the return limited to quantity ordered or quantity delivered? | Default: delivered | Evidence: message says "ordered quantity".
Q: What does "Status Change" do exactly (Picked)? | Default: marks the authorised return as picked up by the DSR | Evidence: button `savesalePick`, status 04 Picked.
Q: Does the return reverse stock at approval or only at the GRN? | Default: only at the GRN | Evidence: no stock effect in the flows.
Q: Are discounts/offers on returned items reversed proportionally? | Default: yes (Discount shown) | Evidence: Discount field only.
Q: Can a return be made before the cash memo is marked delivered? | Default: no | Evidence: chain order only.

## 13. Sources
`framework_atlas/flows/00070001.md`, `00700001.md`, `00730001.md`, `00710001.md`, `group_11.md`; DB: snd_pr_dot_documenttype, snd_pr_dos_documentstatus, glb_pr_rnt_reason_type, wkf_wf_weo_wrkflw_event_orga, snd_tr_cmm_cashmemo_master. No SR table of its own exists (CM-02 lives in the cash memo tables).
