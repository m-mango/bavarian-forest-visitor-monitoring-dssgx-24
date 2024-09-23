# Import libraries
import streamlit as st
import awswrangler as wr
import datetime
from src.streamlit_app.pages_in_dashboard.data_accessibility.data_retrieval import get_data_from_query
from src.streamlit_app.pages_in_dashboard.data_accessibility.query_viz_and_download import get_visualization_section


def select_category():
    """
    Select the category of data to access using st.selectbox from Streamlit.

    Returns: 
        category (str): The category selected by the user.
    """
    # select the dropdown for the category
    category = st.selectbox("Select data category", 
                            ["weather", "visitor_sensors", "parking", "visitor_centers"],
                            index=0)
    
    return category

def select_date():
    """
    Select the start and end date for data access using date inputs in Streamlit.

    Returns: 
        tuple: The selected start and end date in the format "MM-DD-YYYY".
    """
    
    # Define the default start and end dates
    default_start = datetime.datetime.now() - datetime.timedelta(days=7)
    default_end = datetime.datetime.now()

    # Create the date input widget with start date
    d = st.date_input(
        "Select the start date",
        default_start,
        format="MM.DD.YYYY",
    )
    # Create the date input widget with end date
    e = st.date_input(
        "Select the end date",
        default_end,
        format="MM.DD.YYYY",
    )
    # capture the selected date
    start_date = d.strftime("%m-%d-%Y")
    end_date = e.strftime("%m-%d-%Y")

    # prompt if the end date is chosen before start date
    if start_date > end_date:
        st.error("Error: End date must fall after start date.")
        st.stop()

    return start_date, end_date

