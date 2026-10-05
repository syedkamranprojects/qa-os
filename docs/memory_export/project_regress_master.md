---
name: project-regress-master
description: "Regress-Master - app-agnostic data-driven web test runner being built in the workspace; Phase 0 skeleton done, engine code gated on sign-off."
metadata: 
  node_type: memory
  type: project
  originSessionId: 8dd9a349-6460-4115-8859-ba785c098e87
  modified: 2026-09-11T13:02:19.590Z
---

`C:\MyWork\gias-qa-workspace\regress-master\` (own git repo, `git init` + first
commit `d2e81d8` done 2026-09-08). A clean rewrite of the proprietary framework
at `C:\git-projects\NGSelenium-Testing` ("REGRESS MASTER" by Centegy).

**Goal:** application-agnostic data-driven web test runner. Tests = rows in the
`selenium-framework-db` PostgreSQL schema (`fct_pr_*`); an engine reads a
selected test-flow id + version, drives a browser, verifies against the app DB,
reports. The app under test is configuration (one `fct_pr_app_application` row +
a menu-group band + seed SQL) plus one `AppAdapter` impl. GIAS is the first
configured app, not hard-coded.

**Architecture (frozen in docs/):** 3 layers - `engine-core` (headless, knows no
app) / `runner-cli` / `runner-gui` (thin JavaFX). `AppAdapter` SPI
(startSession / navigateToScreen / enterScreenContent / endSession), selected by
app id via ServiceLoader. **GIAS adapter = the existing `..\gias-qa-core`
project** (login + flyout menu nav), thin `GiasAppAdapter` wrapper in Phase 2 -
no rewrite of gias-qa-core. The framework's own `fct_pr_mgsm...` navigation
model is bypassed for GIAS.

**Vocabulary is frozen** (queried live 2026-09-08): 11 component types
`0000`-`0010`, 10 `(type,event)` pairs. Codes the old Main.java references but
which have no DB rows (`0012`-`0025`, `02xx`, mobile) are NOT implemented in v1.
Key rewrite change: **hard-fail, never silent-skip** on unmapped code / unknown
locateby / null locator - see docs/error-contract.md.

**GIAS menu-group band = `88xx` sequential** - one framework menu-group per GIAS
level-2 menu branch, assigned in menu-tree order (`8801` = Parameter Setup >
General/Global, ...). Table in docs/apps/gias.md. `psc_screenid` = `88xx` + 2-digit seq.

**Schema delta found:** live `selenium-framework-db` is leaner than old
Main.java assumes - missing `psf_app_ids`, `psq_qryparameters`,
`psq_validationType`, `psef_validationType`, `fct_pr_alg_app_allowable_groups`,
etc. Resolve per-column in Phase 1. Noted in docs/vocabulary.md §3 and sql/README.md.

**Status:** Phase 0 (docs + skeleton) DONE, commit d2e81d8. Phase 1 IN PROGRESS,
commit 509d8a0: `framework-db` Maven module - schema + seed as **Flyway
migrations** V1 (baseline schema, verbatim from live DB) / V2 (core vocab: 11
types, 10 pairs, 3 test types) / V3 (GIAS app row 88 + placeholder URL
`http://localhost:8080/genins` + version 1.0 + login user `administrator` empty
pw) / V4 (88xx band = 39 menu groups, one per GIAS L2 branch). GIAS seeds in
`db/migration_gias`, on path only when `regress.db.appModules` includes `gias`
(default). `FrameworkDbMigrator.migrateToLatest(DbConfig.load())` runs on app
load; also a runnable `-cli` jar (migrate|info|validate|repair). Parent pom +
module pom, Flyway 10.22 / PG 42.7 / JDK 21. **NOT yet compiled or applied - no
Maven on PATH in this workspace.** `.gitattributes` forces LF on `*.sql` (Flyway
checksum stability).

