---
description: Run the full QA OS life cycle for a Jira story - analyse, test cases, test steps and the team Excel (gates G2/G3), data, live recording, Regress Master scripts and verification
argument-hint: <JIRA-KEY> [--app snd] [--env cnr2dev3] [--story <export file>]
---

Use the `qa-orchestrator` skill and follow its procedure for `$ARGUMENTS`.
- Stop at checkpoint 1 to show the ambiguities, unless the user said to accept the defaults.
- Finish with the workbook path, the readiness counts, and the command to live-run the `ready` cases
  (the user runs it; Claude never enters passwords).
