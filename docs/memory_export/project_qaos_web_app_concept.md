---
name: project_qaos_web_app_concept
description: "Parked idea (2026-10-07) - QA web app (Jira dashboard, AI cases/steps, gated AI execution, download scripts) on top of qa-os; start only after training + one final output with QA team."
metadata:
  node_type: memory
  type: project
  originSessionId: df650cc1-356d-474d-adf7-8eb3b17aca31
  modified: 2026-10-07T04:45:23.926Z
---

User wants a web app for QA users on top of qa-os: SSO login, Jira assigned/pending tickets, AI-generated cases and steps with
review/approve, a one-time AI execution run (Selenium MCP) with status notifications, then download of the final scripts + test data.
Agreed concept saved in `qa-os/docs/WEB_APP_CONCEPT.md` (thin web shell over the existing pipeline stages/gates via the Claude Agent SDK,
execution runner inside the client network, service-account logins by the deterministic runner, "Needs input" pause status, MVP 1-3).

**Why:** turn the QA OS pipeline into a product the whole QA team uses without Claude Code.
**How to apply:** do NOT start development until S&D training is done AND the QA team has produced one final output end to end
(ideally validated in the legacy engine). When the user resumes it, read WEB_APP_CONCEPT.md and write the full design doc next.
Related: [[project_snd_test_automation]], [[feedback_qaos_shareable]].
