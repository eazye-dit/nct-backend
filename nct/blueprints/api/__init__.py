from flask import Blueprint, jsonify
from datetime import datetime

api = Blueprint('api', __name__, url_prefix='/api') # All routes based on @api will have its
                                                    # base on the URI at /api/

@api.route('/car/<reg>') # Will be on /api/car/<registration number here>
def lookup_car(reg): # reg in the URI will be passed to the function
    # some database lookup here
    car = {
        "registration": reg,
        "last_test": datetime.now(), # Let's just say the last test was right now
        "make": "Ford",
        "model": "Fiesta",
        "year": 2012
    }
    return jsonify(car) # We return a jsonified representation of the object we created above