Phase 2 DONE (written), commit 8c4726d - user gave explicit go-ahead
("go ahed for Phase 2"), lifting the earlier gate. `engine-core` (app-agnostic)
+ `runner-cli`, ~48 Java files, ~3700 lines:
- `api/` AppAdapter SPI + AppAdapterRegistry (ServiceLoader)
- `model/` vocabulary as enums (ComponentType/EventAction/LocateBy), Vocabulary
  drift check, row records, ScreenPlan/TestFlowPlan
- `config/` ConfigRepository + JdbcConfigRepository (plain JDBC, real queries
  against the V1 schema: flow->menu groups->screens by prefix->fields
  version-filtered + events + queries)
- `exec/` FlowExecutor->ScreenRunner->FieldFiller(Layer A)/EventRunner(Layer B)/
  Verifier; single LocatorResolver; ExecutionControl; ProgressListener; RunContext
- `result/` RunResult/ScreenResult/StepResult, exit codes 0/1/2/3
- `report/` JsonReporter + HtmlReporter
- Error contract enforced: EngineError E1-E10 -> Outcome.ERROR (!= FAIL);
  unimplemented control type -> visible ERROR row (never silent skip); inactive
  pair -> WARNING row
- Implemented: text/dropdown/datepicker/readable fills; Load Data, Verification
  (SCREEN), Refresh, Wait, Fill Single, Click, Click Alert.
- NOT_IMPLEMENTED (reported as ERROR, for Phase 5 live tuning): autoselect,
  dropdown-grid, multi-select, grid-input fills; Q2Q data verification;
  validation checks; toast text from fct_rp_set_screen_event_toast.
- Data-row (Excel/CSV) input NOT wired - values from psf_fixed_value or in-run
  value repository; field with neither -> visible SKIPPED.
`runner-cli`: `regress --app 88 --version 1.0 --login 8801 --flow <id>`; migrates
framework DB on load; deps Selenium 4.27 / Jackson 2.18 / JDK 21.

`gias-adapter` DONE, commit 2c186b9 - user chose "mvn install gias-qa-core to
local repo". `GiasAppAdapter` (com.regressmaster.gias, app id "88") wraps
gias-qa-core: `Gias.start(GiasConfig built from AppConfig baseUrl + LoginUser
username + GIAS_TEST_PASSWORD)` -> `session().loginWithDefaults()`;
`navigateToScreen` resolves `ScreenRef.routingHint` -> `GiasMenu` constant ->
`menu().open()`; `enterScreenContent` -> `frames().toContentOrDetail()`;
`endSession` -> `Gias.close()`. Registered via META-INF/services (ServiceLoader);
`runner-cli` has it as a runtime dep. Routing-hint forms accepted:
`giasmenu:<NAME>` / bare `GiasMenu` constant / `path:A>B>C` / `source:<page.jsp>`.
The current Phase-1 seed only gives menu-GROUP hints (`gias-menu:0101` from
`pmg_searchtext`) which the adapter rejects - **per-screen routing hints
(GiasMenu keys on fct_pr_sc_screens rows) are the remaining Phase 1 task**.

gias-qa-core API used: `Gias` (start/driver/frames/session/menu/close/quit),
`GiasConfig.Builder` (public fields + build()), `GiasSession.loginWithDefaults/
assertOnMenuScreen`, `MenuNavigator.open(GiasMenu)`, `MenuCatalog.load()/byPath/
leaves`, `MenuItem.key()/sourcePageName()`, `GiasFrames.toContentOrDetail()`.
gias-qa-core is `com.gias.qa:gias-qa-core:0.1.0-SNAPSHOT`, compiler release 25 ->
**whole regress-master reactor now targets --release 25**, compiler plugin 3.14.0.

**NOT compiled anywhere yet** - no Maven / JDK 25 on PATH in this workspace.
Build order: `cd ../gias-qa-core && mvn install` (JDK 25), then `mvn package` in
regress-master.

