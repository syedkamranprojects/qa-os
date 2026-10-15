---
option: Vehicle Master Bulk Upload Creation (and Modification)
area: master_data
doc_types: [vehicle]
screens: [Vehicle Master Bulk Upload Creation, Vehicle Master Bulk Upload Modification, Vehicle Profile]
roles: [HQ user, DT user (Maker), Approval user (Checker)]
markets: [PK]
status: partly trained (verbal 2026-10-14); screens not yet walked live
---

# Vehicle Master Bulk Upload (PK)

Source: Jira SDMS-5997 ([PK] story, QA Verified 2025-09-29) [jira SDMS-5997] and verbal training by Syed Kamran with the QA team on 2026-10-14 [stated 2026-10-14 Syed Kamran].

## 1. Purpose
- Vehicle Profile creates **one vehicle at a time** at screen level. The client wants to create, and later modify, vehicles **in bulk through an Excel upload**, using master data that already exists in the system (distributor, geo hierarchy, allowed value lists) [stated 2026-10-14 Syed Kamran].

## 2. Screen and flow (creation)
1. The screen has two **mandatory filters** [stated 2026-10-14 Syed Kamran] [jira SDMS-5997]:
   - **Geo Hierarchy**: the drop-down lists the **geo level 2** entries.
   - **Distributor**: lists the distributors that lie under the selected geo level.
2. **Download file:** the system downloads an **empty template** to the browser's download folder.
3. The user fills the template manually. Columns marked `*` are mandatory, the rest optional.
4. **Upload:** the system verifies the mandatory data and the field rules. Correct rows are created and then **appear on the Vehicle Profile screen** [stated 2026-10-14 Syed Kamran].
5. Errors: the system returns the template with the rows in error marked, with the error descriptions separated by commas. Success message: "Vehicle Data Uploaded Successfully" [jira SDMS-5997] (not yet observed live).

## 3. Template columns (`*` = mandatory) [stated 2026-10-14 Syed Kamran]
Distributor Code*, Code, Description*, Status*, Model Name*, Vehicle Color, Registration Number*, Model ID*, Chassis Number, Engine Number, Manufacturing Year, Owner NID, Owner Name, Meter Reading Type, Fuel Type, Vehicle Dimensions (L,W,H) Cubic Meters*, Allow multi trips*, Vehicle Model Description*, Mileage*, Vehicle Type, Fleet Type (CAPTIVE/THIRD_PARTY/ADHOC)*, Unloading Side, Deep Freezer (Y/N), Cold Chain (Y/N), User Count, Average Rate, Unit of Volume (METERS_CUBIC)*, Min Volume*, Max Volume*, Unit of Weight (KG)*, Min Weight*, Max Weight*, Limit Multi Trip, Min GSV, Max GSV, Min NIV, Max NIV, Min TIV, Max TIV.

That is 17 mandatory columns. The defaults for blank optional cells and the allowed value lists come from the story [jira SDMS-5997]:
- Code: generated if blank, otherwise the given code is used.
- Status: Active / In-Active, default Active.
- Model Name, Vehicle Color, Meter Reading Type, Fuel Type, Vehicle Type, Fleet Type, Unloading Side, Deep Freezer, Cold Chain: fixed value lists.
- Number defaults: Mileage 10; Min / Max Volume 0 / 10; Min / Max Weight 0 / 600; GSV / NIV / TIV 10 / 100000000.

## 4. Validations [jira SDMS-5997]
- A mandatory field is missing.
- The distributor code is not valid.
- The registration number is a **duplicate**.
- The same field rules as manual Vehicle Profile creation apply.
- Modification: the Code must exist for the distributor.

Linked bugs (all closed) give regression ideas:
- another distributor's data was accepted (SDMS-6718);
- duplicate registration numbers inside one file were accepted (SDMS-6719, 6717);
- letters in Dimensions were accepted (6749);
- an upload without a vehicle code failed (6739).

## 5. Approval [jira SDMS-5997] (superseded 2026-10-14: HQ-only option, no approval in PK, see section 7)
- An HQ user's upload needs no approval.
- A DT user's upload is Forwarded and the vehicles are created after approval.
- Screen-level path not yet observed.

## 6. Open (to learn live)
- Menu path and screen ids.
- Where a DT upload is approved.
- The error-file format, and whether valid rows are saved when other rows fail.
- The Modification screen and its download content.
- Whether distributor 15108843 is a Locus DT; for Locus DTs every column is mandatory [jira SDMS-5997].

## 7. Answers 2026-10-14 [stated 2026-10-14 Syed Kamran]
- **HQ only:** the bulk upload option is used by the **HQ user only**, who has the rights to upload vehicles for several distributors. So there is no DT path and no approval step in practice (the story's DT/Forward text does not apply to PK).
- **Errors block the whole file:** the file **cannot be uploaded until every error is removed**. A file with any invalid row is rejected and returned with the errors marked; nothing is created (no partial upload).
- **Mandatory = only the `*` columns** for distributor 15108843 (not a Locus DT); the "all fields mandatory for Locus DTs" rule does not apply.
