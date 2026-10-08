# QA OS final design (v2, 2026-09-30)

This settles the design in `ARCHITECTURE.md` v1.0 and replaces its §6 (agents) and §12 (checkpoints). It keeps what worked in the 2026-09-24..29 runs and adds the useful parts of the "orchestrator + sub-agents + skills + persistent knowledge" pattern. API testing is out of scope.

## 1. Why a v2: what went wrong in practice
- **The agents and skills were designed, but none of them ever loaded.** The `qa-os` plugin is not registered in the workspace (`.claude/settings.json` has no `extraKnownMarketplaces` / `enabledPlugins`). The Agent tool only offers the built-in agent types, so every stage ran inline in the main session.
  - That caused the context compactions, the lost instructions, and the rediscovery of the same UI quirks.
- The steps were discovered by trial and error during recording (Order Editing), when they should have been approved before it.
- Nothing proves the final product: no generated SQL has been validated or replayed by the legacy engine.

## 2. Principles (final)
1. **Thin orchestrator, specialist agents.** The main session holds the conversation and `run.json`. Each stage runs in its own agent context with its own skill and a **restricted tool list**. Files are the hand-off.
2. **Standards live in skills, not in agent prompts.** You change a skill to change the quality bar, and several agents share one skill.
3. **Gates, not autonomy.** Each stage ends at a gate, and the next stage never starts without explicit approval.
   - **Approval** = "approved", "go ahead", "yes", "LGTM".
   - **Anything else is feedback.** The stage is re-delegated with the original brief plus the feedback, never from a fresh start.
4. **User intervention is minimised, not eliminated.** Budget per story: 2 approvals (cases, step sheet), the logins at switch points, and 1 review (SQL + workbook). Everything else is solved in software and logged in `friction.md`.
5. **Record once, replay many.** The MCP recording uses one data row per flow. The legacy engine does all regression and bulk runs.
6. **Knowledge compounds.** Every run promotes verified facts to the app pack. Facts are tagged, and only the tags matching the story are loaded.
7. **Safe by construction.** Connectors are read-only. Claude never types credentials, never applies SQL, and only makes data-changing steps on `non_production` envs.

## 3. Pipeline and gates

| Stage | Agent | Output | Gate (who) |
|---|---|---|---|
| 0 Intake | orchestrator (`qaos_intake.py`) | `decisions.json`, `run.json` | asks only for fields missing from the story's QA-OS block |
| 1 Analyse | story-analyst | `requirement.json` + ambiguities | **G1** BA/QA answers ambiguities (skipped if none) |
| 2 Cases | test-designer | `cases.json` (max 10 core, rest backlog) + workbook | **G2** QA approves cases |
| 3 Step sheet | step-author | `step_sheet.md` + `steps.json` in the business vocabulary, each step `clear` or `needs input` | **G3** QA approves the steps and answers the `needs input` items |
| 4 Data | data-engineer | `data.json` (one row per flow, discovered from the DB) | none, unless seeding is needed |
| 5 Record | recorder | `recording_*.json`, `friction.md`, locators | the only interventions are **logins at switch points** |
| 6 Generate | framework-generator | `flow_spec.json`, `framework.sql`, rollback, case-data workbook | none (must pass the validator) |
| 7 Verify | verifier | `review.md` (traceability + SQL validation) | **G4** framework owner reviews and applies |
| 8 Report | reporter | execution report; Jira comment | **G5** QA confirms the ticket before posting |
| Wrap-up | orchestrator (`qaos_promote.py`) | knowledge candidates | QA picks which to promote |

G3 is the step sheet you asked for after the Order Editing struggle. It moves the back-and-forth out of the recording.

## 4. Agents (final roster)

| Agent | State | Skills | Tools (restricted) | Model |
|---|---|---|---|---|
| story-analyst | written | case-format, jira-conventions | Read/Write run folder, Atlassian MCP (read) | opus |
| test-designer | written | case-format | Read/Write, Python | opus |
| step-author | written | step-vocabulary, step-dsl | Read/Write, snd-schema (read), app pack | sonnet |
| data-engineer | written | data-recipes | Read/Write, app DB (read) | sonnet |
| **recorder** | **missing** (replaces "executor") | recording-protocol, step-vocabulary | Selenium MCP, Read/Write run folder. No DB and no SQL | sonnet |
| **framework-generator** | **missing** (was "script-generator") | framework-conventions | selenium-framework-db (read), Python, Read/Write. No browser | sonnet |
| **verifier** | **missing** | framework-conventions | Read-only + selenium-framework-db (read) | opus |
| **reporter** | **missing** | report-template, jira-conventions | Read, Atlassian MCP (comment only, after G5) | sonnet |
| app-cartographer | written | app-knowledge | app DB (read), Selenium MCP | sonnet |
| bulk-data-factory | later | casedata-contract | app DB + framework-db (read), Python | sonnet |

Agents stay one level deep. Only the orchestrator spawns them.

## 5. Skills (standards)

