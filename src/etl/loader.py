import sys
from pathlib import Path

# Fix for ModuleNotFoundError: Adding project root to Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

import pandas as pd
import sqlite3
import logging
import os
from src.etl.normaliser import normalize_ticker, normalize_year
from src.etl.validator import DataValidator

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DB_PATH = "nifty100.db"

# Mapping raw file names to our SQL table names
FILE_TO_TABLE_MAP = {
    "companies.xlsx": "companies",
    "profitandloss.xlsx": "profitandloss",
    "balancesheet.xlsx": "balancesheet",
    "cashflow.xlsx": "cashflow",
    "prosandcons.xlsx": "prosandcons",
    "analysis.xlsx": "analysis",
    "documents.xlsx": "documents",
    "financial_ratios.xlsx": "financial_ratios",
    "market_cap.xlsx": "market_cap",
    "peer_groups.xlsx": "peer_groups",
    "sectors.xlsx": "sectors",
    "stock_prices.xlsx": "stock_prices",
}


def load_excel_file(file_path: str, is_core: bool = True) -> pd.DataFrame:
    """
    Reads an Excel file into a pandas DataFrame and applies normalization.
    """

    try:
        header_row = 1 if is_core else 0
        df = pd.read_excel(file_path, header=header_row)

        if "company_id" in df.columns:
            df["company_id"] = df["company_id"].apply(normalize_ticker)
        elif "id" in df.columns and "companies" in str(file_path).lower():
            df["id"] = df["id"].apply(normalize_ticker)

        if "year" in df.columns:
            df["year"] = df["year"].apply(normalize_year)
        elif "Year" in df.columns:
            df["Year"] = df["Year"].apply(normalize_year)

        return df
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return pd.DataFrame()


def setup_database():
    """Executes the schema.sql file to create tables."""
    schema_path = Path("src/etl/schema.sql")
    if not schema_path.exists():
        logger.error(f"Schema file not found at {schema_path}")
        return False

    try:
        with sqlite3.connect(DB_PATH) as conn:
            with open(schema_path, "r") as f:
                schema_script = f.read()
            conn.executescript(schema_script)
            logger.info("Database Schema initialized successfully.")
        return True
    except Exception as e:
        logger.error(f"failed to initialized schema: {e}")
        return False


def load_all_data():
    """Loads all Excel files, validates them, and inserts into the SQLite DB."""
    if not setup_database():
        return

    raw_dir = Path("data/raw")
    supp_dir = Path("data/supporting")

    all_files = list(raw_dir.glob("*xlsx")) + list(supp_dir.glob("*.xlsx"))
    if not all_files:
        logger.error("No Excel files found in data/raw or data/supporting.")
        return

    data_dict = {}
    audit_records = []

    # 1. Read and Normalize Data
    for file_path in all_files:
        file_name = file_path.name
        table_name = FILE_TO_TABLE_MAP.get(file_name)
        if not table_name:
            continue

        is_core = "raw" in str(file_path.parent)
        logger.info(f"Processing {file_name} for table '{table_name}'...")
        df = load_excel_file(str(file_path), is_core=is_core)

        if not df.empty:
            data_dict[table_name] = df

    # 2. Run Data Quality Validation
    validator = DataValidator()
    validator.validate_all(data_dict)

    # 3. Load into Database
    # We must load 'companies' first to avoid Foreign Key errors
    table_load_order = ["companies"] + [t for t in data_dict.keys() if t != "companies"]

    with sqlite3.connect(DB_PATH) as conn:
        for table_name in table_load_order:
            if table_name not in data_dict:
                continue
            df = data_dict[table_name]
            try:
                df.to_sql(table_name, conn, if_exists="append", index=False)
                row_count = len(df)
                logger.info(f"Loaded {row_count} rows into '{table_name}'.")

                audit_records.append(
                    {
                        "table_name": table_name,
                        "rows_loaded": row_count,
                        "status": "SUCCESS",
                    }
                )
            except Exception as e:
                logger.error(f"Failed to load table {table_name}: {e}")
                audit_records.append(
                    {
                        "table_name": table_name,
                        "row_loaded": 0,
                        "status": f"FAILED: {str(e)}",
                    }
                )

    # 4. Save Load Audit CSV
    os.makedirs("reports", exist_ok=True)
    audit_df = pd.DataFrame(audit_records)
    audit_df.to_csv("reports/load_audit.csv", index=False)
    logger.warning(
        "Full data load completed. check 'reports/load_audit.csv' for details"
    )


if __name__ == "__main__":
    print("Initiating Full Data Load pipeline..")
    load_all_data()
