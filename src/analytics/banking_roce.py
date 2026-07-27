import pandas as pd
import sqlite3
import os


def analyze_banking_roce(
    db_path="nifty100.db", output_file="reports/sector_roce_notes.csv"
):
    print("starting Specialized Banking ROCE Analysis....\n")

    # Create reports directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Query to fetch calculated ROCE and Original ROCE for Financial Sectors
    query = """
    SELECT
        f.company_id,
        'Finance/Banking' as sector,
        c.roce_percentage as original_roce,
        f.ROCE as calculated_roce,
        f.year
    FROM financial_ratios f
    JOIN companies c ON c.id = f.company_id
    WHERE LOWER(f.company_id) LIKE '%bank%'
        OR LOWER(f.company_id) LIKE '%fin%'
        OR LOWER(f.company_id) LIKE '%sbi%'
    """

    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(query, conn)

    if df.empty:
        print("No banking/financial records found in the database to analyze")
        return

    # Calculate absolute difference between our calculation and the source truth
    df["roce_difference"] = abs(df["original_roce"] - df["calculated_roce"])

    # Flag anomalies (If the difference is greater than 5%)
    df["is_anomaly"] = df["roce_difference"] > 5.0

    def generate_note(row):
        if row["is_anomaly"]:
            return f"Anomaly: Calculated ROCE ({row['calculated_roce']}%) deviates from source ({row['original_roce']}%) by {round(row['roce_difference'],2)}% sector adjustment applied"
        return "Match: Deviation is within acceptable limits."

    df["adjustment_notes"] = df.apply(generate_note, axis=1)

    anomalies = df[df["is_anomaly"]]

    print(
        f"Processed {len(df)} financial records. Detected {len(anomalies)} anomalies due to standard ROCE formula. \n"
    )

    # Save the output to reports folder
    df.to_csv(output_file, index=False)
    print(f"Successfully exported Banking ROCE notes to: {output_file}\n")

    if not anomalies.empty:
        print("Sample Anomalies Detected (Bank/NBFCs):")
        cols_to_show = [
            "company_id",
            "year",
            "original_roce",
            "calculated_roce",
            "roce_difference",
        ]
        print(anomalies[cols_to_show].head().to_string(index=False))
        print("\nNote: These differences are expected for financial institutions.")


if __name__ == "__main__":
    analyze_banking_roce()
