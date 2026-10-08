# Training report - S&D Promotions and Budget (GLOBAL), 2026-10-07

- Trainer: Syed Zulfiqar (taken from the account; confirmation pending, Q-PR8)
- Market: GLOBAL (module not market-specific; the manual's examples are Pakistan's configuration)
- Environment: none (no live walk). R1 = cnr1dev1, R2 = cnr2dev3.
- Consolidated: 2026-10-08 into `apps/snd/knowledge/business/` (this report, the log beside it, and the QA-team write-up `2026-10-08_SND_Promotions_and_Budget_QA_Team.docx`).

## 1. Methods used
- **B. Verbal explanation in chat**: facts F1-F23, tag `[stated 2026-10-07 Syed Zulfiqar]`.
- **A. Document**: the user manual "Promotions and Budgets 2026_R2.pptx" (51 slides, "Promotion Master - User Manual", July 2026, market Pakistan, R2), text and notes read 2026-10-07 in the main session; digest taken from the 2026-10-08 QA-team write-up. Tag `[stated 2026-10-07 doc:Promotions and Budgets 2026_R2.pptx s.<slides>]` with the write-up's ranges (6-31 Promotion Layout, 14 Target Discount, 34-41 Budget Setup, 42-50 off-invoice / claims); `s.?` where no slide was given (PRAT / mobile sync).
- **Source gap**: the pptx is **not in the workspace** (trainer's Desktop). It should be filed as `apps/snd/knowledge/sources/20261007_Promotions and Budgets 2026_R2.pptx` and listed in `sources/README.md` (not done here: outside `business/`). Screenshots of the deck were never viewed, so field mandatory markers and message texts are missing.
- Supporting evidence read (no live action): menu harvests of 2026-09-25 (`knowledge/env/cnr1dev1/menu.KPO_mp.json`, `knowledge/env/cnr2dev3/menu.KPO_slv.json`) and the L4 sweep labels in `knowledge/screens_observed/` (cnr2dev3), tagged `[db 2026-09-25 menu]` / `[db 2026-09-25 L4]`. No `[observed]` tag was added for promotion behaviour.

## 2. Facts added per page
| Page | Added |
|---|---|
| `promotions_and_budget/README.md` (new) | area summary, page list, related pages |
| `promotions_and_budget/promotions_and_budget.md` (new, 13 sections) | all 23 verbal facts (F1-F23); about 44 manual facts (routes, header fields, scheduler, Exclusive / Super Exclusive, Qualify table, Criteria, Resultant + 6 limits, worked examples, Budget Setup who / upload / template / new / edit / 2 default combinations, 8 upload validations, IO rules, off-invoice credit note rules, forward / approval, claims job and report, Pakistan configuration); 8 menu / L4 facts (screen paths, option ids, R1 vs R2 menu differences, mapped labels); route table, screen table, order / budget effect table, status table, 11 test cases + boundaries + traps; 10 open questions |
| `order_to_delivery_planning/order_booking.md` §8 | 3 lines: F16 (budget at save), F17-F19 (free goods / stock), F21 (not applied when the balance is short) |
| `order_to_delivery_planning/order_editing_cancellation.md` §8 | 1 line: F23 (cancellation gives budget back; manual s.14 agrees; edit open as Q-PR1) |
| `delivery_and_returns/sales_return.md` §8 | 1 line: F20, F22 (full / partial return give-back), link to Q-SR2 / contradiction 33 / Q-PR10 |
| `order_to_delivery_planning/stock_allocation.md` §8 | 1 line: F17, F19 (free SKU not allocated when out of stock) |
| `order_to_delivery_planning/transaction_inquiry.md` §8 | 1 line: Total Offering = order-side reading; budget read on Current Promotion |
| `INDEX.md` | new section "Outside the Daily Cycle: promotions and budget (GLOBAL module)" + one document-map row + Updated note |
| `glossary.md` | 14 terms: Promotion Layout, Current Promotion, Current Promotion Approver, Active Promotions, PRAT, Integrator job, Exclusive / Super Exclusive, Qualify / Criteria / Resultant, Discount Limit / Discount Cap, Target Discount, Budget Setup, IO number, Off-invoice credit note, R1 / R2 |
| `OPEN_QUESTIONS.md` | status line, Q-PR1..Q-PR10 in their class sections, contradictions 33-34, section 6 counts, legend |
| `LIVE_LEARNING_CHECKLIST.md` | new section with checks L46-L51 for the class B questions |
| `learning_sessions/README.md` | session row |

No existing statement was changed or deleted; the cross-references are new one-line bullets.

## 3. Questions opened (none answered)
| Id | Class | Question | Default |
|---|---|---|---|
| Q-PR1 | B | Does an order edit that lowers the discount give budget back? | yes, re-priced like a re-save |
| Q-PR2 | C (1b) | Are Discount Limit and Discount Cap the same setting? | no: per order vs per customer |
| Q-PR3 | B | Integrator job schedule on cnr1dev1 / cnr2dev3 | unknown; wait for the next run |
| Q-PR4 | C (1b) | Does a free-goods promotion also use (quantity) budget? | stock only unless a QTY budget exists |
| Q-PR5 | B | Which promotion features are missing in R1 vs R2? | missing until seen on cnr1dev1 |
| Q-PR6 | C (1b) | Purpose of Bulk Promo Allocation and Cash Memo Promotion Viewer | out of scope until taught |
| Q-PR7 | B | Which test promotions / budgets exist on cnr1dev1 (PK)? | read-only walk on the group 11 promotions |
| Q-PR8 | A | Trainer name for the tags | Syed Zulfiqar |
| Q-PR9 | B | What "Confirmed" means for free goods (orders are Confirmed at save when allocated) | Confirmed = allocated |
| Q-PR10 | B | Partial return: give-back = the return's Total Offering or only the returned share? | the return's Total Offering |

Q-PR1-Q-PR7 are the QA-team doc's 7 questions; Q-PR8 is from the log; Q-PR9 and Q-PR10 came up in this consolidation. Open questions: **34 -> 44 = A 16 + B 18 + C 10** (1a 7, 1b 3).

## 4. Contradictions and checks against existing pages
- **New contradiction 33 (OPEN, Q-PR10)**: F22 says a partial return gives back only the budget of the returned allocation; the Q-SR2 answer (2026-10-08) and the walks show that a partial return re-prices the remaining basket through a middle invoice, so lines with 0 returned quantity also carry discount reversals (returns 714 and 715). If the give-back follows the return's Total Offering, it is more than the returned lines' share. Both statements are kept.
- **New contradiction 34 (OPEN)**: the trainer describes Current Promotion as an allocated / utilised inquiry (F7, F11); the L4 sweep of DT_PROMOTION (cnr2dev3, 2026-09-25) holds a Document Type / Execution Status setup form. Probably a stale capture; the screen needs to be mapped again before anyone writes steps for it.
- **Checked, no contradiction**: `order_editing_cancellation.md` "promotions are re-applied on the smaller basket" [observed 2026-10-01] fits F16 (budget at save). Whether the edit also gives budget back is not stated, so it became Q-PR1.
- **Checked, no contradiction**: cancellation gives the budget back (F23), and the manual's s.14 (Target Discount) agrees.
- **Ambiguity, not a contradiction**: F17 "free goods apply only once the order is Confirmed", while orders already read Confirmed (execution 02) right after save (contradiction 3, resolved) and orders with no stock stay unallocated with status Order (Q16 / Q27). Filed as Q-PR9.
- **Source gaps found**: the manual (R2) names "IO Listing", but the R2 menu of KPO_slv shows "IO Master" and only the R1 menu of KPO_mp shows "IO Listing". The manual's "Credit Note" screen does not match any menu entry ("Debit\Credit Note", "Credit Note Editing"). Both are folded into Q-PR5.

## 5. What still needs a live walk
Nothing is asserted until it has been seen. Confirm on **cnr1dev1 (R1)** first, because the manual describes R2. Use **cnr2dev3 (R2)** only to see the manual's version.
- cnr1dev1, read-only (L48, L49): the promotion / budget / claim / receivable menus of the Maker and the Checker; whether Current Promotion Approver and Active Promotions exist for them; the real labels of Current Promotion (contradiction 34) and Budget Setup; allocated / utilised of the group 11 promotions (Automation2, MARCH001, MARCH002, May001, May003).
- cnr1dev1, data-changing, QA Team Lead's go-ahead only: budget Utilized before and after an order save (case 1), a cancellation (6), an order edit (L46, Q-PR1), a full and a partial return (7, 8; L51, Q-PR10); free goods with and without free-SKU stock (L50, Q-PR9); the balance boundary (cases 2-3, which needs a dedicated test budget).
- cnr2dev3: Promotion Layout (Save, then Apply), the Excel upload, approval on Current Promotion Approver and the integrator job (Q-PR3), the Budget Setup upload validations (case 11), IO Listing / IO Master and the off-invoice credit note upload and approval. Record every message text (knowledge-intake §1b), because none has been captured yet.
- The app-cartographer should map Promotion Layout (INCENTIVE_SCHEME_BUILDER), IO Listing (DYL_202028) and DT_PROMOTION again (L4).

## 6. Not done here (main session)
- `docs/STATUS.md` resume point.
- Filing the pptx in `apps/snd/knowledge/sources/` and `sources/README.md`.
- G0 sign-off of the area (QA lead only).
