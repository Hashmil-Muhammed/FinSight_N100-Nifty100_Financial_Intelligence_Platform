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


def generate_sector_and_screener_reports():
    """
    Automated PDF Report Generator
    Generates Sector Reports  and Screener Output Reports
    """
    print(" Sector & Screener PDFs ...")

    # 1. SETUP DIRECTORIES
    root_path = Path(__file__).resolve().parents[2]
    db_path = os.path.join(root_path, "nifty100.db")

    reports_dir = os.path.join(root_path, "reports")
    sector_dir = os.path.join(reports_dir, "sector")
    screener_dir = os.path.join(reports_dir, "screener")
    temp_dir = os.path.join(reports_dir, "temp_charts")
    output_dir = os.path.join(root_path, "output")

    for directory in [sector_dir, screener_dir, temp_dir, output_dir]:
        os.makedirs(directory, exist_ok=True)

    if not os.path.exists(db_path):
        db_path = os.path.join(root_path, "data", "nifty100.db")

    # 2. LOAD DATA
    try:
        conn = sqlite3.connect(db_path)
        df_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='sectors';"
        )
        if cursor.fetchone():
            df_sectors = pd.read_sql("SELECT * FROM sectors", conn)
        else:
            df_sectors = pd.DataFrame()

        conn.close()
        print(" Successfully loaded database tables.")
    except Exception as e:
        print(f" Error loading data: {e}")
        return

    # HELPER to clean DataFrames safely
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

    df_ratios = clean_id(df_ratios)
    df_sectors = clean_id(df_sectors)

    # CRITICAL FIX FOR MISSING DATA & PARSE ERRORS
    roe_col = next(
        (c for c in df_ratios.columns if c == "roe"),
        next((c for c in df_ratios.columns if "roe" in c), None),
    )
    de_col = next(
        (c for c in df_ratios.columns if c in ["d_e", "debt_equity"]),
        next((c for c in df_ratios.columns if "debt" in c), None),
    )
    opm_col = next(
        (c for c in df_ratios.columns if c == "opm"),
        next((c for c in df_ratios.columns if "opm" in c), None),
    )

    # Convert to numeric immediately to filter out completely blank rows
    for c in [roe_col, de_col, opm_col]:
        if c:
            df_ratios[c] = pd.to_numeric(df_ratios[c], errors="coerce")

    # Drop rows where ALL key metrics are NaN
    cols_to_check = [x for x in [roe_col, de_col, opm_col] if x]
    if cols_to_check:
        df_ratios_clean = df_ratios.dropna(subset=cols_to_check, how="all").copy()
    else:
        df_ratios_clean = df_ratios.copy()

    # Handle the 'PARSE_ERROR' in year by replacing it with '0000' so valid years sort higher
    if "year" in df_ratios_clean.columns:
        df_ratios_clean["year"] = (
            df_ratios_clean["year"].astype(str).replace("PARSE_ERROR", "0000")
        )
        df_ratios_clean = df_ratios_clean.sort_values(
            by=["company_id", "year"], ascending=[True, False]
        )

    latest_ratios = df_ratios_clean.drop_duplicates(
        subset=["company_id"], keep="first"
    ).copy()

    if latest_ratios.empty:
        print(
            " Error: No valid data found in financial_ratios after removing empty rows."
        )
        return

    sector_col = (
        next((c for c in df_sectors.columns if "sector" in c or "industry" in c), None)
        if not df_sectors.empty
        else None
    )

    if sector_col and not df_sectors.empty:
        df_merged = pd.merge(
            latest_ratios,
            df_sectors[["company_id", sector_col]],
            on="company_id",
            how="left",
        )
    else:
        df_merged = latest_ratios.copy()
        sector_col = "sector"
        df_merged[sector_col] = "General Sector"

    df_merged[sector_col] = df_merged[sector_col].fillna("Unknown Sector")

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.alignment = 1
    date_str = datetime.now().strftime("%Y%m%d")

    def safe_fmt(val, is_pct=False):
        if pd.isna(val):
            return "N/A"
        try:
            return f"{round(float(val), 2)}%" if is_pct else str(round(float(val), 2))
        except:
            return "N/A"

    # 8.3 GENERATE SECTOR REPORTS
    print("\n Generating Sector Reports...")
    sectors = df_merged[sector_col].unique()
    sector_count = 0

    for sector in sectors:
        sector_safe_name = (
            str(sector).replace("/", "_").replace("&", "and").replace(" ", "_")
        )
        pdf_path = os.path.join(sector_dir, f"{sector_safe_name}_report_{date_str}.pdf")

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []

        elements.append(Paragraph(f"Sector Intelligence Report: {sector}", title_style))
        elements.append(Spacer(1, 20))

        sector_data = df_merged[df_merged[sector_col] == sector]

        if roe_col and de_col and not sector_data.empty:
            median_roe = sector_data[roe_col].median()
            median_de = sector_data[de_col].median()

            valid_roe_data = sector_data.dropna(subset=[roe_col])
            best_co = (
                valid_roe_data.loc[valid_roe_data[roe_col].idxmax()]
                if not valid_roe_data.empty
                else None
            )
            worst_co = (
                valid_roe_data.loc[valid_roe_data[roe_col].idxmin()]
                if not valid_roe_data.empty
                else None
            )

            elements.append(Paragraph("Sector Median KPIs", styles["Heading2"]))
            median_table = [
                ["Metric", "Sector Median"],
                ["Median ROE", safe_fmt(median_roe, True)],
                ["Median D/E", safe_fmt(median_de, False)],
            ]

            t1 = Table(median_table, colWidths=[200, 150])
            t1.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (1, 0), colors.darkcyan),
                        ("TEXTCOLOR", (0, 0), (1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.aliceblue),
                    ]
                )
            )
            elements.append(t1)
            elements.append(Spacer(1, 20))

            if best_co is not None and worst_co is not None:
                elements.append(
                    Paragraph(
                        "Performance Highlights (Based on ROE)", styles["Heading2"]
                    )
                )
                highlight_table = [
                    ["Category", "Company", "ROE"],
                    [
                        " Top Performer",
                        str(best_co["company_id"]),
                        safe_fmt(best_co[roe_col], True),
                    ],
                    [
                        " Lowest Performer",
                        str(worst_co["company_id"]),
                        safe_fmt(worst_co[roe_col], True),
                    ],
                ]
                t2 = Table(highlight_table, colWidths=[150, 100, 100])
                t2.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                            ("TEXTCOLOR", (0, 1), (0, 1), colors.green),
                            ("TEXTCOLOR", (0, 2), (0, 2), colors.red),
                        ]
                    )
                )
                elements.append(t2)

        doc.build(elements)
        print(f" Generated Sector Report: {sector_safe_name}_report.pdf")
        sector_count += 1

    if sector_count == 0:
        print(" No sectors found to generate reports.")

    # 8.4 GENERATE SCREENER OUTPUT REPORT
    print("\n Generating Screener Output Report...")
    screener_files = [
        os.path.join(root_path, "output", "screener_output.xlsx"),
        os.path.join(root_path, "screener_output.xlsx"),
    ]

    screener_file = next((f for f in screener_files if os.path.exists(f)), None)
    df_screen = pd.DataFrame()

    if screener_file:
        temp_screen = clean_id(pd.read_excel(screener_file))
        if (
            "year" in temp_screen.columns
            and temp_screen["year"]
            .astype(str)
            .str.contains("PARSE", case=False, na=False)
            .any()
        ):
            print(
                " Existing Screener file has PARSE_ERRORs. Regenerating clean data..."
            )
        else:
            df_screen = temp_screen

    # Re-generate if empty or corrupt
    if df_screen.empty:
        df_screen = df_merged.copy()
        df_screen["composite_score"] = (
            pd.to_numeric(df_screen[roe_col], errors="coerce").fillna(0)
            + pd.to_numeric(df_screen[opm_col], errors="coerce").fillna(0)
            - (pd.to_numeric(df_screen[de_col], errors="coerce").fillna(0) * 10)
        )
        comp_col = "composite_score"

        save_path = os.path.join(output_dir, "screener_output.xlsx")

        # Ensure we drop the helper column before saving
        if "year" in df_screen.columns:
            df_screen["year"] = df_screen["year"].replace("0000", "Unknown")

        df_screen.to_excel(save_path, index=False)
        print(f" Cleaned Screener Data saved to: {save_path}")
    else:
        comp_col = next(
            (c for c in df_screen.columns if "composite" in c or "score" in c), None
        )

    if comp_col and not df_screen.empty:
        df_screen = df_screen.sort_values(by=comp_col, ascending=False).head(10)

        screener_pdf = os.path.join(screener_dir, f"screener_results_{date_str}.pdf")
        doc_screen = SimpleDocTemplate(screener_pdf, pagesize=letter)
        scr_elements = []

        scr_elements.append(
            Paragraph("Screener Output Report - Top 10 Ranked Companies", title_style)
        )
        scr_elements.append(Spacer(1, 20))

        plt.figure(figsize=(7, 4))
        companies = df_screen["company_id"].astype(str).tolist()
        scores = pd.to_numeric(df_screen[comp_col], errors="coerce").fillna(0).tolist()

        plt.bar(companies, scores, color="purple")
        plt.xticks(rotation=45)
        plt.title("Top 10 Companies by Composite Score")
        plt.ylabel("Score")
        plt.tight_layout()

        chart_path = os.path.join(temp_dir, "screener_top10.png")
        plt.savefig(chart_path)
        plt.close()

        scr_elements.append(Image(chart_path, width=450, height=250))
        scr_elements.append(Spacer(1, 20))

        table_data = [["Rank", "Company ID", "Composite Score"]]
        for i, row in enumerate(df_screen.iterrows(), 1):
            _, r = row
            table_data.append(
                [str(i), str(r["company_id"]), safe_fmt(r[comp_col], False)]
            )

        t3 = Table(table_data, colWidths=[50, 150, 150])
        t3.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.indigo),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
        )
        scr_elements.append(t3)

        doc_screen.build(scr_elements)
        print(f" Generated Screener Report: screener_results_{date_str}.pdf")
    else:
        print(
            " Error: Could not generate Screener PDF (Missing Composite Score or empty data)."
        )

    print("\nComplete! Sector & Screener Reports saved to 'reports/' directory.")


if __name__ == "__main__":
    generate_sector_and_screener_reports()
