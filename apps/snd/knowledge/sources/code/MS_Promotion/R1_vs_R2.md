# MS_Promotion: R1 (UL-R1-BD) vs R2 (UL-R2-COUNTRY) feature comparison

Read-only code study for QA business training. Written 2026-10-08.

## Sources and conventions

| Side | Branch | Commit | Env | Export |
|---|---|---|---|---|
| R1 (Pakistan + Bangladesh) | UL-R1-BD | 51e7e815 (2026-10-06) | cnr1dev1 | scratchpad/ms_UL-R1-BD |
| R2 (Unilever R2 countries: TH/PH/VN/MY are named in commits) | UL-R2-COUNTRY | 462cb561 (2026-10-06) | cnr2dev3 | scratchpad/ms_UL-R2-COUNTRY |

- Tag format: `[code <branch>@<commit> <path>]`. Paths are relative to `PromotionBuilder/src/main/java/com/centegy/`. Resource paths start with `resources/`, meaning `PromotionBuilder/src/main/resources/`.
- `R1@` means `UL-R1-BD@51e7e815`. `R2@` means `UL-R2-COUNTRY@462cb561`.
- Method: `diff -r` of the two exports (jar, gradle, version.txt and .source ignored), and `git log` between `origin/UL-R1-BD` and `origin/UL-R2-COUNTRY` (merge-base 4d7e066d, 2026-05-15).
- Scale of the difference: 130 differing paths. R2 has 38 extra files and R1 has 2 extra files. PromotionSetupService is 2297 lines in R1 and 4200 lines in R2.
- Neither export has `.sql` files, Excel templates or a separate mobile-sync module, so there is no SQL or template difference to report. The Excel "column name/sequence" upload check exists on both sides.
- **Caveat on ticket ids:** the two branches merge into each other ("Merged from R1", "Merge PK-BD into R2-Country", "Back Porting from R2"). Since the merge-base, R2 has 432 non-version commits that R1 does not have, and many of them date from 2025. Linking a ticket to a feature below is therefore based on the commit subject and the files it touched. It does not prove that the whole ticket is absent from R1. The code diff is the authority.
- Version strings: R1 is `1.1.109.0` and R2 is `2.3.102.0` [code R1@ resources/version.txt] [code R2@ resources/version.txt].

---

## A. Features R2 has and R1 does not

### A1. Promotion lifecycle states (New / Ready / Active / Inactive / Expired)
- **R1 has:** only the Active flag (`PPMS_ACTIVE` A/I). It has no state column [code R1@ promotion/domain/entities/PromotionSetup.java].
- **R2 has:**
  - A `PPMS_STATE` column [code R2@ promotion/domain/entities/PromotionSetup.java].
  - A promotion can be activated only from NEW, READY or ACTIVE. Otherwise the message is "Status cannot be modified at this state: {0}" (`status.notbe.modified`).
  - Changing Active to Inactive sets the state to INACTIVE [code R2@ promotion/domain/services/PromotionSetupService.java upsertPromotionSetup].
  - The `/updateStateToExpired` endpoint marks active promotions whose end date has passed as EXPIRED [code R2@ promotion/rest/controllers/PromotionSetupController.java] [code R2@ promotion/domain/dao/PromotionSetupRepository.java updateStateToExpired].
  - An integration upload can set INACTIVE only while the promotion is NEW or READY [code R2@ promotion/domain/services/PromotionETLService.java updatePromoProperties].
- **Difference:** the whole state model is R2-only.
- **Tickets:** SDMS-3050 ("Additional statuses for promotions - New, Ready & Expired"), SDMS-5533, SDMS-7590, SDMS-7888.

### A2. Activate Promotion screen (bulk status update) and pre-activation validation
- **R1 has:** nothing equivalent.
- **R2 has:**
  - `POST /promotionSetup/updatePromoStatus` takes `code~status,...` [code R2@ promotion/rest/controllers/PromotionSetupController.java].
  - Per-code messages: "Promotion not found", "Promotion already active in the system" and "... status has been updated successfully".
  - `validatePromotionBeforeStatusUpdate` checks:
    - the header: Promotion Name, Start and End Date, Sub Type, Entity Type, Status, Claimable, Claimable Percentage, and "End Date should be greater than Start Date";
    - the budget: "Budget Id is required when Budget Level ...", "No budget found for the given Budget Id and Budget Level";
    - qualify and criteria items exist ("... Code is required", "Comparison Operator is required", "Value is required");
    - the Resultant section has at least one item;
    - enrichment rules.

    [code R2@ promotion/domain/services/PromotionSetupService.java validatePromotionBeforeStatusUpdate, promotionHeaderValidation, promotionBudgetValidation]
  - The same validation runs when the layout is saved with Active=A. A failure gives "Promotion failed with the following error {0}" (`promo.save.error`) [code R2@ resources/messages.properties].
  - `GET /getFutureInactive` lists future and inactive promotions [code R2@ promotion/rest/controllers/PromotionSetupController.java].
