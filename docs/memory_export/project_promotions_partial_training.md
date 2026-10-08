---
name: project-promotions-partial-training
description: "S&D promotions - what was learned (Promotion Layout structure, Automation2 slab behaviour, free goods), what is NOT trained (creating/editing promotions), ask-when-needed rule."
metadata:
  node_type: memory
  type: project
  originSessionId: b5778f77-fda9-45aa-a9b0-f6d24e0e917f
  modified: 2026-10-08T13:12:17.353Z
---

Knowledge lives in qa-os/apps/snd/knowledge/business/promotions_and_budget/ (+ test_data/PK.md "Promotions usable"). Trained 2026-10-07/08: QA member session + manual digest, then two live walks on cnr1dev1 as Auto_Multi_Orga.

**Learned live (2026-10-08):**
- Promotion Layout (Company setup > Promotion > Promotion Layout, menu id INCENTIVE_SCHEME_BUILDER) is open to Auto_Multi_Orga. List = Scheme button, paged (299 promos, 31 pages, no search); open a promo by double-clicking its row. Builder toolbar: Save, Copy & Save As New Scheme, Cancel, Console, Back, Scheduler (cron builder), Allocation (disabled without budget). No Apply button seen.
- Header: Promo Code, Name, Alternate Name, dates, Entity Type (Outlet), Promo Sub Type (Normal Scheme), Status, Resultant Type (BONUS2 / TRADEOFFER / COUPON / CONSUMER PROMOTION / FRITMAMT / JUPITER - no "BONUS"), Group Type (1-Seq1..), Budget Hirearchy (ORGA~DIST~DSRS). Settings bar: Claimable, Promo Ret Type, Trade Offer Flag, CM Count, Discount Cap, price basis.
- Builder = Qualify / Criteria / Resultant palettes, Root Group AND/OR, Include/Exclude; Additional Limits = Repeat Limit, For Every Factor, Purchase Limit, Discount Limit (per invoice).
- Free goods = Resultant palette "Product" with type Fixed Value + unit (e.g. JAY81832 "Free Piece": Gross > 2000 -> 14 PC Dove free).
- Automation2 (BONUS2, active, distributor 15108843): >= 5 CS of the 5 trained SKUs; Range Slab 1-10 CS -> 5 %, 11+ -> 10 % of gross. G12 walk proved: slab chosen on total cases and applied FLAT to all lines; discount on gross before tax; Total Offering line = header Discount (Transaction Inquiry, Document Type "Sales"). Orders COL26000002029 (5 %) / 030 (10 %); outlet 1000000013 had tax 0.
- Framework DB: ~90 promotion flows (group 74 Pak All Promotion Charges, group 12, BD 81/83, PH budget 84/85) but NO flow on Promotion Layout - promotions were always created by hand.

**Not trained (long-term gap):** creating/editing a promotion. First attempt (QUICK-20261008-1739) stopped by the QA lead: "promotion is quite difficult module, we need you to get training on it". Unknowns: mandatory fields, how it becomes applied, slab From/To unit, settings-bar meanings.

**Why / how to apply:** QA lead: ask at the time when a run touches promotions; never execute creation/editing until trained. 14 pending trainer questions: learning_sessions/2026-10-08_Promotions_questions_for_trainer.md. Next candidate walk: group 74. Related: [[feedback-knowledge-gap-gate]], [[feedback-never-mention-source-code]], [[reference-ms-promotion-repo]].
