import awswrangler as wr
import pandas as pd
import numpy as np
import warnings
from sourcing_data.source_historic_visitor_count import source_historic_visitor_count 
from pre_processing.preprocess_historic_visitor_count_data import preprocess_visitor_count_data
from sourcing_data.source_visitor_center_data import source_visitor_center_data
from sourcing_data.source_weather import source_weather_data
from pre_processing.preprocess_weather_data import process_weather_data
from pre_processing.join_sensor_weather_visitorcenter import get_joined_dataframe
from pre_processing.features_zscoreweather_distanceholidays import get_zscores_and_nearest_holidays
from pre_processing.preprocess_visitor_center_data import process_visitor_center_data
from datetime import datetime

warnings.filterwarnings("ignore")

source_train_path = "s3://dssgx-munich-2024-bavarian-forest/preprocessed_data/joined_sensor_weather_visitorcenter_2016-2024.csv"

delta_calculations_path = "s3://dssgx-munich-2024-bavarian-forest/preprocessed_data/holidays_deltaweather_features_df.csv"

############################################################################################################
# Global Variables
############################################################################################################

# Set the start and end date for training
start_date = '2023-01-01'
end_date = '2024-07-22'

# Columns to use for preprocessing
columns_to_use = [
'Time',  'Bayerisch Eisenstein IN',  'Bayerisch Eisenstein OUT',  'Brechhäuslau IN',  'Brechhäuslau OUT',  
'Deffernik IN',  'Deffernik OUT',  'Diensthüttenstraße IN',  'Diensthüttenstraße OUT',  'Felswandergebiet IN',  
'Felswandergebiet OUT',  'Ferdinandsthal IN',  'Ferdinandsthal OUT',  'Fredenbrücke IN',  'Fredenbrücke OUT',  
'Gfäll IN',  'Gfäll OUT',  'Gsenget IN',  'Gsenget OUT',  'Klingenbrunner Wald IN',  'Klingenbrunner Wald OUT',  
'Klosterfilz IN',  'Klosterfilz OUT',  'Racheldiensthütte IN',  'Racheldiensthütte OUT',  'Sagwassersäge IN',  
'Sagwassersäge OUT',  'Scheuereck IN',  'Scheuereck OUT',  'Schillerstraße IN',  'Schillerstraße OUT',  
'Schwarzbachbrücke IN',  'Schwarzbachbrücke OUT',  'Falkenstein 2 OUT',  'Falkenstein 2 IN',  'Lusen 2 IN',  
'Lusen 2 OUT',  'Lusen 3 IN',  'Lusen 3 OUT',  'Waldhausreibe IN',  'Waldhausreibe OUT',  'Waldspielgelände IN',  
'Waldspielgelände OUT',  'Wistlberg IN',  'Wistlberg OUT',  'Bucina MERGED IN',  'Bucina MERGED OUT',  
'Falkenstein 1 MERGED IN',  'Falkenstein 1 MERGED OUT',  'Lusen 1 MERGED IN',  'Lusen 1 MERGED OUT',  
'Trinkwassertalsperre MERGED IN',  'Trinkwassertalsperre MERGED OUT',  
'traffic_abs',  'sum_IN_abs',  'sum_OUT_abs',  'Temperature (°C)',  'Relative Humidity (%)',  
'Precipitation (mm)',  'Wind Speed (km/h)',  'Sunshine Duration (min)',  'Tag',  'Monat',  
'Wochentag',  'Wochenende',  'Jahreszeit',  'Laubfärbung',  'Schulferien_Bayern',  'Schulferien_CZ',  
'Feiertag_Bayern',  'Feiertag_CZ',  'HEH_geoeffnet',  'HZW_geoeffnet',  'WGM_geoeffnet',  
'Lusenschutzhaus_geoeffnet',  'Racheldiensthuette_geoeffnet',  'Falkensteinschutzhaus_geoeffnet',  
'Schwellhaeusl_geoeffnet'
]


