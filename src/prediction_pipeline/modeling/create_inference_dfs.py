"""
This script creates a dictionary with predictions for the selected models. 

This needs to load the models from AWS and train on an inference df that is generated from 
the source_preprocess_inference_data function. 
"""

import awswrangler as wr
import pandas as pd
import streamlit as st
from pycaret.regression import load_model
from sklearn.preprocessing import MinMaxScaler


# Your AWS bucket and folder details where models are stored
bucket_name = 'dssgx-munich-2024-bavarian-forest'
folder_prefix = 'models/models_trained/1483317c-343a-4424-88a6-bd57459901d1/'  # If you have a specific folder


target_vars_et  = ['traffic_abs', 'sum_IN_abs', 'sum_OUT_abs', 
                    'Lusen-Mauth-Finsterau IN', 'Lusen-Mauth-Finsterau OUT', 
                    'Nationalparkzentrum Lusen IN', 'Nationalparkzentrum Lusen OUT',
                    'Rachel-Spiegelau IN', 'Rachel-Spiegelau OUT', 
                    'Falkenstein-Schwellhäusl IN', 'Falkenstein-Schwellhäusl OUT',
                    'Scheuereck-Schachten-Trinkwassertalsperre IN', 'Scheuereck-Schachten-Trinkwassertalsperre OUT', 
                    'Nationalparkzentrum Falkenstein IN', 'Nationalparkzentrum Falkenstein OUT']


# model names 
model_names = [f'extra_trees_{var}' for var in target_vars_et]

@st.cache_resource
def load_latest_models(bucket_name, folder_prefix, models_names):
    """
    Load the latest files from an S3 folder based on the model names, 
    and dynamically create variables with 'loaded_' as prefix.

    Parameters:
    - bucket_name (str): The name of the S3 bucket.
    - folder_prefix (str): The folder path within the bucket.
    - models (list): List of model names without the 'extra_trees_' prefix.

    Returns:
    - dict: A dictionary containing the loaded models with keys prefixed by 'loaded_'.
    """

    # Dictionary to store loaded models
    loaded_models = {}

    # Loop through each model to get the latest pickle (.pkl) file
    for model in models_names:
        # List objects in the S3 bucket with the model prefix
        saved_lr = load_model(
            platform="aws",
            authentication={'bucket' : bucket_name, 'path': folder_prefix},
            model_name=model)
        
        # Store the loaded model in the dictionary
        loaded_models[f'{model}'] = saved_lr
    
    return loaded_models



def predict_with_models(loaded_models, df_features):
    """
    Given a dictionary of models and a DataFrame of features, this function predicts the target
    values using each model and saves the inference predictions to AWS S3 (to be further loaded from Streamlit).
    
    Parameters:
    - loaded_models (dict): A dictionary of models where keys are model names and values are the trained models.
    - df_features (pd.DataFrame): A DataFrame containing the features to make predictions on.

    Returns:
    - pd.DataFrame: A DataFrame containing the predictions of all models per region.
    """

    overall_predictions = pd.DataFrame()

    # Iterate through the loaded models
    for model_name, model in loaded_models.items():
        # Check if the model has a predict method
        if hasattr(model, 'predict'):
            # Make predictions
            predictions = model.predict(df_features)
            
            # Create a new DataFrame for the predictions with the time column
            df_predictions = pd.DataFrame(predictions, columns=['predictions'])

            # Make the index column 'Time'
            df_predictions['Time'] = df_features.index

            # Make sure predictions are integers and not floats
            df_predictions['predictions'] = df_predictions['predictions'].astype(int)
    
            # save the prediction dataframe as a parquet file in aws
            wr.s3.to_parquet(df_predictions,path = f"s3://{bucket_name}/models/inference_data_outputs/{model_name}.parquet")

            print(f"Predictions for {model_name} stored successfully")
            df_predictions["region"] = model_name.split('extra_trees_')[1].split('.parquet')[0]

            # Create a weekly relative traffic column with sklearn min-max scaling
            scaler = MinMaxScaler()
            df_predictions['weekly_relative_traffic'] = scaler.fit_transform(df_predictions[['predictions']])

            # Create a new column for color coding based on traffic thresholds
            df_predictions['traffic_color'] = df_predictions['weekly_relative_traffic'].apply(
                lambda x: 'red' if x > 0.40 else 'green' if x < 0.05 else 'blue'
            )

            # Append the predictions to the overall_predictions DataFrame
            overall_predictions = pd.concat([overall_predictions, df_predictions])

        else:
           print(f"Error: {model_name} is not a valid model. It is of type {type(model)}")
    
    return overall_predictions

def visitor_predictions(inference_data):

    loaded_models = load_latest_models(bucket_name, folder_prefix, model_names)

    print("Models loaded successfully")
    
    overall_inference_predictions = predict_with_models(loaded_models, inference_data)

    # Convert the 'Time' column to datetime format
    overall_inference_predictions['Time'] = pd.to_datetime(overall_inference_predictions['Time'], errors='coerce')

    # Get the days from the values (dates) in the 'Time' column
    overall_inference_predictions['day'] = overall_inference_predictions['Time'].dt.day_name()

    # Create a new column to combine both date and day for radio buttons
    overall_inference_predictions['day_date'] = overall_inference_predictions['Time'].dt.strftime('%A, %d %b %Y')

    return overall_inference_predictions

