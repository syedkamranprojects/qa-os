---
description: Validate a QA OS flow (dry run) and tell the user how to run it live with the deterministic player
argument-hint: <path to flow.json>
---

Use the `step-dsl` skill.

1. Run `python runtime/qaos_player.py $ARGUMENTS --dry-run` from the `qa-os` folder and report the result.
2. If the dry run passes and the flow contains `login`, give the user the live command to run themselves
   (Claude must not enter passwords):
   `python runtime/qaos_player.py $ARGUMENTS`
3. When they say it has finished, read the newest `runs/<case>/<timestamp>/result.json` and summarise the verdict,
   any failed step, and the evidence files.
