
from src.source_data import source_all_data
import altair as alt
import src.streamlit_app.page_layout_config as page_layout_config
from PIL import Image

import awswrangler as wr
import boto3

bucket = "dssgx-munich-2024-bavarian-forest"
raw_data_folder = "raw-data"
preprocessed_data_folder = "preprocessed_data"

def source_historic_visitor_counting_data():
    boto3.setup_default_session(profile_name='TM-DSSGx')

    def load_csv_files_from_aws_s3(path: str, **kwargs) -> pd.DataFrame:
        """Loads individual or multiple CSV files from an AWS S3 bucket.

        Args:
            path (str): The path to the CSV files on AWS S3.
            **kwargs: Additional arguments to pass to the read_csv function.

        Returns:
            pd.DataFrame: The DataFrame containing the data from the CSV files.
        """

        df = wr.s3.read_csv(path=path, **kwargs)
        return df

    historic_visitor_counts = load_csv_files_from_aws_s3(
        path=f"s3://{bucket}/{raw_data_folder}/hourly-historic-visitor-counts-all-sensors/",
        skiprows=2
    )

    print(f"Historic Visitor Counting Data sourced with {historic_visitor_counts.shape[0]} rows and {historic_visitor_counts.shape[1]} columns. The dataframe looks like:\n{historic_visitor_counts.head()}")

    return historic_visitor_counts


def create_dashboard():
    col1, col2 = page_layout_config.get_page_layout()

    with col1:
        logo = Image.open("src/streamlit_app/assets/bf_logo2.png")
        st.image(logo, width=100)
        st.title("Plan Your Trip to the Bavarian Forest")

    with col2:
        st.write("Hello col 2")
        # # get the language selection menu
        # get_language_selection_menu()
        
        # # get the weather section
        # get_weather_section()

        # # create recreational section
        # get_recreation_section()

    

def pipeline():

    historic_visitor_counts, all_parking_data, weather_data_df = source_all_data()

    print(historic_visitor_counts.head(), all_parking_data.head(), weather_data_df.head())

    return

if __name__ == "__main__":

    pipeline()

    create_dashboard()

    