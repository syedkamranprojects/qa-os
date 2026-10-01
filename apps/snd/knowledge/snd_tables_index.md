# S&D table index

Generated from `DD-S&D Entity Model - Data Dictionary 24 June 2026.xlsx` by `dd_build.py` — do not edit by hand.
548 tables, 10808 columns. Full column detail: `snd_tables.json`.

## Banner Module

| Table | Cols | Description |
|---|---|---|
| `BNR_BR_BNH_BANNER_HEADER` | 16 | Banner Header Table - Banner Module |
| `BNR_BR_BNT_BANNER_TYPE` | 13 | Banner Type Table - Banner Module |
| `BNR_BR_CEB_CLKBL_BNR_ENT_TYP` | 13 | Clickable Banner Entity Type Table - Banner Module |
| `BNR_BR_CEC_CLKBL_ENT_CODE_MP` | 12 | Clickable Banner Entity Code Mapping Table - Banner Module |
| `BNR_BR_LBM_LINK_BANNER_MAP` | 16 | Link + Banner Mapping Table - Banner Module |
| `BNR_BR_LIH_LINK_HEADER` | 11 | Link Header Table - Banner Module |
| `BNR_BR_LIV_LINK_VALUES` | 12 | Link Values Table - Banner Module |
| `BNR_BR_LNS_LINK_SCREEN_MAPP` | 7 | Link + Screen Mapping Table - Banner Module |
| `BNR_BR_LNT_LINK_TYPE` | 17 | Link Type Table - Banner Module |

## Fact Table

| Table | Cols | Description |
|---|---|---|
| `FACT_KRD_KPIRESULTANTDATA` | 20 | KPI Resultant Data Table - Fact Table |

## Finance Tables

| Table | Cols | Description |
|---|---|---|
| `FIN_LG_NLG_NOTIF_LOG` | 9 | Notification Log Table - Financial Module |
| `FIN_PR_GLM_GUARDRAIL_LIMIT` | 17 | GuardRail Limit Setup Table - Financial Module |
| `FIN_PR_NAS_NOTIF_ACTIVITY` | 14 | Notification Activity Table - Financial Module |
| `FIN_PR_NCO_NOTIF_CONFIG` | 14 | Notification Configuration Table - Financial Module |
| `FIN_PR_NDD_NOTIF_DUEDIARY` | 15 | Notification Due Diary Table - Financial Module |
| `FIN_PR_NER_NOTIF_EMAILRECP` | 11 | Notification Email Recepient Table - Financial Module |
| `FIN_PR_RCOA_ACCOUNT_SETUP` | 46 | Chart of Account Setup Table - Financial Module |
| `FIN_PR_RCOA_ACTIVITYCONTROL` | 42 | RCOA Activity Control Table - Financial Module |
| `FIN_PR_RCOA_REPORT` | 14 | Reporting Chart of Account Transactional Table - Financial Module |
| `FIN_PR_RCOA_REP_LAYOUT` | 13 | Reporting Layout Setup Table - Financial Module |
| `FIN_PR_RCOA_TYPE` | 13 | Chart of Account Type Table - Financial Module |
| `FIN_PR_RCOA_UOM` | 13 | Unit of Measurement Table - Finacial Module |
| `FIN_PR_RSC_RCOA_SOURCECOMB_MAP` | 11 | RCOA Source Combination Mapping Table - Financial Module |
| `FIN_PR_VEL_VALID_EXCEPTION_LOG` | — | Validation Exception Log Table - Financial Module |
| `FIN_PR_VLD_VALIDATION_STP_DTL` | 23 | Validation Setup Detail Table - Financial Module |
| `FIN_PR_VLH_VALIDATION_STP_HD` | 10 | Validation Setup Header Table - Financial Module |
| `FIN_TR_RCOA_QUERYDATA_INSERT` | 15 | RCOA Query Data Insert Table - Financial Module |
| `FIN_TR_RCOA_REP_TRANSACTION` | — | RCOA Transaction Reporting Repository Table - Financial Module |
| `FIN_TR_RCOA_TRANSACTIONS` | 52 | RCOA Transaction Repository Table - Financial Module |
| `FIN_TR_RCOA_TRANSACTIONS_FILE` | 40 | RCOA Transaction from File Input Table - Financial Module |
| `FIN_TR_RCOA_TRANSACTIONS_INPUT` | 64 | RCOA Transaction from Manual Input Table - Financial Module |
| `FIN_TR_RCOA_TRANSACTIONS_INTG` | 35 | RCOA Transaction from DMS Integration Table - Financial Module |
| `FIN_TR_RCOA_TRANS_EXCEPTION` | 66 | RCOA Transaction Exception Table - Financial Module |
| `FN_RCOA_DATA_INPUT` | 22 | RCOA Data Input - Finance Tables |

## General Parameters

