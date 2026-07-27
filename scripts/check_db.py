# import sqlite3
# import pandas as pd
# import os

# db_path = os.path.join("nifty100.db")

# try:
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = cursor.fetchall()

#     if not tables:
#         print("No tables found in the database.")
#     else:
#         print(f"Found {len(tables)} tables in the database:")
#         for table in tables:
#             table_name = table[0]
#             print(f"\n--- Table: {table_name} ---")
#             df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 0", conn)
#             print("Columns:", list(df.columns))
#     conn.close()
# except Exception as e:
#     print(f"Error: {e}")


# import sqlite3
# conn = sqlite3.connect('nifty100.db')
# cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print("Tables in DB:", cursor.fetchall())
# conn.close()


# import sqlite3
# conn = sqlite3.connect('nifty100.db')
# cursor = conn.cursor()
# tables = ['financial_ratios', 'profitandloss', 'balancesheet', 'companies']
# for table in tables:
#     cursor.execute(f"SELECT COUNT(*) FROM {table}")
#     print(f"Table '{table}' has {cursor.fetchone()[0]} rows.")

# conn.close()


import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db_path = os.path.join(BASE_DIR, "nifty100.db")
if not os.path.exists(db_path):
    db_path = os.path.join(BASE_DIR, "data", "nifty100.db")

print(f"🔍 Checking Database at: {db_path}\n")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"📦 TABLES IN DB: {tables}\n")

    for table in ["companies", "financial_ratios"]:
        if table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = [row[1] for row in cursor.fetchall()]
            print(f"📋 COLUMNS IN '{table}':\n {columns}\n")
        else:
            print(f"❌ Table '{table}' NOT FOUND!\n")

    conn.close()
except Exception as e:
    print(f"Error: {e}")
