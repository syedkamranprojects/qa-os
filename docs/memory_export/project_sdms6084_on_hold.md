---
name: project-sdms6084-on-hold
description: SDMS-6084 (PK, Off Days dropdown on Distributor Profile HQ) - full run done 2026-10-15: 16 pass, TC11 blocked (no legacy data), TC12/13 skipped; D-6084-1 not reproduced
metadata:
  type: project
---

SDMS-6084 run `qa-os/runs/SDMS-6084/20261009-1753`, execute stage done 2026-10-15. The workbook was rebuilt.

**Results (19 cases):**
- **16 PASS:** TC01–TC10 and TC14–TC19.
- **TC03** passed after its step 10 was corrected (approved by the QA lead): picking a selected day again removes it.
- **TC11** is blocked because no distributor has an Off Days value from before the dropdown. Checked read-only: 15108843, 15178537, 125555555 and 50250327. Not read: 18011494 (its HQ list is empty) and 956783323 (81 rows).
- **TC12/TC13** (order delivery date) were skipped by the QA lead.

**D-6084-1** (Report To "Required" while Sub Distributor = N) was not reproduced on 2026-10-14/15: about 20 Updates succeeded. Ask QA whether it was fixed.

**Rules:**
- Sub Distributor = Y enables Report To; with N, Report To is disabled and not needed.
- Distributor Profile DT has its own Update and saves Off Days directly, with no approval.
- Saved days display in selection order.

**Auto_Multi_Orga** can select 6 PK distributors, not only 15108843.

**How to apply:**
- Recordings exist for paths P1/P2/P3/P5/P6/P7/P8 (`recording_TC04/05/08/09/10/15/19.json`). Regress Master scripts are generated only when asked.
- Recorder `results.json` files vary in shape. `qaos_workbook.py` now normalises them; a hardening item is to unify the format.

Related: [[feedback-post-training-workflow]].
