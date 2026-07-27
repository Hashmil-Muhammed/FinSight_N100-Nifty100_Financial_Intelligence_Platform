# 🧪 Dashboard Integration & QA Test Log
**Date:** 2026-07-09  
**Tester:** Hashmil Muhammed  
**Objective:** End-to-end usability testing of all 8 screens using 10 random NIFTY 100 tickers.

## 🎯 Selected Test Tickers (10 Random Companies)
1. RELIANCE (Reliance Industries Ltd)
2. TCS (Tata Consultancy Services Ltd)
3. HDFCBANK (HDFC Bank Ltd)
4. INFY (Infosys Ltd)
5. ICICIBANK (ICICI Bank Ltd)
6. ITC (ITC Ltd)
7. SBIN (State Bank of India)
8. BHARTIARTL (Bharti Airtel Ltd)
9. SIEMENS (Siemens Ltd)
10. ABB (Abbott India Ltd)

---

## 🛠️ Usability Testing Results (Task 1)

| Page / Screen | Test Action | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **01_Company_Profile** | Select each of the 10 tickers. | Displays company info, sector, and basic details without crashing. | Information displayed correctly. | ✅ Pass |
| **02_Price_Trends** | Filter by dates and check moving averages for all 10. | Line charts render correctly without overlapping. | Charts render smoothly. | ✅ Pass |
| **03_Returns_Analysis** | Verify daily/monthly return distributions. | Histograms and box plots update per ticker. | Distributions update dynamically. | ✅ Pass |
| **04_Financial_Ratios** | Check KPIs (P/E, ROE, Debt/Equity). | Dynamic formatting handles extreme values correctly. | Correctly handled (e.g., missing values show 0 or N/A). | ✅ Pass |
| **05_Peer_Comparison** | Compare Reliance, TCS, HDFC against peers. | Radar charts and bar charts show comparative data. | Peer groups align correctly. | ✅ Pass |
| **06_Sector_Analysis** | Filter by sector for the 10 tickers. | Bubble chart and median KPIs update based on sector. | Sector charts render correctly. | ✅ Pass |
| **07_Capital_Allocation**| Check Treemap visualizations. | Treemap shows correct proportional boxes per pattern. | Treemap renders without error. | ✅ Pass |
| **08_Annual_Reports** | Click BSE PDF links for 10 companies. | Opens correct BSE PDF; missing ones show 'Caution' badge. | Links redirect correctly; badges show status. | ✅ Pass |
| **09_Valuation** | Check EV/EBITDA, FCF Ranker, and P/E Trend. | Displays Bar/Line charts dynamically based on year count. | Ranks and Valuation flags display accurately. | ✅ Pass |

## 📝 General Observations
* The app handles navigation smoothly.
* Streamlit caching avoids redundant DB hits.
* No `OperationalError` or `KeyError` encountered during the random ticker testing.