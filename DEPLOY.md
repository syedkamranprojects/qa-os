# Deploying QA OS to the QA team

This covers rolling the `qa-os` plugin out to other QA members / a shared QA environment checkout, separate from `README.md`'s "one-time setup on a QA member's PC" (which assumes the plugin is already registered). Read that too — this file is about *getting the plugin there in the first place* and keeping it current.

## 1. Get the files onto the target machine

Pick whichever matches how your team shares code:

- **Shared/network drive or existing checkout of this workspace:** nothing to do — `qa-os/` already sits inside it.
- **Git:** this folder is its own git repo (`qa-os/.git`), independent of anything above it.
  ```bash
  cd qa-os
  git remote add origin <your-team-git-remote>
  git push -u origin main --tags
  ```
  Each QA member then clones it anywhere and the workspace's `.claude/settings.json` (below) just needs a path that resolves to their clone.
- **Zip:** `git archive --format=zip -o qa-os-v0.4.0.zip v0.4.0` (run after tagging, see §4) produces a clean archive excluding `runs/`, caches and anything gitignored. Unzip into the target workspace.

## 2. Register the plugin in that workspace

**Standard layout (v0.5.0+):** `qa-os` itself is the workspace (`<drive>:\qa-os`) and already contains `.claude/settings.json` with `"path": "./"` - nothing to do. **Nested layout:** in the workspace root (the folder that contains `qa-os/`), `.claude/settings.json` needs:

```json
{
  "extraKnownMarketplaces": {
    "qa-os": { "source": { "source": "directory", "path": "./qa-os" } }
  },
  "enabledPlugins": { "qa-os@qa-os": true }
}
```

Use a **relative** path (`./qa-os`), never an absolute one — that's what makes this file safe to share/commit. If `qa-os/` lives somewhere other than directly under the workspace root, adjust the path accordingly (still relative).

Then, from a terminal in that workspace:
```bash
claude plugin marketplace add ./qa-os
claude plugin install qa-os@qa-os --scope project
```
(or just restart Claude Code in that workspace if `settings.json` already has the block above — it will pick it up on trust).

## 2a. MCP connectors (Selenium + read-only databases)

Run `connectors\setup_mcp.bat` on each machine (details: `connectors/db-mcp/README.md`). It configures `selenium`, `snd-schema` and `selenium-framework-db` in the Claude desktop config. For a QA lead who only trains Claude on the business, `docs/TRAINING_GUIDE.md` is the complete walkthrough.

## 3. Per-person one-time setup

Each QA member, on their own machine, does the steps in `README.md` → "Setup on a QA member's PC":
1. Python 3.10+, Google Chrome.
2. `pip install -r requirements.txt`.
3. Their own credentials — **never shared, never committed**:
   - Copy `credentials.example.json` to `%USERPROFILE%\.qa-os\credentials.json` and fill in passwords for the users they're authorized to use, **or**
   - set `SD_TEST_USER` / `SD_TEST_PASSWORD` (and per-role `SD_PASSWORD_<USER>`) as environment variables or in their own gitignored `.claude/settings.local.json`.
4. `python runtime/qaos_doctor.py` → should print `READY`.
5. `python runtime/qaos_config.py validate` → should print `OK` (warnings are fine; errors are not).

**Claude never reads or types these credentials.** Only the deterministic player (`qaos_player.py`) and, during a recording, the QA member themselves (typing into the browser) ever touch a password.

## 4. Updating the plugin (for whoever maintains it)

Claude Code loads the plugin from a **versioned cache**, not live from this folder. After changing any agent, skill, command or schema under `plugins/qa-os/`:

1. Bump `version` in **both** `plugins/qa-os/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` (they must match).
2. `claude plugin marketplace update qa-os`
3. `claude plugin update qa-os@qa-os --scope project`
4. Restart the Claude Code session.
5. Confirm: ask the Agent tool for an unknown agent name — the error message lists every loaded agent, so you can check yours is there.

For quick local iteration without bumping the version every time: `claude --plugin-dir ./qa-os/plugins/qa-os`.

Tag a release once it's been smoke-tested (`qaos_doctor.py` READY, `qaos_config.py validate` OK, `claude plugin validate ./qa-os/plugins/qa-os` passes):
```bash
git -C qa-os tag -a v0.4.0 -m "v0.4.0: see RELEASE_NOTES.md"
```

## 5. Running it in a QA environment (not just a dev laptop)

If "QA environment" means a shared machine/VM that the whole team drives the browser from (rather than each person's own laptop):

- `apps/snd/app.yaml` already has `non_production: true` on `cnr1dev1`/`cnr2dev3` — this is required before any data-changing step is authorized. If you add a new environment, set this explicitly; it defaults to **false** (no authorization) if omitted.
- The credentials file (`~/.qa-os/credentials.json`) lives under that machine's own user profile — set it up there, same as §3.
- Multiple QA members sharing one machine/session should use **separate OS user accounts** (or at least separate `%USERPROFILE%`) so credentials files don't collide and so `runs/` output from different people's work doesn't overwrite.
- The browser session is whatever's open in that Claude Code session at the time — there's no persistent login across sessions yet (see `FINAL_DESIGN.md` for the planned per-role browser-profile work).

## 6. First thing to try after install

Every new QA member is, by default, a **cold start**: different machine, different
Claude account, none of the development history or memory this platform was built
under. `qa-os/CLAUDE.md` is meant to make Claude Code pick this up automatically
(it points any fresh session at `docs/STATUS.md` and the business knowledge before it
does anything else) — but confirm it actually did, don't assume:
- Ask Claude "what do you know about this QA OS setup so far?" — it should cite
  `docs/STATUS.md` / `apps/snd/knowledge/business/INDEX.md` without being told to read them.
- If it doesn't (older Claude Code version, or `CLAUDE.md` auto-load disabled in their
  settings), tell it explicitly once: "read qa-os/docs/STATUS.md and
  apps/snd/knowledge/business/INDEX.md before we start."

Then:
```
/qa-os:status
```
should list any existing runs and summarize the `snd` app pack's knowledge (screen counts, menu harvest age). Then try the existing pilot:
```
python runtime/qaos_steps.py cheatsheet
```
to see the step vocabulary a QA member writes test steps in, and read `docs/QA_STEP_CHEAT_SHEET.md`.

## Rollback

If a version misbehaves: `claude plugin update qa-os@qa-os --scope project --version <older-version>` (or re-tag/checkout the previous git tag and repeat §4). `qaos.yaml` and `app.yaml` changes are plain files — revert them with git the same way.
