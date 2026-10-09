---
name: recording-protocol
description: How to record one flow through the browser MCP for QA OS - login hand-off, helper injection, one-step-at-a-time execution, toast capture, real clicks, stop rules, trace keys and the recording file. Use whenever a flow is executed live to capture ids, messages and locators.
---

# Recording protocol (browser MCP, one flow, one data row)

A recording is a **one-time proof run**, not regression. It captures what the legacy engine needs: element ids, the order of actions, the exact messages, and the business result. The engine replays everything else, with no AI.

## 0. Before you start
1. Read the approved step sheet (`step_sheet.md` / `steps.json`) and the app pack (`apps/<app>/app.yaml`, `steps/library.yaml`, `knowledge/ui.md`). Every step comes from the sheet; **never invent a step.**
2. Check authorization in `decisions.json`: data- or stock-changing steps run only when the environment is `non_production: true` and the action is allowed by the story's `allow:`. One-way actions (approve, forward, submit, delete, authorize) need naming. Anything not authorized is skipped and marked `unverified`, not asked mid-run.
3. **One calendar day.** A cycle that creates stock, orders and a GIN must finish before midnight; the app keys stock balances by date (a run that crossed midnight failed with "No stock balance found"). If the run will span days, say so at the start.
4. Read the app pack's settings with `python runtime/qaos_config.py app <app>`; roles and users come from there, never from memory.

## 1. Login and switch points (the only routine human step)
- **Never type a user id or password.** Open the environment URL, then ask the QA member once, in one short sentence: "Log in as <user> (<role>), company <company>, distributor <code>; tell me when you're in."
- **Company and Distributor are not secrets: pick them yourself** from `apps/<app>/app.yaml` (`environments.<env>.company`, `users.<user>.distributor`). The QA member types only the user id and password and presses Login, then tells you.
- After the QA member says they are in, **verify** who is logged in (the user name shown in the header) before any step. Mismatch: stop and say so.
- A switch point is `Logout` then `Login as <role>`. Log out yourself (open the profile menu, click `li#logout`), then ask for the next login. Say what comes next in the same message.
- A login clears the injected helper and localStorage. After every login: re-inject the helper (section 2).

## 2. The helper (inject once per login)
`plugins/qa-os/runtime/qaos_helpers.js` gives `window.qaos` with `open`, `pick`, `text`, `click`, `clickCapture`, `tab`, `options`, `read`, `rows`, `headers`, `crumb`, `session`, `note`, `remember`, and the **passive watcher** (`watch`, on by default), which logs real Selenium typing and clicks, menu navigation, grid cells (with column captions), tabs, toasts, popups and alerts by itself.
- **Inject the built file, as an argument** (no pasting into the script text, no escaping): read `plugins/qa-os/runtime/qaos_helpers.min.js` (built by `python plugins/qa-os/runtime/build_helper.py`; rebuild after any change to the source) and call execute_script with
  `script: "localStorage.qaos_src = arguments[0]; eval(arguments[0]); qaos.reset(); return qaos.watch();"` and `args: ["<file text>"]`.
  Do this **before the first step** (so the menu navigation is logged). If a helper was already injected on this page earlier (a previous attempt, a precondition check, an older build), **reload the page first** (`location.reload()`, the login survives): an existing watcher keeps its old listeners and `watch()` only answers "already on". After a full page reload: `eval(localStorage.qaos_src); return qaos.watch();` (the log survives in localStorage; do NOT reset again).
- **Never hand-edit the log.** If the watcher misses something, write it to `exec/results.json` and `friction.md`; the recording stays exactly as logged.
- **Remember steps:** for `Remember <Field> as <NAME>` call `qaos.remember('#<id>' or '<label>', '<NAME>')` after the value is shown; it logs the value and becomes a fill-repository event.
- **Grid number cells** (DevExtreme): real click on the cell, then `document.activeElement.select()` via execute_script, then press the digit keys one by one, then Tab. Never send_keys (the editor re-renders and goes stale) and never type after a caret (a cell holding 0 becomes "20").
- **Long dropdown / type-ahead lists:** type the code or text into the field, then immediately click the single remaining option. Never scroll-click a long list (it picks the wrong row) and never leave the field before picking (the typed text is discarded).
- Probe `qaos.session()` before each flow. Expired session: ask for one re-login and stop.

