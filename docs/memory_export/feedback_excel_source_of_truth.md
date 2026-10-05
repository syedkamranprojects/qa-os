---
name: excel-source-of-truth
description: The QA member finalizes test steps in the Excel (Test Steps column); Claude executes from that Excel via import + check, never from its own draft.
metadata:
  type: feedback
---

On 2026-09-30 the user said: once the QA member has finalized the steps and updated the Excel's Test Steps column, Claude must use the Excel file to execute the flow through the Selenium MCP.

**Why:** the Excel is the record the QA team owns and validates; execution must match exactly what they approved, and edits made in Excel must not be lost.

**How to apply:** `runtime/qaos_export.py` writes the Excel; after the QA member edits it, run `runtime/qaos_import.py <xlsx> --run <run>` (dry run, show PROBLEM/CHECK/CHANGED), then `--apply --approved-by` after they confirm; the recorder runs the applied `step_draft_<TC>.json`. Use a new file version name per export (the file may be open in Excel). See [[use-agents-and-skills]], [[snd-test-automation-project]].
