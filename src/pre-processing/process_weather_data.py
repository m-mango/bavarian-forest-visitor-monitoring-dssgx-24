# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import warnings

# Ignore warnings
warnings.filterwarnings('ignore')

import source_data as sd

def fill_missing_values(data, parameters):
    """
    Fill missing values in the weather data using linear interpolation or zero values.

    Args:
        data (pandas.DataFrame): Processed hourly weather data.
        parameters (list): List of column names to process.

    Returns:
        pandas.DataFrame: DataFrame with missing values filled.
    """
    total_rows = data.shape[0]

    for parameter in parameters:
        # Calculate missing values and their percentage
        missing_values = data[parameter].isnull().sum()
        missing_percentage = (missing_values / total_rows) * 100

        # Calculate zero values and their percentage
        zero_values = data[parameter].eq(0).sum()
        zero_percentage = (zero_values / total_rows) * 100

        # Check for missing values in the 'Time' column
        if parameter == 'Time' and missing_values > 0:
            print(f'Missing values in Time column: {missing_percentage:.2f}%')
            print('Please check the missing values in the Time column')
            exit()

        if missing_values == 0:
            print(f'No missing values in {parameter} column')
        else:
            print(f'Missing values in {parameter} column: {missing_percentage:.2f}%')

            if zero_percentage > 60:
                # Fill missing values with 0.0 if zero values are significant
                print(f'Zero values in {parameter} column: {zero_percentage:.2f}%')
                data[parameter].fillna(0.0, inplace=True)
                print(f'Missing values in {parameter} column filled with 0.0')
            else:
                # Use linear interpolation to fill missing values
                data[parameter].interpolate(method='linear', inplace=True)
                # Round the interpolated values to 2 decimal places
                data[parameter] = data[parameter].round(2)
                print(f'Missing values in {parameter} column filled using linear interpolation')

    return data


def main():

    _,_, weather_data_df = sd.source_all_data()

        # Get the list of columns to process
    parameters = weather_data_df.columns.to_list()

    print(f'Processing weather data with the following columns: {parameters}')

    # Fill missing values in the weather data
    imputed_data = fill_missing_values(weather_data_df, parameters)

    return imputed_data
if __name__ == "__main__":
    main()


