import pandas as pd
import numpy as np
import sqlite3
import os
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def run_kmeans_clustering():
    """
    Statistical Analysis & Clustering
    Applies StandardScaler and KMeans(n=5) on features:
    ROE, D/E, Revenue CAGR, FCF CAGR, OPM.
    Uses the elbow method to validate K and exports cluster_labels.csv
    """
    print(" KMeans Clustering - Machine Learning...")

    # 1. SETUP PATHS
    root_path = Path(__file__).resolve().parents[2]
    db_path = os.path.join(root_path, "nifty100.db")
    cf_excel_path = os.path.join(root_path, "cashflow_intelligence.xlsx")
    output_csv = os.path.join(root_path, "cluster_labels.csv")
    elbow_plot = os.path.join(root_path, "reports", "elbow_method_plot.png")

    # Ensure reports directory exists for the plot
    os.makedirs(os.path.join(root_path, "reports"), exist_ok=True)

    if not os.path.exists(db_path):
        db_path = os.path.join(root_path, "data", "nifty100.db")

    # 2. LOAD REQUIRED DATA
    try:
        # Load Financial Ratios for ROE, D/E, OPM, Revenue CAGR
        conn = sqlite3.connect(db_path)
        df_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
        conn.close()

        # Load Cashflow Intelligence for FCF CAGR
        if not os.path.exists(cf_excel_path):
            print(f" Error: {cf_excel_path} not found. Required for FCF CAGR.")
            return
        df_cf = pd.read_excel(cf_excel_path)
        print(" Successfully loaded database and cashflow intelligence data!")
    except Exception as e:
        print(f" Error loading data: {e}")
        return

    # 3. CLEAN AND MERGE DATA
    # Helper to clean column names and IDs safely
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
        df = df.loc[:, ~df.columns.duplicated()]

        if isinstance(df["company_id"], pd.DataFrame):
            df["company_id"] = df["company_id"].iloc[:, 0]

        df["company_id"] = df["company_id"].astype(str).str.strip().str.upper()
        return df

    df_ratios = clean_id(df_ratios)

    # Extract latest year data from ratios
    if "year" in df_ratios.columns:
        df_ratios = df_ratios.sort_values(
            by=["company_id", "year"], ascending=[True, False]
        )
    df_ratios = df_ratios.drop_duplicates(subset=["company_id"], keep="first")

    df_cf = clean_id(df_cf)

    # Merge Ratios and Cashflow Data
    df_merged = pd.merge(df_ratios, df_cf, on="company_id", how="left")

    # 4. FEATURE ENGINEERING & EXTRACTION
    # Dynamically identify the exact column names
    roe_col = next((c for c in df_merged.columns if "roe" in c), None)
    de_col = next(
        (c for c in df_merged.columns if "d_e" in c or "debt_equity" in c), None
    )
    opm_col = next((c for c in df_merged.columns if "opm" in c), None)

    # Catch any revenue/sales cagr column
    rev_cagr_col = next(
        (c for c in df_merged.columns if "revenue_cagr" in c or "sales_growth" in c),
        None,
    )

    # Catch FCF CAGR
    fcf_cagr_col = next(
        (c for c in df_merged.columns if "fcf cagr" in c or "fcf_cagr" in c), None
    )

    # If any required column is completely missing, create a dummy one with zeros to prevent ML crash
    for col_name, var_name in [
        ("ROE", roe_col),
        ("D/E", de_col),
        ("OPM", opm_col),
        ("Rev CAGR", rev_cagr_col),
        ("FCF CAGR", fcf_cagr_col),
    ]:
        if not var_name:
            print(
                f" Warning: {col_name} not found. Injecting default 0.0 values to proceed."
            )
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

    print("⚙️ Preprocessing Features for ML Algorithm (Handling NaNs & Infs)...")
    feature_cols = [roe_col, de_col, opm_col, rev_cagr_col, fcf_cagr_col]
    features_df = df_merged[["company_id"] + feature_cols].copy()

    # Custom parser for string-based CAGR columns (e.g., handling "Turnaround ")
    def parse_mixed_numeric(val):
        if pd.isna(val):
            return np.nan
        val = str(val).strip()
        if "%" in val:
            return float(val.replace("%", ""))
        if "Turnaround" in val:
            return 15.0  # Proxy positive growth
        if "Negative" in val:
            return -10.0  # Proxy negative growth
        if "Insufficient" in val or "N/A" in val:
            return np.nan
        try:
            return float(val)
        except ValueError:
            return np.nan

    # Apply parser safely
    features_df[fcf_cagr_col] = features_df[fcf_cagr_col].apply(parse_mixed_numeric)
    features_df[rev_cagr_col] = features_df[rev_cagr_col].apply(parse_mixed_numeric)

    # Replace Infinity values with NaN
    features_df = features_df.replace([np.inf, -np.inf], np.nan)

    # Impute Missing Values (NaN) Safely
    for col in feature_cols:
        features_df[col] = pd.to_numeric(features_df[col], errors="coerce")
        median_val = features_df[col].median()

        # If the entire column is NaN, median() returns NaN. Fallback to 0.0
        if pd.isna(median_val):
            median_val = 0.0

        features_df[col] = features_df[col].fillna(median_val)

    # 5. DATA SCALING (StandardScaler)
    # ML models require features to be on the same scale (Mean=0, Variance=1)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(features_df[feature_cols])

    # 6. ELBOW METHOD VALIDATION
    print(" Generating Elbow Method Plot to validate K=5...")
    wcss = []

    # Cap the max clusters to the number of available samples or 10
    max_clusters = min(11, len(scaled_data) + 1)

    for i in range(1, max_clusters):
        kmeans_test = KMeans(n_clusters=i, init="k-means++", random_state=42, n_init=10)
        kmeans_test.fit(scaled_data)
        wcss.append(kmeans_test.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, max_clusters), wcss, marker="o", linestyle="--", color="b")
    plt.title("Elbow Method For Optimal k")
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("WCSS (Within-Cluster Sum of Square)")

    if max_clusters > 5:
        plt.axvline(x=5, color="r", linestyle="--", label="Selected k=5")

    plt.legend()
    plt.grid(True)
    plt.savefig(elbow_plot)
    plt.close()
    print(f" Elbow plot saved to: {elbow_plot}")

    # 7. KMEANS CLUSTERING (k=5)
    print(" Applying KMeans Clustering (k=5)...")
    # Using 5 clusters as specified in the sprint document
    n_clusters = min(5, len(scaled_data))  # Fallback if less than 5 companies exist

    kmeans = KMeans(n_clusters=n_clusters, init="k-means++", random_state=42, n_init=10)
    clusters = kmeans.fit_predict(scaled_data)

    # Calculate distance from centroid for each data point
    centroids = kmeans.cluster_centers_
    distances = [
        np.linalg.norm(scaled_data[i] - centroids[clusters[i]])
        for i in range(len(scaled_data))
    ]

    # 8. PREPARE OUTPUT
    results_df = pd.DataFrame(
        {
            "company_id": features_df["company_id"],
            "cluster_id": clusters,
            "cluster_name": "Pending Profile",  # Will be updated
            "distance_from_centroid": [round(d, 4) for d in distances],
        }
    )

    # Sort by cluster_id for readability
    results_df = results_df.sort_values(by="cluster_id").reset_index(drop=True)

    results_df.to_csv(output_csv, index=False)

    print(f"\n Complete! ML Clustering done for {len(results_df)} companies.")
    print(f" Results saved to: {output_csv}\n")

    print(" SAMPLE OUTPUT:")
    print(results_df.head(8).to_string(index=False))


if __name__ == "__main__":
    run_kmeans_clustering()
