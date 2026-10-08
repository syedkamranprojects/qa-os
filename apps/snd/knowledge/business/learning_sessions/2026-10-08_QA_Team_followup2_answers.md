# QA team answers to the 2026-10-08 second follow-up (received 2026-10-08, via Syed Zulfiqar in chat)
Tag for merging: [stated 2026-10-08 QA Team (follow-up 2)].

1. Q-SV2 (which "Return Document" posts OUT in Stock Inquiry?): "Purchase return to the company"
   => "Return Document" in the Q-SV1 stock list means a purchase return of stock from the distributor to the company. It posts OUT. Sales returns from outlets are a different document and come back IN through the Goods Return Note (observed on 3 days, returns 713-715 / GRNs 246-248). The QA team did not give the menu option name: finding it is still LIVE_LEARNING_CHECKLIST L45 (read-only menu search).

2. D-G11-2b-1 (route 02112 for 2026-10-01 Complete, but slips 1131-1136 Un Posted and invoices COL26000002004 / COL26000002005 still open; seen 2026-10-05 and 2026-10-06): "Irrelevant question - abnormal data"
   => Withdrawn as a defect: the 2026-10-01 state is abnormal environment data on cnr1dev1, not product behaviour to report. The design rule from Q-DS3 still stands (a settled route must have all its slips Posted and adjusted), so the positive check "after Route Settlement every slip of that route/date is Posted" is kept.
   Carry-over: the 2026-10-01 leftovers (slips 1131-1136 Un Posted, invoices 2004 / 2005 open) stay on the env and still inflate outlet 04 / 05 outstanding totals; do not use them as fixtures or as evidence for expected values.
