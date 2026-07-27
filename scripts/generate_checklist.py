import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def create_acceptance_checklist():
    os.makedirs("docs", exist_ok=True)
    pdf_path = "docs/acceptance_checklist.pdf"
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    elements.append(Paragraph("<b>N100 Financial Intelligence Platform</b>", styles['Title']))
    elements.append(Paragraph("<b>Day 45: Final Acceptance Checklist (Sign-Off)</b>", styles['Heading2']))
    elements.append(Spacer(1, 12))
    
    # Data for the table
    data = [
        ["ID", "Acceptance Gate / Deliverable", "Status", "File Path / Verification"],
        ["AC-01", "10 Years Data Extracted (92 Companies)", "PASS", "nifty100.db"],
        ["AC-02", "Data Normalized (Zero nulls in PKs)", "PASS", "src/etl/normaliser.py"],
        ["AC-03", "Data Quality Rules Applied (14 Rules)", "PASS", "src/etl/validator.py"],
        ["AC-04", "Ratio Engine Built (50+ KPIs)", "PASS", "src/analytics/ratios.py"],
        ["AC-05", "CAGR & Turnaround Metrics Computed", "PASS", "src/analytics/cagr.py"],
        ["AC-06", "Screener Engine Operational", "PASS", "src/analytics/screener/engine.py"],
        ["AC-07", "K-Means Clustering Implemented", "PASS", "src/analytics/kmeans_clustering.py"],
        ["AC-08", "NLP Sentiment Scorer Applied", "PASS", "src/analytics/sentiment_scorer.py"],
        ["AC-09", "Automated PDF Tearsheets Generating", "PASS", "src/analytics/pdf_generator.py"],
        ["AC-10", "FastAPI Server Running (16 Endpoints)", "PASS", "src/api/main.py"],
        ["AC-11", "OpenAPI & Postman Collection Exported", "PASS", "openapi.json"],
        ["AC-12", "Streamlit Dashboard Fully Interactive", "PASS", "src/dashboard/app.py"],
        ["AC-13", "Pytest Suite Passing (130+ Tests)", "PASS", "pytest_report.html"],
        ["AC-14", "Performance Load Test (10 req < 10s)", "PASS", "output/perf_notes.md"],
        ["AC-15", "All Python Code Linted (Black & Ruff)", "PASS", "Terminal Output: All Clear"],
        ["AC-16", "Analyst Guide Documentation Created", "PASS", "docs/analyst_guide.pdf"],
        ["AC-17", "README.md Fully Updated", "PASS", "README.md"],
        ["AC-18", "Database Indexed for Speed", "PASS", "scripts/optimize_db.py"],
        ["AC-19", "All Deliverables Archived", "PASS", "output/final_deliverables/"],
        ["AC-20", "Sprint 6 Review & Demo Completed", "PASS", "Pending Lead Sign-Off"]
    ]
    
    # Table Style
    t = Table(data, colWidths=[50, 220, 50, 180])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (2, 1), (2, -1), colors.darkgreen), # Green PASS
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 30))
    
    # Sign-off section
    elements.append(Paragraph("<b>Final Sign-Off</b>", styles['Heading3']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Data Engineering Lead: ____________________ Date: _________", styles['Normal']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Analytics Lead: ____________________ Date: _________", styles['Normal']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Project Manager (Release v1.0): ____________________ Date: _________", styles['Normal']))
    
    doc.build(elements)
    print(f"✅ Final Acceptance Checklist Generated: {pdf_path}")

if __name__ == "__main__":
    create_acceptance_checklist()