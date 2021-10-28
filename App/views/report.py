from flask import Blueprint, redirect, request, jsonify, send_from_directory

reportViews = Blueprint('reportViews', __name__)

from App.models import *
from App.controllers import *

@reportViews.route('/api/reports', methods=["GET"])
def displayReport():
    displayData = getReportData()
    return displayData

@reportViews.route('/api/reports/standard', methods=["POST"])
@jwt_required()
def standardReport():
    reportDetails = request.get_json()
    outcomeMessage = reportPotholeStandard(current_user, reportDetails)
    return json.dumps(outcomeMessage)

@reportViews.route('/api/reports/driver', methods=["POST"])
@jwt_required()
def driverReport():
    reportDetails = request.get_json()
    outcomeMessage = reportPotholeDriver(current_user, reportDetails)
    return json.dumps(outcomeMessage)