| Table | Cols | Description |
|---|---|---|
| `GLB_LG_PTL_PAYMENT_TRANS_LOG` | 21 | Payment Gateway Transaction Logging Table - General Parameters |
| `GLB_NG_ENT_ENTITY` | 6 | Entity Setup Table - General Parameters (Number Generation Module) |
| `GLB_NG_NGC_NUMBRGENRATION_CNFG` | 11 | Number Generation Configuration Table - General Parameters (Number Generation Module) |
| `GLB_NG_NGM_NUMBRGENRATION_MAPP` | 8 | Number Generation + Organization Mapping Table - General Parameters (Number Generation Module) |
| `GLB_NG_NGN_NUMBERGENERATION` | 5 | Number Generation Setup Table - General Parameters (Number Generation Module) |
| `GLB_NG_RNG_REFERENCENUMBERGEN` | 7 | Referenced Number Generation Table - General Parameters (Number Generation Module) |
| `GLB_PR_AAN_AGE_ANALYSIS` | 20 | Aging Analysis Table for Reporting Purpose - General Parameters |
| `GLB_PR_ADT_ADDRESSTYPE` | 13 | Address Type Setup Table - (General Parameters). i.e. Home Address, Office Address, Rental Address etc. |
| `GLB_PR_AEE_ALLOW_ENTTOENTITY` | 24 | Entity To Entity Allowable Table - General Parameters |
| `GLB_PR_AFP_AFFILIATE_PROGRAM` | 12 | Affliate Program Setup Table - General Parameters This table will use for defining the Affiliated Programs/Apps. i.e. SAVYOUR and ABHI Pay etc. These Affiliated Programs are those Programs/Applications in which Our Applications (Tokrie, Rasayee etc) will be referred through a Link. Upon click on this Link, our application will be opened. In this way these affiliated programs will also get the payment as a commission. |
| `GLB_PR_ANC_ANLS_CLASIFY` | 18 | Analysis Classification Table - General Paramters |
| `GLB_PR_ANT_ANLS_TYPE` | 14 | Analysis Type Table - General Parameters |
| `GLB_PR_APV_APP_VERSIONING` | 12 | Application Versioning Table - General Parameters |
| `GLB_PR_BEM_BUSENTITY_MISTYPE` | 17 | MIS Type Setup Of Business Entities Table - (General Parameters) MIS Types of Outlet, Distributor, Warehouse etc. In case of Outlet, Retail, Wholsale, Departmental Store, Modern Trade, Institutions, Hospitals etc. In case of Distributor, Corporate, Individual, Call Center, HPC etc. In case of Warehouse, Auto and Manual etc. |
| `GLB_PR_BEO_BUSENTITY_ORGRANK` | 12 | Organizational Ranking Setup Of Business Entities Table - (General Parameters) |
| `GLB_PR_BER_BUSENTITY_RANKING` | 12 | Ranking Setup Of Business Entities Table - (General Parameters) |
| `GLB_PR_BET_BUSENTITY_TYPE` | 13 | Business Entities Type Setup Table - (General Parameters) Distributor = DIST, Outlet = OUTL, Warehouse = WRHS, Product = PROD, DSRS = DSRS, Courier = COUR etc. |
| `GLB_PR_BNB_BANKBRANCH` | 13 | Bank Branch Setup Table - (General Parameters). |
| `GLB_PR_BNK_BANK` | 13 | Bank Setup Table - (General Parameters). |
| `GLB_PR_BRK_BRICK_SETUP` | 12 | Brick Setup Table - General Parameters This is kind of a Grouping. i.e. Karachi East, Karachi West, Karachi North and Karachi South etc. |
| `GLB_PR_BRM_BUSINESS_REPO_MAP` | 12 | Business Function + Repository Mapping Table - General Parameters |
| `GLB_PR_BST_BUSINESSTYPE` | 12 | Business Type Setup Table - (General Parameters). i.e. Coporation, Partnership, Sole Proprietorship etc. |
| `GLB_PR_CCY_CTRYCTY` | 12 | Country/City Setup Table - (General Parameters). |
| `GLB_PR_CHD_CHARGES_SETUP_DTL` | 12 | Charges Setup Detail Table - General Parameters Tax Charges on Outlet, Delivery Charges on DSR etc. |
| `GLB_PR_CHO_COMPANYHOLIDAYS` | 9 | Company Holidays Setup Table - General Parameters |
| `GLB_PR_CHS_CHARGES_SETUP` | 14 | Charges Setup Table - General Parameters Tax Charges, Delivery Charges etc. |
| `GLB_PR_CLS_CALENDAR_SETUP` | 17 | Calendar Setup Table - General Parameters |
| `GLB_PR_CLT_CALENDAR_TYPE_STP` | 20 | Calendar Type Setup Table - General Parameters |
| `GLB_PR_CMS_CASHMEMO_SUB_TYPE` | 14 | Cash Memo Sub Type Table - General Parameters |
| `GLB_PR_CMT_CASHMEMO_TYPE` | 13 | Cashmemo Type Table - General Parameters |
| `GLB_PR_COT_CONTACTTYPE` | 12 | Contact Type Setup Table - (General Parameters). i.e. Personal Contact, Business Contact, Organizational Contact, Group Contact etc. |
| `GLB_PR_CRM_CREDITMODE` | 12 | Credit Mode Setup Table - (General Parameters).i.e. Credit, Trade Credit, Consumer Credit, Bank Credit etc. |
| `GLB_PR_CTK_CHANGE_TRACK` | 10 | Change Track Table - General Parameters |
| `GLB_PR_CUR_CURRENCIES` | 18 | Currencies Setup Table - (General Parameters). |
| `GLB_PR_DSG_DESIGNATION` | 12 | Designation Setup Table - (General Parameters). |
| `GLB_PR_DTF_DIST_WISE_FEATURE` | 10 | Distributor Wise Feature Table - General Parameters |
| `GLB_PR_DVT_DEVICETYPE` | 12 | Device Type Setup Table - (General Parameters). i.e. IPEQ, Palmtop, Mobile Device, HHT etc. |
| `GLB_PR_EXP_EXPENSE_SETUP` | 12 | Expenses Setup Table - General Parameters |
| `GLB_PR_EXR_CURR_EXGRATES` | 19 | Currency Exchange Rates Setup Table - (General Parameters). |
| `GLB_PR_EXT_EXGRATETYPE` | 12 | Exchange Rate Type Setup Table - (General Parameters). |
| `GLB_PR_FNE_FINANCIAL_ELEMENT` | 12 | Financial Element Setup Table - (General Parameters). Assets, Liabilities, Revenue, Expense, Equity etc. |
| `GLB_PR_FQY_FREQUENCY` | 13 | Frequency Setup Table - (General Parameters). Daily, Weekly, Fortnighly, Monthly etc. |
| `GLB_PR_FRT_FEATURE_TYPE` | 13 | Feature Type Table - General Parameters |
| `GLB_PR_GCO_GLOBAL_CONFIG_ORG` | 9 | Global Configuration Organization wise Table - General Parameters |
| `GLB_PR_GEC_GENERAL_CONFIG` | 13 | General Configuration Table - General Parameters |
| `GLB_PR_GLC_GLOBALCONFIGURATION` | 12 | Global Configuration Table - General Parameters |
| `GLB_PR_GOS_GLOBAL_ORG_SETUP` | 12 | Global Setup for Organization Table - General Parameters This table will use for storing the Application's Global Values based on organization. |
| `GLB_PR_GRT_GROUP_TYPE_SETUP` | 12 | Group Type Setup Table - General Parameters |
| `GLB_PR_HLS_HIERARCHY_LVL_STP` | 9 | Hierarchy Level Setup Table - General Parameters |
| `GLB_PR_IDN_IDENTIFIERTYPE` | 12 | Identifier Type Setup Table - (General Parameters). CNIC, Passport, Driving License and Social Security Number etc. |
| `GLB_PR_INS_INSTRUMENT_STATUS` | 13 | Instrument Status Table - General Parameters Different Status of Instruments (Cheque, Deposit Slip, Pay Order etc). i.e. Collected, Realized, Bounced and Cancelled etc. |
| `GLB_PR_KRS_KPIRESULTANT_SETP` | 20 | KPI Resultant Setup Table - General Parameters |
| `GLB_PR_LNG_LANGUAGE` | 15 | Language Setup Table - (General Parameters). |
| `GLB_PR_LOC_LOCATION` | 49 | Location (Distributor) Setup Table - (General Parameters). i.e. Pakistan, Egypt etc. Also Distributors can be defined. |
| `GLB_PR_LOL_LOCALITY` | 12 | Town / Locality / Sub Locality Setups Table - (General Parameters). |
| `GLB_PR_LOT_LOCATION_TYPE` | 12 | Location Type Setup Table - (General Parameters). Corporate, Individual, Call Center etc. |
| `GLB_PR_MDF_MBLTY_DYNMC_FILTR` | 18 | Mobility Dynamic Filter Table - (General Parameters). |
| `GLB_PR_MRT_MARITALSTATUS` | 12 | Marital Status Setup Table - (General Parameters). |
| `GLB_PR_MSP_MISC_PARAM` | 14 | Misclenouse Parameters Setup Table - (General Parameters). |
| `GLB_PR_OGL_ORG_GLOBALIZATION` | 13 | Organization Globalization Setup Table - General Parameters |
| `GLB_PR_OPT_OPTION_TYPE` | 11 | Option Type Table - General Parameters |
| `GLB_PR_ORD_ORGADATASETS` | 12 | Organization Wise Data Set for Power BI Table - General Parameters |
| `GLB_PR_ORF_ORGA_WISE_FEATURE` | 8 | Organization Wise Feature Table - General Parameters |
| `GLB_PR_ORG_LNG_LNGORG_MAP` | 8 | Organization + Language Mapping Table - (General Parameters). |
| `GLB_PR_ORG_ORGANIZATION` | 30 | Organization/Company Setup Table - (General Parameters). |
| `GLB_PR_ORP_PRINCIPAL` | 24 | Global Principal Setup Table - (General Parameters). Product Manufacturing Companies. i.e. Unilever, Colgate Palmolive, GSK, Shan Foods etc. |
| `GLB_PR_PCT_PYMNT_CONTRCT_TYP` | 13 | Payment Contract Type Table - General Parameters |
| `GLB_PR_PHS_PLACEHOLDER_SETUP` | 11 | Place Holder Setup Table - (General Parameters). |
| `GLB_PR_PLH_PHS_LVL1_HOLIDAYS` | 15 | Distributor/Physical Level 1 Holidays Setup Table - General Parameters |
| `GLB_PR_PMT_PROGRAM_TYPE` | 12 | Program Type Setup Table - General Parameters |
| `GLB_PR_PPC_PARACONTROL` | 12 | Parameter Control Setup Table - (General Parameters). |
| `GLB_PR_PPL_PARALEVELS` | 11 | Parameter Level Setup Table - (General Parameters). |
| `GLB_PR_PRV_PROVINCE` | 12 | Province Setup Table - (General Parameters). |
| `GLB_PR_PSC_POSTAL_CODE` | 13 | Postal Code Table - General Parameters |
| `GLB_PR_PTP_PERIODTYPE` | 17 | Period Type Setup Table - (General Parameters). Daily, Weekly, Monthly, Quarterly, Half Yearly, Yearly. |
| `GLB_PR_PYM_PAYMENTMODE` | 14 | Payment Mode Setup Table - (General Parameters). Cash, Cheque, Credit Card, Debit Card, Easy Paisa etc. |
| `GLB_PR_QLN_QUALIFICATION` | 12 | Qualification Setup Table - (General Parameters). |
| `GLB_PR_RGN_REGION` | 12 | Region Setup Table - (General Parameters). Southern, Eastern, Western and Northern etc. |
| `GLB_PR_RNT_REASON_TYPE` | 15 | Reason Type Table - General Parameters This Parameter has use for defining the Reasons against Sales Return. i.e. Damage, Expire, No Cash, Rejection, Entry Mistake, Wrong Order, False Booking, Stock Sufficient etc. |
| `GLB_PR_SCH_SCHEME` | 12 | Scheme Parameter Table - General Parameters Discounts, Free Pieces etc. |
| `GLB_PR_SCR_SERVICE_CREDENTLS` | 11 | Service Credentials Table - General Parameters |
| `GLB_PR_SGT_SUGGESTED_TYPES` | 13 | Suggested Types Table - General Parameters Transactions Generation Basis. i.e. In case of GIN generation, Cash Memo List, Cash Memo Summary, Average Histroy, Manual etc. In case of GRN generation, Sales Return List, Sales Return Summary, Manual etc. In case of DA, Auto DA and Manual etc. |
| `GLB_PR_SOF_SALES_OFFICE` | 13 | Sales Office Setup Table - General Parameters |
| `GLB_PR_SRT_SALES_ROUTE_TYPE` | 13 | Sales Route Type Table - General Parameters |
| `GLB_PR_STS_SEGMENT_TYPE` | 13 | Segment Type Table - General Parameters |
| `GLB_PR_TEC_TERMS_CONDITION` | 13 | Terms and Condition Table - General Parameters |
| `GLB_PR_TRS_TRIP_STATUS` | 13 | Trip Status Table - General Parameters |
| `GLB_PR_TRT_TOUR_TYPE` | 13 | Tour Type Table - General Parameters |
| `GLB_PR_TXC_TAX_CLASS` | 13 | Tax Class Table - General Parameters |
| `GLB_PR_TXT_TAX_TYPE` | 15 | Tax Type Table - General Parameters |
| `GLB_PR_UOM_UNITOFMEASURE` | 13 | Unit Of Measurement Setup for Product Table - (General Parameters). Carton, Dozen, Pieces, Liter, Pack etc. |
| `GLB_PR_VCS_VOICE_SETUP` | 13 | Voice Setup Table - (General Parameters). This Table use to define the Messages which are displaying on the Application's screens. For example : "To go the @screenName Please press 'Next' button to proceed.". |
| `GLB_PR_VHT_VEHICLE_TYPE` | 12 | Vehicle Type Table - General Parameters |
| `GLB_PR_VSP_VOICE_SETUP` | 12 | Voice Setup Table (Without Organization) - (General Parameters). |

