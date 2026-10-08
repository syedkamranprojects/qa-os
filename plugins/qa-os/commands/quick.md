---
description: Main entry after training - a short request or one-liner (no Jira ticket) -> Claude writes its own steps from its training, executes once live, and generates Regress Master SQL + case data
argument-hint: [app] "<short request>"   e.g. snd "create one order and order detail with two products"
---

Use the `quick-script` skill in this session with the request `$ARGUMENTS` (default app `snd`). Follow Q0 to Q6.
**First, before anything else, confirm the run context with the QA member in one question** (Q0): market, environment,
who is running it, the Maker (and Checker) user, and anything else the request leaves open - options from the app pack,
never assumed silently; the confirmed context goes into run.json and the header of the generated SQL.
Then map the request to trained business actions (stop if an option is not trained), create a QUICK-<date>-<time> run,
write the cases, your own steps and the data rows from the trained knowledge only (test data catalog; never from
existing framework workbooks or event chains, no app DB lookups), ask for ONE approval, execute ONE case once (the QA
member types the logins), then generate the Regress Master SQL, rollback and case-data workbook for all cases and
report how to apply and run them. Never type credentials or apply SQL.
