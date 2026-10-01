# Using QA OS: a guide for QA team members

You give Claude a story; Claude proposes test cases in plain steps, runs each flow once in the browser while you log in, and produces the scripts and data for the legacy framework. You review; you never write code.

## What you do, in order
| # | You | Claude |
|---|---|---|
| 1 | Paste the story (or the Jira key). If you can, add the short **QA-OS block** at the end (environment, user, scope, terms, what may be changed; see `docs/QUESTION_BANK.md`) | Reads the block, picks the account that can reach all the screens, and writes `decisions.json` |
| 2 | Answer at most a few questions in one message (scope, unclear wording) | Lists ambiguities with a default for each; the BA's questions go into one note |
| 3 | Review the **test cases**: up to 10 core cases, written in the standard step vocabulary (`docs/STEP_VOCABULARY.md`) | Writes cases and steps; the rest goes to a backlog |
| 4 | **Log in** when asked, and again at each *switch point* (`Logout` then `Login as <role>`) | Opens the browser, checks who is logged in, runs the steps one at a time, records messages and ids |
| 5 | Review the results and the **differences between the story and the app** | Writes the findings, the BA note, and the friction list |
| 6 | Hand the reviewed SQL and workbook to the framework owner | Generates `framework.sql`, rollback, the case-data workbook and a review note; **never applies anything** |

## Commands (type these in Claude Code)
| Command | Use |
|---|---|
| `/qa-os:run <KEY>` | The whole cycle for a story |
| `/qa-os:cases <KEY>` | Only analysis and test cases |
| `/qa-os:steps <KEY>` | Only the steps for existing cases |
| `/qa-os:status [KEY]` | Where a story stands |
| `/qa-os:learn <app> [screen]` | Learn a screen or menu of the application |
Anything else can be asked in plain words: "run the Dispatch Advice flow", "approve the DA with the other user", "add the step *Verify stock* to the library".

## Step language in one minute
Every step is `[Actor] Verb Object ...`: `[Maker] Create Dispatch Advice with Warehouse = "Auto Main Warehouse"`, `[Checker] Approve Dispatch Advice DA1`, `[Maker] Logout`. Actors are **roles** (Maker, Checker ...), not user names. Full list of terms: `docs/STEP_VOCABULARY.md`; what each term runs: `apps/<app>/steps/library.yaml`.

## Rules to remember
- **You log in; Claude never types passwords.** Passwords must not be pasted into the chat; if one was, change it.
- Steps that change data run only on environments marked non-production; steps that cannot be undone (forward, approve, delete, submit) run only when the story's QA-OS block allows them or you say so.
- Maker and checker are different users. Claude stops at every switch point and waits for you.
- Claude asks last: only what the knowledge base, the live application and the story cannot answer.

## Where to look
| What | Where |
|---|---|
| Test cases (Excel), steps, results | `qa-os/runs/<KEY>/<timestamp>/` |
| SQL, rollback, case-data workbook, review note | `.../framework/` |
| Story vs application differences | `.../BA_NOTE.md` |
| What blocked or slowed the run | `.../friction.md` |
| What the project already knows about an application | `qa-os/apps/<app>/knowledge/` (screens, access, decisions, framework flows) |
| The design and current status | `qa-os/docs/ARCHITECTURE.md`, `qa-os/docs/STATUS.md` |
