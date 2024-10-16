# imports
import streamlit as st
from src.streamlit_app.pages_in_dashboard.visitors.language_selection_menu import TRANSLATIONS

def get_recreation_section():
    """
    Get the recreational activities section for the Bavarian Forest National Park.

    Args:
        None
    Returns:
        None
    """
   
    st.markdown(f"### {TRANSLATIONS[st.session_state.selected_language]['recreational_activities']}")


    activities = {
        TRANSLATIONS[st.session_state.selected_language]['hiking']: {
            "emoji": "🥾",
            "description": TRANSLATIONS[st.session_state.selected_language]['hiking_description'],
            "link": TRANSLATIONS[st.session_state.selected_language]['hiking_link']
        },
        TRANSLATIONS[st.session_state.selected_language]['cycling']: {
            "emoji": "🚴‍♂️",
            "description": TRANSLATIONS[st.session_state.selected_language]['cycling_description'],
            "link": TRANSLATIONS[st.session_state.selected_language]['cycling_link']
        },
        TRANSLATIONS[st.session_state.selected_language]['camping']: {
            "emoji": "🏕️",
            "description": TRANSLATIONS[st.session_state.selected_language]['camping_description'],
            "link": TRANSLATIONS[st.session_state.selected_language]['camping_link']
        },
        TRANSLATIONS[st.session_state.selected_language]['snowshoeing']: {
            "emoji": "🌨️",
            "description": TRANSLATIONS[st.session_state.selected_language]['snowshoeing_description'],
            "link": TRANSLATIONS[st.session_state.selected_language]['snowshoeing_link']
        },
        TRANSLATIONS[st.session_state.selected_language]['skiing']: {
            "emoji": "🎿",
            "description": TRANSLATIONS[st.session_state.selected_language]['skiing_description'],
            "link": TRANSLATIONS[st.session_state.selected_language]['skiing_link']
        },
    }

    for activity, info in activities.items():
        st.markdown(f"""
            <div style="
                padding: 5px 10px;
                margin-bottom: 8px;
                background-color: #215202;
                border-radius: 5px;
                text-align: left;">
                <h5 style="color: #fff; margin: 0;">{info['emoji']} {activity}</h5>
                <p style="color: #ccc; margin: 3px 0; font-size: 0.9em;">{info['description']}</p>
                <a href="{info['link']}" target="_blank" style="color: #00a0ff; font-size: 0.9em; text-decoration: none;f">{TRANSLATIONS[st.session_state.selected_language]['learn_more']}</a>
            </div>
        """, unsafe_allow_html=True)
