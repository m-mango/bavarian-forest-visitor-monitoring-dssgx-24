
# import the required libraries
import streamlit as st
import pandas as pd
import awswrangler as wr
import re
from src.config import aws_s3_bucket

# Types of queries that the functions will use to know what data to retrieve

query_types = {
    'type1': ['What is the property value for the sensor sensor from start_date to end_date?' ,
             ['property','sensor','start_date','end_date']
    ],
    'type2': [
        'What is the property value for the sensor sensor for the month of month for the year year?',
        ['property', 'sensor', 'month', 'year']
    ],
    'type3': [
        'What is the property value for the sensor sensor for the season of season for the year year?',
        ['property', 'sensor', 'season', 'year']
    ],
    'type4': [
        'What is the property value from start_date to end_date?',
        ['property', 'start_date', 'end_date']
    ],
    'type5': [
        'What is the property value for the month of month for the year year?',
        ['property', 'month', 'year']
    ],
    'type6': [
        'What is the property value for the season of season for the year year?',
        ['property', 'season', 'year']
    ]
}


def get_files_from_aws(selected_category):

    # Specify the S3 bucket and folder path
    prefix = f"/preprocessed_data/bf_preprocessed_files/{selected_category}/"  # Make sure to include trailing slash
    # List all objects in the specified S3 folder
    objects = wr.s3.list_objects(f"s3://{aws_s3_bucket}{prefix}")
    return objects

def convert_number_to_month_name(month):

    """
    Convert a month number (1-12) to its corresponding month name.

    Parameters:
        month (int): The month number.

    Returns:
        str: The name of the month.
    """

    month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                   5: 'May', 6: 'June', 7: 'July', 8: 'August', 
                   9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    
    return month_dict[month]

def convert_number_to_season_name(season):
    season_dict = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    return season_dict[season]

def extract_values_according_to_type(selected_query,type):
    """Extract values from a query string based on the specified query type.

    This function uses regular expressions to extract relevant values from the 
    `selected_query` string according to the specified `type`. The extracted values
    may include properties, sensors, dates, months, seasons, and years, depending on the type.

    Args:
        selected_query (str): The selected query string from which to extract values.
        type (str): The type of the query. Options include:
            - 'type1': Query for date range.
            - 'type2': Query for month and year.
            - 'type3': Query for season and year.
            - 'type4': Query for date range (weather category).
            - 'type5': Query for month and year (weather category).
            - 'type6': Query for season and year (weather category).

    Returns:
        dict: A dictionary containing the extracted values, where keys are based on
              the field names specified in `query_types`, including:
              - 'property'
              - 'sensor'
              - 'month'
              - 'season'
              - 'year'
              - 'start_date'
              - 'end_date'

    Raises:
        AttributeError: If the expected regex match is not found in the selected_query.
    """

    if selected_query == None:
        return None
    
    if type == 'type1':
        property = re.search(r'What is the (.+?) value', selected_query).group(1)
        sensor = re.search(r'for the sensor (.+?) from', selected_query).group(1)
        start_date = re.search(r'from (.+?) to', selected_query).group(1)
        end_date = re.search(r'to (.+?)\?', selected_query).group(1)
        extracted_values = [property, sensor, start_date, end_date]
    elif type == 'type2':
        property = re.search(r'What is the (.+?) value', selected_query).group(1)
        sensor = re.search(r'for the sensor (.+?) for the month of', selected_query).group(1)
        month = re.search(r'for the month of (.+?) ', selected_query).group(1)
        year = re.search(r'for the year (.+?)\?', selected_query).group(1)
        extracted_values = [property, sensor]
        
    elif type == 'type3':
        property = re.search(r'What is the (.+?) value', selected_query).group(1)
        sensor = re.search(r'for the sensor (.+?) for the season of', selected_query).group(1)
        season = re.search(r'for the season of (.+?) for', selected_query).group(1)
        year = re.search(r'for the year (.+?)\?', selected_query).group(1)
        extracted_values = [property, sensor]

    elif type == 'type4':
        property = re.search(r'What is the (.+?) value', selected_query).group(1)
        start_date = re.search(r'from (.+?) to', selected_query).group(1)
        end_date = re.search(r'to (.+?)\?', selected_query).group(1)
        extracted_values = [property, start_date, end_date]

    elif type == 'type5':
        property = re.search(r'What is the (.+?) value', selected_query).group(1)
        month = re.search(r'for the month of (.+?) for the year', selected_query).group(1)
        year = re.search(r'for the year (.+?)\?', selected_query).group(1)
        extracted_values = [property]

    elif type == 'type6':
        property = re.search(r'What is the (.+?) value', selected_query).group(1)
        season = re.search(r'for the season of (.+?) for the year', selected_query).group(1)
        year = re.search(r'for the year (.+?)\?', selected_query).group(1)
        extracted_values = [property]


    # Get the structure from query_types for 'type1'
    type_struc = query_types[type][1] 

    # Map the extracted values to the keys in the structure
    result = {key: value for key, value in zip(type_struc, extracted_values)}

    return result


