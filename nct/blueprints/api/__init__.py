from flask import Blueprint, jsonify, make_response, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from nct import db
from passlib.hash import pbkdf2_sha256
from nct.models import *
from nct.utils import *
from nct.blueprints.api import endpoints as e
from datetime import datetime

api = Blueprint('api', __name__, url_prefix='/api') # All routes based on @api will have its
                                                    # base on the URI at /api/

from nct.blueprints.api import admin, mechanic # Load admin and mechanic endpoints

@api.route('/')
def api_home():
    method = request.args.get('method', default=None, type=str)
    # The basic list of public endpoints
    endpoints = e.public

    if current_user.is_authenticated:
        # Both administrators and mechanics can log out
        endpoints = endpoints + [endpoint("/api/logout/", "Logs the user out")]

        roles = get_roles(current_user.id)

        if "Administrator" in roles:
            endpoints = endpoints + e.admin

        if "Mechanic" in roles:
            endpoints = endpoints + e.mechanic

        # If a user for some reason is both a mechanic and an administrator,
        # all endpoints should be available to them.

    if method is not None and method.upper() in ["GET", "POST", "DELETE"]:
        endpoints = [x for x in endpoints if x["method"] == method.upper()]
    return jsonify({
        "status": 200,
        "available_endpoints": endpoints, # Return the final list of endpoints
        "docs": "https://github.com/eazye-dit/nct-backend/wiki/Endpoints"
    })


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

