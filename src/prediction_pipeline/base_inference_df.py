from src.prediction_pipeline.sourcing_data.source_weather import source_weather_data
from src.prediction_pipeline.sourcing_data.source_visitor_center_data import source_visitor_center_data
from src.prediction_pipeline.pre_processing.features_zscoreweather_distanceholidays import add_nearest_holiday_distance, add_daily_max_values, add_moving_z_scores
from src.prediction_pipeline.source_and_feature_selection import apply_cliclic_tranformations
from datetime import datetime
import pandas as pd

"""
This script processes and merges weather data with visitor center data to create a comprehensive 
inference dataset for analysis. It imports necessary functions for sourcing weather and visitor 
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
    columns_to_add = ['Time','Tag',  'Monat','Wochentag',  'Wochenende',  'Jahreszeit',  'Laubfärbung',
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
    #get weather for previous 10 days to calculate zscores
    weather_data_inference = source_weather_data(start_time = datetime.now() - pd.Timedelta(days=10), 
                                                 end_time = datetime.now() + pd.Timedelta(days=7))

    # get visitor center data
    visitor_center_data = source_visitor_center_data()
    visitor_center_data["Time"] = pd.to_datetime(visitor_center_data["Time"])

    join_df = join_inference_data(weather_data_inference, visitor_center_data)

    #feature engineering
    inference_data_with_distances = add_nearest_holiday_distance(join_df)

    inference_data_with_daily_max = add_daily_max_values(inference_data_with_distances, weather_columns_for_zscores)

    inference_data_with_new_features = add_moving_z_scores(inference_data_with_daily_max, 
                                                           weather_columns_for_zscores, 
                                                           window_size_for_zscores)
    
    inference_data_with_cyclic_features = apply_cliclic_tranformations(inference_data_with_new_features, cyclic_features = ['Tag','Hour', 'Monat', 'Wochentag'])

    #slice from start time = today
    inference_data_with_cyclic_features = inference_data_with_cyclic_features[
                                        inference_data_with_cyclic_features["Time"] >= datetime.now()
                                        ]

    return inference_data_with_cyclic_features