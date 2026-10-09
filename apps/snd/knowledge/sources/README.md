# S&D training sources

Documents a trainer gives Claude (user guides, instruction manuals, SOPs, training decks, spreadsheets).

- **New files:** drop them into `inbox/`, then start a training session (`/qa-os:train snd`). Claude reads each file, records its facts in the business pages tagged `[stated <date> doc:<file> p.<page>]`, and moves it here as `<yyyymmdd>_<file>`.
- **Confidential material:** only add documents the team may share inside this repository. Anything client-restricted stays out of git (keep it in `inbox/` and do not commit it, or give it verbally).

| Date added | File | Title / owner | Version | Areas covered |
|---|---|---|---|---|
| | | | | |
| 2026-10-08 | 20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx | QA team answers to the G11-PK session-3 review (rules + open questions) | filled 2026-10-08 | all four areas; text copy: business/learning_sessions/2026-10-08_QA_Team_Review_answers.md |
| 2026-10-08 | 20261008_PJP updated R2.pptx | "PJP Master - DCODE: User Guide" (25 slides; market Pakistan; participants DT user); given by trainer Syed Zulfiqar | v1.1, last updated 06-Aug-2024 (file name says R2) | master data: PJP Creation, PJP Change Request, Change Track PJP Config, Selling Category, Section, outlet-to-section mapping, Section Bulk Upload -> business/master_data/pjp.md (P1-P13; screenshots not viewed) |
| 2026-10-08 | 20261008_outlet changes.pptx | "Outlet Master - DMS-NG: User Guide" (25 slides, Centegy; no market or date given; embedded narration audio); given by trainer Syed Zulfiqar | v1.2 | master data: Outlet Profile, Outlet Approval II, change-track screens, Outlet Status, Excel change / creation uploads, Outlet Price -> business/master_data/outlet.md (O1-O14; screenshots and audio not reviewed) |

Source gaps (not in the workspace, on the trainer's Desktop; planned names): `20261008_claim management manual_R2 Aug 2026.pptx` (claims deck, 12 slides, R2, Aug 2026; digested in business/promotions_and_budget/claims.md) and `20261007_Promotions and Budgets 2026_R2.pptx` (promotions deck, 51 slides, R2, July 2026; digested in business/promotions_and_budget/promotions_and_budget.md).
