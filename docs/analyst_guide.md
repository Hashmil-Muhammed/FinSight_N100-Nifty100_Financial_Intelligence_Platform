# 📈 N100 Financial Intelligence Platform - Analyst Guide
**Version:** 1.0 | **Audience:** Equity Research Analysts

## 1. Introduction
This guide provides complete instructions on how to leverage the Nifty 100 Platform for stock screening, peer comparison, and financial deep-dives.

## 2. Using the Streamlit Dashboard
The dashboard is accessed via `http://localhost:8501`.
* **Market Overview Tab:** View all 92 tracked companies.
* **Company Analysis Tab:** Enter a ticker (e.g., `TCS`) to view historic P&L, balance sheets, and key ratios.
* **Stock Screener Tab:** Use the left sidebar to set filters like `Min ROE > 15%` or `Debt/Equity < 0.5`. The engine will rank the best matching companies.

## 3. PDF Tearsheet Generation
To generate a one-page summary for client meetings:
1. Navigate to the Company Analysis tab.
2. Search for your target company.
3. Click the **"Download Tearsheet (PDF)"** button. 
4. The system directly queries the `/api/v1/companies/{ticker}/tearsheet` endpoint and downloads a formatted PDF.

## 4. REST API Direct Access
For quantitative analysts who prefer raw data:
* **Base URL:** `http://127.0.0.1:8000/api/v1`
* **Get All Ratios:** `GET /companies/{ticker}/ratios`
* **Custom Screener:** `GET /screener?min_roe=20&min_cagr=10`
Full OpenAPI documentation is available at `/docs` for testing via Postman or cURL.

## 5. Troubleshooting
* **Error: "Connection Refused" on Dashboard:** Ensure the FastAPI server is running on Port 8000.
* **Missing Data / [] Array:** The company might not have reported those specific metrics for the selected year.
* **Database Locked Error:** Stop the server, wait 5 seconds, and restart.