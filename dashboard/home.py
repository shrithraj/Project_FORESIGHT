import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Project FORESIGHT",
    page_icon="📊",
    layout="wide"
)

st.title("📊 PROJECT FORESIGHT")
st.caption("AI Powered Retail Demand Forecasting & Inventory Intelligence Platform")

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

DATA = Path("data/processed/master_dataset.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

filtered = df[
    df["Category"].isin(category)
]

# --------------------------------------------------
# KPIs
# --------------------------------------------------

revenue = filtered["Revenue"].sum()
units = filtered["Units_Sold"].sum()
products = filtered["SKU_ID"].nunique()


c1,c2,c3 = st.columns(3)

c1.metric(
    "💰 Revenue",
    f"₹{revenue:,.0f}"
)

c2.metric(
    "📦 Units Sold",
    f"{units:,.0f}"
)

c3.metric(
    "🛒 Products",
    products
)



st.divider()

# --------------------------------------------------
# Revenue Trend
# --------------------------------------------------

daily = (
    filtered
    .groupby("Date",as_index=False)["Revenue"]
    .sum()
)

fig = px.line(
    daily,
    x="Date",
    y="Revenue",
    title="Daily Revenue Trend",
    template="plotly_dark"
)

fig.update_layout(height=420)

st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# Charts
# --------------------------------------------------

left,right = st.columns(2)

with left:

    cat = (
        filtered
        .groupby("Category")["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        cat,
        names="Category",
        values="Revenue",
        hole=.55,
        title="Revenue by Category",
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    month = (
        filtered
        .groupby(filtered["Date"].dt.month_name())["Revenue"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        month,
        x="Date",
        y="Revenue",
        color="Revenue",
        title="Monthly Revenue",
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)

st.divider()

# --------------------------------------------------
# Top Products
# --------------------------------------------------

st.subheader("🔥 Top 10 Products")

top = (
    filtered
    .groupby("SKU_ID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top,
    x="Revenue",
    y="SKU_ID",
    orientation="h",
    color="Revenue",
    template="plotly_dark"
)

st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# Sales Heatmap
# --------------------------------------------------

st.subheader("📅 Weekly Sales Pattern")

heat = (
    filtered.assign(
        Weekday=filtered["Date"].dt.day_name(),
        Month=filtered["Date"].dt.month_name()
    )
    .pivot_table(
        values="Revenue",
        index="Weekday",
        columns="Month",
        aggfunc="sum"
    )
)

fig = px.imshow(
    heat,
    aspect="auto",
    text_auto=True,
    template="plotly_dark"
)

fig.update_layout(height=500)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# --------------------------------------------------
# Latest Records
# --------------------------------------------------

st.subheader("📋 Latest Transactions")

st.dataframe(
    filtered.sort_values("Date",ascending=False).head(20),
    use_container_width=True
)
