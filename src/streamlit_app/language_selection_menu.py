import streamlit as st


# Add a dropdown menu for language selection with emojis
LANGUAGE_OPTIONS= {
    "English": "🇬🇧 English",
    "German": "🇩🇪 Deutsch",
    }
# Language dictionary with translations
TRANSLATIONS = {
    "English": {
        "title": "Plan Your Trip",
        "description": "Welcome to the National Park Dashboard",
        "weather": "Weather Forecast",
        "forecast": "Occupancy Forecast",
        "parking": "Parking Information",
        "recreation": "Recreational Activities",
        "travel": "How to Reach",
    },
    "German": {
        "title": "Planen Sie Ihre Reise",
        "description": "Willkommen im Nationalpark-Dashboard",
        "weather": "Wettervorhersage",
        "forecast": "Belegungsprognose",
        "parking": "Parkplatzinformationen",
        "recreation": "Freizeitaktivitäten",
        "travel": "Anreise",
    },
}


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

    language = st.selectbox("Select Language", 
                            options=list(LANGUAGE_OPTIONS.keys()), 
                            format_func=lambda x: LANGUAGE_OPTIONS[x])

    # Use the selected language to display content
    selected_lang = TRANSLATIONS[language]