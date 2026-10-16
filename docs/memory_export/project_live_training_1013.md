---
name: project-live-training-1013
description: 2026-10-13/14 live training with the QA team on group 66 open points - COMPLETE; roles/workflow rule, Q-PO1/PJ6/7/8/DM1/DM2 answered; delivery days not in R1
metadata:
  type: project
---

On 2026-10-13 the QA lead held a live training session with QA team members Feroz Hussain and Muhammad Fahad (PK, cnr1dev1). It covered the open and parked group 66 Setup points.
- **Answered and proven live:**
  - Q-PJ8: approval follows the creating user's level. A DT user's record needs TSSM approval; an HQ user's doesn't.
  - Q-PJ7: GPS/DDO are changed via PJP Change Request, and the TSSM approves on the same screen.
  - Q-PJ6: PJP Daily Inquiry Process creates the daily route plus the outlets due that day; the result shows after a full reload.
  - #5: code numbering is a technical DB setup, not QA.
- **New rules:**
  - one DSR per PJP;
  - a DSR must be mapped on Distributor Mapping before it appears on PJP Creation;
  - DSR Forward needs a Residence address and a CNIC;
  - Prospect Outlet Forward needs the user's right and a Company address.
- **Defects:** D-TRAIN-1013-1 (Prospect Outlet Approval error, known, reported to dev) and D-TRAIN-1013-2 (Change Track Outlet Profile lists In-Active outlets, QA to confirm).

**Why:** this closes most of the parked group 66 questions.

**How to apply:** resume on 2026-10-14 at 10:30 with the same trainers, using `qa-os/docs/STATUS.md` (latest section) and `runs/TRAIN-SND-PK/20261013-QA-Team/session_log.md`. Open items:
- #1 Q-PO1: what enabled Forward on the team's C0154187445;
- #6: confirm D-TRAIN-1013-2;
- #7 Delivery Man Shuffling (Q-DM1/Q-DM2);
- #8 Section Profile delivery days;
- #9 D-G66-2-1 fix date;
- the step 35 framework decision.

Logins: Claude types the user ID, the user types the password ([[feedback-login-timer]]). Related: [[feedback-parked-questions]], [[project-learn-g66-setup]].


**Completed 2026-10-14:**
- R1 roles: 0001/0005 DT submit, 0002/0008 approval, 0014 HQ (no approval).
- Rule: a user can act on a document only if his role is in that document's workflow diagram. Check this first when Forward or Approve is disabled.
- Change Track Outlet Profile lists Draft outlets by design.
- Delivery Man Shuffling is correct apart from the known on-load 'PJP not found' message.
- D-G66-2-1 is fixed.
- The section delivery-days field is not in R1; skip it in scenarios.
- Group 66 step 35 runs as headquarter.
- Open questions: 56; open defect D-TRAIN-1013-1.
