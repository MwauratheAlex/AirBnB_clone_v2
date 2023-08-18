#!/usr/bin/python3
""" starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/hbnb_filters")
def hbnb_filters():
    """ display a HTML page """
    states = sorted(storage.all(State).values(), key=lambda state: state.name)
    amenities = sorted(storage.all(Amenity).values(), key=lambda a: a.name)
    return render_template(
            "10-hbnb_filters.html", states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(exception=None):
    """ closes the session """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
