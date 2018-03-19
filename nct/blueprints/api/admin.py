from nct.blueprints.api import api
from nct.models import Appointment, Account
from nct.utils import get_roles, get_car
from flask_login import login_required, current_user
from flask import jsonify, make_response
from datetime import datetime, timedelta

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

