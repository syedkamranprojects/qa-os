---
name: qa-orchestrator
description: QA OS life cycle for a Jira story (intake -> analyse -> cases -> steps -> record via MCP -> scripts). Use when a QA user pastes a story or asks to run, continue or check the QA cycle for a ticket.
---

# QA OS orchestrator (v0.6)

Design: `qa-os/docs/ARCHITECTURE.md`. Questions to users: `qa-os/docs/QUESTION_BANK.md`. You run in the **main session** and stay thin:
keep state in `runs/<KEY>/<timestamp>/run.json`, give each stage to its agent with a short brief (input files -> output file),
check the output, update `run.json`. Never load full case lists, screen catalogs or the access data into your own context; query them with the tools below.

## Principles (from the user)
- **Login is the only routine human step.** Never type passwords. Every other question is a last resort: look in the app pack, the live app (read-only), the story, and earlier answers first (`decisions.json`).
- **Max 10 core cases per story**; the rest go to the `Backlog` section of `cases.json`.
- **MCP execution is a one-time recording per flow**, one data row, to capture ids, paths and messages. The legacy engine runs all cases and data variations.
- Log every obstacle in `friction.md` and fix it in software (helper, app pack), not with a question.

## Stage 0 - intake and account selection (before analysis)
1. `python runtime/qaos_run.py init <KEY> --app <app> --env <env> [--story <file>]` (env may be a placeholder until step 3).
2. **Parse the story's intake block** (`--- QA-OS --- ... --- /QA-OS ---`, see QUESTION_BANK.md) and write `decisions.json`:
   ```
   python runtime/qaos_intake.py parse <run> [--story <file>] [--screens "Screen A;Screen B"]
   ```
   - Fields (all optional): env, user, scope, market, screens, terms, data, allow, never, expected-variance. Missing values come from the app pack (`apps/<app>/knowledge/decisions.json`) or a default and are marked **assumed**.
   - The parser also runs the account selection of step 3 when screens are known (from the block, `--screens`, or `requirement.json` after analysis). If the story has no screen names yet, run it again with `--screens` after analyse.
   - It computes the bounded authorization (see step 5) and lists **warnings**: read them, mention only the ones that need a decision (e.g. "no account reaches every screen").
   - `python runtime/qaos_intake.py show <run>` prints the result. Do not ask the user anything the block or the app pack already answered.
