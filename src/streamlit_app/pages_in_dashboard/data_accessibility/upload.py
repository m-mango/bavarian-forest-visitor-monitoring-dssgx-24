import pandas as pd
import streamlit as st
import awswrangler as wr
from src.streamlit_app.pages_in_dashboard.data_accessibility.pandas_profiling_styling import custom_pandas_profiling_report 
from src.streamlit_app.pre_processing.data_quality_check import data_quality_check

# AWS Setup
bucket = "dssgx-munich-2024-bavarian-forest"
base_folder = "raw-data/bf_raw_files"


def write_csv_file_to_aws_s3(df: pd.DataFrame, path: str, **kwargs) -> None:
    """Writes a CSV file to AWS S3."""
    wr.s3.to_csv(df, path=path, **kwargs)

def generate_file_name(category: str, upload_timestamp: str) -> str:
    """Generates a file name based on the category."""
    return f"{category.replace(' ', '_')}_uploaded_{upload_timestamp}.csv"

# Function to read the uploaded file
def read_csv_file(uploaded_file):
    # Check the file extension and read accordingly
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        return pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        return None

def upload_section():
    st.header("Upload Data")

    # Initialize session state variables if they don't exist
    if "data" not in st.session_state:
        st.session_state.data = None

    # Select category
    category = st.selectbox(
        "Select the data category",
        ["visitor_count_sensors", "visitors_count_centers", "other"],
    )

    # File upload
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

    # Initialize `data` to None
    data = None

    # Only read the file if it has been uploaded
    if uploaded_file:
        # Process based on category
        if category == "visitor_count_sensors":
            data = pd.read_csv(uploaded_file, skiprows=2, index_col=None)
        elif category == "visitors_count_centers":
            data = pd.read_excel(uploaded_file, dtype=object, engine =  'openpyxl')
        elif category == "other":
            data = pd.read_csv(uploaded_file)

    # Ensure that both file and category are provided before proceeding
    if uploaded_file and category and data is not None:
        # Store the data in session state
        st.session_state.data = data

        # Display the header and place the upload button next to it
        st.write(" ")  # Add some space between elements
        col_preview, col_upload = st.columns([8, 2])

        with col_preview:
            st.header("Preview of Data")

        with col_upload:
            # Confirm button (aligned to the right side, bigger size)
            upload_confirm = st.button(
                label="Confirm Upload",
                disabled=not uploaded_file,
                help="Review the data before confirming upload",
            )
            st.write(f"<style>.stButton > button {{width: 100%; height: 50px;}}</style>", unsafe_allow_html=True)

        if not upload_confirm:
            # Show the preview and summary report below the header
            st.dataframe(st.session_state.data)
            st.header("Data Summary Report")

            # Use the custom Pandas Profiling report function with the new theme
            custom_pandas_profiling_report(st.session_state.data)

        if upload_confirm:
            # Send the uploaded file to data_quality_check instead of the DataFrame
            status = data_quality_check(st.session_state.data, category)

            if not status:
                st.error("Data quality check failed. Please check the data and try again.")
            else:
                st.success("Data quality check passed.")
                # Capture upload timestamp
                upload_timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')

                # Generate file name and S3 path
                file_name = generate_file_name(category, upload_timestamp)
                s3_path = f"s3://{bucket}/{base_folder}/{category.replace(' ', '_')}/{file_name}"

                # Upload the file to AWS S3
                write_csv_file_to_aws_s3(st.session_state.data, s3_path, index=False)
                st.success("File successfully uploaded.")
