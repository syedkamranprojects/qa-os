---
name: reference-ms-promotion-repo
description: S&D promotion microservice repo C:\MyWork\MS_Promotion; branch per region (UL-R1-BD = R1 PK/BD cnr1dev1), studied read-only for training.
metadata:
  type: reference
---
C:\MyWork\MS_Promotion (Java, remote scm/git/MS_Promotion) = S&D promotion microservice. Branches are per customer/region, not "latest": `origin/UL-R1-BD` = Unilever R1 (PK + BD, cnr1dev1), `origin/UL-R2-COUNTRY` = R2 (cnr2dev3), `NonUL-*` = non-Unilever; local `master` is stale (2025-04). Read via `git archive origin/<branch>` into scratchpad, never checkout/fetch.
Studied 2026-10-08 at UL-R1-BD@51e7e815: qa-os/apps/snd/knowledge/sources/code/MS_Promotion/. Budget upload lives in a separate target-service; S&D order service decides cashmemoEvent S / revert / adjust. Promotion tables (prm_pm_*, glb_pr_orf_orga_wise_feature) are readable via snd-schema. Related: [[feedback-knowledge-gap-gate]], [[reference-snd-table-catalog]].
