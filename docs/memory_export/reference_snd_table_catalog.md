---
name: snd-table-catalog
description: "S&D (DCODE) knowledge base in qa-os/apps/snd/knowledge/ (dictionary JSON, lookup tool, domain + UI notes, menu, DB-declared screens) and the live snd-schema DB findings; read before writing S&D test steps or queries."
metadata:
  node_type: memory
  type: reference
  originSessionId: eb4a66f7-6654-4151-a641-fe8df7bda0d6
  modified: 2026-09-25T06:53:49.439Z
---

**Purpose (user, 2026-09-24):** the S&D dictionary + `snd-schema` DB access exist so I remember the app's flows, screens and fields,
and can write test steps myself when generating test cases from Jira stories.

Files in `C:\MyWork\gias-qa-workspace\qa-os\apps\snd\knowledge\` (tools in `..\tools\`):
- `domain.md`: entity, order and product model. `ui.md`: verified login, menu API and SKU Substitution screen.
- `snd_tables.json` (548 tables / 10,808 cols), `snd_tables_index.md`, `snd_screen_field_map.json`, `dd_quality_report.md`.
- `snd_menu_*` (from smm tables), `screens_db/` (295 DB-declared dynamic screens, from `tools/build_screens.py`), `raw/` extracts, `env/<env>/` live harvests.
- Search with `python ../tools/dd_lookup.py <regex> | -t TABLE | -r TABLE | -s "caption"`. Don't read the 2 MB JSON whole.
- The DD source xlsx is still in `regress-master\docs\snd-tables\` (it was locked by Excel during the move); `dd_build.py` finds it there.

Live DB: connector `mcp__snd-schema__*`, PostgreSQL 11.7, db `ng_astrone`, schema public, table names lowercase. It is the **only** S&D DB and is the
base layer; environments such as cnr2dev3 add regional/version features (e.g. SKU Substitution) on top ([[no-docs-learn-from-metadata]]).
Facts:
- Orgs 0101/0102 Danone Indonesia, 99 GLOBAL; transactions to 2026-01-30.
- DT and outlets share `snd_en_pp1_prf_bsen_phs_lvl1` (DIST/OUTL); outlet subtype = `snd_pr_chh_chanel_hierarchy`.
- Sale/order = cash memo (`snd_tr_cmm_cashmemo_master/detail`).
- `smm_*` = security module (applications, app options, option groups = menu, roles, users); `dyp_dp_*` = dynamic page metadata.
- Tables ending exactly in `_m` = multi-language copies.
- Label text for `DYP.*` keys is not in the DB; it lives in the app's `/ngui/asset/i18n/<lang>.json`.

Dictionary caveat: the Table Name cell on continuation rows is often wrong (the parser uses serial numbers); the dictionary lacks newer tables.
See [[snd-test-automation-project]].
