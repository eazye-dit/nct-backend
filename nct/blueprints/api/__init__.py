from flask import Blueprint, jsonify, make_response, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from nct import db
from passlib.hash import pbkdf2_sha256
from nct.models import *
import re

api = Blueprint('api', __name__, url_prefix='/api') # All routes based on @api will have its
                                                    # base on the URI at /api/

def endpoint(uri, method="GET"):
    return {"uri": uri, "method": method}

@api.route('/')
def api_home():
    # The basic list of public endpoints
    endpoints = [
        endpoint("/api/"),
        endpoint("/api/login/", "POST"),
        endpoint("/api/vehicle/:regnumber/")
    ]

    if current_user.is_authenticated:
        endpoints.append("/api/logout/") # Both administrators and mechanics can log out

        roles = get_roles(current_user.id)

        if "Administrator" in roles:
            endpoints += [
                endpoint("/api/admin/appointments/"),
                endpoint("/api/admin/appointment/:id/"),
                endpoint("/api/admin/appointment/:id/", "POST"),
                endpoint("/api/admin/appointment/:id/", "DELETE"),
                endpoint("/api/admin/new/appointment/"),
                endpoint("/api/admin/new/mechanic/")
            ]

        if "Mechanic" in roles:
            endpoints += [
                endpoint("/api/mechanic/appointments/"),
                endpoint("/api/mechanic/test/:regnumber/"),
                endpoint("/api/mechanic/test/:regnumber/", "POST")
            ]

        # If a user for some reason is both a mechanic and an administrator,
        # all endpoints should be available to them.

    return jsonify({
        "status": 200,
        "available_endpoints": endpoints, # Return the final list of endpoints
        "docs": "https://github.com/eazye-dit/nct-backend/wiki/Endpoints"
    })


def bad_login():
    # Just to avoid writing this statement 3 times
    return make_response(jsonify({"status": 400, "message": "Login details incorrect"}), 400)


@api.route('/login/', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('api.api_home')) # Redirect home if we're already authenticated

    if not "password" in request.values and not "username" in request.values:
        # TODO: using request.values is kind of hacky and should be reconsidered
        # If password and username is not found in the request body, we'll say it's a bad login.
        return bad_login()

    user = Account.query.filter_by(username = request.values["username"]).first()

    if user == None:
        # If we can't find a user with that username, call bad login
        return bad_login()

    if pbkdf2_sha256.verify(request.values["password"], user.password): # Verify password!
        login_user(user)
        user.last_login = datetime.now() # Refresh last_login
        db.session.commit()
        return redirect(url_for('api.api_home'))
    else:
        # Call bad login if the password does not match.
        return bad_login()


@api.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('api.api_home'))


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

@api.route('/vehicle/<regnumber>') # Will be on /api/vehicle/<registration number here>
def lookup_car(regnumber): # regnumber in the URI will be passed to the function
    if not valid_registration(regnumber):
        return make_response(
            jsonify({
                "status": 400,
                "message": "{} is not a valid registration number".format(regnumber)
            }),
            400
        )
    car = get_car(regnumber, current_user.is_authenticated)
    if car:
        object = {
            "status": 200,
            "message": "Success",
            "vehicle": car
        }
    # We return a jsonified representation of the object we created above
    return make_response(jsonify(object), object["status"])

@api.route('/admin/appointments/')
@login_required
def admin_appointments():

    roles = get_roles(current_user.id)

    if not "Administrator" in roles:
        return make_response(
            jsonify({
                "status": 401,
                "message": "Unauthorized"
            }),
            401
        )

    # TODO: handle arguments according to documentation

    # Get appointments up to 5 days ahead
    appointments = Appointment.query.filter(Appointment.date < datetime.now() + timedelta(days=5))
    response = []
    for appointment in appointments:
        car = get_car(appointment.registration, True) # Get car information
        mechanic = Account.query.get(appointment.assigned) # And assigned mechanic information

        # And add it all to our response list
        response.append({
            "vehicle": car,
            "assigned": {
                "username": mechanic.username,
                "first": mechanic.f_name,
                "last": mechanic.l_name
            },
            "date": appointment.date,
            "completed": appointment.is_tested
        })

    return jsonify({
        "status": 200,
        "message": "Success",
        "appointments": response
    })
