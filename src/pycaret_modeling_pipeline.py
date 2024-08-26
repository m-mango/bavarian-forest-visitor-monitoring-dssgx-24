import logging
from pycaret.time_series import setup, compare_models, pull, finalize_model, predict_model, save_model, load_model
from preprocessing import main as preprocess_data  # Importing the preprocessing function

# Set up logging
logging.basicConfig(level=logging.INFO)

def setup_pycaret_environment(data):
    """
    Initialize the PyCaret environment for time series forecasting.
    
    :param data: The dataset as a Pandas DataFrame.
    :return: PyCaret's setup object for further processing.
    """
    try:
        exp = setup(
            data=data, 
            target='target',  # Your target column (visitor counts)
            session_id=123, 
            fold=2,           # Number of cross-validation folds
            fh=168,           # Forecast horizon (168 hours = 1 week)
            seasonal_period=24 # Seasonal period (daily seasonality for hourly data)
        )
        logging.info("PyCaret environment setup completed successfully")
        return exp
    except Exception as e:
        logging.error(f"Failed to set up PyCaret environment: {e}")
        raise

def train_and_save_model():
    """
    Trains the best model based on the comparison and saves the final model.

    Models to be included in comparison:
    - 'arima': Autoregressive Integrated Moving Average, good for univariate time series data.
    - 'prophet': A model designed by Facebook for forecasting time series data with strong seasonal effects.
    - 'xgboost': An efficient and flexible gradient boosting algorithm (may need to be excluded if not supported).
    - 'sarima': Seasonal ARIMA, which extends ARIMA by considering seasonality.
    - 'ets': Error, Trend, Seasonality model, another approach for forecasting.

    Logs and displays the performance of each model.
    """
    try:
        # Get the preprocessed data from the preprocessing script
        data = preprocess_data()  # This replaces the previous load_data function

        # Set up the environment
        setup_pycaret_environment(data)

        # Compare models and log the performance of each model
        best_model = compare_models(include=['arima', 'prophet', 'auto_arima'], n_select=1)
        logging.info(f"Best model: {best_model}")

        
        # Pulling the comparison results as a DataFrame
        results_df = pull()
        logging.info("Model comparison completed. Here are the results:")
        logging.info(f"\n{results_df}")
        
        # Display the comparison results as a table
        print("\nModel Comparison Results:\n")
        print(results_df)
        
        # Log the best model
        logging.info(f"Best model: {best_model}")

        # Finalize the model (retrain on the full dataset)
        final_model = finalize_model(best_model)

        # Save the model to a file
        save_model(final_model, 'best_time_series_model')
        logging.info("Model training and saving completed successfully")
        
    except Exception as e:
        logging.error(f"Failed to train the model: {e}")
        raise

def make_predictions():
    """
    Load the saved model and make predictions for the next 168 hours.
    """
    try:
        # Load the saved model
        model = load_model('best_time_series_model')
        logging.info("Model loaded successfully")

        # Get the preprocessed data from the preprocessing script (if needed for prediction)
        data = preprocess_data()

        # Generate predictions for the next 168 hours
        future_predictions = predict_model(model, fh=168)

        # Print or save predictions
        future_predictions.to_csv('output/future_predictions.csv')
        logging.info("Predictions generated and saved to future_predictions.csv")
        print(future_predictions.head())
        
    except Exception as e:
        logging.error(f"Failed to make predictions: {e}")
        raise

def main():
    train_and_save_model()
    make_predictions()

if __name__ == "__main__":
    main()