- **Tickets:** SDMS-7148 (Bulk Update Promotion Status to Active), SDMS-7492, SDMS-9697.

### A3. Customer Discount (distributor-level promotion) screens and approval
- **R1 has:** no staging tables, no controllers and no `promoSecType` "CD" logic.
- **R2 has:**
  - Table `PRM_PM_STD_STAGING_TABLE_DT` with distributor, promotion code, dates, slab unit, repo, from/to, get type, and product level/analysis/code/UOM [code R2@ promotion/domain/entities/PromotionStgBEntityLevel.java].
  - Slab detail table `PRM_PM_SPD_STAGING_TABLE_DTL` [code R2@ promotion/domain/entities/PromotionStgBEntitySlab.java].
  - Endpoints `/promotionStaging/be/distAll`, `/distApproval` and `/distApprovalL1` [code R2@ promotion/rest/controllers/PromotionStgBEntityLevelController.java].
  - Approval lists are limited to the user's locations (`smm_pr_usl_userlocation`).
  - Two-level approval through feature `MULTI_APPROVAL`: status INPROCESS1 goes to INPROCESS [code R2@ promotion/domain/services/PromotionStgBEntityLevelService.java].
  - A promotion that carries a distributor code (`EPP1_BUSENT_PHS_LVL1_CODE` / `entityLevel1Code`) qualifies only for orders of that distributor [code R2@ promotion/execution/beans/components/qualifiers/BusinessQualifier.java].
  - CD and TPR promotions are kept out of the general cache and are indexed through the exclude/include entity table instead [code R2@ promotion/domain/dao/PromotionSetupRepository.java] [code R2@ promotion/domain/services/PromotionETLService.java].
  - A free product is blocked for CD on sales return without reference (cash-memo type 16) [code R2@ promotion/execution/beans/components/resolvers/BusinessResolver.java].
  - Feature `MULTI_SLAB_VIEW` adds a "View Details" option for multi-slab CD rows [code R2@ promotion/domain/services/PromotionSetupService.java getPromoConfigUI].
- **Tickets:** SDMS-2928 ([TH] Customer Discount creation), SDMS-4336, 4363, 4540, 4589, 4733, 4930, 6324, 6733, SDMS-9157 ([VN] two-level approval), SDMS-10052 (multi-slab), SDMS-11959, SDMS-12076.

### A4. Distributor Markup (charges) screens, approval, and SKU-level markup
- **R1 has:** none of this. `ChargesSetup` and the staging-charges entities are absent.
- **R2 has:**
  - Table `PRM_PM_SDC_STAGING_DT_CHARGS` with `PSDC_PPA1_LEVEL/CODE` (product-analysis level) and `PSDC_MARKUP_TYPE` [code R2@ promotion/domain/entities/PromotionStgBEntityCharges.java].
  - Endpoints `/promotionStaging/dm/{distAll,distApproval,updateEndDate}` and `/promotionStaging/dmud/...`. The "dmud" variant is used when the charge's `PCHS_CHARGES_IMPACT = 'D'` [code R2@ promotion/rest/controllers/PromotionStgBEntityChargesController.java, PromotionStaging1ChargesController.java] [code R2@ promotion/domain/services/PromotionSetupService.java updateEndDate].
  - Charges master `GLB_PR_CHS_CHARGES_SETUP` [code R2@ promotion/domain/entities/ChargesSetup.java].
  - End-date edit messages include "End date should be Equal / greater than current date", "End date could not be less than start date" and an overlap check [code R2@ promotion/domain/services/PromotionStgBEntityChargesService.java].
- **Unclear:** whether "dmud" means markdown, or "markup up/down". A `MARKDOWN("0010")` sub-type exists in R2 but is commented out [code R2@ promotion/execution/beans/components/PromotionHeader.java].
- **Tickets:** SDMS-5436, 5492, 5518, 4897, SDMS-10750 (price change rights on SKU level per DT), SDMS-10979, SDMS-11556.

### A5. TPR (HQ-level price reduction) list and end-date edit
- **R1 has:** no.
- **R2 has:**
  - Table `PRM_PM_STH_STAGING_TABLE_HQ` and `POST /promotionStaging/ho/updateEndDate` [code R2@ promotion/domain/entities/PromotionStgOrgaLevel.java] [code R2@ promotion/rest/controllers/PromotionStgOrgaLevelController.java].
  - Upload of TPR promotions writes product include rows [code R2@ promotion/domain/services/PromotionETLService.java].
