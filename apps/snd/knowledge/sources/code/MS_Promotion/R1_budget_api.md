# R1 (PK + BD) Promotion microservice - Budget, Redemption, Validations, API, Data

Source: MS_Promotion branch UL-R1-BD @ 51e7e815 (version.txt = 1.1.109.0), read-only study for QA business training.

Evidence convention: `[code UL-R1-BD@51e7e815 <path>:<line>]`. Java paths are relative to
`PromotionBuilder/src/main/java/com/centegy/`; resource paths start with `res/` =
`PromotionBuilder/src/main/resources/`. "unclear" = not provable from this repo.

**Biggest scope finding first:** the *Budget Setup* screen data (budget catalog, its levels, the
Allocated/Utilized/Balance columns and the budget Excel upload with its validations) is owned by a
**separate target-service** (`targetMaster.base.url`, default `http://localhost/target-service`). The
promotion service only *reads* budgets over REST and *records consumption* in its own allocation
tables [code UL-R1-BD@51e7e815 promotion/domain/services/TargetMasterService.java:30],
[...TargetMasterService.java:60], [...:82], [...:213], [...:244], [...:327]. So most "budget upload"
messages in question 2 are **not in this repo** (see section 2).

---

## 1. Budget model

### 1.1 What a "budget" is in this service
- A budget = a **Target Catalog** row (budget code = `TTGC_TARGET_ID`) with a **hierarchy combination**
  (`TTGC_HIER_COMB`, e.g. `ORGA~DIST~DSRS`) and detail rows per hierarchy value (`TTCD_HIER_VALUE`,
  e.g. `0106~D001~DSR01`) holding `TTCD_TARGET_VALUE` / `TTCD_TARGET_QTY` (allocated) and
  `TTCD_ALLOCATED_VALUE` / `TTCD_ALLOCATED_QTY`
  [code UL-R1-BD@51e7e815 promotion/domain/entities/TargetMasterModel.java:11], [...:142], [...:151],
  [code UL-R1-BD@51e7e815 promotion/domain/entities/TargetMasterDetailModel.java:14], [...:48]-[...:116].
- A promotion points at its budget through `PRM_PM_PMS_PROMOTION_SETUP.TTGC_TARGET_ID`, plus
  `PPMS_BUDGET_LEVEL`, `PPMS_BUDGET_VALUE`, `PPMS_CHECK_BUDGET`, `PPSC_PROMOTION_SECTYPE`, `PPMS_PROJECT_CODE`
  [code UL-R1-BD@51e7e815 promotion/domain/entities/PromotionSetup.java:374], [...:468], [...:477], [...:486], [...:591], [...:600].

### 1.2 Levels (ORGA / DIST / DSR / Outlet)
- Hierarchy tokens available to a budget come from the order payload: `DIST` = customerAccountID,
  `DSRS` = DSR, `OUTL` = entityCode (outlet) [code UL-R1-BD@51e7e815 promotion/execution/fillers/domains/snd/SnDRepositoryFiller.java:68]-[...:70].
- The value combination for a document is built by taking each token of the budget's `HIER_COMB`
  and reading it from the order (e.g. `ORGA~DIST~DSRS` -> `0106~<dist>~<dsr>`)
  [code UL-R1-BD@51e7e815 promotion/execution/beans/components/domain/PromotionBudget.java:228]-[...:230].
- Default hierarchy fallback string `ORGA~DIST~DSRS` (from repository `BUD_HIE`) exists, but the method
  is private and never called - treat as dead code [code UL-R1-BD@51e7e815 promotion/rest/controllers/PromotionSetupController.java:572]-[...:585].
- **Bottom-up fallback:** if no budget row exists at the exact level and the budget has
  `TTGC_BTM_UP = 'Y'`, the service climbs one level (e.g. DSR -> DIST) and uses the parent's
  **remaining** value (`target value - allocated value`); it stops (no budget) when only `ORGA` is left.
  Exact-level match uses the full target value/qty
  [code UL-R1-BD@51e7e815 promotion/domain/services/TargetMasterService.java:108]-[...:157], ORGA stop [...:116], parent remaining [...:130], exact [...:153].
- PJP-level budget: no PJP token is read by the filler for budgets - **unclear / not supported in this code**.
- Coupon "Loyalty B2B" (`CouponVer = LTYB2B`) promotions append `~DIST` to the allocation key, i.e.
  consumption is tracked per distributor even if the budget is higher-level
  [code UL-R1-BD@51e7e815 promotion/execution/beans/components/domain/PromotionBudget.java:253]-[...:257],
  [code UL-R1-BD@51e7e815 promotion/annotation/enums/ExecutionPolicy.java:8].

### 1.3 Budget kinds applied per promotion line
On each qualified resultant the resolver builds up to five budget checks
[code UL-R1-BD@51e7e815 promotion/execution/beans/components/resolvers/AllocationResolver.java:55]-[...:86]:

