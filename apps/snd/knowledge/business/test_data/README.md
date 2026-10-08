# Test data catalogs (training material)

QA OS takes **all test data from training** (QA lead rule, 2026-10-08): when it writes test cases and steps (quick mode Q2, story runs Stage 3) it reads only these catalogs and the business pages - it does not open the app or query the app DB. One file per market (`PK.md`, `BD.md`, ...).

- Each entry carries its source tag: `[observed <date> <session>]` (seen live in a training walk) or `[stated <date> <name>]` (given by a trainer).
- Live state (stock, today's documents) is NOT kept here; runs check it with precondition steps during execution.
- A request that needs data the catalog does not have is a knowledge gap: short -> ask the user and add the answer here; long-term -> training session.
- Trainers: add or correct entries in a training session (`/qa-os:train snd`), or tell Claude in chat.
