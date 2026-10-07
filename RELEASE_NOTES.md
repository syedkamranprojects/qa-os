# QA OS release notes

## v0.5.0 — 2026-10-07 (S&D training release)

For QA leads who want to train Claude on the S&D (DCODE) business **with their own Claude account**. Start with `docs/TRAINING_GUIDE.md`.

### New
- **Training workflow:** skill `knowledge-intake` + command `/qa-os:train <app>`. One way to take in any training method — documents (user guide, manual, SOP, deck, spreadsheet in `apps/snd/knowledge/sources/inbox/`), verbal explanation, Q&A / quiz, or a live walk of a framework group (11 Daily Cycle PK, 61 BD, 66 Setup PK). Every fact is tagged (`[stated <date> <name>]`, `doc:<file> p.<n>`, `[observed]`), earlier statements are never overwritten, conflicts become open questions, and each session ends with consolidation, a report and a STATUS resume point.
- **Connector setup in one step:** `connectors/setup_mcp.bat` configures Selenium, `snd-schema` and `selenium-framework-db` in the Claude desktop config (backup first, hidden password input, live connection test; `-ClaudeCode` also registers them for the CLI).
- **Bundled read-only DB connector** `connectors/db-mcp/` (trimmed from the team's nl2sql MCP server: SELECT-only, LLM parts removed, one schema cache per database, Oracle client path configurable).
- `.claude/settings.json` ships with the release (plugin registration + allow list): unzip to `<drive>:\qa-os`, open that folder, done. `connectors/workspace_settings.example.json` covers the nested-folder layout.
- **Release package:** `qa-os-v0.5.0.zip` (extract to the root of any drive -> `<drive>:\qa-os`).

### Knowledge in this release (S&D)
- Group 11 Daily Cycle PK walked end to end three times; the 2026-10-06 run (with the QA Team Leads) covered all 46 active rows including Order Editing and the first Route Settlement done by Claude. 12 questions answered that day; 47 open (`OPEN_QUESTIONS.md`).
- New rules: Order Editing needs unallocated orders due today; Reattempt orders due today must be covered in a GIN before settlement; yellow/green settlement rows; settlement Save posts slips and adjusts invoices; cheque step is check-only; DSR adjustment = DSR shortage; Outstanding Outlet amounts adjust FIFO; tax master-data rule for zero-tax invoices.
- Group 66 Setup PK walked to seq 18. BD (region R1) users added: Auto_Bangla / AutoBD_tssm, company 010105, distributor 05108843.
- QA team review sheet: `learning_sessions/2026-10-06_G11-PK_QA_Team_Review.docx`.

### Changed
- `docs/OPERATING_RULES.md` rewritten for the current rules (markets/users table, group run rules, permissions); `CLAUDE.md` points cold-start sessions at the training workflow; `docs/memory_export/` refreshed (36 notes); `credentials.example.json` lists the BD users.

### Known issues
1. Generated framework SQL has still never been applied/replayed in the legacy engine.
2. cnr1dev1 stock carry-over job did not run on 2026-10-06 (Opening 0) — environment owner.
3. Order COL26000002018 (Reattempt, due 2026-10-07) blocks the PK route 02112 settlement until it is covered in a GIN.
4. Only one person should run a daily cycle per distributor per day on the shared environment.
5. Ticket runs SDMS-2990 / SDMS-12390 are parked until training is complete.

## v0.4.0 — 2026-10-01 (first team release)

This is the first version meant to go to the whole QA team, not just the one machine it was built on. Everything below was verified live on cnr1dev1 (S&D / DCODE, Unilever Pakistan) unless marked otherwise.

### What's in this release

**Platform**
- Claude Code plugin `qa-os@qa-os` — 8 agents, 8 skills, 6 commands. Install once per machine (see `DEPLOY.md`), then it's available in every Claude Code session opened in this workspace.
- App packs: `apps/snd` (S&D / DCODE — active) and `apps/gias` (GIAS — scaffolded, phase 2). Adding a new application under test means adding an app pack, not changing the platform.
- Central settings: `qaos.yaml` (limits, gates, safety rules) and `apps/<app>/app.yaml` (environments, users, roles, markets). Checked with `python runtime/qaos_config.py validate`.

**The life cycle (story → cases → steps → recording → framework scripts)**
- `story-analyst`, `test-designer`, `step-author`, `data-engineer`, `app-cartographer` — stages 1-4 and app learning.
- `recorder` — runs one approved flow live through the browser MCP, one data row, stops at each login switch. Never types credentials.
- `framework-generator` — turns a passing recording into `CTA_CONFIG_ASSERTION` SQL, a rollback script and the case-data workbook for the legacy Selenium Regress engine. Never applies SQL.
- `verifier` — independent read-only review of the generated output against the live schema before a human (the framework owner) applies anything.

**Assisted step authoring (new this release)**
- `qaos_steps.py` — checks a test step against the predefined vocabulary (`vocabulary/core.yaml`) and the real screen labels; suggests the closest match on a typo; never guesses a label.
- `qaos_export.py` / `qaos_import.py` — the Excel round trip. Claude exports cases + steps to Excel; the QA member edits the **Test Steps** column in plain English; Claude imports it, checks every line, and that becomes the execution source. Recorded results are written back into the same workbook.
- `step-authoring` skill — the "next step" dialogue for a QA member who wants to build a sheet interactively in chat, with suggested options plus free text at every turn.

**Learning mode (new this release)**
- Claude can walk an application's business flows on its own — no questions to the user — building a plain-language knowledge base (`apps/snd/knowledge/business/`): what each document is, who does what, status transitions, stock/financial effects, messages, and test ideas. Every statement is tagged `[observed]`, `[db]`, `[inferred]` or `[unknown]`.
- Real screen harvests (`apps/snd/knowledge/screens_observed/LIVE_*.json`) and the framework flow atlas (`apps/snd/knowledge/framework_atlas/`, 31 groups / 547 flows / 1,477 screens) feed both learning mode and the step checker.
- Open business questions are consolidated and triaged in `apps/snd/knowledge/business/OPEN_QUESTIONS.md`: answered with evidence, safe to default, or a genuine BA decision (kept to about a dozen, each with a default so nothing blocks on it).

### Verified end-to-end (this run)
- Dispatch Advice: create → add line → forward → approve (maker/checker, different users) — passed live, generated framework SQL, independently verified (`runs/PILOT-DA-GIN/20260930-1615/`).
- Stock Inquiry business-effect check after a DA approval.
- A same-day Dispatch Advice → Goods Issue Note chain, which surfaced two real findings (see below).

### Known issues / open items for this environment
1. **Stock and orders are keyed by calendar day.** A Dispatch Advice approved "yesterday" does not carry its stock into "today" (Opening resets to 0), and a Goods Issue Note is refused if its cash memos' delivery date is before the PJP's current working date. **The whole receive → order → issue chain must run inside one calendar day.** This is now the default assumption everywhere in the app packs and skills.
2. **No separation-of-duty control is declared for GIN approval** in the Pakistan workflow (`StockUpdateGIN v53`: Verify and Approve are the same role, 0005). Our "maker ≠ checker" rule is a QA policy, not an enforced app control — don't expect the app to block a self-approval.
3. **13 open BA questions** remain (`apps/snd/knowledge/business/OPEN_QUESTIONS.md`, class C) — e.g. where approved DA losses land in stock, whether a start-of-day step is expected, what a DSR Adjustment does to Route Settlement. Each has a default; none blocks a run.
4. **GIAS app pack is scaffolded, not wired for phase 2 yet** (no player, no framework-db rows). It reuses the existing element cache and flow JSONs from phase 1.
5. **Generated framework SQL has never been applied/replayed in the legacy engine.** Every `framework.sql` produced so far is a reviewed draft for the framework owner (gate G4); nothing has been run end-to-end through the deterministic engine.

### Upgrading from an ad-hoc setup
If your Claude session already has an older copy of this plugin cached, bump the version and refresh it (see `DEPLOY.md` → "Updating the plugin") — editing files alone does not change what's loaded.

---
*Previous versions (0.1.0–0.3.6) were internal iterations on the same machine and are not separately documented; see the plugin version history in `plugins/qa-os/.claude-plugin/plugin.json` git history from this point forward.*
