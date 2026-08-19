import pandas as pd
from pathlib import Path

PROCESSED = Path("data/processed")

print("=" * 60)
print("PROJECT FORESIGHT - DATA MERGING")
print("=" * 60)

# Read cleaned datasets
sales = pd.read_csv(PROCESSED / "sales_daily_clean.csv")
sku = pd.read_csv(PROCESSED / "sku_master_clean.csv")
calendar = pd.read_csv(PROCESSED / "calendar_clean.csv")
inventory = pd.read_csv(PROCESSED / "inventory_snapshot_clean.csv")

# Convert Date columns
sales["Date"] = pd.to_datetime(sales["Date"])
calendar["Date"] = pd.to_datetime(calendar["Date"])
inventory["Date"] = pd.to_datetime(inventory["Date"])

# Merge sales with SKU
merged = sales.merge(
    sku,
    on="SKU_ID",
    how="left"
)

# Merge calendar
merged = merged.merge(
    calendar,
    on="Date",
    how="left"
)

# Merge inventory
merged = merged.merge(
    inventory.drop(columns=["Date"]),
    on="SKU_ID",
    how="left"
)

# Save
merged.to_csv(
    PROCESSED / "master_dataset.csv",
    index=False
)

print("\nMerged Dataset Created Successfully")
print(merged.head())
print("\nRows :", len(merged))
print("Columns :", len(merged.columns))