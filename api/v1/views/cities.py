#!/usr/bin/python3
""" City view object that handles all default RESTFul API actions """

from flask import Flask, make_response, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from . import app_views


def to_dict(obj):
    """ retrieves an object into a valid JSON """
    return obj.to_dict()


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ retrieves the list of all cities object of a state """
    ret_state = storage.get(State, state_id)
    if ret_state is None:
        abort(404)
    cities = []
    for city in ret_state.cities:
        cities_dic = to_dict(city)
        cities.append(cities_dic)
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ retreives a city with the city_id """
    ret_city = storage.get(City, city_id)
    if ret_city is None:
        abort(404)
    return jsonify(to_dict(ret_city))


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ deletes a city with the given state_id """
    ret_city = storage.get(City, city_id)
    if ret_city is None:
        abort(404)
    storage.delete(ret_city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def add_new_city(state_id):
    """ adds a new city to the given state_id """
    ret_state = storage.get(State, state_id)
    if ret_state is None:
        abort(404)
    add_city = request.get_json()
    if not add_city:
        abort(400, "Not a JSON")
    elif 'name' not in add_city:
        abort(400, "Missing Name")
    else:
        new_city = City(**add_city)
        setattr(new_city, "state_id", state_id)
        storage.new(new_city)
        storage.save()
        return jsonify(to_dict(new_city)), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_cities(city_id):
    """ updates a city value of a given city id """
    ret_city = storage.get(City, city_id)
    if ret_city is None:
        abort(404)
    put_data = request.get_json()
    if not put_data:
        abort(400, "Not a JSON")
    put_data.pop('id', None)
    put_data.pop('created_at', None)
    put_data.pop('updated_at', None)
    put_data.pop('state_id', None)

    for key, value in put_data.items():
        setattr(ret_city, key, value)
    storage.save()
    return jsonify(to_dict(ret_state)), 200
