# S&D (DCODE) domain knowledge

What we know about how the S&D application is modelled, from the data dictionary
(`snd_tables.json`) **plus what was verified in the live DB** (`snd-schema` connector,
PostgreSQL db `ng_astrone`). Verified facts are marked ✔ with the date; everything
else is from the dictionary and may not match this database.

Use it to write test steps and choose test data. Screen names and menu paths are
**not** here yet — they come from the S&D menu table (pending) and Selenium exploration.

## The live DB (✔ 2026-09-24)

- 1,185 tables in `public`, 282 named `snd_*`. Table names are **lowercase** (dictionary is uppercase).
- Connected as `postgres` (superuser); the connector rejects writes, but a read-only user would be safer.
- **Organizations** (`glb_pr_org_organization`, 5 rows): `0101` Danone Indonesia Waters (active),
  `0102` Danone Indonesia Astron (active), `99` GLOBAL, `010104` Unilever Pakistan and `010105` Unilever Bangladesh (both inactive).
  Multi-tenant: almost every table is keyed by `porg_orgacode`, and setup tables repeat per org.
- **Only org `0101` has transactions.** Data runs to **2026-01-30** (last cash memo), so this DB is a snapshot from around January 2026.
- **Missing vs the dictionary:** `snd_tr_slm_sales_master`, `snd_pr_asp_account_sale_price`,
  `snd_pr_prs_substitution_map`. No auto-substitute policy table exists. The SDMS-10351 story ([PH], created May 2026)
  postdates this snapshot, so the feature tables are probably in a newer DB.
- Static or temp tables named `ng_*` (integration/callback staging) and `*_backup*` copies exist; ignore them.

## Entities (people and places)

| Concept | Table | How to pick the rows |
|---|---|---|
| Distributor (DT/DIST) | `snd_en_pp1_prf_bsen_phs_lvl1` | `pbet_busentity_type='DIST'` — ✔ 172 rows |
| Outlet | same table | `pbet_busentity_type='OUTL'` — ✔ 615,029 rows |
| Warehouse / customer | same table | `WHRS` 705, `WRHS` 61, `CUST` 11 |
| DSR (sales rep) | `snd_en_pp2_prf_bsen_phs_lvl2` — ✔ 2,530 rows | keyed by `epp2_busent_phs_lvl2_code` |
| Location (distributor site) | `glb_pr_loc_location` — ✔ 937 rows | `ploc_locacode` |
| Outlet subtype (= channel hierarchy) | `snd_pr_chh_chanel_hierarchy` — ✔ 229 active / 1 inactive | outlet's `pchh_chnlhier_code`; flag is `pchh_active` (`Y`/`N`) |
| Outlet ↔ DT/DSR route | `snd_en_opr_outlet_pjp_route`, `snd_en_pjp_pjphead(_daily)`, `snd_en_pjv_pjpvisit_daily` | PJP = permanent journey plan; the daily visit table has 9.1M rows |

Entity primary key: `porg_orgacode` + `pbet_busentity_type` + `epp1_busent_phs_lvl1_code`.
Always filter on entity type, because DTs and outlets share one table.

## Products and prices

- Product: `snd_pr_prd_product` (✔ 24,291 rows), key `porg_orgacode` + `porp_princode` (base/principal code) + `pprd_prodcode`.
- Product hierarchy: `snd_pr_pa1_prod_analysis_1` … `pa5` (axes / sub-axes).
- Outlet price: `snd_pr_osp_outlet_sale_price` (✔ 318,731 rows).
- Batch/stock type: `snd_pr_bth_prod_batch`, `snd_pr_stt_sku_stocktype`.
- Old **product exclusion policy** (`snd_pr_peh_prod_exd_polcy_hd` / `snd_pr_ped_prod_exd_polcy_dt`, ✔ both empty):
  header (`ppeh_code`, `ppeh_start_date`, `ppeh_end_date`, `ppeh_active`) + detail (distributor,
  `pchh_chnlhier_code`, product analysis / product). This is probably the "previous SKU exclusion list"
  that SDMS-10351's comment says to remove; the new policy is DT + outlet subtype only.