| Budget | Code | Source of the limit | Unit consumed |
|---|---|---|---|
| Promotion header budget | promotion's `TTGC_TARGET_ID` | target-service detail row | discount value (REPO tag) or quantity (free product) [PromotionBudget.java:262] |
| Scheme count | `SCHCMCOUNT` | promotion property `SCHCMCOUNT` > 0 | 1 per document [PromotionBudget.java:263]-[...:265] |
| Outlet cash-memo count | `CMCOUNT` | promotion property `CMCOUNT` > 0 | 1 per document |
| Budget discount cap | `BUDDISCCAP` | another budget code named in the property | value |
| Discount cap (header) | `DISCCAPLMT` | promotion property `DISCCAP` > 0 | value |

(Budget type enum: [code UL-R1-BD@51e7e815 promotion/execution/beans/components/PromotionHeader.java:16]-[...:20].)

### 1.4 Allocated / Utilized / Balance (consumption ledger)
- Consumption is stored in **`PRM_PM_PAL_PROM_ALLOCATION`** keyed by orga + field comb + value comb +
  budget id + promotion code: `PPAL_ALLOCATED_VALUE/QTY` (= Allocated snapshot), `PPAL_ACHIEVED_VALUE/QTY`
  (= Utilized). Balance = Allocated - Achieved (not stored)
  [code UL-R1-BD@51e7e815 promotion/domain/entities/PromotionAllocation.java:11]-[...:125].
- Every movement is journaled in **`PRM_PM_PAR_PROM_ALLOCATN_REF`** (one row per document per event:
  `PPAR_DOCUMENT_REF`, `PPAR_ACHIEVED_VALUE/QTY` (+ for A, - for R), `PPAR_CM_EVENT` A/R,
  `PPAR_LOG_EVENT`) [code UL-R1-BD@51e7e815 promotion/domain/entities/PromotionAllocationReference.java:14]-[...:163].
- Row is created on first use with achieved 0 (`INSERT ... ON CONFLICT DO NOTHING`)
  [code UL-R1-BD@51e7e815 promotion/domain/dao/PromotionAllocationRepository.java:29]-[...:30].
- If the budget in target-service was **raised**, the allocated snapshot is raised on next use; if it was
  **lowered**, it is only lowered when already-achieved <= new budget (so a budget can never effectively
  drop below what is already utilized) [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionAllocationService.java:200]-[...:216].
- "Current Promotion" grid shows Allocated = `TTCD_TARGET_VALUE/QTY` at `ORGA~DIST` for the logged-in
  distributor, Achieved = SUM of `PPAL_ACHIEVED_VALUE/QTY` over `ORGA~DIST%` (i.e. distributor + all its
  DSR rows) [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionSetupService.java:1460]-[...:1515].

### 1.5 When Utilized increases
- Budget is consumed only when the calling order/cash-memo request carries **`cashmemoEvent = "S"`**;
  every budget check in the resolver is gated on `S`
  [code UL-R1-BD@51e7e815 promotion/execution/beans/components/resolvers/AllocationResolver.java:57], [...:62], [...:67], [...:74], [...:83].
- `cashmemoEvent` absent -> defaults to `"C"`, and with `"C"` the service returns **no promotions at all**
  [code UL-R1-BD@51e7e815 promotion/execution/fillers/domains/snd/SnDRepositoryFiller.java:315]-[...:319],
  [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionSetupService.java:215]-[...:219].
- Any other value (e.g. `N`) calculates promotions without consuming budget (the budget is only *checked*
  in the qualifier, see 1.7). `R` = return: allocation qualifier, resolver and adjustable are all skipped
  ("budget is not recorded") [code UL-R1-BD@51e7e815 promotion/execution/beans/components/resolvers/AllocationResolver.java:23]-[...:24],
  [...qualifiers/AllocationQualifier.java:39], [...adjustable/AllocationAdjustable.java:21]-[...:22].
- Which UI action (order Save / Confirm / Invoice) sends `S` is decided by the order service - **unclear
  from this repo**.
- Mobile-synced documents: `POST /promotionAllocation/allocate` writes consumption directly, journal
  `PPAR_LOG_EVENT = 'MOB-SYNC'`, and refuses a second allocation for the same document+promotion+budget
  ("Allocation Already exists!") [code UL-R1-BD@51e7e815 promotion/rest/controllers/PromotionAllocationController.java:56]-[...:96],
  [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionAllocationService.java:532]-[...:539], [...:740].
  Note: this path adds the full value with **no balance check** [...PromotionAllocationService.java:703]-[...:719].
  For count/cap budgets the limit comes from the promotion JSON property, default **1.0** if missing [...:633]-[...:673].

### 1.6 When Utilized decreases
- **Edit of an order** (`entryMode = "E"`): before re-applying, the document's previous allocation for that
  promotion is reverted (journal row event `R`), then re-consumed with the new value - so lowering the
  discount on edit gives budget back [code UL-R1-BD@51e7e815 promotion/execution/beans/components/adjustable/AllocationAdjustable.java:42]-[...:50],
  [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionAllocationService.java:113]-[...:117].
