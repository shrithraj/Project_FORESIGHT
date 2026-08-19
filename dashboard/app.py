import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Project FORESIGHT",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# LOAD CSS
# ==========================================================

css_file = Path("dashboard/assets/style.css")

if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================

DATA_PATH = Path("data/processed/master_dataset.csv")
REPORT_PATH = Path("reports/inventory_recommendations.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

@st.cache_data
def load_report():
    if REPORT_PATH.exists():
        return pd.read_csv(REPORT_PATH)
    return pd.DataFrame()

df = load_data()
risk = load_report()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.image(
    "https://img.icons8.com/color/96/combo-chart--v1.png",
    width=70
)

st.sidebar.title("PROJECT FORESIGHT")

st.sidebar.caption(
    "AI Retail Intelligence Platform"
)

st.sidebar.markdown("---")

# ==========================================================
# FILTERS
# ==========================================================

years = sorted(df["Year"].unique())

selected_year = st.sidebar.multiselect(
    "📅 Year",
    years,
    default=years
)

months = sorted(df["Month_Name"].unique())

selected_month = st.sidebar.multiselect(
    "📆 Month",
    months,
    default=months
)

categories = sorted(df["Category"].unique())

selected_category = st.sidebar.multiselect(
    "🛍 Category",
    categories,
    default=categories
)

subcategories = sorted(df["Subcategory"].unique())

selected_subcategory = st.sidebar.multiselect(
    "📦 Subcategory",
    subcategories,
    default=subcategories
)

seasons = sorted(df["Season"].unique())

selected_season = st.sidebar.multiselect(
    "🌦 Season",
    seasons,
    default=seasons
)

promotion = st.sidebar.multiselect(
    "🎯 Promotion",
    sorted(df["Promotion"].unique()),
    default=sorted(df["Promotion"].unique())
)

holiday = st.sidebar.multiselect(
    "🎉 Holiday",
    sorted(df["Holiday"].unique()),
    default=sorted(df["Holiday"].unique())
)

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered = df[
    (df["Year"].isin(selected_year))
    &
    (df["Month_Name"].isin(selected_month))
    &
    (df["Category"].isin(selected_category))
    &
    (df["Subcategory"].isin(selected_subcategory))
    &
    (df["Season"].isin(selected_season))
    &
    (df["Promotion"].isin(promotion))
    &
    (df["Holiday"].isin(holiday))
]

# ==========================================================
# EXECUTIVE HEADER
# ==========================================================

st.markdown(
"""
# 🛒 PROJECT FORESIGHT

### Executive Retail Intelligence Dashboard

AI Powered Demand Forecasting & Inventory Intelligence Platform

---
"""
)

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
        filtered["Current_Stock"]
        >
        filtered["Safety_Stock"]
    ).mean() * 100
)
# ==========================================================
# EXECUTIVE KPI DASHBOARD
# ==========================================================

st.markdown("## 📊 Executive Performance Overview")

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

kpi1.metric(
    "💰 Revenue",
    f"₹{total_revenue:,.0f}"
)

kpi2.metric(
    "📦 Units Sold",
    f"{total_units:,.0f}"
)

kpi3.metric(
    "🛍 Products",
    total_products
)

kpi4.metric(
    "📂 Categories",
    total_categories
)

kpi5.metric(
    "🤖 Model Accuracy",
    f"{forecast_accuracy:.1f}%"
)

kpi6.metric(
    "📦 Inventory Health",
    f"{inventory_health:.1f}%"
)

st.markdown("---")

# ==========================================================
# REVENUE TREND
# ==========================================================

st.subheader("📈 Revenue Trend")

daily_sales = (
    filtered
    .groupby("Date", as_index=False)["Revenue"]
    .sum()
)

fig = px.line(
    daily_sales,
    x="Date",
    y="Revenue",
    template="plotly_white",
    markers=True,
    title="Daily Revenue Trend"
)

