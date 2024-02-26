#!/usr/bin/python3
""" State view object that handles all default RESTFul API actions """

from flask import Flask, make_response, jsonify, abort, request
from models import storage
from models.user import User
from . import app_views


def to_dict(obj):
    """ retrieves an object into a valid JSON """
    return obj.to_dict()


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ retrieves the list of all users objects """
    all_users = storage.all(User)
    ret_user = []
    for user in all_users.values():
        user_dic = to_dict(user)
        ret_user.append(user_dic)
    return jsonify(ret_user)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ retreives a user with the user_id """
    ret_user = storage.get(User, user_id)
    if ret_user is None:
        abort(404)
    return jsonify(to_dict(ret_user))


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ deletes a user with the given user_id """
    ret_user = storage.get(User, user_id)
    if ret_user is None:
        abort(404)
    storage.delete(ret_user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_new_user():
    """ adds a new user using with user name """
    add_user = request.get_json()
    if not add_user:
        abort(400, "Not a JSON")
    elif 'name' not in add_user:
        abort(400, "Missing Name")
    else:
        new_user = User(**add_user)
        storage.new(new_user)
        storage.save()
        return jsonify(to_dict(new_user)), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ updates a user value of a given user id """
    ret_user = storage.get(User, user_id)
    if ret_user is None:
        abort(404)
    put_data = request.get_json()
    if not put_data:
        abort(400, "Not a JSON")
    put_data.pop('id', None)
    put_data.pop('created_at', None)
    put_data.pop('updated_at', None)

    for key, value in put_data.items():
        setattr(ret_state, key, value)
    storage.save()
    return jsonify(to_dict(ret_user)), 200
