#!/usr/bin/python3

""" module returns a JSON structure """
from flask import jsonify
from . import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ returns JSON status """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Returns the statistics of objects in JSON format """
    objs = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']

    objs_stat = {}

    for obj in objs:
        objs_stat[obj] = storage.count(obj)
    return jsonify(**objs_stat)
