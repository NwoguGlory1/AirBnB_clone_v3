#!/usr/bin/python3
""" State view object that handles all default RESTFul API actions """

import json
from flask import Flask, make_response, jsonify
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
    all_states = storage.all(State)
    for state in all_states.values():
        if state.id == state_id:
            return jsonify(to_dict(state))
    return jsonify({"error": "Not found"}), 404 
