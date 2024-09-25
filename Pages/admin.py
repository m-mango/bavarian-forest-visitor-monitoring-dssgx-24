# import the necessary libraries
import streamlit as st
from src.streamlit_app.pages_in_dashboard.admin.password import check_password
from src.streamlit_app.pages_in_dashboard.admin.visitor_count import visitor_count
from src.streamlit_app.pages_in_dashboard.admin.parking import get_parking_section
from Main import pipeline

# Title of the page - page layout
st.write("# Bavarian Forest admin page")

# password check
check_password()

# visitor count information
visitor_count()

# parking lot information
_, processed_parking_data = pipeline()
get_parking_section(processed_parking_data)