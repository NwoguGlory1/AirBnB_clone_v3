#!/usr/bin/python3
""" Script that contains blueprint for the API """

from flask import Blueprint
""" imports Blueprint"""

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
""" blueprint for the API """

from api.v1.views.index import *
from api.v1.views.states import *
