---
name: project-quick-mode-redesign
description: DONE 2026-10-09 (plugin 0.5.2) - /qa-os:quick = ad-hoc AI test execution; request is the case; steps internal; scripts only if user says yes after a pass.
metadata:
  type: project
---
Agreed with the QA lead 2026-10-08 (implement on 2026-10-09):
- `/qa-os:quick` is for **ad-hoc AI execution for testing**. The request itself is the test case: no cases.json / case workbook unless the user explicitly asks for cases (e.g. "with 5 positive test cases").
- Main output = **test result**: pass/fail, observed messages, documents created, evidence, defects.
- **Steps stay as an internal plan** (strict mode needs written steps): shown in the single approval, kept in the run folder for audit, not a deliverable.
- **Always record silently** (watcher), so scripts can be generated later without re-running.
- **After a PASS only, ask:** "Do you want Regress Master scripts for this flow?" Yes -> SQL + rollback + case data (ask how many data rows; default 1 = executed case); No -> end with the test report.
- `/qa-os:run` (story/ticket life cycle) keeps designed cases, approved step sheet, scripts always.

**Why:** QA lead: ad-hoc requests are themselves the case; quick is for AI execution testing; scripts only when the user wants to save the flow for Regress Master.

**How to apply (tomorrow):** update quick-script skill (Q1-Q6), commands/quick.md, docs/OPERATING_RULES.md, user manual; then bump plugin version and update the installed copy. Supersedes the "N cases -> N rows always" part of [[feedback-post-training-workflow]]. Related: [[project-qaos-quick-mode]], [[feedback-run-context-first]].

**Implemented 2026-10-09 (plugin 0.5.2):** quick-script skill rewritten (Q0 context, Q1 one case = the request, Q2 internal steps, Q3 one approval, Q4 one AI test run always recorded, Q5 test_report.md, Q6 scripts only after PASS on request, also later from the recording), commands/quick.md, OPERATING_RULES, USER_MANUAL md/html/pdf. Not tried live yet in the new form.
