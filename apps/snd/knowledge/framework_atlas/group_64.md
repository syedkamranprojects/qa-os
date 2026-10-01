# Group 64 - GIS group

Source `gtf:64`. Market guess (from name): None. Rows: 3 (active 2, inactive 1). User switch points: 1 (2).

Allowed apps (alg): app 3 GIS CLASSIC -> D:/Selenium/Automation/GIS_QA// (workbook variant inferred: None)
Starts with an app login flow: False (first active flow 02090001).

Login rule (engine): a row with login status not empty and not `N` logs out and in again as that row's user; empty or `N` continues in the same session.

## The cycle, step by step (active rows)
1. **seq 2 - Client Insurance Setup** (`02090001`) - area: Master/Setup
   - **SWITCH USER POINT**: log out and log in as **Sm.Shoaib** (serial 5)
   - consumes: `REPO_ClientCode` produced within same flow; `REPO_AgentCode` produced within same flow
   - produces: `REPO_AgentCode`, `REPO_ClientCode`
   - checks: none configured
   - screens: USER LOGIN -> Login_Selection_Client -> Application_Setup_Screen -> Menu_Setup_Screen_Client -> Client_Setup -> Client_Agent_Address ...
   - detail: flows/02090001.md ; trace prefix `64:2:02090001`
2. **seq 3 - Analaysis 4** (`00460001`) - area: Master/Setup
   - actor: same session (Sm.Shoaib)
   - consumes: `REPO_GINNO` unresolved in group
   - checks: 0 message/field assertion(s); group assertion sheet(s): `GIN_APPROVAL_REJECT_ASSR`
   - screens: Good Issue N Reject Appro Promo
   - detail: flows/00460001.md ; trace prefix `64:3:00460001`

## Inactive rows (skipped by the engine)
- seq 1 USER LOGIN (`02080001`) status N
