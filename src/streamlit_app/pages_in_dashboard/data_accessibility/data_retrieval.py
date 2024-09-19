import streamlit as st
import pandas as pd
import awswrangler as wr
import re

bucket = "dssgx-munich-2024-bavarian-forest"

query_types = {'type1': ['What is the property value for the sensor sensor from start_date to end_date?' , ['property','sensor','start_date','end_date']],
               'type2': ['What is the property value for the sensor sensor for the month of month (year)?', ['property','sensor','month','year']],
               'type3': ['What is the property value for the sensor sensor for the season of season (year)?', ['property','sensor','season','year']],
               'type4': ['What is the property value from start_date to end_date?', ['property','start_date','end_date']],
               'type5': ['What is the property value for the month of month for the year year?', ['property','month','year']],
               'type6': ['What is the property value for the season of season for the year year?',['property','season','year']]
                }

def get_files_from_aws(selected_category):

    # Specify the S3 bucket and folder path
    prefix = f"/preprocessed_data/bf_preprocessed_files/{selected_category}/"  # Make sure to include trailing slash
    # List all objects in the specified S3 folder
    objects = wr.s3.list_objects(f"s3://{bucket}{prefix}")
    return objects

def convert_number_to_month_name(month):
    month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                   5: 'May', 6: 'June', 7: 'July', 8: 'August', 
                   9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    return month_dict[month]

def convert_number_to_season_name(season):
    season_dict = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    return season_dict[season]

def extract_values_according_to_type(selected_query,type):
    """
    Extract the values from the query according to the type.
    
    Args:
    selected_query : str : The selected query.
    type : str : The type of the query.

    Returns:
    dict : The extracted values from the selected query like month, season, year, property, sensor, start_date, end_date.

    """

    if type == 'type1':
        property = re.search(r'What is the (.+?) value', selected_query).group(1)
        sensor = re.search(r'for the sensor (.+?) from', selected_query).group(1)
        start_date = re.search(r'from (.+?) to', selected_query).group(1)
        end_date = re.search(r'to (.+?)\?', selected_query).group(1)
        extracted_values = [property, sensor, start_date, end_date]
    elif type == 'type2':
        property = re.search(r'What is the (.+?) value', selected_query).group(1)
        sensor = re.search(r'for the sensor (.+?) for the month of', selected_query).group(1)
        month = re.search(r'for the month of (.+?) \(', selected_query).group(1)
        year = re.search(r'\((.+?)\)\?', selected_query).group(1)
        extracted_values = [property, sensor, month, year]
        
    elif type == 'type3':
        property = re.search(r'What is the (.+?) value', selected_query).group(1)
        sensor = re.search(r'for the sensor (.+?) for the season of', selected_query).group(1)
        season = re.search(r'for the season of (.+?) \(', selected_query).group(1)
        year = re.search(r'\((.+?)\)\?', selected_query).group(1)
        extracted_values = [property, sensor, season, year]

    elif type == 'type4':
        property = re.search(r'What is the (.+?) value', selected_query).group(1)
        start_date = re.search(r'from (.+?) to', selected_query).group(1)
        end_date = re.search(r'to (.+?)\?', selected_query).group(1)
        extracted_values = [property, start_date, end_date]

    elif type == 'type5':
        property = re.search(r'What is the (.+?) value', selected_query).group(1)
        month = re.search(r'for the month of (.+?) for the year', selected_query).group(1)
        year = re.search(r'for the year (.+?)\?', selected_query).group(1)
        extracted_values = [property, month, year]

    elif type == 'type6':
        property = re.search(r'What is the (.+?) value', selected_query).group(1)
        season = re.search(r'for the season of (.+?) for the year', selected_query).group(1)
        year = re.search(r'for the year (.+?)\?', selected_query).group(1)
        extracted_values = [property, season, year]


    # Get the structure from query_types for 'type1'
    type_struc = query_types[type][1] 

    # Map the extracted values to the keys in the structure
    result = {key: value for key, value in zip(type_struc, extracted_values)}

    return result

