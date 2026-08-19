import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/raw")

files = {
    "Sales": "sales_daily.csv",
    "SKU": "sku_master.csv",
    "Calendar": "calendar.csv",
    "Inventory": "inventory_snapshot.csv"
}

print("=" * 60)
print("PROJECT FORESIGHT - DATA VALIDATION")
print("=" * 60)

for name, filename in files.items():

    print(f"\n{name}")

    df = pd.read_csv(RAW_DATA / filename)

    print("-" * 40)

    print("Rows :", len(df))
    print("Columns :", len(df.columns))

    print("\nMissing Values")

    print(df.isnull().sum())

    print("\nDuplicate Rows :", df.duplicated().sum())

    print("\nData Types")

    print(df.dtypes)

print("\nValidation Completed Successfully")