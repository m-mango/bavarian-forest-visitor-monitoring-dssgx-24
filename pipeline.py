import pandas as pd
import streamlit as st
from src.source_data import source_all_data
import altair as alt
import src.streamlit_app.page_layout_config as page_layout_config
from PIL import Image


def create_dashboard():
    col1, col2 = page_layout_config.get_page_layout()

    with col1:
        logo = Image.open("src/streamlit_app/assets/bf_logo2.png")
        st.image(logo, width=100)
        st.title("Plan Your Trip to the Bavarian Forest")

    with col2:
        st.write("Hello col 2")
        # # get the language selection menu
        # get_language_selection_menu()
        
        # # get the weather section
        # get_weather_section()

        # # create recreational section
        # get_recreation_section()

    

def pipeline():

    historic_visitor_counts, all_parking_data, weather_data_df = source_all_data()

    print(historic_visitor_counts.head(), all_parking_data.head(), weather_data_df.head())

    return

if __name__ == "__main__":

    pipeline()

    create_dashboard()

    