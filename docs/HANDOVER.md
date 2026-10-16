# QA OS handover to Muhammad Fahad (16 October 2026)

From **Monday 19 October 2026** QA OS is owned by **Muhammad Fahad**. Syed Kamran moves to GIS full-time and can be consulted with limited availability. Feroz Hussain and Syed Zulfiqar support Fahad.

## 0. Installing on Fahad's machine (one time)
1. Unzip **`qa-os-v0.6.0.zip`** into the workspace folder, giving a `qa-os` folder.
2. Unzip **`qa-os-v0.6.0_handover_work.zip`** into the **same** workspace folder. It adds the ticket runs (`runs/SDMS-*`) and ticket notes (`inbox/`) so the work in progress continues.
3. Follow `DEPLOY.md`: register the plugin, connect the MCP connectors (Selenium browser, Jira, the read-only S&D database and the framework database) and do the per-person setup.
4. Check: `python runtime/qaos_config.py mode` prints **QA**, owner Muhammad Fahad, and the three trainers.
5. Open Claude Code in the `qa-os` folder and type `/qa-os:status`.

## 1. What QA OS is, in one paragraph
QA OS is an "AI intern" for S&D / DCODE testing that runs inside Claude Code. It is trained on the business: screens, rules, roles, messages, Pakistan setup. Given a Jira ticket, it:
1. reads the ticket;
2. writes the test cases and plain-English steps into **one Excel** for you to approve;
3. runs **one case of each path** live in the browser;
4. reports pass/fail with Jira-ready defect drafts;
5. for every path that passed, produces the **Regress Master scripts** (SQL + case-data Excel) for the framework owner, **Muhammad Imran**.

Cases on the same path, negative cases included, are not run by the AI. They become data rows that Regress Master replays.

## 2. Your machine and your role
- **Your machine is a QA installation**: the release zip, no git. `python runtime/qaos_config.py mode` must print **QA**.
- **You own QA OS day to day:** you start ticket runs, approve the Excel, train it, and keep the business knowledge correct.
- **Only three people may train QA OS: Muhammad Fahad, Feroz Hussain and Syed Zulfiqar.** Claude checks the name at the start of every training and refuses anyone else.
- **You cannot change the QA OS design on your machine** (skills, agents, tools, rules). Claude refuses and notes the request in `feedback/design_gaps.md`.
- **When something important must change**, make a patch and send it to Syed Kamran:
  ```
  python runtime/qaos_patch.py export --note "what is needed and why"
  ```
  The zip lands in `feedback/patches/`. It carries your training, your runs and your notes. Syed Kamran applies it in the dev copy and sends you a **new release zip**. After installing the new release, run `python runtime/qaos_patch.py import-local <your last patch zip>` so that training you did after sending the patch is kept.

## 3. Daily use
Open Claude Code in the `qa-os` folder. Claude reads `CLAUDE.md`, `docs/STATUS.md` and the business pages on its own.

| You want to | Type | What happens |
|---|---|---|
| Test a Jira ticket | `/qa-os:run SDMS-xxxx` | Claude asks the run context (market, environment, who runs it, Maker / Checker users, distributor) and checks the ticket is Pakistan and that every screen is trained. It then gives you **one Excel** to approve (questions with defaults, cases, paths, steps, data). After approval it runs one case per path. |
| Test an idea without a ticket | `/qa-os:quick <one line>` | Claude plans one case, you approve, it runs once and reports. Scripts only if you ask. |
| Train Claude | `/qa-os:train snd` | Claude asks your name, checks you are a trainer, then learns from your explanation, a document, Q&A or a live walk. Every new screen also gets a "screen file" (what the screen looks like). |
| See where things are | `/qa-os:status` | Run status per ticket. |

**Logins:** Claude types the **user ID**; you type the **password** in the browser window Claude opened. Then you either log in yourself, or tell Claude "click on login". Claude never types or reads passwords. There is one login per user role for the whole run (Maker first, then the Checker for approvals).

**When Claude stops and asks:** this is by design. Any difference between what it predicted and what the screen does stops that path, and Claude asks you. Your answer is saved so the same question is not asked again. A real defect stops only its own path.