# Dictionary to map the columns to the location
regionwise_sensor_mapping = {
    'Falkenstein-Schwellhäusl': {
        'IN': [
            'Bayerisch Eisenstein IN', 'Brechhäuslau IN', 'Deffernik IN', 
            'Ferdinandsthal IN', 'Schillerstraße IN'
        ],
        'OUT': [
            'Bayerisch Eisenstein OUT', 'Brechhäuslau OUT', 'Deffernik OUT', 
            'Ferdinandsthal OUT', 'Schillerstraße OUT'
        ]
    },
    'Nationalparkzentrum Falkenstein': {
        'IN': ['Falkenstein 1 IN', 'Falkenstein 2 IN'],
        'OUT': ['Falkenstein 1 OUT', 'Falkenstein 2 OUT']
    },
    'Scheuereck-Schachten-Trinkwassertalsperre': {
        'IN': ['Gsenget IN', 'Scheuereck IN', 'Trinkwassertalsperre IN'],
        'OUT': ['Gsenget OUT', 'Scheuereck OUT', 'Trinkwassertalsperre OUT']
    },
    'Lusen-Mauth-Finsterau': {
        'IN': [
            'Bucina IN', 'Felswandergebiet IN', 'Fredenbrücke IN', 
            'Schwarzbachbrücke IN', 'Waldhausreibe IN', 'Wistlberg IN', 'Sagwassersäge IN'
        ],
        'OUT': [
            'Bucina OUT', 'Felswandergebiet OUT', 'Fredenbrücke OUT', 
            'Schwarzbachbrücke OUT', 'Waldhausreibe OUT', 'Wistlberg OUT', 'Sagwassersäge OUT'
        ]
    },
    'Rachel-Spiegelau': {
        'IN': [
            'Diensthüttenstraße IN', 'Gfäll IN', 'Klingenbrunner Wald IN', 
            'Klosterfilz IN', 'Racheldiensthütte IN', 'Waldspielgelände IN'
        ],
        'OUT': [
            'Diensthüttenstraße OUT', 'Gfäll OUT', 'Klingenbrunner Wald OUT', 
            'Klosterfilz OUT', 'Racheldiensthütte OUT', 'Waldspielgelände OUT'
        ]
    },
    'Nationalparkzentrum Lusen': {
        'IN': ['Lusen 1 IN', 'Lusen 2 IN', 'Lusen 3 IN'],
        'OUT': ['Lusen 1 OUT', 'Lusen 2 OUT', 'Lusen 3 OUT']
    }
}



dtype_dict = {
    'datetime64[ns]': [
        'Time'
    ],
    
    'float64': [
        'traffic_abs',
        'Temperature (°C)',
        'Relative Humidity (%)',
        'Wind Speed (km/h)',
        'Monat',
        'sum_IN_abs',
        'sum_OUT_abs',
        
        # traffic data
        'Falkenstein-Schwellhäusl IN',
        'Rachel-Spiegelau IN',
        'Nationalparkzentrum Falkenstein IN',
        'Nationalparkzentrum Lusen IN',
        'Lusen-Mauth-Finsterau IN',
        'Scheuereck-Schachten-Trinkwassertalsperre IN',
        'Falkenstein-Schwellhäusl OUT',
        'Rachel-Spiegelau OUT',
        'Nationalparkzentrum Falkenstein OUT',
        'Nationalparkzentrum Lusen OUT',
        'Lusen-Mauth-Finsterau OUT',
        'Scheuereck-Schachten-Trinkwassertalsperre OUT',
        'Bayerisch Eisenstein IN', 'Bayerisch Eisenstein OUT',
        'Brechhäuslau IN', 'Brechhäuslau OUT',
        'Deffernik IN', 'Deffernik OUT',
        'Diensthüttenstraße IN', 'Diensthüttenstraße OUT',
        'Felswandergebiet IN', 'Felswandergebiet OUT',
        'Ferdinandsthal IN', 'Ferdinandsthal OUT',
        'Fredenbrücke IN', 'Fredenbrücke OUT',
        'Gfäll IN', 'Gfäll OUT',
        'Gsenget IN', 'Gsenget OUT',
        'Klingenbrunner Wald IN', 'Klingenbrunner Wald OUT',
        'Klosterfilz IN', 'Klosterfilz OUT',
        'Racheldiensthütte IN', 'Racheldiensthütte OUT',
        'Sagwassersäge IN', 'Sagwassersäge OUT',
        'Scheuereck IN', 'Scheuereck OUT',
        'Schillerstraße IN', 'Schillerstraße OUT',
        'Schwarzbachbrücke IN', 'Schwarzbachbrücke OUT',
        'Falkenstein 1 IN', 'Falkenstein 1 OUT',
        'Falkenstein 2 IN', 'Falkenstein 2 OUT',
        'Lusen 1 IN', 'Lusen 1 OUT',
        'Lusen 2 IN', 'Lusen 2 OUT',
        'Lusen 3 IN', 'Lusen 3 OUT',
        'Waldhausreibe IN', 'Waldhausreibe OUT',
        'Waldspielgelände IN', 'Waldspielgelände OUT',
        'Wistlberg IN', 'Wistlberg OUT',
        'Bucina IN', 'Bucina OUT',
        'Trinkwassertalsperre IN', 'Trinkwassertalsperre OUT',
        
        # Z-Score data
        'ZScore_Daily_Max_Temperature (°C)',
        'ZScore_Daily_Max_Relative Humidity (%)',
        'ZScore_Daily_Max_Wind Speed (km/h)',
        
        # Distance to nearest holidays
        'Distance_to_Nearest_Holiday_Bayern',
        'Distance_to_Nearest_Holiday_CZ'
    ],
    
    'category': [
        'Wochentag',
        'Wochenende',
        'Jahreszeit',
        'Laubfärbung',
        'Feiertag_Bayern',
        'Feiertag_CZ',
        'HEH_geoeffnet',
        'HZW_geoeffnet',
        'WGM_geoeffnet',
        'Lusenschutzhaus_geoeffnet',
        'Racheldiensthuette_geoeffnet',
        'Falkensteinschutzhaus_geoeffnet',
        'Schwellhaeusl_geoeffnet',
        'Schulferien_Bayern',
        'Schulferien_CZ',
        'coco_2'
    ]
}

