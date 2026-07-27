from fastapi import APIRouter, Depends
import sqlite3
from src.api.database import get_db

router = APIRouter(prefix="/companies", tags=["Documents"])


@router.get("/{ticker}/documents")
def get_company_documents(ticker: str, db: sqlite3.Connection = Depends(get_db)):
    """11.15 Annual report links for a company."""
    try:
        cursor = db.cursor()
        cursor.execute("PRAGMA table_info(documents)")
        cols = [row[1] for row in cursor.fetchall()]
        col_name = (
            "company_id"
            if "company_id" in cols
            else ("ticker" if "ticker" in cols else "id")
        )

        cursor.execute(f"SELECT * FROM documents WHERE {col_name} = ?", (ticker,))
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        return {"error": f"Database Error: {str(e)}"}
