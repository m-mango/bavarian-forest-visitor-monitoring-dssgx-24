import streamlit as st
from PIL import Image
import base64

# def get_recreation_section():
#     """
#     Display recreational activities in the Bavarian Forest National Park.
#     """

#     # Title
#     st.markdown("### Recreational Activities")

#     # Add custom CSS for table styling
#     st.markdown("""
#         <style>
#         .activity-table {
#             width: 100%;
#             margin: auto;
#             border-collapse: collapse;
#         }
#         .activity-table td {
#             padding: 15px;
#             text-align: left;
#             vertical-align: middle;
#             border-bottom: 1px solid #dddddd;
#         }
#         .activity-table img {
#             width: 50px;
#             height: 50px;
#             margin-right: 20px;
#         }
#         a {
#             text-decoration: none;
#             color: #2e86c1;
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     # Icons with links
#     activities = [
#         {"name": "Hiking", "icon": "src/streamlit_app/assets/hiking.png", "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/hiking/index.htm"},
#         {"name": "Cross Country Skiing", "icon": "src/streamlit_app/assets/skiing.png", "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/cross_country_skiing/index.htm"},
#         {"name": "Cycling", "icon": "src/streamlit_app/assets/cycling.png", "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/bicycling/index.htm"},
#         {"name": "Camping", "icon": "src/streamlit_app/assets/camping.png", "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/facilities/camping/index.htm"},
#     ]

#     # Function to convert image to base64
#     def get_base64_image(image_path):
#         with open(image_path, "rb") as img_file:
#             encoded = base64.b64encode(img_file.read()).decode()
#         return encoded

#     # Create the table structure
#     st.markdown('<table class="activity-table">', unsafe_allow_html=True)

#     for activity in activities:
#         # Encode the icon as base64
#         base64_icon = get_base64_image(activity["icon"])
        
#         # Display each row with icon and name
#         st.markdown(f"""
#             <tr>
#                 <td>
#                     <a href="{activity['link']}" target="_blank">
#                         <img src="data:image/png;base64,{base64_icon}" alt="{activity['name']}">
#                     </a>
#                 </td>
#                 <td>
#                     <a href="{activity['link']}" target="_blank">{activity['name']}</a>
#                 </td>
#             </tr>
#         """, unsafe_allow_html=True)

#     # Close the table structure
#     st.markdown('</table>', unsafe_allow_html=True)





def get_base64_image(image_path):
    """
    Convert an image to a base64 encoded string.
    """
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded

def get_recreation_section():
    """
    Display recreational activities in the Bavarian Forest National Park.
    """

    # Title
    st.markdown("### Recreational Activities")

    # Icons with links
    activities = [
        {"name": "Hiking", "icon": "src/streamlit_app/assets/hiking.png", "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/hiking/index.htm"},
        {"name": "Cross Country Skiing", "icon": "src/streamlit_app/assets/skiing.png", "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/cross_country_skiing/index.htm"},
        {"name": "Cycling", "icon": "src/streamlit_app/assets/cycling.png", "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/bicycling/index.htm"},
        {"name": "Camping", "icon": "src/streamlit_app/assets/camping.png", "link": "https://www.nationalpark-bayerischer-wald.bayern.de/english/visitor/facilities/camping/index.htm"},
    ]

    # Create rows for each activity
    for activity in activities:
        # Encode the icon as base64
        base64_icon = get_base64_image(activity["icon"])
        
        # Create columns for icon and name
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"""
                <a href="{activity['link']}" target="_blank">
                    <img src="data:image/png;base64,{base64_icon}" alt="{activity['name']}" style="width: 50px; height: 50px;">
                </a>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <a href="{activity['link']}" target="_blank" style="text-decoration: none; color: #2e86c1;">
                    {activity['name']}
                </a>
            """, unsafe_allow_html=True)
