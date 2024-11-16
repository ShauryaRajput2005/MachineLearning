import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set page configuration
st.set_page_config(page_title="Influencer Impact Dashboard", layout="wide")

# Title and Description
st.title("Influencer Impact on Brand Sales")
st.markdown("""
Analyze the effectiveness of influencer marketing campaigns using this interactive dashboard. 
Track sales trends, calculate ROI, and identify the top-performing influencers.
""")

# Sidebar for data upload
st.sidebar.header("Upload Data")
social_data_file = st.sidebar.file_uploader("Upload Influencer Data (CSV):", type=["csv"])
sales_data_file = st.sidebar.file_uploader("Upload Sales Data (CSV):", type=["csv"])

# Function to load data
def load_data(file):
    return pd.read_csv(file)

# Process data if both files are uploaded
if social_data_file and sales_data_file:
    social_data = load_data(social_data_file)
    sales_data = load_data(sales_data_file)

    # Display uploaded data
    with st.expander("View Uploaded Data"):
        st.subheader("Influencer Data")
        st.dataframe(social_data)
        st.subheader("Sales Data")
        st.dataframe(sales_data)

    # Merge data on a common key (e.g., timestamp)
    merged_data = pd.merge(social_data, sales_data, on="timestamp", how="inner")

    # Display merged data
    with st.expander("View Merged Data"):
        st.dataframe(merged_data)

    # Key Metrics Overview
    st.header("Key Metrics Overview")
    total_revenue = merged_data["sales"].sum()
    total_units_sold = merged_data["units_sold"].sum()
    total_campaign_cost = merged_data["campaign_cost"].sum() if "campaign_cost" in merged_data.columns else 0
    avg_roi = (total_revenue / total_campaign_cost) if total_campaign_cost > 0 else 0

    metrics = {
        "Total Revenue ($)": total_revenue,
        "Total Units Sold": total_units_sold,
        "Total Campaign Costs ($)": total_campaign_cost,
        "Average ROI (%)": avg_roi * 100,
    }
    st.write(pd.DataFrame(metrics, index=["Value"]).T)

    # Influencer Impact Analysis
    st.header("Influencer Impact Analysis")
    influencer_group = merged_data.groupby("influencer_name").agg({
        "units_sold": "sum",
        "sales": "sum",
        "campaign_cost": "sum",
        "timestamp": "count"
    }).reset_index()
    influencer_group["ROI"] = (influencer_group["sales"] / influencer_group["campaign_cost"]) * 100
    influencer_group = influencer_group.sort_values(by="ROI", ascending=False)

    st.subheader("Influencer Performance Table")
    st.dataframe(influencer_group)

    st.subheader("Bar Chart: ROI by Influencer")
    roi_bar_chart = px.bar(
        influencer_group, x="influencer_name", y="ROI", color="ROI", 
        title="ROI by Influencer", labels={"ROI": "Return on Investment (%)"},
        color_continuous_scale="Blues"
    )
    st.plotly_chart(roi_bar_chart, use_container_width=True)

    # Correlation Analysis
    st.header("Correlation Analysis")
    correlation_data = merged_data[["sales", "engagement", "likes", "comments", "shares"]].corr()
    correlation_fig = px.imshow(
        correlation_data, text_auto=True, color_continuous_scale="RdBu_r", title="Correlation Heatmap"
    )
    st.plotly_chart(correlation_fig, use_container_width=True)

    # Sales Trend Analysis
    st.header("Sales Trend Analysis")
    sales_trend_fig = px.line(
        merged_data, x="timestamp", y="sales", title="Sales Trend Over Time", labels={"sales": "Revenue ($)"}
    )
    st.plotly_chart(sales_trend_fig, use_container_width=True)

    # Platform Performance
    st.header("Platform Performance")
    if "platform" in merged_data.columns:
        platform_group = merged_data.groupby("platform").agg({
            "sales": "sum",
            "units_sold": "sum",
            "campaign_cost": "sum"
        }).reset_index()
        st.subheader("Platform Performance Table")
        st.dataframe(platform_group)

        platform_bar_chart = px.bar(
            platform_group, x="platform", y="sales", color="sales", title="Revenue by Platform",
            labels={"sales": "Revenue ($)"}, color_continuous_scale="Viridis"
        )
        st.plotly_chart(platform_bar_chart, use_container_width=True)

    # Cost-Efficiency Analysis
    st.header("Cost-Efficiency Analysis")
    if "campaign_cost" in influencer_group.columns:
        cost_efficiency_fig = px.scatter(
            influencer_group, x="campaign_cost", y="ROI", color="ROI", size="units_sold",
            title="ROI vs Campaign Cost", labels={"campaign_cost": "Campaign Cost ($)", "ROI": "Return on Investment (%)"}
        )
        st.plotly_chart(cost_efficiency_fig, use_container_width=True)

    # Filters for Custom Analysis
    st.sidebar.header("Filters")
    selected_influencer = st.sidebar.selectbox("Select Influencer:", ["All"] + list(influencer_group["influencer_name"]))
    selected_platform = st.sidebar.selectbox("Select Platform:", ["All"] + list(merged_data["platform"].unique() if "platform" in merged_data.columns else []))

    if selected_influencer != "All":
        merged_data = merged_data[merged_data["influencer_name"] == selected_influencer]

    if selected_platform != "All":
        merged_data = merged_data[merged_data["platform"] == selected_platform]

    # Final Recommendations
    st.header("Recommendations")
    st.markdown("""
    - Partner with influencers with the highest ROI for future campaigns.
    - Focus on platforms that drive the most engagement and revenue.
    - Analyze optimal posting times to align campaigns with periods of high sales.
    """)

else:
    st.warning("Please upload both Influencer Data and Sales Data to proceed.")
