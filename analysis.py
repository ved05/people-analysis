"""
In-depth analysis: People ↔ PGs, service scores, gaps, catch-up plan.
Outputs: people_summary, pg_summary, catch_up_plan (CSV + console).
"""
import sys
import re
import os
from collections import defaultdict

try:
    import pandas as pd
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl", "-q"])
    import pandas as pd

TRACKER_PATH = r"c:\Users\catwa\Desktop\people\Copy of Divisional Meeting Updates Tracker  .xlsx"
USA_REPORT_PATH = r"c:\Users\catwa\Desktop\people\Final USA report. Scores (4).xlsx"
OUTPUT_DIR = r"c:\Users\catwa\Desktop\people\output"
ADDITIONAL_PEOPLE_PATH = os.path.join(os.path.dirname(TRACKER_PATH), "additional_people.csv")

# PG/client names to exclude when treating a cell as a "person" name
EXCLUDE_PERSON = {
    "West", "Central", "East", "Boston", "Claims", "Billing", "Audit", "CPOs",
    "Rework post audit", "Shared Billing / Claims report", "Priority Sheets ",
    "Priority Doc Prep ", "Other Important Tasks ", "9 IST", "5th Audit",
    "October", "November", "December", "August", "September", "July", "January",
    "Under Audit", "at risk", "Fair", "need to setup", "not connected", "on hold", "YES",
    "Batch 2", "Batch 3", "East central ", "Central ", "NaN", "nan",
}

# People to exclude: no status/description given (add more as needed)
EXCLUDE_PEOPLE_NO_DESCRIPTION = {
    "Bhargava", "Gagan",
}

# Phrase that marks PGs we don't send sheets to (exclude from analysis)
DONT_SEND_SHEETS_PHRASE = "dont send them sheets"  # also match "don't send"

def normalize_pg(pg):
    if pd.isna(pg) or str(pg).strip() == "":
        return None
    return str(pg).strip().lower()

def split_person_names(s):
    if pd.isna(s) or str(s).strip() == "":
        return []
    s = str(s).strip()
    if s in EXCLUDE_PERSON or s.lower() in ("nan", "ownership", "names", "pgs", "region"):
        return []
    parts = re.split(r"\s*\+\s*", s)
    out = []
    for p in parts:
        p = p.strip()
        if p and p not in EXCLUDE_PERSON and len(p) > 1:
            out.append(p)
    return out

def is_likely_person(s):
    if pd.isna(s) or str(s).strip() == "":
        return False
    s = str(s).strip()
    if s in EXCLUDE_PERSON or re.match(r"^[\d\.\-\/\s:]+$", s):
        return False
    if re.match(r"^(january|february|march|april|may|june|july|august|september|october|november|december)", s, re.I):
        return False
    return True

# ---------------------------------------------------------------------------
# TRACKER: extract (person, PG) pairs from all sheets
# ---------------------------------------------------------------------------

def parse_reworks(df):
    pairs = set()
    # Header often in row 1: Region, Names, Ownership, PGs, ...
    for r in range(2, len(df)):
        names_col = df.iloc[r, 1] if df.shape[1] > 1 else None
        ownership_col = df.iloc[r, 2] if df.shape[1] > 2 else None
        pg_col = df.iloc[r, 3] if df.shape[1] > 3 else None
        pg = normalize_pg(pg_col)
        if not pg:
            continue
        for val in [names_col, ownership_col]:
            for person in split_person_names(val):
                if person and pg:
                    pairs.add((person, pg))
    return pairs

def parse_priority_tracker(df):
    pairs = set()
    # Row 0: Region, PGs, ... Row 1: NaN, NaN, Ownership, July, Ownership, August, ...
    # PG in col 1; ownership values in cols where row 1 contains "ownership"
    if len(df) < 2:
        return pairs
    ownership_cols = []
    for c in range(df.shape[1]):
        h = str(df.iloc[1, c]).strip().lower() if df.shape[0] > 1 else ""
        if "ownership" in h:
            ownership_cols.append(c)
    for r in range(2, len(df)):
        pg = normalize_pg(df.iloc[r, 1]) if df.shape[1] > 1 else None
        if not pg:
            continue
        for c in ownership_cols:
            val = df.iloc[r, c]
            for person in split_person_names(val):
                if person and pg:
                    pairs.add((person, pg))
    return pairs