## Mobility Setups - BackOffice

| Table | Cols | Description |
|---|---|---|
| `MOB_MB_LKN_LSTNR_KYWRD_SCREN` | 6 | Screen Wise Listener Key Word Table - Mobility Setups - BackOffice |
| `MOB_MB_LKS_LISTNR_KEYWRD_STP` | 11 | Listener Key Word Setup Table - Mobility Setups - BackOffice |
| `MOB_MB_MGA_MODLGRP_ASSOCTION` | 12 | Model Group Assoication Table - Mobility Setups - BackOffice |
| `MOB_MB_MMS_MODEL_SETUP` | 11 | Model Setup Table - Mobility Setups - BackOffice |
| `MOB_MB_MSA_SCREEN_ASSOCIATE` | 14 | Screen Association Table - Mobility Setups - BackOffice |
| `MOB_MB_MSS_SCREEN_SETUP` | 12 | Screen Setup Table - Mobility Setups - BackOffice |
| `MOB_MB_MUA_USER_ASSOCIATION` | 12 | User Association Table - Mobility Setups - BackOffice |
| `MOB_MB_MUG_USER_GROUP_SETUP` | 13 | User Group Setup Table - Mobility Setups - BackOffice |
| `MOB_MB_NMU_NAVIGATION_MENU` | 16 | Navigation Menu Table - Mobility Setups - BackOffice |
| `MOB_MB_PEM_PRIN_ENTITY_MAP` | 12 | Principal Wise Entities Mapping to Other Entities Table - Mobility Setups - BackOffice |
| `MOB_MB_PWE_PRIN_WISE_ENTITY` | 15 | Principal Wise Entities Table - Mobility Setups - BackOffice |
| `MOB_MB_SEM_SCREEN_EVENT_MAP` | 7 | Screen and Event Mapping Table - Mobility Setups - BackOffice |
| `MOB_MB_SVM_SCREEN_VOICE_MAP` | 7 | Screen and Voice Setup Mapping Table - Mobility Setups - BackOffice |

## Mobility Setups - SNDMOBILITY

| Table | Cols | Description |
|---|---|---|
| `MOB_MB_IND_INDCTR_DEFINITION` | 12 | Indicator Definition Setup Table - Mobility Setups - SNDMOBILITY |
| `MOB_MB_INS_INDICATOR_SETUP` | 15 | Indicator Setup Table - Mobility Setups - SNDMOBILITY |
| `MOB_MB_MAF_MOBILE_APP_FLOW` | 17 | Applications Flow for Mobile/Device Table - Mobility Setups - SNDMOBILITY |
| `MOB_MB_MRS_MOBILITY_RELEASE` | 9 | Mobility Releases Table - Mobility Setups - SNDMOBILITY |
| `MOB_MB_OUT_NEW_OUTLET_SETUP` | 29 | New Outlet Setup Table - Mobility Setups - SNDMOBILITY |
| `MOB_MB_USG_USER_SETTING` | 7 | User Settings Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_BAC_BUSS_ACTIVITIES` | 13 | Business Activities Setup Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_BEM_BUSACTVTY_LVL2_MP` | 8 | Physical Level 2 and Business Activities Mapping Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_BGT_LVL1_TIME_SLB_MAP` | 9 | Business Entity Level 1 + Global Time Slab Setup Mapping Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_COR_CUST_ORD_RESPONSE` | 11 | Customer Order Response Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_ECL_ENT_CURNT_LATLONG` | 10 | Current Latitude and Longitude of Business Entity Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_GTS_GLOBAL_TIME_SLAB` | 13 | Global Time Slab Setup Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_HRM_HIERARCHIES_MAP` | 11 | Two Hierarchies Mapping Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_OPB_OUTL_PRD_BAR_MAP` | 13 | Outlet + Product BAR Code Mapping Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_OSG_OUTLET_SEGMENTS` | 6 | Outlet + Segments Mapping Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_OSM_OUT_STAFF_MEMBER` | 13 | Outlet Staff Member Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_OUR_OUTLT_REGISTRTION` | 12 | Outlet Registration Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_OWR_OUTLET_WEB_REGIST` | 29 | New Outlet Web Registration Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_PCM_PROG_CMPL_TYP_MAP` | 8 | Program Type + Compliance Config Mapping Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_PID_PROD_IMAGE_DETAIL` | 9 | Product Image Detail Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_PIM_PROD_IMAGE_MASTER` | 17 | Product Image Master Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_PQM_PROG_QUESTION_MAP` | 14 | Program Question Mapping Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_PRT_PROGRAM_TYPE` | 17 | Program Type Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_REV_REVIEW` | 18 | Review/Feedback from Customer into "B To C" Business Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_SEG_SEGMENTS_SETUP` | 12 | Segments Setup Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_TWR_TWOWAY_RECEPTOR` | 12 | Two Way Receptor Table - Mobility Setups - SNDMOBILITY |
| `MOB_PR_URC_UNREG_CUSTOMERS` | 15 | Un-Registered Customers Table - Mobility Setups - SNDMOBILITY |
| `MOB_TR_MNS_MANUAL_SURVEY` | 15 | Manual Survey Setup Table - Mobility Setups - SNDMOBILITY |
| `MOB_TR_SAA_SUR_ANS_ANALYSIS` | 11 | Survey Answer Analysis Table - Mobility Setups - SNDMOBILITY |
| `MOB_TR_SRA_SURVEY_ANSWER` | 30 | Survey Answer Setup Table - Mobility Setups - SNDMOBILITY |
| `MOB_TR_SRV_SURVEY` | 11 | Survey Setup Table - Mobility Setups - SNDMOBILITY |

## Product

| Table | Cols | Description |
|---|---|---|
| `SND_PR_ALW_PRD_POLICY_BSE_RANK` | 9 | Product Policy On Business Entities Ranks Setup Table - (Product). |
| `SND_PR_ALW_PRD_POLICY_BSE_TYPE` | 9 | Product Policy On Business Entities Types Setup Table - (Product). |
| `SND_PR_ALW_PRD_POLICY_GEOHRCHY` | 9 | Product Policy On Geographical Hierarchy Setup Table - (Product). |
| `SND_PR_ALW_PRD_POLICY_LSM` | 9 | Product Policy on Life Style Measurement (LSM) Setup Table - (Product). |
| `SND_PR_ALW_PRD_POLICY_OUTCHNEL` | 9 | Product Policy On Outlet Channel Setup Table - (Product). |
| `SND_PR_ALW_PRD_POLICY_STRATA` | — | Product Policy On Strata Setup Table - (Product). |
| `SND_PR_ASP_ACCOUNT_SALE_PRICE` | 26 | Account Sales Price Table - (Product) |
| `SND_PR_BOM_PROD_BILLOFMATERIAL` | 14 | Bill Of Material (BOM) Setup Table - (Product). |
| `SND_PR_BTH_PROD_BATCH` | 50 | Product Batch Setup Table - (Product). |
| `SND_PR_DPP_DIST_PRCH_PRICE` | 28 | Distributor Purchase Price Structure Table - (Product) |
| `SND_PR_DSP_DIST_SALE_PRICE` | 26 | Distributor Sales Price Structure Table - (Product) |
| `SND_PR_GPP_GLOBAL_PRCH_PRICE` | 32 | Global Purchase Price Structure Table - (Product) |
| `SND_PR_GSP_GLOBAL_SALE_PRICE` | 23 | Global Sales Price Structure Table - (Product) |
| `SND_PR_OSP_OUTLET_SALE_PRICE` | 25 | Outlet Sales Price Structure Table - (Product) |
| `SND_PR_PA1_PROD_ANALYSIS_1` | 19 | Product - Analysis-1 (Axe/SubAxe) Setup Table - (Product). |
| `SND_PR_PA2_PROD_ANALYSIS_2` | 18 | Product - Analysis-2 (Classification) Setup Table - (Product). |
| `SND_PR_PA3_PROD_ANALYSIS_3` | 18 | Product - Analysis-3 (Func/SubFunc) Setup Table - (Product). |
| `SND_PR_PA4_PROD_ANALYSIS_4` | 14 | Product - Analysis-4 Setup Table - (Product). |
| `SND_PR_PA5_PROD_ANALYSIS_5` | 14 | Product - Analysis-5 Setup Table - (Product). |
| `SND_PR_PAB_PROD_ABCCLSFICATION` | 12 | Product ABC Classification Setup Table - (Product). |
| `SND_PR_PED_PROD_EXD_POLCY_DT` | 13 | Product Excluding Policy Detail Table - (Product) |
| `SND_PR_PEH_PROD_EXD_POLCY_HD` | 14 | Product Excluding Policy Header Table - (Product) |
| `SND_PR_PLV_PROD_LOCALVALIDITY` | 13 | Product Local Validity Setup Table - (Product). |
| `SND_PR_PR1_PROD_PRCESTR_LVL1` | 13 | Product Price Structure Table for Distributor Level Prices. (Product) |
| `SND_PR_PRC_PROD_PRICESTR_CMB` | 35 | Product Price Structure Combination Table - (Product). |
| `SND_PR_PRD_PRODUCT` | 70 | Product Setup Table - (Product). |
| `SND_PR_PRF_PROD_PRCESTR_SDTL` | 13 | Product Price Structure Sub Detail Table - (Product) |
| `SND_PR_PRH_PROD_POLICY_HD` | 13 | Product Policy Header Table - (Product) |
| `SND_PR_PRM_MOB_PRICES` | 25 | Mobility Prices Table - (Product). |
| `SND_PR_PRM_PRODUCT_MORPHING` | 10 | Product Morphing Table - (Product) |
| `SND_PR_PRM_PRODUCT_REF_MAPP` | 11 | Product+Reference Type Mapping Table - (Product) |
| `SND_PR_PRO_PROD_POLICY` | — | Product Policy Setup Table - (Product). |
| `SND_PR_PRS_PROD_PRICESTRUCTURE` | 14 | Product Price Structure Header Table - (Product). |
| `SND_PR_PRS_SUBSTITUTION_MAP` | 12 | Substitute Product Mapping Table - (Product) |
| `SND_PR_PSD_PROD_PRICESTR_DTL` | 17 | Product Price Structure Table for Different Levels Prices based on Field/Value Combination. (Product) |
| `SND_PR_PTY_PROD_TYPE` | 14 | Product Type Setup Table - (Product). |
| `SND_PR_RET_REFERENCE_TYPE` | 9 | Reference Type Table - (Product) |
| `SND_PR_SPG_PROD_SUGPRDGP` | 14 | Suggested Product Group Detail Table for "B To C Business" - (Product). |
| `SND_PR_SPH_PROD_SUGPRDHR` | 12 | Suggested Product Group Header Table for "B To C Business" - (Product). |
| `SND_PR_UOM_PROD_UNITOFMEASURE` | 20 | Product Unit of Measurement Setup Table - (Product). |
| `SND_PR_UOM_PROD_UOMDETAIL` | 13 | Product Unit of Measurement Detail Table - (Product). |
| `SND_PR_UOM_PROD_UOMHEADER` | 15 | Product Unit of Measurement Header Table - (Product). |

