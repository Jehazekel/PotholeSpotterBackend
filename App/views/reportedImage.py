from flask import Blueprint, redirect, request, jsonify, send_from_directory

reportedImageViews = Blueprint('reportedImageViews', __name__)

from App.models import *
from App.controllers import *


@reportedImageViews.route('/api/reports/pothole/<potholeID>/report/<reportID>/images/<imageID>', methods=["GET"])
def getIndividualReportedImage(potholeID, reportID, imageID):
    displayData, statusCode = getIndividualPotholeReportImage(reportID, imageID)
    return displayData, statusCode

@reportedImageViews.route('/api/reports/pothole/<potholeID>/report/<reportID>/images', methods=["GET"])
def getReportImages(potholeID, reportID):
    displayData, statusCode = getPotholeReportImages(reportID)
    return displayData, statusCode

#DELETE
@reportedImageViews.route('/api/reports/pothole/<potholeID>/report/<reportID>/images/<imageID>', methods=["DELETE"])
@jwt_required()
def deletePotholeImage(potholeID, reportID, imageID):
    displayData, statusCode = deletePotholeReportImage(current_user, potholeID, reportID, imageID)
    return displayData, statusCode


#ADD
@reportedImageViews.route('/api/reports/pothole/<potholeID>/report/<reportID>/images', methods=["POST"])
@jwt_required()
def addPotholeImage(potholeID, reportID):
    imageDetails = request.get_json()
    displayData, statusCode = addPotholeReportImage(current_user, potholeID, reportID, imageDetails)
    return displayData, statusCode