def parse_batch2(df):
    pairs = set()
    # Row 1: PG names in columns 1+; Col 0 rows 2+: people names
    if len(df) < 3 or df.shape[1] < 2:
        return pairs
    for r in range(2, len(df)):
        person_cell = df.iloc[r, 0]
        for person in split_person_names(person_cell):
            if not person:
                continue
            for c in range(1, df.shape[1]):
                pg = normalize_pg(df.iloc[1, c])
                if not pg or len(pg) < 2 or "batch" in pg:
                    continue
                pairs.add((person, pg))
    return pairs

def parse_entire_team_summary(df):
    pairs = set()
    # Try to find columns: something like Names/Ownership and PG
    # From scan, this sheet had many status columns. Look for "PG" or "pg" in header and a name-like column
    if len(df) < 2:
        return pairs
    headers = df.iloc[0].astype(str).str.lower() if len(df) > 0 else []
    pg_col = None
    name_cols = []
    for c, h in enumerate(headers):
        if "pg" in h and "health" not in h and "status" not in h:
            pg_col = c
        if "name" in h or "ownership" in h or "allocation" in h:
            name_cols.append(c)
    if pg_col is None or not name_cols:
        return pairs
    for r in range(1, len(df)):
        pg = normalize_pg(df.iloc[r, pg_col])
        if not pg:
            continue
        for nc in name_cols:
            for person in split_person_names(df.iloc[r, nc]):
                if person and pg:
                    pairs.add((person, pg))
    return pairs

def load_tracker_person_pg():
    xl = pd.ExcelFile(TRACKER_PATH)
    all_pairs = set()
    for sheet in xl.sheet_names:
        df = pd.read_excel(TRACKER_PATH, sheet_name=sheet, header=None)
        if sheet == "Reworks":
            all_pairs |= parse_reworks(df)
        elif sheet == "Priority Tracker":
            all_pairs |= parse_priority_tracker(df)
        elif "Batch" in sheet:
            all_pairs |= parse_batch2(df)
        elif "Entire Team" in sheet or "Summary" in sheet:
            all_pairs |= parse_entire_team_summary(df)
    return all_pairs

# ---------------------------------------------------------------------------
# ADDITIONAL PEOPLE (team roster: DGOS, Leads, Engineering, RPM, PreAuth, Cybersecurity)
# ---------------------------------------------------------------------------

def load_additional_people():
    """Load additional_people.csv: name -> team. Returns dict; empty if file missing."""
    out = {}
    if not os.path.isfile(ADDITIONAL_PEOPLE_PATH):
        return out
    try:
        df = pd.read_csv(ADDITIONAL_PEOPLE_PATH, encoding="utf-8")
        if "name" in df.columns and "team" in df.columns:
            for _, r in df.iterrows():
                name = str(r["name"]).strip()
                if name and name.lower() != "nan":
                    out[name] = str(r.get("team", "")).strip()
    except Exception:
        pass
    return out

# ---------------------------------------------------------------------------
# USA REPORT: PG list, scores, health status
# ---------------------------------------------------------------------------

def load_usa_master():
    df = pd.read_excel(USA_REPORT_PATH, sheet_name="USA master tracker")
    pg_col = None
    health_col = None
    score_cols = []
    divisional_col = None
    ehr_col = None
    internal_alloc_col = None
    for c in df.columns:
        s = str(c).strip().lower()
        if s == "pg":
            pg_col = c
        if "health status" in s or "pgs health" in s:
            health_col = c
        if "score" in s:
            score_cols.append(c)
        if "divisional" in s and "group" in s:
            divisional_col = c
        if s == "ehr" or "ehr name" in s:
            ehr_col = c if ehr_col is None else ehr_col
        if "internal allocation" in s:
            internal_alloc_col = c
    if pg_col is None:
        pg_col = df.columns[0]
    # Latest score column (prefer Jan 2026, then Dec 25, etc.)
    latest_score_col = None
    for name in ["Jan' 2026 score", "Jan' 2026", "Dec' 25 Score", "Dec' 25", "Nov' 25 Score"]:
        for c in df.columns:
            if name in str(c):
                latest_score_col = c
                break
        if latest_score_col is not None:
            break
    if not latest_score_col and score_cols:
        latest_score_col = score_cols[0]
    return df, pg_col, health_col, score_cols, latest_score_col, divisional_col, ehr_col, internal_alloc_col

