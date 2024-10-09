import streamlit as st
from PIL import Image

# get the streamlit app modules
import src.streamlit_app.pages_in_dashboard.visitors.page_layout_config as page_layout_config
import src.streamlit_app.pages_in_dashboard.visitors.language_selection_menu as lang_sel_menu
import src.streamlit_app.pages_in_dashboard.visitors.weather as weather
import src.streamlit_app.pages_in_dashboard.visitors.parking as parking 
import src.streamlit_app.pages_in_dashboard.visitors.visitor_count as visitor_count
import src.streamlit_app.pages_in_dashboard.visitors.recreational_activities as recreation
import src.streamlit_app.pages_in_dashboard.visitors.other_information as other_info

# imports for the prediction_pipeline
from src.prediction_pipeline.sourcing_data.source_historic_visitor_count import source_historic_visitor_count 
from src.prediction_pipeline.pre_processing.preprocess_historic_visitor_count_data import preprocess_visitor_count_data
from src.prediction_pipeline.sourcing_data.source_visitor_center_data import source_visitor_center_data
from src.prediction_pipeline.sourcing_data.source_weather import source_weather_data
from src.prediction_pipeline.pre_processing.preprocess_weather_data import process_weather_data
from src.prediction_pipeline.pre_processing.join_sensor_weather_visitorcenter import get_joined_dataframe
from src.prediction_pipeline.pre_processing.features_zscoreweather_distanceholidays import get_zscores_and_nearest_holidays
from src.prediction_pipeline.pre_processing.preprocess_visitor_center_data import process_visitor_center_data
from datetime import datetime

# Set the page layout - it is a two column layout
col1, col2 = page_layout_config.get_page_layout()

def create_dashboard_main_page():

    """
    Create the dashboard for the Bavarian Forest National Park visitor information page.

    Args:
        None

    Returns:
        None
    """
    
    with col1:

        # Display the logo and title of the column
        logo = Image.open("src/streamlit_app/assets/logo-bavarian-forest-national-park.png")
        st.image(logo, width=300)
        st.title("Plan Your Trip to the Bavarian Forest 🌲")

        # Get the visitor count section
        visitor_count.get_visitor_counts_section()

        # get the parking section
        parking.get_parking_section()


    with col2:
        # get the language selection menu
        lang_sel_menu.get_language_selection_menu()
        
        # get the weather section
        weather.get_weather_section()
        

        # create recreational section
        recreation.get_recreation_section()

        # Get the other information section
        other_info.get_other_information()


    
@st.cache_data
def pipeline():
    """
    The prediction pipeline to fior getting the data for model inference. The pipeline sources the data, 
    preprocesses it and returns the processed data. The sourced data includes the historic visitor count data,
    the visitor center data and the weather data.

    Args:
        None

    Returns:
        pd.DataFrame: The preprocessed data for model inference
    """

    ####################################################################################################
    # Prediction Pipeline
    ####################################################################################################
    
    # get the historic visitor count data
    sourced_visitor_count_df = source_historic_visitor_count()
   
    processed_visitor_count_df = preprocess_visitor_count_data(sourced_visitor_count_df)

    # get the visitor centers data
    sourced_vc_data_df = source_visitor_center_data()

    processed_vc_df_hourly,_ = process_visitor_center_data(sourced_vc_data_df)

    # get the weather data
    weather_data = source_weather_data(start_time = datetime(2023, 1, 1), end_time = datetime(2024, 7, 22) )

    processed_weather_df = process_weather_data(weather_data)

    # join the dataframes
    joined_df = get_joined_dataframe(processed_weather_df, processed_visitor_count_df, processed_vc_df_hourly)

    #  z score normalization
    columns_for_zscores = [ 'Temperature (°C)','Relative Humidity (%)','Wind Speed (km/h)']
    with_zscores_and_nearest_holidays_df = get_zscores_and_nearest_holidays(joined_df, columns_for_zscores)

    return with_zscores_and_nearest_holidays_df


if __name__ == "__main__":

    # call the sourcing and processing pipeline
    with_zscores_and_nearest_holidays_df = pipeline()

    # create the dashboard
    create_dashboard_main_page()

    