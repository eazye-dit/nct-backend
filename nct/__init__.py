from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login

app = Flask(__name__) # Initialise app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://nct:totallysecret@localhost/nct'
app.secret_key = 'abcdefghijklmnopqrstuvwxyz'

db = SQLAlchemy(app)

login = flask_login.LoginManager()
login.init_app(app)

from nct import views # The different pages are defined in views.py
