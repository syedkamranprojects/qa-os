---
name: minimise-user-intervention
description: QA OS flows must run with as little user intervention as possible; log every obstacle in a friction file and turn it into a platform fix.
metadata:
  node_type: memory
  type: feedback
  originSessionId: eb4a66f7-6654-4151-a641-fe8df7bda0d6
  modified: 2026-09-28T06:17:00.482Z
---

While running stories through the MCP, the user wants the flow to need **no user intervention beyond login**. Every time something blocks or slows the run (missing data, navigation trick failing, toast missed, UI race), record it in `runs/<key>/<ts>/friction.md` with the software fix, and prefer building that fix over asking the user.

**Why:** the goal of QA OS is a smooth, mostly unattended story-to-scripts flow that other QA members can use; user-answered questions and manual data hunts do not scale. The user said this explicitly on 2026-09-28 (Van Sales run).

**How to apply:** discover fixtures yourself through the app's read APIs before asking; run UI steps one at a time (never parallel); capture toasts with polling; keep known app rules and story variances in the app pack. Ask the user only for login, destructive/stock-changing actions, and BA-level decisions. See [[snd-test-automation-project]], [[qaos-shareable]].

**Addendum 2026-09-29:** for long framework replays the QA lead wants the test steps provided/approved by QA up front (a step sheet in the standard vocabulary, with hints where the app differs from the framework) so Claude does not have to discover screen behaviour by trial and error; Claude drafts the sheet from the framework tables and marks each step clear / needs input.

**Correction 2026-10-01 (important):** I ran the per-step "next step" dialogue (AskUserQuestion, 3-4 questions per case, plus approvals and re-approvals) for my own work on TC01/TC02 and the user was frustrated: it maximises intervention. The point of walking through the application's options is for CLAUDE to learn the business of the application, not to quiz the user. **Rules:** (1) For my own learning and for drafting, work alone: use the atlas, DB metadata and read-only live exploration, decide with sensible defaults and record each assumption; ask only for logins and for decisions that truly need a human (a business rule only a BA knows). (2) Never more than one batched question per session segment; prefer "Default if you skip". (3) The per-step dialogue is only for a QA member who chooses to author steps in chat; the default for QA members is: Claude drafts the whole sheet, the QA member edits the Excel once. (4) Do not ask for approval of things the user already told me to do (e.g. "execute once the Excel is final"). See [[qaos-purpose-app-context]].
