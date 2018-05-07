from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
import flask_login

app = Flask(__name__) # Initialise app

# these should be hidden away in a separate file, so for now i'm just using obvious
# and not secret.. secrets
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://nct:totallysecret@localhost/nct'
app.secret_key = 'abcdefghijklmnopqrstuvwxyz'

db = SQLAlchemy(app)

login = flask_login.LoginManager()
login.init_app(app)

from nct import errors, views # The different pages are defined in views.py


def create_app(db_uri):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.secret_key = "1234abcdef"

    db = SQLAlchemy(app)

    login = flask_login.LoginManager()
    login.init_app(app)

    from nct import views, errors

    return app
