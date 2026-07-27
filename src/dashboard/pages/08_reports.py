import streamlit as st
import pandas as pd
import sys
import os

# Path Setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from dashboard.utils.db import load_data


def render_annual_reports():
    st.set_page_config(page_title="Annual Reports", page_icon="📄", layout="wide")
    st.title("📄 Annual Reports (BSE)")
    st.markdown(
        "View and download the annual reports of NIFTY 100 companies. Missing reports are highlighted with badges."
    )
    st.markdown("---")

    # 1. Fetch Data Directly from the Correct Tables
    try:
        df_comp = load_data("SELECT id, company_name FROM companies")
        df_rep = load_data("SELECT * FROM documents")
    except Exception as e:
        st.error(
            f"Error fetching data from database. Make sure the 'documents' table exists. Error: {e}"
        )
        return

    # 2. Standardize IDs (THE FIX FOR AttributeError)
    def clean_id(df):
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.copy()

        df.columns = [str(c).lower().strip() for c in df.columns]
        df = df.loc[:, ~df.columns.duplicated()]

        if "id" in df.columns and "company_id" in df.columns:
            df = df.drop(columns=["id"])
        elif "id" in df.columns:
            df.rename(columns={"id": "company_id"}, inplace=True)

        if "company_id" in df.columns:
            if isinstance(df["company_id"], pd.DataFrame):
                df["company_id"] = df["company_id"].iloc[:, 0]

            df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()

        return df

    df_comp = clean_id(df_comp)
    df_rep = clean_id(df_rep)

    # 3. Safe Merge
    if "company_id" in df_comp.columns and "company_id" in df_rep.columns:
        df = pd.merge(df_comp, df_rep, on="company_id", how="left")
        df = df.loc[:, ~df.columns.duplicated()]
    else:
        st.error("Data mapping failed due to missing company_id keys.")
        return

    # 4. Column Mapping dynamically
    df.columns = [str(c).lower() for c in df.columns]
    year_col = next((c for c in df.columns if "year" in c), None)
    pdf_col = next(
        (
            c
            for c in df.columns
            if "annual_report" in c
            or "pdf" in c
            or "link" in c
            or "url" in c
            or "bse" in c
        ),
        None,
    )

    if not year_col:
        df["year"] = "N/A"
        year_col = "year"
    if not pdf_col:
        df["pdf_link"] = None
        pdf_col = "pdf_link"

    df[year_col] = (
        df[year_col].fillna("N/A").astype(str).str.replace(".0", "", regex=False)
    )

    # 5. Badge Assignment for Missing Reports
    def get_status_badge(link):
        if (
            pd.isna(link)
            or str(link).strip() == ""
            or str(link).lower() in ["none", "nan", "n/a"]
        ):
            return "🔴 Missing Report"
        return "🟢 Available"

    df["status"] = df[pdf_col].apply(get_status_badge)

    display_df = df[["company_name", year_col, "status", pdf_col]].copy()
    display_df.columns = ["Company Name", "Financial Year", "Status", "BSE PDF Link"]

    # 6. Streamlit Side filters
    col1, col2 = st.columns([1, 2])
    with col1:
        companies_list = ["All Companies"] + sorted(
            display_df["Company Name"].dropna().unique().tolist()
        )
        selected_company = st.selectbox("🔍 Filter by Company Name:", companies_list)
    with col2:
        status_filter = st.radio(
            "Filter by Report Status:",
            ["All", "🟢 Available", "🔴 Missing Report"],
            horizontal=True,
        )

    if selected_company != "All Companies":
        display_df = display_df[display_df["Company Name"] == selected_company]
    if status_filter != "All":
        display_df = display_df[display_df["Status"] == status_filter]

    # 7. Render Interactive Data Table
    st.subheader(f"Annual Reports List ({len(display_df)} records found)")
    st.dataframe(
        display_df,
        use_container_width=True,
        column_config={
            "BSE PDF Link": st.column_config.LinkColumn(
                "BSE PDF Link",
                display_text="View PDF",
                help="Click to open the official BSE annual report document.",
            ),
            "Status": st.column_config.TextColumn(
                "Status",
                help="Shows whether the report link is available or missing with color badges.",
            ),
        },
        hide_index=True,
    )


if __name__ == "__main__":
    render_annual_reports()
