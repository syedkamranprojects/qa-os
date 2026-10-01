---
description: Run the QA OS life cycle for a Jira story (currently stages analyse → cases → steps)
argument-hint: <JIRA-KEY> [--app snd] [--env cnr2dev3] [--story <export file>]
---

Use the `qa-orchestrator` skill and follow its procedure for `$ARGUMENTS`.
- Stop at checkpoint 1 to show the ambiguities, unless the user said to accept the defaults.
- Finish with the workbook path, the readiness counts, and the command to live-run the `ready` cases
  (the user runs it; Claude never enters passwords).
