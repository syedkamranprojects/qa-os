# S&D (DCODE) UI knowledge — verified live

Verified with Selenium MCP on **2026-09-25** against `https://dcodecnr2dev3.unilever.com/ngui`
as user **KPO_PH** (Philippines), distributor **15181887-CHRIS JANN**.

## Environments

| Env | URL | Users | Notes |
|---|---|---|---|
| cnr2dev3 | `https://dcodecnr2dev3.unilever.com/ngui` | KPO_slv, KPO_ph | **Has SDMS-10351** (SKU Substitution screens). Use for the pilot. |
| cnr1dev1 | `https://Dcodecnr1dev1.unilever.com/ngui` | KPO_mp | Not yet explored. |

Passwords live only in the gitignored `settings.local.json` (`SD_TEST_PASSWORD`), never in files or chat.

**DB mismatch:** the `snd-schema` connector (PostgreSQL `ng_astrone` @ 10.1.113.38, user `postgres`) has **no**
SKU Substitution menu entries or tables, so it is **not** the database behind cnr2dev3. Use the live app
(the menu API below) as the source of truth for menus until the matching DB connector is available.

## Login flow (SSO, OAuth2)

1. `GET /ngui` → redirects to `/sso-dev/oauth2/authorize?...client_id=snd_online_mobility...`
2. Login form: `input[name=username]` (id `a3`), `input[name=password]` (id `a4`), `button[type=submit]` "Login". CSRF hidden field `_csrf`.
3. Redirect to `/ngui/multiple-organization` → **Distributor** select (DevExtreme). Options are
   `div[role=option].dx-list-item` with text `<code>-<name>` (KPO_PH: `15181887-CHRIS JANN`, `50200411-STMI II`, `50200779-MONTANA`).
   Click the option, then the **Proceed** button. Calls `POST /global-service/api/v1/location/setLocationInSession?locationCode=<code>`.
4. Lands on `/ngui/content-master/menu`. The user name is shown top right (`KPO_PH`).
5. **Logout:** click the user name → `li#logout`. Returns to the SSO login page.

Automation rule: credentials are typed by the deterministic runner from env vars; Claude does not type passwords.

