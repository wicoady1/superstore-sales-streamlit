import streamlit as st
import pandas as pd

# Import custom modules
from utils import load_data, filter_data
from tabs.dashboard import show_dashboard
from tabs.raw_data import show_raw_data
from tabs.forecast import show_forecast

# Load data
df = load_data()

# Display the first 10 rows of the dataframe
## st.title('SuperSales Data Analysis')
## st.subheader('First 10 rows of the dataset')
## st.dataframe(df.head(10))

## ============
## Create Sidebar for Streamlit
## ============
st.sidebar.title('SuperSales Data Analysis')
st.sidebar.header('Filter Data')

# Create a list of unique year-month combinations in format 'YYYY-MM'
date_options = df['Order_YearMonth'].sort_values().dt.strftime('%Y-%m').unique().tolist()

date_range_min = st.sidebar.selectbox(
    'Select Minimum Month-Date:',
    options=date_options,
    index=0
)

date_range_max = st.sidebar.selectbox(
    'Select Maximum Month-Date:',
    options=date_options,
    index=len(date_options)-1
)


region = st.sidebar.multiselect(
    'Select Region:',
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

category = st.sidebar.multiselect(
    'Select Category:',
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

if date_range_min > date_range_max:
    st.sidebar.error("Error: Minimum date must be before maximum date.")

# Filter data based on selections
filtered_df = filter_data(df, date_range_min, date_range_max, region, category)

# Create tabs
dashboard_tab, raw_data_tab, forecast_tab = st.tabs(["📊 Dashboard", "📋 Raw Data", "📈 Forecast"])

# Tab 1: Dashboard
with dashboard_tab:
    show_dashboard(filtered_df)

# Tab 2: Raw Data
with raw_data_tab:
    show_raw_data(filtered_df)
    
# Tab 3: Forecast
with forecast_tab:
    show_forecast(filtered_df)

