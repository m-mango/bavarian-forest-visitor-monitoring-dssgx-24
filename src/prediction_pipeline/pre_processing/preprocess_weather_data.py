"""
Weather Data Sourcing

This script retrieves hourly weather data (Precipitation, Temperature, Wind Speed, Relative Humidity, Sunshine Duration, and coco) for the Bavarian Forest region from the Meteostat API, and saves the processed data to a CSV file.

Usage:
- To run this script, simply execute it using Python:
  $ python src/weather_data_sourcing_and_processing.py
- The script will automatically fetch weather data for the specified date range, process it, and save it to a CSV file.
- Please change the AWS credentials, global variables (start and end time, latitude, and longitude), and the S3 bucket and folder name before running the script.

Output:
- The sourced and processed weather data is saved as '/sourced_weather_data_2016-24_non_imputed.csv' and '/processed_weather_data_2016-24_imputed.csv' in the 'preprocessed_data' folder 
    in the 'dssgx-munich-2024-bavarian-forest' AWS S3 bucket.

"""

# Import necessary libraries
import warnings

# Ignore warnings
warnings.filterwarnings('ignore')


############################################################################################################
# Define global variables
############################################################################################################
# Uncomment this if you want to get the weather data for the next 7 days starting from today
# Get dates for the data sourcing
# START_TIME = datetime.now()
# END_TIME = (START_TIME + pd.Timedelta(days=7))

# Set up S3 bucket and folder
bucket = "dssgx-munich-2024-bavarian-forest"
preprocessed_data_folder = "preprocessed_data"


############################################################################################################
# Define functions
############################################################################################################

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
                if data[parameter].dtype == 'category':
                    #fill with previous row value  
                    data[parameter].fillna(method='pad', inplace=True)
                else:
                # Use linear interpolation to fill missing values
                    data[parameter].interpolate(method='linear', inplace=True)
                    # Round the interpolated values to 2 decimal places
                    data[parameter] = data[parameter].round(2)
                    print(f'Missing values in {parameter} column filled using linear interpolation')

    return data



def process_weather_data(sourced_df):
    """
    This function creates a point over the Bavarian Forest National Park, retrieves hourly weather data
    for the specified time period, processes the data to extract necessary weather parameters,
    and saves the processed data to a CSV file.
    """
    sourced_df["coco_2"] = sourced_df["coco_2"].astype("category")
    # Get the list of columns to process
    parameters = sourced_df.columns.to_list()

    # Fill missing values in the weather data
    imputed_data = fill_missing_values(sourced_df, parameters)
    
    # # Uncomment the following line to save the processed data to a CSV file
    # # Save the processed data to a CSV file
    # save_data_to_csv(imputed_data, 'outputs/weather_data_final/processed_weather_data_2016-24_forecasted_imputed.csv')


    return imputed_data