def select_filters(category):

    """
    Select additional filters such as months, seasons, sensors, weather values, or parking values.

    Args:
        category (str): The category selected by the user. Can be one of:
                        "weather", "parking", "visitor_sensors", "visitor_centers".

    Returns:
        tuple: A tuple containing selected_months, selected_seasons, selected_properties,
               selected_sensors, and the selected year (if applicable).
    """

    st.markdown("### More Filters")
    year = None
    # Select month(s)
    selected_months = st.multiselect(
        "Select month(s)",
        ["January", "February", "March", "April", "May", "June", 
                 "July", "August", "September", "October", "November", "December"], None,
    )
    # Select season(s)
    selected_seasons = st.multiselect(
        "Select season(s)",
        options=["Winter", "Spring", "Summer", "Fall"],
        default=None
    )
    # Only show the year selection if a month or a season is selected
    if selected_months or selected_seasons:
        # Get the current year
        current_year = datetime.datetime.now().year
        
        # Generate a list of years from 2016 to the current year
        years = list(range(2016, current_year + 1))
        
        # Streamlit selectbox for year
        year = st.selectbox("Select year", options=years, index=0)

    else:
        year = None
        st.write("Please select a month or season to choose a year.")

        
    # Select the sensors or weather values or parking values
    category_based_filters = {
        "weather" : [
            'Temperature (°C)', 'Precipitation (mm)', 'Wind Speed (km/h)', 'Relative Humidity (%)', 'Sunshine Duration (min'
            ],
        "parking" : {'sensors':[
                                'p-r-spiegelau-1','parkplatz-fredenbruecke-1','parkplatz-graupsaege-1',
                                'parkplatz-nationalparkzentrum-falkenstein-2','parkplatz-nationalparkzentrum-lusen-p2'
                                'parkplatz-skisportzentrum-finsterau-1','parkplatz-waldhaeuser-ausblick-1',
                                'parkplatz-waldhaeuser-kirche-1','parkplatz-zwieslerwaldhaus-1',
                                'parkplatz-zwieslerwaldhaus-nord-1','scheidt-bachmann-parkplatz-1',
                                'skiwanderzentrum-zwieslerwaldhaus-2'],

                     'properties':[
                         'occupancy', 'capacity', 'occupancy_rate'],
                    },

        'visitor_sensors'  :[
                                        'Bayerisch Eisenstein', 'Bayerisch Eisenstein IN',
                                        'Bayerisch Eisenstein OUT', 'Bayerisch Eisenstein Fußgänger',
                                        'Bayerisch Eisenstein Fahrräder',
                                        'Bayerisch Eisenstein Fußgänger IN',
                                        'Bayerisch Eisenstein Fußgänger OUT',
                                        'Bayerisch Eisenstein Fahrräder IN',
                                        'Bayerisch Eisenstein Fahrräder OUT', 'Brechhäuslau IN',
                                        'Brechhäuslau OUT', 'Brechhäuslau', 'Brechhäuslau Fußgänger IN',
                                        'Brechhäuslau Fußgänger OUT', 'Bucina_Multi', 'Bucina_Multi OUT',
                                        'Bucina_Multi Fußgänger', 'Bucina_Multi Fahrräder',
                                        'Bucina_Multi Fußgänger IN', 'Bucina_Multi Fahrräder IN',
                                        'Bucina_Multi Fahrräder OUT', 'Bucina_Multi Fußgänger OUT',
                                        'Deffernik', 'Deffernik IN', 'Deffernik OUT',
                                        'Deffernik Fußgänger', 'Deffernik Fahrräder',
                                        'Deffernik Fahrräder IN', 'Deffernik Fahrräder OUT',
                                        'Deffernik Fußgänger IN', 'Deffernik Fußgänger OUT',
                                        'Diensthüttenstraße', 'Diensthüttenstraße Fußgänger IN',
                                        'Diensthüttenstraße Fußgänger OUT', 'Felswandergebiet',
                                        'Felswandergebiet IN', 'Felswandergebiet OUT', 'Ferdinandsthal',
                                        'Ferdinandsthal IN', 'Ferdinandsthal OUT', 'Fredenbrücke',
                                        'Fredenbrücke Fußgänger IN', 'Fredenbrücke Fußgänger OUT', 'Gfäll',
                                        'Gfäll Fußgänger IN', 'Gfäll Fußgänger OUT', 'Gsenget',
                                        'Gsenget IN', 'Gsenget OUT', 'Gsenget Fußgänger',
                                        'Gsenget Fahrräder', 'Gsenget IN.1', 'Gsenget OUT.1',
                                        'Gsenget Fahrräder IN', 'Gsenget Fahrräder OUT',
                                        'Klingenbrunner Wald', 'Klingenbrunner Wald IN',
                                        'Klingenbrunner Wald OUT', 'Klingenbrunner Wald Fußgänger',
                                        'Klingenbrunner Wald Fahrräder',
                                        'Klingenbrunner Wald Fußgänger IN',
                                        'Klingenbrunner Wald Fußgänger OUT',
                                        'Klingenbrunner Wald Fahrräder IN',
                                        'Klingenbrunner Wald Fahrräder OUT', 'Klosterfilz',
                                        'Klosterfilz IN', 'Klosterfilz OUT', 'Klosterfilz Fußgänger',
                                        'Klosterfilz Fahrräder', 'Klosterfilz Fußgänger IN',
                                        'Klosterfilz Fußgänger OUT', 'Klosterfilz Fahrräder IN',
                                        'Klosterfilz Fahrräder OUT', 'Racheldiensthütte',
                                        'Racheldiensthütte IN', 'Racheldiensthütte OUT',
                                        'Racheldiensthütte Fußgänger', 'Racheldiensthütte Fahrräder',
                                        'Racheldiensthütte Fahrräder IN', 'Racheldiensthütte Cyclist OUT',
                                        'Racheldiensthütte Pedestrian IN',
                                        'Racheldiensthütte Pedestrian OUT', 'Sagwassersäge',
                                        'Sagwassersäge Fußgänger IN', 'Sagwassersäge Fußgänger OUT',
                                        'Scheuereck', 'Scheuereck IN', 'Scheuereck OUT', 'Schillerstraße',
                                        'Schillerstraße IN', 'Schillerstraße OUT', 'Schwarzbachbrücke',
                                        'Schwarzbachbrücke Fußgänger IN',
                                        'Schwarzbachbrücke Fußgänger OUT', 'TFG_Falkenstein_1',
                                        'TFG_Falkenstein_1 Fußgänger zum Parkplatz',
                                        'TFG_Falkenstein_1 Fußgänger zum HZW', 'TFG_Falkenstein_2',
                                        'TFG_Falkenstein_2 Fußgänger In Richtung Parkplatz',
                                        'TFG_Falkenstein_2 Fußgänger In Richtung TFG', 'TFG_Lusen_1',
                                        'TFG_Lusen_1 Fußgänger Richtung TFG',
                                        'TFG_Lusen_1 Fußgänger Richtung Parkplatz', 'TFG_Lusen_2',
                                        'TFG_Lusen_2 Fußgänger Richtung Vögel am Waldrand',
                                        'TFG_Lusen_2 Fußgänger Richtung Parkplatz', 'TFG_Lusen_3',
                                        'TFG_Lusen_3 TFG Lusen 3 IN', 'TFG_Lusen_3 TFG Lusen 3 OUT',
                                        'Trinkwassertalsperre_MULTI', 'Trinkwassertalsperre_MULTI IN',
                                        'Trinkwassertalsperre_MULTI OUT',
                                        'Trinkwassertalsperre_MULTI Fußgänger',
                                        'Trinkwassertalsperre_MULTI Fußgänger IN',
                                        'Trinkwassertalsperre_MULTI Fußgänger OUT',
                                        'Trinkwassertalsperre_MULTI Fahrräder',
                                        'Trinkwassertalsperre_MULTI Fahrräder IN',
                                        'Trinkwassertalsperre_MULTI Fahrräder OUT', 'Waldhausreibe',
                                        'Waldhausreibe IN', 'Waldhausreibe OUT', 'Waldspielgelände_1',
                                        'Waldspielgelände_1 IN', 'Waldspielgelände_1 OUT', 'Wistlberg',
                                        'Wistlberg Fußgänger IN', 'Wistlberg Fußgänger OUT'],
                                
                                  
        'visitor_centers' : [
                            'Besuchszahlen_HEH',
                            'Besuchszahlen_HZW', 'Besuchszahlen_WGM', 'Parkpl_HEH_PKW',
                            'Parkpl_HEH_BUS', 'Parkpl_HZW_PKW', 'Parkpl_HZW_BUS'
                            ]
    }
    if category == "weather":
        selected_properties = st.multiselect("Select the weather properties", category_based_filters[category], default=None)
        selected_sensors = None

    elif category == "parking":
        selected_properties = st.multiselect("Select the parking values", category_based_filters[category]['properties'], default=None)  
        selected_sensors = st.multiselect("Select the parking sensor you want to find the values for?", category_based_filters[category]['sensors'], default=None)

    elif category == "visitor_sensors":
        selected_sensors = st.multiselect("Select the visitor sensor you want to find the count for?", category_based_filters[category], default=None)
        selected_properties = None

    elif category == "visitor_centers":
        selected_sensors = st.multiselect("Select the visitor center you want to find the count for?", category_based_filters[category], default=None)
        selected_properties = None

    else:
        selected_properties = None
        selected_sensors = None

    return selected_months, selected_seasons, selected_properties, selected_sensors, year

