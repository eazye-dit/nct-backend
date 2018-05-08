from nct.blueprints.api import api
from nct import db
from nct.models import *
from nct.utils import *
from flask_login import login_required, current_user
from flask import jsonify, make_response, request, abort, redirect, url_for
from datetime import datetime, timedelta
from functools import wraps
from sqlalchemy import func

@api.route('/admin/appointments/')
@admin_required
def admin_appointments():
    date = request.args.get('date', default=None, type=str)
    ahead = request.args.get('ahead', default=5, type=int)
    mech = request.args.get('mechanic', default=None, type=int)
    completed = request.args.get('completed', default=False, type=bool)

    d = datetime.now()
    if date:
        try:
            d = datetime.strptime(date, '%Y-%m-%d')
        except:
            pass # Let d remain unchanged if the date input is wrongly formatted
    if completed:
        appointments = Appointment.query.filter(Appointment.is_tested != None).order_by(Appointment.date.desc())
    else:
        appointments = Appointment.query.filter(
                ((d <= Appointment.date) | (Appointment.is_tested == None)) &
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
        d = datetime.strptime(content["date"], "%Y-%m-%d %H:%M")
        if not is_available(content["assigned"], d, ignore=appointment.id):
            return make_response(jsonify({
                    "status": 202,
                    "message": "Mechanic is unavailable at that time"
                }), 202
            )
        appointment.date = d
        appointment.assigned = content["assigned"]
        db.session.commit()
    elif request.method == "DELETE":
        appointment.is_deleted = True
        db.session.commit()
        msg = "Deleted"
    if appointment.is_tested != None:
        return jsonify({
            "status": 200,
            "message": msg,
            "test": format_test(appointment.id),
            "appointment": format_appointment(appointment)
        })
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

@api.route('/admin/mechanic/<id>/', methods=["GET", "DELETE"])
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


@api.route('/admin/search/')
@admin_required
def search():
    owner = request.args.get('owner', default=None, type=str)
    if not owner:
        abort(400)

    owner_obj = Owner.query.filter(func.concat(Owner.f_name, ' ', Owner.l_name).like(owner)).first()
    if not owner_obj:
        return make_response(jsonify({
                "status": 404,
                "message": "Owner '{}' not found".format(owner)
            }), 404
        )

    vehicles = Vehicle.query.filter_by(owner=owner_obj.id)

    vehicle_list = []

    for vehicle in vehicles:
        vehicle_list.append({
            "registration": vehicle.registration,
            "make": vehicle.make,
            "model": vehicle.model,
            "year": vehicle.year,
            "colour": vehicle.colour,
            "vin": vehicle.vin
        })

    return jsonify({
        "status": 200,
        "message": "Success",
        "owner": {
            "id": owner_obj.id,
            "f_name": owner_obj.f_name,
            "l_name": owner_obj.l_name,
            "vehicles": vehicle_list,
            "phone": owner_obj.phone
        }
    })

@api.route('/admin/new/appointment/', methods=["POST"])
@admin_required
def new_appointment():
    content = request.get_json()
    if not verify_appointment(content):
        abort(400)

    d = datetime.strptime(content["date"], "%Y-%m-%d %H:%M")
    if not is_available(content["assigned"], d, ignore=appointment.id):
        return make_response(
            jsonify({
                "status": 202,
                "message": "Mechanic is unavailable at that time"
            }), 202
        )
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


@api.route('/admin/new/vehicle/', methods=["POST"])
@admin_required
def new_vehicle():
    content = request.get_json()
    if not verify_vehicle(content):
        abort(400)
    if not Owner.query.get(content["owner"]):
        abort(404)
    vehicle = Vehicle(content["registration"], content["make"], content["model"], content["year"], content["vin"], content["owner"], content["colour"])
    db.session.add(vehicle)
    db.session.commit()
    return redirect(url_for('api.lookup_car', regnumber=vehicle.registration))

@api.route('/admin/new/owner/', methods=["POST"])
@admin_required
def new_owner():
    content = request.get_json()
    fields = ["f_name", "l_name", "phone"]
    for field in fields:
        if field not in content:
            abort(400)
    owner = Owner(content["f_name"], content["l_name"], content["phone"])
    db.session.add(owner)
    db.session.commit()
    return redirect(url_for('api.lookup_owner', id=owner.id))

@api.route('/admin/owner/<id>/')
@admin_required
def lookup_owner(id):
    owner = Owner.query.get(id)
    if not owner:
        abort(404)
    o = {"f_name": owner.f_name, "l_name": owner.l_name, "id": owner.id}
    if owner.phone:
        o["phone"] = owner.phone
    return jsonify({
        "status": 200,
        "message": "Success",
        "owner": o
    })
