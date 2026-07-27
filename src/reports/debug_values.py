import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")
df = pd.read_sql("SELECT * FROM peer_percentiles LIMIT 10", conn)
print("--- DATABASE DATA PREVIEW ---")
print(df.to_string())
print("\n--- COLUMN DATA TYPES ---")
print(df.dtypes)
conn.close()
