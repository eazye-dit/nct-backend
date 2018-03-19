from nct.blueprints.api import api
from nct.models import Appointment, Account
from nct.utils import get_roles, get_car, admin_required, format_appointment
from flask_login import login_required, current_user
from flask import jsonify, make_response, request, abort
from datetime import datetime, timedelta
from functools import wraps

@api.route('/admin/appointments/')
@admin_required
def admin_appointments():
    # TODO: handle arguments according to documentation

    # Get appointments up to 5 days ahead
    appointments = Appointment.query.filter(Appointment.date < datetime.now() + timedelta(days=5))
    response = []
    for appointment in appointments:
        car = get_car(appointment.registration, True) # Get car information
        mechanic = Account.query.get(appointment.assigned) # And assigned mechanic information

        # And add it all to our response list
        response.append(format_appointment(appointment))

    return jsonify({
        "status": 200,
        "message": "Success",
        "appointments": response
    })

@api.route('/admin/appointment/<id>', methods=["GET", "POST", "DELETE"])
@admin_required
def admin_appointment(id):
    appointment = Appointment.query.get(id)
    if request.method == "POST":
        abort(501) # Not implemented
    elif request.method == "DELETE":
        abort(501)
    if not appointment:
        abort(404) # Not found
    else:
        return jsonify({
            "status": 200,
            "message": "Success",
            "appointment": format_appointment(appointment)
        })

@api.route('/admin/new/appointment', methods=["POST"])
@admin_required
def new_appointment():
    abort(501)

@api.route('/admin/new/mechanic', methods=["POST"])
@admin_required
def new_mechanic():
    abort(501)


