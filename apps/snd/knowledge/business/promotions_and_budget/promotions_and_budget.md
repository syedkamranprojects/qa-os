---
option: Promotions and Budget
area: promotions_and_budget
doc_types: [promotion (scheme), promotion budget, IO number, off-invoice credit note, claim]
screens: [INCENTIVE_SCHEME_BUILDER, DT_PROMOTION, CURRENT_PROMOTION_APPROVER, ACTIVE_PROMOTIONS, BUDGET_LAYOUT, BULK_PROMO_ALLOCATION, CASH_MEMO_PROMOTION_VIEWER, DYL_202028, OFF_INVOICE_CREDIT, CREDIT_NOTE_APPROVAL, DYL_102014]
framework_flows: []
markets: [GLOBAL]
roles: [Maker, Checker]
depends_on: [order_booking, stock_allocation, order_editing_cancellation, sales_return, transaction_inquiry]
sources: [sme, document, source-code]
updated: 2026-10-08
---

# Promotions and Budget: how it works (S&D / DCODE)

Status: DRAFT written by Claude from one training session (2026-10-07, Syed Zulfiqar: verbal facts F1-F23 and the user manual "Promotions and Budgets 2026_R2.pptx", 51 slides, "Promotion Master - User Manual", July 2026, market Pakistan, R2), the 2026-10-08 QA-team write-up of that session, and the menu / L4 screen maps harvested 2026-09-25. **Nothing here has been observed live** (no walk yet), so there is no [observed] tag except where the order side was already seen in the group 11 walks (marked). Tags: **[stated 2026-10-07 Syed Zulfiqar]** = verbal ruling of the trainer (abbreviated below as **[stated SZ]**); **[stated 2026-10-07 doc:Promotions and Budgets 2026_R2.pptx s.<slides>]** = the manual (abbreviated **[stated doc s.<slides>]**; s.? = slide not given in the write-up); **[db 2026-09-25 menu]** = menu API harvest per user role (`knowledge/env/<env>/menu.<user>.json`); **[db 2026-09-25 L4]** = screen sweep labels (`knowledge/screens_observed/*.json`, cnr2dev3, KPO_slv); [inferred] = Claude's reading. Trainer rulings win over the manual (knowledge-intake §3). Rules: `docs/LEARNING_STANDARD.md` §3.
**Source gap:** the pptx itself is **not in the workspace** (it is on the trainer's Desktop; planned file name `apps/snd/knowledge/sources/20261007_Promotions and Budgets 2026_R2.pptx`); slide numbers are taken from the 2026-10-08 write-up, which gives ranges only (6-31 Promotion Layout, 14 Target Discount, 34-41 Budget Setup, 42-50 off-invoice / claims) and no screenshots were viewed. Re-check slide references when the file is filed.
**Code study added 2026-10-08 (method D, source code):** the promotion microservice MS_Promotion was read on branch UL-R1-BD @ 51e7e815 (version 1.1.109.0, R1 = PK + BD, cnr1dev1) and compared with UL-R2-COUNTRY @ 462cb561 (R2, cnr2dev3); studies in `../../sources/code/MS_Promotion/` (`R1_engine.md`, `R1_budget_api.md`, `R1_vs_R2.md`). Tag **[code UL-R1-BD@51e7e815 <file>:<line>]** (R2: **[code UL-R2-COUNTRY@462cb561 <file>]**); Java paths are relative to `PromotionBuilder/src/main/java/com/centegy/` and given here by file name only (the full path is in the study files); `res/` = `PromotionBuilder/src/main/resources/`. A [code] fact says **what the promotion service does**, not the business intent and not what the user sees: it is never [observed], it is asserted only as an expectation "to be confirmed live" (like [db]), and where it disagrees with a [stated] fact both are kept and a contradiction is filed (OPEN_QUESTIONS §5, rows 35-42). **Several behaviours are decided by the caller, not by this service:** the S&D order service decides which action sends `cashmemoEvent = S` (budget booked), when `/promotionAllocation/revert | adjust | compensate | adjustApproved` are called (cancel, return, approval), the stock and "Confirmed" checks of free goods, and what lines a return sends; the separate **target-service** owns Budget Setup and its upload validations. <!--i-->
Source flows: none (not in framework group 11).
Last updated: 2026-10-08 (code study). <!--i-->

## 1. Purpose
- A promotion (scheme) rewards an outlet's order with a discount (percentage or fixed value of Gross) or free goods when the order qualifies; promotions can be linked to a budget that limits how much reward is given; Promotion and Budget are one business area [stated SZ (F3)] [stated doc s.6-31].
- The Promotion module is a **generalised system feature, not tied to a market**; each market uses only the promotions defined for it (Pakistan sees only Pakistan's promotions) [stated SZ (F1, F4)].
- The promotion screens exist in every region; functionality grows with the region number: R1 = cnr1dev1, R2 = cnr2dev3 [stated SZ (F2)]. Everything in R1 is ported to R2, but R2 features are not necessarily ported back to R1, so an R2 document may describe features missing in R1 [stated SZ (F5)].
- Place in the business: promotions are master data **set up before** orders; they act on Order Booking (discount / free goods at save), Order Editing and Cancellation, Sales Return (re-pricing and budget give-back) and are read on Transaction Inquiry > Total Offering. The Daily Cycle (group 11) uses existing promotions (Automation2, MARCH001, MARCH002, May001, May003) but never creates or changes one [observed 2026-10-01 G11-1, order side only; see transaction_inquiry.md].
- Off-invoice rewards are paid later as credit notes against an IO number, and claims are settled outside DCODE [stated doc s.42-50].

## 2. Actors and roles
- Only two QA roles exist (Maker / Checker; `apps/snd/app.yaml`). Which cnr1dev1 / cnr2dev3 users may open the promotion screens is not yet known: the menu of KPO_mp (cnr1dev1) lists Promotion Layout, Current Promotion, Budget Setup, IO Listing, Off-Invoice Credit Note (+ Approval) but **not** Current Promotion Approver or Active Promotions; the menu of KPO_slv (cnr2dev3) lists both [db 2026-09-25 menu]. Menus are per role, so the absence may be role- or region-dependent (Q-PR5) [inferred].
- **Manual promotion** (Promotion Layout): created by a setup user; Save, then Apply; **no approval** [stated SZ (F12)].
- **Excel-upload promotion**: approved on Current Promotion Approver by **any user who has the approval role** (no fixed user) [stated SZ (F14)].
  - Code (R1), for the manual and the Excel routes above: the promotion service has **no approve endpoint and no promotion status other than Active A / Inactive I**; a manual save writes the promotion with the Active flag chosen on screen [code UL-R1-BD@51e7e815 PromotionSetupService.java:1000-1131]. There is no "Apply" call or "allocated" state in this service (contradiction 40, Q-PR15). <!--i-->
- **API promotion (e.g. PRAT)**: no user approval; it becomes part of DCODE directly [stated SZ (F10, F13)].
  - Code (R1): `POST /promotionSetup/updateProjectCodeAndBudgetValue` sets project code + budget value and **activates** a promotion whose end date is after today, with no approval [code UL-R1-BD@51e7e815 PromotionSetupService.java:1851-1889] [code UL-R1-BD@51e7e815 PromotionUploadService.java:58-81]; that this is the PRAT feed is [inferred] (the word PRAT does not appear in the code). <!--i-->
- On cnr1dev1 the KPO_mp menu has no Current Promotion Approver either [db 2026-09-25 menu].
- Code (R1): **Current Promotion Approver** has no endpoint in the promotion service (no approver workflow; only `PUT /promotionAllocation/adjustApproved`, a budget re-adjust after an approved document) [code UL-R1-BD@51e7e815 PromotionAllocationController.java:51-54]; the approver screen is probably in a workflow service or the UI [inferred] (Q-PR16). <!--i-->
- **Budgets**: the Trade Category team sends budget files to the MIS team, who amend and upload them in Budget Setup; budgets are kept at region or distributor level [stated doc s.34-41].
- **IO numbers**: CD Finance creates the IO code in the third-party system; MIS creates the same code in DCODE (IO Listing) [stated doc s.42-50].
- **Off-invoice credit notes**: uploaded, reviewed and forwarded for **TM approval**; approved on Off-Invoice Credit Note Approval [stated doc s.42-50]. Which application role code (0001 / 0002 / 9999) maps to "TM" is [unknown] (Q-PR5 / Q-RL1 context).
- Order users (Maker) never touch promotions directly: the system applies them at order save [stated SZ (F16)] [observed 2026-10-01 G11-1, order side].

## 3. Documents and master data
- **Promotion (scheme)**: header + Qualify + Criteria + Resultant (section 4); identified by a unique **Promo Code** [stated doc s.6-31]. Promotions seen on group 11 orders: Automation2 / Automation2-3 (BONUS2), MARCH001 (BONUS2), MARCH002 (TRADEOFFER), May001 (BONUS2), May003 (BONUS2) [observed 2026-10-01 G11-1; transaction_inquiry.md]. Their definitions have not been read.
- **Resultant Type** values include BONUS and TRADEOFFER [stated doc s.6-31]; the orders show BONUS2 / TRADEOFFER [observed 2026-10-01 G11-1].
  - Code (R1): resultant types are **DB master data**, not code; there is no `TRADEOFFER` literal in the service. The nearest code concept is the **trade-off flag** `TrdOffFlg` (header field `tradeOff`), which decides whether earlier promotions' discounts are subtracted first (section 4.4a) [code UL-R1-BD@51e7e815 PromotionETLService.java:307]. Only SCHEME-type promotions (type 0001) are calculated on an order; sub-types SCHCHARGE 0005 and SCHTAX 0006 **add** to the amount, every other sub-type reduces it [code UL-R1-BD@51e7e815 PromotionHeader.java:70-74, 96-118] [code UL-R1-BD@51e7e815 PromotionExecutor.java:90-91]. A resultant line is either a **money discount** (tag REPO, typically code DISONGROSS "Discount on Gross") or a **free product** (tag PROD, value type F) [code UL-R1-BD@51e7e815 BusinessResolver.java:40-41] [code UL-R1-BD@51e7e815 BreakupResolver.java:64-68]. Value types: P percentage, F fixed or "X for every N", L formula [code UL-R1-BD@51e7e815 ResolvablePromotionItem.java:594-602]. <!--i-->
- **Promotion budget**: created in Budget Setup with Catalog Id, Date From / To, Bottom Up, measurement, Is Active and an entity-level combination (Distributor, Organization, DSR, Outlet, PJP); two combinations exist by default: **Outlet only**, and **Organization + Distributor + Outlet** [stated doc s.34-41]. The Budget Setup grid carries Budget Code, Period Start / End Date, Allocated Budget, Utilized Budget, Balance, **Allocated / Utilized / Balance Budget QTY**, Ref. Promo Code, Ref. Promo Type, Final Allocation Date [db 2026-09-25 L4 BUDGET_LAYOUT] (the QTY columns suggest quantity budgets too: Q-PR4 [inferred]).
- **Budget Hierarchy**: organisation > distributor > sub-element; the budget sits on the sub-element [stated doc s.6-31].

### Budget model in the code (R1, added 2026-10-08) <!--i-->
- **Owner:** Budget Setup data (catalog, levels, Allocated / Utilized / Balance, the budget Excel upload and its validations) belongs to a separate **target-service**; the promotion service only **reads** budgets over REST and **records consumption** in its own tables [code UL-R1-BD@51e7e815 TargetMasterService.java:30, 60, 82, 213, 244, 327]. <!--i-->
- **Budget = target catalog row** (budget code `TTGC_TARGET_ID`) with a hierarchy combination `TTGC_HIER_COMB`, e.g. **`ORGA~DIST~DSRS`**, and one detail row per value combination `TTCD_HIER_VALUE` (e.g. `0106~D001~DSR01`) holding the target value / qty [code UL-R1-BD@51e7e815 TargetMasterModel.java:11, 142, 151] [code UL-R1-BD@51e7e815 TargetMasterDetailModel.java:14, 48-116]. A promotion points at it through `PRM_PM_PMS_PROMOTION_SETUP.TTGC_TARGET_ID` plus `PPMS_BUDGET_LEVEL`, `PPMS_BUDGET_VALUE`, `PPMS_CHECK_BUDGET` [code UL-R1-BD@51e7e815 PromotionSetup.java:374, 468, 477, 486]. <!--i-->
- **Levels from the order:** DIST = the order's distributor (customerAccountID), DSRS = the DSR, OUTL = the outlet; the order's value combination is built token by token from the budget's HIER_COMB [code UL-R1-BD@51e7e815 SnDRepositoryFiller.java:68-70] [code UL-R1-BD@51e7e815 PromotionBudget.java:228-230]. A PJP-level budget is not read by this code [code study: not supported / unclear]. <!--i-->
- **Bottom-up (`TTGC_BTM_UP = Y`):** when no budget row exists at the exact level, the service climbs one level (e.g. DSR -> DIST) and uses the parent's **remaining** value (target - allocated); it stops (no budget) when only ORGA is left; an exact-level match uses the full target value [code UL-R1-BD@51e7e815 TargetMasterService.java:108-157]. <!--i-->
- **Consumption ledger:** `PRM_PM_PAL_PROM_ALLOCATION` per orga + field comb + value comb + budget + promotion: `PPAL_ALLOCATED_VALUE/QTY` (allocated snapshot) and `PPAL_ACHIEVED_VALUE/QTY` (= Utilized); **Balance = Allocated - Achieved, not stored** [code UL-R1-BD@51e7e815 PromotionAllocation.java:11-125]. Every movement is journaled in `PRM_PM_PAR_PROM_ALLOCATN_REF` (one row per document per event: `PPAR_DOCUMENT_REF`, `PPAR_ACHIEVED_VALUE/QTY`, `PPAR_CM_EVENT` A = apply / R = reverse, `PPAR_LOG_EVENT`) [code UL-R1-BD@51e7e815 PromotionAllocationReference.java:14-163]. Utilized never goes below 0 [code UL-R1-BD@51e7e815 PromotionAllocationRevertService.java:90-94, 139-143]. <!--i-->
- A budget **raised** in target-service raises the allocated snapshot at the next use; a budget **lowered** is only lowered when already-achieved <= the new budget (a budget never effectively drops below what is utilised) [code UL-R1-BD@51e7e815 PromotionAllocationService.java:200-216]. <!--i-->
- **Current Promotion** (code of `GET /promotionSetup/distAll`): Allocated = target value / qty at `ORGA~DIST` for the logged-in distributor; Achieved = SUM of `PPAL_ACHIEVED_VALUE/QTY` over `ORGA~DIST%` (the distributor plus all its DSR rows) [code UL-R1-BD@51e7e815 PromotionSetupService.java:1339, 1460-1515]. <!--i-->
- **Five budget checks per resultant line** [code UL-R1-BD@51e7e815 AllocationResolver.java:55-86]: header budget `TTGC_TARGET_ID` (value for a REPO discount, **quantity for free goods** [code UL-R1-BD@51e7e815 PromotionBudget.java:262]); scheme count `SCHCMCOUNT` (1 per document); outlet cash-memo count `CMCOUNT` (1 per document, per hierarchy combination); `BUDDISCCAP` (another budget named in the property, value); Discount Cap `DISCCAP` / `DISCCAPLMT` (value, across orders). <!--i-->
- **Organisation flags** in `GLB_PR_ORF_ORGA_WISE_FEATURE` (option type SCHEMEBUILDER or BUDGET) [code UL-R1-BD@51e7e815 OrganizationFeaturePromoRepository.java:15-28] [code UL-R1-BD@51e7e815 PromotionUtils.java:392-410]: **`ALLOW_PARTIAL_BUDGET`** (Y = a short balance gives a partial discount, section 6), `PROMOTION_PROMPT` (Y = a failing promotion reverts budgets and returns the error to S&D; N default = skip it and continue) [code UL-R1-BD@51e7e815 PromotionExecutor.java:74, 138-190], `CHECK_PROJECT_CODE`, `PROMO_AUTO_PREFIX`, `FUTURE_ANY_PROMO_REQUIRED`, `BUDGET_QTY_VISIBILITY` (R1 only: quantity budget columns created only when Y). Values on cnr1dev1 for PK (010104) and BD (010105): not read yet (Q-PR12). <!--i-->
- **Auto budget creation on promotion Save** (`POST /promotionSetup/saveAsMap`): if a Budget Level is set and no budget exists with code = promotion code, the service posts one to target-service at ORGA level; Check Budget = N ("unconstrained") -> budget = the promotion's budget value, level forced to ORGA; otherwise the budget is created with value **0** at the chosen level. A Budget Level cleared with no target **deletes** the budget catalog + detail rows with code = promotion code [code UL-R1-BD@51e7e815 PromotionSetupController.java:331-335] [code UL-R1-BD@51e7e815 TargetMasterService.java:229-288]. Promotion date / status changes are **not** synced to the budget (the REST call is commented out) [code UL-R1-BD@51e7e815 TargetMasterService.java:342-372]. <!--i-->

### Loyalty B2B (R1 only, SDMS-12111) (added 2026-10-08, code) <!--i-->
- A promotion with `CouponVer = LTYB2B` is a **Loyalty B2B** promotion: executed like an external coupon scheme ("Discount on Gross" from the external scheme value); business qualifier, section qualifier, business resolver and post-promo resolver are skipped for it [code UL-R1-BD@51e7e815 ExecutionPolicy.java:8] [code UL-R1-BD@51e7e815 CouponResolver.java:107-113]. <!--i-->
- On save: sec type `PromoSecType = LTYB2B`; with a budget level, Check Budget = N and budget value **999,999,999,999.00** (effectively unlimited), auto-created at ORGA; at run time `~DIST` is appended to the allocation key, so consumption is tracked per distributor [code UL-R1-BD@51e7e815 PromotionSetupService.java:1095-1101] [code UL-R1-BD@51e7e815 PromotionBudget.java:253-257]. <!--i-->
- Editing an LTYB2B / coupon order reverts its budgets (SDMS-12374) [code UL-R1-BD@51e7e815 CouponResolver.java:162]. R2 has no LTYB2B handling (its slot means coupon "1.0") [code UL-R2-COUNTRY@462cb561 ExecutionPolicy.java]. Not taught by the trainer; no screen mapped [inferred: set up on Promotion Layout]. <!--i-->
- **IO number** (internal order) used to trace off-invoice payouts and claims; 10-12 characters, unique [stated doc s.42-50].
- **Off-invoice credit note**: one row per customer + IO + payout month + year [stated doc s.42-50]; the approval grid shows Document No., IO Number, IO Description, Payout Month, Payout Year, Distributor, Customer, PJP code, Credit Note Amount, Credit Note Expiry Date [db 2026-09-25 L4 CREDIT_NOTE_APPROVAL]. Transaction Inquiry offers Document Types "OFF INVOICE CREDIT NOTE" and "Off Invocie Credit Note" (sic) [observed 2026-10-01 Block 1; transaction_inquiry.md §4].
- **Claim**: sent to Atlas with distributor, claim no., outlet, document, amount and promo / IO code [stated doc s.42-50].
- Master data a promotion reads: product hierarchy (Qualify), outlets / DSRs / distributors / geography / tags such as cash memo type (Criteria) [stated doc s.6-31].

### Pakistan configuration (F4)
The manual's "Market: Pakistan" means its examples and restrictions are **Pakistan's configuration**, not global rules [stated SZ (F4)]:
- Entity Type = **Outlet** only [stated doc s.6-31; meaning stated SZ (F4)].
- Promo Sub Type = **normal** scheme only [stated doc s.6-31; meaning stated SZ (F4)].
- Other markets (e.g. Bangladesh, R1 = PK + BD) may use other entity types / sub types; not taught yet [inferred].

### R1 / R2 caveat (F5)
The manual describes R2 (cnr2dev3). Before asserting any fact of this page on cnr1dev1 (R1), confirm the feature exists there [stated SZ (F5)]. Known menu differences on 2026-09-25 (per user role, so not yet proof of a region difference): R2 KPO_slv has Current Promotion Approver, Active Promotions, Customer Discount (+ Approval), Distributor Markup (+ Approval), Temporary Price Reduction, Off invoice Budget Upload, Claim Review And Approval, IO Master; R1 KPO_mp has IO Listing, Promotion Eligible, Custom Tags, Event Custom, Disqualified Promotion, Redemption Limit and none of the R2-only items [db 2026-09-25 menu]. The manual's "IO Listing" exists in the R1 menu, while the R2 menu shows "IO Master" instead (Q-PR5) [db 2026-09-25 menu].

### R1 vs R2 in the code (added 2026-10-08) <!--i-->
Branch diff UL-R1-BD @ 51e7e815 (1.1.109.0) vs UL-R2-COUNTRY @ 462cb561 (2.3.102.0): 130 differing paths; full list with evidence in `../../sources/code/MS_Promotion/R1_vs_R2.md` (**section D = the R2-manual features likely missing on cnr1dev1**). Feature flags are per organisation, so a feature present in code may still be off on an environment. Summary: <!--i-->
- **R2 only (do not assert on cnr1dev1 until seen there):** promotion states New / Ready / Active / Inactive / Expired and the Activate Promotion (bulk status) screen with pre-activation validation; Customer Discount screens and two-level approval; Distributor Markup (+ SKU-level markup); TPR list and end-date edit; Current Promotion end-date edit, Original End Date, 7-day look-ahead; Promotion Layout user rights (create / update / copy) and the Copy & Save switch; Promotion Mechanics header fields (Deal Type, Budget Level Code, Sales Org, Final Allocation Date); two-level budget and budget-to-promotion sync; free-product budget in **amount** with price strategy, stock type and UOM; multi-variant free products; Coupon 1.0 / 2.0 / 3.0; SFTP / integration creation screen, export and enrichment; Outlet Segment / Outlet Rank criteria; "For every" percentage; exclusion per sub-type; "IO Number" wording [code UL-R2-COUNTRY@462cb561, see R1_vs_R2.md A1-A23]. <!--i-->
- **Ordering differs:** in R1 Exclusive / Super Exclusive run **before** every sequence (execution order -1 / -2); in R2 the -1 / -2 marking is commented out and **group sequence wins** [code UL-R1-BD@51e7e815 PromotionSetupService.java:1107-1113] [code UL-R2-COUNTRY@462cb561 PromotionSetupRepository.java, PromotionExecutor.java]. An R2 manual statement about sequence vs Exclusive does not hold on R1. <!--i-->
- **R1 only:** Loyalty B2B (LTYB2B, section above); the `BUDGET_QTY_VISIBILITY` switch; exclusive-first ordering; negative sign of charge / tax lines in the order breakup (business impact unclear) [code UL-R1-BD@51e7e815 BreakupResolver.java:192-194]. <!--i-->
- **Partial budget** differs: R1 applies `ALLOW_PARTIAL_BUDGET` to every resultant type; R2 only to percentage resultants or free-product-amount budgets and adjusts the other budgets down to match [code UL-R2-COUNTRY@462cb561 PromotionBudget.java getPartialBudgetFlag]. <!--i-->
- **Same on both:** promotion / business / budget-type enums, the custom-tag and promo-description Excel download / upload and their "Sheet Altered..." messages, the only scheduled job (60 s cache refresh). <!--i-->

## 4. Inputs: screens and fields

### 4.1 Routes into DCODE
| Route | Where it starts | Approval | How it becomes live | Tag |
|---|---|---|---|---|
| Manual | Promotion Layout (Scheme tab, New) | None | Save, then Apply; applies to upcoming orders | [stated SZ (F6, F9, F12)] [stated doc s.6-31] |
| Excel upload | Uploaded into Current Promotion Approver | Yes, any user with the approval role | A **scheduled integrator job** brings it into DCODE after approval | [stated SZ (F8, F9, F10, F14, F15)] |
| API integration (e.g. PRAT) | Third-party system | None | Becomes part of DCODE directly | [stated SZ (F9, F10, F13)] |
After that, back office syncs the promotions to the mobile app as files, so back office and mobile apply the same schemes [stated doc s.?].

Code facts on the routes (R1, added 2026-10-08): <!--i-->
- **Excel / integrator upload:** `GET /promotionSetup/upload?orgaCode=` reads the staging tables `PRM_PM_TSH_TEMP_SCHEME_HEAD` (+ `_TSQ` qualify, `_TSR` resultant, `_TSS` slab, `_TSG` group) for rows modified after the watermark in `PRM_PM_LUT_LAST_UPLOAD_TIME`; rejects a promotion without a Qualify row or without resultant and slab; builds the promotion (Claimable = Y, 100%; SCHCMCOUNT, CMCOUNT, DISCCAP = outlet capping, SlabUnit, TrdOffFlg); **deletes and re-inserts** an existing same-code promotion; staging active Y/A -> A, else I; writes `PTSH_PROCESS_STATUS` S/F and `PTSH_PROCESS_MESSAGE` back; answers Total / Success / Fail counts [code UL-R1-BD@51e7e815 PromotionSetupController.java:210-315] [code UL-R1-BD@51e7e815 PromotionETLService.java:299-379] [code UL-R1-BD@51e7e815 TempPromotionHeadService.java:31-53]. The endpoint is **pull-triggered: no integrator cron exists in this service** (`quartz.enabled=false`) [code UL-R1-BD@51e7e815 res/application-common.properties:76-77]; who calls it and when is outside this repository (Q-PR3 answered at service level, Q-PR16). No approval step exists in this service (contradiction 42). <!--i-->
- **API:** see section 2 (`updateProjectCodeAndBudgetValue` activates; `POST /associateTarget`, `/promoCodesAssociateWithTargetCodes` link promotions to budget codes) [code UL-R1-BD@51e7e815 PromotionSetupRepository.java:52-53]. <!--i-->
- **When a change reaches orders:** a save triggers a cache reload after about **3 s**; a job also compares DB and cache **every 60 s** and reloads what changed; so a newly saved or activated promotion applies within about 3-60 s [code UL-R1-BD@51e7e815 PromotionCacheUpdateService.java:22-39] [code UL-R1-BD@51e7e815 PromotionDefinitionProvider.java:466-470, 763-890] [code UL-R1-BD@51e7e815 PromotionSetupService.java:1747]. Manual reload: `POST /promotionSetup/reloadPromotions` [code UL-R1-BD@51e7e815 PromotionSetupController.java:522-525]. <!--i-->
- **Mobile sync (inferred caller):** `POST /promotionSetup/getActivePromos` returns the promotions applicable to given outlets / products **that still have budget at ORGA~DIST** (or no budget), plus all tax / charge promotions; mobile consumption comes back through `POST /promotionAllocation/allocate` (journal `PPAR_LOG_EVENT = MOB-SYNC`, refuses a second allocation for the same document + promotion + budget, adds the full value **without a balance check**) [code UL-R1-BD@51e7e815 PromotionSetupService.java:2194-2296] [code UL-R1-BD@51e7e815 PromotionAllocationService.java:532-539, 703-719]. <!--i-->

### 4.2 Screens
| Screen | Menu path | Option id / route | Purpose | Tag |
|---|---|---|---|---|
| Promotion Layout | Company Setup > Promotion > Promotion Layout | INCENTIVE_SCHEME_BUILDER, /scheme-builder/promotion-list | Create a promotion manually (Scheme tab, New) | purpose [stated SZ (F6)]; menu [db 2026-09-25 menu, both envs] |
| Current Promotion Approver | Company Setup > Promotion > Current Promotion Approver | CURRENT_PROMOTION_APPROVER, /dtPromotion/current-promotion-approver | Landing place of third-party (PRAT) / uploaded promotions; approve Excel uploads here | purpose [stated SZ (F8, F10)]; menu cnr2dev3 only [db 2026-09-25 menu] |
| Current Promotion | Company Setup > Promotion > Current Promotion | DT_PROMOTION, /dtPromotion/dt-promotion-list | Inquiry of active promotions with amount / quantity **allocated and utilised**; the screen used in practice | [stated SZ (F7, F11)]; menu both envs [db 2026-09-25 menu] |
| Active Promotions | Company Setup > Promotion > Active Promotions | ACTIVE_PROMOTIONS, /scheme-builder/active-promotions | Lists active promotions only (no budget figures) | [stated SZ (F11)]; menu cnr2dev3 only [db 2026-09-25 menu] |
| Budget Setup | Target > Budget > Budget Setup | BUDGET_LAYOUT, /target | Create, allocate (Excel), edit promotion budgets | [stated doc s.34-41]; menu both envs [db 2026-09-25 menu] |
| Transaction Inquiry | Transaction Inquiry (DYL_102014; write-up: Transaction > Order > Transaction History) | DYL_102014 | Total Offering tab: each promotion applied to an order, type and discount | [observed 2026-10-01 G11-1]; see transaction_inquiry.md |
| Bulk Promo Allocation | Target > Target > Bulk Promo Allocation | BULK_PROMO_ALLOCATION, /target/promo-target-builder | Purpose not taught (Q-PR6); tabs ORGA, DIST, CHNLHIER | [db 2026-09-25 L4] |
| Cash Memo Promotion Viewer | Configuration > System Configuration > Cash Memo Promotion Viewer | CASH_MEMO_PROMOTION_VIEWER, /dyl/layout | Purpose not taught (Q-PR6); a setup grid Code, Description, Abbreviation, Default, Status, Level Type, Level No | [db 2026-09-25 L4] |
| IO Listing | Transaction > Claim > IO Listing | DYL_202028 (R1 menu); R2 menu shows "IO Master" DYL_202058 | Create the IO code | [stated doc s.42-50]; [db 2026-09-25 menu] |
| Off-Invoice Credit Note | Transaction > Receivable > Off-Invoice Credit Note | OFF_INVOICE_CREDIT, /excel-upload/off-invoice-credit-excel-upload | Excel upload of off-invoice credit notes against an active IO | [stated doc s.42-50]; [db 2026-09-25 menu] |
| Credit Note | Transaction > Receivable > Credit Note (manual wording) | not matched: the menus show "Debit\Credit Note" (DYL_201901) and "Credit Note Editing" | Review and Forward for TM approval | [stated doc s.42-50]; menu mapping [unknown] |
| Off-Invoice Credit Note Approval | Transaction > Receivable > Off-Invoice Credit Note Approval | CREDIT_NOTE_APPROVAL, /credit-note/credit-note-approval | Select rows, Approve All | [stated doc s.42-50]; [db 2026-09-25 L4] |
| Claim screens | Transaction > Claim > (Claim Period Setup / Distributor Claim Period, Claim Approval, Claim Inquiry ...) | CLAIM_PERIOD, CLAIM_APPROVAL, ... | Claim period and claim follow-up; claims themselves are settled outside DCODE | [db 2026-09-25 menu]; purpose [stated doc s.42-50] |

L4 labels already mapped (sweep cnr2dev3 2026-09-25, labels only) [db 2026-09-25 L4]:
- **Current Promotion Approver** grid: Code, Description, Alternate Description, Start Date, End Date, Reference Code, Status.
- **Active Promotions** grid: Promo Code, Promo Description, Alternate Description, Start Date, End Date, Status, State, Ref. Promo Code, Ref. Promo Type; a Save button (disabled).
- **Current Promotion (DT_PROMOTION)**: the sweep captured a Document Type / Execution Status setup form (Execution Status, Description, Abbreviation, Default, Active, Level No, Level Type, Execution Identifier; Add / Save / Update / Delete), which does **not** match the trainer's description (allocated / utilised inquiry). Probably a stale form captured by the sweep; re-harvest (contradiction 34) [inferred].
- **Bulk Promo Allocation**: tabs ORGA, DIST, CHNLHIER; no fields captured.
- **Cash Memo Promotion Viewer**: Code*, Description*, Abbreviation, Default*, Status*, Level Type, Level No; Add / Save / Update / Delete.
- **Budget Setup**: grid as in section 3.

### 4.2a Screen -> promotion-service endpoint map (code R1, added 2026-10-08) <!--i-->
Service context path `/promotion-service`, port 8094 on R1 [code UL-R1-BD@51e7e815 res/application-common.properties:1-2]. "Proven" = the endpoint's code does what the screen is said to do; the screen-to-endpoint link itself is still [inferred] until a recording shows the call. Use these for read-only API / DB checks, never to change data. <!--i-->

| Screen | Endpoint (method + path) | What it does | Mapping | Evidence | <!--i-->
|---|---|---|---|---| <!--i-->
| Promotion Layout | POST `/promotionSetup/saveAsMap`, POST `/saveAsNew`, GET `/getpromo/{code}` | save, copy (Save As New), open | proven | [code UL-R1-BD@51e7e815 PromotionSetupController.java:171, 331, 505] | <!--i-->
| Promotion Layout | GET `/downloadCustomTag`, POST `/uploadCustomTag`, DELETE `/clearCustomTag` | product / tag allow-list Excel | proven | [code UL-R1-BD@51e7e815 PromotionSetupController.java:351-447] | <!--i-->
| Promotion Layout | GET `/getPromoAudit?promo=&flag=` | change history from `AUD_LG_AT_AUDITTRAIL` | proven | [code UL-R1-BD@51e7e815 PromotionSetupController.java:528] | <!--i-->
| Current Promotion | GET `/promotionSetup/distAll` (older `/listall`) | distributor's running SCHNORMAL promotions with Allocated / Achieved value + qty | proven (code), screen label still suspect (contradiction 34) | [code UL-R1-BD@51e7e815 PromotionSetupController.java:346, 450] | <!--i-->
| Active Promotions | GET `/promotionHeader/getAllActivePromotion`; POST `/promotionSetup/getActivePromos` | active promotions by orga / outlet type / outlet | proven | [code UL-R1-BD@51e7e815 PromotionEligibilityHeaderController.java:42] [code UL-R1-BD@51e7e815 PromotionSetupController.java:160] | <!--i-->
| Active promo Excel | GET `/downloadPromoDesc`, POST `/uploadPromoDesc` | description / alternate description / project code | proven | [code UL-R1-BD@51e7e815 PromotionSetupController.java:455, 468] | <!--i-->
| Current Promotion Approver | none in this service | - | not found (Q-PR16) | - | <!--i-->
| Bulk Promo Allocation | POST `/promotionAllocation/allocate` (list of document, promotion, budget, achieved value / qty, field / value comb) | records budget consumption for already-calculated documents in bulk | **inferred** (Q-PR6) | [code UL-R1-BD@51e7e815 PromotionAllocationController.java:56-96] | <!--i-->
| Cash Memo Promotion Viewer | GET `/promotionSetup/getPEL?orgaCode=&docNo=&docType=&logType=` (REQ, RES or ALL) | last promotion request / response log of a document from `PRM_PM_PEV_PROMO_EVT_LOG`; "No Record Found! ..." if none | **inferred** (Q-PR6; the L4 sweep showed a setup grid instead) | [code UL-R1-BD@51e7e815 PromotionSetupController.java:551-557] [code UL-R1-BD@51e7e815 PromotionSetupService.java:2059-2090] | <!--i-->
| Budget Setup | not in this service: target-service `/api/v1/targetMaster*` | budget catalog, levels, upload | proven (owner) | [code UL-R1-BD@51e7e815 TargetMasterService.java:30] | <!--i-->
| Order Booking / Editing / Return (S&D) | POST `/getResultantsForCashmemo` (also `/getResultantsForCharges`, `/getResultantsForBreakup`) | promotion calculation of a document | proven | [code UL-R1-BD@51e7e815 PromotionSetupController.java:105-138] | <!--i-->
| Cancel / return / approval (S&D) | PUT `/promotionAllocation/revert`, `/compensate/{event}/{eventLog}`, `/adjust`, `/adjustApproved` | budget give-back / redo | proven (code); which S&D action calls which: unknown (Q-PR11) | [code UL-R1-BD@51e7e815 PromotionAllocationController.java:36-54] | <!--i-->
| Integrator | GET `/promotionSetup/upload`; POST `/updateProjectCodeAndBudgetValue`, `/associateTarget`, `/promoCodesAssociateWithTargetCodes` | section 4.1 | proven (code), caller unknown | [code UL-R1-BD@51e7e815 PromotionSetupController.java:210, 409, 425, 511] | <!--i-->
| Loyalty redemption | POST `/redemption/apply`, GET `/info`, `/currinfo`, DELETE `/revert`; POST `/voucher/apply` | points / voucher redeem, enquiry, revert | proven (code); screen not mapped | [code UL-R1-BD@51e7e815 RedemptionController.java:12-35] | <!--i-->

### 4.3 Promotion Layout: header fields [stated doc s.6-31]
Promo Code (unique), Promo Name, Start / End Date, Entity Type, Promo Sub Type, Status, Resultant Type (BONUS, TRADEOFFER ...), Group Type (Charges, Seq1-Seq4, VAT, Adv. Tax, 3rd Schedule Tax, Adv. Tax 3rd Sch), Referral Scheme, Bus. Reference No., Budget Hierarchy (organisation > distributor > sub-element), State (active / inactive / allocated), Ref promo code and type, and the I/O number used to trace claims. Mandatory markers: [unknown] (screenshots not viewed).

Code (R1) on the header: the **State** "allocated" does not exist in the service; only the Active flag A / I (`PPMS_ACTIVE`) [code UL-R1-BD@51e7e815 PromotionSetupRepository.java:26, 72-76] (contradiction 40). Auto numbering prefix `<PROMO_AUTO_PREFIX or JC><MM>-`; manual vs auto numbering via `GET /getPromoNumGenMechanismIsManual` [code UL-R1-BD@51e7e815 PromotionSetupService.java:1724-1759]. Promotion header `entityType` must equal the order's entity type, or be empty [code UL-R1-BD@51e7e815 PromotionSetupService.java:189]. <!--i-->

### 4.4 Scheduling and priority [stated doc s.6-31]
- **Scheduler**: a CRON expression makes a promotion recur (e.g. 7:40 every Monday to Friday).
  - Code (R1): the `frequency` is a Quartz cron expression; the order date-time must match it; an invalid cron fails the promotion (log "Frequency qualification failed") [code UL-R1-BD@51e7e815 FrequencyQualifier.java:67-95]. Date window: the order is rejected if the document date-time is before start or after end, compared on **full date-time** (log "Start/End date qualification failed") [code UL-R1-BD@51e7e815 FrequencyQualifier.java:59-65]; tax promotions use the delivery date when `taxOnDate = DD`, schemes when `schemeOnDate = DD` [code UL-R1-BD@51e7e815 FrequencyQualifier.java:44-57]. <!--i-->
- **Exclusive**: for its product or brand it overrides every other scheme the order qualifies for.
  - Code (R1), consistent in effect: an exclusive promotion (sub-type SCHNORMAL only) that has started marks every product / level of its Qualify section "EXCL = Y"; a **non-exclusive** promotion checked later fails if any of its qualify products is marked [code UL-R1-BD@51e7e815 ExclusionQualifier.java:46-86]. Nuances: the marking happens **even when the exclusive promotion fails its own quantity or criteria check** (all qualifiers run, the result is combined at the end) [code UL-R1-BD@51e7e815 PromotionDefinition.java:182-186]; **two exclusive promotions on the same SKU both apply** (the exclusive branch only marks, never checks) [code UL-R1-BD@51e7e815 ExclusionQualifier.java:55-60]; the rule is skipped on returns [code UL-R1-BD@51e7e815 ExclusionQualifier.java:25]. <!--i-->
- **Super Exclusive**: for an occasion; while active no other scheme applies at all.
  - Code (R1), **contradicts**: Super Exclusive only **runs first** (execution order -2); the logic that would run only super-exclusive promotions when any exist is **commented out** (commit "super exclusion code removed"), so other promotions still apply unless the Exclusive marking blocks them [code UL-R1-BD@51e7e815 PromotionExecutor.java:93-104] (contradiction 39, Q-PR13). <!--i-->

### 4.4a Execution order and trade-off (code R1, added 2026-10-08) <!--i-->
- On save: **Super Exclusive -> execution order -2, Exclusive -> -1, every other promotion null (= 0)** [code UL-R1-BD@51e7e815 PromotionSetupService.java:1107-1113]. <!--i-->
- Promotions run in the order **execution order, then group sequence (`sequance`), then sub-sequence**, nulls = 0 [code UL-R1-BD@51e7e815 PromotionSetupRepository.java:26-27] [code UL-R1-BD@51e7e815 PromotionDefinitionProvider.java:170-173]. So Super Exclusive first, then Exclusive, then the rest by Group Type sequence. There is **no "best deal wins"**: every promotion that qualifies is applied in turn. "Seq1-Seq4" are only DB values of the group sequence; how charges / taxes slot in is DB setup [inferred]. <!--i-->
- Group Type = `promotionTypeGroupCode` -> a PromotionTypeGroup row with sequence, sub-sequence and a parent group [code UL-R1-BD@51e7e815 PromotionTypeGroup.java:20-21]. <!--i-->
- **Trade-off flag `TrdOffFlg`** decides the base [code UL-R1-BD@51e7e815 AbstractPromotionItem.java:221-339, 356-436] [code UL-R1-BD@51e7e815 PromotionTypeGroupService.java:57-92]: <!--i-->
  - empty: **gross** (no deduction); <!--i-->
  - **G**: subtract, product by product, the discounts already applied by promotions of the **parent group chain**; <!--i-->
  - **A**: as G, plus the discounts of promotions already applied in the **same group**. <!--i-->
  - Charges and taxes (apply type "add") enter with a negative sign, so they **increase** the base of later promotions [code UL-R1-BD@51e7e815 AbstractPromotionItem.java:587-603]. <!--i-->
  - A resultant with `totalGross` set uses the order gross and skips both Include / Exclude and the trade-off deduction [code UL-R1-BD@51e7e815 ResolvablePromotionItem.java:707-713]. <!--i-->
- **Save As New defect candidate:** in Save As New the -2 of Super Exclusive is overwritten with null unless Exclusive is also set, so a Super Exclusive copy may run in normal order [code UL-R1-BD@51e7e815 PromotionSetupService.java:1831-1838] (section 11). <!--i-->

### 4.5 Qualify (what must be bought) [stated doc s.6-31]
Product hierarchy values, a quantity, a unit (QTY1 = cases, QTY3 = pieces, VOL ...) and an operator such as "greater than or equal to". Two selections combine:

| Selection 1 | Selection 2 | Operator | Applied on | Discount calculated on |
|---|---|---|---|---|
| Include | Include | AND | Both | Both |
| Include | Exclude | AND | Both | Selection 1 only (selection 2 is a must-buy) |
| Include | Include | OR | Either | Either |
| Include | Exclude | OR | Selection 1 | Selection 1 (selection 2 excluded) |

Code (R1) on the same four rows [code UL-R1-BD@51e7e815 QualifyingPromotionGroup.java:164-198] [code UL-R1-BD@51e7e815 AbstractPromotionItem.java:168-180] [code UL-R1-BD@51e7e815 ResolvablePromotionItem.java:235-289] [code UL-R1-BD@51e7e815 ResultantProcessor.java:28]: <!--i-->
- The qualify check sums each selection's products **whatever their Include / Exclude flag** (an excluded selection is still a must-buy); AND stops at the first failure, OR at the first success. The discount base is the sum of **all Include products of the whole Qualify section**; Exclude products are forced to 0 (Exclude wins if a product appears twice). <!--i-->
- Include + Include AND: confirmed (both). Include + Exclude AND: confirmed (selection 1 only, selection 2 must-buy). Include + Exclude OR: confirmed in effect; if only selection 2 is bought the promotion qualifies with value 0 and is dropped (a result is kept only if its value is > 0). <!--i-->
- **Include + Include OR: differs** - the promotion qualifies when either selection reaches its threshold, but the discount is on **everything bought from both selections**, including a selection that did not reach its own threshold (the base does not check which OR branch qualified) (contradiction 35, Q-PR14). <!--i-->
- Single-value items without a product list (e.g. order GROSSAMT) subtract earlier group discounts (trade-off) before the comparison; product-list items do not [code UL-R1-BD@51e7e815 QualifyingPromotionItem.java:127-134]. Default operator when blank is `==` [code UL-R1-BD@51e7e815 PromotionDefinitionDeserializer.java:253]. <!--i-->

**Quantity units and rounding (code R1)** [code UL-R1-BD@51e7e815 SnDRepositoryFiller.java:138-203]: <!--i-->
- Base quantity (pieces) = Qty3 + Qty2 x QTY2_FACTOR + Qty1 x QTY1_FACTOR (factors from the product's custom-tag params). <!--i-->
- **QTY1 = floor(base / QTY1_FACTOR), QTY2 = floor(base / QTY2_FACTOR)** (rounded down); QTY3 = base / QTY3_FACTOR; VOL = VOL_FACTOR x base. Example: 30 pieces at 24 per case count as **1** QTY1, not 1.25, so a "QTY1 >= 2" promotion needs 48 pieces [code UL-R1-BD@51e7e815 SnDRepositoryFiller.java:158-172, 188-189]. <!--i-->
- Values are also rolled up to the product hierarchy codes PRODANA1-5, so a promotion can be set at brand or category level; LPPC = number of distinct lines. <!--i-->
- "For every" units are truncated: units = floor(measured / factor), benefit = value x units [code UL-R1-BD@51e7e815 ResolvablePromotionItem.java:612-644]. <!--i-->
- Slab matching rounds the measured value to 2 decimals (HALF_DOWN) and takes the first row with from <= value <= to [code UL-R1-BD@51e7e815 PromotionSlabRange.java:272-348, 376-379]. **Repeat = Y** re-runs the match on the remainder (value - row From) and adds results with the same tag; in repeat mode a percentage uses the slab **From** value as its base [code UL-R1-BD@51e7e815 PromotionSlabRange.java:336-369] [code UL-R1-BD@51e7e815 ResolvablePromotionItem.java:722-736]. Bundle mode (`forEveryApplyType = G`): value = number of complete bundles = min over items of floor(bought / required) [code UL-R1-BD@51e7e815 PromotionSlabRange.java:288-297]. <!--i-->
- Money: the two code studies differ. The engine study found no rounding call on the calculation path (DECIMAL128; "final rounding is up to S&D") [code UL-R1-BD@51e7e815 PromotionUtils.java:121-127, 139-161]; the budget study cites a 2 dp HALF_UP rounding helper [code UL-R1-BD@51e7e815 PromotionUtils.java:121-126, 221-226]. Treat money rounding as **unclear**; assert the amounts S&D shows. <!--i-->

### 4.6 Criteria (who is eligible) [stated doc s.6-31]
Outlets, DSRs, distributors, geography or other tags such as cash memo type, each Include or Exclude, singly or in groups; bulk lists by Excel download / upload. In Pakistan the Entity Type is Outlet only (section 3).
- Code (R1): every Criteria item must pass; Include on a list = "value in list", Exclude = "not in list" [code UL-R1-BD@51e7e815 SectionQualifier.java:26-44] [code UL-R1-BD@51e7e815 QualifyingPromotionItem.java:156-165]. Attributes available from the order: distributor DIST, DSR DSRS, outlet OUTL, channel / geography / sales hierarchies (and their parent levels), outlet attributes ATTRIB01-14, payment mode, delivery mode, cash memo type CASHMEMOTP, document type, ranks [code UL-R1-BD@51e7e815 SnDRepositoryFiller.java:68-70, 305-424, 771-847]. A missing order value fails the item [code UL-R1-BD@51e7e815 QualifyingPromotionItem.java:124-125]. The entity-exclusion table query exists but the order path never calls it (unclear whether exclusion lists are enforced elsewhere) [code UL-R1-BD@51e7e815 PromotionSetupRepository.java:32-33]. Product allow-list Excel: column count and name / sequence must match the download; after the start date rows are only added, never removed [code UL-R1-BD@51e7e815 PromotionETLService.java:419-566]. <!--i-->

### 4.7 Resultant (the reward) and limits [stated doc s.6-31, Target Discount s.14]
A direct discount or range slabs; each a percentage or fixed value of Gross, or free SKUs.

| Limit | Meaning | Tag |
|---|---|---|
| For Every Factor | Repeat the reward for every given quantity | [stated doc s.6-31] |
| Purchase Limit | Maximum quantity per invoice that gets the promotion | [stated doc s.6-31] |
| Discount Limit | Maximum discount on one sales order | [stated doc s.6-31] |
| Discount Cap | Maximum a customer can get, e.g. 30% of 200,000 = 60,000 is capped at 50,000 | [stated doc s.6-31]; same setting as Discount Limit? Q-PR2 |
| Repeat Limit | Maximum times the reward repeats, e.g. buy 6 get 1 free, at most 4 times | [stated doc s.6-31] |
| Target Discount | Budget quota given to a distributor and split across DSRs; the promotion stops when it is used up; cancelled orders free the quota | [stated doc s.14] |

Code (R1) on the limits [code UL-R1-BD@51e7e815 ResolvablePromotionItem.java:503-547, 586-588, 612-644, 816-818] [code UL-R1-BD@51e7e815 AllocationResolver.java:55-86] [code UL-R1-BD@51e7e815 PromotionETLService.java:302]: <!--i-->

| Setting | Scope in code | Behaviour in code | vs the manual | <!--i-->
|---|---|---|---| <!--i-->
| For Every factor | per order line / group | units = integer part of measured / factor; benefit = value x units; a money benefit larger than the gross of its base item becomes 0 | consistent | <!--i-->
| Purchase Limit (`purchaseLimit`) | **per order** | caps the eligible base (percentage with a QTY slab unit: unit price x limit; `percentageLimitOn = P`: limit % of the target; bundle: maximum bundle count) | consistent ("per invoice") | <!--i-->
| Discount Limit (`discountLimitValue`) | **per order, per resultant; never stored** | caps the discount: percentage base capped at limit x 100 / value; For-Every units capped at limit x factor / value; formula min(value, limit) | consistent | <!--i-->
| Discount Cap (`DISCCAP`, setup field `outletCapping`) | **across orders**, per combination of the DISCCAPLMT target hierarchy (likely per outlet: DB config) | a running value budget written to `PRM_PM_PAL_PROM_ALLOCATION` on every booked order; used up -> 0 (or the remainder when partial budget is on) | consistent with "maximum a customer can get"; Q-PR2 answered by code (still class C) | <!--i-->
| Budget Discount Cap (`BUDDISCCAP`) | across orders, a named budget | value budget; no error if the budget is not found; one BUDDISCCAP budget may be linked to one promotion only (setup message, section 9) | not in the manual | <!--i-->
| Scheme count `SCHCMCOUNT` / outlet cash-memo count `CMCOUNT` | across orders (whole scheme / per hierarchy combination, likely outlet) | count budgets, 1 per booked document | the manual's "max count" example [inferred] | <!--i-->
| Repeat Limit | - | **no such setting**; the only repeat is the slab Repeat Y/N with no maximum [code UL-R1-BD@51e7e815 PromotionDefinitionDeserializer.java:511-512] | **contradicts** the manual (contradiction 41, Q-PR17) | <!--i-->
| Target Discount | - | no order-level concept; targets serve KPI / target grids and Purchase Limit "% of target" [code UL-R1-BD@51e7e815 PromotionGrid.java:166-215] | the manual's quota = the header budget at DIST / DSR level [inferred] | <!--i-->

`slabCount` / `budgetSlabCountFlag` are read from the promotion JSON but never used in execution (a slab count limit is probably not enforced in R1) [code UL-R1-BD@51e7e815 PromotionDefinitionDeserializer.java:508-527]. <!--i-->

Worked examples in the manual: 2% with cap; 2% with must-have and max count; fixed 2; slab of 2% plus 300; 4% when gross is at least 1,000 and cash memo type is 01; Super Exclusive for one outlet; 5% Exclusive [stated doc s.6-31].

### 4.8 Budget Setup [stated doc s.34-41]
- Upload: Budget Allocation > ORGA or DIST > Export to Excel (template) > Upload Excel. Template columns: Code, Description, Allocated Budget, Utilized Budget, Balance.
- New Budget: Catalog Id, Date From / To, Bottom Up, measurement, Is Active, entity-level combination (section 3).
- Edit Budget: select a budget, change it, Save.
- Code (R1): Budget Setup and its upload belong to the **target-service** (`/api/v1/targetMasterDetail/...`), not to the promotion service, so none of the upload validations of section 8 can be confirmed from this code [code UL-R1-BD@51e7e815 TargetMasterService.java:244, 327] (Q-PR16). Bulk budget heads from the integrator go through `/uploadBulkBudgetListByTagName` [code UL-R1-BD@51e7e815 TargetMasterService.java:296-340]. <!--i-->

### 4.9 Off-invoice inputs [stated doc s.42-50]
- IO Listing: IO number, start date, end date (rules in section 8).
- Off-Invoice Credit Note: Excel upload against an active IO (customer, IO, payout month / year, expiry date, amount).


### Promotion Layout as seen live on cnr1dev1 (QUICK-20261008-1739, stopped before Save) [observed 2026-10-08]
- Auto_Multi_Orga (distributor 15108843) can open Company setup > Promotion > Promotion Layout [observed 2026-10-08]. The page opens with the buttons Scheme, Download Excel, Upload Excel; Scheme shows the paged promotion list (no search box; 259 codes on 31 pages); New opens the scheme builder with the toolbar Save, Cancel, Console, Back, Scheduler, Allocation and the switches Scheduler ON/OFF, Exclusive ON/OFF, Super Exclusive ON/OFF; **no Apply button before the first Save** [observed 2026-10-08].
- The header is an editable grid: Promo Code, Promo Name, Alternate Name, Start Date, End Date, Entity Type, Promo Sub Type, Comments, Status, Resultant Type, Group Type, Budget Hirearchy (spelled so on screen), Referral Scheme, Bus. Reference No. [observed 2026-10-08].
- Options seen: Promo Sub Type includes "Normal Scheme"; Resultant Type = BONUS2, CONSUMER PROMOTION, COUPON, COUPON 1.0, FRITMAMT, JUPITER, TRADEOFFER (**no "BONUS"**, unlike the manual); Group Type = 1-Seq1, 2-Seq2, 3-Seq3, 4-Seq4, 6-Adv.Tax(VAT), 7-3rd Schedule Tax, 8-Adv.Tax(3rd Sch), AdvTax(3rdSch), OOH SEQ1, OOH SEQ2, Value Added Tax; Budget Hirearchy = ORGA~DIST~DSRS only [observed 2026-10-08].
- Builder palettes: Qualify = Group, Formula, Allowable, LPPC, Order Number Count For Cashmemo, Reference Registration, Outlet Order Count, Unique Code, Document Type, Prod Lvl 1-9, Master Product, Product, Tax Master, Tax Detail, Gross Amount; Criteria = Group, Master Channel, Channel, Location, Outlet, Chain Outlets, DSR, Tiers and others; Resultant = Range Slab, Grid, Gross Amount (incl. / excl. tax), MRSP Gross Amount, Tax Gross Amount, Discount on Gross, Loyality Points, Product Amt Includ Tax, Prodcut Amt Excluding Tax, Product (no item named free goods / bonus) [observed 2026-10-08].
- QA member's answers for a free-goods scheme (not yet executed): Resultant Type BONUS2; Group Type 1-Seq1; Budget Hierarchy ORGA~DIST~DSRS; Qualify palette Product (SKU, quantity, unit cases, >=), Criteria palette Outlet (include), Resultant palette Product (free SKU, quantity, unit pieces) [stated 2026-10-08 Syed Kamran].
- **Read-only walk 2026-10-08 (two existing promotions, nothing saved)** - log: [../learning_sessions/2026-10-08_SND-PK_SyedKamran_PromotionLayout_walk_log.md](../learning_sessions/2026-10-08_SND-PK_SyedKamran_PromotionLayout_walk_log.md):
  - A promotion opens by double-click on the list row; an existing one adds "Copy & Save As New Scheme"; Allocation is disabled without a budget [observed 2026-10-08].
  - Settings bar: Promo Version, Claimable, Claimable Percent, LPPC, Promo Ret Type, Sch Cashmemo Count, Product AttributesCoins (price basis), Trade Offer Flag, CM Count, Discount Cap, Budget Discount Cap [observed 2026-10-08].
  - Each section has Root Group (AND / OR), nested groups, Include / Exclude, ON / OFF and an Entity Filter; the Resultant has **Additional Limits: Repeat Limit, For Every Factor, Purchase Limit (Per Invoice), Discount Limit (Per Invoice)** [observed 2026-10-08] (so Repeat Limit is on the R1 screen).
  - **Automation2** (the active group 11 promotion): buy >= 5 (QTY1) of the 5 trained SKUs, distributor 15108843 included, Range Slab Discount On Gross: 1-10 = 5 %, 11-99999 = 10 % of Gross Amount [observed 2026-10-08].
  - **Free goods** are a Resultant **Product** with type Fixed Value and a unit, e.g. JAY81832 "Free Piece": Gross Amount > 2000 -> 14 PC of 20006444 free (types: Fixed Value, Percentage, Formula) [observed 2026-10-08].
  - Still to be trained: slab From / To unit, the settings-bar fields, mandatory fields of a new promotion and when it becomes "applied" (no Apply button seen).
- **Group 12 learning walk 2026-10-08 (framework flow 00910001 "Order Booking Promotion", Maker Auto_Multi_Orga, cnr1dev1)** - log: [../learning_sessions/2026-10-08_SND-PK_SyedKamran_G12_promotion_walk.md](../learning_sessions/2026-10-08_SND-PK_SyedKamran_G12_promotion_walk.md):
  - Order A COL26000002029 (outlet 1000000012, 1 CS of each of the 5 Automation2 SKUs = 5 CS): Gross 28,931.32, Discount -1,446.57 = **5.000 %**, Tax 5,383.88, Net 32,869.00; Order B COL26000002030 (outlet 1000000013, 2+2+2+2+3 = 11 CS): Gross 61,545.15, Discount -6,154.51 = **10.000 %**, Tax 0, Net 55,391.00. Messages "Validation successfully", "Order Save successfully" [observed 2026-10-08].
  - **The Range Slab is chosen on the total qualifying cases and applied flat to the whole quantity** (11 CS -> 10 % on every line, not 5 % on the first 10); each line's discount is its own gross x the slab %; the discount is taken **on gross before tax** and tax is computed after it; Net is rounded to the whole rupee on Order View [observed 2026-10-08].
  - Transaction Inquiry > Total Offering shows one line per applied promotion (Automation2 / BONUS2) whose sum equals the header Discount; the orders are found with Document Type "Sales" [observed 2026-10-08]. Only Automation2 applied to these SKUs and outlets; no free goods [observed 2026-10-08].
- **Training status of the builder: NOT trained (long-term gap)**. The QA lead stopped the first AI execution on 2026-10-08: "promotion is quite difficult module, we need you to get training on it". No AI execution or script generation that creates or edits promotions until a training session on Promotion Layout (header, Qualify / Criteria / Resultant palettes, Save / Apply / Allocation / Scheduler) has been done [stated 2026-10-08 Syed Kamran].

## 5. Process: the business steps in order
No framework flow and no live walk exist yet, so there are no trace keys. Steps in the standard vocabulary, from the trainer and the manual:

A. Manual promotion [stated SZ (F6, F12)] [stated doc s.6-31]
1. [Maker] Navigate to Company Setup > Promotion > Promotion Layout; Click New on the Scheme tab.
2. [Maker] Enter the header (Promo Code, Name, dates, Entity Type, Sub Type, Resultant Type, Group Type, Budget Hierarchy ...).
3. [Maker] Enter Qualify, Criteria and Resultant (with limits).
4. [Maker] Click Save; then Click Apply. No approval; the promotion applies to upcoming orders.

B. Excel-upload promotion [stated SZ (F8, F10, F14, F15)]
1. [Maker] Upload the promotion file into Current Promotion Approver.
2. [Checker] (any user with the approval role) Approve the promotion on Current Promotion Approver.
3. [System] The scheduled integrator job brings the approved promotion into DCODE; only then does it reach orders.

C. API promotion (PRAT) [stated SZ (F13)]
1. [System] The third-party system sends the promotion; it becomes part of DCODE directly (no approval).

D. Budget [stated doc s.34-41]
1. [Maker] Navigate to Target > Budget > Budget Setup; Choose Budget Allocation > ORGA or DIST; Click Export to Excel (template).
2. [Maker] Fill Code, Description, Allocated Budget (Utilized / Balance as given); Click Upload Excel; Verify the validations (section 8).
3. [Maker] Optional: New Budget / Edit Budget (select, change, Save).

E. Order effect (system) [stated SZ (F16-F23)]
1. [Maker] Book an order (Order Booking); at save the qualifying fixed / percentage promotions apply and the budget's Utilized goes up.
2. [Maker] Verify on Transaction Inquiry > Total Offering (one line per promotion) and on Current Promotion (Utilized before / after).
- Code (R1) behind step E1: S&D posts the order to `/getResultantsForCashmemo`; with `cashmemoEvent = C` (also the default when S&D sends none) no promotion is calculated; budgets are **booked only when `cashmemoEvent = S`**; any other value (e.g. N, a preview) calculates without booking; R = return, no booking [code UL-R1-BD@51e7e815 PromotionSetupService.java:215-219] [code UL-R1-BD@51e7e815 SnDRepositoryFiller.java:315-319] [code UL-R1-BD@51e7e815 AllocationResolver.java:23-24, 57-83]. **Which order action sends S (save / confirm / invoice) is decided by the S&D order service** (Q-PR11). Each qualifying promotion runs Qualifiers (date / frequency, business, sections, exclusivity, coupon) -> Resolvers (value) -> Post-resolvers (business, coupon, budget allocation, breakup to lines, post-promo) [code UL-R1-BD@51e7e815 PromotionSection.java:21-22]. <!--i-->

F. Off-invoice credit note and claim [stated doc s.42-50]
1. [Maker] (MIS) Navigate to Transaction > Claim > IO Listing; create the IO code given by CD Finance.
2. [Maker] Navigate to Transaction > Receivable > Off-Invoice Credit Note; upload the Excel against the active IO.
3. [Maker] Navigate to Credit Note; review; Click Forward (for TM approval).
4. [Checker] Navigate to Off-Invoice Credit Note Approval; select rows; Click Approve All (status In-Active -> Active).
5. [System] On the claim days (10th, 20th, 30th; "Claim Days" on the distributor) a scheduled job sends the claims to Atlas.

## 6. Outputs and effects
How orders use the budget: taken at order save, given back on cancellation or return; a promotion never applies partly.

| Event | Effect on the promotion and budget | Tag |
|---|---|---|
| Order saved, fixed or percentage promotion | Applied; budget **Utilized goes up at save** | [stated SZ (F16)] |
| (code) Order request with `cashmemoEvent = S` | Every budget of every qualified resultant is booked: Achieved up by the discount (REPO) or the free quantity (PROD), count budgets +1 per document; journal row A in `PRM_PM_PAR_PROM_ALLOCATN_REF`. Consistent with F16 **if** S&D sends S at save, and broader (free goods are booked on the same event) | [code UL-R1-BD@51e7e815 AllocationResolver.java:55-87] [code UL-R1-BD@51e7e815 PromotionBudget.java:262-265]; which action sends S: Q-PR11 | <!--i-->
| Order saved, free-goods promotion | Stock of the free SKU is checked; the promotion applies only once the order is **Confirmed**; the stock check and Confirmed condition apply only to stock-based (free-goods) promotions | [stated SZ (F17, F18)]; meaning of "Confirmed" here: Q-PR9 |
| (code) Free goods in the promotion service | **No stock check and no order-status check**: `DocumentStatus` is copied in but never read; free goods are calculated and their **quantity budget** booked on the same S event as discounts. The only free-goods limits here are tied to the GIN state: after GIN approval / in process, a new free-product scheme gives 0 and the free quantity cannot exceed the original. If F17 / F19 hold, the S&D order service enforces them (contradiction 37) | [code UL-R1-BD@51e7e815 SnDRepositoryFiller.java:408, 418] [code UL-R1-BD@51e7e815 BusinessResolver.java:40-60] [code UL-R1-BD@51e7e815 BusinessQualifier.java:32-33, 66-87] | <!--i-->
| Free SKU out of stock | Order is saved, but the free goods are **not allocated** | [stated SZ (F19)] |
| Remaining budget less than the discount | Promotion is **not applied at all**; no partial discount up to the balance | [stated SZ (F21)] |
| (code) Short balance | Budget fully used (balance <= 0): line value 0, not applied ("Allocation exhausted"). 0 < balance < requested: **not applied** ("Partial Allocation not configured") **unless the org flag `ALLOW_PARTIAL_BUDGET = Y`**, then **applied partially, capped at the balance**. Balance exactly = requested: applied in full [inferred from grant = min(requested, balance)]. F21 holds only while the flag is not Y (contradiction 36, Q-PR12) | [code UL-R1-BD@51e7e815 PromotionAllocationService.java:141-179] [code UL-R1-BD@51e7e815 PromotionBudget.java:274-286, 412-425] | <!--i-->
| (code) Budget code configured but no budget row | Header budget: promotion line **not validated** ("Budget not found"), so not applied; count budgets silently skipped | [code UL-R1-BD@51e7e815 PromotionBudget.java:293-305] | <!--i-->
| Order cancelled | Budget is given back | [stated SZ (F23)]; [stated doc s.14] agrees (cancelled orders free the quota) |
| (code) Give-back calls | The engine never gives back by itself. S&D must call `PUT /promotionAllocation/revert?documentReference=&eventLog=` (reverses the document's whole latest booking per key, journal R, log suffix `-RVRT-ALC-PROMOTION`) or `/adjust` / `/adjustApproved` (reverse the last booking and re-book the **new value S&D supplies**, capped at the remaining balance; 0 reverses everything incl. count budgets) or `/compensate/{event}/{eventLog}`. **The service never computes a proportion**: a "proportional" give-back is computed by the caller (contradiction 38). Which S&D action calls which: Q-PR11 | [code UL-R1-BD@51e7e815 PromotionAllocationController.java:36-54] [code UL-R1-BD@51e7e815 PromotionAllocationService.java:236-254, 319-357] [code UL-R1-BD@51e7e815 PromotionAllocationRevertService.java:266-327] | <!--i-->
| Order edited (quantity reduced, promotions re-applied) | Budget give-back for the lowered discount not stated | [unknown], Q-PR1 (edit re-applies promotions [observed 2026-10-01 G11-1], order_editing_cancellation.md) |
| (code) Order edited (`entryMode = E`) | **Full re-pricing**: before re-booking, the document's previous booking of the same promotion and budget is reversed (journal R), then the new value booked (A); a lower discount gives the difference back. A promotion that no longer qualifies has its booking reversed ("Reverting budgets"); one that qualifies with value 0 is reversed by the breakup step. Q-PR1 **answered by code - confirm live** (needs S&D to send entryMode E and the same documentReference) | [code UL-R1-BD@51e7e815 PromotionAllocationService.java:113-117] [code UL-R1-BD@51e7e815 AllocationAdjustable.java:42-51] [code UL-R1-BD@51e7e815 BreakupResolver.java:51-56] | <!--i-->
| (code) Order edited after GIN approval (entry mode E, GIN state A) | Only promotions already on the order may qualify ("... promotion code not exists in provided promoCodeList"); new free-product schemes give 0; free quantity capped at the original | [code UL-R1-BD@51e7e815 BusinessQualifier.java:66-87] [code UL-R1-BD@51e7e815 BusinessResolver.java:40-60] | <!--i-->
| Full return | Budget is given back in full (Utilized goes down) | [stated SZ (F20, F22)] |
| Partial return | Budget is given back for the returned allocation only | [stated SZ (F22)]; vs the middle-invoice re-pricing of Q-SR2: contradiction 33, Q-PR10 |
| (code) Return (cash memo type 999999999999, `cashmemoEvent = R`) | Only the promotion codes S&D passes in `promoCodes` are re-evaluated (loaded from the DB, not the cache); criteria, date / frequency and exclusivity checks are skipped; the engine recalculates on whatever lines S&D sends; **no budget is booked or reversed on the R event**; "CODE~0" nulls a free-product line ("Free product not allowed on return after discount ..."), "CODE~1" nulls a discount line. The give-back amount comes from S&D via `/adjust` or `/revert` (contradiction 33 code evidence) | [code UL-R1-BD@51e7e815 PromotionExecutor.java:80-87] [code UL-R1-BD@51e7e815 SectionQualifier.java:31-35] [code UL-R1-BD@51e7e815 PromotionBudget.java:382-410] [code UL-R1-BD@51e7e815 PostPromoResolver.java:44-66] | <!--i-->
| (code) Error during calculation | `PROMOTION_PROMPT = N` (default): the failing promotion is skipped, others continue. `= Y`: budgets reverted (new document: all; edit: re-adjusted) and the error returned to S&D; the order log gets "Error-promotioncalculation" | [code UL-R1-BD@51e7e815 PromotionExecutor.java:74, 138-190] [code UL-R1-BD@51e7e815 PromotionSetupController.java:106-127] | <!--i-->
| Excel-upload promotion approved | Reaches orders only after the next integrator job run | [stated SZ (F15)] |
| Off-invoice credit note approved | Status In-Active -> Active; payout as credit note | [stated doc s.42-50] |

How to check: budget use is read on **Current Promotion** (allocated / utilised) [stated SZ (F7, F11)] (Budget Setup also shows Utilized Budget and Balance [db 2026-09-25 L4]); on an order, Transaction Inquiry > **Total Offering** lists each promotion and its discount and their sum equals the header Discount [observed 2026-10-01, 2026-10-05, 2026-10-06 group 11 walks]. A before / after reading of Utilized is the only budget assertion; no budget effect has been observed yet.

### DB tables for read-only test checks (code R1, added 2026-10-08) <!--i-->
Table and column names from the entity classes [code UL-R1-BD@51e7e815, files as listed]; which connector exposes them (snd-schema or another DB) is not yet checked [inferred]. Read-only `SELECT` only. <!--i-->

| Table | Key / useful columns | Use in a test | <!--i-->
|---|---|---| <!--i-->
| `PRM_PM_PMS_PROMOTION_SETUP` | PORG_ORGACODE, PPMS_PROMOTION_CODE; PPMS_START_DATE / END_DATE, PPMS_ACTIVE (A / I), PPST_PROMOTION_SUBTYPE, TTGC_TARGET_ID, PPMS_BUDGET_LEVEL, PPMS_BUDGET_VALUE, PPMS_CHECK_BUDGET, PPSC_PROMOTION_SECTYPE, PPMS_PROJECT_CODE, PPMS_EXECUTION_ORDER, PPMS_PROMOTION_JSON | promotion header; execution order -2 / -1 / null; end-date time part (PromotionSetup.java:28-600) | <!--i-->
| `PRM_PM_PAL_PROM_ALLOCATION` | orga, PPAL_FIELD_COMB, PPAL_VALUE_COMB, TTGC_TARGET_ID, PPMS_PROMOTION_CODE; PPAL_ALLOCATED_VALUE / QTY, PPAL_ACHIEVED_VALUE / QTY | Utilized per budget level, before / after (PromotionAllocation.java:11-125) | <!--i-->
| `PRM_PM_PAR_PROM_ALLOCATN_REF` | PPAR_ALLOCATION_ID; PPAR_DOCUMENT_REF, PPAR_CM_EVENT (A / R), PPAR_ACHIEVED_VALUE / QTY, PPAR_LOG_EVENT | per-document journal: which action booked or gave back what (PromotionAllocationReference.java:14-163) | <!--i-->
| `TGT_PR_TGC_TARGET_CATALOG` / `TGT_PR_TCD_TARGT_CATALOG_DTL` | TTGC_TARGET_ID, TTGC_HIER_COMB, TTGC_BTM_UP, TTGC_ACTIVE, period; TTCD_HIER_VALUE, TTCD_TARGET_VALUE / QTY, TTCD_ALLOCATED_VALUE / QTY | budget head and per-level budget (TargetMasterModel.java, TargetMasterDetailModel.java) | <!--i-->
| `PRM_PM_PEV_PROMO_EVT_LOG` | PPEV_TRANS_CODE (document no.), PPEV_TRANS_TYPE, PPEV_EVENT, PPEV_REQ_JSON, PPEV_RESP_JSON | **why a promotion or budget was (not) applied** (log texts of section 9) (PromotionEventLog.java:12-130) | <!--i-->
| `PRM_PM_TSH_TEMP_SCHEME_HEAD` (+ TSQ, TSR, TSS, TSG), `PRM_PM_LUT_LAST_UPLOAD_TIME` | PTSG_PROMO_CODE, PTSH_PROCESS_STATUS (S / F), PTSH_PROCESS_MESSAGE; UPLOAD_DATE | upload staging, result and watermark | <!--i-->
| `PRM_PM_PAT_PROM_ALLOW_TAGS`, `PRM_PM_PEE_PROM_ELGBL_ENTITY`, `PRM_PM_PEP_PROM_ELGBL_PROD`, `PRM_PM_DQP_DISQUALIFIED_PROM` | promotion + tag / entity / product; PDQP_FAILING_REASON | allow-list, eligibility, disqualification reasons | <!--i-->
| `GLB_PR_ORF_ORGA_WISE_FEATURE` | PORG_ORGACODE, POPT_OPTION_TYPE (SCHEMEBUILDER / BUDGET), PFRT_FEATURE_TYPE, PORF_VALUES | org flags: ALLOW_PARTIAL_BUDGET, PROMOTION_PROMPT, CHECK_PROJECT_CODE, PROMO_AUTO_PREFIX, FUTURE_ANY_PROMO_REQUIRED, BUDGET_QTY_VISIBILITY | <!--i-->
| `SND_LG_ORL_ORDER_LOG` | LORL_DOCUMENT_NO, LORL_DETAIL_INFO | "Error-promotioncalculation" entries | <!--i-->
| `AUD_LG_AT_AUDITTRAIL` | aat_tablename, aat_pkcolumnvalue = `<promo>~<orga>` | promotion change history | <!--i-->

Useful invariant: for one budget key, `PPAL_ACHIEVED_VALUE` = SUM(`PPAR_ACHIEVED_VALUE`) over the journal (A positive, R negative), floored at 0 [code UL-R1-BD@51e7e815 PromotionAllocationRevertService.java:90-94]. A mismatch after concurrent saves / edits points at SDMS-10155 (section 11). <!--i-->

## 7. Statuses and transitions
| From | Action | To | By | Tag |
|---|---|---|---|---|
| (new) | Save, then Apply (manual) | live in DCODE | setup user | [stated SZ (F12)] |
| uploaded (Excel) | Approve on Current Promotion Approver | approved, waiting for the integrator job | user with the approval role | [stated SZ (F10, F14)] |
| approved (Excel) | scheduled integrator job | part of DCODE | system | [stated SZ (F15)] |
| (API / PRAT) | integration | part of DCODE | system | [stated SZ (F13)] |
| promotion State | active / inactive / allocated | (values only; transitions unknown) | ? | [stated doc s.6-31]; transitions [unknown] |
| (code) (new) | Save (`saveAsMap`) with Active flag | Active A or Inactive I; only A / Y promotions are loaded for orders, and the cache keeps those whose end date >= the previous day | setup user | [code UL-R1-BD@51e7e815 PromotionSetupRepository.java:26, 72-76] [code UL-R1-BD@51e7e815 PromotionDefinitionProvider.java:434-461]; no "allocated" state (contradiction 40) | <!--i-->
| (code) any | Save As New (copy) | new promotion **Inactive I**; DISCCAP, BUDDISCCAP, discount cap values, project code, budget level, budget value and target stripped; allow-list tags copied | setup user | [code UL-R1-BD@51e7e815 PromotionSetupService.java:1762-1848] | <!--i-->
| (code) future promotion | start date reaches today | **frozen** (`entryMode = F`, also on the start day, SDMS-2845): only End Date, the JSON and the Active flag can change; Inactive saves the status only | system | [code UL-R1-BD@51e7e815 PromotionSetupController.java:183-188] [code UL-R1-BD@51e7e815 PromotionSetupService.java:1059-1077] | <!--i-->
| (code) staging row | integrator `/upload` | promotion deleted + re-inserted, A (staging Y / A) or I; staging status S / F | caller of `/upload` (unknown) | [code UL-R1-BD@51e7e815 PromotionETLService.java:299-366] | <!--i-->
| (code) inactive, end date after today | API `updateProjectCodeAndBudgetValue` | Active | integration | [code UL-R1-BD@51e7e815 PromotionSetupService.java:1851-1889] | <!--i-->
| Off-invoice credit note In-Active | Approve All | Active | approver (TM) | [stated doc s.42-50] |
| Claim Draft | ... (10 statuses) | Closed Transaction | outside DCODE (Power BI report) | [stated doc s.42-50] |

## 8. Rules and validations
Promotion rules
- A promotion never applies partly: if the remaining budget is less than the discount, it is not applied at all [stated SZ (F21)].
  - Code: true only while org flag `ALLOW_PARTIAL_BUDGET` is not Y; with Y the discount / free quantity is cut to the balance [code UL-R1-BD@51e7e815 PromotionAllocationService.java:141-179] (contradiction 36, Q-PR12). <!--i-->
- Fixed / percentage promotions apply at order save without a stock check; the stock check and the Confirmed condition are only for free-goods promotions [stated SZ (F18)].
  - Code: the promotion service has no stock or order-status check for any type (contradiction 37); if the rule holds it lives in the S&D order service. <!--i-->
- Exclusive overrides every other scheme for its product / brand; Super Exclusive blocks every other scheme while active [stated doc s.6-31].
  - Code: Exclusive consistent in effect (with the nuances of section 4.4); Super Exclusive only runs first in R1 (contradiction 39). <!--i-->
- Each market sees only its own promotions [stated SZ (F1, F4)].
  - Code: every query and budget is keyed by organisation code `PORG_ORGACODE` [code UL-R1-BD@51e7e815 PromotionSetup.java:28] (consistent). <!--i-->
- Promo Code is unique [stated doc s.6-31].
  - Code: a new record with an existing code is refused: "Promotion Code {0} is already exists." [code UL-R1-BD@51e7e815 PromotionSetupService.java:1023-1025] (consistent). <!--i-->
- Excel-upload promotions need approval; manual and API promotions do not [stated SZ (F10, F12, F13)].
  - Code: no approval step exists in the promotion service for any route (contradiction 42; the approval may live in another service, Q-PR16). <!--i-->

Promotion setup rules in the code (R1, added 2026-10-08; exact texts in section 9) [code UL-R1-BD@51e7e815 PromotionSetupService.java:1000-1131]: <!--i-->
- New record with an existing code -> refused (duplicate code message). <!--i-->
- `BUDDISCCAP` budget already used by another promotion -> refused [code UL-R1-BD@51e7e815 PromotionSetupService.java:1043-1051]. <!--i-->
- Org flag `CHECK_PROJECT_CODE = Y`, status Active, Claimable = Y and no project code -> refused ("Project Code not found ...") [code UL-R1-BD@51e7e815 PromotionSetupService.java:1054-1056, 1133-1151]. <!--i-->
- Start date before today -> refused [code UL-R1-BD@51e7e815 PromotionSetupService.java:1105-1118]; start / end date null -> refused [code UL-R1-BD@51e7e815 PromotionSetup.java:527, 561]. <!--i-->
- Promotion already started (start date <= today): only End Date, JSON and status may change; end date before today -> refused; changed start date -> refused [code UL-R1-BD@51e7e815 PromotionSetupService.java:1059-1077]. <!--i-->
- Future promotion edit keeps budget / project / target fields from the DB; clearing the budget level clears the target [code UL-R1-BD@51e7e815 PromotionSetupService.java:1080-1093]. <!--i-->
- Execution order set on save (section 4.4a); auto budget created on save (section 3). <!--i-->
- Promo description upload: description > 100 characters, unknown orga / promotion, project-code length, or blanking an existing project code -> row error [code UL-R1-BD@51e7e815 PromotionETLService.java:568-676]. Allow-list / description Excel: column count and name / sequence must equal the download [code UL-R1-BD@51e7e815 PromotionETLService.java:561-578]. <!--i-->
- Budget concurrency: the booking path locks the allocation row (`SELECT ... FOR UPDATE`, own transaction); **the plain revert path does not lock** ("no need to lock here"), compensate / adjust do [code UL-R1-BD@51e7e815 PromotionAllocationService.java:110-133, 197] [code UL-R1-BD@51e7e815 PromotionAllocationRevertService.java:39-61, 190, 276]. <!--i-->
- `documentReference` trap: a request with a DocumentNumber but no documentReference gets a **random UUID** as reference, so a later edit or revert cannot find the original booking [code UL-R1-BD@51e7e815 SnDRepositoryFiller.java:292-301]. <!--i-->
- Budget upload validations (below) are **not in the promotion service** (target-service); unconfirmed by code (Q-PR16). <!--i-->

Budget upload validations (each is a negative test) [stated doc s.34-41]
- The promotion code must exist and be active.
- A promotion that has already ended cannot be edited, by HQ or distributor users.
- The distributor must exist, be active and be accessible to the session user.
- The budget must be greater than 0 and never negative.
- The budget cannot be less than the amount already spent.
- Allocated plus used cannot exceed the promotion's budget limit.
- Mandatory columns must be filled.
- Amounts are rounded to 2 decimals (131.4566 -> 131.46; 131.443 -> 131.44).

Off-invoice rules [stated doc s.42-50]
- IO number unique, not blank, 10-12 characters; start and end date today or later; end date not before start date.
- Off-invoice credit note: active customer; customer channel must match the IO's channel; no duplicate of customer + IO + payout month + year; expiry date on or before the IO end date; amount with at most 2 decimals.

## 9. Messages
None observed (no live walk yet). The manual's message texts were not captured in the write-up (screenshots not viewed); every save / approve / upload above needs its message observed live before it can be asserted (knowledge-intake §1b).

**Message texts found in the code (R1, added 2026-10-08) [code] - assertion candidates, NOT observed.** Exact strings as in the source (spelling kept, e.g. "is already exists"). Type on screen (toast, popup, inline) is unknown until observed; the UI may wrap or translate them. Promote a row to an assertion only after it is seen live. <!--i-->

Promotion setup (user-facing exceptions, `res/messages.properties`): <!--i-->
| Text | Trigger | Evidence | <!--i-->
|---|---|---| <!--i-->
| "Promotion Code {0} is already exists." | Save (new) or Save As New with an existing code | [code UL-R1-BD@51e7e815 PromotionSetupService.java:1024, 1811] [code UL-R1-BD@51e7e815 res/messages.properties:8] | <!--i-->
| "Budget Discount Cap already associated with another promotion." | Save with a BUDDISCCAP budget already used | [code UL-R1-BD@51e7e815 PromotionSetupService.java:1050] [code UL-R1-BD@51e7e815 res/messages.properties:9] | <!--i-->
| "Project Code not found, EITHER update the project code OR save with INACTIVE status." | Save Active + Claimable without project code, CHECK_PROJECT_CODE = Y | [code UL-R1-BD@51e7e815 PromotionSetupService.java:1055] [code UL-R1-BD@51e7e815 res/messages.properties:10] | <!--i-->
| "End date could not be less than effective date." | Edit of a started promotion with end date before today | [code UL-R1-BD@51e7e815 PromotionSetupService.java:1068] [code UL-R1-BD@51e7e815 res/messages.properties:11] | <!--i-->
| "Start date cannot be modified after scheme effective date." | Edit of a started promotion with a changed start date | [code UL-R1-BD@51e7e815 PromotionSetupService.java:1070] [code UL-R1-BD@51e7e815 res/messages.properties:12] | <!--i-->
| "Start date could not be less than system date." | Save / Save As New with a start date before today | [code UL-R1-BD@51e7e815 PromotionSetupService.java:1117, 1817] [code UL-R1-BD@51e7e815 res/messages.properties:13] | <!--i-->
| "startDate could not be null or empty." / "endDate could not be null or empty." | Save without dates | [code UL-R1-BD@51e7e815 PromotionSetup.java:527, 561] [code UL-R1-BD@51e7e815 res/messages.properties:5-6] | <!--i-->
| "Sheet Altered, column count mismatch! Uploaded sheet should have {0} Columns, instead of {1};" | allow-list / description Excel with wrong column count | [code UL-R1-BD@51e7e815 PromotionETLService.java:561, 575] [code UL-R1-BD@51e7e815 res/messages.properties:14] | <!--i-->
| "Sheet Altered, column name/sequence mismatch! Uploaded sheet should be same as Download." | same, wrong column names / order | [code UL-R1-BD@51e7e815 PromotionETLService.java:564, 578] [code UL-R1-BD@51e7e815 res/messages.properties:15] | <!--i-->
| "Allocation head not found {0}" | budget revert / compensate with no allocation | [code UL-R1-BD@51e7e815 PromotionAllocationRevertService.java:67, 197] [code UL-R1-BD@51e7e815 res/messages.properties:7] | <!--i-->

Promotion upload screens (controller literals) [code UL-R1-BD@51e7e815 PromotionSetupController.java:98, 267, 271, 390, 394, 399, 418, 485] [code UL-R1-BD@51e7e815 PromotionETLService.java:375, 379]: "File uploaded successfully"; "File is empty unable to uploaded"; "Please enter promotion code, before Upload the File"; "Please select a file to upload"; "Promotion code not exists"; "<code> - Promotion code has been failed with error: The promotion code failed due to improperly defined qualifiers. There should be a Qualify section"; "... There should be a Promotion Resultants or a Promotion Slabs."; "<code> - Promotion code has uploaded successfully"; "<code> - Promotion code has been failed with error: <reason>". Error-sheet column texts (`PromoDescription_Error.xlsx`): ",Invalid Scheme Id found", ",Invalid Tag Code found", ",Invalid code found", ",Invalid Orga code found", ",Invalid length of Promo desc found", ",Invalid length of Promo alternate desc found", ",Invalid length of Project code found", ",Invalid promo found", ",Can not unmapped project code" [code UL-R1-BD@51e7e815 PromotionETLService.java:419-676]. <!--i-->

Allocation / integration API responses (not screen texts unless a screen shows them) [code UL-R1-BD@51e7e815 PromotionAllocationController.java:77-91] [code UL-R1-BD@51e7e815 PromotionAllocationService.java:613-617] [code UL-R1-BD@51e7e815 PromotionSetupService.java:1867-1880, 2087]: "Allocation Successfully Recorded!", "Budget not found", "Allocation Already exists!", "Try Again Later! Failed To Record Allocation.", "Budget not matched! BudgetCode: %s, HirComb: %s, ValueComb: %s", "could not be null or empty or incorrect key found", "promotion details updated having specified code!", "promotion specified code NOT-FOUND!", "No Record Found! <orga>-<doc>-<type>". <!--i-->

Engine **event-log** texts (stored in `PRM_PM_PEV_PROMO_EVT_LOG` response JSON, readable with `getPEL`; **not popups**; the best evidence of why a promotion did not apply) [code UL-R1-BD@51e7e815, files per text in R1_engine.md §9]: "Start/End date qualification failed"; "Frequency qualification failed"; "Business qualification failed, due to promotion code not exists in provided promoCodeList"; "Business qualification failed, due to payload currentPromoSubType not matched in promoTypeList"; "Range slab applied" / "Range slab not applied"; "gross amount exhausted"; "Group discount deducted"; "Allocation exhausted"; "Partial Allocation not configured"; "Allocation key not found"; "Allocation exhausted for combination"; "Budget not found"; "Applied budget"; "Reverting budgets"; "Business resolver failed, new free product scheme cannot be applied"; "On Cashmemo after GIN approval, Free product quantity cannot be greater than original value in Cashmemo"; "Free product not allowed on return after discount, reverting allocation..."; "Discount not allowed on return after free product, reverting allocation..."; "Line level discount validation error, reverting allocation..."; order log "Error-promotioncalculation". <!--i-->

Loyalty / voucher redemption texts (R1, `res/application-promotion.properties:67-92`) are listed in `../../sources/code/MS_Promotion/R1_budget_api.md` §6 (e.g. "Voucher already applied", "Not enough Loyalty Points or Amount to avail", "Invalid voucher"); no redemption screen is mapped yet. <!--i-->

## 10. Dependencies
- Before: product hierarchy, outlets / DSRs / distributors (Criteria), a budget in Budget Setup when the promotion is budgeted, an active IO for off-invoice credit notes [stated doc s.6-31, s.34-41, s.42-50].
- Excel-upload promotions depend on the **integrator job** having run after approval; it is normally scheduled, not started by hand [stated SZ (F15)]; schedule per env unknown (Q-PR3).
- Free-goods promotions depend on stock of the free SKU for the day (stock_inquiry_and_balances.md, stock_allocation.md) [stated SZ (F17, F19)].
- After: Order Booking, Order Editing / Cancellation, Sales Return, Transaction Inquiry (Total Offering) read the promotion; claims go to Atlas on the claim days [stated SZ; stated doc s.42-50].
- Date rules: Start / End Date of the promotion and the CRON scheduler decide when it applies [stated doc s.6-31]; an ended promotion cannot be edited [stated doc s.34-41].
- Code (R1, added 2026-10-08): the promotion service depends on the **S&D order service** (sends the order, the `cashmemoEvent`, `entryMode`, `documentReference`, the return's `promoCodes`, and calls the give-back endpoints) and on the **target-service** (budgets) [code UL-R1-BD@51e7e815 TargetMasterService.java:30]. A saved or activated promotion reaches orders after the cache reload (about 3 s after save, at most about 60 s) [code UL-R1-BD@51e7e815 PromotionCacheUpdateService.java:22-39]; the active-promotion listing includes promotions starting up to **tomorrow** [code UL-R1-BD@51e7e815 PromotionExecutor.java:256-263]. <!--i-->

## 11. Test design hints
Every budget case compares **Utilized on Current Promotion before and after** the action, and the order's **Total Offering**. Before asserting any case on cnr1dev1 (R1), confirm the feature exists there (F5).

| # | Case | Expected | Tag |
|---|---|---|---|
| 1 | Book an order that meets a percentage promotion | Discount in Total Offering; Utilized up by that discount | [stated SZ (F16)] |
| 2 | Boundary: remaining budget exactly equals the discount | Promotion applies; balance becomes 0 | [inferred from F21] |
| 3 | Boundary: remaining budget 0.01 below the discount | Promotion not applied at all | [stated SZ (F21)] |
| 4 | Free-goods promotion, free SKU in stock | Free goods allocated once the order is Confirmed | [stated SZ (F17)] |
| 5 | Free-goods promotion, free SKU out of stock | Order saved, free goods not allocated | [stated SZ (F19)] |
| 6 | Cancel an order with a promotion | Utilized down by the order's discount | [stated SZ (F23)] |
| 7 | Full return of a delivered order | Utilized down by the full discount | [stated SZ (F22)] |
| 8 | Partial return | Utilized down only by the returned part (slab promotions may re-price, Q-SR2 / Q-PR10) | [stated SZ (F22)]; contradiction 33 |
| 9 | Exclusive promotion plus other qualifying schemes | Only the exclusive one applies to that product | [stated doc s.6-31] |
| 10 | Excel-upload promotion approved | Reaches orders only after the next integrator job run | [stated SZ (F15)] |
| 11 | Budget upload breaking each validation of section 8 | Upload refused with an error (texts unknown) | [stated doc s.34-41] |

Cases from the code study (R1, added 2026-10-08) - expectations "to be confirmed live"; read Utilized before / after and, where the connector allows, `PRM_PM_PAL_PROM_ALLOCATION` / `PRM_PM_PAR_PROM_ALLOCATN_REF` / `PRM_PM_PEV_PROMO_EVT_LOG` (read-only): <!--i-->

| # | Case | Expected per code | Tag | <!--i-->
|---|---|---|---| <!--i-->
| 12 | Boundary: remaining budget **exactly equals** the discount | applied in full; balance 0 | [code UL-R1-BD@51e7e815 PromotionAllocationService.java:141-179] (grant = min(requested, balance)) | <!--i-->
| 13 | Boundary: balance 0.01 below the discount, `ALLOW_PARTIAL_BUDGET = N` (or absent) | not applied; event log "Partial Allocation not configured" | same; consistent with F21 | <!--i-->
| 14 | Same, `ALLOW_PARTIAL_BUDGET = Y` | applied **partially**, discount = balance; balance 0 | same; contradicts F21 (contradiction 36) | <!--i-->
| 15 | Balance already 0 | not applied; "Allocation exhausted" | [code UL-R1-BD@51e7e815 PromotionAllocationService.java:174-178] | <!--i-->
| 16 | QTY floor: a "QTY1 >= 1" promotion, buy 1 piece less than one case (e.g. 23 pieces at 24 / case), then exactly 24 | 23 pieces = 0 QTY1, not qualified; 24 = qualified; 47 pieces still count as 1 QTY1 | [code UL-R1-BD@51e7e815 SnDRepositoryFiller.java:158-172] | <!--i-->
| 17 | Include + Include OR, one selection below its threshold | qualifies; discount on the products of **both** selections | contradiction 35 | <!--i-->
| 18 | Edit that lowers the discount (entry mode E) | journal R of the old booking + A of the new one; Utilized down by the difference | Q-PR1 answered by code - confirm live | <!--i-->
| 19 | Exclusive promotion that fails its own threshold + a normal promotion on the same SKU | the normal one is still **blocked** (marking runs anyway) | [code UL-R1-BD@51e7e815 ExclusionQualifier.java:46-86] [code UL-R1-BD@51e7e815 PromotionDefinition.java:182-186] | <!--i-->
| 20 | Super Exclusive + a normal promotion on another SKU of the same order (no Exclusive marking) | **both apply** in R1 | contradiction 39 | <!--i-->

Likely defects to test live (code study; report as defects only after a live reproduction): <!--i-->
- **Save As New of a Super Exclusive promotion** loses execution order -2 (stored null) unless Exclusive is also set, so the copy runs in normal order; check `PPMS_EXECUTION_ORDER` of the copy [code UL-R1-BD@51e7e815 PromotionSetupService.java:1831-1838]. <!--i-->
- **Count budgets consumed twice**: a promotion with two resultant (benefit) lines and `SCHCMCOUNT` / `CMCOUNT` = 1 may use the count twice on one order (count budgets are built per resultant line) [code UL-R1-BD@51e7e815 AllocationResolver.java:50-87]. <!--i-->
- **End date stored as midnight**: the date window compares full date-time, so a promotion whose end date is stored as 00:00 may stop applying to orders later on its last day; book an order in the afternoon of the end date [code UL-R1-BD@51e7e815 FrequencyQualifier.java:59-65]. <!--i-->
- **Preview vs save budget**: the up-front budget qualifier is not registered, so a preview / non-S request shows the discount even when the budget is used up, and only the S save gives 0; compare the discount shown before save with the saved Total Offering when the balance is short [code UL-R1-BD@51e7e815 PromotionSection.java:21] [code UL-R1-BD@51e7e815 AllocationResolver.java:57]. <!--i-->
- **Reversal without row lock (SDMS-10155 "budget removing when multi user save")**: the plain revert path does not lock the allocation row; two users editing / cancelling and saving orders on the same DSR budget at the same time can lose an update; afterwards compare `PPAL_ACHIEVED_VALUE` with SUM(`PPAR_ACHIEVED_VALUE`) for that key [code UL-R1-BD@51e7e815 PromotionAllocationRevertService.java:39-61]. Whether SDMS-10155 is fixed in this build: unclear. <!--i-->
- **Missing documentReference**: a request without documentReference gets a random UUID, so the later edit / cancel cannot find the original booking (Utilized stays up after a cancel); check the journal's `PPAR_DOCUMENT_REF` of an order booked from each channel (back office, mobile sync) [code UL-R1-BD@51e7e815 SnDRepositoryFiller.java:292-301]. <!--i-->
- **Mobile-sync allocation without balance check**: `/promotionAllocation/allocate` adds the full value even beyond the balance [code UL-R1-BD@51e7e815 PromotionAllocationService.java:703-719]. <!--i-->

More boundaries: budget amount with 3-4 decimals (rounding 131.4566 / 131.443); budget = amount already spent (allowed) vs 0.01 below (refused); IO number of 9 / 10 / 12 / 13 characters; IO end date = start date (allowed) vs one day earlier; credit note expiry = IO end date vs one day later; Discount Cap example 30% of 200,000 capped at 50,000; Repeat Limit buy 6 get 1, 4 times then the 5th not given [stated doc; boundaries inferred].

Traps (what a green run would not prove)
- Total Offering summing to the header Discount (already a group 11 check) proves nothing about the budget; read Utilized before / after.
- A promotion uploaded and approved does not reach orders until the integrator job runs; a case booked right after approval may wrongly fail (Q-PR3).
- Active Promotions shows no budget figures; never use it for budget checks [stated SZ (F11)].
- Partial returns re-price the remaining basket (middle invoice, Q-SR2), so the give-back may differ from a pro-rata of the returned line.
- Pakistan configuration (Outlet entity only, normal sub type) is not a global rule; BD may differ.
- The L4 map of Current Promotion is suspect (contradiction 34): map the screen again before writing steps against it.
- Shared test environment: creating or changing promotions / budgets changes every order booked afterwards (group 11 amounts are stable only while the promotion masters are unchanged [observed 2026-10-05 G11-2, order_booking.md]); get the QA Team Lead's go-ahead and use dedicated test promotions (Q-PR7).
- (code) A promotion saved or activated a moment ago may not apply yet: allow about 60 s for the cache refresh before booking [code UL-R1-BD@51e7e815 PromotionCacheUpdateService.java:22-39]. <!--i-->
- (code) A discount shown before save is a calculation, not a budget booking; only the S event books (preview vs save) [code UL-R1-BD@51e7e815 AllocationResolver.java:57]. <!--i-->
- (code) When a promotion "does not apply", read the document's event log (`PRM_PM_PEV_PROMO_EVT_LOG`, section 9) before calling it a defect: date window, frequency, exclusivity, budget and GIN-state rules all log a reason. <!--i-->
- (code) Org flags (`ALLOW_PARTIAL_BUDGET`, `PROMOTION_PROMPT`, ...) change the expected result; read them for the org before asserting a budget boundary (Q-PR12). <!--i-->

## 12. Open questions
Filed in OPEN_QUESTIONS.md (2026-10-08):
- Q-PR1: Does an order edit that lowers the discount give budget back? | Default: yes, the edit save re-prices the order and Utilized drops by the difference | Class: B | Evidence: the log's open item; edit re-applies promotions [observed 2026-10-01 G11-1].
- Q-PR2: Are Discount Limit and Discount Cap the same setting? | Default: no: Limit = per sales order, Cap = per customer | Class: C | Evidence: manual s.6-31 describes both.
- Q-PR3: What is the integrator job's schedule on cnr1dev1 and cnr2dev3? | Default: unknown; wait for the next run and re-check Current Promotion before booking | Class: B | Evidence: F15.
- Q-PR4: Does a free-goods promotion also use budget (quantity), or only stock? | Default: stock only, unless Budget Setup shows a QTY budget for it | Class: C | Evidence: Budget Setup has QTY columns [db 2026-09-25 L4].
- Q-PR5: Which promotion features are missing in R1 (cnr1dev1) compared with R2? | Default: assume an R2-only feature is missing in R1 until seen there | Class: B | Evidence: F5; menu differences (section 3).
- Q-PR6: What are Bulk Promo Allocation and Cash Memo Promotion Viewer used for? | Default: out of scope until taught | Class: C | Evidence: mapped screens only.
- Q-PR7: Which test promotions and budgets exist on cnr1dev1 for Pakistan that can be used for a live walk? | Default: read-only walk on the group 11 promotions (Automation2, MARCH001, MARCH002, May001, May003) | Class: B | Evidence: transaction_inquiry.md.
- Q-PR8: Trainer name for the tags | Default: Syed Zulfiqar (taken from the account) | Class: A | Evidence: session log header.
- Q-PR9: What does "Confirmed" mean for free goods (orders read Confirmed right after save when allocated; unallocated ones stay status Order)? | Default: Confirmed = allocated; free goods are allocated together with the order | Class: B | Evidence: F17; contradiction 3 (Confirmed = execution 02 at save) and Q16 / Q27 answers.
- Q-PR10: On a partial return, does Utilized drop by the return's Total Offering (original minus middle invoice) or only by the returned lines' share? | Default: by the return's Total Offering (the middle-invoice difference) | Class: B | Evidence: F22 vs Q-SR2 answer; contradiction 33.

Code study 2026-10-08 (details and evidence in OPEN_QUESTIONS.md sections 1b, 2f, 3, 5): <!--i-->
- Q-PR1 **answered by code - confirm live**: an edit (entry mode E) fully re-prices; the old booking is reversed and the new value booked, so a lower discount gives the difference back (section 6). L46 stays as the live confirmation. <!--i-->
- Q-PR2 code evidence (stays open, class C, trainer to confirm): Discount Limit = per order, never stored; Discount Cap (DISCCAP) = running value budget across orders per hierarchy combination (section 4.7). <!--i-->
- Q-PR3 **answered by code - confirm live**: the promotion service has no integrator cron; `/promotionSetup/upload` is pull-triggered by an unknown caller; the only scheduled job is the 60 s cache refresh. Who calls `/upload` and when: Q-PR16. <!--i-->
- Q-PR4 code evidence (stays open, class C): the header budget of a free-goods promotion is a **quantity** budget booked on the S event [code UL-R1-BD@51e7e815 AllocationResolver.java:55] [code UL-R1-BD@51e7e815 PromotionAllocationService.java:138-145]. <!--i-->
- Q-PR5 **answered by code - confirm live**: the R2-only feature list is `../../sources/code/MS_Promotion/R1_vs_R2.md` section D (summary in section 3); L48 confirms the menus. <!--i-->
- Q-PR6 code evidence (stays open, class C, inferred): Bulk Promo Allocation ~ `POST /promotionAllocation/allocate`; Cash Memo Promotion Viewer ~ `GET /promotionSetup/getPEL` (section 4.2a). <!--i-->
- Q-PR9 / Q-PR10 code evidence: no stock / status check and no proportional give-back in the promotion service (contradictions 37, 38, 33). <!--i-->
- Q-PR11: Which S&D order actions send `cashmemoEvent = S`, and which call `/promotionAllocation/revert`, `/adjust`, `/adjustApproved`, `/compensate` (cancel, edit, return, approval)? | Default: S at order save; revert at cancel; adjust at return approval | Class: B | Evidence: section 6 code rows; check by reading the allocation journal after each action. <!--i-->
- Q-PR12: What are `ALLOW_PARTIAL_BUDGET` and `PROMOTION_PROMPT` for PK (010104) and BD (010105) on cnr1dev1? | Default: N (F21 holds) | Class: B | Evidence: contradiction 36. <!--i-->
- Q-PR13: In R1, does a Super Exclusive promotion block other promotions (manual) or only run first (code)? Also: does a failing Exclusive still block, and does a Save As New copy of a Super Exclusive lose its run-first order? | Default: code behaviour (runs first only) | Class: B | Evidence: contradiction 39. <!--i-->
- Q-PR14: Include + Include OR: is the discount on both selections' products even when one selection is below its threshold? | Default: code behaviour (both) | Class: B | Evidence: contradiction 35. <!--i-->
- Q-PR15: What does "Apply" do on Promotion Layout, and where does the State "allocated" come from (the service only knows Active / Inactive)? | Default: Apply = save with Active; "allocated" not asserted | Class: B | Evidence: contradiction 40. <!--i-->
- Q-PR16: Where do the Budget Setup upload validations, the Current Promotion Approver approval and the integrator trigger live (target-service, workflow service, UI, scheduler)? | Default: assert only observed messages there | Class: C (1b, dev / trainer) | Evidence: contradiction 42; section 4.8. <!--i-->
- Q-PR17: Which setting implements the manual's **Repeat Limit** (no such setting in R1 code; slab Repeat has no maximum; Purchase Limit can cap the bundle count)? | Default: do not assert a Repeat Limit | Class: C (1b, trainer) | Evidence: contradiction 41. <!--i-->

## 13. Sources
- Session log: `../learning_sessions/2026-10-07_SND-GLOBAL_SyedZulfiqar_log.md` (F1-F23, verbal; method A + B).
- QA-team write-up: `../learning_sessions/2026-10-08_SND_Promotions_and_Budget_QA_Team.docx` (verbal facts + manual digest with slide ranges, 11 test cases, 7 open questions).
- Manual: "Promotions and Budgets 2026_R2.pptx" (51 slides, July 2026, market Pakistan, R2) **not in the workspace** (source gap; planned `apps/snd/knowledge/sources/20261007_Promotions and Budgets 2026_R2.pptx`).
- Menu harvest: `apps/snd/knowledge/env/cnr1dev1/menu.KPO_mp.json`, `apps/snd/knowledge/env/cnr2dev3/menu.KPO_slv.json` (2026-09-25).
- L4 screen map (sweep cnr2dev3 2026-09-25): `apps/snd/knowledge/screens_observed/{DT_PROMOTION, CURRENT_PROMOTION_APPROVER, ACTIVE_PROMOTIONS, BULK_PROMO_ALLOCATION, CASH_MEMO_PROMOTION_VIEWER, BUDGET_LAYOUT, CREDIT_NOTE_APPROVAL, OFF_INVOICE_CREDIT}.json`.
- Order-side evidence: `../order_to_delivery_planning/transaction_inquiry.md` (Total Offering, group 11 walks).
- Source code (method D, 2026-10-08): MS_Promotion branch UL-R1-BD @ 51e7e815 (1.1.109.0) and UL-R2-COUNTRY @ 462cb561 (2.3.102.0), repository `scm/git/MS_Promotion`, read-only; studies `../../sources/code/MS_Promotion/README.md`, `R1_engine.md`, `R1_budget_api.md`, `R1_vs_R2.md`; report `../learning_sessions/2026-10-08_SND-GLOBAL_code_MS_Promotion_report.md`. <!--i-->
