# Training session log - Promotion Layout read-only walk (S&D, PK, cnr1dev1)

- Date: 2026-10-08 (after the stopped run QUICK-20261008-1739)
- Trainer: Syed Kamran (QA lead), method C (live walk), read-only: "select existing promotion code and go through each screen / tab on promotion layout"
- User: Auto_Multi_Orga (company Unilever Pakistan Limited, distributor 15108843). Nothing was saved, applied, copied or allocated; Scheduler opened and closed without Save; one dropdown list opened and closed without a change.

## Facts observed [observed 2026-10-08 walk]
| # | Fact |
|---|---|
| O1 | Promotion Layout opens on a page with Scheme, Download Excel, Upload Excel; Scheme lists all promotions (299 on 2026-10-08, 31 pages of 10, no search box). List columns: Code, Description, Alternate Description, Start Date, End Date, Resultant Type, Allocated Budget, Utilized Budget, Balance, Allocated Budget QTY, Utilized Budget QTY, Balance QTY, Status. |
| O2 | Resultant types in use: BONUS2 123, TRADEOFFER 117, COUPON 23, CP 2, JUPITAR 2, empty 32. Group 11 promotions: Automation2 (BONUS2, Active, 2026-05-08..2029-11-29), May001 / May003 / MARCH001 (BONUS2, Inactive), MARCH002 (TRADEOFFER, Inactive). |
| O3 | A promotion opens by double-click on its row in the builder (/ngui/scheme-builder). Toolbar of an existing promotion: Save, Copy & Save As New Scheme, Cancel, Console, Back, Scheduler, Allocation; switches Scheduler / Exclusive / Super Exclusive (their state is not readable from the screen text). Allocation is disabled on promotions without a budget (Automation2, Free Piece). |
| O4 | Header grid: Promo Code, Promo Name, Alternate Name, Start Date, End Date, Entity Type, Promo Sub Type, Comments, Status; second row Resultant Type, Group Type, Referral Scheme, Bus. Reference No., Budget Hirearchy. |
| O5 | Settings bar under the header: Promo Version, Claimable, Claimable Percent, LPPC, Promo Ret Type, Sch Cashmemo Count, Product AttributesCoins (price basis, e.g. "Price without Tax"), Trade Offer Flag, CM Count, Discount Cap, Budget Discount Cap. |
| O6 | Builder = three sections (Qualify, Criteria, Resultant), each with a palette ("Select Qualify / Criteria / Resultant"), a "Root Group" with AND / OR, groups that can be nested, Include / Exclude and ON / OFF per item, and an "Entity Filter" panel. The Resultant section has an "Additional Limits" panel: Repeat Limit, For Every Factor, Purchase Limit (Per Invoice), Discount Limit (Per Invoice). |
| O7 | **Automation2** (group 11): Qualify = group of 5 products 62740537, 20050310, 62690363, 20050308, 69997598 (unit QTY1), operator "Greater Than OR Equal To", quantity 5; Criteria = DISTRIBUTOR 15108843 (Auto KARACHI), Include; Resultant = Range Slab "Discount On Gross": slab 1 from 1 to 10 = Percentage 5 of Gross Amount, slab 2 from 11 to 99999 = Percentage 10 of Gross Amount; Resultant switches Repeat, Forevery, Apply Remaning, Slab Count, Row Count; Additional Limits all empty; Claimable Yes 100, Promo Ret Type Discount, Price without Tax, Trade Offer Flag Group, CM Count 999999, Discount Cap empty, Referral Scheme Yes. |
| O8 | **JAY81832 "Free Piece"** (free goods example): Qualify = Gross Amount, operator "Greater Than", 2000; Criteria = DISTRIBUTOR 50250327 (Muller & Phipps, Korangi Karachi), Include; Resultant = palette **Product** = 20006444 DOVE BAR WHITE 48 x 135g, type **Fixed Value 14, unit PC** (types offered: Fixed Value, Percentage, Formula); Claimable No. |
| O9 | Scheduler = a cron builder (tabs Seconds, Minutes, Hours, Day, Month, Year; Clear, Save). |

## Open for the trainer
- From / To of a Range Slab: in what unit (cases of the qualify group, or amount)?
- What do Promo Ret Type, Trade Offer Flag, CM Count, Product AttributesCoins and Referral Scheme do?
- Free goods "Fixed Value 14 PC": 14 pieces free per qualifying order (or per For Every Factor)?
- Saving a NEW promotion: which header fields are mandatory, and when is it "Applied" (no Apply button seen)?