- **Error during calculation** with org feature `PROMOTION_PROMPT = Y`: new document -> all its allocations
  reverted; edit -> previous allocations re-adjusted / reversed
  [code UL-R1-BD@51e7e815 promotion/execution/PromotionExecutor.java:74], [...:156]-[...:180].
- **Cancel / full return** (external call): `PUT /promotionAllocation/revert?documentReference=&eventLog=`
  reverts every promotion allocation of the document (log suffix `-RVRT-ALC-PROMOTION`)
  [code UL-R1-BD@51e7e815 promotion/rest/controllers/PromotionAllocationController.java:36]-[...:39],
  [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionAllocationService.java:236]-[...:254].
- **Compensate** `PUT /promotionAllocation/compensate/{event}/{eventLog}`: A -> reverse allocations,
  R -> re-apply reversed ones, E -> both [...PromotionAllocationService.java:319]-[...:357].
- **Partial return / approved quantity change**: `PUT /promotionAllocation/adjust` and `/adjustApproved`
  revert the document's last allocation and re-apply `min(new value, remaining balance)`; new value 0
  also reverts count budgets [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionAllocationRevertService.java:266]-[...:327].
- Which business screens call revert / compensate / adjust (cancel, GRN return, approval) - **unclear
  from this repo** (callers are in order-service).
- Utilized never goes below 0 (floored) [...PromotionAllocationRevertService.java:90]-[...:94], [...:139]-[...:143].
- Loyalty redemption revert is a different thing: `DELETE /redemption/revert` deletes the document's rows
  in the loyalty data holder [code UL-R1-BD@51e7e815 redemption/domain/services/RedemptionService.java:203]-[...:239].

### 1.7 Short balance: no-apply vs partial
- Qualifier: a promotion is disqualified up-front only if its budget is already fully exhausted
  [code UL-R1-BD@51e7e815 promotion/execution/beans/components/qualifiers/AllocationQualifier.java:73]-[...:106],
  [code UL-R1-BD@51e7e815 promotion/execution/beans/components/domain/PromotionBudget.java:362]-[...:369].
- Resolver: grant = `min(requested discount, balance)`.
  - balance <= 0 -> "Allocation exhausted", promotion line value set to **0 and not applied**.
  - 0 < balance < requested: applied **partially (capped at balance)** only if org feature
    **`ALLOW_PARTIAL_BUDGET = Y`** (option type `SCHEMEBUILDER`); otherwise "Partial Allocation not
    configured" and **not applied at all**
    [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionAllocationService.java:141]-[...:179],
    [code UL-R1-BD@51e7e815 promotion/execution/beans/components/domain/PromotionBudget.java:274]-[...:286], [...:412]-[...:425].
- Budget code configured but no budget row found -> promotion line not validated ("Budget not found")
  for header budget; count budgets silently skip [...PromotionBudget.java:294]-[...:305].
- These are log events only (in `PRM_PM_PEV_PROMO_EVT_LOG` response JSON) - no user popup text from
  this service.

### 1.8 Concurrency (cf. SDMS-10155 "budget removing when multi user save")
- Apply path locks the allocation row with `SELECT ... FOR UPDATE` (PESSIMISTIC_WRITE) inside its own
  transaction (REQUIRES_NEW) [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionAllocationService.java:110]-[...:133], [...:197].
- **Revert path does NOT lock** ("no need to lock here") and runs in a separate transaction per row
  [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionAllocationRevertService.java:39]-[...:61].
  Compensate/adjust do lock [...:190], [...:276]. Risk: simultaneous edit/cancel + save on the same
  budget row can lose an update. Test idea: two users saving/editing orders on the same DSR budget at once,
  then compare `PPAL_ACHIEVED_VALUE` with SUM(`PPAR_ACHIEVED_VALUE`) for that key.
- **documentReference trap:** if the request has `DocumentNumber` but no `documentReference`, the filler
  overwrites the reference with a random UUID, so a later edit/revert cannot find the original
  allocation [code UL-R1-BD@51e7e815 promotion/execution/fillers/domains/snd/SnDRepositoryFiller.java:292]-[...:301].
- Whether SDMS-10155 is fixed by this code - **unclear**.

### 1.9 Auto Budget Creation / Loyalty Promotion (SDMS-12111, PromoSecType)
- On promotion Save (`POST /promotionSetup/saveAsMap`) the service calls
  `generateBudgetHeadBasedOnPromotion` [code UL-R1-BD@51e7e815 promotion/rest/controllers/PromotionSetupController.java:331]-[...:335].
- If `budgetLevel` is set and no budget exists with code = promotion code, it posts to target-service
  `/api/v1/targetMasterDetail/uploadBulkBudgetByTagName` with TAG_NAME `ORGA`, SCHEME_CODE = promo code,
  SCHEME_BUDGET, UTILIZED 0, BALANCE 0, qty columns if org feature `BUDGET_QTY_VISIBILITY = Y` (option
  `BUDGET`), BUDGET_LEVEL [code UL-R1-BD@51e7e815 promotion/domain/services/TargetMasterService.java:229]-[...:266].
  - `checkBudget = N` ("unconstrained"): budget value = promotion budget value, level forced to `ORGA`.
  - `checkBudget` not N: budget created with value **0** at the chosen level [...:240]-[...:242].
