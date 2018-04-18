from nct import app # Import the application from __init__
from nct.blueprints.api import api
from flask import render_template

app.register_blueprint(api) # Register the api blueprint from blueprints/api/

@app.route('/') # On the base address, return hello world
def hello():
    return render_template('login.tpl')
