import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw")

sales = pd.read_csv(DATA_PATH / "sales_daily.csv")
sku = pd.read_csv(DATA_PATH / "sku_master.csv")
calendar = pd.read_csv(DATA_PATH / "calendar.csv")
inventory = pd.read_csv(DATA_PATH / "inventory_snapshot.csv")

print("Sales Shape:", sales.shape)
print("SKU Shape:", sku.shape)
print("Calendar Shape:", calendar.shape)
print("Inventory Shape:", inventory.shape)