import streamlit as st
import pandas as pd

def show_raw_data(filtered_df):
    """
    Display the raw data tab with search functionality and download option.
    
    Args:
        filtered_df: Filtered DataFrame to display
    """
    st.title("📋 Raw Data")
    st.write("This tab shows the filtered raw data based on the sidebar selections.")
    
    # Add search functionality
    search_term = st.text_input("Search in data:", "")
    
    # Filter data based on search term if provided
    if search_term:
        search_results = filtered_df[filtered_df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)]
        st.dataframe(search_results, use_container_width=True)
    else:
        st.dataframe(filtered_df, use_container_width=True)
    
    # Add download button
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_supersales_data.csv",
        mime="text/csv",
    )