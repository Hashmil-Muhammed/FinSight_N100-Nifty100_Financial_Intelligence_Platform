import pandas as pd
import sqlite3
import os
from pathlib import Path


def run_cluster_profiling():
    """
    Statistical Analysis & Clustering
    Analyzes the mean of features per cluster and assigns descriptive labels:
    High-Quality Growth, Emerging Growth, Defensive Dividend, Value Cyclicals, Distressed.
    Updates the cluster_labels.csv file.
    """
    print(" Cluster Profiling...")

    # 1. SETUP PATHS
    root_path = Path(__file__).resolve().parents[2]
    db_path = os.path.join(root_path, "nifty100.db")
    cf_excel_path = os.path.join(root_path, "cashflow_intelligence.xlsx")
    cluster_csv = os.path.join(root_path, "cluster_labels.csv")

    if not os.path.exists(cluster_csv):
        print(f" Error: {cluster_csv} not found.")
        return

    # 2. LOAD DATA
    try:
        # Load Cluster Labels from T
        df_clusters = pd.read_csv(cluster_csv)
        df_clusters["company_id"] = (
            df_clusters["company_id"].astype(str).str.strip().str.upper()
        )

        # Load Financial Ratios
        conn = sqlite3.connect(
            db_path
            if os.path.exists(db_path)
            else os.path.join(root_path, "data", "nifty100.db")
        )
        df_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
        conn.close()

        # Load Cashflow Intelligence
        df_cf = pd.read_excel(cf_excel_path)
        print(" Successfully loaded clusters, database, and cashflow data!")
    except Exception as e:
        print(f" Error loading data: {e}")
        return

    # 3. CLEAN AND PREPARE FEATURES
    def clean_id(df):
        if df.empty:
            return df
        df.columns = [str(c).lower().strip() for c in df.columns]
        df = df.loc[:, ~df.columns.duplicated()]
        id_col = next(
            (
                c
                for c in df.columns
                if c in ["id", "company_id", "cid", "company", "symbol"]
            ),
            df.columns[0],
        )

        if "company_id" in df.columns and id_col != "company_id":
            df = df.drop(columns=["company_id"])

        df.rename(columns={id_col: "company_id"}, inplace=True)
        if isinstance(df["company_id"], pd.DataFrame):
            df["company_id"] = df["company_id"].iloc[:, 0]
        df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()
        return df

    df_ratios = clean_id(df_ratios)
    if "year" in df_ratios.columns:
        df_ratios = df_ratios.sort_values(
            by=["company_id", "year"], ascending=[True, False]
        )
    df_ratios = df_ratios.drop_duplicates(subset=["company_id"], keep="first")

    df_cf = clean_id(df_cf)

    # Merge Clusters with Features
    df_merged = pd.merge(df_clusters, df_ratios, on="company_id", how="left")
    df_merged = pd.merge(df_merged, df_cf, on="company_id", how="left")

    # Identify Features Dynamically
    roe_col = next((c for c in df_merged.columns if "roe" in c), None)
    de_col = next(
        (c for c in df_merged.columns if "d_e" in c or "debt_equity" in c), None
    )
    opm_col = next((c for c in df_merged.columns if "opm" in c), None)
    rev_cagr_col = next(
        (c for c in df_merged.columns if "revenue_cagr" in c or "sales_growth" in c),
        None,
    )
    fcf_cagr_col = next(
        (c for c in df_merged.columns if "fcf cagr" in c or "fcf_cagr" in c), None
    )

    # Setup defaults for missing columns
    for col_name, var_name in [
        ("ROE", roe_col),
        ("D/E", de_col),
        ("OPM", opm_col),
        ("Rev CAGR", rev_cagr_col),
        ("FCF CAGR", fcf_cagr_col),
    ]:
        if not var_name:
            dummy_name = f"dummy_{col_name.lower()}"
            df_merged[dummy_name] = 0.0
            if col_name == "ROE":
                roe_col = dummy_name
            elif col_name == "D/E":
                de_col = dummy_name
            elif col_name == "OPM":
                opm_col = dummy_name
            elif col_name == "Rev CAGR":
                rev_cagr_col = dummy_name
            elif col_name == "FCF CAGR":
                fcf_cagr_col = dummy_name

    def parse_mixed_numeric(val):
        if pd.isna(val):
            return 0.0
        val = str(val).strip()
        if "%" in val:
            return float(val.replace("%", ""))
        if "Turnaround" in val:
            return 15.0
        if "Negative" in val:
            return -10.0
        if "Insufficient" in val or "N/A" in val:
            return 0.0
        try:
            return float(val)
        except ValueError:
            return 0.0

    df_merged[fcf_cagr_col] = df_merged[fcf_cagr_col].apply(parse_mixed_numeric)
    df_merged[rev_cagr_col] = df_merged[rev_cagr_col].apply(parse_mixed_numeric)

    feature_cols = [roe_col, de_col, opm_col, rev_cagr_col, fcf_cagr_col]
    for col in feature_cols:
        df_merged[col] = pd.to_numeric(df_merged[col], errors="coerce").fillna(0)

    # 4. CLUSTER PROFILING & LABEL ASSIGNMENT
    print("⚙️ Analyzing Cluster Profiles to assign Business Labels...")

    # Calculate the mean of features for each cluster
    cluster_profiles = (
        df_merged.groupby("cluster_id")[feature_cols].mean().reset_index()
    )

    # Calculate a custom "Health Score" to rank clusters from Best to Worst
    # Formula: ROE + OPM + Rev_CAGR - (Debt_Equity * 20)
    cluster_profiles["health_score"] = (
        cluster_profiles[roe_col]
        + cluster_profiles[opm_col]
        + cluster_profiles[rev_cagr_col]
        - (cluster_profiles[de_col] * 20)
    )

    # Sort clusters by health score descending (Rank 1 is best)
    ranked_clusters = cluster_profiles.sort_values(by="health_score", ascending=False)[
        "cluster_id"
    ].tolist()

    # Map the 5 specific labels based on the ranking
    # To handle cases with fewer than 5 clusters gracefully
    labels_ordered = [
        "High-Quality Growth",  # Best Financial Profile
        "Emerging Growth",  # Second Best
        "Defensive Dividend",  # Moderate / Stable
        "Value Cyclicals",  # Lower Quality / High Debt
        "Distressed",  # Worst Financial Profile
    ]

    label_mapping = {}
    for i, cid in enumerate(ranked_clusters):
        label_mapping[cid] = (
            labels_ordered[i] if i < len(labels_ordered) else "Unknown Profile"
        )

    # Assign new labels back to the dataframe
    df_clusters["cluster_name"] = df_clusters["cluster_id"].map(label_mapping)

    # 5. SAVE AND DISPLAY REPORT
    df_clusters.to_csv(cluster_csv, index=False)

    print(
        f"\n Complete! Assigned descriptive labels to all {len(df_clusters)} companies."
    )
    print(f" Updated labels saved to: {cluster_csv}\n")

    print(" CLUSTER PROFILES (Mean values per group):")
    # Clean up the output table for display
    display_profiles = cluster_profiles.copy()
    display_profiles["Assigned Label"] = display_profiles["cluster_id"].map(
        label_mapping
    )
    display_cols = [
        "cluster_id",
        "Assigned Label",
        roe_col,
        de_col,
        opm_col,
        rev_cagr_col,
        fcf_cagr_col,
    ]

    # Round numerics for clean display
    for col in display_cols[2:]:
        display_profiles[col] = display_profiles[col].round(2)

    print(display_profiles[display_cols].to_string(index=False))


if __name__ == "__main__":
    run_cluster_profiling()
