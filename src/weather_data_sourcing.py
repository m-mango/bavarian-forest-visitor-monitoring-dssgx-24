
"""
Weather Data Sourcing

This script retrieves hourly weather data (Precipitation, Temperature, Wind Speed, Relative Humidity, and Sunshine Duration) for the Bavarian Forest region from the Meteostat API, and saves the processed data to a CSV file.

Usage:
- To run this script, simply execute it using Python:
  $ python src/weather_data_sourcing.py
- The script will automatically fetch weather data for the specified date range, process it, and save it to a CSV file.

Output:
- The processed data will be saved as 'bf-weather.csv' in the './outputs/weather_data_final/' directory.
"""

# Import necessary libraries
import warnings
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
from meteostat import Point, Hourly

# Ignore warnings
warnings.filterwarnings('ignore')



############################################################################################################
# Define global variables
############################################################################################################

# Set time period for sourcing the data
START_TIME = datetime(2017, 1, 1)
END_TIME = datetime(2024, 7, 31)

# Coordinates of the Bavarian Forest (Haselbach)
# These coordinates are based on the weather recommendation by Google for a Bavarian Forest Weather search
LATITUDE = 49.31452390542327
LONGITUDE = 12.711573421032


############################################################################################################
# Define functions
############################################################################################################

def get_hourly_data(region, start_date, end_date):
    """
    Fetch hourly weather data for a specified region and date range.

    This function retrieves hourly weather data from the Meteostat API or another defined source,
    returning it as a pandas DataFrame.

    Args:
        region (Point): A `Point` object representing the geographical location (latitude, longitude).
        start_date (datetime): The start date for data retrieval.
        end_date (datetime): The end date for data retrieval.

    Returns:
        pandas.DataFrame: A DataFrame containing hourly weather data with the following columns:
            - time: Datetime of the record.
            - temp: Temperature in degrees Celsius.
            - dwpt: Dew point in degrees Celsius.
            - prcp: Precipitation in millimeters.
            - wdir: Wind direction in degrees.
            - wspd: Wind speed in km/h.
            - wpgt: Wind gust in km/h.
            - pres: Sea-level air pressure in hPa.
            - tsun: Sunshine duration in minutes.
            - snow: Snowfall in millimeters.
            - rhum: Relative humidity in percent.
            - coco: Weather condition code.
    """
    # Fetch hourly data
    data = Hourly(region, start_date, end_date).fetch()
    
    # Reset the index
    data.reset_index(inplace=True)
    return data


def process_hourly_data(data):
    """
    Process raw hourly weather data by cleaning and formatting.

    This function drops unnecessary columns, renames the remaining columns to more descriptive names,
    and converts the 'time' column to a datetime format.

    Args:
        data (pandas.DataFrame): A DataFrame containing raw hourly weather data.

    Returns:
        pandas.DataFrame: A DataFrame containing the processed hourly weather data with the following columns:
            - Time: Datetime of the record.
            - Temperature (°C): Temperature in degrees Celsius.
            - Precipitation (mm): Precipitation in millimeters.
            - Wind Speed (km/h): Wind speed in km/h.
            - Sunshine Duration (min): Duration of sunshine in minutes.
            - Relative Humidity (%): Relative humidity in percent.
    """
    # Drop unnecessary columns
    data = data.drop(columns=['dwpt', 'snow', 'wdir', 'wpgt', 'pres', 'coco'])

    # Rename columns for clarity
    data = data.rename(columns={
        'time': 'Time',
        'temp': 'Temperature (°C)',
        'prcp': 'Precipitation (mm)',
        'wspd': 'Wind Speed (km/h)',
        'tsun': 'Sunshine Duration (min)',
        'rhum': 'Relative Humidity (%)'
    })

    # Convert the 'Time' column to datetime format
    data['Time'] = pd.to_datetime(data['Time'])
    return data


def save_data_to_csv(data, save_path):
    """
    Save processed weather data to a CSV file.

    This function saves the processed DataFrame to a specified directory. If the directory does not exist,
    it will be created.

    Args:
        data (pandas.DataFrame): A DataFrame containing the processed hourly weather data.
        save_path (str): The directory path where the CSV file will be saved.

    Returns:
        None
    """
    # Create the directory if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    # Save the data to CSV
    data.to_csv(os.path.join(save_path, 'bf-weather.csv'), index=False)
    print('Data saved successfully!')


def main():
    """
    This function creates a point over the Bavarian Forest National Park, retrieves hourly weather data
    for the specified time period, processes the data to extract necessary weather parameters,
    and saves the processed data to a CSV file.
    """
    # Create a Point object for the Bavarian Forest National Park entry
    bavarian_forest = Point(lat=LATITUDE, lon=LONGITUDE)

    # Fetch hourly data for the location
    hourly_data = get_hourly_data(bavarian_forest, START_TIME, END_TIME)

    # Process the hourly data to extract and format necessary weather parameters
    processed_hourly_data = process_hourly_data(hourly_data)

    # Save the processed data to a CSV file
    save_data_to_csv(processed_hourly_data, save_path='./outputs/weather_data_final/')


# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()