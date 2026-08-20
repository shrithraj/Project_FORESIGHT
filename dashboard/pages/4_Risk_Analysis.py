import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Risk Analysis | Project FORESIGHT",
    page_icon="⚠️",
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
df["Risk"] = "Balanced"

df.loc[
    df["Current_Stock"] <= df["Safety_Stock"],
    "Risk"
] = "Stockout Risk"

df.loc[
    df["Current_Stock"] > df["Reorder_Point"] * 2,
    "Risk"
] = "Overstock Risk"

risk = df


# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("⚠️ Inventory Risk Intelligence Dashboard")

st.caption(
    "AI Powered Stock Risk Monitoring & Inventory Intelligence"
)

st.divider()

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Risk Filters")

risk_filter = st.sidebar.multiselect(
    "Risk Level",
    sorted(risk["Risk"].unique()),
    default=sorted(risk["Risk"].unique())
)

filtered = risk[
    risk["Risk"].isin(risk_filter)
].copy()

stockout = len(filtered[filtered["Risk"] == "Stockout Risk"])
balanced = len(filtered[filtered["Risk"] == "Balanced"])
overstock = len(filtered[filtered["Risk"] == "Overstock Risk"])

total_products = filtered["SKU_ID"].nunique()

if "Current_Stock" in filtered.columns:
    avg_current_stock = filtered["Current_Stock"].mean()
else:
    avg_current_stock = 0

if "Current_Stock" in filtered.columns:
    avg_current_stock = filtered["Current_Stock"].mean()
else:
    avg_current_stock = 0

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

stockout = len(
    filtered[
        filtered["Risk"] == "Stockout Risk"
    ]
)

balanced = len(
    filtered[
        filtered["Risk"] == "Balanced"
    ]
)

overstock = len(
    filtered[
        filtered["Risk"] == "Overstock Risk"
    ]
)

total_products = filtered["SKU_ID"].nunique()

if "Current_Stock" in filtered.columns:
    avg_current_stock = filtered["Current_Stock"].mean()
else:
    avg_current_stock = 0

risk_score = (
    (
        balanced /
        max(len(filtered), 1)
    ) * 100
)
# ==========================================================
# EXECUTIVE KPI DASHBOARD
# ==========================================================

st.markdown("## 📊 Executive Risk KPIs")

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric(
    "🔴 Stockout",
    stockout
)

k2.metric(
    "🟡 Balanced",
    balanced
)

k3.metric(
    "🟢 Overstock",
    overstock
)

k4.metric(
    "📦 Products",
    total_products
)

k5.metric(
    "📈 Avg Current Stock",
    f"{avg_current_stock:.1f}"
)

st.divider()

# ==========================================================
# RISK SCORE
# ==========================================================

st.markdown("## 🎯 Inventory Risk Score")

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=risk_score,
        number={"suffix":"%"},
        title={"text":"Inventory Health Score"},
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

fig.update_layout(height=350)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()
# ==========================================================
# RISK DISTRIBUTION
# ==========================================================

st.markdown("## 📊 Risk Distribution")

left, right = st.columns(2)

# ----------------------------------------------------------
# Risk Distribution
# ----------------------------------------------------------

with left:

    fig = px.pie(
        filtered,
        names="Risk",
        hole=0.60,
        color="Risk",
        color_discrete_map={
            "Stockout Risk": "#EF4444",
            "Balanced": "#FACC15",
            "Overstock Risk": "#22C55E"
        },
        title="Inventory Risk Distribution"
    )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------------------------
# Units Sold Distribution
# ----------------------------------------------------------

with right:

    fig = px.histogram(
    filtered,
    x="Units_Sold",
    nbins=25,
    color="Risk",
    title="Units Sold Distribution",
    color_discrete_map={
        "Stockout Risk":"#EF4444",
        "Balanced":"#FACC15",
        "Overstock Risk":"#22C55E"
    }
)

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================================
# TOP Current Stock PRODUCTS
# ==========================================================

st.markdown("## 📈 Top Best Selling  Products")

top20 = (
    filtered
    .sort_values(
    "Units_Sold",
    ascending=False
)
    .head(20)
)

fig = px.bar(
    top20,
    x="SKU_ID",
    y="Units_Sold",
    color="Risk",
    text_auto=".2f",
    color_discrete_map={
        "Stockout Risk":"#EF4444",
        "Balanced":"#FACC15",
        "Overstock Risk":"#22C55E"
    },
    title="Top 20 Best Selling  Products"
)

