#!/usr/bin/python3
"""Flask API App"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from os import getenv
from flask import jsonify

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """Close storage session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return a JSON-formatted 404 response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host=HOST, port=PORT, threaded=True)
