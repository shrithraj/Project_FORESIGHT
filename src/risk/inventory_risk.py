import pandas as pd
import joblib
from pathlib import Path

# =====================================================
# PROJECT FORESIGHT - INVENTORY RISK ENGINE
# =====================================================

DATA = Path("data/processed")
MODEL = Path("models/random_forest.pkl")
REPORT = Path("reports")

REPORT.mkdir(exist_ok=True)

# =====================================================
# LOAD DATA
# =====================================================

print("=" * 60)
print("PROJECT FORESIGHT - INVENTORY RISK ENGINE")
print("=" * 60)

df = pd.read_csv(DATA / "master_dataset.csv")

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values(["SKU_ID", "Date"])

# =====================================================
# FEATURE ENGINEERING
# =====================================================

df["DayOfWeek"] = df["Date"].dt.dayofweek
df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)
df["IsWeekend"] = df["Weekend"].astype(int)

df["Lag_1"] = (
    df.groupby("SKU_ID")["Units_Sold"]
    .shift(1)
)

df["Lag_7"] = (
    df.groupby("SKU_ID")["Units_Sold"]
    .shift(7)
)

df["Rolling_7"] = (
    df.groupby("SKU_ID")["Units_Sold"]
    .transform(lambda x: x.rolling(7).mean())
)

df["Rolling_30"] = (
    df.groupby("SKU_ID")["Units_Sold"]
    .transform(lambda x: x.rolling(30).mean())
)

df = df.dropna()

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load(MODEL)

latest = df.groupby("SKU_ID").tail(1).copy()

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

latest["Forecast"] = (
    model.predict(latest[features])
    .round()
    .astype(int)
)

# =====================================================
# DAYS OF INVENTORY
# =====================================================

latest["Days_of_Inventory"] = (
    latest["Current_Stock"] /
    latest["Forecast"].clip(lower=1)
).round(1)

# =====================================================
# RISK CLASSIFICATION
# =====================================================

def classify(days):

    if days < 7:
        return "Stockout Risk"

    elif days > 30:
        return "Overstock Risk"

    else:
        return "Healthy"


latest["Risk"] = latest["Days_of_Inventory"].apply(classify)

# =====================================================
# RISK SCORE
# =====================================================

latest["Risk_Score"] = (
    (30 - latest["Days_of_Inventory"])
    .clip(lower=0) / 30 * 100
).round(1)

# =====================================================
# PRIORITY
# =====================================================

def priority(score):

    if score >= 80:
        return "Critical"

    elif score >= 50:
        return "High"

    elif score >= 25:
        return "Medium"

    else:
        return "Low"


latest["Priority"] = latest["Risk_Score"].apply(priority)

# =====================================================
# RECOMMENDATION
# =====================================================

def recommendation(row):

    if row["Risk"] == "Stockout Risk":

        if row["Priority"] == "Critical":
            return "Emergency Purchase"

        elif row["Priority"] == "High":
            return "Increase Purchase Order"

        else:
            return "Monitor Daily"

    elif row["Risk"] == "Overstock Risk":
        return "Run Promotion / Reduce Purchase"

    return "Maintain Current Stock"


latest["Recommendation"] = latest.apply(
    recommendation,
    axis=1
)

# =====================================================
# FINAL REPORT
# =====================================================

result = latest[
    [
        "SKU_ID",
        "Forecast",
        "Current_Stock",
        "Days_of_Inventory",
        "Risk_Score",
        "Priority",
        "Risk",
        "Recommendation"
    ]
]

result = result.sort_values(
    by="Risk_Score",
    ascending=False
)

# =====================================================
# SAVE REPORT
# =====================================================

result.to_csv(
    REPORT / "inventory_risk.csv",
    index=False
)

# =====================================================
# DISPLAY
# =====================================================

print("\nInventory Risk Report\n")
print(result.head(20))

print("\nTotal Products :", len(result))
print("Critical :", (result["Priority"] == "Critical").sum())
print("High :", (result["Priority"] == "High").sum())
print("Medium :", (result["Priority"] == "Medium").sum())
print("Low :", (result["Priority"] == "Low").sum())

print("\nRisk report saved successfully.")
print("Location : reports/inventory_risk.csv")
print("=" * 60)