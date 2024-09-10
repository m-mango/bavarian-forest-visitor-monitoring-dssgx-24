import streamlit as st
from src.streamlit_app.pages_in_dashboard.data_accessibility.data_retrieval import get_retrieved_df
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
# from streamlit_pandas_profiling import st_profile_report


def get_visualization_section():
    """
    Get the visualization section.
    """
    st.markdown("# Data visualization")

    # get the data from the query
    retrieved_df = get_retrieved_df()

    # # display the data
    # st.write(retrieved_df)

    # display the visualization
    # Do a very basic line plot of the dataframe with maiking the time column as the index
    retrieved_df["Time"] = pd.to_datetime(retrieved_df["Time"])
    retrieved_df.set_index("Time", inplace=True)

    st.line_chart(retrieved_df)


    # # add a download button and add two options to download the data in csv or excel format
    # if st.button("Download Options"):
    #     st.markdown("## Download the data")
    #     st.markdown("Click below to download the data.")
    #     st.markdown("### Download as CSV")
    #     csv = retrieved_df.to_csv(index=False)
    #     st.markdown(f'<a href="data:file/csv;base64,{csv}" download="data.csv">Download CSV File</a>', unsafe_allow_html=True)

    # Generate Pandas Profiling report
    # pr = retrieved_df.profile_report()
    pr = ProfileReport(retrieved_df, minimal=True, dark_mode=True)
    st_profile_report(pr)

    # export=pr.to_html()
    # st.download_button(label="Download Full Report", data=export, file_name='report.html')


    # st.write("### Profiling Report")
    # st_profile_report(profile)
