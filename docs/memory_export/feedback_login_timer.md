---
name: feedback-login-timer
description: After asking the QA member to log in, start a ~20 s timer, then check the login page - credentials typed -> press Login and continue; already in -> continue; empty -> ask again and wait.
metadata:
  type: feedback
---
When prompting the QA member for a login (S&D / QA OS runs and walks), start a background timer (20 s, e.g. a background `sleep 20`) right after the prompt. When it fires, check the page: user id + password filled -> press Login (Claude still never types credentials) and continue; already logged in (company picker / home) -> continue; fields empty -> prompt the user again and wait for their message.

**Why:** QA lead, 2026-10-09: "When you prompt for login set a timer to click on login assuming user must have entered. If he has not, then you prompt user again to enter credentials and wait for user to inform you."

**How to apply:** every login hand-off (switch points in walks, quick runs). Related: [[feedback-always-enter-comments]] (login hand-off), [[feedback-minimise-user-intervention]].
QA lead 2026-10-09: 20 seconds is enough.

**Update 2026-10-09 (QA lead):** "Cant you just enter at least User ID, I will enter password myself" -> Claude types the **user ID** in the login page, the QA member types only the **password**; the 20 s timer presses Login once the password is filled. Claude never types or reads a password.
