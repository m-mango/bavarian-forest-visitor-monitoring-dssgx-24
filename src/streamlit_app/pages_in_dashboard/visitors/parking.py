# Import necessary libraries
import streamlit as st
import pydeck as pdk
import pandas as pd

def get_fixed_size():
    """
    Get a fixed size value for the map markers.
    """
    return 300  

def calculate_color(occupancy_rate):
    """
    Calculate the color of the marker based on the occupancy rate.

    Args:
        occupancy_rate (float): The occupancy rate of the parking section.

    Returns:
        list: A list of RGB values representing the color of the marker.
    """
    occupancy_rate = float(occupancy_rate)

    if occupancy_rate >= 80:
        return [230, 39, 39] # red
    elif occupancy_rate >= 60:
        return [244, 251, 81] # yellow
    else:
        return [109, 249, 2] # green

def occupancy_to_color(occupancy_rate):
    """
    Convert occupancy rate to a CSS gradient color value.
    
    Args:
        occupancy_rate (float): The occupancy rate of the parking section.

    Returns:
        str: The CSS color string representing the gradient color.
    """
    occupancy_rate = float(occupancy_rate)
    if occupancy_rate >= 80:
        return "red"
    elif occupancy_rate >= 60:
        return "yellow"
    else:
        return "green"

def get_occupancy_status(occupancy_rate):
    """
    Get the occupancy status (High, Medium, Low) based on the occupancy rate.

    Args:
        occupancy_rate (float): The occupancy rate of the parking section.

    Returns:
        str: The occupancy status ("High", "Medium", "Low").
    """
    if occupancy_rate >= 80:
        return "High"
    elif occupancy_rate >= 60:
        return "Medium"
    else:
        return "Low"

def render_occupancy_bar(occupancy_rate):
    """
    Render a color bar representing the occupancy rate using HTML and CSS.

    Args:
        occupancy_rate (float): The occupancy rate of the parking section.

    Returns:
        None
    """
    # Ensure occupancy rate is between 0 and 100
    occupancy_rate = min(max(float(occupancy_rate), 0), 100)
    
    # Define the color based on occupancy
    bar_color = occupancy_to_color(occupancy_rate)

    # Create an HTML div with the appropriate width based on occupancy rate
    st.markdown(f"""
    <div style="width: 100%; background-color: lightgrey; border-radius: 5px; padding: 3px;">
        <div style="width: {occupancy_rate}%; background-color: {bar_color}; height: 25px; border-radius: 5px;"></div>
    </div>
    """, unsafe_allow_html=True)

def get_parking_section(processed_parking_data):
    """
    Display the parking section of the dashboard with a map showing the real-time parking occupancy 
    and interactive metrics.

    Args:
        processed_parking_data (pd.DataFrame): Processed parking data.

    Returns:
        None
    """
    st.markdown("### Real Time Parking Occupancy")
    
    # Set a fixed size for all markers
    processed_parking_data['size'] = get_fixed_size()
    processed_parking_data['color'] = processed_parking_data['current_occupancy_rate'].apply(calculate_color)

    # Convert the occupancy rate to numeric and handle errors
    processed_parking_data['current_occupancy_rate'] = pd.to_numeric(processed_parking_data['current_occupancy_rate'], errors='coerce')

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
        },
        map_style="road"
    )
    st.pydeck_chart(deck)

    # Map occupancy rate to status (High, Medium, Low)
    processed_parking_data['occupancy_status'] = processed_parking_data['current_occupancy_rate'].apply(get_occupancy_status)

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
        # col1.metric(label="Available Spaces", value=f"{selected_data['current_availability']} cars")
        col1.metric(label="Capacity", value=f"{selected_data['current_capacity']} cars")
        
        # Display occupancy status and bar
        with col2:
            # st.markdown("**Occupancy Status**")
            st.metric(label = "Occupancy Status", value=f"{selected_data['occupancy_status']}")
        with col3:
            st.markdown("**Occupancy Rate**")
            render_occupancy_bar(selected_data['current_occupancy_rate'])

