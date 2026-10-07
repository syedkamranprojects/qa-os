---
name: reference-group-users-query
description: "Read the user/login per framework group row from selenium-framework-db with the QA lead's query (never select plu_password); login status N on seq 1 still means \"start as that user\""
metadata:
  node_type: memory
  type: reference
  originSessionId: b5778f77-fda9-45aa-a9b0-f6d24e0e917f
  modified: 2026-10-05T12:15:45.919Z
---

To know which user runs each row of a framework group (e.g. 66 NG_Setup Flow_PK, 11 Daily Cycle), use the QA lead's query (2026-10-05), WITHOUT the password column:

SELECT d.pgtfd_sequenceno, d.ptf_testflowid, tf.ptf_description, d.plu_serial_no, u.plu_name, d.pgtf_testflow_login_status, tfd.pmg_menugroupid
FROM fct_pr_gtfd_group_test_flow_detail d
JOIN fct_pr_gtf_group_test_flow f ON d.pgtf_grouptestflowid = f.pgtf_grouptestflowid
LEFT JOIN fct_pr_lu_login_users u ON d.plu_serial_no = u.plu_serial_no
LEFT JOIN fct_pr_tfd_test_flow_details tfd ON d.ptf_testflowid = tfd.ptf_testflowid
JOIN fct_pr_tf_test_flow tf ON d.ptf_testflowid = tf.ptf_testflowid
WHERE d.pgtf_grouptestflowid = '<group>' AND d.pgtfd_status = 'Y' ORDER BY d.pgtfd_sequenceno;

- **Why:** the framework atlas mislabels seq 1-4 of group 66 as "runner default login"; the DB says Automation (serial 28). Running them as Auto_Multi_Orga left Prospect Outlet Forward disabled.
- **How to apply:** run this before any group replay and take the user per row from it; `fct_pr_lu_login_users.plu_password` is plain text - never select it (use explicit columns). Then follow each flow's fct_pr_sef_screen_events_flow (active rows, sequence order) + active fields.

Related: [[feedback-group-flow-execution-rules]], [[project-g11-session3-plan]]