3. **Account selection (Q-ENV-1 / Q-ENV-2), done by the parser with the tool below; you can also run it by hand:**
   ```
   python apps/<app>/tools/access_lookup.py plan-user "<screen 1>" "<screen 2>" ... [--org <orgcode>]
   ```
   - Screens = the story's screen names (from the story text, or `requirement.json` `screens` after analysis).
   - `--org` = the market of the story (`access.market_of_story` in `app.yaml`: PK/PKBD -> 010104).
   - The tool ranks every account we can log in as by how many screens its **live menu** reaches (DB access is used only where no live menu matches) and prints data notes per account.
   - Use the RECOMMENDED account when the intake block gives none. If the block names an `env`/`user`, check it against the tool: if it misses screens, tell the user in one sentence and use the recommendation.
   - If **no account covers every screen**, split the story by environment, or ask Q-ENV-1 once (with the tool's table as evidence).
   - Update `run.json` (`env`, `user`) and record the choice and reason in `decisions.json`.
   - A screen reported "DB only (not in live menu: verify)" is unconfirmed: check it when the browser is open.
4. **Unknown screen or unknown market difference?** `access_lookup.py screen "<name>"` shows route, menu path, roles per market; `features <org>` and `diff-features <orgA> <orgB>` show market configuration. The DB is ~83% current for screens; the live menu wins.
5. **Environment authorization:** `allow:` actions in the intake block count only when the chosen environment has `non_production: true` in `app.yaml`. One-way actions (approve, forward, submit, delete) count only if named in `allow:`. Everything else that changes data or stock is skipped and marked unverified.

## Knowledge-gap gate (QA lead rule, 2026-10-08) - before ANY AI execution or script generation
Before executing an AI flow (recording) or generating scripts, check that the knowledge needed is present (business pages with `[observed]`/`[stated]` facts for every action, screen, rule, message and data choice). If something is missing, **ask the user** and classify the gap:
| Gap | Examples | Action |
|---|---|---|
| **Short / ad-hoc** (answerable in chat in a few lines) | a value or data choice, which outlet type to use, the meaning of a field, an expected message, one business rule, which user/role | Ask with `AskUserQuestion` (or plainly); record the answer as `[stated <date> <name>]` in the run's `decisions.json` and, if reusable, in the business page (knowledge-intake method B); then **continue the run** |
| **Long-term** (needs a training session) | an untrained screen, module or business process (e.g. incentive -> credit note chain), an unknown market setup, a chain of several untrained options | Say what is missing and ask for training (`/qa-os:train <app>`: explain, documents or a walk). **Do NOT execute the story/flow or generate scripts** until it is trained; the run stays paused at this gate |
Never guess to fill a gap, and never take the missing knowledge from old framework flows or workbooks.

Apply this gate at the end of analysis (before cases/steps are approved) and again before recording (Stage 4) and generation (Stage 5).

## Stage 1 - analyse (checkpoint C1)
- Give story-analyst the run folder; run `qaos_run.py validate <run>`; then `stage <run> analyse done`.
- Present scope + the ambiguities in one message. Ambiguities already answered by the intake block or `decisions.md` are not asked again.
- Story-vs-app differences go to `BA_NOTE.md` (one list), not to the QA user.
- **Record every answer** the moment it arrives (QA in chat, or BA later):
  `python runtime/qaos_intake.py answer <run> --id Q-VAR-1 --kind variance|term|rule|other --key "<short key>" --value "<text>" [--ruling app-is-right|not-built|ask-ba] [--owner BA|QA] [--reusable]`
  Use `--reusable` for anything that holds for the whole app (glossary terms, variance rulings, business rules); never for story-specific answers (data, environment, scope).

## Gates (settings in `qaos.yaml` -> `gates`, `approval_phrases`)
A stage never starts until the gate before it is approved. **Approval** = the QA member says "approved", "go ahead", "yes", "LGTM" or "looks good". Anything else (a change, a question, a concern) is **feedback**: send it back to the same agent with the original brief plus the feedback, never a fresh start; if unsure which it is, ask. Gates: G1 ambiguities answered (skip if none), **G2 cases approved**, **G3 step sheet approved**, G4 framework owner applies the SQL, G5 QA confirms the Jira ticket before a comment is posted. Never post to Jira without G5.

## Stage 2 - cases (gate G2)
- test-designer (skill `case-format`) -> `cases.json` with **at most 10 core cases** (`limits.max_core_cases_per_story`) + backlog; `validate`. Present a short summary (counts, core list, backlog size) and wait for G2.

## Stage 3 - step sheet (gate G3)
- **Assisted mode (default, `qaos.yaml` -> `authoring.mode`).** Run the **`step-authoring` skill in the main session**: Claude drafts what the atlas and app pack support as *suggestions*, then asks the QA member for the next step one at a time (suggested options plus free text), rephrases free English into the predefined wording (`vocabulary/core.yaml`, checker `runtime/qaos_steps.py`), validates labels against the real screen, and asks for confirmation. The draft is `<run>/step_draft_<TCnn>.json`; the QA member's cheat sheet is `docs/QA_STEP_CHEAT_SHEET.md`. Subagents never ask the QA member questions.
- **Excel round trip:** the QA member can finalize the steps in the Excel's *Test Steps* column. Import it with `runtime/qaos_import.py` (dry run, show problems, then `--apply --approved-by` after they confirm); execution always runs from the applied draft, never from an unchecked Excel. See the `step-authoring` skill.
- step-author (skills `step-dsl`, `step-vocabulary`) turns the approved drafts into `steps.json` **and** `step_sheet.md` from `plugins/qa-os/skills/step-vocabulary/step_sheet_template.md`; in `auto` mode it also drafts the steps itself. Steps are drafted from Claude's trained business knowledge (`apps/<app>/knowledge/business/`), never from the framework atlas or existing framework flows (QA lead rule, 2026-10-08).
- Each step is `clear` or `NEEDS INPUT`; questions are listed once at the end, each with a default. Present the sheet, collect the QA member's answers in one round, and wait for G3. **Nothing is recorded before G3.**
- Readiness values: ready | needs-data | needs-verb | needs-learning | manual | deferred.

## Stage 3b - data (checkpoint C2)
- Discover fixtures yourself through the app's read APIs and grids before asking (see friction log A2/B10); ask Q-DATA only when nothing is found.
- Ask before any step that changes data/stock unless the intake block already authorizes it (Q-RISK).

## Stage 4 - record (agent `recorder`, skill `recording-protocol`)
- **Group the cases by path first** (QA lead, 2026-10-09): cases with the same screens, fields, buttons and order differ only in data and become case-data rows of one recording; cases with different actions (remove a selection, free text, another field, another screen) are a separate path. Write the grouping to `<run>/paths.json` (`[{path, label, record: TCnn, rows: [TCnn...], manual: [TCnn...]}]`), show it to the QA member as "N paths for M cases" with the G3 sheet, and record one representative case per path. Checks the engine cannot assert (list contents, "not shown twice", alert text) are marked manual.
- Per path, delegate to the **recorder** agent with a short brief: run folder, ONE case id, app, env, the approved sheet and that case's data row - nothing else (no app knowledge, no ids); it discovers screens, elements, ids, tabs and messages live. The other cases of the same path become case-data rows at generation. It runs the flow through the browser MCP with one data row, stops at each switch point for the QA member's login, and writes `exec/results.json`, `recording_<flow>.json` (passing flows only) and `friction.md`.
- The recorder is the only agent with the browser. Relay each switch-point message to the QA member (who to log in as, role, company, distributor) and pass their "logged in" back. Check the counts it returns; do not re-run a step it reported blocked without a decision.
- One calendar day: for a chain that creates stock or orders, the whole chain runs on the same day (see `recording-protocol`).

## Stage 5 - generate (agent `framework-generator`, skill `framework-conventions`)
- Delegate to **framework-generator**: recordings -> `flow_spec.json`, `framework.sql`, `framework_rollback.sql`, the case-data workbook and `review_note.md`, all under `framework/`. It has no browser and never applies SQL.

## Stage 5b - verify (agent `verifier`, checkpoint G4)
- Delegate to **verifier** (read-only): traceability, SQL and workbook validation against the live schema, honest counts -> `review.md`. Present its verdict, the counts and the findings; the framework owner reviews and applies the SQL (G4). Ask the framework owner only Q-FW questions, once.

## Stage 6 - promotion (end of every run)
`python runtime/qaos_promote.py <run>` is a **dry run**: it lists the reusable terms, variances and rules the run would add to the app pack, what is already there, and any conflict. Show the list to the user in one message and apply only after their OK:
`python runtime/qaos_promote.py <run> --apply`. Conflicts are never overwritten unless the user says so (`--force`). Entries carry status observed < stated < ruled and provenance (story, date, who); the app pack (`apps/<app>/knowledge/decisions.json`, readable copy `decisions.md`) is shared by the whole QA team, so this is the one place where a wrong entry hurts other people.

## Report back
Workbook/SQL paths; core vs backlog counts; what was recorded vs authored-unverified; the BA note; friction items fixed or open; how many questions were asked (target: login only).

## Tools (Claude runs these; QA users do not)
| Tool | Use |
|---|---|
| `apps/<app>/tools/access_lookup.py` | `plan-user`, `screen`, `user --can`, `who`, `features`, `diff-features`, `validate-live` |
| `plugins/qa-os/runtime/qaos_helpers.js` | page helper injected via the browser MCP |
| `framework/tools/qaos_record_multi.py`, `gen_framework_sql.py` | recording + rows.json -> multi-screen flow spec + case data -> SQL + workbook |
| `runtime/qaos_run.py` | run folder, `validate` (also checks `decisions.json` and the 10-core-case cap), stage state |
| `runtime/qaos_intake.py` | `parse` the intake block -> `decisions.json`; `answer`; `show` |
| `runtime/qaos_export.py` / `runtime/qaos_import.py` | draft -> Excel record; edited Excel -> checked draft (round trip) |
| `runtime/qaos_steps.py` | step checker and draft keeper: `check`, `labels`, `suggest`, `add`, `undo`, `render`, `lint`, `index` |
| `runtime/qaos_promote.py` | dry-run / `--apply` promotion of reusable decisions into the app pack |
The older Python player (`runtime/qaos_player.py`) is an interim fallback only; it types credentials from env and is no longer the main path.

## Step language (applies to Stage 2 and to every recording)
Write and report test steps only in the standard vocabulary (`docs/STEP_VOCABULARY.md`, definitions in `apps/<app>/steps/library.yaml`): `[Actor] Verb Object ...`, roles not user names, one verb per step, `Expect:` lines for checks. Maker and checker are different users: put a `Logout` / `Login as <role>` pair (a switch point) between them and stop for the QA lead's login. QA members' usage guide: `docs/QA_GUIDE.md`.
