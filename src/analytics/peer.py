import pandas as pd
import sqlite3
import os


def calculate_peer_percentiles(
    db_path="nifty100.db", peer_file="data/supporting/peer_groups.xlsx"
):
    print("Starting peer Group Percentile Calculation ....")

    # 1. Load Financial Ratios from Database
    with sqlite3.connect(db_path) as conn:
        # We take the latest year data for peer comparison
        ratios_df = pd.read_sql("SELECT * FROM financial_ratios", conn)

    # 2. Load Peer Groups Excel File
    if not os.path.exists(peer_file):
        print(f"Error: {peer_file} not found!")
        return
    peer_df = pd.read_excel(peer_file)

    # 💡 FIX: Get the actual name of the peer group column from the Excel file
    # (Assuming company_id is the first column and the peer group is the second column)
    peer_group_col = peer_df.columns[1]

    # 3. Merge both dataframes on company_id
    # Ensure both dataframes have the 'company_id' column for merging
    if "company_id" not in peer_df.columns:
        # If the first column is named something else like 'Ticker', rename it
        peer_df.rename(columns={peer_df.columns[0]: "company_id"}, inplace=True)

    df = pd.merge(ratios_df, peer_df, on="company_id", how="inner")

    # 4. Define metrics to rank
    # Note: For Debt_to_Equity, lower is better. For others, higher is better.
    metrics = {
        "ROE": True,
        "ROCE": True,
        "Net_Profit_Margin": True,
        "PAT_CAGR_5Y": True,
        "Debt_to_Equity": False,  # means lower debt gets higher rank
    }

    print(f"Calculating PERCENT_RANK for {len(df)} records across peer Groups...")

    # 5. Calculate Percentile Rank grouped by year and peer_group
    for metric, is_higher_better in metrics.items():
        if metric in df.columns:
            rank_col_name = f"{metric}_Rank"
            # Calculate rank (0 to 100)
            df[rank_col_name] = (
                df.groupby(["year", peer_group_col])[metric].rank(
                    pct=True, ascending=is_higher_better
                )
                * 100
            )
            # Fill NaN values with 0
            df[rank_col_name] = df[rank_col_name].fillna(0).round(2)

    # 6. Save to new Database Table (peer_percentiles)
    with sqlite3.connect(db_path) as conn:
        df.to_sql("peer_percentiles", conn, if_exists="replace", index=False)

    print(f"Successfully created 'peer_percentiles' table in {db_path}!")


if __name__ == "__main__":
    calculate_peer_percentiles()
