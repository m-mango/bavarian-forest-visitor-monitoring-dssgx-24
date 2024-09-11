##################################################
# Package Import Section
##################################################
import pandas as pd  # Provides data structures and data analysis tools.
import numpy as np  # Supports large, multi-dimensional arrays and matrices.
import pyarrow as pa  # Provides functionalities for handling Apache Arrow data.
import pyarrow.parquet as pq  # Enables reading and writing Parquet files using PyArrow.

# Documentation:
# The above code imports essential libraries for data manipulation and file handling:
# - `pandas` is used for data manipulation and analysis, providing data structures such as DataFrames.
# - `numpy` is used for numerical operations and supports multi-dimensional arrays and matrices.
# - `pyarrow` is used for efficient handling of Arrow data, which is a cross-language development platform for in-memory data.
# - `pyarrow.parquet` is specifically used for reading and writing Parquet files, which is a columnar storage file format optimized for use with big data processing frameworks.

# Note: Ensure these libraries are installed in your environment. You can install them using pip:
# pip install pandas numpy pyarrow

##########################################################################
##########################################################################
# Import raw data
##########################################################################
##########################################################################

# Import raw data
# Define the path to the Excel file containing the raw data
file_path = r'C:\Users\garov\OneDrive\Documents\GitHub\bavarian-forest-visitor-monitoring-dssgx-24\outputs\Raw Data\national-park-vacation-times-houses-opening-times.xlsx'

# Load the Excel file into a DataFrame
# `pd.read_excel` reads an Excel file into a pandas DataFrame.
# In this case, the file contains data related to national park vacation times and house opening times.
df_visitcenters = pd.read_excel(file_path)

# Documentation:
# - `file_path` is a string that specifies the location of the Excel file on the local filesystem.
# - `pd.read_excel` is used to load the data from the specified Excel file into a pandas DataFrame.
# - `df_visitcenters` is the DataFrame that will store the data loaded from the Excel file.

# Note: Ensure the specified file path is correct and the Excel file exists at that location. The file should be accessible and readable by the script.

##########################################################################
##########################################################################
# Modify data types
##########################################################################
##########################################################################

# Change all binary variables (0, 1) from float64 type to bool type
# Iterate over each column in the DataFrame
for column in df_visitcenters.columns:
    # Check if all values in the column are either 0, 1, or NaN
    if df_visitcenters[column].isin([0, 1, np.nan]).all():
        # Convert the column to boolean type (binary values: True, False)
        df_visitcenters[column] = df_visitcenters[column].astype('bool')

# Documentation:
# - This code converts columns in the DataFrame `df_visitcenters` that contain only binary values (0 and 1) to a boolean type.
# - `df_visitcenters[column].isin([0, 1, np.nan]).all()` checks if all values in the column are either 0, 1, or NaN.
# - `astype('bool')` converts the column from float64 type to boolean type, where 0 becomes False and 1 becomes True.

# Convert columns with object data type to category type
# This is useful for categorical variables with more than 3 levels
for col in df_visitcenters.select_dtypes(include=['object']).columns:
    df_visitcenters[col] = df_visitcenters[col].astype('category')

# Print the data types of each column to verify the conversion
print(df_visitcenters.dtypes)

# Documentation:
# - This code converts columns in the DataFrame `df_visitcenters` with data type 'object' to 'category' type.
# - `df_visitcenters.select_dtypes(include=['object']).columns` selects columns with 'object' data type, which are typically string variables.
# - `astype('category')` changes these columns to 'category' type, which is more memory efficient and suitable for categorical data.
# - `print(df_visitcenters.dtypes)` displays the data types of all columns in the DataFrame to verify the conversion.

# Convert specific columns to numeric type (float64)
# Using 'errors="coerce"' will convert invalid parsing to NaN
df_visitcenters['Parkpl_HEH_PKW'] = pd.to_numeric(df_visitcenters['Parkpl_HEH_PKW'], errors='coerce')
df_visitcenters['Waldschmidthaus_geoeffnet'] = pd.to_numeric(df_visitcenters['Waldschmidthaus_geoeffnet'], errors='coerce')

