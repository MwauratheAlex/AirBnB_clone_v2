#!/usr/bin/python3
""" starts a Flask web application """
import os
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/cities_by_states")
def cities_by_states():
    """ display a HTML page """
    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown(exception=None):
    """ close the session """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
