"""
Scan Excel files:
- Tracker: people names (Names + Ownership columns only)
- USA report: services score and PG
"""
import sys
import re

try:
    import pandas as pd
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl", "-q"])
    import pandas as pd

TRACKER_PATH = r"c:\Users\catwa\Desktop\people\Copy of Divisional Meeting Updates Tracker  .xlsx"
USA_REPORT_PATH = r"c:\Users\catwa\Desktop\people\Final USA report. Scores (4).xlsx"

# Known PG/client/org names to exclude from people list (from your data)
EXCLUDE = {
    "West", "Central", "East", "Boston", "Batch 2", "Batch 3", "East central ", "Central ",
    "Claims", "Billing", "Audit", "Rework post audit", "Shared Billing / Claims report", "CPOs",
    "Housecall MD", "Bloom", "Brownfield", "Paragon", "TTUHSC", "VPPC Nov Dec", "Rocky Mountain Nov Dec",
    "Housecall MD Oct to Dec (Claims)", "Grace At home ", "Grace at home", "9 IST", "5th Audit",
    "October", "November", "December", "August", "September", "July", "January",
    "Under Audit", "at risk", "Fair", "need to setup", "not connected with pg", "not connected", "on hold", "YES",
    "Priority Sheets ", "Priority Doc Prep ", "Other Important Tasks ",
    "UT Health", "Hyde Park Health Associates", "TruCare", "Boerne", "MD Primary Care", "Americare Medical Group",
    "Optimized", "Riverside", "BIDMC", "Caring", "Bowdoin",
    "Housecall MD - Oct ", "Bloom - Dec ", "COFMC- Nov ", "COFMC- Dec", "CNT - Nov", "CNT - Dec", "Apple MD - Dec",
    "Diversecare - Dec ", "Community First - Sept ", "Hyde Park - Oct", "ORTHOPEDICS - Oct",
    "Grace at home - Aug ", "Grace at home - sept ",
}

def split_names(s):
    if pd.isna(s) or str(s).strip() == "":
        return []
    s = str(s).strip()
    parts = re.split(r"\s*\+\s*", s)
    return [p.strip() for p in parts if p.strip()]

def extract_people_from_series(ser, exclude_dates=True):
    names = set()
    for v in ser.dropna().astype(str):
        v = v.strip()
        if not v or v.lower() in ("nan", "ownership", "names", "region", "pgs", "months", "deadline", "remarks", "audit round"):
            continue
        if re.match(r"^[\d\.\-\/\s:]+$", v) and exclude_dates:  # dates/times
            continue
        if re.match(r"^(january|february|march|april|may|june|july|august|september|october|november|december)", v, re.I):
            continue
        if " + " in v or "+" in v:
            for p in split_names(v):
                if p not in EXCLUDE and len(p) > 1:
                    names.add(p)
        else:
            if v not in EXCLUDE and len(v) > 1:
                names.add(v)
    return names

def scan_tracker():
    print("=" * 60)
    print("PEOPLE NAMES – Copy of Divisional Meeting Updates Tracker")
    print("(from 'Names' and 'Ownership' columns only)")
    print("=" * 60)
    xl = pd.ExcelFile(TRACKER_PATH)
    all_people = set()
    for sheet in xl.sheet_names:
        df = pd.read_excel(TRACKER_PATH, sheet_name=sheet, header=None)
        for c in range(min(20, df.shape[1])):
            # Header can be in row 0 or 1 (e.g. Reworks has "Names" in row 1)
            first = (str(df.iloc[0, c]).strip().lower() if df.shape[0] > 0 else "")
            second = (str(df.iloc[1, c]).strip().lower() if df.shape[0] > 1 else "")
            if first not in ("names", "ownership") and second not in ("names", "ownership"):
                continue
            header_row = 1 if second in ("names", "ownership") else 0
            col_vals = df.iloc[header_row + 1:, c]  # skip header row(s)
            names = extract_people_from_series(col_vals)
            all_people.update(names)
    # Also Batch - 2: first column has names (Madhuluta, Priti, Ananya, Baistami)
    df_b2 = pd.read_excel(TRACKER_PATH, sheet_name="Batch - 2", header=None)
    if df_b2.shape[1] > 0:
        names = extract_people_from_series(df_b2.iloc[1:, 0])
        for n in names:
            if n not in EXCLUDE and len(n) > 1 and not re.match(r"^Batch", n, re.I):
                all_people.add(n)
    all_people = sorted([p for p in all_people if p not in EXCLUDE])
    print("\nUnique people names:")
    for i, name in enumerate(all_people, 1):
        print(f"  {i:2}. {name}")
    print(f"\nTotal: {len(all_people)} people")
    return all_people

def scan_usa_report():
    print("\n" + "=" * 60)
    print("SERVICES SCORE & PG – Final USA report. Scores (4)")
    print("=" * 60)
    xl = pd.ExcelFile(USA_REPORT_PATH)
    df_master = pd.read_excel(USA_REPORT_PATH, sheet_name="USA master tracker")
    print("\n--- PG (USA master tracker) ---")
    pg_col = [c for c in df_master.columns if str(c).strip().lower() == "pg"][0]
    pgs = df_master[pg_col].dropna().unique().tolist()
    for i, pg in enumerate(sorted(pgs), 1):
        print(f"  {i:2}. {pg}")
    print(f"\nTotal PGs: {len(pgs)}")
    print("\n--- SCORES (USA master tracker) ---")
    score_cols = [c for c in df_master.columns if "score" in str(c).lower()]
    print("Score columns:", score_cols)
    print("\nMonthly score columns (0/1): e.g. \"Jan' 2026 score\", \"Dec' 25 Score\", \"Nov' 25 Score\", ...")
    print("Sample (Dec' 25 Score):", df_master["Dec' 25 Score"].dropna().tolist()[:15])
    print("\n--- Overall Score (Scores sheet) ---")
    df_scores = pd.read_excel(USA_REPORT_PATH, sheet_name="Scores")
    if "Overall Score" in df_scores.columns:
        print("Overall Score sample:", df_scores["Overall Score"].dropna().tolist()[:15])
    print("\n(No column named 'Services Score' found; monthly scores and Overall Score are available.)")

if __name__ == "__main__":
    scan_tracker()
    scan_usa_report()