# Documentation:
# - This section of the script converts specific columns in the DataFrame `df_visitcenters` from object type to numeric (float64) type.
# - The function `pd.to_numeric(df_visitcenters['Parkpl_HEH_PKW'], errors='coerce')` is used to convert the 'Parkpl_HEH_PKW' column to numeric type, with errors being coerced to NaN.
# - Similarly, `pd.to_numeric(df_visitcenters['Waldschmidthaus_geoeffnet'], errors='coerce')` converts the 'Waldschmidthaus_geoeffnet' column to numeric type.

# Convert specific columns representing binary variables to boolean type
df_visitcenters['Schulferien_Bayern'] = df_visitcenters['Schulferien_Bayern'].astype(bool)
df_visitcenters['Schulferien_CZ'] = df_visitcenters['Schulferien_CZ'].astype(bool)

# Documentation:
# - This section of the script converts specific columns in the DataFrame `df_visitcenters` that represent binary variables to boolean type.
# - The function `astype(bool)` changes the 'Schulferien_Bayern' and 'Schulferien_CZ' columns to boolean type, where 0 becomes False and 1 becomes True.

# Find indices of the date '9/29/2021'
indices = df_visitcenters[df_visitcenters['Datum'] == '9/29/2021'].index

# Ensure there is a second instance
if len(indices) > 1:
    # Replace the second instance with '9/29/2023'
    df_visitcenters.at[indices[1], 'Datum'] = '9/29/2023'

# Documentation:
# - This section of the script identifies rows in the DataFrame `df_visitcenters` where the 'Datum' column has the date '9/29/2021'.
# - `df_visitcenters[df_visitcenters['Datum'] == '9/29/2021'].index` finds the indices of these rows. This date is duplicated in the raw data.
# - If there is more than one occurrence of the date '9/29/2021', the second occurrence is updated to '9/29/2023'.
# - If there is no second instance, no action is taken.

##########################################################################
##########################################################################
# Create New Variables/Columns
##########################################################################
##########################################################################

def add_date_variables(df):
    """
    Create new columns for day, month, and year from a date column in the DataFrame.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing the 'Datum' column with date information.
    
    Returns:
    pandas.DataFrame: DataFrame with additional columns for day, month, and year.
    """
    # Convert 'Datum' column to datetime format
    df['Datum'] = pd.to_datetime(df['Datum'])
    
    # Add new columns for day, month, and year
    df['Tag'] = df['Datum'].dt.day
    df['Monat'] = df['Datum'].dt.month
    df['Jahr'] = df['Datum'].dt.year
    
    # Change data types for modeling purposes
    df['Tag'] = df['Tag'].astype('Int64')
    df['Monat'] = df['Monat'].astype('category')
    df['Jahr'] = df['Jahr'].astype('Int64')
    
    return df

# Usage example
df_visitcenters = add_date_variables(df_visitcenters)

# Documentation:
# - The function `add_date_variables` takes a DataFrame `df` with a 'Datum' column and adds new columns for day ('Tag'), month ('Monat'), and year ('Jahr').
# - It converts the 'Datum' column to datetime format and extracts day, month, and year into separate columns.
# - The new columns are cast to appropriate data types for further analysis or modeling.

def add_season_variable(df):
    """
    Create a new column 'Jahreszeit' in the DataFrame based on the month variable.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing the 'Monat' column with month information.
    
    Returns:
    pandas.DataFrame: DataFrame with an additional 'Jahreszeit' column representing the season.
    """
    # Define the seasons based on the month
    df['Jahreszeit'] = df['Monat'].apply(
        lambda x: 'Frühling' if x in [3, 4, 5] else
                  'Sommer' if x in [6, 7, 8] else
                  'Herbst' if x in [9, 10, 11] else
                  'Winter' if x in [12, 1, 2] else
                  np.nan
    )
    
    # Convert the 'Jahreszeit' column to category type
    df['Jahreszeit'] = df['Jahreszeit'].astype('category')
    
    return df

# Apply the function to df_visitcenters
df_visitcenters = add_season_variable(df_visitcenters)

