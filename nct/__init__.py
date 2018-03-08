from flask import Flask

app = Flask(__name__) # Initialise app

from nct import views # The different pages are defined in views.py
