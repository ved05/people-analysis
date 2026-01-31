# People & PG Services – Analysis & Catch-up Plan

Analysis of all people (FTE + interns) and PGs (physician groups) so you can **get caught up with services for all PGs**.

## Quick start – one command, two simple outputs

1. **Run analysis** (reads Tracker + USA report; writes everything including the simple view):
   ```bash
   python analysis.py
   ```

2. **View the analysis the simple way** (no dashboard, no multiple CSVs):
   - **Open one report:** `output/IN_DEPTH_ANALYSIS_REPORT.md` – full in-depth analysis in one document (Executive Summary → People → PGs → Gaps → Catch-up → People with capacity). Read top to bottom or print to PDF.
   - **Open one workbook:** `output/People_PG_Analysis_Report.xlsx` – one Excel file with sheets: **Summary** (key numbers + top actions), **People**, **PGs**, **Catch-up plan**, **People with capacity**. Everything in one place.

3. **Optional – dashboard:**  
   ```bash
   pip install -r requirements.txt
   python -m streamlit run app.py
   ```

## What’s included

| File | Purpose |
|------|--------|
| **output/IN_DEPTH_ANALYSIS_REPORT.md** | **Simple view:** Complete in-depth analysis in one Markdown report. |
| **output/People_PG_Analysis_Report.xlsx** | **Simple view:** One Excel workbook (Summary + People + PGs + Catch-up + People with capacity). |
| **ANALYSIS_PLAN.md** | In-depth plan: people analysis, PG/services analysis, catch-up plan. |
| **analysis.py** | Main script: person–PG mapping, score trends, workload tiers, gaps, catch-up plan, report + Excel. |
| **app.py** | Streamlit dashboard (optional). |
| **output/people_summary.csv** | Each person, PG count, workload tier, PGs. |
| **output/pg_summary.csv** | Each PG, owners, health, score, score trend, divisional group, EHR, single-owner flag, gap, action. |
| **output/catch_up_plan.csv** | Priority list: PGs that need allocation or catch-up. |
| **output/people_with_capacity.csv** | People with few PGs (candidates to take on more). |
| **output/suggested_assignments.csv** | Priority 1 PGs with a suggested owner (round-robin from people with capacity). |
| **output/double_risk_pgs.csv** | PGs with single owner AND at risk/very disappointment (add backup). |
| **output/division_health_crosstab.csv** | Count of PGs by division and health status. |
| **output/score_history_last6.csv** | Last 6 months of service scores per PG. |

## Data sources

- **Tracker:** `Copy of Divisional Meeting Updates Tracker  .xlsx` (Reworks, Priority Tracker, Batch - 2, Entire Team Summary).
- **USA report:** `Final USA report. Scores (4).xlsx` (USA master tracker: PG, scores, health status).

## Updating

When Tracker or USA report changes, run:

```bash
python analysis.py
```

Then reload the dashboard (or restart `streamlit run app.py`) to see updated data.