def get_queried_df(processed_category_df, get_values, type, selected_category, start_date, end_date):
   
    """Retrieve a filtered DataFrame based on the selected category and query type.

    This function filters the input DataFrame `processed_category_df` according to the
    specified `selected_category` and `type`. It uses values provided in the `get_values`
    dictionary to perform the filtering.

    Args:
        processed_category_df (pd.DataFrame): The DataFrame containing processed data.
        get_values (dict): A dictionary containing values for filtering, including:
            - 'property' (str): The property to select from the DataFrame.
            - 'start_date' (str): Start date for filtering (format: 'YYYY-MM-DD').
            - 'end_date' (str): End date for filtering (format: 'YYYY-MM-DD').
            - 'month' (int): Month for filtering.
            - 'year' (int): Year for filtering.
            - 'season' (str): Season for filtering (e.g., 'spring', 'summer').
        type (str): The type of query to perform. Options include:
            - 'type1': Filter by date range.
            - 'type2': Filter by month and year.
            - 'type3': Filter by season and year.
            - 'type4': Filter by date range (weather category).
            - 'type5': Filter by month and year (weather category).
            - 'type6': Filter by season and year (weather category).
        selected_category (str): The category to filter by. Options include:
            - 'parking'
            - 'weather'
            - 'visitor_centers'
            - 'visitor_sensors'

    Returns:
        pd.DataFrame: A DataFrame containing the filtered data for the specified property.

    Raises:
        KeyError: If 'property' is not in `get_values`.
        ValueError: If an invalid type or selected_category is provided.
    """

    if get_values is None:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        queried_df = processed_category_df[
            (processed_category_df.index.date >= start_date.date()) &
            (processed_category_df.index.date <= end_date.date())
        ]
        return queried_df

    # get the property value from the get values dictionary
    if 'property' in get_values:
        property_value = get_values['property']
    
    # Implement filtering logic based on selected_category and type

    if selected_category == 'parking':
        
        if type == 'type1':
            start_date = pd.to_datetime(get_values['start_date'])
            end_date = pd.to_datetime(get_values['end_date'])
            queried_df = processed_category_df[
                (processed_category_df.index.date >= start_date.date()) &
                (processed_category_df.index.date <= end_date.date())
            ]
            queried_df = queried_df[[property_value]]
            return queried_df  
        
        if type == 'type2':
            month = get_values['month']
            year = int(get_values['year'])
            queried_df = processed_category_df[
                (processed_category_df['month'] == month) &
                (processed_category_df['year'] == year)
            ]
            queried_df = queried_df[[property_value]]
            return queried_df
                
        if type == 'type3':
            season = get_values['season']
            year = int(get_values['year'])
            queried_df = processed_category_df[
                (processed_category_df['season'] == season) &
                (processed_category_df['year'] == year)
            ]
            queried_df = queried_df[[property_value]]
            return queried_df
        
    if selected_category == 'weather':
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

    if selected_category == 'visitor_centers' or selected_category == 'visitor_sensors':
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
        
