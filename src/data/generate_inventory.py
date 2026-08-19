import pandas as pd
import numpy as np
from pathlib import Path

RAW_DATA = Path("data/raw")

sales = pd.read_csv(RAW_DATA / "sales_daily.csv")
sku_master = pd.read_csv(RAW_DATA / "sku_master.csv")

np.random.seed(42)

inventory_rows = []

latest_date = sales["Date"].max()

for _, sku in sku_master.iterrows():

    sku_id = sku["SKU_ID"]

    avg_sales = sales[
        sales["SKU_ID"] == sku_id
    ]["Units_Sold"].mean()

    lead_time = np.random.randint(3, 15)

    safety_stock = int(avg_sales * lead_time * 0.5)

    reorder_point = int(avg_sales * lead_time)

    current_stock = np.random.randint(
        reorder_point,
        reorder_point * 3
    )

    on_order = np.random.randint(
        0,
        reorder_point
    )

    inventory_rows.append({

        "Date": latest_date,

        "SKU_ID": sku_id,

        "Current_Stock": current_stock,

        "On_Order": on_order,

        "Lead_Time_Days": lead_time,

        "Safety_Stock": safety_stock,

        "Reorder_Point": reorder_point

    })

inventory = pd.DataFrame(inventory_rows)

inventory.to_csv(
    RAW_DATA / "inventory_snapshot.csv",
    index=False
)

print()
print(inventory.head())
print()
print("Inventory Rows :", len(inventory))