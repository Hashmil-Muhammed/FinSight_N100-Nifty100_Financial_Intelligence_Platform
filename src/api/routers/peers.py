from fastapi import APIRouter, Depends
import sqlite3
from src.api.database import get_db

# No prefix here so we can define absolute paths inside /api/v1
router = APIRouter(tags=["Peers"])


@router.get("/peers/{group_name}")
def get_peer_group(group_name: str, db: sqlite3.Connection = Depends(get_db)):
    """11.11 All companies in a peer group with percentile ranks."""
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM peer_groups WHERE peer_group = ?", (group_name,))
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        return {"error": f"Database Error: {str(e)}"}


@router.get("/companies/{ticker}/peers/compare")
def compare_company_peers(ticker: str, db: sqlite3.Connection = Depends(get_db)):
    """11.12 Radar data: company vs peer group average."""
    try:
        cursor = db.cursor()
        # Fallback check for company_id vs id
        cursor.execute("PRAGMA table_info(peer_percentiles)")
        cols = [row[1] for row in cursor.fetchall()]
        col_name = "company_id" if "company_id" in cols else "id"

        cursor.execute(
            f"SELECT * FROM peer_percentiles WHERE {col_name} = ?", (ticker,)
        )
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        return {"error": f"Database Error: {str(e)}"}
