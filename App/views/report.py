from flask import Blueprint, redirect, request, jsonify, send_from_directory

reportViews = Blueprint('reportViews', __name__)

from App.models import *
from App.controllers import *

@reportViews.route('/api/reports', methods=["GET"])
def displayReports():
    displayData, statusCode = getReportData()
    return displayData, statusCode

@reportViews.route('/api/reports/pothole/<potholeID>', methods=["GET"])
def displayPotholeReports(potholeID):
    displayData, statusCode = getPotholeReports(potholeID)
    return displayData, statusCode

@reportViews.route('/api/reports/pothole/<potholeID>/report/<reportID>', methods=["GET"])
def displayIndividualPotholeReport(potholeID, reportID):
    displayData, statusCode = getIndividualPotholeReport(potholeID, reportID)
    return displayData, statusCode

@reportViews.route('/api/reports/standard', methods=["POST"])
@jwt_required()
def standardReport():
    reportDetails = request.get_json()
    outcomeMessage, statusCode = reportPotholeStandard(current_user, reportDetails)
    return json.dumps(outcomeMessage), statusCode

@reportViews.route('/api/reports/driver', methods=["POST"])
@jwt_required()
def driverReport():
    reportDetails = request.get_json()
    outcomeMessage, statusCode = reportPotholeDriver(current_user, reportDetails)
    return json.dumps(outcomeMessage), statusCode