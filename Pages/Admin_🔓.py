# import the necessary libraries
import streamlit as st
from src.streamlit_app.pages_in_dashboard.admin.password import check_password
from src.streamlit_app.pages_in_dashboard.admin.visitor_count import visitor_count
from src.streamlit_app.pages_in_dashboard.admin.parking import get_parking_section

# Title of the page - page layout
st.write("# Bavarian Forest admin page")

# password check
check_password()

# visitor count information
visitor_count()

# Load the already preprocessed parking data
processed_parking_data = st.session_state['preprocessed_parking_data']

get_parking_section(processed_parking_data)