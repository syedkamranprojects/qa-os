# R1 promotion engine: how a promotion is applied to an order (UL-R1-BD @ 51e7e815)

Source: export of MS_Promotion branch UL-R1-BD @ 51e7e815 (Unilever R1 = Pakistan + Bangladesh).
This is a read-only code study written for QA business training.

Evidence tags look like `[code UL-R1-BD@51e7e815 <path>:<line>]`. Each `<path>` is relative to
`PromotionBuilder/src/main/java/com/centegy/` unless the tag says otherwise.
"Unclear" means the code does not settle the point. Confirm it live or in the S&D order code. Do not
treat it as a fact.

Scope note: this service only calculates promotions and books budgets. Order states, stock and the
UI live in the S&D order application, which calls this service. Anything that depends on S&D is
flagged as such.

---

## 0. The pipeline in one picture

1. S&D posts the order to `POST /promotionSetup/getResultantsForCashmemo`
   [code UL-R1-BD@51e7e815 promotion/rest/controllers/PromotionSetupController.java:105].
   The same engine also serves `/getResultantsForCharges` (CHARGES) and `/getResultantsForBreakup`
   (ORDERBREAKUP) [code ... PromotionSetupController.java:130-137].
2. The S&D filler turns the order into a repository. The repository holds the header values
   (distributor, DSR, outlet, gross amounts), one row per product line (QTY1/2/3, VOL, GROSSAMT,
   NetAmount) and roll-ups to product hierarchy levels PRODANA1..5
   [code ... promotion/execution/fillers/domains/snd/SnDRepositoryFiller.java:63-229].
3. If `cashmemoEvent` = "C", which is also the default when S&D sends nothing, the service returns
   an empty result and runs no promotion
   [code ... promotion/domain/services/PromotionSetupService.java:215-219]
   [code ... SnDRepositoryFiller.java:315-319].
4. The service loads all active SCHEME-type promotions, ordered by execution order, then group
   sequence, then sub-sequence (section 4). Each one gets a cheap pre-scan
   [code ... promotion/execution/loader/PromotionDefinitionProvider.java:161-205, 329-366].
5. Each promotion in that order goes through:
   - Qualifiers: date window/frequency, business, sections, exclusivity, coupon
     [code ... promotion/execution/beans/components/PromotionSection.java:21]
   - Resolvers, which calculate the value
     [code ... promotion/execution/beans/components/PromotionDefinition.java:125-166]
   - Post-resolvers: Business, Coupon, Allocation (budget), Breakup (spread to lines), PostPromo
     [code ... PromotionSection.java:22]
6. A promotion's result is kept only if it is "validated" and its value is > 0. The one exception
   is COUPON, which is kept even at 0
   [code ... promotion/execution/processor/ResultantProcessor.java:28].
7. Each result is added to a running list. Later promotions read that list when "trade-off" applies
   (section 4) [code ... promotion/execution/PromotionExecutor.java:117-132].

---

## 1. Promotion types, sub-types, resultant types and value types

### 1.1 Enums hard-coded in the engine

| Enum | Values (id) | What it does in code | Evidence |
|---|---|---|---|
| PromotionType | SCHEME 0001, LOYALTY 0002, MERCHANDIZING 0003, VALIDATION 0004 | Order calculation loads only SCHEME (`PromotionType.SCHEME.value()`) | [code ... promotion/execution/beans/components/PromotionHeader.java:70-74] [code ... PromotionExecutor.java:90-91] |
| PromotionSubType | SCHNORMAL 0001, SCHPOINTS 0002, SCHDISCOUNT 0003, SCHVOUCHER 0004, ALL "", SCHCHARGE 0005 (apply "add"), SCHTAX 0006 (apply "add"), REDEMPTION 0007, ORDERBREAKUP 0008, TARGETBASEDLOYALTY 0009 | Every sub-type except CHARGE and TAX has apply type "sub", meaning it reduces the amount. CHARGE and TAX are "add", meaning they increase it | [code ... PromotionHeader.java:96-118] |
| PromotionBusinessType | SCHEME 0001, LOYALTY 0002, CHARGES 0005, COUPON 0004, REDEMPTION 0005, ORDERBREAKUP 0008, TARGETBASEDLOYALTY 0009 | Derived from the sub-type: POINTS/DISCOUNT become LOYALTY, VOUCHER becomes COUPON, CHARGE/TAX become CHARGES, everything else is SCHEME | [code ... PromotionHeader.java:33-67] |
| BudgetTypes | SCHCMCOUNT, DISCCAP, CMCOUNT, BUDDISCCAP | Budget and limit property keys (section 5) | [code ... PromotionHeader.java:16-20] |
| SectionType | QUALIFY, CRITERIA, RESULTANT | Section 0 is Qualify (products), section 1 is Criteria (who/where), section 2 is Resultant (what you get) | [code ... PromotionSection.java:24-29] |
| LogicalOperator | AND, OR | Operator for qualify and resultant groups | [code ... promotion/execution/beans/components/controls/contracts/AbstractPromotionGroup.java:7-10] |
| ExecutionPolicy | NONE, CASHMEMOEVENTNORMAL (cashmemoEvent=N), CASHMEMOEVENTRETURN (cashmemoEvent=R), CASHMEMOTYPE (CASHMEMOTP=999999999999), COPOUNVERSION1 (CouponVer=LTYB2B) | Switches individual qualifiers or resolvers off for some flows (return, coupon) | [code ... promotion/annotation/enums/ExecutionPolicy.java:3-8] |

