import pandas as pd
import numpy as np
from pathlib import Path

RAW_DATA = Path("data/raw")

calendar = pd.DataFrame()

calendar["Date"] = pd.date_range(
    "2024-01-01",
    "2025-12-31"
)

calendar["Year"] = calendar["Date"].dt.year
calendar["Month"] = calendar["Date"].dt.month
calendar["Month_Name"] = calendar["Date"].dt.month_name()
calendar["Week"] = calendar["Date"].dt.isocalendar().week
calendar["Quarter"] = calendar["Date"].dt.quarter
calendar["Day"] = calendar["Date"].dt.day
calendar["Day_Name"] = calendar["Date"].dt.day_name()

calendar["Weekend"] = calendar["Day_Name"].isin(
    ["Saturday","Sunday"]
)

calendar["Holiday"] = False

calendar["Season"] = np.where(

    calendar["Month"].isin([12,1,2]),

    "Winter",

    np.where(

        calendar["Month"].isin([3,4,5]),

        "Summer",

        np.where(

            calendar["Month"].isin([6,7,8]),

            "Monsoon",

            "Festival"

        )

    )

)

calendar.to_csv(
    RAW_DATA/"calendar.csv",
    index=False
)

print("Calendar Generated")

print(calendar.head())

print()

print("Rows :",len(calendar))