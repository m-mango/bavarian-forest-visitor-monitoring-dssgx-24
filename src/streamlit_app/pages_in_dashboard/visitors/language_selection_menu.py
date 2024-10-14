import streamlit as st


# Add a dropdown menu for language selection with emojis
LANGUAGE_OPTIONS= {
    "German": "🇩🇪 Deutsch",
    "English": "🇬🇧 English",
    }
# Language dictionary with translations
TRANSLATIONS = {
    "English": {
        'title': 'Plan Your Trip to the Bavarian Forest 🌲',
        'select_language': 'Select Language',
        'visitor_counts_forecasted': 'Visitor Counts (Forecasted)',
        'forecasted_visitor_data': 'The following data represents forecasted visitor traffic',
        'select_day': 'Select a day',
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        'saturday': 'Saturday',
        'sunday': 'Sunday',
        'visitor_foot_traffic_for_day': 'Relative Visitor Foot Traffic for [day, date] (Hourly)',
        'visitor_foot_traffic': 'Visitor Foot Traffic',
        'low_traffic': 'Low Traffic',
        'moderate_traffic': 'Moderate Traffic',
        'peak_traffic': 'Peak Traffic',
        'real_time_parking_occupancy': 'Real Time Parking Occupancy',
        'select_parking_section': 'Select a parking section',
        'available_spaces': 'Available Spaces',
        'capacity': 'Capacity',
        'occupancy_rate': 'Occupancy Rate',
        'weather_forecast': 'Weather Forecast',
        '7_day_hourly_weather': '7-Day Hourly Weather Forecast',
        'temperature': 'Temperature (°C)',
        'date': 'Date',
        'mon': 'Mon',
        'tue': 'Tue',
        'wed': 'Wed',
        'thu': 'Thu',
        'fri': 'Fri',
        'sat': 'Sat',
        'sun': 'Sun',
        'peaks': 'Peaks',
        'recreational_activities': 'Recreational Activities',
        'hiking': 'Hiking | Explore trails through the scenic wilderness.',
        'cycling': 'Cycling | Cycle through picturesque routes.',
        'camping': 'Camping | Relax under the stars at designated camping spots.',
        'snowshoeing': 'Snowshoeing | Enjoy snowshoeing during the winter months.',
        'skiing': 'Skiing | Ski on the best cross-country trails.',
        'learn_more': 'Learn More',
        'other_information': 'Other Information',
        'visitor_centers': 'Visitor Centers',
        'popular_entrances': 'Popular Entrances to the Park',
        'best_way_to_get_there': 'Best Way to Get There'
    },
    "German": {
        'title': 'Planen Sie Ihren Besuch im Nationalpark Bayerischer Wald 🌲',
        'select_language': 'Sprache auswählen',
        'visitor_counts_forecasted': 'Besucheraufkommen (Prognose)',
        'forecasted_visitor_data': 'Diese Grafik zeigt den prognostizierten Besucherverkehr',
        'select_day': 'Tag auswählen',
        'monday': 'Montag',
        'tuesday': 'Dienstag',
        'wednesday': 'Mittwoch',
        'thursday': 'Donnerstag',
        'friday': 'Freitag',
        'saturday': 'Samstag',
        'sunday': 'Sonntag',
        'visitor_foot_traffic_for_day': 'Voraussichtliches Besucheraufkommen am [day, date] (pro Stunde)',
        'visitor_foot_traffic': 'Besucheraufkommen',
        'low_traffic': 'Niedrig',
        'moderate_traffic': 'Mittel',
        'peak_traffic': 'Hoch',
        'real_time_parking_occupancy': 'Parkplatzbelegung (LIVE)',
        'select_parking_section': 'Parkplatz auswählen',
        'available_spaces': 'Aktuell verfügbare Stellplätze',
        'capacity': 'Kapazität',
        'occupancy_rate': 'Belegungsrate',
        'weather_forecast': 'Wettervorhersage',
        '7_day_hourly_weather': '7-Tage Wetter',
        'temperature': 'Temperatur (°C)',
        'date': 'Datum',
        'mon': 'Mo',
        'tue': 'Di',
        'wed': 'Mi',
        'thu': 'Do',
        'fri': 'Fr',
        'sat': 'Sa',
        'sun': 'So',
        'peaks': 'Spitzen',
        'recreational_activities': 'Aktivitäten im Nationalpark Bayerischer Wald',
        'hiking': 'Wandern | 350 Kilometer bestens markiertes Wanderwegenetz.',
        'cycling': 'Radfahren | 200 km ausgewiesene Radwege.',
        'camping': 'Camping | Ausgewiesene Zelt- und Wohnmobilstellplätze',
        'snowshoeing': 'Schneeschuhwandern | Das Wanderwegenetz auch im Winter erkunden.',
        'skiing': 'Langlaufen | 80 Kilometer Langlaufloipen durch den winterlichen Nationalpark Bayerischer Wald.',
        'learn_more': 'Mehr Infos',
        'other_information': 'Weitere Information',
        'visitor_centers': 'Besucherzentren',
        'popular_entrances': 'Beliebte Zugänge zum Park',
        'best_way_to_get_there': 'Anreise und ÖPNV'
    }
}

# Initialize language in session state if it doesn't exist
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = 'German'  # Default language

def update_language():
    if st.session_state.selected_language == 'German':
        st.session_state.selected_language = 'English'
    else:
        st.session_state.selected_language = 'German'

def get_language_selection_menu():
    # Custom CSS to position the dropdown menu in the top right corner
    st.markdown(
    """
    <style>
    /* Style the selectbox for top right corner positioning */
    .stSelectbox {
        position: relative;
        top: 10px; /* Adjust top positioning */
        right: 10px; /* Adjust right positioning */
        width: 50px; /* Set dropdown width */
        z-index: 100; /* Ensure it's on top */
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    selected_language = st.selectbox(TRANSLATIONS[st.session_state.selected_language]['select_language'], 
                            options=list(LANGUAGE_OPTIONS.values()),
                            index=0 if st.session_state.selected_language == 'German' else 1,
                            # Update the session_state when changing the input
                            on_change=update_language,
                            )