# Learning session report: S&D GLOBAL promotions and budget, source-code study of MS_Promotion (2026-10-08)

| Item | Value |
|---|---|
| Date | 2026-10-08 |
| App / market | S&D (DCODE), GLOBAL module (promotions and budget); R1 = Pakistan + Bangladesh |
| Method | **D (source code)**, read-only; no live walk, no DB query, no trainer in the loop |
| Requested by | Syed Zulfiqar |
| Source | MS_Promotion (promotion microservice, Java), repository `scm/git/MS_Promotion`, local `C:\MyWork\MS_Promotion`; branches read from `git archive` exports, nothing in the repository changed |
| Branches | **UL-R1-BD @ 51e7e815** (2026-10-06, version 1.1.109.0, R1, cnr1dev1) - the subject; **UL-R2-COUNTRY @ 462cb561** (2026-10-06, version 2.3.102.0, R2, cnr2dev3) - compared only |
| Studies | `../../sources/code/MS_Promotion/README.md`, `R1_engine.md` (how a promotion is applied), `R1_budget_api.md` (budget, setup rules, messages, endpoints, tables, org flags), `R1_vs_R2.md` (feature diff) |
| Tag | `[code UL-R1-BD@51e7e815 <path>:<line>]`, R2 facts `[code UL-R2-COUNTRY@462cb561 <path>]`; Java paths relative to `PromotionBuilder/src/main/java/com/centegy/` (file name only in the pages) |

## 1. What a [code] fact is (and is not)
- It says what the **promotion service** does. It is never `[observed]` and is asserted only as an expectation "to be confirmed live" (like `[db]`).
- It never overrides a `[stated]` ruling: every disagreement is kept on both sides and filed as a contradiction for the trainer.
- **Decided outside this service** (named on every page that depends on it): which S&D order action sends `cashmemoEvent = S` (budget booked); when `/promotionAllocation/revert | adjust | adjustApproved | compensate` are called (cancel, edit, return, approval) and with what amount; the stock and "Confirmed" checks of free goods; the lines a return sends; Budget Setup and its upload validations (separate **target-service**); the approval on Current Promotion Approver and the trigger / schedule of the integrator `/upload` call.

## 2. Facts added per page

| Page | What was added | Approx. lines / rows with [code] facts (evidence tags) |
|---|---|---|
| `promotions_and_budget/promotions_and_budget.md` | Status note on the code tag; code bullets next to the [stated] facts in §2 (no approval / Apply in the service, API activation, no approver endpoint), §3 (resultant types are DB data, value types), new **§3 "Budget model in the code"** (target-service owner, ORGA~DIST~DSRS, bottom-up TTGC_BTM_UP, PRM_PM_PAL_PROM_ALLOCATION / PRM_PM_PAR_PROM_ALLOCATN_REF, 5 budget checks, org flags incl. ALLOW_PARTIAL_BUDGET, auto budget creation), new **§3 "Loyalty B2B (R1 only, SDMS-12111)"**, new **§3 "R1 vs R2 in the code"**; §4.1 routes (upload staging tables, no cron, cache 3-60 s, mobile sync); new **§4.2a screen -> endpoint map** (proven vs inferred); §4.3 header (no "allocated" state, numbering); §4.4 scheduler / Exclusive / Super Exclusive; new **§4.4a execution order and trade-off** (-2 / -1 / SEQ / sub-seq, TrdOffFlg empty / G / A, Save As New defect candidate); §4.5 code reading of the four Include / Exclude rows + **quantity units and rounding** (QTY1 / QTY2 floor, For-Every floor, slab 2 dp, repeat, bundle; money rounding unclear between the two studies); §4.6 criteria; §4.7 limits table (Purchase Limit, Discount Limit, Discount Cap, BUDDISCCAP, counts, Repeat Limit absent, Target Discount); §4.8 budget upload owner; §5 E (cashmemoEvent); §6 14 "(code)" rows beside the stated rows + **DB tables for read-only checks** + invariant; §7 5 code status rows; §8 code notes next to each stated rule + **promotion setup rules**; §9 **message texts found in the code** (setup exceptions with triggers, upload literals, error-sheet texts, API responses, event-log texts) as assertion candidates, not observed; §10 dependencies; §11 cases 12-20, **7 likely defects**, 4 traps; §12 code notes on Q-PR1-Q-PR10 and new Q-PR11-Q-PR17; §13 sources | about 120 lines / rows (216 tags) |
| `OPEN_QUESTIONS.md` | Updated line + status line; 1b code evidence on Q-PR2, Q-PR4, Q-PR6 and new Q-PR16, Q-PR17; new **§2f answered by code - confirm live** (Q-PR1, Q-PR3, Q-PR5); §3 strike-through of the three, code evidence on Q-PR9, Q-PR10, new Q-PR11-Q-PR15; §5 code evidence on 33 and 34, new rows 35-42; §6 arithmetic | 27 lines (53 tags) |
| `glossary.md` | 8 new terms (cashmemoEvent, Execution order / TrdOffFlg, ALLOW_PARTIAL_BUDGET, Budget hierarchy combination / bottom-up, Allocation journal, Promotion event log, Loyalty B2B, Target-service); 4 rows annotated (Integrator job, Exclusive / Super Exclusive, Discount Limit / Cap, Budget Setup) | 12 rows |
| `LIVE_LEARNING_CHECKLIST.md` | L46-L48 marked as confirmations of answers given by code; new **L52-L56** (allocation journal per action, org flags, execution order / exclusivity, Include + Include OR, Promotion Layout buttons / states) | 8 rows |
| `INDEX.md` | One-line update of the promotions row | 1 |
| `order_to_delivery_planning/order_booking.md` | One line: S event, partial-budget flag, QTY floor | 1 |
| `order_to_delivery_planning/order_editing_cancellation.md` | One line: edit fully re-prices; cancel give-back depends on the revert call; after-GIN limits | 1 |
| `delivery_and_returns/sales_return.md` | One line: return re-evaluates only the original codes; give-back supplied by S&D | 1 |
| `order_to_delivery_planning/stock_allocation.md` | One line: no stock check in the promotion service | 1 |