| Skill | State | Holds |
|---|---|---|
| qa-orchestrator | written (v0.3) | stage machine, gates, approval phrases, re-delegation rule |
| step-dsl | written | DSL v1 primitives and the player |
| step-vocabulary | **move** from `docs/STEP_VOCABULARY.md` + `apps/<app>/steps/library.yaml` | `[Actor] Verb Object` steps, switch points, maker/checker |
| case-format | **missing** | case fields, 10-core cap, coverage heuristics, naming, team workbook |
| recording-protocol | **missing** | login hand-off, helper re-injection, background script + polling, real clicks for tabs/checkboxes, toast capture, friction logging |
| framework-conventions | **missing** | how a `CTA_CONFIG_ASSERTION` flow is built (menu group, screens, fields, events, custom events 0001-0014, group flow + login status), learned from group 11 |
| report-template | **missing** | execution report layout, Jira comment format |
| jira-conventions, data-recipes, app-knowledge, casedata-contract | missing / partial | as named |

## 6. Knowledge (persistent, tagged)
- Every file in `apps/<app>/knowledge/` gets front-matter: `tags` (screen ids, flow ids, doc types, market), `source` (db-declared / observed / stated), `updated`.
- `knowledge/INDEX.json` is generated from the front-matter. At Stage 0 the orchestrator matches the story's screens and terms to the tags and passes **only the matching paths** to each agent.
- Promotion (`qaos_promote.py`) stays dry-run by default. Only reusable rulings and verified behaviour are promoted.

## 7. Tools and resources

| Need | Have | Missing |
|---|---|---|
| Story | Atlassian MCP | **SDMS project access** |
| App metadata | snd-schema, gias-schema (read) | newer data dictionary (Van Sales tables) |
| Framework metadata | selenium-framework-db (read) | **a test copy of CTA_CONFIG_ASSERTION where generated SQL can be applied and replayed** |
| Browser | Selenium MCP + injected helper | **`qaos-browser` MCP** (below) |
| People | QA lead | **named framework owner** (validates SQL), **BA contact** (rulings), **a test-user sheet per role and market** (maker/checker/stock controller) |
| Governance | guardrail hook (Bash/Write/Edit) | SubagentStop schema check, URL allow-list, audit log (ARCHITECTURE §11.2) |

**`qaos-browser` MCP**: wraps the fixes we keep redoing by hand as stable tools:
- `wait_for_login(user)`: pause until the QA lead has logged in, then verify the user shown.
- `switch_user(role)`: log out and hand off to the QA lead.
- `navigate(menu)` by sidebar search.
- `fill`, `choose` (DevExtreme), `filter_grid`, `click_real`.
- `capture_toast`, `accept_alert`.
- Helper re-injection after every login.

This removes the ~30 s script-timeout churn and makes recordings the same for every QA member.

## 8. Gap register (what is missing to reach the goal)

| # | Gap | Priority | Fix | Owner |
|---|---|---|---|---|
| 1 | ~~Plugin never registered~~ **DONE 2026-09-30** (plugin v0.2.0 enabled at project scope) | **P0** | add the marketplace + `enabledPlugins` to `.claude/settings.json`; restart; check the agents appear | Claude (needs your OK to edit settings) |
| 2 | ~~recorder, framework-generator, verifier agents~~ **WRITTEN 2026-09-30** (needs a restart to load; first live use pending) | **P0** | write them from what worked in the group 11 replay | Claude |
| 3 | ~~recording-protocol, framework-conventions, case-format, step-vocabulary skills~~ **WRITTEN 2026-09-30** | **P0** | extract from `framework_flows/*.md`, `friction.md`, `STEP_VOCABULARY.md` | Claude |
| 4 | No proof the generated SQL runs in the legacy engine | **P0** | read-only SQL validator (ids, FKs, event chains vs group 11) + **one flow applied on a test copy and replayed** | Claude (validator), framework owner (apply + replay) |
| 5 | ~~Step-sheet gate (G3) not in the orchestrator~~ **DONE 2026-09-30** (orchestrator v0.4, template in step-vocabulary) | **P0** | add the `step_sheet.md` template + G3 to qa-orchestrator | Claude |
| 6 | Knowledge not tagged; whole packs are loaded | P1 | front-matter + `INDEX.json` + Stage 0 matching | Claude |
| 7 | `qaos-browser` MCP | P1 | build it from `qaos_helpers.js` + recording-protocol | Claude |
| 8 | Business steps are not compiled into DSL/recording | P1 | a compiler from `library.yaml` to DSL (`switch_user`, `filter_grid` primitives) | Claude |
| 9 | Hooks from §11.2 (schema check at SubagentStop, URL allow-list, audit) | P1 | plugin `hooks/hooks.json` | Claude |
| 10 | Jira SDMS access, BA contact, framework owner, per-role test-user sheet | P1 | organisation | QA lead |
| 11 | reporter + Jira comment | P2 | agent + report-template | Claude |
| 12 | bulk-data-factory | P2 | as ARCHITECTURE §13A | Claude |
| 13 | GIAS app pack from the existing GIAS caches | P2 | move `.claude/element-cache/gias` into `apps/gias` | Claude |
| 14 | KPO_mp password pasted in chat | hygiene | rotate | QA lead |

**Definition of done for the platform:** a QA member installs the plugin, pastes a story with a QA-OS block, approves cases (G2) and the step sheet (G3), logs in at the switch points, and receives a validated `framework.sql` + workbook. The framework owner applies them, and the legacy engine replays them with no AI.
