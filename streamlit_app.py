import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Advanced Influencer Impact Dashboard", layout="wide")

# Title and Description
st.title("Advanced Influencer Impact on Brand Sales")
st.markdown("""
This advanced dashboard analyzes influencer marketing campaigns, providing insights on ROI, sales spikes, and time-series analysis.
Track sales trends, calculate ROI, perform time variance analysis, and explore how influencer activities influence sales over time.
""")

# Sidebar for data upload
st.sidebar.header("Upload Data")
influencer_data_file = st.sidebar.file_uploader("Upload Influencer Data (CSV):", type=["csv"])

# Function to load data
def load_data(file):
    return pd.read_csv(file)

# Process data if file is uploaded
if influencer_data_file:
    influencer_data = load_data(influencer_data_file)

    # Ensure the 'Post Date' is in datetime format
    influencer_data['Post Date'] = pd.to_datetime(influencer_data['Post Date'], errors='coerce')

    # Display uploaded data
    with st.expander("View Uploaded Data"):
        st.dataframe(influencer_data)

    # Key Metrics Overview
    st.header("Key Metrics Overview")
    total_revenue = influencer_data["Revenue ($)"].sum()
    total_units_sold = influencer_data["Units Sold"].sum()
    total_campaign_cost = influencer_data["Campaign Cost ($)"].sum()
    avg_roi = (total_revenue / total_campaign_cost) * 100 if total_campaign_cost > 0 else 0

    metrics = {
        "Total Revenue ($)": total_revenue,
        "Total Units Sold": total_units_sold,
        "Total Campaign Costs ($)": total_campaign_cost,
        "Average ROI (%)": avg_roi,
    }
    st.write(pd.DataFrame(metrics, index=["Value"]).T)

    # Influencer Impact Analysis
    st.header("Influencer Impact Analysis")
    influencer_group = influencer_data.groupby("Influencer ID").agg({
        "Units Sold": "sum",
        "Revenue ($)": "sum",
        "Campaign Cost ($)": "sum",
        "ROI (%)": "mean",
        "Sales Spike": lambda x: "Yes" if "Yes" in x.values else "No"
    }).reset_index()

    influencer_group = influencer_group.sort_values(by="ROI (%)", ascending=False)

    st.subheader("Top Influencers by ROI")
    st.dataframe(influencer_group)

    # Bar Chart: ROI by Influencer
    st.subheader("Bar Chart: Influencers vs ROI")
    roi_bar_chart = px.bar(
        influencer_group, x="Influencer ID", y="ROI (%)", color="ROI (%)", 
        title="ROI by Influencer", labels={"ROI (%)": "Return on Investment (%)"},
        color_continuous_scale="Blues"
    )
    st.plotly_chart(roi_bar_chart, use_container_width=True)

    # Sales Spike vs ROI
    st.subheader("Sales Spike vs ROI")
    sales_spike_vs_roi = px.box(
        influencer_group, x="Sales Spike", y="ROI (%)", 
        title="Sales Spike vs ROI", labels={"ROI (%)": "Return on Investment (%)"}
    )
    st.plotly_chart(sales_spike_vs_roi, use_container_width=True)

    # Correlation Analysis
    st.header("Correlation Analysis")
    correlation_data = influencer_data[["Follower Count", "Engagement Rate (%)", "Units Sold", "Revenue ($)", "Campaign Cost ($)", "ROI (%)"]].corr()
    correlation_fig = px.imshow(
        correlation_data, text_auto=True, color_continuous_scale="RdBu_r", title="Correlation Heatmap"
    )
    st.plotly_chart(correlation_fig, use_container_width=True)

    # Time-Series Decomposition (Variance Analysis)
    st.header("Time-Series Decomposition (Variance Analysis)")

    # Group by date and sum revenue to get a daily or weekly aggregation
    influencer_data_daily = influencer_data.groupby("Post Date").agg({
        "Revenue ($)": "sum"
    }).reset_index()

    influencer_data_daily.set_index("Post Date", inplace=True)

    # Decompose the time series into Trend, Seasonal, and Residuals using statsmodels
    decomposition = seasonal_decompose(influencer_data_daily["Revenue ($)"], model="multiplicative", period=7)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

    decomposition.trend.plot(ax=ax1, title="Trend Component", color="blue")
    decomposition.seasonal.plot(ax=ax2, title="Seasonality Component", color="green")
    decomposition.resid.plot(ax=ax3, title="Residuals Component", color="red")

    st.pyplot(fig)

    st.markdown("""
    The time-series decomposition provides the following insights:
    - **Trend Component**: Represents the overall sales trend over time.
    - **Seasonality Component**: Captures repeating patterns, e.g., weekly or monthly cycles.
    - **Residuals Component**: Shows the random noise or residuals after removing trend and seasonality.
    """)

    # Platform Performance
    st.header("Platform Performance")
    platform_group = influencer_data.groupby("Platform").agg({
        "Revenue ($)": "sum",
        "Units Sold": "sum",
        "Campaign Cost ($)": "sum"
    }).reset_index()

    st.subheader("Sales by Platform")
    st.dataframe(platform_group)

    platform_bar_chart = px.bar(
        platform_group, x="Platform", y="Revenue ($)", color="Revenue ($)", title="Revenue by Platform",
        labels={"Revenue ($)": "Revenue ($)"}, color_continuous_scale="Viridis"
    )
    st.plotly_chart(platform_bar_chart, use_container_width=True)

    # Engagement vs Sales by Platform
    st.subheader("Engagement vs Sales by Platform")
    engagement_sales_platform = px.scatter(
        influencer_data, x="Engagement Rate (%)", y="Revenue ($)", color="Platform", 
        size="Units Sold", title="Engagement vs Sales by Platform",
        labels={"Revenue ($)": "Revenue ($)", "Engagement Rate (%)": "Engagement Rate (%)"}
    )
    st.plotly_chart(engagement_sales_platform, use_container_width=True)

    # Cost-Efficiency Analysis
    st.header("Cost-Efficiency Analysis")
    cost_efficiency_fig = px.scatter(
        influencer_group, x="Campaign Cost ($)", y="ROI (%)", color="ROI (%)", size="Units Sold",
        title="ROI vs Campaign Cost", labels={"Campaign Cost ($)": "Campaign Cost ($)", "ROI (%)": "Return on Investment (%)"}
    )
    st.plotly_chart(cost_efficiency_fig, use_container_width=True)

    # Filters for Custom Analysis
    st.sidebar.header("Filters")
    selected_influencer = st.sidebar.selectbox("Select Influencer:", ["All"] + list(influencer_group["Influencer ID"]))
    selected_platform = st.sidebar.selectbox("Select Platform:", ["All"] + list(influencer_data["Platform"].unique()))

    if selected_influencer != "All":
        influencer_data = influencer_data[influencer_data["Influencer ID"] == selected_influencer]

    if selected_platform != "All":
        influencer_data = influencer_data[influencer_data["Platform"] == selected_platform]

    # Final Recommendations
    st.header("Summary & Recommendations")
    st.markdown("""
    - Partner with influencers with the highest ROI for future campaigns.
    - Focus on platforms that drive the most engagement and revenue.
    - Analyze optimal posting times to align campaigns with periods of high sales.
    """)

else:
    st.warning("Please upload the Influencer Data to proceed.")
