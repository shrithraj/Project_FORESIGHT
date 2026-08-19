import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

DATA = Path("data/processed")

# Load master dataset
df = pd.read_csv(DATA / "master_dataset.csv")

# Convert dates
df["Date"] = pd.to_datetime(df["Date"])

# Sort data
df = df.sort_values(["SKU_ID", "Date"])

# ----------------------------
# Feature Engineering
# ----------------------------

df["DayOfWeek"] = df["Date"].dt.dayofweek
df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)
df["IsWeekend"] = df["Weekend"].astype(int)

df["Lag_1"] = df.groupby("SKU_ID")["Units_Sold"].shift(1)
df["Lag_7"] = df.groupby("SKU_ID")["Units_Sold"].shift(7)

df["Rolling_7"] = (
    df.groupby("SKU_ID")["Units_Sold"]
      .transform(lambda x: x.rolling(7).mean())
)

df["Rolling_30"] = (
    df.groupby("SKU_ID")["Units_Sold"]
      .transform(lambda x: x.rolling(30).mean())
)

# Remove rows with missing lag values
df = df.dropna()

# ----------------------------
# Features and Target
# ----------------------------

features = [
    "DayOfWeek",
    "Month",
    "WeekOfYear",
    "Promotion",
    "Holiday",
    "IsWeekend",
    "Lag_1",
    "Lag_7",
    "Rolling_7",
    "Rolling_30",
    "Current_Stock"
]

X = df[features]
y = df["Units_Sold"]

# Time-based split (recommended for forecasting)
split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("=" * 50)
print("Training Shape :", X_train.shape)
print("Testing Shape  :", X_test.shape)
print("=" * 50)