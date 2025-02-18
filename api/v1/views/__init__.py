#!/usr/bin/python3
"""View module for the API v1"""

from flask import Blueprint
from api.v1.views.index import *

# Creating an instance of Blueprint for API v1 views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
