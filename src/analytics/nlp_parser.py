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
    print("Starting NLP task: CAGR Cross-Validator...")

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

    # Load database data
    try:
        conn = sqlite3.connect(db_path)
        # Read the table
        df_db = pd.read_sql("SELECT * FROM financial_ratios", conn)
        conn.close()
        print(" Successfully loaded database metrics.")
    except Exception as e:
        print(f" Error reading database: {e}")
        return

    # Super-clean DB columns
    df_db.columns = [str(c).lower().strip() for c in df_db.columns]

    # Find ID col safely
    known_names = ["id", "company_id", "cid", "company", "symbol"]
    id_col = next((c for c in df_db.columns if c in known_names), None)

    if not id_col:
        id_col = df_db.columns[0]

    df_db.rename(columns={id_col: "company_id"}, inplace=True)
    df_db["company_id"] = df_db["company_id"].astype(str).str.strip().str.upper()

    results = []
    not_found_logs = []

    # Iterate through the parsed rows to cross-validate
    for _, row in df_parsed.iterrows():
        company = str(row["company_id"]).strip().upper()
        metric = str(row["metric_type"]).upper()

        try:
            period = int(float(row["period_years"]))
            parsed_val = float(row["value_pct"])
        except Exception:
            continue

        # Filter DB for this company
        comp_data = df_db[df_db["company_id"] == company]
        if comp_data.empty:
            if company not in not_found_logs:
                print(
                    f"DB Warning: Company '{company}' not found in financial_ratios table."
                )
                not_found_logs.append(company)
            continue

        # Map metric names to multiple possible DB column patterns
        expected_db_cols = []
        if "SALES" in metric or "REVENUE" in metric:
            expected_db_cols = [
                f"revenue_cagr_{period}y",
                f"sales_cagr_{period}y",
                f"revenue_cagr_{period}",
            ]
        elif "PROFIT" in metric or "PAT" in metric:
            expected_db_cols = [
                f"pat_cagr_{period}y",
                f"profit_cagr_{period}y",
                f"pat_cagr_{period}",
            ]
        else:
            continue

        # Find actual column
        actual_db_col = None
        for expected in expected_db_cols:
            match = next((c for c in df_db.columns if expected in c), None)
            if match:
                actual_db_col = match
                break

        if actual_db_col:
            db_val = comp_data.iloc[0][actual_db_col]

            # Convert safely avoiding string errors like "N/A"
            try:
                db_val = float(db_val)
                if pd.isna(db_val):
                    continue
            except (ValueError, TypeError):
                continue

            diff = abs(parsed_val - db_val)
            flag = " DIVERGENCE > 5%" if diff > 5.0 else " MATCH"

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
        else:
            print(
                f"DB Warning: Could not find any column matching {expected_db_cols} for '{company}'."
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
            print(f"FOUND {len(diverged)} RECORDS WITH >5% DIVERGENCE:")
            print(
                diverged[
                    ["company_id", "metric_type", "period_years", "absolute_diff"]
                ].to_string(index=False)
            )
        else:
            print(
                "Excellent! All cross-validated metrics match within the 5% threshold."
            )
    else:
        print(
            "\n No matching metrics found after applying flexible searches. Please check the warnings above."
        )


if __name__ == "__main__":
    validate_cagr()
