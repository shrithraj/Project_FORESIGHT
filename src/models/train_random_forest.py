import pandas as pd
import joblib
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

# -------------------------
# Load Dataset
# -------------------------

DATA = Path("data/processed")
MODEL_DIR = Path("models")

MODEL_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA / "master_dataset.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values(["SKU_ID", "Date"])

# -------------------------
# Feature Engineering
# -------------------------

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

df = df.dropna()

# -------------------------
# Features
# -------------------------

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

split = int(len(df) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

# -------------------------
# Train Model
# -------------------------

print("Training Random Forest...")

model = RandomForestRegressor(

    n_estimators=200,

    random_state=42,

    n_jobs=-1

)

model.fit(X_train, y_train)

# -------------------------
# Prediction
# -------------------------

pred = model.predict(X_test)

# -------------------------
# Metrics
# -------------------------

mae = mean_absolute_error(y_test, pred)

rmse = mean_squared_error(y_test, pred) ** 0.5

r2 = r2_score(y_test, pred)

print()

print("=" * 40)

print("MODEL PERFORMANCE")

print("=" * 40)

print(f"MAE  : {mae:.2f}")

print(f"RMSE : {rmse:.2f}")

print(f"R²   : {r2:.4f}")

# -------------------------
# Save Model
# -------------------------

joblib.dump(
    model,
    MODEL_DIR / "random_forest.pkl"
)

print()

print("Model Saved Successfully!")