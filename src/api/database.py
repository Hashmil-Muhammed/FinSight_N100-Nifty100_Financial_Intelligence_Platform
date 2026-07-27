import sqlite3
import os
import logging

# Get the absolute path of the root directory (2 levels up from src/api)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Point to the nifty100.db in the root folder
DB_PATH = os.path.join(BASE_DIR, "nifty100.db")

# Fallback to data/nifty100.db just in case
if not os.path.exists(DB_PATH):
    DB_PATH = os.path.join(BASE_DIR, "data", "nifty100.db")


def get_db():
    """
    FastAPI dependency to create and yield a database connection.
    """
    # Prevent SQLite from auto-creating a blank DB if it doesn't exist
    if not os.path.exists(DB_PATH):
        logging.error(f"CRITICAL: Database not found at {DB_PATH}")
        raise Exception(
            f"Database file is missing at {DB_PATH}. Please check the path."
        )

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
