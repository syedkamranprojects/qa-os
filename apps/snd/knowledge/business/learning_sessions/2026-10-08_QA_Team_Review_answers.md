# QA team answers to the 2026-10-06 review (received 2026-10-08)

Source: `knowledge/sources/20261008_2026-10-06_G11-PK_QA_Team_Review_answered.docx` (filled by the QA team). Verbatim text of the answer columns; tag for merging: [stated 2026-10-08 QA Team].

## Section 2 - rules learned (Agree? / Comment)

### Rule 1 (Order editing) - Agree: Y
Rule: Order Editing lists only orders that are unallocated and whose delivery date is today. Before step 15: run Delivery Date Change to today, then unallocate the order.

### Rule 2 (Order editing) - Agree: Y
Rule: Saving an order edit re-allocates the order automatically.
Comment: Yes, only unallocated stock orders will appear on the Order Editing screen. The user can only reduce the order quantity. Once the changes are saved, the system will automatically allocate the available stock against the modified order/invoice.

### Rule 3 (Order editing) - Agree: N
Rule: After the GIN is approved, an order can be edited without unallocating it.
Comment: ORGA Parameter: CASHMEMO_EDIT / Purpose: Controls whether a Cash Memo can be edited after creation/approval.  / If set to Y: The system allows the user to edit the Cash Memo, subject to the applicable business rules (e.g., quantity can only be reduced and a modification reason is required).  / If set to N: Cash Memo editing is disabled.  / Business Context: In Pakistan, this feature is used to allow Cash Memo modification after the GIN has been approved. On saving the modification, the system adjusts the corresponding GIN stock quantity accordingly.

### Rule 4 (Order editing) - Agree: Y
Rule: A Cashmemo Reschedule unallocates the order (2018 reappeared on the Unallocated tab).

### Rule 5 (Transaction Inquiry) - Agree: Y
Rule: Ordered = the outlet’s original order quantity; Allocated = what available stock allowed. Ordered 5 CS 4 PC / Allocated 4 / Delivered 3 on 2015 is expected.
Comment: Based on Stock availability given the stock and deliver QTY will be modified on delivery

### Rule 6 (Stock) - Agree: Y
Rule: GIN approval moves Allocated to Out; GRN approval posts In; SAN approval posts Out. 62740537 ended at Opening 0 / In 97 / Out 89 / Closing 8.
Comment: For Stock Reconciliation, the current day's stock is reconciled and cleared to ensure the correct opening stock is carried forward for the next day's activities.

### Rule 7 (Stock) - Agree: Y
Rule: Opening must carry the previous day’s closing. Opening 0 after a day with closing stock (259 on 5 Oct, 0 on 6 Oct) means the environment’s carry-over job did not run. Check the previous closing before any stock validation.
Comment: Stock Carry Forward: The closing stock from the previous working day is carried forward as the opening stock for the next working day.

### Rule 8 (Tax) - Agree: Y
Rule: Outlets 06 and 07 swapped tax behaviour because their master data and the tax promotion were modified.
Comment: Based on the outlet’s tax attributes—Registered/Non-Registered, Tax Filer, Advance Tax Exempted, and Tax Exempted—the system recalculates the applicable tax on the invoice.

### Rule 9 (Tax) - Agree: Y
Rule: A zero-tax invoice for an outlet that is not tax-exempt cannot be delivered; a tax-exempt outlet’s zero-tax invoice is allowed. Not exercised yet (zero-tax order 2017 was cancelled).
Comment: Parameter: ZERO_TAX_ORDER_EXEMPTION / Purpose: Controls whether orders/invoices with zero tax can be delivered.  / If set to Y: The system allows the zero-tax order/invoice to be delivered.  / If set to N: The system does not allow delivery of the zero-tax order/invoice.

### Rule 10 (Collections) - Agree: Y
Rule: Two collection modes: Outstanding Cash memos = collect per invoice (cash or cheque per slip type); Outstanding Outlet = enter cash/cheques per outlet and the system adjusts them FIFO, oldest invoice first.
Comment: There is a feature to manually enter collections through the Back Office using the Deposit Slip screen. After creating a deposit slip, three tabs are available for user convenience: / Outstanding Cash Memos: This tab displays all delivered orders where the net amount has not been fully adjusted. The user can search by Cash Memo number and record the payment received through cash or cheque. / Outstanding Outlets: This tab displays outlets that have outstanding Cash Memos. The user can enter the collection amount at the outlet level. Upon saving, the system automatically adjusts the amount against the applicable outstanding Cash Memos for that outlet. / Deposit Slip Detail: This tab displays the collection details entered and assigned to the respective deposit slip, allowing the user to review the recorded transactions.

### Rule 11 (Collections) - Agree: Y
Rule: Duplicate cheque numbers are allowed because no cheque inventory is kept.
Comment: System is allowed to enter the duplicate cheque number

