---
name: step-authoring
description: The assisted step-authoring dialogue - Claude drafts what it can, then asks the QA member for the next step one at a time with suggested options plus free text, rephrases the answer into the predefined wording, checks the labels against the real screen, and asks for confirmation. Use in the main session whenever test steps are being written or completed with a QA member (gate G3).
---

# Assisted step authoring (the "next step" dialogue)

Assisted mode is the default (`qaos.yaml` -> `authoring.mode`). The QA member supplies the application knowledge Claude lacks; Claude supplies the discipline: predefined words, exact screen labels, checks and records. **This skill runs in the main session** (only the main session can ask the user); subagents never ask the QA member anything.

Tools (deterministic): `python runtime/qaos_steps.py` - `check`, `labels`, `suggest`, `add`, `undo`, `render`, `lint`. Vocabulary: `vocabulary/core.yaml` (cheat sheet: `docs/QA_STEP_CHEAT_SHEET.md`). Draft file per case: `<run>/step_draft_<TCnn>.json`.

## The loop (one step per turn)
1. **Start.** State the case in one line (title, expected result, roles). Pre-fill what is already known and safe, as **suggestions**, not as accepted steps: from the atlas flow (`build_atlas.py --find`, `flows/<id>.md`), the app pack, and earlier approved sheets for the same screen. Nothing is added to the draft until the QA member accepts it.
2. **Show the draft so far** (`qaos_steps.py render <draft>`), compact.
3. **Ask for the next step** with the question tool (`AskUserQuestion`), one call per step:
   - **Question "Next step"**: 2 to 4 options. Options are concrete, canonical steps with real values, taken from `suggest` and the case data (for example `Navigate to Dispatch Advice`, `Create Dispatch Advice with Warehouse = Auto Main Warehouse`), plus **"The flow is complete"** when the case's expected result is already covered. The tool's built-in "Other" is where the QA member types free English.
   - Keep option labels short; put the full canonical step in the description.
4. **Handle the answer.**
   - **A suggested option was picked** -> it is already canonical. Run `add` (which runs `check`) and continue; no confirmation needed.
   - **Free text (Other)** -> rephrase it into exactly one predefined form (see rules below), run `check` on your rewrite, then **ask for confirmation** in the next call together with the next-step question (two questions in one `AskUserQuestion`):
     - "I understood: `<canonical step>`. Correct?" - options "Yes, add it" / "No, I will rephrase".
     - "Next step" as above.
     If the confirmation is "No", ignore the second answer and ask again with what they said.
   - **`check` fails** -> do not add. Explain in one line and offer the fix as options: the closest real labels (`did you mean Warehouse?`), the closest verb forms, or "Do: <sentence> (manual)". Never invent a label to make a step pass.
   - **The QA member is unsure** -> offer "Show me what is on this screen": run `labels "<Screen>"` and list fields, buttons and tabs so they can choose. If the screen has no knowledge yet, say so and offer to look it up live (recorder or `app-cartographer`), not to guess.
5. **After an action that needs a check** (`Create`, `Add line`, `Save`, `Forward`, `Approve`, `Reject`, `Click <Button>`): ask "What should the screen show?" with options: the message text if known from the atlas/app pack, "Record the message when it first appears" (`Verify message (text to be recorded)`), a status check (`Verify status of <Document> is <status>`). Add the answer as a Verify step.
6. **Switch points.** When the actor changes, add `Logout` then `Login as <Role>` automatically and say so.
7. **Repeat** until "The flow is complete", then `lint <draft>`: fix problems first, mention warnings once.
8. **Finish the case:** show the final table (`render`), list anything `unverified` (labels with no screen knowledge) and the risk column, and ask for **approval** of the step sheet (gate G3, phrases in `qaos.yaml`). Anything else is feedback: change the draft and ask again.

