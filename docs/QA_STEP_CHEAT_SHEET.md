# QA OS predefined step words

Write each step in one of these forms. Use the label exactly as it appears on the screen. If a step does not fit, start it with `Do:` and it will be treated as manual.

| Step form | You can say it like | Risk |
|---|---|---|
| `Login as <Role>` | log in as, sign in as, login with the user of, log in | read-only |
| `Select distributor <name or code>` | choose distributor, pick distributor, distributor is | read-only |
| `Switch user to <Role>` | change user to, logout and login as, log in as a different user | read-only |
| `Logout` | log out, sign out, exit | read-only |
| `Navigate to <Screen>[ > <Tab>]` | go to, open screen, open menu, open the screen | read-only |
| `Go to tab <Tab>` | switch to tab, open tab, click tab, move to tab | read-only |
| `Open <Document> <number or NAME>` | open the record, find and open, search and open, edit | read-only |
| `Filter <Column> = <value>` | search by, filter by, find rows where | read-only |
| `Enter <Field> = <value>` | type, fill, put, set | read-only |
| `Choose <Field> = <value>` | select, pick, dropdown, set dropdown | read-only |
| `Create <Document> with <Field> = <value>, <Field> = <value>` | add new, new, create a new, make a | changes-data |
| `Add line to <Document>: <Field> = <value>, <Field> = <value>` | add product, add item, add row, add detail line | changes-data |
| `Add loss to line <n>: <Field> = <value>, <Field> = <value>` | add damage, add lost quantity, record loss | changes-data |
| `Remember <Field> as <NAME>` | note down, keep, store, save the number as | read-only |
| `Save <Document>` | store, click save, update | changes-data |
| `Delete <Document>` | remove, cancel the record | one-way |
| `Forward <Document> with comment "<text>"` | send for approval, submit, send to next level, push | one-way |
| `Approve <Document>[ with comment "<text>"]` | authorize, accept, ok the, sign off | one-way |
| `Reject <Document> with comment "<text>"` | send back, decline, refuse | one-way |
| `Select all rows` | tick all, select everything, check all, tick the header box | read-only |
| `Select rows where <Column> = <value>` | tick the rows with, select the row with | read-only |
| `Click <Button>` | press, hit, push the button, process | changes-data |
| `Verify message "<text>"` | check the message, message should be, toast shows, expect message | read-only |
| `Verify <Document> is [not ]listed` | check it is in the list, should appear in the grid, should not be in the grid | read-only |
| `Verify status of <Document> is <status>` | check status, status should be, approval status is | read-only |
| `Verify <Field> is <value>` | check, field should show, value should be, make sure | read-only |
| `Do: <plain sentence>` | anything else | read-only |


## Rules of thumb
1. **One line = one step.** Start with the verb from the table.
2. **Use the label exactly as it appears on the screen** (for example `Vendor Code`, not "vendor"). If you are not sure, Claude shows you the screen's real labels and you pick.
3. **Say who does it** only when the person changes. `Login as Checker` or `Switch user to Checker` starts the checker's steps.
4. **Approval is by a different user** on the same screen: `Approve Dispatch Advice DA1`.
5. **Give each new document a name** so later steps can refer to it: `Remember Document No as DA1`, then `Open Dispatch Advice DA1`.
6. **After every action say what you expect**: `Verify message "Saved successfully"`. If you do not know the text, write `Verify message (text to be recorded)`.
7. **Do not write waits, element ids or mouse actions.** Claude handles those.
8. **Not sure how to say it?** Just write it in plain English; Claude rephrases it into these forms and asks you to confirm.

## Example (Dispatch Advice, maker and checker)
```
1. Login as Maker
2. Navigate to Dispatch Advice
3. Create Dispatch Advice with Warehouse = Auto Main Warehouse, Vendor Code = UPL WH, SO Number = Automation_01
4. Verify message "Saved successfully"
5. Remember Document No as DA1
6. Add line to Dispatch Advice DA1: Product = 62740537, Quantity CS = 80
7. Forward Dispatch Advice DA1 with comment "Auto"
8. Verify message "Forwarded successfully"
9. Switch user to Checker
10. Navigate to Dispatch Advice
11. Approve Dispatch Advice DA1
12. Verify status of DA1 is Approved
```
