import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Inventory | Project FORESIGHT",
    page_icon="📦",
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
# PAGE TITLE
# ==========================================================

st.title("📦 Inventory Intelligence Dashboard")

st.caption(
    "AI Powered Inventory Monitoring & Stock Optimization"
)

st.divider()

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Inventory Filters")

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

season = st.sidebar.multiselect(
    "Season",
    sorted(df["Season"].unique()),
    default=sorted(df["Season"].unique())
)

filtered = df[
    (df["Category"].isin(category))
    &
    (df["Season"].isin(season))
]

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_stock = filtered["Current_Stock"].sum()

safety_stock = filtered["Safety_Stock"].sum()

reorder_stock = filtered["Reorder_Point"].sum()

avg_lead = filtered["Lead_Time_Days"].mean()

inventory_health = (
    (
        filtered["Current_Stock"] >
        filtered["Safety_Stock"]
    ).mean() * 100
)

# ==========================================================
# KPI CARDS
# ==========================================================

st.markdown("## 📊 Inventory KPIs")

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "📦 Current Stock",
    f"{total_stock:,.0f}"
)

k2.metric(
    "🛡 Safety Stock",
    f"{safety_stock:,.0f}"
)

k3.metric(
    "🔄 Reorder Point",
    f"{reorder_stock:,.0f}"
)

k4.metric(
    "🚚 Avg Lead Time",
    f"{avg_lead:.1f} Days"
)

k5.metric(
    "✅ Health Score",
    f"{inventory_health:.1f}%"
)

st.divider()
# ==========================================================
# INVENTORY BY CATEGORY
# ==========================================================

st.markdown("## 📦 Inventory Distribution")

left, right = st.columns(2)

# ----------------------------------------------------------
# Current Inventory by Category
# ----------------------------------------------------------

with left:

    inventory = (
        filtered
        .groupby("Category", as_index=False)["Current_Stock"]
        .sum()
        .sort_values("Current_Stock", ascending=False)
    )

    fig = px.bar(
        inventory,
        x="Category",
        y="Current_Stock",
        color="Current_Stock",
        color_continuous_scale="Viridis",
        text_auto=".2s",
        title="Current Inventory by Category"
    )

    fig.update_layout(
        height=450,
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

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=inventory_health,
            number={"suffix":"%"},
            title={"text":"Inventory Health"},
            gauge={
                "axis":{"range":[0,100]},
                "bar":{"color":"royalblue"},
                "steps":[
                    {"range":[0,40],"color":"#EF4444"},
                    {"range":[40,70],"color":"#FACC15"},
                    {"range":[70,100],"color":"#22C55E"}
                ]
            }
        )
    )

    gauge.update_layout(height=450)

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

st.divider()

# ==========================================================
# STOCK VS SAFETY STOCK
# ==========================================================

st.markdown("## 🛡 Stock vs Safety Stock")

stock_compare = (
    filtered.groupby("Category", as_index=False)
    .agg(
        Current_Stock=("Current_Stock","sum"),
        Safety_Stock=("Safety_Stock","sum")
    )
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        name="Current Stock",
        x=stock_compare["Category"],
        y=stock_compare["Current_Stock"]
    )
)

fig.add_trace(
    go.Bar(
        name="Safety Stock",
        x=stock_compare["Category"],
        y=stock_compare["Safety_Stock"]
    )
)

fig.update_layout(
    barmode="group",
    height=500,
    title="Current Stock vs Safety Stock"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# REORDER ANALYSIS
# ==========================================================

st.markdown("## 🔄 Reorder Point Analysis")

reorder = (
    filtered.groupby("Category", as_index=False)
    .agg(
        Current_Stock=("Current_Stock","sum"),
        Reorder_Point=("Reorder_Point","sum")
    )
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=reorder["Category"],
        y=reorder["Current_Stock"],
        mode="lines+markers",
        name="Current Stock"
    )
)

fig.add_trace(
    go.Scatter(
        x=reorder["Category"],
        y=reorder["Reorder_Point"],
        mode="lines+markers",
        name="Reorder Point"
    )
)

