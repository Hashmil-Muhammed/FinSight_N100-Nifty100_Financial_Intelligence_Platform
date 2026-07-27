import sqlite3
import pandas as pd


class CashFlowEngine:
    def __init__(self, db_path="nifty100.db"):
        self.db_path = db_path

    def fetch_data(self):
        """
        fetch data from Cashflow and P&L table.
        """
        query = """
        SELECT 
            c.company_id,
            c.year,
            c.operating_activity as cfo,
            c.investing_activity as cfi,
            c.financing_activity as cff,
            p.net_profit,
            p.sales
        FROM cashflow c
        JOIN profitandloss p
            ON c.company_id = p.company_id AND c.year = p.year
        """
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn)
        return df

    def get_allocation_pattern(self, cfo, cfi, cff):
        """
        Classifies the company into one of 8 Capital Allocation Patterns based on cash flow signs
        """
        if pd.isna(cfo) or pd.isna(cfi) or pd.isna(cff):
            return "Unknown"

        cfo_sign = "+" if cfo >= 0 else "-"
        cfi_sign = "+" if cfi >= 0 else "-"
        cff_sign = "+" if cff >= 0 else "-"

        pattern = f"{cfo_sign}{cfi_sign}{cff_sign}"

        # 8 Capital Allocation Classes
        classes = {
            "+--": "1. Mature / Cash Cow (Generating cash, investing, paying debt/dividends)",
            "+-+": "2. Growth / Expansion (Generating cash, heavy investing, raising capital)",
            "++-": "3. Restructuring (Generating cash, selling assets, paying debt)",
            "+++": "4. Cash Accumulator (Generating cash, selling assets, raising capital)",
            "---": "5. Liquidity Crisis (Burning cash, investing, paying debt - Unsustainable)",
            "--+": "6. High Burn / Startup (Burning cash, investing, relying on financing)",
            "-+-": "7. Winding Down (Burning cash, liquidating assets to pay debt)",
            "-++": "8. Distressed (Burning cash, liquidating assets, raising capital to survive)",
        }
        return classes.get(pattern, "Unknown")

    def run(self):
        print("Initializing cash flow KPI Engine...\n")
        df = self.fetch_data()

        # Calculate CapEx (Capital Expenditure)
        df["CapEx"] = df["cfi"].apply(
            lambda x: abs(x) if pd.notnull(x) and x < 0 else 0
        )

        # 1. Free Cash Flow (FCF) = CFO - CapEx
        df["FCF"] = df["cfo"] - df["CapEx"]

        # 2. CFO Quality Score = CFO / Net Profit
        df["CFO_Quality_Score"] = df.apply(
            lambda row: (
                round(row["cfo"] / row["net_profit"], 2)
                if pd.notnull(row["net_profit"]) and row["net_profit"] > 0
                else None
            ),
            axis=1,
        )

        # 3. CapEx Intensity = CapEx / Sales
        df["CapEx_Intensity"] = df.apply(
            lambda row: (
                round((row["CapEx"] / row["sales"]) * 100, 2)
                if pd.notnull(row["sales"]) and row["sales"] > 0
                else None
            ),
            axis=1,
        )

        # 4. FCF Conversion Ratio = FCF / Net Profit
        df["FCF_Conversion"] = df.apply(
            lambda row: (
                round((row["FCF"] / row["net_profit"]) * 100, 2)
                if pd.notnull(row["net_profit"]) and row["net_profit"] > 0
                else None
            ),
            axis=1,
        )

        # 5. Capital Allocation Pattern (8 Classes)
        df["Capital_Allocation_Pattern"] = df.apply(
            lambda row: self.get_allocation_pattern(row["cfo"], row["cfi"], row["cff"]),
            axis=1,
        )

        print(f"✅ Successfully Computed Cash flow KPIs for {len(df)} records. \n")
        return df


if __name__ == "__main__":
    engine = CashFlowEngine()
    result_df = engine.run()

    print("📊 Sample Calculated Cash flow KPIs:")
    cols_to_show = [
        "company_id",
        "year",
        "FCF",
        "CFO_Quality_Score",
        "CapEx_Intensity",
        "Capital_Allocation_Pattern",
    ]
    print(result_df[cols_to_show].head(10).to_string(index=False))

    print("\n📈 Capital Allocation Pattern Distribution:")
    print(result_df["Capital_Allocation_Pattern"].value_counts().to_string())
