import streamlit as st
from PIL import Image
import base64




# def get_recreation_section():
#     """
#     Display recreational activities in the Bavarian Forest National Park.
#     """


#     st.markdown("### Recreational Activities")

#     activities = {
#         "Hiking": {
#             "emoji": "🥾",
#             "description": "Discover the best hiking trails.",
#             "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/hiking/index.htm"
#         },
#         "Cycling": {
#             "emoji": "🚴‍♂️",
#             "description": "Explore scenic cycling routes.",
#             "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/bicycling/index.htm"
#         },
#         "Camping": {
#             "emoji": "🏕️",
#             "description": "Find serene camping spots.",
#             "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/facilities/camping/index.htm"
#         },
#         "Snowshoeing": {
#             "emoji": "🌨️",
#             "description": "Try snowshoeing in the winter.",
#             "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/snowshoeing/index.htm"
#         },
#         # "Skiing": {
#         #     "emoji": "🎿",
#         #     "description": "Enjoy cross-country skiing.",
#         #     "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/cross_country_skiing/index.htm"
#         # },
#     }

#     # Create tabs for each activity
#     tabs = st.tabs(list(activities.keys()))

#     for idx, activity in enumerate(activities):
#         with tabs[idx]:
#             st.markdown(f"### {activities[activity]['emoji']} {activity}")
#             st.write(activities[activity]["description"])
#             st.markdown(f"[More Info]({activities[activity]['link']})")



def get_recreation_section():
   
    st.markdown("### Recreational Activities")


    activities = {
        "Hiking": {
            "emoji": "🥾",
            "description": "Explore trails through the scenic wilderness.",
            "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/hiking/index.htm"
        },
        "Cycling": {
            "emoji": "🚴‍♂️",
            "description": "Cycle through picturesque routes.",
            "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/bicycling/index.htm"
        },
        "Camping": {
            "emoji": "🏕️",
            "description": "Relax under the stars at designated camping spots.",
            "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/facilities/camping/index.htm"
        },
        "Snowshoeing": {
            "emoji": "🌨️",
            "description": "Enjoy snowshoeing during the winter months.",
            "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/snowshoeing/index.htm"
        },
        "Skiing": {
            "emoji": "🎿",
            "description": "Ski on the best cross-country trails.",
            "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/cross_country_skiing/index.htm"
        },
    }

    for activity, info in activities.items():
        st.markdown(f"""
            <div style="
                padding: 5px 10px;
                margin-bottom: 8px;
                background-color: #333;
                border-radius: 5px;
                text-align: left;">
                <h5 style="color: #fff; margin: 0;">{info['emoji']} {activity}</h5>
                <p style="color: #ccc; margin: 3px 0; font-size: 0.9em;">{info['description']}</p>
                <a href="{info['link']}" target="_blank" style="color: #00ff00; font-size: 0.9em; text-decoration: none;">Learn More</a>
            </div>
        """, unsafe_allow_html=True)
