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

    # Select month(s)
    months = st.multiselect(
        "Select month(s)",
        options=["January", "February", "March", "April", "May", "June", 
                 "July", "August", "September", "October", "November", "December"],
        default=None
    )
    
    # Select season(s)
    seasons = st.multiselect(
        "Select season(s)",
        options=["Winter", "Spring", "Summer", "Fall"],
        default=None
    )
    # Select the sensors or weather values or parking values
    category_based_filters = {
        "weather" : ['Temperature', 'Humidity', 'Wind Speed', 'Precipitation', 'Sunshine Duration'],
        "parking" : {'sensors':['p-r-spiegelau-1','parkplatz-fredenbruecke-1','parkplatz-graupsaege-1',
                                'parkplatz-nationalparkzentrum-falkenstein-2','parkplatz-nationalparkzentrum-lusen-p2'
                                'parkplatz-skisportzentrum-finsterau-1','parkplatz-waldhaeuser-ausblick-1',
                                'parkplatz-waldhaeuser-kirche-1','parkplatz-zwieslerwaldhaus-1',
                                'parkplatz-zwieslerwaldhaus-nord-1','scheidt-bachmann-parkplatz-1',
                                'skiwanderzentrum-zwieslerwaldhaus-2'],
                     'properties':['Occupancy', 'Capacity', 'Occupancy Rate'],},
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

    return months, seasons, selected_properties

def generate_queries(category, start_date, end_date, months, seasons, selected_properties):
    """
    Generate queries based on the selected category, date range, months, and seasons.
    assign the queries to a dictionary with type 1 query is "What is the {category} value from the {start_date} to the {end_date}?"
    type2 query is "What is the {category} value for the month of {month}?" and type 3 query is "What is the {category} value for the season of {season}?"

    """

    queries = {}

    queries["type1"] = f"What is the {category} value from the {start_date} to the {end_date}?"

    if months:
        for month in months:
            queries["type2"] = (f"What is the {category} value for the month of {month}?")
    if seasons:
        for season in seasons:
            queries["type3"] = (f"What is the {category} value for the season of {season}?")
    if selected_properties:
        for property in selected_properties:
            queries["type4"] = (f"What is the {property} {category} value from the {start_date} to the {end_date}?")

    return queries

def get_query_section():
    """
    Get the query section.
    """

    # display the query box

    # add a more filters section to select months seasons etc
    with st.form("More filters"):
        st.markdown("## Data query")

        col1, col2 = st.columns((1,1))

        with col1:
            selected_category = select_category()

        with col2:
            start_date, end_date = select_date()

        months, seasons, selected_properties = select_filters(selected_category)
        
        # Give options to select your queries in form of a dropdown
        queries_dict = generate_queries(selected_category, start_date, end_date, months, seasons, selected_properties)

        # get all the values of the all the keys in the dictionary queries

        queries = list(queries_dict.values())

        selected_query = st.selectbox("Select a query", queries)
    
        # Every form must have a submit button.
        submitted = st.form_submit_button("Run Query")
        if submitted:

            get_data_from_query(queries_dict, selected_query, selected_category)
            st.write("Query executed successfully!")
            get_visualization_section()



