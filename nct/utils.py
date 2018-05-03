from nct.models import *
from flask import jsonify, abort, make_response
import re
from functools import wraps
from flask_login import login_required, current_user
from datetime import datetime

def endpoint(uri, desc, method="GET"):
    return {"uri": uri, "desc": desc, "method": method}

def bad_login():
    return make_response(jsonify({"status": 401, "message": "Login details incorrect"}), 401)

def get_roles(ident):
    # Get names of roles that the user has
    return [Role.query.get(x.r_id).name for x in AccountRole.query.filter_by(u_id = ident)]

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_func(*args, **kwargs):
        roles = get_roles(current_user.id)
        if not "Administrator" in roles or current_user.is_deleted:
            abort(401)
        return f(*args, **kwargs)
    return decorated_func

def mechanic_required(f):
    # TODO: Make mechanic/admin_required the same decorator with an argument to decide which is required
    @wraps(f)
    @login_required
    def decorated_func(*args, **kwargs):
        roles = get_roles(current_user.id)
        if not "Mechanic" in roles or current_user.is_deleted:
            abort(401)
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

def verify_test(content):
    if not "test" in content:
        return False
    test = content["test"]
    if not "id" in test or not "results" in test:
        return False
    if len(test["results"]) == 0:
        return False
    for result in test["results"]:
        if not "id" in result:
            return False
        if not "checked_id" in result:
            return False
        if not "comment" in result:
            return False
    return True

def format_test(appointment):
    test = {
        "id": appointment,
        "results": []
    }
    results = TestResult.query.filter_by(appointment=appointment).all()
    testfails = TestResultFailure.query.filter_by(appointment=appointment).all()
    fails = []
    for testfail in testfails:
        fails.append(Failure.query.get(testfail.failure))

    for result in results:
        step = Step.query.get(result.step)
        resultfail = [{"id": x.id, "item": x.item, "name": x.name} for x in fails if x.step == result.step]
        test["results"].append({
            "comment": result.comment,
            "step": {
                "id": step.id,
                "name": step.name
            },
            "failures": resultfail
        })
    return test

def verify_appointment(content):
    fields = ["date", "assigned", "vehicle"]
    for field in fields:
        if not field in content:
            return False
    try:
        datetime.strptime(content["date"], "%Y-%m-%d %H:%M")
    except:
        return False
    account = Account.query.get(content["assigned"])
    if not account:
        return False
    role = Role.query.filter_by(name="Mechanic").first()
    if not AccountRole.query.filter_by(u_id=account.id, r_id=role.id).first():
        return False
    if not Vehicle.query.get(content["vehicle"]):
        return False
    return True

def verify_registration(content):
    fields = ["username", "password", "f_name", "l_name"]
    for field in fields:
        if not field in content:
            return False
    return True

def verify_vehicle(content):
    fields = ["registration", "make", "model", "year", "vin", "colour", "owner"]
    for field in fields:
        if not fields in content:
            return False
    if not valid_registration(content["registration"]):
        return False
    return True

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

