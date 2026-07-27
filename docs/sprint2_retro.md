# 🔄 Sprint 2 Retrospective: Analytics Engine

**Date:** June 2026
**Lead Analyst:** Hashmil Muhammed
**Status:** Completed successfully

## 🎯 Sprint Goals Achieved
1. **Profitability KPIs:** Successfully programmed Net Profit Margin, Operating Profit Margin, ROE, and ROCE across 1200+ historical records.
2. **Leverage & Efficiency KPIs:** Computed Debt-to-Equity, ICR, and Asset Turnover with specialized banking carve-outs.
3. **Growth Metrics (CAGR):** Built sliding window (3Y, 5Y, 10Y) CAGR engine solving negative-base math constraints using a custom `Turnaround` flag.
4. **Cash Flow Analytics:** Engineered FCF, CFO Quality Score, CapEx Intensity, and a proprietary 8-class Capital Allocation Pattern algorithm.
5. **Database Ingestion:** Seamlessly merged outputs from all 3 sub-engines and successfully populated `financial_ratios` table in SQLite (`nifty100.db`).
6. **Testing:** Achieved 100% pass rate across 20 specialized edge-case unit tests.

## 🚧 Challenges & Solutions
- **Challenge:** Banking sector formulas (D/E, ROCE) clashed with standard industrial definitions, throwing our averages off.
- **Solution:** Integrated string-matching logic (`company_id` containing 'bank'/'fin') to bypass/flag these specific rows cleanly.
- **Challenge:** Initial database column misalignments (e.g., `operating_activities` vs `operating_cash_flow`).
- **Solution:** Utilized `PRAGMA table_info()` dynamic checking to adapt fetch queries to actual schema states.

## 🚀 Plan for Sprint 3 (Screener Module)
With all core ratios and KPIs populated in our database, Sprint 3 will focus on building the **Query & Screener Engine**. We will write complex filtering logics to extract "High Growth", "Undervalued", and "Cash Rich" companies based on the newly calculated data.