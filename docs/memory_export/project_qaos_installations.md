---
name: project-qaos-installations
description: QA OS knows if it is the dev working copy (qaos.dev.yaml, gitignored, never packaged) or the QA team's release (release.json); no restrictions yet; in qa, design gaps go to feedback/design_gaps.md
metadata:
  type: project
---

Built 2026-10-12 (plugin 0.5.7) at the QA lead's request, before the QA patch.
- `python runtime/qaos_config.py mode` prints DEV or QA.
- **Dev** = the file `qa-os/qaos.dev.yaml` (owner and design_contact: Syed Kamran). The file is gitignored and `tools/build_release.py` refuses to package it.
- **QA** = the release zip, which carries a `release.json` (version, build date, built_by, design_contact). No marker always means QA.
- Each run.json records `installation`, and the SQL header prints `-- QA OS: v<version> (<mode> installation)`.

The QA team receives the patch as a release zip, not via git. QA members **train the system freely**; nothing is restricted yet, because the QA lead is not sure which features to restrict.

In a qa installation, Claude does not change tools, skills, hooks, design docs or recordings. Design and tool gaps it notices are noted in `feedback/design_gaps.md`, and the QA member is told to check with Syed Kamran first.

**Why:** the QA lead wants the two installations clearly identified, with flags that allow restricting QA users later.
**How to apply:** check the mode at the start of any QA OS session. When restrictions are decided, enforce them through the mode: a hook plus a skill check. Related: [[feedback-qa-env-strict-mode]], [[feedback-qaos-shareable]].
