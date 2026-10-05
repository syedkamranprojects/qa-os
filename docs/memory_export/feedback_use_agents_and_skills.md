---
name: use-agents-and-skills
description: "QA OS work must be distributed across the plugin's sub-agents and skills (context isolation), not run inline in the main session; the user asked this repeatedly."
metadata:
  node_type: memory
  type: feedback
  originSessionId: eb4a66f7-6654-4151-a641-fe8df7bda0d6
  modified: 2026-09-30T05:10:28.945Z
---

The user has asked several times that QA OS stages run in their respective agents and skills, so each agent handles its own context. On 2026-09-30 they pointed out that I had forgotten this, and I found the cause: the `qa-os` plugin (qa-os/.claude-plugin/marketplace.json) was never registered in `.claude/settings.json`, so none of its agents or skills loaded and every stage ran inline.

**Why:** running inline caused context compactions, lost instructions and repeated UI rediscovery. The platform must be shareable across QA members, and that only works through installed agents and skills.

**How to apply:**
- Check that the qa-os agents appear in the Agent tool's list before starting stage work. If they don't, fix the registration first.
- Delegate each stage to its agent, with a file-based brief.
- Keep the main session as a thin orchestrator with gates.
- The final design and the gap register are in `qa-os/docs/FINAL_DESIGN.md`. See [[snd-test-automation-project]], [[minimise-user-intervention]].

**Gotcha (2026-09-30):** plugins load from a versioned cache (`~/.claude/plugins/cache/qa-os/qa-os/<ver>`). New/edited agents and skills are invisible until you bump the version in plugin.json + marketplace.json, run `claude plugin marketplace update qa-os` and `claude plugin update qa-os@qa-os --scope project`, then restart. Verify by calling the Agent tool with the new type: an unknown type's error lists the loaded agents.
