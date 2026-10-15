---
name: case-format
description: The QA OS standard for test cases - fields, ids, kinds, the 10-core-case cap and backlog, coverage heuristics, traceability and the team workbook. Use when designing, reviewing or approving test cases.
---

# Test case standard

Contract: `plugins/qa-os/schemas/cases.schema.json` (`cases.json`). The team workbook is rendered from it by `python runtime/qaos_workbook.py <run>`; the workbook is layout only. Global limits live in `qaos.yaml` (`limits`).

## Fields (every case)
| Field | Rule |
|---|---|
| `id` | `TC01`.. (`^TC\d{2,3}$`), unique in the run |
| `title` | starts with **Verify**; negative/alternate cases show as `ALT-` in the workbook |
| `kind` | `positive`, `negative`, `boundary`, `regression`, `business-effect` |
| `traces` | at least one requirement item id (`R*`, `AC*`, `SC*`, `AMB*`) |
| `preconditions` | what must already be true (roles, documents, stock), in plain words |
| `data_needs` | what **one** data row must satisfy; never bulk variations |
| `expected` | judgeable: exact message text when known, exact status or amount |
| `beyond_story` | `true` when the case tests behaviour the story does not state; listed in the Notes sheet for the BA |
| `priority` | `P1`, `P2`, `P3` |

## The cap
- **No fixed cap on core cases** (design v4, 2026-10-15): as many as the rules and ACs need; the QA member trims at approval. The `Backlog` section holds **one-line ideas only** (title + why), promoted to core only by the QA member.
- Every core case belongs to exactly one path (`paths.json`); negatives on the same screens are data rows of that path.

## Coverage heuristics
1. **Positive** for every "When" item and screen action (open, list, create, update, approve, download, upload).
2. **Negative**, one per validation: mandatory blank, invalid or non-existent code, inactive code, value of another distributor, altered pre-filled value, duplicates, wrong file format.
3. **Boundary**: inclusive dates, same-day vs next-day, min/max length from the screen's knowledge.
4. **State rules**: future, current, expired records.
5. **Business effect** per acceptance criterion, from every entry point it names, including the negative side.
6. **Regression** for each scope change found in story comments.
7. **Maker/checker**: any document with approval gets a case covering create by a maker and approval by a different user.

## Rules
- Base cases on the story and the app pack, not on example workbooks.
- Use the app's own names (screen, field, status); note story-vs-app differences as known variances (`decisions.json`), not as failing cases.
- A case that changes data or stock says on which environments it may run (`non_production` only).
- Steps are written later in plain English with event columns and approved together with the cases (one approval); a case never contains locators or waits.
