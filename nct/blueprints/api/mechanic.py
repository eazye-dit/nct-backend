from nct import db
from nct.blueprints.api import api
from nct.models import Appointment, Account, Step, Failure, TestResult
from nct.utils import get_car, mechanic_required, format_appointment, verify_test
from flask_login import current_user
from flask import jsonify, make_response, request, abort
from datetime import datetime, timedelta

@api.route('/mechanic/appointments/')
@mechanic_required
def mechanic_appointments():
    # Get appointments up to 5 days ahead
    appointments = Appointment.query.filter_by(assigned=current_user.id).filter((Appointment.date < datetime.now() + timedelta(days=5)) & Appointment.is_deleted == False).order_by(Appointment.date.asc())
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

@api.route('/mechanic/test/<appointment>/', methods=["GET", "POST"])
@mechanic_required
def test(appointment):
    appointment = Appointment.query.get(appointment)
    if appointment.assigned != current_user.id:
        abort(403)
    if appointment.is_tested:
        results = TestResult.query.filter_by(appointment=appointment.id).all()
        test_result = {
            "message": "Appointment is already completed",
            "test": {
                "id": appointment.id,
                "results": []
            }
        }
        for result in results:
            step = Step.query.filter_by(id=result.step).first()
            if result.failure:
                f = Failure.query.filter_by(id=result.failure).first()
                failure = {
                    "id": f.id,
                    "name": f.name,
                    "item": f.item
                }
            else:
                failure = None
            test_result["test"]["results"].append({
                "step": {
                    "id": step.id,
                    "name": step.name
                },
                "failure": failure,
                "comment": result.comment})
        return jsonify(test_result)
    if request.method == "POST":
        content = request.get_json(silent=True)
        if content and verify_test(content):
            test = content["test"]
            steps = [r["id"] for r in test["results"]]
            for step in Step.query.all():
                # First check if the test result contains all steps
                if not step.id in steps:
                    # If it encounters a missing step, then call it a bad request
                    abort(400)
            for result in test["results"]:
                if result["checked_id"] == None:
                    pass
                elif not Failure.query.filter_by(step=result["id"], id=result["checked_id"]).first():
                    # if the checked failure is not a valid id in the database, raise Bad request
                    abort(400)
                db_result = TestResult(appointment.id, result["id"], result["checked_id"], result["comment"])
                db.session.add(db_result)
            appointment.is_tested = True
            db.session.commit()
            return jsonify({
                "status": 200,
                "message": "Success",
                "test": test,
            })
        else:
            abort(400)
    steps = []
    for step in Step.query.all():
        failures = []
        for failure in Failure.query.filter_by(step=step.id).all():
            failures.append({
                "id": failure.id,
                "item": failure.item,
                "name": failure.name
            })
        steps.append({
            "id": step.id,
            "name": step.name,
            "description": step.description,
            "notes": step.notes,
            "failures": failures
        })
    return jsonify({
        "status": 200,
        "message": "Success",
        "steps": steps,
        "appointment": format_appointment(appointment)
    })
