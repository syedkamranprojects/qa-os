---
name: project-qaos-handover-fahad
description: From 2026-10-19 QA OS is owned by Muhammad Fahad on a QA installation (no git); only Fahad, Feroz Hussain and Syed Zulfiqar may train; design changes come to Syed Kamran as patches (runtime/qaos_patch.py)
metadata:
  type: project
---

On 2026-10-16 an email from the lead (Muhammad Irfan) moved Syed Kamran to GIS full-time from Monday 2026-10-19. QA OS passes to **Muhammad Fahad**. Feroz Hussain and Syed Zulfiqar support him, and Syed Kamran stays available with limited access.

**Arrangement (QA lead, 2026-10-16):**
- Fahad's machine is **always a QA installation**: release zip, no git. He trains it and maintains it locally.
- **Only Muhammad Fahad, Feroz Hussain and Syed Zulfiqar may train.** This is set in `qaos.yaml` `installation.trainers` and checked with `python runtime/qaos_config.py trainer "<name>"`.
- For important design or tool changes, Fahad sends a **patch** (`runtime/qaos_patch.py export`) to Syed Kamran. Syed applies it in the dev copy (`apply`) and sends a new release. Fahad then runs `import-local` so his newer local training is kept.
- The design guard message names the owner (Fahad) and the patch route.

The handover document is `qa-os/docs/HANDOVER.md`. It is written in plain language for the QA team, with no technical hardening items.

**How to apply:** in this dev workspace, Syed Kamran is now a part-time design contact. Expect requests to arrive as patch zips. Apply them with `qaos_patch.py show` / `apply`, then rebuild the release (`tools/build_release.py`).

Related: [[project-qaos-design-v4]], [[project-qaos-installations]].
