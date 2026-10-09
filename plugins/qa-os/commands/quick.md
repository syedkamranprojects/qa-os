---
description: Main entry after training - an ad-hoc request or one-liner (no Jira ticket) -> Claude plans the test from its training, executes it once live as an AI test run and reports the result; Regress Master scripts only if wanted after a pass
argument-hint: [app] "<ad-hoc request>"   e.g. snd "book an order for one outlet with two products"
---

Use the `quick-script` skill in this session with the request `$ARGUMENTS` (default app `snd`). Follow Q0 to Q6.
**First, before anything else, confirm the run context with the QA member in one question** (Q0): market, environment,
who is running it, the Maker (and Checker) user, and anything else the request leaves open - options from the app pack,
never assumed silently.
The request itself is the test case: do not design a case list unless the request asks for cases. Map the request to
trained business actions (stop if an option is not trained), create a QUICK-<date>-<time> run, plan the steps (internal)
and the data from the trained knowledge only (test data catalog; never from framework workbooks or event chains, no app
DB lookups), ask for ONE approval, execute once live (the QA member types the logins; the run is always recorded), and
report the test result (pass / fail, messages, documents, defects). Only after a PASS ask whether the QA member wants
Regress Master scripts (SQL + rollback + case data) for this flow; generate them only on yes. Never type credentials or
apply SQL.
