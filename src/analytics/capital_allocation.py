import pandas as pd
import sqlite3
import os
from pathlib import Path


def generate_capital_allocation():
    """
    MCash Flow Intelligence
    Capital Allocation Matrix mapping 8 CFO/CFI/CFF sign patterns.
    Appends the result to cashflow_intelligence.xlsx.
    """
    print("Cash Flow Intelligence (Capital Allocation)...")

    root_path = Path(__file__).resolve().parents[2]
    output_file = os.path.join(root_path, "cashflow_intelligence.xlsx")
    db_path = os.path.join(root_path, "nifty100.db")

    if not os.path.exists(output_file):
        print(f" Error: {output_file} not found.")
        return

    # 1. LOAD EXISTING EXCEL FILE
    try:
        df_existing = pd.read_excel(output_file)
        # Standardize Company ID for clean merging
        df_existing["Company ID"] = (
            df_existing["Company ID"].astype(str).str.strip().str.upper()
        )
        print(" Successfully loaded existing cashflow_intelligence.xlsx")
    except Exception as e:
        print(f" Error reading Excel file: {e}")
        return

    # 2. LOAD DB CASHFLOW TABLE
    if not os.path.exists(db_path):
        db_path = os.path.join(root_path, "data", "nifty100.db")

    try:
        conn = sqlite3.connect(db_path)
        df_cf = pd.read_sql("SELECT * FROM cashflow", conn)
        conn.close()
        print(" Successfully loaded cashflow table from database.")
    except Exception as e:
        print(f" Error reading database: {e}")
        return

    # BULLETPROOF CLEANING HELPER
    def clean_df(df):
        # Standardize column names to lowercase
        df.columns = [str(c).lower().strip() for c in df.columns]
        df = df.loc[:, ~df.columns.duplicated()]

        # Identify the primary ID column dynamically
        id_col = next(
            (
                c
                for c in df.columns
                if c in ["id", "company_id", "cid", "company", "symbol"]
            ),
            None,
        )
        id_col = id_col if id_col else df.columns[0]

        # Drop existing 'company_id' if it conflicts with the detected ID column
        if "company_id" in df.columns and id_col != "company_id":
            df = df.drop(columns=["company_id"])

        df.rename(columns={id_col: "company_id"}, inplace=True)
        df = df.loc[:, ~df.columns.duplicated()]

        # Force column to be a Series if it accidentally became a DataFrame
        if isinstance(df["company_id"], pd.DataFrame):
            df["company_id"] = df["company_id"].iloc[:, 0]

        df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()
        return df

    df_cf = clean_df(df_cf)

    # 3. SMART COLUMN MATCHERS
    cfo_col = next(
        (c for c in df_cf.columns if "operating" in c.replace("_", " ") or "cfo" in c),
        None,
    )
    cfi_col = next(
        (c for c in df_cf.columns if "investing" in c.replace("_", " ") or "cfi" in c),
        None,
    )
    cff_col = next(
        (c for c in df_cf.columns if "financing" in c.replace("_", " ") or "cff" in c),
        None,
    )

    if not all([cfo_col, cfi_col, cff_col]):
        print(" Error: Could not find CFO, CFI, or CFF columns in database.")
        print(f"Found -> CFO: {cfo_col}, CFI: {cfi_col}, CFF: {cff_col}")
        return

    print(f" Using Columns -> CFO: '{cfo_col}', CFI: '{cfi_col}', CFF: '{cff_col}'")

    # Convert columns to numeric safely
    for col in [cfo_col, cfi_col, cff_col]:
        df_cf[col] = pd.to_numeric(df_cf[col], errors="coerce").fillna(0)

    # Sort strictly by descending year to get the most recent financial year first
    if "year" in df_cf.columns:
        df_cf = df_cf.sort_values(by=["company_id", "year"], ascending=[True, False])

    results = []

    # 4. CAPITAL ALLOCATION MATRIX LOGIC
    print(" Mapping 8 CFO/CFI/CFF sign patterns...")

    def get_allocation_label(cfo, cfi, cff):
        # Determine the sign for each cash flow component
        s_cfo = "+" if cfo > 0 else "-"
        s_cfi = "+" if cfi > 0 else "-"
        s_cff = "+" if cff > 0 else "-"
        pattern = f"{s_cfo}{s_cfi}{s_cff}"

        # Standard Financial Analysis Matrix for the 8 permutations
        matrix = {
            "+--": "Mature / Cash Cow (Reinvesting & Paying Debt/Dividends)",
            "+-+": "Aggressive Growth (Funding CapEx with Ops + External Capital)",
            "++-": "Restructuring (Selling Assets to Pay Down Debt)",
            "+++": "Cash Hoarder (Generating Ops Cash, Selling Assets, Raising Capital)",
            "---": "Severe Distress (Burning Ops Cash, Investing, Paying Debt - Draining Reserves)",
            "--+": "Start-up / High Growth (Burning Ops Cash, Investing Heavily, Externally Funded)",
            "-+-": "Struggling (Selling Assets to cover Operational Burn & Debt)",
            "-++": "Distress & Restructuring (Burning Ops, Selling Assets, Raising Capital to Survive)",
        }
        return matrix.get(pattern, "Unknown Pattern")

    # Get the latest year data for each company and evaluate the matrix
    for company, group in df_cf.groupby("company_id"):
        latest_record = group.iloc[0]
        label = get_allocation_label(
            latest_record[cfo_col], latest_record[cfi_col], latest_record[cff_col]
        )

        results.append({"Company ID": company, "Capital Allocation Label": label})

    df_results = pd.DataFrame(results)

    # 5. MERGE WITH EXISTING DATA AND SAVE
    if not df_results.empty:
        df_final = pd.merge(df_existing, df_results, on="Company ID", how="left")
        df_final.to_excel(output_file, index=False)

        print(
            f"\n Complete! Appended Capital Allocation Matrix for {len(df_results)} companies."
        )
        print(f" Report updated at: {output_file}\n")

        print(" SAMPLE UPDATED OUTPUT:")
        cols_to_show = ["Company ID", "Capital Allocation Label"]
        print(df_final[cols_to_show].head(7).to_string(index=False))
    else:
        print(" Could not map allocation patterns.")


if __name__ == "__main__":
    generate_capital_allocation()
