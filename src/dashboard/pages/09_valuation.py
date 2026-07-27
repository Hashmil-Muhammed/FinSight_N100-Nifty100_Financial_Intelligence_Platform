import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Set up path to access db module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from dashboard.utils.db import load_data


def render_valuation_analysis():
    st.set_page_config(page_title="Valuation Analysis", page_icon="📈", layout="wide")
    st.title("Valuation & Market Data Analysis")
    st.markdown(
        "Analyze historical P/E, P/B, EV/EBITDA trends, and rank companies by FCF & Dividend Yields."
    )
    st.markdown("---")

    # ==========================================
    # STEP 1: SAFE DATA FETCHING
    # ==========================================
    try:
        df_comp = load_data("SELECT id, company_name FROM companies")
        df_sec = load_data("SELECT * FROM sectors")
        df_rat = load_data("SELECT * FROM financial_ratios")
        df_mc = load_data("SELECT * FROM market_cap")
    except Exception as e:
        st.error(
            f"Error fetching data from database. Check if tables exist. Details: {e}"
        )
        return

    # ==========================================
    # STEP 2: SAFE ID STANDARDIZATION
    # ==========================================
    def clean_id(df):
        if df is None or df.empty:
            return pd.DataFrame()
        df = df.copy()

        df.columns = [str(c).lower().strip() for c in df.columns]
        df = df.loc[:, ~df.columns.duplicated()]

        id_col = next((c for c in df.columns if c in ["id", "company_id", "cid"]), None)

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
    df_sec = clean_id(df_sec)
    df_rat = clean_id(df_rat)
    df_mc = clean_id(df_mc)

    # ==========================================
    # STEP 3: MERGING TABLES SAFELY
    # ==========================================
    if "company_id" in df_comp.columns:
        df = df_comp.set_index("company_id")
        for d in [df_sec, df_rat, df_mc]:
            if not d.empty and "company_id" in d.columns:
                d = d.set_index("company_id")
                df = df.join(d, rsuffix="_dup")
        df = df.reset_index()
        df = df.loc[:, ~df.columns.str.endswith("_dup")]
    else:
        st.error("Critical Error: 'company_id' missing from base companies data.")
        return

    # ==========================================
    # STEP 4: DYNAMIC COLUMN MAPPING & CALCULATION (TASK 1 & TASK 2)
    # ==========================================
    col_mapping = {
        "pe": next(
            (c for c in df.columns if "pe_ratio" in c or "p_e" in c or c == "pe"), None
        ),
        "pb": next(
            (c for c in df.columns if "pb_ratio" in c or "p_b" in c or c == "pb"), None
        ),
        "ev_ebitda": next(
            (c for c in df.columns if "ev_ebitda" in c or "evebitda" in c), None
        ),
        "roe": next((c for c in df.columns if "roe" in c), None),
        "mkt_cap": next(
            (c for c in df.columns if "market_cap" in c or "marketcap" in c), None
        ),
        "sector": next(
            (c for c in df.columns if "sector" in c and c != "company_id"), None
        ),
        "year": next((c for c in df.columns if "year" in c), None),
        # TASK 2: New columns for FCF & Dividend
        "fcf": next(
            (c for c in df.columns if "fcf" in c or "free_cash_flow" in c), None
        ),
        "div_yield": next(
            (c for c in df.columns if "dividend_yield" in c or "div_yield" in c), None
        ),
    }

    pe_c = col_mapping["pe"]
    pb_c = col_mapping["pb"]
    ev_c = col_mapping["ev_ebitda"]
    roe_c = col_mapping["roe"]
    mkt_c = col_mapping["mkt_cap"]
    sec_c = col_mapping["sector"]
    year_c = col_mapping["year"]
    fcf_c = col_mapping["fcf"]
    div_c = col_mapping["div_yield"]

    # Convert all necessary columns to numeric
    numeric_cols = [pe_c, pb_c, ev_c, roe_c, mkt_c, fcf_c, div_c]
    for col in numeric_cols:
        if col and col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Clean Year column
    if year_c and year_c in df.columns:
        df[year_c] = df[year_c].astype(str).str.extract(r"(\d{4})")[0].fillna("N/A")

    # Ensure market cap is positive to prevent division errors
    if mkt_c:
        df[mkt_c] = df[mkt_c].abs().replace(0, 1)

    # TASK 2.1: FCF Yield Calculation (FCF / Market_Cap * 100)
    if fcf_c and mkt_c:
        df["FCF_Yield_%"] = (df[fcf_c] / df[mkt_c]) * 100
    else:
        df["FCF_Yield_%"] = 0.0

    # Ensure Dividend Yield column exists
    if not div_c:
        df["Dividend_Yield_%"] = 0.0
        div_c = "Dividend_Yield_%"

    # Stop if critical columns are missing
    if not sec_c or not pe_c:
        st.error(
            "Missing critical columns (Sector or P/E Ratio) for Valuation Analysis."
        )
        return

    # ==========================================
    # STEP 5: UI FILTERS
    # ==========================================
    st.sidebar.header("Filter Controls")

    sectors = ["All Sectors"] + sorted(df[sec_c].dropna().unique().tolist())
    selected_sector = st.sidebar.selectbox("Select Sector:", sectors)

    if selected_sector != "All Sectors":
        df_filtered = df[df[sec_c] == selected_sector]
    else:
        df_filtered = df

    companies = ["All Companies"] + sorted(
        df_filtered["company_name"].dropna().unique().tolist()
    )
    selected_company = st.sidebar.selectbox("Select Company:", companies)

    if selected_company != "All Companies":
        df_filtered = df_filtered[df_filtered["company_name"] == selected_company]

    # ==========================================
    # STEP 6: VISUALIZATIONS (TASK 1)
    # ==========================================
    # UI FIX: Gracefully handle missing data edge case
    if df_filtered.empty:
        st.warning(
            "No data available for the selected filters. Please try another company or sector."
        )
        return

    st.subheader("Multiples Analysis Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**1. Historical P/E Trend**")
        if year_c and not df_filtered[year_c].isin(["N/A"]).all():
            trend_data = (
                df_filtered.groupby([year_c, "company_name"])[pe_c].mean().reset_index()
            )
            trend_data = trend_data.sort_values(by=year_c)

            unique_years = trend_data[year_c].nunique()

            if unique_years > 1:
                fig_pe = px.line(
                    trend_data,
                    x=year_c,
                    y=pe_c,
                    color="company_name",
                    markers=True,
                    title="P/E Ratio Trend",
                    labels={year_c: "Financial Year", pe_c: "P/E Ratio"},
                )
            else:
                single_year = trend_data[year_c].iloc[0]
                fig_pe = px.bar(
                    trend_data,
                    x="company_name",
                    y=pe_c,
                    color="company_name",
                    title=f"P/E Ratio (Year: {single_year})",
                    labels={"company_name": "Company", pe_c: "P/E Ratio"},
                )
                if selected_company == "All Companies":
                    fig_pe.update_xaxes(showticklabels=False)

            fig_pe.update_layout(
                showlegend=(
                    selected_company == "All Companies"
                    and selected_sector != "All Sectors"
                )
            )
            st.plotly_chart(fig_pe, use_container_width=True)
        else:
            st.warning("Historical 'Year' data is not properly mapped.")

    with col2:
        st.markdown("**2. Value vs Quality (P/B vs ROE)**")
        if pb_c and roe_c and mkt_c:
            valid_scatter = df_filtered[
                (df_filtered[pb_c] != 0) & (df_filtered[roe_c] != 0)
            ]

            if not valid_scatter.empty:
                if year_c:
                    valid_scatter = valid_scatter.sort_values(year_c).drop_duplicates(
                        subset=["company_name"], keep="last"
                    )

                fig_scatter = px.scatter(
                    valid_scatter,
                    x=pb_c,
                    y=roe_c,
                    size=mkt_c,
                    color=sec_c if selected_sector == "All Sectors" else "company_name",
                    hover_name="company_name",
                    title="P/B vs ROE (Size: Market Cap)",
                    labels={
                        pb_c: "Price to Book (P/B)",
                        roe_c: "Return on Equity (ROE)",
                    },
                )
                fig_scatter.update_layout(showlegend=False)
                st.plotly_chart(fig_scatter, use_container_width=True)
            else:
                st.info("Not enough positive P/B and ROE data to plot.")
        else:
            st.warning("P/B, ROE, or Market Cap columns are missing.")

    # ==========================================
    # STEP 7: EV/EBITDA COMP TABLE (TASK 1.3)
    # ==========================================
    st.markdown("---")
    st.subheader("EV/EBITDA Comparison Table")

    if ev_c:
        table_data = df_filtered[["company_name", sec_c, ev_c]].copy()
        table_data = (
            table_data.groupby(["company_name", sec_c])[ev_c].mean().reset_index()
        )

        sector_medians = df.groupby(sec_c)[ev_c].median().reset_index()
        sector_medians.rename(columns={ev_c: "Sector_Median_EV_EBITDA"}, inplace=True)

        table_data = pd.merge(table_data, sector_medians, on=sec_c, how="left")

        table_data["Premium_Flag"] = table_data.apply(
            lambda x: (
                "⚠️ High Premium"
                if x[ev_c] > (x["Sector_Median_EV_EBITDA"] * 1.2)
                else "✅ Normal"
            ),
            axis=1,
        )

        table_data.rename(
            columns={
                "company_name": "Company",
                sec_c: "Sector",
                ev_c: "Current EV/EBITDA",
            },
            inplace=True,
        )

        st.dataframe(table_data.round(2), width="stretch", hide_index=True)
    else:
        st.warning("EV/EBITDA data is not available in the dataset.")

    # ==========================================
    # STEP 8: TASK 2 - FCF & DIVIDEND YIELD RANKER
    # ==========================================
    st.markdown("---")
    st.subheader("FCF & Dividend Yield Ranker")
    st.markdown(
        "Filter companies by Minimum Dividend Yield and rank them based on Free Cash Flow (FCF) Yield to identify value signals."
    )

    min_yield = st.slider(
        "Select Minimum Dividend Yield (%) Threshold:",
        min_value=0.0,
        max_value=15.0,
        value=0.0,
        step=0.5,
    )

    rank_df = (
        df[df[sec_c] == selected_sector]
        if selected_sector != "All Sectors"
        else df.copy()
    )

    if year_c and not rank_df.empty:
        rank_df = rank_df.sort_values(year_c).drop_duplicates(
            subset=["company_name"], keep="last"
        )

    rank_df = rank_df[rank_df[div_c] >= min_yield]

    if not rank_df.empty:
        display_cols = ["company_name", sec_c, div_c, "FCF_Yield_%"]
        rank_df = rank_df[display_cols].copy()

        rank_df.rename(
            columns={
                "company_name": "Company Name",
                sec_c: "Sector",
                div_c: "Dividend Yield (%)",
                "FCF_Yield_%": "FCF Yield (%)",
            },
            inplace=True,
        )

        rank_df = rank_df.sort_values(
            by=["FCF Yield (%)", "Dividend Yield (%)"], ascending=[False, False]
        )
        rank_df.insert(0, "Rank", range(1, 1 + len(rank_df)))

        st.dataframe(rank_df.round(2), width="stretch", hide_index=True)
    else:
        st.info(
            f"No companies found with a Dividend Yield of {min_yield}% or higher in the selected sector."
        )

    # ==========================================
    # STEP 9: TASK 3 - OVERVALUATION FLAGS & EXPORTS
    # ==========================================
    st.markdown("---")
    st.subheader("⚖️ Overvaluation Flags & Downloads")
    st.markdown(
        "Identifies if a stock is trading at a Caution (High P/E) or Discount (Low P/E) compared to its sector."
    )

    if pe_c and sec_c:
        # Create a fresh copy for Task 3 to avoid KeyError
        flag_df = df_filtered.copy()

        # Keep latest year data for current valuation
        if year_c and not flag_df.empty:
            flag_df = flag_df.sort_values(year_c).drop_duplicates(
                subset=["company_name"], keep="last"
            )

        # Calculate Sector Median PE safely
        sector_pe_medians = df.groupby(sec_c)[pe_c].median().reset_index()
        sector_pe_medians.rename(columns={pe_c: "Sector_Median_PE"}, inplace=True)

        # Merge medians into flag_df
        flag_df = pd.merge(flag_df, sector_pe_medians, on=sec_c, how="left")

        # Apply valuation logic
        def get_valuation_badge(row):
            median_pe = row["Sector_Median_PE"]
            comp_pe = row[pe_c]

            if pd.isna(median_pe) or median_pe == 0:
                return "⚪ Fair Value"
            if comp_pe > (median_pe * 1.5):
                return "🔴 Caution (Overvalued)"
            elif comp_pe > 0 and comp_pe < (median_pe * 0.7):
                return "🟢 Discount (Undervalued)"
            else:
                return "⚪ Fair Value"

        flag_df["Valuation_Flag"] = flag_df.apply(get_valuation_badge, axis=1)

        # Display table
        display_flag_cols = [
            "company_name",
            sec_c,
            pe_c,
            "Sector_Median_PE",
            "Valuation_Flag",
        ]
        display_flag_df = flag_df[display_flag_cols].copy()
        display_flag_df.rename(
            columns={
                "company_name": "Company Name",
                sec_c: "Sector",
                pe_c: "Current P/E Ratio",
            },
            inplace=True,
        )

        st.dataframe(display_flag_df.round(2), width="stretch", hide_index=True)

        # Download Buttons
        st.markdown("### Download Reports")
        col_d1, col_d2 = st.columns(2)

        with col_d1:
            csv_summary = flag_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Valuation Summary (CSV)",
                data=csv_summary,
                file_name="valuation_summary.csv",
                mime="text/csv",
            )

        with col_d2:
            export_flags = display_flag_df[
                display_flag_df["Valuation_Flag"].str.contains("Caution|Discount")
            ]
            csv_flags = export_flags.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Valuation Flags (CSV)",
                data=csv_flags,
                file_name="valuation_flags.csv",
                mime="text/csv",
            )
    else:
        st.warning(
            "P/E Ratio or Sector column is missing. Cannot compute overvaluation flags."
        )


if __name__ == "__main__":
    render_valuation_analysis()
