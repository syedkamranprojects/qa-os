# Document lifecycle: the cross-cutting approval pattern (S&D / DCODE)

Updated: 2026-10-01 (live blocks 1-3b)

Consolidated 2026-10-01 from the area pages. Tags as in the pages: [observed], [db], [inferred], [unknown].

## 1. The common pattern

Maker creates -> saves (Draft, grid status In-Active) -> Forward with a mandatory comment -> Pending for approval -> a different user, the Checker, opens the same document and uses Forward again -> Approved (Active / Authorized) [observed for DA, DA Loss, GIN up to Pending; db for GRN, SAN, Sales Return].

Rules that repeat across documents:
- **Verified Forward semantics (live 2026-10-01).** A **Draft** document's Forward belongs to the **Maker**: enabled for Auto_Multi_Orga, disabled for the Checker Auto_Tssm (GIN 29: Forward/Reject/Terminate all disabled for the Checker). A **Pending for approval** document's Forward is the **Checker's approval**: enabled for Auto_Tssm together with Reject and Terminate, disabled for the Maker (GIN 505; DA 1356 approved this way: "Forwarded successfully", grid Status Active, Approval Status Approved, Received Date set) [observed]. The **comment is mandatory** ("Please add comments"). Side effects happen at the checker's Forward: the DA approval creates the day's stock row and the **loss record** (no loss record exists after the maker's Forward; Serial 638 appears after the approval) [observed]. The workflow definition itself does not separate the people: GIN StockUpdateGIN v53 has Verify and Approve both for role 0005 [db].
- **One "Forward" button, two meanings.** The maker's Forward means "submit"; the checker's Forward means "approve". Reject and Terminate are the alternatives and were disabled for the Maker on Pending GIN/GRN rows [observed]. The framework therefore finds no separate "Approve" label.
- **Comment is mandatory** at Forward: "Please add comments" (DA), "Please Enter the Comments" (Sales Return), a Comments popup that needs text plus a blur (Tab) before Save; special characters are refused ("Do not use Special charters.") [observed/atlas].
- **Success message** is "Forwarded successfully" for both the submit and the approve action [observed].
- **Maker and checker are different users** (Auto_Multi_Orga / Auto_Tssm). A checker cannot create a DA ("Current user is not authorized to save this record!") [observed]. Self-approval: KPO_mp approved its own DA 570 [observed] and the GIN workflow declares Verify and Approve for the same role 0005 [db], so "must differ" is a QA convention, not an app control (contradiction resolved 2026-10-01; BA2 still asks if the business wants it enforced).
- **Approval has a business precondition** that can fail at the checker's step: GIN approval needs a same-day stock balance ("No stock balance found for products: [...]") [observed]; the DA approval is the step that creates it for the received product.
- **Silent Save** (no toast, no document number) means a mandatory field is missing (DA Type empty after Add) [observed 2026-10-01].
- **Reopen before Forward**: the document must be opened from the grid by its number (DA: switching tabs blanks the header) [observed].
- **Workflow statuses** in the DB: 01 Draft, 02 Pending for approval, 03 Approved, 04 Rejected, 05 Terminated [db: wkf_wf_wfs_workflow_status]; documents also have a document status (Authorized / Un-Authorized ...) and a grid Status (Active / In-Active), which are three different columns of the same state.

## 2. Per document type

| Document | Approval? | Statuses the pages give | Tag |
|---|---|---|---|
| Dispatch Advice (DA-01) | maker + checker | Draft; header shows Un-Authorized / Draft right after save, grid In-Active -> Pending for approval -> Approved, grid Active, Received Date = today; Rejected, Terminated [db] | observed |
| DA Loss record | checker only; record created by the system when a DA with losses is APPROVED (not at the maker's Forward) | Pending for approval -> Approved; Rejected/Terminated [db statuses 01-05] | observed |
| Order / cash memo (CM-01) | none | document 04 Ordered; execution 02 Confirmed -> 03 Planning completed (on a GIN) -> 13 Ready to dispatch / 10 Delivered/Invoiced; document 01 Delivered / 03 Cancelled; 02 Un-Delivered, 05 Amendment, 06 Re-attempt exist | observed/db |
| Goods Issue Note (GN-01) | maker + checker | Draft/In-Active -> Pending for approval -> Approved (doc 01 Authorized); Rejected -> doc 02 Un-Authorized; Cancelled doc 03 / wf 05 | observed (to Pending), db |
| Goods Return Note (GR-01) | maker + checker | Draft -> Pending -> Approved; Rejected/Terminated | db/inferred |
| Sales Return (CM-02) | maker + checker, and Status Change after approval | Un-Authorized (02) -> Pending -> Authorized (01) -> Picked (04); Cancelled (03) | inferred/db |
| SAN stock out | maker + checker | Draft (status I) -> Pending -> Approved (status A) | db |
| Deposit Slip | none active (approval row 00140002 inactive) | status I -> A with posting date | db |
| Cashmemo Reschedule / Status, Route Settlement, Cheque Status, DSR Adjustment, PJP Daily Inquiry Update, Transaction Inquiry, Stock Inquiry | none | see pages: execution 19 / 10; no status; instrument P/L/R/B/C/A; AD-07 01-04; n/a | db/inferred |

## 3. Known deviations in vocabulary

1. **Three status columns per document.** Workflow status (Draft / Pending for approval / Approved), document status (Authorized / Un-Authorized / Cancelled; Picked for CM-02) and the grid Status (Active / In-Active). A DA header right after save shows Un-Authorized while the grid says In-Active and Approval Status says Draft [observed]. Assert on one column and name it.
2. **"Confirmed" vs "Ordered" (resolved 2026-10-01).** "Confirmed" is its own execution status 02 (identifier ALC), "Planning completed" is execution 03 and "Ordered" is document status 04 and execution status 01 [db]. The Transaction Inquiry Document Status column shows the execution status text: booked orders on a GIN read "Planning completed" [observed].
3. **DA Active / In-Active** is the grid Status, not an approval status; the approval states are Draft / Pending for approval / Approved.
4. **Cancelled** exists as document status 03 and as execution status 05 [db].
5. **Authorized (01) means approved** for GIN/Sales Return/AD-07, while for the DA the page uses Approved/Active. AD-07 also has 03 Adjustment.
6. **Deposit Slip and Cheque** use letter codes (I, A; P, L, R, B, C, A), not words.
7. **Menu names differ from flow names**: Dispatch Advice has no approval menu entry (approval is the same screen, Forward); GIN/GRN approvals are on the same screens; "Dispatch Advice Approval", "OTC Stock Out" and "Opening/Closing Stock" screens were not found in the live menu [observed].
8. **Loss approval** is a second workflow on the same DA, started by the DA approval: DA Approved does not mean the loss is approved (DA 1356 Approved, loss Serial 638 Pending) and a Pending loss does not block the stock posting of the received quantity [observed].
9. **Reject/Terminate** transitions are only [db]; none was executed live.
