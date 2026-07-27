from fastapi import APIRouter, Depends
import sqlite3
from src.api.database import get_db

router = APIRouter(prefix="/sectors", tags=["Sectors"])


@router.get("")
def get_all_sectors(db: sqlite3.Connection = Depends(get_db)):
    """
    11.9 List all sectors.
    Note: Sector column is missing in the DB, returning placeholder message.
    """
    return {"message": "Sector data is not available in the current database schema."}


@router.get("/{sector}/companies")
def get_sector_companies(sector: str, db: sqlite3.Connection = Depends(get_db)):
    """
    11.10 All companies in a sector.
    """
    return {"message": f"Sector filtering for '{sector}' is disabled due to DB schema."}
