# Step sheet: <KEY or flow name>   (run <folder>)
Status: DRAFT for gate G3      App: <app>   Env: <env>   Market: <PK>   Date: <yyyy-mm-dd>
Actors: Maker = <user>, Checker = <user>, ...      One-day chain: <yes/no>      Authorization (from decisions.json): <allow list>

## Steps
| # | Actor | Step | State | Trace | Expect | Risk |
|---|---|---|---|---|---|---|
| 1 | Maker | Login as Maker | clear | 11:1:021400000 | user shown = <user> | read-only |
| 2 | Maker | Navigate to <Screen> | clear | 11:2:<flow> | breadcrumb shows the screen | read-only |
| 3 | Maker | Create <Document> with <Field> = <value> | NEEDS INPUT (Q1) | 11:2:<flow>:<screen>:e3 | message (to be recorded) | changes data |
| ... | | | | | | |

## Switch points
1. after step <n>: Logout, Login as <Checker role> (<user>)

## Questions for QA (each answered once)
**Q1 - <topic>**
What I found: <one sentence with evidence>.
What I need: <decision>.
Default if you skip: <default>.
Options: 1) ... 2) ...

## Sign-off
Approved by: ______   Date: ______   (approval phrase in chat counts: "approved" / "go ahead" / "LGTM")