**Common blockers:**
- **"Access Denied":** the site's gateway blocks after heavy use. Wait until it opens again, then say "retry".
- **Wrong distributor picked:** Claude checks the distributor in the profile menu and corrects it.
- **Rejected login:** retype the password in the same window.

## 4. Users on cnr1dev1 (Pakistan)
| Role | User | Notes |
|---|---|---|
| DT user / Maker | **Auto_Multi_Orga** (also Automation) | Company Unilever Pakistan Limited, distributor **15108843 - Ibrahim Traders** ("Auto KARACHI" on some screens). The login can select 6 PK distributors. |
| Checker / approvals | **Auto_Tssm** | TSSM approvals |
| HQ user | **headquarter** | Role 0014, HQ screens, no approval |

R1 roles: 0001/0005 = DT submit, 0002/0008 = approval, 0014 = HQ. A user can act only if their role is in the screen's workflow.

## 5. Ticket status (16 October 2026)
| Ticket | Subject | Status | Next action |
|---|---|---|---|
| SDMS-6084 | Off Days dropdown on Distributor Profile HQ | **Done.** 16 of 19 pass; TC11 blocked (no distributor has an old free-text value); TC12/13 skipped on purpose. Report To defect D-6084-1 did not come back. | Ask QA whether D-6084-1 was fixed. Scripts can be generated on request. |
| SDMS-12084 | Order Editing DT / B2B orders (BD CR, valid for PK) | QA answered the questions document (15 Oct). | 1) Ask QA for **one B2B cash memo for 15108843**, unallocated, delivery date today. 2) Claude does a read-only look at **Order Editing** and **Order Editing HQ** as Auto_Multi_Orga and headquarter. 3) Run `/qa-os:run SDMS-12084`. |
| SDMS-5997 | Vehicle Master Bulk Upload | Parked after a read-only look as headquarter. Only one screen exists ("Vehicle Master Bulk Upload"); the template was downloaded. | Answer 3 questions: is it one screen for create and update? Is "Auto KARACHI" = 15108843? Are updates done by uploading rows with an existing Code? |
| SDMS-6550 | System users hidden on the User screen; logout after a user change | **Training needed** on the User screens (Company setup > Users). | Train Claude: which screen, what a system user is, which attributes count, how to see the logout, which test user may be changed. |
| SDMS-5372 | Dispatch Advice primary loss reason codes | Paused at analysis (older design). | Restart with `/qa-os:run SDMS-5372` when wanted. |
| SDMS-2990, SDMS-12390 | — | Parked earlier, waiting for training. | Later. |
| SDMS-11461 | GIN message (R2) | Skipped: not Pakistan. | — |

## 6. Where things are (in the `qa-os` folder)
- `apps/snd/knowledge/business/`: everything Claude knows about the business. Start at `INDEX.md`. Open questions are in `OPEN_QUESTIONS.md`.
- `apps/snd/screens/`: one screen file per trained screen. `_index.json` lists which screens are trained and their gaps.
- `apps/snd/knowledge/business/learning_sessions/`: training logs and the question documents sent to QA, with their answers.
- `runs/<TICKET>/<date-time>/`: each run's Excel (`<TICKET>_TestCases.xlsx`), `summary.md`, results and recordings.
- `feedback/design_gaps.md`: design requests noted on your machine. `feedback/patches/`: patches to send.
- `docs/DESIGN_V4_DECISIONS.md`: every design decision. `docs/OPERATING_RULES.md`: standing rules. `docs/STATUS.md`: latest status. `docs/QA_GUIDE.md` and `docs/TRAINING_GUIDE.md`: how-to guides.

## 7. Rules to keep
- **Tickets:** current work is **Pakistan only**. Bangladesh CRs are skipped unless QA confirms they apply to Pakistan.
- **Training:** a screen that was never trained stops the run. Train it first.
- **Approval:** the Excel you approve is the source of truth. Edit it, and Claude re-imports it and shows only what changed.
- **Never:** share passwords with Claude, apply SQL, or post to Jira from Claude. Claude drafts and you post.
- **Scripts:** go to **Muhammad Imran**, who applies them on a test copy and replays them first.

## 8. Who to ask
- **Business questions:** Feroz Hussain and Syed Zulfiqar.
- **Regress Master scripts and the framework:** Muhammad Imran.
- **QA OS design:** Syed Kamran, limited availability. Send a patch with a note.
