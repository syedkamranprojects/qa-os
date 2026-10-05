---
name: project-gias-full-menu-catalog
description: The entire GIAS General Insurance (app 88) menu tree has been extracted from the DB to .claude/element-cache/gias/menu/ as tree JSON + flat path index + text outline
metadata: 
  node_type: memory
  type: project
  originSessionId: 7a27c51a-74ee-42af-8c2d-e972c2e8b18a
  modified: 2026-09-01T05:47:10.380Z
---

On 2026-09-01 the **whole** GIAS General Insurance menu was extracted from the
Oracle DB (not screen-scraped) and cached under
`.claude/element-cache/gias/menu/`:

- `gias_menu_tree.json` - nested root->branch->leaf tree; each node has
  `level_code`, `label`, `path` (label breadcrumb); leaves also carry
  `launch.source` (target JSP) and `launch.show_page_args` (exact arg order
  for `fcshowPage()`).
- `gias_menu_paths.json` - flat, one row per leaf (screen name -> how to reach it).
- `gias_menu_outline.txt` - indented human-readable dump.
- `README.md` - explains the schema + regeneration.
- Builder: `scratchpad/build_menu_tree.py` (in the session scratchpad; the
  source SQL is in its header). Regenerate by re-running the query via
  `mcp__gias-schema__run_readonly_query` then the script.

**Where GIAS stores the menu:** table `SH_SM_AM_APPMENU`, column
`SAM_LEVELCODE` is a materialized path (2 chars per level;
`parent = code[:-2]`, `depth = len/2`). Leaf target page comes from
`SH_SM_AN_APPSUBOPTION.SAN_SOURCE` joined on
`(SAA_APPCODE, SPT_PRGTYPECODE, SAO_OPTCODE, SAN_SUBOPTCODE)`. Runtime build:
`shsm.SHSM_ApplicationProfile.fsgenerateRuntimeMenu()` from
`shsm/shsm_mn_menu.jsp`; leaf click = `fcshowPage(appCode, prgType, optCode,
subOptCode, source, levelCode, validateClass)`.

**Shape:** 7 top-level menus (`01` Parameter Setup, `02` Transactions,
`03` Process, `04` Authority Module, `05` Setting & Configuration,
`06` MIS Reports, `07` Work Flow), 56 branches, 402 leaves, max depth 4.
`SH_SM_AM_APPMENU` also holds menus for apps 01/02/92/94/98/99 - only app 88
was exported (the only active GIAS login app - see [[reference_gias_schema_queries]]).

**Caveats baked into the JSON `caveats` field:** DB `SAM_NOOFCHILD` is stale
(use computed `children_count`); 3 leaf level codes are reused by 2 screens
each (`02010906`, `02030501`, `02042013`); `fsgenerateRuntimeMenu` renumbers
sibling level codes per user at runtime, so the **label breadcrumb `path` is
the stable navigation key, not the number**; the file is the full catalog,
live per-user visibility is still filtered by `SH_SM_UO_USERAUTOPTION`.

Relationship to earlier caches: this supersedes the hand-built partial
`shsm/shsm_mn_menu.json` for breadth. The flyout stateful-retry gotcha and
the structured flow schema still live in [[project_gias_menu_navigation]];
replay-without-LLM intent in [[feedback_structured_flow_replay]].
