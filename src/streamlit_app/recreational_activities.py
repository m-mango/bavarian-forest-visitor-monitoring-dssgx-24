import streamlit as st
from PIL import Image
import base64




def get_recreation_section():
    """
    Display recreational activities in the Bavarian Forest National Park.
    """


    st.markdown("### Recreational Activities")

    activities = {
        "Hiking": {
            "emoji": "🥾",
            "description": "Discover the best hiking trails.",
            "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/hiking/index.htm"
        },
        "Cycling": {
            "emoji": "🚴‍♂️",
            "description": "Explore scenic cycling routes.",
            "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/bicycling/index.htm"
        },
        "Camping": {
            "emoji": "🏕️",
            "description": "Find serene camping spots.",
            "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/facilities/camping/index.htm"
        },
        "Snowshoeing": {
            "emoji": "🌨️",
            "description": "Try snowshoeing in the winter.",
            "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/snowshoeing/index.htm"
        },
        # "Skiing": {
        #     "emoji": "🎿",
        #     "description": "Enjoy cross-country skiing.",
        #     "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/cross_country_skiing/index.htm"
        # },
    }

    # Create tabs for each activity
    tabs = st.tabs(list(activities.keys()))

    for idx, activity in enumerate(activities):
        with tabs[idx]:
            st.markdown(f"### {activities[activity]['emoji']} {activity}")
            st.write(activities[activity]["description"])
            st.markdown(f"[More Info]({activities[activity]['link']})")




        