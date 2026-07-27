import streamlit as st
import plotly.express as px
import sys
import os

# Path correction to reach project root (src folder)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from dashboard.utils.db import load_data


def render_home():
    st.set_page_config(page_title="Nifty 100 | Home", page_icon="🏠", layout="wide")
    st.title("🏠 Nifty 100 Overview")
    st.markdown("---")

    # Real broad_sector distribution query
    sector_query = """
        SELECT broad_sector, COUNT(*) as company_count 
        FROM sectors 
        GROUP BY broad_sector
    """
    sector_df = load_data(sector_query)

    # Fetch average ROE and NPM for the latest year
    kpi_query = """
        SELECT AVG(ROE) as avg_roe, AVG(NPM) as avg_npm 
        FROM financial_ratios 
        WHERE year = (SELECT MAX(year) FROM financial_ratios)
    """
    kpi_df = load_data(kpi_query)

    st.info(
        "📊 **Market Health:** Nifty 100 aggregated financial health based on the latest database analysis."
    )

    # Top Level KPIs using Streamlit metrics
    st.subheader("Key Performance Indicators (Latest Year)")
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_roe = (
            kpi_df["avg_roe"].iloc[0]
            if not kpi_df.empty and kpi_df["avg_roe"].iloc[0] is not None
            else 0
        )
        st.metric(label="Average ROE", value=f"{avg_roe:.2f}%")

    with col2:
        avg_npm = (
            kpi_df["avg_npm"].iloc[0]
            if not kpi_df.empty and kpi_df["avg_npm"].iloc[0] is not None
            else 0
        )
        st.metric(label="Average Net Profit Margin", value=f"{avg_npm:.2f}%")

    with col3:
        total_companies = sector_df["company_count"].sum() if not sector_df.empty else 0
        st.metric(label="Total Companies Tracked", value=int(total_companies))

    st.markdown("---")

    # Display Sector Distribution as a Real Donut Chart
    st.subheader("Sector-wise Distribution")
    if not sector_df.empty:
        fig = px.pie(
            sector_df,
            names="broad_sector",
            values="company_count",
            hole=0.4,
            title="Real Nifty 100 Companies by Broad Sector",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        # FIX: Changed 'percent+label' to 'percent' to show ONLY percentages inside chart
        fig.update_traces(textposition="inside", textinfo="percent")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(
            "Sector data not available. Please check the database configuration."
        )


if __name__ == "__main__":
    render_home()
