---
name: project-g11-session3-done
description: G11 PK session 3 (2026-10-06) full seq 1-71 walked with QA Team Lead; settlement unblock rule for Reattempt orders; Q-DS2/Q-CS1 answered; merge into pages started
metadata:
  node_type: memory
  type: project
  originSessionId: b5778f77-fda9-45aa-a9b0-f6d24e0e917f
  modified: 2026-10-06T11:35:22.582Z
---

2026-10-06: framework group 11 (Daily Cycle, PK, cnr1dev1) walked seq 1-71 in one day with the QA Team Lead. Log: qa-os/runs/LEARN-G11-PK/20261006/session_log.md (copied to learning_sessions/2026-10-06_G11-PK_session3_log.md by the merge agent).

Rules stated by the QA Team Lead that day:
- Order Editing lists only unallocated orders with delivery date today (Delivery Date Change first, then unallocate).
- Route Settlement fails with "Un-Deliver Order exists for today delivery!" while a Reattempt order is due today. Fix: allocate it (Order Stock Allocation, Order Date = its booking date), make a new GIN, have the Checker approve it, and mark it Delivered in Cashmemo Status. It may stay unpaid.
- Step 55 Cheque Status is a check only; never press Bounce. Step 56 DSR Adjustment: enter the workbook's 400.
- Q-DS2: duplicate cheque numbers are allowed because no cheque inventory is kept.

Claude did the settlement itself: Edit, then cash Received (editable), then row Save, which gave "Saved Successfully" and the row turned green.

**Why:** the next runs (and the QA environment) must handle these without asking again.
**How to apply:** before step 51, check Route Settlement for orders due today that are undelivered. COL26000002018 (Reattempt, due 2026-10-07) will block the next day's settlement unless it gets the same treatment.

Answered by the QA lead later the same day:
- **Q-DS4:** the doubled Outstanding Outlet totals are a display defect.
- **Q-DJ1:** a DSR adjustment is a DSR shortage that arises while taking money from the outlet.
- **Q-TI1:** Ordered is the outlet's original order quantity; Allocated is what the available stock allowed.
- **Q-OB2:** Opening must carry over the previous day's closing. Opening 0 means the stock job did not run in the environment.
- **Q-TX1:** the tax change came from master data. A zero-tax invoice of a non-exempt outlet can't be delivered.

- **Q-DS5:** the Outstanding Outlet tab adjusts an outlet's payment FIFO, oldest invoice first. The Outstanding Cash memos tab collects per invoice.

- **Q-RS1:** the day close clears Route Settlement's previous-day check, which runs per PJP. A yellow row means the route is not closed; green means closed.

- **Q-DS2:** deposit slips are not blocked against each other before settlement. Route Settlement's Save reconciles, posts the slips and adjusts the invoices; paid invoices then drop off the collection screens.

All of these are merged into the pages; 47 questions are open overall. No question from that day is left open. Q-RS4 (zero-activity routes) stays open until the user decides.

Next steps: G0 sign-off, Senior QA check, QA environment prep.

Related: [[project-g11-session3-plan]], [[reference-snd-day-close]]
