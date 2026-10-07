---
name: feedback-post-training-workflow
description: "After S&D training, QA members start from a short request or one-liner (no Jira), AI execution follows Claude's own trained steps (never existing framework data), and the output is Regress Master SQL"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b5778f77-fda9-45aa-a9b0-f6d24e0e917f
  modified: 2026-10-07T13:17:22.464Z
---

The QA lead's rule, stated 2026-10-07:
1. After training, the team will not start from Jira tickets. They give a **short request or one-liner** (e.g. "create one order and order detail with two products script"). Claude runs the AI cycle with `/qa-os:quick` (skill quick-script) and generates the **SQL scripts for Regress Master** (selenium-framework-db / CTA_CONFIG_ASSERTION), plus rollback and case data.
2. **While executing the flow, Claude does not use existing Selenium framework data.** No case-data workbook rows, no fct_pr_sef event chains, no atlas flow steps. It runs from its **training** and the **test steps it wrote itself**. The framework DB is only read when generating the SQL (ids, conventions, reuse of an identical screen/field definition).

3. **The AI cycle executes only ONE case's data**, following the test steps, to identify the **screens, elements, element ids and tabs (tab ids)** plus the messages. It is never one live run per case. When a request asks for "N test cases", all N become case-data rows for Regress Master and only the single representative case runs live. The QA lead stated this twice on 2026-10-07; the first quick run wrongly executed 4 orders because the instruction arrived late.

**Why:** the point of training is that Claude knows the business; replaying the old framework would just copy its stale data and drift (FRAMEWORK_DRIFT).

**How to apply:**
- Treat the request text as the requirement; don't ask for a Jira key.
- Stop and ask for training when a screen is untrained.
- Group walks that follow the framework are allowed only when a trainer explicitly asks for one as training (knowledge-intake method C).

Related: [[project-qaos-quick-mode]], [[feedback-group-flow-execution-rules]]
