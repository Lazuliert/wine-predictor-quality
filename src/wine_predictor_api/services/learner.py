import os
import pandas as pd
import validators
from wine_predictor_api import logger, api_config
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import joblib
import math


def load_data():
    """
    Load Dataset

    :return:
    """
    logger.debug(f"Loading dataset ...")
    data_dir_path = api_config.get("data", {}).get("path")
    if not validators.url(data_dir_path) and not os.path.isfile(data_dir_path):
        raise FileNotFoundError("Data path could not be found")

    return pd.read_csv(data_dir_path)


def load_model():
    """
    Load Model

    :return:
    """
    logger.debug(f"Loading model ...")
    model_dir_path = api_config.get("model", {}).get("path")
    if not validators.url(model_dir_path) and not os.path.isfile(model_dir_path):
        raise FileNotFoundError("Model path could not be found")

    return joblib.load(model_dir_path)


def evaluate_model(model, test_data, test_target):
    """
    Evaluate the model performance on the given test data

    :param model:
    :param test_data:
    :param test_target:

    :return:
    """
    logger.debug(f"Evaluation model ...")
    y_predicted = model.predict(test_data)
    mse = mean_squared_error(y_predicted, test_target)
    return mse


def save_model(model, output_path):
    """
    Save the model on the given output path

    :param model:
    :param output_path:
    :return:
    """
    logger.debug(f"Saving model in {output_path}...")
    return joblib.dump(model, output_path)


def train_model():
    """
    Train model from data

    :return:
    """
    # load data
    try:
        dataset = load_data()
    except FileNotFoundError as fnf:
        logger.error(f"File not Found error raised. {str(fnf)} ")
        return "File not found", 404

    # Preparing the data (split data ... )
    target = dataset['TARGET']
    features = dataset.drop('TARGET', axis=1)
    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=0)

    # Train the model
    linear_model = LinearRegression()
    linear_model.fit(x_train, y_train)

    # Evaluate the performance of the model
    mse_old = math.inf
    mse_new = evaluate_model(model=linear_model, test_data=x_test, test_target=y_test)
    logger.debug(f"mse: {mse_new}")

    # Evaluate performance of existing model (if any)
    try:
        existing_model = load_model()
        mse_old = evaluate_model(model=existing_model, test_data=x_test, test_target=y_test)
    except FileNotFoundError as fnf:
        logger.error(f"File not Found error raised. {str(fnf)} ")

    # Save the model if efficient
    if mse_new < mse_old:
        save_model(model=linear_model, output_path=api_config.get("model", {}).get("path"))
        # Return status and description
        return "New model has been successfully trained and saved as default", 201
    else:
        #  In case  the performance is less than existing, discard it
        return "New model has been successfully trained but discarded", 200