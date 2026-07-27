from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
import sqlite3
import os
from src.api.database import get_db

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("")
def list_companies(db: sqlite3.Connection = Depends(get_db)):
    """11.1 List all 92 companies"""
    try:
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, company_name, roe_percentage, roce_percentage FROM companies"
        )
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ticker}")
def get_company_profile(ticker: str, db: sqlite3.Connection = Depends(get_db)):
    """11.2 Full company profile"""
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM companies WHERE id = ?", (ticker,))
        company = cursor.fetchone()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")

        cursor.execute(
            "SELECT * FROM financial_ratios WHERE company_id = ? ORDER BY year DESC LIMIT 1",
            (ticker,),
        )
        latest_ratios = cursor.fetchone()

        return {
            "profile": dict(company),
            "latest_kpis": dict(latest_ratios) if latest_ratios else None,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ticker}/pl")
def get_profit_and_loss(
    ticker: str,
    from_year: Optional[str] = None,
    to_year: Optional[str] = None,
    db: sqlite3.Connection = Depends(get_db),
):
    """11.3 P&L history"""
    cursor = db.cursor()
    query = "SELECT * FROM profitandloss WHERE company_id = ?"
    params = [ticker]
    if from_year:
        query += " AND year >= ?"
        params.append(from_year)
    if to_year:
        query += " AND year <= ?"
        params.append(to_year)
    cursor.execute(query + " ORDER BY year ASC", params)
    return [dict(row) for row in cursor.fetchall()]


@router.get("/{ticker}/bs")
def get_balance_sheet(
    ticker: str,
    from_year: Optional[str] = None,
    to_year: Optional[str] = None,
    db: sqlite3.Connection = Depends(get_db),
):
    """11.4 Balance sheet history"""
    cursor = db.cursor()
    query = "SELECT * FROM balancesheet WHERE company_id = ?"
    params = [ticker]
    if from_year:
        query += " AND year >= ?"
        params.append(from_year)
    if to_year:
        query += " AND year <= ?"
        params.append(to_year)
    cursor.execute(query + " ORDER BY year ASC", params)
    return [dict(row) for row in cursor.fetchall()]


@router.get("/{ticker}/cashflow")
def get_cashflow(
    ticker: str,
    from_year: Optional[str] = None,
    to_year: Optional[str] = None,
    db: sqlite3.Connection = Depends(get_db),
):
    """11.5 Cash flow history"""
    cursor = db.cursor()
    query = "SELECT * FROM cashflow WHERE company_id = ?"
    params = [ticker]
    if from_year:
        query += " AND year >= ?"
        params.append(from_year)
    if to_year:
        query += " AND year <= ?"
        params.append(to_year)
    cursor.execute(query + " ORDER BY year ASC", params)
    return [dict(row) for row in cursor.fetchall()]


@router.get("/{ticker}/ratios")
def get_ratios(ticker: str, db: sqlite3.Connection = Depends(get_db)):
    """11.6 All pre-computed KPIs"""
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM financial_ratios WHERE company_id = ? ORDER BY year ASC",
        (ticker,),
    )
    return [dict(row) for row in cursor.fetchall()]


@router.get("/{ticker}/tearsheet")
def get_tearsheet(ticker: str):
    """11.7 Returns pre-generated tearsheet PDF (binary download)."""
    # Dynamic Project Root Finder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = None
    while current_dir != os.path.dirname(current_dir):
        if "nifty100.db" in os.listdir(current_dir):
            project_root = current_dir
            break
        current_dir = os.path.dirname(current_dir)

    if not project_root:
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )

    file_path = os.path.join(
        project_root, "reports", "tearsheets", f"{ticker}_tearsheet.pdf"
    )

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"PDF file {ticker}_tearsheet.pdf not found inside reports/tearsheets/",
        )

    return FileResponse(
        path=file_path,
        filename=f"{ticker}_Financial_Tearsheet.pdf",
        media_type="application/pdf",
    )
