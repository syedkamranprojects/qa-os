# Case-data samples profile

- NG_Dcode_QA_OTC (Bangla).xlsx: 149 sheets, 230 data rows
- NG_Dcode_QA_OTC (PHP).xlsx: 221 sheets, 332 data rows
- NG_Dcode_QA_OTC (Pak).xlsx: 183 sheets, 353 data rows
- NG_Dcode_QA_OTC (Vietnam).xlsx: 206 sheets, 308 data rows
- NG_Dcode_QA_OTC.xlsx: 165 sheets, 234 data rows

## Control columns (sheets using them, of 924)
- PK: 907 sheets; values: '01'×566, '01-01'×268, '01-02'×85, '06'×53, '01-03'×38, '01-04'×33, '02'×30, '02-01'×26
- PK_DESC: 538 sheets; values: '0001 - Value Added Tax Positive 01'×28, 'DEPOSIT Slip Positive'×18, 'OB Positive 01-01'×16, 'Deposit Slip Save Positive'×16, 'Tax Amount Validation from Header Positive 01'×13, 'OTC Stock Out'×12, 'DA Positive Case 01'×11, 'Transaction Inquiry Val After Order Editing Total Offering P'×11
- STPONERR: 666 sheets; values: 'N'×1151
- CASE_TYPE: 528 sheets; values: 'TN'×765, 'TP'×4
- EXPECTED_INPUT: 44 sheets; values: 
- EXPECTED_MESSAGE: 566 sheets; values: 'Saved successfully'×65, 'Forwarded successfully'×61, 'Order Save successfully'×42, 'Record Saved Successfully!'×40, 'Process completed successfully'×19, 'Validation successfully'×10, 'Save successfully'×10, 'Success'×10
- CHECK_VALIDATION: 255 sheets; values: 'Y'×592, 'N'×23
- EVENT_ID: 0 sheets; values: 
- SWIPE: 0 sheets; values: 
- per-field variants (<col>_CASE_TYPE etc.): {}

## Field header style: {'caption/other': 2387, 'UPPER_SNAKE': 233, 'lower_snake': 70}
## Field value kinds (all cells): {'text': 2352, 'digits': 1277, 'number': 351, 'code-desc': 295, 'text-date yyyy-mm-dd': 257, 'code': 169, 'empty': 82, 'text-date dd-mm-yyyy': 74}
## Date formats: {'text-date yyyy-mm-dd': 257, 'text-date dd-mm-yyyy': 74}
## Fields holding "code - description" values (first 15): ['stock arrival', 'stock type', 'auto', 'so number', 'pjp', 'section', 'outlet name', 'document date from', 'document date to', 'order date', 'pjp number', 'end date', 'distributors', 'delivery man pjp', 'delivery man dsr']

## PK parent -> child links (first 25 of 7674)
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Dispatch Advice II
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Dispatch_Advice_Detail2_ASSR
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Dispatch Advice II Grid
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Dispatch Advice II Approval
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Dispatch Advice Approval
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Order Booking_BD
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Transaction InquiryVal AfterOB
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Order Booking Detail2_BD(3)
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Stock Allocation_BD
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Stock Unallocation_BD
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Order Editing_BD
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Order Cancellation_BD
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Delivery Date Change_BD
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> DELIVERYDATE_CHNG_ASSR
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> DA_FORWARD_ASSR
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> DA_APPROVALFRWD_ASSR
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Approval Screen
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Dispatch Advice Loss Approval
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> DA_LOSS_APPROVALFRWD_ASSR
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Goods Issue Note
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Goods Issue Note CM Selection
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Goods Issue Note Forward
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> GIN_FORWARD_ASSR
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> Goods Issue Note Approval
- NG_Dcode_QA_OTC (Bangla).xlsx: Order Booking_BD (2) -> GIN_APPROVAL_SAVE_ASSR

## Sheets not matching any psc_screenname (82): ['Dispatch_Advice_Detail2_ASSR', 'Order Booking_BD (2)', 'Order Booking Detail_BD(3)', 'Transaction InquiryVal AfterOB', 'Trans InquiryVal AfterOB Detail', 'Trans_InquiryVal_AfterOB_Det2', 'Trans_InquiryVal_AfterOB_Header', 'Order Booking Detail2_BD(3)', 'Order Editing Detail2_BD (2)', 'Order_Booking_Detail_BD_ASSR', 'Order Booking Detail2 (2)', 'ORD_EDIT_VALD_ASSR', 'Order_Editing_Detail_BD_ASSR', 'DELIVERYDATE_CHNG_ASSR', 'DA_FORWARD_ASSR', 'DA_APPROVALFRWD_ASSR', 'DA_LOSS_APPROVALFRWD_ASSR', 'GIN_DTL_SAVE_ASSR', 'GIN_FORWARD_ASSR', 'GIN_APPROVAL_SAVE_ASSR', 'FRESH_SALES_RETURN_ASSR', 'FRESH_SALES_RETURN_Full_ASSR', 'Sales Return2', 'Sales_Retur', 'Sales Return Detail3', 'SaleRetDTL_Valid_ASSR', 'SaleRetDTL_SAVE_ASSR', 'SR_StatsChang_DTL_SAVE_ASSR', 'SaleRetrunView_ASSR', 'SaleRetrunViewApprval_ASSR', 'GRN_DTL_SAVE_ASSR', 'GRN_FORWARD_ASSR', 'GRN_APPROVAL_ASSR', 'DEPOSIT_SAVE_ASSR', 'GLOBAL-REPO', 'DEPOSIT_DTL_SAVE_ASSR', 'DEPOSITSLIP_FWD_ASSR', 'Cheque_Status_ASSR', 'ORD_STATUS_SAVE_ASSR', 'Unallocated_ASSR']
