"""
This script creates a dictionary with predictions for the selected models. 

This needs to load the models from AWS and train on an inference df that is generated from the source_preprocess_inference_data function. This last function is in base_inference_df.py and seems to be working fine.

1. """



#from base_inference_df import source_preprocess_inference_data
import boto3
import pickle
import pandas as pd
from pycaret.regression import load_model, predict_model  # Change to regression if needed
from base_inference_df import source_preprocess_inference_data
# Initialize S3 client
s3 = boto3.client('s3')


# Your AWS bucket and folder details where models are stored
bucket_name = 'dssgx-munich-2024-bavarian-forest'
folder_prefix = 'models/models_trained/b6d6d8dc-9cd7-4213-a1d1-d567170ccdd7/'  # If you have a specific folder


target_vars_et  = ['traffic_abs', 'sum_IN_abs', 'sum_OUT_abs', 'Lusen-Mauth-Finsterau IN', 'Lusen-Mauth-Finsterau OUT', 
               'Nationalparkzentrum Lusen IN', 'Nationalparkzentrum Lusen OUT', 'Rachel-Spiegelau IN', 'Rachel-Spiegelau OUT', 'Falkenstein-Schwellhäusl IN', 'Falkenstein-Schwellhäusl OUT',             'Scheuereck-Schachten-Trinkwassertalsperre IN', 'Scheuereck-Schachten-Trinkwassertalsperre OUT', 
               'Nationalparkzentrum Falkenstein IN', 'Nationalparkzentrum Falkenstein OUT']


#models_names = ["extra_trees_" + model for model in target_vars_et]

models_names = ["extra_trees_Falkenstein-Schwellhäusl IN"]

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
        
        print(type(saved_lr))
        print(saved_lr)





def predict_with_models(loaded_models, df_features):
    """
    Given a dictionary of models and a DataFrame of features, this function predicts the target
    values using each model and stores the results in a dictionary of DataFrames.
    
    Parameters:
    - loaded_models (dict): A dictionary of models where keys are model names and values are the trained models.
    - df_features (pd.DataFrame): A DataFrame containing the features to make predictions on.

    Returns:
    - dict: A dictionary where keys are model names and values are DataFrames containing the predictions.
    """
    # Initialize an empty dictionary to store DataFrames
    prediction_dfs = {}

    # Iterate through the loaded models
    for model_name, model in loaded_models.items():
        # Check if the model has a predict method
        if hasattr(model, 'predict'):
            # Make predictions
            predictions = model.predict(df_features)
            
            # Create a new DataFrame for the predictions
            df_predictions = pd.DataFrame(predictions, columns=[f'{model_name}_predictions'])
            
            # Store the DataFrame in the dictionary
            prediction_dfs[model_name] = df_predictions
        #else:
           # print(f"Error: {model_name} is not a valid model. It is of type {type(model)}")

    return prediction_dfs

def main():
    load_latest_models(bucket_name, folder_prefix, models_names)
    
    #inference_data = source_preprocess_inference_data()
    
    #prediction_dfs = predict_with_models(loaded_models, inference_data)
    #print(prediction_dfs)

if __name__ == "__main__":
    main()