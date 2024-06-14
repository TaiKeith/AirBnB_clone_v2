#!/usr/bin/python3
"""Start Flask web application"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Routing to root, strict_slashes ensure
    the URL works whether it ends with or without the /
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Routing to /hbnb, strict_slashes ensure
    the URL works whether it ends with or without the /
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """Routing to /c/ using variables"""
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route('/python/', defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_fun(text):
    """Routing to /python/ using variables"""
    text = text.replace('_', ' ')
    return "python {}".format(text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