## Orders and sales: the cash memo (✔)

**A "sale/order" in S&D is a cash memo**, not the `order_req` tables (`snd_tr_orm_order_req_master` and
`snd_tr_ord_order_req_detail` exist but hold 0 rows).

- Header: `snd_tr_cmm_cashmemo_master` — ✔ 2,079,400 rows. Key: `porg_orgacode`,
  `pbet_busentity_type`, `epp1_busent_phs_lvl1_code` (the seller DT), `pdot_docmtype`, `tcmm_docno`.
- Lines: `snd_tr_cmm_cashmemo_detail` (✔ 2,254,685 rows), key adds `tcmd_srno`; product in `porp_princode` / `pprd_prodcode`,
  quantities in `tcmd_qty_1..5`, and `tcmd_previous_qty_b4_suggest` / `tcmd_previous_rate_b4_suggest`
  (values before a suggested change). **Substitution would show up as changed product codes or these "previous" columns — not yet verified.**
- The outlet is on the header in the `*_a` / `*_b` / `*_c` entity column groups
  (`epp1_busent_code_phs_lvl1_a/b/c`); which suffix is the outlet is not yet confirmed.
- Related: charges (`_cashmemo_charges`), payment (`_cashmemo_payment`), promotions (`_cashmemo_offering`, `_offritem`),
  financial breakup (`_cmf_cashmemo_finelm`), locked promos, print log, suggested-product-group (`snd_tr_cms_cashmemo_sugprdgp`).
- Dates and statuses on the header: `tcmm_docm_date`, `tcmm_schdelv_date`, `tcmm_delivery_date`,
  `pdos_docmstatus` (document status, master `snd_pr_dos_documentstatus` ✔ 530 rows), `tcmm_sub_status`, `pexs_execution_status`,
  `tcmm_stock_allocated_status`, `pvst_visit_status`, `tcmm_net_amt_bcy`, `tcmm_received_amt_bcy`.
- **Document types on cash memos** (`snd_pr_dot_documenttype`, org `0101`; ✔ counts from the header):
  `CM-01` Sales (1,170,157), `CM-09` Empty Bottles (892,911), `CM-02` Sales Return (5), `CM-07` Sales Return without reference (1),
  `AD-04` / `AD-06` DSR adjustments (8,163 each, inactive types). Others defined: `CM-04` Fresh Sales Return, `CM-06` B2B Sale,
  `CM-05` Pre Order (inactive), `CM-08/10` Customer Account Closed, `CM-11` Return without reference (ZRE2), `CM-SO` Sellout.
  Other document families: `GN-01` Goods Issue Note, `GR-01` Goods Return Note.
- Where orders come from: mobility syncs into `snd_en_ori_order_integration` (✔ 988,172 rows) and `snd_tr_ofh_order_file_header`
  (✔ 2,087,942 rows); `snd_lg_orl_order_log` (✔ 1 row) is the order log. Exact sync-to-cash-memo flow not verified.

## Stock

`snd_tr_stm_stock_master/detail` (✔ 87 rows), `snd_tr_ssb_salestock_balance` (✔ 139,651), goods notes `snd_tr_gnm_gingrn_master`
(✔ 275,778), allocated stock `snd_tr_als/ald_*`, physical stock `snd_tr_psh/psd_*`, daily snapshot `snd_tr_dss_*`.
DSR settlement: `snd_tr_rsl/rsd_dsr_route_settlem*`.

## Mobility

`mob_*` tables (setup for the mobile app: screens `mob_mb_mss_screen_setup` ✔ 13 rows, app flow, screen/event map).
Mobile orders are not created in the browser; use them via the integration tables above or mark such cases manual.

## Open questions to close before relying on this for test data

1. Which DB/environment holds the SDMS-10351 tables and the [PH] (Philippines) org? This one is Indonesia (0101/0102).
2. Outlet on the cash memo header: `_a`, `_b` or `_c` suffix?
3. How substitution is recorded on a cash memo (line product change, flag, or separate log).
4. Real column names for document status codes in `pdos_docmstatus`.
