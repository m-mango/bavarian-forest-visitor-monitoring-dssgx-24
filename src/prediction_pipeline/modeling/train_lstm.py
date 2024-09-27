# Import necessary libraries
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Bidirectional, Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split

def load_data():
    """
    Load preprocessed data from the feature_selection_and_preprocessing module.
    Returns:
        df (pd.DataFrame): The preprocessed dataframe with features and target variables.
    """
    from feature_selection_and_preprocessing import get_preprocessed_data
    return get_preprocessed_data()

def split_features_targets(df, target_vars):
    """
    Split the dataframe into features and target variables.

    Parameters:
        df (pd.DataFrame): The dataframe with features and target variables.
        target_vars (list): List of target variable column names.

    Returns:
        X (np.ndarray): Feature array.
        y (np.ndarray): Target variable array.
    """
    X = df.drop(columns=target_vars).values  # Features
    y = df[target_vars].values  # Target variables
    return X, y

def split_train_test(X, y, test_size=0.1):
    """
    Split data into training and test sets.

    Parameters:
        X (np.ndarray): Feature array.
        y (np.ndarray): Target variable array.
        test_size (float): Proportion of the dataset to include in the test split.

    Returns:
        X_train (np.ndarray): Training features.
        X_eval (np.ndarray): Evaluation features.
        y_train (np.ndarray): Training targets.
        y_eval (np.ndarray): Evaluation targets.
    """
    return train_test_split(X, y, test_size=test_size, shuffle=False)

def create_sequences(X, y, window_size):
    """
    Create sequences from the data for LSTM input.

    Parameters:
        X (np.ndarray): Feature array.
        y (np.ndarray): Target variable array.
        window_size (int): The number of time steps to include in each sequence.

    Returns:
        X_seq (np.ndarray): Sequence features.
        y_seq (np.ndarray): Sequence targets.
    """
    X_seq, y_seq = [], []
    for i in range(len(X) - window_size):
        X_seq.append(X[i:i + window_size])
        y_seq.append(y[i + window_size])
    return np.array(X_seq), np.array(y_seq)

def build_lstm_model(input_shape, output_size):
    """
    Build and compile the LSTM model.

    Parameters:
        input_shape (tuple): Shape of the input data (time_steps, features).
        output_size (int): Number of target variables.

    Returns:
        model (tensorflow.keras.Model): Compiled LSTM model.
    """
    model = Sequential()
    model.add(Input(shape=input_shape))
    model.add(Bidirectional(LSTM(128, return_sequences=True)))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(64)))
    model.add(Dropout(0.3))
    model.add(Dense(output_size))  # Output layer with the number of target variables
    model.compile(optimizer='adam', loss='mse')
    return model

def train_model(model, X_train_seq, y_train_seq, epochs=50, batch_size=64):
    """
    Train the LSTM model.

    Parameters:
        model (tensorflow.keras.Model): The compiled LSTM model.
        X_train_seq (np.ndarray): Training sequence features.
        y_train_seq (np.ndarray): Training sequence targets.
        epochs (int): Number of epochs to train the model.
        batch_size (int): Batch size for training.

    Returns:
        history (tensorflow.keras.callbacks.History): Training history.
    """
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    history = model.fit(X_train_seq, y_train_seq, epochs=epochs, batch_size=batch_size, validation_split=0.1, callbacks=[early_stopping])
    return history

def save_model(model, model_path='lstm_model.h5'):
    """
    Save the trained model to a file.

    Parameters:
        model (tensorflow.keras.Model): The trained LSTM model.
        model_path (str): Path to save the model file.
    """
    model.save(model_path)

# Main function to execute the training pipeline
def training_pipeline():
    """
    Main function to execute the training pipeline for the LSTM model.
    """
    # Load preprocessed data
    df = load_data()

    # Define target variables
    target_vars = ['traffic_abs', 'sum_IN_abs', 'sum_OUT_abs', 
                   'Lusen-Mauth-Finsterau IN', 'Lusen-Mauth-Finsterau OUT', 
                   'Falkenstein-Schwellhäusl IN', 'Falkenstein-Schwellhäusl OUT', 
                   'Rachel-Spiegelau IN', 'Rachel-Spiegelau OUT',  
                   'Nationalparkzentrum Lusen IN', 'Nationalparkzentrum Lusen OUT', 
                   'Scheuereck-Schachten-Trinkwassertalsperre IN', 
                   'Scheuereck-Schachten-Trinkwassertalsperre OUT', 
                   'Nationalparkzentrum Falkenstein IN', 'Nationalparkzentrum Falkenstein OUT']

    # Split features and target variables
    X, y = split_features_targets(df, target_vars)

    # Split into training and evaluation sets
    X_train, X_eval, y_train, y_eval = split_train_test(X, y)

    # Create sequences
    window_size = 168  # 7 days, assuming data is hourly
    X_train_seq, y_train_seq = create_sequences(X_train, y_train, window_size)
    X_eval_seq, y_eval_seq = create_sequences(X_eval, y_eval, window_size)

    # Build the LSTM model
    input_shape = (X_train_seq.shape[1], X_train_seq.shape[2])
    output_size = y_train_seq.shape[1]
    model = build_lstm_model(input_shape, output_size)

    # Train the model
    train_model(model, X_train_seq, y_train_seq)

    # Save the trained model
    save_model(model)

# Execute the training pipeline
if __name__ == "__main__":
    training_pipeline()
