# QA OS — status at end of session (Friday 2026-09-25) — resume on Monday

## 1. The goal (unchanged)
A QA user gives Claude a Jira story. Claude turns it into test cases and steps, **runs the flow itself through the Selenium/Vibium MCP**,
records screens, menu paths, element ids and messages, and generates the **`CTA_CONFIG_ASSERTION` SQL** (+ case-data workbook) for the
**legacy Regress framework**. A person reviews and applies the SQL; the QA team then runs the flow in the legacy framework. QA users write no code.

**Working rules agreed:**
- The QA user logs in **once** in the browser Claude opens. Claude **never types passwords**, so login is always a human step.
- Claude executes through the **MCP**, not by asking people to run Python commands. (The Python player was an interim workaround.)
- No user guide exists for any app: knowledge comes from DB metadata + the live app + Jira stories.
- One data row per case while Claude executes; bulk data is generated only for the legacy engine.
- SQL is **never auto-applied**: always a reviewed file.
- The platform must work in other QA members' Claude environments (plugin, no machine-specific paths).

## 2. Phase status
| Phase | Status |
|---|---|
| P0 Foundation | Done |
| P1 Story → cases → steps | Done (SDMS-10351: 53 cases with steps) |
| P2 Execution and test data | **Closed** (see §4); order/business-effect cases wait for QA fixtures, uploads deferred |
| P3 Framework scripts + bulk data | **Started**: first SQL draft + case data generated, not yet validated in the framework |
| P4 Handover to QA team | Not started |

## 3. What exists (all under `C:\MyWork\gias-qa-workspace\qa-os`)
| Path | Content |
|---|---|
| `docs/ARCHITECTURE.md` | Full design (agents, app packs, tiers, hooks, bulk data §13A) |
| `plugins/qa-os/` | Agents (app-cartographer, story-analyst, test-designer, step-author, data-engineer), skills (qa-orchestrator, step-dsl), commands, schemas |
| `apps/snd/` | S&D app pack: `app.yaml`, observed screens, knowledge (menu, i18n, data dictionary, **sweep of 314 screens**), flows, tools |
| `apps/snd/knowledge/sweep/cnr2dev3.KPO_slv.json` | Whole-app read-only sweep: 314/314 screens, 3,300 fields, ids, buttons, grids |
| `apps/snd/knowledge/screens_observed/` | One file per swept screen |
| `framework/cta_config_assertion.md` | Legacy framework schema map + case-data contract (verified with real workbooks) |
| `framework/tools/gen_framework_sql.py` | Flow spec → SQL + rollback + case-data workbook + review sheet |
| `runs/SDMS-10351/20260925-1214/` | The pilot run: requirement, cases, steps, workbook, exec results, `framework/` SQL draft |
| `runtime/` | Interim Python helpers: player, run manifest, workbook renderer, data resolver, doctor |

## 4. SDMS-10351 pilot outcome
- 53 cases: **12 Passed, 6 Failed, 35 Not Executed** (22 upload cases deferred by decision; TC44/47/48/50 stay manual; TC43/45/46/49/51/52 need QA fixtures).
- **Two real app defects found** (raise with the BA/dev): (1) an **expired policy (PL000000050) is fully editable** with Update enabled;
  (2) **Type stays editable on a current policy** (story says only End Date).