- If `budgetLevel` is empty and `targetID` is null on save, the existing budget catalog + detail rows
  with code = promo code are **deleted** [...:267]-[...:288].
- Loyalty B2B (`CouponVer = LTYB2B`): on save `PromoSecType = 'LTYB2B'`; with a budget level,
  `checkBudget = 'N'` and budget value = 999,999,999,999.00 (effectively unlimited)
  [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionSetupService.java:1095]-[...:1101].
- Excel/integrator upload creates budget heads in bulk via `/uploadBulkBudgetListByTagName`
  [code UL-R1-BD@51e7e815 promotion/rest/controllers/PromotionSetupController.java:242]-[...:244],
  [code UL-R1-BD@51e7e815 promotion/domain/services/TargetMasterService.java:296]-[...:340].
- Promotion date/status change -> budget dates/status sync: `updateTargetBasedOnPromotion` builds the
  payload but the REST post is **commented out** - currently a no-op
  [code UL-R1-BD@51e7e815 promotion/domain/services/TargetMasterService.java:342]-[...:372].

---

## 2. Budget upload validations

Confirmed: **none of the budget upload validations are in this repo.** The Budget Setup upload is
handled by target-service (`/api/v1/targetMasterDetail/...`) [code UL-R1-BD@51e7e815 promotion/domain/services/TargetMasterService.java:244], [...:327].

| Assumed rule | Status here |
|---|---|
| promo code exists / active | unclear (target-service) |
| ended promotion not editable | unclear for budget; for promotion setup see 3.2 |
| distributor exists / active / accessible | unclear (target-service) |
| value > 0 | unclear |
| not below spent | not validated at upload here; at consumption time allocation is never lowered below achieved [PromotionAllocationService.java:200]-[...:216] |
| allocated + used <= limit | unclear |
| mandatory columns | unclear for budget; promotion-side sheets use column count/name checks (below) |
| rounding to 2 decimals | promotion engine rounds money to 2 dp HALF_UP [code UL-R1-BD@51e7e815 promotion/util/PromotionUtils.java:121]-[...:126], [...:221]-[...:226]; slab tag value 2 dp HALF_DOWN [code UL-R1-BD@51e7e815 promotion/execution/beans/components/controls/PromotionSlabRange.java:378]; budget upload rounding unclear |

Excel uploads that ARE in this repo (promotion side):
- **Custom tag / allowable product upload** (`POST /promotionSetup/uploadCustomTag`): column count and
  name/sequence must match the download; per-row errors returned as `PromoDescription_Error.xlsx` with
  `ErrorColumn`: ",Invalid Scheme Id found", ",Invalid Tag Code found", ",Invalid code found". After the
  promotion has started (`entryMode = F`) rows are only **added**, never removed; before start the tag list
  is replaced [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionETLService.java:419]-[...:566].
- **Promo description / project code upload** (`POST /promotionSetup/uploadPromoDesc`): ",Invalid Orga
  code found", ",Invalid length of Promo desc found" (>100), ",Invalid length of Promo alternate desc
  found", ",Invalid length of Project code found", ",Invalid promo found", ",Can not unmapped project
  code" (blanking an existing project code) [...PromotionETLService.java:568]-[...:676]. Download contains
  active SCHNORMAL promotions not yet ended (or all not ended if `FUTURE_ANY_PROMO_REQUIRED = Y`) [...:80]-[...:105].

---

## 3. Promotion setup flows

### 3.1 Save (new) - `POST /promotionSetup/saveAsMap`
[code UL-R1-BD@51e7e815 promotion/domain/services/PromotionSetupService.java:1000]-[...:1131]
1. Code already exists on a new record -> "Promotion Code {0} is already exists." [...:1023]-[...:1025].
2. `BUDDISCCAP` budget already used by another promotion -> "Budget Discount Cap already associated with another promotion." [...:1043]-[...:1051].
3. Org feature `CHECK_PROJECT_CODE = Y`, status Active, `Claimable = Y`, no project code -> "Project Code not found, EITHER update the project code OR save with INACTIVE status." [...:1054]-[...:1056], [...:1133]-[...:1151].
4. Start date must be >= today, else "Start date could not be less than system date." [...:1105]-[...:1118].
5. Execution order: Super-exclusive -> -2, Exclusive -> -1, else null [...:1107]-[...:1113].
6. Auto number prefix `<PROMO_AUTO_PREFIX or JC><MM>-` [...:1755]-[...:1759]; manual vs auto numbering via `GET /getPromoNumGenMechanismIsManual` [...:1724]-[...:1743].
7. Then auto budget creation (1.9).

