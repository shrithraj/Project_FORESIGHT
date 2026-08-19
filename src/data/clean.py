import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/raw")
PROCESSED_DATA = Path("data/processed")

PROCESSED_DATA.mkdir(parents=True, exist_ok=True)

files = {
    "sales_daily.csv": "sales_daily_clean.csv",
    "sku_master.csv": "sku_master_clean.csv",
    "calendar.csv": "calendar_clean.csv",
    "inventory_snapshot.csv": "inventory_snapshot_clean.csv"
}

print("=" * 60)
print("PROJECT FORESIGHT - DATA CLEANING")
print("=" * 60)

for raw_file, clean_file in files.items():

    print(f"\nProcessing {raw_file}")

    df = pd.read_csv(RAW_DATA / raw_file)

    # Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before - len(df)

    # Remove rows where all values are missing
    df = df.dropna(how="all")

    # Fill numeric missing values
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Fill text missing values
    object_cols = df.select_dtypes(include=["object","string"]).columns
    df[object_cols] = df[object_cols].fillna("Unknown")

    # Convert Date column if present
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    # Remove negative values from important columns
    for col in ["Units_Sold", "Revenue", "Current_Stock"]:
        if col in df.columns:
            df = df[df[col] >= 0]

    # Save cleaned file
    df.to_csv(PROCESSED_DATA / clean_file, index=False)

    print(f"Rows : {len(df)}")
    print(f"Duplicates Removed : {duplicates_removed}")

print("\nCleaning Completed Successfully")