- PromotionType, sub-type and resultant type are also database master tables (PromotionResultantType,
  PromotionSubType, PromotionTypeGroup entities). The engine reads the sub-type master for its
  `promotionImpact` flag: "A" means the sub-type adds to the amount
  [code ... promotion/execution/beans/components/controls/contracts/AbstractPromotionItem.java:587-603].
  The full list of resultant types is DB data. Only two literals appear in code: `"COUPON"`
  [code ... ResultantProcessor.java:28] and `"CP"` [code ... promotion/execution/beans/components/resolvers/PostPromoResolver.java:99].
  What "CP" means is unclear. In code it only attaches the list of qualifying products to free-product
  results.

### 1.2 Value types on a resultant line (how the benefit is calculated)

Each resultant line has a `valueType`, read from the promotion JSON
[code ... promotion/execution/loader/PromotionDefinitionDeserializer.java:348].
The engine runs whichever calculator matches
[code ... promotion/execution/beans/components/controls/ResolvablePromotionItem.java:594-602]:

| valueType | Calculator | Business meaning | Evidence |
|---|---|---|---|
| P | PercentageCalculation | Percentage discount. Discount = value% × base. Base = sum of included products' amounts, less earlier group discounts (trade-off), then capped by Purchase Limit and Discount Limit. If the base is 0, the log says "gross amount exhausted" and the value is 0 | [code ... ResolvablePromotionItem.java:693-793] |
| F, with a For-Every item and factor > 0 | ForEveryCalculation | "X for every N": units = floor(measured value ÷ factor), benefit = value × units. Used for free goods (PROD resultant, value = free quantity per block) and for fixed money per block. If the money benefit is greater than the gross of its base item, the benefit is set to 0 | [code ... ResolvablePromotionItem.java:605-660] |
| F, factor = 0 | FixValueCalculation | Flat fixed amount. Set to 0 if it is greater than the gross of its base item | [code ... ResolvablePromotionItem.java:829-858] |
| L | FormulaCalculation | Formula-builder result, less earlier group discounts, never negative, capped by Discount Limit | [code ... ResolvablePromotionItem.java:802-823] |
| (none matched) | — | The line is returned unchanged as a fixed value. Log text: "Fix discount resolver" | [code ... ResolvablePromotionItem.java:444-447] |

Two kinds of resultant line exist:
- **Money discount**: tag `REPO`, typically code `DISONGROSS` ("Discount on Gross")
  [code ... promotion/execution/beans/components/resolvers/BreakupResolver.java:64-68]
  [code ... promotion/execution/beans/components/resolvers/CouponResolver.java:107-113].
- **Free product (BONUS)**: tag starts with `PROD` and valueType is F. BusinessResolver identifies
  free goods by exactly this test [code ... promotion/execution/beans/components/resolvers/BusinessResolver.java:40-41].

**TRADEOFFER**: no such literal exists in code. The nearest concept is the trade-off flag `TrdOffFlg`,
which comes from the setup header field `tradeOff`
[code ... promotion/domain/services/PromotionETLService.java:307]. It controls whether earlier
promotions' discounts are subtracted first (section 4).

### 1.3 Slabs (range table)

- `PromotionSlabRange` contains rows. Each row has from/to columns and one or more resultants
  [code ... promotion/execution/beans/components/controls/PromotionSlabRange.java:41-86].
- The engine picks the first row whose columns all match `from <= value <= to`. The value is first
  rounded to 2 decimals (HALF_DOWN) [code ... PromotionSlabRange.java:272-348, 376-379].
- The measured value is the sum of included products in the slab unit (`SlabUnit` property, e.g.
  QTY3/VOL/GROSSAMT). For amount units (AMOUNT/GROSSAMT) earlier group discounts are subtracted first
  [code ... PromotionSlabRange.java:281-307].
- **Repeat = Y**: after a row matches, the engine stores the remainder (value − row.from) and runs the
  match again on that remainder. Results with the same tag and code are added together
  [code ... PromotionSlabRange.java:336-341, 353-369].
  In repeat mode a percentage resultant uses the **slab From value** as its base, not the actual
  amount. For QTY slab units, From is converted to money as From × unit price
  [code ... ResolvablePromotionItem.java:722-736].
- **Apply remaining percentage**: if this is set and the last result is a percentage, that result is
  applied once more [code ... PromotionSlabRange.java:214-221].
- **Bucket/bundle mode** (`forEveryApplyType = G`): the slab value is the number of complete bundles.
  That is the minimum over bundle items of floor(bought ÷ required)
  [code ... PromotionSlabRange.java:288-297].
