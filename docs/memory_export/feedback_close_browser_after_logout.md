---
name: feedback-close-browser-after-logout
description: Always close the Selenium browser session right after a GIAS logout completes
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 59391d59-0278-4867-8d1f-30dffb278d43
  modified: 2026-08-10T10:11:55.929Z
---

Always call `mcp__selenium__close_session` immediately after a GIAS logout finishes (both confirm/alert dialogs accepted and the login screen is confirmed) - don't leave the session open waiting for further instructions.

**Why:** User explicitly asked for this as a standing rule during live Selenium testing of GIAS ([[project-gias-element-cache]]), not a one-off for that session.

**How to apply:** In any test-orchestrator flow that ends in a logout step, treat "close the browser" as an implicit last step of the logout action itself, not something to wait for the user to request separately.
