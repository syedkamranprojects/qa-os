# SND access knowledge layer

Who can open which screen, per market (organization), plus per-market feature flags. Built from `snd-schema` (read-only connector) on 2026-09-29.
Used by Claude through `apps/snd/tools/access_lookup.py`; QA users never run it.

| File | Content | Source table(s) |
|---|---|---|
| `screens.json` | 2,118 screens: id, title, category, route, param, layout/admin flags | `smm_pr_apo_appoption` |
| `menu_groups.json` | 910 menu nodes (tree: id, title, level, parent, option id) | `smm_pr_opg_optiongroups` |
| `role_options.json` | role -> screen ids, for orgs 010104 (Pakistan), 010105 (Bangladesh), 99 (GLOBAL) | `smm_pr_rop_roleoption` |
| `role_names.json` | role ids and the few descriptions that exist | `smm_pr_rol_role` |
| `users.json` | 696 users of the two Unilever orgs: code, status, roles, locations. **E-mail-like codes are masked** (`user-xxxxxxxx`); no passwords, names, e-mails or phone numbers are stored | `smm_pr_sus_user`, `smm_pr_url_userroles`, `smm_pr_usl_userlocation` |
| `features.json` | per-org feature flags with descriptions | `glb_pr_orf_orga_wise_feature`, `glb_pr_frt_feature_type` |

## Questions it answers
```
python apps/snd/tools/access_lookup.py screen "Route Settlement"        # where, route, which roles/users per market
python apps/snd/tools/access_lookup.py user KPO_MP --can Route Settlement
python apps/snd/tools/access_lookup.py who "DSR Profile HQ" "PJP Creation HQ" "Route Settlement"   # which user to log in as
python apps/snd/tools/access_lookup.py features 010104 TIMEZONE
python apps/snd/tools/access_lookup.py diff-features 010104 010105      # market differences
python apps/snd/tools/access_lookup.py validate-live KPO_MP             # DB vs the live menu of that user
```

## How current is it? (validate-live KPO_MP, cnr1dev1, 2026-09-29)
DB grants KPO_MP 1,396 screens; the live menu shows 438. **365 are in both (83% of the live menu); 73 live screens are not in the DB** (newer than the schema), including the Van Sales screens (`STOCK_REQUISITION`, `CASHMEMO-STATUS-VANSALES`, `DYL_202035`). The other ~1,000 DB screens are sub-options and admin containers that never show in the menu.
Rule: **the DB tells us access for older screens; for anything not found here, the live menu (`env/<env>/menu.<user>.json`) is the truth.**

## Limits
- Access is **screen-level only**. Per-role button permissions (approve, forward) are not defined in this DB (`smm_pr_roa_role_actiontypes` and `smm_pr_doa_denyoptionactivity` are empty; option-action types are only Save/Update/Delete/Custom).
- Data scope (which distributors/warehouses a user sees) is only partly captured (user locations); `ggl_gm_dat_dataauthority` is not extracted yet.
- Only orgs 010104, 010105 and 99 are extracted (Danone orgs 0101/0102 are another client).
- KPO_SLV and KPO_PH are not in this DB.

## Refreshing
Claude re-runs the extract queries through the snd-schema connector, saves the results and runs `python apps/snd/tools/build_access.py <extract dir>` (`features.json` and `role_names.json` are re-written from the query results). Suggested cadence: when the app version changes or a story mentions an unknown screen.
Privacy: keep e-mail-like user codes masked; do not add name, e-mail, phone or password columns.
