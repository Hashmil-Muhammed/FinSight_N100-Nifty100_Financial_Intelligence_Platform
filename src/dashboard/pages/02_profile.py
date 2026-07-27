import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Fix path to import db
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from dashboard.utils.db import load_data


# Helper function to safely format metrics
def format_metric(value, is_percentage=False):
    if pd.isna(value) or value is None:
        return "N/A"
    if is_percentage:
        return f"{value:.2f}%"
    return f"{value:.2f}"


def render_profile():
    st.set_page_config(page_title="Company Profile", page_icon="🏢", layout="wide")
    st.title("🏢 Company Profile & Tearsheet")
    st.markdown("---")

    # 1. Company Search (Dropdown)
    companies_query = "SELECT id, company_name FROM companies ORDER BY company_name"
    companies_df = load_data(companies_query)

    if companies_df.empty:
        st.warning("No companies found in the database.")
        return

    company_list = companies_df["company_name"].tolist()
    selected_company_name = st.selectbox("🔍 Search for a company:", company_list)

    if selected_company_name:
        # Get selected company ID and remove any hidden spaces
        comp_id = str(
            companies_df[companies_df["company_name"] == selected_company_name][
                "id"
            ].iloc[0]
        ).strip()

        # Fetch Company Basic Details
        details_query = f"SELECT * FROM companies WHERE TRIM(id) = '{comp_id}'"
        details_df = load_data(details_query)

        # FIX: Fetch the latest year that ACTUALLY HAS valid KPI data (ROE IS NOT NULL)
        kpi_query = f"""
            SELECT * FROM financial_ratios 
            WHERE TRIM(company_id) = '{comp_id}' 
            AND ROE IS NOT NULL 
            ORDER BY year DESC LIMIT 1
        """
        kpi_df = load_data(kpi_query)

        # 2. Company Card (Description)
        if not details_df.empty:
            st.subheader(details_df["company_name"].iloc[0])
            st.write(f"**About:** {details_df['about_company'].iloc[0]}")
            st.write(f"🌐 [Company Website]({details_df['website'].iloc[0]})")
            st.markdown("---")

        # 3. KPI Tiles (6 Metrics)
        st.subheader("Key Performance Indicators (Latest Valid Year)")
        if not kpi_df.empty:
            cols = st.columns(6)

            roe = format_metric(kpi_df["ROE"].iloc[0], is_percentage=True)
            roce = format_metric(kpi_df["ROCE"].iloc[0], is_percentage=True)
            npm = format_metric(kpi_df["NPM"].iloc[0], is_percentage=True)
            d_e = format_metric(kpi_df["D_E"].iloc[0], is_percentage=False)
            icr = format_metric(kpi_df["ICR"].iloc[0], is_percentage=False)
            asset_turnover = format_metric(
                kpi_df["Asset_Turnover"].iloc[0], is_percentage=False
            )

            cols[0].metric("ROE", roe)
            cols[1].metric("ROCE", roce)
            cols[2].metric("Net Profit Margin", npm)
            cols[3].metric("Debt to Equity", d_e)
            cols[4].metric("Interest Coverage", icr)
            cols[5].metric("Asset Turnover", asset_turnover)
        else:
            st.warning(
                f"⚠️ No valid calculated KPI data found for {selected_company_name}."
            )

        st.markdown("---")

        # 4. Financial Charts (P&L, Balance Sheet, Cash Flow)
        st.subheader("📊 10-Year Financial Trends")
        chart_col1, chart_col2, chart_col3 = st.columns(3)

        with chart_col1:
            pl_query = f"SELECT year, sales, net_profit FROM profitandloss WHERE TRIM(company_id) = '{comp_id}' ORDER BY year"
            pl_df = load_data(pl_query)
            if not pl_df.empty:
                fig_pl = px.bar(
                    pl_df,
                    x="year",
                    y=["sales", "net_profit"],
                    barmode="group",
                    title="P&L: Sales vs Net Profit",
                    color_discrete_sequence=["#1f77b4", "#2ca02c"],
                )
                st.plotly_chart(fig_pl, use_container_width=True)

        with chart_col2:
            bs_query = f"SELECT year, total_assets, total_liabilities FROM balancesheet WHERE TRIM(company_id) = '{comp_id}' ORDER BY year"
            bs_df = load_data(bs_query)
            if not bs_df.empty:
                fig_bs = px.line(
                    bs_df,
                    x="year",
                    y=["total_assets", "total_liabilities"],
                    title="Balance Sheet Trends",
                    color_discrete_sequence=["#ff7f0e", "#d62728"],
                )
                st.plotly_chart(fig_bs, use_container_width=True)

        with chart_col3:
            cf_query = f"SELECT year, operating_activity, investing_activity, financing_activity FROM cashflow WHERE TRIM(company_id) = '{comp_id}' ORDER BY year"
            cf_df = load_data(cf_query)
            if not cf_df.empty:
                fig_cf = px.bar(
                    cf_df,
                    x="year",
                    y=[
                        "operating_activity",
                        "investing_activity",
                        "financing_activity",
                    ],
                    title="Cash Flow Breakdown",
                    color_discrete_sequence=["#2ca02c", "#d62728", "#1f77b4"],
                )
                st.plotly_chart(fig_cf, use_container_width=True)


if __name__ == "__main__":
    render_profile()
