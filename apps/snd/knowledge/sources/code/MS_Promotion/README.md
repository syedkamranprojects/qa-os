# Code study: MS_Promotion (promotion microservice, Java)

Read-only study for business training (method D, source code). Nothing in the repository was changed; branches were read from `git archive` exports.

| Branch | Commit | Version | Region / env |
|---|---|---|---|
| origin/UL-R1-BD | 51e7e815 (2026-10-06) | 1.1.109.0 | R1 = Pakistan + Bangladesh, cnr1dev1 |
| origin/UL-R2-COUNTRY | 462cb561 (2026-10-06) | 2.3.102.0 | R2, cnr2dev3 (compared only) |

Repository: C:\MyWork\MS_Promotion (remote scm/git/MS_Promotion). Studied 2026-10-08 for Syed Zulfiqar.

- `R1_engine.md` - how a promotion is applied to an order (types, qualify/criteria, order and exclusivity, limits, free goods, edit/return/cancel, messages)
- `R1_budget_api.md` - budget model, utilisation and give-back, promotion setup rules and messages, REST endpoints, tables, org flags
- `R1_vs_R2.md` - promotion features in R2 and not in R1 (and vice versa)

Facts are tagged `[code UL-R1-BD@51e7e815 <path>:<line>]`. Code shows what the service does, not the business intent: a code fact that disagrees with a [stated] ruling is a contradiction for the trainer, never an override. Several behaviours are decided by the caller (S&D order service, target service), which is not in this repository.
