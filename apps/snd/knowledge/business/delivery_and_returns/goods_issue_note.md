# Goods Issue Note (GIN): how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]** seen live in a replay or recording, **[db]** declared by the application DB or the framework tables, **[inferred]** concluded by Claude from names or structure (to be confirmed), **[unknown]** not determinable yet.
Updated: 2026-10-01 (live blocks 1-3b)
Last updated: 2026-10-01. Source flows: atlas `00050001` (group 11 seq 20), `00780001` (seq 23), `02810001` (seq 24).

## 1. Purpose
A GIN is the document by which the distributor's stock controller issues stock out of the warehouse to a delivery man (DSR) for the cash memos (orders) he will deliver that day. It turns allocated orders into a load list: the cash memos of one PJP/DSR are picked, the SKU totals are summed, and the stock leaves the warehouse once the checker approves. [inferred from names and observed screens]. Position in the Daily Cycle: after Stock Allocation / Delivery Date Change (seq 12-19), before delivery (Cashmemo Status seq 33), returns (seq 34-38) and settlement.

## 2. Actors and roles
- Maker = Stock Controller, user `Auto_Multi_Orga` [observed, atlas group 11]. Checker = `Auto_Tssm` [observed]. Maker and checker are different users in the framework [switch point at seq 23]; the app does not declare it (see below) [corrected 2026-10-01: was tagged observed].
- **Live-verified 2026-10-01 [db, read-only SQL]: org 010104 (and 010105) use workflow `StockUpdateGIN` (latest v53), NOT `StockUpdateGIN4Level`** (that one is bound to the parent orgs 0101 and 0102). StockUpdateGIN has two user tasks in sequence, "Verify" then "Approve", BOTH candidate group 0005 (role 0005 in 010104 = "Distributor Role", not an authorizer role); gateways: forwarded false returns to Verify, cancelled true ends the process; the end listener StockUpdateProcess applies the stock update. **Separation of duty is therefore NOT declared in the workflow**; maker vs checker is a QA convention. StockUpdateGIN4Level v3 (parents only): Verify 0005, Approve 1 0008, Approve 2 0005, Final Approve 0008 (0008 = Territory Manager Role, authorizer). GINApprovalSaga v29 service tasks after final approval: MarkGinApprovedSaga, MarkGinApprovedReversalSaga, updateStock, DecreaseCashmemoQuantity, DeleteCMReference, revertCMReferencesByGinno, GeneratePjpHeadDailySaga; the field setting flips docStatus 02 -> 01 and status I -> A at final approval. Whether Auto_Multi_Orga / Auto_Tssm hold role 0005 / 0008 could not be checked (user TSSM has 0008 in 010104).
- Workflow definition `StockUpdateGIN4Level` (event `GIN`, parent orgs), with sagas `ginApprovalSaga`, `ginManualApprovalSaga`, `ginGrnCancelSaga`, `AUTO_GIN_SAGA` declared [db: wkf_wf_weo_wrkflw_event_orga, wkf_wf_wfs_workflow_status.wwes_event_id]. "4Level" gives four approval levels for the parent orgs only; org 010104 has two (Verify, Approve), one checker click was used in the framework [db 2026-10-01; whether a second Forward is needed after Verify was never observed because GIN 505 approval was refused].

## 3. Documents and master data
- Document type `GN-01` "Goods Issue Note" (group GN), statuses 01 Authorized, 02 Un-Authorized, 03 Cancelled [db: snd_pr_dot_documenttype, snd_pr_dos_documentstatus]. Header table `snd_tr_gnm_gingrn_master` (shared with the Goods Return Note `GR-01`), lines `snd_tr_gnm_gingrn_detail`, links to cash memos in `snd_tr_gnm_gingrn_refinfo` (refdoctype `CM-01`) [db].
- Line transaction nature: 47 "Sales" or 49 "Manual" [db: snd_pr_trn_trans_nature]. Suggested Type: 0001 "Cashmemo List" (default) or 0002 "Manual" [db: glb_pr_sgt_suggested_types].
- Number: the GIN of the 2026-09-30 replay was 505 [observed]. Repo `REPO_GINNO` carries it to later flows [atlas].
- Master data: Delivery Man PJP (`02112-AutomationDSR` on dev), warehouse, vehicle, DSR, products with stock [observed].

