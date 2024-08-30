import hmac
import streamlit as st
import awswrangler as wr
import pandas as pd
import plotly.express as px

bucket = "dssgx-munich-2024-bavarian-forest"
preprocessed_data_folder = "preprocessed_data"

st.write("# Bavarian Forest admin page")

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here
st.write("This page is under construction  🚧 ")

st.write("# Visitor Count Information")

# Load the predicted data from the AWS S3 bucket
path = f"s3://{bucket}/{preprocessed_data_folder}/predicted_traffic_for_dashboard.csv"
predicted_df = wr.s3.read_csv(path=path)

# Confirm data load
print("Predicted values from model data loaded successfully!")

# Convert the 'Unnamed: 0' column to datetime format
predicted_df['Unnamed: 0'] = pd.to_datetime(predicted_df['Unnamed: 0'])

# Get the days and dates from the values(dates) in the 'Unnamed: 0' column
predicted_df['day'] = predicted_df['Unnamed: 0'].dt.day_name()
predicted_df['date'] = predicted_df['Unnamed: 0'].dt.strftime('%Y-%m-%d')

# Create a combined day and date column for better interpretation
predicted_df['day_date'] = predicted_df['day'] + " (" + predicted_df['date'] + ")"

# Get unique values for the day and date list
days_list = predicted_df['day_date'].unique()

# Get radio button for selecting the day
day_selected = st.radio(
    label='Select a day', options=days_list, index=0
)

# Filter the DataFrame based on the selected day
day_df = predicted_df[predicted_df['day_date'] == day_selected]

# Plot an interactive bar chart for absolute traffic prediction
day_df['prediction_color'] = day_df['prediction_label'].apply(
    lambda x: 'red' if x > 100 else 'green' if x < 30 else 'blue'
)

# Get the maximum value of the occupancy column for fixing the y-axis
max_occupancy_value = predicted_df['prediction_label'].max()

fig2 = px.bar(
    day_df,
    x='Unnamed: 0',  # timestamp column
    y='prediction_label',
    color='prediction_color',  # Use the prediction color column
    labels={'prediction_label': 'Expected Traffic (Absolute)', 'Unnamed: 0': 'Hour of Day'},
    title=f"Expected Visitor Foot Traffic (Absolute , Hourly) for {day_selected}",
    color_discrete_map={'red': 'red', 'blue': 'blue', 'green': 'green'}
)

# Customize hover text for absolute traffic prediction
fig2.update_traces(
    hovertemplate=(
        'Hour: %{x|%H:%M}<br>'
        'Occupancy: %{y} visitors <br>'  # Add the prediction_label value as "Occupancy" in hover info
    ),
)


# Update layout for absolute traffic chart
fig2.update_layout(
    xaxis_title='Hour of the selected day',
    yaxis_title='Expected Traffic (Absolute)',  # Added y-axis title
    template='plotly_dark',
    legend_title_text='Visitor Foot Traffic',
    yaxis=dict(range=[0, max_occupancy_value])  # Fixing the y-axis
)

# Update the legend names
fig2.for_each_trace(
    lambda t: t.update(name={
        'red': 'High Occupancy',
        'blue': 'Medium Occupancy',
        'green': 'Low Occupancy'
    }.get(t.name, t.name))
)


# Display the interactive bar chart for absolute traffic prediction
st.plotly_chart(fig2)
