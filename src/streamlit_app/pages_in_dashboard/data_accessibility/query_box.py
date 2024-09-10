# Import libraries
import streamlit as st
import awswrangler as wr
import datetime
from src.streamlit_app.pages_in_dashboard.data_accessibility.data_retrieval import get_data_from_query
from src.streamlit_app.pages_in_dashboard.data_accessibility.query_viz_and_download import get_visualization_section


def select_category():
    """
    Select the category of data to access.

    Returns:
    """
    # select the dropdown for the category
    category = st.selectbox("Select data category", 
                            ["weather", "visitor occupancy", "parking"],
                            index=0)
    
    return category

def select_date():
    """
    Select the date of the data to access.
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
    Select additional filters such as months, seasons, etc.
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
        "weather" : ['Temperature (°C)', 'Precipitation (mm)', 'Wind Speed (km/h)', 'Relative Humidity (%)', 'Sunshine Duration (min'],
        "parking" : {'sensors':['p-r-spiegelau-1','parkplatz-fredenbruecke-1','parkplatz-graupsaege-1',
                                'parkplatz-nationalparkzentrum-falkenstein-2','parkplatz-nationalparkzentrum-lusen-p2'
                                'parkplatz-skisportzentrum-finsterau-1','parkplatz-waldhaeuser-ausblick-1',
                                'parkplatz-waldhaeuser-kirche-1','parkplatz-zwieslerwaldhaus-1',
                                'parkplatz-zwieslerwaldhaus-nord-1','scheidt-bachmann-parkplatz-1',
                                'skiwanderzentrum-zwieslerwaldhaus-2'],
                     'properties':['occupancy', 'capacity', 'occupancy rate'],},
        "visitor occupancy"  : {'sensors':["Bayerisch Eisenstein", "Brechhäuslau", "Deffernik", "Diensthüttenstraße", "Felswandergebiet", "Ferdinandsthal", "Fredenbrücke", "Gfäll", "Gsenget", "Klingenbrunner Wald",
                              "Klosterfilz", "Racheldiensthütte", "Schillerstraße", "Scheuereck", "Schwarzbachbrücke", "Falkenstein 2", "Lusen 2","Lusen 3", "Waldhausreibe", "Waldspielgelände", "Wistlberg",
                              "Bucina", "Falkenstein 1", "Lusen 1", "Trinkwassertalsperre"],
                              'properties':['IN','OUT','TOTAL']}
    }
    if category == "weather":
        selected_properties = st.multiselect("Select the weather properties", category_based_filters[category], default=None)
        selected_sensors = None
    elif category == "parking":
        selected_properties = st.multiselect("Select the parking values", category_based_filters[category]['properties'], default=None)  
        selected_sensors = st.multiselect("Select the parking sensor you want to find the values for?", category_based_filters[category]['sensors'], default=None)
    elif category == "visitor occupancy":
        selected_properties = st.multiselect("Select the visitor sensor you want to find the occupancy for?", category_based_filters[category]['properties'], default=None)
        selected_sensors = st.multiselect("Select the visitor sensor you want to find the occupancy for?", category_based_filters[category]['sensors'], default=None)
    else:
        selected_properties = None
        selected_sensors = None

    return selected_months, selected_seasons, selected_properties, selected_sensors, year

def get_queries_for_parking(start_date, end_date, months, seasons, selected_properties, selected_sensors, year):
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




def get_queries_for_visitor_occupancy(start_date, end_date, months, seasons, selected_properties, selected_sensors, year):
    queries = {}

    # Queries for the date range (type1)
    if selected_sensors:
        for sensor in selected_sensors:
            for property in selected_properties:
                queries.setdefault("type1", []).append(
                    f"What is the {property} value for the sensor {sensor} from {start_date} to {end_date}?"
                )

    # Queries for the selected months and year (type2)
    if months:
        for month in months:
            for sensor in selected_sensors:
                for property in selected_properties:
                    queries.setdefault("type2", []).append(
                        f"What is the {property} value for the sensor {sensor} for the month of {month} for the year {year}?"
                    )

    # Queries for the selected seasons and year (type3)
    if seasons:
        for season in seasons:
            for sensor in selected_sensors:
                for property in selected_properties:
                    queries.setdefault("type3", []).append(
                        f"What is the {property} value for the sensor {sensor} for the season of {season} for the year {year}?"
                    )

    return queries


def generate_queries(category, start_date, end_date, months, seasons, selected_properties, selected_sensors, year):
    """
    Generate queries based on the selected category, date range, months, and seasons.
    assign the queries to a dictionary with type 1 query is "What is the {category} value from the {start_date} to the {end_date}?"
    type2 query is "What is the {category} value for the month of {month}?" and type 3 query is "What is the {category} value for the season of {season}?"

    """

    if category == 'parking':
        queries = get_queries_for_parking(start_date, end_date, months, seasons, selected_properties, selected_sensors, year)
    if category == 'weather':
        queries = get_queries_for_weather(start_date, end_date, months, seasons, selected_properties, year)
    if category == 'visitor occupancy':
        queries = get_queries_for_visitor_occupancy(start_date, end_date, months, seasons, selected_properties, selected_sensors, year)

    return queries

def get_query_section():
    """
    Get the query section.
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
            get_visualization_section()


            # get visualization for the queried data
            get_visualization_section(queried_df)


  


