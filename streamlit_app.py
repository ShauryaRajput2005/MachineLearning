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

    st.subheader("Influencer Performance Table")
    st.dataframe(influencer_group)

    st.subheader("Bar Chart: ROI by Influencer")
    roi_bar_chart = px.bar(
        influencer_group, x="Influencer ID", y="ROI (%)", color="ROI (%)", 
        title="ROI by Influencer", labels={"ROI (%)": "Return on Investment (%)"},
        color_continuous_scale="Blues"
    )
    st.plotly_chart(roi_bar_chart, use_container_width=True)

    # Correlation Analysis
    st.header("Correlation Analysis")
    correlation_data = influencer_data[["Follower Count", "Engagement Rate (%)", "Units Sold", "Revenue ($)", "Campaign Cost ($)", "ROI (%)"]].corr()
    correlation_fig = px.imshow(
        correlation_data, text_auto=True, color_continuous_scale="RdBu_r", title="Correlation Heatmap"
    )
    st.plotly_chart(correlation_fig, use_container_width=True)

    # Sales Trend Analysis
    st.header("Sales Trend Analysis")
    sales_trend_fig = px.line(
        influencer_data, x="Post Date", y="Revenue ($)", title="Sales Trend Over Time", labels={"Revenue ($)": "Revenue ($)"}
    )
    st.plotly_chart(sales_trend_fig, use_container_width=True)

    # Platform Performance
    st.header("Platform Performance")
    platform_group = influencer_data.groupby("Platform").agg({
        "Revenue ($)": "sum",
        "Units Sold": "sum",
        "Campaign Cost ($)": "sum"
    }).reset_index()

    st.subheader("Platform Performance Table")
    st.dataframe(platform_group)

    platform_bar_chart = px.bar(
        platform_group, x="Platform", y="Revenue ($)", color="Revenue ($)", title="Revenue by Platform",
        labels={"Revenue ($)": "Revenue ($)"}, color_continuous_scale="Viridis"
    )
    st.plotly_chart(platform_bar_chart, use_container_width=True)

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
    st.header("Recommendations")
    st.markdown("""
    - Partner with influencers with the highest ROI for future campaigns.
    - Focus on platforms that drive the most engagement and revenue.
    - Analyze optimal posting times to align campaigns with periods of high sales.
    """)

else:
    st.warning("Please upload the Influencer Data to proceed.")
