import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

# 1. Check if financial_ratios has any data at all
ratios_count = pd.read_sql("SELECT count(*) as count FROM financial_ratios", conn).iloc[
    0
]["count"]
print(f"Total records in financial_ratios: {ratios_count}")

# 2. Check a sample of financial_ratios
sample_ratios = pd.read_sql("SELECT * FROM financial_ratios LIMIT 5", conn)
print("\nSample from financial_ratios:")
print(sample_ratios.head())

# 3. Check if any company_ids match between tables
query = """
SELECT count(*) 
FROM peer_percentiles p
JOIN financial_ratios r ON p.company_id = r.company_id
"""
match_count = pd.read_sql(query, conn).iloc[0]["count"]
print(
    f"\nNumber of matching records between peer_percentiles and financial_ratios: {match_count}"
)

conn.close()
