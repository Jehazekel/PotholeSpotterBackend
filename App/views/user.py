from flask import Blueprint, redirect, request, jsonify, send_from_directory

userViews = Blueprint('userViews', __name__)

from App.models import *
from App.controllers import *


@userViews.route('/register', methods=["POST"])
def registerUserView():
    regData = request.get_json()
    outcomeMessage, statusCode = registerUserController(regData)
    return json.dumps(outcomeMessage), statusCode

@userViews.route('/login', methods=["POST"])
def loginUserView():
    loginDetails = request.get_json()
    outcomeMessage, statusCode = loginUserController(loginDetails)
    return json.dumps(outcomeMessage), statusCode

@userViews.route("/identify", methods=["GET"])
@jwt_required()
def identify():
    outcomeMessage, statusCode = identifyUser(current_user)
    return json.dumps(outcomeMessage), statusCode

@userViews.route("/", methods=["GET"])
def test():
    return json.dumps({"message": "Flask app is deployed!"}), 200