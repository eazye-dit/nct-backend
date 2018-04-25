from nct import app
from flask import make_response, jsonify

@app.errorhandler(405)
def method_not_allowed(e):
    return make_response(
        jsonify({
            "status": 405,
            "message": "Method not allowed"
        }),
        405
    )

@app.errorhandler(404)
def not_found(e):
    return make_response(
        jsonify({
            "status": 404,
            "message": "Not found"
        }),
        404
    )

@app.login_manager.unauthorized_handler
def unauthorized_handler():
    return make_response(
        jsonify({
            "status": 401,
            "message": "Login required"
        }),
        401
    )

@app.errorhandler(501)
def not_implemented(e):
    return make_response(
        jsonify({
            "status": 501,
            "message": "Not implemented"
        }),
        501
    )

@app.errorhandler(403)
def forbidden_handler(e):
    return make_response(
        jsonify({
            "status": 403,
            "message": "Unauthoried"
        }),
        403
    )