# Documentation:
# - The function `add_season_variable` takes a DataFrame `df` with a 'Monat' column and creates a new column 'Jahreszeit' that represents the season.
# - The lambda function within `apply` assigns the season based on the month value: 'Frühling' for March-May, 'Sommer' for June-August, 'Herbst' for September-November, and 'Winter' for December-February.
# - `np.nan` is used for any month values not matching these ranges, though in practice, all month values should be covered.
# - The new 'Jahreszeit' column is then converted to a category type for efficient handling of categorical data.

def add_and_translate_day_of_week(df):
    """
    Create a new column 'Wochentag' that represents the day of the week in German.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing the 'Datum' column with date information.
    
    Returns:
    pandas.DataFrame: DataFrame with updated 'Wochentag' column in German.
    """
    # Create a new column 'Wochentag2' with the day of the week in English
    df['Wochentag2'] = df['Datum'].dt.day_name()
    df['Wochentag2'] = df['Wochentag2'].astype('category')
    
    # Define the translation mapping from English to German
    translation_map = {
        'Monday': 'Montag',
        'Tuesday': 'Dienstag',
        'Wednesday': 'Mittwoch',
        'Thursday': 'Donnerstag',
        'Friday': 'Freitag',
        'Saturday': 'Samstag',
        'Sunday': 'Sonntag'
    }
    
    # Replace the English day names in the 'Wochentag2' column with German names
    df['Wochentag2'] = df['Wochentag2'].replace(translation_map)
    
    # Remove the 'Wochentag' column from the DataFrame
    df = df.drop(columns=['Wochentag'], errors='ignore')
    
    # Rename 'Wochentag2' to 'Wochentag'
    df = df.rename(columns={'Wochentag2': 'Wochentag'})
    
    return df

# Apply the function to df_visitcenters
df_visitcenters = add_and_translate_day_of_week(df_visitcenters)

# Documentation:
# - The function `add_and_translate_day_of_week` creates a new column 'Wochentag' in the DataFrame based on the 'Datum' column, showing the day of the week in German.
# - It first generates 'Wochentag2' with the day names in English and converts it to a category type.
# - A translation map is used to replace English day names with German equivalents.
# - The original 'Wochentag' column is removed, and 'Wochentag2' is renamed to 'Wochentag'.
# - `errors='ignore'` is used in `drop` to avoid errors if 'Wochentag' column is not present.

def add_weekend_variable(df):
    """
    Create a new binary column 'Wochenende' indicating whether the day is a weekend.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing the 'Wochentag' column with German day names.
    
    Returns:
    pandas.DataFrame: DataFrame with an additional 'Wochenende' column indicating weekend status.
    """
    # Create a new binary column 'Wochenende' where True represents weekend days (Saturday, Sunday)
    df['Wochenende'] = df['Wochentag'].apply(lambda x: x in ['Samstag', 'Sonntag'])
    
    # Convert the 'Wochenende' column to boolean type
    df['Wochenende'] = df['Wochenende'].astype(bool)
    
    return df

# Apply the function to df_visitcenters
df_visitcenters = add_weekend_variable(df_visitcenters)

# Documentation:
# - The function `add_weekend_variable` adds a new column 'Wochenende' to the DataFrame `df`.
# - It sets 'Wochenende' to True if the day is 'Samstag' (Saturday) or 'Sonntag' (Sunday) and False otherwise.
# - The new 'Wochenende' column is converted to a boolean type for clarity and efficiency.

##########################################################################
##########################################################################
# Re-order variables to put date-related variables next to each other
##########################################################################
##########################################################################

