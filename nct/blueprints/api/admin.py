from nct.blueprints.api import api
from nct import db
from nct.models import *
from nct.utils import get_roles, get_car, admin_required, format_appointment, verify_appointment, verify_registration
from flask_login import login_required, current_user
from flask import jsonify, make_response, request, abort, redirect, url_for
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
                (Appointment.is_deleted == False) &
                (Appointment.date < d + timedelta(days=ahead))).order_by(Appointment.date.asc()
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

@api.route('/admin/appointment/<id>/', methods=["GET", "POST", "DELETE"])
@admin_required
def admin_appointment(id):
    appointment = Appointment.query.get(id)
    msg = "Success"
    if appointment == None:
        abort(404)
    if request.method == "POST":
        content = request.get_json()
        if not verify_appointment(content):
            abort(400)
        if not content["vehicle"] == appointment.registration:
            abort(403)
        appointment.date = datetime.strptime(content["date"], "%Y-%m-%d %H:%M")
        appointment.assigned = content["assigned"]
        db.session.commit()
    elif request.method == "DELETE":
        appointment.is_deleted = True
        db.session.commit()
        msg = "Deleted"
    return jsonify({
        "status": 200,
        "message": msg,
        "appointment": format_appointment(appointment)
    })

@api.route('/admin/mechanics/')
@admin_required
def mechanics():
    mechs = []
    mechanic_role = Role.query.filter_by(name="Mechanic").first()
    for user in Account.query.all():
        if AccountRole.query.filter_by(u_id=user.id, r_id=mechanic_role.id).first():
            mechs.append({
                "username": user.username,
                "first": user.f_name,
                "last": user.l_name,
                "id": user.id
            })
    return jsonify({
        "status": 200,
        "message": "Success",
        "mechanics": mechs
    })

@api.route('/admin/mechanic/<id>', methods=["GET", "DELETE"])
@admin_required
def get_mechanic(id):
    role = Role.query.filter_by(name="Mechanic").first()
    account = Account.query.get(id)
    if not account:
        abort(404)
    if not AccountRole.query.filter_by(u_id=account.id, r_id=role.id).first():
        return make_response(jsonify({
            "status": 202,
            "message": "The requested account exists, but is not a mechanic"
        }), 202)
    if request.method == "DELETE":
        account.is_deleted = True
        db.session.commit()
        return jsonify({
            "status": 200,
            "message": "Mechanic deleted"
        })
    return jsonify({
        "status": 200,
        "message": "Success",
        "mechanic": {
            "username": account.username,
            "first": account.f_name,
            "last": account.l_name,
            "id": account.id
        }
    })

@api.route('/admin/new/appointment/', methods=["POST"])
@admin_required
def new_appointment():
    content = request.get_json()
    if not verify_appointment(content):
        abort(400)
    appointment = Appointment(content["vehicle"], content["assigned"], content["date"])
    db.session.add(appointment)
    db.session.commit()
    return redirect(url_for('api.admin_appointment', id=appointment.id))

@api.route('/admin/new/mechanic/', methods=["POST"])
@admin_required
def new_mechanic():
    content = request.get_json()
    role = Role.query.filter_by(name="Mechanic").first()
    if not verify_registration(content):
        abort(400)
    if Account.query.filter_by(username=content["username"]).first():
        abort(400)
    account = Account(content["username"], content["password"], content["f_name"], content["l_name"])
    db.session.add(account)
    db.session.commit()
    accountrole = AccountRole(account.id, role.id)
    db.session.add(accountrole)
    db.session.commit()
    return redirect(url_for('api.get_mechanic', id=account.id))

