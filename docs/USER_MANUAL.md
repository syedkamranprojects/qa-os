# QA OS — user manual

QA OS turns Claude into a QA assistant for our applications (S&D / DCODE first). You talk to it in plain English in the Claude desktop app, and use a few **slash commands** that start with `/qa-os:`.

Setup is in `docs/TRAINING_GUIDE.md` §1. Open the folder `<drive>:\qa-os` in Claude, then type `/qa-os:` in the message box to see the list.

## The commands at a glance

| Command | What it does | Use it when |
|---|---|---|
| `/qa-os:status` | Shows recent runs and what Claude knows about each app | Start of the day, or to check progress |
| `/qa-os:train` | Training session: teach Claude the business | **Now** (S&D training phase) |
| `/qa-os:quick` | Ad-hoc request in one line → live AI test run → test result (Regress Master scripts on request after a pass) | **Main use after training** |
| `/qa-os:learn` | Refreshes screens, menus and field labels of an app | After a release changes screens |
| `/qa-os:cases` | Jira story → requirement analysis → test cases + Excel | Only if a Jira story is available |
| `/qa-os:steps` | Writes executable test steps for those cases | After cases are approved |
| `/qa-os:run` | Does cases and steps in one go for a story | Only if a Jira story is available |
| `/qa-os:play` | Checks a saved flow and tells you how to run it without AI | To replay a finished flow |

After training, QA OS is used through `/qa-os:quick` with short requests. The Jira-based commands (`cases`, `steps`, `run`) remain available but are not the normal starting point.

---

## 1. `/qa-os:status`: where are we?

```
/qa-os:status
/qa-os:status SDMS-2990
```
**You get:** the latest runs (ticket or case, verdict, failed step), and for each app how many screens are known and when they were last harvested.

---

## 2. `/qa-os:train`: teach Claude the business

```
/qa-os:train snd
/qa-os:train snd PK walk 11
/qa-os:train snd BD explain
```
Claude first asks your **name**, the **market** (PK or BD), the **environment** (cnr1dev1) and how you want to train today. Then use any of these methods.

**a) Give it a document.** Copy the file into `apps\snd\knowledge\sources\inbox\`, then say:
> I put "Route Settlement user guide.pdf" in the inbox. Learn it and tell me what is different from what you already know.

*Claude:* "I added 14 rules from chapters 3–5 to the settlement page. Two of them conflict with what I saw live on 6 Oct. Which is right: …?"

**b) Explain in your own words**
> In Bangladesh, a CLP incentive creates a credit note at month end. It is adjusted against the outlet's next invoice.

*Claude:* "Recorded as stated by you today. It also answers open question Q-…; I've updated the delivery and returns page."

**c) Ask it to run a framework group live**
> Execute group 11 for PK today from seq 1.
> Resume group 66 from seq 19.

At each user switch, Claude logs out and says, for example, "Please log in as Auto_Tssm". **You type the user and password in the browser**, then reply "logged in, go ahead" (Claude can press the Login button for you). Claude picks the company and distributor itself. If it gets stuck, it stops and asks you.

**d) Questions and quiz**
> Show me the open questions for settlement.
> I'll give you a test case: predict the result first, then execute it.

**Finish:**
> Close the training session.

Claude merges everything into the knowledge pages, writes a session report, and updates `docs/STATUS.md`. Then send your work back: see the training guide, §6.

---

## 3. `/qa-os:quick`: the main way to work after training (no ticket)

```
/qa-os:quick snd "book an order for one outlet with two products"
/qa-os:quick snd "BD: book an order for one outlet with three SKUs, then allocate it"
```
Quick mode is for **testing**: you give an ad-hoc request in one line, and Claude tests it live and tells you the result. Your request **is** the test case.
1. **Confirms the run context first.** Market, environment, who is running it and which users log in: one short question, nothing assumed.
2. **Plans the test from its training.** It maps your words to the business actions and screens it was trained on, and picks the data from the trained test data catalog (outlets, PJPs, SKUs). If something isn't trained, it asks you (a quick answer) or asks for a training session first (`/qa-os:train`).
3. **You approve once.** Claude shows the steps it will follow, the data and what will be created in the environment.
4. **Executes once, live.** You type the logins. Checks that depend on today (e.g. stock) run first.
5. **Reports the result:** PASS / FAIL / BLOCKED, every message the app showed, the documents created and any defect found.
6. **Scripts only if you want them.** After a **pass**, Claude asks: *"Do you want Regress Master scripts for this flow?"* Say yes and it generates `framework.sql` (the new test flow), a rollback script and the Excel case data (for the executed case, or with more data rows if you ask), checked by the verifier. Say no and you keep just the test result. The run is always recorded, so you can ask for the scripts later without running it again: *"generate scripts for QUICK-20261009-1430"*.

*Example result:* "PASS: order COL2600000xxxx, 'Validation successfully', 'Order Save successfully'. Do you want Regress Master scripts for this flow?"

---

## 4. `/qa-os:learn`: refresh screen knowledge

```
/qa-os:learn snd
/qa-os:learn snd "Transaction > Receivable > Deposit Slip"
```
**You get:** what was added or changed (menus, fields, labels), and any differences between the database definitions and the live screens.

---

## 5. `/qa-os:cases`: from a Jira story to test cases *(optional, needs a Jira story)*

```
/qa-os:cases SDMS-2990
/qa-os:cases SDMS-2990 --story C:\temp\SDMS-2990.docx
```
The Jira connector must be signed in; otherwise give `--story` with an exported or pasted story.

1. Claude analyses the story: rules, acceptance criteria, and **ambiguities**. Answer the ambiguities (gate G1).
2. It designs up to 10 core cases plus a backlog, and writes the team Excel workbook.
3. You review and approve the cases (gate G2). Reply "approved", or give your changes.

---

## 6. `/qa-os:steps`: write the test steps *(after cases are approved)*

```
/qa-os:steps SDMS-2990
```
Claude writes the steps in our standard wording, for example:
> [Maker] Navigate to Dispatch Advice
> [Maker] Create Dispatch Advice with Warehouse = Auto Main Warehouse
> [Checker] Forward Dispatch Advice with comment "Automation Approval"

It checks each label against the real screen and marks every step **clear** or **needs input**. Fix the "needs input" steps in the Excel (column *Test Steps*, plain English), then approve (gate G3).

---

## 7. `/qa-os:run`: the whole front half in one command *(optional, needs a Jira story)*

```
/qa-os:run SDMS-2990 --app snd --env cnr1dev1
```
This runs analysis → cases → steps, stopping at each gate for your approval. At the end you get the workbook path and the list of cases ready to run.

---

## 8. `/qa-os:play`: replay a finished flow without AI

```
/qa-os:play runs/SDMS-2990/20261007-1037/flows/TC01.json
```
Claude dry-runs the flow first. If the flow needs a login, it gives you the command to run yourself (so your password never goes through Claude):
```
python runtime/qaos_player.py runs/SDMS-2990/20261007-1037/flows/TC01.json
```
When it finishes, say "done". Claude summarises the result and the evidence files.

---

## Good to know
- **Claude never types passwords** and never applies SQL. Database access is read-only.
- **Gates:** Claude waits for your approval at each gate. "approved", "go ahead", "yes" or "LGTM" approve; anything else is treated as feedback.
- **Plain English works too.** You don't have to use commands; for example, "what are the open questions for Order Editing?" or "why did Route Settlement fail?"
- **One daily cycle per distributor per day** on the shared environment.
- **Stuck?** Look at the troubleshooting table in the training guide (§8), or ask Claude: "check docs/STATUS.md and tell me where we are".
