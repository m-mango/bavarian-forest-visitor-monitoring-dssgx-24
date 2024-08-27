#import libraries

import pandas as pd
import locale
import glob
import chardet
import numpy as np

"""



LOAD PREPROCESSED DATA FROM AWS


"""

df = visitor_counts_parsed_dates.reset_index(drop=True)

#lists and dictionaries for columns that need to be dropped or renamed

to_drop = ['Brechhäuslau Fußgänger IN', 'Brechhäuslau Fußgänger OUT', 'Waldhausreibe Channel 1 IN', 'Waldhausreibe Channel 2 OUT']

to_create = ['Bucina_Multi IN']


to_rename = {'Bucina IN': 'Bucina PYRO IN',
          'Bucina OUT': 'Bucina PYRO OUT',
          'Gsenget IN.1': 'Gsenget Fußgänger IN',
          'Gsenget OUT.1': 'Gsenget Fußgänger OUT',
          'Gfäll Fußgänger IN' : 'Gfäll IN',
          'Gfäll Fußgänger OUT': 'Gfäll OUT',
          'Fredenbrücke Fußgänger IN' : 'Fredenbrücke IN',
          'Fredenbrücke Fußgänger OUT': 'Fredenbrücke OUT',
          'Diensthüttenstraße Fußgänger IN': 'Diensthüttenstraße IN' ,
          'Diensthüttenstraße Fußgänger OUT': 'Diensthüttenstraße OUT',
          'Racheldiensthütte Cyclist OUT' : 'Racheldiensthütte Fahrräder OUT',
          'Racheldiensthütte Pedestrian IN' : 'Racheldiensthütte Fußgänger IN',
          'Racheldiensthütte Pedestrian OUT' : 'Racheldiensthütte Fußgänger OUT',
          'Sagwassersäge Fußgänger IN' : 'Sagwassersäge IN',
          'Sagwassersäge Fußgänger OUT': 'Sagwassersäge OUT',
          'Schwarzbachbrücke Fußgänger IN' : 'Schwarzbachbrücke IN',
          'Schwarzbachbrücke Fußgänger OUT' : 'Schwarzbachbrücke OUT',
          'NPZ_Falkenstein IN' : 'Falkenstein 1 PYRO IN',
          'NPZ_Falkenstein OUT' : 'Falkenstein 1 PYRO OUT',
          'TFG_Falkenstein_1 Fußgänger zum Parkplatz' : 'Falkenstein 1 OUT',
          'TFG_Falkenstein_1 Fußgänger zum HZW' : 'Falkenstein 1 IN',
          'TFG_Falkenstein_2 Fußgänger In Richtung Parkplatz' : 'Falkenstein 2 OUT',
          'TFG_Falkenstein_2 Fußgänger In Richtung TFG' : 'Falkenstein 2 IN',
          'TFG_Lusen IN' : 'Lusen 1 PYRO IN',
          'TFG_Lusen OUT' : 'Lusen 1 PYRO OUT',
          'TFG_Lusen_1 Fußgänger Richtung TFG': 'Lusen 1 EVO IN',
          'TFG_Lusen_1 Fußgänger Richtung Parkplatz' : 'Lusen 1 EVO OUT',
          'TFG_Lusen_2 Fußgänger Richtung Vögel am Waldrand': 'Lusen 2 IN',
          'TFG_Lusen_2 Fußgänger Richtung Parkplatz' : 'Lusen 2 OUT',
          'TFG_Lusen_3 TFG Lusen 3 IN': 'Lusen 3 IN',
          'TFG_Lusen_3 TFG Lusen 3 OUT': 'Lusen 3 OUT',
          'Waldspielgelände_1 IN': 'Waldspielgelände IN',
          'Waldspielgelände_1 OUT': 'Waldspielgelände OUT',
          'Wistlberg Fußgänger IN' : 'Wistlberg IN',
          'Wistlberg Fußgänger OUT' : 'Wistlberg OUT',
          'Trinkwassertalsperre IN' : 'Trinkwassertalsperre PYRO IN', 
          'Trinkwassertalsperre OUT' : 'Trinkwassertalsperre PYRO OUT'
          }

def process_dataframe(df, rename, drop, create):
    """
    Processes the given DataFrame by renaming columns, dropping specified columns, and creating a new column.

    Args:
        df (pd.DataFrame): The DataFrame to be modified.
        rename (dict): A dictionary where the keys are existing column names and the values are the new column names.
        drop (list): A list of column names that should be removed from the DataFrame.
        create (str): The name of the new column that will be created by summing the "Bucina_Multi Fahrräder IN" 
                      and "Bucina_Multi Fußgänger IN" columns.

    Returns:
        pd.DataFrame: The modified DataFrame with the specified changes applied.
    """
    # Rename columns according to the provided mapping
    df.rename(columns=rename, inplace=True)
    print(len(rename), ' columns were renamed')

    # Remove the specified columns from the DataFrame
    df.drop(columns=drop, inplace=True)
    print(len(drop), ' repeated columns were dropped')

    # Add a new column by summing two existing columns
    df[create] = df["Bucina_Multi Fahrräder IN"] + df["Bucina_Multi Fußgänger IN"]
    print(len(create), ' column was created')

    return df

df = process_dataframe(df, rename=to_rename, drop=to_drop, create=to_create)



