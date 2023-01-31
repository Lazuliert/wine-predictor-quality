export FLASK_APP="wine_predictor_api:create_app"
export FLASK_DEBUG=true
PORT=5000

py -m flask run -h 0.0.0.0 -p $PORT
