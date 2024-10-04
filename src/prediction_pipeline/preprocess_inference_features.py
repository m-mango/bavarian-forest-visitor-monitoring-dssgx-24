"""
This script processes and merges weather data with visitor center data to create a comprehensive 
inference dataset for prediction. It imports necessary functions for sourcing and preprocessing weather and visitor 
center data, as well as functions for feature engineering related to z-scores and holiday distances. 

The main functionalities include:

1. **Merging Data**: The `join_inference_data` function merges weather data with selected columns 
   from visitor center data based on a common 'Time' column.
   
2. **Data Preprocessing**: The `source_preprocess_inference_data` function sources weather and 
   visitor center data for a specified date range, processes it to compute additional features 
   (like holiday distances, daily maximum values, and moving z-scores), and filters the data to 
   include only future timestamps.

The result is a processed DataFrame ready for further analysis or modeling.
"""
# Write the paths from src when called from the Main.py
from sourcing_data.source_weather import source_weather_data
from sourcing_data.source_visitor_center_data import source_visitor_center_data
from pre_processing.preprocess_visitor_center_data import process_visitor_center_data
from pre_processing.features_zscoreweather_distanceholidays import add_nearest_holiday_distance, add_daily_max_values, add_moving_z_scores
# Import the transformations from the training feature selection script
from source_and_feature_selection import process_transformations

from datetime import datetime
import pandas as pd



weather_columns_for_zscores = ['Temperature (°C)', 'Relative Humidity (%)', 'Wind Speed (km/h)']
window_size_for_zscores = 5

def join_inference_data(weather_data_inference, visitor_centers_data):

    """Merge weather data with visitor centers data.

    Args:
        weather_data_inference (pd.DataFrame): DataFrame containing weather data.
        visitor_centers_data (pd.DataFrame): DataFrame containing visitor centers data.

    Returns:
        pd.DataFrame: Merged DataFrame with selected columns from visitor centers data.
    """

    # Define the columns you want to bring from visitor_centers_data
    columns_to_add = ['Time','Tag', 'Hour', 'Monat','Wochentag',  'Wochenende',  'Jahreszeit',  'Laubfärbung',
                    'Schulferien_Bayern', 'Schulferien_CZ','Feiertag_Bayern',  'Feiertag_CZ',
                    'HEH_geoeffnet',  'HZW_geoeffnet',  'WGM_geoeffnet', 'Lusenschutzhaus_geoeffnet',  'Racheldiensthuette_geoeffnet', 'Falkensteinschutzhaus_geoeffnet', 'Schwellhaeusl_geoeffnet']  

    # Perform the merge, keeping all rows from weather_data
    merged_data = pd.merge(
                weather_data_inference,
                visitor_centers_data[columns_to_add],  # Select only the columns you need
                how='left',  # Keep all rows from weather_data
                on='Time'  # Join on the 'Time' column
                )
    
    return merged_data


def source_preprocess_inference_data():

    """Source and preprocess inference data from weather and visitor center sources.

    This function fetches weather and visitor center data, merges them, and computes additional features
    such as nearest holiday distance, daily max values, and moving z-scores.

    Returns:
        pd.DataFrame: DataFrame containing preprocessed inference data.
    """

    ## Source Weather Data for inference
    # get weather for previous 10 days to calculate zscores
    weather_data_inference = source_weather_data(start_time = datetime.now() - pd.Timedelta(days=10), 
                                                 end_time = datetime.now() + pd.Timedelta(days=7))

    ## Source Visitor Center Data for inference
    visitor_center_data = source_visitor_center_data()
    processed_visitor_center_data = process_visitor_center_data(visitor_center_data)
    # process_visitor_center_data() returns a tuple with hourly data and daily data, we just need the first one
    hourly_visitor_center_data = processed_visitor_center_data[0]
    #hour column was not being created in process_visitor_center_data()
    hourly_visitor_center_data['Hour'] = hourly_visitor_center_data['Time'].dt.hour
    join_df = join_inference_data(weather_data_inference, hourly_visitor_center_data)

    # Get z scores for the weather columns
    inference_data_with_distances = add_nearest_holiday_distance(join_df)

    inference_data_with_daily_max = add_daily_max_values(inference_data_with_distances, weather_columns_for_zscores)

    inference_data_with_new_features = add_moving_z_scores(inference_data_with_daily_max, 
                                                           weather_columns_for_zscores, 
                                                           window_size_for_zscores)


    # Apply the cyclic and categorical trasformations from the training dataset (same as the training dataset)
    inference_data_with_coco_enconding = process_transformations(inference_data_with_new_features)

    # drop data for any day previous to datetime.now()
    inference_data_with_coco_enconding = inference_data_with_coco_enconding[
                                        inference_data_with_coco_enconding["Time"] >= datetime.now()
                                        ]
    

    #set Time column as index   
    inference_data_with_coco_enconding = inference_data_with_coco_enconding.set_index('Time')
    #drop column named Date
    inference_data_with_coco_enconding = inference_data_with_coco_enconding.drop(columns=['Date'])
    
    return inference_data_with_coco_enconding