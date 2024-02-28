#!/usr/bin/python3
""" App controller module """

from flask import Flask, jsonify, make_response
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv
from models import storage

app = Flask(__name__)
""" Creates an instance of class, Flask"""

app.register_blueprint(app_views)
""" registers the blueprint to app """
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """ calls the storage.close functionality """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Function to handle the error
    Returns  a JSON response, jsonify converts dictionary,
    "error": "Not found" into a JSON response
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def other_400_error(error):
    """
    Function to handle other custom 400 errors
    Returns a JSON response, jsonify converts dictionary
    """
    return make_response(jsonify({"error": error.description}), 400)

if __name__ == '__main__':
    """ Ensures that code runs only when executed directly """
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
