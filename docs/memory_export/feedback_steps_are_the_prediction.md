---
name: feedback-steps-are-the-prediction
description: "AI execution exists to confirm that knowledge-predicted cases/steps are correct; a live screen scan may check and bind steps but must never silently rewrite the prediction; scan in the same session, no headless"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b5778f77-fda9-45aa-a9b0-f6d24e0e917f
  modified: 2026-10-12T06:16:06.095Z
---

The QA lead (2026-10-12): Claude writes test cases and steps from its trained knowledge as a **prediction**, and the AI agent executes them to **confirm the generated steps are OK**. That confirmation is the point of the design.

A read-only screen scan before execution was agreed in principle. It runs in the same browser session right after the QA member's login; headless was rejected. The scan only does two things:
- It checks the predicted steps against the real screen: element exists, mandatory/read-only, missing sub-tab or option. Each conflict is reported as a finding against the prediction.
- It binds labels to ids.

It never replaces the knowledge-based steps without a trace. Keep both "predicted" and "corrected after scan/execution", so the accuracy of the training can be measured and the gaps go back into the knowledge.

**Why:** if steps were simply generated from the live screen, executing them would prove nothing about the training.
**How to apply:** design note + pilot on DSR Profile - DT; record each scan/execution correction as a knowledge finding (business page or open question). Related: [[feedback-post-training-workflow]], [[feedback-knowledge-gap-gate]].