## 4. Inputs: screens and fields
Menu "Goods Issue Note" (`/ngui/good-issue-notes/GIN`, option `GOOD_ISSUE_NODE`) [observed, atlas].
- Master grid -> **Add** opens the Header [observed]. **Delivery Man PJP** (dropdown; fills DSR, Warehouse, Vehicle by itself) [observed]. **Delivery Date*** (mandatory, must be typed) [observed/atlas]. GIN Date = today [observed]. Suggested Type defaults to Cashmemo List [observed].
- Tab **Cash Memo Selection** (atlas screen `000502`): filter by DSR Name, header checkbox selects all; grid fields **Actual CS / Actual DZ / Actual PC** [atlas]. 9 eligible cash memos on 2026-09-30 [observed].
- **Button states observed 2026-10-01** (read from aria-disabled, nothing clicked; GIN grid 14 rows, 3 pages of 5; statuses Pending for approval 505/169/131/128/113/69/67/61/27, Rejected 104/103, Draft 29/22/20; all Status In-Active; approved GIN 504 is not listed): Maker Auto_Multi_Orga on Pending 505: Add enabled, Forward/Reject/Terminate/De-linking/Save All DISABLED; Maker on Draft 29: Add, Forward, De-linking, Save All ENABLED, Reject/Terminate DISABLED. Checker Auto_Tssm on Pending 505: Forward, Reject, Terminate, Add ENABLED, De-linking and Save All disabled (De-linking probably needs selected rows); Checker on Draft 29: Forward, Reject, Terminate DISABLED. No approval log / history control exists on any tab for either user [observed].
- Tab **Detail** (`000503`): SKUs with Current Stock, Suggest, Actual; read-only **Gross Amount**, **Weight (Kg)**; button **Save All** (`saveallBtn`) [observed/atlas].
- Forward (`000504`): open the GIN from the master grid (filter by Document No = GIN number), click Forward, Comments popup, Save [observed].

## 5. Process: the business steps in order
1. [Maker] Navigate to Goods Issue Note; Add. (11:20:00050001)
2. [Maker] Choose Delivery Man PJP; Enter Delivery Date; GIN Date is today.
3. [Maker] Go to tab Cash Memo Selection; select all cash memos (header checkbox). Expect: `actual quantity could not be beyond the suggested quantity.` if an Actual exceeds Suggest [atlas toast history].
4. [Maker] Go to tab Detail; Save All. Expect: `Saved successfully.` GIN is created Draft / In-Active [observed].
5. [Maker] Remember GIN No as GIN1; Open GIN1; Forward with comment. A **Draft GIN's Forward belongs to the Maker** (enabled for him, disabled for the Checker); Expect: `Forwarded successfully`; Approval Status = Pending for approval [observed; button states verified 2026-10-01].
6. [Maker] Logout; [Checker] Login; Open GIN1; Forward (Approve) with comment (11:23:00780001). **The Pending GIN's Forward is the Checker's approval** (enabled for him, disabled for the Maker) [observed 2026-10-01]. Expect: `Forwarded successfully` [atlas toast history]. Observed 2026-09-30: refused with `No stock balance found for products: [20050308, 20050310, 62690363, 62740537, 69997598]` [observed].
7. [Stock Controller] Check stock after GIN in Stock Inquiry (11:24:02810001): Period Type, Balance Date, Category, Brand -> refresh; filter warehouse and stock type; read In CS / Out CS / In PC / Out PC and closing; compare with workbook/DB [atlas].

## 6. Outputs and effects
- A GIN header in Draft/In-Active, then Pending for approval, then Active/Approved [observed for the first two; third [inferred] from the Dispatch Advice analogy and atlas].
- On approval the issued quantities are expected to leave the warehouse stock for the DSR [inferred from the "No stock balance found" refusal at approval and the Out columns of Stock Inquiry]. Stock balance rows live in `snd_tr_ssb_salestock_balance`, keyed by balance date, with reserved-quantity columns [db].
- Linked cash memos advance their execution status: `03 Planning completed` (identifier GIN) when put on a GIN, `13 Ready to dispatch/Packed` (identifier GINAPPRVD) after GIN approval; `24 CM adhoc addition in GIN` and `25 CM adhoc removal from GIN` exist for changes [db: glb_pr_exs_execution_status CM-01; the mapping to the GIN steps is [inferred]].

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| (none) | Save All | Draft, In-Active | Maker | [observed] |
| Draft | Forward with comment | Pending for approval (wf 02) | Maker | [observed] |
| Pending | Forward/Approve | Active, Approved (doc status 01 Authorized, wf 03) | Checker | [db]; attempt failed on a stale day |
| Pending | Reject | wf 04 Rejected (doc status 02 Un-Authorized) | Checker | [db] (such GIN rows exist) |
| any | Cancel | doc status 03 Cancelled, wf 05 Terminated | [unknown] | [db] |
Workflow statuses: 01 Draft, 02 Pending for approval, 03 Approved, 04 Rejected, 05 Terminated [db: wkf_wf_wfs_workflow_status].