**Gotcha (2026-09-25 live run):** a DevExtreme `dx-selectbox` contains a hidden `<input type=hidden>` *before* the
visible editor input, so a generic `//div[contains(@class,'dx-selectbox')]//input` matches the hidden one and never
becomes clickable. Always target `input.dx-texteditor-input` (or the widget's `id`). The distributor select is
searchable: click, type the distributor code, then click the matching `div[role=option]`. The arrow
(`.dx-dropdowneditor-button`) is the fallback.

**Gotcha 2:** DevExtreme grids scroll horizontally inside the panel. Columns out of view (e.g. SKU Substitution
Policy's *Status*) have empty Selenium `.text`, so read header or cell text with JS `textContent`, not `.text`.

## Menu

- **API:** `GET /menu-service/api/v1/optionGroup/allMenusByRoles` with header `Authorization: Bearer <localStorage.accessToken>`.
  Returns the **role-filtered** menu (KPO_PH: 392 entries) with fields `optionGroupId, parentOptionGroupId, level, seqNo,
  longDescription, appOptionId, pathAngular, pageUrlParam`. Same model as `smm_pr_opg_optiongroups` + `smm_pr_apo_appoption`.
  Dynamic-layout screens have `pathAngular=/dyl/layout` and `pageUrlParam=layoutCode=<code>`.
- **Sidebar:** top-level items are `li#<optionGroupId>` (e.g. `li#NG09` = Transaction). The icon tooltip text is the `title` of the `<i>`.
- **Navigate (most reliable):** click the top-level `li#<id>` → type in the flyout search `input[name=filterText]` ("Search Here")
  → click `li#<childOptionGroupId>` (class `menu-child-node loadPage`). Search matches `longDescription`.

## SDMS-10351 screens (under Transaction / `NG09`)

| Menu text | optionGroupId / appOptionId | Route |
|---|---|---|
| SKU Substitution Policy | `SKU_SUBSTITUTION_POLICY` | `/content-master/mobility/sku-substitution-policy` |
| SKU Substitution Policy View | `SKU_SUBSTITUTION_POLICY_VIEW` | same route + `type=view` |
| SKU Substitution Upload | `SKU_SUBSTITUTION_UPLOAD` | `/excel-upload/sku-substitution-upload` |

### SKU Substitution Policy screen

Breadcrumb `Home > Transaction > SKU Substitution Policy`. Left: grid "SKU Substitution Policy" (DevExtreme) with
"Show filter row" checkbox. Right: "Entry" form.

**Grid columns:** Policy code · Description · Type · Start Date · End Date · Abbreviation · Status.
Rows: `tr.dx-data-row`; select a row by clicking a cell, e.g. `//tr[contains(@class,'dx-data-row')][td[normalize-space(.)='PL000000051']]/td[2]`.

**Form fields** (the `id` attributes are stable; DevExtreme widgets):

| Label | Locator | Widget | Required | Notes |
|---|---|---|---|---|
| Policy code | `#code` | dx-text-box | — | Always read-only; auto-generated (`PL0000000nn`) |
| Description | `#name` | dx-text-box | ✔ | |
| Type | `#type` | dx-select-box | ✔ | Only option: `3 – Based on DT + Channel` (default) |
| Start Date | `#fromDate` | dx-date-box | ✔ | Format `yyyy-MM-dd`, defaults to today |
| End Date | `#dataTo` | dx-date-box | ✔ | Format `yyyy-MM-dd`, defaults to today |
| Status | `#status` | dx-select-box | ✔ | `Active` (default) / `In-Active` |
| Abbreviation | `#abbreviation` | dx-text-box | ✔ | |

**Buttons:** `#add` (Add), `#save` (Save), `#update` (Update), and plain buttons "Download Excel" / "Upload Excel"
(locate by text: `//button[normalize-space()='Download Excel']`).

**Button state (observed):**

| State | Add | Save | Update | Download / Upload |
|---|---|---|---|---|
| Nothing selected (new-entry mode) | disabled | **enabled** | disabled | disabled |
| Row selected | **enabled** (switch to new) | disabled | **enabled** | **enabled** |

**Current policy selected** (PL000000051, start 2026-09-24 ≤ today 2026-09-25): read-only = Policy code, Description,
Start Date, Status, Abbreviation; editable = **End Date** and **Type**. This matches the story ("current policy → only end
date editable"), **except Type stays editable** — a possible defect, or harmless because Type has only one value. Verify.

**Existing data (2026-09-25):** PL000000051 "Automation SKU Substitution Policy Test" 2026-09-24→2026-09-30 AUTOSKU1 Active;
PL000000050 "TEST SKU EXCLUSION" 2026-08-03→2026-08-05 TEST Active.

⚠ **PL000000050 has already expired, and it is still shown in the grid.** The story's line is ambiguous. Our test cases
assumed expired policies are *hidden*, but the app shows them. Confirm the intended behaviour with the BA before
treating either as a defect.

Not yet explored: Download Excel content, Upload Excel dialog and messages, the SKU Substitution Upload screen,
the View screen, validation messages on Save.

## Verified in the group 11 replay (cnr1dev1, 2026-09-29/30)
Details per flow: `framework_flows/`. Each item is observed, not documented by the vendor.

**Order Stock Allocation** (layout 201904)
- Orders are **auto-allocated when an order is saved** (Allocation Status FULL). The screen's default Order Date is today; orders booked yesterday need Order Date typed (send-keys, then Enter) to appear.
- Unallocate (select rows, Unallocate, accept the "Are you sure you want to proceed?" alert) answered **"stock not found."** for all 9 orders, also for the 8 new ones alone; nothing changed. Cause unknown; open question for the framework owner / BA.

**Order Editing / Order Cancellation**
- With a date range covering the order dates, the Outlet Name list stays empty for orders that show as Allocated. The outlet API (`getOultetsForOrderEditing`) returned `[]` for the PJP/section/category, while a wide range returned older outlets. Observed correlation with allocation; not proven (unallocation failed).
- Date fields typed in the DOM are ignored by the app's model; the requests still carried today's date. Type them with key events.

**Delivery Date Change** (layout 201080)
- Changing Order Date resets the PJP to another one: choose PJP `02111~AutomationOB1` after the date. Selecting all rows and Process (accept the alert) answered `Delivery Date has been changed successfully, processed orders: 9`.

**Goods Issue Note** (`/ngui/good-issue-notes/GIN`)
- Master grid first; the **Add** button opens the header form. Header: Delivery Man PJP `02112-AutomationDSR` -> DSR, Warehouse and Vehicle fill in by themselves (vehicle `0040-Automation211206`, the framework lists `74-Sect to Locus`); GIN Date is today; Delivery Date must be typed. Suggested Type defaults to Cashmemo List.
- **Cash Memo Selection** tab lists the eligible cash memos (9 here); the header checkbox selects all. **Detail** tab shows the SKUs (Current Stock, Suggest, Actual) and the **Save All** button (`saveallBtn`): `Saved successfully.` The header form clears after the save; the new GIN (505) appears in the master grid as Draft / In-Active.
- Open the GIN from the master grid (click the GIN No. cell), then click the `#forward` dx-button; the Comments popup needs text, a blur (Tab), then Save: `Forwarded successfully`; Approval Status becomes Pending for approval.
- The checker (Auto_Tssm) approves on the same screen with the same Forward action. On 2026-09-30 it failed with **"No stock balance found for products: [20050308, 20050310, 62690363, 62740537, 69997598]"** because stock had been received the previous calendar day (09-29): stock balances are keyed by date. **A cycle that creates stock and issues it must run within one calendar day.** The Generate Opening Balances button in Stock Inquiry may be the remedy; it changes stock and was not used.

**Login and session**
- After Company, a Distributor dropdown appears. A new login clears localStorage (the injected helper); re-inject after each login. Logout: click the user name in the header, then `li#logout`.
