import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    # Replace 'influencer_data.csv' with your file path
    data = pd.read_csv('influencer_brand_sales.csv')
    return data

data = load_data()

# Streamlit App
st.title("Influencer Impact on Brand Sales Dashboard")

# Filter options
platforms = st.sidebar.multiselect("Select Platforms", data['Platform'].unique(), default=data['Platform'].unique())
products = st.sidebar.multiselect("Select Products", data['Product ID'].unique(), default=data['Product ID'].unique())

# Filtered data
filtered_data = data[(data['Platform'].isin(platforms)) & (data['Product ID'].isin(products))]

# KPI Metrics
st.header("Key Metrics")
total_revenue = filtered_data['Revenue ($)'].sum()
average_roi = filtered_data['ROI (%)'].mean()
top_influencer = filtered_data.loc[filtered_data['Revenue ($)'].idxmax(), 'Influencer ID']

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue ($)", f"${total_revenue:,.2f}")
col2.metric("Average ROI (%)", f"{average_roi:.2f}")
col3.metric("Top Influencer", top_influencer)

# Bar chart: Revenue by influencer
st.header("Revenue by Influencer")
fig, ax = plt.subplots()
filtered_data.groupby('Influencer ID')['Revenue ($)'].sum().sort_values().plot(kind='barh', ax=ax, color='skyblue')
ax.set_title("Revenue by Influencer")
ax.set_xlabel("Revenue ($)")
ax.set_ylabel("Influencer ID")
st.pyplot(fig)

# Scatter plot: ROI vs Engagement Rate
st.header("ROI vs Engagement Rate")
fig, ax = plt.subplots()
ax.scatter(filtered_data['Engagement Rate (%)'], filtered_data['ROI (%)'], alpha=0.7, color='orange')
ax.set_title("ROI vs Engagement Rate")
ax.set_xlabel("Engagement Rate (%)")
ax.set_ylabel("ROI (%)")
st.pyplot(fig)

# Sales Spike Analysis
st.header("Sales Spike Analysis")
sales_spike_counts = filtered_data['Sales Spike'].value_counts()
fig, ax = plt.subplots()
sales_spike_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=['lightgreen', 'tomato'], labels=['No Spike', 'Spike'])
ax.set_ylabel("")
ax.set_title("Proportion of Sales Spikes")
st.pyplot(fig)

# Data Table
st.header("Filtered Data Table")
st.dataframe(filtered_data)

# Download filtered data
st.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_data.to_csv(index=False),
    file_name="filtered_influencer_data.csv",
    mime="text/csv",
)

