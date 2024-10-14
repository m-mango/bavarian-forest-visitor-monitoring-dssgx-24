# import libraries
import streamlit as st
from src.streamlit_app.pages_in_dashboard.visitors.language_selection_menu import TRANSLATIONS


def get_other_information():

    """
    Get the other information section.
    """
    st.markdown(f"### {TRANSLATIONS[st.session_state.selected_language]['other_information']}")


    with st.expander(f":green[{TRANSLATIONS[st.session_state.selected_language]['visitor_centers']}]"):
        st.markdown(f":green[{TRANSLATIONS[st.session_state.selected_language]['visitor_centers_description']}]")
        st.markdown(f"[{TRANSLATIONS[st.session_state.selected_language]['learn_more']}]({TRANSLATIONS[st.session_state.selected_language]['visitor_centers_link']})")

    with st.expander(f":green[{TRANSLATIONS[st.session_state.selected_language]['popular_entrances']}]"):
        st.markdown(f":green[{TRANSLATIONS[st.session_state.selected_language]['entrances_description']}]")
        st.markdown(":green[**1 - Falkenstein**]")
        st.markdown(f"[{TRANSLATIONS[st.session_state.selected_language]['learn_more']}](https://www.nationalpark-bayerischer-wald.bayern.de/besucher/einrichtungen/npz_falkenstein/index.htm)")

        st.markdown(":green[**2 - Lusen**]")
        st.markdown(f"[{TRANSLATIONS[st.session_state.selected_language]['learn_more']}](https://www.nationalpark-bayerischer-wald.bayern.de/besucher/einrichtungen/npz_lusen/index.htm)")

    with st.expander(f":green[{TRANSLATIONS[st.session_state.selected_language]['best_way_to_get_there']}]"):
        st.markdown(f":green[{TRANSLATIONS[st.session_state.selected_language]['getting_there_description']}]")
        st.markdown(f"[{TRANSLATIONS[st.session_state.selected_language]['learn_more']}](https://www.nationalpark-bayerischer-wald.bayern.de/service/anreise/)")


    

