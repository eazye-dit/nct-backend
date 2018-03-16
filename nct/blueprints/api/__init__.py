from flask import Blueprint, jsonify, make_response
from datetime import datetime
import re

api = Blueprint('api', __name__, url_prefix='/api') # All routes based on @api will have its
                                                    # base on the URI at /api/

@api.route('/')
def api_home():
    return jsonify({
        "status": 200,
        "available_endpoints": [ # This should be programmatically generated somehow, later on
            "/api/",
            "/api/login/",
            "/api/vehicle/:regnumber/"
        ]
    })

@api.route('/login/') # TODO: This thing
def login():
    return jsonify({
        "status": 200,
        "message": "Login has not been implemented yet"
    })

def valid_registration(reg):
    """A simple function to check validity of registration numbers"""
    try:
        # We always expect the first two digits in `reg` to be digits
        year = int(reg[:2])
    except ValueError:
        # If it's not a digit, we'll say it's not valid
        return False
    if year > 12:
        # If the year is 13 or higher, there is a third digit
        # (either 1 or 2 for registration before or after summer) after the year number.
        pattern = "^(\d{2})([12])([A-Za-z]{1,2})(\d{1,6})$"
    else:
        pattern = "^(\d{2})([A-Za-z]{1,2})(\d{1,6})$"
    prog = re.compile(pattern)
    # `match()` will return None if there's no match.
    # This will effectively be the same as False when we check `if not valid_registration()`
    return prog.match(reg)

@api.route('/vehicle/<regnumber>') # Will be on /api/vehicle/<registration number here>
def lookup_car(regnumber): # regnumber in the URI will be passed to the function
    # some database lookup here
    if not valid_registration(regnumber):
        return make_response(
            jsonify({
                "status": 400,
                "message": "{} is not a valid registration number".format(regnumber)
            }),
            400
        )
    car = {
        "status": 200,
        "message": "Success",
        "vehicle": {
            "registration": regnumber,
            "make": "FORD",
            "model": "FIESTA",
            "year": 2012,
            "colour": "WHITE"
        }
    }
    return jsonify(car) # We return a jsonified representation of the object we created above