def reorder_columns(df):
    """
    Reorder columns in the DataFrame to place date-related variables together.
    
    Parameters:
    df (pandas.DataFrame): DataFrame with various columns including date-related variables.
    
    Returns:
    pandas.DataFrame: DataFrame with columns reordered to place date-related variables next to each other.
    """
    # Define the desired order of columns
    column_order = [
        'Datum', 'Tag', 'Monat', 'Jahr', 'Wochentag', 'Wochenende', 'Jahreszeit', 'Laubfärbung',
        'Besuchszahlen_HEH', 'Besuchszahlen_HZW', 'Besuchszahlen_WGM', 
        'Parkpl_HEH_PKW', 'Parkpl_HEH_BUS', 'Parkpl_HZW_PKW', 'Parkpl_HZW_BUS', 
        'Schulferien_Bayern', 'Schulferien_CZ', 'Feiertag_Bayern', 'Feiertag_CZ', 
        'HEH_geoeffnet', 'HZW_geoeffnet', 'WGM_geoeffnet', 'Lusenschutzhaus_geoeffnet', 
        'Racheldiensthuette_geoeffnet', 'Waldschmidthaus_geoeffnet', 
        'Falkensteinschutzhaus_geoeffnet', 'Schwellhaeusl_geoeffnet', 'Temperatur', 
        'Niederschlagsmenge', 'Schneehoehe', 'GS mit', 'GS max'
    ]
    
    # Reorder columns in the DataFrame
    df = df[column_order]
    
    return df

# Apply the function to df_visitcenters
df_visitcenters = reorder_columns(df_visitcenters)

# Documentation:
# - The function `reorder_columns` rearranges the columns of the DataFrame `df` so that all date-related variables are grouped together.
# - The desired column order is specified in the `column_order` list.
# - The DataFrame `df` is then reordered according to this list of columns.

##########################################################################
##########################################################################
# Final Data Cleaning - Correct Specific Variables/Values that are Strange
##########################################################################
##########################################################################

def correct_and_convert_schulferien(df):
    """
    Corrects a typo in the 'Schulferien_Bayern' column and converts it to boolean type.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing the 'Schulferien_Bayern' column.
    
    Returns:
    pandas.DataFrame: DataFrame with corrected 'Schulferien_Bayern' values and converted to boolean type.
    """
    # Correct the typo in specific value for column 'Schulferien_Bayern' (from `10` to `0`)
    df.loc[df['Datum'] == '2017-04-30', 'Schulferien_Bayern'] = 0
    
    # Change 'Schulferien_Bayern' to bool type
    df['Schulferien_Bayern'] = df['Schulferien_Bayern'].astype(bool)
    
    return df

# Apply the function to df_visitcenters
df_visitcenters = correct_and_convert_schulferien(df_visitcenters)

# Documentation:
# - The function `correct_and_convert_schulferien` fixes a typo in the 'Schulferien_Bayern' column for a specific date and converts the column to boolean type.
# - The typo is corrected by setting the value to `0` where the date is '2017-04-30'.
# - The column 'Schulferien_Bayern' is then converted to boolean type to reflect correct binary values.

def correct_besuchszahlen_heh(df):
    """
    Corrects the 'Besuchszahlen_HEH' column by rounding up values with non-zero fractional parts to the nearest whole number.
    Converts the column to Int64 type to retain NaN values.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing the 'Besuchszahlen_HEH' column.
    
    Returns:
    pandas.DataFrame: DataFrame with 'Besuchszahlen_HEH' corrected and converted to Int64 type.
    """
    # Apply np.ceil() to round up values with non-zero fractional parts to nearest whole number
    df['Besuchszahlen_HEH'] = df['Besuchszahlen_HEH'].apply(
        lambda x: np.ceil(x) if pd.notna(x) and x % 1 != 0 else x
    )
    
    # Convert 'Besuchszahlen_HEH' to Int64 to retain NaN values
    df['Besuchszahlen_HEH'] = df['Besuchszahlen_HEH'].astype('Int64')
    
    return df

# Apply the function to df_visitcenters
df_visitcenters = correct_besuchszahlen_heh(df_visitcenters)

# Documentation:
# - The function `correct_besuchszahlen_heh` fixes the 'Besuchszahlen_HEH' column by rounding up values with fractional parts to the nearest whole number.
# - The use of `np.ceil()` ensures that any value with a non-zero decimal part is rounded up.
# - The column is then converted to Int64 type to retain NaN values while ensuring all numeric values are integers.

