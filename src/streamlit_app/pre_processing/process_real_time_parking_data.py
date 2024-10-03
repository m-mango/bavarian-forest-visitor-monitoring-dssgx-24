# import libraries
import pandas as pd
import streamlit as st


def impute_missing_data(all_parking_data):

    # Fill missing values in the parking data

    # if there are null values in the capacity column, fill them with the with 40 (it is the lowest capacity value from all the sensors)
    all_parking_data['current_capacity'].fillna(40, inplace=True)

    # if there are null values in the occupancy column, fill them with the corresponding capacity value
    all_parking_data['current_occupancy'].fillna(all_parking_data['current_capacity'], inplace=True)

    # if there are null values in the occupancy rate column, fill them with the occupancy divided by the capacity   
    all_parking_data['current_occupancy_rate'].fillna(all_parking_data['current_occupancy']/all_parking_data['current_capacity'], inplace=True)


    # Convert to data type int

    all_parking_data['current_capacity'] = all_parking_data['current_capacity'].astype(int)
    all_parking_data['current_occupancy'] = all_parking_data['current_occupancy'].astype(int)

    # add a column called 'current availability' that is the difference between the capacity and the occupancy

    all_parking_data['current_availability'] = all_parking_data['current_capacity'] - all_parking_data['current_occupancy']

    return all_parking_data

def process_real_time_parking_data(parking_data_df):
    """
    Process the real-time parking data by imputing missing values.

    Args:
        parking_data_df (pandas.DataFrame): Raw real-time parking data.
    
    Returns:
        pandas.DataFrame: Processed real-time parking data.
    """


    clean_parking_data = impute_missing_data(parking_data_df)

    if 'preprocessed_parking_data' not in st.session_state:
        st.session_state['preprocessed_parking_data'] = clean_parking_data

    print("Parking data processed and cleaned!")

    return clean_parking_data

