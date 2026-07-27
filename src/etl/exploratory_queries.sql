-- Query 1: Total number of companies loaded
SELECT COUNT(*) as total_companies FROM companies;

-- Query 2: Companies count per sector
SELECT sector, COUNT(*) as company_count FROM sectors GROUP BY sector ORDER BY company_count DESC;

-- Query 3: Top 5 companies with the highest market capitalization
SELECT company_id, market_cap_cr FROM market_cap ORDER BY market_cap_cr DESC LIMIT 5;

-- Query 4: Total rows across core financial tables (Completeness Check)
SELECT 
    (SELECT COUNT(*) FROM profitandloss) as pnl_rows,
    (SELECT COUNT(*) FROM balancesheet) as bs_rows,
    (SELECT COUNT(*) FROM cashflow) as cf_rows;

-- Query 5: Find the maximum net profit recorded in the P&L table
SELECT company_id, year, net_profit FROM profitandloss ORDER BY net_profit DESC LIMIT 1;

-- Query 6: Check JIOFIN data rows (Our short coverage case from Day 6)
SELECT * FROM profitandloss WHERE company_id = 'JIOFIN';

-- Query 7: Average stock price for a sample company (e.g., RELIANCE or SBIN)
SELECT company_id, AVG(close_price) as avg_closing_price FROM stock_prices GROUP BY company_id LIMIT 5;

-- Query 8: Find top 5 companies with the highest cash from operating activities
SELECT company_id, year, cash_from_operating FROM cashflow ORDER BY cash_from_operating DESC LIMIT 5;

-- Query 9: Verify Foreign Key constraints (Join companies with their sectors)
SELECT c.id, c.company_name, s.sector 
FROM companies c
JOIN sectors s ON c.id = s.company_id 
LIMIT 5;

-- Query 10: Count of validation documents loaded
SELECT COUNT(*) as total_documents FROM documents;