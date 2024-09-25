import streamlit as st

# get the streamlit app modules
import src.streamlit_app.pages_in_dashboard.visitors.page_layout_config as page_layout_config
import src.streamlit_app.pages_in_dashboard.visitors.language_selection_menu as lang_sel_menu
import src.streamlit_app.pages_in_dashboard.visitors.weather as weather
import src.streamlit_app.pages_in_dashboard.visitors.parking as parking 
import src.streamlit_app.pages_in_dashboard.visitors.visitor_count as visitor_count
import src.streamlit_app.pages_in_dashboard.visitors.recreational_activities as recreation
import src.streamlit_app.pages_in_dashboard.visitors.other_information as other_info

# get the process data functions
import src.streamlit_app.pre_processing.process_forecast_weather_data as pwd
import src.streamlit_app.pre_processing.process_real_time_parking_data as prtpd
from src.streamlit_app.source_data import source_all_data

from PIL import Image

# Set the page layout - it is a two column layout
col1, col2 = page_layout_config.get_page_layout()

def create_dashboard_main_page(processed_weather_data, processed_parking_data):

    """
    Create the dashboard for the Bavarian Forest National Park.

    Args:
        processed_weather_data (pd.DataFrame): Processed weather data.
        processed_parking_data (pd.DataFrame): Processed parking data.

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
        parking.get_parking_section(processed_parking_data)


    with col2:
        # get the language selection menu
        lang_sel_menu.get_language_selection_menu()
        
        # get the weather section
        weather.get_weather_section(processed_weather_data)
        

        # create recreational section
        recreation.get_recreation_section()

        # Get the other information section
        other_info.get_other_information()


    
@st.cache_data
def pipeline():
    """
    Run the sourcing and processing pipeline for the dashboard.
    
    Args:
        None
    
    Returns:
        processed_weather_data (pd.DataFrame): Processed weather data.
        processed_parking_data (pd.DataFrame): Processed parking data.
    """

    # Source all data
    visitor_counts_data, parking_data, weather_data  = source_all_data()

    # Process the weather data
    processed_weather_data = pwd.process_weather_data(weather_data)

    # process the parking data
    processed_parking_data = prtpd.process_real_time_parking_data(parking_data)
    
    # # TODO : Add code for getting the prediction data automatically

    # step 1: Source data from aws raw_data folder (source_data.py) - DONE
    # step 2: Process/filter the data to add the missing values, imputations etc.
    #  # process_visitor_count_data = prtpd.process_visitor_count_data(historic_visitor_counts)

    # step 3: get the processed_weather_data and processed_parking_data and join to the processed_visitor_count_data
    # # joined_data = join_data(processed_weather_data, processed_parking_data, process_visitor_count_data) # join data script

    # step 4: run the prediction model on the joined data
    # # prediction_data = run_prediction_modeljoined_data) # prediction model script

    # step 5: save the prediction data as csv to AWS for streamlit to use - DONE (script already added visitor_count.py)

    return processed_weather_data, processed_parking_data

if __name__ == "__main__":

    # call the sourcing and processing pipeline
    processed_weather_data, processed_parking_data = pipeline()

    # create the dashboard
    create_dashboard_main_page(processed_weather_data, processed_parking_data)

    