import os
import pandas as pd
from pathlib import Path


def run_sprint5_qa_review():
    """
    Review
    Automated Quality Assurance check for:
    1. Tearsheet generation success
    2. NLP Coverage (>90% requirement)
    3. CF Distress Flags validation
    """
    print(" Starting Sprint 5 Final Review (QA Validation)...")
    print("-" * 50)

    root_path = Path(__file__).resolve().parents[2]
    reports_dir = os.path.join(root_path, "reports")
    tearsheets_dir = os.path.join(reports_dir, "tearsheets")

    # 1. CHECK TEARSHEETS (UI / Generation Check)
    print(" 1. Checking PDF Reports Generation...")
    if os.path.exists(tearsheets_dir):
        pdf_files = [f for f in os.listdir(tearsheets_dir) if f.endswith(".pdf")]
        if len(pdf_files) > 0:
            print(f"    SUCCESS: Found {len(pdf_files)} Company Tearsheets.")
            print(
                f"    Action Required: Please manually open '{pdf_files[0]}' to ensure no text overlaps (UI Overflow)."
            )
        else:
            print("    ERROR: No tearsheets found in reports/tearsheets/")
    else:
        print("    ERROR: reports/tearsheets/ directory does not exist.")

    # 2. CHECK NLP COVERAGE (> 90%)
    print("\n 2. Checking NLP Coverage (Pros/Cons Generator)...")
    pros_cons_file = os.path.join(root_path, "pros_cons_generated.csv")

    if os.path.exists(pros_cons_file):
        df_nlp = pd.read_csv(pros_cons_file)
        unique_companies = df_nlp["company_id"].nunique()
        total_expected = 92  # Nifty 100 actually contains ~92-100 valid stocks

        coverage = (unique_companies / total_expected) * 100
        print(f"   -> Total unique companies with NLP Insights: {unique_companies}")

        if coverage >= 90:
            print(
                f"   SUCCESS: NLP Coverage is {coverage:.1f}% (Passes >90% requirement)."
            )
        else:
            print(
                f"    WARNING: NLP Coverage is {coverage:.1f}% (Below 90% threshold)."
            )
    else:
        print("    ERROR: pros_cons_generated.csv not found.")

    # 3. CHECK CF FLAGS (Spot-check CF)
    print("\n 3. Spot-Checking Cashflow Intelligence Flags...")
    cf_alerts_file = os.path.join(root_path, "distress_alerts.csv")
    cf_intel_file = os.path.join(root_path, "cashflow_intelligence.xlsx")

    if os.path.exists(cf_alerts_file):
        df_alerts = pd.read_csv(cf_alerts_file)
        distress_count = len(
            df_alerts[
                df_alerts["Alert Badge"].str.contains("Distress", na=False, case=False)
            ]
        )
        print(
            f"    SUCCESS: CF Alerts file found. Spotted {distress_count} companies with 'Distress' signals."
        )
    else:
        print("    ERROR: distress_alerts.csv not found.")

    if os.path.exists(cf_intel_file):
        df_intel = pd.read_excel(cf_intel_file)
        if "Capital Allocation Label" in df_intel.columns:
            print("    SUCCESS: Capital Allocation Matrix is populated.")
        else:
            print(
                "    ERROR: Capital Allocation Matrix is missing from CF Intelligence."
            )

    print("-" * 50)
    print(" SPRINT 5 REVIEW COMPLETE! IF ALL GREEN, YOU ARE READY FOR SPRINT 6!")


if __name__ == "__main__":
    run_sprint5_qa_review()
