#TODO: change the index name ('Unnamed: 0') of the timestamps of the predicted csv in the generation script and also in visitor_count.py
# import the necessary libraries
import streamlit as st
import awswrangler as wr
import pandas as pd
import plotly.express as px


# AWS Setup
########################################################################################

bucket = "dssgx-munich-2024-bavarian-forest"
preprocessed_data_folder = "preprocessed_data"

########################################################################################

def get_visitor_counts_section():
    """
    Get the visitor counts section with the highest occupancy rate.

    Args:
        None
    
    Returns:
        None
    """
    st.markdown("## Visitor Counts (Forecasted) 🚶🚶‍♀️")

    # Load the predicted data from the AWS S3 bucket
    path = f"s3://{bucket}/{preprocessed_data_folder}/predicted_traffic_for_dashboard.csv"
    predicted_df = wr.s3.read_csv(path=path)
    
    # Confirm data load
    print("Predicted values from model data loaded successfully!")

    # Convert the 'Unnamed: 0' column to datetime format
    predicted_df['Unnamed: 0'] = pd.to_datetime(predicted_df['Unnamed: 0'], errors='coerce')

    # Get the days from the values (dates) in the 'Unnamed: 0' column
    predicted_df['day'] = predicted_df['Unnamed: 0'].dt.day_name()

    # Create a new column to combine both date and day for radio buttons
    predicted_df['day_date'] = predicted_df['Unnamed: 0'].dt.strftime('%A, %d %b %Y')

    days_list = predicted_df['day_date'].unique()

    # Add a note that this is forecasted data
    st.markdown(":green[*The following data represents forecasted visitor traffic.*].")

    # Get radio button for selecting the day
    day_selected = st.radio(
        label='Select a day', options=days_list, index=0
    )

    # Extract the selected day for filtering (using date)
    day_df = predicted_df[predicted_df['day_date'] == day_selected]

    # Create a new column for color coding based on traffic thresholds
    day_df['traffic_color'] = day_df['weekly_relative_traffic'].apply(
        lambda x: 'red' if x > 0.40 else 'green' if x < 0.05 else 'blue'
    )

    # Plot an interactive bar chart for relative traffic
    fig1 = px.bar(
        day_df,
        x='Unnamed: 0',  # Assuming 'Unnamed: 0' column represents the hours of the day
        y='weekly_relative_traffic',
        color='traffic_color',  # Use the traffic color column
        labels={'weekly_relative_traffic': '', 'Unnamed: 0': 'Hour of Day'},
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

    # Display the interactive bar chart for relative traffic
    st.plotly_chart(fig1)

