# QA OS

If you are opening this folder for the first time, or starting a QA OS task without
earlier context in this conversation: **read `docs/STATUS.md` first** (bottom section
is the current resume point), then `apps/snd/knowledge/business/INDEX.md` (the closest
thing to a user guide this application has — no vendor documentation exists).

Do not re-derive, re-explore or re-ask for anything already written in those files or
the pages they point to (the business knowledge pages, the framework atlas, the step
vocabulary). Treat this workspace as having no memory from any prior session unless
`docs/STATUS.md` says otherwise.

This file exists specifically so a fresh Claude session — a different machine, a
different account, no shared memory — still finds its footing automatically. See
`RELEASE_NOTES.md` for what the platform does and `DEPLOY.md` for one-time setup
(MCP connectors, credentials, plugin registration) before anything here will work.

**Owner (from 2026-10-19): Muhammad Fahad** - read `docs/HANDOVER.md` first. Only Muhammad Fahad, Feroz Hussain and Syed Zulfiqar may train QA OS (check with `python runtime/qaos_config.py trainer "<name>"`). Important design changes go as a patch (`python runtime/qaos_patch.py export --note "..."`) to Syed Kamran.

Check which installation this is with `python runtime/qaos_config.py mode` (dev = QA OS team's working copy with `qaos.dev.yaml`; qa = the QA team's release). In a qa installation, design or tool gaps are noted in `feedback/design_gaps.md`, not fixed (see docs/OPERATING_RULES.md).

Standing preferences and run rules of the QA lead (account-independent): read `docs/OPERATING_RULES.md` (copies of the assistant memory notes are in `docs/memory_export/`). Latest resume point: end of `docs/STATUS.md`.

**Current phase (v0.6.0, design v4 - `docs/DESIGN_V4_DECISIONS.md`):** training by the three trainers (`/qa-os:train snd`, guide `docs/TRAINING_GUIDE.md`); Jira tickets via `/qa-os:run <KEY>` (Pakistan only); ad-hoc requests via `/qa-os:quick`. AI runs one case per path; Regress Master scripts go to the framework owner Muhammad Imran. Claude types only the user ID, never a password; never applies SQL.
