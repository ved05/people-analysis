# In-Depth Analysis Plan: People & Services – Get Caught Up With All PGs

## 1. Objective

- **Analyse all people** (FTE + interns) who work on patient/PG-related services.
- **Map every PG** to current service status (scores, health, allocation).
- **Identify gaps**: PGs that are under-served, behind on scores, or under-allocated.
- **Produce a catch-up plan**: who should do what so services are covered for all PGs.

---

## 2. Data Sources (Already Scanned)

| Source | What we have |
|--------|----------------|
| **Tracker** (*Copy of Divisional Meeting Updates Tracker  .xlsx*) | People names (81), **person–PG assignments** (Names/Ownership vs PGs across Reworks, Priority Tracker, Batch - 2, Entire Team Summary). |
| **USA report** (*Final USA report. Scores (4).xlsx*) | **88 PGs**, monthly service scores (0/1), **PGs health status** (Fair, at risk, Good, etc.), Internal Allocation, Workflow, EHR, etc. |

---

## 3. Analysis Dimensions

### 3.1 People analysis

- **Full list of people** (from Tracker: Names + Ownership, all sheets).
- **Per person:**
  - Which **PGs** they are assigned to (from Tracker).
  - **Workload**: number of PGs per person (and optionally per sheet/type of work).
  - **FTE vs Intern**: if we get this from a column or list later, we’ll tag it.
- **Under-/over-utilised people**:  
  - Very few PGs → potential capacity to take on more.  
  - Very many PGs → risk of not catching up on services.

### 3.2 PG / services analysis

- **Full list of PGs** (from USA master tracker).
- **Per PG:**
  - **Service scores**: monthly (Jan’25–Jan’26) and trend (improving/declining/stable).
  - **PGs health status**: at risk, Fair, Good, etc.
  - **Who is allocated**: list of people from Tracker (ownership/names).
  - **Internal Allocation** (from USA report) vs **actual people** (from Tracker): aligned or gap.
- **Gaps:**
  - PGs with **no person** assigned in Tracker but present in USA report → need allocation.
  - PGs with **low/declining scores** or **at risk** → need more or different support.
  - PGs with **low or zero recent scores** (e.g. Dec’25, Jan’26) → catch-up priority.

### 3.3 Catch-up plan (actionable output)

- **Priority 1 – PGs with no allocation:**  
  List PGs that appear in USA report but have no (or unclear) person in Tracker → assign owner(s).
- **Priority 2 – PGs at risk / low scores:**  
  List PGs by health status and recent score; suggest reinforcing allocation or adding support.
- **Priority 3 – Balance workload:**  
  People with spare capacity (few PGs) → suggest assigning them to Priority 1/2 PGs.
- **Summary table:**  
  PG | Current owner(s) | Health / recent score | Gap (Y/N) | Recommended action.

---

## 4. What We Will Build

### 4.1 Analysis script (Python)

1. **Load Tracker**  
   - Parse Reworks, Priority Tracker, Batch - 2, Entire Team Summary.  
   - Extract **(person, PG)** pairs (handle “Person A + Person B” and multiple PGs per row).

2. **Load USA report**  
   - USA master tracker: PG, Divisional Group, monthly score columns, PGs health status, Internal Allocation.  
   - Optionally: Scores sheet (Overall Score) if we can align by PG or person.

3. **Build:**
   - **Person–PG matrix**: each person → list of PGs they work on.
   - **PG–people matrix**: each PG → list of people assigned.
   - **PG scores summary**: per PG, latest score, score trend, health status.

4. **Gap logic:**
   - PG in USA report with **no person** in Tracker → “No allocation”.
   - PG with **at risk / Fair** or **recent score = 0** → “Needs catch-up”.
   - Person with **very few PGs** → “Capacity for more PGs”.

5. **Outputs:**
   - **people_summary.csv**: person, list of PGs, PG_count, role (if we have it).
   - **pg_summary.csv**: PG, assigned_people, health_status, latest_score, score_trend, gap_flag, recommended_action.
   - **catch_up_plan.csv**: PG, priority (1/2/3), current_owners, gap_description, recommended_action.
   - **Console summary**: counts (people, PGs, PGs with no allocation, PGs at risk, people with capacity).

### 4.2 Optional: Streamlit dashboard

- **Tabs:** People | PGs & services | Gaps & catch-up plan.
- **Filters:** by person, PG, health status, score range.
- **Tables:** people list with PG count; PG list with owners and scores; catch-up list.
- **Charts:** PGs per person; score distribution; PGs by health status; priority counts.
- **Export:** download CSV/Excel of any table.

---

## 5. Implementation Steps

| Step | Task | Output |
|------|------|--------|
| 1 | Parse Tracker: (person, PG) from all sheets | `person_pg_pairs` |
| 2 | Parse USA master: PG, scores, health status | `pg_master` |
| 3 | Build person→PGs and PG→people | In-memory + CSV |
| 4 | Flag PGs with no allocation; PGs at risk / low score | `pg_summary`, `catch_up_plan` |
| 5 | Identify people with capacity (few PGs) | In `people_summary` and catch-up suggestions |
| 6 | Write CSVs and console report | `output/` folder |
| 7 | (Optional) Streamlit app | Run locally |

---

## 6. Success Criteria

- Every **PG** in the USA report is either:  
  - linked to at least one person in the Tracker, or  
  - explicitly flagged as “No allocation” in the catch-up plan.
- Every **person** in the Tracker is listed with their PGs and workload.
- **Catch-up plan** lists PGs that need action (no allocation, at risk, low score) with clear recommended actions.
- Analysis is **repeatable**: re-run script when Tracker or USA report is updated.

---

## 7. Files to Create / Use

| File | Purpose |
|------|--------|
| `ANALYSIS_PLAN.md` | This plan. |
| `analysis.py` | Main script: load data, person–PG, PG scores, gaps, catch-up logic, export CSVs. |
| `scan_excel.py` | Already exists; can reuse for structure or quick scans. |
| `output/people_summary.csv` | Person, PGs, PG_count. |
| `output/pg_summary.csv` | PG, owners, health, scores, gap, action. |
| `output/catch_up_plan.csv` | Priority list for catching up services. |
| `app.py` (optional) | Streamlit dashboard. |
| `requirements.txt` | pandas, openpyxl, streamlit (if dashboard). |

---

## 8. Built

| Item | Status |
|------|--------|
| `analysis.py` | Implemented: Tracker parsing (Reworks, Priority Tracker, Batch - 2), USA master load, person–PG matrix, PG summary, gap flags, catch-up plan, people-with-capacity. |
| `output/people_summary.csv` | Person, pg_count, pgs. |
| `output/pg_summary.csv` | PG, assigned_people, health_status, latest_score, gap, recommended_action. |
| `output/catch_up_plan.csv` | Priority, PG, current_owners, gap_description, recommended_action. |
| `output/people_with_capacity.csv` | People with low PG count (candidates to assign to PGs with no allocation). |
| `app.py` (Streamlit) | Dashboard: People, PGs & services, Catch-up plan, People with capacity. |
| `requirements.txt` | pandas, openpyxl, streamlit. |

**How to run**

1. **Analysis (refresh data):**  
   `python analysis.py`  
   Writes/updates all CSVs in `output/`.

2. **Dashboard:**  
   `streamlit run app.py`  
   Open the URL shown (e.g. http://localhost:8501). Use tabs to view people, PGs, catch-up plan, and people with capacity.
