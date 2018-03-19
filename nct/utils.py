from nct.models import *
from flask import jsonify, make_response
import re

def endpoint(uri, desc, method="GET"):
    return {"uri": uri, "desc": desc, "method": method}

def bad_login():
    return make_response(jsonify({"status": 400, "message": "Login details incorrect"}), 400)

def get_roles(ident):
    # Get names of roles that the user has
    return [Role.query.get(x.r_id).name for x in AccountRole.query.filter_by(u_id = ident)]

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

def get_car(reg, details):
    c = Vehicle.query.get(reg)
    if c != None:
        car = {
            "registration": c.registration,
            "make": c.make,
            "model": c.model,
            "year": c.year,
            "colour": c.colour
        }
        if details:
            # Give more info out if the user is authenticated.
            owner = Owner.query.get(c.owner)
            car["owner"] = {"first": owner.f_name.upper(), "last": owner.l_name.upper()}
            car["vin"] = c.vin
        return car
    else:
        return False
