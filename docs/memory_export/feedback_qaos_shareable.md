---
name: qaos-shareable
description: "QA OS must work unchanged in other QA members' Claude environments; avoid machine-specific paths and hidden local setup; SDMS-10351 is only the pilot, not the target."
metadata:
  node_type: memory
  type: feedback
  originSessionId: eb4a66f7-6654-4151-a641-fe8df7bda0d6
  modified: 2026-09-25T11:22:05.393Z
---

QA OS will be shared with several QA members, each using it in their own Claude environment (user, 2026-09-25). They questioned why execution
ran as Python commands that the user had to run, and why the work was so focused on the SKU Substitution Policy ticket.

**Why:** it is meant as a team "Claude OS for QA" across many stories and apps (S&D now, GIAS next), not a one-person, one-ticket setup.

**How to apply:**
- Treat SDMS-10351 purely as the pilot. Nothing in the agents, skills or player may be SKU-specific. Prove generality on other stories and screens.
- Avoid hard-coded absolute paths and local-only setup. Everything must install via the plugin plus a documented runtime dependency check.
- **Execution model (answered 2026-09-25):**
  - Claude never enters passwords, even via scripts it launches, so any run that includes login is triggered by the QA member (or CI / the legacy engine).
  - Keep that trigger a single, simple command.
  - The long-term execution path is the legacy Regress engine (Java) reading the generated framework-db scripts; the QA OS player is an interim authoring and verification runner.

**File-upload automation (user, 2026-09-25):** "skip test cases which have file upload... we can find an alternate solution", because it is difficult.
Those cases are marked `readiness: deferred` (22 of 53 for SDMS-10351: TC16-28, 29-35, 37, 40) and shown as Not Executed in the workbook. Don't run or count them until an
alternative is agreed. Not lost by that: rules R10 and R13, and effectively the R14 overlap rule, now have no automated case.
Alternatives to propose when revisiting: (A) keep as manual QA cases, (B) replay the upload's backend call over HTTP using the session token
(captured via the browser network log), (C) the player's upload step plus reading the error file the app downloads (implemented, never confirmed live).

Jira access to project SDMS is pending (the user will say when it's granted); until then, use story exports.
See [[snd-test-automation-project]].
