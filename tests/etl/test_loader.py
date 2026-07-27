import sqlite3
import os
import pytest


@pytest.fixture
def db_cursor():
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    db_path = os.path.join(BASE_DIR, "nifty100.db")
    if not os.path.exists(db_path):
        db_path = os.path.join(BASE_DIR, "data", "nifty100.db")
    conn = sqlite3.connect(db_path)
    yield conn.cursor()
    conn.close()


def test_companies_row_count(db_cursor):
    """Test if exactly 92 companies are loaded"""
    db_cursor.execute("SELECT COUNT(*) FROM companies")
    assert db_cursor.fetchone()[0] == 92


@pytest.mark.parametrize(
    "table_name",
    ["companies", "profitandloss", "balancesheet", "cashflow", "financial_ratios"],
)
def test_essential_tables_exist(db_cursor, table_name):
    """Test if all 5 essential tables are created in the database"""
    db_cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
    )
    assert db_cursor.fetchone() is not None


@pytest.mark.parametrize(
    "expected_col", ["company_name", "face_value", "roce_percentage", "roe_percentage"]
)
def test_companies_columns(db_cursor, expected_col):
    """Test if critical columns exist in companies table"""
    db_cursor.execute("PRAGMA table_info(companies)")
    cols = [row[1] for row in db_cursor.fetchall()]
    assert expected_col in cols