No [stated] or [observed] fact was deleted or reworded; code facts sit next to them.

## 3. Questions
- **Answered by code - confirm live** (section 2f; removed from the open count, live check kept as confirmation): **Q-PR1** (an edit fully re-prices: old booking reversed, new value booked; L46), **Q-PR3** (no integrator cron in the promotion service; `/upload` pull-triggered; only the 60 s cache refresh; caller / schedule moved to Q-PR16; L47), **Q-PR5** (R2-only feature list = `R1_vs_R2.md` section D; L48).
- **Code evidence added, kept open:** Q-PR2 (Limit per order vs Cap running across orders; class C, matches the default, trainer to confirm), Q-PR4 (free goods consume a quantity budget when one is linked; class C), Q-PR6 (inferred endpoints: Bulk Promo Allocation ~ `/promotionAllocation/allocate`, Cash Memo Promotion Viewer ~ `/promotionSetup/getPEL`; class C), Q-PR9 (no stock / status check in the service), Q-PR10 (give-back amount supplied by S&D).
- **New (7):** B 5 - Q-PR11 (which S&D action sends S and calls revert / adjust / compensate), Q-PR12 (ALLOW_PARTIAL_BUDGET / PROMOTION_PROMPT for PK 010104 and BD 010105), Q-PR13 (Super Exclusive / Exclusive behaviour in R1, Save As New), Q-PR14 (Include + Include OR base), Q-PR15 (what Apply is; "allocated" state); C 2 in 1b - Q-PR16 (where target-service validations, approver and integrator trigger live), Q-PR17 (Repeat Limit).
- **Open totals:** before 44 = A 16 + B 18 + C 10 (1a 7, 1b 3); **now 48 = A 16 + B 20 + C 12 (1a 7, 1b 5)**.

