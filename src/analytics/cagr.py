import sqlite3
import pandas as pd


class CAGREngine:
    def __init__(self, db_path="nifty100.db"):
        self.db_path = db_path

    def fetch_data(self):
        """fetch data from the P&L table (ordered by Company ID and Year)"""
        query = """
        SELECT company_id,  year, sales, net_profit, eps
        FROM profitandloss
        ORDER BY company_id, year
        """

        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df

    def compute_cagr(self, start_val, end_val, periods):
        """
        computes and returns the CAGR and a Turnaround flag (CAGR, Is_Turnaround).
        """

        if pd.isna(start_val) or pd.isna(end_val) or periods == 0:
            return None, False

        # Turnaround Logic: Previously in loss (<= 0), currently in profit (> 0)
        if start_val <= 0 and end_val > 0:
            return None, True

        # Previously in loss OR Currently in loss (CAGR cannot be calculated mathematically)
        if start_val <= 0 or end_val <= 0:
            return None, False

        # Standard CAGR Formula: ((End / Start) ^ (1/N)) - 1
        cagr = ((end_val / start_val) ** (1 / periods)) - 1
        return round(cagr * 100, 2), False

    def run(self):
        print("Initializing CAGR Calculation Engine...\n")
        df = self.fetch_data()

        windows = [3, 5, 10]
        metrics = {"sales": "Revenue", "net_profit": "PAT", "eps": "EPS"}

        results = []

        # Group by company and calculate metrics individually
        for _, group in df.groupby("company_id"):
            group = group.reset_index(drop=True)

            for i, row in group.iterrows():
                res_row = {"company_id": row["company_id"], "year": row["year"]}

                for w in windows:
                    # Check if data from 'w' years ago exists
                    if i >= w:
                        prev_row = group.iloc[i - w]

                        for col, name in metrics.items():
                            val, turnaround = self.compute_cagr(
                                prev_row[col], row[col], w
                            )
                            res_row[f"{name}_CAGR_{w}Y"] = val

                            # Set Turnaround flag exclusively for Net Profit (PAT)
                            if name == "PAT":
                                res_row[f"PAT_Turnaround_{w}Y"] = turnaround
                    else:
                        for col, name in metrics.items():
                            res_row[f"{name}_CAGR_{w}Y"] = None
                            if name == "PAT":
                                res_row[f"PAT_Turnaround_{w}Y"] = False
                results.append(res_row)

        final_df = pd.DataFrame(results)
        print(f"Successfully computed CAGR metrics for {len(final_df)} records. \n")

        # Display the list of Turnaround companies, if any exist
        turnarounds = final_df[final_df["PAT_Turnaround_5Y"] == True]
        if not turnarounds.empty:
            print(
                "Note: Found Turnaround Companies (Navigate to Positive PAT in 5Y windows):"
            )
            print("\n")

        return final_df


if __name__ == "__main__":
    engine = CAGREngine()
    results_df = engine.run()

    print("Sample Calculated CAGR (10Y Window):")
    # Filter and display companies that have 10-year data available.
    sample = results_df.dropna(subset=["Revenue_CAGR_10Y"]).head(10)
    cols_to_show = [
        "company_id",
        "year",
        "Revenue_CAGR_10Y",
        "PAT_CAGR_10Y",
        "EPS_CAGR_10Y",
    ]
    print(sample[cols_to_show].to_string(index=False))
