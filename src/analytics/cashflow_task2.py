import pandas as pd
import sqlite3
import os
from pathlib import Path


def calculate_capex_and_fcf():
    """
    Cash Flow Intelligence
    Calculates CapEx Intensity and FCF Conversion Rate.
    Appends the results to the existing cashflow_intelligence.xlsx file.
    """
    print(" Cash Flow Intelligence - (CapEx & FCF)...")

    root_path = Path(__file__).resolve().parents[2]
    output_file = os.path.join(root_path, "cashflow_intelligence.xlsx")

    db_path = os.path.join(root_path, "nifty100.db")
    if not os.path.exists(db_path):
        db_path = os.path.join(root_path, "data", "nifty100.db")

    # 1. LOAD EXISTING EXCEL FILE
    if not os.path.exists(output_file):
        print(f" Error: {output_file} not found. ")
        return

    try:
        df_existing = pd.read_excel(output_file)
        df_existing["Company ID"] = (
            df_existing["Company ID"].astype(str).str.strip().str.upper()
        )
        print(" Successfully loaded existing cashflow_intelligence.xlsx")
    except Exception as e:
        print(f" Error reading Excel file: {e}")
        return

    # 2. LOAD DB TABLES
    try:
        conn = sqlite3.connect(db_path)
        df_pl = pd.read_sql("SELECT * FROM profitandloss", conn)
        df_cf = pd.read_sql("SELECT * FROM cashflow", conn)
        conn.close()
    except Exception as e:
        print(f" Error reading database: {e}")
        return

    # --- CLEANING HELPER ---
    def clean_df(df):
        df.columns = [str(c).lower().strip() for c in df.columns]
        df = df.loc[:, ~df.columns.duplicated()]

        id_col = next(
            (
                c
                for c in df.columns
                if c in ["id", "company_id", "cid", "company", "symbol"]
            ),
            None,
        )
        id_col = id_col if id_col else df.columns[0]

        if "company_id" in df.columns and id_col != "company_id":
            df = df.drop(columns=["company_id"])

        df.rename(columns={id_col: "company_id"}, inplace=True)
        df = df.loc[:, ~df.columns.duplicated()]

        if isinstance(df["company_id"], pd.DataFrame):
            df["company_id"] = df["company_id"].iloc[:, 0]

        df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()
        return df

    df_pl = clean_df(df_pl)
    df_cf = clean_df(df_cf)

    # 3. SMART COLUMN MATCHERS (FIXED)
    sales_col = next((c for c in df_pl.columns if "sales" in c or "revenue" in c), None)

    # EXACT FIX FOR EBITDA / OPERATING PROFIT
    ebitda_col = next(
        (
            c
            for c in df_pl.columns
            if "operating_profit" in c
            or "ebitda" in c
            or "op_profit" in c
            or ("operating" in c and "profit" in c)
        ),
        None,
    )

    cfo_col = next(
        (
            c
            for c in df_cf.columns
            if "operating" in c or "cfo" in c or "cash_from" in c
        ),
        None,
    )

    # Priority for CapEx: Check for fixed assets first, otherwise fallback to investing activity
    capex_col = None
    for c in df_cf.columns:
        if "capex" in c or "fixed_assets" in c or "capital_expenditure" in c:
            capex_col = c
            break
    if not capex_col:
        capex_col = next((c for c in df_cf.columns if "investing" in c), None)

    if not all([sales_col, ebitda_col, cfo_col, capex_col]):
        print(" Error: Could not find required columns in database.")
        print(
            f"Found -> Sales: {sales_col}, EBITDA: {ebitda_col}, CFO: {cfo_col}, CapEx: {capex_col}"
        )
        return

    print(
        f" Using Columns -> Sales: '{sales_col}', EBITDA: '{ebitda_col}', CFO: '{cfo_col}', CapEx: '{capex_col}'"
    )

    # Merge and Convert to Numeric
    df_merged = pd.merge(
        df_pl[["company_id", "year", sales_col, ebitda_col]],
        df_cf[["company_id", "year", cfo_col, capex_col]],
        on=["company_id", "year"],
        how="inner",
    )

    for col in [sales_col, ebitda_col, cfo_col, capex_col]:
        df_merged[col] = pd.to_numeric(df_merged[col], errors="coerce").fillna(0)

    df_merged = df_merged.sort_values(
        by=["company_id", "year"], ascending=[True, False]
    )

    results = []

    # 4. CALCULATE METRICS
    for company, group in df_merged.groupby("company_id"):
        latest_5 = group.head(5)
        if len(latest_5) == 0:
            continue

        total_sales = latest_5[sales_col].sum()
        total_ebitda = latest_5[ebitda_col].sum()
        total_cfo = latest_5[cfo_col].sum()

        # CapEx is usually negative (outflow), so we take absolute value
        total_capex = abs(latest_5[capex_col].sum())

        # Free Cash Flow = Cash from Operations - CapEx
        fcf = total_cfo - total_capex

        # CapEx Intensity = (CapEx / Revenue) * 100
        capex_intensity = (total_capex / total_sales * 100) if total_sales > 0 else 0

        # FCF Conversion Rate = (FCF / EBITDA) * 100
        fcf_conversion = (fcf / total_ebitda * 100) if total_ebitda > 0 else 0

        # Labels mapping
        if capex_intensity < 3:
            capex_label = " Asset-light (<3%)"
        elif capex_intensity > 8:
            capex_label = " Capital Intensive (>8%)"
        else:
            capex_label = " Average Intensity"

        if fcf_conversion > 60:
            fcf_label = " Efficient (>60%)"
        elif fcf_conversion < 30:
            fcf_label = " CapEx Heavy (<30%)"
        else:
            fcf_label = " Average Conversion"

        results.append(
            {
                "Company ID": company,
                "CapEx Intensity %": round(capex_intensity, 2),
                "CapEx Label": capex_label,
                "FCF Conversion %": round(fcf_conversion, 2),
                "FCF Conversion Label": fcf_label,
            }
        )

    # 5. MERGE WITH EXISTING DATA AND SAVE
    df_new = pd.DataFrame(results)

    if not df_new.empty:
        df_final = pd.merge(df_existing, df_new, on="Company ID", how="left")
        df_final.to_excel(output_file, index=False)

        print(f"\n Complete! Merged new metrics for {len(df_new)} companies.")
        print(f" Report updated at: {output_file}\n")

        print(" SAMPLE UPDATED OUTPUT:")
        cols_to_show = [
            "Company ID",
            "Quality Badge",
            "CapEx Label",
            "FCF Conversion Label",
        ]
        print(df_final[cols_to_show].head(5).to_string(index=False))
    else:
        print(" Could not calculate metrics.")


if __name__ == "__main__":
    calculate_capex_and_fcf()
