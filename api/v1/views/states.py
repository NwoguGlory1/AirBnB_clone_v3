#!/usr/bin/python3
""" State view object that handles all default RESTFul API actions """

from flask import Flask, make_response, jsonify, abort, request
from models import storage
from models.state import State
from . import app_views


def to_dict(obj):
    """ retrieves an object into a valid JSON """
    return obj.to_dict()


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ retrieves the list of all state objects """
    all_states = storage.all(State)
    ret_state = []
    for state in all_states.values():
        state_dic = to_dict(state)
        ret_state.append(state_dic)
    return jsonify(ret_state)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ retreives a state with the state_id """
    ret_state = storage.get(State, state_id)
    if ret_state is None:
        abort(404)
    return jsonify(to_dict(ret_state))


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ deletes a state with the given state_id """
    ret_state = storage.get(State, state_id)
    if ret_state is None:
        abort(404)
    storage.delete(ret_state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_new_state():
    """ adds a new state using with state name """
    add_state = request.get_json()
    if not add_state:
        abort(400, "Not a JSON")
    elif 'name' not in add_state:
        abort(400, "Missing Name")
    else:
        new_state = State(**add_state)
        storage.new(new_state)
        storage.save()
        return jsonify(to_dict(new_state)), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates a state value of a given state id """
    ret_state = storage.get(State, state_id)
    if ret_state is None:
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
    return jsonify(to_dict(ret_state)), 200
