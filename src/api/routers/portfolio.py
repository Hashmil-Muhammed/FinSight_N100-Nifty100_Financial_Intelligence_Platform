from fastapi import APIRouter, Depends
import sqlite3
from src.api.database import get_db

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/stats")
def get_portfolio_stats(db: sqlite3.Connection = Depends(get_db)):
    """11.14 Portfolio-level statistics for core KPIs."""
    try:
        cursor = db.cursor()
        # Fetching basic stats as dynamic fallback
        query = """
            SELECT 
                AVG(ROE) as avg_roe, MAX(ROE) as max_roe, MIN(ROE) as min_roe,
                AVG(D_E) as avg_de, MAX(D_E) as max_de, MIN(D_E) as min_de
            FROM financial_ratios 
            WHERE year = (SELECT MAX(year) FROM financial_ratios)
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return dict(result) if result else {"message": "No stats available"}
    except Exception as e:
        return {"error": f"Database Error: {str(e)}"}