Phase 3 DONE, commit cc5df93. `runner-gui` = thin JavaFX 25 run form (no FXML):
Run tab (App/Version/TestType/TestFlow(s) multi-select/LoginUser/Browser/
Headless/ScreenshotEveryStep/ContinueOnError/ReportDir/Execute - all lists from
the framework DB, nothing editable; last pick saved to savedSelections.txt
tilde-delimited), Progress tab (live TableView via FxProgressListener +
Terminate/Pause/Resume -> ExecutionControl), Report tab (report.html path + Open
via HostServices). `AppServices` migrates DB on launch + opens
JdbcConfigRepository; Execute runs `Engine.run` in a `javafx.concurrent.Task`
(daemon thread, never SwingWorker). engine-core `ConfigRepository` gained
`apps()/testTypes()/testFlows()` (+ `TestType`, `TestFlowSummary` records).
Dev launch: `mvn -pl runner-gui -am javafx:run` (javafx-maven-plugin 0.0.8).

**Repo state:** local git only. GUI now compiles & runs for the user (they fixed
imports + line-ending stuff on their box). Key later commits: a0f300d (test
List<String[]> fix), e3af53b (RegressGuiLauncher - plain main class so JavaFX
runs off the classpath; run THIS not RegressGuiApp), history rewrite removed a
committed DB password, 2bc9a91 (test-flow authoring).

