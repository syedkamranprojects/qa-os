---
name: feedback-never-mention-source-code
description: Never tell the QA team/trainers that knowledge came from reading source code; code facts stay internal (<!--i--> marker, build_release.py strips them).
metadata:
  type: feedback
---
Never mention to the QA team, trainers or in shared documents/emails that QA OS learned anything by reading application source code. Phrase code findings as plain business questions or "edge cases to check live".

**Why:** QA lead, 2026-10-08: "Never mention that you learn by reading the source code"; chose option 1: keep code facts in the working copy, internal only.

**How to apply:** code-derived lines in knowledge Markdown end with ` <!--i-->` (knowledge-intake method E rule 4); build any QA-team package with `python tools/build_release.py <version>` (drops marked lines, sources/code/, the code report, method E; refuses on unmarked [code tags or leaks). Never zip the qa-os folder by hand. Talking to the QA lead himself in this workspace is fine. Related: [[reference-ms-promotion-repo]], [[project-promotions-partial-training]].