numeric_features_for_modelling = ['Temperature (°C)', 'Relative Humidity (%)', 'Wind Speed (km/h)', 'ZScore_Daily_Max_Temperature (°C)', 
                    'ZScore_Daily_Max_Relative Humidity (%)','ZScore_Daily_Max_Wind Speed (km/h)',
                    'Distance_to_Nearest_Holiday_Bayern','Distance_to_Nearest_Holiday_CZ','Tag_sin', 'Tag_cos', 'Monat_sin', 'Monat_cos',
                    'Hour_sin', 'Hour_cos','Wochentag_sin', 'Wochentag_cos']

categorical_features_for_modelling = ['Wochenende','Laubfärbung', 'Schulferien_Bayern', 'Schulferien_CZ', 
                        'Feiertag_Bayern', 'Feiertag_CZ', 'HEH_geoeffnet', 'HZW_geoeffnet', 'WGM_geoeffnet', 
                        'Lusenschutzhaus_geoeffnet', 'Racheldiensthuette_geoeffnet', 'Falkensteinschutzhaus_geoeffnet', 
                        'Schwellhaeusl_geoeffnet','sunny', 'cloudy', 'rainy', 'snowy', 'extreme','stormy','Frühling',
                        'Sommer', 'Herbst', 'Winter']

target_vars_et = ['traffic_abs', 'sum_IN_abs', 'sum_OUT_abs', 'Lusen-Mauth-Finsterau IN', 'Lusen-Mauth-Finsterau OUT', 
               'Nationalparkzentrum Lusen IN', 'Nationalparkzentrum Lusen OUT', 'Rachel-Spiegelau IN', 'Rachel-Spiegelau OUT', 
               'Falkenstein-Schwellhäusl IN', 'Falkenstein-Schwellhäusl OUT', 
               'Scheuereck-Schachten-Trinkwassertalsperre IN', 'Scheuereck-Schachten-Trinkwassertalsperre OUT', 
               'Nationalparkzentrum Falkenstein IN', 'Nationalparkzentrum Falkenstein OUT']

coco_mapping = {
    1: [1, 2],       # Clear, Fair
    2: [3, 4, 5],    # Cloudy, Overcast, Fog
    3: [7, 8, 9, 17, 18, 19],  # Light Rain, Rain, Heavy Rain, Rain Shower, Heavy Rain Shower, Sleet Shower
    4: [14, 15, 16, 21, 22],   # Light Snowfall, Snowfall, Heavy Snowfall, Snow Shower, Heavy Snow Shower
    5: [6, 10, 11, 12, 13, 20], # Freezing Fog, Freezing Rain, Heavy Freezing Rain, Sleet, Heavy Sleet, Heavy Sleet Shower
    6: [23, 24, 25, 26, 27]    # Lightning, Hail, Thunderstorm, Heavy Thunderstorm, Storm
}

###########################################################################################################################
# Functions
###########################################################################################################################


