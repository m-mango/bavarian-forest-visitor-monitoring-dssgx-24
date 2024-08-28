import pandas as pd
import streamlit as st
from src.source_data import source_all_data
import altair as alt

# get the streamlit app modules
import src.streamlit_app.page_layout_config as page_layout_config
import src.streamlit_app.language_selection_menu as lang_sel_menu
import src.streamlit_app.weather as weather

# get the process data functions
import src.pre_processing.process_forecast_weather_data as pwd
import src.pre_processing.process_real_time_parking_data as prtpd

from PIL import Image


def create_dashboard(processed_weather_data, processed_parking_data):
    col1, col2 = page_layout_config.get_page_layout()
    with col1:
        logo = Image.open("src/streamlit_app/assets/bf_logo2.png")
        st.image(logo, width=100)
        st.title("Plan Your Trip to the Bavarian Forest")

    with col2:
        # get the language selection menu
        lang_sel_menu.get_language_selection_menu()
        
        # get the weather section
        weather.get_weather_section(processed_weather_data)
        

        # # create recreational section
        # get_recreation_section()

    

def pipeline():

    # Source all data
    visitor_counts_data, parking_data, weather_data,  = source_all_data()

    # Process the weather data
    processed_weather_data = pwd.process_weather_data(weather_data)

    # process the parking data
    processed_parking_data = prtpd.process_real_time_parking_data(parking_data)

    # # process the visitor count data
    # process_visitor_count_data = prtpd.process_visitor_count_data(historic_visitor_counts)


    return processed_weather_data, processed_parking_data

if __name__ == "__main__":

    # call the sourcing and processing pipeline
    processed_weather_data, processed_parking_data = pipeline()


    # create the dashboard
    create_dashboard(processed_weather_data, processed_parking_data)

    