- **Tickets:** SDMS-2944 (TPR), SDMS-7410, SDMS-7619 / 7666 (edit TPR end date), SDMS-8297.

### A6. Current Promotion screen extensions (end-date edit, original end date, N-day look-ahead, filters)
- **R1 has:** the current-promotion lister with code, description and date filters [code R1@ promotion/domain/services/PromotionSetupService.java].
- **R2 has:**
  - `PPMS_ORIGINAL_END_DATE`, plus filters on originalEndDate, referenceCode, promoSecType and projectCode (IO number).
  - Look-ahead window set by `FUTURE_PROMO_DAYS` (default 7).
  - Budget hierarchy that includes `GEOAD01` (ORGA~GEOAD01~DIST) [code R2@ promotion/domain/services/PromotionSetupService.java getDateByConfig, getCurrentPromotion].
  - `GET /distAllede` and `POST /updateEndDate`. The end date can only be reduced, with the message "End date could not be increased from approved End date..." [code R2@ promotion/domain/services/PromotionSetupService.java updateEndDate].
- **Tickets:** SDMS-3374 / 3412 (original end date), SDMS-4577 (seven-day visibility), SDMS-5688, 5714, 5727, 5496.

### A7. Promotion user access control (create / update / copy rights)
- **R1 has:** no.
- **R2 has:**
  - Table `PRM_PM_ACP_ACCES_CNTRL_PROM` (PACP_CREATE / UPDATE / COPY per user) and `GET /promotionUserAccessControl/getPromotionSetupUserPrivileges` [code R2@ promotion/domain/entities/PromotionUserAccessControl.java] [code R2@ promotion/rest/controllers/PromotionUserAccessControlController.java].
  - Messages "User not allowed to create / update / copy promotion" [code R2@ resources/messages.properties].
  - Copy and save is also gated by feature `PROMO_COPY_IS_ALLOW`, with the message "You are not allowed to copy and save the promotion..." [code R2@ promotion/rest/controllers/PromotionSetupController.java saveAsNew].
- **Tickets:** SDMS-3165 (control access list of promotion layout), SDMS-7159 (copy promotion).

### A8. Layout freeze by section type
- **R1 has:** the layout is frozen (EntryMode F) only when the start date is today or earlier [code R1@ promotion/rest/controllers/PromotionSetupController.java getPromoByID].
- **R2 has:** the same rule, plus a freeze for any promotion whose `promoSecType` is listed in feature `PROMO_FREEZABLE_SEC_TYPE` [code R2@ promotion/rest/controllers/PromotionSetupController.java getPromoByID].
- **Ticket:** commit 2025-08-15 "Freeze promotion based on Sec Type configuration".

### A9. Promotion mechanics header fields (Deal type, Budget level code, Sales org, Final allocation date, Capping target)
- **R1 has:** budget level and budget value, project code, check-budget flag and sec type [code R1@ promotion/domain/entities/PromotionSetup.java].
- **R2 has:**
  - New columns `PPMS_DEAL_TYPE`, `PPMS_BUDGET_LEVEL_CODE`, `PPMS_SALES_ORGANIZATION`, `PPMS_CAPPING_TARGET_ID`, `PPMS_SOURCE` and `PPMS_REFERENCE_CODE`, and a transient final-allocation date [code R2@ promotion/domain/entities/PromotionSetup.java].
  - The temp/upload header adds `PTSH_BUDGET_CONTROL_LEVEL`, `PTSH_EXECUTION_LEVEL`, `PTSH_CLOSING_DATE`, `PTSH_BSA` and others [code R2@ promotion/domain/entities/TempPromotionHead.java].
- **Tickets:** SDMS-9161 (Define Promotion Mechanics in "Promotion Layout"), commit 2025-12-08 "target capping id ... in promotion setup header".

### A10. Budget: two-level budget hierarchy, value budget for free SKU, bottom-up, final allocation date
- **R1 has:**
  - One ORGA budget row per promotion. The quantity columns are sent only when `BUDGET_QTY_VISIBILITY` = Y.
  - Loyalty B2B promotions get an unconstrained ORGA budget (see B1) [code R1@ promotion/domain/services/TargetMasterService.java createsBudgetHeadBasedOnPromotion].
