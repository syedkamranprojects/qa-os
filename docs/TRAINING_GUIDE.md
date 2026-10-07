# Training Claude on S&D with QA OS — guide for the QA lead

Release v0.5.0 (2026-10-07). For a QA lead who wants to train Claude on the S&D (DCODE) business with **their own Claude account and machine**. Claude starts with no memory of earlier sessions; everything it knows comes from this folder: the business pages, the session logs, `docs/STATUS.md`, `docs/OPERATING_RULES.md` and `docs/memory_export/`.

You can train it any way you like, and mix the methods:

| Method | You do | Claude does |
|---|---|---|
| **A. Documents** | Drop a user guide, instruction manual, SOP, deck or spreadsheet into `apps/snd/knowledge/sources/inbox/` | Reads it, records each rule in the business pages tagged with the document and page, and flags anything that contradicts what was already seen live |
| **B. Explain** | Explain a process or rule in chat, in your own words | Records it tagged with your name and the date; marks matching open questions as answered |
| **C. Walk a group** | Ask it to execute a framework group (e.g. group 11 Daily Cycle PK, group 61 BD, group 66 Setup PK); type the logins when it hands over | Executes each active flow live in order, records messages and effects, stops and asks when stuck |
| **D. Q&A / quiz** | Answer its open questions, or quiz it with test cases | Predicts, executes or looks up, compares, and fixes the pages where it was wrong |

## 1. Install (one time, about 20 minutes)

**Prerequisites:** Windows, Google Chrome, Python 3.10+ (tick "Add to PATH"), Node.js LTS, the **Claude desktop app** (Code tab) signed in with your account, and **read-only logins for the two databases** (S&D application DB and the framework DB `CTA_CONFIG_ASSERTION`) from the DBA or Syed.