- **Story questions for the BA** (in the workbook's Notes sheet, AMB1–AMB14): expired policies listed in the grid (AMB1); Type editable (AMB3);
  policy grid not per distributor (AMB10); download's Entity Code is the earlier uploaded DT, not the login DT (AMB11); Status shown Yes/No (AMB12);
  headers-only upload accepted (AMB13); generic upload error message (AMB14); template has a code column, no description (AMB4).
- Rules **R10, R13 and the R14 overlap rule have no automated case** while uploads are deferred: QA must cover them by hand.

## 5. Framework SQL draft (the main deliverable so far)
`runs/SDMS-10351/20260925-1214/framework/`: `framework.sql` (14 INSERTs, one transaction, pre-flight id check, rows tagged `QAOS-SDMS-10351`),
`framework_rollback.sql`, `NG_Dcode_QA_SDMS-10351.xlsx`, `framework_review.md`, `flow_spec.json`.
Ids: menu group **0611**, screen **061101**, flow **06110001**; master_app_id **1**. Covers **create policy** only.
**Not validated yet**: needs a Framework admin to apply it to a *test copy* of `CTA_CONFIG_ASSERTION`, place the workbook in `<BASE_PATH>\casedata\`
(BASEPATH_1 config; the DB has no base path for app 1), and run flow `06110001` once.

## 6. Environments and users (passwords only in the gitignored `.claude/settings.local.json`)
| Env | URL | User | Notes |
|---|---|---|---|
| cnr2dev3 | https://dcodecnr2dev3.unilever.com/ngui | **KPO_slv**, distributor **50000451** | Has SKU Substitution screens **and** working Order Booking. Best default. Offered distributors: 50000451, 50000598, 50000599 |
| cnr2dev3 | same | KPO_ph (15181887, 50200411, 50200779) | SKU screens present; Order Booking dropdowns empty |
| cnr1dev1 | https://dcodecnr1dev1.unilever.com/ngui | KPO_mp (no distributor) | Order Booking works; **no SKU Substitution screens**; 437 openable screens |
Password keys: `SD_TEST_USER/SD_TEST_PASSWORD` (KPO_ph), `SD_PASSWORD_KPO_MP`, `SD_PASSWORD_KPO_SLV`.
Test data left on cnr2dev3: policies PL000000052 ("QAOS TC07 auto sub exclusion", 2026-10-05..15). The base DB `snd-schema` (ng_astrone) has **no PH data** and no SKU Substitution tables.

## 7. Open items
**Waiting on you**
- Review `framework.sql`; find someone to apply it to a test framework DB and run flow 06110001.
- A **second story** to run as a QA user (the plan for Monday).
- **Jira SDMS access** (the Atlassian account authenticates but can't see the project; pasted exports used meanwhile).
- **QA fixtures** for the order cases (`runs/SDMS-10351/20260925-1214/QA_FIXTURES.md` + `fixtures.json`).
- BA answers to the story questions (§4).
**On my side**
- Build the **recorder**: Claude executes steps through the MCP and produces `flow_spec.json` (then SQL) automatically. Today the spec is written by hand.
- Sweep KPO_mp/cnr1dev1 and KPO_ph; a **tab pass** for tabbed screens (Outlet Profile shows ~30 of 83 fields on the first tab); dropdown options.
- SQL for the remaining SKU flows (update-policy TC36–42) and order flows once fixtures exist.
- Bulk-data-factory for the legacy case-data workbooks (contract is verified in `framework/cta_config_assertion.md` §5.1).
- Wrap the MCP-driven execution into the plugin agents/skills (P4) and retire the Python player.

## 8. Plan for Monday
1. You paste the **second story**; we run it the way a QA member would: story → questions → cases/steps → you log in once → I execute via MCP →
   recorder → SQL + case data → review note. Measure friction (rounds, manual fixes, SQL shape vs existing flows).
2. In parallel, the framework owner validates the SKU draft.
3. Pick up fixtures / BA answers / Jira access as they arrive.

## 9. Gotchas learned (details in `apps/snd/knowledge/ui.md` and `sweep/README.md`)
- DevExtreme: `dx-selectbox` has a hidden input first; off-screen grid headers need `textContent`; text boxes commit on blur (press Tab); grids can be paged without a next arrow.
- Sidebar clicking is fragile; **navigate directly by route** (`history.pushState` + `popstate`) inside the page.
- Description validation: max 100, **no special characters**; the message shows only on hover of the field's error icon.
- Order Booking date is read-only = today. Order flow: PJP → Selling Category → Section → Outlet → `Order Detail` → lines (`New Order`, `Add a row`); Save not yet seen.
- Legacy rows use button ids `saveBtn/updateBtn`; the current app uses `save/update`.
- Windows: Git-Bash `/tmp` paths are not visible to Windows Python; use the Windows Python at `C:\Users\syed.kamran\AppData\Local\Python\bin\python.exe`.
- The Selenium MCP browser is closed; the user logs in again when needed (the logout menu isn't reachable from the distributor page).

---
# Update: Monday 2026-09-28 (Van Sales run) — resume here

## Decisions made today
- **Cap: at most 10 core test cases per story**; the rest go to a backlog (kept in cases.json, promoted later). Design change to the test-designer: emit <=10 core cases, each adding a new flow/screen/rule.
- **MCP execution is a one-time recording per flow** (one data row), not a regression run. The legacy engine runs all cases and data variations. Only run an MCP recording when the script needs an id, path or real message we do not have yet.
- **Minimise user intervention**: only login (and stock-changing / BA decisions) need the user. Every obstacle goes to `friction.md` with the software fix.
- Environment for Van Sales: **cnr1dev1 as KPO_mp** (Unilever). Navigation there = sidebar search box + click (pushState does not work).

## Van Sales run: `runs/VAN-SALES-E2E/20260928-1012/`
Stages done: analyse (39 rules, 13 ambiguities), cases (42 = 10 core proposed + backlog), steps, execute (recording), scripts. Not done: data, bulk.
Files: `requirement.json`, `cases.json`, `steps.json`, `exec/results.json` (7 ready cases: 4 passed, 2 failed, 1 blocked), `live_findings.md`, `friction.md`, `framework/` (`recording_create_request.json`, `flow_spec.json`, `framework.sql` 13 INSERTs, `framework_rollback.sql`, `NG_Dcode_QA_VAN-SALES-E2E.xlsx` 3 rows, `framework_review.md`). **Nothing applied.**
Test data left on cnr1dev1: Van Sale Stock Requests **20260000000570** (PJP FARSSPJP01, LUX 2 CS + SURF EXCEL 1 CS) and **20260000000571** (PJP HBVANPJP01, LUX 1 CS), both Drafts (grid says "New"). Fixture: PJP FARSSPJP01 / HBVANPJP01, warehouse C0000000001 M&P Main; products with stock LUX 67648757, SURF EXCEL 68383414.

## Story variances to send to the BA (live app vs story)
"Van Seller" DSR type is "Van Sales"; no Reference PJP field on PJP Creation HQ; grid columns lack PJP Code/DSR Code/GIN No; buttons are Add/Submit/Cancel (no New/Delete/Forward); status shows "New" (Draft); no request-level Delete (lines only Edit); no Picklist Reference on the GIN; only one Draft per PJP.

## What was built today
- `plugins/qa-os/runtime/qaos_helpers.js` (injectable page helper + action log; tested live) and `framework/tools/qaos_record.py` (log + meta -> flow_spec.json).
- Rule saved to memory: minimise user intervention.

## Next (in order)
1. Framework owner reviews `framework.sql` (Van Sales) and the earlier SKU one; applies to a test copy; runs flows 06120001 / 06110001.
2. Reduce cases.json to 10 core + backlog; record the missing small flows (DSR Type option, Reference PJP absence, Route Settlement PJP list) with the helper.
3. Build fixture discovery (read APIs with the page token) and the known-variance / app-rules registry in the app pack; session probe + one re-login.
4. Stock-changing flows (Forward/Submit, GIN approval): author, mark unverified, record only with the user's explicit OK.
5. Query snd-schema for stock-request status codes (Draft vs New) and document status table when the tool is available.
6. Wrap the helper + recorder into plugin skills/agents; retire the Python player.
Gotchas: sessions expire after a long idle gap (re-login); UI steps must run one at a time; toasts vanish in <1 s (use clickCapture); duplicate ids (`Cancel` is also the Submit id); switching Header/Detail before Save discards lines.

---
# Update: Tuesday 2026-09-29 (knowledge layer)
- Ran a read-only inspection of snd-schema: `apps/snd/knowledge/db_inspection_2026-09-29.md`. Key facts: orgs = markets (010104 Unilever Pakistan, 010105 Bangladesh, 0101/0102 Danone Indonesia, 99 Global); KPO_MP = Pakistan; DB has no Van Sales tables; per-role button permissions are not in the DB (screen-level only).
- Built the **access knowledge layer** `apps/snd/knowledge/access/` (screens, menu tree, role->screens, users (e-mail codes masked), per-org feature flags) + tools `access_lookup.py` (screen / user / who / features / diff-features / validate-live) and `build_access.py`. DB covers 83% of KPO_MP's live menu; 73 live screens are newer than the DB (incl. Van Sales).
- Also this session: `cases.json` cut to 10 core + 32 backlog; read-only recordings of TC02/TC05/TC26; `BA_NOTE.md` written; `docs/QUESTION_BANK.md` (question checkpoints + story intake block).
Next: wire access_lookup into the orchestrator (pick the user for a story automatically, C0/Q-ENV-2); add non_production flag + intake-block parser; get a newer data dictionary for Van Sales; extract data-authority scope.
- **Orchestrator wired to the access layer (v0.3):** skill `plugins/qa-os/skills/qa-orchestrator/SKILL.md` now has Stage 0 (read intake block, `access_lookup.py plan-user ... --org` picks env/user from live menus + DB + `account_notes.json`, authorization only on `non_production` envs). New: `plan-user` command, `knowledge/access/account_notes.json`, `app.yaml` (`org`, `non_production`, `access:` block). Not built yet: an automatic intake-block parser (Claude reads it), decisions.md promotion, per-role button permissions.
- **Intake parser + promotion built (2026-09-29):** `runtime/qaos_intake.py` (parse / answer / show -> `decisions.json`, schema `plugins/qa-os/schemas/decisions.schema.json`), `runtime/qaos_promote.py` (dry run by default, `--apply`, conflicts kept for review, status observed < stated < ruled, provenance), app-pack file `apps/snd/knowledge/decisions.json` (seeded with 1 observed term and 2 observed rules). `qaos_run.py validate` now checks `decisions.json` and the 10-core-case cap. Tested on 3 scratch stories (full block / no block / block naming an account that lacks the screens) and on promotion (add, upgrade, duplicate, idempotent second apply); the real app pack and the real Van Sales run were not modified. Not yet run on the real Van Sales run (no intake block was written for it). Next: try the flow on the next real story; extract data-authority scope; per-role button permissions need the live app.
- **Van Sales intake run (2026-09-29):** intake block appended to `runs/VAN-SALES-E2E/20260928-1012/inputs/story.md` (written by Claude at the QA lead's request; review before reuse); real `qaos_intake.py parse` OK (`decisions.json`; KPO_mp verified against 6/6 screens; allow create+save, never forward/approve/delete); `validate` all OK. Promotion **applied**: term "Van Seller = Van Sales" now `stated` in `apps/snd/knowledge/decisions.json` (+ `decisions.md`). Intake `expected-variance` lines are no longer promotable (release-specific): only a reusable BA ruling promotes a variance.

## What is needed from the user next (priority)
1. A framework owner to apply `framework.sql` (Van Sales flow 06120001, SKU flow 06110001) to a test copy of CTA_CONFIG_ASSERTION and run the flows: nothing is validated in the legacy engine yet (critical path).
2. Send `runs/VAN-SALES-E2E/20260928-1012/BA_NOTE.md` to the BA; record answers with `qaos_intake.py answer ... --owner BA --reusable`, then `qaos_promote.py --apply`.
3. A second real story with an intake block: first true end-to-end test (target: login only).
Optional: OK to record Forward / GIN approval (stock-changing); a newer data dictionary that includes Van Sales tables; Jira SDMS access; change the KPO_mp password (it was pasted in chat).

---
# Update: 2026-09-29 (Dispatch Advice replay + step vocabulary)
- **Framework replay started (Dispatch Advice, flow group 11 "Daily Cycle Only Positive Flow")**: read the framework tables (`apps/snd/knowledge/framework_flows/DISPATCH_ADVICE.md`), ran the DA slice live on cnr1dev1: DA **570** created (M&P Main Warehouse, as KPO_mp; Automation login was invalid), 4 lines, 1 loss row, forwarded, approved by the same user (deviation). Then found the automation data lives under distributor 15108843 (login Auto_Tssm, which is approve-only: "Current user is not authorized to save this record!"). The DA slice is NOT yet run as designed (maker + separate checker, Auto Main Warehouse, workbook quantities): needs a maker login (Auto_Multi_Orga or Automation).
- Framework drift found: rowEditBtn_Save_0 assumes row 0; loss modal save has no toast; `forwardBtn` wrapper needs inner-button click; comment needs blur; gridFilterCheckbox is a toggle.
- **Standard step vocabulary** (`docs/STEP_VOCABULARY.md`), **S&D step library** (`apps/snd/steps/library.yaml`: 21 business steps (17 verified live), actors Maker/Checker/StockController/HeadOffice, DA screen ids, real messages, `verified` flags) and **QA guide** (`docs/QA_GUIDE.md`) created; skills updated. Rules from the QA lead: maker-checker with an explicit switch point (Logout, Login as <role>); approval = same Dispatch Advice option, different user, just approve.
- Not built yet: parser/compiler from business steps to DSL/player (the library is the specification; Claude executes it by hand for now); `switch_user` and `filter_grid` primitives; steps.schema.json still lists DSL v1 verbs only.
- **DA slice complete (2026-09-29):** DA 1350 created+forwarded by Maker (Auto_Multi_Orga), approved by Checker (Auto_Tssm), stock validated by Stock Controller (Auto_Multi_Orga): `apps/snd/knowledge/framework_flows/TC-DA-01_executed.md` (TC-DA-01 pass, TC-DA-02 partial: framework assumes a clean day; loss stock needs the skipped Loss Approval). Chain continues with Order Booking (0001), Stock Allocation (0013) ... as Auto_Multi_Orga.
- **Order Booking executed (2026-09-29):** order COL26000001995 via framework flow 00010001, totals equal the workbook (gross 143,109.13, net 134,999.00): `apps/snd/knowledge/framework_flows/TC-OB-01_executed.md`. Chain progress: DA (created/forwarded/approved/loss-approved) -> stock validation -> Order Booking done; next Stock Allocation (0013) as Auto_Multi_Orga.

---
# Update: end of 2026-09-29 (Dispatch Advice cycle replay) — RESUME HERE TOMORROW
## What happened today (details in `apps/snd/knowledge/framework_flows/`)
- Built: access knowledge layer, intake parser + promotion, question bank, step vocabulary + S&D step library + QA guide, orchestrator v0.3 (see earlier sections).
- **Replayed the framework's Pakistan "Daily Cycle" (group 11) on cnr1dev1 through the browser**, reading `fct_pr_gtfd_group_test_flow_detail` (semantics: plu_serial_no = user, login_status Y = log out and log in as that user; 10 switch points in the cycle). Done: DA create/forward (Auto_Multi_Orga) -> DA approval (Auto_Tssm) -> DA loss approval (Auto_Tssm) -> stock validation -> Order Booking (8 orders COL26000001995-2002, all totals = workbook) -> Stock Allocation -> Transaction Inquiry check. Executed test cases: `TC-DA-01_executed.md` (TC-DA-01..03), `TC-OB-01_executed.md` (TC-OB-01..03). Full log: `DISPATCH_ADVICE.md` (parts 1-9), session plan for the whole cycle inside it.
- **Blocked at chain seq 15 Order Editing**: Outlet Name list is empty ("No data to display") for the automation PJP with today's dates. Draft step sheet with all open questions: `STEP_SHEET_DRAFT_next.md`.
## Decisions from the QA lead
- Standard step vocabulary; maker/checker with explicit switch points (Logout, Login as <role>); approval = same option, different user.
- Claude never types credentials (user id or password); it logs the window out and the QA lead logs in at each switch.
- **QA should provide/approve the test steps (a step sheet) before execution to avoid back-and-forth**; Claude drafts it from the framework tables and marks steps "clear" / "needs input".
## Data left on cnr1dev1
DA 570 (M&P, KPO_mp; approved by the same user, deviation), DA 1350 (Auto KARACHI, Auto Main Warehouse; approved), loss record 637 approved, orders COL26000001995-2002 (8, Confirmed, allocated; delivery date 2026-10-05), order COL26000001988 allocated by the allocation step. Van Sale Stock Requests 20260000000570/571 (Drafts, KPO_mp) from Monday.
## Findings for the framework owner (collected; each in the TC files)
Loss modal save has no message; `rowEditBtn_Save_<row>` index; `forwardBtn` wrapper vs inner `forward`; comment needs blur; `gridFilterCheckbox` toggle state; workbook Reference Number 100 collides on rerun (field inactive in framework); stock validation assumes a clean day and loss stock (Damaged/Lost) not seen in Stock Inquiry after loss approval (open question); auto-allocation at order save vs manual allocation flow; Order Editing/Cancellation outlet list empty (suspected delivery-date range); `Automation` login rejected; maker user not named in the tables.
## Tomorrow
1. QA answers the 4 questions in `STEP_SHEET_DRAFT_next.md` (esp. Order Editing/Cancellation, unallocation, delivery date).
2. Continue the cycle from seq 15 as Auto_Multi_Orga (browser must be logged in again; the session was closed), then GIN, then the switch to Auto_Tssm (seq 23).
3. Still open from before: framework owner validates the SKU and Van Sales SQL drafts; BA note for Van Sales; loss-stock location question; the maker default user.
Tools/gotchas: in-page order booking routine (type-ahead via key events, run in background and poll, tool call limit ~30 s); helper is lost on every new login (re-inject); real clicks needed for tabs and the filter checkbox; browser alerts (Allocation) are accepted with the alert tool.

---
# Update: 2026-10-01 — v0.4.0 released; PAUSED for user to learn the app; account switch pending

**If you are a new session picking this up (possibly a different Claude account): read this whole section before doing anything.** Don't re-run learning-mode agents or re-derive what's already written — read the files named below instead.

## What exists now (all shipped in `qa-os/`, which is its own git repo, tag `v0.4.0`)
- **The plugin**: 8 agents (`story-analyst`, `test-designer`, `step-author`, `data-engineer`, `app-cartographer`, `recorder`, `framework-generator`, `verifier`), 8 skills, 6 commands. Loads from a **versioned plugin cache** — editing files alone does nothing; see `DEPLOY.md` §4 to bump/reload.
- **Assisted step authoring + Excel round trip**: `vocabulary/core.yaml` (predefined step words), `runtime/qaos_steps.py` (checks a step against the real screen labels), `runtime/qaos_export.py` / `qaos_import.py` (Claude drafts → QA member finalizes in Excel's Test Steps column → Claude imports+checks → executes from exactly that). QA cheat sheet: `docs/QA_STEP_CHEAT_SHEET.md`.
- **Business knowledge** (the closest thing to a user guide that exists — **read `apps/snd/knowledge/business/INDEX.md` first**):
  - `apps/snd/knowledge/business/` — 23 pages across 4 areas (inbound stock, order→delivery planning, delivery & returns, settlement & finance) + `glossary.md`, `document_lifecycle.md`, `OPEN_QUESTIONS.md` (52 open items: 14 safe-default, 25 verify-live, 13 genuine BA decisions, each with a default — none blocks work), `LIVE_LEARNING_CHECKLIST.md` (33-item live-verification plan, items L01-L12 done, L13-L33 not done), `LIVE_FINDINGS.md` (raw evidence log).
  - `apps/snd/knowledge/framework_atlas/` — the whole legacy framework (`CTA_CONFIG_ASSERTION`) mapped: 31 groups, 547 flows, 1,477 screens. `apps/snd/tools/build_atlas.py --find "<text>"` looks up a flow by business term.
  - `apps/snd/knowledge/screens_observed/LIVE_*.json` — 23 real screens harvested live (fields, buttons, grids, messages).
- **One verified end-to-end case**: Dispatch Advice create→add line→forward (maker)→approve (checker), recorded live, framework SQL generated and independently reviewed 4 times (`runs/PILOT-DA-GIN/20260930-1615/`, `review.md`..`review_v4.md`). SQL has never been applied/replayed in the legacy engine — that's still open.
- **Release packaging**: `RELEASE_NOTES.md` (what's in v0.4.0 + 5 known issues), `DEPLOY.md` (install/update/rollback steps for the QA team). Distributable archive: `C:\MyWork\gias-qa-workspace\dist\qa-os-v0.4.0.zip`.

## The one big fact learned today (now baked into the knowledge pages, don't re-discover it)
**Stock and orders are keyed by calendar day.** A Dispatch Advice approved "yesterday" does not carry its stock into "today" (Opening resets to 0 for anything not received that same day), and a Goods Issue Note is refused if its cash memos' delivery date is before the PJP's current working date (exact message: *"cashmemo(s) found with delivery date earlier than the pjp working date"*). **The whole receive → order → issue chain (Dispatch Advice → Order Booking → Delivery Date Change → GIN → ...) must run inside one calendar day**, with fresh same-day data every time. This blocked the group-11 Pakistan replay twice (2026-09-30 and 2026-10-01) and is why the cycle needs restarting fresh rather than resumed from stale data.

## Why we're paused (not a technical blocker — a deliberate pause)
The user wants to personally build understanding of the application (as Maker, Checker, and themselves) before continuing, since no vendor user guide exists — using the business knowledge pages above as a head start. They are also switching from a personal Claude account (usage running out) to their company's Claude Team subscription. **Do not auto-resume live-walk/learning-mode agents.** Wait for the user to say they're ready.

## What does NOT travel with a plain file copy / account switch (tell the user if relevant)
- Claude's cross-session memory (`~/.claude/projects/.../memory/*.md`) is local to this machine/OS profile, not the Claude account — should still load in a new session on this same machine regardless of which email is signed in, but has never been verified to survive an actual account switch.
- `runs/` (raw execution evidence, incl. `PILOT-DA-GIN/`) is gitignored — not shipped in the git repo or the zip. Only what got distilled into `apps/snd/knowledge/` travels.
- MCP server connectors (`snd-schema`, `selenium-framework-db`, `selenium`, `gias-schema`, Atlassian) are configured in Claude Code's own settings, not in this repo — must be set up fresh per machine/account. The user is setting these up themselves on the Team account.
- Credentials (`~/.qa-os/credentials.json` or env vars) — per-person, never shared, never typed by Claude.

## Exact resume plan (once the user says go)
1. Quick health check: `python runtime/qaos_doctor.py` (expect READY), `python runtime/qaos_config.py validate` (expect OK), confirm the plugin's 8 agents are loaded (call an unlikely agent name — the error lists what's loaded).
2. Confirm `apps/snd/knowledge/business/OPEN_QUESTIONS.md` — ask if the user got any BA answers while learning; apply them (`qaos_promote.py` pattern) if so.
3. Restart **Daily Cycle Only Positive Flow, Pakistan market, group 11, env cnr1dev1** from the top (Login → Dispatch Advice) with a **fresh same-day** data set — do not reuse DA 1353-1357, GIN 505, or any prior-day document. Honor the one-calendar-day rule above from the start: plan the whole session (DA → orders → delivery date → GIN → returns → settlement) to run in one sitting, one day.
4. Logins are still never typed by Claude — ask for Maker (`Auto_Multi_Orga`) first, Checker (`Auto_Tssm`) at the switch points, per `apps/snd/app.yaml` roles.

---
# Update: 2026-10-01 evening — learning session G11-PK 1 done (stopped at seq 51) — RESUME HERE

**Read first:** `apps/snd/knowledge/business/learning_sessions/2026-10-01_G11-PK_session1_report.md` (what was walked, rules learned, defects, framework drift, open questions, resume plan). Raw per-flow facts: `..._session1_log.md` in the same folder.

## Done today (after the v0.4.0 pause; the QA lead resumed work in this session)
- **Learning standard** written: `docs/LEARNING_STANDARD.md` (output contract L1-L4, confidence tags incl. new `[stated]`, pluggable sources, phases, G0). ARCHITECTURE §7A points to it. Not built yet: `app-learning` skill, `learning:` block in app.yaml, page front-matter + INDEX.json, coverage checker (§10 backlog).
- **Roles simplified** (QA lead): only **Maker** and **Checker**, several users each. `apps/snd/app.yaml` cnr1dev1: Maker = [Automation, Auto_Multi_Orga], Checker = [Auto_Tssm]; `runtime/qaos_config.py` + `qaos_player.py` accept lists; vocabulary/library/skill updated; plugin bumped to **0.4.1** (needs `claude plugin marketplace update qa-os` + `claude plugin update qa-os@qa-os --scope project` + restart).
- **S&D navigation** recorded in app.yaml `menu:` (top-left hamburger `#menurollin` -> Search Here -> item; ignore the Kaspersky cert notice on the home page).
- **Learning walk of group 11 (business facts only, no ids)** on cnr1dev1, one calendar day: seq 1-50 walked (seq 15 skipped by the QA lead for QA/BA discussion; seq 18 done on one order; deposit slips with real numbers), stopped at **seq 51 Route Settlement: "Following previous days not closed! Please close date. 2026-09-30"**.

## Next (in order)
1. QA lead / BA: answer **Q-RS1** (how to close a working day; may 2026-09-30 be closed?) and Q-OE1/Q-OE2 (Order Editing) — listed in `apps/snd/knowledge/business/OPEN_QUESTIONS.md` §8.
2. ~~Consolidate~~ **DONE 2026-10-01 evening**: session log merged into all touched L3 pages (front-matter added, [Maker]/[Checker] steps with trace keys, test hints, questions), glossary (+17 terms), document_lifecycle (§0), INDEX, LIVE_LEARNING_CHECKLIST, OPEN_QUESTIONS §8 (18 new questions; not renumbered yet). Still to do: coverage report + G0 sign-off request for inbound stock and order-to-delivery.
3. Finish the cycle (seq 51-71) on a **fresh day from seq 1** (stock/day rule) once the day-close question is settled; today's documents (DA 1358, orders 2003-2008, GIN 506, return 713, slips 1131-1136, GRN 246) must not be continued on another day.
4. Then other groups (positive/negative) as the QA lead requests, same standard.

## Gotchas learned today (for the recorder / replays)
- Logins must be done in the **Selenium-controlled window**; one login landed in another browser.
- DevExtreme grids: number inputs go stale on clear -> click the cell, select, press keys one by one; checkbox cells need scrollIntoView; fixed-column grids duplicate links (click by position).
- Dropdown option clicks can land on the neighbouring item (verify with elementFromPoint before clicking); cascades clear the fields below.
- Multi-cheque popup dates must be typed MM/DD/YYYY; other dates yyyy-mm-dd.
- Menu deep links redirect to the menu; after clicking a menu item the side menu may stay open over the page.

## Planned: Senior QA knowledge check (QA lead, 2026-10-01)
After the positive cycle (group 11) is completed through its last active flow, **seq 71 "Transaction Inquiry Validate After Sales Return" (03770001)**, a **Senior QA user** will test Claude's S&D business knowledge. They give test cases; Claude states the **expected output first** (from the knowledge pages, with confidence tags), executes the case live, and the result is compared. Misses go back into the knowledge pages. Prerequisites: seq 51-71 walked, plus the Consolidate phase done. This works as the human check for gate G0 of docs/LEARNING_STANDARD.md.


---
# Update: 2026-10-05 - learning session G11-PK 2 (fresh full run) stopped at seq 51 - RESUME HERE

**Read first:** `apps/snd/knowledge/business/learning_sessions/2026-10-05_G11-PK_session2_report.md` (flows, confirmations, new findings, left-over documents, resume plan); raw log `..._session2_log.md`; Order Editing screenshots in `learning_sessions/screenshots/`. Operating rules and the QA lead's standing preferences: `docs/OPERATING_RULES.md` (copied from the assistant's account memory so a different Claude account has them).

## State
- Seq 1-50 walked again on one day (2026-10-05); every number and message matched session 1. Seq 15 Order Editing skipped again (QA lead). Stopped at **seq 51 Route Settlement**: "Following previous days not closed! Please close date. 2026-10-01".
- **Waiting for the QA team**: Q-RS1 (how to close a working day; 2026-10-01), Q-OE1/Q-OE2 (Order Editing delivery-date filter / how seq 15 reaches its order).
- Documents of today (DA 1359, orders 2009-2014, GIN 507, return COL26000000714, slips 1137-1142, GRN 247) must not be reused on another day.

## Next
1. QA answers -> apply to OPEN_QUESTIONS and the pages. 2. Continue from seq 51 (check whether Route Settlement for 2026-10-05 still opens on a later day, else rerun from seq 1 on a fresh day). 3. Seq 52-60, 68-71. 4. Consolidate session 2 into the pages, renumber questions, coverage report, G0. 5. Senior QA knowledge check after seq 71. 6. Still open: `qaos_login.py` failed for Auto_Multi_Orga (ask for the terminal error); plugin 0.4.1 not reloaded (`claude plugin marketplace update qa-os`, `claude plugin update qa-os@qa-os --scope project`, restart); qa-os changes not committed to git.

---
# Update: 2026-10-05 afternoon - group 11 PK walked to the END (seq 71) - RESUME HERE

**Read first:** `runs/LEARN-G11-PK/20261005-RS/session_log.md` (seq 51-71, same calendar day as session 2's seq 1-50).
- QA lead: earlier days had been left un-closed; a QA team member closed them (more detail promised). **Day close = PJP Daily Inquiry Update (DYL_BG1022): Mark Status End Of Day + DSR Files Status Complete -> Current Status E.** Route 02112 for 2026-10-01 and 2026-10-05 is settled (Complete) and closed.
- Seq 51-54 read after settlement (slips Posted, cheques Clear, Offset = slip allocations); 55 Cheque Status and 56 DSR Adjustment BYPASSED (QA lead); 57 day close done; 58-59 SAN 96 created/forwarded (Maker) and approved (Checker); 60 stock Out +50; 68-71 Transaction Inquiry: edited-order tax/detail/offering match the workbook, header Tax of seq 70 and all sales-return values in the workbook are stale (drift).
- Claude Code auto mode blocked typing amounts on the shared env; the QA lead switched the session to Ask permissions (blocks stopped).
- Documents added today: SAN 96 (Approved). Browser closed after logout.
## Next
1. ~~Consolidate~~ DONE 2026-10-05 (pages, OPEN_QUESTIONS renumbered 56 open, FRAMEWORK_DRIFT.md 26 items, coverage report learning_sessions/2026-10-05_G11-PK_coverage_report.md). Next: QA lead G0 review per area (settlement not ready).
2. Senior QA knowledge check (predict, execute, compare).
3. Still open: QA lead's detailed day-close note; Q-OE1/Q-OE2 (seq 15); framework drift list for the framework owner; qa-os changes not committed.

---
# Update: 2026-10-05 evening - NG_Setup Flow_PK (framework group 66) learning walk, paused after seq 18 - RESUME HERE
**Read first:** `runs/LEARN-G66-PK/20261005/session_log.md` (status table at the end) and `run_sheet.md` (atlas + NG_Dcode_QA_Setup.xlsx, now in framework/casedata-samples/).
- Method (QA lead): user per row from the group query (memory reference-group-users-query; never select plu_password); per screen follow fct_pr_sef_screen_events_flow active rows + active fields; positive workbook rows.
- Seq 1-18 done except seq 4 Forward / seq 5 (Prospect Outlet Forward disabled). App pack: user `headquarter` (role HeadOffice) added to apps/snd/app.yaml for seq 32-34.
- Outlet 1000000001 (group 11 outlet 01) was changed by seq 13-16 with the QA lead's OK: NTN number + now Registered / Tax Payer No -> group 11 tax for outlet 01 may change.
- Next: session with the QA Team Lead (session-3 plan for group 11 + group 66 questions), then resume group 66 at seq 19 Distributor Mapping (Auto_Multi_Orga).

---
# Update: 2026-10-06 - group 11 PK session 3 COMPLETE (full seq 1-71 with the QA Team Lead) and consolidated - RESUME HERE

**Read first:** `apps/snd/knowledge/business/learning_sessions/2026-10-06_G11-PK_session3_report.md` (walk, documents, rules, questions, drift, G0 readiness per area); raw log `..._session3_log.md` (copy of `runs/LEARN-G11-PK/20261006/session_log.md`).

## State
- Group 11 (Daily Cycle Only Positive Flow, Pakistan, cnr1dev1) walked **end to end in one calendar day (2026-10-06) WITH the QA Team Lead**: all 46 active rows. Seq 15 Order Editing ran for the first time. **Route Settlement was performed by Claude.** Seq 55 was a check only. Seq 56 was saved. The day was closed (E).
- **Consolidated 2026-10-06** into the business pages:
  - all four areas, glossary, document_lifecycle, INDEX, LIVE_FINDINGS (incl. defect D-G11-3-1), FRAMEWORK_DRIFT (section 2b, rows 27-36);
  - OPEN_QUESTIONS: now 47 open = A 15 + B 19 + C 13 (1a 12, 1b 1).
- QA Team Lead answers applied:
  - Q-OE1 / Q-OE2 / Q-OE4: Order Editing lists only unallocated orders with delivery date today. Run Delivery Date Change, then Unallocate. The save re-allocates; after the GIN no unallocation is needed.
  - Q-RS1 (fully): settlement procedure; a Reattempt order due today must be allocated, put on a GIN, approved and delivered; the day close clears the per-PJP previous-day check (yellow row = not closed, green = closed).
  - Q-CS1: seq 55 is a check only, no Bounce.
  - Q-DS2 (fully): duplicate cheque numbers are allowed (no cheque inventory); slips are not blocked before settlement; Route Settlement Save reconciles, posts and adjusts, and fully adjusted invoices leave the collection screens.
  - Q-DS4: Outstanding Outlet doubled totals are a display defect.
  - Q-DJ1: DSR Adjustment = a DSR shortage while taking money from the outlet; it increases Total Shortage and Balance.
  - Q-TI1: Ordered = original order quantity, Allocated = allocated from available stock (expected).
  - Q-OB2: Opening must carry the previous Closing; 10-06 Opening 0 vs 10-05 Closing 259 = the environment's carry-over job did not run (LIVE_FINDINGS E-G11-3-1; report it to the environment owner).
  - Q-TX1: outlet 06/07 tax swap = master-data modification; rule: a zero-tax invoice of a non-exempt outlet cannot be delivered.
  - Q-DS5: Deposit Slip Outstanding Outlet amounts are auto-adjusted FIFO onto the outlet's oldest invoice (intended); Outstanding Cash memos collects per invoice.

## Carry-over on cnr1dev1 (important for the next run)
- **Order COL26000002018 (Reattempt, delivery 2026-10-07, unallocated) will block the 2026-10-07 settlement of route 02112** ("Un-Deliver Order exists for today delivery!") unless it is handled. Before seq 51:
  1. Allocate it (Order Stock Allocation, Order Date 2026-10-06).
  2. Put it on a GIN and have the Checker approve it.
  3. Mark it Delivered in Cashmemo Status.

  Alternatively, ask the QA team to handle it.
- Open receivables on 02112: 2012 (108,202, unpaid by the QA Team Lead's choice) and 2015 (73,556). Do not reuse any 2026-10-06 document (list in the report section 2).

## Next (in order)
1. No open question left from today: Q-DS2, Q-DS4, Q-DJ1, Q-TI1, Q-OB2, Q-TX1, Q-DS5 and Q-RS1 were all answered on 2026-10-06 (Q-RS4's zero-activity detail stays open by the user's choice). For the BA: Q-SR1, Q-OE3, BA11, the rest of section 1a. Environment owner: the stock carry-over job (E-G11-3-1).
2. Re-run the coverage check (LEARNING_STANDARD section 7) and ask the QA lead for **G0 sign-off** per area. The report rates inbound_stock, order_to_delivery_planning and delivery_and_returns ready for review; settlement_and_finance is close.
3. **Senior QA knowledge check**: predict, execute, compare. Prerequisite (seq 1-71 walked + consolidated) is now met.
4. Then prepare for the **QA environment**: app.yaml env, users, data, and the one-day rule including yesterday's Reattempt orders.
5. **Group 66 (NG_Setup Flow_PK) is still paused after seq 18**; resume at seq 19 Distributor Mapping (Auto_Multi_Orga). See the 2026-10-05 evening update above.
6. Still open from before: framework owner review of FRAMEWORK_DRIFT.md; qa-os changes not committed to git.

### 2026-10-06 (end of day) — next topic: bulk-data-factory
- Approach agreed with the QA lead (not started): generate bulk case-data workbooks from the flow definition in CTA_CONFIG_ASSERTION (sheets/headers/_ASSR) + data pools from snd-schema (active outlets on PJP/section with tax flag, SKUs in stock with price) + case matrix from the knowledge pages (positive, ATP boundary, negative; stock budget); messages only from the observed catalog; downstream values via repo_* columns; validator before delivery. Template: framework/casedata-samples/NG_Dcode_QA_OTC (Pak).xlsx; contract: framework/cta_config_assertion.md §5/5.1.
- First slice: Order Booking + Order Booking Detail + its _ASSR sheet (group 11 PK), ~20 outlets x 3-5 SKUs, then one legacy-engine run by QA.
- Pending decisions (QA lead): scope; amount assertions (captured / runtime repo_*+CHECK_VALIDATION / skipped); rows per run; who runs it and where.
- Also pending: QA team answers to learning_sessions/2026-10-06_G11-PK_QA_Team_Review.docx; close Q-RS4/BA14 in OPEN_QUESTIONS (user to confirm).

---
# Note 2026-10-07: future web app (parked)
Concept for a QA web app on top of QA OS (Jira dashboard, AI cases/steps, gated execution, downloads) saved in `docs/WEB_APP_CONCEPT.md`. **Parked** until S&D training is done and the QA team has produced one final output end to end. Not the current resume point.

---
# Release v0.5.0 (2026-10-07): S&D training release for the QA team
- Purpose: a QA lead trains Claude on S&D with their own Claude account (documents, verbal explanation, Q&A, or live walks of group 11 / 61 / 66). Guide: `docs/TRAINING_GUIDE.md`. Workflow: skill `knowledge-intake`, command `/qa-os:train snd`; sessions log to `runs/TRAIN-SND-<market>/<date>-<trainer>/` and consolidate into `apps/snd/knowledge/business/`.
- Setup: `connectors/setup_mcp.bat` (Selenium + bundled read-only `connectors/db-mcp` for snd-schema and selenium-framework-db) + `connectors/workspace_settings.example.json`.
- Package: `qa-os-v0.5.0.zip` (full; extract to the root of any drive -> `<drive>:\qa-os`, which is also the workspace; `.claude/settings.json` ships inside).
- Training results come back as a git branch `training/<name>-<date>` or a zip of `apps/snd` + STATUS.md + `runs/TRAIN-SND-*`; merge them centrally (consolidation rules in the knowledge-intake skill).
- **Workflow after training (QA lead, 2026-10-07):** no Jira tickets as the start; QA members give a short request / one-liner -> `/qa-os:quick` (skill `quick-script`) -> Claude writes its own steps from its training, picks today's data, executes once live, and generates Regress Master SQL + rollback + case data. AI execution never uses existing Selenium framework data (workbooks, event chains, atlas steps); the framework DB is read only for SQL generation. Recorder agent and OPERATING_RULES updated accordingly. First live quick run pending.

---
# Update: 2026-10-08 - QA team written answers to the 2026-10-06 review MERGED - RESUME HERE
**Read first:** `apps/snd/knowledge/business/learning_sessions/2026-10-08_QA_Team_answers_merge_report.md` (what changed per page, answered / partly / open, contradictions, defects, follow-ups); verbatim answers in `..._QA_Team_Review_answers.md` (filled docx in `apps/snd/knowledge/sources/`). Tag used: [stated 2026-10-08 QA Team].
- OPEN_QUESTIONS: **36 open = A 15 + B 12 + C 9 (1a 7, 1b 2)** (was 47). Closed 14 (BA2, BA11, BA12, Q-OE3, Q-SR2, Q16, Q27, Q29, Q48, Q-DS3, Q-GRN1, Q-GRN2, Q53, Q58); Q-SR1 partly; Q-SV1 not answered and Q-DS4 reopened (both follow-ups sent 2026-10-08); new Q-OE5 and Q-RL1 (class B).
- Key new rules: ORGA parameters **CASHMEMO_EDIT** (after-GIN edit: reduce only, reason, approved GIN quantity reduced on save) and **ZERO_TAX_ORDER_EXEMPTION** (Y deliver zero-tax invoices, N block); roles 0001 submit / 0002 TSSM approve / 0003 DSR / 0004 Warehouse / 9999 HQ, two-level workflow; Route Settlement: ignore colours (Edit link = not settled), Payable - Received = DSR Cash Shortage, GIN qty must match GRN qty else "Stock Mismatch", previous-day check = working date today and closing date N-1; collections in production come from the Delivery App (mobile sync auto-creates Unposted slips); GRN shortage auto-creates a DSR adjustment; stock moves on approval.
- New defect **D-G11-2b-1**: route 02112 of 2026-10-01 Complete with slips 1131-1136 Un Posted (report it). New contradiction **28**: CASHMEMO_EDIT says the GIN is reduced on an after-GIN edit, three walks saw no stock movement (Q-OE5).
- Next: (1) wait for the Q-DS4 / Q-SV1 follow-ups; (2) next walk: L42 (CASHMEMO_EDIT + GIN after an edit), L43 (role codes), L41 (zero-tax parameter first); (3) then the coverage check and G0 sign-off, Senior QA knowledge check, QA environment preparation (unchanged order from the 2026-10-06 update); carry-over on cnr1dev1 (Reattempt 2018) still applies.
- **Follow-up answers merged (2026-10-08, same day):** see section 7 (addendum) of the merge report; source `learning_sessions/2026-10-08_QA_Team_followup_answers.md`, tag [stated 2026-10-08 QA Team (follow-up)]. Q-DS4 closed (Outstanding Outlet totals are correct, **D-G11-3-1 withdrawn**); Q-SV1 closed (stock checks = per-transaction movement + balance: DA In, Return Document Out, GIN Out, GRN In, SAN +/-); Q-OE5 closed (**no stock movement at an after-GIN cash memo edit**; the "GIN reduced on save" statement above is superseded); new Q-SV2 (B: which Return Document posts Out, L45). OPEN_QUESTIONS now **34 open = A 15 + B 12 + C 7 (1a 7, 1b 0)**; contradictions 21 resolved / 5 partly / 6 open. Next item (1) above is done; the walk list is now L43, L41, L45, optional L42 (parameter value only) and L44.

---
# Update: 2026-10-08 (later) - hardening groups A, B, C done in code - RESUME HERE for the QA release
Register: `docs/HARDENING.md` (release gate = section D). Design: `docs/FINAL_DESIGN.md` v3 (draft, user review pending).
- **A (recording):** watcher fixes in `plugins/qa-os/runtime/qaos_helpers.js` (grid labels via aria-describedby, default cells, remember, popups, nav_click); injection by argument from `qaos_helpers.min.js` (`build_helper.py`). A1/A2/A3/A5/A7 mock-tested only (FIXED-UNPROVEN).
- **C (generation):** new converter `framework/tools/qaos_record_multi.py` (recording -> multi-screen spec: child screens, navigation from the sidebar click, Load Data per screen, waits after toasts, 0006 type-ahead, 0010 repo fields, and **case-data rows for all N cases from `rows.json`**, fields bound by exact value match; gaps never guessed). Tests: `framework/tools/test_qaos_record_multi.py` (8) + `test_gen_framework_sql.py` (7), all OK. framework-generator agent, quick-script, recording-protocol, recorder, FINAL_DESIGN point at it. C1/C4/C6 need the engine replay.
- **B (process):** B4 label index + `[Role]` prefix in `qaos_steps.py check`; B6 `qaos_run.py init --request` writes requirement.json for quick runs, stages tracked. B7/B8 environment, C9 engine owner: open, need QA-lead acceptance.
- **Next (release gate D):** (1) acceptance run: a clean session runs one `/qa-os:quick` request end to end with no tool changes, single case, about 30 min (needs the QA member for logins); (2) framework owner applies the SQL on a test copy and replays all N rows; (3) rebuild zip, bump version (v0.6.0).

---
# Update: 2026-10-08 (evening) - quick-run rehearsal done, engine replay pending - RESUME HERE
- Rehearsal run `runs/QUICK-20261008-1429/20261008-1429` ("Create Order Book and Order Detail with 5 positive test cases"; PK, cnr1dev1, run by Syed Kamran, Maker Auto_Multi_Orga). Attempt 1 (order COL26000002027, outlet 1000000019) exposed watcher bugs A13-A16 (fixed, archived in attempt1_old_watcher/); attempt 2 TC04 passed (order COL26000002028, outlet 1000000017). Generated: menu group 0648, screens 064801-03, flow 06480001, 31 inserts, workbook 5 cases / 32 rows; verifier: "ready for framework-owner test-copy apply".
- 2026-10-08: the user applied framework.sql successfully; the Regress Master (legacy engine) replay has NOT run yet - results to be shared on 2026-10-09.
- Next: read the engine result -> check in the app (5 orders, RepoValues 01..05_QUICK_ORDERNUMBER, 5 evaluations per _ASSR sheet) -> mark C1/C4/C6 and A-items proven or log new HARDENING rows. Note: TC04 outlet 1000000017 already has today's order; if replayed on a later day this does not matter.
- Then: commit groups A/B/C + run-context work (user pushes), release gate D (clean-session acceptance run, zip v0.6.0, docs). The session's installed plugin copy lacks /qa-os:quick: re-register/update the plugin from qa-os/ first.
