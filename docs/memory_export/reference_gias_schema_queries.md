---
name: reference-gias-schema-queries
description: "How to look up GIAS applications/systems directly from the Oracle DB via mcp__gias-schema__run_readonly_query, plus the confirmed results"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 15874ffb-524e-452e-ab42-ab7c543b7919
  modified: 2026-08-19T05:05:42.001Z
---

The `mcp__gias-schema__run_readonly_query` MCP tool runs read-only SELECTs
against the live GIAS Oracle DB (SELECT-only, write/DDL keywords rejected,
results capped at max_rows). Use it to verify dropdown codes (application,
system, department, etc.) instead of guessing from the UI or stale config.

**Query used to list applications for a given system:**
```sql
SELECT * FROM SH_SM_AA_APPLICATION ssaa WHERE ssaa.SSS_SYSTEMCODE IN('01','02') ORDER BY 1;
```

**Query used to list all systems:**
```sql
SELECT * FROM SH_SM_SS_SYSTEM ssss;
```

**Results as of 2026-08-19:**
- Systems: only `02` = "General Insurance" is active (`SST_STATUSCODE='Y'`).
  System `01`="ERP" and systems `03`, `25`, `26`, `27` (General
  Module/test/TESTING/TEST) are all inactive (`'N'`).
- Applications under systems 01/02: `01`=Parameter, `05`=Human Resource,
  `06`=Payroll, `88`=General Insurance (system 02, the active one),
  `92`=Payroll Management System, `94`=Human Resource Management System.
  There is no app code `13`.

This confirmed `GIAS_DEFAULT_APPLICATION` should be `"88"`, not `"13"` -
see [[project_gias_element_cache]] for the fix applied to
`.claude/settings.json`.
