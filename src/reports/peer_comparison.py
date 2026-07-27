import pandas as pd
import sqlite3
import os


def generate_excel_report(
    db_path="nifty100.db", output_file="output/peer_comparison.xlsx"
):
    print("\n📊 Generating Report (Merging tables in Pandas)...")
    conn = sqlite3.connect(db_path)

    # 1. Fetch Ranks and Financial Data separately
    df_ranks = pd.read_sql("SELECT * FROM peer_percentiles", conn)
    df_ratios = pd.read_sql(
        "SELECT company_id, year, ROE, NPM FROM financial_ratios", conn
    )
    conn.close()

    # 2. Ensure year columns match for merging
    df_ranks["year"] = df_ranks["year"].astype(str).str.strip()
    df_ratios["year"] = df_ratios["year"].astype(str).str.strip()

    # 3. Merge based on company_id and year
    df = pd.merge(df_ranks, df_ratios, on=["company_id", "year"], how="left")

    # 4. Filter for the latest year
    latest_year = df["year"].max()
    df = df[df["year"] == latest_year].copy()

    # 5. Clean up: Fill missing values with 0
    df = df.fillna(0)

    # 6. Save to Excel
    os.makedirs("output", exist_ok=True)
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for group in df["peer_group_name"].unique():
            if pd.isna(group):
                continue
            subset = df[df["peer_group_name"] == group]
            sheet_name = str(group)[:31].replace("/", "-")
            subset.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"✅ Excel generated successfully at: {output_file}")


if __name__ == "__main__":
    generate_excel_report()
