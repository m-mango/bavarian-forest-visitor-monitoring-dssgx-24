import pandas as pd
import streamlit as st
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

def source_current_bayern_cloud_parking_data():
    print("Current Bayern Cloud Parking Data sourced.")

def process_historic_visitor_counting_data():
    print("Historic Visitor Counting Data processed.")


def pipeline():
    source_historic_visitor_counting_data()
    source_current_bayern_cloud_parking_data()
    process_historic_visitor_counting_data()

def create_dashboard():
    st.title('Bavarian Forest - Digital Visitor Monitoring')

    def visualize_current_bayern_cloud_parking_data():
        print("Current Bayern Cloud Parking Data visualized.")



if __name__ == "__main__":

    pipeline()

    create_dashboard()

    