def correct_and_convert_wgm_geoeffnet(df):
    """
    Corrects the 'WGM_geoeffnet' column by replacing the value 11 with 1.
    Converts the column to boolean type.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing the 'WGM_geoeffnet' column.
    
    Returns:
    pandas.DataFrame: DataFrame with 'WGM_geoeffnet' corrected and converted to boolean type.
    """
    # Replace single value of 11 with 1 in 'WGM_geoeffnet' column
    df['WGM_geoeffnet'] = df['WGM_geoeffnet'].replace(11, 1)
    
    # Convert 'WGM_geoeffnet' column to boolean type
    df['WGM_geoeffnet'] = df['WGM_geoeffnet'].astype(bool)
    
    return df

# Apply the function to df_visitcenters
df_visitcenters = correct_and_convert_wgm_geoeffnet(df_visitcenters)

# Documentation:
# - The function `correct_and_convert_wgm_geoeffnet` fixes the 'WGM_geoeffnet' column by replacing any instance of the value `11` with `1`.
# - The column is then converted to boolean type to reflect the correct binary status.

def remove_last_row_if_needed(df):
    """
    Removes the last row from the DataFrame if it has 2923 rows.
    
    Parameters:
    df (pandas.DataFrame): DataFrame to be checked and modified.
    
    Returns:
    pandas.DataFrame: Updated DataFrame with the last row removed if the initial length was 2923.
    """
    # Check if the DataFrame has exactly 2923 rows
    if len(df) == 2923:
        # Drop the last row
        df = df.iloc[:-1]
    
    return df

# Apply the function to df_visitcenters
df_visitcenters = remove_last_row_if_needed(df_visitcenters)

# Documentation:
# - The function `remove_last_row_if_needed` removes the last row from the DataFrame `df` if it has exactly 2923 rows.
# - This ensures that the DataFrame has the expected number of rows after this operation.

def detect_outliers_std(df, column, num_sd=7):
    """
    Detect outliers in a specific column of the DataFrame using the standard deviation method.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing the column to check.
    column (str): Name of the column to check for outliers.
    num_sd (int): Number of standard deviations to define the outlier bounds (default is 7).
    
    Returns:
    pandas.DataFrame: DataFrame containing rows with outliers in the specified column.
    """
    mean = df[column].mean()
    std_dev = df[column].std()
    
    # Define the bounds for outliers
    lower_bound = mean - num_sd * std_dev
    upper_bound = mean + num_sd * std_dev
    
    # Identify outliers
    outliers_mask = (df[column] < lower_bound) | (df[column] > upper_bound)
    return df[outliers_mask][['Datum', column]]

def handle_outliers(df, columns, num_sd=7):
    """
    Detect and handle outliers for a list of columns by replacing them with NaN.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing the columns to check.
    columns (list): List of column names to check for outliers.
    num_sd (int): Number of standard deviations to define the outlier bounds (default is 7).
    
    Returns:
    pandas.DataFrame: DataFrame with outliers replaced by NaN in the specified columns.
    """
    outliers = {}
    
    # Detect outliers and store in dictionary
    for column in columns:
        outliers[column] = detect_outliers_std(df, column, num_sd)
    
    # Handle outliers by replacing with NaN
    for column in columns:
        mean = df[column].mean()
        std_dev = df[column].std()
        lower_bound = mean - num_sd * std_dev
        upper_bound = mean + num_sd * std_dev
        df.loc[(df[column] < lower_bound) | (df[column] > upper_bound), column] = np.nan
    
    return df, outliers

# Apply the function to df_visitcenters
df_visitcenters, outliers_dict = handle_outliers(df_visitcenters, columns_to_check)

# Documentation:
# - The function `detect_outliers_std` identifies outliers in a specified column using the standard deviation method.
# - The function `handle_outliers` applies the outlier detection to a list of columns, replaces detected outliers with NaN, and returns the modified DataFrame along with a dictionary of detected outliers.

##########################################################################
##########################################################################
# Create an hourly level DataFrame by expanding each day into 24 hours

# This hourly data frame is later joined with other data for predictions
##########################################################################
##########################################################################

