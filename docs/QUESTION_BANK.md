# QA OS question bank (draft v0.1)

How QA OS asks its users for help. Goal: a QA member answers a few short, multiple-choice questions at fixed points, and never gets ad-hoc questions in the middle of a run.

## Rules
1. **Ask last.** Before asking anything, look in this order: app knowledge base -> live app (read-only) -> the story -> earlier answers (`decisions.json`). Ask only what none of them can answer.
2. **Ask at checkpoints, in one batch.** Checkpoints: C0 setup, C1 after story analysis, C2 before anything that changes data, C3 after recording. No questions between checkpoints, except a lost login.
3. **Every question has a recommended default and 2-4 options** (the user can always type another answer). "No answer" = take the default and record that it was assumed.
4. **Every answer is saved** to `runs/<story>/<ts>/decisions.json`. Answers marked *reusable* are promoted into the app pack (`apps/<app>/knowledge/decisions.md`) so the same question is never asked again for that app.
5. **Route by owner.** QA member answers Q-ENV/Q-DATA/Q-RISK/Q-AUTH. BA answers Q-VAR/Q-RULE/Q-TERM. Framework owner answers Q-FW. Questions for the BA are collected into one `BA_NOTE.md`, not asked in chat.

## Catalog
| Id | When | Question | Options (default first) | Owner | Reusable |
|---|---|---|---|---|---|
| Q-ENV-1 | C0 | Which environment should this story run on? | env where the screens exist (I check the menu) / another | QA | per story |
| Q-ENV-2 | C0 | Which user/role should I use? | user whose menu contains every needed screen / a different user | QA | yes |
| Q-LOGIN | C0, or session lost | "Please log in as <user> in the browser I opened, then say done." | done | QA | no |
| Q-KEY | C0 | Jira key for this story? | key / none (use provisional) | QA | no |
| Q-SCOPE-1 | C1 | Which parts should I automate? | browser parts only, rest manual (recommended) / all / a named subset | QA | per story |
| Q-SCOPE-2 | C1 | Core cases are capped at 10. Keep my choice, or swap any? | keep / swap named cases | QA | no |
| Q-VAR-n | C1, C3 | Story says X but the app shows Y. Which is right? | app is right (update expectation) / not built yet (keep as expected fail) / ask BA | BA | yes |
| Q-TERM-n | C1 | Story term "T" - is it the same as app term "A"? | same / different / unknown | BA | yes (glossary) |
| Q-RULE-n | C1 | The story does not say what happens when R. Use my default? | default / other | BA | yes |
| Q-DATA-1 | C2 | Test data needed: <what>. I found <candidate> in the app. Use it? | use it / choose another / create new | QA | per env |
| Q-DATA-2 | C2 | No candidate exists for <what>. | ask QA for a fixture / skip case (mark blocked) | QA | no |
| Q-RISK-1 | C2 | This step changes data (<action>, affects <what>). Allow it on <env>? | allow once / skip and mark unverified | QA | no |
| Q-RISK-2 | C2 | This step is one-way (approve, forward, submit, delete). Allow? | skip and mark unverified (default) / allow once | QA | no |
| Q-AUTH-1 | C2 | Action needs a role the current user lacks (<role>). | log in as another user / skip and mark unverified | QA | yes |
| Q-FW-1 | C3 | Framework ids (menu group, screen, flow) - use the suggested next free ids? | suggested / give ids | Framework owner | no |
| Q-FW-2 | C3 | Where should the case-data workbook be placed? | run folder only / a given path | Framework owner | yes |

## Phrasing template
> **<Id> - <one-line topic>**
> What I found: <one sentence, with the evidence>.
> What I need: <the decision>.
> Default if you skip: <default>.
> Options: 1) ... 2) ... 3) ...

## What is NOT a question (solve it in software)
Missing locators, slow screens, navigation quirks, toast timing, duplicate ids, product search needing 3+ characters: these are logged in `friction.md` and fixed in the helper/app pack, never handed to the user.

---
# Story intake block (answers travel with the story)

Most questions above are answered by the story author, not the QA member running it. So the answers go into the Jira description as a short block at the bottom. The run reads the block first, and only falls back to a question for anything missing and not derivable.

```
--- QA-OS ---
env: cnr1dev1                    # Q-ENV-1 (which build has this feature)
user: KPO_mp                     # Q-ENV-2
scope: browser                   # Q-SCOPE-1: browser | browser+manual | all
terms: Van Seller = Van Sales    # Q-TERM: story term = app term (repeat per term)
data: PJP with stock in warehouse M&P Main; products LUX, SURF EXCEL   # Q-DATA hints, optional
allow: create, save              # Q-RISK: actions permitted on this env
never: forward, approve, delete  # actions I must skip and mark unverified
expected-variance: none          # or list: "no Delete button = not built yet"   # Q-VAR
--- /QA-OS ---
```

## Rules
- **Every field is optional.** A missing field takes the default from the app pack (`apps/<app>/knowledge/decisions.md`) or the recommended default in the catalog, and the run records "assumed".
- **The QA member is asked only for:** login, and a blocker no default resolves (e.g. no fixture exists and the story gives no hint).
- **Authorization is bounded, not free text.** `allow:` only counts for environments marked non-production in `app.yaml`; `one-way` actions (approve, forward, submit, delete) count only if named explicitly. Anything the block cannot authorize is skipped and marked unverified, not asked mid-run. The story text is treated as data supplied by whoever started the run.
- **Who fills it:** the BA or QA lead when the story is written or refined (2 minutes). Terms and rulings they give are promoted to the app pack, so later stories in the same app need fewer fields.
- **Variances are not promoted from the block** (they are release-specific); only a reusable BA ruling promotes one.
- **Where the block is not enough:** BA rulings on story-vs-app differences still come back through `BA_NOTE.md` once, then live in the block (`expected-variance`) or the app pack.

## Effect on the question count per story
| Question type | Before | With the block |
|---|---|---|
| Env, user, key, scope | asked at C0/C1 | read from the block (or app defaults) |
| Terms, rules, variances | asked at C1 | in block, or in app pack after first answer |
| Data | asked at C2 | discovered by me; block gives hints |
| Risk / authorization | asked at C2 | in `allow` / `never` |
| Login | asked | still asked (human only) |
Target for an established app: **login only**, plus rare blockers.

## Scope values and tools (added with the parser)
- `scope: browser` = automate the browser-drivable parts and leave the rest out; `browser+manual` (default) = automate those, and write manual cases for mobile/backend/process parts; `all` = attempt everything.
- Optional extra fields: `market:` (e.g. PKBD; otherwise read from the story text: PK/PKBD -> org 010104) and `screens:` (semicolon list; otherwise taken from the analysis).
- The block is read by `python runtime/qaos_intake.py parse <run>` (writes `decisions.json`, picks the account, computes authorization, lists warnings). Answers are recorded with `qaos_intake.py answer`; reusable ones are promoted into the app pack by `python runtime/qaos_promote.py <run> [--apply]` (dry run by default). Schema: `plugins/qa-os/schemas/decisions.schema.json`.
