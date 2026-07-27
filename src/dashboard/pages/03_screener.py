import streamlit as st
import sys
import os

# Path correction
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from dashboard.utils.db import load_data


def render_screener():
    st.set_page_config(page_title="Financial Screener", page_icon="🔍", layout="wide")
    st.title("🔍 Financial Screener")
    st.markdown("---")

    # 1. Fetching Data
    query = """
        SELECT company_id as company_name, ROE, ROCE, NPM, D_E, ICR, Asset_Turnover 
        FROM financial_ratios 
        WHERE year = (
            SELECT year FROM financial_ratios 
            GROUP BY company_id 
            ORDER BY year DESC 
            LIMIT 1
        )
    """
    df = load_data(query)

    if df.empty:
        st.warning("No data found in financial_ratios table.")
        return

    # Clean data: Replace NaN with 0
    df = df.fillna(0)

    # 2. Sidebar Filters
    st.sidebar.header("⚙️ Filter Criteria")

    def get_slider_range(series):
        mn, mx = float(series.min()), float(series.max())
        return mn, (mx if mx > mn else mn + 1.0)

    # Sliders defined ONCE
    min_r, max_r = get_slider_range(df["ROE"])
    selected_roe = st.sidebar.slider(
        "Minimum ROE (%)", min_r, max_r, min_r, key="roe_slider"
    )

    min_roc, max_roc = get_slider_range(df["ROCE"])
    selected_roce = st.sidebar.slider(
        "Minimum ROCE (%)", min_roc, max_roc, min_roc, key="roce_slider"
    )

    min_n, max_n = get_slider_range(df["NPM"])
    selected_npm = st.sidebar.slider(
        "Minimum NPM (%)", min_n, max_n, min_n, key="npm_slider"
    )

    min_d, max_d = get_slider_range(df["D_E"])
    selected_de = st.sidebar.slider(
        "Maximum Debt to Equity", min_d, max_d, max_d, key="de_slider"
    )

    # 3. Apply Filter Logic
    filtered_df = df[
        (df["ROE"] >= selected_roe)
        & (df["ROCE"] >= selected_roce)
        & (df["NPM"] >= selected_npm)
        & (df["D_E"] <= selected_de)
    ]

    # 4. Display Results
    st.subheader(f"📊 Results: {len(filtered_df)} Companies Found")

    # Display table using wide mode
    st.dataframe(
        filtered_df.style.format(precision=2), use_container_width=True, height=400
    )

    # Download CSV
    if not filtered_df.empty:
        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Results", csv, "screener_results.csv", "text/csv"
        )


if __name__ == "__main__":
    render_screener()
