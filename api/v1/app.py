#!/usr/bin/python3

""" App controller module """
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from flask_cors imort CORS
from os import getenv
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
CROS(app, resources={r"/*": {"origins": "0.0.0.0"}}


@app.teardown_appcontext
def teardown(exception):
    """ calls the storage.close functionality """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """ returns a Jsonify not found error """
    return make_response(jsonify(error="Not found"), 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