## Promotion Module

| Table | Cols | Description |
|---|---|---|
| `PRM_PM_ACP_ACCES_CNTRL_PROM` | 8 | Access Control of Promotion Table - Promotion Module |
| `PRM_PM_CGM_CSTMTG_GRPTYP_MAP` | 12 | Custom Tag and Group Type Mapping Table - Promotion Module |
| `PRM_PM_DDT_DH_DATA_TYPE` | 15 | Data Type for Data Holder Table - Promotion Module |
| `PRM_PM_DFT_DH_FUNCTION_TYPE` | 11 | Function Type for Data Holder Table - Promotion Module |
| `PRM_PM_DHR_DATA_HOLDER` | 43 | Data Holder Table - Promotion Module |
| `PRM_PM_DQP_DISQUALIFIED_PROM` | 11 | Disqualified Promotion Table - Promotion Module |
| `PRM_PM_ERC_ENT_REDMPTION_CAP` | 12 | Entity Redemption Cap Table - Promotion Module |
| `PRM_PM_GRM_GRPTYP_REPO_MAP` | 11 | Group Type and Repository Mapping Table - Promotion Module |
| `PRM_PM_GTS_GROUPTYPE_SETUP` | 11 | Group Type Table - Promotion Module |
| `PRM_PM_LUT_LAST_UPLOAD_TIME` | 2 | Promotion Last Upload Time - Promotion Module |
| `PRM_PM_MDC_MAX_DT_CHARGES` | 10 | Maximum Distributor Charges Table - Promotion Module |
| `PRM_PM_PAL_PROM_ALLOCATION` | 20 | Promotion Allocation Table - Promotion Module |
| `PRM_PM_PAR_PROM_ALLOCATN_REF` | 20 | Promotion Allocation Reference Table - Promotion Module |
| `PRM_PM_PAT_PROM_ALLOW_TAGS` | 10 | Promotion Allowable Tags Table - Promotion Module |
| `PRM_PM_PCE_PROM_CACHE_EVENT` | 9 | Promotion Cache Event Log Table - Promotion Module |
| `PRM_PM_PEA_PROM_ENTITY_ATRBT` | 9 | Promotion Entity Attributes Table - Promotion Module |
| `PRM_PM_PED_PROM_ENT_GRP_DTL` | 11 | Promotion Entity Group Detail Table - Promotion Module |
| `PRM_PM_PEE_PROM_ELGBL_ENTITY` | 10 | Promotion Eligible Entities Table - Promotion Module |
| `PRM_PM_PEG_PROM_ENTITY_GROUP` | 11 | Promotion Entity Group Table - Promotion Module |
| `PRM_PM_PEH_PROM_ELGBL_HEADER` | 19 | Promotion Eligible Header Table - Promotion Module |
| `PRM_PM_PEL_PROM_ENTITY_ELMNT` | 8 | Promotion Entity Elements Table - Promotion Module |
| `PRM_PM_PEP_PROM_ELGBL_PROD` | 12 | Promotion Eligible Products Table - Promotion Module |
| `PRM_PM_PEV_PROMO_EVT_LOG` | 17 | Promotion Event Logging Table - Promotion Module |
| `PRM_PM_PMS_PROMOTION_SETUP` | 52 | Promotion Setup Table - Promotion Module |
| `PRM_PM_PMT_PROMOTION_TYPE` | 12 | Promotion Type Table - Promotion Module |
| `PRM_PM_PRM_PROM_MECHANICS` | 9 | Promotion Mechanics Table - Promotion Module |
| `PRM_PM_PRT_PROM_RESULTNT_TYP` | 11 | Promotion Resultant Type Table - Promotion Module |
| `PRM_PM_PSC_PROMOTION_SECTYPE` | 15 | Promotion Sec Type - Promotion Module |
| `PRM_PM_PSG_PROM_SUBTYPE_GRP` | — | Promotion Sub Type Group Table - Promotion Module |
| `PRM_PM_PSL_PROMOTION_SLABS` | 16 | Promotion Slabs Table - Promotion Module |
| `PRM_PM_PST_PROMOTION_SUBTYPE` | 12 | Promotion Sub Type Table - Promotion Module |
| `PRM_PM_PTG_PROM_TYPE_GROUP` | 14 | Promotion Type Group Table - Promotion Module |
| `PRM_PM_PVS_PROM_VOUCHER_STP` | 36 | Promotion Voucher Setup Table - Promotion Module |
| `PRM_PM_SDC_STAGING_DT_CHARGS` | 19 | Distributor Charges on Staging Table - Promotion Module |
| `PRM_PM_SPD_STAGING_TABLE_DTL` | 15 | Stagging Detail Table - Promotion Module |
| `PRM_PM_STD_STAGING_TABLE_DT` | 26 | Promotion Staging for DT Table - Promotion Module |
| `PRM_PM_STH_STAGING_TABLE_HQ` | 22 | Promotion Staging for HQ Table - Promotion Module |
| `PRM_PM_TPE_TMP_PROM_ENRCHMNT` | 11 | Temp Promotion Enrichment Table - Promotion Module |
| `PRM_PM_TSA_TMP_SCHM_ALLOWABL` | 13 | Temporary Scheme Allowable Table - Promotion Module |
| `PRM_PM_TSG_TEMP_SCHEME_GROUP` | 18 | Temporary Scheme Group Table - Promotion Module |
| `PRM_PM_TSH_TEMP_SCHEME_HEAD` | 36 | Temporary Scheme Header Table - Promotion Module |
| `PRM_PM_TSQ_TMP_SCHEM_QUALIFY` | 17 | Temporary Scheme Qualify Table - Promotion Module |
| `PRM_PM_TSR_TMP_SCHM_RESULTNT` | 23 | Temporary Scheme Resultant Table - Promotion Module |
| `PRM_PM_TSS_TEMP_SCHEME_SLAB` | 30 | Temporary Scheme Slab Table - Promotion Module |
| `PRM_PM_VHT_VOUCHER_TYPE` | 11 | Voucher Type Table - Promotion Module |

## S&D Specific Parameters

