from flask import Blueprint, redirect, request, jsonify, send_from_directory

userViews = Blueprint('userViews', __name__)

from App.models import *
from App.controllers import *


@userViews.route('/register', methods=["POST"])
def registerUserView():
    regData = request.get_json()
    outcomeMessage = registerUserController(regData)
    return json.dumps(outcomeMessage)

@userViews.route('/login', methods=["POST"])
def loginUserView():
    loginDetails = request.get_json()
    outcomeMessage = loginUserController(loginDetails)
    return json.dumps(outcomeMessage)

@userViews.route("/identify", methods=["GET"])
@jwt_required()
def identify():
    outcomeMessage = identifyUser(current_user)
    return json.dumps(outcomeMessage)

@userViews.route("/test", methods=["GET"])
def test():
    return json.dumps({"message": "website served"})