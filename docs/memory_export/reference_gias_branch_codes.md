---
name: reference-gias-branch-codes
description: "GIAS login branch codes - the login dropdown is backed by PR_GN_LC_LOCATION.PLC_LOCACODE; \"GIS Setup\" branch = 0010010001."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 8dd9a349-6460-4115-8859-ba785c098e87
  modified: 2026-09-08T12:04:22.478Z
---

The GIAS login branch dropdown `#myForm:ddlPLC_LOCACODE` (branch selection screen)
is populated from **`PR_GN_LC_LOCATION`** (Oracle) - column **`PLC_LOCACODE`** is
the option value, `PLC_LOCADESC` the label, `PLC_LOCASHORT` the short name,
`PLC_LOCAACTIVE='Y'` for live branches. Query via `mcp__gias-schema__run_readonly_query`.

Key code:
- **`0010010001`** = "GIS Setup Branch For IT" (short `HOM`, active, type D / branch
  type C). **Parameter Setup menu items (Business Class Setup etc.) only render in
  the menu when logged in under this branch** - the post-login menu is
  permission/branch-driven (`SH_SM_UB_USERAUTBRANCH` + option authority per branch).
- `0801500508` = the Regress-Master GIAS adapter's built-in fallback default (not
  necessarily an active branch in this DB).

For a Regress-Master run, set the branch via `GIAS_DEFAULT_BRANCH` env var or
`-Dgias.branch=<code>` (the `GiasAppAdapter` reads these in `overrideFromEnv`; else
falls back to `0801500508`). Also `.claude/settings.json` `GIAS_DEFAULT_BRANCH` for
the Selenium-MCP `login_to_document_selection` flow. Related:
[[project-regress-master]], [[project-gias-menu-navigation]].
