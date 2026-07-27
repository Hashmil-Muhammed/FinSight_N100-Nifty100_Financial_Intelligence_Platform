import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def generate_pdf_reports():
    """
    Automated PDF Report Generator
    Generates Company Tearsheets and Portfolio Summary PDFs.
    """
    print(" PDF Report Generator ...")

    # 1. SETUP DIRECTORIES
    root_path = Path(__file__).resolve().parents[2]
    db_path = os.path.join(root_path, "nifty100.db")

    reports_dir = os.path.join(root_path, "reports")
    tearsheets_dir = os.path.join(reports_dir, "tearsheets")
    portfolio_dir = os.path.join(reports_dir, "portfolio")
    temp_dir = os.path.join(reports_dir, "temp_charts")

    for directory in [tearsheets_dir, portfolio_dir, temp_dir]:
        os.makedirs(directory, exist_ok=True)

    if not os.path.exists(db_path):
        db_path = os.path.join(root_path, "data", "nifty100.db")

    # 2. LOAD DATA
    try:
        conn = sqlite3.connect(db_path)
        df_pl = pd.read_sql("SELECT * FROM profitandloss", conn)
        df_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
        conn.close()
        print(" Successfully loaded database tables.")
    except Exception as e:
        print(f" Error loading data: {e}")
        return

    # --- PERFECT CLEANING HELPER ---
    def clean_id(df):
        if df.empty:
            return df
        df.columns = [str(c).lower().strip() for c in df.columns]
        df = df.loc[:, ~df.columns.duplicated()]

        priority_cols = ["company_id", "symbol", "ticker", "company", "cid", "id"]
        id_col = next((c for c in priority_cols if c in df.columns), df.columns[0])

        if "company_id" in df.columns and id_col != "company_id":
            df = df.drop(columns=["company_id"])

        df.rename(columns={id_col: "company_id"}, inplace=True)
        df = df.loc[:, ~df.columns.duplicated()]

        if isinstance(df["company_id"], pd.DataFrame):
            df["company_id"] = df["company_id"].iloc[:, 0]

        df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()
        return df

    df_pl = clean_id(df_pl)
    df_ratios = clean_id(df_ratios)

    # 3. IDENTIFY TARGET COLUMNS EXACTLY
    sales_col = next(
        (c for c in df_pl.columns if c in ["sales", "revenue"]),
        next((c for c in df_pl.columns if "sales" in c), None),
    )
    pat_col = next(
        (c for c in df_pl.columns if c in ["net_profit", "pat"]),
        next((c for c in df_pl.columns if "profit" in c), None),
    )

    roe_col = next(
        (c for c in df_ratios.columns if c == "roe"),
        next((c for c in df_ratios.columns if "roe" in c), None),
    )
    roce_col = next(
        (c for c in df_ratios.columns if c == "roce"),
        next((c for c in df_ratios.columns if "roce" in c), None),
    )
    de_col = next(
        (c for c in df_ratios.columns if c in ["d_e", "debt_equity"]),
        next((c for c in df_ratios.columns if "debt" in c), None),
    )
    opm_col = next(
        (c for c in df_ratios.columns if c == "opm"),
        next((c for c in df_ratios.columns if "opm" in c), None),
    )

    # FORCE NUMERIC CONVERSION to remove string-based 'NaN's
    for df, cols in [
        (df_pl, [sales_col, pat_col]),
        (df_ratios, [roe_col, roce_col, de_col, opm_col]),
    ]:
        for c in cols:
            if c and c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")

    valid_companies = [
        c for c in df_pl["company_id"].unique() if not c.isnumeric() and c != "NAN"
    ]
    companies = (
        valid_companies[:3]
        if len(valid_companies) >= 3
        else df_pl["company_id"].unique()[:3]
    )

    print(f" Generating Tearsheets for {len(companies)} companies (Test Batch)...")

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.alignment = 1

    def safe_fmt(val, is_pct=False):
        if pd.isna(val):
            return "N/A"
        return f"{round(float(val), 2)}%" if is_pct else str(round(float(val), 2))

    # 8.1 GENERATE COMPANY TEARSHEETS
    for company in companies:
        pdf_path = os.path.join(tearsheets_dir, f"{company}_tearsheet.pdf")
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []

        elements.append(Paragraph(f"Financial Tearsheet: {company}", title_style))
        elements.append(Spacer(1, 20))

        company_pl = df_pl[df_pl["company_id"] == company].sort_values("year")

        # Filter out rows where all KPI metrics are completely NaN for this company before picking the latest
        company_ratios = df_ratios[df_ratios["company_id"] == company]
        company_ratios_clean = company_ratios.dropna(
            subset=[roe_col, roce_col, de_col], how="all"
        ).sort_values("year", ascending=False)

        # Chart Generation
        if sales_col and pat_col and not company_pl.empty:
            plt.figure(figsize=(6, 4))
            years = company_pl["year"].astype(str).tolist()
            sales = company_pl[sales_col].fillna(0).tolist()
            pat = company_pl[pat_col].fillna(0).tolist()

            x = range(len(years))
            plt.bar(
                x, sales, width=0.4, label="Revenue", color="#1f77b4", align="center"
            )
            plt.bar(
                [i + 0.4 for i in x],
                pat,
                width=0.4,
                label="Net Profit",
                color="#2ca02c",
                align="center",
            )
            plt.xticks([i + 0.2 for i in x], years, rotation=45)
            plt.title(f"{company} - Revenue & Profit Trend")
            plt.legend()
            plt.tight_layout()

            chart_path = os.path.join(temp_dir, f"{company}_chart.png")
            plt.savefig(chart_path)
            plt.close()

            elements.append(Image(chart_path, width=400, height=250))
            elements.append(Spacer(1, 20))

        # KPI Table
        if not company_ratios_clean.empty:
            latest = company_ratios_clean.iloc[0]
            elements.append(
                Paragraph(
                    "Key Performance Indicators (Latest Valid Year)", styles["Heading2"]
                )
            )

            data = [
                ["Metric", "Value"],
                ["Return on Equity (ROE)", safe_fmt(latest.get(roe_col), True)],
                ["Return on Capital (ROCE)", safe_fmt(latest.get(roce_col), True)],
                ["Debt to Equity (D/E)", safe_fmt(latest.get(de_col), False)],
                ["Operating Margin (OPM)", safe_fmt(latest.get(opm_col), True)],
            ]

            t = Table(data, colWidths=[200, 100])
            t.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            elements.append(t)

        doc.build(elements)
        print(f"📄 Generated Tearsheet: {company}_tearsheet.pdf")

    # 8.2 GENERATE PORTFOLIO SUMMARY
    print("\n Generating Portfolio Summary PDF...")
    date_str = datetime.now().strftime("%Y%m%d")
    summary_pdf = os.path.join(portfolio_dir, f"portfolio_summary_{date_str}.pdf")
    doc_sum = SimpleDocTemplate(summary_pdf, pagesize=letter)
    sum_elements = []

    sum_elements.append(Paragraph("Nifty 100 - Portfolio Summary Report", title_style))
    sum_elements.append(Spacer(1, 20))

    # Drop rows where KPIs are entirely NaN before grabbing the latest year per company
    df_ratios_clean = df_ratios.dropna(subset=[roe_col, roce_col, de_col], how="all")
    latest_ratios = df_ratios_clean.sort_values(
        "year", ascending=False
    ).drop_duplicates(subset=["company_id"])

    table_data = [["Company ID", "ROE (%)", "ROCE (%)", "D/E Ratio"]]

    for _, row in latest_ratios.head(25).iterrows():
        table_data.append(
            [
                str(row["company_id"]),
                safe_fmt(row.get(roe_col), True),
                safe_fmt(row.get(roce_col), True),
                safe_fmt(row.get(de_col), False),
            ]
        )

    t_sum = Table(table_data, colWidths=[150, 100, 100, 100])
    t_sum.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )

    sum_elements.append(t_sum)
    doc_sum.build(sum_elements)
    print(f" Generated Portfolio Summary: portfolio_summary_{date_str}.pdf")
    print("\nComplete! Clean PDFs successfully saved.")


if __name__ == "__main__":
    generate_pdf_reports()
