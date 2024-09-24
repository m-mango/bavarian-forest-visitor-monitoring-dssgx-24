from src.prediction_pipeline.base_inference_df import source_preprocess_inference_data


#bring model from aws





def generate_forecasts_for_targets(inference_df, target_vars, model_path):
    """
    Generate forecasts for each target variable using corresponding models.

    Parameters:
    - inference_df: DataFrame containing features for predictions.
    - target_vars: List of target variables.
    - model_path: Path to save and load models.

    Returns:
    - forecasts_dict: Dictionary containing DataFrames with predictions for each target variable.
    """
    forecasts_dict = {}

    for target in target_vars:
        if target in inference_df.columns:
            # Create a copy of inference_df for the current target variable
            current_df = inference_df.copy()

            # Load the corresponding model for the target variable
            model = load_model(f"{model_path}/extra_trees_{target}")

            # Generate predictions using the model
            predictions = predict_model(model, data=current_df)

            # Store the predictions in the DataFrame
            current_df['predicted_' + target] = predictions['prediction_label']

            # Store the DataFrame in the dictionary
            forecasts_dict[target] = current_df

            print(f"Forecasts for target variable '{target}' added to DataFrame.")
        else:
            print(f"Target variable '{target}' is not in the inference DataFrame.")
    
    return forecasts_dict

forecasts = generate_forecasts_for_targets(inference_df, target_vars_et, save_path)