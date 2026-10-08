# Area: promotions and budget (S&D / DCODE, GLOBAL module)

Updated: 2026-10-08 (first consolidation: training session 2026-10-07 with Syed Zulfiqar, verbal facts F1-F23, plus the digest of the user manual "Promotions and Budgets 2026_R2.pptx" as written up for the QA team on 2026-10-08). Evidence: [../learning_sessions/2026-10-07_SND-GLOBAL_SyedZulfiqar_log.md](../learning_sessions/2026-10-07_SND-GLOBAL_SyedZulfiqar_log.md), [../learning_sessions/2026-10-08_SND_Promotions_and_Budget_QA_Team.docx](../learning_sessions/2026-10-08_SND_Promotions_and_Budget_QA_Team.docx); report [../learning_sessions/2026-10-07_SND-GLOBAL_SyedZulfiqar_report.md](../learning_sessions/2026-10-07_SND-GLOBAL_SyedZulfiqar_report.md).

Status: DRAFT. **Nothing in this area has been observed live yet** (no walk on cnr1dev1 or cnr2dev3), so there are no [observed] tags; facts are [stated] (trainer or manual), [db] (menu harvest / L4 screen map of 2026-09-25) or [inferred]. This area is **not part of the group 11 Daily Cycle**; it is a GLOBAL module (every market uses it with its own configuration) [stated 2026-10-07 Syed Zulfiqar].

1. A promotion (scheme) gives a discount, a fixed amount or free goods when an order qualifies; promotions reach DCODE by three routes (manual in Promotion Layout, Excel upload approved on Current Promotion Approver, API e.g. PRAT) [stated 2026-10-07 Syed Zulfiqar].
2. A promotion can carry a budget; a fixed / percentage promotion consumes it at order save, cancellation and returns give it back, and an insufficient balance means the promotion is not applied at all [stated 2026-10-07 Syed Zulfiqar].
3. Budget use is read on **Current Promotion** (allocated / utilised); the order side is read on Transaction Inquiry > **Total Offering** (one line per promotion, sum = header Discount, already observed in the group 11 walks) [stated 2026-10-07 Syed Zulfiqar; observed 2026-10-01 G11-1 on the order side only].
4. The manual is an **R2** document; R1 (cnr1dev1) may lack features, so confirm each feature on cnr1dev1 before asserting it there [stated 2026-10-07 Syed Zulfiqar].

## Training status: PARTIAL - ask when needed (QA lead rule, 2026-10-08)
**Exception (2026-10-08): creating or editing promotions in Promotion Layout is NOT trained (long-term gap) - do not execute or generate scripts for it; ask for a training session.** Reading promotion screens and order-side effects may still use the ask-when-needed rule.
This area is trained incrementally: the QA lead will give more information on this module when it is needed. When a quick request, run or AI execution touches promotions or budgets:
- use what is here ([stated] facts first; [code] facts only as "to be confirmed");
- if the request needs something not covered, or one of the pending questions in [../learning_sessions/2026-10-08_Promotions_questions_for_trainer.md](../learning_sessions/2026-10-08_Promotions_questions_for_trainer.md) affects it, **ask the user at that moment** (knowledge-gap gate: a short answer -> record it as [stated] and continue; a whole untrained part, e.g. a promotion type or screen never explained -> ask for training first, no execution);
- never assert a promotion amount, budget effect or message that is only [code] or [inferred].

## Pages (one line each)
| Page | What it holds |
|---|---|
| [promotions_and_budget.md](promotions_and_budget.md) | All 13 sections: routes into DCODE, screens, Promotion Layout (header, scheduler, Exclusive / Super Exclusive, Qualify / Criteria / Resultant, limits), Budget Setup and its upload validations, order / budget effect table, off-invoice credit notes and claims, PK configuration, test design hints. |

## Related pages (cross-references added 2026-10-08)
- [../order_to_delivery_planning/order_booking.md](../order_to_delivery_planning/order_booking.md): budget taken at order save; free goods and stock; insufficient budget.
- [../order_to_delivery_planning/stock_allocation.md](../order_to_delivery_planning/stock_allocation.md): free SKU stock check.
- [../order_to_delivery_planning/order_editing_cancellation.md](../order_to_delivery_planning/order_editing_cancellation.md): cancellation gives the budget back.
- [../delivery_and_returns/sales_return.md](../delivery_and_returns/sales_return.md): returns give the budget back (full / partial; Q-SR2 middle invoice).
- [../order_to_delivery_planning/transaction_inquiry.md](../order_to_delivery_planning/transaction_inquiry.md): Total Offering per promotion.

## Open questions
Q-PR1 to Q-PR10 in [../OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md) (classes A / B / C as filed there); contradictions 33 and 34 in its section 5.
