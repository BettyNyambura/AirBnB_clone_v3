#!/usr/bin/python3
"""
View module for handling Place objects in API v1.
Provides RESTful API actions for Place objects, including retrieving,
creating, updating, and deleting places.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a specific Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a specific Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")

    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a specific Place object by ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
