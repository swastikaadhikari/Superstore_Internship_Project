#Builds an interactive sales dashboard 
#importing the libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data #caches the dataset to improve performance
def load_data():
    df = pd.read_csv("Sample - Superstore.csv", encoding='latin-1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data() #Load the dataset

# Sidebar filters
st.sidebar.header("Filters") #add a header in the sidebar
category = st.sidebar.multiselect("Category", df['Category'].unique(), df['Category'].unique()) #select produt categories
region = st.sidebar.multiselect("Region", df['Region'].unique(), df['Region'].unique()) #select region
segment = st.sidebar.multiselect("Segment", df['Segment'].unique(), df['Segment'].unique()) #select customer segments 

# Apply filters to the dataset based on user selection
filtered_df = df[
    (df['Category'].isin(category)) & #Filter by selected categories
    (df['Region'].isin(region)) & #Filter by selected regions
    (df['Segment'].isin(segment)) #Filter by selected segments
]

# Main title of the dashboard
st.title("📦 Superstore Sales Dashboard")

# Key Performance Indicators
total_sales = filtered_df['Sales'].sum() #Calculate total sales
total_profit = filtered_df['Profit'].sum() #Calculate total profit
num_orders = filtered_df['Order ID'].nunique() #Count unique order IDs

#Display KPIs using Streamlit metric widgets
col1, col2, col3 = st.columns(3) #Create three columns for KPI display
col1.metric("Total Sales", f"${total_sales:,.0f}") #Show formatted sales value
col2.metric("Total Profit", f"${total_profit:,.0f}") #Show formatted profit value
col3.metric("Total Orders", num_orders) #show total number of orders

# Sales by Category visualization
st.subheader("Sales by Category") #Add subheading
fig_cat = px.bar(filtered_df.groupby("Category")["Sales"].sum().reset_index(),
                 x='Category', y='Sales', color='Category') #Create a bar chart
st.plotly_chart(fig_cat) #Display the chart


#Profit by Category
st.subheader("Profit by Category") #Add subheading
fig_profit = px.bar(filtered_df.groupby("Category")["Profit"].sum().reset_index(),
                 x='Category', y='Profit',color='Category') #Create a bar chart
st.plotly_chart(fig_profit) #Display the chart

#Sales by Region
st.subheader("Sales by Region") #Add a subheading
fig_sales = px.pie(filtered_df, names='Region', values='Sales') #create a piechart
st.plotly_chart(fig_sales) #Display the chart

# Profit by Region visualization
st.subheader("Profit by Region") #Add a subheading
fig_profit = px.pie(filtered_df, names='Region', values='Profit') #create a piechart
st.plotly_chart(fig_profit) #Display the chart

# Time series: Sales over time
st.subheader("Monthly Sales Trend")
monthly_sales = filtered_df.resample('M', on='Order Date')['Sales'].sum().reset_index()
fig3, ax3 = plt.subplots()
sns.lineplot(data=monthly_sales, x='Order Date', y='Sales', marker='o', ax=ax3)
plt.xticks(rotation=45)
st.pyplot(fig3)

# Sales over Time
st.subheader("Sales Over Time") #Add a subheading
sales_time = filtered_df.groupby("Order Date")["Sales"].sum().reset_index() #Aggregate sales by data
fig_time = px.line(sales_time, x='Order Date', y='Sales', title="Sales Trend Over Time") #create a line chart
st.plotly_chart(fig_time) #Display the chart

# Top Products
st.subheader("Top 10 Products by Sales") #Add a subheading
top_products = filtered_df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10).reset_index() #Get top 10 products
fig_top = px.bar(top_products, x='Sales', y='Product Name', orientation='h', title="Top 10 Products") #Create a horizontal bar chart
st.plotly_chart(fig_top) #Display the chart

# Download data
st.subheader("Download Filtered Data") #Add s su
st.download_button("Download CSV", filtered_df.to_csv(index=False), "filtered_data.csv", "text/csv")