fig.update_layout(
    height=500,
    title="Current Stock vs Reorder Point"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# STOCK STATUS
# ==========================================================

low_stock = filtered[
    filtered["Current_Stock"] <= filtered["Safety_Stock"]
]

reorder_required = filtered[
    filtered["Current_Stock"] <= filtered["Reorder_Point"]
]

c1, c2, c3 = st.columns(3)

c1.metric(
    "⚠ Low Stock Items",
    len(low_stock)
)

c2.metric(
    "📦 Reorder Required",
    len(reorder_required)
)

c3.metric(
    "🏪 Total Products",
    filtered["SKU_ID"].nunique()
)

st.divider()
# ==========================================================
# TOP PRODUCTS BY INVENTORY
# ==========================================================

st.markdown("## 🏆 Top Products by Current Stock")

top_inventory = (
    filtered.groupby("SKU_ID", as_index=False)
    .agg(
        Current_Stock=("Current_Stock", "sum"),
        Revenue=("Revenue", "sum")
    )
    .sort_values("Current_Stock", ascending=False)
    .head(10)
)

fig = px.bar(
    top_inventory,
    x="Current_Stock",
    y="SKU_ID",
    orientation="h",
    color="Revenue",
    color_continuous_scale="Turbo",
    text_auto=".2s",
    title="Top 10 Products by Inventory"
)

fig.update_layout(
    height=500,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# INVENTORY TREND
# ==========================================================

st.markdown("## 📈 Inventory Trend")

inventory_trend = (
    filtered.groupby("Date", as_index=False)
    .agg(
        Current_Stock=("Current_Stock", "sum")
    )
)

fig = px.line(
    inventory_trend,
    x="Date",
    y="Current_Stock",
    markers=True,
    title="Daily Inventory Trend",
    template="plotly_white"
)

fig.update_layout(
    height=450,
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# SEASONAL INVENTORY ANALYSIS
# ==========================================================

left, right = st.columns(2)

with left:

    season_inventory = (
        filtered.groupby("Season", as_index=False)
        .agg(
            Current_Stock=("Current_Stock", "sum")
        )
    )

    fig = px.pie(
        season_inventory,
        names="Season",
        values="Current_Stock",
        hole=0.60,
        title="Inventory Distribution by Season",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(height=420)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    lead_time = (
        filtered.groupby("Category", as_index=False)
        .agg(
            Lead_Time=("Lead_Time_Days", "mean")
        )
    )

    fig = px.bar(
        lead_time,
        x="Category",
        y="Lead_Time",
        color="Lead_Time",
        color_continuous_scale="Oranges",
        text_auto=".1f",
        title="Average Lead Time by Category"
    )

    fig.update_layout(height=420)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================================
# INVENTORY HEATMAP
# ==========================================================

st.markdown("## 🔥 Inventory Heatmap")

heat = (
    filtered.assign(
        Month=filtered["Date"].dt.month_name()
    )
    .pivot_table(
        values="Current_Stock",
        index="Category",
        columns="Month",
        aggfunc="mean",
        fill_value=0
    )
)

month_order = [
    "January","February","March","April",
    "May","June","July","August",
    "September","October","November","December"
]

existing_months = [m for m in month_order if m in heat.columns]
heat = heat[existing_months]

fig = px.imshow(
    heat,
    aspect="auto",
    color_continuous_scale="Blues",
    text_auto=".0f"
)

fig.update_layout(
    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True
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

    st.success("🎉 Great! No products currently require replenishment.")

else:

    recommendation_columns = [
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
        col for col in recommendation_columns
        if col in recommendations.columns
    ]

    st.dataframe(
        recommendations[available_columns],
        use_container_width=True,
        hide_index=True
    )

    csv = recommendations[available_columns].to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Inventory Report",
        data=csv,
        file_name="inventory_recommendations.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()

# ==========================================================
# CATEGORY INVENTORY SUMMARY
# ==========================================================

st.markdown("## 📊 Category Inventory Summary")

summary = (
    filtered.groupby("Category")
    .agg(
        Current_Stock=("Current_Stock", "sum"),
        Safety_Stock=("Safety_Stock", "sum"),
        Reorder_Point=("Reorder_Point", "sum"),
        Avg_Lead_Time=("Lead_Time_Days", "mean"),
        Revenue=("Revenue", "sum")
    )
    .reset_index()
)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==========================================================
# DATASET SUMMARY
# ==========================================================

st.markdown("## 📑 Inventory Dataset Summary")

d1, d2, d3, d4 = st.columns(4)

d1.metric(
    "Products",
    filtered["SKU_ID"].nunique()
)

d2.metric(
    "Categories",
    filtered["Category"].nunique()
)

d3.metric(
    "Total Records",
    f"{len(filtered):,}"
)

d4.metric(
    "Average Stock",
    f"{filtered['Current_Stock'].mean():.1f}"
)

st.divider()

# ==========================================================
# INVENTORY STATUS
# ==========================================================

st.markdown("## 📈 Inventory Status")

healthy = len(
    filtered[
        filtered["Current_Stock"] > filtered["Safety_Stock"]
    ]
)

warning = len(
    filtered[
        (filtered["Current_Stock"] <= filtered["Safety_Stock"]) &
        (filtered["Current_Stock"] > filtered["Reorder_Point"])
    ]
)

critical = len(
    filtered[
        filtered["Current_Stock"] <= filtered["Reorder_Point"]
    ]
)

status = pd.DataFrame(
    {
        "Status": [
            "Healthy",
            "Warning",
            "Critical"
        ],
        "Products": [
            healthy,
            warning,
            critical
        ]
    }
)

fig = px.pie(
    status,
    names="Status",
    values="Products",
    hole=0.55,
    color="Status",
    color_discrete_map={
        "Healthy": "#22C55E",
        "Warning": "#FACC15",
        "Critical": "#EF4444"
    },
    title="Inventory Status Distribution"
)

fig.update_layout(height=450)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()
