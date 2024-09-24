import streamlit as st
import pandas as pd
import awswrangler as wr
from ydata_profiling import ProfileReport

# AWS Setup
bucket = "dssgx-munich-2024-bavarian-forest"
base_folder = "raw-data/bf_raw_files"

def write_csv_file_to_aws_s3(df: pd.DataFrame, path: str, **kwargs) -> None:
    """Writes a CSV file to AWS S3."""
    wr.s3.to_csv(df, path=path, **kwargs)

def read_csv_file(uploaded_file):
    """Reads a CSV file uploaded by the user."""
    return pd.read_csv(uploaded_file, parse_dates=True, infer_datetime_format=True, low_memory=False)

def generate_file_name(category: str, upload_timestamp: str) -> str:
    """Generates a file name based on the category."""
    return f"{category.replace(' ', '_')}_uploaded_{upload_timestamp}.csv"

def list_files_in_s3(category: str) -> list:
    """Lists files in S3 for a given category and returns only file names."""
    s3_prefix = f"{base_folder}/{category.replace(' ', '_')}"
    full_paths = wr.s3.list_objects(f"s3://{bucket}/{s3_prefix}/")
    return [path.split('/')[-1] for path in full_paths]  # Extract only the file names

def load_csv_files_from_aws_s3(path: str, **kwargs) -> pd.DataFrame:
    """Loads individual or multiple CSV files from an AWS S3 bucket."""
    df = wr.s3.read_csv(path=path, **kwargs)
    return df
def custom_pandas_profiling_report(report):
    """Injects custom CSS into the Pandas Profiling report, including header, footer, and other components."""
    report_html = report.to_html()

    # Define custom CSS styles for theming
    custom_styles = """
    <style>
        /* General body styles */
        body {
            background-color: #000000;
            color: #fafafa;
            font-family: 'sans serif';
        }

        /* Header styling */
        .profile-header {
            background-color: #000000 !important;
            color: #fafafa !important;
        }
        .profile-header h1 {
            color: #fafafa !important;
        }
        /* Customize the icon dropdown menu */
        .profile-header .icon-menu, .profile-header .icon-menu:hover {
            color: #fafafa !important;
        }

        /* Sidebar (Overview, Variables) */
        .nav-tabs {
            background-color: #333333 !important;
        }
        .nav-tabs .nav-link {
            color: #fafafa !important;
        }
        .nav-tabs .nav-link.active {
            background-color: #f63366 !important;  /* Highlight active tab */
            color: #000000 !important;
        }

        /* Footer styling */
        .profile-footer {
            background-color: #000000 !important;
            color: #fafafa !important;
        }
        .profile-footer p {
            color: #fafafa !important;
        }

        /* Content area styling */
        .report-content, .container {
            background-color: #000000 !important;
            color: #fafafa !important;
        }

        /* Headings and section titles */
        .title, .section-header, h1, h2, h3, h4, h5, h6 {
            color: #fafafa !important;
        }

        /* Tables */
        .table, .dataframe, .df {
            color: #fafafa !important;
        }
        .dataframe thead th {
            color: #fafafa !important;
            background-color: #333333; /* Darker background for table headers */
        }
        .dataframe tbody tr:nth-child(odd) {
            background-color: #333333;
        }
        .dataframe tbody tr:nth-child(even) {
            background-color: #444444;
        }
        .dataframe td {
            color: #fafafa !important;
        }

        /* Dropdowns */
        .dropdown-menu, .selectbox {
            background-color: #333333;
            color: #fafafa;
        }
        .dropdown-menu a, .selectbox option {
            color: #fafafa;
        }

        /* Form elements */
        input, textarea, select {
            background-color: #333333;
            color: #fafafa;
        }
        input::placeholder, textarea::placeholder {
            color: #fafafa;
        }
    </style>
    """
    
    # Inject the custom styles into the report's HTML
    report_html = custom_styles + report_html

    # Render the report in Streamlit
    st.components.v1.html(report_html, height=800, scrolling=True)

def get_upload_and_download_section():
    """Main function to handle Streamlit app logic for uploading, processing, and downloading data."""
    st.markdown("## Data Access Point")

    # Tabs for Upload and Download
    tab1, tab2 = st.tabs(["Upload Data", "Download Data"])

    with tab1:
        st.header("Upload Data")
        
        # Select category
        category = st.selectbox(
            "Select the data category",
            ["visitor count sensors", "visitors count centers", "other"]
        )
        
        # File upload
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

        if uploaded_file and category:
            data = read_csv_file(uploaded_file)

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

            # Show the preview and summary report below the header
            st.dataframe(data)
            st.header("Data Summary Report")

            # Use the custom Pandas Profiling report function with the new theme
            pr = ProfileReport(data, minimal=True)
            custom_pandas_profiling_report(pr)

            if upload_confirm:
                # Capture upload timestamp
                upload_timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')

                # Generate file name and S3 path
                file_name = generate_file_name(category, upload_timestamp)
                s3_path = f"s3://{bucket}/{base_folder}/{category.replace(' ', '_')}/{file_name}"

                # Upload the file to AWS S3
                write_csv_file_to_aws_s3(data, s3_path, index=False)
                st.success("File successfully uploaded.")

    with tab2:
        st.header("Download Data")
        
        # Select category
        category = st.selectbox(
            "Select the data category to browse",
            ["visitor count sensors", "visitors count centers", "other"]
        )
        
        # List files based on category
        if category:
            files = list_files_in_s3(category)
            selected_file = st.selectbox("Select a file to preview", files) if files else None

            if selected_file:
                # Preview button (enabled only when a file is selected)
                preview_confirm = st.button(
                    label="Preview Data",
                    disabled=not selected_file,
                    help="Preview the data before confirming download"
                )

                if preview_confirm:
                    # Correctly construct the full path to the selected file
                    file_path = f"s3://{bucket}/{base_folder}/{category.replace(' ', '_')}/{selected_file}"

                    # Load and preview selected file
                    st.write(f"Preview of {selected_file}")
                    data = load_csv_files_from_aws_s3(file_path)
                    st.dataframe(data)

                    # Download button
                    st.download_button(
                        label="Download selected file as CSV",
                        data=data.to_csv(index=False),
                        file_name=selected_file,
                        mime='text/csv',
                    )

