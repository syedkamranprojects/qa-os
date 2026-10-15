# Screen files (`<option_id>.json`)

One machine-readable file per trained S&D screen (design v4 decisions 0.2, 0.3, 3.1-3.3). The step author binds plain-English
steps to element ids from it; the recorder and the player use it during execution. Contract:
`plugins/qa-os/schemas/screen.schema.json`. The list of files, with each file's status and gaps, is `_index.json`.

| Part | What it holds |
|---|---|
| `menu`, `route`, `layout_code`, `kind` | Sidebar path, option id (= `li#<option_id>`), search text, top group; dynamic (layout) or static screen |
| `tabs`, `panels` | Tabs with the live tab id and sub-tabs; config panels (page, table, grids) |
| `fields` | By on-screen label: `element` (live DOM id), `locator` (only when seen live), `widget`, `required`, `data_field`, `list_source`, `max_length`, `disable_rule`, `provenance` (db / observed / recorded / stated + env, date, ref) |
| `buttons`, `grids` | By label / caption: element ids, wrapper ids, grid row-id pattern (`row_N_<field>`), editable cells, row buttons, filters |
| `messages` | Toasts, confirms and inline messages seen, with when they appear |
| `lessons` | Screen-level lessons (ids, control behaviour), saved automatically; business rules are not here |
| `differences` | Config vs live (live wins), per env, with a status (`open`, `reported`, `accepted`, `defect`, `closed`) |
| `business_page`, `trained` | The business page of the screen; trained flag, date and how (business page, group 11/66 walk, run, live look) |

A field without `locator` is known only from the config tables: its `element` is the expected id, not yet seen live.

## Build and refresh
```
python apps/snd/tools/build_screen_file.py "Distributor Profile HQ"        # one screen (title or option id)
python apps/snd/tools/build_screen_file.py --all-trained                   # every trained screen + _index.json
python apps/snd/tools/build_screen_file.py --all-trained --env cnr1dev1    # live sources of one environment only
python apps/snd/tools/test_build_screen_file.py                            # test (builds Distributor Profile HQ in memory)
```
The builder merges `knowledge/screens_db` (config), `knowledge/screens_observed` (sweep and live harvests), run recordings under
`runs/` and `tools/screen_lessons_backfill.json`. It reads files only, is deterministic, and never drops what is already in a
screen file: lessons, messages, difference statuses and hand-written field facts (e.g. `disable_rule`, `options_seen`, `note`) are
kept. Add a new lesson straight into `lessons[]`; set a difference's `status` by hand once it is reported or accepted.