- **R2 has:**
  - Up to 2 budget rows, built from `budgetLevel` and `budgetLevelCode` split on "~" (for example a region budget, then region~dist).
  - `TTCD_PRICE` is sent with the budget.
  - When check-budget = N, the hierarchy comes from feature `BUDGET/TGT_HIER_COMBINATION` (default DIST) with BOTTOM_UP=H. Otherwise `BUDGET/BOTTOM_UP_VAL` applies.
  - `FINAL_ALLOCATION_DATE` is sent [code R2@ promotion/domain/services/TargetMasterService.java getFilledBudgetRow, getLevel1BudgetRow, getLevel2BudgetRow].
  - Target dates, active flag and budget are pushed back to the target service when the promotion changes (`updateTargetBasedOnPromotion`).
  - A budget increase through upload is accepted only if it is at least the allocated value: "Budget value should be greater than to allocated budget value" [code R2@ promotion/domain/services/PromotionETLService.java updateBudgetBasedOnPromotion].
  - The allocation date is validated against finalAllocationDate (commit 2026-06-23).
  - Budget required check: "Budget should be defined when budget is required." (`budget.is.required`) [code R2@ resources/messages.properties].
- **Tickets:** SDMS-9073 ([VN] budget allocation / reallocation), SDMS-9436, 9813, 9902, 9941, 10274, 10456, 10527, 11302 (budget type H), SDMS-8613.

### A11. Free-product resultant in amount (budget type V), price strategy (PP / TP / CP), stock type, configurable UOM
- **R1 has:** free-product budget by quantity only. The resultant has no price or budget-type fields [code R1@ promotion/execution/beans/components/controls/ResolvablePromotionItem.java].
- **R2 has:**
  - New resultant fields: `budgetType` (Q/V), `price`, `priceStrategy`, `stockType` (SON/FRE) and `sequence` [code R2@ promotion/execution/loader/PromotionDefinitionDeserializer.java].
  - Matching temp columns `PTSR_/PTSS_BUDGET_TYPE`, `_PRICE` and `_STOCK_TYPE` [code R2@ promotion/domain/entities/TempPromotionResultant.java, TempPromotionSlab.java].
  - With budget type V, the price is taken from the distributor purchase price (PP) or the trade price (TP, `SND_PR_DSP_DIST_SALE_PRICE` / `SND_PR_GSP_GLOBAL_SALE_PRICE`). If no price is found, the promotion is not applied ("Business resolver failed, price not found") [code R2@ promotion/execution/beans/components/resolvers/BusinessResolver.java].
  - The budget is consumed as quantity × price, so the allocated free quantity is rounded down to whole units [code R2@ promotion/domain/services/PromotionAllocationService.java findAndMerged] [code R2@ promotion/execution/beans/components/domain/PromotionBudget.java hasFreeProductAmountBudget].
  - The allocation reference stores `PPAR_PRICE` and `PPAR_FOC_UOM` [code R2@ promotion/domain/entities/PromotionAllocationReference.java].
  - Default price strategy comes from feature `CASHMEMO/FREE_PROD_SCHEME_UTILIZE_PRICE_TYPE` (default CP) [code R2@ promotion/domain/entities/TempPromotionSlab.java].
- **Tickets:** commit 2025-05-20 "free sku scheme budget in amount CR", SDMS-10525, SDMS-10562 (Resultant Product UOM configurable), SDMS-11266, SDMS-11606 (NUTI promotions use Purchase Price), SDMS-9612, ADMS-2039.

### A12. Multi-variant free product
- **R1 has:** 1 free product per resultant. No variant limit is exposed.
- **R2 has:**
  - `GET /getPromoConfigUI` returns `ProdVariantLimit` from feature `MULTI_VARIANT` (default 1, VN = 5 according to the code comment) [code R2@ promotion/domain/services/PromotionSetupService.java getPromoConfigUI].
  - The resultant product level is "M" when there are several variants [code R2@ promotion/execution/beans/components/controls/ResolvablePromotionItem.java isMultiVariant].
  - On return, the product price is taken from the last allocation reference.
- **Tickets:** SDMS-9166, SDMS-9858 (Product Variant switch), SDMS-10535.

### A13. Coupon versions 1.0 / 2.0 / 3.0 (TH/PH Coupon promotions)
- **R1 has:** the same coupon resolver, but its "version 1" trigger value is `CouponVer = "LTYB2B"` (see B1). No 1.0, 2.0 or 3.0 values exist [code R1@ promotion/annotation/enums/ExecutionPolicy.java].
- **R2 has:**
  - `COPOUNVERSION1("1.0")`, `COPOUNVERSION2("2.0")` and `COPOUNVERSION3("3.0")` [code R2@ promotion/annotation/enums/ExecutionPolicy.java].
  - Version 1.0 builds a "Discount on Gross" resultant from the external scheme value. Version 2.0 is a no-op branch [code R2@ promotion/execution/beans/components/resolvers/CouponResolver.java].
  - Upload accepts COUPON 1.0 / 3.0 without the normal qualifier validation, and skips 4.0 rows in status I [code R2@ promotion/domain/services/PromotionSetupService.java upload].
  - The exclusion qualifier is skipped for coupon 1.0 [code R2@ promotion/execution/beans/components/qualifiers/ExclusionQualifier.java].
