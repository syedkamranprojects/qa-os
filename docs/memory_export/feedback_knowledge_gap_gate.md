---
name: feedback-knowledge-gap-gate
description: "Before any AI execution or script generation, check knowledge; short/ad-hoc gap -> ask user, record, continue; long-term gap -> ask for training, do NOT execute the story/flow"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b5778f77-fda9-45aa-a9b0-f6d24e0e917f
  modified: 2026-10-08T07:43:26.534Z
---

The QA lead's rule, stated 2026-10-08: whenever Claude is about to execute the AI flow or generate scripts and needs more knowledge, it must ask the user to provide training or details. There are two kinds:
- **Short / quick / ad-hoc**: a value, a data choice, a field meaning, an expected message, one rule. Ask, record the answer as [stated] in the run's decisions.json (and in the business page if it is reusable), then **run**.
- **Long-term**: an untrained screen, module or business process, or a new market setup. Ask for a training session (`/qa-os:train`). **Do not execute the story or flow**, and do not generate scripts, until it is trained.

**Strict, test data included (2026-10-08).** Writing test cases, steps and test data uses training only, mainly the per-market catalog `qa-os/apps/snd/knowledge/business/test_data/<market>.md`. The app is opened only to execute the approved steps. Live state, such as stock, is checked by precondition steps during execution. The user wants a good design and says we are still evolving.

**Why:** guessing or improvising produces wrong scripts. Short gaps shouldn't block work, but real knowledge gaps need proper training.

**How to apply:**
- Apply the gate at analysis, before recording, and before generation. It's written into the quick-script and qa-orchestrator skills, knowledge-intake method C2, OPERATING_RULES and HARDENING B9.
- Never fill a gap by guessing or from old framework flows or workbooks.

Related: [[feedback-post-training-workflow]], [[feedback-qa-env-strict-mode]]
