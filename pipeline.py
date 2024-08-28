import pandas as pd
import streamlit as st

def source_historic_visitor_counting_data():
    print("Historic Visitor Counting Data sourced.")

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

    