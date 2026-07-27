import pandas as pd
import sqlite3
import os
from pathlib import Path


def calculate_cfo_quality():
    """
    Cash Flow Intelligence
    Calculates 5-year average CFO/PAT ratio and assigns a quality badge.
    """
    print(" Starting  Cash Flow Intelligence ...")

    root_path = Path(__file__).resolve().parents[2]
    output_file = os.path.join(root_path, "cashflow_intelligence.xlsx")

    db_path = os.path.join(root_path, "nifty100.db")
    if not os.path.exists(db_path):
        db_path = os.path.join(root_path, "data", "nifty100.db")

    if not os.path.exists(db_path):
        print(" Error: Database nifty100.db not found.")
        return

    try:
        conn = sqlite3.connect(db_path)
        print(" Reading 'profitandloss' and 'cashflow' tables from database...")

        df_pl = pd.read_sql("SELECT * FROM profitandloss", conn)
        df_cf = pd.read_sql("SELECT * FROM cashflow", conn)
        conn.close()
        print(" Successfully loaded data from database!")
    except Exception as e:
        print(f" Error reading database: {e}")
        return

    # --- PERFECT CLEANING HELPER ---
    def clean_df(df):
        df.columns = [str(c).lower().strip() for c in df.columns]
        df = df.loc[:, ~df.columns.duplicated()]

        # Standardize ID
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

        return df

    df_pl = clean_df(df_pl)
    df_cf = clean_df(df_cf)

    if "year" not in df_pl.columns or "year" not in df_cf.columns:
        print(
            " Error: 'year' column is missing from the tables. Cannot calculate 5-year average."
        )
        return

    # ---------------------------------------------------------
    # FIXED COLUMN MATCHING LOGIC (Handles underscores & spaces)
    # ---------------------------------------------------------
    # Find Net Profit (PAT) column in P&L
    pat_col = next(
        (
            c
            for c in df_pl.columns
            if "net profit" in c.replace("_", " ")
            or "pat" in c
            or "profit after" in c.replace("_", " ")
            or "net_profit" in c
        ),
        None,
    )

    # Find Operating Cash Flow (CFO) column in Cashflow
    cfo_col = next(
        (
            c
            for c in df_cf.columns
            if "operating" in c.replace("_", " ")
            or "cfo" in c
            or "cash from op" in c.replace("_", " ")
            or "cash_from" in c
        ),
        None,
    )

    if not pat_col:
        print(
            f" Error: Could not find Net Profit/PAT column in P&L. Available: {list(df_pl.columns)}"
        )
        return
    if not cfo_col:
        print(
            f" Error: Could not find Operating Cash Flow column in Cashflow. Available: {list(df_cf.columns)}"
        )
        return

    print(f" Using '{pat_col}' for PAT and '{cfo_col}' for CFO.")

    # Merge P&L and Cashflow on company_id and year
    df_merged = pd.merge(
        df_pl[["company_id", "year", pat_col]],
        df_cf[["company_id", "year", cfo_col]],
        on=["company_id", "year"],
        how="inner",
    )

    # Convert to numeric safely
    df_merged[pat_col] = pd.to_numeric(df_merged[pat_col], errors="coerce").fillna(0)
    df_merged[cfo_col] = pd.to_numeric(df_merged[cfo_col], errors="coerce").fillna(0)

    # Sort to get the latest years first
    df_merged = df_merged.sort_values(
        by=["company_id", "year"], ascending=[True, False]
    )

    results = []

    # Process each company
    for company, group in df_merged.groupby("company_id"):
        # Get the latest 5 years of data (or less if 5 years aren't available)
        latest_5 = group.head(5)

        if len(latest_5) == 0:
            continue

        # Calculate sums over the 5 years
        total_cfo = latest_5[cfo_col].sum()
        total_pat = latest_5[pat_col].sum()

        # Calculate CFO Quality Score
        if total_pat > 0:
            cfo_quality_score = total_cfo / total_pat
        elif total_pat <= 0 and total_cfo > 0:
            # If company is making losses but still generating cash, that's high quality
            cfo_quality_score = 1.5
        else:
            cfo_quality_score = 0

        cfo_quality_score = round(cfo_quality_score, 2)

        # Assign Badge as per Sprint 4-5 requirements
        if cfo_quality_score > 1.0:
            badge = " High Quality Earnings"
        elif cfo_quality_score < 0.5:
            badge = " Accrual Risk"
        else:
            badge = " Average Quality"

        results.append(
            {
                "Company ID": company,
                "5-Year Total PAT": round(total_pat, 2),
                "5-Year Total CFO": round(total_cfo, 2),
                "CFO Quality Score": cfo_quality_score,
                "Quality Badge": badge,
            }
        )

    df_results = pd.DataFrame(results)

    if not df_results.empty:
        df_results.to_excel(output_file, index=False)
        print(f"\n CFO Quality Calculation complete for {len(df_results)} companies.")
        print(f" Report saved to: {output_file}\n")

        print(" SAMPLE OUTPUT:")
        print(df_results.head(5).to_string(index=False))
    else:
        print(" Could not generate scores.")


if __name__ == "__main__":
    calculate_cfo_quality()
