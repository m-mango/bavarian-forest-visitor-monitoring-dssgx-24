# imports libraries
import streamlit as st
import altair as alt
from src.streamlit_app.data_accessibility.query_box import get_query_section
from src.streamlit_app.data_accessibility.query_viz_and_download import get_visualization_section

# Define the page layout of the Streamlit app

st.set_page_config(
page_title='Access the park data🌲',
page_icon="🌲",
layout="wide",
initial_sidebar_state="expanded")

alt.themes.enable("dark")

# Define the app layout

col1, col2 = st.columns((1.5,2), gap='medium')
with col2:
    get_query_section()

    get_visualization_section()