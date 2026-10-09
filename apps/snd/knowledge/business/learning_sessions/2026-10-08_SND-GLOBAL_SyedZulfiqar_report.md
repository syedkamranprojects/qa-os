# Training report - S&D claims, PJP and outlet master data (GLOBAL), 2026-10-08

- Trainer: Syed Zulfiqar
- Market: GLOBAL unless a rule is market-specific (the PJP guide is Pakistan; Jira tickets carry their region)
- Environment: none (no live walk). R1 = cnr1dev1, R2 = cnr2dev3.
- Log: `2026-10-08_SND-GLOBAL_SyedZulfiqar_log.md` (beside this report). Consolidated 2026-10-09 into `apps/snd/knowledge/business/`.
- **Naming:** this session's rulings F1-F11 clash with the 2026-10-07 session's F1-F23, so they are always cited **"F<n> (10-08)"**, e.g. `[stated 2026-10-08 Syed Zulfiqar (F7 10-08)]`.

## 1. Methods used
- **A. Documents** (tag `[stated 2026-10-08 doc:<file> s.<n>]`):
  - "claim management manual_R2 Aug 2026.pptx" (12 slides, Centegy, R2, Aug 2026) - digest D1-D9. **Source gap: not in the workspace** (trainer's Desktop; planned `apps/snd/knowledge/sources/20261008_claim management manual_R2 Aug 2026.pptx`).
  - "PJP updated R2.pptx" (25 slides, PJP Master user guide v1.1, 06-Aug-2024, Pakistan) - P1-P13; filed as `apps/snd/knowledge/sources/20261008_PJP updated R2.pptx`.
  - "outlet changes.pptx" (25 slides, Outlet Master user guide v1.2) - O1-O14; filed as `apps/snd/knowledge/sources/20261008_outlet changes.pptx`.
  - Screenshots of all three decks (and the outlet deck's narration audio) were not reviewed: mandatory markers, menu paths and most message texts are missing.
  - Still a source gap from the previous session: "Promotions and Budgets 2026_R2.pptx" is also not in the workspace. Both gaps are listed in `apps/snd/knowledge/sources/README.md`.
- **B. Verbal rulings** F1-F11 (10-08) (tag `[stated 2026-10-08 Syed Zulfiqar (F<n> 10-08)]`).
- **Jira** (SDMS search, centegy.atlassian.net, trainer authorised; tag `[jira <KEY>]` with region and status; every [jira] fact is an expectation "to be confirmed live"; New / Open tickets describe a bug or a wish). The log notes that one ticket's description contains a plain-text login; it was not looked up or copied.

## 2. Facts added per page
| Page | Added |
|---|---|
| `promotions_and_budget/claims.md` (new, 13 sections) | 9 deck facts D1-D9 (Claim Inquiry grid, Claim Detail, Reference Info, Adhoc Job Executor + "Message sent successfully.", four conditions, amount rule); 2 rulings F8, F9 (10-08); about 9 Jira facts (Jupiter / Non-Jupiter families, BD claim calendar SDMS-7051, Organization Claim Period, unsettled Jupiter = defect SDMS-12408, TH model SDMS-11924 incl. negative claims); known R2-deck claim facts linked; 8 candidate cases; Q-CL1..Q-CL6 ON HOLD |
| `promotions_and_budget/README.md` | claims.md row, update note (claims ON HOLD), Q-CL pointer |
| `master_data/README.md` (new area) | area summary, training status, page list, related pages |
| `master_data/pjp.md` (new, 13 sections) | 13 guide facts P1-P13; F7, F8 (10-08); about 25 Jira facts (J1 daily PJP job, working dates, "PJP not created"; J2 Section Default delivery days over distributor default, max-days bugs; J3 R1 configuration row, weekend message, fortnightly, TH F1/F2/F4; J5 multi-section outlets, unique-section setting; other: duplicate record, BG code, inactive PJPs); group 11 02111 -> 02112 matches P7 (Reference PJP); 7 candidate cases; Q-PJ1, Q-PJ2, Q-PJ3, Q-PJ5 ON HOLD, Q-PJ4 answered |
| `master_data/outlet.md` (new, 13 sections) | 14 guide facts O1-O14; F1-F7 (10-08) (F5 corrects the deck's s.17 wording); SDMS-12227 workflow DT 0005 -> TM 0008 -> HQ 0001, post-activation edit limit, Completion / Activation dates, with the F6 (10-08) ruling "no conflict"; SDMS-12365; link to group 66 seq 13-16 (outlet 1000000001 NTN / tax flags, 2026-10-05), Q-TX1 and test_data/PK.md; 8 candidate cases |
| `promotions_and_budget/promotions_and_budget.md` | added next to existing facts (no rewording, no line ending with `<!--i-->` touched or added): header update note; §2 TM user = Auto_Tssm (F7 10-08); §3 quantity budgets at ORGA (SDMS-10146), constrained / unconstrained (SDMS-11953); §4.1 integrator runs daily (F10 10-08) + other job schedules (F8 10-08); §4.2 Bulk Promo Allocation = Budget Setup allocation upload (SDMS-9438, 11264, 10146, 10610); §4.7 Discount Limit vs Cap parked (F11 10-08), purchase limit per invoice (SDMS-3027, 11686); §5 F pointer to claims.md; §6 rows: free goods use quantity budget only for SKUs given (SDMS-10626, 10863), cancellation give-back open PK bug (SDMS-11596), order edit gives budget back (SDMS-5481), fresh return bug (SDMS-10625 / 10663), integrator daily (F10); §7 row; §8 Jira summary bullet; §10, §11 traps, §12 update block, §13 sources |
| `OPEN_QUESTIONS.md` | status paragraph; Q-PR2 parked (F11), Q-PR4 / Q-PR6 Jira evidence (kept open); new section 1c (10 ON HOLD); new section 2h (Q-PR3, Q-PJ4); Q-PR1 Jira evidence (still to confirm live); Q-PR3 row marked answered; Q-RL1 F7 + SDMS-12227 evidence; contradictions 43, 44; section 6 arithmetic; legend |
| `glossary.md` | 15 terms (Claim Inquiry, Adhoc Job Executor, Claim Days, Claim / Claimable %, Jupiter / Non-Jupiter claims, PJP / Reference PJP, Selling Category (master), Section / Default delivery days, PJP Change Request / Change Track PJP Config, Outlet Approval II, Change Track Outlet *, Operative Info, Credit Limit Block / Warn, Outlet Price, TM user = Auto_Tssm); 3 rows annotated (Integrator job, Discount Limit / Cap, IO number - already present) |
| `INDEX.md` | Updated note; claims.md row; new section "Before the Daily Cycle: master data" (pjp.md, outlet.md); two document-map rows (PJP, Outlet) |
| `learning_sessions/README.md` | session row |
| `../sources/README.md` | rows for the PJP and outlet decks; source-gap note for the claims and promotions decks |

Fact count (approx.): documents 36 (D 9, P 13, O 14); rulings 11 (F1-F11 (10-08)); Jira about 55 statements across 50+ tickets. No existing statement was deleted or reworded; the only edits to existing lines are appended "(2026-10-08: ...)" annotations and appended evidence in open-question rows.

## 3. Questions
Answered:
- **Q-PR3** (B): the integrator job for Excel-approved promotions runs **daily** [stated 2026-10-08 Syed Zulfiqar (F10 10-08)] (it was already outside the open count, answered by evidence earlier; L47 can be closed).
- **Q-PJ4** (new and answered): the TM approver on cnr1dev1 is **Auto_Tssm** [stated 2026-10-08 Syed Zulfiqar (F7 10-08)].
- Q-CL5 partly: the claim job's name differs per market (F9 (10-08)); PK name to be read live - kept ON HOLD.

Parked: **Q-PR2** Discount Limit vs Cap (F11 (10-08)); still counted open in 1b; assert neither; settle only when a run or ticket shows a difference.

Evidence added, kept open "to confirm live": Q-PR1 (SDMS-5481: edit re-books budget), Q-PR4 (SDMS-10626, 10863, 10146: free goods use quantity budget for given SKUs), Q-PR6 (Bulk Promo Allocation = Budget Setup allocation upload; Cash Memo Promotion Viewer still unknown), Q-RL1 (F7 + SDMS-12227 role codes).

Opened, all **ON HOLD** [stated 2026-10-08 Syed Zulfiqar: do not re-ask until the trainer returns to the topic] (class C, new section 1c): Q-CL1, Q-CL2, Q-CL3, Q-CL4, Q-CL5, Q-CL6 (claims C1-C6), Q-PJ1, Q-PJ2, Q-PJ3, Q-PJ5 (PJP J1, J2, J3, J5).

**Open totals: 47 -> 57 = A 16 + B 19 + C 22 (1a 7, 1b 5, 1c 10 ON HOLD).**

## 4. Contradictions
- **New 43 (OPEN, Q-RL1):** TM / approver role code. QA team table: 0002 TSSM approves [stated 2026-10-08 QA Team]; SDMS-12227: TM = 0008 (DT 0005, HQ 0001) [jira SDMS-12227]; Auto_Tssm is the TM user (F7 10-08). Read Auto_Tssm's role on the Profile screen (L43).
- **New 44 (OPEN, ON HOLD with Q-CL1):** claim period / schedule. Deck: N-1 orders, job on the 10th / 20th / 30th via Claim Days; trainer: claim job weekly or daily per configuration (F8 10-08); BD Jira: claim calendar, all delivered orders since the last claim (SDMS-7051). Possibly per-market configuration (F9 10-08).
- **Not filed (ruled):** outlet approval - F1 (10-08) and the deck (company user approves) vs SDMS-12227's TM forward step: **no conflict**, the TM step comes before the HQ approval [stated 2026-10-08 Syed Zulfiqar (F6 10-08)].
- **Doc issue corrected by the trainer:** outlet deck s.17 says "Change Track Outlet Operative Info" for document changes; documents are changed on Change Track Outlet Document (F5 10-08).
- **Bug vs ruling (not a contradiction):** F23 (2026-10-07) "cancellation gives budget back" vs the open PK bug SDMS-11596 (cancelled invoice's promo amount not reversed, New): the ruling is the intent; a failing case is the known bug.
- Contradictions total: 44 listed; 21 resolved, 5 partly, 18 open.

## 5. What still needs a live walk
- **Claims**: nothing until the trainer returns (ON HOLD). Then: Adhoc Job Executor job names (PK), Claim Inquiry menu path and labels, one claim from group 11 orders delivered N-1 (only with the trainer and the QA Team Lead).
- **PJP (cnr1dev1, read-only first):** PJP Creation of 02111 / 02112 (header, configuration rows, Reference PJP, frequency / repeat days), Section Automation_Testing_Section (Default delivery days vs the observed +6 days), Selling Category 001; TM pending list as Auto_Tssm; messages. Any create / change only with the QA Team Lead's go-ahead (shared group 11 fixtures).
- **Outlet (cnr1dev1, read-only first):** menu paths; Outlet Profile tabs of 1000000001 and 1000000004-11 (tax flags vs Q-TX1); whether Outlet Profile TM exists in R1; credit-limit Block / Warn messages and Outlet Price effect at booking (data-changing, go-ahead needed); Auto_Tssm's role code (L43, contradiction 43).
- Promotions: unchanged list from the 2026-10-07 report; L47 can be dropped (Q-PR3 answered); L46 (edit give-back) now has Jira support.

## 6. Notes for the main session
- **app.yaml roles note: Auto_Tssm = TM user (F7 10-08)** (app.yaml not edited: out of scope for this consolidation). Role code still open (contradiction 43).
- Not done here: `docs/STATUS.md` resume point; order_booking.md cross-references for F2 / F3 / F4 (10-08) (tax change for new orders only, credit limit at booking, Outlet Price) - the facts are on master_data/outlet.md, the order-booking page was not touched; LIVE_LEARNING_CHECKLIST.md (closing L47, new PJP / outlet read-only checks).
- Filing the claims deck and the promotions deck in `apps/snd/knowledge/sources/` when the trainer provides them.
- G0 sign-off of any area: QA lead only.
