---
name: feedback-messages-as-assertions
description: Toasts, browser alerts, in-page popups and inline validations must all be captured (type + exact text) in training and recordings and turned into assertions; engine cannot assert alert text
metadata:
  type: feedback
---

The QA lead said on 2026-10-07: during training and AI execution, consider every **toast message, alert and popup** as a message for the **assertions** of the generated scripts.

**Why:** the assertions are what make a Regress Master script a test; a missing or paraphrased message is a weak test.

**How to apply:**
- In training, record each message on the option's page: type, exact text, trigger, buttons.
- In recordings, write `observed.messages`, with type toast/alert/popup/inline. Read alert text before accepting.
- In generation:
  - toast → `0000/0013 TSTMSG,<X>_ASSR` + EXPECTED_MESSAGE
  - popup → `0000/0013 ELEVAL` on the modal text element, then a click on its button
  - inline → `ELEVLD` (CASE_TYPE TP)
  - alert → `0005/0002` accept/dismiss only. The legacy engine (Main.java "Click Alert") reads the alert text but does not assert it, so list it in review_note and propose an engine change to the framework owner.

The rules are written into the skills recording-protocol, framework-conventions, knowledge-intake and quick-script.

Related: [[feedback-post-training-workflow]], [[reference-regress-casedata-contract]]
