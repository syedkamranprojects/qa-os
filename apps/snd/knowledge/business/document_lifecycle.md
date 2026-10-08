# Document lifecycle: the cross-cutting approval pattern (S&D / DCODE)

Updated: 2026-10-01 (live blocks 1-3b); 2026-10-01 G11-1 consolidation (section 0); 2026-10-05 G11-2/2b consolidation (section 0b); 2026-10-06 G11-3 consolidation (section 0c); 2026-10-08 QA team written answers (section 0d)

Consolidated 2026-10-01 from the area pages. Tags as in the pages: [observed], [db], [inferred], [unknown].

## 0. Live-verified in learning session G11-1 (2026-10-01 evening) [observed 2026-10-01 G11-1]
Evidence: [learning_sessions/2026-10-01_G11-PK_session1_log.md](learning_sessions/2026-10-01_G11-PK_session1_log.md).
- **The pattern holds for five documents end to end**: Dispatch Advice (1358), DA Loss record (639), Goods Issue Note (506), Sales Return (COL26000000713, on the Sales Return View screen) and Goods Return Note (246): Maker saves (Draft / In-Active) -> Maker Forward + mandatory comment -> Pending for approval -> Checker opens the same document and Forwards -> Approved. Sales Return answers with a result window "Sales Return Status ... Success" instead of a toast; the others toast "Forwarded successfully".
- **Approved documents leave the working grid** for GIN, GRN and Sales Return View (only open documents are listed); the DA grid keeps the approved DA (Active / Approved / Authorized, Received Date set).
- **One Checker Forward is the final approval** for the GIN in org 010104 (stock Allocated -> Out immediately), although the workflow declares Verify + Approve (answers the earlier open point).
- **Exception to the Forward semantics**: on the Pending **DA**, the **Maker still had Forward and Reject enabled** (not clicked); on the Pending GIN they were disabled. Possible defect / Q-DA1.
- **Loss record**: on a Pending loss record the Checker has Forward but **Reject disabled**.
- **Stale form after Forward**: the form keeps showing "Draft" until the document is reopened from the grid; reopen before reading the status.
- **Approval preconditions confirmed**: GIN approval succeeds when the stock was received the same day and the cash memos' delivery date equals the GIN delivery date (the two earlier failure messages came from stale-day data).
- **Settlement precondition**: Route Settlement needs every earlier working day closed ("Following previous days not closed! Please close date. 2026-09-30").

## 0b. Confirmed and extended in learning sessions G11-2 / G11-2b (2026-10-05) [observed 2026-10-05 G11-2, G11-2b]
Evidence: [learning_sessions/2026-10-05_G11-PK_session2_log.md](learning_sessions/2026-10-05_G11-PK_session2_log.md), [learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md](learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md).
- **Second day, same pattern**: DA 1359, loss 640, GIN 507, Sales Return COL26000000714, GRN 247 followed the Maker save -> Maker Forward + comment -> Checker Forward = approval pattern with the same messages as on 10-01.
- **Sixth document end to end: SAN 96** (Stock Adjustment Admin): Maker Save ("Saved successfully", In-Active / Draft) -> Maker Forward ("Forwarded successfully", Pending for approval) -> Checker Forward ("Forwarded successfully", Active / Approved in ONE step). The Checker also has Reject on the Pending SAN (not clicked).
- **Posting is a separate lifecycle step for deposit slips**: Un Posted (after Save / Save All) -> Posted at Route Settlement; a posted slip is read-only. A route can show Complete while its slips are still Un Posted (10-01; Q-DS3). (superseded 2026-10-08: a Complete route with Un Posted slips is not a valid state; defect D-G11-2b-1 [stated 2026-10-08 QA Team])
- **Route and day lifecycle**: Route Settlement row Incomplete -> Complete (green, no Edit) when settled; the day is then closed on PJP Daily Inquiry Update (End Of Day + Complete -> Current Status E, "Record Updated Successfully"). Route Settlement refuses while the oldest earlier day is not closed.
- **Cheques**: after posting they read "Clear"; the only later transition offered is Bounce (one-way).
- **Sales return** ends as Picked (Transaction Inquiry, Document Type Sales Return); its source cash memo stays Delivered/Invoiced.
- **Comment rule**: the comment must really be typed and visible in the box before Save ("Please add comments" otherwise) [stated 2026-10-05 QA lead; observed].