## 3. Running steps
- **One UI step at a time.** Never run UI actions in parallel; only reads may be batched.
- **Wait for conditions, never fixed sleeps**: a header, "Data grid with N rows", a toast, a field value.
- **The tool limit is about 30 s.** For anything longer, start an async function in the page, return "started", then poll a `window.__x` result in a second call.
- **Async results.** After `qaos.pick`, `options` or `open`, read the outcome in a second call; the first call returns before the UI settles.
- **Navigate** through the sidebar search box (`qaos.open('<Screen name>')`), not by URL; URL tricks fail on some environments.
- **Toasts vanish in under a second.** Use `qaos.clickCapture(id)` for every Save / Forward / Process and record the text. Assert only messages you have observed; a message you did not see is `not observed`, never guessed.
- **Alerts** ("Are you sure you want to proceed?") are browser dialogs: **read the text first** (alert tool `get_text`), then accept (or dismiss, as the sheet says), then read the toast.
- **Capture every message the app shows, with its type** - they become the assertions of the generated flow (QA lead, 2026-10-07):
  - `toast` - success/error toast (`.dx-toast-message`), via `qaos.clickCapture`;
  - `alert` - browser dialog (text from `get_text`, the button used: accept/dismiss);
  - `popup` - an in-page modal/dialog (e.g. "Error  Un-Deliver Order exists for today delivery!", "Are you sure you want to save transaction?"): its title, message text, buttons, and a stable locator of the message element (`.modal-content` body, dx-popup content);
  - `inline` - field validation text or a red/required field (`aria-invalid`), with the field label.
  Record them in `observed.messages` as a list: `[{"type": "toast|alert|popup|inline", "text": "...", "buttons": [...], "locator": "...", "after": "<step>"}]`. Exact text, never paraphrased.
- **Real clicks vs script clicks.** Use a real Selenium click for: tabs, grid checkboxes (the header select-all too), the `#forward` dx-button, Save in the Comments popup. A scripted `.click()` on those does nothing. Scripted clicks are fine for plain buttons.
- **Typing.** Text and product type-ahead need key events (the Selenium send-keys tool, then Tab/Enter). Setting `value` in the DOM does not reach the app's model (a date typed that way was ignored). Do not use the tool's clear option: it causes stale elements; send the full text instead.
- **Comments popups** need a blur (Tab) before Save, or the app answers "Please add comments".
- **Visible only.** Ids repeat across hidden views (`saveBtn`, `Cancel`); scope to visible elements. Prefer visible text over an id when an id is duplicated.
- **Screen state traps.** Switching Header/Detail before Save discards unsaved lines; "Add" resets the form. Follow the order of the step sheet (header, then lines, then save); do not look up the app pack during execution.
- **Execution uses only the step sheet and one data row** (QA lead rule, 2026-10-08): no business pages, session logs, training hints or framework flows/ids. Discover screens, elements, ids, tabs and messages live and note them (section 5).
- **Dates.** Use today's date unless the sheet says otherwise; the framework's workbook dates are examples, not requirements.

## 4. When something goes wrong
- **One** targeted retry of a non-mutating step is fine. **Never retry a step that changes data or stock** more than once; a second failure is a finding, not a puzzle.
- Diagnose from the app itself, read-only: the page's own API calls (`performance.getEntriesByType('resource')`) and read-only GETs with the page token show why a list is empty.
- If a step is blocked, mark it `blocked` with the message and evidence, skip only the steps that depend on it, and continue the chain where the sheet allows. Report the block; do not improvise a workaround that changes data.
- Every obstacle goes to `friction.md` as: what happened, cost, fix to build. Do not turn it into a question for the QA member unless it needs a business decision.

## 5. What to record (per step)
```
{ "trace": "<group>:<seq>:<flow>:<screen>:e<event serial>",   // only when replaying a framework flow; else the step number
  "actor": "Maker", "step": "Forward Dispatch Advice DA1 with comment \"Auto\"",
  "result": "pass|fail|blocked|skipped|unverified",
  "observed": {"toast": "Forwarded successfully", "status": "Pending for approval", "document": "1350",
               "messages": [{"type": "toast", "text": "Forwarded successfully", "after": "Save"}]},
  "evidence": "element ids used, screen, grid row" }
```
- Copy each step's text **exactly** as written in the sheet into the results (the Excel record attaches results by step number and leading verb). Inject the **full** helper file, not a trimmed copy: a trimmed helper does not log the real clicks and the recording cannot become framework rows.
- Remember values (document numbers) under their sheet names (`DA1`) so later steps and the flow spec can refer to them.
- Write `exec/results.json` and the helper log (`qaos.dump()`) into the run folder as you go, so a run can resume.
- **Before every Logout (switch point), dump the action log**: call `qaos.dump()` and write it to `<run>/recording_<case>_<part>.json`. The log lives in page memory and is lost at logout and login (a recording had to be rebuilt by hand once).
- Screenshots: save only into a folder that already exists (for example the run folder's `evidence/`); create it first.
- The log is converted later (framework-generator, `framework/tools/qaos_record_multi.py`) only after the flow passed. Start the watcher before the first step, so the sidebar menu click is logged (it becomes the flow navigation). A failed or blocked step is never turned into framework rows.

## 6. Never
- Enter credentials, read the credentials file, or ask for a password in chat.
- Click "Generate Opening Balances" or any other stock-creating admin button that is not in the sheet.
- Delete or edit data you did not create in this run.
- Mark a step `pass` because nothing visibly failed. A pass needs an observed message or state.
- **Reading a status after an action (S&D change-track / approval screens):** the grid does not refresh by itself, and re-clicking the same menu item does not reload it. Go to another screen and back (or reload the page) before reading the new status; an approval read too early looks "not applied" (G66 seq 29 / 31, 2026-10-09).
- **Login hand-off timer (QA lead, 2026-10-09):** after asking the QA member to log in, the main session starts a 20 s timer; when it fires it checks the page: credentials typed -> press Login; already logged in -> continue; fields empty -> ask again and wait. Claude never types credentials.
