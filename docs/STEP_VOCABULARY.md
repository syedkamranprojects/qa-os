# QA OS step vocabulary (v1.0)

One shared language for test steps, for the reader of a test case **and** for Claude. A step says *who* does *what* to *which document*, in plain words. Each business step is defined once per app in `apps/<app>/steps/library.yaml`, which also says what it executes and what to watch out for. The technical step DSL (`plugins/qa-os/skills/step-dsl`) stays underneath as the executable layer.

## 1. How a test case is written

```
TC-DA-01  Create, forward and approve a Dispatch Advice with loss
Objective : a maker creates a Dispatch Advice, a checker approves it, and stock is received
Actors    : Maker = <user>, Checker = <user>          (roles, not names, in the steps)
Data      : one row (Warehouse, Vendor, Products, Quantities ...)
Steps
  1. [Maker]   Login as Maker
  2. [Maker]   Navigate to Dispatch Advice
  3. [Maker]   Create Dispatch Advice with Warehouse = "Auto Main Warehouse", Vendor Code = "UPL WH", SO Number = "Automation_<date>"
                Expect: message "Saved successfully"
  4. [Maker]   Remember Document No as DA1
  5. [Maker]   Add line to Dispatch Advice: Product = 62740537, Quantity CS = 80
                Expect: message "Saved Successfully!"
  6. [Maker]   Add loss to line 2: Stock = Damaged, Loss Reason = Area Closed, Quantity CS = 4
  7. [Maker]   Forward Dispatch Advice DA1 with comment "Auto"
                Expect: message "Forwarded successfully"; Approval Status = Pending for approval
  8. [Maker]   Logout
  9. [Checker] Login as Checker
 10. [Checker] Navigate to Dispatch Advice
 11. [Checker] Approve Dispatch Advice DA1
                Expect: message "Forwarded successfully"; Status = Active; Approval Status = Approved
 12. [Checker] Logout
Expected result : Dispatch Advice DA1 is Approved and its stock is received
```
Rules of the format:
- One line = one step = one verb from section 2. Number the steps. Start each with the **actor in brackets**.
- **Roles, not user names** in steps (Maker, Checker, Stock Controller). The actor map (library.yaml `actors`) says which user plays which role in which environment.
- `Expect:` lines are checks; the message text is the app's real text.
- Values come from the **data row**, not typed into steps; `<date>` and `Remember ... as NAME` values are placeholders.
- Every user change is written as `Logout` then `Login as <role>`. (Same as `Switch user to <role>`, which Claude runs as those two steps.)

## 2. The vocabulary

**Session**
| Step | Meaning |
|---|---|
| `Login as <role>` | The QA lead logs in as the user playing that role (Claude never types passwords). Claude then checks that the user name shown on screen is the expected one |
| `Select distributor <name or code>` | Choose the distributor after login, where the app asks for one |
| `Switch user to <role>` | Shorthand for `Logout` + `Login as <role>` |
| `Logout` | Sign out through the profile menu; ends the session |

**Navigation**
| Step | Meaning |
|---|---|
| `Navigate to <Screen>` | Open the screen by its menu name (Claude searches the sidebar). Optional tab: `Navigate to Dispatch Advice > Dispatch Detail` |
| `Open <Document> <no or name>` | Filter the screen's grid by document number and open the first matching row |

**Entering data**
| Step | Meaning |
|---|---|
| `Enter <Field> = <value>` | Type into a text or date field |
| `Choose <Field> = <value>` | Pick a value in a dropdown |
| `Create <Document> with <Field> = <value>, ...` | Fill the header fields and Save it. Expect the save message |
| `Add line to <Document>: <Field> = <value>, ...` | Add one detail row (product, quantity ...) and save the row |
| `Add loss to line <n>: <Field> = <value>, ...` | Add a loss row to a detail line, calculate and save the line |
| `Remember <Field> as <NAME>` | Store a value shown on screen (usually the Document No) for later steps: `Open DA1` |

**Document lifecycle**
| Step | Meaning |
|---|---|
| `Save <Document>` / `Update <Document>` / `Delete <Document>` | The screen's own buttons |
| `Forward <Document> with comment "<text>"` | Forward for the next level, with a mandatory comment |
| `Approve <Document>` (= `Authorize <Document>`) | A **checker** completes the approval of a forwarded document. In S&D this is the Forward button on a document that is *Pending for approval*; it must be done by a user other than the maker |
| `Reject <Document> with comment "<text>"` | Reject instead of approve |

**Checks**
| Step | Meaning |
|---|---|
| `Verify message "<text>"` | The toast after the previous action contains this text (the exact text is recorded the first time) |
| `Verify status of <Document> is <status>` | Status and/or Approval Status in the screen's grid |
| `Verify <Field> is <value>` | A field or grid cell shows this value |
| `Verify <Document> is listed` / `is not listed` | Grid presence |
| `Verify stock of <Product> in <Warehouse> changed by <n>` | Stock check on the stock screen or inquiry (planned) |

**Rules for wording**
- Use the **screen's own names** for screens, fields, buttons and statuses (Dispatch Advice, Vendor Code, Forward).
- Prefer the lifecycle verbs above to "click the Forward button" (the how is in the library).
- Do not write waits, element ids or locators in a test case. Those belong to the library and the helper.
- A step that is not in this vocabulary is written as `Do: <plain sentence>` and is treated as **manual** until it is added to the library.

## 3. How steps run (what Claude does with them)
1. Each business step is looked up in `apps/<app>/steps/library.yaml` and expanded into the executable primitives (`login`, `navigate`, `enter`, `choose`, `click`, `select_row`, `verify_ui`, `capture` ...). Steps whose library entry is `verified: false` are run as recording steps and flagged.
2. Claude runs them one at a time through the browser, logs each action, and captures the messages.
3. The same steps, with the recorded ids and messages, become the framework events (flow spec -> SQL + case-data workbook), so the legacy engine repeats exactly what was written.
4. Any user change stops the run at a **switch point** (`Logout`, `Login as <role>`); Claude verifies who is logged in before going on.

## 4. Adding a new term
Add the step to `library.yaml` (name, parameters, expansion, expected message, gotchas) and add a row to this document. A term is only accepted if it names a business action, not a mouse action. Ask Claude: "add step `<name>` to the S&D library".
