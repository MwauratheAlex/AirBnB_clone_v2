#!/usr/bin/python3
""" starts a Flask web application """
from flask import Flask
from flask import render_template
from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/states_list")
def states_list():
    """ display a HTML page """
    states = storage.all(State).values()
    return render_template("7-states_list.html", states=states)

@app.teardown_appcontext
def teardown(exception=None):
    """ removes the current SQLAlchemy Session """
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