- `slabCount`, `slabTargetId`, `budgetSlabCountFlag` and `budgetRowSlabCountFlag` are read from JSON
  [code ... PromotionDefinitionDeserializer.java:508-527], but no execution code uses them. Whether a
  slab count limit is enforced is unclear (probably not in this branch).

---

## 2. Qualify logic (products and quantities)

### 2.1 Units and product hierarchy

For each order line the filler computes [code ... SnDRepositoryFiller.java:138-199]:
- Base quantity = Qty3 + Qty2 × QTY2_FACTOR + Qty1 × QTY1_FACTOR. The factors come from the product's
  custom-tag params.
- QTY3 = base ÷ QTY3_FACTOR if that factor > 0. QTY2 = floor(base ÷ QTY2_FACTOR).
  QTY1 = floor(base ÷ QTY1_FACTOR) (rounding mode FLOOR) [code ... SnDRepositoryFiller.java:158-172].
  Business names are unclear. In practice QTY3 is the smallest unit (pieces) and QTY1/QTY2 are packs,
  rounded down. Example: 30 pieces at 24 per carton count as **1** QTY1, not 1.25.
- VOL = VOL_FACTOR × base quantity [code ... SnDRepositoryFiller.java:188-189].
- GROSSAMT, GRSINCLTAX, GRSEXCLTAX, MRPGROSS, TAXGROSS and NetAmount are taken from each line as
  sent [code ... SnDRepositoryFiller.java:120-125, 493-513].
- Every value is also added up into the line's PRODANA1CODE..PRODANA5CODE hierarchy codes, so a
  promotion can be defined at brand or category level [code ... SnDRepositoryFiller.java:175-199].
  The hierarchy is also built from the custom-tag tree [code ... SnDRepositoryFiller.java:214-219, 236-270].
- LPPC (number of distinct product lines) is counted [code ... SnDRepositoryFiller.java:201-203].
- Header values include REPO.GROSSAMT (order gross), NETAMT, and ORDNUM/ORDNUMOUTL. The last two are
  hard-coded to 99999 [code ... SnDRepositoryFiller.java:68-87].
- A product with no custom-tag data (unknown product) gets no quantities. The error logs for this are
  commented out [code ... SnDRepositoryFiller.java:150-153, 204-209].

### 2.2 How a selection is checked

- A selection is one qualify item. It has a unit (`tagAttributeCode`, e.g. QTY1/QTY3/VOL/GROSSAMT),
  an operator, a value, an include/exclude flag (`assignmentFlag`) and a list of products or levels.
  **Every product in the selection takes the selection's own include/exclude flag**
  [code ... PromotionDefinitionDeserializer.java:241-254, 293-307].
- Numeric check: the engine adds up the selection's products in the selection's unit, then compares
  with `==`, `>=`, `>`, `<=` or `<` [code ... promotion/execution/beans/components/controls/QualifyingPromotionItem.java:126-155].
  The sum uses `withIncludedFlag = true`, so **excluded products are counted the same way in the
  qualify check** [code ... AbstractPromotionItem.java:168-180].
  If a selection contains GROSSAMT, the order gross is used instead [code ... AbstractPromotionItem.java:175-177].
  The default operator when blank is `==` [code ... PromotionDefinitionDeserializer.java:253].
- For a single-value numeric item with no product list (e.g. REPO GROSSAMT), earlier group discounts
  (trade-off) are subtracted before the comparison. When the selection has a product list, the
  product sum replaces this and **no deduction is made** [code ... QualifyingPromotionItem.java:127-134].
- String check (criteria): with a list, Include means the order value must be in the list and Exclude
  means it must not be (`isIncluded() == anyMatch(...)`). Without a list the check is `==` or `!=`
  [code ... QualifyingPromotionItem.java:156-165]. Boolean check is equality with default "N"
  [code ... QualifyingPromotionItem.java:191-193].
- If the order value is missing, the item fails [code ... QualifyingPromotionItem.java:124-125].
  Caveat: whether a product-list selection always resolves to a non-null value is unclear. It depends
  on the saved JSON shape. Verify live.
- Group operators: AND stops at the first failure, OR stops at the first success
  [code ... QualifyingPromotionGroup.java:164-198].

### 2.3 What the discount is calculated on (Include/Exclude)

- A resultant's product base is copied from the whole root qualify group: every selection's products,
  each with its own include flag [code ... PromotionDefinitionDeserializer.java:369-375, 426-454].
- Discount base = sum of products whose flag is Include. Any product flagged Exclude is then forced to
  0 [code ... ResolvablePromotionItem.java:235-289]. If a product appears twice and either copy is
  Exclude, Exclude wins [code ... ResolvablePromotionItem.java:187-200].
- If the resultant has `totalGross` set (useTotalGross), the base is the order gross itself. In that
  case Include/Exclude and the trade-off deduction are skipped
  [code ... ResolvablePromotionItem.java:707-713] [code ... BreakupResolver.java:144-150].