- **Tickets:** SDMS-4374 (Coupon 1.0 in DCODE - SaleReturn), 4998, 6512, 11728, commit 2025-11-24 "Handling Coupon Version 3.0 in upload".

### A14. Integration / SFTP promotion creation (upload from staging header tables), export, and enrichment
- **R1 has:**
  - `GET /promotionSetup/upload` turns `TempPromotionHead` rows into promotions. It deletes and recreates any existing code.
  - The temp header has 23 columns: no coupon version, claimable, IO number, state, deal type, alt name or sub type.
  - Claimable is hard-coded to Y and 100% [code R1@ promotion/rest/controllers/PromotionSetupController.java upload] [code R1@ promotion/domain/entities/TempPromotionHead.java] [code R1@ promotion/domain/services/PromotionETLService.java].
- **R2 has:**
  - Upload keyed on a reference code: a promotion already present (`PPMS_REFERENCE_CODE`) is skipped, not overwritten.
  - Duplicate-safe numbering.
  - Header fields CouponVer, Claimable, Claimperc, IO (OPSO) id and value, sec type, sub type, alt name, state, deal type, budget level code, sales org and final allocation date.
  - Slab from/to kept as 2-decimal values.
  - Validation messages "... Resultant section should have at least one item", "... should have a Qualify section".
  - Per-row status written back to the temp header ("Promotion code has uploaded successfully" or "...failed with error").

    [code R2@ promotion/domain/services/PromotionSetupService.java upload, validationPromo] [code R2@ promotion/domain/services/PromotionETLService.java upload, validateDuplicationAndSave]
  - `GET /promotionSetup/updatePromoProperties` updates end date, state and budget of already-created promotions and returns Total / Success / Fail counts [code R2@ promotion/rest/controllers/PromotionSetupController.java].
  - `GET /promotionTemp/exportPromotions` (repository "NutiExport") and a paged temp-header lister [code R2@ promotion/rest/controllers/TempPromotionHeadController.java] [code R2@ promotion/domain/services/TempPromotionHeadService.java].
  - Enrichment table `PRM_PM_TPE_TMP_PROM_ENRCHMNT` (per section and repo: enable / modify / remove) controls which fields a user may edit on an uploaded promotion. It is active when `PROMO_ENRICHMENT_ALLD` = Y and the source equals `PROMO_ENRICHMENT_SRC` [code R2@ promotion/domain/entities/TempPromotionEnrichment.java] [code R2@ promotion/domain/services/PromotionETLService.java].
- **Tickets:** SDMS-10021 / SDMS-10207 (SFTP Promotion Creation screen), SDMS-4816 (enrichment), SDMS-3427 / 3411 (TPM promotions), SDMS-6409, 7264, 11389, 10545.

### A15. Promotion sequencing (SEQ1 / SEQ2 / SEQ3) and exclusive ordering
- **R1 has:**
  - On save, super-exclusive sets execution order -2 and exclusive sets -1 [code R1@ promotion/domain/services/PromotionSetupService.java upsertPromotionSetup, lines ~1107-1112].
  - Execution order is `executionOrder`, then group sequence, then sub-sequence [code R1@ promotion/domain/dao/PromotionSetupRepository.java].
  - The super-exclusive short-circuit in the executor is commented out [code R1@ promotion/execution/PromotionExecutor.java] (commit 5a86607c "super exclusion code removed").
- **R2 has:**
  - The -2 / -1 marking is commented out.
  - Order is group sequence, then sub-sequence, then executionOrder, in the query and again in the executor [code R2@ promotion/domain/dao/PromotionSetupRepository.java] [code R2@ promotion/execution/PromotionExecutor.java].
  - The promotion type group list is sorted by sequence [code R2@ promotion/domain/dao/PromotionTypeGroupRepository.java].
- **Difference:** in R1, exclusive and super-exclusive promotions run first regardless of sequence. In R2, sequence wins. This changes which promotion applies first; worth a test on cnr1dev1.
- **Tickets:** SDMS-8038 (Promo Sequencing not working accurately in R2), SDMS-4442, 5571, 6882, 6897, 6917, commit 2025-08-22 "unmarking the execution order for exclusive / unexclusive".

