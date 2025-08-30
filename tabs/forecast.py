import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def show_forecast(filtered_df):
    """
    Display the forecast tab with sales predictions for the next year.
    
    Args:
        filtered_df: Filtered DataFrame to use for forecasting
    """
    st.title("📈 Sales Forecast")
    st.write("This tab shows sales forecasts based on historical data.")
    
    # Add a slider to control forecast horizon
    forecast_horizon = st.slider(
        "Forecast Horizon (months)",
        min_value=3,
        max_value=60,
        value=12,
        step=1,
        help="Select the number of months to forecast"
    )
    
    # Aggregate data by month for forecasting
    monthly_sales = filtered_df.groupby('Order_YearMonth')['Sales'].sum().reset_index()
    monthly_sales = monthly_sales.sort_values('Order_YearMonth')
    
    # Check if we have enough data for forecasting (at least 12 months)
    if len(monthly_sales) < 12:
        st.warning("⚠️ Not enough data for reliable forecasting. Please select a date range with at least 12 months of data.")
        return
    
    # Create a time series from the monthly data
    time_series = pd.Series(
        monthly_sales['Sales'].values,
        index=pd.DatetimeIndex(monthly_sales['Order_YearMonth']),
        name='Sales'
    )
    
    # Display the historical data
    st.subheader("Historical Monthly Sales")
    fig_historical = px.line(
        monthly_sales, 
        x='Order_YearMonth', 
        y='Sales',
        title='Historical Monthly Sales'
    )
    fig_historical.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        yaxis=dict(tickprefix='$', tickformat=',.0f')
    )
    st.plotly_chart(fig_historical, use_container_width=True)
    
    # Decompose the time series to show trend, seasonality, and residuals
    st.subheader("Time Series Decomposition")
    
    # Only perform decomposition if we have enough data
    if len(time_series) >= 24:  # Need at least 2 years for meaningful decomposition
        try:
            decomposition = seasonal_decompose(time_series, model='additive', period=12)
            
            # Create subplots for decomposition components
            fig_decomp = go.Figure()
            
            # Original
            fig_decomp.add_trace(go.Scatter(
                x=decomposition.observed.index,
                y=decomposition.observed.values,
                mode='lines',
                name='Observed'
            ))
            
            # Trend
            fig_decomp.add_trace(go.Scatter(
                x=decomposition.trend.index,
                y=decomposition.trend.values,
                mode='lines',
                name='Trend'
            ))
            
            # Seasonal
            fig_decomp.add_trace(go.Scatter(
                x=decomposition.seasonal.index,
                y=decomposition.seasonal.values,
                mode='lines',
                name='Seasonal'
            ))
            
            fig_decomp.update_layout(
                title='Time Series Decomposition',
                xaxis_title='Date',
                yaxis_title='Sales ($)',
                yaxis=dict(tickprefix='$', tickformat=',.0f'),
                height=500
            )
            
            st.plotly_chart(fig_decomp, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not perform time series decomposition: {e}")
    else:
        st.info("⚠️ At least 24 months of data are needed for time series decomposition.")
    
    # Forecast future sales
    st.subheader(f"Sales Forecast for Next {forecast_horizon} Months")
    
    # Create a model for forecasting
    try:
        # Use Holt-Winters Exponential Smoothing for forecasting
        model = ExponentialSmoothing(
            time_series,
            trend='add',
            seasonal='add',
            seasonal_periods=12,  # Monthly data
            damped=True
        )
        
        # Fit the model
        model_fit = model.fit(optimized=True)
        
        # Generate forecast using the slider value
        forecast = model_fit.forecast(forecast_horizon)
        
        # Create a date range for the forecast period
        last_date = time_series.index[-1]
        forecast_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_horizon, freq='MS')
        forecast.index = forecast_dates
        
        # Create a DataFrame for the forecast
        forecast_df = pd.DataFrame({
            'Date': forecast.index,
            'Forecast': forecast.values
        })
        
        # Combine historical and forecast data for plotting
        historical_df = pd.DataFrame({
            'Date': time_series.index,
            'Sales': time_series.values
        })
        
        # Create the plot
        fig_forecast = go.Figure()
        
        # Add historical data
        fig_forecast.add_trace(go.Scatter(
            x=historical_df['Date'],
            y=historical_df['Sales'],
            mode='lines',
            name='Historical Sales',
            line=dict(color='blue')
        ))
        
        # Add forecast data
        fig_forecast.add_trace(go.Scatter(
            x=forecast_df['Date'],
            y=forecast_df['Forecast'],
            mode='lines',
            name='Forecast',
            line=dict(color='red', dash='dash')
        ))
        
        # Update layout
        fig_forecast.update_layout(
            title=f'Sales Forecast for Next {forecast_horizon} Months',
            xaxis_title='Date',
            yaxis_title='Sales ($)',
            yaxis=dict(tickprefix='$', tickformat=',.0f'),
            legend=dict(x=0.01, y=0.99, traceorder='normal'),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # Display forecast data in a table
        st.subheader("Forecast Data")
        forecast_table = forecast_df.copy()
        forecast_table['Date'] = forecast_table['Date'].dt.strftime('%Y-%m')
        forecast_table['Forecast'] = forecast_table['Forecast'].map('${:,.2f}'.format)
        st.dataframe(forecast_table, use_container_width=True)
        
        # Add download button for forecast data
        csv = forecast_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download forecast data as CSV",
            data=csv,
            file_name="sales_forecast.csv",
            mime="text/csv",
        )
        
    except Exception as e:
        st.error(f"Error generating forecast: {e}")
        st.info("Try selecting a different date range or ensure you have consistent monthly data.")