### 3.2 Edit
- Promotion already started (start date before today) -> screen frozen (`entryMode = F`); only End
  date, JSON and status can change; end date before today -> "End date could not be less than effective
  date."; changed start date -> "Start date cannot be modified after scheme effective date."; inactive
  status saves only the status [...PromotionSetupService.java:1059]-[...:1077].
- `GET /getpromo/{code}` returns `entryMode = F` when start date <= today (SDMS-2845: same-day promo also
  frozen) [code UL-R1-BD@51e7e815 promotion/rest/controllers/PromotionSetupController.java:183]-[...:188].
- Future promotion edit keeps budget/project/target fields from DB; clearing budget level clears target [...:1080]-[...:1093].

### 3.3 Save As New - `POST /promotionSetup/saveAsNew`
Copies a scheme, strips `DISCCAP`, `BUDDISCCAP`, discount cap values, clears project code, budget level,
budget value, target, and saves **Inactive** (`I`); copies allowable tags from the source scheme
[code UL-R1-BD@51e7e815 promotion/domain/services/PromotionSetupService.java:1762]-[...:1848].

### 3.4 Approve / "Current Promotion Approver"
No approval / approver workflow exists in this service (no approve endpoint, no status other than A/I).
The only approval-related item is `PUT /promotionAllocation/adjustApproved` (budget re-adjust after an
approved document) [code UL-R1-BD@51e7e815 promotion/rest/controllers/PromotionAllocationController.java:51]-[...:54].
Approver screen behaviour - **unclear (likely workflow-service / UI)**. Activation via integration: see 3.6.

### 3.5 Excel / integrator upload of promotions - `GET /promotionSetup/upload?orgaCode=`
[code UL-R1-BD@51e7e815 promotion/rest/controllers/PromotionSetupController.java:210]-[...:259]
- Reads staging tables `PRM_PM_TSH_TEMP_SCHEME_HEAD` (+ `_TSQ` qualify, `_TSR` resultant, `_TSS` slab,
  `_TSG` group) rows modified after the last upload time in `PRM_PM_LUT_LAST_UPLOAD_TIME` and not yet in
  setup [...:217].
- Rejects: no Qualify (`Q`) row; no resultant and no slab (messages in section 6) [...:261]-[...:276].
- Builds the promotion JSON (properties SCHCMCOUNT, CMCOUNT, DISCCAP=outlet capping, SlabUnit,
  Claimable=Y, Claimperc=100, TrdOffFlg) and **deletes + re-inserts** an existing same-code promotion;
  active Y/A -> A, else I [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionETLService.java:299]-[...:366].
- Writes status/message back to `PTSH_PROCESS_STATUS` / `PTSH_PROCESS_MESSAGE`
  [code UL-R1-BD@51e7e815 promotion/domain/services/TempPromotionHeadService.java:31]-[...:53].
- Response: "Total Promo(s)", "Success Promo(s)", "Fail Promo(s)" counts [...PromotionSetupController.java:301]-[...:315].

### 3.6 PRAT / API integration
- `POST /promotionSetup/updateProjectCodeAndBudgetValue` takes a list of {code, projectCode, budgetValue};
  sets project code + budget value and **activates** the promotion if its end date is after today
  [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionSetupService.java:1851]-[...:1889],
  [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionUploadService.java:58]-[...:81].
  That this is the PRAT feed is an inference (the word PRAT does not appear in code) - **unclear**.
- `POST /associateTarget` and `/promoCodesAssociateWithTargetCodes` link promotion(s) to budget code(s)
  and copy the budget's hierarchy into `PPMS_BUDGET_LEVEL` [code UL-R1-BD@51e7e815 promotion/domain/dao/PromotionSetupRepository.java:52]-[...:53].

### 3.7 Integrator job / schedules
- No cron property for the integrator exists in any properties file; `quartz.enabled=false`,
  `scheduled.process.interval=500` [code UL-R1-BD@51e7e815 res/application-common.properties:76]-[...:77].
  The `/upload` endpoint is pull-triggered; who calls it and when - **unclear**.
- Only scheduled job: promotion cache refresh from DB every 60 s (fixedDelay) + heartbeat row in
  `PRM_PM_PCE_PROM_CACHE_EVENT` [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionCacheUpdateService.java:22]-[...:39].
  QA note: a newly saved/edited promotion may take up to ~1 minute to take effect in calculation.
- Manual cache tools: `POST /promoEvictionFromCache`, `GET /updateCacheFromDB`, `/promotionCacheInfo/*`.

### 3.8 Sync to mobile
- `POST /promotionSetup/getActivePromos` returns promotions applicable to given outlets/products **and
  only those with remaining budget at ORGA~DIST** (or no budget), plus all tax/charge promos (0005/0006);
  `showoutlets=Y` returns per-outlet map [code UL-R1-BD@51e7e815 promotion/domain/services/PromotionSetupService.java:2194]-[...:2296],
  [code UL-R1-BD@51e7e815 promotion/domain/dao/PromotionAllocationRepository.java:41]. That mobile sync is the
  caller - inferred, **unclear**.
