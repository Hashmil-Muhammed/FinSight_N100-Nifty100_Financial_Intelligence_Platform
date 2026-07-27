from fastapi import APIRouter, Depends, Query
from typing import Optional
import sqlite3
from src.api.database import get_db

router = APIRouter(prefix="/screener", tags=["Screener"])


@router.get("")
def screen_companies(
    min_roe: Optional[float] = Query(None, description="Minimum ROE percentage"),
    max_de: Optional[float] = Query(None, description="Maximum Debt to Equity ratio"),
    min_cagr: Optional[float] = Query(None, description="Minimum 3Y Revenue CAGR"),
    db: sqlite3.Connection = Depends(get_db),
):
    """
    11.8 Screener Endpoint: Filters companies based on financial criteria.
    (Sector filter disabled dynamically based on available DB schema)
    """
    try:
        # Use exact column names from your database scan
        query = """
            SELECT c.id as company_id, c.company_name, 
                   r.ROE, r.D_E, r.Revenue_CAGR_3Y
            FROM companies c
            JOIN financial_ratios r ON c.id = r.company_id
            WHERE r.year = (SELECT MAX(year) FROM financial_ratios)
        """
        params = []

        if min_roe is not None:
            query += " AND r.ROE >= ?"
            params.append(min_roe)
        if max_de is not None:
            query += " AND r.D_E <= ?"
            params.append(max_de)
        if min_cagr is not None:
            query += " AND r.Revenue_CAGR_3Y >= ?"
            params.append(min_cagr)

        # Sort by ROE as primary metric since composite_score is not present
        query += " ORDER BY r.ROE DESC"

        cursor = db.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    except Exception as e:
        return {"error": f"Database Error: {str(e)}"}