# ---------------------------------------------------------------------------
# IN-DEPTH REPORT: one Markdown + one Excel (simple way to see everything)
# ---------------------------------------------------------------------------

def write_in_depth_report(df_people, df_pg, df_catch, people_with_capacity, no_alloc, at_risk, capacity_threshold, df_team_roster=None, df_suggested_assignments=None, df_double_risk=None, division_health_ct=None, df_score_history=None):
    """Write IN_DEPTH_ANALYSIS_REPORT.md and People_PG_Analysis_Report.xlsx."""
    md_path = os.path.join(OUTPUT_DIR, "IN_DEPTH_ANALYSIS_REPORT.md")
    excel_path = os.path.join(OUTPUT_DIR, "People_PG_Analysis_Report.xlsx")

    # ---- Glossary (plain-language definitions) ----
    glossary = """
## Glossary

| Term | Meaning |
|------|--------|
| **PG** | Physician group / client we send sheets or services to. |
| **Score** | Monthly service score (0 or 1): did we deliver on time? 1 = met, 0 = not met. |
| **Latest score** | Most recent month's score (e.g. Jan 2026 or Dec 25). |
| **Score trend** | Improving = recent months better than older; Declining = worse; Stable = similar. |
| **Health status** | PG's overall status: Good, Fair, at risk, very disappointment, might loose very less activity, not called. |
| **Gap** | This PG needs action: either no owner (assign) or at risk/low score (reinforce). |
| **No allocation** | No person assigned in the Tracker for this PG. |
| **Single owner** | Only one person assigned; if they're unavailable, PG has no backup. |
| **People with capacity** | People with few PGs (e.g. <= 1) who can take on more. |
| **Internal allocation** | From USA report: who is supposed to own this PG (may differ from Tracker). |
| **EHR** | Electronic health record: YES/NO/Not working – affects how we deliver. |
| **Division** | Divisional group (EAST, CENTRAL, WEST, EAST CENTRAL). |
"""

    # ---- Markdown report ----
    lines = []
    lines.append("# Complete In-Depth Analysis: People & PG Services")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append(f"- **People** (with at least one PG, from Tracker): **{len(df_people)}**")
    lines.append(f"- **PGs** (in scope, we send sheets): **{len(df_pg)}**")
    lines.append(f"- **PGs with NO allocation:** **{no_alloc}** – need owner(s) assigned.")
    lines.append(f"- **PGs with gap** (at risk or low score but have owners): **{at_risk}** – need reinforced support.")
    lines.append(f"- **People with capacity** (<= {int(capacity_threshold)} PG(s)): **{len(people_with_capacity)}** – can take on more PGs.")
    lines.append("")
    lines.append("**Bottom line:** Assign owners to PGs with no allocation; use people with capacity. Reinforce support for at-risk PGs.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. People Deep Dive (Tracker – people with PGs only)")
    lines.append("")
    lines.append("| Person | PG count | Workload tier | PGs |")
    lines.append("|-------|----------|---------------|-----|")
    workload_col = "workload_tier" if "workload_tier" in df_people.columns else None
    for _, r in df_people.iterrows():
        tier = r.get(workload_col, "") if workload_col else ""
        pgs_safe = str(r["pgs"]).replace("|", "; ")[:100]
        if len(str(r["pgs"])) > 100:
            pgs_safe += "..."
        lines.append(f"| {r['person']} | {r['pg_count']} | {tier} | {pgs_safe} |")
    lines.append("")
    high = (df_people["workload_tier"] == "High").sum() if "workload_tier" in df_people.columns else 0
    low = (df_people["workload_tier"] == "Low").sum() if "workload_tier" in df_people.columns else 0
    lines.append(f"- **High workload:** {high} people. **Low workload (capacity):** {low} people.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. PGs Deep Dive")
    lines.append("")
    lines.append("| PG | Owners | Health | Latest score | Score trend | Single owner? | Gap | Action |")
    lines.append("|----|--------|--------|--------------|-------------|---------------|-----|--------|")
    for _, r in df_pg.iterrows():
        owners = (str(r.get("assigned_people") or "").replace("|", "; "))[:40] + ("..." if len(str(r.get("assigned_people") or "")) > 40 else "")
        pg_safe = str(r["pg"]).replace("|", " ")[:35]
        lines.append(f"| {pg_safe} | {owners} | {r.get('health_status', '')} | {r.get('latest_score', '')} | {r.get('score_trend', '')} | {r.get('single_owner', '')} | {r.get('gap', '')} | {r.get('recommended_action', '')} |")
    lines.append("")
    single_owner_pgs = (df_pg["single_owner"] == "Yes").sum() if "single_owner" in df_pg.columns else 0
    lines.append(f"- **Single-owner PGs:** {single_owner_pgs} – consider backup coverage.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Gaps & Catch-Up Plan")
    lines.append("")
    lines.append("| Priority | PG | Current owners | Health | Gap | Recommended action |")
    lines.append("|----------|-----|----------------|--------|-----|---------------------|")
    for _, r in df_catch.iterrows():
        lines.append(f"| {r['priority']} | {r['pg']} | {r['current_owners']} | {r['health_status']} | {r['gap_description']} | {r['recommended_action']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. People With Capacity (candidates to assign)")
    lines.append("")
    for _, r in people_with_capacity.iterrows():
        pgs_safe = str(r["pgs"]).replace("|", "; ")
        lines.append(f"- **{r['person']}** – {r['pg_count']} PG(s): {pgs_safe}")
    lines.append("")
    if df_team_roster is not None and len(df_team_roster) > 0:
        lines.append("---")
        lines.append("")
        lines.append("## 6. Team Roster (DGOS, Leads, Engineering, RPM, PreAuth, Cybersecurity)")
        lines.append("")
        lines.append("| Person | Team | PG count | PGs |")
        lines.append("|--------|------|----------|-----|")
        for _, r in df_team_roster.iterrows():
            pgs_safe = str(r.get("pgs", "") or "").replace("|", "; ")[:80]
            if len(str(r.get("pgs", "") or "")) > 80:
                pgs_safe += "..."
            lines.append(f"| {r['person']} | {r['team']} | {r['pg_count']} | {pgs_safe} |")
        lines.append("")

    # Suggested assignment table (PG -> suggested owner)
    if df_suggested_assignments is not None and len(df_suggested_assignments) > 0:
        lines.append("---")
        lines.append("")
        lines.append("## 7. Suggested Assignments (Priority 1 PGs -> suggested owner)")
        lines.append("")
        lines.append("Use this to assign owners; update the Tracker with the chosen owner.")
        lines.append("")
        lines.append("| PG | Suggested owner | Current owner |")
        lines.append("|----|-----------------|---------------|")
        for _, r in df_suggested_assignments.iterrows():
            pg_safe = str(r["pg"]).replace("|", " ")[:45]
            lines.append(f"| {pg_safe} | {r.get('suggested_owner', '')} | {r.get('current_owner', '')} |")
        lines.append("")

    # Division x health cross-tab
    if division_health_ct is not None and division_health_ct.size > 0:
        lines.append("---")
        lines.append("")
        lines.append("## 8. Division x Health (count of PGs by division and health status)")
        lines.append("")
        lines.append("Rows = division, Columns = health status. Use to see where to focus.")
        lines.append("")
        ct_str = division_health_ct.to_string()
        lines.append("```")
        lines.append(ct_str[:2000] + ("..." if len(ct_str) > 2000 else ""))
        lines.append("```")
        lines.append("")

    # Double-risk PGs (single owner + at risk / very disappointment)
    if df_double_risk is not None and len(df_double_risk) > 0:
        lines.append("---")
        lines.append("")
        lines.append("## 9. Double-Risk PGs (single owner AND at risk / very disappointment)")
        lines.append("")
        lines.append("Highest priority for adding backup or reinforcing support.")
        lines.append("")
        lines.append("| PG | Current owner | Health | Latest score | Action |")
        lines.append("|----|---------------|--------|--------------|--------|")
        for _, r in df_double_risk.iterrows():
            pg_safe = str(r["pg"]).replace("|", " ")[:35]
            lines.append(f"| {pg_safe} | {r.get('current_owner', '')} | {r.get('health_status', '')} | {r.get('latest_score', '')} | {r.get('recommended_action', '')} |")
        lines.append("")

    # Score history (last 6 months) - sample first 15 PGs
    if df_score_history is not None and len(df_score_history) > 0:
        lines.append("---")
        lines.append("")
        lines.append("## 10. Score History (last 6 months) – sample")
        lines.append("")
        lines.append("Full table in score_history_last6.csv and Excel sheet.")
        lines.append("")
        cols = list(df_score_history.columns)
        lines.append("| " + " | ".join(str(c)[:12] for c in cols) + " |")
        lines.append("|" + "---|" * len(cols))
        for _, r in df_score_history.head(15).iterrows():
            row_vals = [str(r.get(c, ""))[:12] for c in cols]
            lines.append("| " + " | ".join(row_vals) + " |")
        lines.append("")

    # Glossary at end
    lines.append("---")
    lines.append("")
    lines.append(glossary.strip())
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Report generated by analysis.py. Re-run when Tracker or USA report changes.*")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Wrote {md_path}")

    # ---- Excel workbook (one file, multiple sheets) ----
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        # Sheet 1: Summary (key numbers + top actions)
        summary_data = {
            "Metric": [
                "People (with at least one PG)",
                "PGs (in scope)",
                "PGs with NO allocation",
                "PGs with gap (at risk/low score)",
                "People with capacity (can take more PGs)",
                "",
                "Top action 1",
                "Top action 2",
            ],
            "Value": [
                len(df_people),
                len(df_pg),
                no_alloc,
                at_risk,
                len(people_with_capacity),
                "",
                "Assign owners to PGs with no allocation (see Catch-up sheet).",
                "Use people with capacity to take on those PGs (see People with capacity sheet).",
            ],
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name="Summary", index=False)
        df_people.to_excel(writer, sheet_name="People", index=False)
        df_pg.to_excel(writer, sheet_name="PGs", index=False)
        df_catch.to_excel(writer, sheet_name="Catch-up plan", index=False)
        people_with_capacity.to_excel(writer, sheet_name="People with capacity", index=False)
        if df_team_roster is not None and len(df_team_roster) > 0:
            df_team_roster.to_excel(writer, sheet_name="Team roster", index=False)
        if df_suggested_assignments is not None and len(df_suggested_assignments) > 0:
            df_suggested_assignments.to_excel(writer, sheet_name="Suggested assignments", index=False)
        if division_health_ct is not None and division_health_ct.size > 0:
            division_health_ct.to_excel(writer, sheet_name="Division x Health")
        if df_double_risk is not None and len(df_double_risk) > 0:
            df_double_risk.to_excel(writer, sheet_name="Double-risk PGs", index=False)
        if df_score_history is not None and len(df_score_history) > 0:
            df_score_history.to_excel(writer, sheet_name="Score history (last 6)", index=False)
    print(f"  Wrote {excel_path}")