- Mobile consumption posted back via `/promotionAllocation/allocate` (MOB-SYNC, 1.5).

---

## 4. REST endpoints (context path `/promotion-service`, port 8094; most also under `/api/v1/...`)
[code UL-R1-BD@51e7e815 res/application-common.properties:1]-[...:2]. Controllers extending
`RestControllerBase` also expose generic CRUD/list (core library, not in repo - exact paths unclear).

| Screen (likely) | Method + path | Purpose | Evidence |
|---|---|---|---|
| Current Promotion | GET `/promotionSetup/distAll` | Distributor's running SCHNORMAL promos with Allocated/Achieved value+qty, filters code/desc/altName/dates | PromotionSetupController.java:450; PromotionSetupService.java:1339 |
| Current Promotion (older) | GET `/promotionSetup/listall` | List; distributor user -> promos with ORGA~DIST allocation, N-minus days | PromotionSetupController.java:346; PromotionSetupService.java:1246-1285 |
| Promotion Layout | POST `/promotionSetup/saveAsMap`, POST `/saveAsNew`, GET `/getpromo/{code}` | Save, copy, open | PromotionSetupController.java:331, 505, 171 |
| Promotion Layout | GET `/downloadCustomTag`, POST `/uploadCustomTag`, DELETE `/clearCustomTag`, GET `/listtags`, `/tagModel`, `/getListOfCustomTag` | Product/tag allow-list Excel | PromotionSetupController.java:351-447, 517 |
| Promotion Layout | GET `/getPromoAudit?promo=&flag=` | Change history from `AUD_LG_AT_AUDITTRAIL` | PromotionSetupController.java:528; PromotionSetupRepository.java:120-125 |
| Active Promotions | GET `/promotionHeader/getAllActivePromotion` | Active promos by orga/principal/outlet type/outlet | PromotionEligibilityHeaderController.java:42 |
| Active Promotions / sync | POST `/promotionSetup/getActivePromos` | See 3.8 | PromotionSetupController.java:160 |
| Active promo Excel | GET `/downloadPromoDesc`, POST `/uploadPromoDesc` | Desc / alt desc / project code | PromotionSetupController.java:455, 468 |
| Current Promotion Approver | none found | unclear | - |
| Bulk Promo Allocation | POST `/promotionAllocation/allocate` (body = list of {documentReference, documentType, documentNumber, promotionCode, budgetCode, acheivedVal, acheivedQty, fieldComb, valueComb, allocatedUnit}) | Records budget consumption for already-calculated documents in bulk; screen mapping inferred - **unclear** | PromotionAllocationController.java:56-96 |
| Budget ops | PUT `/promotionAllocation/revert`, `/compensate/{event}/{eventLog}`, `/adjust`, `/adjustApproved` | Give back / redo consumption | PromotionAllocationController.java:36-54 |
| Cash Memo Promotion Viewer | GET `/promotionSetup/getPEL?orgaCode=&docNo=&docType=&logType=REQ|RES|ALL` | Last promotion request/response log for a document from `PRM_PM_PEV_PROMO_EVT_LOG`; "No Record Found! ..." if none. Screen mapping inferred - **unclear** | PromotionSetupController.java:551; PromotionSetupService.java:2059-2090 |
| Order calc | POST `/getResultantsForCashmemo`, `/getResultantsForCharges`, `/getResultantsForBreakup` | Promotion calculation for a document | PromotionSetupController.java:105-138 |
| Budget Setup | not in this service | target-service `/api/v1/targetMaster*` | TargetMasterService.java:30 |
| Integrator | GET `/promotionSetup/upload`, POST `/updateProjectCodeAndBudgetValue`, `/associateTarget`, `/promoCodesAssociateWithTargetCodes` | 3.5-3.6 | PromotionSetupController.java:210, 511, 409, 425 |
| Loyalty redemption | POST `/redemption/apply`, GET `/info`, `/currinfo`, DELETE `/revert`; POST `/voucher/apply` | Points/voucher redeem, enquiry, revert | redemption/rest/controllers/RedemptionController.java:12-35; VoucherSetupController.java:13-23 |
| Diagnostics | GET `/getSDV` ("Ver-101225-111516"), `/getSRT` | Build tag, last restart | PromotionSetupController.java:537-549 |

---

## 5. Tables for read-only DB checks

