# SDMS-12084 (Order Editing DT, B2B orders): questions for the QA team (2026-10-15)

Context: QA confirmed that this ticket also applies to Pakistan (R1, cnr1dev1). QA OS is trained on Order Editing, the order flow (booking, allocation, unallocation) and the R1 roles. It is **not** trained on the new **Order Editing DT** screen or on **B2B orders**. Please answer these before the test cases are run.

## A. B2B orders
1. What makes an order a **B2B order** in Pakistan? For example: the outlet's "B2B enroll" flag, the order or document type ("B2B Sale"), or the channel the order comes in from (interface)?
2. On the **Order Editing** screen, how can a user tell a B2B order from a non-B2B order? Is there a column, a flag, an order number prefix or a document type?
3. Can a B2B order be **created through the DCODE screens** (e.g. Order Booking for a B2B-enrolled outlet)? Or does it only come in through the interface?

## B. Test data on cnr1dev1
4. Is there a **B2B order** for distributor 15108843 (IBRAHIM TRADERS), or for another PK distributor, that can be brought to the editable state (**unallocated, delivery date today**, as Order Editing requires)? Please share the order number(s).
5. If none exists, how should we create one for testing, and who can do it?
6. Which **non-B2B order** may we edit for the test? Or should we book a new one ourselves through Order Booking?

## C. Users and access
7. Which login is the **DT user** for this ticket: Auto_Multi_Orga or Automation? Which is the **HQ user**: headquarter?
8. When a DT user should no longer access the existing **Order Editing** screen, is it simply **missing from their menu**? Or is the screen visible but showing a message (please give the exact text)?
9. Has the new **Order Editing DT** screen been given to the DT and HQ roles on cnr1dev1 already? Where is it in the menu (expected: Home > Transaction > Order > Order Editing DT)?

10a. A menu option **Order Editing HQ** already exists next to Order Editing. Which one does the story mean by "the existing Order Editing screen" for HQ users?

## D. Behaviour
10. On **Order Editing DT**, is a B2B order **hidden completely** (not in the list and not found by search)? Or is it listed but blocked from editing (with which message)?
11. Are the **editing actions** on Order Editing DT exactly the same as on Order Editing (quantity reduction with reason, validation, save)?
12. Should an **HQ user** see B2B orders on **Order Editing DT** too, or only non-B2B orders there as well (the story says the DT screen shows only non-B2B orders)?

The same questions, with QA OS's current assumptions and yellow answer columns, are in `2026-10-15_SDMS-12084_QA_Team_Questions.docx`. Answers will be recorded on the Order Editing business page and used to write the test cases. If an answer is missing, the related case is parked and run later.