## 0c. Confirmed and extended in learning session G11-3 (2026-10-06, with the QA Team Lead) [observed 2026-10-06 G11-3]
Evidence: [learning_sessions/2026-10-06_G11-PK_session3_log.md](learning_sessions/2026-10-06_G11-PK_session3_log.md).
- **Third day, same pattern**: DA 1360, loss 641, GIN 508 and GIN 509, Sales Return COL26000000715, GRN 248, SAN 97: Maker save -> Maker Forward + comment -> Checker Forward = approval, same messages.
- **Allocation is part of the order lifecycle**: Order Editing before the GIN needs the order unallocated; the edit save re-allocates it; a Cashmemo Reschedule unallocates it; a Reattempt order must be allocated again before a new GIN [stated 2026-10-06 QA Team Lead; observed].
- **Route lifecycle, full**: Incomplete (yellow) -> Edit refused while an order due today is undelivered ("Un-Deliver Order exists for today delivery!") -> Edit + row Save ("Saved Successfully") -> Complete (green, no Edit); slips Posted; cheques Clear. Day order: settlement -> DSR adjustment -> day close (E).
- **DSR Adjustment (AD-07)** is saved directly by the Maker after a confirm modal ("Are you sure you want to save transaction?" -> "Record Saved Successfully"); no approval step seen; status column not shown (Q53).
- **Cheque Status in the cycle** is a check only; Bounce is never pressed [stated 2026-10-06 QA Team Lead].
- **Deposit slip states** [stated 2026-10-06 QA Team Lead]: Un Posted slips are never blocked against each other (a memo may be allocated on several unposted slips); Route Settlement Save posts all the route's cash and cheque slips (Un Posted -> Posted) and adjusts the invoices; fully adjusted invoices leave the collection screens.
## 0d. QA team written answers (2026-10-08) [stated 2026-10-08 QA Team]
Evidence: [learning_sessions/2026-10-08_QA_Team_Review_answers.md](learning_sessions/2026-10-08_QA_Team_Review_answers.md).
- **Approval is by role through a workflow**: each setup and transaction has a predefined workflow naming the Submit and Approve role codes; R1 = two levels: 0001 NG User submits (Authorized N), 0002 TSSM approves; 0003 DSR and 0004 Warehouse are mobile roles (Authorized N); 9999 HQ bypasses the workflow where no approval is needed (BA2). Open: cnr1dev1 users' role codes and the KPO_mp self-approval (Q-RL1).
- **Stock moves on approval** of the document (add or deduct), never at Forward (Q58).
- **DSR Adjustment has no workflow** (Q53).
- **Deposit slips (production)**: auto-created Unposted from the DSR's mobile sync -> Posted when Route Settlement completes; the Back Office screen is the manual path. A settled route with Un Posted slips is a defect (Q-DS3, D-G11-2b-1).
- **Route**: settled state = Edit link gone (blank); colours are to be ignored (rule 17).
- **Cheques**: Cleared/Realized at posting (PK/BD) -> Bounced (Bounced Cheque option) reverses the invoice payment, outstanding at outlet level (BA11).
- **Cash memo after the GIN**: editable only when ORGA parameter CASHMEMO_EDIT = Y (quantity reduction, reason); Save reduces the approved GIN quantity (stated; not seen on three walks, Q-OE5).
- **Allocation** at Order / Cash Memo / Invoice creation: full, partial (available only) or none (unallocated, status Order) (Q16 / Q27).

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
| SAN stock out | maker + checker | Draft (status I) -> Pending -> Approved (status A) [db]; observed 2026-10-05: In-Active / Draft -> In-Active / Pending for approval -> Active / Approved, one Checker Forward | db; observed 2026-10-05 G11-2b |
| Deposit Slip | none active (approval row 00140002 inactive) | status I -> A with posting date [db]; screen Un Posted -> Posted at Route Settlement [observed 2026-10-05 G11-2b] | db; observed 2026-10-05 G11-2b |
| Cashmemo Reschedule / Status, Route Settlement, Cheque Status, DSR Adjustment, PJP Daily Inquiry Update, Transaction Inquiry, Stock Inquiry | none (2026-10-06: DSR Adjustment saved by the Maker without approval; Route Settlement performed by the Maker) | see pages: execution 19 / 10; no status; instrument P/L/R/B/C/A; AD-07 01-04; n/a [db]. Observed 2026-10-05: Route Status Incomplete -> Complete; cheques Clear (then only Bounce); PJP daily row Current Status E after End Of Day / Complete | db/inferred; observed 2026-10-05 G11-2b |

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
10. **Cheque "Clear" (2026-10-05)** is shown on screen but is not in the db instrument-status list (P/L/R/B/C/A); assert the screen text "Clear" [observed 2026-10-05 G11-2b].
11. **Cashmemo Status grid** shows Document Status "Ordered" (document status) for cash memos on an approved GIN, while Transaction Inquiry shows the execution text Ready to dispatch/Packed [observed 2026-10-05 G11-2].