### A16. Exclusion scoped per sub-type, and GROSSAMT exclusion
- **R1 has:** exclusion only for SCHNORMAL, using a single exclusion flag per product [code R1@ promotion/execution/beans/components/qualifiers/ExclusionQualifier.java].
- **R2 has:**
  - Exclusion for SCHNORMAL and SCHCHARGE, with the flag kept per sub-type (`<subtype>-EXCL`). A charge (markup) exclusive no longer blocks normal schemes, and normal exclusives no longer block charges.
  - Gross-amount (GROSSAMT) exclusion.
  - Skipped for coupon 1.0.

  [code R2@ promotion/execution/beans/components/qualifiers/ExclusionQualifier.java]
- **Tickets:** SDMS-4897 (markup created with super exclusive), SDMS-11701.

### A17. "For every" percentage calculation
- **R1 has:** a percentage discount applies once to the qualifying amount.
- **R2 has:** when feature `FOR_EVERY_PERC_CALC` = Y, a percentage resultant with a for-every factor is multiplied per bucket or per factor [code R2@ promotion/execution/beans/components/controls/ResolvablePromotionItem.java ForEveryPercentageCalculation] [code R2@ promotion/domain/services/PromotionSetupService.java].
- **Ticket:** SDMS-8201 (for-every wrong for range slab). The other tickets are unclear.

### A18. New criteria: outlet segments, outlet rank, outlet type in getActivePromos
- **R1 has:** OUTTYPE in one place only. No `segments` and no `OUTLETRANK` [code R1@ promotion/execution/fillers/domains/snd/SnDRepositoryFiller.java].
- **R2 has:**
  - `segments` (multi-value, "^|~|^"), OUTTYPE, OUTLETRANK and VALATTRIB03/04/08 are filled for execution and for active-promotion lookups.
  - Multi-value criteria matching supports `=` and `!=` against lists [code R2@ promotion/execution/fillers/domains/snd/SnDRepositoryFiller.java] [code R2@ promotion/domain/services/PromotionSetupService.java fillEntityAttributes] [code R2@ promotion/execution/beans/components/controls/QualifyingPromotionItem.java].
- **Tickets:** SDMS-4003 (promotion not applying when segment in criteria), SDMS-7453 (Outlet Type criteria).

### A19. IO Number / claimable rules
- **R1 has:**
  - The check runs only if `CHECK_PROJECT_CODE` = Y and the promotion is active.
  - Message: "Project Code not found, EITHER update the project code OR save with INACTIVE status." [code R1@ resources/messages.properties] [code R1@ promotion/domain/services/PromotionSetupService.java validateProjectCodeforClaimablePromo].
- **R2 has:**
  - Claimable with an empty IO number always fails, even without the DB check.
  - Message: "IO Number is mandatory when promotion is claimable." The older text is reworded to "IO Number not found...".
  - Also adds "End date could not be less than Start date." [code R2@ resources/messages.properties] [code R2@ promotion/domain/services/PromotionSetupService.java].
- **Tickets:** SDMS-4072, SDMS-8151, commit 2025-12-15 "IONumber change".

### A20. Budget revert and partial-budget adjustment
- **R1 has:**
  - Revert is called inside the individual resolvers, and coupon revert happens on edit (SDMS-12374) [code R1@ promotion/execution/beans/components/resolvers/CouponResolver.java].
  - Partial budget applies to all resultant types when enabled.
- **R2 has:**
  - A dedicated `RevertResolver` (runs last) that reverts the budget whenever a resultant is not validated [code R2@ promotion/execution/beans/components/resolvers/RevertResolver.java].
  - Partial budget applies only to percentage resultants or free-product-amount budgets.
  - When one budget is partially applied, the other budgets are adjusted down to match [code R2@ promotion/execution/beans/components/domain/PromotionBudget.java getPartialBudgetFlag] [code R2@ promotion/execution/beans/components/resolvers/AllocationResolver.java].
  - `/adjust` and `/adjustApproved` write event-log rows ADJUST and ADJUST-APV [code R2@ promotion/rest/controllers/PromotionAllocationController.java].
- **Tickets:** SDMS-6043, 9393, 9418, 10781, 11605, commit 2025-09-04 "coupon should revert from revert resolver".

### A21. Product / outlet-indexed loading of promotions (performance) and validation at activation
- **R1 has:** all active schemes are loaded from cache.
- **R2 has:**
  - With `PROMO_ALLOW_VALIDATE` = Y, single-box product or outlet qualifiers are written to the include table (`cacheCheck` = Y) and loaded per order product or outlet instead of from cache.
  - Only promotions with end date after today are loaded [code R2@ promotion/domain/services/PromotionStatusUpdateService.java] [code R2@ promotion/execution/PromotionExecutor.java] [code R2@ promotion/domain/dao/PromotionSetupRepository.java].