- Note: the resultant base does **not** check which OR branch actually qualified.

### 2.4 Trainer table (two selections)

| Setup | Trainer says | Code says | Verdict |
|---|---|---|---|
| Include + Include, AND | both | Both must pass their thresholds. Discount base = both selections' products | **Confirmed** |
| Include + Exclude, AND | selection 1 only (sel 2 must-buy) | Both must pass their thresholds, so the excluded selection still has to be bought (the qualify sum ignores the flag). Discount base = selection 1 only, excluded products set to 0 | **Confirmed** |
| Include + Include, OR | either | Qualifies if either selection passes. The discount base is **all** included products bought from both selections, even one that did not reach its own threshold | **Correct the wording**: "either qualifies, but the discount is on everything bought from both" |
| Include + Exclude, OR | selection 1 | Qualifies if sel 1 or sel 2 passes. The base is selection 1 only. If only selection 2 was bought, the promotion qualifies with value 0 and is dropped (value must be > 0) | **Confirmed in effect**, with that nuance |

Evidence for the whole table: [code ... QualifyingPromotionGroup.java:164-198]
[code ... AbstractPromotionItem.java:168-180] [code ... ResolvablePromotionItem.java:235-289]
[code ... ResultantProcessor.java:28]

### 2.5 Pre-scan before full qualification

Before full qualification the loader skips a promotion in two cases
[code ... PromotionDefinitionProvider.java:329-420]:
- No Criteria element matches the order. This check is skipped if any criteria element uses `!=` or
  is Exclude.
- No Qualify element is either a REPO-type ("R") element or a product ("C") actually present in the
  order.

---

## 3. Criteria and eligibility (who and where)

- The Criteria section (index 1) is checked with the same item logic. All its items must pass
  [code ... promotion/execution/beans/components/qualifiers/SectionQualifier.java:26-44].
- Entities and attributes the filler makes available [code ... SnDRepositoryFiller.java:68-70, 305-424, 785-847]:
  - Distributor `DIST`, DSR `DSRS`, outlet `OUTL` / `entityCode`, entityType, refEntity, referral
  - Channel CHNLHIER + CHAD/CHBD/CHCD
  - Geography GEOGHIER + GEOAD/GEOBD/GEOCD
  - Sales hierarchy SALHIER + SALAD/SALBD/SALCD. All three hierarchies are also cut into parent levels
    using repository config [code ... SnDRepositoryFiller.java:771-783, 823-846].
  - Outlet attributes ATTRIB01–14 and VATTRIB03/04/08 (defaults N/N/U), LIFESTYL (AreaType), ADTAXEXMP
  - Payment mode PAYMODE, delivery mode DELVMODE, cash memo type CASHMEMOTP, DOCTYPE, company and
    outlet rank COMPRANK/OUTLRANK
- Include/Exclude on a criteria list means "value in list" / "value not in list"
  [code ... QualifyingPromotionItem.java:157-159].
- Promotion header `entityType` must equal the order's entityType, or be empty
  [code ... PromotionSetupService.java:189].
- Outlet type / geo / rank lookup from the business-entity master is commented out. These must come
  in the payload [code ... SnDRepositoryFiller.java:384].
- A DB query that excludes entities (PromotionExcludeEntity) exists
  [code ... promotion/domain/dao/PromotionSetupRepository.java:32-33], but the order path never calls
  it. Unclear whether exclusion lists are enforced elsewhere.
- Promotion-type filter from the payload: if `includePromoType` = Y, only sub-types in `promoTypeList`
  can apply. If N, those sub-types are blocked. Log text: "Business qualification failed, due to
  payload currentPromoSubType not matched in promoTypeList"
  [code ... promotion/execution/beans/components/qualifiers/BusinessQualifier.java:48-52].

---

## 4. Order of application, exclusivity, groups and trade-off

### 4.1 Order

- DB order is `executionOrder`, then group `sequance`, then `subsequance`. Nulls count as 0
  [code ... PromotionSetupRepository.java:26-27]. The in-memory cache uses the same order
  [code ... PromotionDefinitionProvider.java:170-173].
- On save, **Super Exclusive** gets executionOrder −2, **Exclusive** gets −1 and everything else gets
  null (= 0) [code ... PromotionSetupService.java:1107-1113]. So Super Exclusive runs first, then
  Exclusive, then normal promotions by group sequence and sub-sequence.
- The order is fixed by these numbers. There is no "best deal wins" comparison. Each promotion that
  qualifies is applied in turn.
- The filler defines a `promoOrderBy` variable with sequence first [code ... SnDRepositoryFiller.java:406],
  but nothing reads it.

### 4.2 Exclusive vs Super Exclusive