1. **Get the files.** Make a workspace folder (e.g. `C:\QA\snd-training`) and put `qa-os` inside it:
   - Git: `git clone --branch v0.5.0 https://github.com/syedkamranprojects/qa-os.git` inside the workspace folder, or
   - Zip: unzip `qa-os-v0.5.0.zip` into the workspace folder (you get `...\snd-training\qa-os\`).
2. **Configure the MCP connectors:** double-click `qa-os\connectors\setup_mcp.bat`. It checks Python/Node/Chrome, installs the read-only DB connector, asks for the two database logins (password input is hidden; it tests each connection) and writes Selenium + `snd-schema` + `selenium-framework-db` into your Claude desktop config (a backup is taken first). Details: `connectors/db-mcp/README.md`.
3. **Register the plugin in the workspace:** create `<workspace>\.claude\settings.json` with the content of `qa-os\connectors\workspace_settings.example.json` (it registers the `qa-os` plugin and allows the browser and the two read-only DB connectors).
4. **Python packages for the runtime tools:** in `qa-os`, run `python -m pip install -r requirements.txt`.
5. **Fully quit and restart the Claude desktop app** (system tray -> Quit). Open the workspace folder in the Code tab. When asked to trust the folder and install the plugin, accept.
6. **Permission mode:** in the mode selector under the message box choose **Ask permissions** (not Auto). Approve "always allow" for the selenium tools the first time they are used.
7. **Optional - Jira:** claude.ai -> Settings -> Connectors -> Atlassian -> Connect, sign in with an Atlassian account that can open SDMS tickets, then switch it on for the session (message box `+` -> Connectors). Not needed for training.

**Check it worked** - ask in a new session:
- "Which connectors does this session have?" -> selenium, snd-schema, selenium-framework-db connected.
- "What do you know about this QA OS setup so far?" -> it should cite `docs/STATUS.md` and the business INDEX without being told. If not, say once: "read qa-os/docs/STATUS.md, qa-os/docs/OPERATING_RULES.md and apps/snd/knowledge/business/INDEX.md".
- Type `/qa-os:status` -> it lists runs and the S&D knowledge summary.

## 2. Start a training session

Type:
```
/qa-os:train snd
```
Claude reads the status and the knowledge index, then asks your name, the market (PK or BD - both are region R1), the environment (cnr1dev1) and today's method. Every session gets its own log in `runs/TRAIN-SND-<market>/<date>-<your name>/`.

Example requests:
- **Documents:** "I put the Route Settlement user guide in the inbox - learn it and tell me what contradicts what you already know."
- **Explain:** "Let me explain how credit notes from CLP incentives work in BD..." (then just explain).
- **Walk:** "Execute group 11 for PK today from seq 1", "Resume group 66 from seq 19", "Run the BD daily cycle (group 61)".
- **Q&A:** "Show me the open questions for settlement and I'll answer them", or "I'll give you test cases - predict the result first, then execute".

## 3. Rules Claude follows (so you know what to expect)
- **It never types a user id or password.** At each login it logs the previous user out and waits; you type the credentials in the Chrome window it controls, then tell it to continue (it can press Login for you). It then picks company and distributor itself.
- Users per market: PK Maker Auto_Multi_Orga, Checker Auto_Tssm (distributor 15108843); BD Maker Auto_Bangla, Checker AutoBD_tssm (company 010105, distributor 05108843).
- A daily cycle must finish within **one calendar day** (stock is keyed by day). Start in the morning.
- Before Route Settlement it clears leftover Reattempt orders due today (allocate -> GIN -> approve -> delivered) - see `OPERATING_RULES.md`.
- When something blocks it, it stops and asks you; your answer is recorded with your name and date.
- It never applies SQL to any database and only reads the two databases.
- Anything you say becomes `[stated <date> <your name>]`; documents become `[stated ... doc:<file> p.<page>]`; things it sees on screen become `[observed]`. Older statements are never deleted, only marked superseded, and conflicts become open questions.

## 4. Closing a session
At the end say "close the training session". Claude consolidates the log into the business pages, writes a short report next to the log (`apps/snd/knowledge/business/learning_sessions/`), updates `docs/STATUS.md` with a resume point, and lists the questions answered and still open. Log out and let it close the browser.

## 5. Shared environment etiquette (cnr1dev1)
- Only one person should run the daily cycle for the same distributor on the same day - documents and stock collide otherwise. Agree a slot with the team.
- Do not reuse documents created on an earlier day; read `docs/STATUS.md` "carry-over" first.

## 6. Sending your training back
So everyone (and every Claude account) learns from your sessions:
- **Git (preferred):** commit and push to a branch, e.g. `git checkout -b training/<your-name>-<date>`, `git add -A`, `git commit -m "S&D training <date> <topic>"`, `git push -u origin HEAD`, then tell Syed. Never commit `credentials.json`, `.claude/settings.local.json` or client-restricted documents.
- **Zip (if you only share the S&D pack):** zip `qa-os\apps\snd\`, `qa-os\docs\STATUS.md` and your `qa-os\runs\TRAIN-SND-*` folder and send it. It is merged centrally.

## 7. The S&D-only pack
`qa-os-snd-pack-v0.5.0.zip` contains just the S&D knowledge (`apps/snd/`) plus this guide and the operating rules. Use it to **read and review** what Claude has learned (start at `apps/snd/knowledge/business/INDEX.md`; open questions in `OPEN_QUESTIONS.md`; the QA team review sheet in `learning_sessions/`). To **train** Claude you need the full release (section 1), because the plugin, the connectors and the runtime tools live outside `apps/snd/`.

## 8. Troubleshooting
| Symptom | Fix |
|---|---|
| A connector shows "failed" | Re-run `setup_mcp.bat`; check the DB host is reachable on your network/VPN; restart the desktop app |
| `/qa-os:train` not found | The plugin is not registered: check `<workspace>\.claude\settings.json` (section 1 step 3), restart, accept the plugin install |
| Claude asks for passwords | It should not. Say "type nothing - I will log in" and report it |
| Typing amounts is blocked | Switch the mode selector from Auto to **Ask permissions** |
| Login page says "Invalid username and password" | Retype in the browser yourself; Claude does not see the password |
| The day's stock shows Opening 0 although yesterday closed with stock | Environment carry-over job did not run (known, `LIVE_FINDINGS` E-G11-3-1); tell the environment owner |
