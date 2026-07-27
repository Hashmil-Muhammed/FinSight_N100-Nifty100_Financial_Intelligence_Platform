import pandas as pd
import numpy as np
import sqlite3
import os
from pathlib import Path
import plotly.express as px


def generate_correlation_and_outliers():
    """
    Statistical Analysis & Clustering
    1. Generates Pearson correlation matrix (heatmap) for 10 KPIs.
    2. Detects outliers using Z-scores per metric per sector.
    """
    print("  Correlation & Outliers...")

    root_path = Path(__file__).resolve().parents[2]
    outlier_file = os.path.join(root_path, "outlier_report.csv")
    heatmap_file = os.path.join(root_path, "correlation_heatmap.png")
    db_path = os.path.join(root_path, "nifty100.db")

    if not os.path.exists(db_path):
        db_path = os.path.join(root_path, "data", "nifty100.db")

    # 1. LOAD DATA
    try:
        conn = sqlite3.connect(db_path)
        print(" Reading 'financial_ratios' and 'sectors' tables from database...")
        df_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
        df_sectors = pd.read_sql("SELECT * FROM sectors", conn)
        conn.close()
    except Exception as e:
        print(f" Error reading database: {e}")
        return

    # --- BULLETPROOF CLEANING HELPER ---
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

        if isinstance(df["company_id"], pd.DataFrame):
            df["company_id"] = df["company_id"].iloc[:, 0]

        df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()
        return df

    df_ratios = clean_df(df_ratios)
    df_sectors = clean_df(df_sectors)

    # Get latest year for ratios
    if "year" in df_ratios.columns:
        df_ratios = df_ratios.sort_values(
            by=["company_id", "year"], ascending=[True, False]
        )
    df_latest = df_ratios.drop_duplicates(subset=["company_id"], keep="first")

    # Merge ratios with sectors
    sector_col = next(
        (c for c in df_sectors.columns if "sector" in c or "industry" in c), None
    )
    if sector_col:
        df_merged = pd.merge(
            df_latest,
            df_sectors[["company_id", sector_col]],
            on="company_id",
            how="left",
        )
    else:
        print(" Warning: Sector column not found in sectors table. Using 'Unknown'.")
        df_merged = df_latest.copy()
        sector_col = "sector"
        df_merged[sector_col] = "Unknown"

    df_merged[sector_col] = df_merged[sector_col].fillna("Unknown")

    # 2. SELECT 10 KPIs FOR CORRELATION
    possible_kpis = [
        "roe",
        "roce",
        "d_e",
        "npm",
        "opm",
        "icr",
        "asset_turnover",
        "revenue_cagr_3y",
        "pat_cagr_3y",
        "eps_cagr_3y",
    ]
    actual_kpis = [col for col in possible_kpis if col in df_merged.columns]

    # If we don't have exactly 10, grab other numeric columns to make it 10
    if len(actual_kpis) < 10:
        numeric_cols = df_merged.select_dtypes(include=[np.number]).columns.tolist()
        for col in numeric_cols:
            if col not in actual_kpis and col not in ["year", "id", "company_id"]:
                actual_kpis.append(col)
            if len(actual_kpis) == 10:
                break

    print(f" Selected {len(actual_kpis)} KPIs for analysis.")

    # Ensure all selected columns are numeric
    for col in actual_kpis:
        df_merged[col] = pd.to_numeric(df_merged[col], errors="coerce")

    # 10.4: OUTLIER DETECTION (Z-SCORE PER SECTOR)
    print(" Detecting Outliers (|Z| > 3) per sector...")
    outliers_list = []

    for metric in actual_kpis:
        # Calculate mean and std per sector for this metric
        sector_stats = (
            df_merged.groupby(sector_col)[metric].agg(["mean", "std"]).reset_index()
        )

        # Merge stats back to the main dataframe
        temp_df = pd.merge(
            df_merged[["company_id", sector_col, metric]],
            sector_stats,
            on=sector_col,
            how="left",
        )

        # Calculate Z-score: (Value - Mean) / Std
        # Adding 1e-9 to prevent division by zero errors
        temp_df["z_score"] = (temp_df[metric] - temp_df["mean"]) / (
            temp_df["std"] + 1e-9
        )

        # Filter where |Z| > 3 (Extremely high or low compared to sector peers)
        outliers = temp_df[temp_df["z_score"].abs() > 3].copy()

        for _, row in outliers.iterrows():
            outliers_list.append(
                {
                    "company_id": row["company_id"],
                    "sector": row[sector_col].title(),
                    "metric": metric.upper(),
                    "value": round(row[metric], 2),
                    "sector_mean": round(row["mean"], 2),
                    "sector_std": round(row["std"], 2),
                    "z_score": round(row["z_score"], 2),
                    "flag": "Outlier ",
                }
            )

    df_outliers = pd.DataFrame(outliers_list)

    if not df_outliers.empty:
        df_outliers.to_csv(outlier_file, index=False)
        print(f" Found {len(df_outliers)} Outliers! Saved to {outlier_file}")
    else:
        # Create empty file with headers if no outliers found
        pd.DataFrame(
            columns=[
                "company_id",
                "sector",
                "metric",
                "value",
                "sector_mean",
                "sector_std",
                "z_score",
                "flag",
            ]
        ).to_csv(outlier_file, index=False)
        print(
            f" No extreme outliers (|Z|>3) found. Clean report saved to {outlier_file}"
        )

    # 10.3: CORRELATION MATRIX HEATMAP
    print("⚙️ Generating Pearson Correlation Heatmap...")
    # Calculate Pearson correlation
    corr_matrix = df_merged[actual_kpis].corr(method="pearson")

    # Create Heatmap using Plotly
    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",  # Red-Blue color scale
        title="Pearson Correlation Matrix of Key Financial Metrics (Nifty 100)",
    )

    # Export to PNG image
    try:
        # Requires kaleido installed via requirements.txt
        fig.write_image(heatmap_file, width=1000, height=800, scale=2)
        print(f" Correlation Heatmap saved as Image: {heatmap_file}\n")
    except Exception:
        print(
            " Could not save as PNG (Kaleido issue). Saving as Interactive HTML instead..."
        )
        html_file = heatmap_file.replace(".png", ".html")
        fig.write_html(html_file)
        print(f" Interactive Heatmap saved to: {html_file}\n")


if __name__ == "__main__":
    generate_correlation_and_outliers()