- **Business effect:** none intended. This is a performance feature, but it can make a promotion "not apply" if the index is wrong (see the SDMS-9524 / 10762 bug history).
- **Tickets:** SDMS-9427, 9490, 9524, 10762 ("TH Scheme optimization").

### A22. Event log / transaction inquiry enrichments
- **R1 has:** basic event log.
- **R2 has:**
  - Distributor column on the event log (`EPP1_BUSENT_PHS_LVL1_CODE`) [code R2@ promotion/domain/entities/PromotionEventLog.java].
  - Applied-promotion message "Promotion Applied! value=..., baseAmount=..." with qualifiers, and per-stage timings [code R2@ promotion/execution/PromotionExecutor.java].
- **Tickets:** SDMS-8277 (Distributor column missing in Promo Evt log), commit 2026-10-02 "Promotion-Qualifiers in EvtLog".

### A23. Smaller R2-only endpoints and behaviour
- `GET /getActivePromosCodes` returns active codes for a list of outlets. `getActivePromos` accepts a list of outlets [code R2@ promotion/rest/controllers/PromotionSetupController.java]. Mobile and DMS sync usage is **unclear** from this service alone.
- Cache inspection endpoints: `getCountOfPromotionInHeaderCacheOrgaWise`, `...DetailCache...` and `getPromotionInCache` [code R2@ promotion/rest/controllers/PromotionSetupController.java]. These are technical.
- `/getByRepoCode` and `/getByRepoValue` are commented out in R2 but live in R1 [code R1@ promotion/rest/controllers/PromotionSetupController.java].
- Custom-tag grid supports section-specific extra query filters (`PCGM_QEI`, `PCGM_QEI_MODE`), so qualify, criteria and resultant pickers can show different value lists [code R2@ formulaebuilder/domain/services/CustomTagService.java] [code R2@ promotion/domain/entities/CustomTagGroupTypeMapping.java]. Ticket: unclear (maybe Non-UL Free Products check, commits 2025-12-22).
- Business qualifier "include / exclude promo types" for sale return without reference:
  - R1 matches the payload list against the promotion **sub-type** [code R1@ promotion/execution/beans/components/qualifiers/BusinessQualifier.java] (SDMS-8826 back-port b4b24c80).
  - R2 matches it against the **sec type** (e.g. CD) [code R2@ same file].
  - The same payload can therefore filter differently on the two systems.

---

## B. Features R1 has and R2 does not

### B1. Loyalty B2B promotion (PK-R1 CR)
- **R1 has:**
  - `CouponVer = "LTYB2B"` marks a Loyalty B2B promotion. It is executed like an external coupon scheme ("Discount on Gross" from `externalScheme.originalValue`).
  - Business qualifier, section qualifier, business resolver and post-promo resolver are skipped for it.
  - On save: promoSecType = LTYB2B, checkBudget = N, budgetValue = 999,999,999,999. The budget is auto-created at ORGA level and the budget hierarchy has DIST appended at run time.
  - Product payload items are used when the promotion has no nested products.

  [code R1@ promotion/annotation/enums/ExecutionPolicy.java] [code R1@ promotion/domain/services/PromotionSetupService.java upsertPromotionSetup ~1095-1101] [code R1@ promotion/domain/services/TargetMasterService.java] [code R1@ promotion/execution/beans/components/domain/PromotionBudget.java] [code R1@ promotion/execution/beans/components/resolvers/CouponResolver.java] [code R1@ promotion/execution/beans/components/controls/ResolvablePromotionItem.java getPayloadItemList]
- **R2 has:** the same enum slot, but its value is "1.0". There is no LTYB2B handling.
- **Tickets:** SDMS-12111 (6bacd037, 79ff29ae, 05969891, 6a53c477), SDMS-12374 (e2f39d7e: revert budgets when an LTYB2B / coupon order is edited).
- **Note:** VN has its own "B2B Loyalty Promotion" ticket SDMS-9162 in R2. Whether it is the same business concept is **unclear**.

### B2. Budget quantity columns switch
- **R1 has:** feature `BUDGET_QTY_VISIBILITY` (group BUDGET). The quantity budget columns are created only when it is Y [code R1@ promotion/domain/services/TargetMasterService.java].
- **R2 has:** the quantity columns are always sent [code R2@ same file].

### B3. Exclusive / super-exclusive run first
- See A15. R1 still forces exclusive promotions to the front on save.

### B4. Charge / tax sub-type breakup sign
- **R1 has:** in order breakup, sub-types with apply type "add" (SCHCHARGE, SCHTAX) get a negative child value [code R1@ promotion/execution/beans/components/resolvers/BreakupResolver.java ~line 192].
- **R2 has:** this inversion removed.
- **Business impact:** unclear.

