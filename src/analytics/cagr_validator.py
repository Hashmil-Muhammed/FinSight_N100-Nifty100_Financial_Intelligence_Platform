import pandas as pd
import sqlite3
import os
from pathlib import Path


def validate_cagr():
    """
    Compares the parsed CAGR numbers from analysis_parsed.csv
    against the Ratio Engine's computed CAGR in the database.
    Flags any divergence greater than 5%.
    """
    print(" Starting NLP : CAGR Cross-Validator...")

    # Define file paths
    root_path = Path(__file__).resolve().parents[2]
    parsed_file = os.path.join(root_path, "analysis_parsed.csv")
    output_file = os.path.join(root_path, "cross_validation.csv")

    db_path = os.path.join(root_path, "nifty100.db")
    if not os.path.exists(db_path):
        db_path = os.path.join(root_path, "data", "nifty100.db")

    if not os.path.exists(parsed_file):
        print(f" Error: {parsed_file} not found.")
        return
    if not os.path.exists(db_path):
        print(f" Error: Database nifty100.db not found at {db_path}.")
        return

    # Load the parsed data
    df_parsed = pd.read_csv(parsed_file)

    try:
        conn = sqlite3.connect(db_path)
        target_table = "financial_ratios"
        print(f"🔍 Reading metrics strictly from database table: '{target_table}'")

        df_db = pd.read_sql(f"SELECT * FROM {target_table}", conn)
        conn.close()
    except Exception as e:
        print(f" Error reading database: {e}")
        return

    # Clean DB columns and DROP DUPLICATES
    df_db.columns = [str(c).lower().strip() for c in df_db.columns]
    df_db = df_db.loc[:, ~df_db.columns.duplicated()]

    # FIND ID COLUMN SAFELY
    if "company_id" not in df_db.columns:
        known_names = ["id", "cid", "company", "symbol", "company name"]
        id_col = next((c for c in df_db.columns if c in known_names), None)
        if id_col:
            df_db.rename(columns={id_col: "company_id"}, inplace=True)
        else:
            df_db.rename(columns={df_db.columns[0]: "company_id"}, inplace=True)

    # FIX FOR THE 'str' ATTRIBUTE ERROR (Force Series)
    if isinstance(df_db["company_id"], pd.DataFrame):
        df_db["company_id"] = df_db["company_id"].iloc[:, 0]

    df_db["company_id"] = df_db["company_id"].astype(str).str.strip().str.upper()

    # NEW FIX: Sort by year descending so the newest records come first
    if "year" in df_db.columns:
        df_db = df_db.sort_values(by=["company_id", "year"], ascending=[True, False])

    results = []

    # Iterate through the parsed rows to cross-validate
    for index, row in df_parsed.iterrows():
        company = str(row["company_id"]).strip().upper()
        metric = str(row["metric_type"]).upper()

        try:
            period = int(float(row["period_years"]))
            parsed_val = float(row["value_pct"])
        except Exception:
            continue

        comp_data = df_db[df_db["company_id"] == company]
        if comp_data.empty:
            continue

        # EXACT COLUMN MAPPING
        expected_db_cols = []
        if "SALES" in metric or "REVENUE" in metric:
            expected_db_cols = [f"revenue_cagr_{period}y", f"sales_cagr_{period}y"]
        elif "PROFIT" in metric or "PAT" in metric:
            expected_db_cols = [f"pat_cagr_{period}y", f"profit_cagr_{period}y"]
        else:
            continue

        actual_db_col = None
        for expected in expected_db_cols:
            if expected in df_db.columns:
                actual_db_col = expected
                break

        if not actual_db_col:
            continue

        # THE ULTIMATE FIX: Drop rows where this specific CAGR is NULL/NaN
        valid_comp_data = comp_data.dropna(subset=[actual_db_col])
        if valid_comp_data.empty:
            continue

        # Now safely pick the latest valid year's value
        db_val_raw = valid_comp_data.iloc[0][actual_db_col]

        try:
            db_val = float(db_val_raw)
        except Exception:
            continue

        diff = abs(parsed_val - db_val)
        flag = " DIVERGENCE > 5%" if diff > 5.0 else "✅ MATCH"

        results.append(
            {
                "company_id": company,
                "metric_type": metric.title(),
                "period_years": period,
                "parsed_value": parsed_val,
                "db_column": actual_db_col,
                "db_value": round(db_val, 2),
                "absolute_diff": round(diff, 2),
                "status_flag": flag,
            }
        )

    # Create output dataframe
    df_results = pd.DataFrame(results)

    if not df_results.empty:
        df_results.to_csv(output_file, index=False)
        print(
            f"\n Cross-Validation complete! Checked {len(df_results)} matching records."
        )
        print(f" Report saved to: {output_file}\n")

        diverged = df_results[df_results["absolute_diff"] > 5.0]
        if not diverged.empty:
            print(f" FOUND {len(diverged)} RECORDS WITH >5% DIVERGENCE:")
            print(
                diverged[
                    ["company_id", "metric_type", "period_years", "absolute_diff"]
                ].to_string(index=False)
            )
        else:
            print(
                " Excellent! All cross-validated metrics match within the 5% threshold."
            )
    else:
        print("\n No matching metrics found.")


if __name__ == "__main__":
    validate_cagr()
