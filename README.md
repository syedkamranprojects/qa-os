# QA OS

Agentic QA automation on Claude Code: Jira story → test cases → steps → live execution →
`selenium-framework-db` scripts + bulk case data for the legacy Regress engine.
Design: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

**Status:** P0, P1 done; P2 closed; P3 started. Resume with [docs/STATUS.md](docs/STATUS.md).

**Releasing or installing this for a team:** see [RELEASE_NOTES.md](RELEASE_NOTES.md) (what's in each version, known issues) and [DEPLOY.md](DEPLOY.md) (getting it onto another machine, registering the plugin, updating it).

```
.claude-plugin/marketplace.json   plugin marketplace (install: /plugin marketplace add <this repo>, then /plugin install qa-os)
plugins/qa-os/                    the plugin: agents, skills, commands, schemas
  agents/app-cartographer.md      builds app knowledge from DB metadata + live app
  skills/qa-orchestrator/         life cycle / stage status
  skills/step-dsl/                how to write and run steps
  commands/ play | learn | status
  schemas/steps.schema.json       step DSL v1
runtime/qaos_player.py            deterministic player (Selenium, no LLM); the only thing that types credentials
apps/<app>/                       app packs — the only per-application part
  app.yaml                        envs, login + menu recipes, widget vocabulary
  screens/<option_id>.json        screens verified live (provenance: observed)
  knowledge/                      domain.md, ui.md, data dictionary, menu, screens_db/ (DB-declared), env/<env>/ (harvested)
  flows/                          step-DSL flows
  tools/                          harvest/build scripts
framework/cta_config_assertion.md legacy engine (NGSelenium-Testing @ appium_development) target schema + case-data contract
docs/                             architecture, history
runs/                             run outputs (gitignored)
```

## Try it

```
python runtime/qaos_player.py apps/snd/flows/P0_open_sku_substitution_policy.json --dry-run
python runtime/qaos_player.py apps/snd/flows/P0_open_sku_substitution_policy.json
```

## Setup on a QA member's PC (one time)

1. Install **Python 3.10+** and **Google Chrome**.
2. `python -m pip install -r requirements.txt`. Selenium fetches the matching ChromeDriver automatically on the
   first run; it needs internet or proxy access to do so.
3. Add your own test login to your gitignored `.claude/settings.local.json` `"env"` block (e.g. `SD_TEST_USER`, `SD_TEST_PASSWORD`).
4. Check with `python runtime/qaos_doctor.py`. It should print `READY`. Use `--fix` to install missing packages.

**Credentials:** either your own `~/.qa-os/credentials.json` (copy `credentials.example.json`; passwords only), or `SD_TEST_USER` / `SD_TEST_PASSWORD` as env vars, or the workspace `.claude/settings.local.json` `env` block (gitignored). Only the player reads them; Claude never does.

## Where settings live

| What | File |
|---|---|
| Global defaults: limits (10 core cases), gates, safety rules, browser and wait settings, connector names | `qaos.yaml` |
| Per app: URLs, environments, non-production flag, users, **roles** (Maker, Checker; several users per role allowed), login recipe, **markets** (framework group and app id per market), defaults | `apps/<app-id>/app.yaml` |
| Passwords (per person, outside the repo) | `~/.qa-os/credentials.json` |
| Read everything through | `runtime/qaos_config.py` (`show`, `app`, `role`, `market`, `validate`) |

Adding an app means adding `apps/<app-id>/app.yaml` (same shape as `apps/snd` and `apps/gias`) and listing it in `qaos.yaml`; run `python runtime/qaos_config.py validate`.

## Changing the plugin (maintainers)
Claude Code loads the plugin from a **versioned cache** (`~/.claude/plugins/cache/qa-os/qa-os/<version>`), not from the repo. After editing agents, skills, commands or schemas:
1. Bump `version` in `plugins/qa-os/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`.
2. `claude plugin marketplace update qa-os`, then `claude plugin update qa-os@qa-os --scope project`.
3. Restart the session. (Editing without a version bump changes nothing in the cache.)
For quick iteration without version bumps, start Claude with `claude --plugin-dir ./qa-os/plugins/qa-os`.
