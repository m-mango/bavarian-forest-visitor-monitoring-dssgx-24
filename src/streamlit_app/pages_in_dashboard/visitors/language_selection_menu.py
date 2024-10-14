import streamlit as st


# Add a dropdown menu for language selection with emojis
LANGUAGE_OPTIONS= {
    "German": "🇩🇪 Deutsch",
    "English": "🇬🇧 English",
    }
# Language dictionary with translations
TRANSLATIONS = {
    "English": {
        'title': 'Plan Your Trip to the Bavarian Forest',
        'select_language': 'Select Language'
    },
    "German": {
        'title': 'Planen Sie Ihren Besuch im Nationalpark Bayerischer Wald',
        'select_language': 'Sprache auswählen'
    },
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