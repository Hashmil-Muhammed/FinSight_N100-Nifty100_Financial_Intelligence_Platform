import pandas as pd
import numpy as np
import sqlite3
import os
from pathlib import Path


def generate_portfolio_stats():
    """
    Statistical Analysis & Clustering
    Calculates the distribution (P10, P25, P50, P75, P90, Mean, Std)
    of key metrics like ROE, D/E, and P/E across all companies.
    """
    print(" Statistical Analysis(Portfolio Stats)...")

    # Define file paths
    root_path = Path(__file__).resolve().parents[2]
    output_file = os.path.join(root_path, "portfolio_stats.csv")
    db_path = os.path.join(root_path, "nifty100.db")

    if not os.path.exists(db_path):
        db_path = os.path.join(root_path, "data", "nifty100.db")
        if not os.path.exists(db_path):
            print(" Error: Database nifty100.db not found.")
            return

    # 1. LOAD DB TABLES
    try:
        conn = sqlite3.connect(db_path)
        print(" Reading 'financial_ratios' and 'market_cap' tables from database...")
        # Load tables that contain ROE, D/E, and P/E
        df_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

        # Check if market_cap table exists (often holds P/E data)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='market_cap';"
        )
        has_market_cap = cursor.fetchone() is not None

        if has_market_cap:
            df_mc = pd.read_sql("SELECT * FROM market_cap", conn)
        else:
            df_mc = pd.DataFrame()

        conn.close()
        print(" Successfully loaded data from database!")
    except Exception as e:
        print(f" Error reading database: {e}")
        return

    # --- BULLETPROOF CLEANING HELPER ---
    def clean_and_get_latest(df):
        if df.empty:
            return df

        # Standardize column names
        df.columns = [str(c).lower().strip() for c in df.columns]
        df = df.loc[:, ~df.columns.duplicated()]

        # Identify ID column safely
        id_col = next(
            (
                c
                for c in df.columns
                if c in ["id", "company_id", "cid", "company", "symbol"]
            ),
            None,
        )
        id_col = id_col if id_col else df.columns[0]

        if "company_id" in df.columns and id_col != "company_id":
            df = df.drop(columns=["company_id"])

        df.rename(columns={id_col: "company_id"}, inplace=True)
        df = df.loc[:, ~df.columns.duplicated()]

        if isinstance(df["company_id"], pd.DataFrame):
            df["company_id"] = df["company_id"].iloc[:, 0]

        df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()

        # Sort by year descending to get the latest record per company
        if "year" in df.columns:
            df = df.sort_values(by=["company_id", "year"], ascending=[True, False])

        # Drop duplicates, keeping only the latest year for each company
        df_latest = df.drop_duplicates(subset=["company_id"], keep="first")
        return df_latest

    # Clean data and extract latest year
    df_ratios_latest = clean_and_get_latest(df_ratios)
    df_mc_latest = clean_and_get_latest(df_mc)

    # Merge tables safely to consolidate all metrics
    if not df_mc_latest.empty:
        df_merged = pd.merge(
            df_ratios_latest, df_mc_latest, on="company_id", how="left"
        )
    else:
        df_merged = df_ratios_latest

    # 2. IDENTIFY TARGET COLUMNS DYNAMICALLY
    roe_col = next(
        (c for c in df_merged.columns if "roe" in c or "return on equity" in c), None
    )
    de_col = next(
        (
            c
            for c in df_merged.columns
            if "d_e" in c or "debt_equity" in c or "debt to equity" in c
        ),
        None,
    )
    pe_col = next(
        (
            c
            for c in df_merged.columns
            if "p_e" in c or "pe_ratio" in c or "price to earnings" in c or "pe" == c
        ),
        None,
    )

    print(f" Using Columns -> ROE: '{roe_col}', D/E: '{de_col}', P/E: '{pe_col}'")

    # Mapping target columns to their display names
    target_metrics = {
        "ROE (%)": roe_col,
        "Debt to Equity (D/E)": de_col,
        "P/E Ratio": pe_col,
    }

    results = []

    # 3. CALCULATE PORTFOLIO STATISTICS
    print(" Calculating distributions (P10, P25, P50, P75, P90, Mean, Std)...")

    for metric_name, col_name in target_metrics.items():
        if col_name and col_name in df_merged.columns:
            # Convert to numeric, dropping NaNs and inf values
            series = (
                pd.to_numeric(df_merged[col_name], errors="coerce")
                .replace([np.inf, -np.inf], np.nan)
                .dropna()
            )

            if not series.empty:
                results.append(
                    {
                        "Metric": metric_name,
                        "P10": round(series.quantile(0.10), 2),
                        "P25": round(series.quantile(0.25), 2),
                        "P50 (Median)": round(series.quantile(0.50), 2),
                        "P75": round(series.quantile(0.75), 2),
                        "P90": round(series.quantile(0.90), 2),
                        "Mean": round(series.mean(), 2),
                        "Std": round(series.std(), 2),
                    }
                )
            else:
                print(f" Warning: No valid numeric data found for {metric_name}")
        else:
            print(f" Warning: Column for {metric_name} not found in database.")

    # 4. SAVE OUTPUT
    df_stats = pd.DataFrame(results)

    if not df_stats.empty:
        df_stats.to_csv(output_file, index=False)
        print(f"\n Complete! Calculated statistics for {len(df_stats)} key metrics.")
        print(f" Report saved to: {output_file}\n")

        print(" PORTFOLIO STATISTICS SUMMARY:")
        print(df_stats.to_string(index=False))
    else:
        print(" Could not generate portfolio statistics.")


if __name__ == "__main__":
    generate_portfolio_stats()
