from typing import Tuple
from wine_predictor_api import logger

#logger.debug("Writing for accountability ...")
#logger.info("Just an information ...")
#logger.error("An error occurred ...")

def ping() -> Tuple:
    return "pong", 200