def get_queried_df(processed_category_df, get_values,type):
    # get the property value from the get values dictionary
    property_value = get_values['property']
    #get the sensor name from the get_values dictionary
    if sensor in get_values['sensor']:
        sensor = get_values['sensor']

    if type == 'type1':
        start_date = pd.to_datetime(get_values['start_date'])
        end_date = pd.to_datetime(get_values['end_date'])
        queried_df = processed_category_df[
            (processed_category_df.index.date >= start_date.date()) &
            (processed_category_df.index.date <= end_date.date())
        ]
        queried_df = queried_df[[f'{sensor} {property_value}']]
        return queried_df  
      
    if type == 'type2':
        month = get_values['month']
        year = int(get_values['year'])
        queried_df = processed_category_df[
            (processed_category_df['month'] == month) &
            (processed_category_df['year'] == year)
        ]
        queried_df = queried_df[[f'{sensor} {property_value}']]
        return queried_df
            
    if type == 'type3':
        season = get_values['season']
        year = int(get_values['year'])
        queried_df = processed_category_df[
            (processed_category_df['season'] == season) &
            (processed_category_df['year'] == year)
        ]
        queried_df = queried_df[[f'{sensor} {property_value}']]
        return queried_df
    
    if type == 'type4':
        start_date = pd.to_datetime(get_values['start_date'])
        end_date = pd.to_datetime(get_values['end_date'])
        queried_df = processed_category_df[
            (processed_category_df.index.date >= start_date.date()) &
            (processed_category_df.index.date <= end_date.date())
        ]
        queried_df = queried_df[[property_value]]
        return queried_df
    
    if type == 'type5':
        month = get_values['month']
        year = int(get_values['year'])
        queried_df = processed_category_df[
            (processed_category_df['month'] == month) &
            (processed_category_df['year'] == year)
        ]
        queried_df = queried_df[[property_value]]
        return queried_df

    if type == 'type6':
        season = get_values['season']
        year = int(get_values['year'])
        queried_df = processed_category_df[
            (processed_category_df['season'] == season) &
            (processed_category_df['year'] == year)
        ]
        queried_df = queried_df[[property_value]]
        return queried_df

def create_temporal_columns_for_querying(parking_df):

    parking_df.index = pd.to_datetime(parking_df.index)

    # make a new column called 'month' from the index
    parking_df['month'] = parking_df.index.month

    # convert the numbers in the months column to the month names from the
    parking_df['month'] = parking_df['month'].apply(convert_number_to_month_name)

    # make a new column called 'year' from the index
    parking_df['year'] = parking_df.index.year

    # make a new column called 'season' from the index
    parking_df['season'] = (parking_df.index.month%12 + 3)//3
    # convert the numbers in the season column to the season names

    parking_df['season'] = parking_df['season'].apply(convert_number_to_season_name)


    # # print random 5 rows of the dataframe
    # print(parking_df.head(5))

    return parking_df

def get_sensors_data(objects):
    # if there are multiple objects get the last mostfied one
    object_to_be_queried = objects[-1]
    # Read the parquet file from S3
    df = wr.s3.read_parquet(f"{object_to_be_queried}")
    return df

def get_weather_data(objects):
    # if there are multiple objects get the last mostfied one
    object_to_be_queried = objects[-1]
    # Read the parquet file from S3
    df = wr.s3.read_parquet(f"{object_to_be_queried}")
    return df

def get_parking_data_for_selected_sensor(objects, selected_sensor):
    object_to_be_queried = None
    for obj in objects:
        # check if the selected sensor string is in the chosen object
        if selected_sensor in obj:
            object_to_be_queried = obj

    # Read the parquet file from S3
    df = wr.s3.read_parquet(f"{object_to_be_queried}")
    return df

def get_data_from_query(selected_category,selected_query,selected_query_type):
    """
    Get the data from the query.
    """
    if selected_query_type == 'type1' or selected_query_type == 'type2' or selected_query_type == 'type3':
        selected_sensor = re.search(r'for the sensor (.+?) ', selected_query).group(1)
        selected_property = re.search(r'What is the (.+?) ', selected_query).group(1)
        selected_variable = f"{selected_sensor} {selected_property}"
        objects = get_files_from_aws(selected_category)
        category_df = get_sensors_data(objects)

    else:
        selected_variable = 'None'
    print(selected_variable)
    get_values = extract_values_according_to_type(selected_query,selected_query_type)
    if selected_category == 'parking':
       objects = get_files_from_aws(selected_category)
       category_df = get_parking_data_for_selected_sensor(objects, selected_sensor)

    if selected_category == 'weather':
        objects = get_files_from_aws(selected_category)
        category_df = get_weather_data(objects)

    processed_category_df = create_temporal_columns_for_querying(category_df)
    queried_df = get_queried_df(processed_category_df, get_values,selected_query_type)

    return queried_df