**Test-flow authoring (commit 2bc9a91):** V5 migration adds
`fct_pr_sc_screens.psc_routing_hint` (per-screen menu-leaf hint;
`giasmenu:<GiasMenu constant>` / `path:A>B>C` / `source:<page>.jsp`; NULL ->
engine falls back to menu group's pmg_searchtext). `JdbcConfigRepository` reads
it and prefers it. Authoring is hand-written psql scripts under
`sql/authoring/`: README + `_TEMPLATE_test_flow.sql` (copy/edit/apply,
re-runnable delete-then-insert) + `example_gias_business_class_setup.sql`
(navigation-only smoke flow SMK-BCS-01 to Business Class Setup; field/event rows
TODO from the live page). Convention: each hand-authored GIAS flow gets its own
4-char menu group `88F1..88FA` (screens `88F1nn`) so flows don't pull each
other's screens; the `8801..8839` V4 catalog groups are reference-only. Flow is
NOT bound to an app in the schema - user picks Application in the GUI at run time.
GIAS_TEST_PASSWORD set via IntelliJ run-config env var or `-Dgias.password=`.

**To make it actually run** (needs JDK 25 + Maven + Postgres box):
1. `cd ../gias-qa-core && mvn -q install`
2. `cd regress-master && mvn -q package`  (fix any compile nits - never built)
3. Postgres `regress_master` DB; migrator runs on first launch
4. Seed per-screen GiasMenu routing hints on fct_pr_sc_screens + a first smoke
   flow (the remaining Phase 1 data gap - see docs/apps/gias.md sec 5 &
   gias-adapter/README.md)
5. `mvn -pl runner-cli -am package && java -jar runner-cli/target/regress.jar ...`
   or `mvn -pl runner-gui -am javafx:run`

**Excel data source + per-flow branch (commit 37afbd6, ports the S&D model):**
V6 migration adds `fct_pr_tf_test_flow.ptf_branch_code` (login branch per flow;
GIS Setup = `0010010001` for Parameter Setup screens; NULL -> env default) +
`.ptf_data_file` (workbook name under `regress.data.dir`, default `./data`,
`-Dregress.data.dir` / `REGRESS_DATA_DIR` / CLI `--data-dir`), plus
`fct_pr_sc_screens.psc_data_sheet` and `fct_pr_sf_screen_field.psf_field_source`.
`engine-core.data`: `ExcelDataSource` (Apache POI 5.3) - workbook per flow, sheet
per screen (`psc_screenname`/`psc_data_sheet`), header row 0, one `DataRow` per
non-blank row = one test-case iteration; reserved cols `PK`/`PK_DESC`/`STPONERR`/
`EXPECTED_MESSAGE`. `FlowExecutor` plans all flows up front, resolves branch from
first flow -> `AppConfig.withBranch` -> `startSession`, runs each screen once per
data row (re-navigating each time). `psf_field_source` = EXCEL (row value by
`psf_field_db_column`) | FIXED (`psf_fixed_value`) | REPO (captured by a `0010`
field). No data file -> screen runs once, EXCEL fields report SKIPPED.
`sql/authoring/` template + README + `_CHECK_setup.sql` cover V6.

**Next options:** Phase 4 (authoring assist - live-explore a GIAS screen, emit
fct_pr_sf_screen_field / fct_pr_sef_screen_events_flow INSERTs + the .xlsx sheet);
Phase 5 (GIAS pilot end-to-end). Or a compile/build pass once on a proper box.

## SESSION END 2026-09-08 - resume here tomorrow

**MCP repointed:** `mcp__selenium-framework-db__run_readonly_query` now hits the
LIVE **`regress_master`** Postgres (was `CTA_CONFIG`, the Centegy reference DB).
So I can query the user's real config directly now. `gias-schema` MCP still =
GIAS Oracle app DB. No psql/PG client on the box.

**Where it stands:** regress-master built + GUI runs on the user's JDK-25 box.
User ran a flow: login + GIS Setup branch + flyout nav to Business Class Setup
all worked, screen loaded, run "successful" - but **no Excel data filled**.

**Diagnosed (queried regress_master live):**
- flow `SMK-BCS-01`: `ptf_branch_code='0010010001'` OK, but **`ptf_data_file` IS
  NULL** - no workbook linked.
- only screen `88F101` "Business Class Setup"; **`fct_pr_sf_screen_field` has 0
  rows for `88F1%`**; its only event is `0000/0006` Wait 4s - **no `0000/0001`
  Load Data**. So there is nothing configured to fill. Working as designed.
- `data/SMK-BCS-01.xlsx` (sheet "Business Class Setup") was hand-created by the
  user and committed (`4b8af35`) but nothing references it.
- DB migrated to V6; V6 cols present.

**TOMORROW - to get Excel-driven fill working on `88F101`:**
1. Get REAL locators from the GIAS "Business Class Setup" page (`geninsController.jsp?FROM=16`)
   - offer to open it live via Selenium MCP / test-orchestrator skill (login user
   `administrator`, branch `0010010001` GIS Setup, dept e.g. `13`, app `88`).
2. `UPDATE fct_pr_tf_test_flow SET ptf_data_file='SMK-BCS-01.xlsx' WHERE ptf_testflowid='SMK-BCS-01';`
3. INSERT `fct_pr_sf_screen_field` rows for `88F101` (one per input:
   `psf_field_db_column`=Excel header, `psf_field_source='EXCEL'`, real
   `psf_fieldid`/`psf_locateby`).
4. INSERT a `0000/0001` Load Data step (+ optional `0004/0002` Click Save,
   `0000/0004` Toast) into `fct_pr_sef_screen_events_flow` for `88F101`.
5. Excel sheet must be named exactly `Business Class Setup`, header row =
   the `psf_field_db_column` values + optional `PK`/`PK_DESC`/`STPONERR`/`EXPECTED_MESSAGE`.
6. Rerun the flow from the GUI (App GIAS, ver 1.0, flow SMK-BCS-01, login 8801).

repo tip commit: `4b8af35`. All work committed, tree clean, never pushed (user
will share GitHub creds to push later).

## SESSION 2026-09-11

Fixed sheet-name mismatch (`psc_data_sheet='Business Class Setup - add'` set via
DB, matching the user's actual Excel tab name) - Excel fill then worked, fields
`text0/text1/text3` -> `CODE/DESCRIPTION/SHORTDESC` all correctly mapped.

Flow then hit `E9_NAVIGATION_FAILED` on iteration 2: `unexpected alert open:
"Please Select business type"`. Root cause: Save (iteration 1) raised a GIAS
client-side validation alert (a required "business type" field isn't in the
config yet); GIAS's ChromeDriver runs `unhandledPromptBehaviour=IGNORE` so the
click didn't throw - alert stayed open and broke the NEXT screen's frame-switch
instead, misattributing the failure. **Fixed in commit 9938f2b:**
`EventRunner.click()` now checks for a resulting alert right after clicking,
accepts it, reports FAIL on the Click step itself (not two steps later);
`GiasAppAdapter.navigateToScreen` also defensively clears any stray alert before
every nav (via `new com.gias.qa.core.Dialogs(session.driver()).acceptIfPresent()`
- Dialogs has a public ctor(WebDriver), no gias-qa-core change needed).

**"Business type" field found live (2026-09-11):** screen has TWO type
dropdowns - `text86`/`PBC_BUSICLASS_TYPE_m_` ("Business Class Type",
Conventional/Takaful, already defaults to C - not the culprit) vs
**`policyBusiTypeCombo`/`PPB_CODE_m_`** ("Policy Business Type", starts blank -
**this is the one behind "Please Select business type"**; options
0000000001=Comprehensive/0000000002=Motor Third Party/0000000003=Others,
selectByVisibleText matches first so plain text works in Excel). User added it
themselves (`fct_pr_sf_screen_field`, componenttype 0002) plus
`VehicleUsageTypeCombo`/`POLICY_VECH_TYPE`. Cached at
`.claude/element-cache/gias/genins/pgg_se_businessclass.json` (source JSP
unresolved - ripgrep timed out over the full GIAS tree; narrow the path before
retrying). **Login gotcha found live:** for branch 0010010001 (GIS Setup),
selecting department via a bare `el.value=X; dispatchEvent(change)` can cause a
server 500 on OK - a full focus/input/change/blur sequence works reliably for
both FIRE(11, the live default) and MOTOR(13/user's choice) - `PR_GN_DP_LOCDEPARTMENT`
has zero rows for this branch (no formal dept mapping) but the app accepts it anyway.

**Two more real bugs found + fixed (commit 318ef38), running the flow with 3 data
rows (PK 01/02/03, codes V01005/V01006/V01007):**
1. PK01's Save alert was exactly "Unable to Insert Record", matching its
   EXPECTED_MESSAGE (V01005 already existed - GIAS behaved correctly) - but
   `EventRunner.click()` treated ANY resulting alert as an unconditional FAIL,
   never consulting EXPECTED_MESSAGE. Fixed: alert text vs EXPECTED_MESSAGE
   compared (case/trim-insensitive exact match) -> match = PASS, mismatch = FAIL.
2. PK02 then hit E9_NAVIGATION_FAILED ("root cell 'General Insurance' not
   found") -> aborted the WHOLE run (ERROR is fatal by default), PK03 never ran.
   Root cause: GIAS's flyout DOM only exists on the actual Menu screen; a leaf
   click replaces detailFrame's content, destroying it - true only for the
   FIRST navigation per session. Fixed: `GiasAppAdapter.navigateToScreen` now
   clicks the persistent top-bar "Main menu" landmark (Frame2
   `goToMenuFromTop()`) to force back onto the Menu screen before every flyout
   walk, not just the first - makes repeated per-data-row navigation in one
   session work.

repo tip: `318ef38`. Not yet rebuilt/rerun by the user since these two fixes -
next step is rebuild + rerun SMK-BCS-01 and confirm PK01 PASSes (alert-match),
PK02/PK03 actually execute and Save succeeds ("Record Successfully Inserted").

**ExtentReports added (commit 668dc2d):** new `ExtentReporter` (engine-core,
`com.aventstack:extentreports:5.1.1`, `ExtentSparkReporter`) writes
`extent-report.html` alongside the existing `report.json`/`report.html` (never
instead of - `Reports.writeAll` wraps it best-effort so a failure there can't
break the other two; `runner-gui`'s inline WebView still shows plain
report.html unchanged). One ExtentTest per flow, one node per screen iteration
(category = PK_DESC, info line = data values entered), one log line per step;
Outcome->Extent Status keeps ERROR distinct from FAIL. GUI gets an "Open Extent
report (charts)" button (external browser, not inline - WebView's engine is
older than what Extent's JS charts expect). NOTE: ctx7 lookup for
`extentreports-java` returned mixed v3/v5-era API signals (indexed docs seem to
mix versions) - went with the modern, actively-maintained `ExtentSparkReporter`
API from established knowledge; genuinely unverified by compilation like
everything else in this repo.

**Report UX (commit 3c01da7):** runner-gui's Report tab now has a `WebView`
that loads `report.html` inline (auto-selected when a run finishes) instead of
only a path + external-open button; kept "Open in browser" too. Needed adding
`javafx-web` dependency (parent + runner-gui poms). Also:
`ScreenResult.setDataRow(DataRow)` now records `PK_DESC` + the data row's
column values (CODE/DESCRIPTION/POLICY_BUSI_TYPE/etc, i.e. what was actually
typed/selected for that iteration) alongside PK; `HtmlReporter` prints a
"Test data (PK_DESC): KEY=value · KEY=value" line under each screen heading,
`JsonReporter` adds `pkDesc`/`dataValues` per screen - full audit trail of what
was entered per case, not just the PK number.

**Maven now installed for the user (2026-09-11):** no package manager had it, so
installed Apache Maven 3.9.16 manually to `C:\tools\apache-maven-3.9.16`
(downloaded+checksum-verified from the official Apache mirror), set user env
vars `JAVA_HOME=C:\Program Files\Java\jdk-25` and `MAVEN_HOME`, added
`bin` to user PATH. `mvn -version` confirms JDK 25 pickup. New terminals only -
already-open ones don't see it.

**Real root cause of the recurring `NoClassDefFoundError: org/flywaydb/core/Flyway`
at runtime (2026-09-11) was NOT a stale-repo issue** (that was ruled out after a
clean install still failed) - it was **maven-shade-plugin's default
`createDependencyReducedPom=true`** on `framework-db`'s shade execution (builds
an uber `-cli` jar for the standalone migrator). Shade creates
`dependency-reduced-pom.xml` (deps already bundled into the uber jar stripped
out) and Maven's `install` phase then installs THAT reduced pom for the WHOLE
module - including the real, non-shaded `framework-db-...jar` that `runner-gui`
actually depends on - silently dropping flyway-core/flyway-database-postgresql/
postgresql/slf4j from its transitive deps in `.m2`. Confirmed by diffing the
installed `.m2` pom against `framework-db/dependency-reduced-pom.xml` (byte
-identical) vs the real source pom (which always had the deps correctly).
**Fixed:** added `<createDependencyReducedPom>false</createDependencyReducedPom>`
to the shade execution's `<configuration>` in `framework-db/pom.xml`. General
lesson: any module using shade to build a secondary uber-jar (classifier
attached) alongside its normal thin jar needs this, or `mvn install` corrupts
the module's own published dependency metadata for every consumer in the reactor.

Also: running `javafx:run` (a direct plugin-goal invocation, not a lifecycle
phase) against a multi-module reactor executes the goal on EVERY project in
build order including the root aggregator pom first - which has no `mainClass`
and fails before ever reaching `runner-gui`. Fix is `cd runner-gui && mvn
javafx:run` (or `mvn -pl runner-gui javafx:run` without `-am`, once siblings are
already installed) so only that module's pom (with its own plugin config) runs.

**GIAS_TEST_PASSWORD gains a third resolution path (commit after 668dc2d):**
`GiasAppAdapter.resolvePassword()` now also falls back to a `gias.password` key
in the git-ignored `config/framework-db.properties` file (same file/pattern
already used for the framework DB password), after `-Dgias.password=` and the
env var. Added so an IntelliJ run config doesn't need the secret typed into its
Environment Variables field (which the user initially wanted - persuaded away
from a tracked `application.properties`, which would have leaked it into git
history, toward this already-gitignored file instead). Documented in
`config/framework-db.properties.example`.

**ExtentReports "no UI" fix:** `ExtentSparkReporter` pulls its CSS/JS/icons live
from `cdn.jsdelivr.net` + `stackpath.bootstrapcdn.com` by default - renders as
unstyled plain HTML with zero error if the viewing machine has no outbound
internet (GIAS test box). Fixed by calling `spark.config().setOfflineMode(true)`
in `ExtentReporter.java` (confirmed real via `javap` on the actual
extentreports-5.1.1 jar - `ExtentSparkReporterConfig$Offline` class exists -
since ctx7's docs corpus for this library still only surfaces old v3
`ExtentHtmlReporter` API, not this). Bundles assets locally next to the report instead.

**Plain HtmlReporter screenshots were invisible:** `RunContext.screenshot()`
returns an OS-native absolute path (Windows backslashes), which `HtmlReporter`
put straight into an `<a href>` - invalid HTML, so the link never resolved
(not even a stale-cache issue - IntelliJ had rebuilt fine, the href was just
broken). Fixed: paths relativized against `reportDir` with forward slashes
(works whether opened via runner-gui's WebView `file://` URL or double-clicked
directly), and rendered as inline clickable thumbnails, not a bare "png" text
link. **Separately clarified for the user:** screenshots are only
auto-captured on FAIL/ERROR steps, or on every step if "Screenshot every step"
is checked on the Run tab before Execute - an all-PASS run with that box
unchecked will legitimately have zero screenshots attached; this is
by-design policy, not a bug.

User confirmed (2026-09-11, end of session): after `mvn clean install` +
rerunning from IntelliJ, everything above now works end-to-end.

**New authored flow: `sql/authoring/example_gias_endorsement_entry_add.sql`
(flow SMK-END-01, menu group 88F2, screen 88F201).** Navigation-only smoke,
same shape as SMK-BCS-01: navigate to Transactions > Underwriting >
Endorsement Entry (`giasmenu:TRANSACTIONS__UNDERWRITING__ENDORSEMENT_ENTRY`),
Wait 4s, Click the "Add New" button (xpath, no id/name -
`//input[@type='button' and @value='Add New']`), Wait 3s. Authored from the
live Selenium MCP exploration in [[project_gias_menu_navigation]] (see that
memory for the flyout technique + element cache files this was built from).
`ptf_branch_code` left NULL (unlike SMK-BCS-01's GIS-Setup-only `0010010001`)
since Endorsement Entry isn't branch-restricted. Department is NOT a per-flow
DB column - it's `GIAS_DEFAULT_DEPARTMENT` env / `-Dgias.department=` at run
time (`GiasAppAdapter.java:313`); flow was verified under TRAVEL(22) but any
department works for this screen. Real data-entry (screen 88F202, commented
out at the bottom of the file) is blocked on capturing live field locators for
the "Log Book (Header)" form (Endorsment Type radio, Base Document No,
Endorsment Date, Cancelled Due to, Remarks, Effective Date, Deb Credit Note) -
not yet done, `ggu_gp_gp_logbook.json` only has the heading landmark so far.

Related: [[project-gias-full-menu-catalog]], [[project-gias-menu-navigation]],
[[feedback-structured-flow-replay]]. Engine analysis: scratchpad
`ngselenium-engine-findings.md`.
