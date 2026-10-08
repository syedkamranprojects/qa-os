# Promotions & Budget: questions for the trainer (pending)

Saved 2026-10-08 at the QA lead's request (email drafted, not yet answered). Source of the questions: training 2026-10-07 + code study MS_Promotion UL-R1-BD@51e7e815. Ask them **when a run or request touches the promotion area** (operating rule "Promotion area: ask when needed"); record each answer as [stated <date> <name>] in promotions_and_budget.md and close the question in OPEN_QUESTIONS.md. <!--i-->

| # | Question | Ids |
|---|---|---|
| 1 | Super Exclusive in R1 only runs first, it does not block other promotions (filter commented out). Expected on cnr1dev1? | Q-PR13, contradiction 39 |
| 2 | Include + Include with OR: once either selection qualifies, is the discount on everything bought from both selections? | Q-PR14, contradiction 35 |
| 3 | Free goods "only when Confirmed" and the free-SKU stock check are not in the promotion service: done in the S&D order screens? What does "Confirmed" mean there? | Q-PR9, Q-PR11, contradiction 37 |
| 4 | Partial return: is only the returned part given back, or is the rest of the order re-priced too (as in the sales return walk)? | Q-PR10, contradictions 33, 38 |
| 5 | "Save then Apply" and an "allocated" promotion state are not in the R1 service: where does Apply happen? | Q-PR15, contradiction 40 |
| 6 | Repeat Limit is not in the R1 code: R2 only, or another name? | Q-PR17, contradiction 41 |
| 7 | Excel upload approval and the integrator job are not in the promotion service: which application / job, and its schedule on cnr1dev1? | Q-PR16, contradiction 42 |
| 8 | Short budget: PK = no partial discount (flag N). BD has no flag row: also "not applied at all"? | Q-PR12, contradiction 36 |
| 9 | Discount Limit = per order, Discount Cap = running total across orders: correct? | Q-PR2 |
| 10 | Does a free-goods promotion also use budget (quantity), or only stock? | Q-PR4 |
| 11 | What are Bulk Promo Allocation and Cash Memo Promotion Viewer used for? | Q-PR6 |
| 12 | Which test promotions and budgets for Pakistan can be used on cnr1dev1 (codes, outlets, SKUs)? | Q-PR7 |
| 13 | Please share the manual "Promotions and Budgets 2026_R2.pptx" (file under apps/snd/knowledge/sources/) | source gap |
| 14 | Confirm the trainer name for the tags | Q-PR8 |

Likely defects to check on a live walk: Save As New of a Super Exclusive promotion loses its run-first order; end date stored as midnight; preview discount dropped at save; budget reversal without a row lock (SDMS-10155). Details: promotions_and_budget.md §11. <!--i-->