- **Exclusive** (only for sub-type SCHNORMAL):
  - When an exclusive promotion is checked and has started (start date ≤ today 00:00 server time), it
    marks every product or level in its qualify section as "EXCL = Y".
  - A non-exclusive promotion checked later fails if any of its qualify products or levels is marked
    [code ... promotion/execution/beans/components/qualifiers/ExclusionQualifier.java:46-86].
  - Every qualifier always runs; the result is combined at the end
    [code ... PromotionDefinition.java:182-186]. So an exclusive promotion **marks its products even
    when it fails its own quantity or criteria check**. It only has to get past the loader pre-scan.
    Test point: an exclusive promotion that does not fully qualify may still block later promotions
    on the same SKUs.
  - The rule is skipped on returns (ignoreWhen CASHMEMOTYPE) [code ... ExclusionQualifier.java:25].
- **Super Exclusive**:
  - The only effect in this branch is running first (executionOrder −2).
  - The logic that would run *only* super-exclusive promotions when any exist is commented out
    [code ... PromotionExecutor.java:93-104].
  - So Super Exclusive does not suppress other promotions here, unless they are marked by the
    Exclusive rule. Treat this as a likely gap versus the trainer.
- Bug spotted: in "Save As New", the Super Exclusive −2 is immediately overwritten with null unless
  Exclusive is also set [code ... PromotionSetupService.java:1831-1838]. A Super Exclusive promotion
  created with Save As New may therefore run in normal order.
- Two exclusive promotions on the same SKU: the later one is not blocked, because the "is exclusive"
  branch only marks and never checks [code ... ExclusionQualifier.java:55-60].

### 4.3 Group Type, sequence and trade-off (gross vs after earlier sequences)

- A promotion's `promotionTypeGroupCode` points to a PromotionTypeGroup row. That row has
  sequance/subsequance and a parent group [code ... promotion/domain/entities/PromotionTypeGroup.java:20-21].
- Trade-off flag `TrdOffFlg` controls which earlier discounts are subtracted
  [code ... AbstractPromotionItem.java:221-339, 356-436]:
  - **empty**: no deduction. The discount is calculated on gross.
  - **"G"**: subtract discounts already applied by promotions in the **parent group chain** (walking up
    parent → grandparent), product by product
    [code ... promotion/domain/services/PromotionTypeGroupService.java:57-92].
  - **"A"**: as G, and also subtract discounts from promotions already applied in the **same group**.
- Charges and taxes (sub-type apply type "add", or sub-type master promotionImpact = "A") are entered
  with a negative sign, so they **increase** the base for later promotions
  [code ... AbstractPromotionItem.java:587-603] [code ... BreakupResolver.java:192-194].
- Per-product deduction data comes from line breakups recorded by BreakupResolver. It is only recorded
  when the promotion has a group code [code ... BreakupResolver.java:186-218].
- Seq1–Seq4 labels do not appear in code. They are only DB values of sequance/subsequance. How
  charges and taxes slot into Seq1–4 is unclear (DB setup).
- Tax promotions use the delivery date for the date check when `taxOnDate` = DD. Schemes do the same
  when `schemeOnDate` = DD [code ... promotion/execution/beans/components/qualifiers/FrequencyQualifier.java:44-57].

---

## 5. Limits

These are different settings with different scope:

| Setting (JSON / property) | Scope | Exact behaviour | Evidence |
|---|---|---|---|
| For Every factor (`forEveryFactorValue`) + For Every item | per order line or group | units = **integer** part of (measured ÷ factor), benefit = value × units | [code ... ResolvablePromotionItem.java:612-644] |
| Purchase Limit (`purchaseLimit`) | per order | Caps the eligible base. Percentage with a QTY slab unit: cap = unit price × limit. `percentageLimitOn = P`: cap = limit% of the target. For-Every bundle: added as a maximum bundle count | [code ... ResolvablePromotionItem.java:503-531, 586-588] |
| Discount Limit (`discountLimitValue`) | per order, this resultant | Caps the discount amount. Percentage: base is capped at limit×100/value, so discount ≤ limit. For-Every F: units capped at limit×factor/value. Formula: min(value, limit). The final base is the minimum of (base, purchase cap, discount cap) | [code ... ResolvablePromotionItem.java:534-547, 816-818] |
| Discount Cap (property `DISCCAP`, setup field `outletCapping`) | **across orders**, per combination of the "DISCCAPLMT" target hierarchy (likely per outlet; the hierarchy is DB config) | A manual value budget, written to the allocation tables on every saved order. When it is used up the promotion gives 0, or the remainder if partial budgets are allowed | [code ... PromotionETLService.java:302] [code ... promotion/execution/beans/components/resolvers/AllocationResolver.java:77-84] [code ... promotion/execution/beans/components/domain/PromotionBudget.java:239-242] |
| Budget Discount Cap (`BUDDISCCAP`) | across orders, the linked target | Budget against the named target. No error if the budget is not found | [code ... AllocationResolver.java:69-75] |
| Header budget (targetId) | across orders | Value budget for a REPO discount, quantity budget for free goods. Budget not found → promotion not validated ("Budget not found") | [code ... AllocationResolver.java:55-57] [code ... PromotionBudget.java:293-305] |
| Scheme count `SCHCMCOUNT` | across orders, whole scheme | Count budget: each saved order uses 1 | [code ... AllocationResolver.java:59-62] [code ... PromotionBudget.java:263-265] |
| Outlet cash-memo count `CMCOUNT` | across orders, per hierarchy combination (likely outlet) | Count budget: each saved order uses 1 | [code ... AllocationResolver.java:64-67] |

