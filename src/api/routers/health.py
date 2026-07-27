from fastapi import APIRouter, Depends
import sqlite3
import time
from src.api.database import get_db

router = APIRouter(tags=["Health"])

# Record the exact time the server started
START_TIME = time.time()

# List of expected tables in the database
EXPECTED_TABLES = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "sectors",
    "stock_prices",
    "market_cap",
    "peer_groups",
    "analysis",
]


@router.get("/health")
def health_check(db: sqlite3.Connection = Depends(get_db)):
    """
    11.16 Server health check. Returns DB row counts and server uptime.
    """
    uptime_seconds = round(time.time() - START_TIME, 2)
    db_row_counts = {}

    cursor = db.cursor()
    for table in EXPECTED_TABLES:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            db_row_counts[table] = cursor.fetchone()[0]
        except sqlite3.OperationalError:
            # Table might not exist yet
            db_row_counts[table] = "Table Not Found"

    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime_seconds": uptime_seconds,
        "db_row_counts": db_row_counts,
    }
