# S&D end-to-end test automation — status (end of 2026-09-24)

**Goal:** Jira key → test cases → test steps (written by Claude from app knowledge) → live execution with
Selenium/Vibium MCP → passing flows turned into `selenium-framework-db` SQL (human-reviewed, never auto-applied).
One human checkpoint at the end. Pilot story: **SDMS-10351** (auto-substitute exclusion policy, DT + outlet subtype).

## Done

| What | Where |
|---|---|
| SDMS-10351 test cases (34 cases, blank steps) and generator | `regress-master/data/SDMS-10351 Auto Substitute Exclusion Policy - Test Cases.xlsx`, `docs/snd-workflow/build_sdms10351_testcases.py` |
| Comparison vs the Claude.ai-generated workbook (it has 50 cases, ALT- prefix, Status dropdown; ours has Expected Results, row heights, frozen header) | in chat only — best of both is the plan below |
| Draft `CLAUDE.md` for the S&D project (Jira → Excel → steps → execution) | `docs/snd-workflow/CLAUDE.md.draft` (not yet placed; update it once steps are auto-generated, see below) |
| Data dictionary parsed: 548 tables / 10,808 columns, screen-caption → column maps, lookup script | `docs/snd-tables/` (`snd_tables.json`, `dd_lookup.py`, README) |
| Live DB findings (`snd-schema` MCP → PostgreSQL `ng_astrone`) | `docs/snd-tables/snd_domain_knowledge.md` |
| Full menu catalog from `smm_pr_opg_optiongroups` + `smm_pr_apo_appoption`: 898 nodes, 778 with a screen | `docs/snd-tables/snd_menu_outline.md`, `snd_menu_tree.json`, `snd_menu_flat.json`, built by `snd_menu_build.py` |
| Raw extracts of all screen definitions (not yet parsed) | `docs/snd-tables/raw/` (menu, 301 page layouts, 943 page configs in 10 slices) |

## Key findings to remember

1. **Screens are database-defined.** 306 menu options route to `/dyl/layout` (dynamic layouts); `DYL_<code>` → layout `<code>`
   in `dyp_dp_pgl_pagelayout` → `pagePanel.appOption = DYP_<pagecode>__` → page `<pagecode>` in `dyp_dp_pgm_pagemeta`
   (`dpgm_tablename` = backing table) → controls in `dyp_dp_pgc_pageconfiguration.dpgc_configjson`.
2. **Control JSON has what steps need:** `_code` (textBox/…), `name` (e.g. `txt__ppro_policy_verno`, usable as a stable locator),
   `dataField`, `isRequired`, `readOnly`, `maxLength`, `type`, `defaultValue`, `fieldValidations`. Labels are i18n keys
   like `DYP.P.101055.G....policy_verno`; where the real caption text lives is **not yet found** (check `*_m` translation tables).
3. **Hierarchy:** parent links (`sopg_parentoptgrpid`) are the real structure; the `sopg_level` field is inconsistent (482 of 910 rows
   don't match parent depth). 9 rows point to missing parents.
4. **`_m` tables = multi-language copies** (215 in DB) — user confirmed. `smm_*` = S&D security module (applications, app options,
   option groups, role options, users, roles).
5. Security: `smm_pr_rop_roleoption` (20,159 rows) says which role sees which option; `smm_pr_sus_user` has 1,975 users.
6. Cash memo = sale/order; the DB predates SDMS-10351 (no auto-sub tables) and is Indonesia (0101/0102) while the story is [PH].
7. Tool limits: the MCP query tool allows plain `SELECT` only (no `WITH`); big results are saved to a file and must be parsed with Python.
   Use `C:\Users\syed.kamran\AppData\Local\Python\bin\python.exe` (the WindowsApps `python` alias is blocked). Don't name scripts `inspect.py`.

## Next steps (tomorrow)

1. **Parse `raw/` → `snd_screens.json`**: per page code: description, backing table, controls (type, name, dataField, required,
   readOnly, maxLength, validations), buttons, grid columns; then join layouts → menu options so each menu path knows its screens/fields.
2. Find where **caption text** for the i18n keys is stored, so steps can use on-screen labels.
3. Confirm the **login flow and app URL**, then explore 2–3 real screens with Selenium/Vibium (start with a simple master-data
   screen, e.g. Product Policy) to check the JSON-derived locators against the rendered page.
4. Build the **step generator**: story + screen catalog → steps in the agreed verb convention (Login / Navigate / Enter / Choose / Click / Upload / Verify …).
5. Get the **right database/environment for SDMS-10351** (has the new policy tables, [PH] org) and the S&D test URL + login (secrets file, not chat).
6. Merge the two workbook generators' best parts (ALT- prefix, Status dropdown, Notes sheet, Expected Results, frozen header).
7. Decide where the S&D project lives (separate folder with its own `CLAUDE.md` vs `regress-master/`), then update the CLAUDE.md draft
   so steps are Claude-generated instead of QA-written, keeping one review checkpoint.

## Open questions for the user

- Which DB/environment holds SDMS-10351 (and read-only user instead of `postgres`)?
- S&D test URL, test login, which org/distributor to use.
- Is there a rule where menu code/level encodes the path? (Parent links look authoritative.)
