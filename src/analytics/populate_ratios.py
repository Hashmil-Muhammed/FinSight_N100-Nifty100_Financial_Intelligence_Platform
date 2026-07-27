import sqlite3
import pandas as pd
from src.analytics.ratios import ProfitabilityEngine
from src.analytics.cagr import CAGREngine
from src.analytics.cashflow_kpis import CashFlowEngine


def populate_database(db_path="nifty100.db"):
    print("starting Database Population for Day12..\n")

    # 1. Run all 3 engines and fetch data
    print("Running Profitability & Leverage engine...")
    ratios_df = ProfitabilityEngine(db_path).run()

    print("Running CAGR Engine..")
    cagr_df = CAGREngine(db_path).run()

    print("Running cash flow KPI Engine..")
    cf_df = CashFlowEngine(db_path).run()

    # 2. Merge all DataFrames based on company_id and year
    print("\n merging all analytics data into a single master table..")
    df_merged = pd.merge(ratios_df, cagr_df, on=["company_id", "year"], how="outer")
    df_merged = pd.merge(df_merged, cf_df, on=["company_id", "year"], how="outer")

    # 3. Clean up the columns (Keep only the required KPIs and drop extra columns)
    cols_to_keep = [
        "company_id",
        "year",
        "NPM",
        "OPM",
        "ROE",
        "ROCE",
        "D_E",
        "ICR",
        "Asset_Turnover",
        "Revenue_CAGR_3Y",
        "PAT_CAGR_3Y",
        "EPS_CAGR_3Y",
        "PAT_Turnaround_3Y",
        "Revenue_CAGR_5Y",
        "PAT_CAGR_5Y",
        "EPS_CAGR_5Y",
        "PAT_Turnaround_5Y",
        "Revenue_CAGR_10Y",
        "PAT_CAGR_10Y",
        "EPS_CAGR_10Y",
        "PAT_Turnaround_10Y",
        "FCF",
        "CFO_Quality_Score",
        "CapEx_Intensity",
        "FCF_Conversion",
        "Capital_Allocation_Pattern",
    ]
    # Filter the DataFrame to keep only the KPI columns
    final_cols = [col for col in cols_to_keep if col in df_merged.columns]
    final_df = df_merged[final_cols]

    # 4. Save to SQLite Database
    print(f"\n uploading {len(final_df)} rows to 'financial_ratios' table in SQLite..")
    with sqlite3.connect(db_path) as conn:
        final_df.to_sql("financial_ratios", conn, if_exists="replace", index=False)

    print("Success 'Financial_ratios' table is fully populated \n")

    # 5. Validation Print (Random Sample for Manual Check)
    print("Data Quality Validation (random 3 rows for manual excel check):")
    sample_cols = ["company_id", "year", "OPM", "ROE", "FCF", "Revenue_CAGR_5Y"]
    print(final_df[sample_cols].sample(3).to_string(index=False))
    print(
        "\n Please cross-verify these value with your manual Excel Calculations (+/ - 2% tolerance)"
    )


if __name__ == "__main__":
    populate_database()