| Table | Key columns | Use in tests |
|---|---|---|
| `PRM_PM_PMS_PROMOTION_SETUP` | PORG_ORGACODE, PPMS_PROMOTION_CODE; PPMS_START/END_DATE, PPMS_ACTIVE (A/I), PPST_PROMOTION_SUBTYPE, TTGC_TARGET_ID, PPMS_BUDGET_LEVEL, PPMS_BUDGET_VALUE, PPMS_CHECK_BUDGET, PPSC_PROMOTION_SECTYPE, PPMS_PROJECT_CODE, PPMS_EXECUTION_ORDER, PPMS_PROMOTION_JSON | promotion header (PromotionSetup.java:28-600) |
| `PRM_PM_PAL_PROM_ALLOCATION` | orga, PPAL_FIELD_COMB, PPAL_VALUE_COMB, TTGC_TARGET_ID, PPMS_PROMOTION_CODE; PPAL_ALLOCATED_VALUE/QTY, PPAL_ACHIEVED_VALUE/QTY, PPAL_WORKING_DATE | utilized per budget level (PromotionAllocation.java:11-125) |
| `PRM_PM_PAR_PROM_ALLOCATN_REF` | PPAR_ALLOCATION_ID; PPAR_DOCUMENT_REF, PPAR_CM_EVENT (A/R), PPAR_ACHIEVED_VALUE/QTY, PPAR_LOG_EVENT | per-document consumption journal (PromotionAllocationReference.java:14-163) |
| `TGT_PR_TGC_TARGET_CATALOG` | PORG_ORGACODE, TTGC_TARGET_ID; TTGC_HIER_COMB, TTGC_BTM_UP, TTGC_ACTIVE, TTGC_PERIOD_START/END | budget head (TargetMasterModel.java:11-160) |
| `TGT_PR_TCD_TARGT_CATALOG_DTL` | orga, TTGC_TARGET_ID, TTCD_HIER_COMB, TTCD_HIER_VALUE; TTCD_TARGET_VALUE/QTY, TTCD_ALLOCATED_VALUE/QTY | budget per level (TargetMasterDetailModel.java:14-116) |
| `PRM_PM_PEV_PROMO_EVT_LOG` | PPEV_SERIAL_NO; PPEV_TRANS_CODE (doc no), PPEV_TRANS_TYPE, PPEV_EVENT (e.g. ALLOCATE), PPEV_REQ_JSON, PPEV_RESP_JSON | why a promo/budget was (not) applied (PromotionEventLog.java:12-130) |
| `PRM_PM_TSH_TEMP_SCHEME_HEAD` (+ TSQ, TSR, TSS, TSG) | orga, PTSG_PROMO_CODE; PTSH_PROCESS_STATUS (S/F), PTSH_PROCESS_MESSAGE, PTSH_BUDGET_LEVEL | upload staging + result (TempPromotionHead.java:13-279) |
| `PRM_PM_LUT_LAST_UPLOAD_TIME` | PORG_ORGACODE, UPLOAD_DATE | integrator watermark (PromotionTimestamp.java:9-25) |
| `PRM_PM_PAT_PROM_ALLOW_TAGS` | orga, promo, GFC_TAGNAME, PPAT_CUSTOM_TAG_VALUE | uploaded product allow-list (PromotionAllowableTags.java:14-92) |
| `PRM_PM_PEE_PROM_ELGBL_ENTITY` / `PRM_PM_PEP_PROM_ELGBL_PROD` | promotion id + entity / product | eligibility fill (`POST /fill`) (PromotionSetupService.java:1191-1243) |
| `PRM_PM_DHR_DATA_HOLDER` | PDHR_SERIAL_NO; entity, PDHR_SCHEME_ID, PDHR_DOCUMENT_REF | loyalty points / CM-count holder (PromotionDataHolder.java:20-486) |
| `PRM_PM_DQP_DISQUALIFIED_PROM` | entity, promo, PDQP_FAILING_REASON | disqualification reasons (DisqualifiedPromotion.java:12-82) |
| `SND_LG_ORL_ORDER_LOG` | LORL_DOCUMENT_NO, LORL_DETAIL_INFO | calc errors "Error-promotioncalculation" (PromotionSetupController.java:122; OrderLog.java:9) |
| `PRM_PM_PVS_PROM_VOUCHER_STP`, `PRM_PM_ERC_ENT_REDMPTION_CAP` | voucher code; entity max redeem | redemption (VoucherSetup.java:21; PromotionEntityRedeemCap.java:11) |
| `GLB_PR_ORF_ORGA_WISE_FEATURE` | PORG_ORGACODE, POPT_OPTION_TYPE (SCHEMEBUILDER/BUDGET), PFRT_FEATURE_TYPE, PORF_VALUES | flags ALLOW_PARTIAL_BUDGET, PROMOTION_PROMPT, CHECK_PROJECT_CODE, PROMO_AUTO_PREFIX, FUTURE_ANY_PROMO_REQUIRED, BUDGET_QTY_VISIBILITY (OrganizationFeaturePromoRepository.java:15-28; PromotionUtils.java:392-410) |
| `AUD_LG_AT_AUDITTRAIL` | aat_tablename, aat_pkcolumnvalue = `<promo>~<orga>` | promotion change history (PromotionSetupRepository.java:120-125) |

Useful check: for one budget key, `PPAL_ACHIEVED_VALUE` should equal SUM(`PPAR_ACHIEVED_VALUE`) over
the journal (A positive, R negative), floored at 0.

---

## 6. User-visible messages (exact text)

