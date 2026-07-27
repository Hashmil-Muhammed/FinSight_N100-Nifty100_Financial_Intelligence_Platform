import pandas as pd
import sqlite3
import yaml
import os



class ScreenerEngine:
    def __init__(
        self, db_path="nifty100.db", config_path="config/screener_config.yaml"
    ):
        self.db_path = db_path

        # Ensure the config file exists before trying to open it
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def fetch_data(self):
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql("SELECT * FROM financial_ratios", conn)

    def apply_filter(self, df, criteria):
        """Applies multiple threshold filters based on the YAML config."""

        # Quality
        if "roe" in criteria and "ROE" in df.columns:
            df = df[df["ROE"] >= criteria["roe"]]
        if "debt_to_equity" in criteria and "Debt_to_Equity" in df.columns:
            df = df[df["Debt_to_Equity"] <= criteria["debt_to_equity"]]
        if "fcf" in criteria and "Free_Cash_Flow" in df.columns:
            df = df[df["Free_Cash_Flow"] > criteria["fcf"]]

        # Value
        if "pe_ratio" in criteria and "PE_Ratio" in df.columns:
            df = df[df["PE_Ratio"] <= criteria["pe_ratio"]]
        if "pb_ratio" in criteria and "PB_Ratio" in df.columns:
            df = df[df["PB_Ratio"] <= criteria["pb_ratio"]]

        # Growth & Momentum
        if "pat_cagr_5y" in criteria and "PAT_CAGR_5Y" in df.columns:
            df = df[df["PAT_CAGR_5Y"] >= criteria["pat_cagr_5y"]]
        if "revenue_cagr_5y" in criteria and "Revenue_CAGR_5Y" in df.columns:
            df = df[df["Revenue_CAGR_5Y"] >= criteria["revenue_cagr_5y"]]

        # Dividend
        if "dividend_yield" in criteria and "Dividend_Yield" in df.columns:
            df = df[df["Dividend_Yield"] >= criteria["dividend_yield"]]

        # Debt-Free
        if "borrowings" in criteria and "Borrowings" in df.columns:
            df = df[df["Borrowings"] == criteria["borrowings"]]

        return df

    def run(self, screener_name):
        df = self.fetch_data()
        criteria = self.config.get(screener_name)

        if not criteria:
            print(f"⚠️ Warning: Screener '{screener_name}' not found in config.")
            return pd.DataFrame()  # Return empty dataframe if not found

        return self.apply_filter(df, criteria)


if __name__ == "__main__":
    engine = ScreenerEngine()

    # Let's test a few presets to ensure the engine is fully operational
    test_screeners = ["quality_screener", "value_screener", "growth_screener"]

    for screener in test_screeners:
        result = engine.run(screener)
        print(
            f"✅ Filtered {len(result)} companies for {screener.replace('_', ' ').title()}"
        )
