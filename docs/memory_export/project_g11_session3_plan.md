---
name: project-g11-session3-plan
description: Next step after 2026-10-05 - full group 11 PK run (seq 1-71) on this machine WITH the QA Team Lead to close gaps, then prepare QA OS for the QA environment
metadata:
  type: project
---

Decided 2026-10-05 by the QA lead (user): the next learning session repeats group 11 PK end to end, in one calendar day, on the CURRENT machine (cnr1dev1), with the QA Team Lead present to answer gaps/questions at each step. Afterwards: consolidate, G0 sign-off, Senior QA knowledge check, then prepare QA OS for the QA environment.

**Why:** settlement & finance area was not G0-ready (settlement done by a QA member, seq 55/56 bypassed, day-close procedure pending); seq 15 never walked.

**How to apply:** use the run sheet qa-os/apps/snd/knowledge/business/learning_sessions/G11-PK_session3_plan_with_QA_lead.md (pre-checks P1-P6, questions per seq). Before starting, confirm the session is NOT in auto mode and settings.local.json allows mcp__selenium (Claude may not edit its own permission settings; the user does it). Do the settlement (seq 51) and day close (seq 57) ourselves this time.

Related: [[reference-snd-day-close]], [[project-learn-g11-session2]], [[feedback-group-flow-execution-rules]]
