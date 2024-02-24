from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
jsonify

app = Flask(__name__)
""" Creates an instance of class, Flask"""

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Function to handle the teardown, to close the SQLAchemy session
    after each request.
    """
    storage.close()


if __name__ == '__main__':
    """
    Ensures script runs only when excuted directly,
    not when imported as a module in another script.
    """
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
