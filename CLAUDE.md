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

Standing preferences and run rules of the QA lead (account-independent): read `docs/OPERATING_RULES.md` (copies of the assistant memory notes are in `docs/memory_export/`). Latest resume point: end of `docs/STATUS.md`.

**Current phase (v0.5.0): S&D training.** When someone wants to teach you the business (documents, verbal explanation, Q&A, or "run group 11 / 66 / 61"), use the `knowledge-intake` skill (`/qa-os:train snd`); the trainer's guide is `docs/TRAINING_GUIDE.md`. Never type credentials; never apply SQL.
