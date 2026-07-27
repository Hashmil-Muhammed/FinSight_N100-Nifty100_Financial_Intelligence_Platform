import pandas as pd
import sqlite3
import os
from pathlib import Path


def calculate_fcf_cagr():
    """
    Cash Flow Intelligence
    Computes 5-year and 10-year FCF CAGR, applying turnaround flags.
    Appends the results to the existing cashflow_intelligence.xlsx file.
    """
    print(" Cash Flow Intelligence ...")

    root_path = Path(__file__).resolve().parents[2]
    output_file = os.path.join(root_path, "cashflow_intelligence.xlsx")
    db_path = os.path.join(root_path, "nifty100.db")

    # 1. LOAD EXISTING EXCEL FILE
    if not os.path.exists(output_file):
        print(f" Error: {output_file} not found.")
        return

    try:
        df_existing = pd.read_excel(output_file)
        df_existing["Company ID"] = (
            df_existing["Company ID"].astype(str).str.strip().str.upper()
        )
        print(" Successfully loaded existing cashflow_intelligence.xlsx")
    except Exception as e:
        print(f" Error reading Excel file: {e}")
        return

    # 2. LOAD DB CASHFLOW TABLE
    try:
        conn = sqlite3.connect(db_path)
        df_cf = pd.read_sql("SELECT * FROM cashflow", conn)
        conn.close()
    except Exception as e:
        print(f" Error reading database: {e}")
        return

    #  CLEANING HELPER
    def clean_df(df):
        df.columns = [str(c).lower().strip() for c in df.columns]
        df = df.loc[:, ~df.columns.duplicated()]

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

    df_cf = clean_df(df_cf)

    # 3. SMART COLUMN MATCHERS FOR CFO AND CAPEX
    cfo_col = next(
        (
            c
            for c in df_cf.columns
            if "operating" in c.replace("_", " ") or "cfo" in c or "cash_from" in c
        ),
        None,
    )
    capex_col = None
    for c in df_cf.columns:
        if "capex" in c or "fixed_assets" in c or "capital_expenditure" in c:
            capex_col = c
            break
    if not capex_col:
        capex_col = next(
            (c for c in df_cf.columns if "investing" in c.replace("_", " ")), None
        )

    if not cfo_col or not capex_col:
        print(" Error: Could not find CFO or CapEx columns in cashflow table.")
        return

    print(f" Using Columns -> CFO: '{cfo_col}', CapEx: '{capex_col}'")

    # Convert to numeric safely
    df_cf[cfo_col] = pd.to_numeric(df_cf[cfo_col], errors="coerce").fillna(0)
    df_cf[capex_col] = pd.to_numeric(df_cf[capex_col], errors="coerce").fillna(0)

    # Calculate Free Cash Flow (FCF = Operating Cash Flow - Absolute value of CapEx)
    df_cf["fcf"] = df_cf[cfo_col] - df_cf[capex_col].abs()

    if "year" not in df_cf.columns:
        print(" Error: 'year' column is missing from cashflow table.")
        return

    # Sort strictly by descending year to get newest records first
    df_cf = df_cf.sort_values(by=["company_id", "year"], ascending=[True, False])

    # 4. HELPER FUNCTION TO CALCULATE CAGR OR ASSIGN TURNAROUND FLAGS
    def calc_cagr(start_val, end_val, years):
        if pd.isna(start_val) or pd.isna(end_val):
            return "N/A"

        if start_val < 0 and end_val > 0:
            return "Turnaround "
        elif start_val <= 0 and end_val <= 0:
            return "Negative"
        elif start_val > 0 and end_val <= 0:
            return "Turned Negative "
        elif start_val > 0 and end_val > 0:
            cagr = ((end_val / start_val) ** (1 / years) - 1) * 100
            return f"{round(cagr, 2)}%"

        return "N/A"

    results = []

    # 5. PROCESS EACH COMPANY
    for company, group in df_cf.groupby("company_id"):
        # Reset index to access rows by their order (0 is the latest year)
        group = group.reset_index(drop=True)

        latest_fcf = group.iloc[0]["fcf"] if len(group) > 0 else None

        # 5-Year CAGR (Using data from 5 periods ago)
        fcf_5y_ago = group.iloc[5]["fcf"] if len(group) > 5 else None
        cagr_5y = (
            calc_cagr(fcf_5y_ago, latest_fcf, 5)
            if fcf_5y_ago is not None
            else "Insufficient Data"
        )

        # 10-Year CAGR (Using data from 10 periods ago)
        fcf_10y_ago = group.iloc[10]["fcf"] if len(group) > 10 else None
        cagr_10y = (
            calc_cagr(fcf_10y_ago, latest_fcf, 10)
            if fcf_10y_ago is not None
            else "Insufficient Data"
        )

        results.append(
            {
                "Company ID": company,
                "FCF CAGR (5Y)": cagr_5y,
                "FCF CAGR (10Y)": cagr_10y,
            }
        )

    # 6. MERGE AND SAVE
    df_new = pd.DataFrame(results)

    if not df_new.empty:
        df_final = pd.merge(df_existing, df_new, on="Company ID", how="left")
        df_final.to_excel(output_file, index=False)

        print(f"\n Complete! Appended FCF CAGR for {len(df_new)} companies.")
        print(f" Report updated at: {output_file}\n")

        print(" SAMPLE UPDATED OUTPUT:")
        cols_to_show = ["Company ID", "FCF CAGR (5Y)", "FCF CAGR (10Y)"]
        print(df_final[cols_to_show].head(10).to_string(index=False))
    else:
        print(" Could not calculate CAGR.")


if __name__ == "__main__":
    calculate_fcf_cagr()