## 4. Contradictions (OPEN_QUESTIONS §5)
| # | Trainer / manual | Code (R1) | Question |
|---|---|---|---|
| 33 (existing, evidence added) | F22: partial return gives back the returned allocation | return re-evaluates only the original promotion codes; no booking on R; give-back amount supplied by S&D via `/adjust` or `/revert` | Q-PR10, Q-PR11 |
| 34 (existing, evidence added) | Current Promotion = allocated / utilised inquiry | `distAll` returns Allocated / Achieved per distributor (supports the trainer) | re-harvest |
| 35 | Include + Include OR: discount on "Either" | discount on all Include products of both selections | Q-PR14 |
| 36 | F21: never partial | partial when `ALLOW_PARTIAL_BUDGET = Y` | Q-PR12 |
| 37 | F17 / F19: free-SKU stock checked, applies once Confirmed | no stock or status check in the service; free goods booked on S | Q-PR9, Q-PR11 |
| 38 | F22 / F23: proportional give-back on cancel / return | service never computes a give-back; caller supplies it | Q-PR10, Q-PR11 |
| 39 | Super Exclusive blocks every other scheme | R1: only runs first; filter commented out | Q-PR13 |
| 40 | F12 "Save, then Apply"; State active / inactive / allocated | only Active A / Inactive I; no Apply, no "allocated" | Q-PR15 |
| 41 | Repeat Limit; Resultant Type TRADEOFFER | no Repeat Limit setting; TRADEOFFER is DB data (observed on orders, so not a gap) | Q-PR17 |
| 42 | F10 / F14 / F15 Excel approval + scheduled integrator job | no approve endpoint, no cron; `/upload` pull-triggered | Q-PR16 (Q-PR3 answered at service level) |

Contradictions now: 42 listed; 21 resolved, 5 partly, **16 open** (4, 6, 7, 8, 23, 31, 33-42).

Consistent with the trainer / manual (no contradiction): Include + Include AND, Include + Exclude AND, Include + Exclude OR (in effect), Exclusive (with nuances), unique Promo Code, per-market promotions (keyed by organisation), F16 if S&D sends S at save, Discount Limit vs Cap as two settings.

## 5. Likely defects found in the code (to reproduce live before reporting)
1. Save As New of a Super Exclusive promotion loses execution order -2 (stored null unless Exclusive is also set) - `PromotionSetupService.java:1831-1838`.
2. Count budgets (SCHCMCOUNT / CMCOUNT) may be consumed twice on an order whose promotion has two resultant lines - `AllocationResolver.java:50-87`.
3. End date stored as midnight: the date window compares full date-time, so the promotion may stop applying later on its last day - `FrequencyQualifier.java:59-65`.
4. Preview vs save: the up-front budget qualifier is not registered, so a preview shows a discount that the S save then drops when the budget is exhausted - `PromotionSection.java:21`.
5. Reversal without row lock (SDMS-10155 "budget removing when multi user save"): plain revert does not lock the allocation row - `PromotionAllocationRevertService.java:39-61`.
6. Missing documentReference: the filler substitutes a random UUID, so a later edit / revert cannot find the booking - `SnDRepositoryFiller.java:292-301`.
7. Mobile-sync `/promotionAllocation/allocate` books the full value with no balance check - `PromotionAllocationService.java:703-719`.

## 6. What must be verified live on cnr1dev1
- **Confirmations of code answers:** L46 (edit re-prices, Q-PR1), L47 (integrator caller / schedule, Q-PR3 -> Q-PR16), L48 (R1 menus vs `R1_vs_R2.md` section D, Q-PR5).
- **New checks:** L52 allocation journal after save / edit / cancel / return approval (Q-PR11, contradictions 33, 37, 38); L53 org flags for PK and BD (Q-PR12); L54 execution order and exclusivity (Q-PR13); L55 Include + Include OR base (Q-PR14); L56 Promotion Layout buttons and states (Q-PR15).
- **Existing checks still needed:** L49 (test promotions, Current Promotion labels, contradiction 34), L50 (free goods, Q-PR9), L51 (partial return give-back, Q-PR10).
- **Boundaries from the code** (page §11 cases 12-20): balance = discount; balance 0.01 short with ALLOW_PARTIAL_BUDGET N and Y; balance 0; QTY1 floor (23 / 24 / 47 pieces at 24 per case); Include + Include OR; exclusive failing its threshold; Super Exclusive + normal.
- Before any DB check: find which connector exposes the `PRM_PM_*`, `TGT_PR_*` and `GLB_PR_ORF_*` tables (snd-schema or another), read-only.
- Every message in page §9 stays an assertion candidate until it is seen on screen with its type (toast / popup / inline).
- Never create or change a promotion or budget on the shared environment without the QA Team Lead's go-ahead; use dedicated test promotions.

## 7. Not done / out of scope
- No live walk, no DB query, no trainer review; no [observed] or [stated] tag was added.
- The S&D order service and the target-service repositories were not read (they decide S events, give-back amounts, stock / Confirmed, budget upload validations).
- `docs/`, `plugins/`, tools and `docs/STATUS.md` were not touched (the resume point in STATUS.md is for the main session).
