#TODO: change the index name ('Unnamed: 0') of the timestamps of the predicted csv in the generation script and also in visitor_count.py
# import the necessary libraries
import streamlit as st
import awswrangler as wr
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler


# AWS Setup
########################################################################################

bucket = "dssgx-munich-2024-bavarian-forest"
inference_data_folder = "/models/inference_data_outputs/"

########################################################################################

def get_visitor_counts_section():
    """
    Get the visitor counts section with the highest occupancy rate.

    Args:
        None
    
    Returns:
        None
    """
    st.markdown("## Popular Times")

    # get all the files from the inference data folder
    files = wr.s3.list_objects(f"s3://{bucket}{inference_data_folder}")
    # wr.s3.list_objects(f"s3://{bucket}{prefix}")
    all_preds = []

    # get all the names after extra_trees_ and before .parquet
    for file in files:
        if 'extra_trees' in file:
            all_preds.append(file.split('extra_trees_')[1].split('.parquet')[0])
    
    # do a dropdown for the all_preds
    selected_pred = st.selectbox('Select a region to view', all_preds)

    if selected_pred:
        # Load the data
        path = f"s3://{bucket}{inference_data_folder}extra_trees_{selected_pred}.parquet"
        predicted_df = wr.s3.read_parquet(path=path)
        
        # Confirm data load
        print("Predicted values from model data loaded successfully!")

        # Convert the 'Time' column to datetime format
        predicted_df['Time'] = pd.to_datetime(predicted_df['Time'], errors='coerce')

        # Get the days from the values (dates) in the 'Time' column
        predicted_df['day'] = predicted_df['Time'].dt.day_name()

        # Create a new column to combine both date and day for radio buttons
        predicted_df['day_date'] = predicted_df['Time'].dt.strftime('%A, %d %b %Y')

        # Create a weekly relative traffic column with sklearn min-max scaling
        scaler = MinMaxScaler()
        predicted_df['weekly_relative_traffic'] = scaler.fit_transform(predicted_df[['predictions']])

        # Create a new column for color coding based on traffic thresholds
        predicted_df['traffic_color'] = predicted_df['weekly_relative_traffic'].apply(
            lambda x: 'red' if x > 0.40 else 'green' if x < 0.05 else 'blue'
        )

        days_list = predicted_df['day_date'].unique()

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
        day_df = predicted_df[predicted_df['day_date'] == day_selected]

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
