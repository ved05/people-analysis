"""
Streamlit dashboard: People & PG analysis, catch-up plan.
Run: streamlit run app.py
For multiple viewers: run on a shared machine and share the Network URL (see DEPLOY.md).
"""
import os
import streamlit as st
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
# Fallback when app dir is read-only (e.g. Streamlit Cloud): read from /tmp
OUTPUT_DIR_FALLBACK = "/tmp/people-analysis/output"

def _run_analysis_in_process():
    """Run analysis in the same process; pass PROJECT_DIR so output is written where the app reads it."""
    import io
    import sys
    old_stdout, old_stderr = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
        import analysis
        analysis.run_analysis(base_dir=PROJECT_DIR)
        out_path = os.path.join(PROJECT_DIR, "output", "people_summary.csv")
        if os.path.isfile(out_path):
            return True, None
        # App dir may be read-only on Streamlit Cloud – write to /tmp and app will read from there
        os.makedirs("/tmp/people-analysis", exist_ok=True)
        analysis.run_analysis(base_dir="/tmp/people-analysis")
        fallback_path = os.path.join(OUTPUT_DIR_FALLBACK, "people_summary.csv")
        if os.path.isfile(fallback_path):
            return True, None
        return False, f"Output not found at {out_path} or {fallback_path} (app dir may be read-only)."
    except Exception as e:
        return False, str(e)
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr

def main():
    st.set_page_config(page_title="People & PG Analysis", layout="wide")
    st.title("People & PG Services – Catch-up Analysis")

    # Use fallback output dir when app dir is read-only (e.g. Streamlit Cloud)
    if os.path.isfile(os.path.join(OUTPUT_DIR_FALLBACK, "people_summary.csv")):
        out_dir = OUTPUT_DIR_FALLBACK
    else:
        out_dir = OUTPUT_DIR

    people_path = os.path.join(out_dir, "people_summary.csv")
    pg_path = os.path.join(out_dir, "pg_summary.csv")
    catch_path = os.path.join(out_dir, "catch_up_plan.csv")
    capacity_path = os.path.join(out_dir, "people_with_capacity.csv")
    team_roster_path = os.path.join(out_dir, "team_roster.csv")
    suggested_path = os.path.join(out_dir, "suggested_assignments.csv")
    double_risk_path = os.path.join(out_dir, "double_risk_pgs.csv")
    div_health_path = os.path.join(out_dir, "division_health_crosstab.csv")
    score_history_path = os.path.join(out_dir, "score_history_last6.csv")

    if not os.path.exists(out_dir) or not os.path.exists(people_path):
        import glob
        tracker_candidates = glob.glob(os.path.join(PROJECT_DIR, "Copy of Divisional Meeting Updates Tracker*.xlsx"))
        usa_candidates = glob.glob(os.path.join(PROJECT_DIR, "Final USA report*.xlsx"))
        data_ready = bool(tracker_candidates and usa_candidates)
        if data_ready and st.session_state.get("_analysis_auto_run") is None:
            st.session_state["_analysis_auto_run"] = True
            with st.spinner("Running analysis (first load)..."):
                ok, err = _run_analysis_in_process()
            if ok:
                st.rerun()
            else:
                st.session_state["_analysis_auto_run"] = False
                if err:
                    st.error(err)
        if not os.path.exists(OUTPUT_DIR) or not os.path.exists(people_path):
            st.warning("No analysis output yet. Data files found: run analysis to generate `output/`." if data_ready else "No analysis output yet. Add Tracker and USA report Excel files, then run analysis.")
            if st.button("Run analysis now"):
                ok, err = _run_analysis_in_process()
                if ok:
                    st.success("Analysis complete. Refreshing...")
                    st.rerun()
                else:
                    st.error(err or "Analysis failed.")
            return

    # Sidebar: Refresh data (run analysis so updates to Tracker/USA report show for everyone)
    with st.sidebar:
        st.subheader("Data")
        if os.path.exists(people_path):
            mtime = os.path.getmtime(people_path)
            st.caption(f"Last updated: {datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')}")
        if st.button("Refresh data (run analysis)", type="primary", use_container_width=True):
            with st.spinner("Running analysis..."):
                ok, err = _run_analysis_in_process()
            if ok:
                st.success("Done. Reloading...")
                st.rerun()
            else:
                st.error(err or "Analysis failed.")
        st.caption("Click after updating Tracker or USA report so everyone sees the latest data.")

    import pandas as pd
    df_people = pd.read_csv(people_path)
    df_pg = pd.read_csv(pg_path)
    df_catch = pd.read_csv(catch_path)
    df_capacity = pd.read_csv(capacity_path) if os.path.exists(capacity_path) else None

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("People (with PGs)", len(df_people))
    with col2:
        st.metric("PGs (USA report)", len(df_pg))
    with col3:
        no_alloc = (df_pg["assigned_people"].fillna("") == "").sum()
        st.metric("PGs with no allocation", no_alloc)
    with col4:
        st.metric("Catch-up plan items", len(df_catch))

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "People", "PGs & services", "Catch-up plan", "People with capacity", "Team roster",
        "Suggested assignments", "Double-risk PGs", "Division x Health", "Score history",
    ])

    with tab1:
        st.subheader("People and their PGs")
        filter_person = st.text_input("Filter by person name", key="p")
        if filter_person:
            df_people = df_people[df_people["person"].str.contains(filter_person, case=False, na=False)]
        st.dataframe(df_people, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("PGs: owners, health, score, gap")
        filter_pg = st.text_input("Filter by PG", key="pg")
        filter_gap = st.selectbox("Gap", ["All", "Yes", "No"], key="gap")
        df_display = df_pg.copy()
        if filter_pg:
            df_display = df_display[df_display["pg"].astype(str).str.contains(filter_pg, case=False, na=False)]
        if filter_gap != "All":
            df_display = df_display[df_display["gap"] == filter_gap]
        st.dataframe(df_display, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Catch-up plan (priority actions)")
        priority = st.selectbox("Priority", ["All", "1 - No allocation", "2 - At risk/low score"], key="pri")
        df_c = df_catch.copy()
        if priority == "1 - No allocation":
            df_c = df_c[df_c["priority"] == 1]
        elif priority == "2 - At risk/low score":
            df_c = df_c[df_c["priority"] == 2]
        st.dataframe(df_c, use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("People with capacity (can take more PGs)")
        if df_capacity is not None and len(df_capacity) > 0:
            st.dataframe(df_capacity, use_container_width=True, hide_index=True)
        else:
            st.info("No capacity file or empty. Run analysis.py.")

    with tab5:
        st.subheader("Team roster (DGOS, Leads, Engineering, RPM, PreAuth, Cybersecurity)")
        if os.path.exists(team_roster_path):
            df_roster = pd.read_csv(team_roster_path)
            if len(df_roster) > 0:
                team_filter = st.selectbox("Filter by team", ["All"] + sorted(df_roster["team"].dropna().unique().tolist()), key="team")
                if team_filter != "All":
                    df_roster = df_roster[df_roster["team"] == team_filter]
                st.dataframe(df_roster, use_container_width=True, hide_index=True)
            else:
                st.info("Team roster is empty. Add people in additional_people.csv and run analysis.py.")
        else:
            st.info("No team roster file. Add additional_people.csv and run analysis.py.")

    with tab6:
        st.subheader("Suggested assignments (Priority 1 PGs -> suggested owner)")
        if os.path.exists(suggested_path):
            df_sug = pd.read_csv(suggested_path)
            st.dataframe(df_sug, use_container_width=True, hide_index=True)
        else:
            st.info("Run analysis.py to generate suggested_assignments.csv.")

    with tab7:
        st.subheader("Double-risk PGs (single owner + at risk / very disappointment)")
        if os.path.exists(double_risk_path):
            df_dr = pd.read_csv(double_risk_path)
            st.dataframe(df_dr, use_container_width=True, hide_index=True)
        else:
            st.info("Run analysis.py to generate double_risk_pgs.csv.")

    with tab8:
        st.subheader("Division x Health (count of PGs by division and health)")
        if os.path.exists(div_health_path):
            df_dh = pd.read_csv(div_health_path, index_col=0)
            st.dataframe(df_dh, use_container_width=True)
        else:
            st.info("Run analysis.py to generate division_health_crosstab.csv.")

    with tab9:
        st.subheader("Score history (last 6 months)")
        if os.path.exists(score_history_path):
            df_sh = pd.read_csv(score_history_path)
            st.dataframe(df_sh, use_container_width=True, hide_index=True)
        else:
            st.info("Run analysis.py to generate score_history_last6.csv.")

    st.caption("Data from Tracker + USA report. After updating Tracker or USA report, click **Refresh data** in the sidebar so everyone sees the latest.")

if __name__ == "__main__":
    main()