### B5. Dead code only in R1
- `getActiveLoyals` (loyalty export) exists in the R1 service but no controller calls it [code R1@ promotion/domain/services/PromotionSetupService.java ~716]. Not a user feature.
- `AllocationQualifier` in R1 has a full budget pre-check but is not registered in `PromotionSection` (it is commented out). R2 registers a stub that always returns TRUE [code R1@ / R2@ promotion/execution/beans/components/PromotionSection.java, qualifiers/AllocationQualifier.java]. **Net effect: probably the same on both. Unclear.**

---

## C. Same on both (no business difference found)
- Promotion types, business types and budget types enums (SCHCMCOUNT, DISCCAP, CMCOUNT, BUDDISCCAP). `MARKDOWN` is commented out in R2 only.
- Custom-tag Excel download / upload and promotion-description Excel download / upload (same endpoints, same "Sheet Altered..." message).
- Scheduler: only the 60-second cache refresh (`PromotionCacheUpdateService`) on both.
- No SQL scripts in either export.
- Config differences are environment-only: server port (8094 vs 8082) and SSO URL [code R1@/R2@ resources/application-common.properties].

---

## D. Features in the R2 user manual likely missing on cnr1dev1

Each item below follows from the code diff above. Confirm each one against the live cnr1dev1 menus before you rely on it.

1. **Customer Discount** screens (DT user create, list, approval), including two-level approval and multi-slab "View Details". (A3)
2. **Distributor Markup** screens and approval, including SKU / product-analysis-level markup and the "dmud" variant. (A4)
3. **TPR** (HQ trade price reduction) list and **edit TPR end date**. (A5)
4. **Promotion states** New / Ready / Active / Inactive / Expired, the **Activate Promotion** (bulk status) screen, and the Future/Inactive list. (A1, A2)
5. **Current Promotion end-date edit**, the **Original End Date** column, and the 7-day look-ahead. (A6)
6. **Promotion Layout user rights** (create / update / copy) and the **Copy & Save** on/off switch. (A7)
7. **Promotion Mechanics** header fields: Deal Type, Budget Level Code (two-level / region budget), Sales Org and Final Allocation Date. (A9, A10)
8. **Free-product budget in amount** with Price Strategy (Purchase / Trade / Current price), Stock Type and configurable free-product UOM. (A11)
9. **Multi-variant free products** (more than one free SKU per resultant). (A12)
10. **Coupon 1.0 / 2.0 / 3.0** promotion versions. On R1 the coupon slot is used for Loyalty B2B instead. (A13, B1)
11. **SFTP / integration promotion creation screen**, promotion export, **enrichment** (lock or unlock fields on uploaded promotions), and the update-promotion-properties upload. (A14)
12. **Outlet Segment / Outlet Rank** criteria. (A18)
13. **Promotion Sequence (SEQ1/2/3)** taking priority over the Exclusive flag. In the R2 manual, an exclusive promotion does not jump the sequence; on R1 it does. (A15)
14. **"For every" percentage** discount behaviour (feature-flagged). (A17)
15. The message "IO Number is mandatory when promotion is claimable" and IO-number wording in general. R1 still says "Project Code". (A19)

R1-specific behaviour that an R2 manual will not describe: Loyalty B2B (LTYB2B) promotions and their auto-created unconstrained budget (B1), the `BUDGET_QTY_VISIBILITY` switch (B2), and exclusive-first ordering (B3).

## E. Open / unclear items
- What "dmud" stands for, and which UI menu it maps to (A4).
- Whether R2's VN "B2B Loyalty" (SDMS-9162) and R1's LTYB2B are the same business concept (B1).
- The business impact of the R1-only negative sign for charge / tax breakup (B4).
- Which client (mobile, DMS or SFTP) calls `getActivePromosCodes` and `exportPromotions` (A23, A14).
- Feature flags are read per organisation from the DB. Even where the code exists, a feature may be switched off on a given environment. Flags to check on cnr1dev1 vs cnr2dev3: MULTI_APPROVAL, MULTI_SLAB_VIEW, MULTI_VARIANT, FOR_EVERY_PERC_CALC, FUTURE_PROMO_DAYS, PROMO_ALLOW_VALIDATE, PROMO_COPY_IS_ALLOW, PROMO_ENRICHMENT_ALLD / SRC, PROMO_FREEZABLE_SEC_TYPE, BUDGET/TGT_HIER_COMBINATION, BUDGET/BOTTOM_UP_VAL, CASHMEMO/FREE_PROD_SCHEME_UTILIZE_PRICE_TYPE, CHECK_PROJECT_CODE, BUDGET_QTY_VISIBILITY (R1).
