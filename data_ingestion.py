from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")

datasets = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]

dataframes = {}

# 1. Load and inspect all 10 datasets
print("\n--- DATASET SUMMARY INSPECTION ---")

for dataset in datasets:
    file_path = RAW_DIR / dataset

    if file_path.exists():
        df = pd.read_csv(file_path)
        dataframes[dataset] = df

        print(f"\nDataset: {dataset}")
        print(f"Shape: {df.shape}")

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head())

        # Basic anomaly checks
        print(f"\nMissing Values: {df.isnull().sum().sum()}")
        print(f"Duplicate Rows: {df.duplicated().sum()}")

    else:
        print(f"\nFile not found: {dataset}")


# 2. Explore Fund Master
if "01_fund_master.csv" in dataframes:

    fund_master = dataframes["01_fund_master.csv"]

    print("\n--- FUND MASTER EXPLORATION ---")

    print("\nFund Houses:")
    print(fund_master["fund_house"].unique())

    print("\nCategories:")
    print(fund_master["category"].unique())

    print("\nSub-Categories:")
    print(fund_master["sub_category"].unique())

    print("\nRisk Categories:")
    print(fund_master["risk_category"].unique())


# 3. Validate AMFI Codes
if (
    "01_fund_master.csv" in dataframes
    and "02_nav_history.csv" in dataframes
):

    fund_codes = set(
        dataframes["01_fund_master.csv"]["amfi_code"].astype(str)
    )

    nav_codes = set(
        dataframes["02_nav_history.csv"]["amfi_code"].astype(str)
    )

    missing_codes = fund_codes - nav_codes

    print("\n--- DATA QUALITY SUMMARY ---")

    print(f"Total schemes in Fund Master: {len(fund_codes)}")
    print(f"Unique schemes in NAV History: {len(nav_codes)}")

    if missing_codes:
        print(
            f"WARNING: {len(missing_codes)} AMFI codes "
            "are missing from NAV History."
        )
        print("Missing Codes:", missing_codes)

    else:
        print(
            "Validation Passed: Every AMFI code in "
            "Fund Master exists in NAV History."
        )