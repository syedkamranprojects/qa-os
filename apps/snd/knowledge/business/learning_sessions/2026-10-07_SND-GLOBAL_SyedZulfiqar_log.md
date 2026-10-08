# Training session log - S&D Promotions and Budgets

- Date: 2026-10-07
- Trainer: Syed Zulfiqar (taken from the account; trainer to confirm)
- App: snd (DCODE)
- Market: GLOBAL (module is not market-specific; F1, F5)
- Environment: none used so far (R2 = cnr2dev3 if screens are viewed live)
- Methods: A. document, B. verbal explanation in chat
- Users: none (no live walk)
- Area: promotions + promotion budget (new area; no business page yet). Known before the session: 5 mapped screens in `apps/snd/knowledge/screens_observed/` (DT_PROMOTION = Current Promotion, CURRENT_PROMOTION_APPROVER, ACTIVE_PROMOTIONS, BULK_PROMO_ALLOCATION, CASH_MEMO_PROMOTION_VIEWER); Total Offering lines (BONUS2 / TRADEOFFER) on orders; slab promotions re-priced on edit / part return (Q-SR2 open).

## Sources
- `Promotions and Budgets 2026_R2.pptx` (trainer's Desktop; 51 slides, "Promotion Master - User Manual", updated July 2026, market Pakistan, R2). Text and notes read in full 2026-10-07; screenshots not yet viewed. To be filed as `apps/snd/knowledge/sources/20261007_Promotions and Budgets 2026_R2.pptx`.

## Verbal facts

| # | Fact | Tag | Affects |
|---|---|---|---|
| F1 | The Promotion module is a generalised system feature, not tied to any market; markets use it according to their needs. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, glossary |
| F2 | The promotion screens exist in every region; functionality grows with the region number. R1 = cnr1dev1, R2 = cnr2dev3. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, app.yaml note |
| F3 | Promotions can be associated with a budget; Promotion and Budget are taught as one area. | [stated 2026-10-07 Syed Zulfiqar] | promotions page |
| F4 | The deck's "Market: Pakistan" means its examples and restrictions (Entity Type = Outlet only, Promo Sub Type = normal only) are Pakistan's configuration; each market uses only the promotions defined for it. | [stated 2026-10-07 Syed Zulfiqar] | promotions page (PK configuration section) |
| F6 | **Promotion Layout** (Company Setup > Promotion > Promotion Layout) is where a new promotion is created in DCODE. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, screen map |
| F7 | **Current Promotion** (route /dtPromotion/dt-promotion-list) is an inquiry of active promotions with the amount / quantity allocated and utilised. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, screen map |
| F8 | **Current Promotion Approver** is where promotions from the third party (PRAT) land or are uploaded and are approved; after an integrator job the approved promotions become part of the DCODE system. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, screen map, lifecycle |
| F9 | There are two ways to create a promotion: (1) **manually** in Promotion Layout; (2) **from outside**: Excel upload or API integration (PRAT) into Current Promotion Approver, approved there, then the integrator job brings it into DCODE. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, lifecycle |
| F10 | Refines F9: of the outside routes, **only the Excel upload waits for approval** in Current Promotion Approver; the API integration route does not wait for approval. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, lifecycle |
| F11 | **Active Promotions** (Company Setup > Promotion > Active Promotions) lists only the active promotions. **Current Promotion** is the screen used in practice, because it also shows the budget quota allocated / utilised. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, screen map, test design hint |
| F12 | A **manual** promotion (Promotion Layout) needs **no approval**: Save, then Apply. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, lifecycle |
| F13 | **API-route** promotions (e.g. PRAT) become part of DCODE directly (no approval step on Current Promotion Approver). | [stated 2026-10-07 Syed Zulfiqar] | promotions page, lifecycle |
| F14 | Excel-upload promotions on Current Promotion Approver can be approved by **any user who has the approval role** (no fixed user). | [stated 2026-10-07 Syed Zulfiqar] | promotions page, roles |
| F15 | The **integrator job** that brings approved promotions into DCODE is **normally scheduled** (not started by hand). | [stated 2026-10-07 Syed Zulfiqar] | promotions page, lifecycle, test design hint (wait for the job on a test env) |
| F16 | For a **fixed-value or percentage** promotion, the budget's **Utilized goes up at order save**. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, budget section, order_booking.md |
| F17 | For a **free-goods** promotion, the **stock availability of the free SKU** is checked; the promotion is **not applied unless the order is in Confirmed state**. (Scope of "Confirmed" rule - free goods only or all promotions - asked, see Open.) | [stated 2026-10-07 Syed Zulfiqar] | promotions page, order_booking.md, stock_allocation.md |
| F18 | Answer to the F17 scope question: "the stock check rule applies to stock" - read as: the stock check and the Confirmed-state condition apply only to stock-based (free-goods) promotions; fixed / percentage promotions apply at order save without it. (Reading restated to the trainer for confirmation.) | [stated 2026-10-07 Syed Zulfiqar] | promotions page |
| F19 | Free SKU out of stock: the **order is saved, but the free goods are not allocated**. (F18 reading not objected to; treated as confirmed.) | [stated 2026-10-07 Syed Zulfiqar] | promotions page, order_booking.md, stock_allocation.md |
| F20 | On a **return**, the promotion amount is **returned to the budget** (Utilized goes down). Cancellation: the deck (s.14) says cancelled orders free the quota; asked whether "return" here also covers cancellation. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, sales_return.md, order_editing_cancellation.md |
| F21 | If the **remaining budget is not enough**, the promotion is **not applied at all** (no partial discount up to the balance). | [stated 2026-10-07 Syed Zulfiqar] | promotions page, test design (boundary: balance just below / equal to the discount) |
| F22 | Budget give-back on a return follows the **allocation** of the promotion: a **full return gives the budget back fully**; a **partial return gives back only the part attributable to the returned allocation** (may be partial). Related: Q-SR2 (slab re-pricing on part return) - the give-back should equal the promotion discount reversed by the return. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, sales_return.md, Q-SR2 |
| F23 | **Order cancellation** gives the promotion budget back (as does a partial return, F22). Confirms the deck s.14 (Target Discount: cancelled orders free the quota). | [stated 2026-10-07 Syed Zulfiqar] | promotions page, order_editing_cancellation.md |
| F5 | Versions may differ between R1 and R2: everything in R1 is ported to R2, but R2 features are not necessarily ported back to R1. So an R2 document (this deck) may describe features missing in R1; confirm on cnr1dev1 before asserting there. | [stated 2026-10-07 Syed Zulfiqar] | promotions page, INDEX, test design hints |

## Document digest
Recorded in the chat 2026-10-07 (sections: PRAT integration; Promotion Layout header / scheduler / exclusive / super exclusive / Save then Apply; Qualify, Criteria, Resultant with limits; worked examples; Total Offering; Budget Setup with validations; Off-invoice IO Listing / credit note / approval; Claims). To be consolidated into the page with tags `[stated 2026-10-07 doc:Promotions and Budgets 2026_R2.pptx s.<slide>]`.

## Shared output
- 2026-10-08: QA-team doc "S&D Promotions and Budget — What Claude Learned" (Claude Docs, https://claude.ai/code/artifact/34818731-c034-490e-9024-e028cb975628): F1-F23 + the deck digest, test cases, 7 open questions. Private until the trainer shares it.

## Open (asked, not yet answered)
- ~~Q3~~ answered by F6-F8, Active Promotions answered by F11.
- Manual approval answered by F12; API route answered by F13.
- Approver role answered by F14; integrator job by F15. Open detail (not asked yet): the job's schedule on cnr1dev1 / cnr2dev3.
- F17 scope: does "not applied unless Confirmed" apply to free goods only? If the free SKU has no stock, is the order still saved (without the free goods) or blocked?
- Answered by F19-F21; cancellation by F23. Still open: does an **order edit that lowers the discount** give budget back (default: yes, re-priced like a re-save)? Partial return answered by F22.
- Q4 Are Discount Limit and Discount Cap the same setting?
- Q5 Trainer name for the tags.