fig.update_layout(
    height=500,
    xaxis_title="Product",
    yaxis_title="Current Stock"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# RISK BY CATEGORY
# ==========================================================

if "Category" in filtered.columns:

    st.markdown("## 📦 Category Risk Analysis")

    category_risk = (
        filtered
        .groupby(
            ["Category","Risk"]
        )
        .size()
        .reset_index(name="Products")
    )

    fig = px.bar(
        category_risk,
        x="Category",
        y="Products",
        color="Risk",
        barmode="group",
        title="Risk Distribution by Category",
        color_discrete_map={
            "Stockout Risk":"#EF4444",
            "Balanced":"#FACC15",
            "Overstock Risk":"#22C55E"
        }
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()



# ==========================================================
# CURRENT STOCK VS UNITS SOLD
# ==========================================================

if "Current_Stock" in filtered.columns:

    st.markdown("## 📉 Current Stock vs Units Sold")

    compare = (
        filtered
        .sort_values(
            "Units_Sold",
            ascending=False
        )
        .head(25)
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=compare["SKU_ID"],
            y=compare["Current_Stock"],
            name="Current Stock"
        )
    )

    fig.add_trace(
        go.Bar(
            x=compare["SKU_ID"],
            y=compare["Units_Sold"],
            name="Units Sold"
        )
    )

    fig.update_layout(
        barmode="group",
        height=500,
        title="Current Stock vs Units Sold",
        xaxis_title="SKU ID",
        yaxis_title="Quantity"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

st.divider()
# ==========================================================
# MONTHLY RISK TREND
# ==========================================================

if "Date" in filtered.columns:

    st.markdown("## 📅 Monthly Risk Trend")

    temp = filtered.copy()

    temp["Date"] = pd.to_datetime(temp["Date"])

    monthly = (
        temp.groupby(
            [temp["Date"].dt.to_period("M").astype(str), "Risk"]
        )
        .size()
        .reset_index(name="Products")
    )

    monthly.rename(
        columns={"Date": "Month"},
        inplace=True
    )

    fig = px.line(
        monthly,
        x="Month",
        y="Products",
        color="Risk",
        markers=True,
        title="Monthly Inventory Risk Trend",
        color_discrete_map={
            "Stockout Risk": "#EF4444",
            "Balanced": "#FACC15",
            "Overstock Risk": "#22C55E"
        }
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
# RISK HEATMAP
# ==========================================================

if "Category" in filtered.columns:

    st.markdown("## 🔥 Risk Heatmap")

    heat = (
        filtered.groupby(
            ["Category", "Risk"]
        )
        .size()
        .reset_index(name="Count")
    )

    pivot = heat.pivot(
        index="Category",
        columns="Risk",
        values="Count"
    ).fillna(0)

    fig = px.imshow(
        pivot,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================================
# STOCKOUT ANALYSIS
# ==========================================================

st.markdown("## 🔴 Stockout Analysis")

stockout_df = filtered[
    filtered["Risk"] == "Stockout Risk"
]

if not stockout_df.empty:

    top_stockout = (
        stockout_df
        .sort_values(
            "Current_Stock",
            ascending=False
        )
        .head(15)
    )

    fig = px.bar(
        top_stockout,
        x="SKU_ID",
        y="Current Stock",
        color="Current Stock"   ,
        color_continuous_scale="Reds",
        text_auto=".1f",
        title="Highest Stockout Risk Products"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.success("No products are currently classified as Stockout Risk.")

st.divider()


# ==========================================================
# OVERSTOCK ANALYSIS
# ==========================================================

st.markdown("## 🟢 Overstock Analysis")

overstock_df = filtered[
    filtered["Risk"] == "Overstock Risk"
]

if not overstock_df.empty:

    # Use Forecast if available, otherwise Current Stock
    if "Current Stock" in overstock_df.columns:

        top_overstock = (
            overstock_df
            .sort_values("Current Stock", ascending=False)
            .head(15)
        )

        fig = px.bar(
            top_overstock,
            x="SKU_ID",
            y="Current Stock",
            color="Current Stock",
            color_continuous_scale="Greens",
            text_auto=".1f",
            title="Highest Overstock Products"
        )

    else:

        top_overstock = (
            overstock_df
            .sort_values("Current_Stock", ascending=False)
            .head(15)
        )

        fig = px.bar(
            top_overstock,
            x="SKU_ID",
            y="Current_Stock",
            color="Current_Stock",
            color_continuous_scale="Greens",
            text_auto=".1f",
            title="Highest Overstock Products"
        )

    fig.update_layout(height=450)

    st.plotly_chart(
        fig,
        width="stretch"
    )

else:

    st.success("✅ No products are currently classified as Overstock Risk.")

st.divider()
# ==========================================================
# INVENTORY RISK REPORT
# ==========================================================

st.markdown("## 📋 Inventory Risk Report")

display_columns = [
    "SKU_ID",
    "Risk",
    "Revenue",
    "Current_Stock",
    "Safety_Stock",
    "Reorder_Point"
]

available_columns = [
    col for col in display_columns
    if col in filtered.columns
]

st.dataframe(
    filtered[available_columns],
    use_container_width=True,
    hide_index=True,
    height=450
)

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Risk Report",
    data=csv,
    file_name="inventory_risk_report.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()

# ==========================================================
# DATASET SUMMARY
# ==========================================================

st.markdown("## 📊 Risk Dataset Summary")

d1, d2, d3, d4 = st.columns(4)

d1.metric(
    "Total Records",
    f"{len(filtered):,}"
)

d2.metric(
    "Products",
    filtered["SKU_ID"].nunique()
)

d3.metric(
    "Average Units Sold",
    f"{filtered['Units_Sold'].mean():.2f}"
)

d4.metric(
    "Inventory Health",
    f"{risk_score:.1f}%"
)

st.divider()

# ==========================================================
# RISK STATUS DASHBOARD
# ==========================================================

status = pd.DataFrame(
    {
        "Risk": [
            "Stockout Risk",
            "Balanced",
            "Overstock Risk"
        ],
        "Products": [
            stockout,
            balanced,
            overstock
        ]
    }
)

fig = px.bar(
    status,
    x="Risk",
    y="Products",
    color="Risk",
    text="Products",
    title="Inventory Risk Status",
    color_discrete_map={
        "Stockout Risk": "#EF4444",
        "Balanced": "#FACC15",
        "Overstock Risk": "#22C55E"
    }
)

fig.update_layout(
    height=450,
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

