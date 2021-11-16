from flask import Blueprint, redirect, request, jsonify, send_from_directory

userReportViews = Blueprint('userReportViews', __name__)

from App.models import *
from App.controllers import *



@userReportViews.route('/api/vote/pothole/<potholeID>/report/<reportID>/vote', methods=["POST"])
@jwt_required()
def voteOnReport(potholeID, reportID):
    voteData = request.get_json()
    outcomeMessage, statusCode = voteOnPothole(current_user, potholeID, reportID, voteData)
    return json.dumps(outcomeMessage), statusCode