- **Limit vs Cap**: yes, they are different settings. Discount Limit is per order and never stored.
  Discount Cap (DISCCAP) is a running total stored in PRM_PM_PAL_PROM_ALLOCATION
  [code ... promotion/domain/entities/PromotionAllocation.java:11].
- **Repeat Limit**: no such setting exists. The only repeat is the slab "repeat" Y/N with no maximum
  [code ... PromotionDefinitionDeserializer.java:511-512].
- **Target Discount**: no order-level concept. Targets are used by KPI or target grids (loyalty /
  target-based) [code ... promotion/execution/beans/components/controls/PromotionGrid.java:166-215] and by
  Purchase Limit "% of target" [code ... ResolvablePromotionItem.java:510-519]. Order meaning is unclear.
- CountQualifier and AllocationQualifier exist but are **not registered**, so they never run
  [code ... PromotionSection.java:21]. Count and budget exhaustion is therefore enforced only when
  the budget is booked, not as an up-front qualification.
- Possible issue: count budgets are created once per resultant line [code ... AllocationResolver.java:50-87].
  A promotion with two resultant lines may use SCHCMCOUNT/CMCOUNT twice per order. Unclear; verify.
- **Rounding**:
  - The engine does **not** round money. Division uses DECIMAL128, and `BigDecimalMath.round()`
    (2 dp HALF_UP) is never called on this path [code ... promotion/util/PromotionUtils.java:121-127, 139-161].
    Final rounding is up to S&D.
  - For-Every units and QTY1/QTY2 conversions are truncated (floor).
  - Slab matching uses 2 dp HALF_DOWN [code ... PromotionSlabRange.java:378].

---

## 6. Free goods, stock and the "Confirmed" state

- A free product is a resultant with tag PROD and valueType F. Quantity = value × floor(measured ÷
  factor) [code ... ResolvablePromotionItem.java:612-644].
- A free-goods budget is a **quantity** budget [code ... AllocationResolver.java:55]
  [code ... promotion/domain/services/PromotionAllocationService.java:138-145].
- **Stock check**: none in this service. A search for stock or "confirm" finds nothing in the
  execution path. `DocumentStatus` is copied into the repository [code ... SnDRepositoryFiller.java:408],
  but nothing reads it. Stock availability and what happens when stock runs out belong to the S&D
  order module. Unclear from this code.
- Free-goods rules that do exist here, all tied to GIN (goods issue note) state `ginApproved`
  (I = initial, P = in process, A = edited after approval)
  [code ... SnDRepositoryFiller.java:418] [code ... BusinessQualifier.java:32-33]:
  - Order edited after GIN approval (entryMode E, ginApproved A): only promotions already in the
    order's `allocationList` can qualify. Log text: "Business qualification failed, due to promotion
    code not exists in provided promoCodeList" [code ... BusinessQualifier.java:66-87].
  - GIN in P or A: a free-product scheme that is not already a free scheme on the order gets 0. Log
    text: "Business resolver failed, new free product scheme cannot be applied".
  - In the same states the free quantity is capped at the original allocation. Log text: "On Cashmemo
    after GIN approval, Free product quantity cannot be greater than original value in Cashmemo"
    [code ... BusinessResolver.java:40-60].

---

## 7. Scheduler, dates, state and "Save then Apply"

- **Active state**: only setups with active = 'A' or 'Y' are loaded
  [code ... PromotionSetupRepository.java:26, 72-76]. The cache keeps only active promotions whose end
  date ≥ the previous day [code ... PromotionDefinitionProvider.java:434-461].
  - "Save As New" always saves as inactive 'I' [code ... PromotionSetupService.java:1829].
  - "Allocated" as a promotion state does not exist in code. Unclear.
- **Cache refresh**: every 60 seconds a job compares DB modified date, end date and active flag with
  the cache and reloads what changed [code ... promotion/domain/services/PromotionCacheUpdateService.java:24-34]
  [code ... PromotionDefinitionProvider.java:763-890]. A save also triggers a reload after 3 seconds
  [code ... PromotionDefinitionProvider.java:466-470] [code ... PromotionSetupService.java:1747].
  - So a newly saved or activated promotion should apply to orders within about 3–60 seconds.
  - A manual reload endpoint exists: `POST /promotionSetup/reloadPromotions`
    [code ... PromotionSetupController.java:522-525].
  - "Save then Apply" as a UI step is not in this service. Unclear.
- **Date window**: the order is rejected if docDate < start or > end. Comparison is on full date-time.
  Log text: "Start/End date qualification failed" [code ... FrequencyQualifier.java:59-65].
  - Test point: if the end date is stored as 00:00, an order later that same day may fail. Unclear;
    verify.