def get_regionwise_IN_and_OUT_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the data by summing IN and OUT columns for each region.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the data to preprocess.
        
    Returns:
        pd.DataFrame: The preprocessed DataFrame.
    """

    # Iterate over the regionwise sensor mapping
    for region, sensors in regionwise_sensor_mapping.items():
        # Sum the values for all IN columns of the current region
        if sensors['IN']:
            df[f'{region} IN'] = df[sensors['IN']].sum(axis=1, min_count=1)

        # Sum the values for all OUT columns of the current region
        if sensors['OUT']:
            df[f'{region} OUT'] = df[sensors['OUT']].sum(axis=1, min_count=1)

    return df



def load_csv_files_from_aws_s3(path: str, **kwargs) -> pd.DataFrame:
    """ 
    Loads individual or multiple CSV files from an AWS S3 bucket.
    Args:
        path (str): The path to the CSV files on AWS S3.
        **kwargs: Additional arguments to pass to the read_csv function.
    Returns:
        pd.DataFrame: The DataFrame containing the data from the CSV files.
    """
    df = wr.s3.read_csv(path=path, **kwargs)
    # set time to datetime
    return df

# Helper function to convert columns to datetime
def convert_to_datetime(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for column in columns:
        df[column] = pd.to_datetime(df[column])
    return df

# Merging new features from df_newfeatures into df
def merge_new_features(df: pd.DataFrame, df_newfeatures: pd.DataFrame) -> pd.DataFrame:
    """Merges new features from df_newfeatures into df on 'Time' column."""
    
    # Ensure 'Time' columns are datetime
    df, df_newfeatures = map(lambda x: convert_to_datetime(x, ['Time']), [df, df_newfeatures])

    # Columns to merge
    columns_to_add = [
        'ZScore_Daily_Max_Temperature (°C)',
        'ZScore_Daily_Max_Relative Humidity (%)',
        'ZScore_Daily_Max_Wind Speed (km/h)',
        'Distance_to_Nearest_Holiday_Bayern',
        'Distance_to_Nearest_Holiday_CZ'
    ]

    # Select only existing columns for merging
    selected_columns = [col for col in columns_to_add if col in df_newfeatures.columns]

    # Merge on 'Time' column
    df = df.merge(df_newfeatures[['Time'] + selected_columns], on='Time', how='left')

   #add the hour column additionally
    df['Hour'] = df['Time'].dt.hour

    return df

# Change datatypes based on dtype_dict
def change_datatypes(df: pd.DataFrame, dtype_dict: dict) -> pd.DataFrame:
    """Change column datatypes based on dtype_dict."""
    for dtype, columns in dtype_dict.items():
        df[columns] = df[columns].astype(dtype)

    # set time as the index
    df = df.set_index('Time')
    return df

def apply_cliclic_tranformations(df: pd.DataFrame,cyclic_features: list) -> pd.DataFrame:

    # Convert categorical features to numeric if they are not already
    for feature in cyclic_features:
        if feature in df.columns:
            if pd.api.types.is_categorical_dtype(df[feature]):
                df[feature] = df[feature].cat.codes  # Convert categorical to numeric codes
            
            max_value = df[feature].max()  # Get max value for scaling
            
            # Apply sine and cosine transformations
            df[f'{feature}_sin'] = np.sin(2 * np.pi * df[feature] / max_value)
            df[f'{feature}_cos'] = np.cos(2 * np.pi * df[feature] / max_value)
        else:
            print(f"Warning: Feature '{feature}' not found in DataFrame")
    # Drop the original columns
    columns_to_drop = ['Tag', 'Monat', 'Wochentag', 'Hour']
    df = df.drop(columns=columns_to_drop)

    return df

def standardize_numeric_features(df: pd.DataFrame, standardize_features: list) -> pd.DataFrame: 

    # Loop through each numeric feature and apply z-score normalization
    for feature in standardize_features:
        if feature in df.columns:
            mean_value = df[feature].mean()  # Calculate mean
            std_value = df[feature].std()    # Calculate standard deviation
            
            # Apply z-score normalization
            df[feature] = (df[feature] - mean_value) / std_value
        else:
            print(f"Warning: Feature '{feature}' not found in DataFrame")

    return df



       
def get_dummy_encodings(df: pd.DataFrame, columns_to_use: list) -> pd.DataFrame:
    # Create a copy of the original dataframe
    df_copy = df.copy()

    ################ Get dummy encodings for the coco_2 column ####################
    
    # Dummy encode the column *coco_2*
    dummies = pd.get_dummies(df[columns_to_use[1]], drop_first=False)

    # check if the dummy columns are created  and if not fill the column with False
    for col in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]:
        if col not in dummies.columns:
            dummies[col] = False

    # Rename the dummy columns to more meaningful names
    dummies = dummies.rename(columns={1.0: 'sunny',
                                      2.0: 'cloudy', 
                                      3.0: 'rainy', 
                                      4.0: 'snowy', 
                                      5.0: 'extreme', 
                                      6.0: 'stormy'})
    df_copy = pd.concat([df_copy, dummies], axis=1)

    # 

    ################### dummy encodings for the Jahreszeit column ####################
    # Dummy encode the columns *Jahreszeit*
    season_dummies = pd.get_dummies(df[columns_to_use[0]], drop_first=False)
    
    for col in ['Frühling', 'Sommer', 'Herbst', 'Winter']:
        if col not in season_dummies.columns:
            dummies[col] = False
    
    df_copy = pd.concat([df_copy, season_dummies], axis=1)

    # remove the original columns
    df_copy = df_copy.drop(columns=columns_to_use)
    
    # Return the dataframe with original and new dummy-encoded columns
    return df_copy

def handle_binary_values(df: pd.DataFrame) -> pd.DataFrame:

    # convert the columns with True and False to 1 and 0 and convert the int64 datatype to category
    df = df.replace({True: 1, False: 0})
    # convert the int64 datatype to category
    boolean_columns = df.select_dtypes(include=['int64']).columns
    # Convert these columns to categorical
    df[boolean_columns] = df[boolean_columns].astype('category')

    return df

def remove_merge_from_columns(df: pd.DataFrame) -> pd.DataFrame:

    # remove the MERGED from the column names and remove the extra gap
    if df.columns.str.contains('MERGED').any():
        df.columns = df.columns.str.replace('MERGED', '')
        df.columns = df.columns.str.replace('  ', ' ')
    
    return df

def process_transformations(df: pd.DataFrame) -> pd.DataFrame:
    """Process the transformations on the DataFrame."""

    df = apply_cliclic_tranformations(df, cyclic_features = ['Tag','Hour', 'Monat', 'Wochentag'])
    df = standardize_numeric_features(df, standardize_features = ['Temperature (°C)', 'Relative Humidity (%)', 'Wind Speed (km/h)',
                                                                  'Distance_to_Nearest_Holiday_Bayern','Distance_to_Nearest_Holiday_CZ'])
    df = get_dummy_encodings(df, columns_to_use = ['Jahreszeit', 'coco_2'])
    df = handle_binary_values(df)
    

    return df

def filter_features_for_modelling(df: pd.DataFrame) -> pd.DataFrame:
    """Filter the features for modelling."""
    # Filter the features for modelling
    df = df[numeric_features_for_modelling + categorical_features_for_modelling + target_vars_et]

    return df



def get_features():
        # get the historic visitor count data
    sourced_visitor_count_df = source_historic_visitor_count()
   
    processed_visitor_count_df = preprocess_visitor_count_data(sourced_visitor_count_df)

    # get the visitor centers data

    # source visitor center data
    sourced_vc_data_df = source_visitor_center_data()

    processed_vc_df_hourly,_ = process_visitor_center_data(sourced_vc_data_df)
    processed_vc_df_hourly['Hour'] = processed_vc_df_hourly['Time'].dt.hour
    # get the weather data
    weather_data = source_weather_data(start_time = datetime(2022, 1, 1), end_time = datetime(2024, 7, 22) )

    processed_weather_df = process_weather_data(weather_data)

    # join the dataframes
    joined_df = get_joined_dataframe(processed_weather_df, processed_visitor_count_df, processed_vc_df_hourly)

    #  z score normalization
    columns_for_zscores = [ 'Temperature (°C)','Relative Humidity (%)','Wind Speed (km/h)']
    with_zscores_and_nearest_holidays_df = get_zscores_and_nearest_holidays(joined_df, columns_for_zscores)

    #sourced_df = load_csv_files_from_aws_s3(path=source_train_path) 
    sourced_df = with_zscores_and_nearest_holidays_df

    sliced_df = sourced_df[(sourced_df['Time'] >= start_date) & (sourced_df['Time'] <= end_date)]
    removed_merged_df = remove_merge_from_columns(sliced_df)
    regionwise_df = get_regionwise_IN_and_OUT_columns(removed_merged_df)
    #df_delta_newfeatures = load_csv_files_from_aws_s3(path=delta_calculations_path)
    #merged_df = merge_new_features(regionwise_df, df_delta_newfeatures)
    changed_datatypes_df = change_datatypes(regionwise_df, dtype_dict)
    processed_features_df = process_transformations(changed_datatypes_df)
    filtered_features_df = filter_features_for_modelling(processed_features_df)

    # # save the filtered_df as csv
    # filtered_features_df.to_csv('processed_new_features.csv')

    return filtered_features_df



