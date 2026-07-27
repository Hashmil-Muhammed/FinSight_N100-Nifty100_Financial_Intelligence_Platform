import pandas as pd
import sqlite3
import os
from pathlib import Path


def generate_distress_flags():
    """
    Cash Flow Intelligence
    Identifies Distress Signals and Deleveraging trends.
    Saves output to distress_alerts.csv
    """
    print(" Cash Flow Intelligence")

    # Define file paths
    root_path = Path(__file__).resolve().parents[2]
    output_file = os.path.join(root_path, "distress_alerts.csv")
    db_path = os.path.join(root_path, "nifty100.db")

    if not os.path.exists(db_path):
        db_path = os.path.join(root_path, "data", "nifty100.db")

    # 1. LOAD DB TABLES (Cashflow & Balancesheet)
    try:
        conn = sqlite3.connect(db_path)
        print(" Reading 'cashflow' and 'balancesheet' tables from database...")
        df_cf = pd.read_sql("SELECT * FROM cashflow", conn)
        df_bs = pd.read_sql("SELECT * FROM balancesheet", conn)
        conn.close()
        print(" Successfully loaded data from database!")
    except Exception as e:
        print(f" Error reading database: {e}")
        return

    # PERFECT CLEANING HELPER
    def clean_df(df):
        # Standardize column names to lowercase
        df.columns = [str(c).lower().strip() for c in df.columns]

        # Remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]

        # Identify the primary ID column
        id_col = next(
            (
                c
                for c in df.columns
                if c in ["id", "company_id", "cid", "company", "symbol"]
            ),
            None,
        )
        id_col = id_col if id_col else df.columns[0]

        # Drop existing 'company_id' if it conflicts
        if "company_id" in df.columns and id_col != "company_id":
            df = df.drop(columns=["company_id"])

        # Rename identified column to standard 'company_id'
        df.rename(columns={id_col: "company_id"}, inplace=True)
        df = df.loc[:, ~df.columns.duplicated()]

        # Force column to be a Series if it became a DataFrame by mistake
        if isinstance(df["company_id"], pd.DataFrame):
            df["company_id"] = df["company_id"].iloc[:, 0]

        # Standardize the string format
        df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()
        return df

    # Clean both dataframes
    df_cf = clean_df(df_cf)
    df_bs = clean_df(df_bs)

    if "year" not in df_cf.columns or "year" not in df_bs.columns:
        print(" Error: 'year' column is missing from the tables.")
        return

    # 2. SMART COLUMN MATCHERS
    # Find CFO, CFF, and Borrowings columns dynamically
    cfo_col = next(
        (c for c in df_cf.columns if "operating" in c.replace("_", " ") or "cfo" in c),
        None,
    )
    cff_col = next(
        (c for c in df_cf.columns if "financing" in c.replace("_", " ") or "cff" in c),
        None,
    )
    borrowings_col = next((c for c in df_bs.columns if "borrowing" in c), None)

    if not all([cfo_col, cff_col, borrowings_col]):
        print(" Error: Could not find required columns in database.")
        print(f"Found -> CFO: {cfo_col}, CFF: {cff_col}, Borrowings: {borrowings_col}")
        return

    print(
        f" Using Columns -> CFO: '{cfo_col}', CFF: '{cff_col}', Borrowings: '{borrowings_col}'"
    )

    # 3. MERGE DATAFRAMES
    # Merge Cashflow and Balancesheet on company_id and year
    df_merged = pd.merge(
        df_cf[["company_id", "year", cfo_col, cff_col]],
        df_bs[["company_id", "year", borrowings_col]],
        on=["company_id", "year"],
        how="inner",
    )

    # Convert columns to numeric safely
    for col in [cfo_col, cff_col, borrowings_col]:
        df_merged[col] = pd.to_numeric(df_merged[col], errors="coerce").fillna(0)

    # Sort by company and year descending (newest year first)
    df_merged = df_merged.sort_values(
        by=["company_id", "year"], ascending=[True, False]
    )

    results = []

    # 4. APPLY LOGIC (7.5 & 7.6)
    print(" Processing Distress and Deleveraging rules...")
    for company, group in df_merged.groupby("company_id"):
        group = group.reset_index(drop=True)
        if len(group) == 0:
            continue

        # Get latest year's data
        latest = group.iloc[0]
        cfo_val = latest[cfo_col]
        cff_val = latest[cff_col]
        latest_borrowings = latest[borrowings_col]

        # Get previous year's borrowings for YoY comparison (if available)
        prev_borrowings = (
            group.iloc[1][borrowings_col] if len(group) > 1 else latest_borrowings
        )

        # Initialize default flag
        flag = "Stable"

        # Rule 7.6: Distress Pattern (CFO < 0 AND CFF > 0)
        # Funding operations via debt/equity
        if cfo_val < 0 and cff_val > 0:
            flag = "Distress Signal"

        # Rule 7.5: Debt Repayment Detection (CFF < 0 AND borrowings declining YoY)
        elif cff_val < 0 and latest_borrowings < prev_borrowings:
            flag = "Deleveraging "

        # Only append companies that have a flag (or keep all if you prefer full report)
        # For a clean alerts file, let's keep all and the dashboard can filter
        results.append(
            {
                "Company ID": company,
                "Latest CFO": round(cfo_val, 2),
                "Latest CFF": round(cff_val, 2),
                "Latest Borrowings": round(latest_borrowings, 2),
                "Previous Borrowings": round(prev_borrowings, 2),
                "Alert Badge": flag,
            }
        )

    # 5. SAVE REPORT
    df_results = pd.DataFrame(results)

    if not df_results.empty:
        df_results.to_csv(output_file, index=False)
        print(f"\n Complete! Flagged {len(df_results)} companies.")
        print(f" Alerts saved to: {output_file}\n")

        # Show a summary of alerts
        distress_count = len(
            df_results[df_results["Alert Badge"] == "Distress Signal ⚠️"]
        )
        delev_count = len(df_results[df_results["Alert Badge"] == "Deleveraging "])

        print("SUMMARY:")
        print(f"   -> Distress Signals Found: {distress_count}")
        print(f"   -> Deleveraging Companies: {delev_count}")

        print("\n SAMPLE OUTPUT:")
        print(df_results[["Company ID", "Alert Badge"]].head(8).to_string(index=False))
    else:
        print("Could not calculate flags.")


if __name__ == "__main__":
    generate_distress_flags()
