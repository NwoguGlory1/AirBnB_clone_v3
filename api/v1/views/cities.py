#!/usr/bin/python3
""" Contains the cities view for the API """

from flask import jsonify, abort, request
from models import storage
from models.city import City
from api.v1.views import app_views

states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    """Retrieves the list of all City objects of a State"""
    cities = storage.all(City).State.values()
    return jsonify([city.to_dict() for city in city.states])

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city()
    """Creates a City object."""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201
