# QA OS Web App — concept (parked, 2026-10-07)

**Status: parked.** Start development only after (1) S&D training is finished and (2) the QA team has produced one final output
(framework SQL + case data) end to end and the framework owner has validated it in the legacy engine.

## Idea
A web application for QA users on top of the existing QA OS pipeline: no new AI logic. The app handles login, Jira, a job queue,
review/approval screens, live status and downloads. The AI work stays in the `qa-os` plugin agents/skills, run on a server worker
through the Claude Agent SDK (one stage per job, the run folder is the hand-off, as today). Not fully autonomous: every stage ends at a human gate.

## User flow -> existing QA OS stage
| User flow | QA OS stage (FINAL_DESIGN.md §3) | Runs on |
|---|---|---|
| Dashboard: my assigned + pending Jira tickets | (new) Jira read | web backend |
| Generate test cases | 1 story-analyst -> 2 test-designer | AI worker (no browser) |
| Review / finalize cases | G2 | web UI (grid editor; Excel import/export kept) |
| Generate / finalize steps | 3 step-author -> G3 step sheet | AI worker + web UI |
| Start AI execution cycle | 4 data-engineer -> 5 recorder | execution runner (browser + Selenium MCP) |
| Status notifications | run.json + recorder progress events | SSE/WebSocket + email/Teams |
| Download final output | 6 framework-generator -> 7 verifier | zip: framework.sql, rollback, case-data xlsx, review.md |

## Architecture
```
Browser (QA user) --SSO--> Web app (UI + API + Postgres)
                              |  Jira (per-user OAuth or service account)
                              v
                          Job queue
                    +---------+----------+
             AI worker               Execution runner (inside client network/VPN)
       (stages 1-3, 6-7;             Chrome + Selenium MCP + snd-schema
        no browser, parallel)        (stages 4-5; one run per env/role at a time)
                    +--- run folder / object storage ---+
```
Suggested stack: Python FastAPI backend (reuses runtime/*.py: qaos_intake, qaos_export/import, qaos_run validate,
gen_framework_sql), Postgres, RQ/Celery queue, React (or team's choice) frontend, Claude Agent SDK (Python) with the qa-os plugin.

## Hard parts to design for
1. **Logins in unattended execution.** Claude never types credentials. Default: the deterministic runner (not the model) logs in
   with Maker/Checker service accounts from a vault (qaos.yaml already intends "only the deterministic player" reads credentials).
   Fallback: embedded live browser view so the QA user logs in by hand.
2. **Recordings get stuck.** Add a "Needs input" run status: the run pauses, the question shows in the web UI with options,
   resumes on the answer (Agent SDK permission/user-input callbacks; hooks emit "step 12/30" progress events).
3. **One-calendar-day rule + shared test data.** One execution slot per env/role; pre-check rejects a day-cycle run that can't finish today.
4. **Network.** Runner must reach dcodecnr1dev1.unilever.com and the schema DBs -> likely a VM inside the client network/VPN.
5. **AI licensing.** Server use needs an API key (Anthropic API / Bedrock / Vertex), per-token billing, not Team seats. Measure cost per run on pilots.
6. **SQL never auto-applied.** Download = reviewed package; framework owner applies (G4).

## Ticket/run statuses (draft)
Pulled -> Analysed (G1 questions) -> Cases draft -> Cases approved (G2) -> Steps draft -> Steps approved (G3) -> Data resolved
-> Queued -> Executing (step x/y | Needs input | Waiting login) -> Recorded -> Generating -> Verified -> Ready to download
-> Applied by framework owner (G4) -> Reported to Jira (G5).

## Phases
- **MVP 1 (no browser):** SSO login, Jira dashboard, generate/review/approve cases and steps in browser, export team workbook.
- **MVP 2:** execution runner (queue, live status, Needs input, service-account login) -> generation + verification -> zip download.
- **MVP 3:** Jira comment (G5), knowledge-promotion screen, bulk-data factory, GIAS as second app.

## Preconditions before starting
- One generated framework.sql applied and replayed in the legacy engine (FINAL_DESIGN gap #4).
- Jira SDMS project access.
- Confirm "scripts" = CTA_CONFIG_ASSERTION SQL + case-data workbook (Selenium Java code would be a separate generator).
- Next step when unparked: full design doc (screens, status machine, DB tables, API, runner contract).
