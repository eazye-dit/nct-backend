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
    date = request.args.get('date', default=None, type=str)
    ahead = request.args.get('ahead', default=5, type=int)
    mech = request.args.get('mechanic', default=None, type=int)

    d = datetime.now()
    if date:
        try:
            d = datetime.strptime(date, '%Y-%m-%d')
        except:
            pass # Let d remain unchanged if the date input is wrongly formatted

    appointments = Appointment.query.filter(
                ((d <= Appointment.date) | (Appointment.is_tested == False)) &
                (Appointment.date < d + timedelta(days=ahead))
    ) # A bit of an ugly boolean, but basically: Return the appointments
    # whose appointment dates have not passed (unless the car has not yet been
    # tested), and whose appointment dates are within the range of the number of days
    # to look ahead.
    response = []
    for appointment in appointments:
        car = get_car(appointment.registration, True) # Get car information
        mechanic = Account.query.get(appointment.assigned) # And assigned mechanic information
        if mech:
            if mechanic.id == mech:
                response.append(format_appointment(appointment))
        else:
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


