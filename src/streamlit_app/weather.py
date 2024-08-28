from meteostat import Hourly, Point
from datetime import datetime
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# from language_selection_menu import TRANSLATIONS

# Get the start time as todays date
START_TIME = datetime.now()
END_TIME = (START_TIME + pd.Timedelta(days=7))


# Coordinates of the Bavarian Forest (Haselbach)
# These coordinates are based on the weather recommendation by Google for a Bavarian Forest Weather search
LATITUDE = 49.31452390542327
LONGITUDE = 12.711573421032

def get_hourly_data_forecasted():
    
    """
    Fetch hourly weather data for the Bavarian Forest - forecasted from todays date

    Returns:
    --------
    pd.DataFrame: Hourly weather data
    
    """
    bavarian_forest = Point(lat=LATITUDE, lon=LONGITUDE)
    data = Hourly(bavarian_forest, START_TIME, END_TIME)
    data = data.fetch()
    return data 


def find_peaks(data):

    # only get the highest peaks per day
    peaks = []
    for i in range(1, len(data) - 1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            peaks.append(i)
    return peaks


def get_graph(forecast_data):
    """
    Display a line graph of the temperature and precipitation forecast in the same plot.

    Parameters:
    -----------
    forecast_data: pd.DataFrame
        Hourly weather forecast data.
    """

    fig = go.Figure()

    # Add the temperature line with improved styling
    fig.add_trace(go.Scatter(
        x=forecast_data.index, 
        y=forecast_data['temp'], 
        mode='lines', 
        name='Temperature (°C)',
        line=dict(color='orange', width=2),  # Smoother line with better color
        hovertemplate='Date: %{x}<br>Temperature: %{y}°C<extra></extra>'
    ))

    # Find peak indices for temperature
    peak_indices = find_peaks(forecast_data['temp'])

    # Create a scatter trace for peaks
    peak_points_trace = go.Scatter(
        x=forecast_data.index[peak_indices],
        y=forecast_data['temp'][peak_indices],
        mode='markers',
        marker=dict(
            color=['red' if temp > 26 else 'green' for temp in forecast_data['temp'][peak_indices]], 
            size=10,
            symbol='circle-open'
        ),
        name='Peaks',
        text=forecast_data['temp'][peak_indices].astype(str) + "°C",
        textposition='top center',
        hoverinfo='none'  # Disable hover for peaks to avoid overlapping
    )

    # Add peak points trace to the figure
    fig.add_trace(peak_points_trace)

    # Add the precipitation line
    fig.add_trace(go.Scatter(
        x=forecast_data.index, 
        y=forecast_data['prcp'], 
        mode='lines', 
        name='Precipitation (mm)',
        line=dict(color='blue', width=2, dash='dash'),  # Dashed line for precipitation
        yaxis='y2',  # Use secondary y-axis for precipitation
        hovertemplate='Date: %{x}<br>Precipitation: %{y} mm<extra></extra>'
    ))

    # Update layout for dual y-axes and improved styling
    fig.update_layout(
        title='7-Day Hourly Weather Forecast',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        yaxis2=dict(
            title='Precipitation (mm)',
            overlaying='y',
            side='right',
            showgrid=False  # Remove grid lines from secondary y-axis
        ),
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="top",
            y=-0.3,  # Position below the plot
            xanchor="center",
            x=0.5
        ),
        template='plotly_dark',
        hovermode="x unified"  # Unified hover to show both temperature and precipitation together
    )

    return fig

    
def get_weather_section():
    """
    Display the weather section
    """

    st.markdown("### Weather Forecast")

    # Get the weather data
    forecast_data = get_hourly_data_forecasted()

    fig  = get_graph(forecast_data)

    st.plotly_chart(fig)

    
