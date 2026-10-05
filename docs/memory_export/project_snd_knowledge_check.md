---
name: project-snd-knowledge-check
description: "After the group 11 positive cycle is completed up to seq 71, a Senior QA will test Claude's S&D business knowledge with test cases (predict expected output, execute, compare)."
metadata:
  node_type: memory
  type: project
  originSessionId: a4c8fc60-aee7-4615-b524-027e4cc3842f
  modified: 2026-10-01T13:38:11.607Z
---

Planned activity (QA lead, 2026-10-01): once the full positive Daily Cycle (group 11) has been walked through its last active flow, seq 71 "Transaction Inquiry Validate After Sales Return" (03770001), a **Senior QA user** will run a knowledge check. They give Claude test cases on the S&D application; Claude states the expected output, executes them, and the result is compared with Claude's expectation.

**Why:** it validates that the learning phase (docs/LEARNING_STANDARD.md) produced usable business knowledge before QA OS writes cases and steps from user stories. It works as the human part of gate G0.

**How to apply:** before that session, finish the Consolidate phase so the answers come from the knowledge pages (`qa-os/apps/snd/knowledge/business/`), not from memory of one walk. For each case, write the predicted result first (status, messages, stock and amount effects, with confidence tags), then execute, then record matches and misses in a knowledge-check report that feeds back into the pages. Related: [[project-learn-g11-session1]], [[feedback-group-flow-execution-rules]].
