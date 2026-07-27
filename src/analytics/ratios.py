import sqlite3
import pandas as pd


class ProfitabilityEngine:
    def __init__(self, db_path="nifty100.db"):
        self.db_path = db_path

    def fetch_data(self):
        """
        P&L, Balance Sheet take data in the table.
        """
        query = """
        SELECT
            p.company_id,
            p.year,
            p.sales,
            p.operating_profit,
            p.profit_before_tax,
            p.interest,
            p.net_profit,
            p.opm_percentage as source_opm,
            b.equity_capital,
            b.reserves,
            b.borrowings
        FROM profitandloss p
        JOIN balancesheet b
            ON p.company_id = b.company_id AND p.year = b.year
        """
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df

    # --- Ratio Calculation Functions ---
    def calc_npm(self, row):
        if pd.isna(row["sales"]) or row["sales"] == 0:
            return None
        return round((row["net_profit"] / row["sales"]) * 100, 2)

    def calc_opm(self, row):
        if pd.isna(row["sales"]) or row["sales"] == 0:
            return None
        return round((row["operating_profit"] / row["sales"]) * 100, 2)

    def calc_roe(self, row):
        equity = row["equity_capital"] + row["reserves"]
        if pd.isna(equity) or equity <= 0:
            return None
        return round((row["net_profit"] / equity) * 100, 2)

    def calc_roce(self, row):
        equity = row["equity_capital"] + row["reserves"]
        capital_employed = equity + row["borrowings"]
        if pd.isna(capital_employed) or capital_employed <= 0:
            return None
        return round((row["operating_profit"] / capital_employed) * 100, 2)

    # --- Leverage & Efficiency Ratios (Day 09) ---
    def calc_debt_to_equity(self, row):
        # Edge Case 1: Bank Carve-out (Using company_id instead of sector)
        comp_id = str(row.get("company_id", "")).lower()
        if "bank" in comp_id or "fin" in comp_id or "sbi" in comp_id:
            return None

        equity = row["equity_capital"] + row["reserves"]
        if pd.isna(equity) or equity <= 0:
            return None
        return round(row["borrowings"] / equity, 2)

    def calc_icr(self, row):
        # Edge Case 2: Debt-free Substitution (Zero Interest)
        interest = row["interest"]
        pbt = row["profit_before_tax"]
        if pd.isna(interest) or interest <= 0:
            return 999.0  # High default value for debt-free companies
        return round(pbt / interest, 2)

    def calc_asset_turnover(self, row):
        # Proxy for total assets
        total_assets = row["equity_capital"] + row["reserves"] + row["borrowings"]
        sales = row["sales"]
        if pd.isna(total_assets) or total_assets <= 0 or pd.isna(sales):
            return None
        return round(sales / total_assets, 2)

    def run(self):
        print("Initializing Ratio Engine...\n")
        df = self.fetch_data()

        # Calculate all 7 ratios
        df["NPM"] = df.apply(self.calc_npm, axis=1)
        df["OPM"] = df.apply(self.calc_opm, axis=1)
        df["ROE"] = df.apply(self.calc_roe, axis=1)
        df["ROCE"] = df.apply(self.calc_roce, axis=1)
        df["D_E"] = df.apply(self.calc_debt_to_equity, axis=1)
        df["ICR"] = df.apply(self.calc_icr, axis=1)
        df["Asset_Turnover"] = df.apply(self.calc_asset_turnover, axis=1)

        print(f"✅ Successfully computed 7 ratios for {len(df)} records. \n")
        return df


if __name__ == "__main__":
    engine = ProfitabilityEngine()
    result_df = engine.run()

    print("📊 Sample Calculated Ratios (Leverage & Efficiency):")
    print(
        result_df[["company_id", "year", "D_E", "ICR", "Asset_Turnover"]]
        .head(10)
        .to_string(index=False)
    )