### Rule 12 (Collections) - Agree: N
Rule: Slips are not blocked against each other before settlement; an invoice already on an unposted slip is still offered. Reconciliation happens at Route Settlement.
Comment: The collection flow consists of the following steps: / Payment Collection: The DSR collects payments from outlets through the Delivery App in the form of cash or cheque. / Mobile Synchronization: At the end of the working day, the DSR synchronizes the device data with the Back Office. / Automatic Deposit Slip: Once the data is synchronized, the system automatically generates Cash/Cheque Deposit Slips in the Back Office with an Unposted status. / Route Settlement: The DSR closes the day's activities with the accountant. The accountant reconciles the collected payments and any stock/cash shortages during the route settlement process. / Deposit Slip Posting: Once the route settlement is completed successfully, the status of the related Deposit Slips changes from Unposted to Posted.

### Rule 13 (Collections) - Agree: N
Rule: Doubled totals on the Outstanding Outlet tab (outlet 05 shows 202,322 for one 101,161 invoice) are a display defect. Use Outstanding Cash memos or Transaction Inquiry for amounts.
Comment: There is a Transaction Inquiry screen that displays invoice details, including gross amount, discount, tax, received/offset amount, and net amount etc. / We observed that in this case, the offset amount has been fully adjusted, but it does not impact the net amount. Therefore, based on the current logic, I believe the suggested scenario is showing the correct behavior.

### Rule 14 (Cheque Status) - Agree: Y
Rule: Step 55 is a check only: confirm cheques read “Clear”. Never press Bounce.
Comment: There are three types of cheque statuses: / Cleared/Realized: Once the cheque is received and the related deposit slip is posted, the system automatically adjusts the cheque amount against the respective invoice. However, the cheque realization/clearance date may be a future date. / Bounced: If the cheque is not cleared on the expected cheque date, the user can process it through the Bounced Cheque option in Back Office. This screen displays all deposit slips containing cheques against invoices. The user can select the respective cheque and click Bounced to reverse the payment against the invoice. The reversed amount is then created as an outstanding amount at the outlet level. / Note: Based on country-specific business requirements, countries such as Pakistan and Bangladesh prefer to mark the cheque status as Cleared/Realized immediately after the deposit slip is posted.

### Rule 15 (Route Settlement) - Agree: Y
Rule: Procedure: Edit on the route row → cash Received editable (prefilled), cheque Received read-only, stock shortage editable → row Save → “Saved Successfully”.
Comment: It is the final settlement of the DSR, performed by the accounts person based on the actual payment received from the outlet against the invoice, either in cash or by cheque. / The settlement amount cannot be edited; however, certain fields remain editable in cases where the accountant needs to make adjustments, such as cash utilized by the DSR for fuel or challan expenses. / In case of a stock shortage, if the DSR does not submit the actual returned quantity, the shortage amount is calculated based on the product sale price × shortage quantity (in UOM), with the applicable tax percentage as configured in the Product Configuration screen.

### Rule 16 (Route Settlement) - Agree: Y
Rule: On Save the system reconciles cash, cheques, DSR cash and stock shortage, posts all the route’s slips, adjusts the invoices; fully paid invoices leave every collection screen.
Comment: It is a consolidated record of all activities performed by the DSR during daily deliveries, including: / Delivering orders to outlets and receiving payment in cash or cheque. / Managing stock-in and stock-out against delivered invoices and recording product returns from outlets. / Collecting outstanding payments against previous credit invoices. / Collecting returned products from outlets. / Depositing the collected cash into the nearest bank to minimize the risk of loss or incidents. / Recording any cash shortage if the DSR uses collected cash for personal or unauthorized expenses. / Recording any stock shortage if the DSR fails to return the complete quantity of products. / The distributor/depot maintains DSR/PJP-wise daily collection records and updates the respective outlet ledger to ensure proper tracking and reconciliation of sales, collections, returns, and shortages.

### Rule 17 (Route Settlement) - Agree: Y
Rule: Row colour: yellow = route not closed; green = route closed.
Comment: Kindly ignore the color themes. If the route is not settled, an Edit link will be displayed at the end of the row; otherwise, the field will remain blank.

### Rule 18 (Route Settlement) - Agree: Y
Rule: Settlement is blocked per PJP while that PJP’s previous day is not closed (“Following previous days not closed!”). The day close clears it.
Comment: The system controls this validation. When the accountant attempts to settle the current route, the system checks whether the previous stock has been settled by verifying that the PJP working date is the current date and the closing date is equal to N-1.