# ---------------------------------------------------------------------------
# BUILD SUMMARY & GAP ANALYSIS
# ---------------------------------------------------------------------------

def run_analysis():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Loading Tracker: person–PG assignments...")
    person_pg_pairs = load_tracker_person_pg()
    # Exclude people with no status/description (Bhargava, Gagan, etc.)
    person_pg_pairs = {(p, pg) for p, pg in person_pg_pairs if p not in EXCLUDE_PEOPLE_NO_DESCRIPTION}
    print(f"  Found {len(person_pg_pairs)} (person, PG) pairs (after excluding people with no description)")

    print("Loading USA master tracker...")
    df_usa, pg_col, health_col, score_cols, latest_score_col, divisional_col, ehr_col, internal_alloc_col = load_usa_master()
    usa_pgs = set()
    pg_health = {}
    pg_latest_score = {}
    pg_row = {}
    for _, row in df_usa.iterrows():
        # Skip PGs where we don't send them sheets (any cell in row contains that phrase)
        row_str = " ".join(str(v).lower() for v in row.values if pd.notna(v))
        if "dont send them sheets" in row_str or "don't send them sheets" in row_str:
            continue
        pg = normalize_pg(row.get(pg_col))
        if pg:
            usa_pgs.add(pg)
            pg_health[pg] = str(row.get(health_col, "")).strip() if health_col else ""
            pg_latest_score[pg] = row.get(latest_score_col)
            pg_row[pg] = row

    # Person -> list of PGs (normalized)
    person_to_pgs = defaultdict(set)
    pg_to_persons = defaultdict(set)
    for person, pg in person_pg_pairs:
        if person and pg:
            person_to_pgs[person].add(pg)
            pg_to_persons[pg].add(person)

    # PGs in Tracker (any PG we saw in assignments)
    tracker_pgs = set(pg_to_persons.keys())

    # Match USA PG names to Tracker (fuzzy: normalized)
    usa_pg_to_tracker = {}
    for upg in usa_pgs:
        usa_pg_to_tracker[upg] = upg
        for tpg in tracker_pgs:
            if upg == tpg or upg in tpg or tpg in upg:
                usa_pg_to_tracker[upg] = tpg
                break

    # Load additional people (team roster: DGOS, Leads, Engineering, RPM, PreAuth, Cybersecurity)
    additional_name_to_team = load_additional_people()
    if additional_name_to_team:
        print(f"  Loaded {len(additional_name_to_team)} additional people for Team roster from additional_people.csv")

    # People: ONLY Tracker-derived (people with at least one PG). Team roster people stay in Team roster tab only.
    people_rows = []
    for person in sorted(person_to_pgs.keys()):
        pgs = person_to_pgs[person]
        people_rows.append({"person": person, "pg_count": len(pgs), "pgs": " | ".join(sorted(pgs))})
    df_people = pd.DataFrame(people_rows)
    # Workload tiers (by pg_count: High = top 25%, Low = bottom 25%, Medium = rest)
    if len(df_people) > 0:
        q75 = df_people["pg_count"].quantile(0.75)
        q25 = df_people["pg_count"].quantile(0.25)
        def workload_tier(r):
            c = r["pg_count"]
            if c >= q75: return "High"
            if c <= q25: return "Low"
            return "Medium"
        df_people["workload_tier"] = df_people.apply(workload_tier, axis=1)
    else:
        df_people["workload_tier"] = []
    people_path = os.path.join(OUTPUT_DIR, "people_summary.csv")
    df_people.to_csv(people_path, index=False)
    print(f"  Wrote {people_path}")

    # Team roster: ONLY additional people (separate file for Team roster tab only)
    team_roster_rows = []
    for name, team in sorted(additional_name_to_team.items(), key=lambda x: (x[1], x[0])):
        pgs = person_to_pgs.get(name, set())
        team_roster_rows.append({
            "person": name,
            "team": team,
            "pg_count": len(pgs),
            "pgs": " | ".join(sorted(pgs)) if pgs else "",
        })
    df_team_roster = pd.DataFrame(team_roster_rows)
    team_roster_path = os.path.join(OUTPUT_DIR, "team_roster.csv")
    df_team_roster.to_csv(team_roster_path, index=False)
    print(f"  Wrote {team_roster_path}")

    # Score trend per PG (last 3 months vs previous 3 months from score_cols)
    def get_score_trend(row_series, score_cols_list):
        vals = []
        for c in score_cols_list:
            v = row_series.get(c)
            if pd.notna(v) and str(v).strip() != "":
                try:
                    vals.append(float(v))
                except (TypeError, ValueError):
                    pass
        if len(vals) < 2:
            return "Insufficient data"
        n = len(vals)
        recent = sum(vals[-3:]) / min(3, n) if n >= 1 else 0
        older = sum(vals[:3]) / min(3, n) if n >= 1 else 0
        if recent > older + 0.05:
            return "Improving"
        if recent < older - 0.05:
            return "Declining"
        return "Stable"

    # PG summary: all USA PGs + assignment + health + score + gap + in-depth fields
    pg_rows = []
    for upg in sorted(usa_pgs):
        row_series = pg_row.get(upg, pd.Series())
        display_pg = row_series.get(pg_col, upg) if isinstance(row_series, pd.Series) else upg
        if isinstance(display_pg, float) and pd.isna(display_pg):
            display_pg = upg
        persons = pg_to_persons.get(usa_pg_to_tracker.get(upg, upg), set()) or pg_to_persons.get(upg, set())
        health = pg_health.get(upg, "")
        latest = pg_latest_score.get(upg, "")
        has_allocation = len(persons) > 0
        at_risk = health and ("risk" in str(health).lower() or "disappointment" in str(health).lower() or "fair" in str(health).lower())
        low_score = latest is not None and (latest == 0 or (isinstance(latest, (int, float)) and float(latest) < 0.5))
        gap = not has_allocation or at_risk or low_score
        if not has_allocation:
            rec = "Assign owner(s)"
        elif at_risk or low_score:
            rec = "Reinforce support / catch up on services"
        else:
            rec = "Monitor"
        divisional_group = str(row_series.get(divisional_col, "")).strip() if divisional_col and isinstance(row_series, pd.Series) else ""
        ehr = str(row_series.get(ehr_col, "")).strip() if ehr_col and isinstance(row_series, pd.Series) else ""
        internal_allocation = str(row_series.get(internal_alloc_col, "")).strip() if internal_alloc_col and isinstance(row_series, pd.Series) else ""
        score_trend = get_score_trend(row_series, score_cols) if isinstance(row_series, pd.Series) else "Insufficient data"
        single_owner = "Yes" if len(persons) == 1 else "No"
        pg_rows.append({
            "pg": display_pg,
            "assigned_people": " | ".join(sorted(persons)) if persons else "",
            "pg_count": len(persons),
            "health_status": health,
            "latest_score": latest,
            "score_trend": score_trend,
            "divisional_group": divisional_group,
            "ehr": ehr,
            "internal_allocation": internal_allocation,
            "single_owner": single_owner,
            "gap": "Yes" if gap else "No",
            "recommended_action": rec,
        })
    df_pg = pd.DataFrame(pg_rows)
    pg_path = os.path.join(OUTPUT_DIR, "pg_summary.csv")
    df_pg.to_csv(pg_path, index=False)
    print(f"  Wrote {pg_path}")

    # Catch-up plan: priority list
    catch_up = []
    for row in pg_rows:
        if row["gap"] != "Yes":
            continue
        priority = 1 if not row["assigned_people"] else 2
        catch_up.append({
            "priority": priority,
            "pg": row["pg"],
            "current_owners": row["assigned_people"] or "(none)",
            "health_status": row["health_status"],
            "latest_score": row["latest_score"],
            "gap_description": "No allocation" if not row["assigned_people"] else "At risk or low score",
            "recommended_action": row["recommended_action"],
        })
    catch_up.sort(key=lambda x: (x["priority"], x["pg"]))
    df_catch = pd.DataFrame(catch_up)
    catch_path = os.path.join(OUTPUT_DIR, "catch_up_plan.csv")
    df_catch.to_csv(catch_path, index=False)
    print(f"  Wrote {catch_path}")

    # People with capacity (few PGs) for suggesting reassignment
    capacity_threshold = max(1, df_people["pg_count"].quantile(0.25)) if len(df_people) > 0 else 1
    people_with_capacity = df_people[df_people["pg_count"] <= capacity_threshold].sort_values("pg_count")
    capacity_path = os.path.join(OUTPUT_DIR, "people_with_capacity.csv")
    people_with_capacity.to_csv(capacity_path, index=False)
    print(f"  Wrote {capacity_path}")

    # Suggested assignment table: Priority 1 PGs -> suggested owner (round-robin from people with capacity)
    priority1_pgs = [r["pg"] for r in pg_rows if not r["assigned_people"]]
    capacity_list = people_with_capacity["person"].tolist()
    suggested_assignments = []
    for i, pg in enumerate(priority1_pgs):
        suggested_owner = capacity_list[i % len(capacity_list)] if capacity_list else ""
        suggested_assignments.append({"pg": pg, "suggested_owner": suggested_owner, "current_owner": ""})
    df_suggested = pd.DataFrame(suggested_assignments)
    suggested_path = os.path.join(OUTPUT_DIR, "suggested_assignments.csv")
    df_suggested.to_csv(suggested_path, index=False)
    print(f"  Wrote {suggested_path}")

    # Double-risk PGs: single owner AND (at risk or very disappointment)
    double_risk = []
    for r in pg_rows:
        if r.get("single_owner") != "Yes":
            continue
        h = str(r.get("health_status", "")).lower()
        if "risk" in h or "disappointment" in h or "fair" in h:
            double_risk.append({
                "pg": r["pg"], "current_owner": r["assigned_people"], "health_status": r["health_status"],
                "latest_score": r["latest_score"], "recommended_action": "Add backup owner; reinforce support",
            })
    df_double_risk = pd.DataFrame(double_risk)
    double_risk_path = os.path.join(OUTPUT_DIR, "double_risk_pgs.csv")
    df_double_risk.to_csv(double_risk_path, index=False)
    print(f"  Wrote {double_risk_path}")

    # Division x health cross-tab (count of PGs by division and health status)
    df_pg_for_ct = pd.DataFrame(pg_rows)
    if "divisional_group" in df_pg_for_ct.columns and "health_status" in df_pg_for_ct.columns:
        div_health = pd.crosstab(
            df_pg_for_ct["divisional_group"].fillna("(blank)"),
            df_pg_for_ct["health_status"].fillna("(blank)"),
            margins=True,
        )
        div_health_path = os.path.join(OUTPUT_DIR, "division_health_crosstab.csv")
        div_health.to_csv(div_health_path)
        print(f"  Wrote {div_health_path}")
    else:
        div_health = None

    # Score history: 6 most recent months per PG (report has newest-first, so first 6 = recent)
    if latest_score_col and latest_score_col in score_cols:
        idx = score_cols.index(latest_score_col)
        if idx < len(score_cols):
            # 6 most recent: from latest column going back; take up to 6 columns including latest
            start = max(0, idx - 5)
            last_6_score_cols = score_cols[start:min(start + 6, len(score_cols))]
            if len(last_6_score_cols) < 6 and len(score_cols) >= 6:
                last_6_score_cols = score_cols[:6]  # fallback: first 6 (newest-first report)
        else:
            last_6_score_cols = score_cols[:6] if len(score_cols) >= 6 else score_cols
    else:
        # No latest col: assume first 6 columns are most recent (typical report order)
        last_6_score_cols = score_cols[:6] if len(score_cols) >= 6 else score_cols
    score_history_rows = []
    for upg in sorted(usa_pgs):
        row_series = pg_row.get(upg, pd.Series())
        display_pg = row_series.get(pg_col, upg) if isinstance(row_series, pd.Series) else upg
        if isinstance(display_pg, float) and pd.isna(display_pg):
            display_pg = upg
        rec = {"pg": display_pg}
        for j, c in enumerate(last_6_score_cols):
            val = row_series.get(c) if isinstance(row_series, pd.Series) else None
            rec[f"month_{j+1}"] = val
        score_history_rows.append(rec)
    df_score_history = pd.DataFrame(score_history_rows)
    # Rename month_1..6 to actual column names (short)
    col_map = {f"month_{j+1}": str(last_6_score_cols[j])[:20] for j in range(len(last_6_score_cols))}
    df_score_history = df_score_history.rename(columns=col_map)
    score_hist_path = os.path.join(OUTPUT_DIR, "score_history_last6.csv")
    df_score_history.to_csv(score_hist_path, index=False)
    print(f"  Wrote {score_hist_path}")

    # In-depth report (one Markdown + one Excel) – simple way to see everything
    write_in_depth_report(
        df_people, df_pg, df_catch, people_with_capacity,
        no_alloc=len([r for r in pg_rows if not r["assigned_people"]]),
        at_risk=len([r for r in pg_rows if r["gap"] == "Yes" and r["assigned_people"]]),
        capacity_threshold=capacity_threshold,
        df_team_roster=df_team_roster,
        df_suggested_assignments=df_suggested,
        df_double_risk=df_double_risk,
        division_health_ct=div_health,
        df_score_history=df_score_history,
    )

    # Console summary
    print("\n" + "=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"  People (with at least one PG): {len(person_to_pgs)}")
    print(f"  PGs in USA report:             {len(usa_pgs)}")
    print(f"  PGs with at least one person: {len([p for p in usa_pgs if len(pg_to_persons.get(usa_pg_to_tracker.get(p, p), set()) or pg_to_persons.get(p, set())) > 0])}")
    no_alloc = len([r for r in pg_rows if not r["assigned_people"]])
    print(f"  PGs with NO allocation:        {no_alloc}")
    at_risk = len([r for r in pg_rows if r["gap"] == "Yes" and r["assigned_people"]])
    print(f"  PGs with gap (at risk/low):   {at_risk}")
    print(f"  Catch-up plan items:          {len(catch_up)}")
    print(f"  People with capacity (<={int(capacity_threshold)} PG(s)): {len(people_with_capacity)}")
    print("=" * 60)
    print("\nOutput files in:", OUTPUT_DIR)
    return df_people, df_pg, df_catch

if __name__ == "__main__":
    run_analysis()
