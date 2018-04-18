from nct.blueprints.api import api
from nct.models import Appointment, Account
from nct.utils import get_car, mechanic_required, format_appointment
from flask_login import current_user
from flask import jsonify, make_response, request, abort
from datetime import datetime, timedelta

@api.route('/mechanic/appointments/')
@mechanic_required
def mechanic_appointments():
    # Get appointments up to 5 days ahead
    appointments = Appointment.query.filter_by(assigned=current_user.id).filter(Appointment.date < datetime.now() + timedelta(days=5)).order_by(Appointment.date.asc())
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

@api.route('/mechanic/test/<registration>', methods=["GET", "POST"])
@mechanic_required
def test(registration):
    if request.method == "POST":
        abort(501)
    abort(501)