def create_hourly_dataframe(df):
    """
    Expands the daily data in the DataFrame to an hourly level by duplicating each day into 24 hourly rows.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing daily data with a 'Datum' column representing dates.
    
    Returns:
    pandas.DataFrame: New DataFrame with an hourly level where each day is expanded into 24 hourly rows.
    """
    # Generate a new DataFrame where each day is expanded into 24 rows (one per hour)
    df_hourly = df.loc[df.index.repeat(24)].copy()
    
    # Create the hourly timestamps by adding hours to the 'Datum' column
    df_hourly['Datum'] = df_hourly['Datum'] + pd.to_timedelta(df_hourly.groupby(df_hourly.index).cumcount(), unit='h')
    
    # Rename columns for clarity
    df_hourly = df_hourly.rename(columns=lambda x: x.strip())
    df_hourly = df_hourly.rename(columns={'Datum': 'Time'})
    
    return df_hourly

# Apply the function to df_visitcenters
df_visitcenters_hourly = create_hourly_dataframe(df_visitcenters)

# Documentation:
# - The function `create_hourly_dataframe` transforms daily data into hourly data by expanding each date into 24 hourly rows.
# - The 'Datum' column is updated to reflect the hourly time stamps.
# - The columns are renamed for clarity, with 'Datum' changed to 'Time'.

##########################################################################
##########################################################################
# Function to rename columns and convert datetime
##########################################################################
##########################################################################

def prepare_data(df):
    """
    Rename columns, convert 'time' column to datetime, and set 'time' as the index.
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing data with a 'Datum' column to be renamed and converted.
    
    Returns:
    pandas.DataFrame: The cleaned DataFrame with 'Datum' renamed to 'time', converted to datetime, and 'time' set as index.
    """
    # Rename 'Datum' column to 'time'
    df.rename(columns={'Datum': 'time'}, inplace=True)
    
    # Convert 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'])
    
    # Set 'time' column as index
    df.set_index('time', inplace=True)
    
    return df

##########################################################################
##########################################################################
# Function to save DataFrames to CSV and Parquet files
##########################################################################
##########################################################################

def save_datasets(df_daily, df_hourly, csv_daily_path, csv_hourly_path, parquet_path):
    """
    Save cleaned DataFrames to CSV and Parquet files.
    
    Parameters:
    df_daily (pandas.DataFrame): DataFrame containing daily-level data.
    df_hourly (pandas.DataFrame): DataFrame containing hourly-level data.
    csv_daily_path (str): File path to save the daily-level CSV file.
    csv_hourly_path (str): File path to save the hourly-level CSV file.
    parquet_path (str): File path to save the daily-level Parquet file.
    
    Returns:
    None
    """
    # Save daily-level DataFrame to CSV
    df_daily.to_csv(csv_daily_path, index=True)
    
    # Save hourly-level DataFrame to CSV
    df_hourly.to_csv(csv_hourly_path, index=True)
    
    # Convert DataFrame to Apache Arrow Table
    table = pa.Table.from_pandas(df_daily, preserve_index=True)
    
    # Save DataFrame as Parquet file
    pq.write_table(table, parquet_path)

# Define file paths
csv_daily_file_path = r'C:\Users\garov\OneDrive\Documents\GitHub\bavarian-forest-visitor-monitoring-dssgx-24\outputs\Cleaned Data\df_visitcenters_daily.csv'
csv_hourly_file_path = r'C:\Users\garov\OneDrive\Documents\GitHub\bavarian-forest-visitor-monitoring-dssgx-24\outputs\Cleaned Data\df_visitcenters_hourly.csv'
parquet_file_path = r'C:\Users\garov\OneDrive\Documents\GitHub\bavarian-forest-visitor-monitoring-dssgx-24\outputs\Cleaned Data\df_visitcenters_daily.parquet'

# Apply the functions to process and save datasets
df_visitcenters_cleaned = prepare_data(df_visitcenters)
df_visitcenters_hourly_cleaned = prepare_data(df_visitcenters_hourly)

save_datasets(df_visitcenters_cleaned, df_visitcenters_hourly_cleaned, csv_daily_file_path, csv_hourly_file_path, parquet_file_path)

# Documentation:
# - `prepare_data` renames the 'Datum' column to 'time', converts it to datetime format, and sets it as the index.
# - `save_datasets` saves the cleaned daily and hourly DataFrames to CSV and Parquet files, preserving the index in the files.