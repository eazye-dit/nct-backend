from nct import app # Import the application from __init__
from nct.blueprints.api import api

app.register_blueprint(api) # Register the api blueprint from blueprints/api/

@app.route('/') # On the base address, return hello world
def hello():
    return "hello world"
