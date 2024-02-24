from flask import jsonify
from models import storage
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def get_status():
    """
    Function that executes if user accesses '/status'
    """
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    stats = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }