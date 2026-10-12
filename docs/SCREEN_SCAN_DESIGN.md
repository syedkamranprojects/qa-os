# Screen scan: checking the predicted steps before execution - design note (DRAFT, 2026-10-12)

Status: **draft for the QA lead's review**. It extends `FINAL_DESIGN.md` (v3) with one new stage between "steps" and "execute". It does not change the principles there.

## 1. Purpose
Claude writes the test cases and steps from its trained knowledge. That is a **prediction**. The AI execution exists to **confirm the prediction is right** (QA lead, 2026-10-12).

Today the first contact with the real screen is the execution. A wrong prediction then costs a whole run and a stop:

| Run | Found only at execution |
|---|---|
| DSR Profile quick test (10-09) | Address has sub-tabs (Company / Business / Residence); Forward needs a **Residence** address |
| SDMS-6084 (10-09) | **Report To \*** is mandatory and empty on the distributor, so every Update case was blocked |
| SDMS-6084 (10-09) | Off Days is a multi-select on cnr1dev1; the database still describes a text box |
| DSR / Distributor Profile | menu item ids differ per screen (Address = `Opr-1` on DSR, `addr-1` on Distributor Profile) |

A **read-only screen scan** after the steps are written, and before they run, catches this kind of mismatch at design time. Each one becomes a single question instead of a failed run.

## 2. The rule that keeps the prediction honest
- The steps are written **from knowledge only** (unchanged; principle 2 of FINAL_DESIGN). The scan happens **after** the steps exist.
- The scan **checks and binds**; it **never rewrites** a step. Every mismatch is a **finding**. The QA member decides whether the step is corrected, the knowledge is corrected, or the finding is accepted.
- The original prediction is kept. The run records what the scan corrected and what the execution corrected, so the **accuracy of the training** can be measured and every miss goes back into the knowledge.

## 3. Place in the life cycle

```
Request / story
  -> 1 Analyse                    (knowledge)
  -> 2 Cases                      (knowledge)            gate G2
  -> 3 Steps = the prediction     (knowledge)
  -> 4 SCAN (new)                 read-only, same session after the login
  -> 5 Findings to the QA member  one round; steps / knowledge corrected   gate G3 (steps approved after the scan)
  -> 6 Execute once per path      dynamic check: messages, results, ids that exist only after actions
  -> 7 Scripts                    from the recording (unchanged)
```

- **Login:** the QA member logs in once (Claude types the user ID, the QA member the password). The scan uses that same browser session; there is no headless browser (agreed 2026-10-12). For a Maker/Checker flow, each role's screens are scanned right after that role's login.
- **Agent:** `app-cartographer` in *scan mode*, the only stage besides the recorder that opens the browser. It receives the step sheet, the screen list and the run context, nothing else.

## 4. What the scan may and may not do
| Allowed (read-only) | Never |
|---|---|
| Open the screen through the menu (the same navigation as the steps) | Save, Update, Forward, Approve, Delete, Process, Add + Save, or any button that writes |
| Click tabs, sub-tabs and menu items (Demographics / Address ...) | Type into form fields |
| Open a drop-down or tag box, read its options, close it with Escape | Accept an alert or confirm dialog |
| Show the filter row, filter an **existing** record and select it, so that tabs which need a record become enabled | Create, change or delete any record |
| Read labels, ids, widget types, mandatory marks, read-only state, masks, grid columns, button ids and enabled state | Use the database to replace what the live screen shows |

Leaving the screen discards anything the scan touched; nothing is ever saved.

## 5. Output 1: the screen model (kept in the app pack)
One file per screen layout: `apps/<app>/knowledge/screens/<layoutCode>.json`. It is shared with the team and reused by later runs. The example below is illustrative; the pilot will produce the real one.

```json
{
  "layout": "DT1002", "screen": "DSR Profile - DT", "menu": "#DYL_DT1002",
  "scanned": {"date": "2026-10-12", "env": "cnr1dev1", "market": "PK", "user": "Auto_Multi_Orga"},
  "tabs": [
    {"text": "Demographics", "id": "Dem-1", "via": "menu", "menu_toggle": "btn_1"},
    {"text": "Address", "id": "Opr-1", "via": "menu", "menu_toggle": "btn_1",
     "subtabs": [{"text": "Company", "id": "tab_group_0"}, {"text": "Business", "id": "tab_group_1"}, {"text": "Residence", "id": "tab_group_2"}]},
    {"text": "Documents", "id": "tab_4", "via": "tab"}
  ],
  "fields": [
    {"tab": "Address/Residence", "label": "Cell Phone 1", "id": "txt__eadr_phone1", "widget": "text", "mask": true, "mandatory": true, "readonly": false}
  ],
  "grids": [{"id": "dataGrid", "columns": [{"label": "DSR Code", "filter_id": "rowfilter_TXT__epp2_busent_phs_lvl2_code", "row_id": "row_1_dsr_code"}]}],
  "buttons": [{"text": "Save", "id": "save", "enabled": true}, {"text": "Forward", "id": "forward", "enabled": true}],
  "options": {"DDL__epp1_offdays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
  "record_state": {"record": "AUTO091013", "empty_mandatory": ["Report To"]}
}
```

