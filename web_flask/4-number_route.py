#!/usr/bin/python3
""" starts a Flask web application """
from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def index():
    """ Returns Hello HBNB! """
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    """ Returns HBNB """
    return "HBNB"


@app.route("/c/<text>")
def c(text):
    """ Returns C + <text> """
    return "C {}".format(text.replace("_", " "))


@app.route("/python/", defaults={"text": "is cool"})
@app.route("/python/<text>")
def py(text):
    """ Returns Python + <text> """
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>")
def number(n):
    """ Returns <n> is a number """
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
