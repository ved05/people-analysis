# Understanding the In-Depth Analysis & Your Action Plan

This document explains **what the analysis is**, **what every output means**, and **exactly what to do next** (your in-depth action plan).

---

## Part 1: What Is the “In-Depth Analysis”?

### The goal

You have:

- **People** (FTE + interns) who work on **PGs** (physician groups / clients) and send them **services** (e.g. sheets, claims, billing).
- **PGs** listed in the USA report; each PG has **scores** (did we deliver on time?) and **health status** (e.g. Good, Fair, at risk).

The analysis answers:

1. **Who works on what?** – Which people are assigned to which PGs (from your Tracker).
2. **Which PGs are covered?** – Which PGs have at least one person; which have **none**.
3. **Which PGs are struggling?** – At risk, Fair, or low/zero recent score but we do have owners.
4. **Who has capacity?** – People with few PGs who could take on more.
5. **What should we do?** – A **catch-up plan**: assign owners where missing, reinforce support where at risk.

So: **“In-depth analysis” = one clear picture of people ↔ PGs ↔ scores/health, plus a prioritized list of actions to get services caught up for all PGs.**

---

## Part 2: Where Does the Data Come From?

| Source | What we use |
|--------|-------------|
| **Tracker** (*Copy of Divisional Meeting Updates Tracker*) | Who is assigned to which PG (Names, Ownership, PGs) across Reworks, Priority Tracker, Batch - 2, etc. |
| **USA report** (*Final USA report. Scores (4)* – sheet “USA master tracker”) | List of PGs, monthly service scores (0/1), PGs health status (Good, Fair, at risk, etc.), divisional group, EHR, internal allocation. |
| **additional_people.csv** | Your team roster (DGOS, Leads, Engineering, RPM, PreAuth, Cybersecurity) – used **only** in the **Team roster** tab/file. |

We **exclude**:

- PGs where we “don’t send them sheets” (so we don’t plan work for them).
- People with no status/description (e.g. Bhargava, Gagan) from the main People list.

---

## Part 3: What Each Output Means (In Simple Terms)

### 3.1 People (Tracker only)

- **Who:** Everyone who has **at least one PG** assigned in the Tracker.
- **What you see:** Person name, how many PGs they have, workload tier (High / Medium / Low), list of PGs.
- **Why it matters:** So you know who is doing PG work and who is overloaded (High) vs has capacity (Low).

### 3.2 PGs (USA report – in scope)

- **Who:** Every PG we **do** send sheets to (we excluded “don’t send them sheets”).
- **What you see:** PG name, who is assigned (from Tracker), health status, latest score, score trend (Improving / Stable / Declining), single owner? (Yes/No), gap (Yes/No), recommended action.
- **Why it matters:** So you see which PGs have no owner, which are at risk or low score, and which are stable.

### 3.3 Gaps

- **“Gap” = this PG needs action.**
- **Two types:**
  1. **No allocation** – No person assigned in the Tracker → we need to **assign owner(s)**.
  2. **At risk or low score** – We have owners, but health is Fair/at risk or recent score is 0/low → we need to **reinforce support** or catch up on services.

### 3.4 Catch-up plan

- **What it is:** A **priority list** of all PGs that have a gap (need action).
- **Priority 1:** PGs with **no** owner → “Assign owner(s)”.
- **Priority 2:** PGs with owners but **at risk or low score** → “Reinforce support / catch up on services”.
- **Why it matters:** This is your **to-do list** to get every PG covered and services caught up.

### 3.5 People with capacity

- **Who:** People (from Tracker) who have **few PGs** (e.g. ≤ 1) so they could take on more.
- **Why it matters:** These are the **candidates** to assign to PGs that have no allocation (Priority 1).

### 3.6 Team roster

- **Who:** Only the people from **additional_people.csv** (DGOS, Leads, Engineering, RPM, PreAuth, Cybersecurity).
- **What you see:** Person, team, PG count (if any from Tracker), PGs (if any).
- **Why it matters:** Separate view of your internal teams; they do **not** appear in the main “People” list.

### 3.7 Key numbers (example from a typical run)

- **People (with at least one PG):** 67 → people actually assigned to PGs in the Tracker.
- **PGs (in scope):** 70 → PGs we send sheets to.
- **PGs with NO allocation:** 37 → **37 PGs have no one assigned** → top priority to assign owners.
- **PGs with gap (at risk/low):** 33 → 33 PGs have owners but need reinforced support.
- **People with capacity (e.g. ≤ 1 PG):** 18 → 18 people can be given more PGs (e.g. to cover the 37 with no allocation).

---

## Part 4: In-Depth Action Plan (Step-by-Step)

Use this as your **master action plan**. Do it in order; revisit after you assign people and update the Tracker.

---

### Phase 1: Fix “No allocation” (Priority 1)

**Goal:** Every PG that we send sheets to has at least one owner in the Tracker.

