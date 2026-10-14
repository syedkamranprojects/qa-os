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
updated: 2026-10-14
---

# Delivery Man Shuffling: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the group 66 (NG_Setup Flow_PK) learning walk, seq 36, on cnr1dev1 on 2026-10-09 (trainer / QA lead Syed Kamran). One run only. Tags: **[observed 2026-10-09]** live; **[stated 2026-10-09 Syed Kamran]** QA-lead decision; [inferred] Claude's conclusion. Rules: `docs/LEARNING_STANDARD.md` §3.
Source flows: group 66 seq 36 (02260001 Delivery Man Shuffling: Part 1 Order Booking, Part 2 Delivery Man Shuffling).
Last updated: 2026-10-14 (earlier: 2026-10-09).
**2026-10-12 KNOWN ISSUE:** the QA team answered **N** to our summary of this screen (review statement 16) with "a known issue that requires investigation and resolution" [stated 2026-10-12 QA team]. The behaviour below stays recorded as **observed** but is **not a business rule**: do not assert it as expected behaviour. The correct behaviour was not given: Q-DM2 (**deferred: raise when a ticket touches this area (QA lead 2026-10-12)**); contradiction 48. (superseded 2026-10-14: the QA team confirmed the observed behaviour **is correct** ('yes it is correct'); the **only** defect is the on-load error message 'PJP not found' / "Required parameter 'pjpNo' is not present." shown before a Source PJP is chosen (the known issue) [stated 2026-10-14 QA team]. The behaviour in sections 5-7 is now a **business rule**; Q-DM1 and Q-DM2 are answered, contradiction 48 resolved.)
**2026-10-14 (live training session with the QA team, PK cnr1dev1; trainers Syed Kamran (QA lead), Feroz Hussain, Muhammad Fahad; tag [stated 2026-10-14 QA team]):** Q-DM1 and Q-DM2 answered (#7); log `../learning_sessions/2026-10-14_SND-PK_QA-Team_live_log.md`, report `../learning_sessions/2026-10-14_SND-PK_QA-Team_live_report.md`.

## 1. Purpose
- Moves a booked order (cash memo) from a **source Delivery Man PJP** to a **destination Delivery Man PJP**, i.e. hands the delivery to another delivery man before the goods are issued [observed 2026-10-09; purpose inferred from the screen].
- Place in the business: after Order Booking, before the GIN (delivery planning).
- **Confirmed 2026-10-14** [stated 2026-10-14 QA team]: choose the Source PJP + the Outlet(s) (multi-select) + the destination Delivery Man PJP -> Save "Saved Successfully" -> the order leaves the source list and from then on **belongs to the destination delivery-man PJP** (its DSR / delivery man).

## 2. Actors and roles
- Maker (Auto_Multi_Orga) books the order and shuffles it; no approval step was seen [observed 2026-10-09].
- 2026-10-14 general rule: a user can act on a document only when a role is assigned to the user AND the same role is in that document's workflow diagram [stated 2026-10-14 QA team] (../document_lifecycle.md section 0e); no workflow step was seen on this screen [observed 2026-10-09].

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
- After re-opening, the source DM PJP 8197298470 lists **0 orders**: the order left the source's list [observed 2026-10-09]. (2026-10-12: known issue per the QA team [stated 2026-10-12 QA team]; expected result unknown, Q-DM2.) (superseded 2026-10-14: this **is** the expected result [stated 2026-10-14 QA team]; Q-DM2 answered.)
- AUTO301258 is not offered as a Source PJP, so the order could not be read back under the destination on this screen [observed 2026-10-09]. The order's PJP / DSR in Order View after the shuffle was not checked (Q-DM1). (2026-10-14, Q-DM1 answered: after the shuffle the order belongs to the **destination DM PJP** and its DSR / delivery man, e.g. COL26000002031 8197298470 -> AUTO301258 [stated 2026-10-14 QA team]; the destination read-back on Order View / GIN is still unobserved, so an assertion reads it there [inferred].)

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| order listed under source DM PJP | tick + Save with a destination | no longer under the source | Maker | [observed 2026-10-09] |
| order under source DM PJP | tick + Save with a destination | belongs to the **destination DM PJP** (its DSR / delivery man) | Maker | [stated 2026-10-14 QA team] |

## 8. Rules and validations
- The order is listed under the DM PJP linked by Reference PJP, although its own PJP is the OB PJP [observed 2026-10-09].
- Until a source is chosen the screen shows the error "Required parameter 'pjpNo' is not present." [observed 2026-10-09]. (2026-10-14: this on-load 'PJP not found' message is the **known issue / defect** of the screen; it is **not** an expected message and is never asserted [stated 2026-10-14 QA team].)
- Destination: picking an option from the full list by text failed; typing then clicking the single option worked; the first item can get auto-set [observed 2026-10-09].

## 9. Messages
| Type | Text | Trigger | Tag |
|---|---|---|---|
| error (on screen) | "Required parameter 'pjpNo' is not present." | screen open, no source chosen / destination empty | [observed 2026-10-09] (2026-10-14: known issue, the screen's only defect; not an assertion [stated 2026-10-14 QA team]) |
| toast success | "Saved Successfully" (capital S) | Save with a ticked order | [observed 2026-10-09] |

## 10. Dependencies
- Before: an order booked on an OB PJP linked to the source DM PJP; stock in the OB PJP's warehouse for the order (an order draws stock from its PJP's warehouse, order_booking.md) [observed 2026-10-09]. (superseded 2026-10-12, wording: the order does not draw / deduct stock; availability is checked and the quantity temporarily allocated in that warehouse [stated 2026-10-12 QA team])
- After: GIN on the destination DM PJP [inferred, not walked]. (2026-10-14: the order belongs to the destination DM PJP after the shuffle [stated 2026-10-14 QA team], so its GIN is made on the destination [inferred].)

## 11. Test design hints
| # | Case | Expected | Tag |
|---|---|---|---|
| 1 | Shuffle one order from the source DM PJP to another DM PJP | "Saved Successfully"; the order leaves the source's list | [observed 2026-10-09] | (2026-10-12: known issue [stated 2026-10-12 QA team]; not an expected result until Q-DM2 is answered) (superseded 2026-10-14: expected result, assert it [stated 2026-10-14 QA team])
| 2 | Then read the order on Order View / a GIN of the destination | order now on the destination (to confirm) | [inferred] | (2026-10-14: order belongs to the destination DM PJP / its DSR [stated 2026-10-14 QA team]; screen read-back still to observe)
| 3 | Open the screen without a Source PJP | on-load "Required parameter 'pjpNo' is not present." = known defect; do not assert, do not fail the case on it | [observed 2026-10-09; stated 2026-10-14 QA team] |

Traps: the workbook order outlet 1000000001 is not offered on Aslam PJP OB / Automation_Testing_Section; 1000000014 was used [stated 2026-10-09 Syed Kamran]. The workbook product had no stock in the PJP's warehouse (setup DAs 1362 / 1363 were needed).

## 12. Open questions
- Q-DM1 (class B, OPEN_QUESTIONS.md section 3): after the shuffle, which DM PJP / DSR does the order show (Order View, GIN of the destination)? | Default: the destination PJP. **deferred: raise when a ticket touches this area (QA lead 2026-10-12)**.
- Q-DM2 (new 2026-10-12, class C, 1b): the QA team calls the observed Delivery Man Shuffling behaviour a known issue [stated 2026-10-12 QA team]: what is the correct behaviour (which part is wrong: the source list, the save, the order's PJP afterwards)? | Default: treat the screen as unreliable; no shuffling assertion beyond the observed toast | **deferred: raise when a ticket touches this area (QA lead 2026-10-12)**. Contradiction 48.
- **2026-10-14: Q-DM1 and Q-DM2 ANSWERED** (OPEN_QUESTIONS.md section 2k; deferral removed): the observed behaviour is correct and the order belongs to the destination DM PJP / delivery man; the only defect is the on-load 'PJP not found' / "Required parameter 'pjpNo' is not present." message (known issue) [stated 2026-10-14 QA team]. Contradiction 48 resolved. No open question left on this page.

## 13. Sources
- `../learning_sessions/2026-10-09_G66-PK_session2_log.md` (seq 36, setup DAs 1362 / 1363, run 3); report `../learning_sessions/2026-10-09_G66-PK_session2_report.md`.
- Live training session 2026-10-14 with the QA team (#7, Q-DM1 / Q-DM2): `../learning_sessions/2026-10-14_SND-PK_QA-Team_live_log.md`, report `../learning_sessions/2026-10-14_SND-PK_QA-Team_live_report.md`.
