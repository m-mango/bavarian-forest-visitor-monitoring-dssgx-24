#from base_inference_df import source_preprocess_inference_data
import boto3
import pickle
# Initialize S3 client
s3 = boto3.client('s3')


# Your AWS bucket and folder details where models are stored
bucket_name = 'dssgx-munich-2024-bavarian-forest'
folder_prefix = 'models/models_trained/'  # If you have a specific folder


target_vars_et  = ['traffic_abs', 'sum_IN_abs', 'sum_OUT_abs', 'Lusen-Mauth-Finsterau IN', 'Lusen-Mauth-Finsterau OUT', 
               'Nationalparkzentrum Lusen IN', 'Nationalparkzentrum Lusen OUT', 'Rachel-Spiegelau IN', 'Rachel-Spiegelau OUT', 'Falkenstein-Schwellhäusl IN', 'Falkenstein-Schwellhäusl OUT',             'Scheuereck-Schachten-Trinkwassertalsperre IN', 'Scheuereck-Schachten-Trinkwassertalsperre OUT', 
               'Nationalparkzentrum Falkenstein IN', 'Nationalparkzentrum Falkenstein OUT']


#models_names = ["extra_trees_" + model for model in target_vars_et]

models_names = ["extra_trees_Falkenstein-Schwellhäusl IN.pkl"]

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

    # Loop through each model to get the latest file
    for model in models_names:
        # List objects in the S3 bucket with the model prefix
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix + model)
        #print(response)
        if 'Contents' in response:
            # Sort files by LastModified to get the latest file
            files = sorted(response['Contents'], key=lambda x: x['LastModified'], reverse=True)
            latest_file = files[0]['Key']  # Get the key (file path) of the latest file
            
            obj = s3.get_object(Bucket=bucket_name, Key=latest_file)
            model_data_binary = obj['Body'].read()

            # Unpickle the binary data
            model_data = pickle.loads(model_data_binary)

            # Dynamically create variables with 'loaded_' prefix
            loaded_models[f"loaded_{model}"] = model_data

    print(loaded_models)
    return loaded_models


import pandas as pd
from pycaret.classification import load_model, predict_model  # Change to regression if needed




# Initialize an empty DataFrame for predictions
predictions_df = pd.DataFrame()


def make_predictions(models_names, inference_df):
    """
    Makes predictions using a list of PyCaret models on the given inference DataFrame.
    
    Parameters:
    models_names (list): A list of model names (strings) corresponding to the saved models.
    inference_df (pd.DataFrame): The DataFrame containing the data for which predictions are to be made.
    
    Returns:
    pd.DataFrame: A DataFrame containing the original inference data along with predictions from each model.
    """
    # Initialize an empty DataFrame for predictions
    predictions_df = pd.DataFrame()

    # Loop through each model, make predictions, and store them
    for model_name in models_names:
        model = load_model(model_name)
        preds = predict_model(model, data=inference_df)
        pred_col_name = f'Prediction_{model_name}'
        predictions_df[pred_col_name] = preds['Label']  # Use 'Score' for regression models

    # Concatenate predictions with the original inference DataFrame
    final_df = pd.concat([inference_df, predictions_df], axis=1)
    
    return final_df


def main():
    load_latest_models(bucket_name, folder_prefix, models_names)


if __name__ == "__main__":
    main()