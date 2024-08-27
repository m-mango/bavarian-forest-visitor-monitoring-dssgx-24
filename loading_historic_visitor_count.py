"""
Loading Historic Sensors Data Script

This script loads multiple csv's with the required encoding, concatenates them, and writes a csv file with the product. 


Usage:
- Ensure the data file is located at 'data\manual_visitor_counts'.
- Run the script:
  $ python src/loading_historic_visitor_count.py

Output:
- The complete data is saved as 'bf-weather-imputed.csv' in the './outputs/weather_data_final/' directory.
- A plot of temperature and precipitation is saved as 'bf-weather.png' in the same directory.
"""


import pandas as pd
import locale
import glob
import chardet

def read_data_per_file(file: str) -> pd.DataFrame:
    """
    Reads data from a CSV file and returns it as a pandas DataFrame. Handles skipping rows

    Args:
        file (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The DataFrame containing the data from the CSV file.
    """
    # Detect the encoding
    with open(file, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    data =  pd.read_csv(file, encoding=encoding, skiprows=2)
        
    return data


