# 🔄 Sprint 1 Retrospective: Data Foundation & ETL Pipeline

**Date:** June 2026
**Lead Analyst:** Hashmil Muhammed
**Status:** Completed successfully

## 🎯 Sprint Goals Achieved
1. **Workspace Setup:** Established a professional directory structure and virtual environment with all core dependencies.
2. **Data Ingestion (ETL):** Engineered `loader.py` using Pandas to programmatically read and extract 12 distinct Excel datasets into dataframes.
3. **Data Cleansing:** Developed robust normalizer logic (`normaliser.py`) to handle ticker inconsistencies, whitespace trimming, and standardization of financial years.
4. **Data Quality Engine:** Built `validator.py` implementing 16 strict DQ rules, including PK/FK uniqueness and verifying Balance Sheet tally (`Total Assets = Total Liabilities`).
5. **Schema Architecture:** Designed a highly normalized Star Schema (`schema.sql`) for SQLite.
6. **Database Loading:** Successfully populated the `nifty100.db` database with cleaned records and generated a comprehensive load audit report.

## 🚧 Challenges & Solutions
- **Challenge:** Inconsistent column naming across different Excel files (e.g., `FY23` vs `2023-03`).
- **Solution:** Implemented regex-based year parsing logic in the normalizer to standardize all date columns into an integer format (`YYYY`).
- **Challenge:** Missing values in critical financial columns causing SQLite ingestion to fail due to NOT NULL constraints.
- **Solution:** Engineered a targeted fallback mechanism replacing missing numerical values with `0.0` or generating `Data Quality Flags` for manual review.

## 🚀 Plan for Sprint 2 (Analytics Engine)
With a robust and cleansed database in place, Sprint 2 will focus on programming the core **Financial Analytics Engine**. We will compute over 50 KPIs, including Profitability margins, Leverage metrics, and a dynamic CAGR calculator with Turnaround flag resilience.