import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

df = pd.read_csv(DATA / "subscriber_churn_dataset.csv")

st.set_page_config(
    page_title="Netflix-Style Executive Dashboard",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0B0F19;
        color: #F9FAFB;
    }
    div[data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #334155;
        padding: 18px;
        border-radius: 16px;
    }
    h1, h2, h3 {
        color: #F9FAFB;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎬 Netflix-Style Executive Dashboard")
st.write("Streaming subscriber analytics focused on churn, retention, engagement, and platform performance.")

# Sidebar filters
st.sidebar.header("Filters")

plan_filter = st.sidebar.multiselect(
    "Subscription Plan",
    options=sorted(df["subscription_plan"].unique()),
    default=sorted(df["subscription_plan"].unique())
)

region_filter = st.sidebar.multiselect(
    "Region",
    options=sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

device_filter = st.sidebar.multiselect(
    "Device",
    options=sorted(df["device"].unique()),
    default=sorted(df["device"].unique())
)

filtered = df[
    (df["subscription_plan"].isin(plan_filter)) &
    (df["region"].isin(region_filter)) &
    (df["device"].isin(device_filter))
]

# KPI cards
total_subscribers = len(filtered)
churn_rate = filtered["churn"].mean()
retention_rate = 1 - churn_rate
avg_watch_minutes = filtered["watch_minutes"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Subscribers", f"{total_subscribers:,}")
col2.metric("Churn Rate", f"{churn_rate:.2%}")
col3.metric("Retention Rate", f"{retention_rate:.2%}")
col4.metric("Avg Watch Minutes", f"{avg_watch_minutes:.1f}")

st.divider()

# Charts
c1, c2 = st.columns(2)

with c1:
    churn_by_plan = filtered.groupby("subscription_plan")["churn"].mean().reset_index()
    fig = px.bar(
        churn_by_plan,
        x="subscription_plan",
        y="churn",
        title="Churn Rate by Subscription Plan",
        color_discrete_sequence=["#E50914"]
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    churn_by_device = filtered.groupby("device")["churn"].mean().reset_index()
    fig = px.bar(
        churn_by_device,
        x="device",
        y="churn",
        title="Churn Rate by Device",
        color_discrete_sequence=["#38BDF8"]
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    churn_by_region = filtered.groupby("region")["churn"].mean().reset_index()
    fig = px.bar(
        churn_by_region,
        x="region",
        y="churn",
        title="Churn Rate by Region",
        color_discrete_sequence=["#22C55E"]
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    fig = px.scatter(
        filtered,
        x="watch_minutes",
        y="days_inactive",
        color="churn",
        title="Watch Minutes vs Days Inactive",
        color_continuous_scale=["#22C55E", "#E50914"]
    )
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Executive Summary")
st.write(
    """
    This dashboard simulates a streaming executive analytics view used to monitor subscriber churn,
    retention, engagement behavior, and platform performance. Users with higher inactivity and lower
    watch minutes are more likely to churn, making engagement recovery campaigns a key recommendation.
    """
)
