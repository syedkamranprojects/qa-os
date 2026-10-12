Subject: AI test automation for S&D - weekly summary, 5-9 October 2026

Dear <Department Head>,

A short summary of this week's work on our AI-assisted test automation for S&D (Pakistan).

Progress
- The AI has now learned two complete business cycles: the Daily Cycle (order booking to settlement) and the Setup flow (PJPs, outlets, DSRs, sections).
- It can take a short request or a Jira ticket, prepare test cases and steps, run the test and report the result, and produce automation scripts on request.
- The first AI-generated scripts (Order Booking) ran successfully in our regression tool, and the Order Booking and DSR Profile tests passed.

Why complete training matters
- Until the AI is fully trained on an area, it will raise many questions, or stop and ask for training, instead of running the test. This is by design, so that it never guesses.
- To run the cycle smoothly, the questions and gaps the AI has raised need to be answered by the QA team. Each answer is kept and reused, so the same question is not asked again.

Training is per country, not per region
- The AI is being trained on Pakistan. This does not mean other countries of the same region (e.g. Bangladesh) are covered; each country needs its own training.
- Two countries in one region can have different screens and rules. For example, in Pakistan the Distributor Profile has separate DT and TM screens, while Bangladesh uses a different Distributor Profile screen. Another example: the "Fortnightly" PJP visit frequency was a Bangladesh-only change.

Done by the QA team
- Shared two sets of training material, ran the Daily Cycle session and shared the first Pakistan ticket.

Pending from the QA team
- Response to the Setup flow review shared on 9 October; the first Pakistan ticket is on hold until then.
- A training session on promotions, and more Pakistan tickets.

Done by me
- Led the training sessions, approved the test designs and confirmed the scripts in our regression tool.

Pending from me
- Agree the approach for bulk test data and hand over the next version to the QA team after a final clean test run.

Regards,
Syed Kamran
