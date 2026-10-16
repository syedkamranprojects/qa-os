---
name: project-qaos-design-v4
description: QA OS design v4 agreed step-by-step with Syed Kamran on 2026-10-15 (qa-os/docs/DESIGN_V4_DECISIONS.md) - AI runs one case per path, screen files made in training, one login per role, Regress Master replays data rows
metadata:
  type: project
---

On 2026-10-15 the QA lead reviewed the design after the slow SDMS-6084 run: about 55 minutes of agent time, 9 logins, and AI executing all 19 cases. Every decision is logged in `qa-os/docs/DESIGN_V4_DECISIONS.md` (steps 0-17).

**Key points:**
- **Knowledge:**
  - QA members may change business knowledge directly.
  - The QA OS design may not be changed in the QA installation: stop the person and refer them to the administrator, Syed Kamran.
  - Screen-level lessons are saved automatically; business rules need confirmation.
- **Screen file per screen:** made during training (from the DB, a user guide or verbally, plus reading the screen). A screen without one is a long gap. The live screen wins over the configuration.
- **Cases:**
  - No cap on cases; backlog cases are one-line ideas.
  - Missing data is checked at design time.
- **Paths:**
  - AI runs one case per path; negatives are data rows.
  - If a path's AI run fails, the path is blocked.
- **Steps and approval:**
  - Steps are plain English, plus event columns (event, element id, data column).
  - For "load data", the AI decides the field mapping and the run captures it.
  - A step that doesn't match the screen file means the case needs knowledge.
  - One approval, by the QA member who runs the ticket.
- **Data:**
  - Missing records are created through the app, as steps in the plan.
  - Only shared master data is cleaned up.
  - Each case reads its starting state on screen first.
- **Execution:**
  - No runner program: the AI executes. Claude types the user ID, the QA member types the password.
  - One login per role; Maker work is batched first. One recorder per role session.
  - Any difference from the prediction: stop and ask. A defect stops only its own path.
  - Unknown negative messages are captured by one AI run each.
- **Output:**
  - Jira-ready defect drafts and an Excel + one-page summary.
  - Scripts are generated automatically after every passing path; the verifier runs before hand-over; the framework owner applies them.

**How to apply:** follow `DESIGN_V4_DECISIONS.md` for all new runs. It supersedes the older rules:
- "fresh login per test case": [[feedback-test-execution-from-login]];
- the cap of 10 core cases;
- G2/G3 as separate approvals;
- "scripts only on request": [[project-quick-mode-redesign]].

**Implemented 2026-10-15:**
- 77 screen files in `apps/snd/screens` (builder `build_screen_file.py`).
- `qaos_run.py check`, the approval workbook with `summary.md`, and import with diff.
- The design guard hook for qa installations.
- Skills and agents rewritten.

Framework owner: **Muhammad Imran**. Tuning items are in HARDENING A22. Next: SDMS-5997 as the first v4 run.
