import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="APL Logistics | Supply Chain Control Center",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv("APL_Logistics_Processed.csv")


df = load_data()


# =========================================================
# DATA PREPARATION
# =========================================================

completed_df = df[
    df["Delivery Status"] != "Shipping canceled"
].copy()


# =========================================================
# SIDEBAR — CONTROL PANEL
# =========================================================

st.sidebar.title("🚚 Control Panel")
st.sidebar.markdown("### Shipment Filters")


shipping_modes = sorted(
    completed_df["Shipping Mode"].dropna().unique()
)

selected_shipping_modes = st.sidebar.multiselect(
    "Shipping Mode",
    shipping_modes,
    default=shipping_modes
)


regions = sorted(
    completed_df["Order Region"].dropna().unique()
)

selected_regions = st.sidebar.multiselect(
    "Order Region",
    regions,
    default=regions
)


markets = sorted(
    completed_df["Market"].dropna().unique()
)

selected_markets = st.sidebar.multiselect(
    "Market",
    markets,
    default=markets
)


segments = sorted(
    completed_df["Customer Segment"].dropna().unique()
)

selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    segments,
    default=segments
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = completed_df[
    completed_df["Shipping Mode"].isin(selected_shipping_modes)
    & completed_df["Order Region"].isin(selected_regions)
    & completed_df["Market"].isin(selected_markets)
    & completed_df["Customer Segment"].isin(selected_segments)
].copy()


# =========================================================
# MAIN DASHBOARD HEADER
# =========================================================

st.title("🚚 APL Logistics")

st.subheader("Supply Chain Control Center")

st.markdown(
    """
    **Delivery Performance • Delay Risk • Logistics Efficiency**

    Monitor shipment performance, identify delay patterns,
    compare logistics operations, and explore regional risk hotspots.
    """
)

st.divider()


# =========================================================
# EXECUTIVE KPI SUMMARY
# =========================================================

total_shipments = len(filtered_df)

on_time_rate = (
    (filtered_df["Delivery Performance"] == "On-time").mean() * 100
    if len(filtered_df) > 0 else 0
)

late_risk_rate = (
    filtered_df["Late_delivery_risk"].mean() * 100
    if len(filtered_df) > 0 else 0
)

delayed_shipments = (
    filtered_df["Delivery Performance"] == "Delayed"
).sum()

average_delay = (
    filtered_df.loc[
        filtered_df["Delivery Performance"] == "Delayed",
        "Delay Gap"
    ].mean()
    if delayed_shipments > 0 else 0
)


# =========================================================
# KPI CARDS
# =========================================================

st.markdown("### 📊 Logistics Performance Snapshot")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Completed Shipments",
        f"{total_shipments:,}"
    )

with col2:
    st.metric(
        "On-Time Delivery",
        f"{on_time_rate:.2f}%"
    )

with col3:
    st.metric(
        "Late Delivery Risk",
        f"{late_risk_rate:.2f}%"
    )

with col4:
    st.metric(
        "Average Delay",
        f"{average_delay:.2f} days"
    )

st.divider()


# =========================================================
# FILTER STATUS
# =========================================================

st.caption(
    f"Showing {len(filtered_df):,} completed shipments "
    f"from {len(df):,} total records."
)


# =========================================================
# DELIVERY HEALTH
# =========================================================

st.markdown("## 🚚 Delivery Health")

st.markdown(
    "A high-level view of how completed shipments performed "
    "against their scheduled shipping duration."
)


delivery_order = [
    "Delayed",
    "On-time",
    "Early"
]

delivery_counts = (
    filtered_df["Delivery Performance"]
    .value_counts()
    .reindex(delivery_order, fill_value=0)
)


col1, col2 = st.columns(2)


with col1:

    st.markdown("### Delivery Performance")

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.bar(
        delivery_counts.index,
        delivery_counts.values
    )

    ax.set_xlabel("Performance")
    ax.set_ylabel("Number of Shipments")
    ax.set_title("Shipment Performance Distribution")

    plt.tight_layout()

    st.pyplot(fig)


with col2:

    st.markdown("### Delay Gap Distribution")

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.hist(
        filtered_df["Delay Gap"],
        bins=30
    )

    ax.axvline(
        0,
        linestyle="--",
        linewidth=2
    )

    ax.set_xlabel("Delay Gap (Days)")
    ax.set_ylabel("Number of Shipments")
    ax.set_title("Actual vs Scheduled Shipping Duration")

    plt.tight_layout()

    st.pyplot(fig)


