# Scan Summary: Tracker (People) & USA Report (Services Score, PG)

## 1. People names – *Copy of Divisional Meeting Updates Tracker  .xlsx*

Source: **Names** and **Ownership** columns across all sheets (Reworks, Priority Tracker, Batch - 2, Entire Team Summary).

**Total: 81 unique people**

| # | Name | # | Name | # | Name |
|---|------|---|------|---|------|
| 1 | Adarsh | 28 | Ishwar | 55 | Sadhwika |
| 2 | Adarsh Gowda | 29 | Javeriya | 56 | Sahmika |
| 3 | Adika | 30 | John | 57 | Sakshi |
| 4 | Aditya | 31 | John Mithi | 58 | Sara |
| 5 | Adrika | 32 | John Mithila | 59 | Sathya |
| 6 | Adrika (Rework) | 33 | Johnathan | 60 | Shivani |
| 7 | Afreena | 34 | Jonathan | 61 | Shivi |
| 8 | Amena | 35 | Komal | 62 | Shivi (Rework) |
| 9 | Ananya | 36 | Komal Agarwal | 63 | Shreetika |
| 10 | Annaya | 37 | Madhuluta | 64 | Shruti |
| 11 | Anushka | 38 | Madhur | 65 | Simran |
| 12 | Ask Ekta | 39 | Mahima | 66 | Sophie |
| 13 | Baistami | 40 | Manasvi | 67 | Soumya |
| 14 | Bhargava | 41 | Manaswi | 68 | Soumyadiya |
| 15 | Celine | 42 | Mimansa | 69 | Sowjanya |
| 16 | Celine Mathew | 43 | Mohsin | 70 | Steven |
| 17 | Chaitanya | 44 | Mona | 71 | Suchitra |
| 18 | Cheeruthan | 45 | Mona Rabi | 72 | Sukhman |
| 19 | Cheruthan | 46 | Nabanita | 73 | Sukhman Dhaliwal |
| 20 | Devaleena | 47 | Nikita | 74 | Susan |
| 21 | Devleena | 48 | No EHR | 75 | Sutiksha |
| 22 | Divya | 49 | Om | 76 | Suzanne |
| 23 | Farhaan | 50 | Pratibha | 77 | Swastika |
| 24 | Gagan | 51 | Priti | 78 | Thillai Gowri |
| 25 | Himaja | 52 | RSC | 79 | Tiisetso |
| 26 | Hiya | 53 | Richard | 80 | Vedansh |
| 27 | Himaja | 54 | Rupashi / Rupashi Verma | 81 | Yukta |

*(Note: "No EHR" and "RSC" may be placeholders; you can filter them out in the dashboard.)*

---

## 2. PG – *Final USA report. Scores (4).xlsx*

Sheet: **USA master tracker**  
Column: **PG**

**Total: 88 PGs** (sample below; full list from script).

- Americare, Intracare, ACO Health, APPLE MD, BIDMC, Best Self, Bloom, Boerne Healthcare Group, Boston Senior Medicine, Bowdoin, Boyer family practice, Brockton, COFMC, Care Dimensions, Caring Health, Covenant Care, Doctors at Home, FHCW, Grace at Home, Hawthorn, Health Quality Primary Care, Healthfirst, Hyde Park, IDCOKC, Lowell, MDPC, Medical Associates of NE, New Bedford, Paragon, Prima Care, Providence Care, Renaissance Primary care, Resil Claude, Riverside, Rocky Mountain, Royal VP, TTUHSC, Trucare, UT health, Upham, WoundCentrics, housecall MD, community first, … *(and 44 more)*

---

## 3. Services score – *Final USA report. Scores (4).xlsx*

There is **no column literally named "Services Score"** in the USA report. Available scores:

### USA master tracker – monthly scores (0 or 1)

- **Jan' 2026 score**, **Dec' 25 Score**, **Nov' 25 Score**, **Oct' 25 Score**, **Sept' 25 Score**, **Aug' 25 Score**, **July' 25 Score**, **June' 25 Score**, **May' 25 Score**, **April' 25 Score**, **March' 25 Score**, **Feb' 25 Score**, **JAN' 25 Score**

These are per-PG, per-month (e.g. 0 = not met, 1 = met).  
Sample for **Dec' 25 Score**: `[0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, ...]`

### Scores sheet – Overall Score (decimal)

- **Overall Score**: decimal values (e.g. 0.71, 0.87, 0.81, 0.58).  
  Likely one row per person or per PG; the sheet has no other named columns (only Unnamed 0–12 and Overall Score).

If “services score” means something specific (e.g. a KPI name in another sheet or file), share the exact name and we can map it.

---

## 4. How to re-run the scan

From the project folder:

```bash
python scan_excel.py
```

This prints:

- People names from the Tracker (Names + Ownership).
- PG list and all score columns from the USA report.

You can use this output to feed the dashboard (people from Tracker; PG + scores from USA report).