- **CRON / frequency**: if the promotion has a `frequency`, it is a Quartz cron expression and the
  order date-time must match it. An invalid cron means fail. Log text: "Frequency qualification
  failed" [code ... FrequencyQualifier.java:67-95].
- **Setup-time date rules** (user-visible messages, `messages.properties`):
  - "Start date could not be less than system date."
  - "End date could not be less than effective date."
  - "Start date cannot be modified after scheme effective date."
  - Evidence: [code ... PromotionSetupService.java:1063-1117]
    [code UL-R1-BD@51e7e815 PromotionBuilder/src/main/resources/messages.properties:11-13].
  - Once a promotion is effective, editing only changes end date, JSON and active flag
    [code ... PromotionSetupService.java:1060-1073].
- Active-promotion listing (scan) includes promotions starting up to **tomorrow**
  [code ... PromotionExecutor.java:256-263].

---

## 8. Re-application on edit, return and cancel

- **Order events** (`cashmemoEvent`):
  - C = no calculation [code ... PromotionSetupService.java:215].
  - **S = budgets are booked**. Every budget in AllocationResolver requires cashmemoEvent = "S"
    [code ... AllocationResolver.java:57, 62, 67, 74, 83].
  - R = return. Every budget qualifier, adjustable and resolver is switched off, and all revert
    functions do nothing [code ... AllocationResolver.java:24] [code ... PromotionBudget.java:382-410].
  - N = normal (enum only). Any other value: the promotion is calculated but no budget is booked.
  - Business meaning of each letter (S = save?) is unclear. It is set by S&D.
- **Edit** (entryMode = E):
  - Before re-booking, the previous booking of the same document, promotion and target is reversed,
    then the new value is booked. So **an edit fully re-prices**, including an edit that lowers the
    discount [code ... PromotionAllocationService.java:113-117].
  - If the promotion no longer qualifies after the edit, its budget for this document is reversed
    (AllocationAdjustable). Log text: "Reverting budgets" [code ... promotion/execution/beans/components/adjustable/AllocationAdjustable.java:42-51].
  - If it qualifies but the value becomes 0, BreakupResolver reverses it [code ... BreakupResolver.java:51-56].
- **Return** (cashmemoType = 999999999999):
  - Only the promotion codes passed in `promoCodes` are evaluated, loaded from the DB without cache
    [code ... PromotionExecutor.java:80-87].
  - Criteria, date/frequency and exclusivity checks are skipped [code ... SectionQualifier.java:31-35]
    [code ... FrequencyQualifier.java:29] [code ... ExclusionQualifier.java:25].
  - Trade-off group look-up uses the promotions loaded for this return [code ... promotion/domain/services/PromotionTypeGroupService.java:95-117].
  - The engine recalculates on whatever lines S&D sends. If S&D sends the remaining quantity, the
    slab would re-price on the remaining quantity. What S&D sends is unclear.
  - `promoCodes` entries look like "CODE~0" or "CODE~1". On return, if "~0", a free-product line is
    nulled: "Free product not allowed on return after discount, reverting allocation...". If "~1", a
    discount line is nulled: "Discount not allowed on return after free product, reverting
    allocation..." [code ... PostPromoResolver.java:44-66] [code ... SnDRepositoryFiller.java:386-404].
- **Budget give-back**: the engine does not do it. S&D must call:
  - `PUT /promotionAllocation/revert`: reverses the document's whole latest booking per key
    [code ... promotion/rest/controllers/PromotionAllocationController.java:36-38]
    [code ... PromotionAllocationService.java:236-254].
  - `PUT /promotionAllocation/adjust`: reverses the last booking and re-books the **new
    value/quantity that S&D supplies**, capped at what remains. A value of 0 reverses everything
    [code ... PromotionAllocationController.java:46-48]
    [code ... promotion/domain/services/PromotionAllocationRevertService.java:266-325].
  - The service never calculates a proportion itself.
- **Failure handling** (org feature `PROMOTION_PROMPT`):
  - N (default): the failing promotion is logged and skipped, and the others continue.
  - Y: budgets are reverted and the error is passed to S&D [code ... PromotionExecutor.java:74, 138-190].
  - The controller also writes "Error-promotioncalculation" to the order log [code ... PromotionSetupController.java:106-127].

---

## 9. Messages on this path (exact strings)

Most texts are **event-log** messages, not UI text. They are stored in PRM_PM_PEV_PROMO_EVT_LOG
[code ... promotion/domain/entities/PromotionEventLog.java:12] and can be read through
`GET /promotionSetup/getPEL` [code ... PromotionSetupController.java:551-557]. They are the best
evidence for QA when a promotion did not apply.

