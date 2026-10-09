# QA OS learning standard (v1, 2026-10-01)

How QA OS learns an application's business **before** it writes test cases and steps from user stories.
It applies to every application. Only the **sources** change from app to app; the **output**, the
**phases** and the **quality bar** stay the same.

Related: `ARCHITECTURE.md` §7A (screen-level harvest by the app-cartographer), `FINAL_DESIGN.md`
(life cycle and gates), `apps/<app>/knowledge/business/_TEMPLATE.md` (option page template).

---

## 1. Why a standard

- Most applications under test have **no user guide and no specification**, and the ones that have
  them have them in different shapes.
- QA OS must still reach the same result for every app: a body of business knowledge that the
  story-analyst, test-designer and step-author can read **without knowing how it was learned**.
- So learning is split in two:
  - a **fixed output contract** (what "knowing the app" means, §3); and
  - **pluggable source playbooks** (where the knowledge comes from, §5).
- The method used for S&D (replaying the legacy framework's flows) is **one source type, not the
  standard**. Another app may learn from a user guide, a BA, or live exploration only.

## 2. Principles

1. **Same output, any source.** Every source type writes into the structure in §3. Downstream agents
   only read that structure.
2. **Business first, not locators.** Learning captures purpose, actors, inputs, rules, messages,
   statuses, effects and dependencies. **Element ids and locators are not part of learning.** The
   recorder captures them later, when it executes approved steps to generate the framework scripts.
3. **Every fact is tagged with its confidence** (§3.4). Only `[observed]` and `[stated]` facts may be asserted in a test.
4. **Unknowns are written down, not guessed.** Each unknown becomes an open question with a default
   and a class (§3.5).
5. **Learning is a phase with a gate.** It ends with QA-lead sign-off (G0) per area (§6).
6. **Learning is incremental.** Each story run, recording and BA answer adds to the same pages
   (promotion, §7). Nothing is re-learned from scratch.
7. **Safe by default.** Sources are read-only. Live walks change data only on `non_production`
   environments, only for flows the QA lead named, and Claude never types credentials.

## 3. The output contract (identical for every app)

All business knowledge lives in `apps/<app>/knowledge/business/`.

### 3.1 Levels

| Level | What | File(s) | Definition of done |
|---|---|---|---|
| **L1 Domain map** | Business areas, the documents of each area, the roles, the vocabulary | `INDEX.md` (areas + document map), `glossary.md` | Every area named; every document type has creator, approver, status chain and effect (even if tagged `[unknown]`); roles listed with their users per environment |
| **L2 Process chains** | End-to-end business cycles: order of options, hand-offs between roles, cross-document and day/date rules | `INDEX.md` §1, or `process_<name>.md` when there are several cycles | Every step of the cycle points to an L3 page; every role switch is shown; date and sequence constraints are stated |
| **L3 Business option pages** | One page per business option (screen/transaction a user works in) | `<area>/<option>.md`, using `_TEMPLATE.md` | All 13 template sections present; sections 1, 2, 5, 6, 7 have no `[unknown]`; section 9 has at least one observed message for each save, forward or approve action that was executed |
| **L4 Screen knowledge** | Menu path, fields, labels, widgets, mandatory markers, dropdown sources | `knowledge/screens_*`, `menu`, `i18n` (app-cartographer, ARCHITECTURE §7A) | Every L3 page's screens exist at L4 with real labels |
| **Cross-cutting** | Document lifecycle, rules, open questions, live checklist, evidence log | `document_lifecycle.md`, `OPEN_QUESTIONS.md`, `LIVE_LEARNING_CHECKLIST.md`, `LIVE_FINDINGS.md` | Kept current at the end of every learning session |

L4 is the app-cartographer's job. L1–L3 are this standard's job.

### 3.2 The option page (L3)

Use `_TEMPLATE.md` without dropping sections. When a section has nothing yet, write `[unknown]` and add an open question.

| # | Section | Must answer |
|---|---|---|
| 1 | Purpose | What the business does here, and where it sits in the cycle |
| 2 | Actors and roles | Maker / Checker (the app's roles) and what each can and cannot do on this option |
| 3 | Documents and master data | Document types, number formats, master data needed |
| 4 | Inputs | Real field labels, mandatory fields, defaults, where each value comes from |
| 5 | Process | Numbered steps in the standard vocabulary (`[Actor] Verb Object`) with the trace key |
| 6 | Outputs and effects | Status, stock, finance and related-document effects, plus how to check them (before/after) |
| 7 | Statuses and transitions | from → action → to, by whom |
| 8 | Rules and validations | One rule per line, with its evidence |
| 9 | Messages | Exact texts, and when they appear |
| 10 | Dependencies | What must exist first, what is handed to later options, date rules |
| 11 | Test design hints | Positive, negative and boundary cases, plus traps (what a green run would not prove) |
| 12 | Open questions | `Q: … | Default: … | Class: A/B/C | Evidence: …` |
| 13 | Sources | Which source types and items (flow ids, tables, document sections, run folders) |

### 3.3 Front-matter (for lookup)

Each L3 page starts with a front-matter block, so a story touching one option loads only the pages it needs:

```yaml
---
option: Goods Issue Note
area: delivery_and_returns
doc_types: [GN-01]
screens: [<option ids>]
framework_flows: ["00050001", "00780001"]   # only if the app has legacy flows
markets: [PK]
roles: [Maker, Checker]
depends_on: [order_booking, stock_allocation, delivery_date_change]
sources: [legacy-framework-replay, app-db, live-walk]
updated: 2026-10-01
---
```

A generated `knowledge/INDEX.json` collects the front-matter. At Stage 0 the orchestrator matches a story's terms to it.

### 3.4 Confidence tags (same for every app)

| Tag | Meaning | May be asserted in a test? |
|---|---|---|
| `[observed]` | Seen live in this app/env (walk, recording, run) | Yes |
| `[stated]` | Said by an owner: user guide, spec, BA/QA ruling (with name and date) | Yes, unless observed behaviour contradicts it (then raise a defect or a question) |
| `[db]` | Declared by the app DB or the legacy framework tables | As an expectation marked "to be confirmed live" |
| `[code]` | Read in the application's source code: `[code <branch>@<commit> <path>:<line>]` (what that service does, not the business intent; callers may decide parts of the behaviour) | As an expectation marked "to be confirmed live"; a disagreement with `[stated]` is a contradiction for the trainer, never an override |
| `[jira]` | Read in a Jira ticket: `[jira <KEY>]` (story, bug or CR; note its region and status) | As an expectation marked "to be confirmed live"; a ticket in status New / Open describes a wish or a bug, not current behaviour |
| `[inferred]` | Concluded by Claude from names or structure | No; needs confirmation |
| `[unknown]` | Not determined | No; must have an open question |

When two sources disagree, keep both with their tags and add an open question. Never silently overwrite.

### 3.5 Open-question classes

- **A, safe default:** Claude proceeds with the stated default.
- **B, verify live:** goes to `LIVE_LEARNING_CHECKLIST.md` and is settled by a walk.
- **C, business decision:** batched for the BA. The default holds until answered.

## 4. What learning does NOT do

- **No element ids or locators.** Those come from the recorder at execution time.
- **No test cases or framework SQL.** Learning feeds those stages, it doesn't produce them.
- **No regression verdicts.** A defect seen while learning is noted (L3 §8 or §12) and reported. Learning doesn't decide pass or fail.
- **No bulk data.** It uses one data set per walk.

## 5. Sources: pluggable playbooks

Each app declares its sources and their trust order in `app.yaml`:

```yaml
learning:
  sources:                          # in trust order; the first one that answers a question wins, later ones confirm
    - type: legacy-framework-replay
      connector: selenium-framework-db
      scope: { groups: ["11"], status: "Y" }  # active rows only, in sequence order
    - type: app-db
      connector: snd-schema
    - type: live-walk
      env: cnr1dev1
    - type: sme
      owner: BA
  roles_source: environments.<env>.roles   # Maker / Checker -> users
```

Every playbook has the same five parts: **when to use it**, **inputs**, **procedure**, **mapping to the output contract** and **limits**.

### 5.1 `user-guide` (documentation or specification exists)
- **Use when:** a user guide, functional spec, SOP or training deck exists.
- **Procedure:**
  1. Index the document by chapter, mapped to areas and options.
  2. Extract purpose, actors, steps, rules and messages per option, tagged `[stated]` with a document reference.
  3. Confirm a sample live.
- **Limits:** documents age, so a walk must confirm at least the statuses and messages before they're asserted.

### 5.2 `legacy-framework-replay` (existing automated flows exist)
The framework DB is a record of how the business was automated. It shows option order, role switches, inputs and expected values.
- **Use when:** the app already has flows in `CTA_CONFIG_ASSERTION` (S&D: groups 11, 1, 61, 63, …).
- **Inputs:** the group id, the rows `fct_pr_gtfd_group_test_flow_detail`, and per flow its screens, fields, events and queries, plus the case-data workbook for the market.
- **Procedure:**
  1. Read the group's rows; keep **status Y only**, ordered by `pgtfd_sequenceno`.
  2. Build the login segments: the row's user (`plu_serial_no`), and `pgtf_testflow_login_status = Y` means log out and log in as that user. A row with no user runs as the current session.
  3. Write the L2 chain from the rows.
  4. For each flow: read its framework rows and workbook values to learn the screens, inputs and expected results (tag `[db]`).
  5. Walk it live (§5.4), recording business facts only.
  6. Write the L3 page.
- **Mapping:**
  - group → L2 chain;
  - flow → L3 page sections 4, 5 and 10;
  - framework queries and expected values → section 6;
  - user per row → section 2.
- **Limits:**
  - Shows only what was automated, mostly the positive path.
  - Framework rows may be out of date compared with the app (drift).
  - Inactive rows (status N) are not part of the intended cycle.
- **Not the platform standard:** this is S&D's main source because S&D has no documentation. It is unrelated to the framework DB's other role as the output target (§8).

### 5.3 `app-db` (always available)
- **Use for:** documents, document types, status code tables, workflow definitions, role-option grants, lookups, and the data dictionary (tag `[db]`).
- **Limits:**
  - Says what is possible, not what the business does.
  - Per-role button permissions and screen behaviour are often not in the DB.

### 5.4 `live-walk` (always, to confirm)
- **Use for:** confirming `[db]`, `[stated]` and `[inferred]` facts; exact messages; status changes; stock and finance effects via before/after snapshots.
- **Rules:**
  - Every walk starts from a fresh login, typed by the QA member.
  - Flows that change data run only on `non_production` environments and only when the QA lead named them.
  - Never click one-way actions (e.g. Generate Opening Balances, Reject, Terminate, Bounce) unless the flow is about them.
  - One data set per walk; same-day rules respected.
- **Output:** facts tagged `[observed]` in the L3 pages, plus raw evidence in `LIVE_FINDINGS.md`.

### 5.5 `story-history` (Jira)
- **Use for:** past stories, acceptance criteria, comments and defects, which give rules, edge cases and known variances (tag `[stated]` for accepted criteria, `[observed]` for defects reproduced).
- **Limits:** a story describes a change, not the whole option.

### 5.6 `sme` (BA / QA lead / product owner)
- **Use for:** class C questions and rulings. Answers are recorded with owner and date (`[stated]`) and promoted with `qaos_promote.py`.

### 5.7 Adding a source type
Write a playbook with the five parts above, add it to this section, and map its output to §3. Downstream agents don't change.

## 6. Learning phases (same for every source)

| Phase | What happens | Output |
|---|---|---|
| **0 Scope** | QA lead names the area, cycle or group, the market and the env. Claude lists the options in scope and the sources to use. | `learning_plan.md` in the run folder (options, sources, login segments, data needed, risks) |
| **1 Harvest** | Read the static sources (docs, framework DB, app DB, stories). No browser. | Draft L1/L2, draft L3 pages tagged `[db]` / `[stated]` / `[inferred]`; open questions |
| **2 Walk** | Execute the scoped flows live, in order, with the right roles. Business facts only. | `[observed]` facts, messages, before/after effects; `LIVE_FINDINGS.md` |
| **3 Consolidate** | Merge into the L3 pages; resolve or record contradictions; update L1/L2, glossary, lifecycle. | Updated pages |
| **4 Verify** | Run the checks in §7: template completeness, the definitions of done (§3.1), tag rules. | Coverage report |
| **5 Questions** | Class A defaults applied, class B added to the live checklist, class C batched for the BA. | `OPEN_QUESTIONS.md`, BA note |
| **G0 Sign-off** | QA lead reviews the coverage report and the pages for the area. | Area marked `learned` in `INDEX.md` |

Story work (FINAL_DESIGN stages 1–3) on an area should start only after G0. Before G0, the test-designer must label cases that rely on unverified knowledge.

## 7. Quality checks and coverage report

A learning session ends with a short report (`learning_report.md`) that gives, per area:

- options in scope / options with an L3 page / pages meeting the definition of done;
- share of facts by tag (observed / stated / db / inferred / unknown);
- open questions by class, and which ones this session closed;
- contradictions found (source vs live, page vs page);
- the flows walked, and the flows not walked with the reason;
- data left in the environment (document numbers), so later runs don't reuse it by mistake.

**Promotion:** facts learned in later story runs, recordings or BA answers go into the same pages
through `qaos_promote.py` (dry run by default). An observed fact upgrades a `[db]` or `[inferred]` one. A contradiction is never auto-applied.

## 8. The framework DB has two roles: keep them apart

| Role | Status | Where it's defined |
|---|---|---|
| **Output target:** generated scripts are written as `CTA_CONFIG_ASSERTION` rows + case-data workbook | **Platform standard for every app** | `framework/cta_config_assertion.md`, skill `framework-conventions`, agent `framework-generator` |
| **Learning source:** existing flows are read to learn the business | **One source type** (§5.2), used only where an app has existing flows | This document §5.2; `app.yaml` `learning.sources` |

Learning from the framework doesn't change how scripts are generated, and an app with no legacy flows still generates scripts the same way.

## 9. Current S&D state against this standard

| Item | State |
|---|---|
| Sources | `legacy-framework-replay` (group 11, PK) main; `app-db` (snd-schema); `live-walk` (cnr1dev1); `sme` (BA note pending). No user guide. |
| Roles | Maker = Auto_Multi_Orga (default), Automation; Checker = Auto_Tssm (`app.yaml`) |
| L1 | Done (`INDEX.md`, `glossary.md`) |
| L2 | Daily Cycle chain written from the framework; to be confirmed by the full group 11 walk |
| L3 | 23 pages; most sections tagged `[db]` / `[inferred]`; Dispatch Advice, Order Booking, Stock Inquiry partly `[observed]` |
| Front-matter / `INDEX.json` | Not done |
| G0 | No area signed off yet |
| Next learning session | Group 11, PK, cnr1dev1: 46 active flows in sequence, 11 login segments, within one calendar day, business facts only |

## 10. Implementation backlog (after the first session confirms the method)

1. Skill `app-learning`: this standard in short form plus one playbook file per source type (`references/sources/<type>.md`).
2. Agent for business learning: extend app-cartographer (L4) with L1–L3, or add a `domain-analyst` agent. Decide after the group 11 session.
3. `app.yaml` `learning:` block for `snd` (and `gias`), with `qaos_config.py validate` checking it.
4. Front-matter on the existing 23 pages, plus a `build_knowledge_index.py` that generates `INDEX.json`.
5. `/qa-os:learn` extended: `--source <type> --scope <area|group>`, producing `learning_plan.md` and `learning_report.md`.
6. A coverage checker (template sections, definitions of done, tag rules) that writes the §7 report.
