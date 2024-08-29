import streamlit as st
import pydeck as pdk
import pandas as pd

# Assuming processed_parking_data DataFrame is already available

# Define fixed size for markers
def get_fixed_size():
    return 100  # Choose a fixed size value that works best for your map

def calculate_color(occupancy_rate):
    # Use a simple green-red color map
    return [int(255 * occupancy_rate), int(255 * (1 - occupancy_rate)), 0]

def get_parking_section(processed_parking_data):
    st.markdown("### Real Time Parking Occupancy")
    
    # Set a fixed size for all markers
    processed_parking_data['size'] = get_fixed_size()
    processed_parking_data['color'] = processed_parking_data['current_occupancy_rate'].apply(calculate_color)

    processed_parking_data['current_occupancy_rate'] = pd.to_numeric(processed_parking_data['current_occupancy_rate'], errors='coerce')  # Convert to float
    processed_parking_data['current_occupancy_rate'] = processed_parking_data['current_occupancy_rate'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")


    # Calculate center of the map based on the average of latitudes and longitudes
    avg_latitude = processed_parking_data['latitude'].mean()
    avg_longitude = processed_parking_data['longitude'].mean()

    # PyDeck Map Configuration with adjusted view_state
    view_state = pdk.ViewState(
        latitude=avg_latitude,  # Center map at the average latitude
        longitude=avg_longitude,  # Center map at the average longitude
        zoom=10,  # Zoom level increased for a closer view
        pitch=50
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=processed_parking_data,
        get_position=["longitude", "latitude"],
        get_radius="size",
        get_fill_color="color",
        pickable=True
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "text": "{location}\nAvailable Spaces: {current_availability} cars\nOccupancy Rate: {current_occupancy_rate}%"
        }  # Updated tooltip text with two decimal points for occupancy rate
    )
    st.pydeck_chart(deck)

    # Interactive Metrics
    selected_location = st.selectbox(
        "Select a parking section:", 
        processed_parking_data['location'].unique(),
        key="selectbox_parking_section"
    )

    # Display selected location details
    if selected_location:
        selected_data = processed_parking_data[processed_parking_data['location'] == selected_location].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Available Spaces", value=f"{selected_data['current_availability']} cars")
        col2.metric(label="Capacity", value=f"{selected_data['current_capacity']} cars")
        col3.metric(label="Occupancy Rate", value=f"{selected_data['current_occupancy_rate']}%")