def create_temporal_columns(df):

    """Create temporal columns from the DataFrame index.

    This function takes a DataFrame with a datetime index and creates additional
    columns for month names, year, and season based on the index.

    Args:
        df (pd.DataFrame): The input DataFrame with a datetime index.

    Returns:
        pd.DataFrame: The original DataFrame with added columns:
            - 'month': The name of the month corresponding to the index.
            - 'year': The year extracted from the index.
            - 'season': The name of the season corresponding to the index.

    Raises:
        ValueError: If the index of the DataFrame cannot be converted to datetime.
    """

    df.index = pd.to_datetime(df.index)

    # make a new column called 'month' from the index
    df['month'] = df.index.month

    # convert the numbers in the months column to the month names from the
    df['month'] = df['month'].apply(convert_number_to_month_name)

    # make a new column called 'year' from the index
    df['year'] = df.index.year

    # make a new column called 'season' from the index
    df['season'] = (df.index.month%12 + 3)//3
    # convert the numbers in the season column to the season names

    df['season'] = df['season'].apply(convert_number_to_season_name)

    return df

def get_sensors_data():
    """Fetches sensor data from the most recently modified object.

    This function retrieves the sensor data from a specified object
    in S3 by reading a CSV file. It selects the last object from
    the provided list of objects, assuming this is the most recently
    modified.

    Args:
        objects (list): A list of S3 object paths, where the last
            object is the most recently modified.

    Returns:
        pandas.DataFrame: A DataFrame containing the sensor data read
        from the CSV file.
    """

    df = wr.s3.read_parquet(f"s3://{aws_s3_bucket}/preprocessed_data/preprocessed_visitor_count_sensors_data.parquet")
    return df
def get_visitor_centers_data(objects):
    """Fetches visitor centers data from the most recently modified Excel file.

    This function retrieves visitor centers data from a specified Excel file
    in S3. It selects the last object from the provided list of objects
    that is an Excel file (with extensions '.xlsx' or '.xls'), assuming this
    is the most recently modified Excel file.

    Args:
        objects (list): A list of S3 object paths, where the last
            object ending in '.xlsx' or '.xls' is the most recently modified Excel file.

    Returns:
        pandas.DataFrame: A DataFrame containing the visitor centers
        data read from the Excel file.
    """
    # Filter the list to include only objects that are Excel files
    excel_objects = [obj for obj in objects if obj.endswith(('.xlsx', '.xls'))]
    
    if not excel_objects:
        raise ValueError("No visitor center data found!")
    
    # Select the most recently modified Excel file (i.e., the last one in the list)
    object_to_be_queried = excel_objects[-1]
    
    # Read the Excel file from S3, skipping the last row which is a NaN row
    df = wr.s3.read_excel(f"{object_to_be_queried}", skipfooter=1, engine="openpyxl")

    return df

def get_weather_data(objects):

    """Fetches weather data from the most recently modified object.

    This function retrieves weather data from a specified object
    in S3 by reading an Parquet file. It selects the last object from
    the provided list of objects, assuming this is the most recently
    modified.

    Args:
        objects (list): A list of S3 object paths, where the last
            object is the most recently modified.

    Returns:
        pandas.DataFrame: A DataFrame containing the weather
        data read from the Parquet file.
    """

    # if there are multiple objects get the last mostfied one
    object_to_be_queried = objects[-1]
    # Read the parquet file from S3
    df = wr.s3.read_parquet(f"{object_to_be_queried}")
    return df

