import pandas as pd
import yaml
import sqlite3
import os

# Define the paths
DB_PATH = os.path.join("nifty100.db")
CONFIG_PATH = os.path.join("config", "screener_config.yaml")


def load_screener_config(config_file):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config["presets"]


def load_universe_data(db_path):
    conn = sqlite3.connect(db_path)

    # Get all table names from the database
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Available tables in database: {tables}")  # ഇത് ടേബിളുകൾ കാണിച്ചുതരും

    # Try to find a table that has columns related to financial ratios
    # We look for a table that contains 'ratios' in its name
    target_table = next((t for t in tables if "ratios" in t.lower()), None)

    if not target_table:
        print("Error: Could not find any table with 'ratios' in its name.")
        conn.close()
        return None

    query = f"SELECT * FROM {target_table}"
    print(f"--> Loading data from table: {target_table}")
    df = pd.read_sql(query, conn)
    conn.close()

    # Data cleaning
    for col in df.columns:
        if col not in ["company_id", "year"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    latest_year = df["year"].max()
    df = df[df["year"] == latest_year]

    return df


def apply_screener(df, screener_name, conditions):
    print(f"\n--- Running Screener: {screener_name} ---")

    # Create a copy to filter
    filtered_df = df.copy()

    try:
        for metric, condition in conditions.items():
            # Ensure the metric exists in the dataframe columns
            if metric in filtered_df.columns:
                # Build query string
                query_str = f"{metric} {condition}"
                filtered_df = filtered_df.query(query_str)
            else:
                print(f"Skipping metric '{metric}': Not found in database columns.")

        # Get unique company names
        unique_companies = filtered_df["company_id"].dropna().unique().tolist()

        print(
            f"Found {len(unique_companies)} unique companies matching '{screener_name}'."
        )
        if len(unique_companies) > 0:
            print(unique_companies[:10])

    except Exception as e:
        print(f"Error executing screener '{screener_name}': {e}")


def main():
    print("Initializing Preset Screeners Module...")

    presets = load_screener_config(CONFIG_PATH)
    print("Successfully loaded 6 preset configurations from YAML.")

    df = load_universe_data(DB_PATH)

    print(f"Loaded {len(df)} companies (latest year data) from the universe.")
    for preset_name, conditions in presets.items():
        apply_screener(df, preset_name, conditions)


if __name__ == "__main__":
    main()