| Table | Cols | Description |
|---|---|---|
| `SND_PR_CFR_CASHMEMO_FILE_REF` | 13 | Cash Memo File Reference Table - S&D Specific Parameters |
| `SND_PR_CHH_CHANEL_HIERARCHY` | 27 | Channel Hierarchy Setup Table - (S&D Specific Parameters). |
| `SND_PR_COC_CORD_COMPLIANCE` | 15 | Coordinate Compliance Setup Table - (S&D Specific Parameters). |
| `SND_PR_CPS_CLAIM_PERIOD_STP` | 12 | Claim Period Setup Table - S&D Specific Parameters |
| `SND_PR_DCS_DOC_CMPLTN_STATUS` | 13 | Document Completion Status Table - S&D Specific Parameters |
| `SND_PR_DFM_DOC_FILE_MAPPING` | 9 | Document File Mapping Table - S&D Specific Parameters |
| `SND_PR_DLM_DELIVERY_MODE` | 15 | Delivery Mode Setup Table - (S&D Specific Parameters). |
| `SND_PR_DOS_DOCUMENTSTATUS` | 17 | Document Status Setup Table - (S&D Specific Parameters). |
| `SND_PR_DOT_DOCUMENTTYPE` | 23 | Document Type Setup Table - (S&D Specific Parameters). |
| `SND_PR_DST_DSRTYPE` | 18 | DSR Type Setup Table - (S&D Specific Parameters). |
| `SND_PR_FET_FINANCE_ENTITY` | 12 | Finance Entity Setup Table - (S&D Specific Parameters). |
| `SND_PR_GEO_GEOG_HIERARCHY` | 12 | Geographical Hierarchy Setup Table - (S&D Specific Parameters). |
| `SND_PR_LSM_LIFESTYLEMEASURMENT` | 12 | Life Style Measurment Setup Table - (S&D Specific Parameters). |
| `SND_PR_MSM_MISTYPE_STKTYPE_MP` | 7 | Business MIS Type and Stock Type Mapping Table - S&D Specific Parameters Purpose of table: Expected (to be done): User should be unable to move sound stock from main warehouse to damage warehouse and damage stock from damage warehouse to main warehouse. Currently Happening: User is able to move "Sound" stock to "Damage" warehouse from main warehouse and "Damage" stock to "Main" warehouse from damage warehouse using Stock Adjustment functionality |
| `SND_PR_OCP_ORG_CLM_PRIOD_STP` | 10 | Organization Based Claim Period Setup Table - S&D Specific Parameters |
| `SND_PR_PRT_PRICETYPE` | 13 | Price Type Setup Table - (S&D Specific Parameters). |
| `SND_PR_PSD_PRE_ORD_STOCK_DTL` | 27 | Pre Order Stock Detail Table - S&D Specific Parameters These tables will use for allocating the tentative stock to the Outlets based on any Parameter. i.e. Outlet MIS Type, Channel Hierarchy. |
| `SND_PR_PSH_PRE_ORD_STOCK_HDR` | 13 | Pre Order Stock Header Table - S&D Specific Parameters These tables will use for allocating the tentative stock to the Outlets based on any Parameter. i.e. Outlet MIS Type, Channel Hierarchy. |
| `SND_PR_SDT_SUB_DOCUMENTTYPE` | 16 | Sub Document Type Table - S&D Specific Parameters |
| `SND_PR_SLH_SALES_HIERARCHY` | 19 | Sales Hierarchy Setup Table - (S&D Specific Parameters). |
| `SND_PR_STR_STRATA` | 14 | Strata Setup Table - (S&D Specific Parameters). |
| `SND_PR_STT_SKU_STOCKTYPE` | 16 | Stock Type Setup Table - (S&D Specific Parameters). |
| `SND_PR_TCM_TRANSPORT_COMP` | 12 | Transport Company Setup Table - (S&D Specific Parameters). |
| `SND_PR_TMD_TRANSPORT_MODE` | 12 | Tranport Mode Setup Table - (S&D Specific Parameters). |
| `SND_PR_TRD_TRANSPORTER_DTL` | 17 | Transporter Detail Table - S&D Specific Parameters |
| `SND_PR_TRN_TRANS_NATURE` | 18 | Transaction Nature Setup Table - (S&D Specific Parameters). |
| `SND_PR_VCH_VEHICLE` | 63 | Vehicle Setup Table - (S&D Specific Parameters). |
| `SND_PR_VHC_VEHICLE_COLOR` | 12 | Vehicle Color Setup Table - (S&D Specific Parameters). |
| `SND_PR_VHM_VEHICLE_MAKE` | 12 | Vehicle Make Setup Table - (S&D Specific Parameters). |
| `SND_PR_VND_VENDOR` | 21 | Vendor Setup Table - (S&D Specific Parameters). |
| `SND_PR_VST_VISIT_STATUS` | 22 | Visit Status Type Setup Table - (S&D Specific Parameters). |

## S&D-EN - Entity Model

| Table | Cols | Description |
|---|---|---|
| `SND_EN_AL1_ALW_LOG_LVL1_PRD` | 11 | Allowed Products into Logical Business Entity Level 1 (Selling Category) Setup Table - (S&D - Entity Model). (Selling Category Wise Products) |
| `SND_EN_ALL_ALW_LOG_LOG_LVL1` | 10 | Allowing Logical Business Entities Level 1 (Selling Category, Section etc) To Logical Business Entities Level 1 (Selling Category, Section etc) Setup Table - (S&D - Entity Model). (Selling Category wise Section) |
| `SND_EN_ALP_ALW_LOG_PHS_LVL1` | 11 | Allowing Physical Business Entities Level 1 (Distributor, Outlet, Warehouse etc) To Logical Business Entities Level 1 (Selling Category, Section etc) Setup Table - (S&D - Entity Model). (Section POP Permanent) |
| `SND_EN_AP1_ALW_PHS_PHS_LVL1` | 10 | Allowed Physical Business Entities Level 1 (Distributor, Outlet, Warehouse etc) To Physical Business Entity Level 1 (Distributor, Outlet, Warehouse etc) Setup Table - (S&D - Entity Model). (Distributor wise Outlet, Warehouse etc) |
| `SND_EN_AP2_ALW_PHS_PHS_LVL2` | 10 | Allowed Physical Business Entities Level 2 (DSR, Courier Service etc) To Physical Business Entities Level 1 (Distributor, Outlet, Warehouse etc) Setup Table - (S&D - Entity Model). (Distributor wise DSR, Courier Service etc) |
| `SND_EN_APL_ALW_PHS_LOG_LVL1` | 10 | Allowed Logical Business Entities Level 1 (Selling Category, Section etc) To Physical Business Entities Level 1 (Distributor, Outlet, Warehouse etc) Setup Table - (S&D - Entity Model). (Distributor wise Selling Category, Section etc) |
| `SND_EN_APP_ALW_PHS_LVL1_PRD` | 10 | Allowed Products into Physical Business Entity Level 1 (Distributor) Setup Table - (S&D - Entity Model). (Distributor wise Products) |
| `SND_EN_AUR_ALLOWED_URI` | 7 | Allowed URI Table - (S&D - Entity Model). |
| `SND_EN_DCB_DST_CHNL_BKBR_MAP` | 10 | Distributor + Bank Branch + Channel Hierarchy Mapping Table - (S&D - Entity Model). |
| `SND_EN_DCP_DT_COMPETITOR_PROM` | 14 | Distributor Competitor and Promotion Types Table - (S&D - Entity Model). |
| `SND_EN_DFL_DSR_FILE_LOG` | 14 | DSR File Log Table - (S&D - Entity Model). |
| `SND_EN_DFS_DSR_FILE_STATUS` | 8 | DSR File Status Table - (S&D - Entity Model). |
| `SND_EN_DGD_DISTRIBUTOR_GRP_DT` | 9 | Distributor Group Detail Table - (S&D - Entity Model). |
| `SND_EN_DGH_DISTRIBUTOR_GRP_HD` | 11 | Distributor Group Header Table - (S&D - Entity Model). |
| `SND_EN_DLP_DELIVERY_PLAN` | 11 | Delivery Plan Setup Table - (S&D - Entity Model). |
| `SND_EN_ERD_EXCH_RATE_DIST_WISE` | 14 | Distributor wise Exchange Rate Table - (S&D - Entity Model). |
| `SND_EN_FCT_FCS_TARGETS` | 14 | FC Targets Table - (S&D - Entity Model). |
| `SND_EN_FL1_FVC_COMB_LOG_LVL1` | 18 | Sell. Catg wise Ranking - Sell. Catg wise Credit Freq & Limit - Sell. Catg+Outlet wise Ranking Setup Table - (S&D - Entity Model). |
| `SND_EN_FP1_FVC_COMB_PHS_LVL1` | 19 | Outlet wise Ranking - Outlet wise Visit Frequency & Status - Outlet wise Credit Frequency & Limit - Outlet+Sell. Catg wise Ranking Setup Table - (S&D - Entity Model). |
| `SND_EN_FP2_FVC_COMB_PHS_LVL2` | 18 | DSR wise Ranking - DSR wise Visit Frequency & Status - DSR+Outlet wise Ranking Setup Table - (S&D - Entity Model). |
| `SND_EN_HCL_HOLIDAY_CALENDAR` | 13 | Holiday Calendar Setup Table - (S&D - Entity Model). |
| `SND_EN_IDC_IQ_ENT_DATA` | 55 | IQ Entity Data Table - (S&D - Entity Model). |
| `SND_EN_IOD_IO_DETAIL` | 12 | IO Detail Table - (S&D - Entity Model). |
| `SND_EN_IOM_IO_MASTER` | 25 | IO Master Table - (S&D - Entity Model). |
| `SND_EN_ITS_IQ_ENT_THRESHOLD` | 41 | IQ Entity Threshold Table - (S&D - Entity Model). |
| `SND_EN_IWB_IO_WISE_BUDGET` | 12 | IO Wise Budget Table - (S&D - Entity Model). |
| `SND_EN_OCD_OUTL_CONTRACT_DTL` | 18 | Outlet Contract Detail Table - (S&D - Entity Model). |
| `SND_EN_OCH_OUTL_CONTRACT_HDR` | 20 | Outlet Contract Header Table - (S&D - Entity Model). |
| `SND_EN_OCP_CUSTOM_PROD_OUTLET` | 13 | Outlet Wise Custom Product Table - (S&D - Entity Model). |
| `SND_EN_OFB_OUTLET_FEEDBACK` | 12 | Outlet Wise Feedback Table - (S&D - Entity Model). |
| `SND_EN_OFP_OUTL_FAVORITE_PRD` | 9 | Outlet Wise Favorite Products Table - (S&D - Entity Model). |
| `SND_EN_OGE_OTH_GENENTITY` | 54 | Other Information of General Entities (Insurance Company etc) Table - (S&D - Entity Model). |
| `SND_EN_OL1_OTH_BSEN_LOG_LVL1` | 54 | Other Information of Logical Business Entities Level 1 (Selling Category, Section etc) Table - (S&D - Entity Model). |
| `SND_EN_OP1_OTH_BSEN_PHS_LVL1` | 76 | Other Information of Physical Business Entities Level 1 (Distributor, Outlet, Warehouse etc) Table - (S&D - Entity Model). |
| `SND_EN_OP2_OTH_BSEN_PHS_LVL2` | 54 | Other Information of Physical Business Entities Level 2 (DSR, Courier Service etc) Table - (S&D - Entity Model). |
| `SND_EN_OPR_OUTLET_PJP_ROUTE` | 20 | Permanent Journey Plan for Outlet Table - (S&D - Entity Model). |
| `SND_EN_ORI_ORDER_INTEGRATION` | 11 | Order Integration Table - (S&D - Entity Model). |
| `SND_EN_OSG_OUTLET_SEGMENTS` | 10 | Outlet Segments Table - (S&D - Entity Model). |
| `SND_EN_PCA_PP1_COVERED_AREA` | 10 | Distributor Covered Area Table - (S&D - Entity Model). |
| `SND_EN_PDE_PJP_DELIVERY_EVENT` | 18 | PJP Delivery Events Table - (S&D - Entity Model). |
| `SND_EN_PGE_PRF_GENENTITY` | 57 | General Entities (Insurance Company etc) Setup Table - (S&D - Entity Model). |
| `SND_EN_PGS_PJPVISIT_CYCLE` | 34 | PJP Visit Cycle (Template) Table - (S&D - Entity Model). |
| `SND_EN_PJD_PJPDETAIL` | 33 | PJP Detail (Template) Table - (S&D - Entity Model). |
| `SND_EN_PJD_PJPDETAIL_DAILY` | 31 | PJP Detail Daily Setup Table - (S&D - Entity Model). |
| `SND_EN_PJP_PJPHEAD` | 63 | PJP Header (Template) Table - (S&D - Entity Model). |
| `SND_EN_PJP_PJPHEAD_DAILY` | 66 | PJP Header Daily Setup Table - (S&D - Entity Model). |
| `SND_EN_PJS_PJP_SUB_DETAIL` | 17 | PJP Sub Detail Table - S&D - Entity Model This table will use to handle a scenario that if any DSR visits a section for 3 days in a week. Development was facing some complications related to populating the Grid on the screen therefore they need this table. |
| `SND_EN_PJV_PJPVISIT_DAILY` | 32 | PJP Visit Daily Outlet Setup Table - (S&D - Entity Model). (Section POP Daily) |
| `SND_EN_PL1_PRF_BSEN_LOG_LVL1` | 66 | Logical Business Entities Level 1 (Selling Category, Section etc) Setup Table - (S&D - Entity Model). |
| `SND_EN_PLA_PL1_COVERED_AREA` | 10 | Section Covered Area Table - (S&D - Entity Model). |
| `SND_EN_PP1_PRF_BSEN_PHS_LVL1` | 134 | Physical Business Entities Level 1 (Distributor, Outlet, Warehouse etc) Setup Table - (S&D - Entity Model). |
| `SND_EN_PP2_PRF_BSEN_PHS_LVL2` | 77 | Physical Business Entities Level 2 (DSR, Courier Service etc) Setup Table - (S&D - Entity Model). |
| `SND_EN_RDM_ROLE_BASE_DT_MSG` | 10 | Role Base Distributor Message Table - (S&D - Entity Model). |
| `SND_EN_SGS_SEGMENTS_SETUP` | 12 | Segments Setup Table - (S&D - Entity Model). |
| `SND_EN_SLM_SELLCATG_MAP` | 11 | Selling Category Mapping with Child Selling Category Table - (S&D - Entity Model). |

