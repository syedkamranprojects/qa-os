---
description: Main entry after training - a short request or one-liner (no Jira ticket) -> Claude writes its own steps from its training, executes once live, and generates Regress Master SQL + case data
argument-hint: [app] "<short request>"   e.g. snd "create one order and order detail with two products"
---

Use the `quick-script` skill in this session with the request `$ARGUMENTS` (default app `snd`; market and env
from the request or the app pack). Follow Q0 to Q6: map the request to trained business actions (stop if an option
is not trained), create a QUICK-<date>-<time> run, write the case, your own steps and today's data from the trained
knowledge and the app DB (never from existing framework workbooks or event chains), ask for ONE approval, execute
once (the QA member types the logins), then generate the Regress Master SQL, rollback and case-data workbook and
report how to apply and run them. Never type credentials or apply SQL.
