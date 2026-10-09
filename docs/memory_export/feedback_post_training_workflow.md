---
name: feedback-post-training-workflow
description: "After S&D training: one-liner requests (no Jira); AI execution follows Claude's own steps (never framework data); record one case per distinct path (group cases by path), other cases = data rows; output Regress Master SQL"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b5778f77-fda9-45aa-a9b0-f6d24e0e917f
  modified: 2026-10-08T05:47:58.529Z
---

The QA lead's rule, stated 2026-10-07:
1. After training, the team will not start from Jira tickets. They give a **short request or one-liner** (e.g. "create one order and order detail with two products script"). Claude runs the AI cycle with `/qa-os:quick` (skill quick-script) and generates the **SQL scripts for Regress Master** (selenium-framework-db / CTA_CONFIG_ASSERTION), plus rollback and case data.
2. **While executing the flow, Claude does not use existing Selenium framework data.** No case-data workbook rows, no fct_pr_sef event chains, no atlas flow steps. It runs from the **test steps Claude wrote** using its training. The framework DB is only read when generating the SQL, and only for table structure and free ids (see point 4; reusing existing definitions was dropped on 2026-10-08).

3. **The AI cycle records ONE case per distinct path, not per case and not per ticket** (QA lead, 2026-10-07; refined 2026-10-09). The live run exists to identify the **screens, elements, element ids and tabs (tab ids)** plus the messages. Cases that follow the same path (same screens, fields, buttons, order) and differ only in values or expected message become **case-data rows** of that one recording. Cases that perform different actions (e.g. remove a selection, type free text, change another field, continue on another screen) are a **separate path**, so each needs one recording of its own. At the step stage, group the cases by path, show the grouping to the QA member ("N paths for M cases"), then record one representative case per group. Checks the engine has no assertion for (list contents, "not shown twice", alert text) are flagged manual, not forced into the engine. Never one live run per case: the first quick run wrongly executed 4 orders of the same path (2026-10-07). Example SDMS-6084 (Off Days): 9 cases = 5 paths (save+reopen TC04/TC07; save+remove TC05/TC06; other field TC08; no-save dropdown checks TC01-03; HQ->DT TC09).

4. **Strict phase separation (2026-10-08).** Training knowledge is used only to write the cases and test steps. The executor (recorder) follows **only** the test steps and one data row: no business pages, no session logs, no training hints, no framework flows, ids or workbooks. It discovers and notes screens, elements, ids and tabs/tab ids live. The generator builds scripts **only** from that recording plus the cases' data rows, and reads the framework DB only for table structure and free ids; it never mirrors existing flows or screens.

The first Order Booking quick run (QUICK-20261007-OB) broke this. The recorder brief pointed to order_booking.md and carried UI hints, and the generator mirrored screens 000101/000102. Its scripts need a clean re-record.

**Why:** the point of training is that Claude knows the business; replaying the old framework would just copy its stale data and drift (FRAMEWORK_DRIFT).

**How to apply:**
- Treat the request text as the requirement; don't ask for a Jira key.
- Stop and ask for training when a screen is untrained.
- Group walks that follow the framework are allowed only when a trainer explicitly asks for one as training (knowledge-intake method C).

Related: [[project-qaos-quick-mode]], [[feedback-group-flow-execution-rules]]
