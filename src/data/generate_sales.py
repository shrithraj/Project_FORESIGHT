import pandas as pd
import numpy as np
from pathlib import Path

RAW_DATA = Path("data/raw")

# Load existing datasets
sku_master = pd.read_csv(RAW_DATA / "sku_master.csv")
calendar = pd.read_csv(RAW_DATA / "calendar.csv")

np.random.seed(42)

sales = []

for _, sku in sku_master.iterrows():

    sku_id = sku["SKU_ID"]

    price = sku["List_Price"]

    # Every product has different popularity
    base_demand = np.random.randint(5, 40)

    for _, day in calendar.iterrows():

        demand = base_demand

        # Weekend boost
        if day["Weekend"]:
            demand *= 1.20

        # Holiday boost
        if day["Holiday"]:
            demand *= 1.50

        # Seasonal effect
        if day["Season"] == "Festival":
            demand *= 1.35

        elif day["Season"] == "Winter":
            demand *= 1.10

        # Promotion (10% chance)
        promo = np.random.choice(
            [0,1],
            p=[0.9,0.1]
        )

        if promo == 1:
            demand *= 1.40

        # Random noise
        demand += np.random.normal(0,3)

        demand = max(0,int(round(demand)))

        revenue = round(demand * price,2)

        sales.append({

            "Date":day["Date"],

            "SKU_ID":sku_id,

            "Units_Sold":demand,

            "Unit_Price":price,

            "Revenue":revenue,

            "Promotion":promo

        })

sales_daily = pd.DataFrame(sales)

sales_daily.to_csv(
    RAW_DATA/"sales_daily.csv",
    index=False
)

print()

print(sales_daily.head())

print()

print("Rows :",len(sales_daily))