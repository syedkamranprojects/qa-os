# Inbound stock and stock checks (area summary)

Updated: 2026-10-01 (live blocks 1-3b)

1. Stock enters the distributor warehouse through a Dispatch Advice (DA): maker creates and forwards, checker approves; received quantity (dispatched minus loss) becomes Sound stock.
2. A DA with losses creates a DA Loss Approval record that the checker approves; where the loss lands as stock is unknown.
3. Stock is shown in Stock Inquiry as Opening/In/Out/Allocated/Closing in CS, DZ, PC per warehouse, product, batch and stock type.
4. Balances are keyed by calendar day; a new day has no data until a movement creates the row: the DA approval creates the row of a received product (Opening 0, In = received) without Generate Opening Balances [observed 2026-10-01]; previous-day closings are not carried automatically.
5. Four framework flows (seq 9, 24, 50, 60) check this stock after DA, GIN, GRN and for opening/closing.
6. Goods Return Note puts undelivered goods back in stock after approval; it has not been replayed live.
7. Maker = Auto_Multi_Orga, checker = Auto_Tssm, stock check by Auto_Multi_Orga.
8. A cycle that receives and issues stock must finish within one calendar day.

Order of pages: dispatch_advice.md, da_loss_approval.md, stock_inquiry_and_balances.md, stock_validation_flows.md, goods_return_note.md.

## What this area hands to the next area
| Handed item | To (area) | Detail |
|---|---|---|
| Approved Sound stock per warehouse for today | Orders (booking, allocation, editing) and GIN | Orders allocate against it; GIN approval needs a balance row for the same day |
| REPO_DOCUMENTNO (DA number) | Same-area approval flows | Used by seq 5 |
| Stock after GIN / GRN checkpoints | Delivery, returns, Route Settlement | GRN quantity back in stock before settlement |
| Day-boundary rule | Every later flow | Run the whole cycle in one calendar day |
| REPO_GRNNO | GRN approval (seq 49) | Same area, then stock check seq 50 |
