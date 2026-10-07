---
name: project-bulk-data-factory-plan
description: "Bulk-data-factory approach agreed 2026-10-06 — start with Order Booking (+Detail +_ASSR) for group 11 PK, generated from framework DB + snd-schema; 4 decisions pending"
metadata:
  node_type: memory
  type: project
  originSessionId: b5778f77-fda9-45aa-a9b0-f6d24e0e917f
  modified: 2026-10-06T13:05:35.307Z
---

On 2026-10-06 the user agreed the approach for the bulk-data-factory, which generates bulk case-data Excel for the legacy selenium-framework-db engine. They want "a proper way to start", to be discussed in a later session.

Agreed approach:
1. Read the flow's shape from CTA_CONFIG_ASSERTION (screens = sheets, psf_field_db_column = headers, _ASSR sheets).
2. Use the existing workbook (framework/casedata-samples/NG_Dcode_QA_OTC (Pak).xlsx) as the style template.
3. Build data pools from snd-schema: active outlets on the section/PJP with their tax flag, SKUs in stock with their price.
4. Build the case matrix from the knowledge pages: positive, ATP boundary, negative cases, within a stock budget.
5. Messages come only from the observed catalog. Downstream values are chained via repo_* columns.
6. Validate, then output in the casedata format.

First slice: Order Booking + Order Booking Detail + its _ASSR sheet, group 11 PK, about 20 outlets × 3–5 SKUs, then one QA run in the legacy engine.

**Why:** the hand-typed workbooks use fixed outlets 01–07 and go stale (FRAMEWORK_DRIFT). The end goal of QA OS is generated scripts plus bulk data replayed without AI.

**How to apply:** when the user resumes this topic, start from the 4 pending decisions:
1. Scope (Order Booking only, or a whole flow).
2. Amount assertions (captured values, runtime repo_*/CHECK_VALIDATION, or skipped).
3. Rows per run.
4. Who runs the workbook in the legacy engine, and on which environment.

The contract is in qa-os/framework/cta_config_assertion.md §5 and §5.1.

Related: [[reference-regress-casedata-contract]], [[project-g11-session3-done]]
