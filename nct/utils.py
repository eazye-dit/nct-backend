from nct.models import *
from flask import jsonify, make_response
import re
from functools import wraps
from flask_login import login_required, current_user

def endpoint(uri, desc, method="GET"):
    return {"uri": uri, "desc": desc, "method": method}

def bad_login():
    return make_response(jsonify({"status": 400, "message": "Login details incorrect"}), 401)

def get_roles(ident):
    # Get names of roles that the user has
    return [Role.query.get(x.r_id).name for x in AccountRole.query.filter_by(u_id = ident)]

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_func(*args, **kwargs):
        roles = get_roles(current_user.id)
        if not "Administrator" in roles:
            return make_response(
                jsonify({
                    "status": 401,
                    "message": "Unauthorized"
                }),
                401
            )
        return f(*args, **kwargs)
    return decorated_func

def mechanic_required(f):
    # TODO: Make mechanic/admin_required the same decorator with an argument to decide which is required
    @wraps(f)
    @login_required
    def decorated_func(*args, **kwargs):
        roles = get_roles(current_user.id)
        if not "Mechanic" in roles:
            return make_response(
                jsonify({
                    "status": 401,
                    "message": "Unauthorized"
                }),
                401
            )
        return f(*args, **kwargs)
    return decorated_func

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

def format_appointment(appointment):
    car = get_car(appointment.registration, True) # Get car information
    mechanic = Account.query.get(appointment.assigned) # And assigned mechanic information
    # And add it all to our response list
    return {
        "id": appointment.id,
        "vehicle": car,
        "assigned": {
            "username": mechanic.username,
            "first": mechanic.f_name,
            "last": mechanic.l_name
        },
        "date": appointment.date,
        "completed": appointment.is_tested,
        "is_deleted": appointment.is_deleted
    }