- **Menu / tab ids per screen** come from here. This answers the "menu choice without a standard tab id" question without hard-coding a text-to-id table: "Address" maps to the id this screen actually has.
- `record_state` describes the record the scan opened (for example "Report To \* empty"). It belongs to the run, not to the shared model.
- **Staleness:** a model is reused only for the same environment and market, and only while it is younger than `scan.max_age_days` (default 14). An app release, or any execution difference, triggers a re-scan. The app's layout metadata in its database may be shown as a first guess, marked `db`; **the live scan always wins**, as the Off Days case showed.

## 6. Output 2: the step check (per run)
`<run>/scan_findings.json`, also shown as a short table. Each finding names the step, what was predicted, what was observed and a suggestion.

| Kind | Example | Blocks? |
|---|---|---|
| `missing_element` | step names a field or button the screen does not have | yes |
| `type_mismatch` | step says "Enter Off Days" (text); the screen has a multi-select | yes |
| `subtab_not_chosen` | step says "Address"; the screen has Company / Business / Residence | yes |
| `option_not_offered` | step picks a value the drop-down does not list | yes |
| `readonly_target` | step types into a read-only field | yes |
| `mandatory_not_covered` | a mandatory field on the step's screen is not filled by any step | yes |
| `precondition` | the chosen record has an empty mandatory field (Report To) | yes |
| `ambiguous_label` | two controls share a caption (the second "Off Days", SDMS-6244) | warn |
| `extra_on_screen` | a tab, button or option the steps never mention | info |

Every finding is answered once, in one round, with one of:
- **fix step:** the step is corrected; the step sheet shows the change;
- **fix knowledge:** the business page was wrong; it is corrected with knowledge-intake method B;
- **accept:** for example, the case expects that refusal.

Only then is G3 approved.

## 7. Binding and the prediction ledger
- **Binding:** after G3, each step gets the element id from the screen model, in a separate `bind` block. The step's wording does not change. The executor uses the id and still observes, so an id that differs at execution is a finding, not a silent fix.
- **Ledger:** `<run>/prediction_ledger.json`, one line per step:
  - `predicted`: the step as first written;
  - `after_scan`: the change, if any, and the finding that caused it;
  - `after_execution`: the change, if any, and why;
  - `cause`: one of `knowledge-gap`, `data`, `app-changed`, `defect`, `wording`.
- **Accuracy** = steps right first time / all steps. It is printed in the test report, and per business area over time, so the QA lead sees where training is still needed.

## 8. What execution still has to prove
These exist only after an action. The scan can predict them from patterns but cannot confirm them:
- toasts, popups and alerts;
- generated document numbers;
- the row that appears after filtering;
- buttons that appear only after Save;
- the business result (status, stock, amounts).

## 9. Changes this needs (implementation plan, after sign-off)
| Part | Change |
|---|---|
| `app-cartographer` agent | new *scan mode*: inputs = step sheet + screens + run context; outputs = screen model + `scan_findings.json`; read-only rules of §4 |
| `qaos_helpers.js` | a read-only `qaos.scan()` that returns the screen model of the open page, reusing the A18/A20 detection (tab and menu ids, wrappers, masks, row-filter ids) |
| `runtime/qaos_scan.py` (new) | compares steps with the model and writes the findings; keeps the ledger |
| `qa-orchestrator`, `quick-script` skills | add stage 4/5; G3 after the findings |
| `step-author` | adds `bind` blocks after G3; never rewrites wording |
| `recorder` | uses the bound ids; reports any id that differs as a finding |
| test report | prediction accuracy line |
| `docs/OPERATING_RULES.md`, `FINAL_DESIGN.md` | link to this note once approved |

**Pilot:** DSR Profile – DT, with steps predicted from knowledge and one login. Then scan, findings, the A20 live check in the same session, and compare with what the 10-09 run found at execution.

## 10. Decisions for the QA lead
1. **Quick mode:** scan before the one approval as well (proposed: yes, same rules; the findings are shown with the plan).
2. **Model age:** re-scan after 14 days, or only after a release / difference?
3. **Verifier cross-check:** the verifier also compares the generated navigation with existing framework mappings for the same screen, as a read-only warning only (proposed: no, unless you want it).
4. **Who answers findings:** the QA member running the case (proposed), or the QA lead for `fix knowledge` findings.
