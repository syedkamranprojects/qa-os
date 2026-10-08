---
name: feedback-qa-env-strict-mode
description: "In the QA environment QA OS must run strictly to design — no live redesign or tool changes, no hand edits, fast; all issues must be fixed and proven before release (docs/HARDENING.md)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b5778f77-fda9-45aa-a9b0-f6d24e0e917f
  modified: 2026-10-08T07:14:11.771Z
---

The QA lead said on 2026-10-08, after watching me patch the watcher, converter and rules in the middle of the Order Booking quick run: when the QA team runs QA OS in the QA environment, Claude will not change the framework design or the tools and will not take this long. Execution must be strict to the designed flow. So, before releasing to QA, every issue has to be identified and rectified.

**Why:** QA members need a predictable, fast product. Mid-run redesign is development work, and doing it during a run hides how unfinished the platform is.

**How to apply:**
- In a QA-environment run, follow the phases exactly. Change no tools, skills, design or recordings, and make no hand edits. On a failure, STOP and report the step, message and evidence.
- Development fixes go into `qa-os/docs/HARDENING.md`, the issue register: sections A recording, B steps/data/process, C generation, D release gate.
- The release gate:
  - every item is fixed or accepted;
  - a clean acceptance run, with no changes or edits, in about 30 minutes;
  - the verifier says ready;
  - one engine replay on a test copy.
- The strict-mode text is in `docs/OPERATING_RULES.md` and the quick-script skill.

Related: [[feedback-post-training-workflow]], [[project-qaos-quick-mode]]
