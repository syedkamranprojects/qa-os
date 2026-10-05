---
name: project-gias-element-cache
description: Status of the GIAS element-locator cache built for shsm_mn_se_main.jsp (login->menu flow) and known-good default codes
metadata: 
  node_type: memory
  type: project
  originSessionId: 59391d59-0278-4867-8d1f-30dffb278d43
  modified: 2026-09-11T12:59:27.712Z
---

As of 2026-08-10, the GIAS QA workspace (`C:\MyWork\gias-qa-workspace`) has a
working element-locator cache covering the full login -> branch ->
application -> department -> menu -> logout flow, seeded and verified live
end-to-end (twice: once during discovery, once in a cache-only run with
zero accessibility scans and zero source reads).

**Files built/updated this session:**
- `.claude/element-cache/gias/shsm/shsm_mn_se_main.json` - 10 elements,
  each with its own `source_file`/`source_hash` (per-element, not
  per-entry-file, since `shsm_mn_se_main.jsp` is only an outer frameset -
  real content lives in `shsm_mn_se_loginpage.jsp`,
  `shgn_gs_se_stdgridscreen_SHSM_DS_LOGINSELECTION.jsp`,
  `shgn_bt_se_button_SHSM_DS_LOGINSELECTION.jsp`, `genins/ggu_mn_login.jsp`,
  `shsm_st_se_title.jsp`).
- `.claude/skills/test-orchestrator/SKILL.md` - added cache-check/write
  workflow, self-healing on stale locators, code-vs-text dropdown
  selection rule.
- `.claude/settings.json` - scoped Write/Edit allow for
  `.claude/element-cache/**`; also holds `GIAS_DEFAULT_APPLICATION` (still
  set to the placeholder `"13"`, which does NOT match any real dropdown
  option - see resolution below).
- `CLAUDE.md` - documents the element-cache convention.

**Known-good codes for the 'administrator' test user** (all confirmed live,
not guesses):
- Branch: `0801500508` (AHD Islamabad Branch) - matches `GIAS_DEFAULT_BRANCH`, correct.
- Application: `88` = General Insurance. Confirmed 2026-08-19 directly
  against the GIAS Oracle DB via `mcp__gias-schema__run_readonly_query`:
  `SH_SM_SS_SYSTEM` shows system `02` ("General Insurance") is the only
  active system (`SST_STATUSCODE='Y'`; system `01`="ERP" and the `03/25/26/27`
  test systems are all inactive). `SH_SM_AA_APPLICATION` for systems 01/02
  shows app code `88`="General Insurance" is the only app under system `02`.
  `GIAS_DEFAULT_APPLICATION` in settings.json was `"13"` (not a valid app
  code at all - no such row exists) and has now been corrected to `"88"` in
  `.claude/settings.json`. Resolved, not just noted.
- Department: `13` = MOTOR (confirmed live; matches `GIAS_DEFAULT_DEPARTMENT=MOTOR`).
  The department dropdown (`text1015`) only appears after selecting
  application 88.

**Not yet cached / open items:**
- The post-login Menu screen's item tree is deliberately NOT cached
  (large, permission-driven, no stable ids) - always live-scan it.
- The Year field (`text0`) on the application-selection screen is
  identified in cache notes but has no dedicated element entry yet.
  Confirmed live 2026-09-11: defaults to the current year (2026) already -
  no action needed unless testing a different year explicitly.
- No actual test scenario (beyond the login->menu->logout flow itself) has
  been run yet - this session was infrastructure-building, not feature
  testing.

**Department 22 = TRAVEL also confirmed live (2026-09-11)**, logging in
successfully through to the Menu screen same as MOTOR(13)/FIRE(11) - see
[[project_gias_menu_navigation]] for the Endorsement Entry flow run under
this department, including a better (synthetic-MouseEvent) flyout technique
than this file's original plain-hover approach.

See also [[feedback_close_browser_after_logout]] and [[reference_gias_schema_queries]] for the DB queries used to confirm application/system codes.
