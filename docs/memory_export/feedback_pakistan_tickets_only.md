---
name: feedback-pakistan-tickets-only
description: QA OS ticket runs are for Pakistan only for now (Region 1, PK); BD CRs / BD-only tickets are aborted - check the ticket's market before starting.
metadata:
  type: feedback
---
Only Pakistan work for now: "we are in Region 1 but working on Pakistan" (QA lead, 2026-10-09). Before starting /qa-os:run on a ticket, check its title/region/screens; a Bangladesh CR (e.g. "BD_CR", PJP Creation BG, BD data) is not run - tell the user and ask for a Pakistan ticket.

**Why:** SDMS-4912 (BD_CR Fortnightly PJP, region PKBD - R1) was analysed and then aborted by the QA lead; Fortnightly was not set up for PK. The QA team will share a Pakistan ticket.

**How to apply:** at Stage 0, flag tickets whose title or screens are BD-specific before analysis. Supersedes the "BD tickets are in scope with PK training" note in [[reference-snd-regions]] for current work.
