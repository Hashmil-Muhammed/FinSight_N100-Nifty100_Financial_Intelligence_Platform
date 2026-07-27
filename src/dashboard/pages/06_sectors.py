import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from dashboard.utils.db import load_data


def render_sector_analysis():
    st.set_page_config(page_title="Sector Analysis", page_icon="🏢", layout="wide")
    st.title("🏢 Sector Analysis")
    st.markdown("---")

    try:
        # 1. Fetch Data
        df_comp = load_data("SELECT id, company_name FROM companies")
        df_sec = load_data("SELECT * FROM sectors")
        df_rat = load_data("SELECT * FROM financial_ratios")
        df_pl = load_data("SELECT * FROM profitandloss")
        df_mc = load_data("SELECT * FROM market_cap")
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
            df = df.drop(
                columns=["id"]
            )  # id-യും company_id-യും ഉണ്ടെങ്കിൽ id ഒഴിവാക്കുന്നു

        if "company_id" in df.columns:
            # CRITICAL FIX for AttributeError
            if isinstance(df["company_id"], pd.DataFrame):
                df["company_id"] = df["company_id"].iloc[:, 0]

            df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()
            df = df.drop_duplicates(subset=["company_id"])

        return df

    df_comp = clean_id(df_comp)
    df_sec = clean_id(df_sec)
    df_rat = clean_id(df_rat)
    df_pl = clean_id(df_pl)
    df_mc = clean_id(df_mc)

    if "company_id" in df_comp.columns:
        df = df_comp.set_index("company_id")
        for d in [df_sec, df_rat, df_pl, df_mc]:
            if not d.empty and "company_id" in d.columns:
                d = d.set_index("company_id")
                df = df.join(d, lsuffix="_left", rsuffix="_right")
        df = df.reset_index()
        df = df.loc[:, ~df.columns.str.endswith("_dup")]
    else:
        st.error("Company ID not found in base data.")
        return

    # 3. Column Mapping (Updated to strictly avoid 'cagr' for sales column)
    df.columns = [str(c).lower() for c in df.columns]

    col_mapping = {
        "roe": next((c for c in df.columns if "roe" in c), None),
        "roce": next((c for c in df.columns if "roce" in c), None),
        "npm": next((c for c in df.columns if "npm" in c), None),
        "sales": next(
            (
                c
                for c in df.columns
                if ("sales" in c or "revenue" in c) and "cagr" not in c
            ),
            None,
        ),
        "mkt_cap": next(
            (c for c in df.columns if "market_cap" in c or "marketcap" in c), None
        ),
        "sector": next(
            (c for c in df.columns if "sector" in c and c != "company_id"), None
        ),
    }

    sales_c = col_mapping["sales"]
    roe_c = col_mapping["roe"]
    roce_c = col_mapping["roce"]
    npm_c = col_mapping["npm"]
    mkt_c = col_mapping["mkt_cap"]
    sector_col = col_mapping["sector"]

    if not sector_col:
        st.error("Sector column missing from the database!")
        return

    # 4. Numeric cleaning
    for col in [sales_c, roe_c, roce_c, npm_c, mkt_c]:
        if col and col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if mkt_c:
        df[mkt_c] = df[mkt_c].abs()
        df[mkt_c] = df[mkt_c].replace(0, 1)

    # 5. UI & Plotting
    sectors = sorted(df[sector_col].dropna().unique().tolist())
    selected_sector = st.sidebar.selectbox("Select Industry Sector:", sectors)
    df_sector = df[df[sector_col] == selected_sector].copy()

    if not df_sector.empty:

        # --- TASK 1: Bubble Chart ---
        st.subheader(f"Bubble Chart: {selected_sector}")
        fig_scatter = px.scatter(
            df_sector,
            x=sales_c,
            y=roe_c,
            size=mkt_c if mkt_c else None,
            color="company_name",
            hover_name="company_name",
            title="Revenue vs ROE (Size: Market Cap)",
        )
        fig_scatter.update_layout(showlegend=False)
        st.plotly_chart(fig_scatter, use_container_width=True)

        # --- TASK 2: Sector Median KPI Bar Chart ---
        st.subheader("Sector Median KPIs")
        kpi_cols = [c for c in [roe_c, roce_c, npm_c] if c]
        if kpi_cols:
            median_data = df_sector[kpi_cols].median().reset_index()
            median_data.columns = ["KPI", "Median Value"]
            fig_bar = px.bar(
                median_data,
                x="KPI",
                y="Median Value",
                text_auto=True,
                color="KPI",
                title="Median Financial Ratios",
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        # --- TASK 3: Data Table (Fixing the None values) ---
        st.subheader("Sector Data")
        df_display = df_sector.fillna("N/A")
        st.dataframe(df_display, use_container_width=True)

    else:
        st.info("No data available.")


if __name__ == "__main__":
    render_sector_analysis()
