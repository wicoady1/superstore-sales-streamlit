import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    """
    Load and preprocess the SuperSales data.
    Returns a pandas DataFrame with processed date columns.
    """
    df = pd.read_csv('datasource/supersales_data.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
    df['Order_YearMonth'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()
    return df

def filter_data(df, date_range_min, date_range_max, region, category):
    """
    Filter the dataframe based on selected filters.
    
    Args:
        df: The input DataFrame
        date_range_min: Minimum date in 'YYYY-MM' format
        date_range_max: Maximum date in 'YYYY-MM' format
        region: List of selected regions
        category: List of selected categories
        
    Returns:
        Filtered DataFrame
    """
    date_options = df['Order_YearMonth'].dt.strftime('%Y-%m').unique().tolist()
    
    if date_range_min > date_range_max:
        # Handle invalid date range
        return df[
            (df['Order_YearMonth'].dt.strftime('%Y-%m').between(min(date_options), max(date_options))) &
            (df['Region'].isin(region)) &
            (df['Category'].isin(category))
        ]
    else:
        return df[
            (df['Order_YearMonth'].dt.strftime('%Y-%m').between(date_range_min, date_range_max)) &
            (df['Region'].isin(region)) &
            (df['Category'].isin(category))
        ]