1. **Open** `output/catch_up_plan.csv` (or the **Catch-up plan** tab in the dashboard / **Catch-up plan** sheet in the Excel report).
2. **Filter** to **Priority 1** (PGs with no allocation).
3. **List** those PGs (e.g. 37). For each PG, decide:
   - Who will be the **primary owner** (and optional backup).
4. **Use “People with capacity”** (`output/people_with_capacity.csv` or that tab/sheet):
   - Match PGs with no owner to people who have capacity (few PGs).
   - Prefer people with 0 or 1 PG to balance workload.
5. **Update the Tracker** (Names/Ownership vs PGs) so every Priority-1 PG now has at least one person.
6. **Re-run** `python analysis.py` and check that “PGs with NO allocation” goes down (aim for 0).

**Output:** A list like: “PG X → assign to Person A; PG Y → assign to Person B; …” and an updated Tracker.

---

### Phase 2: Fix “At risk / low score” (Priority 2)

**Goal:** PGs that have owners but are Fair/at risk or have low/zero recent score get extra support so services catch up.

1. **In the same catch-up plan**, focus on **Priority 2** (at risk or low score).
2. **For each such PG** (e.g. 33):
   - Check **health status** and **latest score** in the PG summary.
   - Decide: do we need a **second person** (backup), **more time** from the current owner, or **process/automation** help?
3. **If you add a second person:** pick from “People with capacity” or from Team roster (if they will be added to the Tracker for that PG).
4. **Update the Tracker** (and any process/timeline) accordingly.
5. **Re-run** the analysis and track that “PGs with gap (at risk/low)” and low scores reduce over time.

**Output:** For each at-risk PG: “Add Person B as backup” or “Owner to focus on catch-up by [date]” or “Process change: …”.

---

### Phase 3: Balance workload (optional but recommended)

**Goal:** No one is overloaded (too many PGs) and people with capacity are used fairly.

1. **Open** the **People** list (Tracker only).
2. **Flag “High” workload** people (top 25% by PG count). Consider:
   - Moving 1–2 PGs to someone with capacity, or
   - Adding a backup owner for their PGs (so single-owner PGs get a second person).
3. **Use “People with capacity”** so that after Phase 1 and 2, workload is more even.
4. **Re-run** the analysis and check that:
   - “PGs with NO allocation” = 0.
   - Number of “High” workload people and “at risk” PGs is acceptable to you.

**Output:** A short list of reassignments (PG X from Person A to Person B) and/or backup owners.

---

### Phase 4: Keep it updated (ongoing)

- **When the Tracker or USA report changes:** run `python analysis.py` again.
- **Review** at least monthly:
  - Executive summary (PGs with no allocation, PGs with gap, people with capacity).
  - Catch-up plan (Priority 1 and 2).
- **Use** the same files/tabs/sheets:
  - **People** = who works on PGs (Tracker only).
  - **PGs** = status and score trend of each PG.
  - **Catch-up plan** = your prioritized action list.
  - **People with capacity** = who can take new PGs.
  - **Team roster** = your internal teams (separate from People).

---

## Part 5: One-Page Summary

| Question | Answer |
|----------|--------|
| What is the in-depth analysis? | A single picture: who is on which PG, which PGs have no owner or are at risk, who has capacity, and what to do first. |
| Where do I look? | `output/IN_DEPTH_ANALYSIS_REPORT.md` or `output/People_PG_Analysis_Report.xlsx` (Summary + People + PGs + Catch-up plan + People with capacity + Team roster). |
| What do I do first? | Assign owners to all **Priority 1** PGs (no allocation) using “People with capacity” and update the Tracker. |
| What do I do next? | For **Priority 2** PGs (at risk/low score), add backup or focus catch-up; balance workload if needed. |
| How do I know I’m done? | Re-run `python analysis.py`. Target: 0 PGs with no allocation; fewer at-risk/low-score PGs; workload acceptable. |

---

## Part 6: Quick Reference – Files and Tabs

| What you want | Where to look |
|---------------|----------------|
| One full story (read or print) | `output/IN_DEPTH_ANALYSIS_REPORT.md` |
| One Excel with all sheets | `output/People_PG_Analysis_Report.xlsx` |
| Just people with PGs (Tracker) | **People** tab/sheet or `output/people_summary.csv` |
| Just PGs and their status | **PGs** tab/sheet or `output/pg_summary.csv` |
| My to-do list (what to fix) | **Catch-up plan** tab/sheet or `output/catch_up_plan.csv` |
| Who can take more PGs | **People with capacity** tab/sheet or `output/people_with_capacity.csv` |
| DGOS, Leads, Engineering, etc. | **Team roster** tab/sheet or `output/team_roster.csv` |

If you want, we can next turn this into a **short checklist** (e.g. a single page you print and tick off each week) or add a **glossary** of terms (PG, gap, score trend, etc.) in the same file.
