---
name: qaos-purpose-app-context
description: "Why the Daily Cycle Only Positive Flow is replayed - to learn the whole application's business into an app context that any agent can use; QA OS must work for any Centegy-architecture app."
metadata:
  node_type: memory
  type: project
  originSessionId: eb4a66f7-6654-4151-a641-fe8df7bda0d6
  modified: 2026-09-30T06:43:47.632Z
---

The user (2026-09-30) clarified that replaying the framework's "Daily Cycle Only Positive Flow" (group 11, Pakistan) is NOT only about passing it. Its purpose is for Claude to learn the business flow of the whole S&D application, which is the same business for all Centegy clients (steps vary a little per client/market). The result must be an **application context** holding everything needed to run the business, plus a standardized way to generate test cases and test steps so Claude can run them easily.

The user also wants to know how well Claude understands the selenium-framework DB: how a flow moves through the tables (one test flow can have many screens), and how, while executing a flow, Claude identifies, remembers and refers to it when creating steps. Claude OS is being designed for any app on Centegy's architecture, not just S&D.

**Why:** a flow-by-flow replay with notes did not scale, and the cycle needs a complete map before any story can be turned into steps.
**How to apply:** build and use `qa-os/apps/snd/knowledge/framework_atlas/` (raw dumps, `atlas.json`, per-flow read-outs, `group_<id>.md`, `INDEX.json`, `apps/snd/tools/build_atlas.py`). Tag every executed step with a trace key group:seq:flow:screen:event. Keep the design app-agnostic (app packs hold the app-specific parts). Note the cycle must run within one calendar day: on 2026-09-30 a GIN approval failed with "No stock balance found for products" because stock and orders were created on 09-29. See [[snd-test-automation-project]], [[use-agents-and-skills]].