def get_queries_for_parking(start_date, end_date, months, seasons, selected_properties, selected_sensors, year):
    
    """
    Generate queries for parking data based on selected date range, months, seasons, properties, and sensors.

    Args:
        start_date (str): The start date for the query.
        end_date (str): The end date for the query.
        months (list): List of selected months for the query.
        seasons (list): List of selected seasons for the query.
        selected_properties (list): List of parking properties to include in the query (e.g., occupancy, capacity).
        selected_sensors (list): List of parking sensors to query data for.
        year (int): The year to use in the queries for months and seasons.

    Returns:
        dict: A dictionary with keys "type1", "type2", and "type3" containing queries for the date range, 
              months, and seasons respectively.
    """
          
    queries = {}

    if selected_sensors:
        for sensor in selected_sensors:
            # Queries for the start_date and end_date range
            for property in selected_properties:
                queries.setdefault("type1", []).append(
                    f"What is the {property} value for the sensor {sensor} from {start_date} to {end_date}?"
                )

            # Queries for each selected month and year
            if months:
                for month in months:
                    for property in selected_properties:
                        queries.setdefault("type2", []).append(
                            f"What is the {property} value for the sensor {sensor} for the month of {month} ({year})?"
                        )

            # Queries for each selected season and year
            if seasons:
                for season in seasons:
                    for property in selected_properties:
                        queries.setdefault("type3", []).append(
                            f"What is the {property} value for the sensor {sensor} for the season of {season} ({year})?"
                        )

    return queries

def get_queries_for_weather(start_date, end_date, months, seasons, selected_properties, year):
    queries = {}

    # Queries for the date range (type1)
    for property in selected_properties:
        queries.setdefault("type4", []).append(
            f"What is the {property} value from {start_date} to {end_date}?"
        )

    # Queries for the selected months and year (type2)
    if months:
        for month in months:
            for property in selected_properties:
                queries.setdefault("type5", []).append(
                    f"What is the {property} value for the month of {month} for the year {year}?"
                )

    # Queries for the selected seasons and year (type3)
    if seasons:
        for season in seasons:
            for property in selected_properties:
                queries.setdefault("type6", []).append(
                    f"What is the {property} value for the season of {season} for the year {year}?"
                )

    return queries

def get_queries_for_visitor_centers(start_date, end_date, months, seasons, selected_sensors, year):
    
    """
    Generate queries for visitor center data based on selected date range, months, seasons, and sensors.

    Args:
        start_date (str): The start date for the query.
        end_date (str): The end date for the query.
        months (list): List of selected months for the query.
        seasons (list): List of selected seasons for the query.
        selected_sensors (list): List of visitor center sensors to query data for.
        year (int): The year to use in the queries for months and seasons.

    Returns:
        dict: A dictionary with keys "type4", "type5", and "type6" containing queries for the date range, 
              months, and seasons respectively.
    """

    queries = {}

    # Queries for the date range (type1)
    for sensor in selected_sensors:
        queries.setdefault("type4", []).append(
            f"What is the {sensor} value from {start_date} to {end_date}?"
        )

    # Queries for the selected months and year (type2)
    if months:
        for month in months:
            for sensor in selected_sensors:
                queries.setdefault("type5", []).append(
                    f"What is the {sensor} value for the month of {month} for the year {year}?"
                )

    # Queries for the selected seasons and year (type3)
    if seasons:
        for season in seasons:
            for sensor in selected_sensors:
                queries.setdefault("type6", []).append(
                    f"What is the {sensor} value for the season of {season} for the year {year}?"
                )

    return queries


