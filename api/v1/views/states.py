#!/usr/bin/python3
"""
View module for handling State objects in API v1.
Provides RESTful API actions for State objects, including retrieving,
creating, updating, and deleting states.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a specific State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False
)
def delete_state(state_id):
    """Deletes a specific State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
