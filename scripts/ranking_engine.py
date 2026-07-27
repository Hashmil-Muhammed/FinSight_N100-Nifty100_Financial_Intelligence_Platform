import pandas as pd
import sqlite3
import os

DB_PATH = os.path.join("nifty100.db")
OUTPUT_FILE = "screener_output.xlsx"


def build_ranking_engine():
    conn = sqlite3.connect(DB_PATH)
    # Getting data from financial_ratios and market_cap for valuation
    df_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
    df_market = pd.read_sql("SELECT * FROM market_cap", conn)
    conn.close()

    # Merging data
    df = pd.merge(df_ratios, df_market, on=["company_id", "year"])
    df = df[df["year"] == df["year"].max()]  # Latest year

    # 1. Normalizing columns (0 to 1 scale)
    # Profitability (ROE, ROCE)
    # Change this line in your ranking_engine.py
    df["profitability_score"] = ((df["ROE"] / 100) + (df["ROCE"] / 100)) / 2

    # Growth (Revenue_CAGR_3Y, PAT_CAGR_3Y)
    df["growth_score"] = (df["Revenue_CAGR_3Y"] + df["PAT_CAGR_3Y"]) / 2

    # Valuation (Inverse of PE - lower PE is better for value)
    df["valuation_score"] = 1 / df["pe_ratio"]

    # 2. Calculating Composite Score (50% Profitability, 30% Growth, 20% Valuation)
    df["composite_score"] = (
        (df["profitability_score"] * 0.5)
        + (df["growth_score"] * 0.3)
        + (df["valuation_score"] * 20)
    )  # Scaling valuation

    # 3. Ranking
    df = df.sort_values(by="composite_score", ascending=False)

    # Export to Excel
    df[
        ["company_id", "composite_score", "ROE", "Revenue_CAGR_3Y", "pe_ratio"]
    ].to_excel(OUTPUT_FILE, index=False)
    print(f"Ranking engine completed! Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    build_ranking_engine()
