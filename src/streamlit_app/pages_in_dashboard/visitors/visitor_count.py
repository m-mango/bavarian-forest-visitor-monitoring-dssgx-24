#TODO: change the index name ('Unnamed: 0') of the timestamps of the predicted csv in the generation script and also in visitor_count.py
# import the necessary libraries
import streamlit as st
import awswrangler as wr
import pandas as pd
import plotly.express as px


# AWS Setup
########################################################################################

bucket = "dssgx-munich-2024-bavarian-forest"
inference_data_folder = "/models/inference_data_outputs/"

########################################################################################

@st.fragment
def get_visitor_counts_section(inference_predictions):
    """
    Get the visitor counts section with the highest occupancy rate.

    Args:
        None
    
    Returns:
        None
    """
    st.markdown("## Popular Times")
    
    # do a dropdown for the all_preds
    regions_to_select = inference_predictions["region"].unique()
    selected_region = st.selectbox('Select a region to view', regions_to_select)

    if selected_region:

        # Filter the DataFrame based on the selected region
        selected_region_predictions = inference_predictions[inference_predictions['region'] == selected_region]

        # Get unique values for the day and date list
        days_list = selected_region_predictions['day_date'].unique()

        # Add a note that this is forecasted data
        st.markdown(":green[*The following data represents forecasted visitor traffic.*].")

        # Create a layout for the radio button and chart
        col1, _ = st.columns([1, 3])

        with col1:
            # Get radio button for selecting the day
            day_selected = st.radio(
                label='Select a day', options=days_list, index=0
            )

        # Extract the selected day for filtering (using date)
        day_df = selected_region_predictions[selected_region_predictions['day_date'] == day_selected]

        # Plot an interactive bar chart for relative traffic
        fig1 = px.bar(
            day_df,
            x='Time',  
            y='weekly_relative_traffic',
            color='traffic_color',  # Use the traffic color column
            labels={'weekly_relative_traffic': '', 'Time': 'Hour of Day'},
            title=f"Relative Visitor Foot Traffic for {day_selected} (Hourly)",
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
            legend_title_text='Vistor Foot Traffic',
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
        )

        # Update the legend names
        fig1.for_each_trace(
            lambda t: t.update(name={'red': 'Peak Traffic', 'green': 'Low Traffic', 'blue': 'Moderate Traffic'}[t.name])
        )

        # Display the interactive bar chart for relative traffic below the radio button
        st.plotly_chart(fig1)
