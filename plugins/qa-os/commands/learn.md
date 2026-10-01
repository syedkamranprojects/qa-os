---
description: Build or refresh an app's knowledge (menu, screens, fields, labels) with app-cartographer
argument-hint: <app> [menu path or option id]
---

Delegate to the `app-cartographer` agent with this brief: app/target = `$ARGUMENTS`. Knowledge lives in
`qa-os/apps/<app>/`. Return what was added or changed, conflicts between the DB and the live env, and any
flow the user must run with the player.
