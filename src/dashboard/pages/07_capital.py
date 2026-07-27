import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Path Setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from dashboard.utils.db import load_data


def render_capital_allocation():
    st.set_page_config(
        page_title="Capital Allocation Map", page_icon="🧩", layout="wide"
    )
    st.title("🧩 Capital Allocation Map")
    st.markdown(
        "Explore how 92 companies are grouped based on their 8 Capital Allocation Patterns. **Click on a pattern to drill down and see the companies inside.**"
    )
    st.markdown("---")

    try:
        # 1. Fetch Data
        df_comp = load_data("SELECT id, company_name FROM companies")
        df_rat = load_data("SELECT * FROM financial_ratios")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return

    # 2. Standardize IDs & Merge safely
    def clean_id(df):
        if df is None or df.empty:
            return pd.DataFrame()

        df = df.copy()
        df = df.loc[:, ~df.columns.duplicated()]

        if "id" in df.columns and "company_id" not in df.columns:
            df.rename(columns={"id": "company_id"}, inplace=True)
        elif "id" in df.columns and "company_id" in df.columns:
            df = df.drop(columns=["id"])

        if "company_id" in df.columns:
            if isinstance(df["company_id"], pd.DataFrame):
                df["company_id"] = df["company_id"].iloc[:, 0]

            df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()
            df = df.drop_duplicates(subset=["company_id"])

        return df

    df_comp = clean_id(df_comp)
    df_rat = clean_id(df_rat)

    # Safely Join Tables
    if "company_id" in df_comp.columns:
        df = df_comp.set_index("company_id")
        if not df_rat.empty and "company_id" in df_rat.columns:
            d = df_rat.set_index("company_id")
            df = df.join(d, rsuffix="_dup")
            df = df.loc[:, ~df.columns.str.endswith("_dup")]
        df = df.reset_index()
    else:
        st.error("Company ID not found in database.")
        return

    # 3. Column Mapping & Data Prep
    df.columns = [str(c).lower() for c in df.columns]

    pattern_col = next(
        (c for c in df.columns if "capital_allocation" in c or "pattern" in c), None
    )

    if not pattern_col:
        st.error("Capital Allocation Pattern column missing from the database!")
        return

    df = df.dropna(subset=["company_name"])

    df[pattern_col] = df[pattern_col].fillna("Unclassified Pattern")
    df["company_count"] = 1

    st.subheader("Interactive Treemap (Click to drill down)")

    fig = px.treemap(
        df,
        path=[px.Constant("All Companies"), pattern_col, "company_name"],
        values="company_count",
        color=pattern_col,
        title="Capital Allocation Patterns (8 Categories)",
        hover_data={"company_count": False, pattern_col: True},
    )

    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25), height=700)

    st.plotly_chart(fig, use_container_width=True)

    # 5. Data Table
    with st.expander("View Raw Data"):
        st.dataframe(
            df[["company_id", "company_name", pattern_col]], use_container_width=True
        )


if __name__ == "__main__":
    render_capital_allocation()
