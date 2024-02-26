#!/usr/bin/python3
""" Script for the index of the API""" 

from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def get_status():
    """
    Function that executes if user accesses '/status'
    """
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """ Function that executes if user accesses '/stats'"""
    objects = {
            'amenities': Amenity,
            'cities': City,
            'places': Place,
            'reviews': Review,
            'states': State,
            'users': User
            }
    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)