## S&D-EN - Other Tables

| Table | Cols | Description |
|---|---|---|
| `GLB_EN_ADR_ADDRESS` | 73 | Address Detail Table - (S&D-Other Tables). |
| `GLB_EN_BAC_BANKACCOUNT` | 59 | Bank Account Detail Table - (S&D-Other Tables). |
| `GLB_EN_BSI_BUSINESSINFO` | 56 | Business Information Detail Table - (S&D-Other Tables). |
| `GLB_EN_COD_CONTACTDETAIL` | 63 | Contact Detail Table - (S&D-Other Tables). |
| `GLB_EN_DEV_DEVICEINFO` | 56 | Device Information Detail Table - (S&D-Other Tables). |
| `GLB_EN_DOC_DOCUMENTDETAIL` | 61 | Document Detail Table - (S&D-Other Tables). |
| `GLB_EN_PEX_PASTEXPERIENCE` | 55 | Previous Experience Detail Table - (S&D-Other Tables). |
| `GLB_EN_QLF_QUALIFICATION` | 56 | Qualification Detail Table - (S&D-Other Tables). |

## S&D-EN - Transactions Tables

| Table | Cols | Description |
|---|---|---|
| `SND_LG_ACS_ASSTCOMPSTAT_LOG` | 20 | Asset Compliance Status Log Table - (S&D - Transactions). |
| `SND_LG_CEL_CLAIM_EXE_LOSS_LOG` | 11 | Claim Execution Loss Log Table - (S&D - Transactions). |
| `SND_LG_CPL_CLAIM_PROCESS_LOG` | 10 | Claim Process Log Table - (S&D - Transactions). |
| `SND_LG_DST_DOCSTATUS_LOG` | 30 | Document Status Log Table - (S&D - Transactions). |
| `SND_LG_ORL_ORDER_LOG` | 19 | Order Log Table - (S&D - Transactions). |
| `SND_LG_VSL_VISITSTATUS_LOG` | 79 | Business Entity's Visit Status Log Table - (S&D - Transactions). |
| `SND_TR_ALD_ALLOCAT_STOCK_DTL` | 25 | Allocated Stock Detail Table - (S&D - Transactions). |
| `SND_TR_ALS_ALLOCATED_STOCK` | 9 | Allocated Stock Header Table - (S&D - Transactions). |
| `SND_TR_ASS_ALOCAT_STK_SB_DTL` | 18 | Allocated Stock Sub Detail Table - (S&D - Transactions). |
| `SND_TR_BRC_BANK_RECONCILE` | 22 | Bank Reconciliation Table - (S&D - Transactions). |
| `SND_TR_CAI_CMM_ADITIONL_INFO` | 13 | Cash Memo Additional Information Table - (S&D - Transactions). To maintain un registered customer’s information. i.e. At the time of spot selling driver will also record name, address and phone number information. |
| `SND_TR_CES_CM_EXTERNAL_SCHEM` | 14 | Cashmemo External Scheme Table - (S&D - Transactions). |
| `SND_TR_CET_CASHMEMO_EXE_TOUR` | 37 | Cashmemo Execution Tour Table - (S&D - Transactions). |
| `SND_TR_CLD_CLAIM_DETAIL` | 39 | Claim Detail Table - (S&D - Transactions). |
| `SND_TR_CLM_CLAIM_MASTER` | 43 | Claim Master Table - (S&D - Transactions). |
| `SND_TR_CLP_CM_LOCK_PROMOS` | 10 | Cashmemo Lock Promotions Table - (S&D - Transactions). |
| `SND_TR_CLR_CLAIM_REFINFO` | 15 | Claim Reference Info Table - (S&D - Transactions). |
| `SND_TR_CMF_CASHMEMO_FINELM` | 21 | Cash Memo Item Wise Financial Breakup Transactional Table - (S&D - Transactions). |
| `SND_TR_CMM_CASHMEMO_CHARGES` | 35 | Cash Memo Charges Table - (S&D - Transactions). |
| `SND_TR_CMM_CASHMEMO_CHRGS_DT` | 23 | Cash Memo Charges Detail Table - (S&D - Transactions). |
| `SND_TR_CMM_CASHMEMO_DETAIL` | 106 | Cash Memo Detail Transactional Table - (S&D - Transactions). |
| `SND_TR_CMM_CASHMEMO_MASTER` | 135 | Cash Memo Master Transactional Table - (S&D - Transactions). |
| `SND_TR_CMM_CASHMEMO_OFFERING` | 53 | Offering - Scheme Discount Header Transactional Table - (S&D - Transactions). |
| `SND_TR_CMM_CASHMEMO_OFFRITEM` | 70 | Offering - Scheme Discount Detail Transactional Table - (S&D - Transactions). |
| `SND_TR_CMM_CASHMEMO_PAYMENT` | 49 | Cash Memo Payment Transactional Table - (S&D - Transactions). |
| `SND_TR_CMM_CASHMEMO_REFINFO` | 13 | Cash Memo Reference Info Transactional Table - (S&D - Transactions). |
| `SND_TR_CMM_OFFINVOICE_OFRITEM` | 28 | Off Invoice Offer Item Table - (S&D - Transactions). |
| `SND_TR_CMP_CASHMEMO_PRNT_LOG` | 12 | Cash Memo Print Log Table - (S&D - Transactions). |
| `SND_TR_CMS_CASHMEMO_SUGPRDGP` | 68 | Cash Memo Table for Suggested Product Group for "B To C Business" - (S&D - Transactions). |
| `SND_TR_DID_DOC_INVOICING_DTL` | 12 | Document Invoicing Detail Table - (S&D - Transactions). |
| `SND_TR_DIN_DOC_INVOICING` | 27 | Document Invoicing Table - (S&D - Transactions). |
| `SND_TR_DOB_DIST_OPN_BAL_DATE` | 9 | Distributor Opening Balance Date Table - (S&D - Transactions). |
| `SND_TR_DRD_DSR_ROUT_TRP_STL_DT` | 17 | DSR Route Trip Settlement Detail Table - (S&D - Transactions). |
| `SND_TR_DRT_DSR_ROUTE_TRIP_SETL` | 24 | DSR Route Trip Settlement Header Table - (S&D - Transactions). |
| `SND_TR_DSC_DALYSTCK_SNPSHT_COM` | — | Daily Stock Snapshot Comments Table - (S&D - Transactions). |
| `SND_TR_DSD_DALYSTCK_SNPSHT_DTL` | — | Daily Stock Snapshot Detail Table - (S&D - Transactions). |
| `SND_TR_DSD_DEPOSIT_SLIP_DTL` | 28 | Deposit Slip Detail Table - (S&D - Transactions). |
| `SND_TR_DSL_DEPOSIT_SLIP` | 37 | Deposit Slip Table - (S&D - Transactions). |
| `SND_TR_DSN_DOC_SEQUENCE_NO` | 16 | Document Sequence Number Transactional Table - (S&D - Transactions). |
| `SND_TR_DSS_DAILYSTOCK_SNAPSHOT` | — | Daily Stock Snapshot Table - (S&D - Transactions). |
| `SND_TR_DTL_DISTRIBUTR_LEDGER` | 11 | Distributor Ledger Table - (S&D - Transactions) DA/RA Amount |
| `SND_TR_EVM_EVENT_MESSAGES` | 11 | Event Messages Table - (S&D - Transactions). |
| `SND_TR_EXM_EXPENSE_MASTER` | 17 | Expense Master Transactional Table - (S&D - Transactions). |
| `SND_TR_FBI_FBR_INTEGRATION` | 16 | FBR Integration Table - (S&D - Transactions). |
| `SND_TR_FDD_FINANCIAL_DOC_DTL` | 23 | Financial Documents (Credit/Debit Note) Detail Table - (S&D - Transactions). |
| `SND_TR_FDH_FINANCIAL_DOC_HDR` | 48 | Financial Documents (Credit/Debit Note) Header Table - (S&D - Transactions). |
| `SND_TR_GNF_GINGRN_FINELM` | 21 | GIN/GRN Item Wise Financial Breakup Transactional Table - (S&D - Transactions). |
| `SND_TR_GNM_GINGRN_DETAIL` | 67 | Goods Note Detail Transactional Table - (S&D - Transactions). |
| `SND_TR_GNM_GINGRN_MASTER` | 84 | Goods Note Master Transactional Table - (S&D - Transactions). |
| `SND_TR_GNM_GINGRN_REFINFO` | 12 | Goods Note Reference Info Transactional Table - (S&D - Transactions). |
| `SND_TR_IND_INSTRUMENT_DETAIL` | 24 | Instrument (Cheque, Deposit Slip, Pay Order etc) Detail Table - (S&D - Transactions). |
| `SND_TR_JCD_JUPITR_CLM_DISTBN` | 13 | Jupitar Claim Distribution Table - (S&D - Transactions). |
| `SND_TR_JPL_JUPITER_PROM_LDGR` | 16 | Jupiter Promotion Ledger Table - (S&D - Transactions) Free Product wise TAX |
| `SND_TR_MIS_OTHERINFO` | 20 | MIS Other Information Table - (S&D - Transactions). |
| `SND_TR_OCI_OUTL_CONTRCT_INSTLM` | 22 | Outlet Contract Installment Table - (S&D - Transactions). |
| `SND_TR_OFD_ORDER_FILE_DETAIL` | 39 | Order File Detail Table - (S&D - Transactions). |
| `SND_TR_OFH_ORDER_FILE_HEADER` | 12 | Order File Header Table - (S&D - Transactions). |
| `SND_TR_ORD_ORDER_REQ_DETAIL` | 66 | Order Requisition Detail Table - (S&D - Transactions). |
| `SND_TR_ORM_ORDER_REQ_MASTER` | 80 | Order Requisition Master Table - (S&D - Transactions). |
| `SND_TR_ORR_ORDER_REQ_REFINFO` | 12 | Order Requisition Reference Info Transactional Table - (S&D - Transactions). |
| `SND_TR_PLG_PROCESS_LOG` | 13 | Process Log Table - (S&D - Transactions). |
| `SND_TR_PSD_PHYSICAL_STOCK_DT` | 38 | Physical Stock Detail Table - (S&D - Transactions). |
| `SND_TR_PSH_PHYSICAL_STOCK_HD` | 16 | Physical Stock Header Table - (S&D - Transactions). |
| `SND_TR_PSR_PICKED_SALE_RETRN` | 27 | Picked Sales Return for making kind of GRN Table - (S&D - Transactions). |
| `SND_TR_RSD_DSR_ROUTE_SETL_DT` | 15 | DSR Route Settlement Detail Table - (S&D - Transactions). |
| `SND_TR_RSL_DSR_ROUTE_SETTLEM` | 26 | DSR Route Settlement Header Table - (S&D - Transactions). |
| `SND_TR_SLD_SALES_DETAIL` | 33 | Sales Detail Table - (S&D - Transactions). |
| `SND_TR_SLM_SALES_MASTER` | 45 | Sales Master Table - (S&D - Transactions). |
| `SND_TR_SLR_SALEMASTER_REFINFO` | 15 | Sales Master Reference Info Table - (S&D - Transactions). |
| `SND_TR_SMI_SMM_ADITIONL_INFO` | 21 | Sales Master Additional Information Table - (S&D - Transactions). |
| `SND_TR_SOD_STOCK_OUT_DETAIL` | 24 | Stock Out Detail Table - (S&D - Transactions). |
| `SND_TR_SOL_OUTLET_LEDGER` | 16 | Outlet Ledger Table - (S&D - Transactions). |
| `SND_TR_SPD_PURCHASE_ORDER_DTL` | 18 | Purchase Order Detail Table - (S&D - Transactions). |
| `SND_TR_SPO_PURCHASE_ORDER` | 19 | Purchase Order Table - (S&D - Transactions). |
| `SND_TR_SRD_STOCK_RESERVE_DTL` | 27 | Stock Reserved Detail Table - (S&D - Transactions). |
| `SND_TR_SRR_SALERETURN_REFINFO` | 13 | Picked Sales Return Reference Info Table - (S&D - Transactions). |
| `SND_TR_SSB_SALESTOCK_BALANCE` | 53 | Sales Stock Balance Transactional Table - (S&D - Transactions). |
| `SND_TR_SST_SALE_ORD_SUGG_STOCK` | 15 | Sales Order Based on Suggested Stock Table - (S&D - Transactions). |
| `SND_TR_STD_STOCK_REQUISTON_DTL` | 21 | Stock Requisition Detail Table - (S&D - Transactions). |
| `SND_TR_STM_STOCK_DETAIL` | 90 | Stock Detail Transactional Table - (S&D - Transactions). |
| `SND_TR_STM_STOCK_MASTER` | 75 | Stock Master Transactional Table - (S&D - Transactions). |
| `SND_TR_STM_STOCK_RECVDETAIL` | 68 | Stock Receive Detail Table for Loss Quantity - (S&D - Transactions). |
| `SND_TR_STM_STOCK_RECVMASTER` | 15 | Stock Receive Master Table for Loss Quantity - (S&D - Transactions). |
| `SND_TR_STM_STOCK_REFINFO` | 12 | Stock Reference Info Transactional Table - (S&D - Transactions). |
| `SND_TR_STR_STOCK_REQUISITION` | 24 | Stock Requisition Table - (S&D - Transactions). |
| `SND_TR_TAC_TARGT_ACHIEVEMENT` | 19 | Target Achievement Table - (S&D - Transactions). |
| `SND_TR_VTD_VAT_DOCUMENT` | 19 | VAT Document Table - (S&D - Transactions). |
| `SND_TR_VTL_VAT_LEDGER` | 12 | VAT Ledger Table - (S&D - Transactions) TAX Amount against DA/RA/Sale/Sales Return |