## 8. Rules and validations
- Delivery Date is mandatory [atlas]. Actual quantity cannot exceed the suggested quantity [atlas toast, 21 occurrences].
- A GIN without lines cannot be saved: `gin detail bean is going to be empty.` [atlas, 9 occurrences].
- Maker and checker must differ in the framework; the workflow declares both steps for the same role 0005 [db 2026-10-01], so this is a QA convention, not an app control [corrected from observed].
- On a Pending GIN the Maker cannot Forward, Reject, Terminate or De-link; on a Draft he can Forward and De-link (add/remove cash memos) but not Reject/Terminate; the Checker can Forward, Reject and Terminate only Pending GINs, nothing on Drafts [observed 2026-10-01]. So only the Checker can cancel (Terminate) a GIN, and only while Pending.
- Detail lines on GIN 505 and Draft 29 show Current Stock 0-0-0 for every line (Suggest = Actual) although Stock Inquiry shows available stock; likely Current Stock is net of allocation [inferred; unexplained].
- GIN 505 holds 9 cash memos (1988, 1995-2002), all order type 01-Back Office, order booker PJP 02111-AutomationOB1, delivery man PJP 02112-AutomationDSR, section 101010101101-Automation_Testing_Section; Detail 5 SKU lines: 20050308 18 CS 16 PC, 20050310 40 CS, 62690363 24 CS 16 PC, 62740537 63 CS, 69997598 48 PC [observed]. Draft 29: 6 lines (e.g. 20043109 45 CS 72 PC, 62740537 81 CS) [observed].
- Approval needs a stock balance for each product on the stock date; balances are keyed by calendar day, so stock received the previous day gave `No stock balance found...` [observed].
- GIN header holds `tgnm_stock_date` and `tgnm_delivery_date` [db]; which one the check uses is [inferred] (stock date).

## 9. Messages
`Saved successfully.` (Save All); `Forwarded successfully` (Forward and Approve); `No stock balance found for products: [...]` (approval); `actual quantity could not be beyond the suggested quantity.`; `gin detail bean is going to be empty.`; `Do not use Special charters.` (comment popup); `Updated successfully` x1 and raw key `workflow.messages.forward` x2 on the approval screen (atlas toast history).

## 10. Dependencies
Reads: cash memos allocated by Stock Allocation / auto-allocation and re-dated by Delivery Date Change (see the order planning pages); stock received by Dispatch Advice (see the inbound stock pages). Hands over: `REPO_GINNO` to Cashmemo Reschedule (seq 32), Sales Return Status Change (38), Deposit Slip (39) [atlas]; approval is the point at which stock is out for delivery. Day boundary: stock must exist on the balance date of the approval; run receive, order, GIN, approve inside one calendar day.

## 11. Test design hints
- Positive: create a GIN for PJP 02112 with all 9 cash memos, Save All, Forward, approve as another user, check Out CS in Stock Inquiry rises by the issued quantity.
- Negative: no cash memo selected; Actual > Suggest; same user approves own GIN (refusal text [unknown]); no Delivery Date; Forward without comment; stock received yesterday (known failure).
- Boundary: Actual = Suggest; Actual = 0 for one SKU; cash memo with several SKUs; Delivery Date today vs future.
- A green framework run does not prove stock arithmetic: the stock checks assert through screenshot_ASSR and a workbook comparison that fails on a busy day [observed for seq 9, DISPATCH_ADVICE notes].

## 12. Open questions (batched for the BA; each with a default)
Q: Does GIN approval deduct warehouse stock immediately, or only reserve it until dispatch? | Default: deducts Sound stock on approval | Evidence: only the refusal message is observed.
Q: Which date does the approval stock check use (GIN Date, Delivery Date, stock date)? | Default: stock date = today | Evidence: observed refusal the day after receipt.
ANSWERED 2026-10-01 (Q35): org 010104 uses StockUpdateGIN v53: two steps (Verify, Approve), both role 0005; four levels exist only for parent orgs [db].
ANSWERED 2026-10-01 (Q36, partly): the Maker can De-link (remove cash memos) on a Draft GIN and not on a Pending one; approved GINs are not listed on the screen; adhoc add/remove statuses 24/25 remain the only path for an approved GIN [observed].
ANSWERED 2026-10-01 (Q37, partly): only the Checker can Reject or Terminate, only while Pending; effect of Terminate on stock and cash memos still unknown (default: cash memos return to the selection pool).

## 13. Sources
`framework_atlas/flows/00050001.md`, `00780001.md`, `02810001.md`, `group_11.md`; `apps/snd/knowledge/ui.md` section "Verified in the group 11 replay"; `framework_flows/STEP_SHEET_DRAFT_next.md`; learning_block1.json, learning_block3a.json (live 2026-10-01), LIVE_FINDINGS.md L05, L10, C3; DB wkf_wf_weo_wrkflw_event_orga, act_re_procdef (StockUpdateGIN v53), srol roles; DB tables snd_tr_gnm_gingrn_master/detail/refinfo, snd_pr_dot_documenttype, snd_pr_dos_documentstatus, snd_pr_trn_trans_nature, glb_pr_sgt_suggested_types, glb_pr_exs_execution_status, wkf_wf_weo_wrkflw_event_orga, wkf_wf_wfs_workflow_status, snd_tr_ssb_salestock_balance. Note: transactional rows exist only for org 0101 in snd-schema (143k authorized GINs); org 010104 has the same document types and statuses.
