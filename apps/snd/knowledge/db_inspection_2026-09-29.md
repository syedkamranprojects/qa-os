# snd-schema inspection (read-only, 2026-09-29)

Purpose: what the base DB can tell QA OS about roles/authorization, document lifecycles, workflow, validations and per-market configuration.

## Organizations = markets
`glb_pr_org_organization`: **0101** Danone Indonesia Waters (A), **0102** Danone Indonesia Astron (A), **010104 Unilever Pakistan Limited** (I), **010105 Unilever Bangladesh Limited** (I), **99** GLOBAL (A). Almost every table is keyed by `porg_orgacode`.
Users per org: 0101 = 1263, **010104 = 513**, 010105 = 183, none/other = 16.
**KPO_MP belongs to org 010104 (Pakistan)** with roles 0001, 0005, 0014, 0017. So cnr1dev1 / KPO_mp is a Pakistan environment (earlier note calling it "Thai/PH-flavoured" was wrong; the Karachi distributors in its grids agree). KPO_SLV and KPO_PH are **not** in this DB (no PH/TH data, as found before).

## Roles and authorization
- Tables: `smm_pr_rol_role` (69 roles), `smm_pr_sus_user` (1,975), `smm_pr_url_userroles` (5,750 user-role rows), `smm_pr_rop_roleoption` (20,159 role-option rows), `smm_pr_apo_appoption` (2,118 screens), `smm_pr_aoa_appoptionactiontype` (599 option-action rows).
- Pakistan roles: 0001 "nguser" (1,223 options), 0002 NG User Admin (365), 0003 Delivery Man (94), 0004 Warehouse (7), 0005 (843), 0006 (682), 0014 (78), 0017 (54), others small or empty; most have no description.
- **Action types are only 5**: SAVE, UPDATE, DELETE, CUSTOM, TRANSLATION. Approve/forward/submit are not modelled here (they are "CUSTOM" buttons or newer app logic).
- `smm_pr_roa_role_actiontypes` (role -> action) is **empty** and `smm_pr_doa_denyoptionactivity` is **empty**: per-role button permissions are not defined in this DB. Authorization is at **screen level** (role -> option). Data scope is by location/distributor (`smm_pr_usl_userlocation`, `ggl_gm_dat_dataauthority`), not inspected yet.

## Document types and statuses
- `snd_pr_dot_documenttype` (452 rows; 122 per Danone org, 71-85 for the Unilever orgs) and `snd_pr_dos_documentstatus` (530 rows), with `snd_pr_dcs_doc_cmpltn_status`, `snd_lg_dst_docstatus_log` (history) and `nature_identifier` codes (e.g. AT authorized, UA un-authorized, CNL cancel).
- Example GN-01 Goods Issue Note statuses (org 0101): 01 Authorized, 02 Un-Authorized, 03 Terminate.
- **Nothing for Van Sales**: no stock-requisition, van or route-settlement document type, and **no `snd_tr_str_*` tables**. The DB is older than the app build we test. The data dictionary spreadsheet does list `SND_TR_STR_STOCK_REQUISITION` and `SND_TR_STD_STOCK_REQUISTON_DTL`, so the app is ahead of this schema.
- Status codes are not a state machine: no transition table was found (allowed next-status is app logic).

## Workflow and validations
- `wkf_wf_wfs_workflow_status` (1,006 rows: 230 for org 010104): status per workflow event; `wkf_wf_wes_wrkflw_event_setp`, `wkf_wf_weo_wrkflw_event_orga`, `wkf_wf_wff_workflow_fields`. Camunda `act_*` tables also exist (BPM engine).
- `vld_vl_vdh_validation_header` (84 rows): validations attached to (org, event, document type, entity); the Pakistan sample rows are inactive and have no message text, so they do not document live business rules.

## Per-org configuration (where market differences live)
`glb_pr_orf_orga_wise_feature` (211 rows) and `glb_pr_dtf_dist_wise_feature` (33): feature flags per org. Pakistan examples: TIMEZONE Asia/Karachi (+05:00), INV_NETAMT_ROUND_OFF ROUND_UP, SALES_RETURN_MAX_DAYS_LIMIT 180, IS_APPROVA_BTN_ENABLE N (USERAPPROVAL), CM_Edit Y (cash memo edit), TAXPAYER/NTN flags. This is the mechanism behind environment/market differences.

## Verdict: what the DB fills, what it does not
| Layer | From this DB | Still needs |
|---|---|---|
| Roles/users/options | Yes: who can open which screen | Which user has the role for a step (approver vs creator) |
| Per-role actions (approve, forward) | No (tables empty; 5 action types only) | Live app + story |
| Document lifecycle | Partial: status codes per doc type | Transitions; anything newer than the schema (Van Sales) |
| Business rules/validations | Very little (inactive, no messages) | Stories + live probing |
| Market configuration | Yes: feature flags per org | Mapping flag -> screen behaviour |
| Van Sales feature | No | Live app, stories, newer data dictionary |
