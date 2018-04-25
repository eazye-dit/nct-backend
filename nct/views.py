from nct import app # Import the application from __init__
from nct.blueprints.api import api
from flask import render_template, redirect, url_for

app.register_blueprint(api) # Register the api blueprint from blueprints/api/

@app.route('/') # On the base address, return hello world
def hello():
    return redirect(url_for('api.api_home'))
