import streamlit as st
from src.streamlit_app.pages_in_dashboard.data_accessibility.data_retrieval import get_data_from_query
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report


def get_visualization_section(retrieved_df):
    """
    Get the visualization section.
    """
    st.markdown("# Data visualization")

    st.line_chart(retrieved_df)

    # Generate Pandas Profiling report
    # pr = retrieved_df.profile_report()
    pr = ProfileReport(retrieved_df,minimal=True)
    st_profile_report(pr)
