---
name: project-regress-master-dcode-gap
description: "First DCODE authoring script written for regress-master, but DCODE has no AppAdapter/app row yet - flow can't execute until that's built"
metadata: 
  node_type: memory
  type: project
  originSessionId: b54266a3-dd90-41e2-a3e2-d9c864c34d01
  modified: 2026-09-23T07:52:39.238Z
---

Authored `regress-master/sql/authoring/example_dcode_sku_substitution_policy_add.sql` (flow `SMK-SKU-01`, group `DCF1`, screen `DCF101`) documenting the live DCODE "SKU Substitution Policy - Add" run (Test Case #1 from `data/SKU Substitution Policy(1).xlsx`) as real fct_pr_sc_screens/fct_pr_sf_screen_field/fct_pr_sef_screen_events_flow rows.

**Why:** User asked to turn the screens/flow just executed live (via Selenium against `dcodecnr2dev3.unilever.com`) into a selenium-framework-db authoring script, following the existing GIAS worked-example convention ([[project-regress-master]]).

**Gaps found while authoring (documented in the script's header comment, not yet resolved):**
1. No `fct_pr_app_application` row for DCODE, and no `AppAdapter` registered for it (only `com.regressmaster.gias.GiasAppAdapter` via ServiceLoader) — this flow **cannot run** in runner-cli/runner-gui today, only exists as prepared data.
2. DCODE's post-login flow has an extra "pick a Distributor, click Proceed" screen with no equivalent concept anywhere in the schema or GIAS's adapter (GIAS login model = branch + department only). Sketched as an optional commented-out `DCF100` screen in the script rather than solved.
3. `psc_routing_hint` reuses the `path:A>B>C` convention as documentation only — DCODE is actually navigated via a live-filtered left search box (type text, click a matching result row), structurally unlike GIAS's flyout tree, so a real `DcodeAppAdapter.navigateToScreen` would need its own implementation, not just a routing-hint string.
4. DCODE's inputs are DevExtreme `dx-select-box`/`dx-texteditor-input` web components with **no `id`/`name` attribute at all** (confirmed live via `document.querySelectorAll`) — used 1-based positional xpath (`(//input[contains(@class,'dx-texteditor-input')])[N]`) instead, weaker than the id/name locators GIAS screens get.
5. Test Case #2 of the same Excel sheet (download template → fill → upload) needs a file-choose interaction with no component type in the current vocabulary (`0000`-`0010`) — not authored.

**How to apply:** Before assuming any DCODE flow is runnable, check whether a `DcodeAppAdapter` + app row now exist — as of 2026-09-23 they did not. If asked to author more DCODE flows, reuse the `DCF1`-style group-id band (parallel to GIAS's `88F1..88FA`) and flag the same gaps rather than re-discovering them. Related: [[project-regress-master]].
