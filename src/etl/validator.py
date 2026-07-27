import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)


class DataValidator:
    """
    Class to validate DataFrames against Data Quality (DQ) Rules.
    Violations are logged and saved to a CSV file.
    """

    def __init__(self):
        self.failures = []

    def log_failure(self, rule_id, company_id, year, field, issue, severity):
        """Helper method to record a validation failure."""
        self.failures.append(
            {
                "rule_id": rule_id,
                "company_id": company_id,
                "year": year,
                "field": field,
                "issue": issue,
                "severity": severity,
            }
        )

    def validate_all(self, data_dict: dict) -> list:
        """
        Runs important DQ rules on the loaded DataFrames.
        """
        logger.info("Starting Data Quality (DQ) Validation...")

        comp_df = data_dict.get("companies")
        pl_df = data_dict.get("profitandloss")
        bs_df = data_dict.get("balancesheet")

        # DQ-01: Company PK Uniqueness (CRITICAL)
        if comp_df is not None and not comp_df.empty:
            duplicates = comp_df[comp_df.duplicated(subset=["id"], keep=False)]
            for _, row in duplicates.iterrows():
                self.log_failure(
                    "DQ-01",
                    row["id"],
                    None,
                    "id",
                    "Duplicate company ticker found",
                    "CRITICAL",
                )

        # DQ-02: Annual PK Uniqueness (CRITICAL)
        if pl_df is not None and not pl_df.empty:
            if "company_id" in pl_df.columns and "year" in pl_df.columns:
                duplicates = pl_df[
                    pl_df.duplicated(subset=["company_id", "year"], keep=False)
                ]
                for _, row in duplicates.iterrows():
                    self.log_failure(
                        "DQ-02",
                        row["company_id"],
                        row["year"],
                        "PK",
                        "Duplicate P&L record for same year",
                        "CRITICAL",
                    )

        # DQ-04: Balance Sheet Balance - Assets vs Liabilities (WARNING)
        if bs_df is not None and not bs_df.empty:
            for _, row in bs_df.iterrows():
                if pd.notna(row.get("total_assets")) and pd.notna(
                    row.get("total_liabilities")
                ):
                    assets = float(row["total_assets"])
                    liab = float(row["total_liabilities"])
                    diff = abs(assets - liab)
                    # Flag if difference is more than 1%
                    if assets != 0 and (diff / assets) > 0.01:
                        self.log_failure(
                            "DQ-04",
                            row["company_id"],
                            row["year"],
                            "total_assets",
                            "Assets != Liabilities (>1% diff)",
                            "WARNING",
                        )

        # DQ-06: Positive Sales (WARNING)
        if pl_df is not None and not pl_df.empty:
            for _, row in pl_df.iterrows():
                if pd.notna(row.get("sales")):
                    sales = float(row["sales"])
                    if sales <= 0:
                        self.log_failure(
                            "DQ-06",
                            row["company_id"],
                            row["year"],
                            "sales",
                            f"Sales is zero or negative ({sales})",
                            "WARNING",
                        )

        # Ensure reports directory exists
        os.makedirs("reports", exist_ok=True)

        # Save to CSV
        if self.failures:
            failures_df = pd.DataFrame(self.failures)
            output_path = "reports/validation_failures.csv"
            failures_df.to_csv(output_path, index=False)
            logger.warning(
                f"Validation finished with {len(self.failures)} issues. Saved to {output_path}"
            )
        else:
            logger.info("Validation passed perfectly! 0 issues found.")

        return self.failures


if __name__ == "__main__":
    print(
        "Validator logic is ready! Testing will be done during the full pipeline run."
    )
