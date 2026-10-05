---
name: reference-snd-navigation
description: "How to open any S&D (DCODE) screen: top-left hamburger -> Search Here -> click item; ignore the Kaspersky cert notice on the home page."
metadata:
  node_type: memory
  type: reference
  originSessionId: a4c8fc60-aee7-4615-b524-027e4cc3842f
  modified: 2026-10-01T11:25:29.029Z
---

S&D (DCODE) navigation, given by the QA lead 2026-10-01 and verified live on cnr1dev1:

1. Click the top-left hamburger menu (`#menurollin`, next to "CENTEGY TECHNOLOGIES").
2. The side menu opens with a "Search Here" box (`input[name=filterText]`, hidden until the menu is open); type the option name, e.g. "Dispatch Advice".
3. Click the matching item (`li#DYL_<layout>`, e.g. DYL_201068 = Dispatch Advice).
4. Click the hamburger again to collapse the menu.

The home page content area may show a Kaspersky "Visiting a domain with an untrusted certificate" notice. Ignore it, never click through it, and don't stop the run for it: menu navigation works regardless.

Recorded in `qa-os/apps/snd/app.yaml` `menu:` (toggle/search). Login hand-off and company/distributor selection: [[feedback-group-flow-execution-rules]].
