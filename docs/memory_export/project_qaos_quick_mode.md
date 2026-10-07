---
name: project-qaos-quick-mode
description: "/qa-os:quick (skill quick-script) built 2026-10-07 — one-line request without a ticket -> one case, one approval, one recording -> case-data rows for an existing framework flow or new framework SQL; not yet tried live"
metadata:
  node_type: memory
  type: project
  originSessionId: b5778f77-fda9-45aa-a9b0-f6d24e0e917f
  modified: 2026-10-07T12:38:51.872Z
---

On 2026-10-07 the user asked that QA OS work from a one-liner with no Jira ticket, e.g. "create one order and order detail with two products script". It was built into release v0.5.0 (not yet tagged when written):
- command `plugins/qa-os/commands/quick.md`
- skill `plugins/qa-os/skills/quick-script/SKILL.md`, steps Q0–Q6

How it works:
1. Check the screens are learned.
2. Map the request to trained business pages (no framework flow is used to drive the run).
3. Run key QUICK-<date>-<time>, with a story block naming the market's Maker and menu options only.
4. One case, steps and data, approved once at gate QG.
5. Record once with the recorder.
6. Output (revised later on 2026-10-07): always new Regress Master SQL + rollback + case data, from the framework-generator, then checked by the verifier. The earlier "type A: reuse the existing flow, rows only" was dropped; see [[feedback-post-training-workflow]].

Bug fixed in `runtime/qaos_intake.py`: a user named in the QA-OS block who has no harvested menu data (Auto_* group users) is now kept with a warning. Before the fix it was replaced by KPO_mp.

**Why:** the user wants scripts for small scenarios without tickets; this is also the future entry point for bulk data ("×N outlets").

**How to apply:** the first live use is still pending. On the first live run, check the generated SQL and workbook with the verifier and the framework owner. Ask before running it during the training phase.

Related: [[project-bulk-data-factory-plan]], [[sdms2990-parked]]
