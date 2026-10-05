# Learning plan: S&D Daily Cycle group 11, Pakistan — session 2 (fresh full run)

Run id `LEARN-G11-PK/20261005-0921`. Standard: `docs/LEARNING_STANDARD.md`. Based on session 1 plan/report (`apps/snd/knowledge/business/learning_sessions/2026-10-01_G11-PK_session1_*`); only deltas are listed here.
Type: learning session (business facts only, no element ids). Date 2026-10-05 (Mon), start 09:21 PKT; whole chain must run today.

## Scope and decisions (QA lead, 2026-10-05)
- Group 11, active rows only, seq 1 -> 71 in order; env cnr1dev1; Unilever Pakistan Limited / 15108843 IBRAHIM TRADERS.
- Maker = Automation (session start) or Auto_Multi_Orga; Checker = Auto_Tssm (app.yaml).
- **Seq 15 Order Editing: RUN IT** (date range must include the orders' delivery date; workbook edit: outlet 04 order, 62740537 -> 4 CS 0 PC, reason Order Change QTY; expected Gross 96,840.34 / Discount -20,718.07 / Tax 14,584.79 / Net 90,707.00).
- **Seq 51 Route Settlement: day-close question (Q-RS1) NOT answered** -> run until seq 51; if "previous days not closed" appears, stop and show the QA lead; decide then.
- Seq 18: unallocate ONE order and re-allocate it (as session 1, QA lead option 1) unless told otherwise.

## Focus for session 2 (what session 1 left open)
- Confirm session-1 facts quickly (no re-learning of what is [observed]); spend attention on the unwalked flows: seq 15, 51-60, 68-71, and open questions Q-SR1, Q-DS1, Q-RS2, Q-GRN1, Q-OB1.
- Morning baseline: Stock Inquiry for 2026-10-05 BEFORE the DA (answers Q-OB1: does a new day open at 0 or with openings?).

## Data
Same products/outlets as session 1 (outlets 1000000004-08, 11 on PJP 02111; delivery PJP 02112). Fresh documents only; do not touch session-1 documents (DA 1358, orders COL26000002003-2008, GIN 506, return 713, slips 1131-1136, GRN 246) or older.

## Stop rules
As session 1 (learning_plan.md of 2026-10-01 §8), plus: stop at the seq 51 day-close message.