## Target Module

| Table | Cols | Description |
|---|---|---|
| `GLB_PR_FCN_FIELD_COMBINATION` | 11 | Field Combination Table - General Parameters |
| `GLB_PR_FGR_FIELD_GROUP` | 12 | Field Group Table - General Parameters |
| `TGR_PR_LYC_LOYALTY_CATALOGUE` | 9 | Loyalty Catalogue Table - Target Module |
| `TGT_PR_ELE_PHS_LVL1_ENROLMNT` | 16 | Physical Level 1 Enrollment Table - Target Module |
| `TGT_PR_END_ENTITY_GROUP_DTL` | 14 | Entity Group Detail Table - Target Module |
| `TGT_PR_ENG_ENTITY_GROUP` | 10 | Entity Group Table - Target Module |
| `TGT_PR_IAP_INCNTVE_ACH_PROCS` | 12 | Incentive Achievement Process - Target Module |
| `TGT_PR_ICD_INCNTV_CLMDISTRB` | 9 | Incentive Claim Distribution - Target Module |
| `TGT_PR_IEP_INC_ENRL_TRGT_PRN` | 18 | Incentive Enrollment Target Principal Wise - Target Module |
| `TGT_PR_IET_INC_ENROLL_TARGET` | 20 | Incentive Enrollment Target Table - Target Module |
| `TGT_PR_IFP_INCNTVE_FOC_PRODUCT` | 9 | Incentive FOC Product Table - Target Module |
| `TGT_PR_INC_INCENTIVE` | 19 | Incentive Table - Target Module |
| `TGT_PR_INR_INCENTIVE_REWARD` | 28 | Incentive Reward Table - Target Module |
| `TGT_PR_INT_INCENTIVE_TYPE` | 13 | Incentive Type Table - Target Module |
| `TGT_PR_IPD_INCENTIVE_PERIOD` | 15 | Incentive Period Table - Target Module |
| `TGT_PR_IPD_INCNTVE_PROCESS_DTL` | 11 | Target Incentive Process Detail Table - Target Module |
| `TGT_PR_IPG_INC_PERIOD_GROUP` | 15 | Incentive Period Group Table - Target Module |
| `TGT_PR_IPH_INCNTVE_PROCESS_HD` | 10 | Target Incentive Process Header Table - Target Module |
| `TGT_PR_IRP_INCNTVE_REWARD_PROD` | 16 | Incentive Reward Product Table - Target Module |
| `TGT_PR_ISB_INCENTIVE_SLABS` | 21 | Incentive Slabs Table - Target Module |
| `TGT_PR_PGD_PROD_GROUP_DETAIL` | 17 | Prod Group Detail Table - Target Module |
| `TGT_PR_PGR_PRODUCT_GROUP` | 13 | Product Group Table - Target Module |
| `TGT_PR_PRD_POINTS_RDMPTION_DTL` | 16 | Points Redemption Detail Table - Target Module |
| `TGT_PR_PTR_POINTS_REDEMPTION` | 14 | Points Redemption Table - Target Module |
| `TGT_PR_RTG_ROUTE_TARGET` | 22 | Route Target Table - Target Module |
| `TGT_PR_TCD_TARGET_CATALOG_ACH` | 23 | Target Catalog Achievement Table - Target Module |
| `TGT_PR_TCD_TARGT_CATALOG_DTL` | 32 | Target Catalog Detail Table - Target Module |
| `TGT_PR_TGC_TARGET_CATALOG` | 27 | Target Catalog Table - Target Module |
| `TGT_PR_TGC_TARGET_SALES_STG` | 15 | Target Sales Stagging Table - Target Module |
| `TGT_PR_TSI_TARGT_SPLIT_INQUIRY` | 19 | Target Split Inquiry Table - Target Module |
| `TGT_PR_TUH_TRGT_USR_HERARCHY` | 10 | Target User Hierarchy Table - Target Module |
| `TGT_PR_VRD_VARIABLE_DETAIL` | 18 | Variable Detail Table - Target Module |
| `TGT_PR_VRG_VARIABLE_GROUP` | 13 | Variable Group Table - Target Module |

