import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from dashboard.utils.db import load_data


def render_peer_comparison():
    st.set_page_config(page_title="Peer Comparison", page_icon="⚖️", layout="wide")
    st.title("⚖️ Peer Comparison")
    st.markdown("---")

    # SMART SQL QUERY: Fetch the latest year that ACTUALLY HAS valid ROE data for each company
    query = """
        SELECT 
            TRIM(c.company_name) as company_name, 
            TRIM(s.broad_sector) as broad_sector, 
            f.ROE, f.ROCE, f.NPM
        FROM companies c
        JOIN sectors s ON TRIM(c.id) = TRIM(s.company_id)
        JOIN financial_ratios f ON TRIM(c.id) = TRIM(f.company_id)
        WHERE f.year = (
            SELECT MAX(year) 
            FROM financial_ratios f2 
            WHERE TRIM(f2.company_id) = TRIM(c.id) AND f2.ROE IS NOT NULL AND f2.ROE != 0
        )
        GROUP BY c.company_name
    """
    df = load_data(query)

    if df.empty:
        st.warning("Database data is missing. Please check your data population.")
        return

    # Clean numeric data completely
    numeric_cols = ["ROE", "ROCE", "NPM"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # REMOVE companies that still have 0 values (Prevents empty bars in chart)
    df = df[(df["ROE"] > 0) | (df["ROCE"] > 0)]

    # UI Selection
    companies_list = sorted(df["company_name"].unique().tolist())
    selected_name = st.selectbox("Select Company:", companies_list)

    if selected_name:
        # Sector matching
        sector = df[df["company_name"] == selected_name]["broad_sector"].iloc[0]

        # Filter peers based on sector
        df_peers = df[df["broad_sector"] == sector]

        st.subheader(f"Comparison with Peers in Industry: {sector}")

        if len(df_peers) <= 1:
            st.info("No other peers with valid data found in this sector.")

        # Melt data for grouped bar chart
        df_melted = df_peers.melt(
            id_vars="company_name",
            value_vars=["ROE", "ROCE", "NPM"],
            var_name="Metric",
            value_name="Percentage (%)",
        )

        # --- FIX FOR INVISIBLE BARS (OUTLIERS) ---
        # We cap the values for the CHART ONLY so smaller bars remain clearly visible.
        df_chart = df_melted.copy()
        df_chart["Percentage (%)"] = df_chart["Percentage (%)"].clip(
            lower=-50, upper=150
        )

        # Plotly Chart
        fig = px.bar(
            df_chart,
            x="company_name",
            y="Percentage (%)",
            color="Metric",
            barmode="group",
            title=f"Peer Financial Ratios - {sector} (Chart capped at 150% for visibility)",
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        # Display Table below the chart (Original data without capping)
        display_cols = ["company_name", "ROE", "ROCE", "NPM"]
        st.dataframe(
            df_peers[display_cols].style.format(precision=2), use_container_width=True
        )


if __name__ == "__main__":
    render_peer_comparison()
