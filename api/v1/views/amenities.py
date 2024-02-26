#!/usr/bin/python3
""" State view object that handles all default RESTFul API actions """

from flask import Flask, make_response, jsonify, abort, request
from models import storage
from models.amenity import Amenity
from . import app_views


def to_dict(obj):
    """ retrieves an object into a valid JSON """
    return obj.to_dict()


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ retrieves the list of all amenity objects """
    all_amenities = storage.all(Amenity)
    ret_amenities = []
    for amenity in all_amenities.values():
        amemity_dic = to_dict(amenity)
        ret_amenities.append(amenity_dic)
    return jsonify(ret_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ retreives an amenity with the amenity_id """
    ret_amenity = storage.get(Amenity, amenity_id)
    if ret_amenity is None:
        abort(404)
    return jsonify(to_dict(ret_amenity))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(state_id):
    """ deletes an amenity with the given amenity_id """
    ret_amenity = storage.get(Amenity, amenity_id)
    if ret_amenity is None:
        abort(404)
    storage.delete(ret_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_new_amenity():
    """ adds a new amenity with amenity name """
    add_amenity = request.get_json()
    if not add_amenity:
        abort(400, "Not a JSON")
    elif 'name' not in add_amenity:
        abort(400, "Missing Name")
    else:
        new_amenity = Amenity(**add_amenity)
        storage.new(new_amenity)
        storage.save()
        return jsonify(to_dict(new_amenity)), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ updates an amenity value of a given amenity id """
    ret_amenity = storage.get(Amenity, amenity_id)
    if ret_amenity is None:
        abort(404)
    put_data = request.get_json()
    if not put_data:
        abort(400, "Not a JSON")
    put_data.pop('id', None)
    put_data.pop('created_at', None)
    put_data.pop('updated_at', None)

    for key, value in put_data.items():
        setattr(ret_amenity, key, value)
    storage.save()
    return jsonify(to_dict(ret_amenity)), 200