| Text | Where |
|---|---|
| "Start/End date qualification failed" | FrequencyQualifier.java:62 |
| "Frequency qualification failed" | FrequencyQualifier.java:75 |
| "Business qualification failed, due to payload currentPromoSubType not matched in promoTypeList" | BusinessQualifier.java:50 |
| "Business qualification failed, due to promotion code not exists in provided promoCodeList" | BusinessQualifier.java:86 |
| "Business qualification skipped, due to empty promoCodeList" | BusinessQualifier.java:89 |
| "Coupon qualification failed, due schemes not found" / "Coupon qualification failed, due to externalScheme is null" | CouponQualifier.java:45, 49 |
| "Qualifying item failed " / "Qualifying item success " | QualifyingPromotionItem.java:200, 204 |
| "Scanning promotion criteria failed" / "Scanning promotion qualification failed" | PromotionDefinitionProvider.java:355, 349 |
| "Group discount deducted" | AbstractPromotionItem.java:346-348 |
| "gross amount exhausted" / "resolving by percentage" / "Fix discount resolver" | ResolvablePromotionItem.java:762, 793, 447 |
| "Range slab applied" / "Range slab not applied" | PromotionSlabRange.java:334, 343 |
| "Allocation exhausted" / "Partial Allocation not configured" / "Allocation key not found" | PromotionAllocationService.java:178, 174, 182 |
| "Allocation exhausted for combination" / "Budget not found" / "Applied budget" | PromotionBudget.java:282, 297/304, 291 |
| "isBudgetValidated ==> false!" / "Applying budget" | AllocationResolver.java:53, 93 |
| "Promotion breakup skipped" / "Promotion breakup applied" / "Promotion breakup failed" | BreakupResolver.java:52, 180, 228 |
| "Line level discount validation error, reverting allocation..." | PostPromoResolver.java:85 |
| "Coupon resolver failed, due AMOUNT_EXHAUSTED!" | CouponResolver.java:155 |
| "Reverting budgets" | AllocationAdjustable.java:43, CouponResolver.java:162 |
| "Promotion log failed with error" / "Promotion revert failed with error" | PromotionExecutor.java:150, 183 |

User-facing exception texts (messages.properties):
- "Allocation head not found {0}" [code ... PromotionAllocationRevertService.java:58]
  [code UL-R1-BD@51e7e815 PromotionBuilder/src/main/resources/messages.properties:7]
- The setup date messages listed in section 7.
- A filler exception text exists but sits inside commented-out code, so it is dead:
  "Promotion execution failed =====> %s, Promotion code %s " [code ... SnDRepositoryFiller.java:720].

---

## 10. Trainer statements vs code

| Trainer statement | Code finding | Status |
|---|---|---|
| Budget is used at order save for fixed/percentage | Budgets are booked only when cashmemoEvent = "S" [code ... AllocationResolver.java:57-83]. Whether "S" is sent at save is up to S&D. This applies to every resultant type, free goods included (quantity budget), not only fixed/percentage | **Consistent if S = save**, but broader. Confirm the S&D event letter |
| Free goods apply only when the order is Confirmed | The engine never reads the order status. DocumentStatus is stored but unused [code ... SnDRepositoryFiller.java:408]. Free goods are calculated and budget-booked on the same "S" event as discounts. Only GIN state limits free goods [code ... BusinessResolver.java:40-60] | **Not supported by this service.** If true, it is enforced in S&D. Unclear |
| Insufficient remaining budget means the promotion is not applied at all (no partial) | True only while org feature `ALLOW_PARTIAL_BUDGET` ≠ Y. With Y, the discount or free quantity is cut to the remaining budget [code ... PromotionAllocationService.java:141-175] [code ... PromotionBudget.java:412-425] | **Partly contradicted**: configurable per organisation |
| Cancel/return gives budget back proportionally | The engine does not book or reverse budget on return (cashmemoEvent R) [code ... PromotionBudget.java:382-410]. Give-back happens only when S&D calls /revert (full reverse) or /adjust (S&D supplies the new amount) [code ... PromotionAllocationRevertService.java:266-325] | **Not computed here.** "Proportional" depends on what S&D sends. Unclear |
| (implicit) Super Exclusive blocks other promotions | Only ordering (−2). The "super exclusive only" filter is commented out [code ... PromotionExecutor.java:93-104] | **Contradicted** for this branch |
| (implicit) Discount is on gross | Only when TrdOffFlg is empty or "totalGross" is set. With TrdOffFlg G/A, earlier groups' (and for A, the same group's) discounts are subtracted first | **Depends on setup** |

## 11. Suggested QA test points coming from the code

1. An exclusive promotion that fails its own threshold: does it still block a later promotion on the
   same SKU? [ExclusionQualifier.java:46-86 + PromotionDefinition.java:182-186]
2. A Super Exclusive promotion alongside a normal one on the same SKU: both apply?
3. Include + Include OR where one selection is below its threshold: is the discount on both selections?
4. A promotion with an end date of today: does an order placed later today still get it?
5. A preview or non-"S" event shows the discount, but the "S" save gives 0 when the budget is used up
   (no budget check before booking).
6. A promotion with two resultant lines and SCHCMCOUNT = 1: is the count used twice?
7. Super Exclusive created via "Save As New": does it lose run-first ordering?