# Fix problems with duplicated values in time column

def correct_and_impute_times(df):
    """
    Identifies rows with missing values in all columns except 'Time', corrects the 'Time' by subtracting one hour, 
    and imputes missing values by copying from the preceding row.

    Args:
        df (pd.DataFrame): The DataFrame to be corrected and imputed.

    Returns:
        pd.DataFrame: The corrected DataFrame with missing values imputed and time index sorted.
    """
    # Identify rows where all columns except 'Time' have missing values
    index_wrong_time = df[df.loc[:, df.columns != "Time"].isna().all(axis=1)].index

    # Subtract one hour from the 'Time' for the identified rows
    df.loc[index_wrong_time, 'Time'] = df.loc[index_wrong_time, 'Time'] - pd.Timedelta(hours=1)

    # Impute missing values by copying from the preceding row for each identified index
    for idx in index_wrong_time:
        if idx > 0:  # Ensure that there is a preceding row
            # Copy values from the preceding row to the current row
            df.loc[idx, df.columns != 'Time'] = df.loc[idx - 1, df.columns != 'Time']

    # Set 'Time' as the index and sort the DataFrame by this index
    df = df.set_index('Time').sort_index()

    print("Repeated values in Time column were identified and solved. Time is now set as index. ")

    return df


df = correct_and_impute_times(df)



# Fix problem of existing values in timestamps when a sensor was not installed

def correct_non_replaced_sensors(df):
    """
    Replaces data with NaN for non-replaced sensors in the DataFrame based on specified timestamps. A dictionary is provided where keys are timestamps as strings and values are lists of column names that should be set to NaN if the index is earlier than the timestamp.

    Args:
        df (pd.DataFrame): The DataFrame to be corrected.

    Returns:
        pd.DataFrame: The DataFrame with corrected sensor data.
    """

    dict_non_replaced = {'2020-07-30 00:00:00' : ['Lusen 1 PYRO IN', 'Lusen 1 PYRO OUT'],
                     '2022-12-20 00:00:00' : ['Lusen 3 IN', 'Lusen 3 OUT'],
                     '2022-10-12 00:00:00' : ['Gsenget IN', 'Gsenget OUT']}


    # Iterate over the dictionary of non-replaced sensors
    for key, columns in dict_non_replaced.items():
        # Convert the timestamp key from string to datetime object
        timestamp = pd.to_datetime(key)
        
        # Set values to NaN for specified columns where the index is earlier than the given timestamp
        df.loc[df.index < timestamp, columns] = np.nan

    print("Out of place values were turn to NaN for Lusen 1 PYRO, Lusen 3 and Gsenget")    

    return df


df = correct_non_replaced_sensors(df)


# Fix overlapping values in replaced sensors

def correct_sensor_data(df):
    """
    Corrects sensor overlapping data by setting specific values to NaN based on replacement dates.

    Args:
        df (pd.DataFrame): The DataFrame containing sensor data to be corrected.

    Returns:
        pd.DataFrame: The DataFrame with corrected sensor data.
    """
    # Define the replacement dates and columns for different sensor types
    replacement_dates = {
        'trinkwassertalsperre': '2021-06-18 00:00:00',
        'bucina': '2021-05-28 00:00:00',
        'falkenstein 1': '2022-12-22 12:00:00'
    }

    multi_columns_dict = {
        'trinkwassertalsperre': [
            'Trinkwassertalsperre_MULTI Fußgänger IN',
            'Trinkwassertalsperre_MULTI Fußgänger OUT',
            'Trinkwassertalsperre_MULTI Fahrräder IN',
            'Trinkwassertalsperre_MULTI Fahrräder OUT',
            'Trinkwassertalsperre_MULTI IN',
            'Trinkwassertalsperre_MULTI OUT'
        ],
        'bucina': [
            'Bucina_Multi OUT',
            'Bucina_Multi Fußgänger IN',
            'Bucina_Multi Fahrräder IN',
            'Bucina_Multi Fahrräder OUT',
            'Bucina_Multi Fußgänger OUT',
            'Bucina_Multi IN'
        ],
        'falkenstein 1': [
            'Falkenstein 1 OUT',
            'Falkenstein 1 IN'
        ]
    }

    pyro_columns_dict = {
        'trinkwassertalsperre': [
            'Trinkwassertalsperre PYRO IN',
            'Trinkwassertalsperre PYRO OUT'
        ],
        'bucina': [
            'Bucina PYRO IN',
            'Bucina PYRO OUT'
        ],
        'falkenstein 1': [
            'Falkenstein 1 PYRO IN',
            'Falkenstein 1 PYRO OUT'
        ]
    }

    # Process each sensor type based on the predefined dictionaries
    for sensor_type in replacement_dates:
        replacement_date = pd.to_datetime(replacement_dates[sensor_type])
        multi_columns = multi_columns_dict.get(sensor_type, [])
        pyro_columns = pyro_columns_dict.get(sensor_type, [])

        # Set to NaN the values in 'multi_columns' for dates on or before the replacement date
        if multi_columns:
            df.loc[df.index <= replacement_date, multi_columns] = np.nan

        # Set to NaN the values in 'pyro_columns' for dates after the replacement date
        if pyro_columns:
            df.loc[df.index > replacement_date, pyro_columns] = np.nan


    print("Fix overlap")
    return df