### Rule 19 (Route Settlement) - Agree: Y
Rule: “Un-Deliver Order exists for today delivery!” blocks settlement when a reattempt order is due today. Before step 51 every reattempt order due that day must be covered in a GIN: allocate (Order Date = booking date) → new GIN → Checker approves → Cashmemo Status Delivered. It may stay unpaid; an unpaid invoice is not a cash shortage.
Comment: Yes, this is system-controlled. Any unsettled transaction for today must be reconciled, where the GIN quantity must match the GRN quantity. Otherwise, the system will display a “Stock Mismatch” error.

### Rule 20 (DSR adjustment) - Agree: Y
Rule: DSR Adjustment Amount records a DSR shortage arising while he collects money from the outlet. Saving 400 raised Total Shortage and Balance by 400; Total Adjusted did not change.
Comment: Yes it couldn’t be allowed to change the stock shortage

### Rule 21 (Day close) - Agree: Y
Rule: Day close = PJP Daily Inquiry Update: End Of Day + Complete → Current Status E. Order of the day: settlement → DSR adjustment → day close.
Comment: This option is used for manual working from the backoffice application.

## Section 3 - open questions

### Q-SR1
Question: When does an approved and picked sales return reduce the outlet’s receivable?
Answer: In the route settlement, multiple activities are performed by the DSR/PJP, including delivering orders to outlets, collecting payments from outlets through cash or cheque, collecting returns, modifying current order quantities (known as Fresh Return), and adjusting approved credit notes at the outlet level. / Note: The Fresh Return transaction is based on the specific country business requirement. For example, it is not used in Pakistan, while Bangladesh uses Fresh Return for current order quantity modification. / Credit note adjustments are applied based on the invoice net amount, where the invoice amount is greater than the credit note amount. / Therefore, it is not necessary for all scenarios or data to appear for every DSR/PJP. However, we will include these scenarios in our regression master tool test flow to ensure proper coverage.

### BA12
Question: (Meaning already answered: a DSR shortage.) Remaining: what reduces a DSR shortage (what feeds Total Adjusted)? Are negative adjustment amounts allowed?
Answer: There are three types of collection/settlement adjustments: / Cash: The receivable amount can be reduced, but it cannot become negative. Any difference will be reflected in the Cash Shortage column. / Cheque: The cheque amount cannot be modified, as the cheque value must remain unchanged. / Stock Shortage: This is generated when the DSR returns the remaining stock to the distributor/depot warehouse. The expected GRN quantity is calculated as: / GIN Quantity – Delivered Order Quantity + Picked Sales Return Quantity / The warehouse in-charge enters the actual received quantity for each product. If there is any difference between the expected and actual received quantity, the system will calculate and display the Stock Shortage.

### BA11
Question: (Step 55 is check-only — answered.) Remaining, for a negative test case only: what does a bounced cheque do to the invoice balance?
Answer: There are three types of cheque statuses: / Cleared/Realized: Once the cheque is received and the related deposit slip is posted, the system automatically adjusts the cheque amount against the respective invoice. However, the cheque realization/clearance date may be a future date. / Bounced: If the cheque is not cleared on the expected cheque date, the user can process it through the Bounced Cheque option in Back Office. This screen displays all deposit slips containing cheques against invoices. The user can select the respective cheque and click Bounced to reverse the payment against the invoice. The reversed amount is then created as an outstanding amount at the outlet level. / Note: Based on country-specific business requirements, countries such as Pakistan and Bangladesh prefer to mark the cheque status as Cleared/Realized immediately after the deposit slip is posted.

### Q-OE3
Question: Should editing or cancelling an order on an approved GIN be blocked or warned?
Answer: We need to understand the business requirement for allowing Cash Memo editing before and after the Goods Issue Note (GIN). / In the R1 region, two different functionalities are applicable for Pakistan (PK) and Bangladesh (BD). / For Pakistan, the business allows the Cash Memo to be modified after the GIN has been approved. This functionality is controlled through the CM_Edit parameter, which must be set to Y; otherwise, the functionality remains disabled. / When enabled: / The user can only reduce the order quantity. / The user must provide a reason for the modification. / Upon clicking Save, the system automatically reduces the corresponding stock quantity in the approved GIN, ensuring that the stock-out quantity matches the modified order quantity for delivery.

