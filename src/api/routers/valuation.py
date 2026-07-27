from fastapi import APIRouter, Depends
import sqlite3
from src.api.database import get_db

router = APIRouter(prefix="/market-cap", tags=["Market Cap"])


@router.get("/{ticker}")
def get_historical_market_cap(ticker: str, db: sqlite3.Connection = Depends(get_db)):
    """11.13 Historical valuation multiples (P/E, P/B, EV/EBITDA)."""
    try:
        cursor = db.cursor()
        cursor.execute("PRAGMA table_info(market_cap)")
        cols = [row[1] for row in cursor.fetchall()]
        col_name = (
            "company_id"
            if "company_id" in cols
            else ("ticker" if "ticker" in cols else "id")
        )

        cursor.execute(
            f"SELECT * FROM market_cap WHERE {col_name} = ? ORDER BY year ASC",
            (ticker,),
        )
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        return {"error": f"Database Error: {str(e)}"}
