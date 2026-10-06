# Inbound stock and stock checks (area summary)

Updated: 2026-10-06 (G11-3 consolidation: DA 1360, loss 641, GRN 248; seq 9 opened the day with Opening 0 again, Q-OB2); 2026-10-05 (G11-2/2b consolidation); 2026-10-01 (G11-1 consolidation; earlier: live blocks 1-3b)

1. Stock enters the distributor warehouse through a Dispatch Advice (DA): maker creates and forwards, checker approves; received quantity (dispatched minus loss) becomes Sound stock. Confirmed on DA 1358 (5 lines, losses on 2): In rose by exactly the received quantity; the Maker still has Forward/Reject on his own Pending DA (Q-DA1) [observed 2026-10-01 G11-1].
2. A DA with losses creates a DA Loss Approval record that the checker approves; where the loss lands as stock is unknown. (Superseded 2026-10-01 G11-1: one loss record per DA, created at the DA approval; approving it creates NO stock row, L21 closed; any use outside stock, e.g. claims, is open.)
3. Stock is shown in Stock Inquiry as Opening/In/Out/Allocated/Closing in CS, DZ, PC per warehouse, product, batch and stock type. Effects seen in one day: DA approval In up; order save Allocated up / Closing down; cancel before GIN releases; GIN approval Allocated -> Out with Closing unchanged; edit/cancel after GIN no effect; GRN approval In up [observed 2026-10-01 G11-1].
4. Balances are keyed by calendar day; a new day has no data until a movement creates the row: the DA approval creates the row of a received product (Opening 0, In = received) without Generate Opening Balances [observed 2026-10-01]; previous-day closings are not carried automatically. (Superseded 2026-10-01 G11-1: by 16:40 the same day all 39 rows had Openings = previous Closing + previous Allocated; who generated them is open, Q-OB1.)
5. Four framework flows (seq 9, 24, 50, 60) check this stock after DA, GIN, GRN and for opening/closing. Their absolute-value assertions fail on a busy day (seq 9 expects In 80, day In 164); check before/after deltas instead [observed 2026-10-01 G11-1].
6. Goods Return Note puts undelivered goods back in stock after approval; it has not been replayed live. (Superseded 2026-10-01 G11-1: GRN 246 walked live; it brings back everything not delivered or returned after the GIN (19 CS reconciled exactly) and posts it as Sound In on approval, without reducing Out.)
7. Maker = Auto_Multi_Orga, checker = Auto_Tssm, stock check by Auto_Multi_Orga (the Maker; Auto_Tssm has no Stock Inquiry).
8. A cycle that receives and issues stock must finish within one calendar day. Route Settlement additionally needs every previous working day closed (Q-RS1) [observed 2026-10-01 G11-1].
9. **New-day rule (2026-10-05, supersedes the carry statements in item 4):** a new day has 0 rows until the first movement; the DA approval created all 39 rows at once with Opening = previous Closing + still-Allocated (62740537: 245 + 63 = 308), so previous closings ARE carried [observed 2026-10-05 G11-2]. Why 10-01 morning differed is Q-OB2.
10. Second independent day (2026-10-05: DA 1359, loss 640, GRN 247) reproduced every G11-1 stock rule and amount; the approved SAN 96 (Stock Adjustment Admin, -50 CS) posts as Out; settlement, posting and the day close move no stock [observed 2026-10-05 G11-2, G11-2b].

Order of pages: dispatch_advice.md, da_loss_approval.md, stock_inquiry_and_balances.md, stock_validation_flows.md, goods_return_note.md.

## What this area hands to the next area
| Handed item | To (area) | Detail |
|---|---|---|
| Approved Sound stock per warehouse for today | Orders (booking, allocation, editing) and GIN | Orders allocate against it; GIN approval needs a balance row for the same day (confirmed by GIN 506, G11-1) |
| REPO_DOCUMENTNO (DA number) | Same-area approval flows | Used by seq 5 |
| Stock after GIN / GRN checkpoints | Delivery, returns, Route Settlement | GRN quantity back in stock before settlement |
| Day-boundary rule | Every later flow | Run the whole cycle in one calendar day |
| REPO_GRNNO | GRN approval (seq 49) | Same area, then stock check seq 50 |

Sources of the G11-2/2b update: learning_sessions/2026-10-05_G11-PK_session2_log.md, learning_sessions/2026-10-05_G11-PK_session2b_resume_log.md.
Sources of the G11-1 update: learning_sessions/2026-10-01_G11-PK_session1_log.md, learning_sessions/2026-10-01_G11-PK_session1_report.md.
