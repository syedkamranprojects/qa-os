---
name: feedback-always-enter-comments
description: In S&D maker-checker Forward popups always type the comment ("Automation Approval") and verify the textarea is filled before pressing Save; also do company+distributor selection after the user's credentials.
metadata:
  type: feedback
---

On every Forward/approve comment popup (GIN, Sales Return View, DA, GRN...) enter the comment "Automation Approval" and read back the textarea value before clicking Save. Typing can fail silently if the dialog is not ready (session 2, 2026-10-05, Sales Return View).

**Why:** QA lead corrected it mid-run ("Always enter the comments"); an empty comment is rejected or recorded blank.

**How to apply:** send_keys, then verify `textarea.value`, then a real click on Save. Also: after the QA lead types credentials, Claude selects company (Unilever Pakistan Limited) and distributor (15108843-IBRAHIM TRADERS) itself, and Claude logs out the current user itself ([[feedback-group-flow-execution-rules]]).
