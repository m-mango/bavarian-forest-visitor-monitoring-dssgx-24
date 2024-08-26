import pandas as pd
import logging
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Set up logging
logging.basicConfig(level=logging.INFO)

def load_raw_data(file_path):
    try:
        data = pd.read_csv(file_path, parse_dates=['Time'], index_col='Time')
        logging.info(f"Raw data loaded successfully from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Failed to load raw data: {e}")
        raise

def preprocess_data(data):
    try:
        # 1. Drop the unnecessary columns
        columns_to_drop = [
            "Besuchszahlen_HEH", "Besuchszahlen_HZW", "Besuchszahlen_WGM", 
            "Parkpl_HEH_PKW", "Parkpl_HEH_BUS", "Parkpl_HZW_PKW", 
            "Parkpl_HZW_BUS", "Temperatur", "Niederschlagsmenge"
        ]
        data = data.drop(columns=columns_to_drop)
        logging.info(f"Dropped unnecessary columns: {columns_to_drop}")

        # 2. Identify categorical and continuous columns
        categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
        continuous_columns = data.select_dtypes(include=['float64', 'int64']).columns.tolist()

        # 3. Pipeline for categorical and continuous features
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),  # Handle missing values
            ('onehot', OneHotEncoder(handle_unknown='ignore'))     # One-Hot Encode
        ])

        continuous_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),           # Handle missing values
            ('scaler', StandardScaler())                           # Normalize
        ])

        # 4. Combine transformers into a preprocessor
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_columns),
                ('num', continuous_transformer, continuous_columns)
            ])

        # 5. Apply transformations
        data_transformed = preprocessor.fit_transform(data)

        # 6. Convert back to DataFrame
        transformed_columns = (
            preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_columns).tolist() +
            continuous_columns
        )
        data_transformed = pd.DataFrame(data_transformed, columns=transformed_columns, index=data.index)

        logging.info("Data preprocessing completed successfully")
        return data_transformed

    except Exception as e:
        logging.error(f"Failed to preprocess data: {e}")
        raise

def main():
    # Load the raw data
    raw_data_path = 'data/cleaned_data/merged_sensor_data.csv'
    data = load_raw_data(raw_data_path)

    # Preprocess the data
    cleaned_data = preprocess_data(data)

    return cleaned_data

if __name__ == "__main__":
    main()
