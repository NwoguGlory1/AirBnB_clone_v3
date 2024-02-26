#!/usr/bin/python3
""" App controller module """

from flask import Flask
from api.v1.views import app_views
from os import getenv
from models import storage

app = Flask(__name__)
""" Creates an instance of class, Flask"""

app.register_blueprint(app_views)
""" registers the blueprint to app """


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


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
