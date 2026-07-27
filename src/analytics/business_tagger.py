import pandas as pd
import sqlite3
import os
import re
from pathlib import Path


def tag_business_description():
    """
    Classifies about_company text into sector tags using keyword matching
    and validates against sectors.xlsx (or DB sectors table).
    """
    print(" Starting NLP : Business Description Tagger...")

    root_path = Path(__file__).resolve().parents[2]
    output_file = os.path.join(root_path, "tag_validation_report.csv")

    db_path = os.path.join(root_path, "nifty100.db")
    if not os.path.exists(db_path):
        db_path = os.path.join(root_path, "data", "nifty100.db")

    # 1. LOAD COMPANIES FROM DATABASE (Because analysis.xlsx doesn't have descriptions)
    try:
        conn = sqlite3.connect(db_path)
        df_companies_raw = pd.read_sql("SELECT * FROM companies", conn)
        print(" Successfully loaded 'companies' from database.")
    except Exception as e:
        print(f" Error reading 'companies' from database: {e}")
        return

    # 2. LOAD SECTORS FROM SECTORS.XLSX
    sectors_file_1 = os.path.join(root_path, "data", "raw", "sectors.xlsx")
    sectors_file_2 = os.path.join(root_path, "data", "supporting", "sectors.xlsx")
    sectors_file = sectors_file_1 if os.path.exists(sectors_file_1) else sectors_file_2

    try:
        if os.path.exists(sectors_file):
            df_sectors_raw = pd.read_excel(sectors_file)
            if len(str(df_sectors_raw.columns[0])) > 30:
                df_sectors_raw = pd.read_excel(sectors_file, skiprows=1)
            print(" Successfully loaded 'sectors.xlsx'.")
        else:
            # Fallback to DB if excel is missing
            df_sectors_raw = pd.read_sql("SELECT * FROM sectors", conn)
            print(" Successfully loaded 'sectors' from database (fallback).")
    except Exception as e:
        print(f" Error loading sectors: {e}")
        return
    finally:
        conn.close()

    # --- BULLETPROOF EXTRACTION FUNCTION (Prevents the 'str' AttributeError) ---
    def extract_clean_data(df, id_keywords, target_keywords):
        # Flatten columns to lowercase list to avoid duplicate name crashes
        col_names = [str(c).lower().strip() for c in df.columns]

        # Find index of ID column
        id_idx = next((i for i, c in enumerate(col_names) if c in id_keywords), 0)

        # Find index of Target column (About or Sector)
        target_idx = next(
            (
                i
                for i, c in enumerate(col_names)
                if any(k in c for k in target_keywords)
            ),
            None,
        )

        # Build a fresh, clean DataFrame with only 1D series
        clean_df = pd.DataFrame()

        # Extract ID and force it to be string
        clean_df["company_id"] = df.iloc[:, id_idx].astype(str).str.strip().str.upper()

        # Extract Target text
        if target_idx is not None:
            clean_df["target_text"] = df.iloc[:, target_idx].astype(str).str.strip()

        return clean_df

    # 3. EXTRACT ONLY THE NEEDED COLUMNS SAFELY
    id_kws = ["id", "company_id", "cid", "company", "symbol", "name", "company name"]

    df_companies = extract_clean_data(
        df_companies_raw, id_kws, ["about", "description", "profile", "business"]
    )
    if "target_text" not in df_companies.columns:
        print(" Error: Could not find 'about_company' column.")
        return

    df_sectors = extract_clean_data(
        df_sectors_raw, id_kws, ["sector", "industry", "macro"]
    )
    if "target_text" not in df_sectors.columns:
        print(" Error: Could not find 'sector' column.")
        return

    # 4. NLP TAGGER LOGIC
    keyword_map = {
        "Financial Services": [
            "bank",
            "finance",
            "loan",
            "credit",
            "insurance",
            "wealth",
            "nbfc",
            "capital",
            "investment",
            "mortgage",
            "lending",
        ],
        "IT": [
            "software",
            "it services",
            "technology",
            "digital",
            "consulting",
            "cloud",
            "cyber",
            "tech",
            "computing",
            "data",
        ],
        "FMCG": [
            "consumer",
            "fmcg",
            "food",
            "personal care",
            "beverages",
            "retail",
            "household",
            "tobacco",
            "cigarettes",
        ],
        "Automobile": [
            "auto",
            "vehicle",
            "motor",
            "car",
            "two-wheeler",
            "tractor",
            "automotive",
            "tyre",
        ],
        "Healthcare": [
            "pharma",
            "healthcare",
            "medicine",
            "drug",
            "hospital",
            "clinical",
            "api",
            "biotech",
            "diagnostics",
        ],
        "Energy": [
            "energy",
            "oil",
            "gas",
            "power",
            "petroleum",
            "solar",
            "coal",
            "renewable",
            "exploration",
            "grid",
        ],
        "Metals & Mining": [
            "steel",
            "metal",
            "mining",
            "aluminium",
            "iron",
            "copper",
            "zinc",
            "cement",
        ],
        "Construction": [
            "cement",
            "construction",
            "infrastructure",
            "real estate",
            "building",
            "materials",
            "realty",
        ],
        "Telecom": [
            "telecom",
            "network",
            "broadband",
            "wireless",
            "communication",
            "tower",
        ],
        "Chemicals": [
            "chemical",
            "agrochemical",
            "polymers",
            "specialty chemicals",
            "fertilizer",
            "paints",
        ],
    }

    results = []

    for _, row in df_companies.iterrows():
        company = row["company_id"]
        text = str(row["target_text"]).lower()

        if pd.isna(row["target_text"]) or text in ["nan", "none", ""]:
            continue

        # Predict sector
        predicted_sector = "Unknown"
        max_matches = 0
        found_keywords = []

        for sector, keywords in keyword_map.items():
            matches = [kw for kw in keywords if re.search(r"\b" + kw + r"\b", text)]
            if len(matches) > max_matches:
                max_matches = len(matches)
                predicted_sector = sector
                found_keywords = matches

        # Actual sector
        actual_sector = "Not Found"
        sector_data = df_sectors[df_sectors["company_id"] == company]
        if not sector_data.empty:
            actual_sector = str(sector_data.iloc[0]["target_text"]).strip().title()

        # Validation Logic
        is_match = False
        if predicted_sector != "Unknown" and actual_sector != "Not Found":
            if (
                predicted_sector.lower() in actual_sector.lower()
                or actual_sector.lower() in predicted_sector.lower()
            ):
                is_match = True
            elif (
                predicted_sector == "IT"
                and "information technology" in actual_sector.lower()
            ):
                is_match = True
            elif (
                predicted_sector == "Financial Services"
                and "financial" in actual_sector.lower()
            ):
                is_match = True
            elif predicted_sector == "FMCG" and "consumer" in actual_sector.lower():
                is_match = True

        status = (
            " MATCH"
            if is_match
            else (" MISMATCH" if predicted_sector != "Unknown" else " UNKNOWN")
        )

        results.append(
            {
                "Company ID": company,
                "Actual Sector": actual_sector,
                "Predicted Tag": predicted_sector,
                "Keywords Matched": (
                    ", ".join(found_keywords) if found_keywords else "None"
                ),
                "Validation Status": status,
            }
        )

    # 5. GENERATE REPORT
    df_results = pd.DataFrame(results)

    if not df_results.empty:
        df_results.to_csv(output_file, index=False)
        print(f"\n✅ Tagging & Validation complete for {len(df_results)} companies.")
        print(f"💾 Report saved to: {output_file}\n")

        matches = len(df_results[df_results["Validation Status"] == " MATCH"])
        mismatches = len(df_results[df_results["Validation Status"] == " MISMATCH"])

        print(" SUMMARY:")
        print(f"   -> Accurate Tags: {matches}")
        print(f"   -> Mismatched Tags: {mismatches}")

        if mismatches > 0:
            print("\n SAMPLE MISMATCHES (Needs manual review):")
            print(
                df_results[df_results["Validation Status"] == " MISMATCH"]
                .head(5)[["Company ID", "Actual Sector", "Predicted Tag"]]
                .to_string(index=False)
            )

    else:
        print(" No text data found to tag.")


if __name__ == "__main__":
    tag_business_description()
