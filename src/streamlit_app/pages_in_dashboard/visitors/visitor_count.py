#TODO: change the index name ('Unnamed: 0') of the timestamps of the predicted csv in the generation script and also in visitor_count.py
# import the necessary libraries
import streamlit as st
import awswrangler as wr
import pandas as pd
import plotly.express as px
from src.streamlit_app.pages_in_dashboard.visitors.language_selection_menu import TRANSLATIONS
from sklearn.preprocessing import MinMaxScaler


# AWS Setup
########################################################################################

bucket = "dssgx-munich-2024-bavarian-forest"
inference_data_folder = "/models/inference_data_outputs/"

########################################################################################

regions = {
    'Bayerischer Wald Total': ['traffic_abs'],
    'Nationalparkzentrum Falkenstein': ['Nationalparkzentrum Falkenstein IN', 'Nationalparkzentrum Falkenstein OUT'],
    'Nationalparkzentrum Lusen': ['Nationalparkzentrum Lusen IN', 'Nationalparkzentrum Lusen OUT'],
    'Falkenstein-Schwellhäusl': ['Falkenstein-Schwellhäusl IN', 'Falkenstein-Schwellhäusl OUT'],
    'Scheuereck-Schachten-Trinkwassertalsperre': ['Scheuereck-Schachten-Trinkwassertalsperre IN', 'Scheuereck-Schachten-Trinkwassertalsperre OUT'],
    'Lusen-Mauth-Finsterau': ['Lusen-Mauth-Finsterau IN', 'Lusen-Mauth-Finsterau OUT'],
    'Rachel-Spiegelau': ['Rachel-Spiegelau IN', 'Rachel-Spiegelau OUT'],
}

@st.fragment
def get_visitor_counts_section(inference_predictions):
    """
    Get the visitor counts section with the highest occupancy rate.

    Args:
        None
    
    Returns:
        None
    """
    st.markdown(f"## {TRANSLATIONS[st.session_state.selected_language]['visitor_counts_forecasted']}")

    # Calculate the traffic rate per region
    for key, value in regions.items():
        if len(value) == 2:
            inference_predictions[key] = inference_predictions[value[0]] + inference_predictions[value[1]]
        else:
            inference_predictions[key] = inference_predictions[value]

        # Create a weekly relative traffic column with sklearn min-max scaling
        scaler = MinMaxScaler()
        inference_predictions[f'weekly_relative_traffic_{key}'] = scaler.fit_transform(inference_predictions[[key]])

        # Create a new column for color coding based on traffic thresholds
        inference_predictions[f'traffic_color_{key}'] = inference_predictions[f'weekly_relative_traffic_{key}'].apply(
            lambda x: 'red' if x > 0.40 else 'green' if x < 0.05 else 'blue'
        )
    
    # do a dropdown for the all_preds
    regions_to_select = list(regions.keys())
    selected_region = st.selectbox(TRANSLATIONS[st.session_state.selected_language]['select_region'], regions_to_select)

    if selected_region:

        # Filter the DataFrame based on the selected region
        selected_region_predictions = inference_predictions[["Time", "day_date", selected_region, f"weekly_relative_traffic_{selected_region}", f"traffic_color_{selected_region}"]]

        # Get unique values for the day and date list
        days_list = selected_region_predictions['day_date'].unique()

        # Add a note that this is forecasted data
        st.markdown(f":green[*{TRANSLATIONS[st.session_state.selected_language]['forecasted_visitor_data']}*].")

        # Create a layout for the radio button and chart
        col1, _ = st.columns([1, 3])

        with col1:
            # Get radio button for selecting the day
            day_selected = st.radio(
                label=TRANSLATIONS[st.session_state.selected_language]['select_day'], options=days_list, index=0
            )

        # Extract the selected day for filtering (using date)
        day_df = selected_region_predictions[selected_region_predictions['day_date'] == day_selected]

        # Plot an interactive bar chart for relative traffic
        fig1 = px.bar(
            day_df,
            x='Time',  
            y=f'weekly_relative_traffic_{selected_region}',
            color=f'traffic_color_{selected_region}',  # Use the traffic color column
            labels={f'weekly_relative_traffic_{selected_region}': '', 'Time': 'Hour of Day'},
            title=f"{TRANSLATIONS[st.session_state.selected_language]['visitor_foot_traffic_for_day']} - {day_selected}",
            color_discrete_map={'red': 'red', 'blue': 'blue', 'green': 'green'}
        )

        # Customize hover text for relative traffic
        fig1.update_traces(
            hovertemplate=(
                'Hour: %{x|%H:%M}<br>'  # Display the hour in HH:MM format
            )
        )

        # Update layout for relative traffic chart
        fig1.update_yaxes(range=[0, 1], showticklabels=False)  # Set y-axis to range from 0 to 1 and hide tick labels
        fig1.update_xaxes(showticklabels=True)  # Keep the x-axis tick labels visible

        fig1.update_layout(
            xaxis_title=None,  # Hide the x-axis title
            yaxis_title=None,  # Hide the y-axis title
            template='plotly_dark',
            legend_title_text=TRANSLATIONS[st.session_state.selected_language]['visitor_foot_traffic'],
            legend=dict(
                itemsizing='constant',
                traceorder="normal",
                font=dict(size=12),
                orientation="h",
                yanchor="top",
                y=-0.3,  # Position the legend below the chart
                xanchor="center",
                x=0.5  # Center the legend horizontally
            ),
            xaxis=dict(
                tickformat='%H:%M'
            )
        )

        # Update the legend names
        fig1.for_each_trace(
            lambda t: t.update(name={
                'red': TRANSLATIONS[st.session_state.selected_language]['peak_traffic'], 'green': TRANSLATIONS[st.session_state.selected_language]['low_traffic'], 'blue': TRANSLATIONS[st.session_state.selected_language]['moderate_traffic']}[t.name])
        )

        # Display the interactive bar chart for relative traffic below the radio button
        st.plotly_chart(fig1)
