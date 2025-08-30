import streamlit as st
import pandas as pd
import plotly.express as px

def show_dashboard(filtered_df):
    """
    Display the dashboard tab with KPIs and charts.
    
    Args:
        filtered_df: Filtered DataFrame to use for visualizations
    """
    st.title("📊 Superstore Sales Dashboard")
    st.write("by Sebastian Kennard")
    st.subheader("Overview")
    
    # Calculate KPIs
    total_sales = filtered_df['Sales'].sum()
    avg_order_value = filtered_df.groupby('Order ID')['Sales'].sum().mean()
    top_customer = filtered_df.groupby('Customer Name')['Sales'].sum().idxmax()
    
    # Display KPI cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Avg Order Value", f"${avg_order_value:,.0f}")
    col3.metric("Top Customer", top_customer)
    
    # 1. Monthly sales trend
    monthly_sales = filtered_df.groupby('Order_YearMonth')['Sales'].sum().reset_index()
    monthly_sales_fig = px.line(monthly_sales, x='Order_YearMonth', y='Sales', title='Monthly Sales Trend')
    # Format y-axis to show USD currency
    monthly_sales_fig.update_layout(
        yaxis=dict(
            tickprefix='$',
            tickformat=',.0f'
        )
    )
    st.plotly_chart(monthly_sales_fig, use_container_width=True)

    # 2. Sales by Category
    category_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
    category_sales_fig = px.bar(category_sales, x='Category', y='Sales', title='Sales by Category')
    # Format y-axis to show USD currency
    category_sales_fig.update_layout(
        yaxis=dict(
            tickprefix='$',
            tickformat=',.0f'
        )
    )
    st.plotly_chart(category_sales_fig, use_container_width=True)

    # 3. Top 10 Products
    top_products = (
        filtered_df.groupby('Product Name')['Sales']
        .sum()
        .nlargest(10)
        .sort_values(ascending=False)
        .reset_index()
    )
    top_products_fig = px.bar(
        top_products, x='Sales', y='Product Name', orientation='h', title='Top 10 Products', 
        text='Sales', text_auto=False,
        hover_data={'Sales': ':$,.2f'}
        )
    # Format text to show USD currency
    top_products_fig.update_traces(texttemplate='$%{x:,.0f}')
    # Ensure descending order in visualization and format x-axis to show USD currency
    top_products_fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        xaxis=dict(
            tickprefix='$',
            tickformat=',.0f'
        )
    )
    st.plotly_chart(top_products_fig, use_container_width=True)

    # 4. Top 10 Customers
    top_customer = (
        filtered_df.groupby('Customer Name')['Sales']
        .sum()
        .nlargest(10)
        .sort_values(ascending=False)
        .reset_index()
    )
    top_customer_fig = px.bar(
        top_customer, x='Sales', y='Customer Name', orientation='h', title='Top 10 Customers', 
        text='Sales', text_auto=False,
        hover_data={'Sales': ':$,.2f'}
        )
    # Format text to show USD currency
    top_customer_fig.update_traces(texttemplate='$%{x:,.0f}')
    # Ensure descending order in visualization and format x-axis to show USD currency
    top_customer_fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        xaxis=dict(
            tickprefix='$',
            tickformat=',.0f'
        )
    )
    st.plotly_chart(top_customer_fig, use_container_width=True)