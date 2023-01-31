import pandas as pd
import os
import validators
from wine_predictor_api import logger, api_config
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import joblib
import math

def load_data():
    data_dir_path = api_config.get("data", {}).get("path")
    logger.debug(f"data pth  = {data_dir_path}")
    if not validators.url(data_dir_path) and os.path.isfile(data_dir_path):
        raise FileNotFoundError("Data path could not be found")
    return pd.read_csv(data_dir_path)

def evaluate_model(model, test_data, test_target):
    logger.debug("Evaluation model...")
    y_predicted = model.predict(test_data)
    mse = mean_squared_error(y_predicted, test_target)
    return mse

def save_model(model, output_path):
    logger.debug(f"Saving model in {output_path}")
    return joblib.dump(model, output_path)

def train_model():
    try:
        dataset = load_data()
    except FileNotFoundError as fnf:
        logger.error(f"File not found error raise. {str(fnf)}")
        return "File not found", 404
    target = dataset['TARGET']
    features = dataset.drop('TARGET', axis=1)
    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=0)

    linear_model = LinearRegression()
    linear_model.fit(x_train, y_train)

    mse_old = math.inf
    mse_new = evaluate_model(model=linear_model, test_data=x_test, test_target=y_test)
    logger.debug(f"mse: {mse_new}")

    save_model(model=linear_model, output_path=api_config.get("model", {}).get("path"))
    return "New model have been sccessully trained", 201