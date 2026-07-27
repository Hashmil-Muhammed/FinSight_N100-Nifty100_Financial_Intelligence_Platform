import sqlite3
import pandas as pd
import streamlit as st
import os

# FIX 1: Added 'r' before the string to make it a raw string.
# This prevents \n in \nifty100.db from breaking the path.
# DB_PATH = r"G:\My Drive\WorkSpace\Bluestock_Fintech_Data_Analyst_Intern\Intership at BlueStock\N100 FINANCIAL INTELLIGENCE PLATFORM\nifty100.db"
DB_PATH = "N100 FINANCIAL INTELLIGENCE PLATFORM/nifty100.db"


@st.cache_data
def load_data(query):
    """
    Function to fetch data from SQLite database with caching.
    """
    if not os.path.exists(DB_PATH):
        st.error(f"Database file not found at {DB_PATH}")
        return pd.DataFrame()

    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()


def get_table_names():
    """
    Utility function to list all tables in the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # FIX 2: Changed row(0) to row[0]
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables
