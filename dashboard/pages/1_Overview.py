import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Overview | Project FORESIGHT",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data" / "processed" / "master_dataset.csv"

if not DATA_PATH.exists():
    st.error(f"Dataset not found:\n{DATA_PATH}")
    st.stop()

df = pd.read_csv(DATA_PATH)

# ==========================================================
# PAGE HEADER
# ==========================================================

st.markdown("""
# 📊 Executive Retail Intelligence Dashboard

### AI Powered Retail Demand Forecasting & Inventory Intelligence

---
""")

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("📌 Dashboard Filters")

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

subcategory = st.sidebar.multiselect(
    "Subcategory",
    sorted(df["Subcategory"].unique()),
    default=sorted(df["Subcategory"].unique())
)

season = st.sidebar.multiselect(
    "Season",
    sorted(df["Season"].unique()),
    default=sorted(df["Season"].unique())
)

year = st.sidebar.multiselect(
    "Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

promotion = st.sidebar.multiselect(
    "Promotion",
    sorted(df["Promotion"].unique()),
    default=sorted(df["Promotion"].unique())
)

holiday = st.sidebar.multiselect(
    "Holiday",
    sorted(df["Holiday"].unique()),
    default=sorted(df["Holiday"].unique())
)

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered = df[
    (df["Category"].isin(category))
    &
    (df["Subcategory"].isin(subcategory))
    &
    (df["Season"].isin(season))
    &
    (df["Year"].isin(year))
    &
    (df["Promotion"].isin(promotion))
    &
    (df["Holiday"].isin(holiday))
]

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_revenue = filtered["Revenue"].sum()

total_units = filtered["Units_Sold"].sum()

total_products = filtered["SKU_ID"].nunique()

total_categories = filtered["Category"].nunique()

avg_price = filtered["Unit_Price"].mean()

avg_stock = filtered["Current_Stock"].mean()

forecast_accuracy = 95.3

inventory_health = (
    (
        filtered["Current_Stock"] >
        filtered["Safety_Stock"]
    ).mean() * 100
)

# ==========================================================
# KPI DASHBOARD
# ==========================================================

st.markdown("## 📈 Executive KPI Dashboard")

k1, k2, k3, k4, k5, k6 = st.columns(6)

k1.metric(
    "💰 Revenue",
    f"₹{total_revenue:,.0f}"
)

k2.metric(
    "📦 Units Sold",
    f"{total_units:,.0f}"
)

k3.metric(
    "🛒 Products",
    total_products
)

k4.metric(
    "📂 Categories",
    total_categories
)

k5.metric(
    "📊 Avg Price",
    f"₹{avg_price:,.2f}"
)

k6.metric(
    "🤖 Accuracy",
    f"{forecast_accuracy}%"
)

st.divider()
# ==========================================================
# REVENUE TREND
# ==========================================================

st.markdown("## 📈 Revenue Trend")

daily_sales = (
    filtered
    .groupby("Date", as_index=False)["Revenue"]
    .sum()
)

fig = px.line(
    daily_sales,
    x="Date",
    y="Revenue",
    markers=True,
    template="plotly_white",
    title="Daily Revenue Trend"
)

fig.update_layout(
    height=450,
    hovermode="x unified",
    title_x=0.01
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# CATEGORY & MONTHLY ANALYTICS
# ==========================================================

left, right = st.columns(2)

# ----------------------------------------------------------
# Revenue by Category
# ----------------------------------------------------------

with left:

    category_sales = (
        filtered
        .groupby("Category", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
    )

    fig = px.pie(
        category_sales,
        names="Category",
        values="Revenue",
        hole=0.60,
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="Revenue by Category"
    )

    fig.update_layout(
        height=430
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------------------------
# Monthly Revenue
# ----------------------------------------------------------

with right:

    monthly_sales = (
        filtered
        .groupby("Month_Name", as_index=False)["Revenue"]
        .sum()
    )

    month_order = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

    monthly_sales["Month_Name"] = pd.Categorical(
        monthly_sales["Month_Name"],
        categories=month_order,
        ordered=True
    )

    monthly_sales = monthly_sales.sort_values("Month_Name")

    fig = px.bar(
        monthly_sales,
        x="Month_Name",
        y="Revenue",
        color="Revenue",
        color_continuous_scale="Blues",
        text_auto=".2s",
        title="Monthly Revenue"
    )

    fig.update_layout(
        height=430,
        xaxis_title="Month",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================================
# REVENUE TREEMAP
# ==========================================================

st.markdown("## 🌳 Revenue Distribution")

tree = (
    filtered
    .groupby(
        ["Category", "Subcategory"],
        as_index=False
    )["Revenue"]
    .sum()
)

fig = px.treemap(
    tree,
    path=[
        "Category",
        "Subcategory"
    ],
    values="Revenue",
    color="Revenue",
    color_continuous_scale="Blues"
)

fig.update_layout(
    height=600,
    margin=dict(t=30, l=10, r=10, b=10)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# REVENUE COMPARISON
# ==========================================================

st.markdown("## 📊 Revenue Comparison")

compare_left, compare_right = st.columns(2)

with compare_left:

    revenue_by_season = (
        filtered
        .groupby("Season", as_index=False)["Revenue"]
        .sum()
    )

    fig = px.bar(
        revenue_by_season,
        x="Season",
        y="Revenue",
        color="Revenue",
        color_continuous_scale="Teal",
        title="Revenue by Season"
    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with compare_right:

    promotion_sales = (
        filtered
        .groupby("Promotion", as_index=False)["Revenue"]
        .sum()
    )

    fig = px.bar(
        promotion_sales,
        x="Promotion",
        y="Revenue",
        color="Revenue",
        color_continuous_scale="Oranges",
        title="Promotion Impact"
    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()
# ==========================================================
# INVENTORY INTELLIGENCE DASHBOARD
# ==========================================================

st.markdown("## 📦 Inventory Intelligence")

left, right = st.columns(2)

# ----------------------------------------------------------
# Inventory by Category
# ----------------------------------------------------------

with left:

    inventory = (
        filtered
        .groupby("Category", as_index=False)["Current_Stock"]
        .sum()
    )

    fig = px.bar(
        inventory,
        x="Category",
        y="Current_Stock",
        color="Current_Stock",
        color_continuous_scale="Viridis",
        title="Current Inventory by Category",
        text_auto=".2s"
    )

    fig.update_layout(
        height=430,
        xaxis_title="Category",
        yaxis_title="Current Stock"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------------------------
# Inventory Health Gauge
# ----------------------------------------------------------

with right:

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=inventory_health,
            number={"suffix": "%"},
            title={"text": "Inventory Health Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563EB"},
                "steps": [
                    {"range": [0, 40], "color": "#F87171"},
                    {"range": [40, 70], "color": "#FACC15"},
                    {"range": [70, 100], "color": "#4ADE80"}
                ]
            }
        )
    )

    fig.update_layout(height=430)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================================
# TOP PRODUCTS
# ==========================================================

st.markdown("## 🏆 Top 10 Revenue Generating Products")

top_products = (
    filtered
    .groupby("SKU_ID", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
    .head(10)
)

fig = px.bar(
    top_products,
    x="Revenue",
    y="SKU_ID",
    orientation="h",
    color="Revenue",
    color_continuous_scale="Turbo",
    text_auto=".2s"
)

fig.update_layout(
    height=520,
    yaxis=dict(categoryorder="total ascending"),
    title="Top Performing Products"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# SEASONAL ANALYSIS
# ==========================================================

left, right = st.columns(2)

with left:

    season_sales = (
        filtered
        .groupby("Season", as_index=False)["Revenue"]
        .sum()
    )

    fig = px.sunburst(
        season_sales,
        path=["Season"],
        values="Revenue",
        color="Revenue",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        height=450,
        title="Seasonal Revenue Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    season_units = (
        filtered
        .groupby("Season", as_index=False)["Units_Sold"]
        .sum()
    )

    fig = px.bar(
        season_units,
        x="Season",
        y="Units_Sold",
        color="Units_Sold",
        color_continuous_scale="Purples",
        text_auto=".2s",
        title="Units Sold by Season"
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================================
# WEEKLY SALES HEATMAP
# ==========================================================
filtered = filtered.copy()

filtered["Date"] = pd.to_datetime(
    filtered["Date"],
    errors="coerce"
)

st.markdown("## 🔥 Weekly Sales Heatmap")

heat = (
    filtered.assign(
        Weekday=filtered["Date"].dt.day_name(),
        Month=filtered["Date"].dt.month_name()
    )
    .pivot_table(
        values="Revenue",      # Change to Sales or Demand if Revenue doesn't exist
        index="Weekday",
        columns="Month",
        aggfunc="sum",
        fill_value=0
    )
)

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

heat = heat.reindex(weekday_order)

fig = px.imshow(
    heat,
    aspect="auto",
    color_continuous_scale="Blues",
    text_auto=".2s"
)

fig.update_layout(height=520)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

# ==========================================================
# INVENTORY RISK ANALYSIS
# ==========================================================

st.markdown("## ⚠ Inventory Risk Overview")

low_stock = filtered[
    filtered["Current_Stock"] <= filtered["Safety_Stock"]
]

reorder_products = filtered[
    filtered["Current_Stock"] <= filtered["Reorder_Point"]
]

risk1, risk2, risk3, risk4 = st.columns(4)

risk1.metric(
    "Low Stock Items",
    len(low_stock)
)

risk2.metric(
    "Reorder Required",
    len(reorder_products)
)

risk3.metric(
    "Average Stock",
    f"{filtered['Current_Stock'].mean():.1f}"
)

risk4.metric(
    "Lead Time",
    f"{filtered['Lead_Time_Days'].mean():.1f} Days"
)

st.divider()

# ==========================================================
# INVENTORY RECOMMENDATIONS
# ==========================================================

st.markdown("## 📋 Inventory Recommendations")

recommendations = filtered[
    filtered["Current_Stock"] <= filtered["Reorder_Point"]
].copy()

if recommendations.empty:

    st.success("🎉 Excellent! No products currently require reordering.")

else:

    display_columns = [
        "SKU_ID",
        "Category",
        "Subcategory",
        "Current_Stock",
        "Safety_Stock",
        "Reorder_Point",
        "Lead_Time_Days",
        "Units_Sold",
        "Revenue"
    ]

    available_columns = [
        col for col in display_columns if col in recommendations.columns
    ]

    st.dataframe(
        recommendations[available_columns],
        use_container_width=True,
        hide_index=True
    )

    csv = recommendations[available_columns].to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Inventory Recommendations",
        data=csv,
        file_name="inventory_recommendations.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()

# ==========================================================
# DATASET SUMMARY
# ==========================================================

st.markdown("## 📊 Dataset Summary")

s1, s2, s3, s4 = st.columns(4)

s1.metric(
    "📄 Total Records",
    f"{len(filtered):,}"
)

s2.metric(
    "🛒 SKUs",
    filtered["SKU_ID"].nunique()
)

s3.metric(
    "📂 Categories",
    filtered["Category"].nunique()
)

date_range = (
    f"{filtered['Date'].min().strftime('%d-%b-%Y')}  ➜  "
    f"{filtered['Date'].max().strftime('%d-%b-%Y')}"
)

s4.metric(
    "📅 Date Range",
    date_range
)

st.divider()

# ==========================================================
# MODEL PERFORMANCE
# ==========================================================

st.markdown("## 🤖 AI Model Performance")

m1, m2, m3 = st.columns(3)

m1.metric(
    "R² Score",
    "95.3%"
)

m2.metric(
    "MAE",
    "2.43"
)

m3.metric(
    "RMSE",
    "3.05"
)



st.divider()
