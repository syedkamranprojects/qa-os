---
description: Show QA OS run status for a ticket or case, and the app-pack knowledge summary
argument-hint: [ticket key or case id]
---

1. List the newest runs under `qa-os/runs/` (all runs, or only `$ARGUMENTS` if given). For each run, show the
   case, mode, verdict, finish time and failed step, reading only each run's `result.json` / `run.json`.
2. Summarise each app pack briefly: screen count in `screens/` (observed) vs `knowledge/screens_db/` (DB-declared),
   and when the menu and i18n were last harvested (`knowledge/env/*/`).
