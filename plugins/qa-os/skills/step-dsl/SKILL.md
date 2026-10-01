---
name: step-dsl
description: How to write QA OS executable test steps (step DSL v1) and run them with the deterministic player. Use when authoring, reviewing or running steps.json flows for any app pack.
---

# QA OS step DSL v1

The contract is `plugins/qa-os/schemas/steps.schema.json`. One file = one test case = **one data row**
(`data`). Bulk rows are only for the legacy engine's case-data workbooks.

```json
{ "case": "TC05", "title": "…", "app": "snd", "env": "cnr2dev3", "user": "KPO_ph",
  "data": { "distributor": "15181887", "policy": "PL000000051" },
  "steps": [ { "do": "login", "distributor": "{{data.distributor}}" },
             { "do": "navigate", "menu": "Transaction > SKU Substitution Policy" },
             { "do": "select_row", "grid": "SKU Substitution Policy", "value": "{{data.policy}}" },
             { "do": "verify_ui", "expect": { "field": "End Date", "state": "editable" } },
             { "do": "logout" } ] }
```

| Verb | Required keys | Notes |
|---|---|---|
| `login` / `logout` | — / — | App-pack recipe; credentials from env only |
| `harvest_menu`, `harvest_i18n` | — | Save the role-filtered menu / label text into the app pack |
| `navigate` | `menu` | Path as shown in the menu, `A > B` |
| `enter`, `choose`, `set_date` | `field`, `value` | Field = on-screen label from `screens/<option_id>.json` |
| `click` | `button` | Button label |
| `select_row` | `grid`, `value` | Row whose first cell equals `value` |
| `verify_ui` | `expect` | One of: `url_contains`, `breadcrumb`, `grid`+`columns`, `fields_present`, `field`+`state`/`value`, `button`+`state`, `message_contains` |
| `capture` | `field`, `as` | Stores a value as `{{captured.<as>}}` |
| `download` | `button`, `as` | Click the button; the file lands in the run's `files/` folder under `as` |
| `edit_excel` | `file`, `rows` | Replaces the data rows of a downloaded workbook: `rows` = list of `{column: value}`; `[]` clears them |
| `upload` | `button`, `file` | Sets the page's file input (`input[type=file]`) to a file in `files/` |
| `harvest_grid` | `as` | Saves all rows of the visible DevExtreme grid (following the pager) to `data/<as>.json`; read-only |
| `capture_message` | `as` | Saves the visible toast/alert text as `{{captured.<as>}}` and `messages/<as>.txt` |
| `screenshot`, `wait` | —, `seconds` | |

`verify_ui` also accepts `{ "excel": "<file>", "columns": [...] | "cells": {...} | "has_rows_for": "<text>" }` for downloaded files,
and `{ "message_kind": "success" | "error" }`. The latter is the learn-first assertion: any success or error message satisfies it,
and the exact text is recorded in `messages/` for QA to tighten into `message_contains` later.

**Placeholders:** `{{data.x}}`, `{{captured.x}}`, `{{today}}`, `{{today+N}}`, `{{today-N}}` (formatted with the app's date format).

## Rules
- Use on-screen **labels**, never raw ids. If a label isn't in the app pack, ask app-cartographer to learn the screen first.
- Every case logs out at the end. Every case starts with a fresh login; don't chain cases.
- Don't write steps that confirm Save/Update/Delete/Upload in *learning* flows. In test flows, those
  steps are the point of the test, and they run only against the dev/QA env in `app.yaml`.

## Running
- `python runtime/qaos_player.py <flow.json> --dry-run` validates the flow and resolves every menu, field and button, without a browser.
- `python runtime/qaos_player.py <flow.json>` runs it headed and writes `runs/<case>/<timestamp>/result.json`, `log.txt` and screenshots.
- Claude must not run a flow containing `login` itself, because that would be Claude entering a password. Ask the user to run it, then read `result.json`.

## Business steps (readable layer above the DSL)
Test cases are written in the **standard step vocabulary** (`docs/STEP_VOCABULARY.md`): `[Actor] Verb Object ...` with roles (Maker, Checker), lifecycle verbs (Create, Add line, Forward, Approve/Authorize, Reject, Save) and checks (Verify message / status / field). Each term is defined once in `apps/<app>/steps/library.yaml` (`expands_to` = the primitives in the table above, plus `notes` with the gotchas learned live, and `verified`). When writing steps: use only vocabulary terms; if a needed term is missing, write `Do: <sentence>` (manual) and offer to add it to the library. Every user change is a **switch point**: `Logout`, then `Login as <role>`, and Claude verifies the logged-in user name before continuing.
