import pandas as pd
import sqlite3
import os
from pathlib import Path


def generate_pros_cons():
    """
    Builds a rule engine with 12 positive and 12 negative rules based on KPIs
    to auto-generate pros and cons for companies.
    """
    print(" Starting NLP : Auto Pros/Cons Rule Engine ...")

    root_path = Path(__file__).resolve().parents[2]
    output_file = os.path.join(root_path, "pros_cons_generated.csv")

    db_path = os.path.join(root_path, "nifty100.db")
    if not os.path.exists(db_path):
        db_path = os.path.join(root_path, "data", "nifty100.db")

    if not os.path.exists(db_path):
        print(f" Error: Database nifty100.db not found at {db_path}.")
        return

    try:
        conn = sqlite3.connect(db_path)

        # Verify financial_ratios table exists
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='financial_ratios';"
        )
        if not cursor.fetchone():
            print(" Error: 'financial_ratios' table not found in database.")
            return

        df_db = pd.read_sql("SELECT * FROM financial_ratios", conn)
        conn.close()
        print(" Successfully loaded financial metrics from database.")
    except Exception as e:
        print(f" Error reading database: {e}")
        return

    # Clean DB columns
    df_db.columns = [str(c).lower().strip() for c in df_db.columns]
    df_db = df_db.loc[:, ~df_db.columns.duplicated()]

    # Safely extract Company ID
    id_col = next(
        (
            c
            for c in df_db.columns
            if c in ["id", "company_id", "cid", "company", "symbol"]
        ),
        None,
    )
    if id_col:
        df_db.rename(columns={id_col: "company_id"}, inplace=True)
    else:
        df_db.rename(columns={df_db.columns[0]: "company_id"}, inplace=True)

    if isinstance(df_db["company_id"], pd.DataFrame):
        df_db["company_id"] = df_db["company_id"].iloc[:, 0]

    df_db["company_id"] = df_db["company_id"].astype(str).str.strip().str.upper()

    # Sort to ensure we process the latest year's data for each company
    if "year" in df_db.columns:
        df_db = df_db.sort_values(by=["company_id", "year"], ascending=[True, False])

    # Drop duplicates to keep only the latest record per company
    df_latest = df_db.drop_duplicates(subset=["company_id"], keep="first")

    # Helper function to safely get numeric values
    def get_val(row, col_name, default=None):
        if col_name in row.index and pd.notna(row[col_name]):
            try:
                return float(row[col_name])
            except ValueError:
                return default
        return default

    results = []

    print(" Running 12 Pro & 12 Con rules engine...")

    # Iterate through each company
    for _, row in df_latest.iterrows():
        company = row["company_id"]

        # Extract required KPIs safely
        roe = get_val(row, "roe")
        roce = get_val(row, "roce")
        d_e = get_val(row, "d_e")
        npm = get_val(row, "npm")
        opm = get_val(row, "opm")
        icr = get_val(row, "icr")
        fcf = get_val(row, "fcf")
        rev_cagr_3y = get_val(row, "revenue_cagr_3y")
        pat_cagr_3y = get_val(row, "pat_cagr_3y")
        cfo_quality = get_val(row, "cfo_quality_score")
        capex_int = get_val(row, "capex_intensity")
        asset_to = get_val(row, "asset_turnover")

        # ==========================================
        # 12 POSITIVE RULES (PROS)
        # ==========================================
        if roe is not None and roe > 20:
            results.append(
                {
                    "company_id": company,
                    "type": "Pro",
                    "rule_triggered": "ROE > 20%",
                    "text": f"High Return on Equity of {roe}%, indicating highly efficient use of shareholder capital.",
                    "confidence_pct": 95,
                }
            )

        if d_e is not None and d_e < 0.1:
            results.append(
                {
                    "company_id": company,
                    "type": "Pro",
                    "rule_triggered": "D/E < 0.1",
                    "text": "Virtually debt-free business, significantly reducing financial and interest rate risks.",
                    "confidence_pct": 98,
                }
            )

        if rev_cagr_3y is not None and rev_cagr_3y > 15:
            results.append(
                {
                    "company_id": company,
                    "type": "Pro",
                    "rule_triggered": "Rev CAGR > 15%",
                    "text": f"Strong top-line growth with a 3-year Revenue CAGR of {rev_cagr_3y}%.",
                    "confidence_pct": 90,
                }
            )

        if pat_cagr_3y is not None and pat_cagr_3y > 15:
            results.append(
                {
                    "company_id": company,
                    "type": "Pro",
                    "rule_triggered": "PAT CAGR > 15%",
                    "text": "Robust profitability growth demonstrating strong earnings momentum over 3 years.",
                    "confidence_pct": 90,
                }
            )

        if fcf is not None and fcf > 0:
            results.append(
                {
                    "company_id": company,
                    "type": "Pro",
                    "rule_triggered": "FCF Positive",
                    "text": "Consistent positive Free Cash Flow generation.",
                    "confidence_pct": 85,
                }
            )

        if opm is not None and opm > 20:
            results.append(
                {
                    "company_id": company,
                    "type": "Pro",
                    "rule_triggered": "OPM > 20%",
                    "text": "High Operating Profit Margins demonstrating strong pricing power in the market.",
                    "confidence_pct": 92,
                }
            )

        if roce is not None and roce > 20:
            results.append(
                {
                    "company_id": company,
                    "type": "Pro",
                    "rule_triggered": "ROCE > 20%",
                    "text": "Excellent Return on Capital Employed, showing effective capital allocation.",
                    "confidence_pct": 94,
                }
            )

        if icr is not None and icr > 5:
            results.append(
                {
                    "company_id": company,
                    "type": "Pro",
                    "rule_triggered": "ICR > 5",
                    "text": "Strong Interest Coverage Ratio; the company can comfortably service its debt obligations.",
                    "confidence_pct": 88,
                }
            )

        if npm is not None and npm > 15:
            results.append(
                {
                    "company_id": company,
                    "type": "Pro",
                    "rule_triggered": "NPM > 15%",
                    "text": "Healthy Net Profit Margins, retaining a solid portion of total revenues.",
                    "confidence_pct": 85,
                }
            )

        if cfo_quality is not None and cfo_quality > 1.0:
            results.append(
                {
                    "company_id": company,
                    "type": "Pro",
                    "rule_triggered": "CFO > PAT",
                    "text": "High earnings quality with Cash Flow from Operations exceeding Net Profit.",
                    "confidence_pct": 96,
                }
            )

        if capex_int is not None and capex_int < 5:
            results.append(
                {
                    "company_id": company,
                    "type": "Pro",
                    "rule_triggered": "CapEx < 5%",
                    "text": "Asset-light business model requiring low capital expenditure.",
                    "confidence_pct": 82,
                }
            )

        if asset_to is not None and asset_to > 1.5:
            results.append(
                {
                    "company_id": company,
                    "type": "Pro",
                    "rule_triggered": "Asset TO > 1.5",
                    "text": "High Asset Turnover indicating highly efficient utilization of company assets.",
                    "confidence_pct": 80,
                }
            )

        # ==========================================
        # 12 NEGATIVE RULES (CONS)
        # ==========================================
        if roe is not None and roe < 10:
            results.append(
                {
                    "company_id": company,
                    "type": "Con",
                    "rule_triggered": "ROE < 10%",
                    "text": f"Subpar Return on Equity of {roe}%, indicating poor returns for shareholders.",
                    "confidence_pct": 90,
                }
            )

        if d_e is not None and d_e > 2.0:
            results.append(
                {
                    "company_id": company,
                    "type": "Con",
                    "rule_triggered": "D/E > 2",
                    "text": "High financial leverage which increases susceptibility to interest rate hikes.",
                    "confidence_pct": 95,
                }
            )

        if rev_cagr_3y is not None and rev_cagr_3y < 5:
            results.append(
                {
                    "company_id": company,
                    "type": "Con",
                    "rule_triggered": "Rev CAGR < 5%",
                    "text": "Sluggish top-line revenue growth over the past 3 years.",
                    "confidence_pct": 85,
                }
            )

        if pat_cagr_3y is not None and pat_cagr_3y < 0:
            results.append(
                {
                    "company_id": company,
                    "type": "Con",
                    "rule_triggered": "PAT CAGR < 0",
                    "text": "Negative profit growth (degrowth) over a 3-year period.",
                    "confidence_pct": 98,
                }
            )

        if fcf is not None and fcf < 0:
            results.append(
                {
                    "company_id": company,
                    "type": "Con",
                    "rule_triggered": "FCF Negative",
                    "text": "Negative Free Cash Flow, potentially requiring external funding.",
                    "confidence_pct": 88,
                }
            )

        if opm is not None and opm < 10:
            results.append(
                {
                    "company_id": company,
                    "type": "Con",
                    "rule_triggered": "OPM < 10%",
                    "text": "Low Operating Margins, vulnerable to input cost inflation.",
                    "confidence_pct": 85,
                }
            )

        if roce is not None and roce < 10:
            results.append(
                {
                    "company_id": company,
                    "type": "Con",
                    "rule_triggered": "ROCE < 10%",
                    "text": "Poor Return on Capital Employed, indicating inefficient capital use.",
                    "confidence_pct": 92,
                }
            )

        if icr is not None and icr < 2:
            results.append(
                {
                    "company_id": company,
                    "type": "Con",
                    "rule_triggered": "ICR < 2",
                    "text": "Weak Interest Coverage, pointing to potential debt servicing stress.",
                    "confidence_pct": 96,
                }
            )

        if npm is not None and npm < 5:
            results.append(
                {
                    "company_id": company,
                    "type": "Con",
                    "rule_triggered": "NPM < 5%",
                    "text": "Razor-thin Net Profit Margins leaving little room for operational errors.",
                    "confidence_pct": 88,
                }
            )

        if cfo_quality is not None and cfo_quality < 0.5:
            results.append(
                {
                    "company_id": company,
                    "type": "Con",
                    "rule_triggered": "CFO << PAT",
                    "text": "Low quality of earnings; Operating Cash Flow is significantly lower than reported profits.",
                    "confidence_pct": 95,
                }
            )

        if capex_int is not None and capex_int > 15:
            results.append(
                {
                    "company_id": company,
                    "type": "Con",
                    "rule_triggered": "CapEx > 15%",
                    "text": "Highly capital-intensive business requiring continuous heavy reinvestment.",
                    "confidence_pct": 85,
                }
            )

        if d_e is not None and d_e > 1.0 and icr is not None and icr < 3:
            results.append(
                {
                    "company_id": company,
                    "type": "Con",
                    "rule_triggered": "High Debt + Low ICR",
                    "text": "Dangerous combination of high debt and low interest coverage.",
                    "confidence_pct": 99,
                }
            )

    # Save Results
    df_results = pd.DataFrame(results)

    if not df_results.empty:
        df_results.to_csv(output_file, index=False)
        print(
            f"\n Rule Engine Complete! Generated {len(df_results)} Pros & Cons across the portfolio."
        )
        print(f" Report saved to: {output_file}\n")

        # Quick Summary
        total_pros = len(df_results[df_results["type"] == "Pro"])
        total_cons = len(df_results[df_results["type"] == "Con"])
        print(" SUMMARY:")
        print(f"   -> Total Pros Generated: {total_pros}")
        print(f"   -> Total Cons Generated: {total_cons}")

        print("\n Sample Output:")
        print(df_results.head(7).to_string(index=False))
    else:
        print(" No Pros or Cons generated. Check if KPI metrics exist in the database.")


if __name__ == "__main__":
    generate_pros_cons()
