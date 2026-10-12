# Design / tool gaps noted in a QA installation

In a **qa** installation (the QA team's release, see `python runtime/qaos_config.py mode`), Claude does not change QA OS tools, skills, design documents or recordings. When Claude notices a design or tool gap during training or a run, it notes it here and tells the QA member to **check with the design contact first** (`qaos.yaml` > `installation.design_contact`).

Send this file back together with your training work (docs/TRAINING_GUIDE.md §6). The QA OS team reviews every row and moves it to `docs/HARDENING.md` when it needs a fix.

| Date | QA member | Run / session | Where (stage, screen, tool) | What happened | Suggested change | Status |
|---|---|---|---|---|---|---|
