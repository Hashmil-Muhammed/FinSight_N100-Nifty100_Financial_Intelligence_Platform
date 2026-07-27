import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")
df = pd.read_sql("SELECT * FROM peer_percentiles", conn)
print("This are the correct column names:")
print(df.columns.tolist())
conn.close()