st.divider()


# =========================================================
# SHIPPING MODE PERFORMANCE
# =========================================================

st.markdown("## 🚢 Shipping Mode Performance")

st.markdown(
    "Compare transportation modes using shipment volume, "
    "on-time performance, and delay intensity."
)


mode_summary = (
    filtered_df.groupby("Shipping Mode")
    .agg(
        Shipments=("Delivery Performance", "count"),
        On_Time_Rate=(
            "Delivery Performance",
            lambda x: (x == "On-time").mean() * 100
        ),
        Delayed_Rate=(
            "Delivery Performance",
            lambda x: (x == "Delayed").mean() * 100
        ),
        Average_Delay=(
            "Delay Gap",
            lambda x: x[x > 0].mean()
        )
    )
    .reset_index()
)

mode_summary["Average_Delay"] = (
    mode_summary["Average_Delay"].fillna(0)
)

mode_summary = mode_summary.sort_values(
    "Delayed_Rate",
    ascending=False
)


mode_summary_display = mode_summary.copy()

mode_summary_display["On_Time_Rate"] = (
    mode_summary_display["On_Time_Rate"].round(2)
)

mode_summary_display["Delayed_Rate"] = (
    mode_summary_display["Delayed_Rate"].round(2)
)

mode_summary_display["Average_Delay"] = (
    mode_summary_display["Average_Delay"].round(2)
)


col1, col2 = st.columns(2)


with col1:

    st.markdown("### On-Time Delivery by Shipping Mode")

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.bar(
        mode_summary["Shipping Mode"],
        mode_summary["On_Time_Rate"]
    )

    ax.set_xlabel("Shipping Mode")
    ax.set_ylabel("On-Time Rate (%)")
    ax.set_title("On-Time Delivery Rate")

    plt.xticks(rotation=25)

    plt.tight_layout()

    st.pyplot(fig)


with col2:

    st.markdown("### Delay Rate by Shipping Mode")

    fig, ax = plt.subplots(figsize=(7, 4))

    ax.bar(
        mode_summary["Shipping Mode"],
        mode_summary["Delayed_Rate"]
    )

    ax.set_xlabel("Shipping Mode")
    ax.set_ylabel("Delayed Rate (%)")
    ax.set_title("Delayed Shipment Rate")

    plt.xticks(rotation=25)

    plt.tight_layout()

    st.pyplot(fig)


st.markdown("### Shipping Mode Performance Details")

