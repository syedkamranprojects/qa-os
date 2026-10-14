---
name: feedback-field-region-scope
description: When a framework workbook/flow expects a field the screen does not have, first ask whether the field is in scope for this region (R1) before treating it as missing or planned; section delivery days = not R1
metadata:
  type: feedback
---

The QA lead, on 2026-10-14, questioned why Claude kept asking about the section "Default Delivery Days" field. The field is **not part of the R1 region** (Pakistan / Bangladesh). The PK framework workbook (group 66 step 32) carries it as a stale value, apparently from another region's flow.

**Why:** the framework workbooks and flows mix in fields from other regions. Treating every missing field as a gap or a planned enhancement wastes the QA team's time.

**How to apply:**
- When a workbook or framework flow expects a field the live screen doesn't show, first check or ask: **"is this field in scope for R1?"**
- If the field is out of scope, record its region on the page and skip it in scenarios; don't raise it again.

Known out-of-scope for R1: section delivery days. Related: [[feedback-no-docs-learn-from-metadata]], [[reference-snd-regions]].
