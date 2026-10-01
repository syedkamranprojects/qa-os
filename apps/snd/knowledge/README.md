# S&D (DCODE) table catalog

Machine-readable version of the S&D data dictionary, used by the end-to-end test
automation to find test data, verify outcomes in the DB, and map screen captions
to columns.

**Source of truth:** `DD-S&D Entity Model - Data Dictionary 24 June 2026.xlsx`
(everything else here is generated from it). When a newer dictionary arrives,
drop it in this folder, remove the old one, and re-run `python ../tools/dd_build.py`.

| File | What it is |
|---|---|
| `snd_tables.json` | 548 tables / 10,808 columns: module, description, PK, and per column type, PK/FK and referenced table. Large (~2 MB) — query it with `dd_lookup.py` rather than reading it whole |
| `snd_tables_index.md` | Module → table → description, one line per table. Good for skimming or grep |
| `snd_screen_field_map.json` | Screen caption → `table.column` for the Distributor, Outlet, DSR and Product profile screens |
| `dd_quality_report.md` | Inconsistencies in the source workbook (see below) |
| `../tools/dd_build.py` | Regenerates all of the above |
| `../tools/dd_lookup.py` | Search helper (usage below) |

## Lookup

```
python ../tools/dd_lookup.py substitution                      # tables/columns matching a keyword (regex)
python ../tools/dd_lookup.py -t SND_PR_PRS_SUBSTITUTION_MAP    # all columns of one table
python ../tools/dd_lookup.py -r SND_PR_CHH_CHANEL_HIERARCHY    # who references this table (FKs)
python ../tools/dd_lookup.py -s "Outlet Code"                  # screen caption -> column
```

## Things to know about the S&D model

- **One table, many entity types.** Distributors *and* outlets both live in
  `SND_EN_PP1_PRF_BSEN_PHS_LVL1` (DSRs in `..._LVL2`), told apart by
  `PBET_BUSENTITY_TYPE`. Always filter on it.
- **Composite keys start with `PORG_ORGACODE`** (organization) and usually
  `PBET_BUSENTITY_TYPE` + the entity code. Transactions add document type +
  document number.
- **Outlet subtype = channel hierarchy**: `SND_PR_CHH_CHANEL_HIERARCHY`, linked from
  the outlet row via `PP1.PCHH_CHNLHIER_CODE`.
- Setup tables follow `<code>_DESC / _ABRV / _DEFAULT / _ACTIVE`; `_ACTIVE` is the
  flag to use when a story says "must exist and be active".
- Multi-language copies of setup tables end in `_M`.

## Source workbook quirks (handled by the parser)

- On continuation rows the **Table Name cell is often copy-pasted and wrong** (~1,100
  rows). The parser assigns columns to the table whose **serial number** started the
  block, and checks that the column prefixes agree.
- 68 tables have column definitions but aren't in the grouping sheet; 8 are in the
  grouping sheet with no columns. Both lists are in `dd_quality_report.md`.
- `DD-S&D-EN-Transactions VER 1` is an older copy of `DD-EN-Transactions VER 12`; VER 12
  wins, and VER 1 only contributes 6 tables missing from VER 12.
- **The dictionary is not complete for recent features** — e.g. the SDMS-10351
  auto-substitute exclusion policy (DT + outlet subtype) has no table here; only
  `SND_PR_PRS_SUBSTITUTION_MAP` (product → substitute, with dates) exists. Anything
  the dictionary lacks must be discovered from the live DB schema.
