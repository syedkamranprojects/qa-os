---
name: step-vocabulary
description: The standard QA OS step language ([Actor] Verb Object), the step sheet QA approves at gate G3 (each step marked clear or needs-input, with trace keys), and how business steps expand into executable primitives. Use when writing, reviewing or executing a step sheet.
---

# Step vocabulary and the step sheet

Full vocabulary: `docs/STEP_VOCABULARY.md`. Per-app definitions (parameters, expansion, expected messages, gotchas, `verified`): `apps/<app>/steps/library.yaml`. Actors and users: `apps/<app>/app.yaml` (`roles`). Technical layer underneath: the `step-dsl` skill.

## Rules
- One line = one step = one verb from the vocabulary; number the steps; start with the **actor in brackets** (`[Maker]` or `[Checker]`, the only two roles; a role can have several users, first = default). Roles, never user names or passwords.
- Use the screen's own names for screens, fields, buttons and statuses. No waits, element ids or locators in a step: those belong to the library and the helper.
- Values come from the data row or from `Remember <Field> as NAME` placeholders; `<date>` = today.
- Every user change is `Logout` then `Login as <role>` (a **switch point**); the run stops there and the QA member logs in.
- Approval is done by a **different user** on the same option (`Approve <Document>`).
- `Expect:` lines hold the app's real message text. If the text was never observed, write `Expect: message (text to be recorded)`; never guess it.
- A step not in the vocabulary is written `Do: <sentence>` and treated as manual until it is added to the library.

## The step sheet (gate G3)
The step sheet is what the QA member reviews and approves **before** any recording. It removes trial and error during the run. Template: `step_sheet_template.md` in this skill's folder. Every step carries:
| Field | Meaning |
|---|---|
| `#` and `[Actor] step` | the vocabulary step |
| `state` | `clear` (tables, app pack and a live check agree) or `NEEDS INPUT` (they disagree or something is unknown; a question is attached) |
| `trace` | for a replayed framework flow: `<group>:<seq>:<flow>` (add `:<screen>:e<n>` when a specific event is meant) |
| `expect` | observed message/status, or "to be recorded" |
| `risk` | `read-only`, `changes data`, `changes stock`, `one-way` (approve/forward/submit/delete) |

Rules for the sheet:
- Draft it from the atlas (`build_atlas.py --find`, `flows/<id>.md`) and the app pack, never from memory. List every question **once**, at the end, each with a default: "Default if you skip: ...".
- Ask only what the sources cannot answer: business decisions, or a disagreement between the framework config and the live app. Missing locators, waits and navigation quirks are not questions.
- Mark each `changes data` / `one-way` step against `decisions.json` authorization: allowed, or skipped-unverified.
- The sheet ends with the **switch points** (users in order) and the **one-day** warning if the chain creates stock or orders.

## Expansion (how a business step runs)
1. Look the step up in `library.yaml` and expand it into primitives (`login`, `navigate`, `enter`, `choose`, `click`, `select_row`, `verify_ui`, `capture` ...). `verified: false` entries run as recording steps and are flagged.
2. The recorder runs them one at a time (see `recording-protocol`), attaches trace keys, and records observed messages.
3. The recording becomes framework events (`framework-conventions`).
4. A step that succeeded live but has no library entry gets one added after the run (name, parameters, expansion, message, gotchas).
