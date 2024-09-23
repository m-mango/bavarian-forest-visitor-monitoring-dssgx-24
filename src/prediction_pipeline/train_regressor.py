import pandas as pd
from source_and_feature_selection import get_features
from pycaret import *
from pycaret.time_series import *
from pycaret.regression import *
import os
import awswrangler as wr


save_path_models = 'models/models_trained/'
save_path_predictions = 'models/inference_data_outputs/'
local_path = os.path.join('outputs','models_trained')
bucket_name = 'dssgx-munich-2024-bavarian-forest'

# Define target columns
target_vars_et  = ['traffic_abs', 'sum_IN_abs', 'sum_OUT_abs', 'Lusen-Mauth-Finsterau IN', 'Lusen-Mauth-Finsterau OUT', 
               'Nationalparkzentrum Lusen IN', 'Nationalparkzentrum Lusen OUT', 'Rachel-Spiegelau IN', 'Rachel-Spiegelau OUT', 
               'Falkenstein-Schwellhäusl IN', 'Falkenstein-Schwellhäusl OUT', 
               'Scheuereck-Schachten-Trinkwassertalsperre IN', 'Scheuereck-Schachten-Trinkwassertalsperre OUT', 
               'Nationalparkzentrum Falkenstein IN', 'Nationalparkzentrum Falkenstein OUT']

numeric_features = ['Temperature (°C)', 'Relative Humidity (%)', 'Wind Speed (km/h)', 'ZScore_Daily_Max_Temperature (°C)', 
                    'ZScore_Daily_Max_Relative Humidity (%)','ZScore_Daily_Max_Wind Speed (km/h)',
                    'Distance_to_Nearest_Holiday_Bayern','Distance_to_Nearest_Holiday_CZ','Tag_sin', 'Tag_cos', 'Monat_sin', 'Monat_cos',
                    'Hour_sin', 'Hour_cos','Wochentag_sin', 'Wochentag_cos']

categorical_features = ['Wochenende','Laubfärbung', 'Schulferien_Bayern', 'Schulferien_CZ', 
                        'Feiertag_Bayern', 'Feiertag_CZ', 'HEH_geoeffnet', 'HZW_geoeffnet', 'WGM_geoeffnet', 
                        'Lusenschutzhaus_geoeffnet', 'Racheldiensthuette_geoeffnet', 'Falkensteinschutzhaus_geoeffnet', 
                        'Schwellhaeusl_geoeffnet','sunny', 'cloudy', 'rainy', 'snowy', 'extreme','stormy','Frühling',
                        'Sommer', 'Herbst', 'Winter']



def save_predictions_to_aws_s3(df: pd.DataFrame, save_path_predictions: str, filename: str) -> pd.DataFrame:
    """Writes an individual CSV file to AWS S3.

    Args:
        df (pd.DataFrame): The DataFrame to write.
        path (str): The path to the CSV files on AWS S3.
        **kwargs: Additional arguments to pass to the to_csv function.
    """

    wr.s3.to_parquet(df, path=f"s3://{bucket_name}/{save_path_predictions}{filename}",index= True)
    return

def save_models_to_aws_s3(model, save_path_models, model_name, local_path):
    """Save the model to AWS S3

    Args:
        model: The model to save

    Returns:
        None
    """

    # make the save path if it does not exist
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    save_model_path = os.path.join(local_path, model_name)
    save_model(model, save_model_path)

    save_path_aws = os.path.join(f"s3://{bucket_name}/", save_path_models, f"{model_name}.pkl")

    wr.s3.upload(f"{save_model_path}.pkl",save_path_aws)
    return

def train_regressor():

    feature_dataframe = get_features()

    for target in target_vars_et:
        print(f"Training Extra Trees Regressor for {target}")
    
        # Ensure the DataFrame has a date-time index
        if isinstance(feature_dataframe.index, pd.DatetimeIndex):
            # Define date ranges for training, testing, and unseen data
            train_start = '2023-01-01'
            train_end = '2024-04-30'
            test_start = '2024-05-01'
            test_end = '2024-07-22'
                
            # Split the data into train, test, and unseen sets based on date ranges

            df_train = feature_dataframe[numeric_features+categorical_features+[target]].loc[train_start:train_end]
            df_test = feature_dataframe[numeric_features+categorical_features+[target]].loc[test_start:test_end]
 
            # Setup PyCaret for the target variable with the combined data
            reg_setup = setup(data=df_train,
                            target=target, 
                            numeric_features=numeric_features, 
                            categorical_features=categorical_features,
                            fold=5,
                            preprocess=False,
                            data_split_shuffle=False,  # Do not shuffle data to maintain date order
                            session_id=123,
                            train_size=0.9)  # Use 90% of data for training 
                
            # Train the Extra Trees Regressor model
            extra_trees_model = create_model('et')
                
            # Predict on the unseen data
            predictions = predict_model(extra_trees_model, data=df_test)
            
            # save the model in aws s3
            save_models_to_aws_s3(extra_trees_model, save_path_models, 
                                  f"extra_trees_{target}",local_path)
            print(f"Model with {target} saved to AWS S3")
            
            # save predictions to aws s3
            file_name = f"predictions_{target}.parquet"
            save_predictions_to_aws_s3(predictions, save_path_predictions,file_name)
            print(f"Predictions with {target} saved to AWS S3")
    return
if __name__ == "__main__":
    train_regressor()