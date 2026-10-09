---
option: Delivery Man Shuffling
area: delivery_and_returns
doc_types: [cash memo (CM-01)]
screens: [Order Booking, Delivery Man Shuffling]
framework_flows: [02260001]
markets: [PK]
roles: [Maker]
depends_on: [order_booking, pjp]
sources: [live-walk, sme]
updated: 2026-10-09
---

# Delivery Man Shuffling: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the group 66 (NG_Setup Flow_PK) learning walk, seq 36, on cnr1dev1 on 2026-10-09 (trainer / QA lead Syed Kamran). One run only. Tags: **[observed 2026-10-09]** live; **[stated 2026-10-09 Syed Kamran]** QA-lead decision; [inferred] Claude's conclusion. Rules: `docs/LEARNING_STANDARD.md` §3.
Source flows: group 66 seq 36 (02260001 Delivery Man Shuffling: Part 1 Order Booking, Part 2 Delivery Man Shuffling).
Last updated: 2026-10-09.

## 1. Purpose
- Moves a booked order (cash memo) from a **source Delivery Man PJP** to a **destination Delivery Man PJP**, i.e. hands the delivery to another delivery man before the goods are issued [observed 2026-10-09; purpose inferred from the screen].
- Place in the business: after Order Booking, before the GIN (delivery planning).

## 2. Actors and roles
- Maker (Auto_Multi_Orga) books the order and shuffles it; no approval step was seen [observed 2026-10-09].

## 3. Documents and master data
- The order: **COL26000002031** (outlet 1000000014-Aautomation_Outlet_14, booked on OB PJP 7918624876-Aslam PJP OB, Delivery Date 2026-10-15, net 3,359) [observed 2026-10-09].
- Delivery Man PJPs offered as destination: AutoPJGIN2-Auto GIN PJP DM, AUTO301301-Auto_test, AUTO301258-Auto_test, AutoPromo2-Auto Promo PJP DM, 8197298470-Aslam PJP DM, 02112-AutomationDSR [observed 2026-10-09].

## 4. Inputs: screens and fields
| Screen | Menu | Fields / actions | Tag |
|---|---|---|---|
| Delivery Man Shuffling | under Transaction > Order | **Source PJP** (multi-select tag box), **Outlet** (multi-select tag box), **Destination PJP** (single drop-down); grid Document No, Document Date, PJP, Outlet, Cashmemo Type, Net Amount + a select-checkbox column; Save | [observed 2026-10-09] |

## 5. Process: the business steps in order
1. [Maker] Book an order on an OB PJP whose Reference PJP is the source DM PJP (here Aslam PJP OB -> Aslam PJP DM) -> "Order Save successfully" [observed 2026-10-09] (66:36:02260001 part 1; see order_booking.md).
2. [Maker] Navigate to Delivery Man Shuffling; Choose Source PJP 8197298470-Aslam PJP DM -> the grid lists the order (its PJP column shows the OB PJP 7918624876, cashmemo type 01-Back Office (BO)) [observed 2026-10-09].
3. [Maker] Choose Outlet 1000000014; Choose Destination PJP AUTO301258-Auto_test; tick the order row; Click Save -> toast **"Saved Successfully"**; the grid empties [observed 2026-10-09] (66:36:02260001 part 2).

## 6. Outputs and effects
- After re-opening, the source DM PJP 8197298470 lists **0 orders**: the order left the source's list [observed 2026-10-09].
- AUTO301258 is not offered as a Source PJP, so the order could not be read back under the destination on this screen [observed 2026-10-09]. The order's PJP / DSR in Order View after the shuffle was not checked (Q-DM1).

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| order listed under source DM PJP | tick + Save with a destination | no longer under the source | Maker | [observed 2026-10-09] |

## 8. Rules and validations
- The order is listed under the DM PJP linked by Reference PJP, although its own PJP is the OB PJP [observed 2026-10-09].
- Until a source is chosen the screen shows the error "Required parameter 'pjpNo' is not present." [observed 2026-10-09].
- Destination: picking an option from the full list by text failed; typing then clicking the single option worked; the first item can get auto-set [observed 2026-10-09].

## 9. Messages
| Type | Text | Trigger | Tag |
|---|---|---|---|
| error (on screen) | "Required parameter 'pjpNo' is not present." | screen open, no source chosen / destination empty | [observed 2026-10-09] |
| toast success | "Saved Successfully" (capital S) | Save with a ticked order | [observed 2026-10-09] |

## 10. Dependencies
- Before: an order booked on an OB PJP linked to the source DM PJP; stock in the OB PJP's warehouse for the order (an order draws stock from its PJP's warehouse, order_booking.md) [observed 2026-10-09].
- After: GIN on the destination DM PJP [inferred, not walked].

## 11. Test design hints
| # | Case | Expected | Tag |
|---|---|---|---|
| 1 | Shuffle one order from the source DM PJP to another DM PJP | "Saved Successfully"; the order leaves the source's list | [observed 2026-10-09] |
| 2 | Then read the order on Order View / a GIN of the destination | order now on the destination (to confirm) | [inferred] |

Traps: the workbook order outlet 1000000001 is not offered on Aslam PJP OB / Automation_Testing_Section; 1000000014 was used [stated 2026-10-09 Syed Kamran]. The workbook product had no stock in the PJP's warehouse (setup DAs 1362 / 1363 were needed).

## 12. Open questions
- Q-DM1 (class B, OPEN_QUESTIONS.md section 3): after the shuffle, which DM PJP / DSR does the order show (Order View, GIN of the destination)? | Default: the destination PJP.

## 13. Sources
- `../learning_sessions/2026-10-09_G66-PK_session2_log.md` (seq 36, setup DAs 1362 / 1363, run 3); report `../learning_sessions/2026-10-09_G66-PK_session2_report.md`.
