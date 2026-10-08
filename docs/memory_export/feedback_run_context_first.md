---
name: feedback-run-context-first
description: Before any QA OS flow run, ask/confirm market, env, who is running, Maker/Checker users etc.; all of it goes into the generated SQL header.
metadata:
  type: feedback
---
Before running a QA OS flow (/qa-os:quick or any recording/script generation), first ask the QA member to confirm the run context: market, environment, who is running it, Maker (and Checker) user, and anything else the request leaves open. Never assume defaults silently.

**Why:** QA lead, 2026-10-08: "Before running flow of qa-os, you need to ask/clarify these questions of market, env, user who is running and whatever required; all these information would become the part of sql script."

**How to apply:** quick-script Q0 step 1 (one AskUserQuestion, options from app.yaml) -> `qaos_run.py init ... --market --run-by --maker [--checker] [--allow]` (validated against app.yaml, stored in run.json `context`) -> `qaos_record_multi.py --run <run>` -> printed in framework.sql / rollback header. Related: [[feedback-post-training-workflow]], [[feedback-qa-env-strict-mode]].
