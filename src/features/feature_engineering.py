import pandas as pd
from pathlib import Path

DATA = Path("data/processed")

df = pd.read_csv(DATA / "master_dataset.csv")

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Sort data
df = df.sort_values(["SKU_ID", "Date"])

# ---------------------------
# Time Features
# ---------------------------

df["DayOfWeek"] = df["Date"].dt.dayofweek
df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)
df["IsWeekend"] = df["Weekend"].astype(int)

# ---------------------------
# Lag Features
# ---------------------------

df["Lag_1"] = df.groupby("SKU_ID")["Units_Sold"].shift(1)

df["Lag_7"] = df.groupby("SKU_ID")["Units_Sold"].shift(7)

# ---------------------------
# Rolling Features
# ---------------------------

df["Rolling_7"] = (
    df.groupby("SKU_ID")["Units_Sold"]
      .transform(lambda x: x.rolling(7).mean())
)

df["Rolling_30"] = (
    df.groupby("SKU_ID")["Units_Sold"]
      .transform(lambda x: x.rolling(30).mean())
)

print(df.head(15))