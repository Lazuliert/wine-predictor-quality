import pandas as pd
import os
import validators
from wine_predictor_api import logger, api_config
from sklearn.metrics import mean_squared_error
import joblib

def load_data():
    data_dir_path = api_config.get("data", {}).get("path")
    if not validators.url(data_dir_path) and os.path.isifle(data_dir_path):
        raise FileNotFoundError("Data path could not be found")
    return pd.read_csv(data_dir_path)

def evaluate_model(model, test_data, test_target):
    logger.debug("Evaluation model...")
    y_predicted = model.predict(test_data)
    mse = mean_squared_error(y_predicted, test_target)
    return mean_squared_error

def save_model(model, output_path):
    logger.debug(f"Saving model in {output_path}")
    return joblib.dump(model, output_path)

def train_model():
    pass