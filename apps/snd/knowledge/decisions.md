# snd decisions (generated from decisions.json; edit through qaos_intake/qaos_promote, not by hand)

Updated 2026-09-29. Status: observed (seen in the app) < stated (story author / QA) < ruled (BA).

## Terms (story term = app term)
| Story term | App term | Status | Source |
|---|---|---|---|
| Van Seller | Van Sales | stated | VAN-SALES-E2E 2026-09-29 (story author) |

## Variances (story vs app)
| Variance | Ruling | Note | Status | Source |
|---|---|---|---|---|

## Rules
| Rule | Text | Status | Source |
|---|---|---|---|
| one Draft request per PJP | Van Sale Stock Request: only one Draft request is allowed per PJP; a second attempt shows 'Draft requisition found, request No: <n>'. | observed | VAN-SALES-E2E 2026-09-28 (live app (cnr1dev1/KPO_mp)) |
| grid status New = Draft | A saved Van Sale Stock Request shows status 'New' in the grid; the story calls it 'Draft'. The duplicate-draft message suggests they are the same state (not confirmed). | observed | VAN-SALES-E2E 2026-09-28 (live app (cnr1dev1/KPO_mp)) |
