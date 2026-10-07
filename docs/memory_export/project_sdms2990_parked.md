---
name: sdms2990-parked
description: "Ticket work parked until system training is finished (2026-10-07) — SDMS-2990 (PH) at G2, SDMS-12390 (BD CLP zero credit note) after analyse."
metadata:
  node_type: memory
  type: project
  originSessionId: 4f9d9dd7-3f94-4731-9b7f-74dae6208ab1
  modified: 2026-10-07T06:33:35.962Z
---

On 2026-10-07 the user tested Claude on two tickets and then parked ticket work:
- SDMS-2990 ([PH] Dispatch Advice NUP): run `qa-os/runs/SDMS-2990/20261007-1037/`, stopped at gate G2 (10 core + 19 backlog cases).
- SDMS-12390 (BD bug, zero credit note against CLP incentive 0000000495): run `qa-os/runs/SDMS-12390/20261007-1121/`, analyse done, stopped at G1 (7 ambiguities, unlearned incentive chain).

**Why:** user judged that Claude is not yet well trained on S&D business flows/domain (the blockers and gaps showed it). Order: finish the R1 (Pakistan + Bangladesh, see [[snd-regions]]) system training first, then other markets.
**How to apply:** don't start or continue ticket runs until the user says training is complete; resume these runs from their gates when asked. Training gaps exposed: incentives/CLP -> credit note chain, promotions setup, Dispatch Advice NUP. Related: [[project_g11_session3_done]].
