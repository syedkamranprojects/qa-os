---
name: feedback-group-flow-execution-rules
description: "When replaying a framework group (e.g. SND group 11) via Selenium MCP, run only status-Y test flows, strictly in sequence order, with the Maker/Checker users from app.yaml."
metadata:
  node_type: memory
  type: feedback
  originSessionId: a4c8fc60-aee7-4615-b524-027e4cc3842f
  modified: 2026-10-01T10:44:44.300Z
---

When executing a framework group test flow (S&D group 11 "Daily Cycle Only Positive Flow" first; other positive/negative groups will follow), run ONLY the test flow ids whose `pgtfd_status = 'Y'` in `fct_pr_gtfd_group_test_flow_detail`, in `pgtfd_sequenceno` order. Never run status-N rows. Use the user named on the row (`plu_serial_no`) — a row with no user runs as the current session user; `pgtf_testflow_login_status = Y` means log out and log in as that user.

Roles: only Maker and Checker exist (no Stock Controller / Order User); each can have several users. Source of truth `qa-os/apps/snd/app.yaml` environments.cnr1dev1.roles (Maker = Auto_Multi_Orga default, Automation; Checker = Auto_Tssm; company Unilever Pakistan Limited, distributor 15108843 IBRAHIM TRADERS).

**These replays are LEARNING runs, not recordings:** capture domain and business flow (purpose of each screen, inputs, rules, validations, messages, statuses, stock/finance effects, dependencies between documents) so Claude can later write test cases and steps from user stories. Do NOT collect element ids/locators here — the recorder agent captures ids later, when it executes approved steps to generate legacy-framework scripts.

**Why:** the QA lead (2026-10-01) wants these replays so Claude learns the S&D domain and process flow end to end and builds the business knowledge; inactive rows are not part of the intended cycle.

**How to apply:** plan the run from the DB rows, group them into login segments, and keep the whole cycle inside one calendar day ([[project-qaos-purpose-app-context]]). Logins are still typed by the QA member, not Claude ([[feedback-qaos-shareable]]).
