---
name: no-docs-learn-from-metadata
description: "Never expect user guides or documented flows for apps under test; derive all app knowledge from the app DB metadata, the live app and Jira stories. Also the DB/connector decisions for S&D."
metadata:
  node_type: memory
  type: feedback
  originSessionId: eb4a66f7-6654-4151-a641-fe8df7bda0d6
  modified: 2026-09-25T06:26:01.990Z
---

For any application under test (S&D now, GIAS and others later), never expect a user guide or a documented flow. The only inputs are:
the application database (business data plus metadata: users, roles, menus, app options, screen definitions), the running app,
and Jira stories. App knowledge must be harvested from these and kept current (design §7A in `qa-os/docs/ARCHITECTURE.md`).

**Why:** the user said so explicitly on 2026-09-25, after I asked for things like a menu table and a DB user instead of deriving them.

**How to apply:**
- Before asking the user for app information, look for it in DB metadata or the live app.
- When presenting a design, always say what inputs are needed from the organisation (connectors, env URLs, test users per role/region, Jira access).

Test data during AI execution: when driving the app with Selenium or Vibium MCP, use one data row per test case. Never use bulk test-data
templates or data-driven Excel files. One row is enough to execute the flow and reach every page and element. Bulk and data-driven runs
belong to the Selenium-Framework engine after scripts are published; script-generator records which fields are parameters.

Related decisions (user, 2026-09-25):
- **Database:** `snd-schema` (`ng_astrone`) is the only S&D DB. Regions and versions vary, but the business flow is the same, so treat the DB as the base
  layer and the live env as an overlay. Don't call the DB "wrong" when a newer feature is missing.
- **Access:** no direct DB access or read-only DB user will be given. The MCP connectors are the access boundary.
- **Framework DB:** the target is `CTA_CONFIG_ASSERTION`, which the `selenium-framework-db` connector already points to.

See [[snd-test-automation-project]].
