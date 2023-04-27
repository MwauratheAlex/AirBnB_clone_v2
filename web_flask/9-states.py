#!/usr/bin/python3
""" starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/states")
def states():
    """ renders states """
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    return render_template("9-states.html", states=states)


@app.route("/states/<id>")
def states_id(id):
    """ renders a state and its cities """
    state_id = "State.{}".format(id)
    state = [storage.all(State).get(state_id)]

    if state[0] is None:
        state = []

    return render_template("9-states.html", states=state)


@app.teardown_appcontext
def teardown(exception=None):
    """ Closes the session """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
