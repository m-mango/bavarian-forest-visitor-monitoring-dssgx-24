# import libraries
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import pytz
from src.streamlit_app.source_data import source_and_preprocess_forecasted_weather_data
from datetime import datetime
from src.streamlit_app.pages_in_dashboard.visitors.language_selection_menu import TRANSLATIONS


# Functions

def find_peaks(data):
    """
    Find peaks in the data.

    Args:
        data (pd.Series): The data to find peaks in.
    
    Returns:
        list: A list of indices where peaks occur.
    """
    peaks = []
    for i in range(1, len(data) - 1):
        if data[i] > data[i-1] and data[i] > data[i+1]:
            peaks.append(i)
    return peaks

def get_graph(forecast_data):
    """
    Display a line graph of the temperature forecast in the same plot,
    with clear day labels on the x-axis and properly formatted hover info.

    Args:
        forecast_data (pd.DataFrame): The forecast data to plot.
    
    Returns:
        plotly.graph_objects.Figure: The plotly figure object.
    """

    forecast_data.set_index('time', inplace=True)

    fig = go.Figure()

    # Add the temperature line with improved styling
    fig.add_trace(go.Scatter(
        x=forecast_data.index, 
        y=forecast_data['temp'], 
        mode='lines', 
        name=TRANSLATIONS[st.session_state.selected_language]['temperature'],
        line=dict(color='orange', width=2),  # Smoother line with better color
        hovertemplate=f'{TRANSLATIONS[st.session_state.selected_language]["date"]}: ' +  '%{x|%d-%m-%Y, %H:%M}<br>' + f'{TRANSLATIONS[st.session_state.selected_language]["temperature"]}: ' + ' %{y}°C<extra></extra>'
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
        name=TRANSLATIONS[st.session_state.selected_language]['peaks'],
        text=forecast_data['temp'][peak_indices].astype(str) + "°C",
        textposition='top center',
        hoverinfo='none'  # Disable hover for peaks to avoid overlapping
    )

    # Add peak points trace to the figure
    fig.add_trace(peak_points_trace)

    fig.update_layout(
    title=TRANSLATIONS[st.session_state.selected_language]['7_day_hourly_weather'],
    xaxis_title=TRANSLATIONS[st.session_state.selected_language]['date'],
    yaxis_title=TRANSLATIONS[st.session_state.selected_language]['temperature'],
    xaxis=dict(
        tickformat='%d-%m',  # Format x-axis as 'Day, Month Date'
        dtick=24 * 60 * 60 * 1000,  # Tick every day
        tickangle=-45,  # Rotate the labels to make them more readable
        color='white',  # Ensure labels are visible on the dark background
        showgrid=False,  # Hide vertical grid lines for better clarity
    ),
    yaxis=dict(
        color='white'  # Ensure y-axis labels are visible
    ),
    legend=dict(
        orientation="h",  # Horizontal legend
        yanchor="top",
        y=-0.4,  # Move the legend further down below the plot
        xanchor="center",
        x=0.5
    ),
    margin=dict(
        l=50, r=50, t=50, b=100  # Increase bottom margin to make space for the x-axis labels
    ),
    template='plotly_dark',
    hovermode="x unified"  # Unified hover to show temperature together
    )


    return fig


@st.fragment(run_every="1h")
def get_weather_section():
    """
    Display the weather section of the dashboard.

    Args:
        processed_weather_data (pd.DataFrame): Processed weather data.
    
    Returns:
        None
    """

    print("Fetching the latest weather forecast data for the current hour...")

    def get_current_hour():
        """
        Get the current hour in the format "HH:00:00".

        Returns:
            str: The current hour interval in the format "HH:MM:00".
        """
        current_time = datetime.now(pytz.timezone('Europe/Berlin'))

        # Get the current hour: Replace the minute value with the truncated value and set seconds and microseconds to 0
        current_hour = current_time.replace(minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:00:00")

        return current_hour
    
    timestamp_latest_weather_data_fetch = get_current_hour()

    processed_weather_data = source_and_preprocess_forecasted_weather_data(timestamp_latest_weather_data_fetch)


    st.markdown(f"### {TRANSLATIONS[st.session_state.selected_language]['weather_forecast']}")
    st.markdown(f"{TRANSLATIONS[st.session_state.selected_language]['weather_data_last_updated']} {timestamp_latest_weather_data_fetch}")


    fig  = get_graph(processed_weather_data)

    st.plotly_chart(fig)