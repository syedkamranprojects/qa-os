---
name: feedback-parked-questions
description: Knowledge gaps and QA questions that don't block current work are parked (not sent); raise them with QA only when a ticket touches that area, during its run
metadata:
  type: feedback
---

On 2026-10-12, after the QA team answered the group 66 Setup review, the QA lead said to note the remaining gaps and questions, not send them. If a new ticket touches an area where we are short, the question is raised during that ticket's test-case execution.

Parked list: `qa-os/apps/snd/knowledge/business/learning_sessions/2026-10-12_G66-PK_parked_questions.md`. The items are marked "deferred: raise when a ticket touches this area" in OPEN_QUESTIONS.md. They are Q-PO1, Q-PJ6, Q-PJ7, Q-PJ8, Q-DM1, Q-DM2, D-G66-2-1, C-49 and C-45.

**Why:** QA's time goes to questions that block real tickets; batches of follow-up questions pile up unanswered.
**How to apply:** at analysis (knowledge-gap gate), check whether the ticket's screens hit a parked item; if so, ask it as part of that run, then record the answer and remove it from the parked list. Don't send standalone follow-up batches. The trainer's promotions questions are handled the same way ([[project-promotions-partial-training]]). Related: [[feedback-knowledge-gap-gate]].
