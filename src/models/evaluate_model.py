import pandas as pd
import matplotlib.pyplot as plt
import joblib
from pathlib import Path

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

DATA = Path("data/processed")
MODEL_DIR = Path("models")
REPORT_DIR = Path("reports/images")

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------
# Load dataset
# ------------------------

df = pd.read_csv(DATA / "master_dataset.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values(["SKU_ID", "Date"])

# ------------------------
# Feature Engineering
# ------------------------

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

X_test = X.iloc[split:]
y_test = y.iloc[split:]

# ------------------------
# Load model
# ------------------------

model = joblib.load(MODEL_DIR / "random_forest.pkl")

pred = model.predict(X_test)

# ------------------------
# Metrics
# ------------------------

print("=" * 40)
print("MODEL EVALUATION")
print("=" * 40)

print(f"MAE  : {mean_absolute_error(y_test,pred):.2f}")
print(f"RMSE : {mean_squared_error(y_test,pred)**0.5:.2f}")
print(f"R²   : {r2_score(y_test,pred):.4f}")

# ------------------------
# Prediction Plot
# ------------------------

plt.figure(figsize=(14,5))

plt.plot(
    y_test.values[:300],
    label="Actual"
)

plt.plot(
    pred[:300],
    label="Predicted"
)

plt.legend()

plt.title("Actual vs Predicted Sales")

plt.savefig(
    REPORT_DIR / "prediction_vs_actual.png"
)

plt.show()

# ------------------------
# Feature Importance
# ------------------------

importance = pd.Series(
    model.feature_importances_,
    index=features
)

importance.sort_values().plot(
    kind="barh",
    figsize=(10,6)
)

plt.title("Feature Importance")

plt.savefig(
    REPORT_DIR / "feature_importance.png"
)

plt.show()

print("\nEvaluation Complete!")