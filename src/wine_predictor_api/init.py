import connexion
from wine_predictor_api import specs


def create_app():
    app = connexion.FlaskApp(__name__, specification_dir=specs.where())
    app.add_api("openapi_spec.yaml")
    return app.app