### BA2
Question: Must the application stop a maker approving his own document (DA, GIN, GRN, SAN, return), or is maker ≠ checker only a QA convention?
Answer: Application Personas and Functional Roles / We need to understand the application personas and their respective functionalities. The application has the following user roles: / Distributor User (0001 – NG User): / This user operates the Back Office application and is responsible for creating and submitting transactions and setup changes for further approval. In the R1 region, a two-level approval workflow is configured for transactions and setup screens. The 0001 – NG User role has the Authorized flag set to N in the Profile screen. / TSSM (0002 – Authorizer): / This role is assigned to users who are authorized to review and approve transactions and setup changes submitted by the Distributor User. / DSR/PJP (0003 – Mobile User): / This role is assigned to DSR/PJP users who operate the Mobile Application. The Authorized flag is set to N. / Warehouse User (0004 – Warehouse User): / This role is responsible for warehouse-related activities through the Mobile Application, including Dispatch Advice, Inventory Management, verification, Goods Issue Note (GIN), Goods Return Note (GRN), and Inventory Audit at the warehouse premises. The Authorized flag is set to N. / Head Quarter (9999 – Global): / This role is primarily used for setup screens and activities that do not require an approval workflow. / Approval Workflow / As part of the application design, setup and transaction activities are controlled through an approval workflow to minimize errors and ensure proper authorization. / Each setup and transaction has a predefined workflow diagram configured in the application. The workflow defines the sequence of activities and specifies the applicable role codes for the Submit and Approval stages. / The HQ (9999 – Global) role is bypassed from the standard approval workflow where approval is not required.

### Q-DS3
Question: Settlement Save posts all slips (answered). But route 02112 for 1 Oct shows Complete while its slips 1131–1136 are still Un Posted (memos 2004, 2005 open). How was 1 Oct closed, and should those receivables stay open?
Answer: This should not be possible. Once the route is settled, all associated deposit slips must be posted, and their amounts must be adjusted against the respective invoices/cash memos. If this does not happen, it should be considered a defect.

### Q48
Question: If cash Received is entered below Payable at settlement, is the difference a cash shortage on the DSR?
Answer: Yes, if there is any difference between the payable amount and the received amount, the difference must be reflected in the DSR Cash Shortage.

### Q-SV1
Question: May framework stock steps (9, 24, 50, 60) be changed to before/after differences instead of fixed values?
Answer: Yes, we execute daily operational transactions as part of smoke testing to ensure the application is stable and to identify any major issues before releasing to the client. / The activities include Dispatch Advice, creating/editing/cancelling Cash Memos, generating Goods Issue Notes (GIN), delivering Cash Memos, and generating Goods Return Notes (GRN) to verify that stock and transactions are correctly processed and transmitted. / These smoke testing activities are performed daily and, when required, multiple times a day to ensure release readiness and minimize the risk of major issues.

### Q-GRN1
Question: When GRN Actual < Suggested, where does the difference go?
Answer: Yes, if a Goods Return is processed and there is a difference between the suggested quantity in UOM and the actual returned quantity, the difference will be considered a DSR Stock Shortage. / Upon approval of the Goods Return, the system automatically creates the DSR adjustment amount, which is then displayed on the Route Settlement screen.

### Q-GRN2
Question: Does a return booked as Damaged/Expired/Lost come back on the GRN with that stock type?
Answer: Yes, the system provides an option to process Sales Returns with reference to an old Cash Memo. The return can be processed for all stock types, including Sound, Damaged, and Expired stock.

### Q16 / Q27
Question: Order quantity above ATP: blocked, warned or accepted? How does allocation behave on short stock?
Answer: In Region 1, both countries have a stock allocation feature that is applied during Order, Cash Memo, or Invoice creation. / The stock allocation logic works as follows: / The system checks the booked order quantity against the available stock. / If the order quantity is less than or equal to the available stock, the required quantity is allocated. / If the order quantity is greater than the available stock, the system allocates the available stock quantity only. / If no stock is available, the order remains unallocated and the Cash Memo status is marked as Order.

### Q29
Question: Does Delivery Date Change refuse a past date?
Answer: Yes, cash memo / invoice delivery date can’t be less then order creation date.

### Q-SR2
Question: Is it intended that a part return re-prices promotions, so lines not returned get discount/tax reversals?
Answer: Sales Return and Fresh Return / The behavior of Sales Return and Fresh Return is as follows: / Sales Return: / A Sales Return is generated against a previously dated invoice. The invoice contains products with different stock types, such as Sound, Damaged, and Expired. Normally, the returned quantity is processed based on the product's sale price × returned quantity in UOM, along with the applicable discount (amount-based or free-product scheme) and tax defined in the Batch Setup. / The system allows the user to return either a single product or the complete invoice. / For a partial return, where not all invoice products or quantities are returned, the system generates a middle invoice/cash memo to calculate the difference between the original invoice quantity and the returned quantity. The system then recalculates the applicable price, discount/scheme, and tax based on the remaining quantity. The difference between the original invoice and the middle invoice is reflected in the Sales Return document. / Fresh Return: / The same calculation and processing logic applies to the Fresh Return. The only difference is that the Fresh Return uses the current document date, whereas a Sales Return is generated against a previously dated invoice.

### Q58
Question: Does a SAN reduce stock at Forward or at approval?
Answer: Yes on document approval action will be impacted on stock either add or deduct

### Q53
Question: Is a DSR adjustment auto-authorized?
Answer: There is no workflow on dsr adjustment document.
