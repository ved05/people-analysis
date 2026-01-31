# Dashboard Plan: People Working on Patient (FTE + Interns)

## 1. Goal
One dashboard that shows **who** in the company (FTE and interns) is supposed to work on patient-related work, with analysis and filters.

---

## 2. Data We Need (and Where It Might Come From)

| Data | Purpose | Likely source |
|------|--------|----------------|
| **Person** | Name / ID | USA report, Tracker |
| **Type** | FTE vs Intern | USA report or HR |
| **Division / Department** | Grouping, filters | Tracker / USA report |
| **Role / Title** | What they do | USA report |
| **Patient-related?** | Yes/No or % | Assignment, role, or manual flag |
| **Scores / Performance** | If relevant | USA report (Scores) |
| **Capacity / Hours** | How much on patient work | Tracker or separate sheet |
| **Status** | Active, On leave, etc. | HR or Tracker |

**Next step:** List the exact column names from:
- `Final USA report. Scores (4).xlsx`
- `Copy of Divisional Meeting Updates Tracker  .xlsx`  

Then we map each column to the above and design the dashboard around real fields.

---

## 3. What to Add to the Dashboard

### 3.1 Overview / Summary
- **Total headcount** for “patient work”: FTE count + intern count.
- **Split:** FTE vs interns (e.g. pie or bar).
- **By division/department:** who has the most people on patient work.

### 3.2 Filters (so you can slice the analysis)
- **Employment type:** FTE / Intern / All.
- **Division / Department.**
- **Role / Title** (if you have it).
- **Patient-related only:** show only people assigned to patient work (if you have a flag or list).

### 3.3 People List / Table
- Table of all people (FTE + interns) who work on patient.
- Columns: Name, Type (FTE/Intern), Division, Role, any Score, Status, etc.
- Sortable and filterable by the filters above.
- Optional: export to CSV/Excel.

### 3.4 Charts / Visuals
- **By type:** FTE vs interns (count or %).
- **By division:** bar chart of headcount per division (patient-only or all).
- **By role:** if you have roles, bar chart of distribution.
- **Trend (if you have dates):** headcount or capacity over time.

### 3.5 Optional (if data exists)
- **Scores:** average or distribution of scores for people on patient work (from USA report).
- **Capacity / hours:** total or average hours allocated to patient work.
- **Gaps:** divisions/teams with no or few people on patient work.

---

## 4. How to Build It (Options)

| Option | Pros | Cons |
|--------|------|------|
| **A. Web app (e.g. React + simple backend)** | Interactive, filters, charts, shareable URL | Needs dev and hosting |
| **B. Python (Streamlit or Dash)** | Fast to build, good for internal use | Someone needs to run the script |
| **C. Excel/Google Sheets** | No code, familiar | Less flexible, no proper filters/charts combo |
| **D. Power BI / Tableau** | Strong analytics, connects to Excel | License and learning curve |

**Recommendation:** Start with **Python (Streamlit)** or a **simple React app** so we can:
- Load both Excel files (or CSVs exported from them).
- Combine FTE + interns into one “people on patient” dataset.
- Add the filters and tables and charts above.

---

## 5. Steps to Do Next

1. **Confirm data:**  
   - Export both Excel files to CSV (or paste column names + 1–2 sample rows) so we can see exact field names and values.
2. **Confirm “patient” definition:**  
   - Is it a column (e.g. “Works on patient: Y/N”), or a list of roles/divisions, or only certain projects?
3. **Choose tech:**  
   - Streamlit vs React (or other) based on who will use it and where it will run.
4. **Build v1:**  
   - One combined dataset (FTE + interns) → summary KPIs, filters, one table, 2–3 charts.
5. **Iterate:**  
   - Add more charts, scores, or capacity once v1 works.

---

## 6. Quick Checklist – What to Add

- [ ] Summary: total FTE + interns on patient work
- [ ] Filter: FTE / Intern / All
- [ ] Filter: Division / Department
- [ ] Filter: Role (if available)
- [ ] Table: all people (name, type, division, role, score, status)
- [ ] Chart: FTE vs interns
- [ ] Chart: Headcount by division
- [ ] Chart: By role (if available)
- [ ] Optional: scores, capacity, trends, export

Once you share the column names (and optionally a CSV sample), we can lock the data model and implement this plan in code.
