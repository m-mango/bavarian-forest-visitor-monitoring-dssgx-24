from ydata_profiling import ProfileReport
import streamlit as st

@st.cache_data(max_entries=1)
def custom_pandas_profiling_report(data):
    
    print("Profiling the uploaded data...")

    report = ProfileReport(data, minimal=True)

    report_html = report.to_html()

    # Render the report in Streamlit
    st.components.v1.html(report_html, height=800, scrolling=True)

