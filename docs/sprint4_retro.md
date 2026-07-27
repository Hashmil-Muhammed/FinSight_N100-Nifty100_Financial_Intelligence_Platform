# 🔄 Sprint 4 Retrospective: Dashboard Development

**Sprint Goal:** Develop a 9-screen interactive Streamlit dashboard integrating database tables, visualizations, and dynamic filtering.

## 🟢 What Went Well?
* **Successful Multi-page App Creation:** Effectively structured the app using Streamlit's multi-page capability with a centralized sidebar for navigation and global filters.
* **Complex Visualizations:** Successfully integrated advanced Plotly charts, including interactive Treemaps (Capital Allocation), Bubble Charts (Sector Analysis), and Radar Charts (Peer Comparison).
* **Robust Error Handling:** Designed a safe fallback mechanism (`clean_id` functions, `fillna`, and `st.warning`) to prevent app crashes when querying tables with missing or null data.
* **File Exports:** Successfully implemented one-click CSV export functionality for calculated metrics and valuation flags.

## 🔴 Blockers & Challenges
* **Database Inconsistencies:** Faced `OperationalError` due to mismatched table names (e.g., `annual_reports` vs `documents`) and duplicated primary keys.
* **Data Type Mismatches:** Date columns were inconsistently formatted (e.g., `'2012-12'` instead of integer years), which initially broke historical trend charts.
* **Streamlit UI Updates:** Faced deprecation warnings for `use_container_width=True` in dataframes, which required updating the codebase to the newer `width="stretch"` standard.

## 💡 Key Learnings
* **Dynamic Merging:** Learned the importance of safely merging historical datasets on both `company_id` and `year` to prevent data duplication and distorted charts.
* **CSS in Streamlit:** Learned how to inject custom CSS via `st.markdown` to fix sidebar overflow issues and wrap long text labels seamlessly.
* **Data Cleaning at Scale:** Realized the critical need for dynamic column mapping (using regex and substrings) to handle slight variations in column names across different tables.