import streamlit as st
import os
import sys
from pathlib import Path

# 1. First: Set up the path
root_path = Path(__file__).resolve().parents[1]  # This points to the 'src' folder
sys.path.append(str(root_path))

# 2. Second: Now import from dashboard
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set page configuration
st.set_page_config(
    page_title="FinSight N100 | Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# PREMIUM WEBSITE CSS INJECTION
# ==========================================
st.markdown("""
<style>
/* Import Premium Web Font */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Remove default Streamlit top padding */
.block-container {
    padding-top: 1.5rem !important;
    max-width: 1400px;
}

/* Hero Section */
.hero-wrapper {
    text-align: center;
    animation: fadeInDown 1s ease-out;
}
.hero-logo {
    width: 85px;
    height: 85px;
    object-fit: contain;
    margin: 0 auto 1rem auto;
    display: block;
    filter: drop-shadow(0 0 12px rgba(0, 198, 255, 0.4));
}
.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00C6FF 0%, #0072FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #94a3b8;
    font-weight: 400;
    margin-bottom: 2rem;
}

/* 💎 Premium Justified Summary Box */
/* 💎 Premium Glassmorphism Summary Card */
.summary-box {
    background: radial-gradient(100% 100% at 50% 0%, rgba(0, 198, 255, 0.08) 0%, rgba(15, 23, 42, 0.6) 100%);
    border: 1px solid rgba(0, 198, 255, 0.2);
    border-radius: 20px;
    padding: 2.2rem 2.8rem;
    max-width: 980px;
    margin: 0 auto 2.5rem auto;
    color: #cbd5e1;
    font-size: 1.08rem;
    line-height: 1.85;
    text-align: justify;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    letter-spacing: 0.2px;
    backdrop-filter: blur(16px) saturate(180%);
    -webkit-backdrop-filter: blur(16px) saturate(180%);
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), 
                0 0 20px 0 rgba(0, 198, 255, 0.1);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    overflow: hidden;
}

/* Hover-ൽ ഉണ്ടാകുന്ന Glowing Effect */
.summary-box:hover {
    transform: translateY(-4px);
    border-color: rgba(0, 198, 255, 0.5);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 
                0 0 30px 2px rgba(0, 198, 255, 0.2);
}

/* 🌟 Bold/Highlight Text Gradient Styling */
.summary-box b {
    background: linear-gradient(135deg, #00C6FF 0%, #0072FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}



/* Tech Stack Badges */
.badge-container {
    display: flex;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 3.5rem;
}
.badge-container img {
    border-radius: 6px;
    transition: transform 0.3s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
}
.badge-container img:hover {
    transform: translateY(-3px);
}

/* Glassmorphism Metrics */
[data-testid="stMetric"] {
    background: rgba(17, 25, 40, 0.6);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    text-align: center;
    transition: transform 0.3s ease, border-color 0.3s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    border-color: #00C6FF;
}
[data-testid="stMetricValue"] {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

/* Feature Grid */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 1.5rem 0 3rem 0;
}
.feature-card {
    background: rgba(17, 25, 40, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 1.8rem;
    transition: all 0.3s ease;
    height: 100%;
}
.feature-card:hover {
    background: rgba(17, 25, 40, 0.8);
    border: 1px solid #0072FF;
    transform: translateY(-5px);
}
.feature-icon { font-size: 2rem; margin-bottom: 1rem; display: block; }
.feature-title { font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-bottom: 0.8rem; }
.feature-text { color: #94a3b8; font-size: 0.9rem; line-height: 1.6; }

/* Navigation Guide Grid */
.nav-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin-bottom: 3rem;
}
.nav-card {
    background: rgba(30, 41, 59, 0.3);
    border-left: 4px solid #00C6FF;
    padding: 1.2rem;
    border-radius: 8px;
    transition: transform 0.3s ease;
}
.nav-card:hover { transform: translateX(5px); background: rgba(30, 41, 59, 0.6); }
.nav-card h4 { margin: 0 0 0.5rem 0; color: #f8fafc; font-size: 1.05rem; display: flex; align-items: center; gap: 8px; }
.nav-card p { margin: 0; color: #94a3b8; font-size: 0.85rem; line-height: 1.5; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0b0f19;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Animations */
@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR CONFIGURATION
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=60)
st.sidebar.title("FinSight N100")
st.sidebar.caption("Financial Intelligence Platform")
st.sidebar.markdown("---")

# 👨‍💻 Developer Profile Card in Sidebar
st.sidebar.markdown("""
<div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;">
    <h4 style="margin:0; color: #00C6FF; font-size: 1.1rem;">Hashmil Muhammed</h4>
    <p style="margin: 5px 0 10px 0; color: #94a3b8; font-size: 0.9rem;">Data Analyst | AI Engineer</p>
    <a href="https://github.com/Hashmil-Muhammed/Bluestock-Data-Analyst-Internship/tree/main/N100%20FINANCIAL%20INTELLIGENCE%20PLATFORM" target="_blank" style="text-decoration: none; color: white; background: #24292e; padding: 6px 12px; border-radius: 5px; font-size: 0.8rem; display: inline-flex; align-items: center; gap: 5px; border: 1px solid #444; width: 100%; justify-content: center;">
        <img src="https://cdn-icons-png.flaticon.com/512/733/733553.png" width="14"> GitHub Repo
    </a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 🧭 Navigation
1. **Home / Overview**
2. **Company Profile**
3. **Financial Screener**
4. **Peer Comparison**
5. **Trend Analysis**
6. **Sector Analysis**
7. **Capital Allocation**
8. **Annual Reports**
9. **Valuation**
""")
st.sidebar.markdown("---")
st.sidebar.info("v1.0 Production Release")


# ==========================================
# MAIN PAGE CONTENT
# ==========================================

# 1. HERO SECTION
st.markdown("""
<div class="hero-wrapper">
<br>
<br>
<img src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png" class="hero-logo">
<div class="hero-title">FinSight N100</div>
<div class="hero-subtitle">Enterprise-Grade Financial Analytics, REST API & Business Intelligence Solution</div>

<div class="summary-box">
Designed for equity research analysts and portfolio managers, <b>FinSight N100</b> is a fully automated end-to-end data engineering pipeline and BI platform. It ingests, cleanses, and analyzes over <b>10 years of historical financial data (~11,000+ data points)</b> across 92 NSE Nifty 100 constituent companies. Powered by a high-speed FastAPI backend and an interactive Streamlit frontend, it delivers unparalleled insights into profitability, valuation, and capital allocation.
</div>

<div class="badge-container">
<img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/FastAPI-REST_API-009688?style=for-the-badge&logo=fastapi&logoColor=white">
<img src="https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge&logo=sqlite&logoColor=white">
<img src="https://img.shields.io/badge/Pandas-Analytics-purple?style=for-the-badge&logo=pandas&logoColor=white">
<img src="https://img.shields.io/badge/Pytest-137_Tests_Passed-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white">
<img src="https://img.shields.io/badge/Streamlit-Live_Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
<img src="https://img.shields.io/badge/Scikit_Learn-KMeans_Clustering-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white">
<img src="https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge&logo=github-actions&logoColor=white">
<img src="https://img.shields.io/badge/API_Docs-Swagger_UI-009688?style=for-the-badge&logo=swagger&logoColor=white">
<img src="https://img.shields.io/badge/GitHub-Portfolio-black?style=for-the-badge&logo=github&logoColor=white">
</div>
</div>
""", unsafe_allow_html=True)


# 2. METRICS SECTION
m1, m2, m3, m4, m5 = st.columns(5)
with m1: st.metric(label="🏢 Companies Tracked", value="92", delta="Nifty 100")
with m2: st.metric(label="📅 Historical Data", value="10 Yrs", delta="11k+ points")
with m3: st.metric(label="📈 KPIs Computed", value="50+", delta="Automated")
with m4: st.metric(label="🧪 System Tests", value="137/137", delta="100% Passed")
with m5: st.metric(label="⚡ API Latency", value="< 0.5s", delta="Optimized")


# 3. CORE CAPABILITIES
st.markdown("<br><h3 style='text-align: center; font-weight: 700; color: white;'>🚀 Core Platform Capabilities</h3>", unsafe_allow_html=True)
st.markdown("""
<div class="feature-grid">
<div class="feature-card">
<span class="feature-icon">⚙️</span>
<div class="feature-title">Automated ETL & Data Foundation</div>
<div class="feature-text">Standardized star-schema SQLite database built with strict primary/foreign key constraints and 16 Data Quality (DQ) validation rules.</div>
</div>
<div class="feature-card">
<span class="feature-icon">📈</span>
<div class="feature-title">Advanced Analytics Engine</div>
<div class="feature-text">Pre-computes 50+ KPIs including profitability margins, leverage metrics, 10Y CAGRs with turnaround flags, and CFO Quality Scores.</div>
</div>
<div class="feature-card">
<span class="feature-icon">🧠</span>
<div class="feature-title">Machine Learning & NLP</div>
<div class="feature-text">Unsupervised K-Means clustering (k=5) for peer grouping, automated keyword tagging, and NLTK VADER sentiment analysis.</div>
</div>
<div class="feature-card">
<span class="feature-icon">🔍</span>
<div class="feature-title">Smart Screener & Benchmarking</div>
<div class="feature-text">Multi-criteria YAML-configurable stock screening, sector-relative composite ranking engine, and interactive radar chart comparisons.</div>
</div>
</div>
""", unsafe_allow_html=True)


# 4. PLATFORM NAVIGATION GUIDE
st.markdown("<h3 style='text-align: center; font-weight: 700; color: white; margin-bottom: 1.5rem;'>📖 Platform Navigation Guide</h3>", unsafe_allow_html=True)
st.markdown("""
<div class="nav-grid">
<div class="nav-card">
<h4>🏠 1. Home / Overview</h4>
<p>Your main dashboard. View high-level market health, top-performing KPIs, and sector-wise distribution of the Nifty 100 universe.</p>
</div>
<div class="nav-card">
<h4>🏢 2. Company Profile</h4>
<p>Deep-dive into a specific company. Search by ticker to view executive summaries, 6-metric KPI tiles, and individual performance charts.</p>
</div>
<div class="nav-card">
<h4>🎯 3. Financial Screener</h4>
<p>Use interactive sliders to filter companies based on custom financial parameters like ROE, Debt/Equity, and Growth thresholds.</p>
</div>
<div class="nav-card">
<h4>🕸️ 4. Peer Comparison</h4>
<p>Benchmark a company against its sector peers using interactive Plotly Radar Charts and proprietary percentile rankings.</p>
</div>
<div class="nav-card">
<h4>📈 5. Trend Analysis</h4>
<p>Visualize 10-year historical trajectories with sparklines. Track long-term revenue, profit, and margin growth trends.</p>
</div>
<div class="nav-card">
<h4>📊 6. Sector Analysis</h4>
<p>Analyze entire industries at a glance. Compare aggregate sector metrics using interactive bubble charts and distribution plots.</p>
</div>
<div class="nav-card">
<h4>💰 7. Capital Allocation</h4>
<p>Understand how companies manage money. Visualizes Cash Flow patterns to classify businesses into phases like 'Cash Cow' or 'Growth'.</p>
</div>
<div class="nav-card">
<h4>📄 8. Annual Reports & NLP</h4>
<p>Access AI-generated qualitative Pros/Cons, business sentiment scores, and direct links to official company annual reports.</p>
</div>
<div class="nav-card">
<h4>⚖️ 9. Valuation</h4>
<p>Evaluate market pricing. View relative valuation multiples (P/E, EV/EBITDA) and automated 'Discount' or 'Caution' flags.</p>
</div>
</div>
""", unsafe_allow_html=True)


# 5. AUTHOR / DEVELOPER SECTION
st.markdown("<h3 style='text-align: center; font-weight: 700; color: white; margin-bottom: 1.5rem;'>👨‍💻 About the Developer</h3>", unsafe_allow_html=True)
st.markdown("""
<div style="background: linear-gradient(145deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.4)); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 2.5rem; max-width: 950px; margin: 0 auto 3rem auto; display: flex; align-items: center; gap: 2.5rem; flex-wrap: wrap; justify-content: center; backdrop-filter: blur(12px); box-shadow: 0 8px 32px rgba(0,0,0,0.25);">
    <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="110" style="border-radius: 50%; filter: drop-shadow(0 4px 15px rgba(0, 198, 255, 0.4)); border: 2px solid rgba(0, 198, 255, 0.3);">
    <div style="flex: 1; min-width: 300px;">
        <h3 style="margin: 0; color: #00C6FF; font-size: 1.6rem; font-weight: 700;">Hashmil Muhammed</h3>
        <p style="color: #cbd5e1; font-size: 1.05rem; margin: 4px 0 12px 0; font-weight: 600; letter-spacing: 0.5px;">AI Engineer | Data Analyst | Web Developer</p>
        <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.7; text-align: justify; margin: 0 0 1.5rem 0;">
            Currently pursuing a Master of Computer Applications (MCA) at SCMS School of Engineering and Technology (SSET). 
            Passionate about building end-to-end data pipelines, financial intelligence platforms, and integrating machine learning with business intelligence. 
            This FinSight N100 platform was built as the capstone project for the Bluestock Fintech Data Analytics Internship.
        </p>
        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <a href="https://github.com/Hashmil-Muhammed" target="_blank" style="text-decoration: none; color: #ffffff; background: #24292e; padding: 8px 16px; border-radius: 8px; font-size: 0.88rem; font-weight: 600; display: inline-flex; align-items: center; gap: 8px; border: 1px solid rgba(255,255,255,0.15); transition: all 0.3s ease;">
                <img src="https://cdn-icons-png.flaticon.com/512/733/733553.png" width="16" style="filter: invert(1);"> GitHub
            </a>
            <a href="https://www.linkedin.com/in/hashmil-muhammed08/" target="_blank" style="text-decoration: none; color: #ffffff; background: #0A66C2; padding: 8px 16px; border-radius: 8px; font-size: 0.88rem; font-weight: 600; display: inline-flex; align-items: center; gap: 8px; transition: all 0.3s ease;">
                <img src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png" width="16" style="filter: invert(1);"> LinkedIn
            </a>
            <a href="mailto:hashmilmuhammedparammal@gmail.com" style="text-decoration: none; color: #ffffff; background: rgba(255, 255, 255, 0.08); padding: 8px 16px; border-radius: 8px; font-size: 0.88rem; font-weight: 600; display: inline-flex; align-items: center; gap: 8px; border: 1px solid rgba(255,255,255,0.15); transition: all 0.3s ease;">
                ✉️ Email
            </a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 0.9rem; margin-top: 20px;'>
Built with Python & Streamlit | Capstone Project by <b>Hashmil Muhammed</b>
</div>
""", unsafe_allow_html=True)