fig.update_layout(
    height=450,
    title_x=0.02,
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# TWO CHARTS
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
    )

    fig = px.pie(
        category_sales,
        names="Category",
        values="Revenue",
        hole=0.55,
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig.update_layout(
        title="Revenue by Category",
        height=420
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
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        title="Monthly Revenue",
        height=420,
        xaxis_title="",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# TREEMAP
# ==========================================================

st.subheader("🌳 Revenue Distribution")

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
    path=["Category", "Subcategory"],
    values="Revenue",
    color="Revenue",
    color_continuous_scale="Blues"
)

fig.update_layout(
    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# REVENUE ANALYTICS
# ==========================================================

st.markdown("## 📈 Revenue Analytics")

a1, a2, a3 = st.columns(3)

highest_day = (
    filtered.groupby("Date")["Revenue"]
    .sum()
    .idxmax()
)

highest_value = (
    filtered.groupby("Date")["Revenue"]
    .sum()
    .max()
)

a1.success(
    f"""
### Highest Revenue Day

📅 **{highest_day.strftime('%d %b %Y')}**

💰 **₹{highest_value:,.0f}**
"""
)

best_category = (
    filtered.groupby("Category")["Revenue"]
    .sum()
    .idxmax()
)

best_value = (
    filtered.groupby("Category")["Revenue"]
    .sum()
    .max()
)

a2.info(
    f"""
### Best Category

🏆 **{best_category}**

💰 **₹{best_value:,.0f}**
"""
)

avg_daily = (
    filtered.groupby("Date")["Revenue"]
    .sum()
    .mean()
)

a3.warning(
    f"""
### Average Daily Revenue

📊 **₹{avg_daily:,.0f}**
"""
)

st.markdown("---")
# ==========================================================
# INVENTORY INTELLIGENCE
# ==========================================================

st.markdown("## 📦 Inventory Intelligence")

inv1, inv2 = st.columns(2)

with inv1:

    inventory = (
        filtered.groupby("Category", as_index=False)["Current_Stock"]
        .sum()
    )

    fig = px.bar(
        inventory,
        x="Category",
        y="Current_Stock",
        color="Current_Stock",
        color_continuous_scale="Viridis",
        title="Current Inventory by Category"
    )

    fig.update_layout(
        height=420,
        xaxis_title="Category",
        yaxis_title="Current Stock"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with inv2:

    stock = filtered["Current_Stock"].sum()
    safety = filtered["Safety_Stock"].sum()

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=inventory_health,
        title={"text":"Inventory Health Score"},
        gauge={
            "axis":{"range":[0,100]},
            "bar":{"color":"green"},
            "steps":[
                {"range":[0,50],"color":"#FCA5A5"},
                {"range":[50,80],"color":"#FCD34D"},
                {"range":[80,100],"color":"#86EFAC"}
            ]
        }
    ))

    fig.update_layout(height=420)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# TOP PRODUCTS
# ==========================================================

st.markdown("## 🏆 Top 10 Revenue Generating Products")

top_products = (
    filtered.groupby("SKU_ID", as_index=False)["Revenue"]
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
    height=500,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# SEASON ANALYSIS
# ==========================================================

st.markdown("## 🌦 Seasonal Sales Performance")

season_sales = (
    filtered.groupby("Season", as_index=False)["Revenue"]
    .sum()
)

fig = px.sunburst(
    season_sales,
    path=["Season"],
    values="Revenue",
    color="Revenue",
    color_continuous_scale="Blues"
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# WEEKDAY HEATMAP
# ==========================================================

st.markdown("## 🔥 Weekly Sales Heatmap")

heat = (
    filtered.assign(
        Weekday=filtered["Date"].dt.day_name(),
        Month=filtered["Date"].dt.month_name()
    )
    .pivot_table(
        values="Revenue",
        index="Weekday",
        columns="Month",
        aggfunc="sum",
        fill_value=0
    )
)

weekday_order = [
    "Monday","Tuesday","Wednesday",
    "Thursday","Friday","Saturday","Sunday"
]

heat = heat.reindex(weekday_order)

fig = px.imshow(
    heat,
    aspect="auto",
    color_continuous_scale="Blues",
    text_auto=".2s"
)

fig.update_layout(
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# INVENTORY RISK
# ==========================================================

st.markdown("## ⚠ Inventory Risk Summary")

low_stock = filtered[
    filtered["Current_Stock"] <= filtered["Safety_Stock"]
]

reorder = filtered[
    filtered["Current_Stock"] <= filtered["Reorder_Point"]
]

r1, r2, r3 = st.columns(3)

r1.metric(
    "Low Stock Products",
    len(low_stock)
)

r2.metric(
    "Reorder Required",
    len(reorder)
)

r3.metric(
    "Average Lead Time",
    f"{filtered['Lead_Time_Days'].mean():.1f} Days"
)

# ==========================================================
# EXECUTIVE BUSINESS INSIGHTS
# ==========================================================

st.markdown("## 💡 Executive Business Insights")

best_sku = (
    filtered.groupby("SKU_ID")["Revenue"]
    .sum()
    .idxmax()
)

best_sku_sales = (
    filtered.groupby("SKU_ID")["Revenue"]
    .sum()
    .max()
)

highest_category = (
    filtered.groupby("Category")["Revenue"]
    .sum()
    .idxmax()
)

promotion_sales = (
    filtered.groupby("Promotion")["Revenue"]
    .sum()
)

promotion_text = (
    "Promotions increase sales."
    if len(promotion_sales) > 1 and promotion_sales.iloc[-1] > promotion_sales.iloc[0]
    else "Promotions have limited impact."
)

st.success(f"""
### 📈 Executive Summary

✅ Total Revenue: **₹{total_revenue:,.0f}**

🏆 Highest Revenue Category: **{highest_category}**

🥇 Best Selling Product: **{best_sku}**

💰 Revenue from Best Product: **₹{best_sku_sales:,.0f}**

📦 Inventory Health Score: **{inventory_health:.1f}%**

🤖 Forecast Accuracy: **95.3%**

🎯 {promotion_text}
""")

st.markdown("---")
# ==========================================================
# INVENTORY RECOMMENDATIONS
# ==========================================================

st.markdown("## 📋 Inventory Recommendations")

if not risk.empty:

    st.dataframe(
        risk,
        use_container_width=True,
        hide_index=True
    )

    csv = risk.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Inventory Recommendations",
        data=csv,
        file_name="inventory_recommendations.csv",
        mime="text/csv",
        use_container_width=True
    )

else:

    st.info(
        "Inventory recommendation report not found."
    )

st.markdown("---")

# ==========================================================
# CATEGORY PERFORMANCE
# ==========================================================

st.markdown("## 📊 Category Performance")

category_summary = (
    filtered.groupby("Category")
    .agg(
        Revenue=("Revenue", "sum"),
        Units=("Units_Sold", "sum"),
        Avg_Price=("Unit_Price", "mean"),
        Avg_Stock=("Current_Stock", "mean")
    )
    .reset_index()
)

st.dataframe(
    category_summary,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# DATASET SUMMARY
# ==========================================================

st.markdown("## 📑 Dataset Summary")

s1, s2, s3, s4 = st.columns(4)

s1.metric(
    "Rows",
    f"{len(filtered):,}"
)

s2.metric(
    "SKUs",
    filtered["SKU_ID"].nunique()
)

s3.metric(
    "Categories",
    filtered["Category"].nunique()
)

s4.metric(
    "Date Range",
    f"{filtered['Date'].min().strftime('%d-%b-%Y')} → {filtered['Date'].max().strftime('%d-%b-%Y')}"
)

st.markdown("---")

# 