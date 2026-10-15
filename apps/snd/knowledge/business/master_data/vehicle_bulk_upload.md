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

## 8. Observed 2026-10-15 (read-only look) [observed 2026-10-15 cnr1dev1 headquarter]
Env cnr1dev1, user headquarter (role 0014), company Unilever Pakistan Limited (010104), distributor 15108843-IBRAHIM TRADERS (profile menu verified). Nothing was uploaded or saved.

- **Login selectors:** company page lists "Unilever Pakistan Limited" and "Unilever Bangladesh Limited -Bangla"; distributor page then lists 0103-Karachi West, 15108843-IBRAHIM TRADERS, 15178537-GNY ENTERPRISES, 50250327-MULLER & PHIPPS (KORANGI - KARACHI).
- **Menu:** only one option exists for headquarter: **Distributor Setup > Vehicle Profile > Vehicle Master Bulk Upload** (option id VEHICLE_MASTER_MODIFICATION, route /excel-upload/vehicle-master-modification; searches "Vehicle", "Vehicle Master", "Bulk", "Creation" found no other vehicle bulk entry). A "Vehicle Master Creation" text exists in the language file but no menu entry for headquarter. **AMB1:** Creation screen not found; needs a person (separate option not granted to role 0014, or the one screen serves both).
- **Screen:** title "Vehicle Master Bulk Upload"; breadcrumb Home > Distributor Setup > Vehicle Profile > Vehicle Master Bulk Upload. Controls: "Geo Hierarchy Code" (select, #geoCode), "Distributor" (multi-select tag box, #distCode), buttons "Download Excel" (#downloadExcel) and "Upload Excel" (#fileInput). No '*' on the labels; both buttons enabled with no filter chosen.
- **Geo values (9):** 001001-GT/MT, 001002-UFS, 001003-Ice Cream, 001004-EKT/BEV, 001222-test, N01001-Province, N02N02-Province, M01M02-Southern Pak, 701701-Leo 002.
- **Distributor list:** only "Auto KARACHI" (name only, no code) under the geos checked; **15108843 was not offered** under any geo. The list loads about 2 s after a geo is picked. The template was downloaded with geo 001001-GT/MT + Auto KARACHI (not 15108843).
- **Message:** toast "File downloaded successfully" after Download Excel.
- **Template (file VehicleMasterModification.xlsx, 4 KB):** one sheet "Excel Template", header row only, **39 columns, 17 with '*'**, no data rows, no data validations, no hidden lists. The '*' columns are exactly the 17 listed in section 3 (Distributor Code, Description, Status, Model Name, Registration Number, Model ID, Vehicle Dimensions, Allow multi trips, Vehicle Model Description, Mileage, Fleet Type, Unit of Volume, Min/Max Volume, Unit of Weight, Min/Max Weight). Header texts carrying the allowed values: Fleet Type (CAPTIVE/THIRD_PARTY/ADHOC), Unloading Side (REAR/TOP/LEFT/RIGHT), Deep Freezer (Y/N), Cold Chain: (Y/N), Unit of Volume (METERS_CUBIC), Unit of Weight (KG). Other lists (Status, Model Name, Meter Reading Type, Fuel Type, Vehicle Type) are not in the file.
- **AMB6:** the template header spells the values as CAPTIVE/THIRD_PARTY/ADHOC and METERS_CUBIC (upper case, underscore), as in the column titles, not the story's "Captive / Third Party / Adhoc".
- **AMB9:** error-file behaviour not visible without an upload (not tested).
- **AMB11:** the Modification download for this selection (Auto KARACHI) held no existing vehicles: header only. It is the same 39-column layout as the creation template, so it cannot show which fields may be changed; still open whether a distributor with vehicles returns them (15108843 could not be selected).
