# ====================================================
# Importing Required Libraries
# ====================================================
import pandas as pd
import numpy as np
from prettytable import PrettyTable
import plotly.graph_objects as go
import plotly.express as px
import plotly as plt
import pycaret as pyc
from plotly.subplots import make_subplots
from pycaret.regression import *

# ====================================================
# Load the Visitor Center Data
# ====================================================

# Define the function to load data file
def load_excel_data(file_path):
    """
    Loads data from an Excel file into a Pandas DataFrame.

    Parameters:
    - file_path (str): The path to the Excel file.

    Returns:
    - df_visitcenters (DataFrame): The DataFrame containing the loaded data.
    """
    # Load the Excel file to a DataFrame
    df_visitcenters = pd.read_excel(file_path)
    
    return df_visitcenters

# Define the file path of the CSV file to load
file_path = r'C:\Users\garov\OneDrive\Documents\GitHub\bavarian-forest-visitor-monitoring-dssgx-24\outputs\Raw Data\national-park-vacation-times-houses-opening-times.xlsx'

# Call the function and load the data as a pandas data frame
if __name__ == "__main__":
    df_visitcenters = load_excel_data(file_path)

# ====================================================
# Load the Visitor Center Data
# ====================================================

