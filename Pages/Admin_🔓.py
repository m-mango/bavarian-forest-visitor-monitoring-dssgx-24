# import the necessary libraries
import streamlit as st
from src.streamlit_app.pages_in_dashboard.admin.password import check_password
from src.streamlit_app.pages_in_dashboard.admin.visitor_count import visitor_count
from src.streamlit_app.pages_in_dashboard.admin.parking import get_parking_section
from src.streamlit_app.source_data import source_and_preprocess_realtime_parking_data

# Title of the page - page layout
st.write("# Bavarian Forest admin page")

# password check
check_password()

# visitor count information
visitor_count()

@st.fragment(run_every="30min")
def get_latest_parking_data_and_visualize_it():
    # Load the already preprocessed parking data
    processed_parking_data, timestamp_latest_parking_data_fetch = source_and_preprocess_realtime_parking_data()

    get_parking_section(processed_parking_data, timestamp_latest_parking_data_fetch)

get_latest_parking_data_and_visualize_it()