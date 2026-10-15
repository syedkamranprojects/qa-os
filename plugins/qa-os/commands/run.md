---
description: Run the full QA OS life cycle for a Jira story - analyse, test cases + paths + plain-English steps in one approval workbook, AI run of one case per path (one login per role), Regress Master scripts per passing path and verification
argument-hint: <JIRA-KEY> [--app snd] [--env cnr2dev3] [--story <export file>]
---

Use the `qa-orchestrator` skill and follow its procedure for `$ARGUMENTS`.
- First ask the run context (market, env, run by, Maker, Checker, distributor) - every time.
- No separate stop after analysis: questions + defaults go into the single approval workbook with the cases, paths and steps.
- After approval, run the AI case of each ready path (Claude types the user ID, the QA member the password), then scripts for each passing path for the framework owner (Muhammad Imran).
- Finish with the workbook path, `summary.md`, pass/fail per path, defect drafts and parked questions.
