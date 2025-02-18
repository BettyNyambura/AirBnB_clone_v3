#!/usr/bin/python3
"""Flask API App"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from os import getenv

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Close storage session"""
    storage.close()


if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = int(getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