## Rephrasing rules (free English -> predefined wording)
- One sentence from the QA member may be several steps: split it, and confirm them together as a numbered list.
- Use the verb's **canonical form** exactly, with the screen's own labels. Map their words with the vocabulary's `says` lists: "put/type/fill" = `Enter`, "select/pick" in a dropdown = `Choose`, "send for approval/submit" = `Forward`, "tick all" = `Select all rows`, "press Process" = `Click Process`.
- Prefer lifecycle verbs (`Forward`, `Approve`, `Save`) over `Click <Button>`. Use `Click <Button>` only for real screen actions (Process, Unallocate, Save All) and only with a button that exists on the screen.
- Values: keep the QA member's values exactly. Never fill in a value they did not give; if a value is missing ask for it, or write a placeholder `<date>` / `{{data.x}}` only when the vocabulary or case data defines it.
- Approval is always by a different user: if they write "approve" under the maker's role, ask which role approves.
- A step that does not fit any verb is written `Do: <their sentence>`; it is manual and is listed for a person to add to the library.

## What to record for learning
- Keep the QA member's original wording with each step (`add ... --raw "<their text>"`). After the case, list new phrasings that mapped cleanly and any labels or steps that were missing; these are **candidates** for the vocabulary's `says` lists and the app's `steps/library.yaml`, promoted only after the QA lead confirms (dry run first, like `qaos_promote.py`).
- Any correction the QA member made to a suggested step is a finding: note it in the run's `friction.md` as "suggestion wrong: <what>, right: <what>".

## Keep the dialogue cheap for the QA member
- One question call per step. No long explanations, no restating the whole sheet each time (show it only every 5 steps or on request).
- Never ask what the tools or app pack can answer (labels, roles, screen names, next-step options).
- Never ask for credentials. Logins happen at switch points and are the QA member's own action.
- If the QA member gives many steps at once, accept the list, run `check` on each, and only ask about the ones that fail.

## Lessons from the pilot (2026-09-30, TC01 Dispatch Advice)
- **Name what the person must do, not "next step".** After the actor changes, ask "What does the Checker do?" and describe the screen state in the question. Never offer a change of role as an option once the switch point (Logout, Login as <Role>) has been added.
- **Say what you added automatically** (for example the switch point) in one plain sentence before the next question.
- **Suggest what the framework flow does, not what you remember.** For each Create/Add step, read the atlas flow page (`flows/<id>.md`) and offer its lines and fields (Product, Stock Type, Batch, CS ...) as options. Take example values from the atlas workbook sample and label them "example value"; never from memory of an earlier run.
- **Unusual order is a warning, not a veto.** If the QA member's order is unusual (a Forward before any line), say so once, offer the usual order, and respect their choice.
- **Natural captions:** if `check` rejects a caption the QA member is clearly using ("Document No"), offer to add an alias to `apps/<app>/knowledge/label_aliases.json` (after the QA lead confirms) instead of asking them to use the internal label.

## The Excel is the source of truth (round trip)
The QA member may finish or change the steps in the **Test Cases** sheet (column *Test Steps*) instead of in chat. Whatever is in the Excel when they say the steps are final is what gets executed.
1. **Export:** `python runtime/qaos_export.py <run> --out <run>/<KEY>_TestCases_Steps_vN.xlsx` (a new version name each time; the old file may be open in Excel and locked).
2. **The QA member edits** the Test Steps cells: one line per step, `<n>. [<Actor>] <step in the standard wording>`, and saves. They tell you the steps are final.
3. **Import (dry run first):** `python runtime/qaos_import.py <xlsx> --run <run>`. It checks every line with `qaos_steps.py check` and lists problems with the closest correction (`PROBLEM`), softer unverified items (`CHECK`) and what changed since the current draft (`CHANGED`). Show these to the QA member in chat, briefly; fix wording with them (this dialogue) or let them fix the Excel.
4. **Apply:** when there are no problems, ask the QA member to confirm the steps are final, then `... --apply --approved-by "<who>"` (the old draft goes to `history/`). If the step count changed the framework mapping is marked stale and must be regenerated.
5. **Execute from the applied draft:** the recorder runs `step_draft_<TC>.json`, which is now exactly the Excel. Never execute from an Excel that was not imported and checked. If the QA member edits the Excel again, repeat from step 3.
