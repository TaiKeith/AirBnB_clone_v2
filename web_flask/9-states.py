#!/usr/bin/python3
"""Start Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """A method that removes the current SQLAlchemy session"""
    storage.close()


@app.route("/states", strict_slashes=False)
def states():
    """Displays a HTML page with a list of all states"""
    states = storage.all(State)
    return render_template('9-states.html', state=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Displays a HTML page with a state object based on it's id"""
    for state in storage.all(State).values():
        if state.id == id:
            return render_template('9-states.html', state=state)
    return render_template('9-states.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
