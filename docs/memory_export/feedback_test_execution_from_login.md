---
name: feedback-test-execution-from-login
description: "Every test case execution must start fresh from login, not reuse an existing browser session"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b54266a3-dd90-41e2-a3e2-d9c864c34d01
  modified: 2026-09-23T07:47:02.312Z
---

Always execute a test case from the beginning, starting with login (and distributor selection if applicable), rather than continuing in an already-authenticated browser session left over from a previous test case.

**Why:** User explicitly corrected mid-task (during SKU Substitution Policy Test Case #2, DCODE app) when I continued reusing the session from Test Case #1 instead of restarting. Each test case should be treated as an independent, self-contained run matching how a manual tester would execute it from a test sheet — login is itself one of the documented test steps, not incidental setup to skip.

**How to apply:** Before executing any numbered test case (from an excel test sheet or otherwise), close any existing browser session (`mcp__selenium__close_session` or equivalent) and start a new one, then perform the full login flow (credentials + any post-login screens like distributor selection) as the first step(s) of the test, even if a session from a prior test case is still open and valid. Applies across tools (Selenium, vibium) and across DCODE apps (dcodecnr1dev1, dcodecnr2dev3, etc.), not just this one screen.
