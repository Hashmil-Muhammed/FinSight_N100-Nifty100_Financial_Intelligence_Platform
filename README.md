<div align="center">

<img src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png" alt="FinSight Logo" width="80" height="80" />

# FinSight N100 | Nifty 100 Financial Intelligence Platform
### Enterprise-Grade Financial Analytics, REST API & Business Intelligence Solution


![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Analytics-purple?style=for-the-badge&logo=pandas&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-137_Tests_Passed-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Live_Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-KMeans_Clustering-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge&logo=github-actions&logoColor=white)
![API Docs](https://img.shields.io/badge/API_Docs-Swagger_UI-009688?style=for-the-badge&logo=swagger&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Portfolio-black?style=for-the-badge&logo=github&logoColor=white)




###  **Live Web Application:** [https://finsight-n100.streamlit.app/](https://finsight-n100.streamlit.app/)

<br>

</div>

<img width="1536" height="1024" alt="ChatGPT Image Jul 24, 2026, 04_57_34 PM" src="https://github.com/user-attachments/assets/67ec2e95-0202-474e-81ba-f69ce7959ff8" />

---

## 📊 Project Metrics Cards

<div align="center">

| 🏢 Companies Tracked | 📅 Historical Data | 📈 KPIs Computed | 🧪 Automated Tests | ⚡ API Latency |
| :---: | :---: | :---: | :---: | :---: |
| **92 NSE Nifty 100** | **10 Years (11k+ points)** | **50+ Ratios & Scores** | **137/137 Passed** | **< 0.5 Seconds** |

</div>

---

## 📋 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [✨ Project Highlights](#-project-highlights)
- [🚀 Key Features](#-key-features)
- [⚙️ Tech Stack](#️-tech-stack)
- [🏗 System Architecture & Workflow](#-system-architecture--workflow)
- [🌐 Live Deployment & Running Locally](#-live-deployment--running-locally)
- [📅 Sprint 1 Progress Tracker (Data Foundation)](#-sprint-1-progress-tracker-data-foundation)
- [📅 Sprint 2 Progress Tracker (Analytics Engine)](#-sprint-2-progress-tracker-analytics-engine)
- [📅 Sprint 3 Progress Tracker (Screener & Ranking Engine)](#-sprint-3-progress-tracker-screener--ranking-engine)
- [📅 Sprint 4 Progress Tracker (Dashboard & Valuation)](#-sprint-4-progress-tracker-dashboard--valuation)
- [📅 Sprint 5 Progress Tracker (NLP & Cash Flow Intelligence)](#-sprint-5-progress-tracker-nlp--cash-flow-intelligence)
- [📅 Sprint 6 Progress Tracker (API, Testing & Delivery)](#-sprint-6-progress-tracker-api-testing--delivery)
- [📂 Repository Structure](#-repository-structure)
- [🛠️ Execution & Setup Guide (Dev Mode)](#️-execution--setup-guide-dev-mode)
- [🗺️ Future Roadmap](#️-future-roadmap)
- [❓ Frequently Asked Questions (FAQ)](#-frequently-asked-questions-faq)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [🙏 Acknowledgements](#-acknowledgements)
- [👨‍💻 Author Details](#-author-details)

---


## 🎯 Project Overview & Abstract

This repository contains the complete 45-day Project for the **Bluestock Fintech Data Analytics Internship**. 

The **Nifty 100 Financial Intelligence Platform** is an enterprise-grade, fully automated financial data engineering and business intelligence solution designed for equity research analysts and portfolio managers. The platform ingests, cleanses, cleans, and analyzes **10 years of historical financial data (~11,000+ data points)** across 92 NSE Nifty 100 index constituent companies, spanning 12 source datasets (7 core financial statements and 5 supplementary datasets).

### 💡 Core Engineering & Analytical Capabilities:
1. **Automated ETL & Data Foundation:** Standardized star-schema SQLite database (`nifty100.db`) built with strict primary/foreign key constraints and 16 Data Quality (DQ) verification rules.
2. **Advanced Analytics & KPI Engine:** Pre-computes 50+ Key Performance Indicators including profitability margins (NPM, OPM, ROE, ROCE with banking adjustments), leverage metrics (D/E, ICR), 3Y/5Y/10Y CAGRs with turnaround flags, and CFO Quality Scores.
3. **Smart Screener & Peer Benchmarking:** Multi-criteria YAML-configurable stock screening, sector-relative composite ranking engine (Profitability, Growth, Valuation), and automated 56 Plotly radar chart peer group comparisons.
4. **Machine Learning & NLP Intelligence:** Unsupervised K-Means clustering ($k=5$) for automated peer grouping, NLP keyword description tagging, dynamic qualitative Pros/Cons generation, and NLTK VADER sentiment analysis.
5. **High-Performance REST API:** Built with **FastAPI** featuring 16 modular endpoints, query caching, and index-optimized database handling capable of serving concurrent requests in `<0.5s`.
6. **Interactive 9-Screen Dashboard & Automated Reports:** Multi-page **Streamlit** frontend interface paired with **ReportLab** dynamic PDF generation for 1-page company executive tearsheets and sector intelligence reports.
7. **CI/CD Quality Assurance:** Fully audited using a 137-case **Pytest** testing suite (100% green pass rate) and validated through 20 project acceptance gates.

**Project Duration :** 45 Days | 6 Sprints | 12 Modules | 120+ Technical Features  
**Status :** `Completed - Production Ready v1.0` <br>
**Live URL :** [https://finsight-n100.streamlit.app/](https://finsight-n100.streamlit.app/)

---

## ✨ Project Highlights

* **Banking & Non-Financial Carve-outs:** Intelligent sector-specific adjustments (e.g., bypassing standard ROCE logic for Banks where borrowing constitutes core inventory).
* **Negative-Base CAGR Resilience:** Advanced mathematical fallback logic eliminating complex logarithmic errors during turnaround financial years.
* **100% Unit Test Pass Rate:** Verified by Pytest across 137 individual edge-case scenarios spanning ETL, KPIs, and API Routers.
* **Load Test Performance:** SQLite indexing strategies optimized to execute 10 concurrent heavy multi-filter screener requests in `< 0.38` seconds.
* **Production-Grade Architecture:** Designed with modularity separating API microservices, ML clustering, Streamlit client UI, and ReportLab PDF renderers.

---

## 🚀 Key Features

* **ETL Pipeline & Data Foundation:** Automated extraction, cleansing, and normalization of 10+ years of P&L, Balance Sheet, and Cash Flow data across 92 companies with 16 Data Quality (DQ) validation rules.
* **Advanced Financial Analytics:** Pre-computed 50+ financial ratios, 3Y/5Y/10Y CAGR metrics with turnaround flags, banking ROCE adjustments, and CFO Quality Scores.
* **Machine Learning & NLP Intelligence:** Unsupervised K-Means clustering ($k=5$) for business profiling, automated NLP keyword tagger, rule-based Pros/Cons generator, and NLTK VADER sentiment analysis.
* **Smart Screener & Peer Benchmarking:** Multi-criteria YAML-driven stock screening, composite ranking engine, and 56 dynamic Plotly radar chart peer group comparisons.
* **High-Performance REST API:** 16 highly optimized FastAPI endpoints with query caching and SQLite indexing, serving concurrent requests in <0.5 seconds.
* **Interactive Dashboard:** 9-screen Streamlit front-end for market overview, custom screening, trend sparklines, and company profiling.
* **Automated PDF Tearsheets:** Executive financial summaries, sector reports, and portfolio intelligence PDFs generated dynamically via ReportLab.

---

## ⚙️ Tech Stack

* **Backend & API:** Python 3.10, FastAPI, Uvicorn, HTTPX
* **Database:** SQLite3 (Indexed for high-speed concurrent queries)
* **Frontend:** Streamlit, Plotly, Matplotlib
* **Data Engineering & ML:** Pandas, NumPy, Scikit-Learn (K-Means), SciPy
* **NLP & Text Analytics:** NLTK (VADER Sentiment Scorer), Regex
* **Reporting & Export:** ReportLab (PDF Engine), OpenPyXL (Excel), Kaleido
* **Testing & QA:** Pytest, Pytest-HTML (137 Unit/Integration Tests)
* **Code Quality & CI:** Black, Ruff

---

## 🏗 System Architecture & Workflow

```text
  [ Raw Data Sources ] ---> [ ETL Pipeline & Normalizer ] ---> [ Data Quality Engine (16 DQ Rules) ]
 (12 Excel Datasets)            (src/etl/loader.py)                   (src/etl/validator.py)
                                                                                  │
                                                                                  ▼
  [ Streamlit Front-End ] <--- [ REST API Server ] <--- [ Star Schema SQLite ] <──┘
  (9 Interactive Pages)      (FastAPI - 16 Endpoints)      (nifty100.db)
            │                         │                           │
            ▼                         ▼                           ▼
  [ Executive PDF Tearsheets ] [ Load Test Automation ] [ K-Means ML & NLP Sentiment ]

```
---

## 🌐 Live Deployment & Running Locally

### 🔗 Access Live App
The interactive 9-page Streamlit Dashboard is publicly hosted and available at:
👉 https://finsight-n100.streamlit.app/

### 💻 Running the Platform Locally
This project features a fully interactive 9-screen multi-page Streamlit application powered by a FastAPI backend. You need two terminal windows to run the platform locally.

### **1. Install Dependencies & Setup Environment**

Ensure you have Python installed. Activate your virtual environment and install the required libraries:

```bash
python -m venv .venv
.\activate_env.bat  # On Windows
pip install -r requirements.txt
python src/etl/loader.py  # Initialize DB
```

### **2. Terminal 1: Start the Backend API Server**

```bash
uvicorn src.api.main:app --port 8000 --reload
```

**API Docs available at:** <http://127.0.0.1:8000/docs>

### **3. Terminal 2: Start the Frontend Dashboard**

Navigate to the root directory and execute:

```bash
streamlit run src/dashboard/app.py
```

**Dashboard available at:** <http://localhost:8501>

---

## 📅 Sprint 1 Progress Tracker (Data Foundation)

### 🔹 Day 01: Environment & Project Foundation
- **Directory Structure:** Established a professional workspace layout (`src/`, `tests/`, `data/`, `reports/`).
- **Virtual Environment:** Set up a clean Python virtual environment (`.venv`) to isolate dependencies.
- **Dependency Management:** Configured `requirements.txt` with core data science and analytical libraries.
- **Environment Variables:** Set up `.env` for managing sensitive configurations like database paths and ports.
- **Automation:** Created a custom `Makefile` and a Windows batch script (`activate_env.bat`).

### 🔹 Day 02: Data Loader & Normalizer Engine
- **Normalizer Logic (`src/etl/normaliser.py`):** Developed robust data cleansing functions for tickers and financial years.
- **Data Loading Pipeline (`src/etl/loader.py`):** Programmed an automated pipeline using `pandas` to read Excel files.
- **Unit Test Suite (`tests/etl/test_normalise.py`):** Authored 23 rigorous unit tests evaluating edge cases.

### 🔹 Day 03: Schema Validator (16 DQ Rules)
- **Data Quality Engine (`src/etl/validator.py`):** Developed a robust data validation class.
- **Rule Implementation:** Coded checks including PK/FK uniqueness and Balance Sheet tally verification.

### 🔹 Day 04: Database Schema Engineering
- **Schema Design (`src/etl/schema.sql`):** Architected the foundational SQLite Star Schema layout.
- **Table Creation:** Written strict DDL statements for 12 tables.

### 🚀 Day 05: Database Loader Pipeline
- **Objective:** Ingest all 12 validated Excel datasets into a centralized SQLite database.
- **Actions:** Loaded data into all tables and generated a load audit report (`reports/load_audit.csv`).

### 🧐 Day 06: Data Quality Manual Review
- **Objective:** Perform manual checks on the loaded SQLite database.
- **Actions:** Queried random companies and checked for minimum year coverage (e.g., `JIOFIN`).

### 🏁 Day 07: Sprint Wrap-Up
- **Objective:** Ensure pipeline stability and finalize Sprint 1.
- **Actions:** Executed exploratory SQL queries and achieved 100% pass rate across 38 unit tests.

---

## 📅 Sprint 2 Progress Tracker (Analytics Engine)

### 📈 Day 08: Profitability Ratios Implementation
- **Objective:** Program core profitability ratios.
- **KPIs Computed:** Net Profit Margin (NPM), Operating Profit Margin (OPM), Return on Equity (ROE), and Return on Capital Employed (ROCE).
- **Edge Case Handling:** Handled negative equity and zero sales scenarios.

### ⚖️ Day 09: Leverage & Efficiency Ratios
- **Objective:** Build metrics to evaluate corporate debt levels and asset utilization.
- **KPIs Computed:** Debt-to-Equity (D/E) Ratio, Interest Coverage Ratio (ICR), and Asset Turnover Ratio.
- **Edge Case Handling:** Developed Bank Carve-out logic and Debt-free substitution.

### 📊 Day 10: CAGR Calculation Engine
- **Objective:** Engineer a Compound Annual Growth Rate (CAGR) calculator.
- **KPIs Computed:** Revenue CAGR, PAT CAGR, and EPS CAGR (3Y, 5Y, and 10Y).
- **Edge Case Handling:** Integrated "Turnaround Flag Logic" and bypassed negative base complex math.

### 💸 Day 11: Cash Flow KPIs & Allocation Patterns
- **Objective:** Analyze cash flow statements.
- **KPIs Computed:** Free Cash Flow (FCF), CFO Quality Score, CapEx Intensity.
- **Pattern Classification:** Developed a proprietary algorithm to classify companies into 8 Capital Allocation Patterns (e.g., Mature/Cash Cow).

### 🗄️ Day 12: Database Population & Core Ingestion
- **Objective:** Aggregate all calculated analytics and ingest them into SQLite.
- **Actions:** Merged outputs using composite keys (`company_id`, `year`) and uploaded 1,467 processed rows to the `financial_ratios` table.

### 🏦 Day 13: Specialized Banking ROCE Adjustments
- **Objective:** Develop a sector-relative approach for Banks and NBFCs.
- **Actions:** Identified that standard ROCE logic fails for financials (as debt is raw material). Logged 54 anomalies dynamically by comparing calculated values against source benchmarks.
- **Deliverable:** `src/analytics/banking_roce.py` & `reports/sector_roce_notes.csv`

### ✅ Day 14: Final Test Validation & Retrospective
- **Objective:** Ensure mathematical perfection across all programmed KPI formulas.
- **Actions:** Authored 25 edge-case unit tests. Achieved a 100% green pass rate (0 failures). Documented all mathematical workarounds in an edge case log.
- **Deliverable:** `tests/kpi/test_analytics_engine.py`, `reports/ratio_edge_cases.log`, `docs/sprint2_retro.md`

---

## 📅 Sprint 3 Progress Tracker (Screener Engine)

### ⚙️ Day 15: Custom Filter Engine & YAML Configuration
- **Objective:** Build a multi-criteria stock screener engine driven by YAML.
- **Actions:** Configured `screener_config.yaml` and implemented dynamic filtering using Pandas.

### 🔍 Day 16: Preset Screener Implementation
- **Objective:** Configure 6 preset screeners (Quality, Value, Growth, Dividend, Momentum, Debt-free).
- **Actions:** Tested presets on the 92-company universe and verified business logic consistency.

### 🏆 Day 17: Composite Ranking Engine
- **Objective:** Develop a ranking engine using a weighted composite score.
- **Actions:** - Implemented weighting: Profitability (50%), Growth (30%), Valuation (20%).
  - Performed sector-relative normalization.
  - Exported final rankings to `screener_output.xlsx`.

### 🏦 Day 18: Peer Group Module
- **Objective:** Compute peer-relative performance.
- **Actions:** Loaded `peer_groups.xlsx`, calculated `PERCENT_RANK` for key metrics per sector, and populated the `peer_percentiles` table in `nifty100.db`.

### 🕸️ Day 19: Radar Chart Visualization
- **Objective:** Generate visual performance comparisons.
- **Actions:** Engineered a Plotly visualization module to generate radar charts for each company against its peer group median. Exported 56 PNG charts to `reports/radar_charts/`.

### 📊 Day 20: Peer Comparison Excel Reports
- **Objective:** Generate robust, sector-wise peer comparison Excel reports.
- **Actions:** Built `src/reports/peer_comparison.py`. Resolved complex data mapping issues by implementing a Pandas `merge` to accurately join percentile rank data (`peer_percentiles`) with actual financial metrics (`financial_ratios`), ensuring correct ROE and NPM values in the final outputs.

### 🏁 Day 21: Sprint 3 Final Wrap & DQ Tests
- **Objective:** Validate Sprint 3 data integrity and conduct retrospective.
- **Actions:** - Authored and ran `tests/dq/test_dq_sprint3.py`, ensuring all percentile ranks fall strictly within the valid 0-100 bounds and checking for null assignment failures.
  - Achieved 100% Green DQ pass rate.
  - Documented action items, learnings, and data merging workarounds in `docs/sprint3_retro.md`. Sprint 3 officially closed.

---

## 📅 Sprint 4 Progress Tracker (Dashboard & Valuation)

### 📅 Day 22: Dashboard Foundation & Scaffold
- **Task 1:** Established directory structure (`src/dashboard/pages/`).
- **Task 2:** Created `src/dashboard/utils/db.py` with `@st.cache_data` for efficient data fetching.
- **Task 3:** Built `app.py` entry point with custom styling, sidebar logo, and branding.

### 📅 Day 23: Home & Company Profile Screens
- **5.1 Home / Overview:** Displayed market health, top KPIs, and sector donut chart.
- **5.2 Company Profile:** Implemented ticker search, 6-metric KPI tiles, and dynamic charts.

### 📅 Day 24: Screener & Peer Comparison Screens
- **5.3 Financial Screener:** Integrated sidebar sliders for real-time data filtering.
- **5.4 Peer Comparison:** Peer group dropdown selector with integrated Radar Chart visualizations.

### 📅 Day 25: Trend Analysis, Sector & Allocation
- **5.5-5.8 Analysis:** Built Trend sparklines, Sector bubble charts, Capital Allocation Treemap, and Annual Report links.

### 📅 Day 26: Valuation & Market Data Module
- **Valuation Analytics:** Computed P/E, P/B, EV/EBITDA trends using `market_cap.xlsx`. Implemented logic to flag Caution/Discount badges.

### 📅 Day 27: Integration Testing & QA
- **Dashboard QA:** Tested all 8 screens, fixed responsiveness, and documented results in `tests/dq/dashboard_qa.md`.

### 📅 Day 28: Sprint Wrap-Up
- **Retrospective:** Finalized project demo preparation, updated navigation guide, and closed Sprint 4.

---

## 📅 Sprint 5 Progress Tracker (NLP & Cash Flow Intelligence)

### 🧠 Day 29: NLP Module Parser & Business Tagger
- **CAGR Cross-Validator:** Engineered `src/analytics/cagr_validator.py` to parse text metrics and cross-validate against the Ratio Engine database computations, intelligently flagging divergences >5%.
- **Business Description Tagger:** Built `src/analytics/business_tagger.py` utilizing an NLP keyword-matching algorithm to classify company sectors from raw business descriptions and validate them against actual database records.

### ⚖️ Day 30: Automated Pros/Cons & Sentiment Scoring
- **Auto Pros/Cons Rule Engine:** Developed `src/analytics/pros_cons_generator.py` mapping 12 positive and 12 negative KPI thresholds (e.g., ROE > 20%, D/E > 2) to dynamically generate over 130 qualitative insights with automated confidence scoring.
- **Sentiment Scorer:** Integrated NLTK VADER via `src/analytics/sentiment_scorer.py` to conduct basic polarity scoring on the generated text, scientifically validating the positive/negative tone of the generated pros and cons.

### 💸 Day 31: Cash Flow Quality & CapEx Analysis
- **CFO Quality Score:** Authored `src/analytics/cashflow_intelligence.py` to evaluate core earnings quality based on 5-year average CFO/PAT ratios, assigning badges such as 'High Quality Earnings' and 'Accrual Risk'.
- **CapEx Intensity & FCF Conversion:** Expanded cash flow analytics (`src/analytics/cashflow_task2.py`) to calculate CapEx/Revenue % and FCF/EBITDA ratios, successfully identifying asset-light vs. capital-intensive business models.
- **FCF CAGR Engine:** Computed 5-year and 10-year Free Cash Flow CAGR via `src/analytics/cashflow_task3.py`, tracking long-term cash generation trends and appending all insights into `cashflow_intelligence.xlsx`.

### ⚠️ Day 32: Financial Distress & Capital Allocation
- **Distress Rule Engine:** Developed `src/analytics/distress_flags.py` to automatically flag companies facing operational crisis or actively deleveraging. Output saved to `distress_alerts.csv`.
- **Capital Allocation Matrix:** Built `src/analytics/capital_allocation.py` to map 8 distinct CFO/CFI/CFF sign patterns to descriptive business phases (e.g., Cash Cow, Aggressive Growth) and appended these labels to the cash flow intelligence report.

### 📈 Day 33: Portfolio Statistics & Correlation Heatmaps
- **Portfolio Stats:** Generated portfolio-level distributions (`src/analytics/portfolio_stats.py`) calculating P10, P25, P50, P75, P90, Mean, and Std for key metrics across the Nifty 100.
- **Correlation & Outliers:** Engineered `src/analytics/correlation_outliers.py` to compute a Pearson Correlation Matrix for 10 core KPIs (visualized as a heatmap via Plotly) and implemented an Outlier Detection algorithm using Z-scores (|Z| > 3).

### 🤖 Day 34: KMeans ML Clustering & Profiling
- **Unsupervised ML:** Implemented `scikit-learn` in `src/analytics/kmeans_clustering.py` to cluster Nifty 100 companies based on 5 key features (ROE, D/E, OPM, Rev CAGR, FCF CAGR). Validated $k=5$ using the Elbow Method.
- **Cluster Profiling:** Developed `src/analytics/cluster_profiling.py` to dynamically assign descriptive business profiles (e.g., High-Quality Growth, Distressed, Value Cyclicals) based on cluster centroids.

### 📄 Day 35: Automated PDF Report Generator & QA
- **ReportLab Integration:** Built a robust PDF pipeline (`src/analytics/pdf_generator.py` & `src/analytics/sector_screener_pdf.py`) utilizing `ReportLab` and `Matplotlib`.
- **Automated Deliverables:** Successfully auto-generated Company Tearsheets (with bar charts and KPI tables), Sector Intelligence Reports, Portfolio Summaries, and Top 10 Screener Outputs.
- **Sprint 5 QA Validation:** Executed `src/analytics/sprint5_review.py` to automatically validate PDF generation, audit CF distress flags, and check NLP coverage.

--- 

## 📅 Sprint 6 Progress Tracker (API, Testing & Delivery)

### 🌐 Day 36-40: FastAPI Backend Development

- **Objective:** Serve all analytical data to the frontend via REST API.

- **Actions:** Built `src/api/main.py` and 16 modular endpoints under `src/api/routers/`. Validated endpoints using Postman.


### 🧪 Day 41-42: Testing & Quality Assurance

- **Objective:** Ensure 100% code stability.

- **Actions:** Wrote comprehensive unit tests (`tests/etl`, `tests/kpi`, `tests/api`). Achieved full pass rate (**137 tests passed**) and exported `pytest_report.html`.


### ⚡ Day 43: Performance Optimization & Integration

- **Objective:** Load testing and DB optimization.

- **Actions:** Added SQLite indexes (`scripts/optimize_db.py`). Handled **10 concurrent screener API requests** in **< 0.5 seconds**. Documented in `perf_notes.md`.


### 📚 Day 44: Documentation & Formatting

- **Objective:** Standardize code and document the platform.

- **Actions:** Applied **black** and **ruff** formatting. Wrote the final `analyst_guide.pdf`. Archived deliverables.


### 🏆 Day 45: Final Delivery & Sign-Off

- **Objective:** Handover the project.

- **Actions:** Generated `acceptance_checklist.pdf`. Validated all **20 Acceptance Gates**. Tagged repository as **Release v1.0**.

---
## 📂 Repository Structure
```text
📦N100 FINANCIAL INTELLIGENCE PLATFORM
 ┣ 📂config                       # System & Logger Configurations
 ┃ ┣ 📜screener_config.yaml       # Multi-criteria Screener Thresholds
 ┃ ┣ 📜logging_config.yaml        # Application Logging Strategy
 ┃ ┗ 📜.env.template              # Environment Variables Spec
 ┣ 📂data                         # Database & Raw Excel Financial Datasets
 ┃ ┣ 📂raw                        # 7 Core Raw Financial Datasets (Read-Only)
 ┃ ┃ ┣ 📜companies.xlsx           # 92 Tracked Companies Metadata
 ┃ ┃ ┣ 📜profitandloss.xlsx       # 10-Year Historical Income Statements
 ┃ ┃ ┣ 📜balancesheet.xlsx        # Historical Balance Sheet Records
 ┃ ┃ ┣ 📜cashflow.xlsx            # Historical Cash Flow Statements
 ┃ ┃ ┣ 📜prosandcons.xlsx         # Qualitative Business Factors
 ┃ ┃ ┣ 📜documents.xlsx           # Annual Report Document Links
 ┃ ┃ ┗ 📜analysis.xlsx            # Textual Ratios & Growth Narrative
 ┃ ┣ 📂supporting                 # 5 Supplementary Benchmark Files
 ┃ ┃ ┣ 📜financial_ratios.xlsx    # Benchmark KPI Validation Sets
 ┃ ┃ ┣ 📜market_cap.xlsx          # Valuation Trends & Valuation Metrics
 ┃ ┃ ┣ 📜peer_groups.xlsx         # Sector Peer Categorization Mapping
 ┃ ┃ ┣ 📜sectors.xlsx             # Sectoral Classifications
 ┃ ┃ ┗ 📜stock_prices.xlsx        # Price Movements Data
 ┃ ┣ 📂processed                  # Cleaned Analytics & NLP Outputs
 ┃ ┃ ┣ 📜analysis_parsed.csv      # Parsed Narrative Metrics
 ┃ ┃ ┣ 📜pros_cons_generated.csv  # Dynamic Rule-Generated Qualitative Points
 ┃ ┃ ┗ 📜cluster_labels.csv       # K-Means Cluster Classifications
 ┃ ┗ 📜nifty100.db                # Centralized Star-Schema SQLite Database
 ┣ 📂docs                         # User Manuals & Sign-Off Documentation
 ┃ ┣ 📜analyst_guide.pdf          # 10-Page Platform Analyst Guide
 ┃ ┣ 📜acceptance_checklist.pdf   # Official Acceptance Sign-Off Document
 ┃ ┣ 📜openapi.json               # Exported OpenAPI REST API Specification
 ┃ ┣ 📜dashboard_guide.md         # Streamlit Navigation Blueprint
 ┃ ┣ 📜sprint2_retro.md           # Sprint 2 Engineering Retrospective
 ┃ ┣ 📜sprint3_retro.md           # Sprint 3 Engineering Retrospective
 ┃ ┣ 📜sprint4_retro.md           # Sprint 4 Engineering Retrospective
 ┃ ┗ 📜sprint5_retro.md           # Sprint 5 Engineering Retrospective
 ┣ 📂output                       # Release Outputs & Artifacts
 ┃ ┣ 📂final_deliverables         # Release v1.0 Archive Directory
 ┃ ┃ ┣ 📜nifty100.db              # Processed SQLite Database
 ┃ ┃ ┣ 📜README.md                # Final Project Documentation
 ┃ ┃ ┣ 📜analyst_guide.pdf        # Analyst Platform Guide
 ┃ ┃ ┣ 📜acceptance_checklist.pdf # Signed Acceptance Document
 ┃ ┃ ┣ 📜pytest_report.html       # Automated QA Audit Report
 ┃ ┃ ┣ 📜perf_notes.md            # Load Testing Audit Report
 ┃ ┃ ┗ 📜openapi.json             # Swagger API Specification
 ┃ ┣ 📜cashflow_intelligence.xlsx # Master Cash Flow Analytical Export
 ┃ ┣ 📜peer_comparison.xlsx       # Peer Group Metric Benchmark Workbooks
 ┃ ┣ 📜screener_output.xlsx       # Filtered & Ranked Investment Recommendations
 ┃ ┣ 📜portfolio_stats.csv        # Portfolio Metric Distributions (P10-P90)
 ┃ ┗ 📜perf_notes.md              # Database & API Performance Notes
 ┣ 📂project_guidelines           # Sprint Specifications & Technical Charters
 ┣ 📂reports                      # Generated Visualizations & Audit Artifacts
 ┃ ┣ 📂tearsheets                 # Automated PDF Executive Summary Reports
 ┃ ┣ 📂sector                     # Automated Sector Intelligence PDFs
 ┃ ┣ 📂portfolio                  # Portfolio Distribution Summary PDFs
 ┃ ┣ 📂screener                   # Top 10 Screener Selection PDFs
 ┃ ┣ 📂radar_charts               # 56 Dynamic Sector Peer Radar Plots (.png)
 ┃ ┣ 📂visualizations             # Correlation Heatmaps & Elbow Plots
 ┃ ┣ 📂alerts                     # Financial Distress & Outlier Logs (.csv)
 ┃ ┣ 📂qa_validation              # NLP Tag & Metric Cross-Validation Reports
 ┃ ┣ 📜pytest_report.html         # Interactive HTML Test Results
 ┃ ┣ 📜load_audit.csv             # ETL Database Ingestion Audit Log
 ┃ ┣ 📜sector_roce_notes.csv      # Banking & Financials Anomaly Audit Log
 ┃ ┗ 📜ratio_edge_cases.log       # Mathematical Constraint Exception Handling Logs
 ┣ 📂scripts                      # System Utility, DB, and Load Testing Scripts
 ┃ ┣ 📜optimize_db.py             # SQLite Index Creation Script
 ┃ ┣ 📜load_test.py               # Concurrent REST API Simulation Tool
 ┃ ┣ 📜ranking_engine.py          # Sector-Relative Weighted Ranking Calculator
 ┃ ┣ 📜screener_preset_test.py    # YAML Filter Validation Executor
 ┃ ┣ 📜archive_project.py         # Deliverable Packaging Automator
 ┃ ┣ 📜generate_checklist.py     # Acceptance Gate Document Generator
 ┃ ┗ 📜check_db.py                # Database Health Inspector
 ┣ 📂src                          # Platform Source Engine Core Codebase
 ┃ ┣ 📂analytics                  # Financial Logic & Machine Learning Engines
 ┃ ┃ ┣ 📂screener                 # Multi-Criteria Filtering Engine
 ┃ ┃ ┃ ┗ 📜engine.py              # Screener Business Logic
 ┃ ┃ ┣ 📜ratios.py                # 50+ Financial Ratio Calculator Engine
 ┃ ┃ ┣ 📜cagr.py                  # Growth & Turnaround Flag Logic
 ┃ ┃ ┣ 📜cashflow_intelligence.py # CFO Quality Score & CapEx Calculator
 ┃ ┃ ┣ 📜banking_roce.py          # Specialized Banking Capital Adjustments
 ┃ ┃ ┣ 📜peer.py                  # Percentile Rank Benchmarking
 ┃ ┃ ┣ 📜kmeans_clustering.py     # Unsupervised K-Means Clustering Model
 ┃ ┃ ┣ 📜cluster_profiling.py     # Dynamic Profile Labeling Engine
 ┃ ┃ ┣ 📜sentiment_scorer.py      # NLTK VADER Sentiment Analyzer
 ┃ ┃ ┣ 📜business_tagger.py       # NLP Keyword Sector Categorizer
 ┃ ┃ ┣ 📜pdf_generator.py         # Dynamic ReportLab Tearsheet Generator
 ┃ ┃ ┗ 📜populate_ratios.py       # DB Ingestion Coordinator
 ┃ ┣ 📂api                        # High-Performance FastAPI REST Framework
 ┃ ┃ ┣ 📂routers                 # Endpoint Module Controller Routers
 ┃ ┃ ┃ ┣ 📜companies.py           # Profiles & Ratios Endpoints
 ┃ ┃ ┃ ┣ 📜screener.py            # Dynamic Screening Endpoints
 ┃ ┃ ┃ ┣ 📜peers.py               # Benchmarks & Radar Chart Endpoints
 ┃ ┃ ┃ ┣ 📜sectors.py             # Sector Summary & Comparison Endpoints
 ┃ ┃ ┃ ┣ 📜portfolio.py           # Distribution & Stats Endpoints
 ┃ ┃ ┃ ┣ 📜valuation.py           # Multiples & Market Cap Endpoints
 ┃ ┃ ┃ ┗ 📜documents.py           # PDF Download Dispatch Endpoints
 ┃ ┃ ┣ 📜main.py                  # API Server Setup & Middleware Rules
 ┃ ┃ ┗ 📜database.py              # SQLite Connection Handler
 ┃ ┣ 📂dashboard                  # Streamlit Multi-Page Client Interface
 ┃ ┃ ┣ 📂pages                    # 9 Multi-Page Interactive Screens
 ┃ ┃ ┃ ┣ 📜01_home.py             # Market Health Overview Dashboard
 ┃ ┃ ┃ ┣ 📜02_profile.py          # Deep-Dive Company Profile Page
 ┃ ┃ ┃ ┣ 📜03_screener.py         # Dynamic Screener Interface
 ┃ ┃ ┃ ┣ 📜04_peer.py             # Interactive Radar Peer Comparison
 ┃ ┃ ┃ ┣ 📜05_trends.py           # Historic Trend Analysis & Sparklines
 ┃ ┃ ┃ ┣ 📜06_sectors.py          # Sector Bubble Analysis Page
 ┃ ┃ ┃ ┣ 📜07_capital.py          # Capital Allocation Treemap Page
 ┃ ┃ ┃ ┣ 📜08_reports.py          # Automated Report Download Page
 ┃ ┃ ┃ ┗ 📜09_valuation.py        # Valuation Multiples Page
 ┃ ┃ ┣ 📂utils                    # Data Fetching & Plotly Visual Utilities
 ┃ ┃ ┗ 📜app.py                   # Streamlit Main App Launcher
 ┃ ┣ 📂etl                        # ETL Pipeline Infrastructure
 ┃ ┃ ┣ 📜loader.py                # Master Excel to SQLite Pipeline Ingester
 ┃ ┃ ┣ 📜normaliser.py            # Cleansing Functions for Tickers & Years
 ┃ ┃ ┣ 📜validator.py             # 16 Data Quality Verification Rules
 ┃ ┃ ┗ 📜schema.sql               # Relational Database DDL Definitions
 ┃ ┣ 📂nlp                        # Sentiment & Pros/Cons Text Parsers
 ┃ ┗ 📂reports                    # Excel & Plotly Chart Generation Engine
 ┣ 📂tests                        # Automated Pytest Quality Assurance Suite
 ┃ ┣ 📂etl                        # Data Cleaning & Validation Test Suite
 ┃ ┣ 📂kpi                        # Formula Precision & Edge Case Test Suite
 ┃ ┣ 📂api                        # Endpoint Status & Payload Test Suite
 ┃ ┗ 📂dq                         # Data Quality Constraint Rule Tests
 ┣ 📜activate_env.bat             # Environment Activation Utility
 ┣ 📜Makefile                     # Automation CLI Command Triggers
 ┣ 📜requirements.txt             # Project Dependencies Listing
 ┣ 📜nifty100.db                  # Central SQLite Database Instance
 ┣ 📜pytest_report.html           # Audited Unit & Integration Test Summary
 ┗ 📜README.md                    # Core Platform Documentation Manual
 ```

---

## 🛠️ Execution & Setup Guide
If you are a developer looking to run specific background jobs or generate standalone reports without using the dashboard, follow these direct execution commands:

### 1. System Deployment & Virtual Environment Setup

Activate the Python dependency environment:

```powershell
.\activate_env.bat
```

### 2. Execute Unit Tests & Generate Report

Run the comprehensive unit test suite to validate the normalization logic:

```bash
make test
```

### 3. Verify the HTML Test Report

Open the generated file at `reports/pytest_report.html` in any web browser to see the professional pipeline audit execution results.

### 4. Run the Analytics Engine (Profitability Ratios)

Execute the scripts to calculate Ratios and CAGR metrics:

```bash
python -m src.analytics.ratios
python -m src.analytics.cagr
```

### 5. Run the Analytics Engines & Populate Database

Execute the master population script to run all analytical modules and ingest data into SQLite:

```bash
python -m src.analytics.populate_ratios
```

### 6. Execute Specialized Banking Analysis

Run the sector-relative ROCE adjustments:

```bash
python -m src.analytics.banking_roce
```

### 7. Execute Complete Unit Test Suite

Run the comprehensive test suite to validate all ETL and Analytics (KPI) logic:

```bash
make test
# OR
pytest tests/
```

### 8. Run the Screener Engine 

Execute the dynamic screener engine to filter companies based on custom parameters:

```bash
python -m src.analytics.screener.engine
```

### 9. Run Screener Engine

```bash
python scripts/screener_preset_test.py
```

### 10. Generate Ranking Report

```bash
python scripts/ranking_engine.py
```

### 11. Generate Peer Percentiles & Charts

```bash
python -m src.analytics.peer
python -m src.reports.radar_charts
```

### 12. Generate Peer Comparison Excel Reports

```bash
python src/reports/peer_comparison.py  
```

### 13. Run Data Quality (DQ) Tests

```bash
python tests/dq/test_dq_sprint3.py
```

### 14. Run Sprint 5 (NLP & Cash Flow Modules)

```bash
# Validation, Tagger, Pros/Cons & Sentiment
python src/analytics/cagr_validator.py
python src/analytics/business_tagger.py
python src/analytics/pros_cons_generator.py
python src/analytics/sentiment_scorer.py

# Cashflow Intelligence & Matrix
python src/analytics/cashflow_intelligence.py
python src/analytics/cashflow_task2.py
python src/analytics/cashflow_task3.py
python src/analytics/distress_flags.py
python src/analytics/capital_allocation.py

# ML Clustering, Statistics & Heatmaps
python src/analytics/portfolio_stats.py
python src/analytics/correlation_outliers.py
python src/analytics/kmeans_clustering.py
python src/analytics/cluster_profiling.py

# Automated PDF Reports & Final Sprint QA
python src/analytics/pdf_generator.py
python src/analytics/sector_screener_pdf.py
python src/analytics/sprint5_review.py
```

### 15. Run Backend REST API Server
Start the FastAPI server on Port 8000:

```bash
uvicorn src.api.main:app --port 8000 --reload
```

### 16. Execute Full Pytest QA Test Suite
Run all 130+ unit, integration, and API endpoint test cases and generate an HTML report:

```bash
python -m pytest tests/ -v --html=pytest_report.html
```

### 17. Execute Database Optimization & Performance Load Test
Apply SQLite indexes on company_id / year and execute 10 concurrent API query simulations:

```bash
python scripts/optimize_db.py
python scripts/load_test.py
```

### 18. Code Formatting & Quality Linting
Format all python files according to PEP8 guidelines using Black and Ruff:

```bash
black src/ tests/ scripts/
ruff check src/ tests/ scripts/ --fix --ignore E402,E712,F841,E722
```

### 19. Generate Documentation PDFs
Generate the Analyst Guide PDF and Final Acceptance Checklist PDF:

```bash
python scripts/make_pdf.py
python scripts/generate_checklist.py
```

### 20. Archive Final Release Deliverables
Package all 23 final project deliverables into the release archive folder:

```bash
python scripts/archive_project.py
```
---

## 🚀 How to Run the Dashboard
This project features a fully interactive 9-screen multi-page Streamlit application. Follow these steps to run the dashboard locally:
#### 1. Install Dependencies:
Ensure you have Python installed. Activate your virtual environment and install the required libraries:
```bash
pip install streamlit pandas plotly sqlite3
```

#### 2. Run the Application:
Navigate to the root directory of the project and execute the following command:
```bash
streamlit run src/dashboard/app.py
```

#### 3. Access the Dashboard:
Once the server starts, open your browser and navigate to the local URL provided in the terminal (usually http://localhost:8501).

---

# 🗺️ Future Roadmap

The platform is designed with scalability and continuous enhancement in mind. Planned future improvements include:

- **Docker Containerization**  
      Package the FastAPI backend and Streamlit dashboard into lightweight Docker containers for simplified deployment across cloud and on-premise environments.

- **Real-Time Market Data Integration**  
      Integrate live stock price streaming using WebSockets to provide real-time valuation metrics and continuously updated dashboards.

- **Advanced AI-Powered Sentiment Analysis**  
      Replace the current NLTK VADER sentiment engine with transformer-based financial language models such as **FinBERT** for deeper analysis of annual reports, earnings calls, and financial news.

- **Automated Email Notification System**  
      Implement configurable email alerts to notify users whenever screened companies satisfy predefined financial or valuation conditions.

---

# ❓ Frequently Asked Questions (FAQ)

### **Q1. Why was SQLite chosen instead of PostgreSQL or MySQL?**

SQLite provides a lightweight, zero-configuration database solution that is ideal for local analytical workloads. Combined with proper indexing and optimized queries, it delivers excellent performance while keeping project setup simple and portable.


### **Q2. How are Banks and NBFCs handled differently?**

Traditional ROCE calculations are not suitable for financial institutions because debt represents an operational resource rather than financial leverage. The platform includes a dedicated **`banking_roce.py`** module that applies sector-specific adjustments to generate more meaningful performance metrics.


### **Q3. How are negative earnings handled during CAGR calculations?**

Standard CAGR formulas cannot accurately process negative-to-positive financial transitions. The platform implements a custom **Turnaround Flag Logic**, allowing CAGR calculations to remain meaningful while avoiding invalid or misleading outputs.

---

# 🤝 Contributing

Contributions are always welcome.

If you would like to improve this project, feel free to:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your improvements with meaningful commit messages.
4. Push your branch to GitHub.
5. Submit a Pull Request for review.

Whether it's improving analytics, optimizing performance, enhancing the dashboard, or adding new features, every contribution is appreciated.

---

# 📄 License

This project is intended for **educational, research, and portfolio purposes**.

Feel free to explore, learn from, and build upon this work while providing appropriate attribution.

---

# 🙏 Acknowledgements

Special thanks to the following communities and organizations that contributed directly or indirectly to this project:

- **Bluestock Fintech** for providing the internship problem statement, project structure, and learning opportunities.
- **National Stock Exchange (NSE) India** for serving as the foundation for financial market analysis.
- **The Python Open Source Community** for developing outstanding libraries including Pandas, NumPy, FastAPI, Streamlit, Plotly, Scikit-learn, ReportLab, and Pytest.
- Every open-source contributor whose work made this project possible.

---

# 👨‍💻 Author

## Hashmil Muhammed

**AI Engineer | Data Scientist | Data Analyst | Python Developer | Machine Learning Enthusiast**

- 🎓 MCA — SCMS School of Engineering & Technology
- 💻 Specializing in AI, Machine Learning, Data Engineering, Financial Analytics, and Full-Stack Development
- 🌱 Passionate about building intelligent, scalable, and production-ready software solutions

**Live Platform:** 
https://finsight-n100.streamlit.app/

**GitHub:**  https://github.com/Hashmil-Muhammed

**LinkedIn:**
 https://www.linkedin.com/in/hashmil-muhammed08/

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a Star.

Thank you for visiting this repository and supporting the project.

</div>




