import sqlite3
import pandas as pd

DB_PATH = "nifty100.db"


def run_manual_review():
    print("Starting Data Quality Manual Review...\n")

    with sqlite3.connect(DB_PATH) as conn:
        # 1. 5 Random Companies Review
        print("1. Random Companies")
        random_5 = pd.read_sql(
            "SELECT id, company_name FROM companies ORDER BY RANDOM() LIMIT 5", conn
        )
        print(random_5.to_string(index=False))
        print("\n")

        # 2. Check Year Coverage (< 5 years)
        print("2. Companies with <5 years of P&L Data")
        query = """
        SELECT company_id, COUNT(DISTINCT year) as year_count
        FROM profitandloss
        GROUP BY company_id
        HAVING year_count < 5
        """

        coverage_df = pd.read_sql(query, conn)

        if coverage_df.empty:
            print("All companies have 5 or more of data. No loader bugs found.")

        else:
            print("Warning: Found companies with less than 5 Years of data:")
            print(coverage_df.to_string(index=False))


if __name__ == "__main__":
    run_manual_review()
