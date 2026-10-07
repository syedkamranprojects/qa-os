---
name: reference-snd-day-close
description: How a working day is closed in S&D cnr1dev1 (PJP Daily Inquiry Update End Of Day) and what Route Settlement / posting look like after it (2026-10-05)
metadata:
  node_type: memory
  type: reference
  originSessionId: b5778f77-fda9-45aa-a9b0-f6d24e0e917f
  modified: 2026-10-05T09:17:13.098Z
---

S&D / DCODE, cnr1dev1, distributor 15108843, delivery PJP 02112 (DSR ITB0189). Learned 2026-10-05 (session log qa-os/runs/LEARN-G11-PK/20261005-RS/session_log.md).

- **Day close = PJP Daily Inquiry Update** (menu DYL_BG1022, group 11 seq 57): Working Date = the day, row 02112 -> Edit -> Mark Status **End Of Day** (only option), DSR Files Status **Complete** (options Process/Complete), End Date may stay empty -> Save -> "Record Updated Successfully" -> Current Status **E**. A QA team member closed 2026-10-01 exactly this way.
- Route Settlement's "Following previous days not closed! Please close date. <date>" means an earlier day of the route is not closed this way. The QA lead said earlier days had been left un-closed and a QA team member closed them; the QA lead promised more detail - update this note when it arrives.
- Route Settlement Route Status filter: All / Complete / Incomplete; a settled route = green row, no Edit link. Settlement posts the day's deposit slips (Un Posted -> Posted, unallocated remainder trimmed), sets cheques to "Clear", and fills Transaction Inquiry Offset Amount.
- Cheque Status screen has only a Bounce action (no "Realized"); QA lead bypasses seq 55 and seq 56 (DSR Adjustment).

Related: [[project-learn-g11-session2]], [[feedback-group-flow-execution-rules]], [[feedback-always-enter-comments]]