def get_queries_for_visitor_sensors(start_date, end_date, months, seasons, selected_sensors, year):
    
    """
    Generate queries for visitor sensor data based on selected date range, months, seasons, and sensors.

    Args:
        start_date (str): The start date for the query.
        end_date (str): The end date for the query.
        months (list): List of selected months for the query.
        seasons (list): List of selected seasons for the query.
        selected_sensors (list): List of visitor sensors to query data for.
        year (int): The year to use in the queries for months and seasons.

    Returns:
        dict: A dictionary with keys "type4", "type5", and "type6" containing queries for the date range, 
              months, and seasons respectively.
    """
    
    queries = {}

    # Queries for the date range (type1)
    for sensor in selected_sensors:
        queries.setdefault("type4", []).append(
            f"What is the {sensor} value from {start_date} to {end_date}?"
        )

    # Queries for the selected months and year (type2)
    if months:
        for month in months:
            for sensor in selected_sensors:
                queries.setdefault("type5", []).append(
                    f"What is the {sensor} value for the month of {month} for the year {year}?"
                )

    # Queries for the selected seasons and year (type3)
    if seasons:
        for season in seasons:
            for sensor in selected_sensors:
                queries.setdefault("type6", []).append(
                    f"What is the {sensor} value for the season of {season} for the year {year}?"
                )

    return queries


def generate_queries(category, start_date, end_date, months, seasons, selected_properties, selected_sensors, year):
    
    """
    Generate queries based on the selected category, date range, months, and seasons.

    Args:
        category (str): The category of data (e.g., 'parking', 'weather', 'visitor_sensors', 'visitor_centers').
        start_date (str): The start date for the queries.
        end_date (str): The end date for the queries.
        months (list): List of selected months for the queries.
        seasons (list): List of selected seasons for the queries.
        selected_properties (list): List of selected properties relevant to the category.
        selected_sensors (list): List of selected sensors relevant to the category.
        year (int): The year to use in the queries for months and seasons.

    Returns:
        dict: A dictionary containing generated queries based on the specified category and filters.
    """

    if category == 'parking':
        queries = get_queries_for_parking(start_date, end_date, months, seasons, selected_properties, selected_sensors, year)
    if category == 'weather':
        queries = get_queries_for_weather(start_date, end_date, months, seasons, selected_properties, year)
    if category == 'visitor_sensors':
        queries = get_queries_for_visitor_sensors(start_date, end_date, months, seasons, selected_sensors, year)
    if category == 'visitor_centers':
        queries = get_queries_for_visitor_centers(start_date, end_date, months, seasons, selected_sensors, year)
    return queries

def get_query_section():
    
    """
    Get the query section for data selection and execution.

    This function displays a user interface for selecting data categories, date ranges, 
    and additional filters such as months and seasons. It allows users to generate 
    specific queries and execute them to retrieve data.

    Returns:
        None: This function does not return any values but updates the Streamlit UI
              with the selected query results and visualizations.
    """
    # display the query box
    st.markdown("## Data query")

    col1, col2 = st.columns((1,1))

    with col1:
        selected_category = select_category()
        print(selected_category)

    with col2:
        start_date, end_date = select_date()
        print(start_date, end_date)

    # add a more filters section to select months seasons etc
    # with st.form("More filters"):
       
    months, seasons, selected_properties, selected_sensors, year = select_filters(selected_category)
    
    # Give options to select your queries in form of a dropdown
    queries_dict = generate_queries(selected_category, start_date, end_date, months, seasons, selected_properties,selected_sensors,year)

    # get all the values of the all the keys in the dictionary queries

    queries = [query for query_list in queries_dict.values() for query in query_list]

    with st.form("Select a query"):

        selected_query = st.selectbox("Select a query", queries)
        
        # get the type of the selected query from the queries dictionary
        for key, value in queries_dict.items():
            if selected_query in value:
                selected_query_type = key

        submitted = st.form_submit_button("Run Query")
    if submitted:
        # get_data_from_query(selected_query,selected_query_type,selected_category)
        queried_df = get_data_from_query(selected_category,selected_query,selected_query_type)
        
        # handle error if the queried df is an empty dataframe
        if queried_df.empty:
            st.error("Error: The query returned an empty dataframe. Please try again.")
            st.stop()
        else:
            st.write("Query executed successfully!")

            # get visualization for the queried data
            get_visualization_section(queried_df)


  


