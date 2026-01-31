# What We Have vs What We Can Add to the In-Depth Analysis

This document lists **what the in-depth analysis already does** and **what we can add** to make it deeper and more actionable. Pick what you want; we can implement in steps.

---

## Part 1: What We Already Have

| Area | What we do today |
|------|-------------------|
| **People** | List of 67 people with PG count, workload tier (High/Medium/Low), list of PGs. |
| **PGs** | Each PG: owners, health status, latest score, score trend (Improving/Stable/Declining), division, EHR, internal allocation, single-owner flag, gap, recommended action. |
| **Catch-up plan** | Priority 1 (no owner – assign) and Priority 2 (at risk/low score – reinforce). |
| **People with capacity** | 18 people with ≤1 PG as candidates to assign. |
| **Team roster** | Separate list of DGOS, Leads, Engineering, RPM, PreAuth, Cybersecurity (29 people). |
| **In-depth report** | Executive summary, breakdown by division, by health status, risk analysis (single-owner PGs, high-workload people, “very disappointment” PGs), capacity vs demand, Priority 1/2 lists, 5-step action plan. |
| **Outputs** | CSVs (people_summary, pg_summary, catch_up_plan, people_with_capacity, team_roster), Markdown report, Excel workbook, Streamlit dashboard. |

---

## Part 2: What We Can Add (Ideas)

Choose what matters most; we can add in phases.

---

### A. Score history and trends

| Add | What it would do | Why useful |
|-----|------------------|------------|
| **Monthly score table per PG** | Show last 6–12 months of scores (0/1) for each PG in the report or a new sheet. | See which PGs have been 0 for many months (chronic catch-up) vs recently slipped. |
| **Chronic zero score** | Flag PGs with latest 3 months all 0. | Prioritise PGs that have been behind for a long time. |
| **Recently improved** | Flag PGs that went from 0 to 1 in the latest month. | See what’s working and recognise progress. |

---

### B. EHR and internal allocation

| Add | What it would do | Why useful |
|-----|------------------|------------|
| **Breakdown by EHR** | Count PGs by EHR status (YES / NO / Not working). Show no-owner and at-risk counts per EHR. | Focus on “No EHR” or “Not working” PGs separately. |
| **Internal allocation vs Tracker** | Compare USA “Internal Allocation” with Tracker owners; flag mismatch (e.g. USA says “John” but Tracker has “Jane”). | Align USA report and Tracker. |
| **Automation status** | Which PGs are “Automated” or “Not allocated” in USA – still need a person or not? | Avoid assigning people where automation is intended. |

---

### C. Workload and assignment

| Add | What it would do | Why useful |
|-----|------------------|------------|
| **Suggested assignment table** | One table: PG (no owner) → suggested owner from “people with capacity” (e.g. by division or load). | Copy-paste into Tracker; faster allocation. |
| **Reassignment suggestions** | “Move PG X from Person A (overloaded) to Person B (capacity).” | Rebalance workload. |
| **Division-based suggestion** | When suggesting owner for a PG, prefer people already in same division (if we have division for people). | Keeps ownership aligned to geography/team. |
| **Workload inequality** | Simple measure (e.g. max PG count vs min, or spread). | Track if workload is becoming more even over time. |

---

### D. Risk and alerts

| Add | What it would do | Why useful |
|-----|------------------|------------|
| **Double-risk PGs** | Flag: single owner **and** (at risk or very disappointment). | Highest priority for backup or reinforcement. |
| **Person at burnout risk** | Flag people who own many “at risk” or “very disappointment” PGs. | Support overloaded people. |
| **PGs with no EHR / Not working** | List and count. | Different action (e.g. fix EHR before adding owner). |
| **Alert summary** | One short list: “This week focus on: [5–10 items].” | Quick focus list for meetings. |

---

### E. Team roster and capacity

| Add | What it would do | Why useful |
|-----|------------------|------------|
| **Team roster as potential owners** | Show that 29 team roster people have 0 PGs; suggest “If added to Tracker, they can take Priority 1 PGs.” | Use DGOS/Leads/Engineering etc. for allocation if you decide to. |
| **Capacity by team** | If we add team to Tracker people later: “X people with capacity in Division Y.” | Plan by team. |

---

### F. Progress and targets

| Add | What it would do | Why useful |
|-----|------------------|------------|
| **Targets** | e.g. “Target: 0 PGs with no allocation; &lt;10 at risk.” | Track progress vs goal. |
| **Before/after snapshot** | When you re-run after assigning: “Previously 37 no owner, now X.” | See impact of actions. |
| **Simple progress table** | Columns: Metric, Last run, This run, Target (e.g. no allocation 37→20→0). | One place to see improvement. |

---

### G. Process and clarity

| Add | What it would do | Why useful |
|-----|------------------|------------|
| **Glossary** | Short definitions: score (0/1), health status values, gap, internal allocation, EHR. | New readers understand the report. |
| **What to do when** | e.g. “New PG in USA report → add to Tracker and assign owner”; “Person leaves → reassign their PGs.” | Clear process. |
| **Weekly/monthly checklist** | “Each week: 1) Run analysis 2) Review no-allocation list 3) Update Tracker.” | Keeps the analysis in use. |

---

### H. Export and workflow

| Add | What it would do | Why useful |
|-----|------------------|------------|
| **Suggested assignments Excel** | One sheet: PG, division, suggested owner, current owner (blank). | Hand to ops to update Tracker. |
| **Division × health cross-tab** | Table: rows = division, columns = health status, cells = count. | See e.g. “CENTRAL has 5 very disappointment.” |
| **Dashboard filters** | Filter by division, health, EHR in the Streamlit app. | Drill down without opening CSV. |

---

## Part 3: Suggested order to add

If you want to extend step by step:

1. **Quick wins**  
   - Suggested assignment table (PG → suggested owner).  
   - Glossary.  
   - Division × health cross-tab.

2. **Next**  
   - Monthly score table (last 6 months per PG).  
   - Double-risk PGs (single owner + at risk/very disappointment).  
   - Alert summary (“Focus this week”).

3. **Later**  
   - EHR breakdown and internal allocation vs Tracker.  
   - Targets and before/after progress.  
   - Weekly checklist and “what to do when”.

---

## Part 4: What do you want to add?

Tell me which of these you want first, for example:

- “Add suggested assignment table and glossary.”  
- “Add score history (last 6 months) and double-risk PGs.”  
- “Add everything in Quick wins.”

Then we can implement those in the analysis and report.