def get_parking_data_for_selected_sensor(selected_sensor):

    """Fetches parking data for a specified sensor from S3.

    This function searches through a list of S3 object paths to find
    the most relevant object that contains the specified sensor name.
    It then retrieves the parking data from the corresponding Parquet file.

    Args:
        objects (list): A list of S3 object paths to search for the
            selected sensor.
        selected_sensor (str): The name of the sensor to filter the
            objects.

    Returns:
        pandas.DataFrame: A DataFrame containing the parking data read
        from the Parquet file.

    Raises:
        ValueError: If the selected sensor is not found in any object.
    """
    path = f"s3://{aws_s3_bucket}/preprocessed_data/preprocessed_parking_data/merged_parking_data/{selected_sensor}.csv"
    df = wr.s3.read_csv(path)
    df.set_index("time", inplace=True)
    return df


def parse_german_dates_regex(
    df: pd.DataFrame,
    date_column_name: str
) -> pd.DataFrame:
    """
    Parses German dates in the specified date column of the DataFrame using regex,
    including hours and minutes if available.

    Args:
        df (pd.DataFrame): The DataFrame containing the date column.
        date_column_name (str): The name of the date column.

    Returns:
        pd.DataFrame: The DataFrame with parsed German dates.
    """
    
    # Define a mapping of German month names to their numeric values
    month_map = {
        "Jan.": "01",
        "Feb.": "02",
        "März": "03",
        "Apr.": "04",
        "Mai": "05",
        "Juni": "06",
        "Juli": "07",
        "Aug.": "08",
        "Sep.": "09",
        "Okt.": "10",
        "Nov.": "11",
        "Dez.": "12"
    }

    # Create a regex pattern for replacing months and capturing time
    pattern = re.compile(r'(\d{1,2})\.\s*(' + '|'.join(month_map.keys()) + r')\s*(\d{4})\s*(\d{2}):(\d{2})')

    # Function to replace the month in the matched string and keep the time part
    def replace_month(match):
        day = match.group(1)
        month = month_map[match.group(2)]
        year = match.group(3)
        hour = match.group(4)
        minute = match.group(5)
        return f"{year}-{month}-{day} {hour}:{minute}:00"

    # Apply regex replacement and convert to datetime
    df[date_column_name] = df[date_column_name].apply(lambda x: replace_month(pattern.search(x)) if pattern.search(x) else x)
    df[date_column_name] = pd.to_datetime(df[date_column_name], errors='coerce')

    return df

@st.cache_data(max_entries=1)
def get_data_from_query(selected_category,selected_query,selected_query_type, start_date, end_date, selected_sensors):

    """Retrieve data based on the selected category and query.

    This function extracts values from the provided query, retrieves data from
    AWS based on the selected category, processes the data, and returns a DataFrame
    containing the queried information.

    Args:
        selected_category (str): The category of data to retrieve. Options include:
            - 'visitor_sensors'
            - 'parking'
            - 'weather'
            - 'visitor_centers'
        selected_query (str): The query string used to extract specific values.
        selected_query_type (str): The type of the query, which determines the 
            format of the expected values.

    Returns:
        pd.DataFrame: A DataFrame containing the filtered data based on the query.

    Raises:
        ValueError: If the selected category is not recognized.
        KeyError: If the expected values are not found in the query.
    """

    if selected_category == 'visitor_sensors':
        sensor_df = get_sensors_data()
        sensor_df = sensor_df.set_index('Time') 
        processed_category_df = create_temporal_columns(sensor_df)
        
    if selected_category == 'parking':
        category_df = get_parking_data_for_selected_sensor(selected_sensors)
        processed_category_df = create_temporal_columns(category_df)

    if selected_category == 'weather':
        objects = get_files_from_aws(selected_category)
        category_df = get_weather_data(objects)
        processed_category_df = create_temporal_columns(category_df)

    if selected_category == 'visitor_centers':
        objects = get_files_from_aws(selected_category)
        category_df = get_visitor_centers_data(objects)
        category_df = category_df.set_index('Datum')
        processed_category_df = create_temporal_columns(category_df)

    get_values = extract_values_according_to_type(selected_query,selected_query_type)

    processed_category_df = get_queried_df(processed_category_df, get_values,selected_query_type, selected_category, start_date, end_date)

    return processed_category_df


