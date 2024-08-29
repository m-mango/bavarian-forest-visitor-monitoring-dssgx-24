import streamlit as st
import pandas as pd
import pydeck as pdk


# Assuming processed_parking_data DataFrame is already available

# Calculate color and size for markers
def calculate_size(occupancy_rate):
    return max(10, min(occupancy_rate * 100, 100))

def calculate_color(occupancy_rate):
    # Use a simple green-red color map
    return [int(255 * occupancy_rate), int(255 * (1 - occupancy_rate)), 0]


def get_parking_section(processed_parking_data):

    st.markdown("### Parking Occupancy")

    processed_parking_data['size'] = processed_parking_data['current_occupancy_rate'].apply(calculate_size)
    processed_parking_data['color'] = processed_parking_data['current_occupancy_rate'].apply(calculate_color)

    # PyDeck Map Configuration
    view_state = pdk.ViewState(
        latitude=49.0,
        longitude=13.0,
        zoom=12,
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
        tooltip={"text": "{location}\nOccupancy: {current_occupancy} cars\n Rate: {current_occupancy_rate:.2f}%"}
    )

    st.pydeck_chart(deck)

    # Interactive Metrics
    selected_location = st.selectbox(
        "Select a parking section:", 
        processed_parking_data['location'].unique(),
        key="selectbox_parking_section" )# Unique key

    # Display selected location details
    if selected_location:
        selected_data = processed_parking_data[processed_parking_data['location'] == selected_location].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Current Occupancy", value=f"{selected_data['current_occupancy']} cars")
        col2.metric(label="Capacity", value=f"{selected_data['current_capacity']} cars")
        col3.metric(label="Occupancy Rate", value=f"{selected_data['current_occupancy_rate']:.2f}%")
