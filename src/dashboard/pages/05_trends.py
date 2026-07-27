import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Path correction to reach the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from dashboard.utils.db import load_data


def render_trends():
    st.set_page_config(page_title="Trend Analysis", page_icon="📈", layout="wide")
    st.title("📈 Trend Analysis")
    st.markdown(
        "Analyze historical trends and Year-over-Year (YoY) growth across P&L and Balance Sheet."
    )
    st.markdown("---")

    # 1. Fetch Companies
    df_comp = load_data("SELECT id, company_name FROM companies")
    if df_comp.empty:
        st.warning("Database empty. Please check your data population.")
        return

    df_comp["id"] = df_comp["id"].astype(str).str.strip()

    # 2. UI: Select Company
    st.sidebar.header("⚙️ Configuration")
    selected_name = st.sidebar.selectbox(
        "Select Company:", sorted(df_comp["company_name"].unique())
    )
    comp_id = df_comp[df_comp["company_name"] == selected_name]["id"].iloc[0]

    # 3. Fetch P&L and Balance Sheet Data
    # FIX: Changed to 'equity_capital' which is the standard column name for share capital
    query = f"""
        SELECT 
            p.year, 
            p.sales, 
            p.operating_profit, 
            p.net_profit,
            b.borrowings,
            b.total_assets,
            (b.equity_capital + b.reserves) AS net_worth
        FROM profitandloss p
        LEFT JOIN balancesheet b 
            ON TRIM(p.company_id) = TRIM(b.company_id) AND p.year = b.year
        WHERE TRIM(p.company_id) = '{comp_id}' 
        ORDER BY p.year ASC
    """
    df_trends = load_data(query)

    if df_trends.empty:
        st.warning(f"No historical data found for {selected_name}.")
        return

    # Force all columns to lowercase first to avoid any case-sensitivity mismatch
    df_trends.columns = df_trends.columns.str.lower()

    # Safely rename columns to perfectly match the UI select options
    df_trends = df_trends.rename(
        columns={
            "sales": "Sales",
            "operating_profit": "Operating_Profit",
            "net_profit": "Net_Profit",
            "borrowings": "Borrowings",
            "total_assets": "Total_Assets",
            "net_worth": "Net_Worth",
        }
    )

    # Clean year strings for plotting
    df_trends["year"] = df_trends["year"].astype(str)

    # 4. UI: Select Metrics for Multi-metric Overlay
    available_metrics = [
        "Sales",
        "Operating_Profit",
        "Net_Profit",
        "Borrowings",
        "Total_Assets",
        "Net_Worth",
    ]
    selected_metrics = st.multiselect(
        "Select Metrics to Overlay:", available_metrics, default=["Sales", "Net_Profit"]
    )

    if not selected_metrics:
        st.info("Please select at least one metric to visualize.")
        return

    missing_cols = [col for col in selected_metrics if col not in df_trends.columns]
    if missing_cols:
        st.error(
            f"Error: The following columns are missing from the database query: {missing_cols}"
        )
        return

    st.subheader(f"Historical Trend for {selected_name}")

    df_plot = df_trends[["year"] + selected_metrics].copy()

    # Convert data to numeric and calculate YoY % Change
    for col in selected_metrics:
        df_plot[col] = pd.to_numeric(df_plot[col], errors="coerce").fillna(0)
        df_plot[f"{col} YoY (%)"] = df_plot[col].pct_change() * 100

    # Melt DataFrame for Plotly
    df_melted = df_plot.melt(
        id_vars="year",
        value_vars=selected_metrics,
        var_name="Metric",
        value_name="Value (Cr)",
    )

    # 5. Render Plotly Line Chart
    fig = px.line(
        df_melted,
        x="year",
        y="Value (Cr)",
        color="Metric",
        markers=True,
        title=f"10-Year Financial Trends - {selected_name}",
    )
    fig.update_layout(
        xaxis_title="Financial Year",
        yaxis_title="Amount (in Cr)",
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

    # 6. Display Detailed Data Table
    st.markdown("### Detailed YoY Growth Table")
    df_plot = df_plot.fillna(0)
    st.dataframe(df_plot.style.format(precision=2), use_container_width=True)


if __name__ == "__main__":
    render_trends()
