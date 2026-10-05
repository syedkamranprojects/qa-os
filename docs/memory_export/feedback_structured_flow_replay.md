---
name: feedback-structured-flow-replay
description: "User wants GIAS navigation captured as structured, parameterized JSON (locators + actions + retry policy) so future runs call Selenium MCP directly without an LLM re-deriving anything"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 15874ffb-524e-452e-ab42-ab7c543b7919
  modified: 2026-08-19T06:11:10.207Z
---

The user explicitly directed (2026-08-19) that element-cache/menu-cache entries
are not the end goal by themselves - they want ordered, machine-executable
"flow" files: read the JSON once, then call the Selenium MCP tools purely from
its structured fields (`action`, `by`, `value`, `frame_path`, `timeout_ms`,
`retry_policy`), with no LLM reasoning needed to figure out sequence, wait
strategy, or error recovery at replay time.

**Why:** stated intent is phase 2 - generating real Selenium Java test code
from this seed data (per CLAUDE.md's "intended seed data for phase 2 code
generation"). An unstructured, prose-heavy cache (like the original
`shsm_mn_se_main.json` element list, or plain text notes in a "context" field)
still requires an LLM to interpret it correctly, which defeats that goal.

**How to apply:** whenever building or updating a GIAS element/menu cache file,
prefer the structured `flow` schema (see [[project_gias_menu_navigation]] for
the concrete design: steps with `action` type, absolute `frame_path`,
`timeout_ms`, `wait_after_ms` for animation-only delays, and `retry_group` +
top-level `retry_policy` for stateful UI like the flyout menu) over ad-hoc
prose fields. When something is discovered live that a naive locator+timeout
replay wouldn't handle (e.g. the flyout menu's stateful retry requirement),
encode the fix as a structured field in the JSON, not as an explanatory
sentence - the test is always "could a dumb player execute this without
asking an LLM what it means."
