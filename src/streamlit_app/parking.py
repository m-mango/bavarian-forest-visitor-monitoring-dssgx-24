import streamlit as st
import random
import pydeck as pdk

# Install libraries
import pandas as pd
import requests
import json
import os


def get_parking_section(processed_parking_data):
    """
    Get the parking section with the highest occupancy rate.

    Args:
        processed_parking_data (pandas.DataFrame): Processed real-time parking data.
    
    Returns:
        None
    """
    st.markdown("### Parking Occupancy")
    # get the streamlit map object to display the bavarian forest section

    # st.map(processed_parking_data, zoom=12, latitude= "latitude", longitude="longitude", size= random.randint(0, 100))

    # Add a size column based on the occupancy rate (scaled for visibility)
    def calculate_size(occupancy_rate):
        size = occupancy_rate * 100  # Scale the size
        return max(10, min(size, 100))  # Ensure the size is between 10 and 100

    processed_parking_data['size'] = processed_parking_data['current_occupancy_rate'].apply(calculate_size)

    # Add a color column based on the occupancy rate (normalized for Streamlit)
    def calculate_color(occupancy_rate):
        red = int(255 * occupancy_rate)
        green = int(255 * (1 - occupancy_rate))
        return f'rgb({red},{green},0)'

    processed_parking_data['color'] = processed_parking_data['current_occupancy_rate'].apply(calculate_color)

    # Prepare the map view
    st.map(processed_parking_data, zoom=12)

        # Let the user select a parking section based on location name
    selected_location = st.selectbox(
        "Select a parking section:", 
        processed_parking_data['location'].unique()  # Ensure unique location names
    )

    # Find the selected row in the DataFrame
    if selected_location in processed_parking_data['location'].values:
        selected_data = processed_parking_data[processed_parking_data['location'] == selected_location].iloc[0]

        # Display metrics for the selected parking section
        st.metric(label="Current Occupancy", value=f"{selected_data['current_occupancy']} cars")
        st.metric(label="Capacity", value=f"{selected_data['current_capacity']} cars")
        st.metric(label="Occupancy Rate", value=f"{selected_data['current_occupancy_rate']*100:.2f}%")
    else:
        st.error(f"Location '{selected_location}' not found in the DataFrame.")


   