Promotion setup (DomainException keys -> `res/messages.properties`):
| Text | Raised at |
|---|---|
| Promotion Code {0} is already exists. | PromotionSetupService.java:1024, 1811 (res/messages.properties:8) |
| Budget Discount Cap already associated with another promotion. | PromotionSetupService.java:1050 (messages:9) |
| Project Code not found, EITHER update the project code OR save with INACTIVE status. | PromotionSetupService.java:1055 (messages:10) |
| End date could not be less than effective date. | PromotionSetupService.java:1068 (messages:11) |
| Start date cannot be modified after scheme effective date. | PromotionSetupService.java:1070 (messages:12) |
| Start date could not be less than system date. | PromotionSetupService.java:1117, 1817 (messages:13) |
| startDate could not be null or empty. / endDate could not be null or empty. | PromotionSetup.java:527, 561 (messages:5-6) |
| Sheet Altered, column count mismatch! Uploaded sheet should have {0} Columns, instead of {1}; | PromotionETLService.java:561, 575 (messages:14) |
| Sheet Altered, column name/sequence mismatch! Uploaded sheet should be same as Download. | PromotionETLService.java:564, 578 (messages:15) |
| Allocation head not found {0} | PromotionAllocationRevertService.java:67, 197 (messages:7) |
| Invalid Tag Name: {0} / Unknown cell type found, operation not supported. | messages:2-3 (raised in formula builder, not traced) |

Promotion setup controller literals [promotion/rest/controllers/PromotionSetupController.java]:
"File uploaded successfully" (:98), "File is empty unable to uploaded" (:390), "Please enter promotion
code, before Upload the File" (:394), "Please select a file to upload" (:399, :485), "Promotion code not
exists" (:418), "<code> - Promotion code has been failed with error: The promotion code failed due to
improperly defined qualifiers. There should be a Qualify section" (:267), "... There should be a Promotion
Resultants or a Promotion Slabs." (:271); ETL: "<code> - Promotion code has uploaded successfully",
"<code> - Promotion code has been failed with error: <reason>" (PromotionETLService.java:375, 379).
Upload error-sheet texts: see section 2.

Integration responses [PromotionSetupService.java]: "could not be null or empty or incorrect key found"
(:1867, :2015), "promotion details updated having specified code!" (:1878), "promotion specified code
NOT-FOUND!" (:1880), "No Record Found! <orga>-<doc>-<type>" (:2087).

Allocation API [PromotionAllocationController.java / PromotionAllocationService.java]: "Allocation
Successfully Recorded!" (:77), "Budget not found" (:80), "Allocation Already exists!" (:84), "Try Again
Later! Failed To Record Allocation." (:91), "Allocation could not be inserted <docRef>" (Service:613),
"Budget not matched! BudgetCode: %s, HirComb: %s, ValueComb: %s" (Service:617).

Engine log-only texts (in PPEV_RESP_JSON, not popups): "Allocation exhausted", "Partial Allocation not
configured", "Allocation key not found" (PromotionAllocationService.java:174-182), "Allocation exhausted
for combination", "Applied budget", "Budget not found" (PromotionBudget.java:282-304).

Loyalty / voucher redemption (`res/application-promotion.properties`, applied in
redemption/execution/domain/snd/LoyaltyValidator.java:110-147):
"Voucher already applied" (VoucherSetupService.java:117), "Not enough Loyalty Points or Amount to avail",
"Minimum redeem limit exceeded {min}", "Loyalty redeem limit exceeded", "Purchase more than Rs. 1500 to
avail your discount", "Maximum redeem limit exceeded {min} - {max}", "Invalid redeem type", "Merchant
saving is not enabled", "Scheme not applicable on cashememo date", "Voucher not applicable on this date",
"Voucher not applicable, voucher limit exceeded", "Voucher amount is not valid", "Scheme is not valid on
this date", "Voucher not valid for this cashmemo purchase", "Invalid voucher" (VoucherSetupService.java:52),
"Voucher not valid for this outlet type", "Voucher not valid for this outlet", "Voucher not valid for this
customer", "This voucher is not valid after cash discount", "The points are not valid after cash
discount", "Limit not defined" (RedemptionService.java:136), "Voucher is not yet applicable"
(LoyaltyValidator.java:145), "Client wallet is empty" (RedemptionManager.java:132), "Error has been
occurred during execution..." (RedemptionManager.java:146, 254), "Unable to delete by cashmemo reference
{%s}" (RedemptionService.java:230), "Invalid scheme type" / "Invalid redemption type"
(IRedemptionCalculator.java:28-43). (res/application-promotion.properties:67-92)

---

## Open questions for the QA lead / dev
1. Which order-service actions send `cashmemoEvent=S` (save vs confirm vs invoice), and which call
   `/promotionAllocation/revert|compensate|adjust|adjustApproved` (cancel, return, approval)?
2. Where do Budget Setup upload validations live (target-service repo/branch)?
3. Is "Current Promotion Approver" in workflow-service or the UI?
4. Which job/caller triggers `GET /promotionSetup/upload` and on what schedule?
5. Is `updateTargetBasedOnPromotion` being a no-op intended (budget dates/status not synced from promotion)?
