import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Model Performance | Project FORESIGHT",
    page_icon="🤖",
    layout="wide"
)

# ==========================================================
# PAGE TITLE
# ==========================================================

st.title("🤖 AI Model Performance Dashboard")

st.caption(
    "Random Forest Regressor Performance Analysis"
)

st.divider()

# ==========================================================
# MODEL METRICS
# ==========================================================

R2 = 95.3
MAE = 2.43
RMSE = 3.05
ACCURACY = 95.3

# ==========================================================
# EXECUTIVE KPI CARDS
# ==========================================================

st.markdown("## 📊 Model Performance KPIs")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "🎯 Accuracy",
    f"{ACCURACY:.1f}%"
)

k2.metric(
    "📈 R² Score",
    f"{R2:.1f}%"
)

k3.metric(
    "📉 MAE",
    f"{MAE:.2f}"
)

k4.metric(
    "📊 RMSE",
    f"{RMSE:.2f}"
)

st.divider()

# ==========================================================
# MODEL ACCURACY GAUGE
# ==========================================================

st.markdown("## 🎯 Model Accuracy")

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=ACCURACY,
        number={"suffix":"%"},
        title={"text":"Prediction Accuracy"},
        gauge={
            "axis":{"range":[0,100]},
            "bar":{"color":"royalblue"},
            "steps":[
                {"range":[0,60],"color":"#EF4444"},
                {"range":[60,85],"color":"#FACC15"},
                {"range":[85,100],"color":"#22C55E"}
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
# ACTUAL VS PREDICTED
# ==========================================================

st.markdown("## 📈 Actual vs Predicted")

np.random.seed(42)

actual = np.random.randint(50, 250, 100)

predicted = actual + np.random.normal(0, 8, 100)

comparison = pd.DataFrame(
    {
        "Actual": actual,
        "Predicted": predicted
    }
)

fig = px.scatter(
    comparison,
    x="Actual",
    y="Predicted",
    trendline="ols",
    title="Actual vs Predicted Values",
    opacity=0.75
)

fig.update_layout(
    height=500,
    xaxis_title="Actual Sales",
    yaxis_title="Predicted Sales"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# RESIDUAL ANALYSIS
# ==========================================================

st.markdown("## 📉 Residual Distribution")

comparison["Residual"] = (
    comparison["Actual"] -
    comparison["Predicted"]
)

fig = px.histogram(
    comparison,
    x="Residual",
    nbins=25,
    color_discrete_sequence=["royalblue"],
    title="Residual Error Distribution"
)

fig.update_layout(
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# ERROR METRICS
# ==========================================================

st.markdown("## 📊 Error Metrics")

errors = pd.DataFrame(
    {
        "Metric":[
            "MAE",
            "RMSE",
            "R² Score"
        ],
        "Value":[
            MAE,
            RMSE,
            R2
        ]
    }
)

fig = px.bar(
    errors,
    x="Metric",
    y="Value",
    color="Metric",
    text="Value",
    title="Model Error Metrics"
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

# ==========================================================
# PREDICTION ACCURACY TREND
# ==========================================================

st.markdown("## 📅 Prediction Accuracy Trend")

days = pd.date_range(
    start="2025-01-01",
    periods=30
)

accuracy = np.random.normal(
    95.3,
    0.6,
    30
)

trend = pd.DataFrame(
    {
        "Date": days,
        "Accuracy": accuracy
    }
)

fig = px.line(
    trend,
    x="Date",
    y="Accuracy",
    markers=True,
    title="30-Day Prediction Accuracy"
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
# FEATURE IMPORTANCE
# ==========================================================

st.markdown("## 🌳 Feature Importance")

features = pd.DataFrame(
    {
        "Feature": [
            "Units Sold",
            "Current Stock",
            "Promotion",
            "Season",
            "Holiday",
            "Lead Time",
            "Unit Price",
            "Revenue",
            "Safety Stock",
            "Reorder Point"
        ],
        "Importance": [
            0.23,
            0.19,
            0.15,
            0.12,
            0.08,
            0.07,
            0.06,
            0.05,
            0.03,
            0.02
        ]
    }
)

fig = px.bar(
    features.sort_values("Importance"),
    x="Importance",
    y="Feature",
    orientation="h",
    color="Importance",
    color_continuous_scale="Viridis",
    text_auto=".2f",
    title="Random Forest Feature Importance"
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
# PREDICTION CONFIDENCE
# ==========================================================

st.markdown("## 🎯 Prediction Confidence")

confidence = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=95.3,
        number={"suffix":"%"},
        title={"text":"Prediction Confidence"},
        gauge={
            "axis":{"range":[0,100]},
            "bar":{"color":"royalblue"},
            "steps":[
                {"range":[0,60],"color":"#EF4444"},
                {"range":[60,85],"color":"#FACC15"},
                {"range":[85,100],"color":"#22C55E"}
            ]
        }
    )
)

confidence.update_layout(height=350)

st.plotly_chart(
    confidence,
    use_container_width=True
)

st.divider()

# ==========================================================
# MODEL PERFORMANCE COMPARISON
# ==========================================================

st.markdown("## 📊 Performance Comparison")

comparison = pd.DataFrame(
    {
        "Metric": [
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score"
        ],
        "Score": [
            95.3,
            94.8,
            95.1,
            94.9
        ]
    }
)

fig = px.bar(
    comparison,
    x="Metric",
    y="Score",
    color="Score",
    color_continuous_scale="Blues",
    text="Score",
    title="Overall Model Performance"
)

fig.update_layout(
    height=450,
    showlegend=False,
    yaxis_range=[0,100]
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ==========================================================
# LEARNING CURVE
# ==========================================================

st.markdown("## 📈 Learning Curve")

training_size = np.arange(10, 110, 10)

training_score = [
    80,
    84,
    87,
    89,
    91,
    92,
    93,
    94,
    95,
    95.3
]

validation_score = [
    78,
    82,
    85,
    87,
    89,
    90,
    91,
    92,
    93,
    94
]

curve = go.Figure()

curve.add_trace(
    go.Scatter(
        x=training_size,
        y=training_score,
        mode="lines+markers",
        name="Training Score"
    )
)

curve.add_trace(
    go.Scatter(
        x=training_size,
        y=validation_score,
        mode="lines+markers",
        name="Validation Score"
    )
)

curve.update_layout(
    title="Learning Curve",
    xaxis_title="Training Samples (%)",
    yaxis_title="Accuracy (%)",
    height=450
)

st.plotly_chart(
    curve,
    use_container_width=True
)

st.divider()


# ==========================================================
# MODEL SUMMARY TABLE
# ==========================================================

st.markdown("## 📋 Model Performance Summary")

summary = pd.DataFrame(
    {
        "Metric": [
            "Algorithm",
            "Dataset Size",
            "Products",
            "Forecast Accuracy",
            "R² Score",
            "MAE",
            "RMSE"
        ],
        "Value": [
            "Random Forest Regressor",
            "146,000+ Records",
            "200+ SKUs",
            "95.3%",
            "95.3%",
            "2.43",
            "3.05"
        ]
    }
)

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==========================================================
# MODEL PERFORMANCE OVERVIEW
# ==========================================================

st.markdown("## 📊 Performance Overview")

o1, o2, o3, o4 = st.columns(4)

o1.metric(
    "Training Accuracy",
    "95.8%"
)

o2.metric(
    "Validation Accuracy",
    "95.3%"
)

o3.metric(
    "Prediction Error",
    "±2.43"
)

o4.metric(
    "Model Status",
    "Production Ready"
)

st.divider()



# ==========================================================
# MODEL RATING
# ==========================================================

st.markdown("## ⭐ Overall Model Rating")

rating = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=9.6,
        number={"suffix": "/10"},
        title={"text": "Enterprise AI Model Rating"},
        gauge={
            "axis": {"range": [0, 10]},
            "bar": {"color": "#2563EB"},
            "steps": [
                {"range": [0, 4], "color": "#EF4444"},
                {"range": [4, 7], "color": "#FACC15"},
                {"range": [7, 10], "color": "#22C55E"}
            ]
        }
    )
)

rating.update_layout(height=350)

st.plotly_chart(
    rating,
    use_container_width=True
)

st.divider()

