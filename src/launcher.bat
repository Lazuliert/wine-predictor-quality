SET FLASK_APP="wine_predictor_api:create_app"
SET FLASK_DEBUG=true

py -m flask run -h 0.0.0.0 -p 5000