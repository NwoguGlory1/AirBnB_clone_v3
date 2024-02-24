#!/usr/bin/python3

""" module returns a JSON structure """
from flask import jsonify
from . import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ returns JSON status """
    return jsonify(status = "OK")
