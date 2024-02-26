#!/usr/bin/python3
""" City view object that handles all default RESTFul API actions """

from flask import Flask, make_response, jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from . import app_views


def to_dict(obj):
    """ retrieves an object into a valid JSON """
    return obj.to_dict()


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(state_id):
    """ retrieves the list of all place object of a city """
    ret_city = storage.get(City, city_id)
    if ret_city is None:
        abort(404)
    places = []
    for place in ret_city.places:
        places_dic = to_dict(place)
        places.append(places_dic)
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ retreives a place with the place_id """
    ret_place = storage.get(Place, place_id)
    if ret_place is None:
        abort(404)
    return jsonify(to_dict(ret_place))


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ deletes a place with the given place_id """
    ret_place = storage.get(Place, place_id)
    if ret_place is None:
        abort(404)
    storage.delete(ret_place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def add_new_place(city_id):
    """ adds a new place to the given city_id """
    ret_city = storage.get(City, city_id)
    if ret_city is None:
        abort(404)
    add_place = request.get_json()
    user = storage.get(User, add_place['user_id'])
    if not add_place:
        abort(400, "Not a JSON")
    elif not user:
        abort(404)
    elif 'name' not in add_place:
        abort(400, "Missing name")
    elif 'user_id' not in add_place:
        abort(400, "Missing user_id")
    else:
        new_place = Place(**add_place)
        setattr(new_place, "city_id", state_id)
        storage.new(new_city)
        storage.save()
        return jsonify(to_dict(new_city)), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_places(place_id):
    """ updates a place value of a given place id """
    ret_place = storage.get(Place, place_id)
    if ret_place is None:
        abort(404)
    put_data = request.get_json()
    if not put_data:
        abort(400, "Not a JSON")

    for key, value in put_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(ret_place, key, value)
    storage.save()
    return jsonify(to_dict(ret_place)), 200
