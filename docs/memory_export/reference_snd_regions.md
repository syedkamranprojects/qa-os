---
name: snd-regions
description: "S&D release regions — R1 = Pakistan + Bangladesh (PKBD); \"Pakistan training\" includes BD tickets in R1."
metadata:
  node_type: memory
  type: reference
  originSessionId: 4f9d9dd7-3f94-4731-9b7f-74dae6208ab1
  modified: 2026-10-07T06:11:10.254Z
---

Stated by the user 2026-10-07: market Pakistan is in region **R1**, and R1 also contains **Bangladesh (BD)**. Jira "Region / Country" = "PKBD - R1" covers both; the market of a ticket comes from the title prefix / Client field (e.g. SDMS-12390 "BD-...", Client Unilever BD -> org 010105). THPH - R2 = Thailand/Philippines.

**How to apply:** R1 tickets (PK or BD) are in scope during the Pakistan training ([[sdms2990-parked]]); don't flag a BD ticket as off-scope. Note app.yaml `market_of_story` maps PKBD -> 010104 (PK) — for BD tickets use org 010105 (BD group 61, cnr1dev1).