st.dataframe(
    mode_summary_display,
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# REGIONAL RISK ANALYSIS
# =========================================================

st.markdown("## 🌍 Regional Risk Analysis")

st.markdown(
    "Examine delivery delays across geographical regions "
    "using delay rate, average delay, shipment volume, "
    "and the Regional Delay Index."
)


overall_delay_rate = (
    (filtered_df["Delivery Performance"] == "Delayed").mean() * 100
    if len(filtered_df) > 0 else 0
)


regional_summary = (
    filtered_df.groupby("Order Region")
    .agg(
        Shipments=("Delivery Performance", "count"),
        Average_Delay=("Delay Gap", "mean"),
        Maximum_Delay=("Delay Gap", "max"),
        Delayed_Shipments=(
            "Delivery Performance",
            lambda x: (x == "Delayed").sum()
        )
    )
    .reset_index()
)


regional_summary["Delay_Rate_%"] = (
    regional_summary["Delayed_Shipments"]
    / regional_summary["Shipments"]
    * 100
)


regional_summary["Regional_Delay_Index"] = (
    regional_summary["Delay_Rate_%"]
    / overall_delay_rate
    if overall_delay_rate > 0 else 0
)


regional_summary = regional_summary.sort_values(
    "Delay_Rate_%",
    ascending=False
)


st.markdown("### Regional Delay Rate")

fig, ax = plt.subplots(figsize=(11, 6))

regional_chart = regional_summary.sort_values(
    "Delay_Rate_%"
)

ax.barh(
    regional_chart["Order Region"],
    regional_chart["Delay_Rate_%"]
)

ax.set_xlabel("Delayed Shipment Rate (%)")
ax.set_ylabel("Order Region")
ax.set_title("Delayed Shipment Rate by Region")

plt.tight_layout()

st.pyplot(fig)


st.markdown("### Regional Delay Index")

regional_display = regional_summary[
    [
        "Order Region",
        "Shipments",
        "Average_Delay",
        "Delay_Rate_%",
        "Regional_Delay_Index"
    ]
].copy()


regional_display["Average_Delay"] = (
    regional_display["Average_Delay"].round(2)
)

regional_display["Delay_Rate_%"] = (
    regional_display["Delay_Rate_%"].round(2)
)

regional_display["Regional_Delay_Index"] = (
    regional_display["Regional_Delay_Index"].round(2)
)


st.dataframe(
    regional_display,
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# MARKET PERFORMANCE
# =========================================================

st.markdown("## 🌐 Market Performance")

st.markdown(
    "Compare delivery delay patterns across major markets "
    "to identify differences in logistics performance."
)


market_summary = (
    filtered_df.groupby("Market")
    .agg(
        Shipments=("Delivery Performance", "count"),
        Average_Delay=("Delay Gap", "mean"),
        Delayed_Shipments=(
            "Delivery Performance",
            lambda x: (x == "Delayed").sum()
        )
    )
    .reset_index()
)


market_summary["Delay_Rate_%"] = (
    market_summary["Delayed_Shipments"]
    / market_summary["Shipments"]
    * 100
)


market_summary = market_summary.sort_values(
    "Delay_Rate_%",
    ascending=False
)


col1, col2 = st.columns(2)


with col1:

    st.markdown("### Market Delay Rate")

    fig, ax = plt.subplots(figsize=(7, 4))

    market_chart = market_summary.sort_values(
        "Delay_Rate_%"
    )

    ax.barh(
        market_chart["Market"],
        market_chart["Delay_Rate_%"]
    )

    ax.set_xlabel("Delayed Rate (%)")
    ax.set_ylabel("Market")
    ax.set_title("Delayed Shipment Rate by Market")

    plt.tight_layout()

    st.pyplot(fig)


with col2:

    st.markdown("### Market Average Delay")

    fig, ax = plt.subplots(figsize=(7, 4))

    market_delay_chart = market_summary.sort_values(
        "Average_Delay"
    )

    ax.barh(
        market_delay_chart["Market"],
        market_delay_chart["Average_Delay"]
    )

    ax.set_xlabel("Average Delay (Days)")
    ax.set_ylabel("Market")
    ax.set_title("Average Delay by Market")

    plt.tight_layout()

    st.pyplot(fig)


st.divider()


# =========================================================
# REGIONAL DELIVERY PERFORMANCE HEATMAP
# =========================================================

st.markdown("## 🗺️ Regional Delivery Performance Map")

st.markdown(
    "The heatmap compares the proportion of delayed, "
    "on-time, and early shipments across regions."
)


regional_heatmap = pd.crosstab(
    filtered_df["Order Region"],
    filtered_df["Delivery Performance"],
    normalize="index"
) * 100


regional_heatmap = regional_heatmap.reindex(
    columns=["Delayed", "On-time", "Early"],
    fill_value=0
)


fig, ax = plt.subplots(figsize=(11, 8))

sns.heatmap(
    regional_heatmap,
    annot=True,
    fmt=".1f",
    linewidths=0.5,
    ax=ax
)

ax.set_title(
    "Regional Delivery Performance (%)"
)

ax.set_xlabel("Delivery Performance")
ax.set_ylabel("Order Region")

plt.tight_layout()

st.pyplot(fig)


st.divider()


# =========================================================
# DELIVERY RISK HOTSPOT EXPLORER
# =========================================================

st.markdown("## 🔥 Delivery Risk Hotspot Explorer")

st.markdown(
    """
    This section identifies operational combinations of
    **Order Region + Shipping Mode** with higher delay rates.

    Shipment volume is shown alongside delay rate so that
    small-volume groups are not interpreted only from their
    percentage value.
    """
)


# ---------------------------------------------------------
# HOTSPOT CALCULATION
# ---------------------------------------------------------

hotspot_analysis = (
    filtered_df
    .groupby(["Order Region", "Shipping Mode"])
    .agg(
        Shipments=("Delivery Performance", "count"),
        Delayed_Shipments=(
            "Delivery Performance",
            lambda x: (x == "Delayed").sum()
        ),
        Average_Delay=(
            "Delay Gap",
            lambda x: x[x > 0].mean()
        ),
        Maximum_Delay=("Delay Gap", "max")
    )
    .reset_index()
)


hotspot_analysis["Average_Delay"] = (
    hotspot_analysis["Average_Delay"].fillna(0)
)


hotspot_analysis["Delay_Rate_%"] = (
    hotspot_analysis["Delayed_Shipments"]
    / hotspot_analysis["Shipments"]
    * 100
)


# ---------------------------------------------------------
# RISK LEVEL
# ---------------------------------------------------------

overall_hotspot_delay = (
    (filtered_df["Delivery Performance"] == "Delayed").mean()
    if len(filtered_df) > 0 else 0
)


def assign_hotspot_risk(rate):

    if overall_hotspot_delay == 0:
        return "No Baseline"

    ratio = (rate / 100) / overall_hotspot_delay

    if ratio >= 1.20:
        return "High"

    elif ratio >= 0.90:
        return "Moderate"

    else:
        return "Lower"


hotspot_analysis["Risk_Level"] = (
    hotspot_analysis["Delay_Rate_%"]
    .apply(assign_hotspot_risk)
)


# ---------------------------------------------------------
# MINIMUM VOLUME FILTER
# ---------------------------------------------------------

minimum_shipments = st.slider(
    "Minimum shipments required for hotspot analysis",
    min_value=1,
    max_value=1000,
    value=100,
    step=50
)


hotspot_filtered = hotspot_analysis[
    hotspot_analysis["Shipments"] >= minimum_shipments
].copy()


hotspot_filtered = hotspot_filtered.sort_values(
    "Delay_Rate_%",
    ascending=False
)


# ---------------------------------------------------------
# HOTSPOT SUMMARY
# ---------------------------------------------------------

hotspot_count = len(hotspot_filtered)

high_risk_count = (
    hotspot_filtered["Risk_Level"] == "High"
).sum()


h1, h2 = st.columns(2)


with h1:

    st.metric(
        "Operational Hotspots",
        f"{hotspot_count:,}"
    )


with h2:

    st.metric(
        "High-Risk Combinations",
        f"{high_risk_count:,}"
    )


# ---------------------------------------------------------
# TOP HOTSPOTS CHART
# ---------------------------------------------------------

st.markdown("### Highest Delay-Risk Combinations")


top_hotspots = hotspot_filtered.head(10).copy()


if len(top_hotspots) > 0:

    top_hotspots["Hotspot"] = (
        top_hotspots["Order Region"]
        + " | "
        + top_hotspots["Shipping Mode"]
    )


    fig, ax = plt.subplots(figsize=(12, 6))

    ax.barh(
        top_hotspots["Hotspot"].iloc[::-1],
        top_hotspots["Delay_Rate_%"].iloc[::-1]
    )

    ax.set_xlabel("Delayed Shipment Rate (%)")
    ax.set_ylabel("Region | Shipping Mode")
    ax.set_title("Top Delivery Risk Hotspots")

    plt.tight_layout()

    st.pyplot(fig)

else:

    st.info(
        "No hotspot combinations meet the selected "
        "minimum shipment threshold."
    )


# ---------------------------------------------------------
# HOTSPOT TABLE
# ---------------------------------------------------------

st.markdown("### Hotspot Details")


hotspot_display = hotspot_filtered[
    [
        "Order Region",
        "Shipping Mode",
        "Shipments",
        "Delayed_Shipments",
        "Delay_Rate_%",
        "Average_Delay",
        "Maximum_Delay",
        "Risk_Level"
    ]
].copy()


hotspot_display["Delay_Rate_%"] = (
    hotspot_display["Delay_Rate_%"].round(2)
)

hotspot_display["Average_Delay"] = (
    hotspot_display["Average_Delay"].round(2)
)

hotspot_display["Maximum_Delay"] = (
    hotspot_display["Maximum_Delay"].round(2)
)


st.dataframe(
    hotspot_display,
    use_container_width=True,
    hide_index=True
)


st.divider()


# =========================================================
# DASHBOARD FOOTER
# =========================================================

st.markdown(
    """
    **APL Logistics Supply Chain Control Center**

    Analytical dashboard developed for delivery performance,
    delay risk, logistics efficiency, and operational hotspot analysis.

    *Cancelled shipments are excluded from completed-delivery
    performance calculations.*
    """
)