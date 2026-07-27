import sqlite3
import os


def optimize_db():
    """Add indexes to SQLite database to optimize query performance"""
    # Find database path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "nifty100.db")

    if not os.path.exists(db_path):
        db_path = "nifty100.db"  # Fallback

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("⚙️ Optimizing Database: Adding Indexes...")

        # Adding indexes as requested in Day 43 Sprint Document
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_company_id ON companies(id);")
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_ratio_company ON financial_ratios(company_id);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_ratio_year ON financial_ratios(year);"
        )

        conn.commit()
        conn.close()
        print("✅ Database optimization complete! Queries will now run much faster.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    optimize_db()
