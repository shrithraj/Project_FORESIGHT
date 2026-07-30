import pandas as pd
import numpy as np
from pathlib import Path

RAW_DATA = Path("data/raw")
RAW_DATA.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

categories = {
    "Furniture": ["Chair", "Table", "Sofa", "Bed", "Desk"],
    "Kitchen": ["Mixer", "Bottle", "Cookware", "Pan", "Storage"],
    "Decor": ["Lamp", "Clock", "Frame", "Vase", "Mirror"],
    "Electronics": ["Speaker", "Fan", "Iron", "Kettle", "Vacuum"]
}

rows = []

sku = 1

for category in categories:

    for subcategory in categories[category]:

        for i in range(10):

            unit_cost = np.random.randint(300,4000)

            list_price = unit_cost*np.random.uniform(1.2,2.5)

            rows.append({

                "SKU_ID":f"SKU{sku:03d}",

                "Category":category,

                "Subcategory":subcategory,

                "Launch_Date":np.random.choice(
                    pd.date_range(
                        "2023-01-01",
                        "2025-01-01"
                    )
                ),

                "Unit_Cost":round(unit_cost,2),

                "List_Price":round(list_price,2)

            })

            sku+=1

sku_master=pd.DataFrame(rows)

sku_master.to_csv(

    RAW_DATA/"sku_master.csv",

    index=False

)

print("SKU Master Generated")

print(sku_master.head())

print()

print("Total Products :",len(sku_master))