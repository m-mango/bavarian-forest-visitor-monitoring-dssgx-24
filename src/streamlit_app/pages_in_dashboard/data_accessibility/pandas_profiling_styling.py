from ydata_profiling import ProfileReport
import streamlit as st

def custom_pandas_profiling_report(data):

    report = ProfileReport(data, minimal=True)

    report_html = report.to_html()

    # Render the report in Streamlit
    st.components.v1.html(report_html, height=800, scrolling=True)

