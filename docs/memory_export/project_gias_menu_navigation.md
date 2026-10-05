---
name: project-gias-menu-navigation
description: "Status of GIAS menu-tree caching (General Insurance > Transactions > Underwriting > Document Entry) and the structured \"flow\" JSON schema built to replay navigation without an LLM"
metadata: 
  node_type: memory
  type: project
  originSessionId: 15874ffb-524e-452e-ab42-ab7c543b7919
  modified: 2026-09-11T12:59:08.115Z
---

As of 2026-08-19, beyond the login->menu cache (see [[project_gias_element_cache]]),
the GIAS QA workspace has:

**Menu-tree cache** - `.claude/element-cache/gias/shsm/shsm_mn_menu.json`, keyed by
dot-path (e.g. `menu.general_insurance.transactions.underwriting.document_entry`),
each entry recording its xpath locator, required interaction (`click` vs `hover`),
and the JSP/hash it was captured against. Menu is permission-driven per user
(`captured_for_user` field) - see [[reference_gias_schema_queries]] for how
app/department codes were confirmed via direct DB queries.

**Document Selection screen cache** - `.claude/element-cache/gias/genins/ggu_dp_intdoc_selection.jsp`
elements (doc type dropdown, status dropdown, Show button) plus the results-grid
row-id naming convention (`<field><6-digit-zero-padded-row-index>`, e.g.
`btn1000004` = Update button for the row whose `GDH_DOC_REFERENCE_NO_r_000004`
matches the target Ref No).

**Structured "flow" schema** (the user's explicit ask) -
`.claude/element-cache/gias/flows/login_to_document_selection.json` is the first
of what should become a library of ordered, parameterized JSON flows: each step
has `action` (navigate/type/click/hover/select/verify), an absolute `frame_path`,
a `by`/`value` locator, and a `timeout_ms` - designed so a non-LLM player can read
the file and call the Selenium MCP tools directly, with no DOM re-exploration.
Goal stated by the user: eventually generate Selenium Java test code from these
flows (phase 2), removing the need for an LLM call at replay time entirely.

**Key gotcha found while live-testing this flow (2026-08-19), now encoded in the
JSON itself as a structured `retry_policy` (not prose):** the GIAS menu's
hover-triggered flyout cascade (`shmalib/jscript/shsm_menu_com.js`) is a
stateful chain. A click on a not-yet-visible deep flyout item can fail with
"element not interactable" even after waiting - and simply re-hovering the
failed (deepest) item again does NOT reliably reopen it. Recovery requires
re-running the FULL ancestor hover sequence from the top of that flyout branch
(e.g. re-hover Transactions, then Underwriting, each with a ~1s settle delay)
before retrying the click. The flow JSON models this via a `retry_group` id
shared by the affected steps plus a top-level `retry_policy.algorithm` telling
the player to replay the whole group, not just the failed step, up to
`max_attempts` times.

**Open/next steps:**
- Only one flow file exists so far (login -> Document Selection). More flows
  (e.g. reaching the policy Update/edit screen, other menu paths) should follow
  the same schema once exercised live.
- The `frame_path` convention is absolute-from-default-content, using per-level
  `{by, value}` pairs (detailFrame by id; mainFrame/buttonFrame/dataFrame/Frame2
  by name) - keep this consistent in future flow files.

**Second flow added (2026-09-11):** `.claude/element-cache/gias/flows/login_to_endorsement_entry_add.json`
- login -> Menu -> Transactions > Underwriting > Endorsement Entry -> click
  "Add New" -> new-endorsement "Log Book (Header)" form
  (`genins/ggu_gp_gp_logbook.jsp?fromselection=yes`). Live-verified end to end,
  login department TRAVEL(22) this time (not MOTOR/13) - confirms department
  choice doesn't affect the menu path itself, only what's visible/permitted.
- **Better flyout technique confirmed live:** instead of this file's plain
  `hover`+xpath-text-match steps (which needed the `retry_group` workaround
  above), reused gias-qa-core's `FlyoutMenuNavigator.java` synthetic-MouseEvent
  JS verbatim (`_fire(el,['mouseover','mouseenter','mousemove'])` per hop,
  `['mouseover','mousedown','mouseup','click']` for root-open and leaf-click) -
  every hop (root -> Transactions -> Underwriting -> Endorsement Entry leaf)
  succeeded first-try, zero retries. The new flow file embeds this JS verbatim
  under a top-level `flyout_js_helpers` key with three reusable actions
  (`flyout_open_root`/`flyout_hover`/`flyout_click_leaf`) instead of raw
  xpath-hover steps - **prefer this pattern over plain hover for all future
  flow files**, it's the same code path gias-qa-core's own AppAdapter uses in
  regress-master (see [[project_regress_master]]) so behavior is proven doubly.
- **Frame-by-name gotcha gains one more member:** `headerFrame` (inner frame
  of `ggu_gp_gp_logbook.jsp`) also has no `id`, only `name` - same rule as
  mainFrame/buttonFrame/dataFrame/Frame2.
- New element caches: `genins/ggu_end_intdoc_selection.json` (Add New button -
  no id, matched by `value` text, does a full `window.location.replace`, not
  an AJAX partial) and `genins/ggu_gp_gp_logbook.json` (only the "Log Book
  (Header)" heading landmark captured so far - individual form fields on that
  screen are NOT yet cached, needed before this can drive a real
  create-endorsement data-entry test).
