# <Business area>: how it works (S&D / DCODE)

Status: DRAFT written by Claude from the framework atlas, the snd-schema DB and observed live replays. No user guide exists. Every statement carries a confidence tag: **[observed]** seen live in a replay or recording, **[db]** declared by the application DB or the framework tables, **[stated]** said by an owner (BA/QA ruling, with name and date), **[inferred]** concluded by Claude from names or structure (to be confirmed), **[unknown]** not determinable yet. Rules: `docs/LEARNING_STANDARD.md` §3.
Last updated: <date>. Source flows: <atlas flow ids and group 11 seq numbers>.

## 1. Purpose
What the business does here and why it exists, in plain language (2-5 sentences). Where it sits in the Daily Cycle (what comes before and after).

## 2. Actors and roles
Who performs each part (only two roles: Maker and Checker; see `apps/snd/app.yaml` roles), which user plays the role on cnr1dev1, whether a different user must approve, and what the other role can or cannot do on this option.

## 3. Documents and master data
The documents this area creates or changes (document type, number format, where the number is shown) and the master data it needs (outlets, PJPs, products, warehouses, price lists ...).

## 4. Inputs: screens and fields
For each screen: menu path, screen title, the real field labels (mandatory marked), defaults the app fills, dropdown sources. Use the labels from the atlas / `step_labels.json` exactly.

## 5. Process: the business steps in order
Numbered steps in the standard vocabulary (`[Actor] Verb Object`), with the expected message (observed text if known), and the framework trace (`group:seq:flow`).

## 6. Outputs and effects
What exists afterwards: document status and approval status, stock movements (which warehouse, stock type, in/out/allocated), financial effect, numbers generated, what other areas now see.

## 7. Statuses and transitions
Table: from status -> action -> to status, by whom, with the confidence tag.

## 8. Rules and validations
Business rules and validations that were observed or declared (mandatory fields, "a document without lines cannot be forwarded", date rules, stock checks, one-draft-per-PJP ...). One line each with the evidence.

## 9. Messages
Exact toast/alert texts seen, and when.

## 10. Dependencies
Data this area reads from earlier areas (repos such as REPO_DOCUMENTNO, ORDERNUMBER, REPO_GINNO) and what it hands to later areas. Day-boundary rules (stock balances are keyed by date).

## 11. Test design hints
Positive and negative cases this area supports, boundary values, what a green framework run would NOT prove (silent-failure traps that apply here).

## 12. Open questions (batched for the BA; each with a default)
Only real business questions that the sources cannot answer. Format: `Q: <question> | Default: <what Claude assumes> | Evidence: <why unknown>`.

## 13. Sources
Atlas flow pages, DB tables/queries (names only), replay notes, with file paths.
