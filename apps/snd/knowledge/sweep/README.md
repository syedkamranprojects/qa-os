# Whole-application sweeps (read-only)

`<env>.<user>.json` — every screen the user's menu can open, visited once and harvested from the live DOM:
fields (label, id, name, widget, required, readonly), buttons, grids (columns), tabs, headings, breadcrumb.

| File | Env / user | Date | Screens | Result |
|---|---|---|---|---|
| `cnr2dev3.KPO_slv.json` | cnr2dev3, KPO_slv, distributor 50000451 | 2026-09-25 | 314 (5 admin pages skipped) | 314 ok, 0 failed, 20.7 min |

Per-screen files: `../screens_observed/<option_id>.json` and `_index.json`.

## Method (no Python, no player)
Claude drives the page through the Selenium MCP: the QA user logs in once in the browser Claude opens, then Claude injects an
in-page crawler that navigates by the app's own router (`history.pushState` + `popstate`), waits until the DOM settles, harvests,
and moves on. Nothing is clicked except navigation; no dropdown is opened; nothing is saved. Results leave the page as one
file download, so nothing large passes through the chat.

## Lessons (kept here so the next sweep starts from them)
- **Clicking through the sidebar is fragile**: a single missed lookup leaves the flyout open and every later item fails (first attempt: 19 of 314).
  **Direct in-app navigation** is reliable and faster (2-4 s per screen; some upload pages take the 14 s cap because they never "settle").
- Wait for the URL to reach the screen's route AND the DOM signature to stay unchanged for ~1.2 s, or the harvest reads a half-loaded page.
- Only the active tab of a tabbed screen is visible; multi-tab screens (Outlet Profile etc.) are under-counted (DB says 79-83 fields, the first tab shows ~30).
- The logout menu does not exist on the distributor-selection page; close the browser session to drop the login.
- Menus differ per user/env: repeat for KPO_mp (cnr1dev1, 437 screens) and KPO_ph (cnr2dev3, 332 screens).