## Validation Module

| Table | Cols | Description |
|---|---|---|
| `VLD_VL_FLD_FILTRATION_DETAIL` | 11 | Filtration Detail Table - Validation |
| `VLD_VL_FLH_FILTRATION_HEADER` | 11 | Filtration Header Table - Validation |
| `VLD_VL_VDD_VALIDATION_DETAIL` | 26 | Validation Detail Table - Validation |
| `VLD_VL_VDH_VALIDATION_HEADER` | 15 | Validation Header Table - Validation |
| `VLD_VL_VDS_VALIDATION_SETUP` | 13 | Validation Setup Table - Validation |
| `VLD_VL_VHR_VALID_HDR_REPO_MP` | 12 | Validation Header and Repository Code & Value Mapping Table - Validation Module |

## (not in grouping) DD-Change Track VER 12

| Table | Cols | Description |
|---|---|---|
| `CHT_PR_CTD_CHANGE_TRACK_DTL` | 19 |  |
| `CHT_PR_CTH_CHANGE_TRACK_HEAD` | 14 |  |

## (not in grouping) DD-Combinations VER 10

| Table | Cols | Description |
|---|---|---|
| `CLC_PR_ANS_ANSWERS` | 15 |  |
| `CLC_PR_ATP_ACTIONTYPES` | 22 |  |
| `CLC_PR_CMC_COMPLIANCECONFIG` | 13 |  |
| `CLC_PR_CMT_COMPLIANCETYPE` | 12 |  |
| `CLC_PR_CON_CONDITIONS` | 13 |  |
| `CLC_PR_CTG_CUSTOMTAGS` | 24 |  |
| `CLC_PR_CTP_CUSTOMTAGS_PARAMS` | 9 |  |
| `CLC_PR_EAM_EVENTACTIONMAPPING` | 7 |  |
| `CLC_PR_ECM_EVENTCUSTTAGMAPPING` | 7 |  |
| `CLC_PR_ERM_EVENTREPOMAPPING` | 8 |  |
| `CLC_PR_EVT_EVENTS` | 10 |  |
| `CLC_PR_KPT_KPITYPE` | 12 |  |
| `CLC_PR_QQM_QNAIRE_QUSTON_MAP` | 25 |  |
| `CLC_PR_QSR_QUESTIONNAIRE` | 13 |  |
| `CLC_PR_QUE_QUESTIONS` | 15 |  |
| `CLC_PR_REP_REPOSITORY` | 20 |  |
| `CLC_PR_REP_REPOSITORY_M` | 8 |  |
| `CLC_PR_RTT_RATETYPE` | 11 |  |
| `CMB_PR_ACD_ACTIONDETAIL` | 25 |  |
| `CMB_PR_CDR_COMBDATERANGES` | 8 |  |
| `CMB_PR_COM_COMBINATIONS` | 17 |  |
| `CMB_PR_COR_COMBINATIONSRANGES` | 8 |  |
| `CMB_PR_COV_COMBINATIONVALUES` | 14 |  |
| `CMB_PR_CVD_COMBDATEVALUERANGES` | 41 |  |
| `CMB_PR_CVR_COMBVALUESRANGES` | 41 |  |
| `FBL_PR_FMM_FORMULAMASTER` | 14 |  |
| `FBL_PR_FMS_FORMULASTEPS` | 12 |  |

## (not in grouping) DD-EN-Transactions VER 12

| Table | Cols | Description |
|---|---|---|
| `SND_TR_CES_CM_EXEC_STATUS` | 21 |  |
| `SND_TR_DSC_DLYSTK_SNPSHOT_COM` | 12 |  |
| `SND_TR_DSD_DLYSTK_SNPSHOT_DTL` | 26 |  |
| `SND_TR_DSS_DLYSTK_SNPSHOT` | 15 |  |
| `SND_TR_GNM_GINGRN_PP2_MAPING` | 12 |  |
| `SND_TR_SMP_SALEMASTER_PAYMENT` | 14 |  |

## (not in grouping) DD-File Uploader VER 12

| Table | Cols | Description |
|---|---|---|
| `FUP_FU_FGS_FILE_UPLD_GLB_STP` | 7 |  |
| `FUP_FU_FUI_FILE_UPLD_STP_INF` | 9 |  |
| `FUP_FU_FUM_FILE_UPLOAD_MASTER` | 21 |  |
| `FUP_FU_FUS_FILE_UPLOAD_SETUP` | 15 |  |
| `FUP_FU_FUT_FILE_UPLOAD_TYPES` | 9 |  |

## (not in grouping) DD-General Parameters VER 12

| Table | Cols | Description |
|---|---|---|
| `GLB_PR_DMC_DEMAND_CHANNEL` | 13 |  |
| `GLB_PR_EXS_EXECUTION_STATUS` | 20 |  |

## (not in grouping) DD-Incentive Module

| Table | Cols | Description |
|---|---|---|
| `INC_PR_ICD_INCNTV_CLMDISTRB` | 8 |  |
| `INC_PR_INR_INCNTV_REWARD` | 15 |  |
| `INC_PR_IPS_INCNTV_PROGSTP` | 15 |  |

## (not in grouping) DD-Product VER 12

| Table | Cols | Description |
|---|---|---|
| `SND_PR_PRP_PROD_POLICY` | 16 |  |
| `SND_PR_PSA_POLICY_STRATA` | 9 |  |
| `SND_PR_RET_REFERENCE_TYPE_M` | 9 |  |

## (not in grouping) DD-S&D-EN-Entity Model VER 12

| Table | Cols | Description |
|---|---|---|
| `SND_EN_ICT_IO_CLAIM_TYPE_MAP` | 11 |  |
| `SND_EN_OID_ORDR_INTGRTON_DTL` | 12 |  |

## (not in grouping) DD-S&D-EN-Transactions VER 1

| Table | Cols | Description |
|---|---|---|
| `SND_ST_VSL_VISITSTATUS_LOG` | 28 |  |
| `SND_TR_OSL_OUTLET_SALES` | 61 |  |
| `SND_TR_PSL_PRIMARY_SALES` | 64 |  |
| `SND_TR_PST_PRIMARY_STOCK` | 35 |  |
| `SND_TR_SSB_SALESSTOCK_BALANCE` | 33 |  |
| `SND_TR_SST_SECONDARY_STOCK` | 39 |  |

## (not in grouping) DD-Target Module VER 12

| Table | Cols | Description |
|---|---|---|
| `TGT_PR_ENG_ENTITY_GROUP_M` | 10 |  |
| `TGT_PR_INC_INCENTIVE_M` | 9 |  |
| `TGT_PR_INT_INCENTIVE_TYPE_M` | 9 |  |
| `TGT_PR_IPG_INC_PERIOD_GROUP_M` | 10 |  |
| `TGT_PR_ISB_INCENTIVE_SLABS_M` | 14 |  |
| `TGT_PR_PGR_PRODUCT_GROUP_M` | 10 |  |
| `TGT_PR_TGC_TARGET_CATALOG_M` | 9 |  |
| `TGT_PR_VRD_VARIABLE_DETAIL_M` | 10 |  |
| `TGT_PR_VRG_VARIABLE_GROUP_M` | 9 |  |

## (not in grouping) Financials Module

| Table | Cols | Description |
|---|---|---|
| `FIN_PR_ACS_ACTIVITY_SETUP` | 12 |  |
| `FIN_TR_RCOA_REP_TRANSACTIONS` | 33 |  |
| `FIN_TR_VEL_VALID_EXCEPTION_LOG` | 22 |  |
